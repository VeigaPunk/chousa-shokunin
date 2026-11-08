#!/usr/bin/env python3
"""curation-r89-mutants — the round-89 C2 counter mutant battery.

Each mutant is a one-point edit to `curation-r89.py`; the counter's own frozen predicate must FAIL on it, on the
tree named. A survivor is a defect of the counter (the round-88 wave's C2 firings: a dead detector and a detached
leg both printed `CURATION_R88=PASS` over honestly-printed failures).

Trees:
  base        the committed tree
  s031-queued the base tree with S031's status flipped `mined` -> `queued`, so S024 loses its mined disposal and
              `TEACHES_UNRESOLVED=1` is printed honestly (the R88CriticClaims `constants-on-broken` tree)
  sup-mirror  the base tree with S031 carrying a contrast phrase + date term absent from its own capture, behind a
              mined S219 mirror row (the `curation-r89-controls.py` SUP case)

Mutants:
  M1-dead-teaches     the detector never flags (the R88CriticClaims `dead-teaches` shape)
  M2-detached-leg     every leg's `ok` forced True on the broken tree (the `constants-on-broken` shape)
  M3-verdict-legs     `passed` derived from the legs alone, not from the printed fields (the pre-round-89 verdict)
  M4-drop-dup-guard   the DUPQID leg forced ok on a duplicate-qid tree
  M5-lowercase-clause the superseder clause matched against the lowercased cell again (the r88 dead clause)

Usage: python3 -B corpus/evidence/round89/curation-r89-mutants.py --root DIR --work DIR
Exit 0 every mutant killed, 1 a survivor, 2 setup.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
COUNTER = os.path.join(HERE, "curation-r89.py")
ENTRY_A = "corpus/knowledge/search-transparency-reporting-r84.md"
ENTRY_B = "corpus/knowledge/provenance-recording-r85.md"
MIRROR_ROW = ("| S219 | mirror row (own-work) — corpus/SOURCES.md | own-work | A | mirror | "
              "corpus/SOURCES.md:1 | supersedes S031 — mirror disposal row | mined | 2026-11-08 | 365d | — |")

BATTERY = os.path.join(HERE, "curation-r89-controls.py")

MUTANTS = [
    ("M1-dead-teaches", "base", [
        ("""        miss = [t for t in named if cap is None or t not in cap.lower()]
        if miss:
            teaches_flagged.append((sid, miss))""",
         """        miss = [t for t in named if cap is None or t not in cap.lower()]
        if False:
            teaches_flagged.append((sid, miss))"""),
    ]),
    ("M2-detached-leg", "s031-queued", [
        ("""    legs.append(("TEACHES", teaches_checked > 0 and teaches_flagged and not teaches_unresolved and not teaches_sup_unresolved,""",
         """    legs.append(("TEACHES", True,"""),
        ("""    legs.append(("SETUP", True, "registry+entries present"))""",
         """    legs.append(("SETUP", True, "registry+entries present"))
    for _i, (_n, _o, _d) in enumerate(legs):
        legs[_i] = (_n, True, _d)"""),
    ]),
    ("M3-verdict-legs", "s031-queued", [
        ("""    passed = (len(legs) == EXPECTED_LEGS and all(ok for _, ok, _ in legs) and fields_hold)""",
         """    passed = len(legs) == EXPECTED_LEGS and all(ok for _, ok, _ in legs)"""),
        ("""    legs.append(("TEACHES", teaches_checked > 0 and teaches_flagged and not teaches_unresolved and not teaches_sup_unresolved,""",
         """    legs.append(("TEACHES", True,"""),
    ]),
    ("M4a-dup-leg-forced", "dup-qid", [
        ("""    legs.append(("DUPQID", not dup_qids,""", """    legs.append(("DUPQID", True,"""),
    ]),
    ("M4b-dup-field-dropped", "dup-qid", [
        ("""                   and len(dup_qids) == 0
""", ""),
    ]),
    # The counter alone cannot see its own dead clause (a vacuous leg is satisfied by zero detections), so this
    # mutant's detector is the control battery: with the clause dead the SUP-clause mirror is ACCEPTED.
    ("M5-lowercase-clause", "sup-mirror", [
        ("""        if not re.match(r"supersedes (S\\d{3,}) —", cells[6]):
            continue
        tl = cells[6].lower()""",
         """        tl = cells[6].lower()
        if not re.match(r"supersedes (S\\d{3,}) —", tl):
            continue"""),
    ]),
]


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


def build_tree(root, dst, kind):
    mirror(root, dst)
    rg = os.path.join(dst, "corpus", "SOURCES.md")
    lines = open(rg, encoding="utf-8", errors="replace").read().split("\n")
    out = []
    for ln in lines:
        if kind == "s031-queued" and ln.startswith("| S031 |"):
            ln = ln.replace("| mined | 2026-10-21 |", "| queued | 2026-10-21 |", 1)
        if kind == "sup-mirror" and ln.startswith("| S031 |"):
            ln = ln.replace("no comparison to other date properties claimed",
                            "no comparison to other date properties claimed; distinct from publication dates", 1)
            out.append(ln)
            out.append(MIRROR_ROW)
            continue
        out.append(ln)
    open(rg, "w", encoding="utf-8").write("\n".join(out))
    if kind == "dup-qid":
        pp = os.path.join(dst, ENTRY_B)
        s = open(pp, encoding="utf-8", errors="replace").read()
        n = s.replace("| Q1 (S215) |", "| Q1, Q1 (S215) |", 1)
        if n == s:
            raise SystemExit("SETUP_MISS dup-qid: warrant cell not found")
        open(pp, "w", encoding="utf-8").write(n)
    return dst


def verdict_of(stdout):
    v = [ln for ln in stdout.splitlines() if ln.startswith("CURATION_R89=")]
    return v[0] if v else "no-verdict"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--work")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    work = a.work or os.environ.get("TMPDIR") or "/fast/scratch/hyaku"
    os.makedirs(work, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="cur89mut-", dir=work)
    src = open(COUNTER, encoding="utf-8").read()
    try:
        killed = 0
        trees = {}
        for kind in ("base", "s031-queued", "sup-mirror", "dup-qid"):
            trees[kind] = build_tree(root, os.path.join(tmp, "tree-" + kind), kind)
        battery_killed = 0
        for mid, kind, edits in MUTANTS:
            body = src
            for old, new in edits:
                if old not in body:
                    print(f"SETUP_MISS {mid}: anchor not found")
                    return 2
                body = body.replace(old, new, 1)
            mdir = os.path.join(tmp, "c-" + mid)
            os.makedirs(mdir, exist_ok=True)
            mp = os.path.join(mdir, "curation-r89.py")
            with open(mp, "w", encoding="utf-8") as fh:
                fh.write(body)
            p = subprocess.run([sys.executable, "-B", mp, "--root", trees[kind]], capture_output=True, text=True)
            dead = p.returncode != 0 or verdict_of(p.stdout) != "CURATION_R89=PASS"
            if mid.startswith("M5"):
                # the clause-death detector is the battery, not the counter's own verdict
                b = subprocess.run([sys.executable, "-B", BATTERY, "--root", root, "--work", tmp,
                                    "--counter", mp], capture_output=True, text=True)
                bkilled = b.returncode != 0
                dev = [ln for ln in b.stdout.splitlines() if ln.startswith("CASE_DEVIATION")]
                print(f"{'KILLED' if bkilled else 'SURVIVOR'} {mid} tree={kind} detector=battery rc={b.returncode}")
                for ln in dev:
                    print(f"  {ln}")
                battery_killed += 1 if bkilled else 0
                continue
            print(f"{'KILLED' if dead else 'SURVIVOR'} {mid} tree={kind} rc={p.returncode} {verdict_of(p.stdout)}")
            for ln in p.stdout.splitlines():
                if ln.startswith("LEG_FAIL"):
                    print(f"  {ln}")
            killed += 1 if dead else 0
        total = killed + battery_killed
        print(f"MUTANTS_KILLED={total}/{len(MUTANTS)} COUNTER_DETECTED={killed} BATTERY_DETECTED={battery_killed}")
        return 0 if total == len(MUTANTS) else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
