#!/usr/bin/env python3
"""R89MutBattery — C2 mutation probe. Counter mutants run against probe trees where the honest
curation-r89.py fails; input-side probes measure the four named limits. The control battery is run with
--counter <mutant> as the second detector (the C2 predicate includes CONTROLS=PASS).
"""
import json
import os
import re
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/chousa-r89/R89MutBattery"
L = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
LAND = os.path.join(S, "tree-land")
OUT = os.path.join(S, "out", "c2")
SRC = os.path.join(LAND, "corpus", "evidence", "round89", "curation-r89.py")
BATTERY = os.path.join(LAND, "corpus", "evidence", "round89", "curation-r89-controls.py")

ENTRY_A = "corpus/knowledge/search-transparency-reporting-r84.md"
ENTRY_B = "corpus/knowledge/provenance-recording-r85.md"
MIRROR_ROW = ("| S219 | mirror row (own-work) — corpus/SOURCES.md | own-work | A | mirror | "
              "corpus/SOURCES.md:1 | supersedes S031 — mirror disposal row | mined | 2026-11-08 | 365d | — |")

C2_TOKENS = [
    "CURATION_R89=PASS", "DUP_QIDS=0", "WARRANT_OK=17/17", "QUOTES_LOCATED=20/20",
    "TEACHES_FLAGGED=1", "TEACHES_UNRESOLVED=0", "SUP_CLAUSE_CHECKED=0", "SUP_UNRESOLVED=0",
]
BATTERY_TOKENS = ["CONTROLS=PASS", "FORGERY_REFUSED=7/7", "PRIOR_ACCEPTED_FORGERY=7/7"]


def mirror(src_root, dst):
    os.makedirs(os.path.join(dst, "corpus", "knowledge"), exist_ok=True)
    os.makedirs(os.path.join(dst, "corpus", "evidence"), exist_ok=True)
    shutil.copy2(os.path.join(src_root, "corpus", "SOURCES.md"), os.path.join(dst, "corpus", "SOURCES.md"))
    for rel in (ENTRY_A, ENTRY_B):
        shutil.copy2(os.path.join(src_root, rel), os.path.join(dst, rel))
    for rel in ("corpus/captures", "corpus/evidence/round57"):
        src = os.path.join(src_root, rel)
        if os.path.isdir(src):
            os.symlink(src, os.path.join(dst, rel))
    return dst


def read(p):
    return open(p, encoding="utf-8", errors="replace").read()


def writew(p, s):
    open(p, "w", encoding="utf-8").write(s)


