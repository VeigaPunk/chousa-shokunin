#!/usr/bin/env python3
"""Round-76 successor correction counter — QUALITY 136 closure of the r75 presence test.

Measures the round-74 lesson's located-quote token counts and the appended correction
block, at `--rev` over committed bytes:

  DERIVE  both counts are read from the AUTHORED bullets (`- Admit S182`, `- Reject
          S183`), never from the first `Located quote:` match anywhere in the file, so
          a decoy inserted above the bullets cannot rebind them;
  V1      both authored bullets are present and the derivation succeeded;
  V2      the block states the derived counts with word boundaries (`\\b16\\b`, `\\b11\\b`);
  V3      the block names the superseded recorded counts (18, 13) and says `superseded`;
  V4      polarity: a block line carrying the corrected counts carries no negation cue;
  V5      magnitude: every `<n> words` / `<n> whitespace tokens` / `<n> tokens` in the
          block has n in {16, 11, 18, 13} — `161` is not `16`;
  V6      the correction block is the LAST `## ` section of the lesson;
  V7      base ancestry: `git merge-base --is-ancestor <base> <rev>`;
  V8      append-only: `git diff --numstat <base> <rev>` removes zero lines;
  V9      the block heading is not inside an HTML comment.

Prints `DERIVED=S182:<n> S183:<n> RECORDED=S182:<n> S183:<n>` then `CHECK V<n> …` and
`C2V=PASS|FAIL checks=<k>/9 rev=<12> base=<12>`.
Exit 0 PASS, 1 FAIL, 2 usage/setup. Changing a check after any seat has scored it is a
new claim, not this one's rule.

Limits: this binds position, polarity, magnitude and ancestry for this block shape; it
does not prove the prose's meaning, and a fully re-implemented correct counter is not a
forge of it.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys

LESSON = "corpus/lessons/round-74.md"
HEAD = "## Correction — round-74 quote counts"
BULLET_A = "- Admit S182"
BULLET_B = "- Reject S183"
QUOTE_A = re.compile(r"Located quote: “([^”]+)”")
QUOTE_B = re.compile(r"Located quote: `([^`]+)`")
REC_A = re.compile(r"\((\d+) words\)")
REC_B = re.compile(r"\(line \d+, (\d+) whitespace tokens\)")
MAGNITUDE = re.compile(r"(\d+)\s+(?:words|whitespace tokens|tokens)\b")
NEGATIONS = ("not ", "never ", "no correction", "incorrect", "wrong to", "≠", "untrue")
ALLOWED = {16, 11, 18, 13}
CANDIDATE_VALUES = (16, 11)


def git(lane: str, *args: str) -> str:
    p = subprocess.run(["git", "-C", lane, *args], capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(f"c2v: git {' '.join(args)} failed rc={p.returncode}: {p.stderr.strip()[:200]}")
    return p.stdout


def anchored_count(text: str, heading: str) -> int:
    return sum(1 for line in text.splitlines() if line.rstrip() == heading)


def section_index(text: str, heading: str) -> int:
    starts = [i for i, line in enumerate(text.splitlines()) if line.rstrip() == heading]
    return starts[-1] if starts else -1


def section(text: str, heading: str) -> str:
    lines = text.splitlines()
    start = section_index(text, heading)
    if start < 0:
        return ""
    out = []
    for line in lines[start + 1:]:
        if line.startswith("## "):
            break
        out.append(line)
    return "\n".join(out)


def last_section_heading(text: str) -> str:
    heads = [line.rstrip() for line in text.splitlines() if line.startswith("## ")]
    return heads[-1] if heads else ""


def bullet_line(text: str, prefix: str) -> str:
    for line in text.splitlines():
        if line.startswith(prefix):
            return line
    return ""


def derive(text: str):
    a, b = bullet_line(text, BULLET_A), bullet_line(text, BULLET_B)
    qa, qb = QUOTE_A.search(a), QUOTE_B.search(b)
    ra, rb = REC_A.search(a), REC_B.search(b)
    if not (qa and qb and ra and rb):
        return None
    return len(qa.group(1).split()), len(qb.group(1).split()), int(ra.group(1)), int(rb.group(1))


def commented_heading(text: str, heading: str) -> bool:
    index = section_index(text, heading)
    if index < 0:
        return False
    before = "\n".join(text.splitlines()[:index])
    return before.count("<!--") > before.count("-->")


def check(text: str, removed: int, ancestor: bool):
    res = []
    d = derive(text)
    res.append(("V1", d is not None, "authored bullets: " + ("found" if d else "missing quote or count")))
    n_a, n_b, rec_a, rec_b = d if d else (0, 0, 0, 0)
    block = section(text, HEAD)
    count = anchored_count(text, HEAD)
    res.append(("V2", count == 1 and re.search(rf"\b{n_a}\b", block) is not None
                and re.search(rf"\b{n_b}\b", block) is not None,
                f"block count={count} states derived {n_a}/{n_b}"))
    low = block.lower()
    res.append(("V3", count == 1 and str(rec_a) in block and str(rec_b) in block and "superseded" in low,
                f"names superseded {rec_a}/{rec_b} with cue: {all(x in block for x in (str(rec_a), str(rec_b)))} "
                f"cue={'superseded' in low}"))
    lines = [line for line in block.splitlines() if str(n_a) in line and str(n_b) in line]
    bad_polarity = [line for line in lines if any(cue in line.lower() for cue in NEGATIONS)]
    res.append(("V4", count == 1 and bool(lines) and not bad_polarity,
                f"corrected lines={len(lines)} negating={len(bad_polarity)}"))
    magnitudes = [int(n) for n in MAGNITUDE.findall(block)]
    res.append(("V5", count == 1 and all(n in ALLOWED for n in magnitudes),
                "magnitudes=" + ",".join(str(n) for n in magnitudes)))
    res.append(("V6", count == 1 and last_section_heading(text) == HEAD,
                f"last section='{last_section_heading(text)}'"))
    res.append(("V7", ancestor, f"base ancestor of rev={ancestor}"))
    res.append(("V8", removed == 0, f"removed lines={removed}"))
    res.append(("V9", count == 1 and not commented_heading(text, HEAD),
                f"block inside comment={commented_heading(text, HEAD)}"))
    return res


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--lane", default=".")
    ap.add_argument("--rev", default="master")
    ap.add_argument("--base", required=True)
    a = ap.parse_args()
    d = derive(git(a.lane, "show", f"{a.rev}:{LESSON}"))
    n_a, n_b, rec_a, rec_b = d if d else (0, 0, 0, 0)
    print(f"DERIVED=S182:{n_a} S183:{n_b} RECORDED=S182:{rec_a} S183:{rec_b}")
    if d is None:
        print("C2V=FAIL checks=0/9 rev=" + a.rev[:12] + " base=" + a.base[:12])
        return 1
    text = git(a.lane, "show", f"{a.rev}:{LESSON}")
    removed = 0
    for line in git(a.lane, "diff", "--numstat", a.base, a.rev, "--", LESSON).splitlines():
        parts = line.split("\t")
        if len(parts) >= 3 and parts[2] == LESSON:
            removed = int(parts[1]) if parts[1].isdigit() else 1
    anc = subprocess.run(["git", "-C", a.lane, "merge-base", "--is-ancestor", a.base, a.rev],
                         capture_output=True)
    res = check(text, removed, anc.returncode == 0)
    for cid, ok, detail in res:
        print(f"CHECK {cid} {'PASS' if ok else 'FAIL'} {detail}")
    passed = sum(1 for _, ok, _ in res if ok)
    verdict = "PASS" if passed == len(res) else "FAIL"
    print(f"C2V={verdict} checks={passed}/{len(res)} rev={a.rev[:12]} base={a.base[:12]}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
