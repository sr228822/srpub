#!/usr/bin/env python

import multiprocessing
from contextlib import closing
import time, random

def foo(x):
    myid = multiprocessing.current_process()._identity[0]
    dur = int(random.random() * 10.0)
    print(f"worker {myid}, my task takes {dur}")
    for i in range(dur):
        print("still working", i)
        time.sleep(1)
    print('done ' + str(x))
    return "neat"

if __name__ == '__main__':
    p = multiprocessing.Pool(processes=1)
    a = p.apply_async(foo, args=('bob',))
    try:
        resp = a.get(timeout=5)
        print("made it, result is ", resp)
    except multiprocessing.TimeoutError:
        print("didnt make it in time")
    time.sleep(5)
