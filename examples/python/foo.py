#!/usr/bin/env python3


class Foo:
    def bar(self):
        print("i am bar")
        return 7

    def bak(self):
        print("i am bak")


def test_foobar():
    f = Foo()
    print("foo is " + str(type(f)))
    print(f.bar())
    print(f.bak())
