#!/usr/bin/env python3

import sys
import time
from srutils import parse_duration, argpop

if __name__ == "__main__":
    millis = argpop(sys.argv, "--millis") or argpop(sys.argv, "millis")

    if len(sys.argv) > 1:
        ago = int(parse_duration(sys.argv[1]))
    else:
        ago = 0

    t = int(time.time()) - ago
    if millis:
        t *= 1000
    print(t)
