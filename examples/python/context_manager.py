#!/usr/bin/env python3

import contextlib2

@contextlib2.contextmanager
def my_context():
    """Core instrumentation logic."""
    print('before')

    yield

    print('after')

with my_context():
    print('foo')
