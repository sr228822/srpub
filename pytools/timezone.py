#!/usr/bin/env python3
import sys
from datetime import datetime

import pytz
from dateutil import parser


def try_epoch(datetime_str):
    """Try to interpret as epoch seconds or milliseconds."""
    try:
        val = int(datetime_str)
    except ValueError:
        try:
            val = float(datetime_str)
        except ValueError:
            return None
    # epoch ms if value is too large for seconds (after year 2100 in seconds)
    if val > 4_102_444_800:
        val = val / 1000.0
        print("Interpreting as epoch milliseconds")
    else:
        print("Interpreting as epoch seconds")
    return datetime.fromtimestamp(val, tz=pytz.UTC)


def parse_and_convert(datetime_str):
    # Try to parse the datetime string
    try:
        # Try epoch first for pure numeric input
        dt = try_epoch(datetime_str)
        if dt is None:
            # Parse the datetime - dateutil.parser handles many formats
            dt = parser.parse(datetime_str)

            # If no timezone info, assume UTC
            if dt.tzinfo is None:
                print("Assuming input is UTC")
                dt = pytz.UTC.localize(dt)

        # Get local timezone
        local_tz = pytz.timezone("US/Eastern")  # Change this to your local timezone

        # Convert to local time
        local_dt = dt.astimezone(local_tz)

        # Convert to UTC
        utc_dt = dt.astimezone(pytz.UTC)

        # Format outputs
        print("")
        epoch_s = int(utc_dt.timestamp())
        epoch_ms = int(utc_dt.timestamp() * 1000)
        print(f"Local (24h): {local_dt.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        print(f"Local (12h): {local_dt.strftime('%Y-%m-%d %I:%M:%S %p %Z')}")
        print(f"UTC:         {utc_dt.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        print(f"Epoch (s):   {epoch_s}")
        print(f"Epoch (ms):  {epoch_ms}")

    except Exception as e:
        print(f"Error parsing datetime: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        parse_and_convert(str(int(datetime.now(pytz.UTC).timestamp())))
    else:
        parse_and_convert(sys.argv[1])
