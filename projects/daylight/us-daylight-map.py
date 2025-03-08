import time
import math

# import datetime
import argparse
from typing import List, Tuple
from datetime import datetime, timezone

from colorstrings import grey_str

# ASCII map of the United States
US_MAP = [
    "                                                      _   ",
    "  \\_________________________                         / \\  ",
    " _|    ||         |      |  ---- _  _           ____(  _) ",
    " |     |(         |      |    /_/ \\// _        / | || /   ",
    " |_____| \\        |------|   /  --\\/ / \\    __/  | /|(    ",
    " |     |  \\_------|      |   \\_   | (  (   /     |/_|/    ",
    " |     |    |     |______|_____\\ _| |   \\_/ ___ _|_|/     ",
    " (_____|____|     |       \\     \\ \\_)------/   ) )        ",
    " |   |    | |_____|__      )____/  |  |    |___)/         ",
    " (   |    |    |     |_____|    \\  |  /---/\\__  \\         ",
    " )   |    |    |     |      \\    \\ )_/    \\ / \\_/         ",
    " \\   \\    |    |     |       |    ||______//____|         ",
    "  |   \\   |____|_____|_______|----|       /      \\        ",
    "  )    \\  /    |    |___     |    /______/_____  /        ",
    "  \\     \\|     |    |  |     |   |   |   / \\   \\/         ",
    "   \\     \\     |    |  |__   |---/   |   \\  \\  /          ",
    "    \\_   /     |    |     ---)   )   |   |   \\/           ",
    "      \\__\\_____|_----        \\   |-|_|_---___/            ",
    "                  \\           )__  |   \\/\\_  \\            ",
    "                   \\_/\\      /   --        )  \\           ",
    "                       \\    /              \\  (           ",
    "                        \\  (                |  |          ",
    "                         \\__\\                \\_|          ",
]


# Define latitude and longitude ranges for the map
# The US mainland roughly spans from about 24°N to 49°N latitude and 66°W to 125°W longitude
LAT_MIN, LAT_MAX = 24.7, 47.5
LON_MIN, LON_MAX = -125, -66


def calculate_sun_position(date_time: datetime) -> Tuple[float, float]:
    """
    Calculate the position of the sun (declination and hour angle).

    Args:
        date_time: Current date and time

    Returns:
        Tuple of (declination, hour_angle) in radians
    """
    # Convert to UTC
    utc_time = date_time.replace(tzinfo=timezone.utc)

    # Calculate day of year
    day_of_year = utc_time.timetuple().tm_yday

    # Calculate the declination of the sun (in radians)
    # This approximation is reasonably accurate
    declination = math.radians(
        23.45 * math.sin(math.radians((360 / 365) * (day_of_year - 81)))
    )

    # Calculate the hour angle of the sun (in radians)
    hour = utc_time.hour + utc_time.minute / 60 + utc_time.second / 3600
    hour_angle = math.radians(15 * (hour - 12))

    return declination, hour_angle


def is_daytime(lat: float, lng: float, declination: float, hour_angle: float) -> bool:
    """
    Determine if a location is in daytime.

    Args:
        lat: Latitude of the location (degrees)
        lng: Longitude of the location (degrees)
        declination: Sun's declination (radians)
        hour_angle: Sun's hour angle (radians)

    Returns:
        True if the location is in daytime, False otherwise
    """
    # Convert latitude to radians
    lat_rad = math.radians(lat)

    # Adjust hour angle for longitude
    # At longitude 0, the hour angle is as calculated
    # For each degree east, the hour angle increases by 1/15 hours (or 4 minutes)
    adjusted_hour_angle = hour_angle + math.radians(lng)

    # Calculate the sun's elevation angle
    elevation = math.asin(
        math.sin(declination) * math.sin(lat_rad)
        + math.cos(declination) * math.cos(lat_rad) * math.cos(adjusted_hour_angle)
    )

    # The sun is above the horizon if the elevation angle is positive
    return elevation > 0


