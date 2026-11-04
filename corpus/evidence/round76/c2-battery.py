#!/usr/bin/env python3
"""Round-76 C2 battery — QUALITY 136 controls for a correction counter.

Unit under test: a COUNTER program that takes `--lane PATH --base REV --rev REV` and
exits 0 iff the round-74 lesson's correction block is compliant. The battery builds
seven disposable fixture repositories under `--work` (each `git init`, one base commit
with the uncorrected lesson, one case commit) and runs the counter on each, then on the
real lane at its tip:

  POSITIVE  good-block        a correction block with different valid wording — must be
                              accepted; a blanket-refusal counter is not a gain
  BOGUS     decoy-above       a decoy `Located quote:` above the authored bullets plus a
                              block stating the decoy's count — the r75 presence test's
                              first-textual-match rebinding (F1) — must be rejected
  BOGUS     negation          the corrected counts stated with a negation — must be rejected
  BOGUS     magnitude         `161 whitespace tokens` for the corrected 16 — must be rejected
  BOGUS     comment-only      the correction hidden inside an HTML comment — must be rejected
  BOGUS     mid-file          a valid block that is not the last `## ` section — must be
                              rejected
  BOGUS     deletion-history  a valid block in a commit that also deletes a line — must
                              be rejected (append-only, not net-append)
  LANE      real              the counter on the real lane at `--rev` over `--lane-base`

Predicate (same sentence as `corpus/evidence/round76/claims.md`):

  `python3 -B corpus/evidence/round76/c2-battery.py --counter COUNTER --work DIR`
  exits 0 and prints exactly
  `C2_BATTERY=PASS bogus_rejected=6/6 positive=1/1 lane=PASS`.

Each counter run is bounded (`--child-timeout`, default 60 s). Exit 0 PASS · 1 FAIL ·
2 usage/setup. Limits: the fixtures are text-shaped blocks; this proves rejection of
these six classes plus lane acceptance, not semantic entailment.
"""
from __future__ import annotations

import argparse
import os
import pathlib
import secrets
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
LANE = HERE.parents[2]
LESSON = "corpus/lessons/round-74.md"
HEAD = "## Correction — round-74 quote counts"
LANE_BASE = "8022f72c889c904b5657d52c7f29e1643392a216"

QUOTE_A = "Before any successor calibration freeze, exercise a real committed append and a real deletion through `load()`"
QUOTE_B = "base = check({k: v for k, v in FIXTURE.items()}, {}, set())"

BASE_LESSON = (
    "# Round 74 — fixture\n\nremovable line\n\n## Gate\n\n"
    "- Admit S182, own-work B. Opened 2026-11-04. Located quote: "
    f"“{QUOTE_A}” (18 words).\n"
    "- Reject S183, own-work C. Opened 2026-11-04. Located quote: "
    f"`{QUOTE_B}` (line 163, 13 whitespace tokens).\n\n"
    "## Boundaries\n\nFixture boundary text.\n"
)

GOOD_BLOCK = (
    f"\n{HEAD}\n\n"
    "Round 76 fixture. Superseded: the authored bullets record 18 words and 13 whitespace "
    "tokens. The quoted strings carry 16 and 11 whitespace tokens, re-derived from the "
    "authored bullets at the measured revision.\n"
)

DECOY = (
    "- Admit S999, decoy row. Opened 2026-11-04. Located quote: "
    "“five word decoy quote here now” (5 words).\n"
)

CASES = {
    "good-block": lambda text: text + GOOD_BLOCK,
    "decoy-above": lambda text: text.replace(
        "- Admit S182",
        DECOY + "- Admit S182") + (
        f"\n{HEAD}\n\nSuperseded: 18 words and 13 whitespace tokens. The quoted strings carry "
        "5 and 11 whitespace tokens.\n"),
    "negation": lambda text: text + (
        f"\n{HEAD}\n\nSuperseded: 18 words and 13 whitespace tokens. The counts 16 and 11 "
        "should not be read as corrected values.\n"),
    "magnitude": lambda text: text + (
        f"\n{HEAD}\n\nSuperseded: 18 words and 13 whitespace tokens. The quoted strings carry "
        "161 whitespace tokens and 11 whitespace tokens.\n"),
    "comment-only": lambda text: text + (
        f"\n<!--\n{HEAD}\n\nSuperseded: 18 words and 13 whitespace tokens. The quoted strings "
        "carry 16 and 11 whitespace tokens.\n-->\n"),
    "mid-file": lambda text: text.replace("## Boundaries", (
        f"{HEAD}\n\nSuperseded: 18 words and 13 whitespace tokens. The quoted strings carry "
        "16 and 11 whitespace tokens.\n\n## Boundaries")),
    "deletion-history": lambda text: text.replace("removable line\n\n", "") + GOOD_BLOCK,
}
BOGUS = tuple(k for k in CASES if k != "good-block")


