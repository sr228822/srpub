#!/usr/bin/python
import sys
import json

for k in sys.stdin:
    js = json.loads(k)
    print(js)
