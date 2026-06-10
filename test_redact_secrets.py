#!/usr/bin/env python3
"""Tests for the bash-history secret redaction in bashrc.

These exercise the *actual* `redact_secrets` shell function from bashrc (by
extracting and sourcing just that function), so the tests stay in sync with the
real implementation rather than duplicating its regexes.
"""

import os
import subprocess
import tempfile

import pytest

BASHRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bashrc")


def _extract_redact_function() -> str:
    """Pull just the redact_secrets() function text out of bashrc.

    Extracting and sourcing only this function avoids triggering the rest of
    bashrc's startup side effects, while still testing the real implementation.
    """
    lines = open(BASHRC).read().splitlines()
    start = next(i for i, ln in enumerate(lines) if ln.startswith("redact_secrets() {"))
    end = next(i for i in range(start + 1, len(lines)) if lines[i] == "}")
    return "\n".join(lines[start : end + 1])


# Write the function to a temp file once; the tests source this file.
_FN_FILE = tempfile.NamedTemporaryFile("w", suffix=".sh", delete=False)
_FN_FILE.write(_extract_redact_function() + "\n")
_FN_FILE.flush()


def redact(cmd: str, no_redact: bool = False) -> str:
    """Run a line through bashrc's redact_secrets and return the result."""
    env = dict(os.environ)
    env["SRPUB_NO_REDACT"] = "1" if no_redact else "0"
    out = subprocess.run(
        ["bash", "-c", f'source "{_FN_FILE.name}"; redact_secrets "$1"', "bash", cmd],
        capture_output=True,
        text=True,
        env=env,
    )
    assert out.returncode == 0, out.stderr
    return out.stdout.rstrip("\n")


# (command, substring of the secret that MUST be gone, substrings that MUST stay)
SHOULD_REDACT = [
    (
        "export MY_PASSWORD=supersecret123456",
        "rsecret123456",
        ["export MY_PASSWORD=", "REDACTED"],
    ),
    (
        "export GITHUB_TOKEN=ghp_abcdefimportantsecret",
        "efimportantsecret",
        ["GITHUB_TOKEN=", "REDACTED"],
    ),
    (
        'curl -H "Authorization: Bearer abcd1234567890tokenvalue"',
        "567890tokenvalue",
        ["Bearer abcd", "REDACTED"],
    ),
    (
        'curl -H "Authorization: Basic dXNlcjpsb25nc2VjcmV0cGFzcw=="',
        "c2VjcmV0cGFzcw",
        ["Basic dXNl", "REDACTED"],
    ),
    (
        "aws configure set x AKIAIOSFODNN7EXAMPLE",
        "ODNN7EXAMPLE",
        ["AKIAIOSF", "REDACTED"],
    ),
    (
        "mysql -u root -phunter2supersecret mydb",
        "hunter2supersecret",
        ["mysql -u root -p", "mydb", "REDACTED"],
    ),
    (
        "curl -u admin:Pa55w0rdLongSecret https://x",
        "Pa55w0rdLongSecret",
        ["curl -u admin:", "https://x", "REDACTED"],
    ),
    (
        "curl --user bob:supersecretpw https://x",
        "supersecretpw",
        ["--user bob:", "REDACTED"],
    ),
    (
        "psql postgres://user:longpassword123@host/db",
        "longpassword123",
        ["postgres://user:", "@host/db", "REDACTED"],
    ),
    (
        "git clone https://sam:ghp_longtokenvalue123@github.com/x/y",
        "longtokenvalue123",
        ["https://sam:", "@github.com/x/y", "REDACTED"],
    ),
]

# Commands that contain no secret and must pass through byte-for-byte. Several
# are deliberately shaped to trip the redaction rules (uid:gid, -p flags, -u).
SHOULD_NOT_CHANGE = [
    "mkdir -p /tmp/foo/bar",
    "cp -p src dst",
    "ssh -p 2222 host",
    "docker run -u 1000:1000 img",
    "git log -p HEAD",
    "grep -u pattern file",
    "ls -la /home/user",
    "curl https://example.com/path",
    "echo hello world",
    "python train.py --epochs 100",
]


@pytest.mark.parametrize("cmd,leaked,kept", SHOULD_REDACT)
def test_secret_is_redacted(cmd, leaked, kept):
    out = redact(cmd)
    assert leaked not in out, f"secret leaked: {out!r}"
    for k in kept:
        assert k in out, f"expected {k!r} preserved in {out!r}"


@pytest.mark.parametrize("cmd", SHOULD_NOT_CHANGE)
def test_safe_command_unchanged(cmd):
    assert redact(cmd) == cmd


def test_no_redact_escape_hatch_passes_through():
    secret = "export MY_PASSWORD=supersecret123456"
    assert redact(secret, no_redact=True) == secret


def test_keeps_only_first_four_chars_of_value():
    # Documents the intended behavior: enough prefix to recognize the value,
    # not enough to use it.
    out = redact("export API_KEY=abcd1234verysecretvalue")
    assert "abcd" in out
    assert "1234verysecretvalue" not in out


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
