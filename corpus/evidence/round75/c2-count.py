#!/usr/bin/env python3
"""Round-75 C2 counter — the round-74 lesson's located-quote token counts.

The r74 verifier spot-check routed one status-neutral defect: the round-74
lesson states its two `Located quote:` token counts as 18 words and 13
whitespace tokens; the quoted strings actually carry 16 and 11 whitespace
tokens (`corpus/lessons/round-74-verifier-spotcheck.md`, "The lesson's
parenthetical 18/13 counts are inaccurate").

This counter derives both counts from the lesson's own quoted strings and
scores four checks over committed bytes at `--rev`:

  Q1  the appended correction block `## Correction — round-74 quote counts`
      appears exactly once (anchored, appended at the end of the lesson)
  Q2  that block states the derived counts 16 and 11
  Q3  that block names the superseded recorded values 18 and 13 as superseded
  Q4  append-only: `git diff --numstat <base> <rev>` removes ZERO lines from
      corpus/lessons/round-74.md

It always prints `DERIVED=S182:<n> S183:<n>`, so the values the block must
state are re-derived at the measured revision rather than asserted.

Exit: 0 C2=PASS (4/4), 1 C2=FAIL, 2 usage/setup. Changing a check after any
seat has scored it is a new claim, not this one's rule.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys

LESSON = "corpus/lessons/round-74.md"
HEAD = "## Correction — round-74 quote counts"
QUOTE_A = re.compile(r"Located quote: “([^”]+)” \((\d+) words\)")
QUOTE_B = re.compile(r"Located quote: `([^`]+)` \(line \d+, (\d+) whitespace tokens\)")


def git(lane: str, *args: str) -> str:
    p = subprocess.run(["git", "-C", lane, *args], capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(f"c2-count: git {' '.join(args)} failed rc={p.returncode}: {p.stderr.strip()[:200]}")
    return p.stdout


def anchored_count(text: str, heading: str) -> int:
    return sum(1 for line in text.splitlines() if line.rstrip() == heading)


def section(text: str, heading: str) -> str:
    lines = text.splitlines()
    starts = [i for i, line in enumerate(lines) if line.rstrip() == heading]
    if not starts:
        return ""
    out = []
    for line in lines[starts[-1] + 1:]:
        if line.startswith("## "):
            break
        out.append(line)
    return "\n".join(out)


def derive(text: str):
    a, b = QUOTE_A.search(text), QUOTE_B.search(text)
    if not a or not b:
        raise SystemExit("c2-count: located quotes not found")
    return len(a.group(1).split()), len(b.group(1).split()), int(a.group(2)), int(b.group(2))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", default="master")
    ap.add_argument("--base", required=True)
    a = ap.parse_args()
    text = git(a.lane, "show", f"{a.rev}:{LESSON}")
    n_a, n_b, rec_a, rec_b = derive(text)
    print(f"DERIVED=S182:{n_a} S183:{n_b} RECORDED=S182:{rec_a} S183:{rec_b}")
    block = section(text, HEAD)
    n = anchored_count(text, HEAD)
    checks = []
    checks.append(("Q1", n == 1, f"correction block count={n}"))
    checks.append(("Q2", n == 1 and str(n_a) in block and str(n_b) in block,
                   f"block states derived counts {n_a}/{n_b}: {str(n_a) in block and str(n_b) in block}"))
    checks.append(("Q3", n == 1 and str(rec_a) in block and str(rec_b) in block,
                   f"block names superseded {rec_a}/{rec_b}: {str(rec_a) in block and str(rec_b) in block}"))
    removed = 0
    for line in git(a.lane, "diff", "--numstat", a.base, a.rev, "--", LESSON).splitlines():
        parts = line.split("\t")
        if len(parts) >= 3 and parts[2] == LESSON:
            removed = int(parts[1]) if parts[1].isdigit() else 1
    checks.append(("Q4", removed == 0, f"removed lines={removed}"))
    for cid, ok, detail in checks:
        print(f"CHECK {cid} {'PASS' if ok else 'FAIL'} {detail}")
    passed = sum(1 for _, ok, _ in checks if ok)
    verdict = "PASS" if passed == len(checks) else "FAIL"
    print(f"C2={verdict} checks={passed}/{len(checks)} rev={a.rev[:12]} base={a.base[:12]}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
