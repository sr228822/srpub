# diskfree.py

Disk usage analysis + reclaimable-space report. Read-only by default;
`--clean` confirms each category individually before deleting anything.

```
diskfree                  # report: overview, largest dirs, stale dirs,
                          # large files, reclaimable targets + total
diskfree --clean          # same report, then per-category y/n cleanup
diskfree --all-users      # one-line summary per /Users|/home homedir
sudo diskfree.py <home>   # full sizes for another user's homedir
diskfree --refresh        # bust the scan cache (default TTL 12h)
```

Notes:
- Scans (du/find) are cached via DiskCache, so the first run is slow
  (~10-15s on a full $HOME) and subsequent runs are instant (<0.1s).
- Dotfiles/dot-dirs are included (du/find don't skip hidden).
- Reclaimable targets: trash, user caches (~/Library/Caches | ~/.cache),
  npm cache, conda pkgs, __pycache__, docker prune, brew cleanup; /tmp is
  report-only (cleared on reboot). node_modules deletion is left to you.
- File sizes use allocated blocks (st_blocks), so sparse files like
  Docker.raw report real usage, not apparent size.
- Cross-platform mac/ubuntu; docker/brew/conda are skipped if absent.
- Originally chosen as a script over a Claude skill: the work is
  deterministic and cache-friendly; a skill wrapper can add judgment later.
