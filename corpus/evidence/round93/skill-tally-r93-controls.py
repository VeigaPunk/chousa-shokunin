#!/usr/bin/env python3
"""skill-tally-r93-controls — round-93 C3 discrimination battery.

Successor of `skill-tally-r92-controls.py`. Scratch `SKILL.md` copies of the landing tree are scored by
the round-92 counter and by `skill-tally-r93.py` against the committed selftest receipt:

  P  positive             the landing `SKILL.md`: both counters PASS
  C1 old-prose-carried    the round-91 clause `r82 bash-pin-override cases 276–283` restored: both refuse
  C2 stale-tally          one current tally set to `PASS (275 cases, 0 skipped)`: both refuse
  C3 deleted-historical   the grounded `161` tally set to `160`: both refuse (the r92 literal still bites)
  D1 deleted-tail         the `215` tail tally one digit changed: r92 never reads outside `## Gates`, so it
                          PASSes; r93's TAIL leg refuses it
  D2 added-tail           one extra undeclared tally appended below the Gates scope: r92 PASSes; r93 fires
                          `HIST_SCOPE_BLEED` and refuses it
  D3 ungrounded-historical one grounding receipt's located quote changed in scratch: r93's HIST_DERIVED is
                          1/2 and it refuses, so the derivation is not vacuous

`HIST_*`, `TAIL_*` and `CASE_RANGE_*` findings are read from stdout; exit codes are the verdicts.

Usage: python3 -B corpus/evidence/round93/skill-tally-r93-controls.py --root DIR --work DIR
Exit 0 every case as expected, 1 a deviation, 2 setup. No network, no writes outside `--work`.
"""
import argparse
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NEW = os.path.join(HERE, "skill-tally-r93.py")
OLD = os.path.join(os.path.dirname(HERE), "round92", "skill-tally-r92.py")
RECEIPT = os.path.join(HERE, "controls", "selftest-r93.txt")
OLD_CLAUSE = ("r39 bash-pin cases 273–275 (pin-bashenv, drift-bashenv) and r82 pin-override cases 276–283, "
              "of which bash-pin-override cases 282–283")
BAD_CLAUSE = "r39 bash-pin cases 273–275 and r82 bash-pin-override cases 276–283"
HIST161 = "`PASS (161 cases, 0 skipped)`"
TAIL215 = "`PASS (215 cases, 0 skipped)`"
GROUND = ("corpus/evidence/round25-final-measure.log",
          "corpus/evidence/round34/audit-dispositions.md")
GROUND161 = GROUND[0]


def run(counter, tree):
    p = subprocess.run([sys.executable, "-B", counter, "--root", tree, "--selftest", RECEIPT],
                       capture_output=True, text=True)
    out = p.stdout or ""
    verdict = [ln for ln in out.splitlines() if "SKILL_TALLY_R9" in ln]
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
    for needle, why in ((HIST161, "161 tally"), (TAIL215, "215 tail tally")):
        if needle not in text:
            print(f"SETUP {why} absent from SKILL.md — is this the landing tree?")
            return 2
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work, exist_ok=True)

    def tree(name, body, grounding=None):
        d = os.path.join(work, name)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8").write(body)
        for rel in GROUND:
            p = os.path.join(d, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            if grounding is not None and rel == GROUND161:
                open(p, "w", encoding="utf-8").write(grounding)
            else:
                shutil.copy2(os.path.join(root, rel), p)
        return d

    results = {}
    pristine_docs = tree("positive", text)

    def case(name, body, expect_old, expect_new, needle_new="", grounding=None):
        d = tree(name, body, grounding)
        rc_old, v_old, _o = run(OLD, d)
        rc_new, v_new, out_new = run(NEW, d)
        ok = (rc_old == expect_old) and (rc_new == expect_new) and (needle_new in out_new if needle_new else True)
        results[name] = ok
        print(f"{'OK' if ok else 'FAIL'} {name}: r92 rc={rc_old} ({v_old}), r93 rc={rc_new} ({v_new})")
        if not ok:
            print("  r93:", " | ".join(ln for ln in out_new.splitlines()
                                       if ln.startswith(("LEG_FAIL", "HIST_", "HIST_SCOPE")))[-400:])
        return ok

    case("positive", text, 0, 0, "SKILL_TALLY_R93=PASS")
    case("old-prose-carried", text.replace(OLD_CLAUSE, BAD_CLAUSE), 1, 1, "MISLABELED=6")
    case("stale-tally", text.replace("PASS (283 cases, 0 skipped)", "PASS (275 cases, 0 skipped)", 1), 1, 1,
         "STALE_TALLIES=1/8")
    case("deleted-historical", text.replace(HIST161, "`PASS (160 cases, 0 skipped)`", 1), 1, 1,
         "LEG_FAIL OTHERS")
    case("deleted-tail", text.replace(TAIL215, "`PASS (214 cases, 0 skipped)`", 1), 0, 1, "TAIL_OK=0")
    tail_cases = 1
    case("added-tail", text + "\nAdditional historical tally `PASS (199 cases, 0 skipped)` retained.\n", 0, 1,
         "HIST_SCOPE_BLEED")
    tail_cases += 1
    case("ungrounded-historical", text, 0, 1, "HIST_DERIVED=1/2",
         grounding="legacy selftest output, no verdict line\n")

    ok = all(results.values())
    print(f"CONTROLS={'PASS' if ok else 'FAIL'} "
          f"OLDPROSE_REFUSED={int(results['old-prose-carried'])}/1 "
          f"PRIOR_ACCEPTED={int(results['positive'])}/1 "
          f"STALE_REFUSED_BOTH={int(results['stale-tally'])}/1 "
          f"HIST_REFUSED_BOTH={int(results['deleted-historical'])}/1 "
          f"TAIL_REFUSED={int(results['deleted-tail'] + results['added-tail'])}/2 "
          f"TAIL_PRIOR_ACCEPTED={int(results['deleted-tail'] and results['added-tail'])}/1 "
          f"TAIL_ADDED_REFUSED={int(results['added-tail'])}/1 "
          f"HIST_UNGROUNDED_REFUSED={int(results['ungrounded-historical'])}/1")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
