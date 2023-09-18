#!/usr/bin/env python3

import sys, traceback

for threadId, stack in sys._current_frames().items():
    print(f"\n# ThreadID: {threadId}")
    for filename, lineno, name, line in traceback.extract_stack(stack):
        print(f'File: "{filename}", line {int(lineno)}, in {name}')
        if line:
            print(f"  {line.strip()}")
