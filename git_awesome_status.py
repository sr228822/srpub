#!/usr/bin/python

from __future__ import print_function

from srutils import *
import sys, re, os
from operator import itemgetter

class Commit:
    def __init__(self, sha, title):
        self.sha = sha
        self.title = title

def clean_up_decorate(lines):
    res = ''
    for line in lines.split('\n'):
        m = re.search(r'\((.+?)\)', line)
        if m:
            decorate = m.group(1)
            tags = decorate.split(',')
            tags = [t.strip() for t in tags if not t.strip().startswith('deploy_build') and not t.strip().startswith('deployed')]
            if not tags:
                line = line.replace('(' + decorate + ')', '')
            else:
                line = line.replace(decorate, ', '.join(tags))
        res += line + '\n'
    return res

def show_sha(sha):
    res = clean_up_decorate(cmd('git --no-pager log --color=always --pretty=format:"%Cgreen%H%Creset   %an %C(yellow)%d%Creset%n   %s%n" -1 ' + sha))
    res = res.replace("Samuel Russell", blue_str("Samuel Russell"))
    res = res.replace("Sam Russell", blue_str("Sam Russell"))
    print(res)
    #cmd('git --no-pager show --pretty=format:"%Cgreen%H%Creset   %an%n   %s%n" ' + sha + ' | head -n 3', noisy=True)

def show_shas(sha_first, sha_last, nmax=100):
    res = clean_up_decorate(cmd('git --no-pager log -n {} --color=always --pretty=format:"%Cgreen%H%Creset   %an %C(yellow)%d%Creset%n   %s%n" {}...{}'.format(nmax, sha_first, sha_last)))
    res = res.replace("Samuel Russell", blue_str("Samuel Russell"))
    res = res.replace("Sam Russell", blue_str("Sam Russell"))
    print(res)
    return res

def show_my_most_recent(fb):
    print('               ....\n')
    res = clean_up_decorate(cmd('git --no-pager log --color=always --author=samrussell --pretty=format:"%Cgreen%H%Creset   %an %C(yellow)%d%Creset%n   %s%n" -1 ' + fb))
    res = res.replace("Samuel Russell", blue_str("Samuel Russell"))
    res = res.replace("Sam Russell", blue_str("Sam Russell"))
    print(res)

def show_sha_grey(sha):
    res = cmd('git --no-pager log --pretty=format:"%H   %an%n   %s%n%Creset" -1 ' + sha)
    if "Samuel Russell" in res:
        ts = res.split("Samuel Russell")
        print(grey_str(ts[0]) + blue_str("Samuel Russell") + grey_str(ts[1]))
    else:
        print(grey_str(res))
    print('')

def show_sha_magenta(sha):
    res = cmd('git --no-pager log --pretty=format:"%C(magenta)%H%Creset   %an%n   %s%n" -1 ' + sha)
    res = res.replace(sha, magenta_str(sha))
    res = res.replace("Samuel Russell", blue_str("Samuel Russell"))
    res = res.replace("Sam Russell", blue_str("Sam Russell"))
    print(res)
    print('')

def fetch_commits_for_branch(branch, n):
    raw = cmd('git log ' + branch + ' --format=oneline -n ' + str(n))
    if 'not a git repository' in raw.lower():
        print(red_str('Not a git repository'))
        sys.exit(0)
    if 'unknown revision or path not in the working tree' in raw:
        return []
    res = []
    for l in raw.rstrip().split('\n'):
        if l.startswith('warning'):
            continue
        ls = l.split()
        sha = ls[0]
        title = " ".join(ls[1:])
        if 'These files were automatically checked in' in title:
            title = sha
        c = Commit(sha, title)
        res.append(c)
    return res

def fb_alternate():
    #print('trying alernate')
    branches_raw = cmd('git branch -vv').rstrip()
    branches = branches_raw.split('\n')
    for branch in branches:
        if branch.startswith('*'):
            m = re.search(r'\[(.*?)\]', branch)
            if m:
                return m.group(1)
            m = re.search(r'HEAD detached at (.+?)\)', branch)
            if m:
                #print("found deatched head", m.group(1))
                return m.group(1)
    # as a fallback, look if any of our local branches track an origin
    if 'origin' in branches_raw:
        return 'origin'
    return 'master'

###########################################################
#     Init and argv stuff
###########################################################
showall = argpop(sys.argv, "--all")
rows, cols = get_term_size()

# Read cache file
home = os.path.expanduser("~")
# TODO templatize by project
cachef = os.path.join(home, ".git_awesome_status")
cache = {}
if os.path.isfile(cachef):
    with open(cachef, 'r') as f:
        dat = f.read()
        js = json.loads(dat)

archived_branches = cache.get("archived_branches", [])

# Print a new line..... seems to help windows reset its coloring
print("")

###########################################################
#     Fetch info about the branch and remote branch
###########################################################

status = cmd('git status -bs').rstrip().split('\n')
if not status or len(status) == 0 or not status[0]:
    print(red_str("Not a git repo"))
    sys.exit(1)
