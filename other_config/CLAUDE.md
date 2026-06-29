# Personal preferences

## Documenting test results / command output

When writing up test results or command output — e.g. a PR's "How Has This Been
Tested?" section, or a summary of a run — lead with a short prose **description**,
then follow it with a **single block of raw terminal output** in a fenced code
block. Paste the output wholesale; use `...` on its own line to elide irrelevant
lines.

Avoid interleave prose with output line-by-line (no "ran X → it said Y, then
ran Z → it said W" style). Description first, then the terminal block.
