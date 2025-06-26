#!/usr/bin/env python3
import sys
import pytz
from dateutil import parser

def parse_and_convert(datetime_str):
    # Try to parse the datetime string
    try:
        # Parse the datetime - dateutil.parser handles many formats
        dt = parser.parse(datetime_str)
        
        # If no timezone info, assume UTC
        if dt.tzinfo is None:
            print("Assuming input is UTC")
            dt = pytz.UTC.localize(dt)
        
        # Get local timezone
        local_tz = pytz.timezone('US/Eastern')  # Change this to your local timezone
        
        # Convert to local time
        local_dt = dt.astimezone(local_tz)
        
        # Convert to UTC
        utc_dt = dt.astimezone(pytz.UTC)
        
        # Format outputs
        print(f"Local (24h): {local_dt.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        print(f"Local (12h): {local_dt.strftime('%Y-%m-%d %I:%M:%S %p %Z')}")
        print(f"UTC:         {utc_dt.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        
    except Exception as e:
        print(f"Error parsing datetime: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python timezone.py '<datetime string>'")
        sys.exit(1)
    
    parse_and_convert(sys.argv[1])