def alt_is_daytime(lat, lng):
    """
    Returns True if it is currently daylight at the given latitude and longitude.
    The calculation is done in UTC.

    Parameters:
      lat (float): Latitude in degrees.
      lng (float): Longitude in degrees (positive east of Greenwich).

    Returns:
      bool: True if the current UTC time is between sunrise and sunset.
    """
    # Constants
    zenith = math.radians(
        90.833
    )  # official zenith for sunrise/sunset (includes refraction)

    # Get current UTC date and time
    now_utc = datetime.now(timezone.utc)
    # Get the day of the year
    n = now_utc.timetuple().tm_yday

    # Convert latitude to radians for calculation
    lat_rad = math.radians(lat)

    # Approximate fractional year (in radians)
    # Using an approximation for solar calculations: gamma = 2π/365 * (N - 1 + (hour - 12)/24)
    gamma = 2 * math.pi / 365 * (n - 1 + (now_utc.hour - 12) / 24.0)

    # Equation of time in minutes (approximation)
    eq_time = 229.18 * (
        0.000075
        + 0.001868 * math.cos(gamma)
        - 0.032077 * math.sin(gamma)
        - 0.014615 * math.cos(2 * gamma)
        - 0.040849 * math.sin(2 * gamma)
    )

    # Solar declination in radians (approximation)
    decl = (
        0.006918
        - 0.399912 * math.cos(gamma)
        + 0.070257 * math.sin(gamma)
        - 0.006758 * math.cos(2 * gamma)
        + 0.000907 * math.sin(2 * gamma)
        - 0.002697 * math.cos(3 * gamma)
        + 0.00148 * math.sin(3 * gamma)
    )

    # Calculate the hour angle for sunrise/sunset
    # cos(omega) = (cos(zenith) - sin(lat) * sin(decl)) / (cos(lat) * cos(decl))
    cos_omega = (math.cos(zenith) - math.sin(lat_rad) * math.sin(decl)) / (
        math.cos(lat_rad) * math.cos(decl)
    )

    # Check for polar conditions:
    if cos_omega > 1:
        # Sun never rises on this location (polar night)
        return False
    elif cos_omega < -1:
        # Sun never sets (midnight sun)
        return True

    # Hour angle in degrees
    omega = math.degrees(math.acos(cos_omega))

    # Calculate solar noon (in minutes) in UTC:
    # The equation below gives the time offset (in minutes) from UTC noon
    solar_noon_offset = lng * 4 - eq_time
    # Solar noon in UTC (in minutes from midnight)
    solar_noon = 720 - solar_noon_offset  # 720 minutes = 12:00 UTC

    # Sunrise and sunset times in minutes from midnight UTC
    sunrise_minutes = solar_noon - (omega * 4)
    sunset_minutes = solar_noon + (omega * 4)

    # Convert current time to minutes from midnight UTC
    current_minutes = now_utc.hour * 60 + now_utc.minute + now_utc.second / 60.0

    # Check if current time is between sunrise and sunset
    return sunrise_minutes <= current_minutes <= sunset_minutes


def render_map(declination: float, hour_angle: float) -> List[str]:
    """
    Render the US map with the current daylight terminator.

    Args:
        declination: Sun's declination (radians)
        hour_angle: Sun's hour angle (radians)

    Returns:
        ASCII map of the US with the terminator rendered
    """
    # Create a copy of the map that we can modify
    rendered_map = []

    # For each position in the map
    for y, row in enumerate(US_MAP):
        new_row = list(row)
        for x, char in enumerate(row):
            if char not in [" ", "\n"]:
                # Get the approximate latitude and longitude for this position
                # Linear mapping from the map to US coordinates
                lat = LAT_MAX - (y / len(US_MAP)) * (LAT_MAX - LAT_MIN)
                lng = LON_MIN + (x / len(row)) * (LON_MAX - LON_MIN)
                # print(f"lat={lat} lng={lng} day={alt_is_daytime(lat, lng)}")

                # Check if this position is in daytime
                # if is_daytime(lat, lng, declination, hour_angle):
                if alt_is_daytime(lat, lng):
                    # Daytime - use original character
                    pass
                else:
                    # Nighttime - darken the character
                    # if char == "-":
                    #    new_row[x] = "="
                    # elif char == "/":
                    #    new_row[x] = "\\"
                    # elif char == "\\":
                    #    new_row[x] = "/"
                    # elif char == "_":
                    #    new_row[x] = "‾"
                    # elif char == "|":
                    #    new_row[x] = ":"
                    # else:
                    #    new_row[x] = "*"
                    new_row[x] = grey_str(char)

        rendered_map.append("".join(new_row))

    return rendered_map


def display_map(rendered_map: List[str]) -> None:
    """
    Display the rendered map in the terminal.

    Args:
        rendered_map: ASCII map to display
    """
    # Clear the terminal (platform-independent)
    print("\033c", end="", flush=True)

    # Display the current time
    now = datetime.now()
    print(f"US Daylight Map - {now.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
    print(flush=True)

    # Display the map
    for row in rendered_map:
        print(row, flush=True)

    print(flush=True)
    print("Legend: Day (normal ASCII), Night (modified ASCII)", flush=True)
    print("Press Ctrl+C to exit", flush=True)


def main() -> None:
    """Main function to run the US daylight map."""
    parser = argparse.ArgumentParser(
        description="Display an ASCII map of the US with the current daylight terminator."
    )
    parser.add_argument(
        "-i",
        "--interval",
        type=int,
        default=5,
        help="Update interval in minutes (default: 5)",
    )
    args = parser.parse_args()

    try:
        while True:
            now = datetime.now()
            declination, hour_angle = calculate_sun_position(now)
            rendered_map = render_map(declination, hour_angle)
            display_map(rendered_map)

            # Wait for the specified interval
            time.sleep(args.interval * 60)
    except KeyboardInterrupt:
        print("\nExiting...", flush=True)


if __name__ == "__main__":
    main()
