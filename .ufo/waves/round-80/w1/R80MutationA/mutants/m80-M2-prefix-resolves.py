#!/usr/bin/env python3
"""Round-80 gate-grounding counter — every Gate record names bytes that carry its quote.

Round 79's non-author spot-check found three registry rows whose `## Gate` record did
not survive re-opening: a quote one word over the ≤25-word bound (S196, 27 words while
the lesson said 25), a stated count off by one (S197, 25 words while the lesson said
24), and a "located quote" that occurs nowhere in the file it cites (S198). The defect
class is that a Gate record is prose: nothing re-opens it.

This counter makes the record machine-checkable. A row is grounded when its round
lesson carries a record line of the form

  GATE-RECORD <id> rev=<40-hex> path=<repo-relative> line=<n> words=<n> quote=<text>

and the counter, reading only committed bytes at `--rev`, finds:

  R1  `<rev>` resolves in the lane repository;
  R2  `path` exists at `<rev>`;
  R3  line `<n>` of that file contains `quote` (substring, non-empty);
  R4  `quote` word count equals `words` and is ≤ 25 (CORPUS.md contract v1).

Family rule (append-only registry): a row whose `teaches` cell opens `supersedes S###`
replaces that row for the audit. The audit set is the family TIPS a recent Gate decides:
a row enters it when a lesson for a round at or after `--since-round` (default 79, the
round whose Gate records the round-79 spot-check found defective) either carries a
`GATE-RECORD <id>` line or a `- Admit <id>` / `- Reject <id>` bullet for it. So the
audit grows with each round instead of demanding a retrofit of the whole registry, and a
row merely mentioned in prose does not enter it. A defective row that has a grounded
superseder is counted `superseded_resolved`, never silently dropped: the audit prints
every tip it read and every superseded row it resolved.

Counting command (same sentence as `corpus/evidence/round80/claims.md`):

  `python3 -B corpus/evidence/round80/gate-grounding-check.py --rev REV`
  prints `GATE_GROUNDING=PASS unresolved=0` and exits 0.

Exit: 0 every audited tip is grounded · 1 at least one tip is unresolved · 2 usage/env.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys

LANE = pathlib.Path(__file__).resolve().parents[3]
ROW = re.compile(r"^\|[ \t]*(S\d{3,})[ \t]*\|")
RECORD = re.compile(
    r"^GATE-RECORD (S\d{3,}) rev=([0-9a-f]{40}) path=(\S+) line=(\d+) words=(\d+) quote=(.+)$")
SUPERSEDES = re.compile(r"^supersedes (S\d{3,})\b")
LESSON = re.compile(r"corpus/lessons/round-(\d+)\.md")
DECIDED = re.compile(r"^- (?:Admit|Reject) (S\d{3,})\b")


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(LANE), *args],
                          capture_output=True, text=True, timeout=120)


def show(rev: str, path: str) -> str | None:
    p = git("show", f"{rev}:{path}")
    return p.stdout if p.returncode == 0 else None


def rows_at(rev: str) -> dict[str, dict[str, str]]:
    text = show(rev, "corpus/SOURCES.md")
    if text is None:
        return {}
    rows: dict[str, dict[str, str]] = {}
    for line in text.splitlines():
        m = ROW.match(line)
        if not m:
            continue
        cells = line.split("|")
        if len(cells) < 13:
            continue
        rows[m.group(1)] = {
            "teaches": cells[7].strip(),
            "status": cells[8].strip(),
            "opened": cells[9].strip(),
            "used-by": cells[11].strip(),
        }
    return rows


def records_at(rev: str) -> dict[str, dict[str, str]]:
    """id -> last GATE-RECORD for it across the committed lessons at `rev`."""
    p = git("ls-tree", "-r", "--name-only", rev, "--", "corpus/lessons")
    if p.returncode != 0:
        return {}
    out: dict[str, dict[str, str]] = {}
    for path in p.stdout.splitlines():
        if not path.endswith(".md"):
            continue
        text = show(rev, path)
        if text is None:
            continue
        for line in text.splitlines():
            m = RECORD.match(line.strip())
            if not m:
                continue
            out[m.group(1)] = {"rev": m.group(2), "path": m.group(3), "line": m.group(4),
                               "words": m.group(5), "quote": m.group(6).strip(),
                               "lesson": path}
    return out


def check(record: dict[str, str]) -> tuple[bool, str]:
    """Apply R1-R4; return (ok, detail)."""
    _p = git("rev-parse", "--verify", record["rev"][:12])
    if _p.returncode != 0:
        return False, f"R1 revision {record['rev'][:12]} does not resolve"
    record = dict(record, rev=_p.stdout.strip())
    text = show(record["rev"], record["path"])
    if text is None:
        return False, f"R2 {record['path']} absent at {record['rev'][:12]}"
    lines = text.splitlines()
    try:
        idx = int(record["line"]) - 1
    except ValueError:
        return False, f"R2 line {record['line']} is not an integer"
    if idx < 0 or idx >= len(lines):
        return False, f"R3 line {record['line']} outside {record['path']} ({len(lines)} lines)"
    if not record["quote"] or record["quote"] not in lines[idx]:
        return False, f"R3 quote absent from {record['path']}:{record['line']}"
    words = len(record["quote"].split())
    if words != int(record["words"]):
        return False, f"R4 quote is {words} words, record says {record['words']}"
    if words > 25:
        return False, f"R4 quote is {words} words (contract bound is 25)"
    return True, f"{record['path']}:{record['line']}@{record['rev'][:12]} words={words}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--rev", default="master")
    ap.add_argument("--since-round", type=int, default=79)
    a = ap.parse_args()
    rev = a.rev
    p = git("rev-parse", rev)
    if p.returncode != 0:
        print(f"gate-grounding: cannot resolve --rev {rev}", file=sys.stderr)
        return 2
    rev = p.stdout.strip()
    rows = rows_at(rev)
    if not rows:
        print(f"gate-grounding: no registry rows readable at {rev}", file=sys.stderr)
        return 2
    records = records_at(rev)
    parents: dict[str, str] = {}
    for rid, row in rows.items():
        m = SUPERSEDES.match(row["teaches"])
        if m and m.group(1) in rows:
            parents[m.group(1)] = rid
    tips = [rid for rid in rows if rid not in parents]
    decided: set[str] = set()
    lp = git("ls-tree", "-r", "--name-only", rev, "--", "corpus/lessons")
    for path in (lp.stdout.splitlines() if lp.returncode == 0 else []):
        m = LESSON.search(path)
        if not m or int(m.group(1)) < a.since_round or not path.endswith(".md"):
            continue
        text = show(rev, path) or ""
        for line in text.splitlines():
            hit = DECIDED.match(line.strip()) or RECORD.match(line.strip())
            if hit:
                decided.add(hit.group(1))
    audited = sorted(rid for rid in tips if rid in decided)
    print(f"LANE_REV={rev} SINCE_ROUND={a.since_round} TIPS={len(tips)} "
          f"AUDITED={len(audited)}")
    unresolved = 0
    resolved = 0
    for rid in audited:
        record = records.get(rid)
        if record is None:
            unresolved += 1
            print(f"ROW {rid} record=none quote_words=- location=- verdict=UNRESOLVED")
            continue
        ok, detail = check(record)
        if ok:
            print(f"ROW {rid} record=ok quote_words={record['words']} location={detail} "
                  f"verdict=OK")
        else:
            unresolved += 1
            print(f"ROW {rid} record=bad quote_words={record['words']} location={detail} "
                  f"verdict=UNRESOLVED")
    for rid, tip in sorted(parents.items()):
        if rid in audited or rid not in decided:
            continue
        record = records.get(tip)
        if record is not None and check(record)[0]:
            resolved += 1
            print(f"SUPERSEDED {rid} by {tip} record=ok verdict=RESOLVED")
        else:
            unresolved += 1
            print(f"SUPERSEDED {rid} by {tip} record={records.get(tip) and 'bad' or 'none'} "
                  f"verdict=UNRESOLVED")
    verdict = "PASS" if unresolved == 0 else "FAIL"
    print(f"GATE_GROUNDING={verdict} unresolved={unresolved} "
          f"superseded_resolved={resolved} audited={','.join(audited)}")
    return 0 if unresolved == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
