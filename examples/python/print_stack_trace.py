

def womp():
    print("inside womp")

    import traceback
    traceback.print_stack()

    return 5

def bork():
    return 4 * womp()

def foo():
    a = 1
    bork()
    return 4


foo()
