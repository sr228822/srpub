#!/usr/bin/env python3


def foo(d):
    d['word'] = 'seven'

mydict = {}
mydict['cool'] = 'neat'

foo(mydict)

print(mydict)
