#!/usr/bin/python

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

if __name__ == '__main__':
    p = multiprocessing.Process(target=foo, args=('bob',))
    p.start()
    p.join(5)
    print("it has been 5 seconds, p is ", p.is_alive())
