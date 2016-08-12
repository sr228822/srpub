#!/usr/bin/python

from utils import *
import sys

def show_sha(sha):
    cmd('git --no-pager log --name-status --pretty=format:"%Cgreen%H%Creset   %an%n   %s%n" -1 -U ' + sha + ' | head -n 3', noisy=True)
    #cmd('git --no-pager show --pretty=format:"%Cgreen%H%Creset   %an%n   %s%n" ' + sha + ' | head -n 3', noisy=True)

def show_sha_grey(sha):
    cmd('git --no-pager log --name-status --pretty=format:"%C(dim)%H   %an%n   %s%n%Creset" -1 -U ' + sha + ' | head -n 3', noisy=True)

def show_sha_magenta(sha):
    cmd('git --no-pager log --name-status --pretty=format:"%C(magenta)%H%Creset   %an%n   %s%n" -1 -U ' + sha + ' | head -n 3', noisy=True)

def git_remote_branch():
    try:
        m = cmd('cat "$(git rev-parse --show-toplevel)"/.git/config | grep merge | head -n 1').split()[-1]
    except:
        return None
    try:
        fb = cmd('git branch -a | grep ' + m + ' | head -n 1').split()[-1]
    except:
        # maybe just use the pure m branch
        #fb = 'origin'
        fb = 'remotes/origin/master'
    return fb

n = 100
k = 300
if 'kernel' in cmd('pwd'):
    #n = 300
    #k = 800
    n = 300
    k = 2000

showall = False
if len(sys.argv) > 1 and sys.argv[1] == '--all':
    showall = True

totraw = cmd("git log --format=oneline -n " + str(n))
if 'Not a git repository' in totraw:
    print red_str('Not a git repository')
    sys.exit(0)
totraw = totraw.rstrip().split('\n')
totsha = []
tottitle = []
for l in totraw:
    ls = l.split()
    sha = ls[0]
    title = " ".join(ls[1:])
    if 'These files were automatically checked in' in title:
        title = sha
    totsha.append(sha)
    tottitle.append(title)

## Uncomment this line to run a fetch before very call, slower but shows a more accurate state #######
#cmd('git fetch')

print '******************************************************************'
print blue_str(bold_str(cmd('git branch | grep -i --exclude=\*svn\* --color=never "*"')))
others = cmd('git branch | grep -i --exclude=\*svn\* --color=always -i --color=never -v "*" | column -c 90')
if others and len(others) > 0:
    print others
print '******************************************************************'
cmd('git status -s -uno', noisy=True)
untrck = cmd('git status -s | grep ??').split('\n')
if len(untrck) > 3:
    print red_str(str(len(untrck)) + ' Untracked files ??')
else:
    for u in untrck:
        print red_str(u)
print ''

fb = git_remote_branch()
if not fb:
    # not a remote-tracking branch
    for sha in totsha[0:6]:
        show_sha(sha)
    sys.exit(1)

originraw = cmd('git log ' + fb + ' --format=oneline -n ' + str(k))
originraw = originraw.rstrip().split('\n')
originsha = []
origintitle = []
for l in originraw:
    ls = l.split()
    sha = ls[0]
    title = " ".join(ls[1:])
    if 'These files were automatically checked in' in title:
        title = sha
    originsha.append(sha)
    origintitle.append(title)

done = 0
cp_but_merged = 0
# print commits cherry picked on top
for i in range(len(tottitle)):
    sha = totsha[i]
    title = tottitle[i]
    if title not in origintitle:
        # cherry picks or created
        done += 1
        show_sha(sha)
    if title in origintitle and sha not in originsha:
        # Cherry picked and merged
        done += 1
        cp_but_merged += 1
        show_sha_magenta(sha)
    if done > 25:
        print red_str("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\nSomething went wrong\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        break

print blue_str("    ********** origin TOT ************")

# print commits in origin missing from HEAD'
num_miss = 0
while True:
    sha = originsha[num_miss]
    title = origintitle[num_miss]
    if sha in totsha and title in tottitle:
        #print sha + ' ' + title + ' is first common'
        break
    num_miss += 1
num_miss -= cp_but_merged

if num_miss > 5 and not showall:
    print grey_str('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print grey_str('   ' + str(num_miss) + ' missing commits')
    print grey_str('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    done += 2
elif num_miss > 0:
    for i in range(len(origintitle)):
        sha = originsha[i]
        title = origintitle[i]
        if title not in tottitle:
            show_sha_grey(sha)
            done += 1
            num_miss -= 1
            if num_miss <= 0:
                break

left = max(1, 8-done)
for i in range(len(origintitle)):
    sha = originsha[i]
    title = origintitle[i]
    if title in tottitle and sha in totsha:
        show_sha(sha)
        left -= 1
        if left == 0:
            break