branchline = status[0] + ' '
m = re.search(r'\.\.\.(.*?) ', branchline)
if m:
    fb = m.group(1)
    branchline = branchline.replace('...', ' ')
    current_branch = branchline.split()[1]
else:
    current_branch = branchline.split()[1]
    fb = fb_alternate()
if fb is None:
    raise Exception("never get here")

master = argpop(sys.argv, "--master")
if master:
    fb = "origin/master"
#print("current_branch", current_branch)
#print("fb", fb)

###########################################################
#     Fetch the log info about local HEAD and remote branch
###########################################################

second_try = False
tot_n = 100
origin_n = 200

while True:
    tot = fetch_commits_for_branch("", tot_n)
    totsha = [c.sha for c in tot]
    tottitle = [c.title for c in tot]

    if not fb:
        # not a remote-tracking branch
        for c in tot[0:6]:
            show_sha(c.sha)
        sys.exit(1)

    origin = fetch_commits_for_branch(fb, origin_n)
    originsha = [c.sha for c in origin]
    origintitle = [c.title for c in origin]

    # How many commits in each category
    made = [c for c in tot[0:50] if c.title not in origintitle]
    made_merged = [c for c in tot[0:50] if c.title in origintitle and c.sha not in originsha]
    missing = [c for c in origin[0:(tot_n-len(made))] if c.sha not in totsha and c.title not in tottitle]
    common = [c for c in origin if c.sha in totsha and c.title in tottitle]

    if len(made) + len(made_merged) < 15:
        break
    else:
        if second_try:
            # something is wierd
            break
        else:
            tot_n = 1000
            origin_n = 1200
            second_try = True

## Uncomment this line to run a fetch before very call, slower but shows a more accurate state #######
#cmd('git fetch')

###########################################################
#     print branch info
###########################################################
other_branches = cmd('git branch').strip().split('\n')
other_branches = [x.strip() for x in other_branches if not x.startswith('*')]
branches_n = len(other_branches)
other_branches = [x for x in other_branches if x not in archived_branches]
archived_n = len(other_branches) - branches_n

#max_len = max([len(x) for x in other_branches]) + 10
max_len = 50
branch_cols = cols / max_len

print
print('*' * (cols - 10))
if current_branch == "HEAD":
    print(magenta_str(bold_str('%30s' % "~~ HEAD detached ~~")))
else:
    print(blue_str(bold_str('%30s' % current_branch)))
branch_data = []
for branch in other_branches:
    try:
        stats = cmd('git show --pretty=format:"%ci %cr" ' + branch + ' -- | head -n 1').split(' ')
        dt = datetime.datetime.strptime(stats[0] + ' ' + stats[1], "%Y-%m-%d %H:%M:%S")
        age = stats[3] + ' ' + stats[4]
    except:
        dt = datetime.datetime.now()
        age = ''
    branch_data.append((branch, dt, age))

for idx, dat in enumerate(sorted(branch_data, key=itemgetter(1), reverse=True)):
    branch, dt, age = dat
    if 'minutes' in age or 'hours' in age:
        age = ''
    print('%30s ' % branch + grey_str('%-10s' % age), end='')
    if idx % branch_cols == 0:
        print('')
print('')
print('*' * (cols - 10))

###########################################################
#     print local status diffs
###########################################################
untracked = []
for l in status[1:]:
    if '??' in l:
        untracked.append(l)
    else:
        print(magenta_str(l))

if len(untracked) > 3:
    print(red_str(str(len(untracked)) + ' Untracked files ??'))
else:
    for u in untracked:
        print(red_str(u))
print('')

###########################################################
#     print commits cherry picked on top
###########################################################
done = 0
cp_but_merged = 0

if len(made) + len(made_merged) > 20:
    # something is wierd
    if len(origin) == 0:
        # we don't generally get here, since we fallback to master
        print(grey_str("    ********** (no origin) ************"))
    else:
        print(red_str("\nUnable to determine alignment with remote\n"))
    show_shas(totsha[0], totsha[8])
    sys.exit(1)

for c in tot[0:50]:
    if c in made:
        done += 1
        show_sha(c.sha)
    if c in made_merged:
        # Cherry picked and merged
        done += 1
        cp_but_merged += 1
        show_sha_magenta(c.sha)

# usually happens if there is no origin
if len(common) == 0:
    sys.exit(1)

if fb == "master":
    print(grey_str("    ********** " + fb + " ************"))
else:
    print(blue_str("    ********** " + fb + " ************"))

###########################################################
#     print commits in origin missing from HEAD'
###########################################################
if len(missing) > 5 and not showall:
    print(grey_str('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'))
    print(grey_str('   ' + str(len(missing)) + ' missing commits'))
    print(grey_str('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'))
    done += 2
elif len(missing) > 0:
    for c in missing:
        show_sha_grey(c.sha)
        done += 1

###########################################################
#     print merged commits in origin and HEAD
###########################################################

left = min(max(1, 10-done), len(common)-1)
originz = show_shas(common[0].sha, common[left].sha, nmax=left)

###########################################################
#     print my last merged commit if not in the above
###########################################################
if 'Samuel Russell' not in originz and 'Sam Russell' not in originz:
    show_my_most_recent(fb)
