#!/usr/bin/env python

import argparse
import json
import os
import subprocess
import sys

from colorstrings import loglevel_color


def ka():
    if e := os.environ["KA_COMMAND"]:
        return e
    return "kubectl"


def as_json(s):
    try:
        return json.loads(s)
    except:
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "pod",
        type=str,
        help="The file",
    )
    parser.add_argument(
        "--namespace",
        type=str,
        default="default",
        help="kube namespace",
    )
    parser.add_argument(
        "--tail",
        action="store_true",
        help="tail live",
    )
    args = parser.parse_args()

    _ka = ka()
    c = f"{_ka} logs -n {args.namespace} {args.pod}"
    if args.tail:
        c += " --follow"
    print(c)

    process = subprocess.Popen(
        c,
        stdout=subprocess.PIPE,
        stderr=sys.stderr,
        shell=True,
        universal_newlines=True,
    )
    while True:
        nextline = process.stdout.readline()
        proc_poll = process.poll()
        if nextline == "" and proc_poll != None:
            print(f"Process extied with code {proc_poll}")
            break
        if nextline:
            if js := as_json(nextline):
                level = js.get("level")
                msg = js.get("message")
                if not msg:
                    sys.stdout.write(nextline)
                    sys.stdout.flush()
                    continue
                tim = js.get("asctime")
                if tim:
                    msg = f"[{tim}] {msg}\n"
                msg = loglevel_color(msg, level)
                sys.stdout.write(msg)
            else:
                sys.stdout.write(nextline)
            sys.stdout.flush()


if __name__ == "__main__":
    main()
