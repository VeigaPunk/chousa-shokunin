#!/usr/bin/env python3
"""c2-count — the round-73 C2 calibration counter (frozen before measurement).

Claim C2 (corpus/evidence/round73/claims.md): the two routed round-72 verifier
spot-check defects are corrected append-only, status-neutral to the r72
rejected-honest-stop ruling.

  V72-1  the r72 narrative says "the unguarded grep ... kills the script under
         set -euo pipefail". The grep at tools/research-gate.sh:8426 sits in an
         `&&` list and is set-e-exempt (it supplies the symptom line only); the
         process exit is the next unguarded sub-run assignment at
         tools/research-gate.sh:8435, which inherits the flock-less --pin
         child's designed rc=2.  Neither line number is recorded anywhere in the
         r72 artifacts.
  V72-2  corpus/evidence/round72/controls/after-r72-corrections.txt heads "every
         count line re-run fresh at the verdicts tree" while its own recorded
         `git rev-parse HEAD` is 7f7ea19a (the landing tip); the counts re-derive
         there (SCORECARD "18 healthy" = 2), and at the verdicts tree 6dd6c82 the
         verdict row's own quotation adds a third hit (3 at 6dd6c82, two
         recorded).  A count line's tree is part of its re-derivation context.

Checks (all over committed bytes at --rev; --base is the r72 spot-check tip):

  C2-1  LOG.md carries exactly one anchored `## Round 72 correction entry`.
  C2-2  that entry names both kill lines 8426 and 8435 and the word exempt.
  C2-3  corpus/lessons/round-72.md carries exactly one anchored
        `## Correction — round-72 spot-check` block naming V72-1, V72-2, both
        line numbers and both trees.
  C2-4  SCORECARD.md carries exactly one anchored `## Round 72 correction note`
        naming V72-1 and V72-2.
  C2-5  that lesson block states the measurement tree exactly: the phrases
        "measured at the landing tip 7f7ea19a", "three at the verdicts tree
        6dd6c82" and "two recorded" all appear in it.
  C2-6  append-only: `git diff --numstat <base> <rev>` removes ZERO lines from
        LOG.md, corpus/lessons/round-72.md and SCORECARD.md.
  C2-7  the two r72 receipts' bytes are unchanged base -> rev.

Exit: 0 C2=PASS (7/7), 1 C2=FAIL, 2 usage/setup.
`--selftest` scores a synthetic compliant fixture and seven mutations of it
(one per check) in memory and prints `SELFTEST=PASS mutations=7/7`; it never
reads the lane.

Contract text frozen with the claim; changing a check after any seat has scored
is a new claim, not this one's rule.
"""
from __future__ import annotations

import argparse
import subprocess
import sys

PATHS = ["LOG.md", "corpus/lessons/round-72.md", "SCORECARD.md"]
RECEIPTS = [
    "corpus/evidence/round72/controls/battery-past-locale-dies-pinzone-r72.txt",
    "corpus/evidence/round72/controls/after-r72-corrections.txt",
]
LOG_HEAD = "## Round 72 correction entry"
LESSON_HEAD = "## Correction — round-72 spot-check"
CARD_HEAD = "## Round 72 correction note"
LESSON_NAMES = ["V72-1", "V72-2", "8426", "8435", "7f7ea19a", "6dd6c82"]
TREE_PHRASES = [
    "measured at the landing tip 7f7ea19a",
    "three at the verdicts tree 6dd6c82",
    "two recorded",
]


def anchored_count(text: str, heading: str) -> int:
    return sum(1 for line in text.splitlines() if line.rstrip() == heading)


def section(text: str, heading: str) -> str:
    """Text from the LAST exact heading line to the next `## ` line (or EOF)."""
    lines = text.splitlines()
    starts = [i for i, ln in enumerate(lines) if ln.rstrip() == heading]
    if not starts:
        return ""
    out = []
    for ln in lines[starts[-1] + 1:]:
        if ln.startswith("## "):
            break
        out.append(ln)
    return "\n".join(out)


def missing(hay: str, needles) -> list[str]:
    return [n for n in needles if n not in hay]


def check(files: dict[str, str], deleted: dict[str, int], changed: set[str]):
    """Return [(id, passed, detail)] — pure, so --selftest can score fixtures."""
    res = []
    log, lesson, card = files["LOG.md"], files["corpus/lessons/round-72.md"], files["SCORECARD.md"]
    n = anchored_count(log, LOG_HEAD)
    res.append(("C2-1", n == 1, f"LOG.md '{LOG_HEAD}' count={n}"))
    entry = section(log, LOG_HEAD)
    miss = missing(entry, ["8426", "8435", "exempt"])
    res.append(("C2-2", not miss, f"LOG entry missing={','.join(miss) or 'none'}"))
    n = anchored_count(lesson, LESSON_HEAD)
    block = section(lesson, LESSON_HEAD)
    miss = missing(block, LESSON_NAMES)
    res.append(("C2-3", n == 1 and not miss,
                f"lesson '{LESSON_HEAD}' count={n} missing={','.join(miss) or 'none'}"))
    n = anchored_count(card, CARD_HEAD)
    miss = missing(section(card, CARD_HEAD), ["V72-1", "V72-2"])
    res.append(("C2-4", n == 1 and not miss,
                f"SCORECARD '{CARD_HEAD}' count={n} missing={','.join(miss) or 'none'}"))
    miss = missing(block, TREE_PHRASES)
    res.append(("C2-5", not miss, f"lesson tree statement missing={','.join(miss) or 'none'}"))
    bad = [p for p in PATHS if deleted.get(p, 0) != 0]
    res.append(("C2-6", not bad,
                "removed lines=" + (",".join(f"{p}:{deleted[p]}" for p in bad) or "0 across LOG/lesson/SCORECARD")))
    hit = sorted(changed & set(RECEIPTS))
    res.append(("C2-7", not hit, f"r72 receipts changed={','.join(hit) or 'none'}"))
    return res


