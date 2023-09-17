#!/usr/bin/env python3

import time
from contextlib import contextmanager


@contextmanager
def my_context(block_description):
    """Core instrumentation logic."""
    start_time = time.time()

    yield

    end_time = time.time()
    print(f"Block {block_description} too {end_time-start_time}s")


with my_context("myblock"):
    time.sleep(1)
    print("foo")
    time.sleep(2)
    print("bork")
