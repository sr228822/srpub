#!/usr/bin/env python3


def decorator(func=None, **options):
    if func is not None:
        # We received the function on this call, so we can define
        # and return the inner function
        def inner(*args, **kwargs):
            if len(options) > 0:
                print("Decorated function with options:")
            else:
                print("Decorated function without options!")

            for k, v in options.items():
                print(f"\t{k}: {v}")

            func(*args, **kwargs)

        return inner

    else:
        # We didn't receive the function on this call, so the return value
        # of this call will receive it, and we're getting the options now.
        def partial_inner(func):
            return decorator(func, **options)

        return partial_inner


@decorator
def function_a(x, y):
    print(x + y)


@decorator(foo="bar", baz=42)
def function_b(x, y):
    print(x + y)
