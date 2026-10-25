#!/usr/bin/env python3
"""receipt-check — a receipt names the tool revision it was measured against, and that revision
still carries the tool (QUALITY 84, round 51).

Header form, in a receipt's first five lines or in a `SKILL.md` Gates table row:
    tool-rev: <40-hex commit> tool: <lane-relative path> [digest: sha256:<64-hex>]
Per receipt: RECEIPT_NO_REV (no header — the round-50 class, a prose header naming no hash,
`corpus/evidence/round50/measure-after.txt:1`); RECEIPT_REV_UNKNOWN (commit not in the lane
repo); RECEIPT_REV_UNLANDED (not an ancestor of the tip); RECEIPT_TOOL_ABSENT;
RECEIPT_TOOL_MOVED (the tool's blob at the tip differs from its blob at the named revision —
the receipt measures code the tip no longer has); RECEIPT_DIGEST_MISMATCH; else RECEIPT_OK.
`--skill SKILL.md` applies the same test to the header in the Gates row (`SKILL_PIN_OK`,
`SKILL_NO_PIN`, or the failing line). Output: one line per receipt, the optional skill line,
`CHECKS=n OK=n FAILS=n` (the skill line counts as a check), `RECEIPT_CHECK=PASS|FAIL`. Exit 0 pass · 1 any failure · 2 root
not a git work tree. Usage: python3 corpus/evidence/round51/receipt-check.py <receipt> [...]
[--root LANE] [--tip REV] [--skill SKILL.md]. Named limits: the header is a convention, not a
signature — a receipt can name a revision it did not run at and this check cannot tell; only
the first five lines are read; a receipt measuring a tree count has no header form here; the
digest leg hashes the blob, not behaviour.
"""

from __future__ import annotations

import argparse, hashlib, pathlib, re, subprocess, sys

LANE = pathlib.Path(__file__).resolve().parents[3]
HEAD_RE = re.compile(
    r"(?:#\s*)?tool-rev:\s*([0-9a-f]{40})\s+tool:\s*([A-Za-z0-9._/-]+)(?:\s+digest:\s*sha256:([0-9a-f]{64}))?"
)


def git(root: pathlib.Path, *args: str) -> tuple[int, bytes]:
    p = subprocess.run(["git", "-C", str(root), *args], capture_output=True)
    return p.returncode, p.stdout


def pin(root: pathlib.Path, tip: str, label: str, rev: str, tool: str, want: str | None) -> tuple[bool, str]:
    if git(root, "cat-file", "-e", f"{rev}^{{commit}}")[0] != 0:
        return False, f"RECEIPT_REV_UNKNOWN {label} rev={rev}"
    if git(root, "merge-base", "--is-ancestor", rev, tip)[0] != 0:
        return False, f"RECEIPT_REV_UNLANDED {label} rev={rev[:12]}"
    rc_a, at_rev = git(root, "rev-parse", f"{rev}:{tool}")
    if rc_a != 0:
        return False, f"RECEIPT_TOOL_ABSENT {label} rev={rev[:12]} tool={tool}"
    rc_b, at_tip = git(root, "rev-parse", f"{tip}:{tool}")
    if rc_b != 0 or at_rev.strip() != at_tip.strip():
        return False, f"RECEIPT_TOOL_MOVED {label} rev={rev[:12]} tool={tool}"
    if want:
        rc_c, blob = git(root, "cat-file", "blob", f"{rev}:{tool}")
        got = hashlib.sha256(blob).hexdigest() if rc_c == 0 else ""
        if got != want:
            return False, f"RECEIPT_DIGEST_MISMATCH {label} recorded={want[:12]} actual={got[:12]}"
    return True, f"RECEIPT_OK {label} rev={rev[:12]} tool={tool}"


def header(path: pathlib.Path) -> re.Match | None:
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines()[:5]:
        m = HEAD_RE.search(line)
        if m:
            return m
    return None


def one(root: pathlib.Path, tip: str, path: pathlib.Path, nopin: str, ok_label: str) -> bool:
    m = header(path)
    if m is None:
        print(f"{nopin} {path}")
        return False
    good, line = pin(root, tip, str(path), m.group(1), m.group(2), m.group(3))
    print(line if ok_label == "RECEIPT_OK" else line.replace("RECEIPT_OK", ok_label))
    return good


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("receipts", nargs="*")
    ap.add_argument("--root", default=str(LANE))
    ap.add_argument("--tip", default="HEAD")
    ap.add_argument("--skill", help="also require the Gates registry row to carry the header form")
    a = ap.parse_args()
    root = pathlib.Path(a.root)
    if git(root, "rev-parse", "--show-toplevel")[0] != 0:
        print(f"ROOT_NOT_GIT {root}")
        return 2
    ok = fails = 0
    for r in a.receipts:
        good = one(root, a.tip, pathlib.Path(r), "RECEIPT_NO_REV", "RECEIPT_OK")
        ok += good
        fails += not good
    if a.skill:
        fails += not one(root, a.tip, pathlib.Path(a.skill), "SKILL_NO_PIN", "SKILL_PIN_OK")
    checks = len(a.receipts) + (1 if a.skill else 0)
    print(f"CHECKS={checks} OK={checks - fails} FAILS={fails}")
    print(f"RECEIPT_CHECK={'PASS' if fails == 0 else 'FAIL'}")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
