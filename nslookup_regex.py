#!/usr/bin/python

import re, sys, socket

import colorstrings

nscache = dict()
def ns_lookup(ip):
    global nscache
    if ip in nscache:
        return nscache[ip]
    try:
        fullhost = socket.gethostbyaddr(ip)[0]
    except:
        nscache[ip] = None
        return None
    if 'prod.uber.internal' in fullhost:
        res = fullhost.split('.')[0]
    else:
        res = fullhost
    nscache[ip] = res
    return res

for line in sys.stdin:
    for ip in re.findall(r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}', line):
        box = ns_lookup(ip)
        if box:
            #print ip + ' is ' + box
            line = line.replace(ip, colorstrings.blue_str(box))
    print line.rstrip()
