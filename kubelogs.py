#!/usr/bin/env python

import argparse
import json
import os
import subprocess
import sys
import time

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


def stream(c, verbose=False):
    waiting_to_start = False
    process = subprocess.Popen(
        c,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
        universal_newlines=True,
    )
    while True:
        nextline = process.stdout.readline()
        proc_poll = process.poll()
        if nextline == "" and proc_poll != None:
            if verbose:
                print(
                    f"Process {c} extied with code {proc_poll}, waiting_to_start={waiting_to_start}"
                )
            return waiting_to_start
        if nextline:
            waiting_to_start = "is waiting to start" in nextline
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
    return False


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
    parser.add_argument('--no-tail', dest='tail', action='store_false')
    parser.set_defaults(tail=True)
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="debug verbose",
    )
    args = parser.parse_args()

    _ka = ka()
    c = f"{_ka} logs -n {args.namespace} {args.pod}"
    if args.tail:
        c += " --follow"
    if args.verbose:
        print(c)

    while True:
        retry = stream(c, verbose=args.verbose)
        if not retry:
            break
        time.sleep(2)


if __name__ == "__main__":
    main()
