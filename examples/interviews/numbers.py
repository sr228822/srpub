#!/usr/bin/python

import sys

groups = ["", "Thousand", "million", "billion", "trillion", "quadrillion", "Quintillion", "sextillion", "septillion"]
ten_labels = ["", "", "Twenty", "thirty", "Fourty", "Fifty", "Sixty", "Seventy", "eighty", "ninety"]
one_labels = ["", "one", "two", "three", "four", "five", "six",  "seven", "eight", "nine"]
teens = {10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "Eighteen", 19: "nineteen"}

def _secstr(sec):
    res = ""
    if sec >= 100:
        h = int(sec / 100)
        res += "{} Hundred ".format(one_labels[h])
        sec = (sec % 100)
    if sec >= 10 and sec <= 19:
        return res + teens[sec]
    res += ten_labels[int(sec / 10)] + " "
    sec = (sec % 10)
    res += one_labels[sec]
    return res

i = int(sys.argv[1])
res = neg = ""
if i < 0:
    neg = "negative "
    i = -i
g = 0
while i != 0:
    diff = (i % 1000)
    res = "{} {} {}".format(_secstr(diff), groups[g], res)
    i = int((i - diff) / 1000)
    g += 1
print(neg + res)
