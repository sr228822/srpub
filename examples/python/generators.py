#!/usr/bin/env python3

import datetime, time

# lists iterables first
print("this is a list, its complete made, stored in memory")
print("  list_iterable = [datetime.datetime.now() for i in range(4)]")
print(
    "  ... notice all the times are the same because they were all made in the beginning"
)
list_iterable = [datetime.datetime.now() for i in range(4)]
for x in list_iterable:
    time.sleep(1)
    print(x)

print("\n\n")

print("this is a generator, its not actually made untill you loop through it")
print("  list_generator = (datetime.datetime.now() for i in range(4))")
print(
    "  ... notice all the times are different because they are being made as we loop through"
)
list_generator = (datetime.datetime.now() for i in range(4))
for x in list_generator:
    time.sleep(1)
    print(x)

print("\n\n")

print("functions with yield serve as generators")


def create_generator():
    print("code before the first yield gets run on the first iteration")
    for i in range(4):
        print("generating " + str(i))
        yield datetime.datetime.now()
    print("code after the last yield gets run after the last iteration")


print("when i create the generator no code is executed")

mygenerator = create_generator()

print("it is only when we begin to iterate it that it actually gets called")
print(
    "at that point it runs to the first yield, and on subsequent calls continues to run to the next yield\n\n"
)

for x in mygenerator:
    time.sleep(1)
    print(x)
