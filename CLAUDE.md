# Environment
- Activate the samdev conda env before running commands: `conda activate samdev`.
- A non-login shell won't have the env on PATH, and `conda activate` does not
  persist between separate tool/shell invocations. If `make lint` / `make fix`
  fail with `ruff: No such file or directory` (the pre-commit hook hits this
  too), call the env binaries by absolute path, e.g.
  `/Users/samrussell/miniconda3/envs/samdev/bin/{python,ruff,pytest}`.

# Workflow
- This is a personal repo: commit and push directly to `main`, no feature
  branches or PRs needed.
- `make lint` checks code; `make fix` auto-fixes. `make lint` runs both
  `ruff check` and `ruff format --check`, so format files too (a new multi-line
  call that fits on one line will fail the format check).

# Layout & tooling
- Python tools live in `pytools/` and share helpers from `srutils.py`
  (`cmd`, `DiskCache`, coloring, time/format utils) and `colorstrings.py`.
  Shell aliases/functions are in `bashrc` (sourced as the user's rc file).
- `bashrc` logs every command to dated files in `~/.logs/` (redacted via
  `redact_secrets`). Useful for "what tools get used most" analysis.
- Tests are flat `test_*.py` pytest files next to the code (no central runner /
  `make test`); run a specific one with the env's `pytest`.
