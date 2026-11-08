#!/usr/bin/env python3
"""skill-tally-r90 — the round-90 C3 (freshness) counting check.

The lane's `SKILL.md` Gates table states, in every `self-test` cell, the expected output of
`bash tools/research-gate.sh --selftest`. Round 89's non-author spot-check routed that surface (`## Routed defects`
item 5): the rows still said `PASS (275 cases, 0 skipped)` while the tool has printed 283 cases since round 82
(`bash-pin-override-*` cases 276–283). A skill claim about a runnable surface is a freshness claim; this check
re-derives it instead of trusting the row.

It runs the subject selftest once (or reads a captured receipt with `--selftest`), extracts the verdict line's case
and skip counts, then binds the **current** tallies in SKILL.md: every Gates-table row whose first cell names
`research-gate` and every line carrying a `Selftest` + `PASS (` statement. Historical paragraphs that quote earlier
values on purpose (`## Historical — ...`) are counted and printed as `OTHER_OCCURRENCES` but are not bound.

Usage: python3 -B corpus/evidence/round90/skill-tally-r90.py --root DIR [--selftest FILE]
Exit 0 every tally row equals the tool's printed counts (and at least one row exists), 1 a stale row or no row,
2 setup (missing SKILL.md, missing/unparseable selftest output, or the selftest did not print a verdict line).
"""
import argparse
import os
import re
import subprocess
import sys

VERDICT_RE = re.compile(r"^RESEARCH_GATE_SELFTEST: PASS \((\d+) cases, (\d+) skipped\)$", re.M)
TALLY_RE = re.compile(r"PASS \((\d+) cases, (\d+) skipped\)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--selftest", help="captured selftest output; omitted means run the tool")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    skill = os.path.join(root, "SKILL.md")
    if not os.path.isfile(skill):
        print(f"SKILL_TALLY_R90=SETUP missing {skill}")
        return 2
    if a.selftest:
        if not os.path.isfile(a.selftest):
            print(f"SKILL_TALLY_R90=SETUP missing selftest receipt {a.selftest}")
            return 2
        out = open(a.selftest, encoding="utf-8", errors="replace").read()
        rc = 0
    else:
        p = subprocess.run(["bash", "tools/research-gate.sh", "--selftest"], cwd=root,
                           capture_output=True, text=True)
        out, rc = (p.stdout or "") + (p.stderr or ""), p.returncode
    m = VERDICT_RE.search(out)
    if not m:
        print(f"SKILL_TALLY_R90=SETUP no verdict line (selftest rc={rc})")
        return 2
    cases, skipped = int(m.group(1)), int(m.group(2))
    text = open(skill, encoding="utf-8", errors="replace").read()

    def current(line):
        lead = line.lstrip()
        return lead.startswith("| `research-gate") or "Selftest `PASS (" in line

    rows, other = [], 0
    for ln in text.splitlines():
        for m in TALLY_RE.finditer(ln):
            if current(ln):
                rows.append((m.group(1), m.group(2)))
            else:
                other += 1
    stale = [(n, s) for n, s in rows if (int(n), int(s)) != (cases, skipped)]
    if not rows:
        print("SKILL_TALLY_R90=FAIL no tally row in SKILL.md")
        return 1
    for n, s in stale:
        print(f"STALE_TALLY PASS ({n} cases, {s} skipped) != tool {cases}/{skipped}")
    print(f"TALLY_ROWS={len(rows)} STALE_TALLIES={len(stale)}/{len(rows)} "
          f"EXPECTED_CASES={cases} EXPECTED_SKIPPED={skipped} OTHER_OCCURRENCES={other} "
          f"SKILL_TALLY_R90={'PASS' if not stale else 'FAIL'}")
    return 0 if not stale else 1


if __name__ == "__main__":
    sys.exit(main())
