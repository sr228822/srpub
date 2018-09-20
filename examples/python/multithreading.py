#!/usr/bin/python

import Queue
import threading
import urllib2
import time

# called by each thread
def get_url(q, url):
    print 'starting ' + str(url)
    time.sleep(4)
    print 'finished ' + str(url)
    q.put('finished ' + str(url))
    #q.put(urllib2.urlopen(url).read())

theurls = ["http://google.com", "http://yahoo.com", "http://uber.com"]

q = Queue.Queue()

for u in theurls:
    t = threading.Thread(target=get_url, args = (q,u))
    t.daemon = True
    t.start()

s = q.get()
print s
