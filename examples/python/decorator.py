#!/usr/bin/env python3

def my_decorator(func):
    def inner(*args, **kwargs):
        print('one, the func is ', func.__name__)
        resp = func(*args, **kwargs)
        print('three')
        return resp
    return inner


class MyClass:
    def __init__(self):
        pass

    @classmethod
    @my_decorator
    def bar(cls):
        print('i am bar')
        return 'brahhhh'

def foo():
    print('two')

print('here is the decorated bar')
c = MyClass()
print(c.bar())

print('\n\nhere is foo with an inline use')
my_decorator(foo)()
