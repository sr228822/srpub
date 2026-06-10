Last open item — #4 diskfree.py — my take on script vs skill:

Build it as a script first; a skill is at most a thin layer on top later. Reasoning: the bulk of this is deterministic and benefits from caching (a du scan is slow — exactly what your DiskCache is for), needs to run identically on mac+ubuntu, and fits the pytools idiom. A Claude skill can't cache and re-derives context every run; its only edge is judgment ("this 40GB folder looks like a stale build"), which a script can approximate with heuristics (size + age + known patterns). So: script does ~90% deterministically; optionally add a skill wrapper afterward that runs it and adds AI judgment on "is this safe to delete?"

Proposed pytools/diskfree.py:
- Report (default, read-only): cached du of configurable roots (default $HOME); top-N largest dirs/files; "stale & large" heuristic (big + old mtime).
- Known reclaimable targets with live sizes: /tmp, trash, ~/Library/Caches (mac) / ~/.cache (linux), pip/conda/npm/yarn caches, __pycache__, node_modules, .DS_Store, docker system df, brew cleanup -n. Prints a reclaimable total.
- --clean: dry-run by default; actually deletes only with a confirm prompt (reusing srutils.yes_or_no). Deletion is destructive, so it's gated and never the default.
- Cross-platform per the convention (OS-specific cache paths, skip docker/brew gracefully if absent).
