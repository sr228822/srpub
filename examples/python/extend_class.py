#!/usr/bin/env python3


class MyClass:
    def __init__(self, a):
        self.a = a

    def foo(self):
        print("a is ", self.a)


class OtherClass(MyClass):
    def __init__(self, a, b):
        MyClass.__init__(self, a)
        self.b = b

    def bork(self):
        print("b is ", self.b)


oc = OtherClass(6, 7)

oc.foo()
oc.bork()
