#!/usr/bin/env bash
# repo-lock.sh — lightweight per-repo Claude session lock.
#
# Lock file: .git/.claude-lock  (per-repo, never committed)
# Format:    session_id timestamp_epoch branch
#
# Staleness: if the timestamp is > STALE_SECS old the lock is expired.
# PreToolUse refreshes the timestamp on every tool call, so a session
# that crashes or goes idle lets the lock expire automatically.
#
# Subcommands:
#   acquire SESSION_ID   — take/refresh lock; warns/blocks if held by another
#   release SESSION_ID   — remove lock if we own it
#   status               — print who holds the lock (if anyone)

STALE_SECS=300  # 5 minutes

_lock_file() {
    local root
    root=$(git rev-parse --show-toplevel 2>/dev/null) || return 1
    echo "${root}/.git/.claude-lock"
}

_now() { date +%s; }
_branch() { git branch --show-current 2>/dev/null; }

_read_lock() {
    local lf="$1"
    [ -f "$lf" ] || return 1
    read -r lock_sid lock_ts lock_branch < "$lf"
}

_is_stale() {
    local ts="$1"
    [ $(( $(_now) - ts )) -gt "$STALE_SECS" ]
}

cmd="$1"
my_sid="$2"

lf=$(_lock_file) || { echo "repo-lock: not in a git repo" >&2; exit 0; }

case "$cmd" in
acquire)
    branch=$(_branch)
    if _read_lock "$lf"; then
        if [ "$lock_sid" = "$my_sid" ] || _is_stale "$lock_ts"; then
            echo "$my_sid $(_now) $branch" > "$lf"
        else
            age=$(( $(_now) - lock_ts ))
            echo "locked: ${lock_sid} ${lock_ts} ${lock_branch}" >&1
            exit 1
        fi
    else
        echo "$my_sid $(_now) $branch" > "$lf"
    fi
    ;;

release)
    if _read_lock "$lf" && [ "$lock_sid" = "$my_sid" ]; then
        rm -f "$lf"
    fi
    ;;

status)
    if _read_lock "$lf"; then
        age=$(( $(_now) - lock_ts ))
        if _is_stale "$lock_ts"; then
            echo "stale lock: session ${lock_sid} on branch '${lock_branch}' (${age}s ago)"
        else
            echo "active lock: session ${lock_sid} on branch '${lock_branch}' (${age}s ago)"
        fi
    else
        echo "no lock"
    fi
    ;;

*)
    echo "Usage: repo-lock.sh acquire|release|status [session_id]" >&2
    exit 1
    ;;
esac
