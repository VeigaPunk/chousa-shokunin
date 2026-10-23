#!/usr/bin/env python3
"""Differential fuzz: landed bash gate vs the python oracle, per record.

Both gates are run on the SAME fixture root; the CLAIM id=... observed=... lines
are compared per record id.  Any divergence is a boundary-rule or matcher
divergence.  Nothing here writes to the lane.
"""
import json
import os
import random
import re
import shutil
import subprocess
import sys

CLAIM_RE = re.compile(r"^CLAIM id=(\S+) expected=\S+ observed=(\S+) ")

HERE = os.path.dirname(os.path.abspath(__file__))
BASH_GATE = os.path.join(HERE, "landed-gate-a6307edf.sh")
ORACLE_GATE = os.path.join(HERE, "oracle-gate.sh")


def build(root, seed):
    rng = random.Random(seed)
    os.makedirs(os.path.join(root, "src"))
    ALPHA = "abcdefghijklmnopqrstuvwxyz"
    records = []
    for k in range(60):
        n = rng.choice([1, 2, 3, 7, 40, 300, 4096, 32763, 32764, 32765, 32766, 32767, 32768, 40000])
        body = "".join(rng.choice(ALPHA) for _ in range(max(1, min(n, 200)))) if n > 200 else \
               "".join(rng.choice(ALPHA + " " + "\n") for _ in range(n))
        if n >= 300:
            # long span: words joined by single spaces, ends on a word end
            words = []
            tot = 0
            while tot < n:
                w = "".join(rng.choice(ALPHA) for _ in range(rng.randint(2, 9)))
                words.append(w)
                tot += len(w) + 1
            body = " ".join(words)
            body = body[:n]
            while body and body[-1] == " ":
                body = body[:-1]
        elif n > 0:
            body = body.replace("\n", " ")
            body = body.strip() or "a"
        span = body
        mode = rng.choice(["verbatim", "mut", "glue-l", "glue-r", "dash-l", "quote-l", "uni-l"])
        src_text = ""
        rec = {"id": "r%03d" % k, "source": "src/f%03d.md" % k, "span": span, "expect": "supported"}
        if mode == "verbatim":
            src_text = "lead text\n" + span + "\ntail text\n"
        elif mode == "mut":
            i = rng.randrange(len(span))
            m = span[:i] + ("a" if span[i] != "a" else "b") + span[i + 1:]
            src_text = "lead text\n" + span + "\ntail text\n"
            rec["span"] = m
        elif mode == "glue-l":
            src_text = "lead " + span + "\ntail\n"
        elif mode == "glue-r":
            src_text = "lead\n" + span + "z tail\n"
        elif mode == "dash-l":
            src_text = "lead-x" + span + " tail\n"
        elif mode == "quote-l":
            src_text = "lead'" + span + " tail\n"
        elif mode == "uni-l":
            src_text = "lead é" + span + " tail\n"
        p = os.path.join(root, rec["source"])
        with open(p, "wb") as fh:
            fh.write(src_text.encode("utf-8"))
        if rng.random() < 0.3 and "\n" in src_text:
            lines = src_text.split("\n")
            hit = [i + 1 for i, l in enumerate(lines) if span[:40] and span[:40] in l]
            if hit:
                rec["line"] = "%d" % rng.choice(hit)
        records.append(rec)
    with open(os.path.join(root, "claims.jsonl"), "w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec) + "\n")
    return records


def run(gate, root):
    p = subprocess.run(["bash", gate, "verify-claims", os.path.join(root, "claims.jsonl"),
                        "--root", root], capture_output=True, text=True, timeout=900, cwd=root)
    out = {}
    for line in p.stdout.splitlines():
        m = CLAIM_RE.match(line)
        if m:
            out[m.group(1)] = m.group(2)
    return out, p.returncode, p.stdout, p.stderr


def main():
    seeds = [int(x) for x in sys.argv[1:]] or [7001, 7002, 7003]
    bad = 0
    for seed in seeds:
        root = os.path.join(HERE, "fuzz-%d" % seed)
        shutil.rmtree(root, ignore_errors=True)
        build(root, seed)
        a, rca, _, _ = run(BASH_GATE, root)
        b, rcb, _, _ = run(ORACLE_GATE, root)
        diffs = []
        for cid in sorted(set(a) | set(b)):
            if a.get(cid) != b.get(cid):
                diffs.append((cid, a.get(cid), b.get(cid)))
        print("seed=%d bash_rc=%d oracle_rc=%d records=%d divergences=%d"
              % (seed, rca, rcb, len(a) + len(b), len(diffs)))
        for d in diffs:
            print("  DIVERGE %s bash=%s oracle=%s" % d)
            bad += len(diffs)
        shutil.rmtree(root, ignore_errors=True)
    print("TOTAL_DIVERGENCES=%d" % bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
