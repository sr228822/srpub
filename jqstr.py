#!/usr/bin/env python3
import json
import sys

if __name__ == "__main__":
    for k in sys.stdin:
        js = json.loads(k)
        print(js)
