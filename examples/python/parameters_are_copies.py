#!/usr/bin/env python

def foo(x):
    x += 1
    print 'inside', x

b = 1
print 'before', b
foo(b)
print 'after', b
