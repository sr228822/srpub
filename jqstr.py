#!/usr/bin/env python3
import sys
import json

for k in sys.stdin:
    js = json.loads(k)
    print(js)
