#!/usr/bin/env python3
"""
Weather module for terminal grid screensaver
Gets real weather data using IP geolocation and Open-Meteo API
"""

import random
import requests
import json
from typing import List
from cachetools.func import ttl_cache

# Cache the weather data for 15 minutes (900 seconds)
@ttl_cache(maxsize=10, ttl=15 * 60)
def get_weather() -> List[str]:
    """Get real weather information using IP geolocation and Open-Meteo API"""
    output = ["Weather:"]

    try:
        # First, get location from IP address
        ip_response = requests.get("https://ipinfo.io/json", timeout=5)
        ip_data = ip_response.json()

        # Extract city and country
        city = ip_data.get("city", "Unknown")
        country = ip_data.get("country", "")
        location = f"{city}, {country}" if country else city

        # Extract coordinates for weather API
        coords = ip_data.get("loc", "").split(",")
        if len(coords) != 2:
            output.append(f"Location: {location}")
            output.append("Weather data unavailable - could not determine coordinates")
            return output

        lat, lon = coords

        # Use Open-Meteo API - completely free with no API key required
        # Documentation: https://open-meteo.com/en/docs
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&current=temperature,apparent_temperature,precipitation,weather_code,wind_speed_10m"
            f"&temperature_unit=fahrenheit"
            f"&wind_speed_unit=mph"
            f"&timezone=auto"
        )

        weather_response = requests.get(weather_url, timeout=5)
        weather_data = weather_response.json()

        # Extract weather information from the response
        if "current" in weather_data:
            current = weather_data["current"]

            # Map weather code to readable condition
            # Based on WMO Weather interpretation codes (WW)
            # See: https://open-meteo.com/en/docs
            weather_codes = {
                0: "Clear sky",
                1: "Mainly clear",
                2: "Partly cloudy",
                3: "Overcast",
                45: "Fog",
                48: "Depositing rime fog",
                51: "Light drizzle",
                53: "Moderate drizzle",
                55: "Dense drizzle",
                56: "Light freezing drizzle",
                57: "Dense freezing drizzle",
                61: "Slight rain",
                63: "Moderate rain",
                65: "Heavy rain",
                66: "Light freezing rain",
                67: "Heavy freezing rain",
                71: "Slight snow fall",
                73: "Moderate snow fall",
                75: "Heavy snow fall",
                77: "Snow grains",
                80: "Slight rain showers",
                81: "Moderate rain showers",
                82: "Violent rain showers",
                85: "Slight snow showers",
                86: "Heavy snow showers",
                95: "Thunderstorm",
                96: "Thunderstorm with slight hail",
                99: "Thunderstorm with heavy hail",
            }

            weather_code = current.get("weather_code", 0)
            weather_desc = weather_codes.get(weather_code, "Unknown")

            temp = current.get("temperature", "N/A")
            feels_like = current.get("apparent_temperature", "N/A")
            precipitation = current.get("precipitation", "N/A")
            wind_speed = current.get("wind_speed_10m", "N/A")

            # Define field names and values for even alignment
            fields = [
                ("Location", location),
                ("Condition", weather_desc),
                ("Temperature", f"{temp:.1f}°F (feels like {feels_like:.1f}°F)"),
                ("Precipitation", f"{precipitation} mm"),
                ("Wind", f"{wind_speed} mph"),
            ]

            # Find the maximum field name length for alignment
            max_field_length = max(len(field[0]) for field in fields)

            # Format output with HTML-compatible spacing
            for field_name, field_value in fields:
                padded_name = field_name + "&nbsp;" * (
                    max_field_length - len(field_name)
                )
                output.append(f"{padded_name}: {field_value}")
        else:
            output.append(f"Location: {location}")
            output.append(
                f"Weather data unavailable - API error: {json.dumps(weather_data.get('reason', 'Unknown error'))}"
            )

    except Exception as e:
        # Fallback to simulated weather if API fails
        output.append("Weather data unavailable - using simulated data")
        output.append(f"Error: {str(e)}")

        # Simulated fallback
        weather_conditions = ["Sunny", "Cloudy", "Rainy", "Snowy", "Foggy", "Windy"]
        condition = random.choice(weather_conditions)
        temp = random.randint(0, 30)

        output.append(f"Condition: {condition}")
        output.append(f"Temperature: {temp}°C")
        output.append(f"Humidity: {random.randint(30, 95)}%")
        output.append(f"Wind: {random.randint(0, 30)} km/h")

    return output


if __name__ == "__main__":
    # Test the weather function when run directly
    weather_info = get_weather()
    for line in weather_info:
        print(line)
