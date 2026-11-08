#!/usr/bin/env python3
"""Build survivor witnesses from committed bytes (and two doctored scratch copies) and run
the landing tool vs the surviving mutant on each. Read-only over the pristine tree."""
import hashlib
import os
import re
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/chousa-r85/R85MutationTool"
TREE = os.path.join(S, "tree")
LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
LANDING = os.path.join(TREE, "tools", "gate-records.py")
OUT = os.path.join(S, "receipts", "witnesses")
MUT = os.path.join(S, "mutants")


def load():
    reg = {}
    for ln in open(os.path.join(TREE, "corpus/SOURCES.md"), encoding="utf-8", errors="replace"):
        m = re.match(r"^ {0,3}\| (S\d{3,}) \|(.+)\|$", ln.rstrip("\n"))
        if m:
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) == 11:
                reg[cells[0]] = cells
    rf = {}
    for ln in open(os.path.join(TREE, "corpus/evidence/round57/refetch.tsv"), encoding="utf-8", errors="replace"):
        f = ln.rstrip("\n").split("\t")
        if len(f) == 9:
            rf.setdefault(f[0], []).append(f)
    return reg, rf


def cap_sha(key):
    return hashlib.sha256(open(os.path.join(TREE, "corpus/captures", key + ".txt"), "rb").read()).hexdigest()


def quote_from(key, n=12):
    text = open(os.path.join(TREE, "corpus/captures", key + ".txt"), encoding="utf-8", errors="replace").read()
    toks = " ".join(text.split()).split(" ")
    toks = [t for t in toks if t]
    q = " ".join(toks[:n])
    return q, len(q.split())


def admit(sid, cells, row, url=None, key=None, fetched=None, sha=None):
    key = key or row[2]
    url = url or row[1]
    fetched = fetched or row[4]
    sha = sha or cap_sha(key)
    q, w = quote_from(key)
    return (f'GATE-RECORD {sid} url={url} fetched={fetched} tier={cells[3]} decision=admit '
            f'capture=corpus/captures/{key}.txt capture_sha256={sha[:16]} words={w} quote="{q}"')


def unreach(sid, cells, row, url=None, fetched=None):
    url = url or row[1]
    fetched = fetched or row[4]
    return (f'GATE-RECORD {sid} url={url} fetched={fetched} tier={cells[3]} decision=reject '
            f'capture=none curl_rc={row[5]} http={row[6]} words=0 quote=none')


def write(name, line):
    p = os.path.join(OUT, name + ".md")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(line + "\n")
    return p


def run(tool, root, rec, label):
    p = subprocess.run([sys.executable, "-B", tool, "verify", "--root", root, "--repo", LANE, rec],
                       capture_output=True, text=True)
    body = (p.stdout + (("\n[STDERR]\n" + p.stderr) if p.stderr else "")).strip()
    return label, p.returncode, body


def main():
    os.makedirs(OUT, exist_ok=True)
    reg, rf = load()
    report = []

    def case(wid, recorder, root, mutant):
        rec = write(wid, recorder)
        rows = [run(LANDING, root, rec, "landing"),
                run(os.path.join(MUT, mutant, "gate-records.py"), root, rec, mutant)]
        report.append((wid, mutant, rows))
        for label, rc, body in rows:
            print(f"--- {wid} / {label} rc={rc}")
            print(body)

    # W-M17: 203-only admit (committed bytes: S021 row http 203, txt_sha == capture sha)
    case("W-M17-203-admit", admit("S021", reg["S021"], rf["S021"][0]), TREE, "M17-refetch-http-2xx-accepted")
    # W-M31: 203 attempt recorded as unreach (committed bytes)
    case("W-M31-203-unreach", unreach("S021", reg["S021"], rf["S021"][0]), TREE, "M31-unreach-success-2xx")
    # W-M14: stale refetch row (committed bytes: S113 row1 txt_sha != current capture sha)
    s113 = rf["S113"][0]
    case("W-M14-stale-refetch", admit("S113", reg["S113"], s113, sha=cap_sha(s113[2])), TREE,
         "M14-refetch-txtsha-conjunct-dropped")
    # W-M30: Unicode-digit year inside the timestamp (Z kept), committed S008 row
    s008 = rf["S008"][0]
    ts = s008[4]
    trans = str.maketrans("0123456789", "\u0660\u0661\u0662\u0663\u0664\u0665\u0666\u0667\u0668\u0669")
    uni_fetched = ts[:4].translate(trans) + ts[4:]
    case("W-M30-unicode-ts", admit("S008", reg["S008"], s008, fetched=uni_fetched), TREE,
         "M30-ts-regex-unicode-relaxed")

    # Doctored scratch roots for the two conjuncts whose committed data has no isolating row.
    for wid, mut, key, val in (
        ("W-M16-refetch-rc28", "M16-refetch-curlrc-accepted", "5", "28"),
        ("W-M13-refetch-key-zero", "M13-refetch-key-conjunct-dropped", "2", "0" * 24),
    ):
        root = os.path.join(S, "tree-doc-" + wid.split("-")[1].lower())
        if os.path.isdir(root):
            shutil.rmtree(root)
        shutil.copytree(TREE, root)
        refp = os.path.join(root, "corpus/evidence/round57/refetch.tsv")
        lines = open(refp, encoding="utf-8").read().split("\n")
        hit = 0
        for i, ln in enumerate(lines):
            f = ln.split("\t")
            if len(f) == 9 and f[0] == "S008" and f[4] == s008[4]:
                f[int(key)] = val
                lines[i] = "\t".join(f)
                hit += 1
                break
        assert hit == 1, wid
        with open(refp, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines))
        rec = write(wid, admit("S008", reg["S008"], s008))
        rows = [run(LANDING, root, rec, "landing"),
                run(os.path.join(MUT, mut, "gate-records.py"), root, rec, mut)]
        report.append((wid, mut, rows))
        for label, rc, body in rows:
            print(f"--- {wid} / {label} rc={rc}")
            print(body)

    with open(os.path.join(OUT, "summary.txt"), "w", encoding="utf-8") as fh:
        for wid, mutant, rows in report:
            fh.write(f"== {wid} vs {mutant}\n")
            for label, rc, body in rows:
                fh.write(f"{label} rc={rc}\n{body}\n")
            fh.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
