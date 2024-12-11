#!/usr/bin/env python3
import argparse
import concurrent.futures
import datetime
import json
import os
import re
import sys
from operator import itemgetter

from srutils import (
    my_email,
    name_aliases,
    is_windows,
    get_term_size,
    cmd,
    yes_or_no,
    blue_str,
    grey_str,
    magenta_str,
    red_str,
    bold_str,
    DiskCache,
    set_verbose,
)


###########################################################
#     Helper Classes & Data
###########################################################
class Commit:
    """Represents a single commit with a SHA and title."""

    def __init__(self, sha: str, title: str):
        self.sha = sha
        self.title = title


git_config_defaults = {
    "user.email": my_email,
    "user.name": name_aliases[0],
    "core.editor": "vim",
}


###########################################################
#     Helper Functions
###########################################################
def clean_up_decorate(lines: str) -> str:
    """
    Cleans up parentheses decorations from git log lines, removing tags related to deployments.
    """
    result_lines = []
    for line in lines.split("\n"):
        match = re.search(r"\((.+?)\)", line)
        if match:
            decorate = match.group(1)
            tags = [t.strip() for t in decorate.split(",")]
            filtered_tags = [
                t
                for t in tags
                if not t.startswith("deploy_build") and not t.startswith("deployed")
            ]
            if not filtered_tags:
                line = line.replace(f"({decorate})", "")
            else:
                line = line.replace(decorate, ", ".join(filtered_tags))
        result_lines.append(line)
    return "\n".join(result_lines) + "\n"


def check_config():
    """
    Check if global git config is set for user email, user name, etc.
    If not, prompt the user to set it.
    """
    print("1st run checking git config:")
    for key, value in git_config_defaults.items():
        current_val = cmd(f"git config --global --get {key}")
        print(f"\tgit config {key} : {current_val}")
        if not current_val:
            if yes_or_no(f"git config --global {key} not set! Set it to {value} now?"):
                cmd(f"git config --global {key} {value}")


def git_op_colored(command: str) -> str:
    """
    Run a git command, clean up decorated lines, highlight aliases, and print the result.
    On Windows, run with straight_through once for colors, then return normal output.
    """
    if is_windows:
        cmd(command, straight_through=True)
        return cmd(command)

    raw = cmd(command)
    cleaned = clean_up_decorate(raw)
    for alias in name_aliases:
        cleaned = cleaned.replace(alias, blue_str(alias))
    print(cleaned)
    return cleaned


def show_sha(sha: str):
    """
    Show details of a single commit (with colors) by SHA.
    """
    command = (
        f'git --no-pager log --color=always --pretty=format:"%Cgreen%H%Creset   %an '
        f'%C(yellow)%d%Creset%n   %s%n" -1 {sha}'
    )
    return git_op_colored(command)


def show_shas(sha_first: str, sha_last: str, nmax: int = 100) -> str:
    """
    Show details of a range of commits between sha_first and sha_last.
    """
    command = (
        f"git --no-pager log -n {nmax} --color=always "
        f'--pretty=format:"%Cgreen%H%Creset   %an %C(yellow)%d%Creset%n   %s%n" '
        f"{sha_first}...{sha_last}"
    )
    return git_op_colored(command)


def show_my_most_recent(fb: str):
    """
    Show the most recent commit by the author Russell on the given branch.
    """
    command = (
        f"git --no-pager log --color=always --author=Russell "
        f'--pretty=format:"%Cgreen%H%Creset   %an %C(yellow)%d%Creset%n   %s%n" -1 {fb}'
    )
    return git_op_colored(command)


def show_sha_grey(sha: str):
    """
    Show a commit with a grey-style highlight.
    """
    command = f'git --no-pager log --pretty=format:"%H   %an%n   %s%n%Creset" -1 {sha}'
    if is_windows:
        cmd(command, straight_through=True)
        return

    res = cmd(command)
    for alias in name_aliases:
        if alias in res:
            parts = res.split(alias)
            res = grey_str(parts[0]) + blue_str(alias) + grey_str(parts[1])
        else:
            res = grey_str(res)
    print(res)
    print("")


