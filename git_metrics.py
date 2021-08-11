#!/usr/bin/python3

from __future__ import print_function

from srutils import *
import argparse
import sys, re
import operator
from collections import namedtuple
import datetime

# A map of known aliases -> name
kauths = {}

# A map of kname to longest-name
longname = {}

MY_NAME = cmd("git config user.name") or "samuel russell"

parser = argparse.ArgumentParser()
parser.add_argument(
    '--user',
    type=str,
    required=False,
    default=MY_NAME,
    help='The user to highlight.')
parser.add_argument(
    '--period',
    type=str,
    required=False,
    help='The time-period to run-over, (e.g. 200 or 2y)')
parser.add_argument(
    '--overall', action='store_true', help='Show overall')
args = parser.parse_args()

def is_int(x):
    try:
        x = int(x)
        return True
    except ValueError:
        return False

def epoch_to_date(e):
    return datetime.datetime.utcfromtimestamp(e).strftime('%Y-%m-%d')

def fmt_float(f, decimals=1, width=4):
    f_fmt = "%." + str(decimals) + "f"
    s_fmt = "%" + str(width) + "s"
    return s_fmt % (f_fmt % f) 

class TimeRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __str__(self):
        return "[{} - {}]".format(epoch_to_date(self.start), epoch_to_date(self.end))

    def add(self, dt):
        self.start = min(self.start, dt)
        self.end = max(self.end, dt)

    def seconds(self):
        return (self.end - self.start)

    def weeks(self):
        return max(1, (self.seconds() / 604800))

    def human_dur(self):
        return dur_to_human(self.seconds())

class GitStat:
    def __init__(self):
        self.cnt = {}
        self.tim = TimeRange(9999999999, 0)

    def add(self, kname, dt):
        self.cnt[kname] = self.cnt.get(kname, 0) + 1
        self.tim.add(dt)


# Set count and dur thresholds
thresh_cnt = 100
thresh_dur = '1y'
if args.period:
    if is_int(args.period):
        thresh_cnt = int(args.period)
    else:
        thresh_dur = args.period
thresh_dur_s = parse_duration(thresh_dur)

all_stat = GitStat()
since_me_stat = GitStat()
thresh_cnt_stat = GitStat()
thresh_dur_stat = GitStat()

user_active_tim = {}

STRIP_PREFX = "ctrl"

def looks_similar(a, b):
    """Return true if string `a` looks pretty similar to `b`

    The algorithm basically comparse each coresponding word for
    case-insensitive substring matches
    """
    a = a.lower().strip()
    b = b.lower().strip()
    if a == b:
        return True
    words_a = a.split(" ")
    words_b = b.split(" ")
    if len(words_a) != len(words_b):
        return False
    for idx in range(len(words_a)):
        if words_a[idx] in words_b[idx] or words_b[idx] in words_a[idx]:
            continue
        return False
    return True

def put_in_known(name, email):
    global kauths
    name = name
    email = email

    # if we have both the name and email, we're done
    if name in kauths and email in kauths:
        #if kauths[name] == kauths[email]:
        #    return
        return

    if name in kauths:
        # we have the name, but not the email
        kauths[email] = kauths[name]
        return

    if email in kauths:
        # we have the email, but not the name
        kauths[name] = kauths[email]
        return

    # we have neither the exact email nor exact name
    found = False
    for other_auth in kauths.keys():
        if looks_similar(name, other_auth):
            kauths[name] = kauths[other_auth]
            kauths[email] = kauths[other_auth]
            return

    # we did not find any similar name matches
    # so add a new entry
    fname = name
    if name.startswith(STRIP_PREFX):
        fname = name[len(STRIP_PREFX):]
    kauths[name] = fname
    kauths[email] = fname

def get_aliases(name, emails=True):
    global kauths
    res = {}
    for k, v in kauths.items():
        if v == name:
            if "@" in k or not emails:
                res[k] = True
    return res.keys()

def print_cnt_dict(title, stat, limit=10):
    sorted_x = sorted(stat.cnt.items(), key=operator.itemgetter(1), reverse=True)
    did_me = False
    total_time = stat.tim.seconds()
    total_cnt = sum(stat.cnt.values())
    print("\n\n=== {} === \t ({}) ({} total)".format(title, stat.tim.human_dur(), total_cnt))
    print("%3s" % "" + "   " + "%5s" % "cnt " + " " + "  %  " + " " + "/week" + " " + "name")
    print("%3s" % "" + "   " + "%5s" % "--- " + " " + "-----" + " " + "-----" + " " + "----")
    for i, x in enumerate(sorted_x):
        kname = x[0]
        is_me = looks_similar(kname, args.user)
        name = longname[kname].title()
        if is_me:
            did_me = True
            name = blue_str(name)
        cnt = x[1]
        rate = (float(cnt) / stat.tim.weeks())  # convert to weekly rate
        if i == limit:
            if did_me:
                break
            else:
                print("                  ...")
        if i >= limit and not is_me:
            continue
        perc = int(100 * cnt / total_cnt)
        print("%3d" % (i+1) + ". " + "%5d  " % cnt + "  %2d" % perc + "%  " + "%.1f " % rate + " {0: <25}".format(name))

