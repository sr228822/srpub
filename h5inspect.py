#!/usr/bin/env python

import argparse
import sys

import h5py

from colorstrings import *

fpath = sys.argv[1]
parser = argparse.ArgumentParser()
parser.add_argument(
    "path",
    type=str,
    help="The file",
)
parser.add_argument(
    "--no-trunc",
    action="store_true",
    help="use the inline typing corpora",
)
args = parser.parse_args()
fpath = args.path

f = h5py.File(fpath, "r")

tab = "  "


def show(name, thing, tabs, full=False):
    if "Group" not in str(type(thing)):
        print(red_str(tab * tabs + name + ": ") + str(thing))
        # if full:
        #    for k in thing:
        #        print(k)
        return

    print(tab * tabs + "{}:".format(name))
    attrs = thing.attrs.items()
    focus = full or "cv_skeleton" in str(list(attrs))
    if len(attrs) > 0:
        print_blue(tab * tabs + "Attrs:")
        for k, v in attrs:
            v = str(v)
            if len(v) > 50 and not args.no_trunc:
                v = v[0:50].replace("\n", "\\n") + "..."
            print(blue_str(tab * tabs + "%25s" % k), v)

    for subthing in thing.keys():
        # print(tab * tabs + "{}:".format(subthing))
        show(subthing, thing[subthing], tabs + 1, full=focus)


print(f)
attrs = f.attrs.items()
if len(attrs) > 0:
    print_blue("Attrs:")
    for k, v in attrs:
        v = str(v)
        if len(v) > 50 and not args.no_trunc:
            v = v[0:50].replace("\n", "\\n") + "..."
        print(blue_str("%25s" % k), v)
print(f.keys())

for key in f.keys():
    print("\n=== {} ===".format(key))
    show(key, f[key], 0)
