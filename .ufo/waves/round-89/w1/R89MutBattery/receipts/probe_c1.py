#!/usr/bin/env python3
"""R89MutBattery — C1 mutation probe. Mutates a copy of corpus/evidence/round89/gate-records-r89.py,
runs the copy's own frozen predicate on the landing tree, and records which mutants the predicate kills.

The landing tree is an extraction of ac0a0892; the live lane repo is used only as --repo for `git grep`
(read-only). No file inside the lane is written.
"""
import json
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/chousa-r89/R89MutBattery"
L = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
LAND = os.path.join(S, "tree-land")
OUT = os.path.join(S, "out", "c1")
SRC = os.path.join(LAND, "corpus", "evidence", "round89", "gate-records-r89.py")
POS = os.path.join(LAND, "corpus", "evidence", "round89", "c1-positives.tsv")

C1_TOKENS = [
    "GATE_RECORDS_R89=PASS",
    "LEG_REREAD=16/16", "RECONCILED=16/16", "CROSSCHECK=15/15", "LEGS_APPENDED=16",
    "POSITIVE=15/15", "FRESH_POSITIVE=5/5", "FORGED_REFUSED=362/362", "EXPECTED_CODE=362/362",
    "D1_REFUSED=3/3", "D2_REFUSED=3/3", "MUT_ADMIT_KILLED=1", "MUT_UNREACH_KILLED=1",
    "DERIVE_NEG=1",
]

# --- edits copied verbatim from the committed mutate-r89.py (used as building blocks) ---
E7B = [
    ('            mut_admit_derived = mut_admit_killed = 0\n            mut_unreach_derived = mut_unreach_killed = 0\n            if files:',
     '            mut_admit_derived = mut_admit_killed = 0\n            mut_unreach_derived = mut_unreach_killed = 0\n            if False:'),
    ('                ("MUT_ADMIT", mut_admit_derived == 1 and mut_admit_killed == 1,\n                 f"derived={mut_admit_derived} killed={mut_admit_killed}"),',
     '                ("MUT_ADMIT", True,\n                 f"derived={mut_admit_derived} killed={mut_admit_killed}"),'),
    ('                ("MUT_UNREACH", mut_unreach_derived == 1 and mut_unreach_killed == 1,\n                 f"derived={mut_unreach_derived} killed={mut_unreach_killed}"),',
     '                ("MUT_UNREACH", True,\n                 f"derived={mut_unreach_derived} killed={mut_unreach_killed}"),'),
]
E7D = [
    ('        div3 = registry_rows_203(root)', '        div3 = 1'),
    ('                ("D1_WIDTH", len(d1) == d1_expected == div3 == ROWS_203, f"{len(d1)}/{d1_expected}/{div3} pin{ROWS_203}"),',
     '                ("D1_WIDTH", True, f"{ROWS_203}/{ROWS_203}/{ROWS_203} pin{ROWS_203}"),'),
    ('                ("D2_WIDTH", len(d2) == d1_expected == div3 == ROWS_203, f"{len(d2)}/{d1_expected}/{div3} pin{ROWS_203}"),',
     '                ("D2_WIDTH", True, f"{ROWS_203}/{ROWS_203}/{ROWS_203} pin{ROWS_203}"),'),
]

MUTANTS = [
    ("C1-N01-credit-mutants", "healthy", [
        ('            if files:\n                ma = os.path.join(tmp, "tool-MUT-ADMIT.py")\n'
         '                if build_mutant(tool, ma, ADMIT_LITERAL, \'r[6].startswith("2")\'):\n'
         '                    mut_admit_derived = 1\n',
         '            if files:\n                ma = os.path.join(tmp, "tool-MUT-ADMIT.py")\n'
         '                mut_admit_derived = mut_admit_killed = 1\n                if False:\n'
         '                    mut_admit_derived = 1\n'),
    ]),
    ("C1-N02-reconcile-taut-E7b", "healthy", E7B + [
        ('            rederived[name] = r_ok\n            if r_ok is not None and r_ok == got_ok:\n                reconciled += 1\n',
         '            rederived[name] = r_ok\n            if r_ok is not None:\n                reconciled += 1\n'),
    ]),
    ("C1-N03-coherent-width-forgery", "healthy", E7D + [
        ('f"D1_EXPECTED={d1_expected} D1_FORGES={len(d1)} DIV3={div3} D1_REFUSED={d1_refused}/{len(d1)} "',
         'f"D1_EXPECTED={ROWS_203} D1_FORGES={len(d1)} DIV3={ROWS_203} D1_REFUSED={d1_refused}/{len(d1)} "'),
    ]),
    ("C1-N04-crosscheck-div3-dropped", "healthy", E7D + [
        ('                      and _ints("DIV3") == [c] and pin == ROWS_203)',
         '                      and pin == ROWS_203)'),
    ]),
    ("C1-N05-tool-witness", "healthy", [
        ('        legs.append(("TOOL", os.path.isfile(tool), "tool present"))',
         '        legs.append(("TOOL", True, "tool present"))'),
    ]),
    ("C1-N06-positive-set-narrowed", "healthy", [
        ('            pos.append((f, int(n), sid, raw))',
         '            pos.append((f, int(n), sid, raw))\n            break'),
    ]),
    ("C1-N07-expected-legs-15", "healthy", [
        ('EXPECTED_LEGS = 16', 'EXPECTED_LEGS = 15'),
    ]),
    ("C1-N08-rows-203-two", "healthy", [
        ('ROWS_203 = 3', 'ROWS_203 = 2'),
    ]),
    ("C1-N09-fresh-limit-one", "healthy", [
        ('    return admits[:2], revs[:2], unreach[:1]', '    return admits[:1], revs[:2], unreach[:1]'),
    ]),
]

