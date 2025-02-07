


def inner_func():
    print(f"foobar is {foobar}")


def outer_func():
    inner_func()

if __name__ == "__main__":
    foobar = 10
    outer_func()
