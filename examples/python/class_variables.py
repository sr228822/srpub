#!/usr/bin/env python3


class MyClass():
    myvar = 0

    @classmethod
    def get(cls):
        return cls.myvar

    @classmethod
    def inc(cls):
        cls.myvar += 1

print(MyClass.get())
MyClass.inc()
print(MyClass.get())
MyClass.inc()
print(MyClass.get())
