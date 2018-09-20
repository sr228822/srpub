#!/usr/bin/python

import sys
import operator
from utils import *

# |sort | uniq -c | sort -nr

seen = dict()
total_cnt = 0
lprint = get_now()
t0 = get_now()

n = 10
if len(sys.argv) > 1:
    n = 10000000 if sys.argv[1] == 'all' else int(sys.argv[1])
duplicated = 'dups' in sys.argv or 'duplicated' in sys.argv

def _print_hist(with_rate=True, alphabetical=False, dups_only=False, with_perc=False):
    global seen, lprint, t0, total_cnt

    if alphabetical:
        sortseen = sorted(seen.items(), key=operator.itemgetter(0), reverse=False)
    else:
        sortseen = sorted(seen.items(), key=operator.itemgetter(1), reverse=True)

    print '------------------------------------------ {} unique, {} total'.format(len(sortseen), total_cnt)
    if with_rate:
        print '  cnt  rate  thing'
        print '  ---  ----  -----'
    elif with_perc:
        print '  cnt    %   thing'
        print '  ---  ----  -----'
    else:
        print '  cnt thing'
        print '  --- -----'
    tdelt = seconds_between(t0, get_now())
    for x in sortseen[0:n]:
        tot = int(x[1])
        if dups_only and tot == 1:
            continue
        rate = tot / tdelt
        if with_rate:
            print ('%5d , ' % tot) + ('%5.1f ' % rate) + str(x[0])
        elif with_perc:
            print ('%5d , ' % tot) + ('%5.1f ' % (100.0 * tot/total_cnt)) + str(x[0])
        else:
            print ('%5d , ' % tot) + str(x[0])

alphabetical = argpop(sys.argv, "--alphabetical")
with_perc = argpop(sys.argv, "--percent")
for line in quick_ingest_line():
    line = line.rstrip().lstrip()
    seen[line] = seen.get(line, 0) + 1
    total_cnt += 1
    if  seconds_between(lprint, get_now()) > 3:
        lprint = get_now()
        _print_hist(alphabetical=alphabetical, dups_only=duplicated, with_perc=with_perc)

print '\nSTDOUT terminated\n\n\n'
if seconds_between(t0, get_now()) < 3:
    _print_hist(with_rate=False, alphabetical=alphabetical, dups_only=duplicated, with_perc=with_perc)
else:
    _print_hist(alphabetical=alphabetical, dups_only=duplicated, with_perc=with_perc)
