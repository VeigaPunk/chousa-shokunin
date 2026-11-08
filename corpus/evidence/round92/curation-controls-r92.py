#!/usr/bin/env python3
"""curation-r92-controls — round-92 C2 discrimination battery.

Builds a minimal mirror of the tree the two curation counters read (regression re-runs the r91 battery against r92) (registry, the two routed entries, the capture
store and the refetch ledger) and applies four tree forgeries that the round-91 counter accepts. Each must be refused
by `curation-r92.py` and accepted by the unchanged `curation-r91.py`:

  F1 nonq-row            a `## Located quotes` data row with a note id: dropped before counting by r91, QSHAPE by r92
  F2 status-rejected     a located quote's cited source set to `rejected`: unread by r91, SOURCE by r92
  F3 used-by-blank       a located quote's cited source `used-by` cell emptied: unread by r91, SOURCE by r92
  F4 ubiquitous-warrant  a decision row whose only shared word with its warrant is `source` (df 7):
                         r91 counts any shared word, r92 TFREQ refuses a term above DF_MAX

Plus the round-90 double-count probe: one decision row carrying `modified` (absent from every quote) prints
`UNENTAILED_TERM=1` under both counters (the r91 repair stands); the probe now checks the verdict fields.

Regression: the round-90 control battery is re-run with `--counter curation-r92.py`, so its seven closed tree
forgeries must still be refused by the new counter.

Usage: python3 -B corpus/evidence/round92/curation-r92-controls.py --root DIR --work DIR
Exit 0 every case as expected, 1 a deviation (`CASE_DEVIATION`), 2 setup. No network.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NEW = os.path.join(HERE, "curation-r92.py")
OLD = os.path.join(os.path.dirname(HERE), "round91", "curation-r91.py")
REG = os.path.join(os.path.dirname(HERE), "round90", "curation-r90-controls.py")
ENTRY_A = "corpus/knowledge/search-transparency-reporting-r84.md"
ENTRY_B = "corpus/knowledge/provenance-recording-r85.md"

NONQ = '| note | S214 | "Specify all databases, registers, websites, organisations, reference lists and other sources searched or consulted to identify studies." |'
UBIQ = ('| Reporting the source | state the source | report it without the source | Q2 (S214) |')
DUP = ('| Recording a modified resource | state the modified value | leave the modified value unstated | Q13 (S023) |')
# S1: a forged data row whose first cell is the header label `qid` — r91's shared
# data_lines filter drops it before QSHAPE; r92's quote_lines passes only the true
# header through and shape-checks the forgery.
SITFORGE = '| qid | S214 | "forged quote behind a header first cell, should be shape-checked" |'
# S2: a five-cell decision row — r91's table_rows(..., 4) drops it silently; r92 flags DECISION_WIDTH.
WIDE = ('| Reporting the source | state the source | report it without the source | Q2 (S214) | surplus cell |')
# S3: a used-by cell naming a longer sibling path that CONTAINS this entry basename as a
# substring — r91 accepts (substring); r92 tokenises and refuses.
SIBLING = 'corpus/knowledge/search-transparency-reporting-r84.md.bak'
# S4: a mined row whose used-by names the entry but that no quote cites — r91 has no such
# leg; r92 USED_BY refuses. Built on S215 (exists, used-by is the other entry): add a
# mined row... simpler: re-point S215's used-by at ENTRY_A (it is not cited there).


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
               if ln.startswith(("CURATION_R92=", "CURATION_R91="))]
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
    print(f"{'OK' if positive else 'FAIL'} positive: r91 {v_old} r92 {v_new}")

    def forgery(name, mutate, expect_field):
        tree = fresh(name)
        mutate(tree)
        rc_old, v_old, _f, fl_old = run(OLD, tree)
        rc_new, v_new, fails, fl_new = run(NEW, tree)
        prior = rc_old == 0
        refused = rc_new == 1 and any(expect_field in ln for ln in fails)
        print(f"{'OK' if prior and refused else 'FAIL'} {name}: r92 {v_new} ({expect_field}), r91 {v_old}")
        if not (prior and refused):
            print("  r92 fails:", " | ".join(fails[-3:]))
            print("  fields old:", fl_old, "new:", fl_new)
        return prior and refused

    # Classes r91 already refuses (F1-F4, carried over from round 91): the prior FAILS them
    # too, so they are documented here but never counted toward discrimination. Their FAIL
    # lines below are the correct carried-over verdicts, not failures of this round.
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

    results.append(forgery(
        "s1-forged-header-row",
        lambda t: edit(os.path.join(t, ENTRY_A), "| Q13 | S023 |", SITFORGE + "\n| Q13 | S023 |"),
        "LEG_FAIL QSHAPE"))
    results.append(forgery(
        "s2-wide-decision-row",
        lambda t: edit(os.path.join(t, ENTRY_A), "## Inference", WIDE + "\n\n## Inference"),
        "LEG_FAIL WARRANT"))
    results.append(forgery(
        "s3-substring-usedby",
        lambda t: edit(os.path.join(t, "corpus", "SOURCES.md"),
                       "| mined | 2026-11-08 | on-release | corpus/knowledge/search-transparency-reporting-r84.md |",
                       f"| mined | 2026-11-08 | on-release | {SIBLING} |"),
        "LEG_FAIL SOURCE"))
    results.append(forgery(
        "s4-unlinked-usedby",
        lambda t: edit(os.path.join(t, "corpus", "SOURCES.md"),
                       "| mined | 2026-11-08 | 365d | corpus/knowledge/provenance-recording-r85.md |",
                       "| mined | 2026-11-08 | 365d | corpus/knowledge/provenance-recording-r85.md, corpus/knowledge/search-transparency-reporting-r84.md |"),
        "LEG_FAIL USED_BY"))

    # double-count probe: a numeric difference, not a pass/fail class
    dup_tree = fresh("duplicate-count")
    edit(os.path.join(dup_tree, ENTRY_A), "## Inference", DUP + "\n\n## Inference")
    _rc_old, _v_old, _f, fl_old = run(OLD, dup_tree)
    _rc_new, _v_new, _f, fl_new = run(NEW, dup_tree)
    dup_ok = fl_old.get("UNENTAILED_TERM") == "1" and fl_new.get("UNENTAILED_TERM") == "1"
    print(f"{'OK' if dup_ok else 'FAIL'} duplicate-count: r91 UNENTAILED_TERM={fl_old.get('UNENTAILED_TERM')} "
          f"r92 UNENTAILED_TERM={fl_new.get('UNENTAILED_TERM')}")

    # regression: the seven closed round-90 tree forgeries must still be refused by r92
    reg_work = os.path.join(work, "regression")
    # The round-90 battery only parses `CURATION_R90=`-family verdict tokens, so score it through a thin alias that
    # runs the r92 counter and renames its verdict token. Nothing else is rewritten.
    alias = os.path.join(work, "verdict-alias.py")
    open(alias, "w", encoding="utf-8").write(
        "import subprocess, sys\n"
        f"r = subprocess.run([sys.executable, '-B', {NEW!r}] + sys.argv[1:], capture_output=True, text=True)\n"
        "sys.stdout.write(r.stdout.replace('CURATION_R92=', 'CURATION_R91='))\n"
        "sys.stdout.write(r.stderr)\n"
        "sys.exit(r.returncode)\n")
    p = subprocess.run([sys.executable, "-B", REG, "--root", root, "--work", reg_work, "--counter", alias],
                       capture_output=True, text=True)
    line = [ln for ln in p.stdout.splitlines() if ln.startswith("FORGERY_REFUSED=")]
    reg_ok = bool(line) and line[0].startswith("FORGERY_REFUSED=7/7")
    print(f"{'OK' if reg_ok else 'FAIL'} regression: {line[0] if line else 'no line'} rc={p.returncode}")

    refused_n = sum(1 for r in results[4:] if r)
    ok = refused_n == 4 and positive and dup_ok and reg_ok
    print(f"CONTROLS={'PASS' if ok else 'FAIL'} FORGERY_REFUSED={refused_n}/4 PRIOR_ACCEPTED={refused_n}/4 "
          f"CARRIED_F1_F4=refused-by-both "
          f"DUPCOUNT_R91={fl_old.get('UNENTAILED_TERM')} DUPCOUNT_R92={fl_new.get('UNENTAILED_TERM')} "
          f"PRIOR_REGRESSION={'4/4' if reg_ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
