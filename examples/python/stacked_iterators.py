def inner():
    return range(5)


i = inner()
print(type(i))
print(i)
for x in i:
    print(x)


def outer():
    i = inner()
    for x in i:
        yield f"neat-{x}"


o = outer()
print(type(o))
print(o)
for x in o:
    print(x)
