#!/usr/bin/env python3
"""curation-r91-controls — round-91 C2 discrimination battery.

Builds a minimal mirror of the tree the two curation counters read (registry, the two routed entries, the capture
store and the refetch ledger) and applies four tree forgeries that round 90's counter accepts. Each must be refused
by `curation-r91.py` and accepted by the unchanged `curation-r90.py`:

  F1 nonq-row            a `## Located quotes` data row with a note id: dropped before counting by r90, QSHAPE by r91
  F2 status-rejected     a located quote's cited source set to `rejected`: unread by r90, SOURCE by r91
  F3 used-by-blank       a located quote's cited source `used-by` cell emptied: unread by r90, SOURCE by r91
  F4 ubiquitous-warrant  a decision row whose only shared word with its warrant is `source` (df 7):
                         r90 counts any shared word, r91 TFREQ refuses a term above DF_MAX

Plus the round-90 double-count probe: one decision row carrying `modified` (absent from every quote) prints
`UNENTAILED_TERM=2` under r90 (the `for term in DEFECT_TERMS:` loop labels it twice) and `UNENTAILED_TERM=1` with the
term it carries under r91.

Regression: the round-90 control battery is re-run with `--counter curation-r91.py`, so its seven closed tree
forgeries must still be refused by the new counter.

Usage: python3 -B corpus/evidence/round91/curation-r91-controls.py --root DIR --work DIR
Exit 0 every case as expected, 1 a deviation (`CASE_DEVIATION`), 2 setup. No network.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NEW = os.path.join(HERE, "curation-r91.py")
OLD = os.path.join(os.path.dirname(HERE), "round90", "curation-r90.py")
REG = os.path.join(os.path.dirname(HERE), "round90", "curation-r90-controls.py")
ENTRY_A = "corpus/knowledge/search-transparency-reporting-r84.md"
ENTRY_B = "corpus/knowledge/provenance-recording-r85.md"

NONQ = '| note | S214 | "Specify all databases, registers, websites, organisations, reference lists and other sources searched or consulted to identify studies." |'
UBIQ = ('| Reporting the source | state the source | report it without the source | Q2 (S214) |')
DUP = ('| Recording a modified resource | state the modified value | leave the modified value unstated | Q13 (S023) |')


def mirror(root, dst):
    os.makedirs(os.path.join(dst, "corpus", "knowledge"), exist_ok=True)
    os.makedirs(os.path.join(dst, "corpus", "evidence"), exist_ok=True)
    shutil.copy2(os.path.join(root, "corpus", "SOURCES.md"), os.path.join(dst, "corpus", "SOURCES.md"))
    for rel in (ENTRY_A, ENTRY_B):
        shutil.copy2(os.path.join(root, rel), os.path.join(dst, rel))
    for rel in (os.path.join("corpus", "captures"), os.path.join("corpus", "evidence", "round57")):
        src = os.path.join(root, rel)
        if os.path.isdir(src):
            os.symlink(src, os.path.join(dst, rel))
    return dst


def run(counter, root):
    p = subprocess.run([sys.executable, "-B", counter, "--root", root], capture_output=True, text=True)
    verdict = [ln for ln in p.stdout.splitlines()
               if ln.startswith(("CURATION_R91=", "CURATION_R90="))]
    fails = [ln for ln in p.stdout.splitlines() if ln.startswith("LEG_FAIL")]
    fields = {}
    for ln in p.stdout.splitlines():
        for k in ("UNENTAILED_TERM", "Q_SHAPE_FAIL", "SOURCE_STATUS_OK", "USED_BY_OK", "TFREQ_OK"):
            m = re.search(rf"(?:^| ){k}=([^ ]+)", ln)
            if m:
                fields[k] = m.group(1)
    return p.returncode, (verdict[0] if verdict else "no-verdict"), fails, fields


def edit(path, old, new, count=1):
    text = open(path, encoding="utf-8").read()
    if old not in text:
        raise SystemExit(f"SETUP pattern absent in {path}: {old[:60]!r}")
    open(path, "w", encoding="utf-8").write(text.replace(old, new, count))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    work = os.path.abspath(a.work)
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work, exist_ok=True)
    pristine = mirror(root, os.path.join(work, "pristine"))

    def fresh(name):
        d = os.path.join(work, name)
        shutil.copytree(pristine, d, symlinks=True)
        return d

    # positive control
    rc_old, v_old, _f, _fl = run(OLD, pristine)
    rc_new, v_new, _f, _fl = run(NEW, pristine)
    positive = rc_old == 0 and rc_new == 0
    print(f"{'OK' if positive else 'FAIL'} positive: r90 {v_old} r91 {v_new}")

    def forgery(name, mutate, expect_field):
        tree = fresh(name)
        mutate(tree)
        rc_old, v_old, _f, fl_old = run(OLD, tree)
        rc_new, v_new, fails, fl_new = run(NEW, tree)
        prior = rc_old == 0
        refused = rc_new == 1 and any(expect_field in ln for ln in fails)
        print(f"{'OK' if prior and refused else 'FAIL'} {name}: r91 {v_new} ({expect_field}), r90 {v_old}")
        if not (prior and refused):
            print("  r91 fails:", " | ".join(fails[-3:]))
            print("  fields old:", fl_old, "new:", fl_new)
        return prior and refused

    results = []
    results.append(forgery(
        "nonq-row",
        lambda t: edit(os.path.join(t, ENTRY_A), "| Q13 | S023 |", NONQ + "\n| Q13 | S023 |"),
        "LEG_FAIL QSHAPE"))
    results.append(forgery(
        "status-rejected",
        lambda t: edit(os.path.join(t, "corpus", "SOURCES.md"),
                       "| mined | 2026-11-08 | on-release | corpus/knowledge/search-transparency-reporting-r84.md |",
                       "| rejected | 2026-11-08 | on-release | corpus/knowledge/search-transparency-reporting-r84.md |"),
        "LEG_FAIL SOURCE"))
    results.append(forgery(
        "used-by-blank",
        lambda t: edit(os.path.join(t, "corpus", "SOURCES.md"),
                       "| mined | 2026-11-08 | on-release | corpus/knowledge/search-transparency-reporting-r84.md |",
                       "| mined | 2026-11-08 | on-release | — |"),
        "LEG_FAIL SOURCE"))
    results.append(forgery(
        "ubiquitous-warrant",
        lambda t: edit(os.path.join(t, ENTRY_A), "## Inference", UBIQ + "\n\n## Inference"),
        "LEG_FAIL TFREQ"))

    # double-count probe: a numeric difference, not a pass/fail class
    dup_tree = fresh("duplicate-count")
    edit(os.path.join(dup_tree, ENTRY_A), "## Inference", DUP + "\n\n## Inference")
    _rc_old, _v_old, _f, fl_old = run(OLD, dup_tree)
    _rc_new, _v_new, _f, fl_new = run(NEW, dup_tree)
    dup_ok = fl_old.get("UNENTAILED_TERM") == "2" and fl_new.get("UNENTAILED_TERM") == "1"
    print(f"{'OK' if dup_ok else 'FAIL'} duplicate-count: r90 UNENTAILED_TERM={fl_old.get('UNENTAILED_TERM')} "
          f"r91 UNENTAILED_TERM={fl_new.get('UNENTAILED_TERM')}")

    # regression: the seven closed round-90 tree forgeries must still be refused by r91
    reg_work = os.path.join(work, "regression")
    # The round-90 battery only parses `CURATION_R90=`-family verdict tokens, so score it through a thin alias that
    # runs the r91 counter and renames its verdict token. Nothing else is rewritten.
    alias = os.path.join(work, "verdict-alias.py")
    open(alias, "w", encoding="utf-8").write(
        "import subprocess, sys\n"
        f"r = subprocess.run([sys.executable, '-B', {NEW!r}] + sys.argv[1:], capture_output=True, text=True)\n"
        "sys.stdout.write(r.stdout.replace('CURATION_R91=', 'CURATION_R90='))\n"
        "sys.stdout.write(r.stderr)\n"
        "sys.exit(r.returncode)\n")
    p = subprocess.run([sys.executable, "-B", REG, "--root", root, "--work", reg_work, "--counter", alias],
                       capture_output=True, text=True)
    line = [ln for ln in p.stdout.splitlines() if ln.startswith("FORGERY_REFUSED=")]
    reg_ok = p.returncode == 0 and line and line[0].startswith("FORGERY_REFUSED=7/7")
    print(f"{'OK' if reg_ok else 'FAIL'} regression: {line[0] if line else 'no line'} rc={p.returncode}")

    refused_n = sum(1 for r in results if r)
    ok = refused_n == 4 and positive and dup_ok and reg_ok
    print(f"CONTROLS={'PASS' if ok else 'FAIL'} FORGERY_REFUSED={refused_n}/4 PRIOR_ACCEPTED={refused_n}/4 "
          f"DUPCOUNT_R90={fl_old.get('UNENTAILED_TERM')} DUPCOUNT_R91={fl_new.get('UNENTAILED_TERM')} "
          f"PRIOR_REGRESSION={'7/7' if reg_ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