TOOL_MUTANTS = [
    ("T-a-unreach-eq-203",
     '        success = kv["curl_rc"] == "0" and 200 <= int(kv["http"]) < 300',
     '        success = kv["curl_rc"] == "0" and kv["http"] == "203"'),
    ("T-a2-unreach-eq-203-literal-kept",
     '        success = kv["curl_rc"] == "0" and 200 <= int(kv["http"]) < 300',
     '        success = kv["curl_rc"] == "0" and 200 <= int(kv["http"]) < 300 and kv["http"] == "203"'),
    ("T-b-admit-int-300",
     'r[5] == "0" and r[6] == "200"',
     'r[5] == "0" and int(r[6]) < 300'),
    ("T-b2-admit-int-300-literal-kept",
     'r[5] == "0" and r[6] == "200"',
     'r[5] == "0" and (r[6] == "200" or int(r[6]) < 300)'),
    ("T-c-git-blob-empty",
     '        return b.stdout if b.returncode == 0 else None',
     '        return b""'),
]


LEG_PROBES = [
    # the D_WIDTH leg alone: third derivation really narrowed, leg measurement intact
    ("P1-width-leg", [('        div3 = registry_rows_203(root)', '        div3 = 1')]),
    # the CROSSCHECK cell alone: printed summary field displaced, measurement intact
    ("P2-crosscheck-leg", [
        ('f"D1_EXPECTED={d1_expected} D1_FORGES={len(d1)} DIV3={div3} D1_REFUSED={d1_refused}/{len(d1)} "',
         'f"D1_EXPECTED={d1_expected + 1} D1_FORGES={len(d1)} DIV3={div3} D1_REFUSED={d1_refused}/{len(d1)} "'),
    ]),
]


def apply_edits(src, edits):
    body = src
    for old, new in edits:
        n = body.count(old)
        if n != 1:
            raise SystemExit(f"SETUP_MISS anchor count={n} for {old[:70]!r}")
        body = body.replace(old, new, 1)
    return body


def predicate(stdout, rc):
    missing = [t for t in C1_TOKENS if t not in stdout]
    return rc == 0 and not missing, missing


def run(counter, work, tool=None, root=LAND):
    os.makedirs(work, exist_ok=True)
    cmd = [sys.executable, "-B", counter, "--root", root, "--repo", L, "--work", work]
    if tool:
        cmd += ["--tool", tool]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def record(cid, path, rc, out, missing):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(out)
    lines = [ln for ln in out.splitlines()
             if ln.startswith(("LEG_FAIL", "UNRECONCILED", "UNCROSSCHECKED", "SETUP_MISS"))]
    return {"id": cid, "rc": rc,
            "verdict": next((ln for ln in out.splitlines() if ln.startswith("GATE_RECORDS_R89=")), "no-verdict"),
            "missing_tokens": missing, "diag": lines}


