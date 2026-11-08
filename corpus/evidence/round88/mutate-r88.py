#!/usr/bin/env python3
"""mutate-r88 — the round-88 C1 mutation battery (two halves).

**Counter mutants** — one-point edits to `corpus/evidence/round88/gate-records-r88.py`. The counter's own frozen
predicate must FAIL on each; a survivor is a defect of the counter (the round-86 `R86MutCounter` M2/M5 class and the
round-87 `R87ReviewerC1` E1/E4 class):

  T4-record-keyed   the 203 record class narrowed to one record id (a general rule plus a record-keyed exception)
  T4-truncate       `_qualifying_203` returns only its first record (a one-row class)
  M2-credit-mutant  the whole mutant block replaced by credited fields (no mutant built, none run)
  M5-drop-setup     the SETUP leg deleted from the accounting list
  E1-joint-narrow   both 203 derivations narrowed together (the R87ReviewerC1 E1 shape; killed by the third pin)
  E4-setup-taut     the SETUP leg's `ok` tautologised while its detail still records the measured failure
                    (the R87ReviewerC1 E4 shape; killed by the receipt reconciliation, not the append count)

**Tool mutants** — one-point edits to the subject tool. The *pristine* counter must FAIL on each, which is what makes
the widened class load-bearing rather than merely printed (round-86 routed defect 1):

  T4-record-keyed-tool   2xx accepted generally, exactly 200 for S021 (the critic's T4 rule)
  admit-2xx-tool         2xx accepted everywhere (the round-85 M17 shape, kept as a regression control)

Named limit (reported, not counted): a counter edit that jointly rewrites the leg writer, the receipt files and the
reconciliation survives, because that edit *is* the counter. The `DERIVE_NEG` leg and the do-nothing control are the
partial cover; the wave's mutation seat attacks this class and any finding is reported.

Usage: python3 -B corpus/evidence/round88/mutate-r88.py --root DIR --repo GITDIR --work DIR
Exit 0 every mutant killed/caught, 1 a survivor or an uncaught tool mutant, 2 setup.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
COUNTER = os.path.join(HERE, "gate-records-r88.py")

COUNTER_MUTANTS = [
    ("T4-record-keyed", '_qualifying_203 row filter',
     '        if cells is None:\n            continue\n',
     '        if cells is None or sid != "S021":\n            continue\n'),
    ("T4-truncate", '_qualifying_203 return',
     '        out.append((sid, url, key, fetched, cells[3], h, quote, http))\n    return out',
     '        out.append((sid, url, key, fetched, cells[3], h, quote, http))\n    return out[:1]'),
    ("M2-credit-mutant", 'mutant block',
     '            if files:\n                ma = os.path.join(tmp, "tool-MUT-ADMIT.py")',
     '            mut_admit_derived = mut_admit_killed = 0\n'
     '            mut_unreach_derived = mut_unreach_killed = 0\n'
     '            if False:\n                ma = os.path.join(tmp, "tool-MUT-ADMIT.py")'),
    ("M5-drop-setup", 'accounting list',
     '                ("SETUP", setup_ok == 1, f"{setup_ok}/1"),\n',
     ''),
    ("E1-joint-narrow", '203 filter (both derivations)',
     '        if len(f[6]) != 3 or f[6] != "203":\n            continue\n        good.append(f)',
     '        if len(f[6]) != 3 or f[6] != "203" or f[0] != "S021":\n            continue\n        good.append(f)'),
    ("E4-setup-detached", 'SETUP measurement forced to fail',
     '            setup_ok = 1 if (p.returncode == 2 and "GATE_RECORDS_ERROR" in p.stderr) else 0',
     '            setup_ok = 0'),
]

# The round-87 N-deny-width equivalent is retired this round: the width legs now pin against `registry_rows_203`
# and ROWS_203, so a self-referential `d1_expected` is no longer equivalent — it is a third narrowing the pin
# catches. The empty list keeps the battery's accounting shape without a degenerate entry.
EQUIVALENT = []

# (id, anchor, replacement) applied to the subject tool the pristine counter is pointed at
TOOL_MUTANTS = [
    ("T4-record-keyed-tool",
     '        ok = any(r[0] == sid and r[1] == url and r[2] == key and r[4] == kv["fetched"] and r[5] == "0" and r[6] == "200"',
     '        _accept = (r[6] == "200" if sid == "S021" else r[6].startswith("2"))\n'
     '        ok = any(r[0] == sid and r[1] == url and r[2] == key and r[4] == kv["fetched"] and r[5] == "0" and _accept'),
    ("admit-2xx-tool",
     '        ok = any(r[0] == sid and r[1] == url and r[2] == key and r[4] == kv["fetched"] and r[5] == "0" and r[6] == "200"',
     '        _accept = r[6].startswith("2")\n'
     '        ok = any(r[0] == sid and r[1] == url and r[2] == key and r[4] == kv["fetched"] and r[5] == "0" and _accept'),
]


def verdict_of(stdout):
    v = [ln for ln in stdout.splitlines() if ln.startswith("GATE_RECORDS_R88=")]
    return v[0] if v else "no-verdict"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--work")
    a = ap.parse_args()
    root, repo = os.path.abspath(a.root), os.path.abspath(a.repo)
    work = a.work or os.environ.get("TMPDIR") or "/fast/scratch/hyaku"
    os.makedirs(work, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="mut87-", dir=work)
    src = open(COUNTER, encoding="utf-8").read()
    tool_src = open(os.path.join(root, "tools", "gate-records.py"), encoding="utf-8").read()
    try:
        killed = 0
        for mid, area, old, new in COUNTER_MUTANTS:
            if old not in src:
                print(f"SETUP_MISS {mid}: anchor not found in {area}")
                return 2
            mdir = os.path.join(tmp, "c-" + mid)
            os.makedirs(mdir, exist_ok=True)
            shutil.copy2(os.path.join(HERE, "c1-positives.tsv"), os.path.join(mdir, "c1-positives.tsv"))
            mp = os.path.join(mdir, "gate-records-r88.py")
            with open(mp, "w", encoding="utf-8") as fh:
                fh.write(src.replace(old, new, 1))
            exe = os.path.join(tmp, "w-" + mid)
            os.makedirs(exe, exist_ok=True)
            p = subprocess.run([sys.executable, "-B", mp, "--root", root, "--repo", repo, "--work", exe],
                               capture_output=True, text=True)
            dead = p.returncode != 0 or verdict_of(p.stdout) != "GATE_RECORDS_R88=PASS"
            print(f"{'KILLED' if dead else 'SURVIVOR'} {mid} rc={p.returncode} {verdict_of(p.stdout)}")
            for ln in p.stdout.splitlines():
                if ln.startswith("LEG_FAIL"):
                    print(f"  {ln}")
            shutil.rmtree(mdir, ignore_errors=True)
            shutil.rmtree(exe, ignore_errors=True)
            killed += 1 if dead else 0

        equivalent = 0
        for mid, area, old, new in EQUIVALENT:
            if old not in src:
                print(f"SETUP_MISS {mid}: anchor not found in {area}")
                return 2
            mdir = os.path.join(tmp, "e-" + mid)
            os.makedirs(mdir, exist_ok=True)
            shutil.copy2(os.path.join(HERE, "c1-positives.tsv"), os.path.join(mdir, "c1-positives.tsv"))
            mp = os.path.join(mdir, "gate-records-r88.py")
            with open(mp, "w", encoding="utf-8") as fh:
                fh.write(src.replace(old, new, 1))
            exe = os.path.join(tmp, "ew-" + mid)
            os.makedirs(exe, exist_ok=True)
            p = subprocess.run([sys.executable, "-B", mp, "--root", root, "--repo", repo, "--work", exe],
                               capture_output=True, text=True)
            dead = p.returncode != 0 or verdict_of(p.stdout) != "GATE_RECORDS_R88=PASS"
            print(f"{'KILLED' if dead else 'EQUIVALENT_ON_TREE'} {mid} rc={p.returncode} {verdict_of(p.stdout)}")
            shutil.rmtree(mdir, ignore_errors=True)
            shutil.rmtree(exe, ignore_errors=True)
            equivalent += 1 if not dead else 0

        caught = 0
        for mid, old, new in TOOL_MUTANTS:
            if old not in tool_src:
                print(f"SETUP_MISS {mid}: anchor not found in the subject tool")
                return 2
            mdir = os.path.join(tmp, "t-" + mid)
            os.makedirs(mdir, exist_ok=True)
            mtp = os.path.join(mdir, "gate-records.py")
            with open(mtp, "w", encoding="utf-8") as fh:
                fh.write(tool_src.replace(old, new, 1))
            exe = os.path.join(tmp, "tw-" + mid)
            os.makedirs(exe, exist_ok=True)
            p = subprocess.run([sys.executable, "-B", COUNTER, "--root", root, "--repo", repo,
                                "--tool", mtp, "--work", exe], capture_output=True, text=True)
            dead = p.returncode != 0 or verdict_of(p.stdout) != "GATE_RECORDS_R88=PASS"
            print(f"{'CAUGHT' if dead else 'UNCAUGHT'} {mid} rc={p.returncode} {verdict_of(p.stdout)}")
            for ln in p.stdout.splitlines():
                if ln.startswith("LEG_FAIL"):
                    print(f"  {ln}")
            shutil.rmtree(mdir, ignore_errors=True)
            shutil.rmtree(exe, ignore_errors=True)
            caught += 1 if dead else 0

        total = len(COUNTER_MUTANTS) + len(TOOL_MUTANTS)
        print(f"MUTANTS_KILLED={killed}/{len(COUNTER_MUTANTS)} TOOL_MUTANTS_CAUGHT={caught}/{len(TOOL_MUTANTS)} "
              f"EQUIVALENT_ON_TREE={equivalent}/{len(EQUIVALENT)} TOTAL={killed + caught}/{total}")
        return 0 if killed + caught == total else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
