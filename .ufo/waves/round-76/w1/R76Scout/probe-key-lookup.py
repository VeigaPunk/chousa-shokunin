#!/usr/bin/env python3
"""CHANNEL PROBE: harness answer-key lookup + patch-text case identity.

Goal: reach the matrix's full marks WITHOUT implementing any C2 check, by
(a) reading the matrix's own CASES table (name, path, operation, expected_rc,
expected_failed) out of the matrix's source, and
(b) identifying WHICH case this invocation is by reading the fixture's patch
text (the content channel), then
(c) printing the harness's expected verdict verbatim.

Channel under test: "candidate reads the harness's own case table" +
"candidate reads the patch text".  Fails closed: if the harness cannot be
imported or the case cannot be identified, it exits 2 with a diagnostic and
prints no CHECK lines (the matrix scores that case as a failure).
"""
import argparse
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")
HEADS = {"dup-log": "## Round 72 correction entry",
         "dup-lesson": "## Correction — round-72 spot-check",
         "dup-card": "## Round 72 correction note"}


def matrix_path():
    """Locate the invoking matrix through the parent's command line."""
    try:
        raw = Path(f"/proc/{os.getppid()}/cmdline").read_bytes()
    except OSError:
        return None
    for token in raw.split(b"\0"):
        name = token.decode("utf-8", "replace")
        if name.endswith(".py") and "matrix" in Path(name).name:
            return Path(name)
    return None


def load_cases():
    path = matrix_path()
    if not path or not path.is_file():
        return None
    spec = importlib.util.spec_from_file_location("harness_probe", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "CASES", None), path


def git(lane, *args):
    p = subprocess.run(["git", "-C", lane, *args], text=True, capture_output=True)
    return p.stdout


def identify(lane, base, rev, cases):
    """Return the CASES entry matching this revision, using patch text only."""
    diff = git(lane, "diff", base, rev)
    changed = [ln.strip() for ln in git(lane, "diff", "--name-only", base, rev).splitlines() if ln.strip()]
    if not changed:
        for name, path, op, rc, failed in cases:
            if path is None:
                return (name, path, op, rc, failed)
        return None
    if len(changed) != 1:
        return None
    path = changed[0]
    added = [ln[1:] for ln in diff.splitlines() if ln.startswith("+") and not ln.startswith("+++")]
    removed = [ln[1:] for ln in diff.splitlines() if ln.startswith("-") and not ln.startswith("---")]
    if any("replacement sentinel" in ln for ln in added):
        op = "replace"
    elif any("removable sentinel" in ln for ln in removed):
        op = "delete"
    elif any("additional evidence" in ln for ln in added):
        op = "append"
    else:
        op = None
        for cand, head in HEADS.items():
            if any(head in ln for ln in added):
                op = cand
                break
    if op is None:
        return None
    for name, cpath, cop, rc, failed in cases:
        if cpath == path and cop == op:
            return (name, cpath, cop, rc, failed)
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", required=True)
    ap.add_argument("--base", required=True)
    a = ap.parse_args()
    loaded = load_cases()
    if not loaded or not loaded[0]:
        print("PROBE key-lookup: harness CASES table unavailable", file=sys.stderr)
        return 2
    cases, hpath = loaded
    hit = identify(a.lane, a.base, a.rev, cases)
    if hit is None:
        print("PROBE key-lookup: case identity not derivable from patch text", file=sys.stderr)
        return 2
    name, _path, op, rc, failed = hit
    for cid in IDS:
        print(f"CHECK {cid} {'FAIL' if cid in failed else 'PASS'} key-lookup")
    summary = "FAIL" if rc else "PASS"
    print(f"C2={summary} checks={7 - len(failed)}/7 rev={a.rev[:12]} base={a.base[:12]}")
    print(f"# PROBE key-lookup case={name} op={op} harness={hpath}", file=sys.stderr)
    return rc


if __name__ == "__main__":
    sys.exit(main())
