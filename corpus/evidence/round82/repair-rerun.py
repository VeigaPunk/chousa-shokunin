#!/usr/bin/env python3
"""repair-rerun.py — round-82 post-scoring repair check (not a claim counter; the claims stay as scored).

Re-runs the wave's attack records through the frozen SKILL.md item-2/item-4 Run lines of a tree (--root) and
tabulates rc against each record's wave classification:
  * R82ExecForms/records/*.md with receipts/classification.tsv (class in|ambiguous|out, item 2|4);
  * the R82ReviewerGate and R82CriticClaims records named below, with the reviewer's stated expectation.
Prints one line per record and a summary; exits 0 always (it is a report, not a gate).
Usage: python3 -B corpus/evidence/round82/repair-rerun.py --root <tree> --wave <lane>/.ufo/waves/round-82/w1
"""
import argparse
import csv
import os
import shlex
import subprocess

RUN = {
    2: "f={r}; ! bash tools/research-gate.sh verify \"$f\" --root . | grep -q '^FINDING NEGATIVE_WITHOUT_SWEEP' && bash tools/research-gate.sh verify-sweeps \"$f\" --root .",
    4: "bash tools/research-gate.sh verify-sweeps {r} --root .",
}
# (record, item, expect) — expect: refuse (in-class K2 form) or pass (K2-free; base passed it)
EXTRA = [
    ("R82ReviewerGate/receipts/records/r-dup-rejections.md", 4, "refuse"),
    ("R82ReviewerGate/receipts/records/r-dup-claims.md", 2, "refuse"),
    ("R82ReviewerGate/receipts/records/r-where-mixed.md", 2, "pass"),
    ("R82ReviewerGate/receipts/records/r-mixed-negatives.md", 2, "pass"),
    ("R82ReviewerGate/receipts/records/r-rejected-claims-schema.md", 4, "pass"),
    ("R82CriticClaims/attack-k2a-record.md", 2, "refuse"),
    ("R82CriticClaims/probe-H-rejectheading-why-col.md", 4, "pass"),
    ("R82CriticClaims/probe-H-criteria-section.md", 4, "pass"),
]


def run(root, item, rec):
    p = subprocess.run(["bash", "-c", RUN[item].format(r=shlex.quote(rec))], cwd=root,
                       capture_output=True, text=True, timeout=300)
    return p.returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--wave", required=True)
    a = ap.parse_args()
    root, w = os.path.abspath(a.root), os.path.abspath(a.wave)
    tally = {}
    with open(os.path.join(w, "R82ExecForms/receipts/classification.tsv")) as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            rec = os.path.join(w, "R82ExecForms/records", row["record"] + ".md")
            if not os.path.isfile(rec):
                print(f"MISSING {row['record']}")
                continue
            rc = run(root, int(row["item"]), rec)
            key = (row["class"], "refused" if rc == 1 else f"rc{rc}")
            tally[key] = tally.get(key, 0) + 1
            if row["class"] == "in" and rc != 1:
                print(f"INCLASS_PASS {row['record']} item={row['item']} rc={rc}")
    for rel, item, exp in EXTRA:
        rec = os.path.join(w, rel)
        rc = run(root, item, rec) if os.path.isfile(rec) else None
        ok = (exp == "refuse" and rc == 1) or (exp == "pass" and rc == 0)
        print(f"EXTRA {rel} item={item} expect={exp} rc={rc} {'ok' if ok else 'bad'}")
    for k in sorted(tally):
        print(f"TALLY class={k[0]} {k[1]}={tally[k]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
