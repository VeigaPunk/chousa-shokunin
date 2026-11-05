#!/usr/bin/env python3
"""Round-79 self-assessment counter v2 — every repair line is validated against the bytes
it names, and the pointer audit covers every block (QUALITY 146 successor).

Round 78's `selfcheck.py` accepted `correction: SKILL.md:168`, `supersedes: 142` and
`erratum: round-77.md:73` as set membership with no content check, so a scratch mirror
carrying all three defects and three hollow repair lines printed `SELFCHECK=PASS
unresolved=0/3` at exit 0 (`R78ReviewB/ALL-three-hollow.txt`), and appending any newer
`## Round-<n> addition` block removed every earlier criterion from pointer auditing
(`R78ReviewB/atkB2-new-block-window.txt`).

Three classes, each repair line carrying a digest assertion about the bytes it names:

  S1  `SKILL.md` gate registry — every row under `## Gates` carries as many cells as its
      header. A malformed row at line N is resolved only by
      `correction: SKILL.md:<N> cells=<n> digest=<16hex>` where `<n>` is the row's actual
      cell count and `<16hex>` is the first 16 hex of `sha256(row bytes)`.
  S2  `corpus/QUALITY.md` — **every** criterion in the file, not only the newest block: each
      path-like token resolves as a path suffix of a committed path. A criterion with an
      unresolved token is resolved only by another criterion carrying
      `supersedes: <id> digest=<16hex>` where `<16hex>` is the first 16 hex of
      `sha256(normalised body of the superseded criterion)` and the superseder's own
      pointers all resolve.
  S3  `corpus/lessons/round-77.md` — every `## Mistakes` table row sits inside the
      `## Mistakes` section. A stranded row at line N is resolved only by
      `erratum: <file>:<N> digest=<16hex>` matching the first 16 hex of
      `sha256(row bytes)`.

Predicate (same sentence as `corpus/evidence/round79/claims.md`):

  `python3 -B corpus/evidence/round79/selfcheck-v2.py --lane .`
  exits 0 and prints exactly `SELFCHECK2=PASS unresolved=0/3`.

`--rev REV` reads every surface and the resolution universe through Git, so a before state
is re-derivable from its own revision. `--digests` prints the digest each repair line must
carry, for the currently unresolved defects.

Usage: python3 corpus/evidence/round79/selfcheck-v2.py --lane DIR [--rev REV] [--digests]
Exit: 0 SELFCHECK2=PASS · 1 SELFCHECK2=FAIL · 2 usage/env.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import subprocess
import sys

PATH_TOKEN = re.compile(r"`([^`\s]+)`")
CORRECTION = re.compile(r"^correction: SKILL\.md:(\d+) cells=(\d+) digest=([0-9a-f]{16})\b")
SUPERSEDES = re.compile(r"supersedes: (\d+) digest=([0-9a-f]{16})")
ERRATUM = re.compile(r"^erratum: ([\w.-]+\.md):(\d+) digest=([0-9a-f]{16})\b")
CRITERION = re.compile(r"^(\d{3})\.\s")
NOT_A_PATH = ("http", "-", "$", "python", "git", "bash", "cc", "/")


def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def read(lane: pathlib.Path, rel: str, rev: str | None) -> str | None:
    if rev:
        p = subprocess.run(["git", "-C", str(lane), "show", f"{rev}:{rel}"],
                           capture_output=True, text=True)
        return p.stdout if p.returncode == 0 else None
    path = lane / rel
    return path.read_text() if path.is_file() else None


def committed_paths(lane: pathlib.Path, rev: str | None) -> list[str]:
    cmd = ["git", "-C", str(lane), "ls-tree", "-r", "--name-only", rev] if rev \
        else ["git", "-C", str(lane), "ls-files"]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return [line for line in p.stdout.splitlines() if line]


def resolves(token: str, tree: list[str]) -> bool:
    tok = token.rstrip("/")
    return any(path == tok or path.endswith("/" + tok) or path.startswith(tok + "/")
               for path in tree)


def cells(line: str) -> list[str]:
    """Split a markdown table row on pipes that are not inside a backtick span."""
    out: list[str] = []
    cur: list[str] = []
    tick = False
    for ch in line.strip():
        if ch == "`":
            tick = not tick
            cur.append(ch)
        elif ch == "|" and not tick:
            out.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    out.append("".join(cur))
    out = [c.strip() for c in out]
    if out and out[0] == "":
        out = out[1:]
    if out and out[-1] == "":
        out = out[:-1]
    return out


def pathlike(token: str) -> bool:
    if (" " in token or "=" in token or "*" in token or ";" in token
            or token.startswith(NOT_A_PATH)):
        return False
    if "/" not in token:
        return False
    core = token.split(":")[0]
    if core.endswith("/"):
        return True
    return bool(re.search(r"\.[A-Za-z0-9]+$", core))


def skill_rows(text: str) -> list[tuple[int, str]]:
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == "## Gates":
            start = i + 1
            break
    if start is None:
        return []
    rows: list[tuple[int, str]] = []
    for i in range(start, len(lines)):
        line = lines[i]
        if not line.startswith("|"):
            if rows and not line.strip():
                break
            continue
        rows.append((i + 1, line))
    return rows


def criteria(text: str) -> dict[int, list[str]]:
    out: dict[int, list[str]] = {}
    current = None
    for line in text.splitlines():
        m = CRITERION.match(line)
        if m:
            current = int(m.group(1))
            out[current] = [line]
        elif current is not None and line and not line.startswith("#"):
            out[current].append(line)
    return out


def body(lines: list[str]) -> str:
    return "\n".join(line.rstrip() for line in lines)


def check_skill(lane: pathlib.Path, rev: str | None, digests: bool) -> tuple[bool, str]:
    text = read(lane, "SKILL.md", rev)
    if text is None:
        return False, "SKILL.md unreadable"
    rows = skill_rows(text)
    if not rows:
        return False, "no ## Gates registry rows"
    header = len(cells(rows[0][1]))
    malformed = [(n, line) for n, line in rows[1:] if len(cells(line)) != header]
    repairs = {}
    for line in text.splitlines():
        m = CORRECTION.match(line)
        if m:
            repairs[int(m.group(1))] = (int(m.group(2)), m.group(3))
    lines = text.splitlines()
    open_defects: list[int] = []
    for n, line in malformed:
        if n in repairs:
            want_cells, want_digest = repairs[n]
            if want_cells == len(cells(line)) and want_digest == digest(line.rstrip("\n")):
                continue
        open_defects.append(n)
    if digests:
        for n, line in malformed:
            print(f"DIGEST correction: SKILL.md:{n} cells={len(cells(line))} "
                  f"digest={digest(line.rstrip(chr(10)))}")
    return not open_defects, (f"header_cells={header} malformed={[n for n, _ in malformed]} "
                              f"repairs={sorted(repairs)} unresolved={open_defects}")


def check_quality(lane: pathlib.Path, rev: str | None, digests: bool) -> tuple[bool, str]:
    text = read(lane, "corpus/QUALITY.md", rev)
    if text is None:
        return False, "corpus/QUALITY.md unreadable"
    crit = criteria(text)
    if not crit:
        return False, "no numbered criteria"
    tree = committed_paths(lane, rev)
    missing: dict[int, list[str]] = {}
    for cid, lines in sorted(crit.items()):
        gaps = [tok for tok in PATH_TOKEN.findall(body(lines))
                if pathlike(tok) and not resolves(tok.split(":")[0], tree)]
        if gaps:
            missing[cid] = gaps
    superseders: dict[int, list[tuple[int, str]]] = {}
    for cid, lines in crit.items():
        for m in SUPERSEDES.finditer(body(lines)):
            superseders.setdefault(int(m.group(1)), []).append((cid, m.group(2)))
    unresolved: list[str] = []
    for cid, gaps in sorted(missing.items()):
        resolved = any(sid not in missing and want == digest(body(crit[cid]))
                       for sid, want in superseders.get(cid, []))
        if not resolved:
            unresolved.append(f"{cid}:{','.join(gaps)}")
    if digests:
        for cid in sorted(missing):
            print(f"DIGEST supersedes: {cid} digest={digest(body(crit[cid]))}")
    return not unresolved, (f"criteria={len(crit)} missing={sorted(missing)} "
                            f"superseders={ {k: [s for s, _ in v] for k, v in superseders.items()} } "
                            f"unresolved={unresolved}")


def check_lesson(lane: pathlib.Path, rev: str | None, digests: bool) -> tuple[bool, str]:
    text = read(lane, "corpus/lessons/round-77.md", rev)
    if text is None:
        return False, "corpus/lessons/round-77.md unreadable"
    lines = text.splitlines()
    section = None
    width = None
    stranded: list[tuple[int, str]] = []
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
            stranded.append((i + 1, line))
    repairs = {}
    for line in lines:
        m = ERRATUM.match(line)
        if m:
            repairs[int(m.group(2))] = (m.group(1), m.group(3))
    open_defects: list[int] = []
    for n, line in stranded:
        if n in repairs:
            want_file, want_digest = repairs[n]
            if want_file == "round-77.md" and want_digest == digest(line.rstrip("\n")):
                continue
        open_defects.append(n)
    if digests:
        for n, line in stranded:
            print(f"DIGEST erratum: round-77.md:{n} digest={digest(line.rstrip(chr(10)))}")
    return not open_defects, (f"mistakes_width={width} stranded={[n for n, _ in stranded]} "
                              f"errata={sorted(repairs)} unresolved={open_defects}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--lane", required=True)
    ap.add_argument("--rev", default=None)
    ap.add_argument("--digests", action="store_true")
    a = ap.parse_args()
    lane = pathlib.Path(a.lane).resolve()
    if not (lane / "SKILL.md").is_file():
        print(f"selfcheck-v2: {lane} is not the lane root", file=sys.stderr)
        return 2
    if a.rev:
        p = subprocess.run(["git", "-C", str(lane), "cat-file", "-e", f"{a.rev}^{{commit}}"],
                           capture_output=True, text=True)
        if p.returncode != 0:
            print(f"selfcheck-v2: cannot resolve --rev {a.rev}", file=sys.stderr)
            return 2
    print(f"LANE={lane} REV={a.rev or 'worktree'}")
    checks = [("S1-skill-registry", check_skill), ("S2-quality-pointers", check_quality),
              ("S3-lesson-mistakes", check_lesson)]
    unresolved = 0
    for name, fn in checks:
        ok, detail = fn(lane, a.rev, a.digests)
        unresolved += not ok
        print(f"CHECK {name} {'ok' if ok else 'FAIL'} {detail}")
    print(f"SELFCHECK2={'PASS' if unresolved == 0 else 'FAIL'} unresolved={unresolved}/{len(checks)}")
    return 0 if unresolved == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
