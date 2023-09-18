#!/usr/bin/env python3

import sys
import traceback

try:
    assert 7 == 1
except AssertionError as e:
    s = traceback.format_exc()
    print(f"lol assert did fail {s}")
    print(f"lol assert message {sys.exc_info()[0]}")

print("im still alive")
