#!/usr/bin/env python3

import re
import subprocess
import sys

import requests

problem = "+".join(sys.argv[1:])
live = False
print("your problem is >>", problem, "<<")

answers = requests.get(f"https://stackoverflow.com/search?q={problem}")
for m in re.findall(r"a href=\"\/questions\/(\d+.+?)[\?\"]", answers.text):
    url = "https://stackoverflow.com/questions/" + m
    print("trying", url)
    resp = requests.get(url)
    for code in re.findall(r"<code>(.*?)</code>", resp.text, re.DOTALL):
        print(code)
        if live:
            subprocess.run(code.split())
        i = input("did that fix it? ")
        if i == "yes":
            sys.exit(0)

        if live:
            subprocess.run(["sudo"] + code.split())
        i = input("did that fix it? ")
        if i == "yes":
            sys.exit(0)

sys.exit(1)