def mutate_tree(kind, d):
    if kind == "base":
        return
    if kind == "dup":
        p = os.path.join(d, ENTRY_B)
        s = read(p)
        n = s.replace("| Q1 (S215) |", "| Q1, Q1 (S215) |", 1)
        assert n != s
        writew(p, n)
        return
    if kind == "sup":
        rg = os.path.join(d, "corpus", "SOURCES.md")
        out = []
        hit = False
        for ln in read(rg).split("\n"):
            if ln.startswith("| S031 |"):
                ln = ln.replace("no comparison to other date properties claimed",
                                "no comparison to other date properties claimed; distinct from publication dates", 1)
                hit = "distinct from publication dates" in ln
                out.append(ln)
                out.append(MIRROR_ROW)
                continue
            out.append(ln)
        assert hit
        writew(rg, "\n".join(out))
        return
    if kind == "s031":
        rg = os.path.join(d, "corpus", "SOURCES.md")
        out, hit = [], False
        for ln in read(rg).split("\n"):
            if ln.startswith("| S031 |"):
                ln = ln.replace("| mined | 2026-10-21 |", "| queued | 2026-10-21 |", 1)
                hit = "| queued | 2026-10-21 |" in ln
            out.append(ln)
        assert hit
        writew(rg, "\n".join(out))
        return
    if kind == "f2":
        rg = os.path.join(d, "corpus", "SOURCES.md")
        out, hit = [], False
        for ln in read(rg).split("\n"):
            if ln.startswith("| S031 |"):
                ln = ln.replace("| mined | 2026-10-21 |", "| rejected | 2026-10-21 |", 1)
                hit = "| rejected | 2026-10-21 |" in ln
            out.append(ln)
        assert hit
        writew(rg, "\n".join(out))
        return
    if kind == "a1c":
        pp = os.path.join(d, ENTRY_A)
        out, on = [], False
        for ln in read(pp).split("\n"):
            if ln.startswith("## "):
                on = ln.strip() == "## Located quotes"
                out.append(ln)
                continue
            if on and re.match(r"^\s*\|\s*Q11\s*\|", ln):
                continue
            if on and re.match(r"^\s*\|\s*Q13\s*\|", ln):
                out.append(ln)
                out.append('| Q99 | S023 | "validity" |')
                continue
            if "| Q11 (S023) |" in ln:
                ln = ln.replace("| Q11 (S023) |", "| Q99 (S023) |", 1)
            out.append(ln)
        writew(pp, "\n".join(out))
        return
    if kind == "a1d":
        pp = os.path.join(d, ENTRY_A)
        s = read(pp)
        n = re.sub(r'^\|\s*Q11\s*\|.*$', '| Q11 | S023 | "range" |', s, count=1, flags=re.M)
        assert n != s
        writew(pp, n)
        return
    if kind == "caseg":
        pp = os.path.join(d, ENTRY_A)
        lines = read(pp).split("\n")

        def span(lines):
            on = False
            s_ = e_ = None
            for i, ln in enumerate(lines):
                if ln.startswith("## "):
                    if on and s_ is not None:
                        e_ = i
                        break
                    on = ln.strip() == "## Located quotes"
                    if on:
                        s_ = i + 1
            return s_, (e_ if e_ is not None else len(lines))

        s_, e_ = span(lines)
        q13 = None
        out = []
        for i, ln in enumerate(lines):
            if s_ is not None and s_ <= i < e_ and re.match(r"^\s*\|\s*(Q\d+)", ln):
                if re.match(r"^\s*\|\s*Q10\s*\|", ln):
                    continue
                if re.match(r"^\s*\|\s*Q13\s*\|", ln):
                    q13 = ln
            out.append(ln)
        assert q13 is not None
        s2, e2 = span(out)
        out[e2:e2] = [re.sub(r"Q13", "Q14", q13, count=1)]
        writew(pp, "\n".join(out))
        return
    if kind == "b1b":
        pp = os.path.join(d, ENTRY_B)
        s = read(pp)
        n = s.replace("| Q1 (S215) |", "| Q1, Q3 (S215) |", 1)
        assert n != s
        writew(pp, n)
        return
    if kind == "nv":
        pp = os.path.join(d, ENTRY_A)
        s = read(pp)
        old = '| Q2 | S214 | "date when each source was last searched or consulted." |'
        new = '| Q2 | S214 | "the date when each source was last searched or consulted by the team" |'
        assert old in s
        writew(pp, s.replace(old, new, 1))
        return
    if kind == "swap":
        # R88ExecC2Forge finding 4: swap the two S023 quote texts under Q10 and Q11, both rows keeping
        # their qids and >=7-token verbatim quotes.
        pp = os.path.join(d, ENTRY_A)
        lines = read(pp).split("\n")
        qi, qj = {}, {}
        for i, ln in enumerate(lines):
            m = re.match(r"^\|\s*(Q\d+)\s*\|\s*S\d+\s*\|\s*\"(.*)\"\s*\|\s*$", ln)
            if m:
                (qi if m.group(1) == "Q10" else qj if m.group(1) == "Q11" else {}).update({i: m.group(2)})
        assert len(qi) == 1 and len(qj) == 1
        (i, ti), = qi.items()
        (j, tj), = qj.items()
        lines[i] = lines[i].replace('"' + ti + '"', '"' + tj + '"', 1)
        lines[j] = lines[j].replace('"' + tj + '"', '"' + ti + '"', 1)
        writew(pp, "\n".join(lines))
        return
    if kind == "sub7":
        # R88ExecC2Forge finding 1: Q1 replaced by the verbatim 8-token prefix, still sharing `reference`.
        pp = os.path.join(d, ENTRY_A)
        s = read(pp)
        old = '"Specify all databases, registers, websites, organisations, reference lists and other sources searched or consulted to identify studies."'
        new = '"Specify all databases, registers, websites, organisations, reference lists"'
        assert old in s
        writew(pp, s.replace(old, new, 1))
        return
    if kind == "unentailed":
        # a decision cell carries a frozen defect term that no located quote carries (the UNENTAILED leg)
        pp = os.path.join(d, ENTRY_A)
        s = read(pp)
        old = ("| Recording when a resource changed | state the date on which the resource was changed | "
               "record that the resource changed without the date on which it changed | Q13 (S023) |")
        new = ("| Recording when a resource changed | state the date on which the resource was changed | "
               "record that the resource was modified without the date on which it was modified | Q13 (S023) |")
        assert old in s
        writew(pp, s.replace(old, new, 1))
        return
    if kind == "reorder":
        pp = os.path.join(d, ENTRY_A)
        lines = read(pp).split("\n")
        a = b = None
        for i, ln in enumerate(lines):
            if ln.startswith("| Reporting the search method |"):
                a = i
            if ln.startswith("| Reporting how studies were selected |"):
                b = i
        assert a is not None and b is not None
        lines[a], lines[b] = lines[b], lines[a]
        writew(pp, "\n".join(lines))
        return
    raise SystemExit("unknown tree kind " + kind)


