#!/usr/bin/env python3
import argparse
import concurrent.futures
import datetime
import re
import sys
from operator import itemgetter
from pathlib import Path

from srutils import (
    my_email,
    name_aliases,
    is_windows,
    get_term_size,
    cmd,
    yes_or_no,
    DiskCache,
    set_verbose,
)

from colorstrings import (
    blue_str,
    cyan_str,
    grey_str,
    magenta_str,
    red_str,
    bold_str,
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
    # Skip config check on Linux
    if sys.platform.lower().startswith("linux"):
        return

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


def get_branch_remote_status() -> dict:
    """
    Returns a dict mapping branch name to remote status (by name match, ignoring tracking):
    - 'local_only': no same-named remote branch
    - 'has_remote': same-named remote branch exists
    - 'gone': same-named remote was deleted (stale local ref exists)
    """
    # Get actual remote branches from server
    ls_remote = cmd("git ls-remote --heads origin 2>/dev/null").strip()
    actual_remote = set()
    for line in ls_remote.split("\n"):
        if line and "\t" in line:
            ref = line.split("\t")[1]
            if ref.startswith("refs/heads/"):
                actual_remote.add(ref[len("refs/heads/"):])

    # Get local remote-tracking refs (may be stale)
    stale_refs = set()
    for line in cmd("git branch -r 2>/dev/null").strip().split("\n"):
        line = line.strip()
        if line.startswith("origin/") and " -> " not in line:
            stale_refs.add(line[len("origin/"):])

    # Classify each local branch by same-named remote status
    status = {}
    for line in cmd("git branch").strip().split("\n"):
        branch = line.lstrip("* ").strip()
        if not branch:
            continue
        if branch in stale_refs and branch not in actual_remote:
            status[branch] = "gone"  # had remote, now deleted
        elif branch in actual_remote:
            status[branch] = "has_remote"
        else:
            status[branch] = "local_only"

    return status


def color_branch_by_remote(branch: str, text: str, remote_status: dict) -> str:
    """Color text based on branch's remote status."""
    status = remote_status.get(branch, "local_only")
    if status == "gone":
        return red_str(text)
    elif status == "has_remote":
        return cyan_str(text)
    else:  # local_only
        return text  # white (default terminal color)


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
    parser.add_argument(
        "--no-remote-status", action="store_true",
        help="Disable branch coloring by remote status"
    )
    args = parser.parse_args()

    if args.verbose:
        set_verbose(True)

    showall = args.all
    rows, cols = get_term_size()
    root = Path(cmd("git rev-parse --show-toplevel").strip())
    repo_name = root.name

    # Initialize cache
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

    # Try to determine alignment with origin using efficient git commands
    if not fb:
        # Not a remote-tracking branch
        tot = fetch_commits_for_branch("", 6)
        for c in tot[:6]:
            show_sha(c.sha)
        sys.exit(1)

    # Use merge-base to efficiently find common ancestor
    merge_base = cmd(f"git merge-base HEAD {fb}").strip()

    # Early exit if merge-base fails (e.g., no common history)
    if not merge_base or "fatal" in merge_base.lower():
        print(red_str("Unable to find common ancestor with remote"))
        tot = fetch_commits_for_branch("", 6)
        for c in tot[:6]:
            show_sha(c.sha)
        sys.exit(1)

    # Count commits efficiently
    commits_ahead_raw = cmd(f"git rev-list --count {fb}..HEAD").strip()
    commits_behind_raw = cmd(f"git rev-list --count HEAD..{fb}").strip()

    try:
        commits_ahead = int(commits_ahead_raw)
        commits_behind = int(commits_behind_raw)
    except ValueError:
        # Fallback if counting fails
        commits_ahead = 0
        commits_behind = 0

    # Fetch only the commits we need to display
    # Get commits on current branch not in upstream (made)
    if commits_ahead > 0:
        made = fetch_commits_for_branch("", min(commits_ahead + 10, 50))
        made = made[:commits_ahead]
    else:
        made = []

    # Get commits in upstream not in current branch (missing)
    # We don't need to fetch all missing commits, just enough to display or count
    # git rev-list --count already told us the exact count
    if commits_behind > 0:
        # Only fetch commits if we're going to display them (when count is small)
        # Otherwise we'll just show the count
        if commits_behind <= 100:
            missing_shas = cmd(f"git rev-list HEAD..{fb}").strip().split("\n")
            missing = []
            for sha in missing_shas:
                missing.extend(fetch_commits_for_branch(sha, 1))
        else:
            # For large numbers, create placeholder objects with the count
            # We'll handle display differently below
            missing = []
            # Just need the count, which we already have in commits_behind
    else:
        missing = []

    # Check for cherry-picked commits (same title, different sha)
    if made:
        origin = fetch_commits_for_branch(fb, min(commits_behind + 50, 200))
        originsha = [c.sha for c in origin]
        origintitle = [c.title for c in origin]
        made_merged = [
            c for c in made if (c.title in origintitle and c.sha not in originsha)
        ]
        made = [c for c in made if c.title not in origintitle]
    else:
        made_merged = []

    # Get common commits for display (starting from merge base)
    common = fetch_commits_for_branch(merge_base, 15)

    # Show branches
    other_branches = cmd("git branch").strip().split("\n")
    other_branches = [x.strip() for x in other_branches if not x.startswith("*")]
    if args.all:
        archived_branches = []
    other_branches = [x for x in other_branches if x not in archived_branches]

    # Calculate column width based on longest branch name
    max_branch_len = max((len(b) for b in other_branches), default=20)
    max_branch_len = max(max_branch_len, len(current_branch), 20)  # at least 20
    age_width = 11  # space + 10 char age field
    col_width = max_branch_len + age_width
    branch_cols = max(1, cols // col_width)
    # If only 1 col fits, use full width; otherwise cap at 3 columns
    branch_cols = min(3, branch_cols)

    print()
    print("*" * (cols - 10))
    if current_branch == "HEAD":
        print(magenta_str(bold_str(f"%{max_branch_len}s" % "~~ HEAD detached ~~")))
    else:
        print(blue_str(bold_str(f"%{max_branch_len}s" % current_branch)))

    # Get remote status if flag enabled
    remote_status = get_branch_remote_status() if not args.no_remote_status else {}

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
        # Pad before coloring so ANSI codes don't affect alignment
        padded_branch = f"%{max_branch_len}s" % branch
        if not args.no_remote_status:
            padded_branch = color_branch_by_remote(branch, padded_branch, remote_status)
        print(padded_branch + " " + grey_str("%-10s" % age), end="")
        if (idx + 1) % branch_cols == 0 or idx == len(branch_data) - 1:
            print("")

    if archived_branches:
        print(grey_str("%30s" % f"{len(archived_branches)} archived branches"))

    print("*" * (cols - 10))

    # Print local status diffs
    untracked = [line for line in status[1:] if "??" in line]
    tracked = [line for line in status[1:] if "??" not in line]
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

    for c in made:
        done += 1
        show_sha(c.sha)

    for c in made_merged:
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
    # Use the actual count from git rev-list instead of len(missing)
    if commits_behind > 5 and not showall:
        print(grey_str("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"))
        print(grey_str("   " + str(commits_behind) + " missing commits"))
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
    elif len(common) == 1:
        originz = show_sha(common[0].sha)
    else:
        originz = ""

    # Print last merged commit by me if not already shown
    if not any(alias in originz for alias in name_aliases):
        show_my_most_recent(fb)


if __name__ == "__main__":
    main()