git_log_raw = cmd("git log master --format='%H,%aN,%ae,%at,%s'")

dt_now = int(time.time())
seen_me = False
commits = git_log_raw.split('\n')
for i, c in enumerate(reversed(commits)):
    cs = c.strip().split(',')
    if len(cs) < 5:
        continue
    sha = cs[0].strip()
    name = cs[1].strip().lower()

    # ewww, some names have commas in them
    if "@" not in cs[2] and "@" in cs[3]:
        name = (name + " " + cs[2].strip().lower())
        cs.pop(2)

    email = cs[2].strip().lower()
    dt = int(cs[3].strip())
    subj = ",".join(cs[4:])

    # Skip merge commits
    if subj.startswith("Merge "):
        continue

    # Skip revert commits
    if subj.startswith("Revert"):
        continue

    is_mine = looks_similar(name, args.user)
    if is_mine:
        seen_me = True

    put_in_known(name, email)
    kname = kauths[name]

    # set the longest-name which kname maps to
    if kname not in longname:
        longname[kname] = kname
    if len(name) >len( longname[kname]):
        longname[kname] = name

    # Add this commit to stat-counters it matches
    all_stat.add(kname, dt)
    if seen_me:
        since_me_stat.add(kname, dt)
    if (dt_now - dt) < thresh_dur_s:
        thresh_dur_stat.add(kname, dt)
    if i > len(commits) - thresh_cnt:
        thresh_cnt_stat.add(kname, dt)

    # Track each users "active contribution range"
    if kname not in user_active_tim:
        user_active_tim[kname] = TimeRange(dt, dt)
    user_active_tim[kname].add(dt)

# calculate each users rate-while-active
rate_while_active = {}
for key in user_active_tim:
    cnt = all_stat.cnt[key]
    rate = (float(cnt) / user_active_tim[key].weeks())  # convert to weekly rate
    rate_while_active[key] = rate

sorted_x = sorted(rate_while_active.items(), key=operator.itemgetter(1), reverse=True)

def print_active_rate():
    print("\n\n=== {} === \t".format("Rate while active"))
    print("%3s" % "" + "  " + "%5s" % "cnt " + " weeks " + "rate " + " " + "name")
    print("%3s" % "" + "  " + "%5s" % "--- " + " ----- " + "---- " + " " + "----")
    limit = 10
    did_me = False
    for i, x in enumerate(sorted_x):
        kname = x[0]
        cnt = all_stat.cnt[kname]
        weeks = user_active_tim[kname].weeks()
        is_me = looks_similar(kname, args.user)
        name = longname[kname].title()
        name = " {0: <25}".format(name)
        if is_me:
            did_me = True
            name = blue_str(name)
        val = x[1]
        if i == limit:
            if did_me:
                break
            else:
                print("                  ...")
        if i >= limit and not is_me:
            continue
        print("%3d" % (i+1) + ". " + "%5d" % cnt + " %5d " % weeks + fmt_float(val, width=4)  + "  " + name + str(user_active_tim[kname]))

#print("\n\n== kauth map ==")
#for k,v in kauths.items():
#    print("%50s" % k, "   ", "%50s" % v)

#print("\n\n== kauth map ==")
#for k,v in all_stat.cnt.items():
#    print("%50s" % k, "   ", "%50s" % v)

if args.overall:
    print_cnt_dict("Overall", all_stat, limit=100)
elif args.period:
    if is_int(args.period):
        print_cnt_dict(f"Last {thresh_cnt}", thresh_cnt_stat)
    else:
        print_cnt_dict(f"Last {thresh_dur}", thresh_dur_stat)
else:
    print_active_rate()
    # print personalized
    print_cnt_dict("Overall", all_stat)
    print_cnt_dict("Since-First", since_me_stat)
    print_cnt_dict(f"Last {thresh_dur}", thresh_dur_stat)
    print_cnt_dict(f"Last {thresh_cnt}", thresh_cnt_stat)

