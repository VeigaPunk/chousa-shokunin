#!/usr/bin/env python3
"""Round-77 correction counter — supersession of the false sentence in the r76 claims file.

Unit under test: `corpus/evidence/round76/claims.md`. The round-76 non-author spot-check
routed defect 3: the frozen prose says routed defect 4 "is honoured by naming the controls
revision in every receipt" while the prefreeze receipts name worktree digests, not the
controls revision (`corpus/lessons/round-76-verifier-spotcheck.md:160-163`). The frozen file
is the artifact a successor reads, so the sentence is superseded by an append-only
correction block in that same file; the frozen bytes are quoted, never rewritten.

Five checks, one command:

  C3-1 FROZEN_TEXT      the superseded clause is still present verbatim (whitespace-normalised,
                        because the clause is split across lines 10-11) — a rewrite fails closed
  C3-2 SUPERSESSION     a `## Correction — round-76 claims prose` heading exists in that file
  C3-3 BOTH_STATES      inside that block the superseded clause is quoted AND the corrected
                        fact is stated ("worktree digests, not the controls revision")
  C3-4 APPEND_ONLY      `git diff --numstat BASE REV -- <file>` deletes zero lines and adds at
                        least one
  C3-5 FINAL_VISIBLE    the correction heading is the last `## ` section of the file and no
                        unclosed HTML comment hides it

Predicate (same sentence as `corpus/evidence/round77/claims.md`):

  `python3 -B corpus/evidence/round77/c3-count.py --lane . --base BASE --rev REV`
  exits 0 and prints exactly `C3=PASS checks=5/5`.

Limits: lexical and line-local. It proves the block's presence, position, quoted superseded
state, corrected phrase and append-only diff — not that the corrected sentence is true
(that is the spot-check's ground) and not that no other sentence in the file is false.

Usage: python3 corpus/evidence/round77/c3-count.py --lane PATH --base REV --rev REV
Exit: 0 C3=PASS · 1 C3=FAIL · 2 usage/setup.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys

TARGET = "corpus/evidence/round76/claims.md"
HEADING = "## Correction — round-76 claims prose"
SUPERSEDED = ("4 (receipt precision) is honoured by naming the controls revision in every receipt")
CORRECTED = "worktree digests, not the controls revision"


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def git(root: pathlib.Path, *args: str) -> str:
    p = subprocess.run(["git", "-C", str(root), *args], text=True, capture_output=True)
    if p.returncode:
        raise RuntimeError(p.stderr.strip()[:300])
    return p.stdout


def section(text: str, heading: str) -> str | None:
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == heading:
            out = [line]
            for nxt in lines[i + 1:]:
                if nxt.startswith("## "):
                    break
                out.append(nxt)
            return "\n".join(out)
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--lane", default=".")
    ap.add_argument("--base", required=True)
    ap.add_argument("--rev", required=True)
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    target = lane / TARGET
    if not target.is_file():
        print(f"c3-count: missing {target}", file=sys.stderr)
        return 2
    text = target.read_text(encoding="utf-8", errors="replace")
    flat = norm(text)
    checks: list[tuple[str, bool, str]] = []

    checks.append(("C3-1", SUPERSEDED in flat, "superseded clause still present verbatim"))

    block = section(text, HEADING)
    checks.append(("C3-2", block is not None, "supersession heading present"))

    both = block is not None and SUPERSEDED in norm(block) and CORRECTED in norm(block)
    checks.append(("C3-3", both, "block quotes the superseded clause and states the corrected fact"))

    try:
        numstat = git(lane, "diff", "--numstat", a.base, a.rev, "--", TARGET)
    except RuntimeError as exc:
        print(f"c3-count: git: {exc}", file=sys.stderr)
        return 2
    deleted = added = 0
    for line in numstat.splitlines():
        parts = line.split("\t")
        if len(parts) == 3:
            added += int(parts[0]) if parts[0].isdigit() else 0
            deleted += int(parts[1]) if parts[1].isdigit() else 0
    checks.append(("C3-4", added > 0 and deleted == 0, f"numstat added={added} deleted={deleted}"))

    final = False
    if block is not None:
        heads = [line for line in text.splitlines() if line.startswith("## ")]
        final = bool(heads) and heads[-1].strip() == HEADING
        idx = text.find(HEADING)
        before = text[:idx]
        if before.count("<!--") != before.count("-->"):
            final = False
    checks.append(("C3-5", final, "correction block is the last section and not comment-hidden"))

    for cid, ok, why in checks:
        print(f"{cid} {'PASS' if ok else 'FAIL'} {why}")
    passed = sum(1 for _cid, ok, _why in checks if ok)
    verdict = "PASS" if passed == len(checks) else "FAIL"
    print(f"C3={verdict} checks={passed}/{len(checks)}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
