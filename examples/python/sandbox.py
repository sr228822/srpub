#!/usr/bin/python


b = 10

x = 0
x += b
for z in range(1000000):
    x += 0.000001
x -= b

print x
