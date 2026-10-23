#!/usr/bin/env python3
r"""Validate the counter's OWN output-parsing rules against REAL gate output.

The counter scores a record from two regexes over the gate's stdout:
  LINE_RE      = ^CLAIM id=(\S+) expected=\S+ observed=(\S+)
  FIND_LINE_RE = ^FINDING CLAIM_LINE_MISMATCH .*\bobs=id=(\S+)
This script builds a small local fixture (short spans, so the gate's argv path
works), runs the real gate on it, and checks that the two regexes recover
exactly the id -> observed mapping and the set of ids named by
CLAIM_LINE_MISMATCH. It also checks the gate's mislocated path: a record whose
span is present but whose "line" names the wrong range must read
observed=mislocated and be named by a CLAIM_LINE_MISMATCH finding.

Usage: counter_regex_check.py <work-dir>
"""
import json
import os
import re
import subprocess
import sys

GATE = "/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh"
LINE_RE = re.compile(r"^CLAIM id=(\S+) expected=\S+ observed=(\S+) ")
FIND_LINE_RE = re.compile(r"^FINDING CLAIM_LINE_MISMATCH .*\bobs=id=(\S+)")


def main():
    work = sys.argv[1]
    os.makedirs(os.path.join(work, "src"), exist_ok=True)
    cases = [
        # (id, source text, span, line field or None)
        ("A1", "alpha beta gamma delta", "beta gamma", None),          # supported
        ("A2", "aa\nbb cc\ndd\nee", "bb cc\ndd", "3-4"),              # mislocated (wrong line)
        ("A3", "alpha beta gamma delta", "zeta", None),                # unsupported (absent)
        ("A4", "alpha beta gamma delta", "beta gamm", None),           # unsupported (mutated)
        ("A5", "aa\nbb cc\ndd\nee", "bb cc\ndd", "2-3"),               # supported + bound
        ("A6", "alpha beta gamma delta", "beta gamma", "1"),          # single-line form, bound
        ("A7", "alpha beta gamma delta", "beta gamma", "2"),          # single-line form, mislocated
    ]
    rows = []
    for cid, text, span, line in cases:
        rel = "src/%s.md" % cid
        with open(os.path.join(work, rel), "w") as f:
            f.write(text + "\n")
        rec = {"id": cid, "source": rel, "span": span, "expect": "supported"}
        if line:
            rec["line"] = line
        rows.append(json.dumps(rec))
    claims = os.path.join(work, "claims.jsonl")
    with open(claims, "w") as f:
        f.write("\n".join(rows) + "\n")

    p = subprocess.run(["bash", GATE, "verify-claims", claims, "--root", work],
                       capture_output=True, text=True, timeout=900, cwd=work)
    out = p.stdout
    observed, dup, f_line = {}, set(), set()
    for ln in out.splitlines():
        m = FIND_LINE_RE.match(ln)
        if m:
            f_line.add(m.group(1))
        m = LINE_RE.match(ln)
        if m:
            if m.group(1) in observed:
                dup.add(m.group(1))
            observed[m.group(1)] = m.group(2)
    for cid in dup:
        observed[cid] = "none"

    expect = {"A1": "supported", "A2": "mislocated", "A3": "unsupported",
              "A4": "unsupported", "A5": "supported", "A6": "supported",
              "A7": "mislocated"}
    want_findings = {"A2", "A7"}
    problems = []
    for cid, e in expect.items():
        got = observed.get(cid, "none")
        if got != e:
            problems.append("id=%s observed=%r expected=%r" % (cid, got, e))
    if f_line != want_findings:
        problems.append("CLAIM_LINE_MISMATCH ids=%s expected=%s" % (sorted(f_line), sorted(want_findings)))
    if p.returncode != 1:
        problems.append("gate rc=%d expected 1" % p.returncode)
    if not any(l.startswith("RESEARCH_GATE: DRIFT") for l in out.splitlines()):
        problems.append("no RESEARCH_GATE: DRIFT line")

    for ln in out.splitlines():
        if ln.startswith("CLAIM ") or "CLAIM_LINE_MISMATCH" in ln:
            print("GATE:", ln)
    print("counter-regex view: observed=%s findings=%s dup=%s" % (observed, sorted(f_line), sorted(dup)))
    if problems:
        for x in problems:
            print("PROBLEM:", x)
    else:
        print("COUNTER REGEX CHECK: PASS (5 records; observed map and finding set both as expected)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
