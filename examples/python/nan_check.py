#!/usr/bin/env python3

import math


def check_for_nan(path, d):
    if type(d) == list:
        for x in d:
            check_for_nan(path, x)
    if type(d) == dict:
        for k in d.keys():
            check_for_nan(f"{path}.{k}", d[k])
    if type(d) == float:
        if math.isnan(d):
            print("I FOUND A NAN")
            print(path)
            print(d)


example = {
    "foo": 8,
    "bork": "asdfa",
    "ban": {
        "notanan": 89.0,
        "target": float("nan"),
    },
}

check_for_nan("", example)
