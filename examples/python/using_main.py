#!/usr/bin/env python3

import sys


def foo():
    print("woooo")


if __name__ == "__main__":
    print("i am being run")
else:
    print("I am being imported")

print(sys.argv)