def git(root: pathlib.Path, *args: str) -> str:
    p = subprocess.run(["git", "-C", str(root), *args], text=True, capture_output=True)
    if p.returncode:
        raise RuntimeError(p.stderr.strip()[:400])
    return p.stdout.strip()


def run_counter(counter: pathlib.Path, lane: pathlib.Path, base: str, rev: str, timeout: int) -> int:
    try:
        p = subprocess.run([sys.executable, "-B", str(counter), "--lane", str(lane),
                            "--base", base, "--rev", rev],
                           stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None
    return p.returncode


def build_fixture(work: pathlib.Path, name: str, timeout: int, counter: pathlib.Path):
    root = work / secrets.token_hex(8)
    root.mkdir(parents=True)
    (root / "corpus/lessons").mkdir(parents=True)
    (root / LESSON).write_text(BASE_LESSON)
    git(root, "init", "-q")
    git(root, "add", "--", LESSON)
    git(root, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "commit", "-qm", "base")
    base = git(root, "rev-parse", "HEAD")
    (root / LESSON).write_text(CASES[name](BASE_LESSON))
    git(root, "add", "--", LESSON)
    git(root, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "commit", "-qm", "case")
    rev = git(root, "rev-parse", "HEAD")
    return root, base, rev


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--counter", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--lane", default=str(LANE))
    ap.add_argument("--lane-base", default=LANE_BASE)
    ap.add_argument("--lane-rev", default="master")
    ap.add_argument("--child-timeout", type=int, default=60)
    a = ap.parse_args()
    counter = pathlib.Path(a.counter).resolve()
    lane = pathlib.Path(a.lane).resolve()
    work = pathlib.Path(a.work).resolve()
    if not counter.is_file():
        print(f"c2-battery: missing counter {counter}", file=sys.stderr)
        return 2
    if a.child_timeout < 1:
        print("c2-battery: --child-timeout must be >= 1", file=sys.stderr)
        return 2
    work.mkdir(parents=True, exist_ok=True)
    print("COUNTER_PATH=" + str(counter))
    print("COUNTER_SHA256=" + __import__("hashlib").sha256(counter.read_bytes()).hexdigest())
    print(f"CHILD_TIMEOUT={a.child_timeout} LANE={lane} LANE_BASE={a.lane_base[:12]} LANE_REV={a.lane_rev}")
    bogus_rejected = bogus_total = 0
    positive_ok = positive_total = 0
    lane_ok = False
    try:
        for name in ("good-block",) + BOGUS:
            root, base, rev = build_fixture(work, name, a.child_timeout, counter)
            try:
                rc = run_counter(counter, root, base, rev, a.child_timeout)
            finally:
                shutil.rmtree(root, ignore_errors=True)
            if name == "good-block":
                positive_total += 1
                positive_ok += rc == 0
                print(f"FIXTURE {name} expected=accept actual={'accept' if rc == 0 else 'reject'} rc={rc}")
            else:
                bogus_total += 1
                rejected = rc not in (0, None)
                bogus_rejected += rejected
                print(f"FIXTURE {name} expected=reject actual={'reject' if rejected else 'accept'} rc={rc}")
        rc = run_counter(counter, lane, a.lane_base, a.lane_rev, a.child_timeout)
        lane_ok = rc == 0
        print(f"LANE real expected=accept actual={'accept' if lane_ok else 'reject'} rc={rc}")
    finally:
        shutil.rmtree(work, ignore_errors=True)
    verdict = bogus_rejected == bogus_total and positive_ok == positive_total and lane_ok
    print(f"bogus_rejected={bogus_rejected}/{bogus_total} positive={positive_ok}/{positive_total} "
          f"lane={'PASS' if lane_ok else 'FAIL'}")
    print(f"C2_BATTERY={'PASS' if verdict else 'FAIL'} bogus_rejected={bogus_rejected}/{bogus_total} "
          f"positive={positive_ok}/{positive_total} lane={'PASS' if lane_ok else 'FAIL'}")
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
