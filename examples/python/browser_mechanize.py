#!/usr/bin/env python3

import re

import mechanize

br = mechanize.Browser()
# resp = br.open("http://www.example.com")
resp = br.open(
    "http://streeteasy.com/for-rent/east-village/status:open%7Cprice:2500-3000%7Cbeds:1?refined_search=true"
)

print(resp.read())
