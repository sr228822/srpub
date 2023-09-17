#!/usr/bin/env python3


try:
    raise Exception("My Exception")
finally:
    print("this happens")
