#!/usr/bin/python

import contextlib2

@contextlib2.contextmanager
def one():
    """Core instrumentation logic."""
    print('before one')

    yield

    print('after one')

@contextlib2.contextmanager
def two():
    """Core instrumentation logic."""
    print('before two')

    yield

    print('after two')

with one(), two():
    print('foo')
