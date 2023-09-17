#!/usr/bin/env python3
import json
import sys

for k in sys.stdin:
    js = json.loads(k)
    print(js)