def show_sha_magenta(sha: str):
    """
    Show a commit with a magenta-style highlight.
    """
    command = f'git --no-pager log --pretty=format:"%C(magenta)%H%Creset   %an%n   %s%n" -1 {sha}'
    if is_windows:
        cmd(command, straight_through=True)
        return

    res = cmd(command)
    res = res.replace(sha, magenta_str(sha))
    for alias in name_aliases:
        res = res.replace(alias, blue_str(alias))
    print(res)
    print("")


def fetch_commits_for_branch(branch: str, n: int) -> list:
    """
    Fetch up to n commits (sha and title) for the given branch.
    If the branch doesn't exist or we're not in a repo, exit gracefully.
    """
    raw = cmd(f"git log {branch} --format=oneline -n {n}")
    if "not a git repository" in raw.lower():
        print(red_str("Not a git repository"))
        sys.exit(1)
    if "unknown revision or path not in the working tree" in raw:
        return []

    commits = []
    for line in raw.rstrip().split("\n"):
        if line.startswith("warning"):
            continue
        parts = line.split()
        sha = parts[0]
        title = " ".join(parts[1:])
        # Adjust title if it matches a known pattern
        if "These files were automatically checked in" in title:
            title = sha
        commits.append(Commit(sha, title))
    return commits


def fb_alternate() -> str:
    """
    Try to find a fallback remote branch if not directly known.
    """
    branches_raw = cmd("git branch -vv").rstrip()
    for branch_line in branches_raw.split("\n"):
        if branch_line.startswith("*"):
            # Try to extract something from brackets [remote/branch]
            match = re.search(r"\[(.*?)\]", branch_line)
            if match:
                return match.group(1)
            # Or HEAD detached scenario
            match = re.search(r"HEAD detached at (.+?)\)", branch_line)
            if match:
                return match.group(1)
    if "origin" in branches_raw:
        return "origin"
    return "master"


def get_branch_age(branch: str):
    """
    Return a tuple of (branch, datetime, age_str).
    """
    try:
        stats = (
            cmd(f'git log -n 1 --pretty=format:"%ci %cr" {branch} -- | head -n 1')
            .strip()
            .split(" ")
        )
        dt = datetime.datetime.strptime(stats[0] + " " + stats[1], "%Y-%m-%d %H:%M:%S")
        age = stats[3] + " " + stats[4] if len(stats) > 4 else ""
    except Exception:
        dt = datetime.datetime.now()
        age = ""
    return branch, dt, age


