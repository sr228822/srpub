#!/usr/bin/env python


def foo(d):
    d['word'] = 'seven'

mydict = {}
mydict['cool'] = 'neat'

foo(mydict)

print mydict
