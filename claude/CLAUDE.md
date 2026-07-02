- try to make things simple.  try to use fewer lines of code, and more straightforward code when possible as long as we dont have to sacrifice functionality

- if there is a sufficiently tricky issue, its okay to add some debug printing and re-run vs trying to guess the solution

- in python, avoid local/defered imports unless they're strictly necessary or asked for

- when adding tests, try to be judicious about how many we add.  Adding too many tests can lead to excssive change-detection

- Feature branches MUST have their upstream set to the repo's trunk, not to their own remote counterpart.  In Chromatic that means `origin/develop`; in most other repos `origin/main`.  Concretely, when creating or first pushing a feature branch use `git push origin HEAD && git branch --set-upstream-to=origin/develop` (or `origin/main`) — do NOT use plain `git push -u origin HEAD`, which sets upstream to `origin/<feature-branch>` and is wrong.  If you happen to notice an existing branch already tracking its own remote, mention it but don't auto-fix — that's a separate decision for me to make.  Rebase against the trunk by default, and push with `--force-with-lease` when a rebase has rewritten history.

- I run multiple Claude sessions across tmux windows against the same working tree, so the current branch can change between my prompts without you knowing.  At the start of each substantive task (anything that will edit files, commit, push, or create a PR), run `git branch --show-current` and compare against the branch you saw last time in this session.  If it changed, stop and confirm with me before doing anything — don't assume the new branch is intentional for this task.

- **Worktrees**: Git worktrees are permitted for parallel development on separate branches. However, never run builds, compile code, run tests, or invoke any build tooling (bazel, make, cmake, cargo, npm build, etc.) inside a worktree directory. All build and test operations must happen in the primary checkout. You may edit files, run git commands, and execute lightweight scripts in worktrees, but redirect any build/test work back to the main checkout.