def git(lane: str, *args: str) -> str:
    p = subprocess.run(["git", "-C", lane, *args], capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(f"c2-count: git {' '.join(args)} failed rc={p.returncode}: {p.stderr.strip()[:200]}")
    return p.stdout


def load(lane: str, rev: str, base: str):
    files = {p: git(lane, "show", f"{rev}:{p}") for p in PATHS}
    deleted = {}
    for line in git(lane, "diff", "--numstat", base, rev, "--", *PATHS).splitlines():
        parts = line.split("\t")
        if len(parts) >= 3:
            deleted[parts[2]] = int(parts[0]) if parts[0].isdigit() else 0
    changed = {ln.strip() for ln in git(lane, "diff", "--name-only", base, rev, "--", *RECEIPTS).splitlines()
               if ln.strip()}
    return files, {p: deleted.get(p, 0) for p in PATHS}, changed


FIXTURE = {
    "LOG.md": "# LOG\n\n## Round 72 — entry\n\ntext\n\n"
              f"{LOG_HEAD}\n\n"
              "- the kill line is the unguarded assignment at tools/research-gate.sh:8435; the grep at "
              "tools/research-gate.sh:8426 is set-e-exempt inside the && list\n",
    "corpus/lessons/round-72.md": "# Round 72\n\n## Gate\n\ntext\n\n"
              f"{LESSON_HEAD}\n\n"
              "V72-1 kill lines 8426 orphan, 8435 exits. V72-2 measured at the landing tip 7f7ea19a; "
              "three at the verdicts tree 6dd6c82 against two recorded.\n",
    "SCORECARD.md": "# chousa — Scorecard\n\n## Axes\n\ntext\n\n"
              f"{CARD_HEAD}\n\n- V72-1 and V72-2 corrected append-only.\n",
}
MUTATIONS = [
    ("C2-1", lambda f, d, c: f.__setitem__("LOG.md", f["LOG.md"].replace(LOG_HEAD, "## Round 72 correction"))),
    ("C2-2", lambda f, d, c: f.__setitem__("LOG.md", f["LOG.md"].replace(":8435", ":8436"))),
    ("C2-3", lambda f, d, c: f.__setitem__("corpus/lessons/round-72.md",
                                           f["corpus/lessons/round-72.md"].replace("V72-2 ", ""))),
    ("C2-4", lambda f, d, c: f.__setitem__("SCORECARD.md", f["SCORECARD.md"].replace(CARD_HEAD, "## Round 72 note"))),
    ("C2-5", lambda f, d, c: f.__setitem__("corpus/lessons/round-72.md",
                                           f["corpus/lessons/round-72.md"].replace("three at the verdicts tree", "three at the landing tip"))),
    ("C2-6", lambda f, d, c: d.__setitem__("LOG.md", 1)),
    ("C2-7", lambda f, d, c: c.add(RECEIPTS[0])),
]


def selftest() -> int:
    base = check({k: v for k, v in FIXTURE.items()}, {}, set())
    bad = [cid for cid, ok, _ in base if not ok]
    if bad:
        print(f"SELFTEST=FAIL fixture_not_compliant={','.join(bad)}")
        return 1
    score = 0
    for cid, mutate in MUTATIONS:
        files = dict(FIXTURE)
        deleted, changed = {}, set()
        mutate(files, deleted, changed)
        got = {i: ok for i, ok, _ in check(files, deleted, changed)}
        if got.get(cid) is False:
            score += 1
        else:
            print(f"SELFTEST mutation_not_caught id={cid}")
    print(f"SELFTEST={'PASS' if score == len(MUTATIONS) else 'FAIL'} mutations={score}/{len(MUTATIONS)}")
    return 0 if score == len(MUTATIONS) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="round-73 C2 counter (frozen)")
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", default=None)
    ap.add_argument("--base", default=None)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.rev or not a.base:
        print("c2-count: --rev and --base are required (or --selftest)", file=sys.stderr)
        return 2
    files, deleted, changed = load(a.lane, a.rev, a.base)
    res = check(files, deleted, changed)
    for cid, ok, detail in res:
        print(f"CHECK {cid} {'PASS' if ok else 'FAIL'} {detail}")
    passed = sum(1 for _, ok, _ in res if ok)
    verdict = "PASS" if passed == len(res) else "FAIL"
    print(f"C2={verdict} checks={passed}/{len(res)} rev={a.rev[:12]} base={a.base[:12]}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
