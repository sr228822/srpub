#!/usr/bin/env python3

import sys
import time

from srutils import argpop, parse_duration
from timezone import parse_and_convert

if __name__ == "__main__":
    millis = argpop(sys.argv, "--millis") or argpop(sys.argv, "millis")

    has_duration = len(sys.argv) > 1
    ago = int(parse_duration(sys.argv[1])) if has_duration else 0

    t = int(time.time()) - ago
    if millis:
        t *= 1000
    parse_and_convert(str(t), show_relative=has_duration, quiet=not has_duration)
