#!/usr/bin/env python3
"""skill-tally-r91-controls — round-91 C3 discrimination battery.

Two scratch `SKILL.md` copies of the landing tree, each with one defect, are scored by the unchanged
`skill-tally-r90.py` and by `skill-tally-r91.py` against the committed selftest receipt:

  F1 old-prose   the round-90 clause `r82 bash-pin-override cases 276–283` restored: r90 never binds the range, so
                 it PASSes; r91 derives the family from the tool's own `ok-case` names and prints
                 `CASE_RANGE_OK=1/2 MISLABELED=6`
  F2 stale-tally one current tally cell set to `PASS (275 cases, 0 skipped)`: both counters must refuse it (the r90
                 leg is carried, not weakened)

`CASE_RANGE_*` findings are read from stdout; the exit codes are the verdicts. No network, no writes outside
`--work`.

Usage: python3 -B corpus/evidence/round91/skill-tally-r91-controls.py --root DIR --work DIR
Exit 0 both cases as expected, 1 a deviation, 2 setup.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NEW = os.path.join(HERE, "skill-tally-r91.py")
OLD = os.path.join(os.path.dirname(HERE), "round90", "skill-tally-r90.py")
RECEIPT = os.path.join(HERE, "controls", "selftest-r91.txt")
OLD_CLAUSE = ("r39 bash-pin cases 273–275 (pin-bashenv, drift-bashenv) and r82 pin-override cases 276–283, "
              "of which bash-pin-override cases 282–283")
BAD_CLAUSE = "r39 bash-pin cases 273–275 and r82 bash-pin-override cases 276–283"


def run(counter, tree):
    p = subprocess.run([sys.executable, "-B", counter, "--root", tree, "--selftest", RECEIPT],
                       capture_output=True, text=True)
    out = p.stdout or ""
    verdict = [ln for ln in out.splitlines()
               if "SKILL_TALLY_R90=" in ln or "SKILL_TALLY_R91=" in ln]
    return p.returncode, (verdict[0] if verdict else "no-verdict"), out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    work = os.path.abspath(a.work)
    if not os.path.isfile(RECEIPT):
        print(f"SETUP missing selftest receipt {RECEIPT}")
        return 2
    src = os.path.join(root, "SKILL.md")
    text = open(src, encoding="utf-8").read()
    if OLD_CLAUSE not in text:
        print("SETUP repaired clause absent from SKILL.md — is this the landing tree?")
        return 2
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work, exist_ok=True)

    def tree(name, body):
        d = os.path.join(work, name)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8").write(body)
        return d

    old_prose = tree("old-prose", text.replace(OLD_CLAUSE, BAD_CLAUSE))
    stale = tree("stale-tally", text.replace("PASS (283 cases, 0 skipped)",
                                             "PASS (275 cases, 0 skipped)", 1))

    rc90, v90, _ = run(OLD, old_prose)
    rc91, v91, out91 = run(NEW, old_prose)
    f1 = rc90 == 0 and rc91 == 1 and "MISLABELED=6" in out91 and "CASE_RANGE_OK=1/2" in out91
    print(f"{'OK' if f1 else 'FAIL'} old-prose: r90 {v90}, r91 {v91}")
    if not f1:
        print("  r91:", " | ".join(ln for ln in out91.splitlines() if "CASE_RANGE" in ln)[-300:])

    rc90s, v90s, o90s = run(OLD, stale)
    rc91s, v91s, o91s = run(NEW, stale)
    f2 = (rc90s == 1 and rc91s == 1 and "STALE_TALLIES=1/9" in o90s
          and "STALE_TALLIES=1/9" in o91s)
    print(f"{'OK' if f2 else 'FAIL'} stale-tally: r90 {v90s} (rc={rc90s}), r91 {v91s} (rc={rc91s})")

    ok = f1 and f2
    print(f"CONTROLS={'PASS' if ok else 'FAIL'} OLDPROSE_REFUSED={int(f1)}/1 PRIOR_ACCEPTED={int(rc90 == 0)}/1 "
          f"STALE_REFUSED_BOTH={int(f2)}/1")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