###########################################################
#     Main Logic
###########################################################
def main():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--archive", type=str, required=False, help="Archive the specified branch"
    )
    parser.add_argument("--master", action="store_true", help="Use origin/master as fb")
    parser.add_argument("--all", action="store_true", help="Show all missing commits")
    parser.add_argument("--verbose", action="store_true", help="Verbose debug logs")
    args = parser.parse_args()

    if args.verbose:
        set_verbose(True)

    showall = args.all
    rows, cols = get_term_size()
    root = cmd("git rev-parse --show-toplevel")
    repo_name = root.strip().split("/")[-1]

    # Initialize cache
    home = os.path.expanduser("~")
    cache = DiskCache(f"git_status_{repo_name}", verbose=args.verbose)

    # Check git config if not done before
    if not cache.get("config_checked"):
        check_config()
        cache.set("config_checked", True)

    # Handle archive action
    archived_branches = cache.get("archived_branches", [])
    if args.archive:
        archived_branches.append(args.archive)
        cache.set("archived_branches", archived_branches)
        sys.exit(0)

    # Print a new line to help reset coloring on Windows
    print("")
    status = cmd("git status -bs").rstrip().split("\n")
    if not status or not status[0]:
        print(red_str("Not a git repo"))
        sys.exit(1)

    branchline = status[0] + " "
    match = re.search(r"\.\.\.(.*?) ", branchline)
    if match:
        fb = match.group(1)
        branchline = branchline.replace("...", " ")
        current_branch = branchline.split()[1]
    else:
        current_branch = branchline.split()[1]
        fb = fb_alternate()

    if fb is None:
        raise Exception("Failed to detect forward-branch")

    if args.master:
        fb = "origin/master"

    # Try to determine alignment with origin
    second_try = False
    tot_n = 100
    origin_n = 200

    while True:
        tot = fetch_commits_for_branch("", tot_n)
        totsha = [c.sha for c in tot]
        tottitle = [c.title for c in tot]

        if not fb:
            # Not a remote-tracking branch
            for c in tot[:6]:
                show_sha(c.sha)
            sys.exit(1)

        origin = fetch_commits_for_branch(fb, origin_n)
        originsha = [c.sha for c in origin]
        origintitle = [c.title for c in origin]

        made = [c for c in tot[:50] if c.title not in origintitle]
        made_merged = [
            c for c in tot[:50] if (c.title in origintitle and c.sha not in originsha)
        ]
        missing = [
            c
            for c in origin[: (tot_n - len(made))]
            if c.sha not in totsha and c.title not in tottitle
        ]
        common = [c for c in origin if (c.sha in totsha and c.title in tottitle)]

        if len(made) + len(made_merged) < 15:
            break
        else:
            if second_try:
                # Something is weird, break anyway
                break
            else:
                tot_n = 1000
                origin_n = 1200
                second_try = True

    # Show branches
    other_branches = cmd("git branch").strip().split("\n")
    other_branches = [x.strip() for x in other_branches if not x.startswith("*")]
    if args.all:
        archived_branches = []
    other_branches = [x for x in other_branches if x not in archived_branches]

    max_len = 50
    branch_cols = min(3, max(1, int(cols / max_len)))

    print()
    print("*" * (cols - 10))
    if current_branch == "HEAD":
        print(magenta_str(bold_str("%30s" % "~~ HEAD detached ~~")))
    else:
        print(blue_str(bold_str("%30s" % current_branch)))

    # Retrieve branch ages concurrently
    branch_data = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_branch_age, b) for b in other_branches]
        for future in concurrent.futures.as_completed(futures):
            branch_data.append(future.result())

    branch_data_sorted = sorted(branch_data, key=itemgetter(1), reverse=True)
    for idx, (branch, dt, age) in enumerate(branch_data_sorted):
        # If age is in hours/minutes, optionally skip showing it.
        if "minutes" in age or "hours" in age:
            age = ""
        print("%30s " % branch + grey_str("%-10s" % age), end="")
        if (idx + 1) % branch_cols == 0 or idx == len(branch_data) - 1:
            print("")

    if archived_branches:
        print(grey_str("%30s" % f"{len(archived_branches)} archived branches"))

    print("*" * (cols - 10))

    # Print local status diffs
    untracked = [l for l in status[1:] if "??" in l]
    tracked = [l for l in status[1:] if "??" not in l]
    for line in tracked:
        print(magenta_str(line))

    if len(untracked) > 3:
        print(red_str(f"{len(untracked)} Untracked files ??"))
    else:
        for u in untracked:
            print(red_str(u))
    print("")

    # Print commits cherry-picked on top
    done = 0
    cp_but_merged = 0

    if len(made) + len(made_merged) > 20:
        # Something is weird
        if len(origin) == 0:
            print(grey_str("    ********** (no origin) ************"))
        else:
            print(red_str("\nUnable to determine alignment with remote\n"))
        show_shas(totsha[0], totsha[8])
        sys.exit(1)

    for c in tot[:50]:
        if c in made:
            done += 1
            show_sha(c.sha)
        if c in made_merged:
            done += 1
            cp_but_merged += 1
            show_sha_magenta(c.sha)

    # Usually happens if there is no origin
    if not common:
        sys.exit(1)

    if fb == "master":
        print(grey_str("    ********** " + fb + " ************"))
    else:
        print(blue_str("    ********** " + fb + " ************"))

    # Print commits in origin missing from HEAD
    if len(missing) > 5 and not showall:
        print(grey_str("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"))
        print(grey_str("   " + str(len(missing)) + " missing commits"))
        print(grey_str("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"))
        done += 2
    else:
        for c in missing:
            show_sha_grey(c.sha)
            done += 1

    # Print merged commits
    left = min(max(1, 10 - done), len(common) - 1)
    if len(common) > 1:
        originz = show_shas(common[0].sha, common[left].sha, nmax=left)
    else:
        originz = ""

    # Print last merged commit by me if not already shown
    if not any(alias in originz for alias in name_aliases):
        show_my_most_recent(fb)


if __name__ == "__main__":
    main()
