#!/usr/bin/env python3


class Test:
    def __init_(self):
        pass

    def foo(cls):
        print("you are in " + str(cls.__name__))


t = Test()
t.foo()
