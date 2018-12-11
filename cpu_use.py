#!/usr/bin/python

from srutils import *
import time
import sys

proc_name = sys.argv[1]

pid = cmd("pidof {}".format(proc_name))

if not pid:
    print("could not find pid for {}".format(proc_name))
    sys.exit(1)

ema = 0.95
avg = None

print(" cur     avg")
while True:
    r = cmd("ps -p {} -o %cpu".format(pid))
    cpu = float(r.split("\n")[1])
    if avg is None:
        avg = cpu
    else:
        avg = (ema * avg) + ((1-ema) * cpu)
    print("%.1f\t%.1f" % (cpu, avg))
    time.sleep(0.25)
