#!/usr/bin/env python3


class MyClass:
    def __init__(self):
        pass

    def foo(self):
        print('i am foo')


def monkey(self):
    print('banana')

MyClass.foo = monkey

c = MyClass()
c.foo()
