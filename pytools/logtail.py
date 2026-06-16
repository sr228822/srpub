#!/usr/bin/env python3
"""
logtail — colorized tail for structured log files.

Parses lines matching: [TIMESTAMP][LOGGER][LEVEL] message
Unrecognized lines are printed as-is (continuation lines, stack traces, etc.).

Usage:
  logtail.py <file>              show last N lines (default 50)
  logtail.py -f <file>           follow (like tail -f)
  logtail.py --level WARNING     only show WARNING and above
  logtail.py -n 100 <file>       show last 100 lines
  cat file.log | logtail.py      read from stdin
"""

import argparse
import re
import sys
import time

from colorstrings import (
    bold_str,
    cyan_str,
    grey_str,
    red_str,
    yellow_str,
)

LOG_RE = re.compile(
    r"^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:,\d+)?)\]"
    r"\[([^\]]+)\]"
    r"\[([A-Z]+)\] ?(.*)"
)

LEVELS = ["DEBUG", "INFO", "WARNING", "WARN", "ERROR", "CRITICAL", "FATAL"]
LEVEL_RANK = {
    "DEBUG": 0,
    "INFO": 1,
    "WARNING": 2,
    "WARN": 2,
    "ERROR": 3,
    "CRITICAL": 4,
    "FATAL": 4,
}


def level_rank(level: str) -> int:
    return LEVEL_RANK.get(level.upper(), 1)


def colorize(line: str, min_rank: int) -> str | None:
    m = LOG_RE.match(line)
    if not m:
        return line  # pass through (stack traces, continuation lines)

    ts, logger, level, msg = m.groups()
    if level_rank(level) < min_rank:
        return None  # filtered out

    prefix = grey_str(f"[{ts}]") + cyan_str(f"[{logger}]")
    if level in ("ERROR", "CRITICAL", "FATAL"):
        level_s = bold_str(red_str(f"[{level}]"))
        msg_s = red_str(msg)
    elif level in ("WARNING", "WARN"):
        level_s = yellow_str(f"[{level}]")
        msg_s = yellow_str(msg)
    elif level == "DEBUG":
        level_s = grey_str(f"[{level}]")
        msg_s = grey_str(msg)
    else:  # INFO
        level_s = f"[{level}]"
        msg_s = msg

    return f"{prefix}{level_s} {msg_s}"


def tail_lines(path: str, n: int) -> list[str]:
    """Return last n lines of file efficiently."""
    with open(path, "rb") as f:
        f.seek(0, 2)
        size = f.tell()
        if size == 0:
            return []
        buf = bytearray()
        pos = size
        found = 0
        chunk = 8192
        while pos > 0 and found <= n:
            read = min(chunk, pos)
            pos -= read
            f.seek(pos)
            buf[:0] = f.read(read)
            found = buf.count(b"\n")
        lines = buf.decode("utf-8", errors="replace").splitlines()
        return lines[-n:] if n else lines


def print_line(line: str, min_rank: int):
    colored = colorize(line, min_rank)
    if colored is not None:
        print(colored)


def main():
    parser = argparse.ArgumentParser(description="Colorized log tail")
    parser.add_argument("file", nargs="?", help="Log file (stdin if omitted)")
    parser.add_argument(
        "-f", "--follow", action="store_true", help="Follow file (like tail -f)"
    )
    parser.add_argument(
        "-n", type=int, default=50, help="Number of lines to show (default 50)"
    )
    parser.add_argument(
        "--level",
        default="DEBUG",
        metavar="LEVEL",
        help="Minimum log level to show: DEBUG INFO WARNING ERROR CRITICAL (default DEBUG)",
    )
    args = parser.parse_args()

    min_rank = level_rank(args.level.upper())

    if args.file is None:
        # Read from stdin — no follow mode
        for line in sys.stdin:
            print_line(line.rstrip(), min_rank)
        return

    # Show tail of existing content
    for line in tail_lines(args.file, args.n):
        print_line(line, min_rank)

    if not args.follow:
        return

    # Follow mode: watch for new lines
    with open(args.file) as f:
        f.seek(0, 2)  # seek to end
        while True:
            line = f.readline()
            if line:
                print_line(line.rstrip(), min_rank)
            else:
                time.sleep(0.1)


if __name__ == "__main__":
    main()
