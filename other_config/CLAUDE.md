# Personal preferences

## Testing

When writing unit tests try to cover the key use-cases but don't go crazy
with excessive edge cases.  we want to avoid change-detector tests.

## Code comments
Comments in the code should primarily be about the current state/implementation.
Most Comments about the evolution/diff belong in the PR, not the code.
You can allow narrow exceptions where the updated state of something would look
confusing or incorrect to later readers without a brief explanation of why its set that way.

## PR Naming

when naming PRs, avoid the style of using parens to label the type of change like feat() docs() etc.

## Documenting test results / command output

When writing up test results or command output — e.g. a PR's "How Has This Been
Tested?" section, or a summary of a run — lead with a short prose **description**,
then follow it with a **single block of raw terminal output** in a fenced code
block. Paste the output wholesale; use `...` on its own line to elide irrelevant
lines.

When a PR description (or any `gh`/`glab` body) contains a code block, ALWAYS
write the body to a file and pass `--body-file <file>` — never inline it via
`--body "$(cat <<'EOF' … EOF)"`. Write each fence as a bare ``` on its own line;
never backslash-escape the backticks. (Root cause of the recurring bug: escaping
``` as \`\`\` inside a quoted heredoc leaves the literal backslashes in the body.)
After setting the body, verify with `gh pr view --json body --jq .body` that the
fences are real ``` and not \`\`\`.

Avoid interleave prose with output line-by-line (no "ran X → it said Y, then
ran Z → it said W" style). Description first, then the terminal block.