MUTANTS = [
    ("C2-N1-set-pin-removed", "caseg", [
        ('    floors_ok = all(loc >= fl and loc == tot and set(qs) == set(QID_SETS.get(rel, ())) and not short\n'
         '                    for rel, loc, tot, fl, qs, short in floor_rows)',
         '    floors_ok = all(loc >= fl and loc == tot and not short\n'
         '                    for rel, loc, tot, fl, qs, short in floor_rows)'),
        ('                   and all(loc >= fl and loc == tot and set(qs) == set(QID_SETS.get(rel, ())) and not short\n'
         '                           for rel, loc, tot, fl, qs, short in floor_rows)',
         '                   and all(loc >= fl and loc == tot and not short\n'
         '                           for rel, loc, tot, fl, qs, short in floor_rows)'),
    ]),
    ("C2-N2-min-tokens-one", "a1d", [
        ('MIN_TOKENS = 7', 'MIN_TOKENS = 1'),
    ]),
    ("C2-N3-warrant-shares-true", "b1b", [
        ('            shares = all(terms & set(re.findall(r"[a-z]{5,}", quotes[q].lower())) for q in resolved)',
         '            shares = True'),
    ]),
    ("C2-N4-dup-detection-deleted", "dup", [
        ('            if len(set(qids)) != len(qids):\n                dup_qids.append((rel, cells[0], cells[3]))\n',
         ''),
    ]),
    ("C2-N5-teaches-unresolved-off", "s031", [
        ('    legs.append(("TEACHES", teaches_checked > 0 and teaches_flagged and not teaches_unresolved and not teaches_sup_unresolved,',
         '    legs.append(("TEACHES", teaches_checked > 0 and teaches_flagged and not teaches_sup_unresolved,'),
        ('                   and len(teaches_unresolved) == 0\n',
         ''),
    ]),
    ("C2-N6-sup-clause-dead", "sup", [
        ('        if miss:\n            teaches_sup_unresolved.append((sid, miss))',
         '        pass'),
        ('    legs.append(("TEACHES", teaches_checked > 0 and teaches_flagged and not teaches_unresolved and not teaches_sup_unresolved,',
         '    legs.append(("TEACHES", teaches_checked > 0 and teaches_flagged and not teaches_unresolved,'),
    ]),
    ("C2-N7-quote-locate-relaxed", "nv", [
        ('            if cap is not None and norm(quote) in cap:',
         '            if cap is not None:'),
    ]),
    ("C2-N8-def-constant-moved", "base", [
        ('MODIFIED_DEF = "date on which the resource was changed"',
         'MODIFIED_DEF = "date on which the resource was modified"'),
    ]),
    ("C2-N9-unentailed-off", "unentailed", [
        ('            for term in DEFECT_TERMS:\n'
         '                if term in (cells[1] + " " + cells[2]).lower() and term not in joined:\n'
         '                    unentailed.append((rel, cells[0], term))',
         '            for term in DEFECT_TERMS:\n'
         '                if False:\n'
         '                    unentailed.append((rel, cells[0], term))'),
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


def run_counter(counter, root, work):
    os.makedirs(work, exist_ok=True)
    p = subprocess.run([sys.executable, "-B", counter, "--root", root], capture_output=True, text=True,
                       env=dict(os.environ, TMPDIR=work))
    return p.returncode, p.stdout, p.stderr


def run_battery(counter, work):
    os.makedirs(work, exist_ok=True)
    p = subprocess.run([sys.executable, "-B", BATTERY, "--root", L, "--work", work, "--counter", counter],
                       capture_output=True, text=True, env=dict(os.environ, TMPDIR=work))
    return p.returncode, p.stdout, p.stderr


def predicate(out, rc):
    return rc == 0 and all(t in out for t in C2_TOKENS), [t for t in C2_TOKENS if t not in out]


def main():
    os.makedirs(OUT, exist_ok=True)
    src = read(SRC)
    results = []

    # 1. honest counter on every probe tree
    trees = {}
    for kind in ("base", "dup", "sup", "s031", "f2", "a1c", "a1d", "caseg", "b1b", "nv", "swap", "sub7", "reorder", "unentailed"):
        d = mirror(L, os.path.join(OUT, "trees", kind))
        mutate_tree(kind, d)
        trees[kind] = d
        rc, out, err = run_counter(SRC, d, os.path.join(OUT, "trees", kind + "-w"))
        with open(os.path.join(OUT, "trees", kind + ".txt"), "w", encoding="utf-8") as fh:
            fh.write(out + ("\nSTDERR:\n" + err if err else ""))
        pf, missing = predicate(out, rc)
        results.append({"id": "TREE-" + kind, "rc": rc, "predicate": pf, "missing_tokens": missing,
                        "verdict": next((ln for ln in out.splitlines() if ln.startswith("CURATION_R89=")), "no-verdict"),
                        "diag": [ln for ln in out.splitlines()
                                 if ln.startswith(("LEG_FAIL", "TEACHES_FLAGGED", "TEACHES_SUP_UNRESOLVED"))]})

    # 2. counter mutants on the tree that exposes each one, plus the battery as second detector
    for cid, kind, edits in MUTANTS:
        mdir = os.path.join(OUT, cid)
        os.makedirs(mdir, exist_ok=True)
        mp = os.path.join(mdir, "curation-r89.py")
        writew(mp, apply_edits(src, edits))
        rc, out, err = run_counter(mp, trees[kind], os.path.join(mdir, "w"))
        with open(os.path.join(mdir, "stdout.txt"), "w", encoding="utf-8") as fh:
            fh.write(out + ("\nSTDERR:\n" + err if err else ""))
        pf, missing = predicate(out, rc)
        rec = {"id": cid, "tree": kind, "rc": rc, "predicate_on_probe_tree": pf, "missing_tokens": missing,
               "verdict": next((ln for ln in out.splitlines() if ln.startswith("CURATION_R89=")), "no-verdict"),
               "diag": [ln for ln in out.splitlines() if ln.startswith(("LEG_FAIL", "TEACHES_FLAGGED", "TEACHES_SUP_UNRESOLVED"))],
               "edits": len(edits)}
        if kind != "base":
            brc, bout, berr = run_battery(mp, os.path.join(mdir, "bw"))
            with open(os.path.join(mdir, "battery.txt"), "w", encoding="utf-8") as fh:
                fh.write(bout + ("\nSTDERR:\n" + berr if berr else ""))
            rec["battery_rc"] = brc
            rec["battery_ok"] = brc == 0 and all(t in bout for t in BATTERY_TOKENS)
            rec["battery_diag"] = [ln for ln in bout.splitlines()
                                   if ln.startswith(("CASE_DEVIATION", "OK ", "FORGERY_REFUSED", "CONTROLS="))]
        results.append(rec)

    with open(os.path.join(OUT, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1)
    for r in results:
        d = dict(r)
        d.pop("diag", None)
        d.pop("battery_diag", None)
        print(json.dumps(d, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
