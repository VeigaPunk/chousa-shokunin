#!/usr/bin/env python3
"""R88ExecC2Forge sweep 2 — verbatim token-floor boundary + stopword-only share +
qid-content swap + isolated sup_unresolved. Same mirror discipline as sweep 1."""
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

def write(d, rel, s):
    open(os.path.join(d, rel), "w", encoding="utf-8").write(s)

def run(root):
    p = subprocess.run([sys.executable, "-B", COUNTER, "--root", root],
                       capture_output=True, text=True)
    return p.returncode, p.stdout.strip().split("\n")

# Verbatim substrings of the S214 capture (whitespace-normalized by the counter).
# Q1 quote committed: "Specify all databases, registers, websites, organisations, reference lists and other
# sources searched or consulted to identify studies." — substrings of it are verbatim in that capture.
SEVEN = "reference lists and other sources searched or consulted"   # 7 tokens
EIGHT = "Specify all databases, registers, websites, organisations, reference lists"  # 8 tokens
SIX = "other sources searched or consulted to"                     # 6 tokens

def sub_quote(qid, quote):
    def f(d):
        s = open(os.path.join(d, ENTRY_A), encoding="utf-8").read()
        s2 = re.sub(r'^\|\s*' + qid + r'\s*\| S214 \|.*$',
                    f'| {qid} | S214 | "{quote}"', s, count=1, flags=re.M)
        assert s2 != s, f"{qid} row not found"
        write(d, ENTRY_A, s2)
    return f

def swap_q10_q11(d):
    pp = os.path.join(d, ENTRY_A)
    s = open(pp, encoding="utf-8").read()
    q10 = re.search(r'^\|\s*Q10\s*\| S023 \|(.*) \|$', s, flags=re.M).group(1)
    q11 = re.search(r'^\|\s*Q11\s*\| S023 \|(.*) \|$', s, flags=re.M).group(1)
    s = re.sub(r'^\|\s*Q10\s*\| S023 \|.*$', f'| Q10 | S023 | {q11} |', s, count=1, flags=re.M)
    s = re.sub(r'^\|\s*Q11\s*\| S023 \|.*$', f'| Q11 | S023 | {q10} |', s, count=1, flags=re.M)
    write(d, ENTRY_A, s)

def stopword_only(d):
    # Cite Q7 (S031, quote has 'which') on the 'Recording when a resource changed' row (warrant Q13).
    # Row cell Do: 'state the date on which the resource was changed' — the only word Q7's quote
    # shares with the row's cells is 'which' (a STOPWORDS member, and terms is stopword-filtered).
    pp = os.path.join(d, ENTRY_A)
    s = open(pp, encoding="utf-8").read()
    n = s.replace('| Q13 (S023) |', '| Q13, Q7 (S031) |', 1)
    assert n != s, "warrant cell not found"
    write(d, ENTRY_B if False else ENTRY_A, n.replace(
        '| Q13, Q7 (S031) |', '| Q13, Q7 (S031) |'))

def d2_isolated(d):
    # S031 teaches gains own contrast+term absent from its capture (publication absent from schema.org page),
    # and a new mined S032 supersedes S031 whose own teaches is clean (contrast 'no comparison', term
    # 'created' present in the DCMI capture that S032 points to). Then S031's flagged row resolves via
    # S032 in the main loop (unresolved=0), but sup_unresolved for S031 must still fire.
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
    s032 = ("| S032 | DCMI Metadata Terms — https://www.dublincore.org/specifications/dublin-core/dcmi-terms/ "
            "| spec | A | DCMI's own term definitions | section 2, /terms/ namespace entries "
            "| supersedes S031 — separate from created date properties, no comparison to other dates | "
            "mined | 2026-11-08 | 365d | — |")
    s = "\n".join(out)
    anchor = re.search(r"\n\| S031 \|", s).start()
    s = s[:anchor+1] + s032 + "\n" + s[anchor+1:]
    write(d, "corpus/SOURCES.md", s)

CASES = [
    ("b1-verbatim-7word-located", sub_quote("Q2", SEVEN)),
    ("b2-verbatim-8word-located", sub_quote("Q1", EIGHT)),
    ("b3-verbatim-6word-below-floor", sub_quote("Q2", SIX)),
    ("a4-swap-q10-q11-quotes", swap_q10_q11),
    ("c1b-stopword-only-share", stopword_only),
    ("d2b-sup-unresolved-isolated", d2_isolated),
]

def main():
    tmp = tempfile.mkdtemp(prefix="c2forge2-", dir=WORK)
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
