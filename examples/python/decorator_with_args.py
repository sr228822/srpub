#!/usr/bin/python

def my_decorator(argument):
    def real_decorator(func):
        def inner(*args, **kwargs):
            print 'one'
            print 'arg to wrapper was ', argument
            resp = func(*args, **kwargs)
            print 'three'
            return resp
        return inner
    return real_decorator


@my_decorator("wapperarglolz")
def foo(fooarg):
    print 'foo with fooarg ', fooarg

def bar(bararg):
    print 'bar with bararg ', bararg

print 'here is the decorated foo'
foo('my fooarg')

print '\n\n\nhere is the inline bar'
my_decorator("thearg")(bar)("thebararg")
