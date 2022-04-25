#!/usr/bin/env python3

from srutils import *
import time
import sys

def is_int(x):
    try:
        i = int(x)
        return True
    except:
        return False

def get_pid():
    a1 = sys.argv[1]
    if is_int(a1):
        return int(a1)
    proc_name = sys.argv[1]

    pid = cmd("pidof {}".format(proc_name))
    if pid:
        return pid

    print("waiting for process to start...")
    while not pid:
        time.sleep(1)
        pid = cmd("pidof {}".format(proc_name))

    return pid

ema = 0.85
avg = None
t0 = time.time()

#print("time\tcur\tavg")
print("CPU %")
while True:
    pid = get_pid()
    if not pid:
        print("No Pid")
        time.sleep(0.25)
        continue

    r = cmd("ps -p {} -o %cpu".format(pid))
    #print(r.split("\n"))
    cpu = float(r.split("\n")[1])
    if avg is None:
        avg = cpu
    else:
        avg = (ema * avg) + ((1-ema) * cpu)
    #print("%.1f\t%.1f\t%.1f" % ((time.time() - t0), cpu, avg))
    print("{} %".format(cpu))
    time.sleep(0.25)