def main():
    os.makedirs(OUT, exist_ok=True)
    src = open(SRC, encoding="utf-8").read()
    results = []

    # baseline
    rc, out, err = run(SRC, os.path.join(OUT, "baseline-w"))
    ok, missing = predicate(out, rc)
    with open(os.path.join(OUT, "baseline.txt"), "w", encoding="utf-8") as fh:
        fh.write(out + ("\nSTDERR:\n" + err if err else ""))
    results.append({"id": "BASELINE", "rc": rc, "predicate": ok, "missing_tokens": missing,
                    "verdict": next((ln for ln in out.splitlines() if ln.startswith("GATE_RECORDS_R89=")), "no-verdict")})

    for cid, _kind, edits in MUTANTS:
        mdir = os.path.join(OUT, cid)
        os.makedirs(mdir, exist_ok=True)
        mp = os.path.join(mdir, "gate-records-r89.py")
        open(mp, "w", encoding="utf-8").write(apply_edits(src, edits))
        shutil.copy2(POS, os.path.join(mdir, "c1-positives.tsv"))
        rc, out, err = run(mp, os.path.join(mdir, "w"))
        ok, missing = predicate(out, rc)
        rec = record(cid, os.path.join(mdir, "stdout.txt"), rc, out, missing)
        rec.update({"predicate": ok, "killed": not ok, "edits": len(edits)})
        with open(os.path.join(mdir, "stderr.txt"), "w", encoding="utf-8") as fh:
            fh.write(err)
        results.append(rec)

    # isolated leg probes: the guards the survivors above defeated, each running with its measurement intact
    for pid, edits in LEG_PROBES:
        pdir = os.path.join(OUT, pid)
        os.makedirs(pdir, exist_ok=True)
        pp = os.path.join(pdir, "gate-records-r89.py")
        open(pp, "w", encoding="utf-8").write(apply_edits(src, edits))
        shutil.copy2(POS, os.path.join(pdir, "c1-positives.tsv"))
        rc, out, err = run(pp, os.path.join(pdir, "w"))
        ok, missing = predicate(out, rc)
        rec = record(pid, os.path.join(pdir, "stdout.txt"), rc, out, missing)
        rec.update({"predicate": ok, "killed": not ok, "edits": len(edits)})
        results.append(rec)

    # named-limit 2 probe: the TOOL leg's witness is the filesystem, so run the honest and the mutated
    # counter on a tool-absent tree.
    absent_tool = os.path.join(OUT, "tool-absent", "no-such-tool.py")
    os.makedirs(os.path.dirname(absent_tool), exist_ok=True)
    rc, out, err = run(SRC, os.path.join(OUT, "toolabsent-honest-w"), tool=absent_tool)
    ok, missing = predicate(out, rc)
    with open(os.path.join(OUT, "toolabsent-honest.txt"), "w", encoding="utf-8") as fh:
        fh.write(out + ("\nSTDERR:\n" + err if err else ""))
    results.append({"id": "TOOL-ABSENT-honest", "rc": rc, "predicate": ok,
                    "verdict": next((ln for ln in out.splitlines() if ln.startswith("GATE_RECORDS_R89=")), "no-verdict"),
                    "diag": [ln for ln in out.splitlines() if ln.startswith(("UNRECONCILED", "UNCROSSCHECKED", "LEG_FAIL"))]})
    mutdir = os.path.join(OUT, "C1-N05-tool-witness")
    rc, out, err = run(os.path.join(mutdir, "gate-records-r89.py"),
                       os.path.join(OUT, "toolabsent-mutant-w"), tool=absent_tool)
    ok, missing = predicate(out, rc)
    with open(os.path.join(OUT, "toolabsent-mutant.txt"), "w", encoding="utf-8") as fh:
        fh.write(out + ("\nSTDERR:\n" + err if err else ""))
    results.append({"id": "TOOL-ABSENT-mutant-N05", "rc": rc, "predicate": ok,
                    "verdict": next((ln for ln in out.splitlines() if ln.startswith("GATE_RECORDS_R89=")), "no-verdict"),
                    "diag": [ln for ln in out.splitlines() if ln.startswith(("UNRECONCILED", "UNCROSSCHECKED", "LEG_FAIL"))]})

    # subject-tool mutants, run by the pristine counter
    tool_src = open(os.path.join(LAND, "tools", "gate-records.py"), encoding="utf-8").read()
    for tid, old, new in TOOL_MUTANTS:
        tdir = os.path.join(OUT, "tools", tid)
        os.makedirs(tdir, exist_ok=True)
        tp = os.path.join(tdir, "gate-records.py")
        if tool_src.count(old) != 1:
            raise SystemExit(f"SETUP_MISS tool anchor count={tool_src.count(old)} for {tid}")
        open(tp, "w", encoding="utf-8").write(tool_src.replace(old, new, 1))
        rc, out, err = run(SRC, os.path.join(tdir, "w"), tool=tp)
        ok, missing = predicate(out, rc)
        with open(os.path.join(tdir, "stdout.txt"), "w", encoding="utf-8") as fh:
            fh.write(out + ("\nSTDERR:\n" + err if err else ""))
        results.append({"id": tid, "rc": rc, "predicate": ok, "caught": not ok,
                        "verdict": next((ln for ln in out.splitlines() if ln.startswith("GATE_RECORDS_R89=")), "no-verdict"),
                        "diag": [ln for ln in out.splitlines() if ln.startswith(("LEG_FAIL", "UNRECONCILED", "UNCROSSCHECKED"))],
                        "missing_tokens": missing})

    with open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1)
    for r in results:
        print(json.dumps(r, ensure_ascii=False)[:600])
    return 0


if __name__ == "__main__":
    sys.exit(main())
