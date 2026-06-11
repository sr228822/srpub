# Claude skills

Git-tracked Claude Code skills, installed onto each machine by quicksetup.sh
as per-skill symlinks into `~/.claude/skills/`.

To add a skill:

```
claude/skills/<skill-name>/SKILL.md     # required
claude/skills/<skill-name>/<helpers>    # optional scripts/templates
```

SKILL.md starts with frontmatter:

```markdown
---
name: skill-name
description: One line saying when Claude should use this skill.
---

Instructions for the skill...
```

Then run `bash quicksetup.sh` (or just the Claude config section) to link it.
Because installs are symlinks, edits here apply everywhere on git pull; no
re-install needed. Machine-local skills can live alongside the symlinks in
`~/.claude/skills/` without conflict.
