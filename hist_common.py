#!/usr/bin/env python3

import argparse
import operator

from srutils import get_now, quick_ingest_line, seconds_between
from colorstrings import grey_str

# |sort | uniq -c | sort -nr


gcom = grey_str(",")


def _print_hist(
    seen,
    total_cnt,
    t0,
    lim,
    with_rate=True,
    alphabetical=False,
    dups_only=False,
    with_perc=True,
):

    if alphabetical:
        sortseen = sorted(seen.items(), key=operator.itemgetter(0), reverse=False)
    else:
        sortseen = sorted(seen.items(), key=operator.itemgetter(1), reverse=True)

    print(
        f"------------------------------------------ {len(sortseen)} unique, {total_cnt} total"
    )
    if with_rate and with_perc:
        print("  cnt      %     rate  thing")
        print("  ---    ----    ----  -----")
    elif with_rate:
        print("  cnt    rate   thing")
        print("  ---    ----   -----")
    elif with_perc:
        print("  cnt      %    thing")
        print("  ---    ----   -----")
    else:
        print("  cnt  thing")
        print("  ---  -----")
    tdelt = seconds_between(t0, get_now())
    for x in sortseen[0:lim]:
        tot = int(x[1])
        if dups_only and tot == 1:
            continue
        rate = tot / tdelt
        perc = 100.0 * tot / total_cnt
        if with_rate and with_perc:
            print(f"{int(tot):5} {gcom}{perc:5.1f} {gcom} {rate:5.1f} {gcom} {x[0]}")
        elif with_rate:
            print(f"{int(tot):5} {gcom} {rate:5.1f} {gcom} {x[0]}")
        elif with_perc:
            print(f"{int(tot):5} {gcom} {perc:5.1f} {gcom} {x[0]}")
        else:
            print(f"{int(tot):5} {gcom} {x[0]}")


def main():
    parser = argparse.ArgumentParser("histogram common lines from file or stdin")
    parser.add_argument(
        "--alphabetical",
        action="store_true",
        help="sort alphametically, not by frequency",
    )
    parser.add_argument("--no-percent", action="store_true", help="dont show percent")
    parser.add_argument("--no-rate", action="store_false", help="dont show the rate")
    parser.add_argument(
        "--duplicates", action="store_true", help="only show duplciates"
    )
    parser.add_argument(
        "--limit", type=int, default=10, help="number of entries to show"
    )
    parser.add_argument(
        "--all", action="store_true", help="show all values (overrides limit)"
    )

    args = parser.parse_args()
    _main(args)


def _main(args):
    limit = args.limit
    if args.all:
        limit = 10000000
    seen = dict()
    total_cnt = 0
    lprint = get_now()
    t0 = get_now()

    for line in quick_ingest_line():
        line = line.rstrip().lstrip()
        seen[line] = seen.get(line, 0) + 1
        total_cnt += 1
        if seconds_between(lprint, get_now()) > 3:
            lprint = get_now()
            _print_hist(
                seen,
                total_cnt,
                t0,
                limit,
                alphabetical=args.alphabetical,
                dups_only=args.duplicates,
                with_perc=(not args.no_percent),
            )

    print("\nSTDOUT terminated\n\n\n")
    if seconds_between(t0, get_now()) < 3:
        _print_hist(
            seen,
            total_cnt,
            t0,
            limit,
            with_rate=False,
            alphabetical=args.alphabetical,
            dups_only=args.duplicates,
            with_perc=(not args.no_percent),
        )
    else:
        _print_hist(
            seen,
            total_cnt,
            t0,
            limit,
            with_rate=(not args.no_rate),
            alphabetical=args.alphabetical,
            dups_only=args.duplicates,
            with_perc=(not args.no_percent),
        )


if __name__ == "__main__":
    main()
