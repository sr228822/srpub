#!/usr/bin/env python

from queue import Queue
import threading
# import requests
# import urllib2
import time
import random

# called by each thread
def get_url(q, url):
    delay = 4 + int(random.random() * 3)
    print(f"starting {url} sleep {delay}")
    time.sleep(delay)
    #q.put(urllib2.urlopen(url).read())
    print(f"finished {url}")
    q.put(f"result {url}")

theurls = ["http://google.com", "http://yahoo.com", "http://uber.com"]

q = Queue()

threads = []
for u in theurls:
    t = threading.Thread(target=get_url, args = (q,u))
    #t.daemon = True
    t.start()
    threads.append(t)


# Poll status
while True:
    status = [t.is_alive() for t in threads]
    print(status)
    if not any(status):
         break
    time.sleep(0.1)

for i in range(len(theurls)):
    s = q.get()
    print(s)
