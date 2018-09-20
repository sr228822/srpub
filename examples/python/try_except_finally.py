#!/usr/bin/python


try:
    raise Exception("My Exception")
finally:
    print 'this happens'
