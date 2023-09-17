#!/usr/bin/env python3

import multiprocessing
import random, time
from contextlib import closing

counter = None


def init(args):
    global counter
    counter = args


def foo(x):
    global counter
    myid = multiprocessing.current_process()._identity[0]

    with counter.get_lock():
        counter.value += 1

    print("starting worker", myid, "value", x, "progress", counter.value)
    time.sleep(random.randint(0, 10))
    print("done " + str(x))


if __name__ == "__main__":
    counter = multiprocessing.Value("i", 0)
    with closing(multiprocessing.Pool(5, initializer=init, initargs=(counter,))) as p:
        p.map(foo, [1, 2, 4, 6, 8, 1, 2, 5, 2, 3, 4, 1, 5, 2, 89, 2, 88])
        p.terminate()
