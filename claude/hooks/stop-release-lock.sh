#!/usr/bin/env bash
# Stop hook: release the repo lock when Claude finishes a turn.

input=$(cat)
session_id=$(echo "$input" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('session_id','unknown'))" 2>/dev/null)
[ -z "$session_id" ] && session_id="unknown"

SRPUB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
bash "$SRPUB_DIR/claude/repo-lock.sh" release "$session_id"
exit 0
