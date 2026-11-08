#!/usr/bin/env python3
"""R88ExecC2Forge sweep 3 — isolated sup_unresolved on a fresh sid; verdict-wording check.
S032 already exists (Shojania, queued). Use S099 for the new mined superseder."""
import os, re, shutil, subprocess, sys, tempfile

ROOT = "/fast/scratch/hyaku/chousa-r88/R88ExecC2Forge/tree"
COUNTER = os.path.join(ROOT, "corpus/evidence/round88/curation-r88.py")
WORK = "/fast/scratch/hyaku/chousa-r88/R88ExecC2Forge"
ENTRY_A = "corpus/knowledge/search-transparency-reporting-r84.md"
ENTRY_B = "corpus/knowledge/provenance-recording-r85.md"

def mirror(dst):
    os.makedirs(os.path.join(dst, "corpus", "knowledge"), exist_ok=True)
    os.makedirs(os.path.join(dst, "corpus", "evidence"), exist_ok=True)
    for rel in ("corpus/SOURCES.md", ENTRY_A, ENTRY_B):
        shutil.copy2(os.path.join(ROOT, rel), os.path.join(dst, rel))
    for link, target in (("corpus/captures", os.path.join(ROOT, "corpus/captures")),
                         ("corpus/evidence/round57", os.path.join(ROOT, "corpus/evidence/round57"))):
        p = os.path.join(dst, link)
        if not os.path.exists(p):
            os.symlink(target, p)
    return dst

def run(root):
    p = subprocess.run([sys.executable, "-B", COUNTER, "--root", root],
                       capture_output=True, text=True)
    return p.returncode, p.stdout.strip().split("\n")

def d2c(d):
    pp = os.path.join(d, "corpus/SOURCES.md")
    lines = open(pp, encoding="utf-8").read().split("\n")
    out = []
    for ln in lines:
        if ln.startswith("| S031 |"):
            old = "no comparison to other date properties claimed"
            new = "no comparison to other date properties claimed; separate from publication dates"
            assert old in ln
            ln = ln.replace(old, new, 1)
        out.append(ln)
    s099 = ("| S099 | DCMI Metadata Terms — https://www.dublincore.org/specifications/dublin-core/dcmi-terms/ "
            "| spec | A | DCMI's own term definitions | section 2, /terms/ namespace entries "
            "| supersedes S031 — separate from created date properties, no comparison to other dates | "
            "mined | 2026-11-08 | 365d | — |")
    s = "\n".join(out)
    anchor = re.search(r"\n\| S031 \|", s).start()
    s = s[:anchor+1] + s099 + "\n" + s[anchor+1:]
    open(pp, "w", encoding="utf-8").write(s)

def dup_repair_7(d):
    """b-floor sharper: a 7-word quote that shares NO distinctive term with its row.
    Q5 row (Reporting the search outcome) gets Q1-substring 'reference lists and other sources searched
    or consulted' (7 words). Row Do: 'describe the results from records identified to studies included'.
    Shared 5+ words? 'records' in quote? quote has 'searched','consulted','reference','sources' — row
    distinctive: describe, results, records, identified, studies, included. Pattern-matched verbatim
    words in quote: reference, lists, other, sources, searched, consulted. None in row cells. So FLOOR
    passes (7 tokens) but WARRANT must fail. That isolates the warrant dependence on token-floor pass."""
    pp = os.path.join(d, ENTRY_A)
    s = open(pp, encoding="utf-8").read()
    s2 = re.sub(r'^\|\s*Q5\s*\| S214 \|.*$',
                '| Q5 | S214 | "reference lists and other sources searched or consulted" |', s, count=1, flags=re.M)
    assert s2 != s
    open(pp, "w", encoding="utf-8").write(s2)

CASES = [("d2c-sup-isolated-S099", d2c), ("b4-verbatim-7word-no-share", dup_repair_7)]

def main():
    tmp = tempfile.mkdtemp(prefix="c2forge3-", dir=WORK)
    try:
        for cid, mut in CASES:
            d = mirror(os.path.join(tmp, cid))
            mut(d)
            rc, lines = run(d)
            print(f"### {cid}")
            for l in lines: print("   ", l)
            print(f"    rc={rc}")
            print()
    finally:
        print("TREES_KEPT_AT", tmp)

if __name__ == "__main__":
    main()
