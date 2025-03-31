#!/usr/bin/env python3

import os
import re
import socket
import sys

import colorstrings
from srutils import save_pickle, load_pickle, cmd


def whois_query(q):
    resp = cmd(f"whois {q}")
    result = ""
    d = dict()
    for line in resp.split("\n"):
        line = line.strip()
        m = re.search("^(.*?)\:(.*?)$", line)
        if m:
            key = m.group(1).lower()
            d[key] = d.get(key, "") + m.group(2).strip()
    result = ""
    for k in ["organisation", "org-name", "city", "stateprov", "country"]:
        if k in d:
            result += d.get(k, "") + ", "
    return result


whoiscache_path = os.path.join(os.getenv("HOME"), ".cache/whois.pkl")
whoiscache = load_pickle(whoiscache_path, dict())


def whois_lookup(ip):
    global whoiscache
    if ip in whoiscache:
        return whoiscache[ip]
    try:
        resp = whois_query(ip)
    except:
        whoiscache[ip] = None
        raise
        return None
    whoiscache[ip] = resp
    return resp


nscache_path = os.path.join(os.getenv("HOME"), ".cache/nslookup.pkl")
nscache = load_pickle(nscache_path, dict())


def ns_lookup(ip):
    global nscache
    if ip in nscache:
        return nscache[ip]
    try:
        fullhost = socket.gethostbyaddr(ip)[0]
    except Exception:
        nscache[ip] = None
        return None
    res = fullhost
    nscache[ip] = res
    return res


def save_caches():
    global nscache
    global whoiscache
    save_pickle(whoiscache, whoiscache_path)
    save_pickle(nscache, nscache_path)


if __name__ == "__main__":
    for line in sys.stdin:
        for ip in re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line):
            dns = ns_lookup(ip)
            whois = whois_lookup(ip)
            if dns or whois:
                comb = (
                    colorstrings.green_str(ip)
                    + " : "
                    + colorstrings.blue_str(f"{dns} : {whois}")
                )
                # print(ip + ' is ' + box)
                line = line.replace(ip, comb)
            else:
                line = line.replace(ip, colorstrings.green_str(ip))
        print(line.rstrip())
    save_caches()
