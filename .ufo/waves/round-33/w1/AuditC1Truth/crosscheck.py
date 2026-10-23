#!/usr/bin/env python3
"""Re-score the base gate's raw verify-claims output, independently.

For each kept fixture: run `bash <gate> verify-claims <keep>/claims.jsonl --root
<keep>` from inside the fixture, parse CLAIM/FINDING lines, score every id with
the counter's stated matching rule (one CLAIM line, observed==truth; LINE_MISMATCH
iff mislocated; SOURCE_REVISION_MISMATCH iff stale), and compare the gate's
observed value with this audit's derived contract verdict. Writes one JSON blob.
"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verify_truth

GATE = "/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh"
CLAIM_RE = re.compile(r"^CLAIM id=(\S+) expected=(\S+) observed=(\S+) source=(\S+) at=(\S+) verdict=(\S+)$")
FLINE_RE = re.compile(r"^FINDING CLAIM_LINE_MISMATCH severity=\S+ surface=claims obs=id=(\S+)(?:\s|$)")
FREV_RE = re.compile(r"^FINDING CLAIM_SOURCE_REVISION_MISMATCH severity=\S+ surface=claims obs=id=(\S+)(?:\s|$)")


def run(keep):
    keep = os.path.abspath(keep)
    truth = json.load(open(os.path.join(keep, "truth.json")))
    p = subprocess.run(["bash", GATE, "verify-claims", "claims.jsonl", "--root", "."],
                       cwd=keep, capture_output=True, text=True, timeout=900)
    out = p.stdout
    observed, dup, fl, fr = {}, set(), set(), set()
    for line in out.splitlines():
        m = FLINE_RE.match(line)
        if m:
            fl.add(m.group(1))
        m = FREV_RE.match(line)
        if m:
            fr.add(m.group(1))
        m = CLAIM_RE.match(line)
        if m and m.group(1) in truth:
            if m.group(1) in observed:
                dup.add(m.group(1))
            observed[m.group(1)] = m.group(3)
    for cid in dup:
        observed[cid] = "none"
    # independent derived truth
    lines = open(os.path.join(keep, "claims.jsonl"), encoding="utf-8").read().splitlines()
    derived = {}
    for line in lines:
        rec = verify_truth.parse_line(line)
        derived[rec["id"]] = verify_truth.derive(rec, keep)[0]
    matched, agree, per_class = 0, 0, {}
    disagreements = []
    for cid, (cls, t) in truth.items():
        obs = observed.get(cid, "none")
        ok = (obs == t and ((cid in fl) == (t == "mislocated"))
              and ((cid in fr) == (t == "stale")))
        matched += ok
        pc = per_class.setdefault(cls, [0, 0])
        pc[1] += 1
        pc[0] += ok
        if derived[cid] != t:
            disagreements.append({"id": cid, "class": cls, "truth": t, "derived": derived[cid]})
        if obs == derived[cid]:
            agree += 1
    return {
        "keep": keep, "gate_rc": p.returncode,
        "gate_summary": next((l for l in out.splitlines() if l.startswith("RESEARCH_GATE:")), None),
        "rescore_matched": matched, "total": len(truth),
        "gate_agrees_with_derived": agree,
        "derived_vs_truth_disagreements": disagreements,
        "per_class_rescore": {k: "%d/%d" % tuple(v) for k, v in sorted(per_class.items())},
        "stderr_tail": p.stderr[-300:],
    }


def main():
    print(json.dumps([run(k) for k in sys.argv[1:]], indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
