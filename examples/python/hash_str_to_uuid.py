#!/usr/bin/env python

import sys
import uuid

def str_to_uuid(s):
    h = hash(s) + sys.maxsize
    return uuid.UUID('%032d' % h)

a = 'i like apples'

print a
print str_to_uuid(a)
print str_to_uuid(a)

b = 'bork bork the bork'
print b
print str_to_uuid(b)
print str_to_uuid(b)
