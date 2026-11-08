#!/usr/bin/env python3
"""skill-tally-r92-controls — round-92 C3 discrimination battery.

Two scratch `SKILL.md` copies of the landing tree, each with one defect, are scored by the unchanged
`skill-tally-r90.py` and by `skill-tally-r92.py` against the committed selftest receipt:

  F1 old-prose   the round-91 clause `r82 bash-pin-override cases 276–283` restored: r90 never binds the range, so
                 it PASSes; r92 derives the family from the tool's own `ok-case` names and prints
                 `CASE_RANGE_OK=1/2 MISLABELED=6`
  F2 stale-tally one current tally cell set to `PASS (275 cases, 0 skipped)`: both counters must refuse it (the r90
                 leg is carried, not weakened)

`CASE_RANGE_*` findings are read from stdout; the exit codes are the verdicts. No network, no writes outside
`--work`.

Usage: python3 -B corpus/evidence/round92/skill-tally-r92-controls.py --root DIR --work DIR
Exit 0 both cases as expected, 1 a deviation, 2 setup.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NEW = os.path.join(HERE, "skill-tally-r92.py")
OLD = os.path.join(os.path.dirname(HERE), "round91", "skill-tally-r91.py")
RECEIPT = os.path.join(HERE, "controls", "selftest-r92.txt")
OLD_CLAUSE = ("r39 bash-pin cases 273–275 (pin-bashenv, drift-bashenv) and r82 pin-override cases 276–283, "
              "of which bash-pin-override cases 282–283")
BAD_CLAUSE = "r39 bash-pin cases 273–275 and r82 bash-pin-override cases 276–283"


def run(counter, tree):
    p = subprocess.run([sys.executable, "-B", counter, "--root", tree, "--selftest", RECEIPT],
                       capture_output=True, text=True)
    out = p.stdout or ""
    verdict = [ln for ln in out.splitlines()
               if "SKILL_TALLY_R91=" in ln or "SKILL_TALLY_R92=" in ln]
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

    rc91o, v91o, _ = run(OLD, old_prose)
    rc91, v91, out91 = run(NEW, old_prose)
    # Carried: r91 already refuses the old prose (CASE_RANGE_OK=1/2 MISLABELED=6 both counters).
    carried = rc91o == 1 and rc91 == 1 and "MISLABELED=6" in out91
    print(f"{'OK' if carried else 'FAIL'} old-prose-carried: r91 {v91o}, r92 {v91}")
    if not carried:
        print("  r92:", " | ".join(ln for ln in out91.splitlines() if "CASE_RANGE" in ln)[-300:])

    rc_old_s, v_old_s, o_old_s = run(OLD, stale)
    rc_new_s, v_new_s, o_new_s = run(NEW, stale)
    f2 = (rc_old_s == 1 and rc_new_s == 1 and "STALE_TALLIES=1/9" in o_old_s
          and "STALE_TALLIES=1/8" in o_new_s)
    print(f"{'OK' if f2 else 'FAIL'} stale-tally: r91 {v_old_s} (rc={rc_old_s}), r92 {v_new_s} (rc={rc_new_s})")

    # T2 discrimination: delete one historical other (161) inside ## Gates. r91 (document-wide,
    # no multiset pin) still passes; r92 refuses with LEG_FAIL OTHERS.
    del_tree = tree("deleted-other", text.replace("`PASS (161 cases, 0 skipped)`", "`PASS (160 cases, 0 skipped)`", 1))
    rc91d, v91d, _ = run(OLD, del_tree)
    rc92d, v92d, out92d = run(NEW, del_tree)
    f_del = rc91d == 0 and rc92d == 1 and "LEG_FAIL OTHERS" in out92d
    print(f"{'OK' if f_del else 'FAIL'} deleted-other: r91 {v91d} (rc={rc91d}), r92 {v92d} (rc={rc92d})")

    ok = carried and f2 and f_del
    print(f"CONTROLS={'PASS' if ok else 'FAIL'} OLDPROSE_REFUSED={int(carried)}/1 PRIOR_ACCEPTED={int(rc91o == 1)}/1 "
          f"STALE_REFUSED_BOTH={int(f2)}/1")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
