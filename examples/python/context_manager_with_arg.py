#!/usr/bin/python

import contextlib2

@contextlib2.contextmanager
def my_context(a):
    """Core instrumentation logic."""
    print 'before ', a

    yield

    print 'after', a


with my_context('thearg'):
    print 'foo'
