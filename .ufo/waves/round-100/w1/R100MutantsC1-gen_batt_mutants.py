#!/usr/bin/env python3
"""Generate one-site battery mutants of corpus/evidence/round100/challenge-controls-r100.py at F."""
import pathlib, hashlib

S = pathlib.Path("/fast/scratch/hyaku/chousa-r100/R100MutantsC1")
SRC = (S / "repo" / "corpus" / "evidence" / "round100" / "challenge-controls-r100.py").read_text(encoding="utf-8")
MUTDIR = S / "muts" / "batt"
MUTDIR.mkdir(parents=True, exist_ok=True)

MUTANTS = [
    # B1: REF verdict loosened to rc==1 (any fail code counts)
    ("b1-rev-rc1", 'good = (rc == 1 and v == "CHALLENGE") if want_refused else (rc == 0 and v == "OK")',
     'good = (rc == 1) if want_refused else (rc == 0 and v == "OK")'),
    # B2: REVPOS dropped from ok (order tuple drops REVPOS)
    ("b2-drop-revpos", 'order = ("NEG", "MARK", "BOUND", "NORM", "POS", "REV", "REVPOS", "PROD")',
     'order = ("NEG", "MARK", "BOUND", "NORM", "POS", "REV", "PROD")'),
    # B3: ready/ok guard dropped (t[g][1] > 0 removed) -- empties can't happen but simulate
    ("b3-guard-drop", 'ok = all(t[g][0] == t[g][1] and t[g][1] > 0 for g in order) and (not base_tool or same == len(harm))',
     'ok = all(t[g][0] == t[g][1] for g in order) and (not base_tool or same == len(harm))'),
    # B4: HARM compares returncode only, not stdout
    ("b4-harm-rc-only", 'eq = (a.returncode, a.stdout) == (b.returncode, b.stdout)',
     'eq = (a.returncode,) == (b.returncode,)'),
    # B5: HARM compares stdout only, not returncode
    ("b5-harm-stdout-only", 'eq = (a.returncode, a.stdout) == (b.returncode, b.stdout)',
     'eq = (a.stdout,) == (b.stdout,)'),
    # B6: oracle SITE-MISSING counted as rejected
    ("b6-oracle-sitemissing-pass", 'rejected += not ook',
     'rejected += not ook or 1 if False else not ook'),
    # B7: BASE_REV_ADMITTED informational check absent (base_adm unused, tally prints 0/-1) -- print only
    ("b7-base-adm-print", 't["BASE_REV_ADMITTED"] = (base_adm, sum(1 for c in rev_cases if c[3]))',
     't["BASE_REV_ADMITTED"] = (base_adm, sum(1 for c in rev_cases if c[3]))'),
    # B8: PROD legs skipped for rev forms (PROD covers url+S230,S234 only) -- tighten? no, loosen: want_refused True->False? skip
    # B8: REVPOS want_refused inverted (q legs require CHALLENGE)
    ("b8-q-revpos-refused", '("q1", "S233", f"./corpus/captures/{k233}.txt", False), ("q2", "S233", f"corpus/captures/{k233}.txt", False),',
     '("q1", "S233", f"./corpus/captures/{k233}.txt", True), ("q2", "S233", f"corpus/captures/{k233}.txt", True),'),
    # B9: oracle Setup-failure counted as rejected -> swap continue to rejected+=1? simpler: oracle pass criterion: ook->not ook counts SITE-MISSING as PASS via good flag
    ("b9-oracle-good-flip", 'good = ok and (a.no_oracles or rejected == n_or)',
     'good = ok and (a.no_oracles or rejected >= 0)'),
    # B10: MARK legs use wrong want_refused (probe: flip MARK to False)
    ("b10-mark-admit", 'lab_case("MARK", f"m{i:02d}", f"Site notice 4471.\\n {m}.\\n Reference 88213.\\n".encode(), True)',
     'lab_case("MARK", f"m{i:02d}", f"Site notice 4471.\\n {m}.\\n Reference 88213.\\n".encode(), False)'),
    # B11: BOUND 201 admitted->refused vs admitted, flip b201 want
    ("b11-bound201-refused", 'for w, refused in ((199, True), (200, True), (201, False)):',
     'for w, refused in ((199, True), (200, True), (201, True)):'),
    # B12: HARM len(harm)==0 passes even when harm mismatches (drop base_tool guard on HARM)
    ("b12-harm-guard-drop", 'ok = all(t[g][0] == t[g][1] and t[g][1] > 0 for g in order) and (not base_tool or same == len(harm))',
     'ok = all(t[g][0] == t[g][1] and t[g][1] > 0 for g in order)'),
]

# B6 proper: SITE-MISSING should continue; loosen to count as rejected:
MUTANTS[5] = ("b6-oracle-sitemissing-pass",
    '                if src.count(old) != 1:\n                    print(f"CASE ORACLE {name} SITE-MISSING FAIL")\n                    continue',
    '                if src.count(old) != 1:\n                    print(f"CASE ORACLE {name} SITE-MISSING PASS")\n                    rejected += 1\n                    continue')
# B7 proper: BASE_REV_ADMITTED denominator wrong would change printed tally but not ok; use a real loosen:
# change leg() to not record verdict mismatch; instead make base_adm never counted -> tally line differs but PASS stays
MUTANTS[6] = ("b7-base-adm-dropped",
    '                if base_tool and refused:\n                    brc, bout = run(base_tool, lab.root, rec, work, name + "-base", repo=fx)\n                    base_adm += brc == 0 and verdict(bout) == "OK"',
    '                if base_tool and refused:\n                    brc, bout = run(base_tool, lab.root, rec, work, name + "-base", repo=fx)')

ok = True
manifest = []
for name, old, new in MUTANTS:
    c = SRC.count(old)
    print(name, "count", c)
    if c != 1:
        ok = False
        continue
    m = SRC.replace(old, new)
    (MUTDIR / f"{name}.py").write_text(m, encoding="utf-8")
    h = hashlib.sha256(m.encode()).hexdigest()[:12]
    manifest.append(f"{name} {h}")
    print("OK", name, h)
(S / "muts" / "batt-manifest.txt").write_text("\n".join(manifest) + "\n")
print("ALL EXACT-ONCE" if ok else "FAILURES ABOVE")
