#!/usr/bin/env python3
"""Round-78 self-assessment counter — do the lane's self-descriptions resolve?

Three classes of self-assessment defect, each named by the round-77 non-author spot-check
(`corpus/lessons/round-77-verifier-spotcheck.md`, routed defects 1, 3 and 4):

  S1  `SKILL.md` gate registry — every registry row carries as many cells as its header. A
      malformed row is resolved by a later `correction: SKILL.md:<line>` line naming that
      row's line number (the registry is append-only evidence, so a row is never rewritten).
  S2  `corpus/QUALITY.md` newest criteria — every path-like token in the criteria added by
      the last `## Round-<n> addition` block resolves as a path suffix of a committed path.
      A criterion is resolved by a later criterion carrying `supersedes: <id>` **and** whose
      own pointers resolve.
  S3  `corpus/lessons/round-77.md` — every `## Mistakes` table row sits inside the
      `## Mistakes` section. A stranded row is resolved by a line carrying
      `erratum: round-77.md:<line>`.

Predicate (same sentence as `corpus/evidence/round78/claims.md`):

  `python3 -B corpus/evidence/round78/selfcheck.py --lane .`
  exits 0 and prints exactly `SELFCHECK=PASS unresolved=0/3`.

The counter is lexical: it proves presence, position and reachability, not that a
correction states the truth. `--rev` reads every surface and the resolution universe
through Git, so a before state is re-derivable from its own revision.

Usage: python3 corpus/evidence/round78/selfcheck.py --lane DIR [--rev REV] [--verbose]
Exit: 0 SELFCHECK=PASS · 1 SELFCHECK=FAIL · 2 usage/env.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys

PATH_TOKEN = re.compile(r"`([^`\s]+)`")
CORRECTION = re.compile(r"^correction: SKILL\.md:(\d+)")
SUPERSEDES = re.compile(r"supersedes: (\d+)")
ERRATUM = re.compile(r"erratum: round-77\.md:(\d+)")
NOT_A_PATH = ("http", "-", "$", "python", "git", "bash", "cc", "/")


def read(lane: pathlib.Path, rel: str, rev: str | None) -> str | None:
    if rev:
        p = subprocess.run(["git", "-C", str(lane), "show", f"{rev}:{rel}"],
                           capture_output=True, text=True)
        return p.stdout if p.returncode == 0 else None
    path = lane / rel
    return path.read_text() if path.is_file() else None


def committed_paths(lane: pathlib.Path, rev: str | None) -> list[str]:
    """Every committed path at the named revision (the resolution universe)."""
    cmd = (["git", "-C", str(lane), "ls-tree", "-r", "--name-only", rev] if rev
           else ["git", "-C", str(lane), "ls-files"])
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        return []
    return [line for line in p.stdout.splitlines() if line]


def resolves(token: str, tree: list[str]) -> bool:
    """A token resolves when it matches a path suffix of a committed path.

    Criteria cite paths relative to their own receipt directory (`controls/x.txt`,
    `R76Review/y.out`), so lane-root resolution would false-fail them; a suffix match
    resolves the citation wherever it actually lives.
    """
    tok = token.lstrip("./")
    if "*" in tok:
        rx = re.compile("^" + re.escape(tok).replace(r"\*", ".*") + "$")
        return any(rx.search(path) for path in tree)
    return any(path == tok or path.endswith("/" + tok) for path in tree)


def cells(line: str) -> list[str]:
    """Split a markdown table row on pipes that are not inside a backtick span."""
    out: list[str] = []
    cur: list[str] = []
    inb = False
    for ch in line.strip():
        if ch == "`":
            inb = not inb
        if ch == "|" and not inb:
            out.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    out.append("".join(cur))
    if out and not out[0].strip():
        out = out[1:]
    if out and not out[-1].strip():
        out = out[:-1]
    return out


def check_skill(lane: pathlib.Path, rev: str | None) -> tuple[bool, str]:
    text = read(lane, "SKILL.md", rev)
    if text is None:
        return False, "SKILL.md unreadable"
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == "## Gates":
            start = i + 1
            break
    if start is None:
        return False, "no ## Gates heading"
    header = None
    malformed: list[int] = []
    for i in range(start, len(lines)):
        line = lines[i]
        if not line.startswith("|"):
            if header is not None and not line.strip():
                break
            continue
        row = cells(line)
        if header is None:
            header = len(row)
        elif len(row) != header:
            malformed.append(i + 1)
    corrected = {int(m.group(1)) for line in lines
                 for m in [CORRECTION.match(line)] if m}
    open_defects = [n for n in malformed if n not in corrected]
    return not open_defects, (f"rows_malformed={malformed} corrected={sorted(corrected)} "
                              f"unresolved={open_defects}")


def check_quality(lane: pathlib.Path, rev: str | None) -> tuple[bool, str]:
    text = read(lane, "corpus/QUALITY.md", rev)
    if text is None:
        return False, "corpus/QUALITY.md unreadable"
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if re.match(r"^## Round-\d+ addition", line):
            start = i + 1
    if start is None:
        return False, "no round-addition block"
    bodies: dict[int, str] = {}
    current = None
    for line in lines[start:]:
        m = re.match(r"^(\d{3})\.\s", line)
        if m:
            current = int(m.group(1))
            bodies[current] = line
        elif current is not None and line and not line.startswith("#"):
            bodies[current] += "\n" + line
    superseders: dict[int, list[int]] = {}
    for cid, body in bodies.items():
        for m in SUPERSEDES.finditer(body):
            superseders.setdefault(int(m.group(1)), []).append(cid)
    tree = committed_paths(lane, rev)
    missing: dict[int, list[str]] = {}
    for cid, body in sorted(bodies.items()):
        gaps = []
        for tok in PATH_TOKEN.findall(body):
            if " " in tok or tok.startswith(NOT_A_PATH) or "/" not in tok:
                continue
            if not resolves(tok, tree):
                gaps.append(tok)
        if gaps:
            missing[cid] = gaps
    unresolved: list[str] = []
    for cid, gaps in sorted(missing.items()):
        clean_superseder = any(cid not in missing for cid in superseders.get(cid, []))
        if not clean_superseder:
            unresolved.append(f"{cid}:{','.join(gaps)}")
    return not unresolved, (f"criteria={sorted(bodies)} missing={sorted(missing)} "
                            f"superseders={superseders} unresolved={unresolved}")


def check_lesson(lane: pathlib.Path, rev: str | None) -> tuple[bool, str]:
    text = read(lane, "corpus/lessons/round-77.md", rev)
    if text is None:
        return False, "corpus/lessons/round-77.md unreadable"
    lines = text.splitlines()
    section = None
    width = None
    stranded: list[int] = []
    for i, line in enumerate(lines):
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        if not line.startswith("|"):
            continue
        row = cells(line)
        if section == "Mistakes":
            if width is None and row and row[0].strip() == "class":
                width = len(row)
            continue
        if width is not None and len(row) == width and row[0].strip() not in ("", "class"):
            stranded.append(i + 1)
    corrected = {int(m.group(1)) for line in lines
                 for m in [ERRATUM.match(line)] if m}
    open_defects = [n for n in stranded if n not in corrected]
    return not open_defects, (f"mistakes_width={width} stranded={stranded} "
                              f"errata={sorted(corrected)} unresolved={open_defects}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--lane", required=True)
    ap.add_argument("--rev", default=None)
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    if not (lane / "SKILL.md").is_file():
        print(f"selfcheck: {lane} is not the lane root", file=sys.stderr)
        return 2
    if a.rev:
        p = subprocess.run(["git", "-C", str(lane), "cat-file", "-e", f"{a.rev}^{{commit}}"],
                           capture_output=True, text=True)
        if p.returncode != 0:
            print(f"selfcheck: cannot resolve --rev {a.rev}", file=sys.stderr)
            return 2
    print(f"LANE={lane} REV={a.rev or 'worktree'}")
    checks = [("S1-skill-registry", check_skill), ("S2-quality-pointers", check_quality),
              ("S3-lesson-mistakes", check_lesson)]
    unresolved = 0
    for name, fn in checks:
        ok, detail = fn(lane, a.rev)
        unresolved += not ok
        suffix = f" {detail}" if (a.verbose or not ok) else ""
        print(f"CHECK {name} {'ok' if ok else 'FAIL'}{suffix}")
    print(f"SELFCHECK={'PASS' if unresolved == 0 else 'FAIL'} unresolved={unresolved}/{len(checks)}")
    return 0 if unresolved == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
