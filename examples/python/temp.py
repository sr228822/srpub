#!/usr/bin/env python3


class Test:
    def __init__(self):
        pass

    def foo(self):
        if hasattr(self, "_has_foo"):
            print("yay")
        print("foo")
        self._has_foo = True


t = Test()
t.foo()
