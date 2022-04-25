#!/usr/bin/env python

words = ['these', 'are', 'words']

print any([x in "bork de bork bork" for x in words])
print any([x in "bork de these bork bork" for x in words])
