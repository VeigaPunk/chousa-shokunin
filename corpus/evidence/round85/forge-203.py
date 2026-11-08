#!/usr/bin/env python3
"""forge-203 — witness for the round-85 REFETCH repair (http exactly 200, not 2xx).

Round 85's frozen C1 predicate counted no forgery of the 200-only class (the `D1-stale-refetch`
leg needed a failed-attempt txt_sha that no admitted record's url carried), so the repair was
asserted but unwitnessed by the predicate (R85CriticClaims). This separate fixture supplies the
witness from committed bytes only: the S021 PubMed row's 203 cookie-challenge body WAS stored by
capture-fetch (it accepted 2xx), so an admit record over that url, key, fetched time and
txt_sha256 passes every check of the OLD tool and must fail REFETCH on the repaired tool.

Usage: python3 -B corpus/evidence/round85/forge-203.py --base-tree DIR --new-tree DIR --repo GITDIR --work DIR
Prints one line per tool: the verdict and exit code for the same forged record.
Exit 0 when the old tool ACCEPTS and the new tool REFUSES with REFETCH; 1 otherwise; 2 usage/IO.
"""
import argparse
import hashlib
import os
import subprocess
import sys

ROW_ID = "S021"
URL = "https://pubmed.ncbi.nlm.nih.gov/17638714/"
QUOTE = "Enable cookies for pubmed.ncbi.nlm.nih.gov and reload this page to continue."


def find_row(tree):
    rows = []
    for ln in open(os.path.join(tree, "corpus/evidence/round57/refetch.tsv"), encoding="utf-8"):
        f = ln.rstrip("\n").split("\t")
        if len(f) == 9 and f[0] == ROW_ID and f[1] == URL:
            rows.append(f)
    for f in rows:
        if f[5] == "0" and f[6] == "203" and f[8] != "-":
            return f
    raise SystemExit("forge-203: no 203 row with a stored body for " + ROW_ID)


def registry_tier(tree):
    for ln in open(os.path.join(tree, "corpus/SOURCES.md"), encoding="utf-8"):
        if ln.startswith("| " + ROW_ID + " |"):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) == 11:
                return cells[3]
    raise SystemExit("forge-203: no registry row for " + ROW_ID)


def run(tool_tree, root, repo, path):
    p = subprocess.run([sys.executable, "-B", os.path.join(tool_tree, "tools/gate-records.py"),
                        "verify", "--root", root, "--repo", repo, path],
                       capture_output=True, text=True)
    line = next((l for l in p.stdout.splitlines() if l.startswith("GATE_RECORD ")), "")
    return p.returncode, line.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-tree", required=True)
    ap.add_argument("--new-tree", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    os.makedirs(a.work, exist_ok=True)
    f = find_row(a.new_tree)
    key, fetched, txt_sha = f[2], f[4], f[8]
    cap = os.path.join(a.new_tree, "corpus/captures", key + ".txt")
    if not os.path.isfile(cap):
        print(f"FORGE203=FAIL missing capture {cap}")
        return 2
    h = hashlib.sha256(open(cap, "rb").read()).hexdigest()
    if h != txt_sha:
        print("FORGE203=FAIL capture sha differs from refetch txt_sha256")
        return 2
    words = len(QUOTE.split())
    tier = registry_tier(a.new_tree)
    rec = (f'GATE-RECORD {ROW_ID} url={URL} fetched={fetched} tier={tier} decision=admit '
           f'capture=corpus/captures/{key}.txt capture_sha256={h[:16]}… words={words} quote="{QUOTE}"')
    path = os.path.join(a.work, "forge203.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(rec + "\n")
    old_rc, old_line = run(a.base_tree, a.new_tree, a.repo, path)
    new_rc, new_line = run(a.new_tree, a.new_tree, a.repo, path)
    print(f"record: {rec}")
    print(f"OLD(base {os.path.basename(a.base_tree)}): rc={old_rc} {old_line}")
    print(f"NEW(landing {os.path.basename(a.new_tree)}): rc={new_rc} {new_line}")
    ok = (old_rc == 0 and " OK" in old_line) and (new_rc == 1 and "FAIL" in new_line and "REFETCH" in new_line)
    print(f"FORGE203={'PASS' if ok else 'FAIL'} old_accepts={old_rc == 0} new_refuses_refetch={'REFETCH' in new_line}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
