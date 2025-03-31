#!/usr/bin/env python3

# def foo():
#    print('yay')

# Code below here will be fine even if foo isn't defined

if "foo" in dir():
    foo()  #  noqa
