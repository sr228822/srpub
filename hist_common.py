#!/usr/bin/python

import sys
import operator
from utils import *

seen = dict()
lprint = get_now()
t0 = get_now()

n = 10
if len(sys.argv) > 1:
    n = int(sys.argv[1])

def _print_hist(with_rate=True):
    global seen, lprint, t0
    sortseen = sorted(seen.items(), key=operator.itemgetter(1), reverse=True)
    print '------------------------------------------ {} unique total'.format(len(sortseen))
    if with_rate:
        print '  cnt  rate  thing'
    else:
        print '  cnt thing'
    tdelt = seconds_between(t0, get_now())
    for x in sortseen[0:n]:
        tot = int(x[1])
        rate = tot / tdelt
        if with_rate:
            print ('%5d ' % tot) + ('%5.1f ' % rate) + str(x[0])
        else:
            print ('%5d ' % tot) + str(x[0])

for line in quick_ingest_line():
    line = line.rstrip().lstrip()
    seen[line] = seen.get(line, 0) + 1
    if  seconds_between(lprint, get_now()) > 3:
        lprint = get_now()
        _print_hist()

print '\nSTDOUT terminated\n\n\n'
if seconds_between(t0, get_now()) < 3:
    _print_hist(with_rate=False)
else:
    _print_hist()
