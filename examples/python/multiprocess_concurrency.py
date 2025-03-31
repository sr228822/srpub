#!/usr/bin/env python3

import multiprocessing
import random
import time
from contextlib import closing


def foo(x):
    myid = multiprocessing.current_process()._identity[0]
    print("I am worker " + str(myid))
    print("starting " + str(x))
    time.sleep(random.randint(0, 10))
    print("done " + str(x))


if __name__ == "__main__":
    with closing(multiprocessing.Pool(5)) as p:
        p.map(foo, [1, 2, 4, 6])
        p.terminate()
