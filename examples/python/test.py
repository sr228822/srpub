#!/usr/bin/python

from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop
from tornado import gen
import time, sys, random, logging
import contextlib2


######## old ############
@gen.coroutine
def fake_web_request(ident):
    print 'starting web request ' + ident
    time.sleep(4)
    print 'finished with web request ' + ident
    return 'hello world'

@gen.coroutine
def my_coroutine(url):
    print 'enter coroutine'
    response_a = yield fake_web_request('a')
    response_b = yield fake_web_request('b')
    response_c = yield fake_web_request('c')
    print 'back in fetch coroutine'
    raise gen.Return(response_a)

@gen.coroutine
def my_coroutine_wrapper(url):
    yield my_coroutine(url)

###### A fake context manager

import contextlib
i = 0

@contextlib.contextmanager
def my_context():
    global i
    i += 1
    print 'enter my context ' + str(i)
    yield
    i -= 1
    print 'exit my context' + str(i)

######### A timeout decorator using signals

from functools import wraps
import errno
import os
import signal
import time

class TimeoutError(Exception):
    pass

def mytimeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator

@contextlib2.contextmanager
def instrument():
    """Core instrumentation logic."""

    start_time = time.time()
    try:
        yield
    except:
        print 'instruemtn exception'
        raise
    else:
        end_time = time.time()
        ms = (end_time - start_time) * 1000
        print 'instrument timing was ' + str(ms)


######## new ############

@gen.coroutine
@instrument()
def foo():
    print "I am fooooooo"
    time.sleep(3)

@gen.coroutine
def pek():
    print "I am pekk"
    yield foo()
    raise gen.Return(1)

print IOLoop().run_sync(lambda: pek())

