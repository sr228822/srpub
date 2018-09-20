#!/usr/bin/python

import os
import mmap
import time

fd = os.open('/tmp/mmaptest', os.O_CREAT | os.O_TRUNC | os.O_RDWR)

assert os.write(fd, '\x00' * mmap.PAGESIZE) == mmap.PAGESIZE

size = mmap.PAGESIZE

data = mmap.mmap(fd, size, mmap.MAP_SHARED, mmap.PROT_WRITE)

i = 0
while True:
    print i
    data[0] = i
    time.sleep(1)
