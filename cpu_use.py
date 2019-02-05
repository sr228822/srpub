#!/usr/bin/python

from srutils import *
import time
import sys

proc_name = sys.argv[1]

pid = cmd("pidof {}".format(proc_name))

if not pid:
    print("waiting for process to start...")
    while not pid:
        time.sleep(1)
        pid = cmd("pidof {}".format(proc_name))

ema = 0.85
avg = None
t0 = time.time()

print("time\tcur\tavg")
while True:
    pid = cmd("pidof {}".format(proc_name))
    if not pid:
        time.sleep(1)
        continue

    r = cmd("ps -p {} -o %cpu".format(pid))
    cpu = float(r.split("\n")[1])
    if avg is None:
        avg = cpu
    else:
        avg = (ema * avg) + ((1-ema) * cpu)
    print("%.1f\t%.1f\t%.1f" % ((time.time() - t0), cpu, avg))
    time.sleep(0.25)
