def womp():
    print("inside womp")

    import traceback

    # get as string
    as_string = traceback.format_stack()
    print(f"--asstr--\n{as_string}\n------")

    # print to stdout
    traceback.print_stack()

    try:
        raise Exception("oh no")
    except Exception:
        # a version that includes the exception
        as_string = traceback.format_exc()
        print(f"--asstr--\n{as_string}\n------")

    return 5


def bork(a):
    return a * womp()


def foo():
    a = 1
    bork(a)
    return 4


foo()
