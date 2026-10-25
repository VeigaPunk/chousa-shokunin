#!/usr/bin/env python3
"""stale-count — fail when a count in lane prose disagrees with its receipt.

Counts checked: `QUOTES=<n>`, `<n>-row manifest`, `<n> located quotes`,
`CAPTURE_BOUND=<n>/<n>`, in corpus/QUALITY.md, corpus/README.md, LOG.md and corpus/lessons/round-49.md,
against the data rows of corpus/evidence/round49/spans.tsv (header excluded).

A hit is resolved only by a LATER line in the SAME file reading
`correction: ... superseded by ...` and naming the stale line (`LOG.md:1803`,
`line 1803`): LOG.md is append-only, so a correction entry closes a line; it may
quote the value it supersedes, not a new disagreeing one.

Usage: python3 corpus/evidence/round50/stale-count-check.py [--root REPO] [--receipt TSV]
Exit:  0 no unresolved hit · 1 an unresolved stale hit · 2 usage/missing input.
"""
import argparse, pathlib, re, sys

PROSE = ("corpus/QUALITY.md", "corpus/README.md", "LOG.md", "corpus/lessons/round-49.md")
PATTERNS = (re.compile(r"QUOTES=(\d+)"), re.compile(r"(\d+)-row manifest"),
            re.compile(r"(\d+) located quotes"), re.compile(r"CAPTURE_BOUND=(\d+)/\1"))
CORRECTION = re.compile(r"correction:.*superseded by")
NAMES = re.compile(r"(?::|line\s+)(\d+)\b")


def receipt_rows(path: pathlib.Path) -> int:
    rows = [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    return len(rows) - (1 if rows and rows[0].startswith("id\t") else 0)


def said(text: str, m: int) -> list[int]:
    ns = [int(mo.group(1)) for pat in PATTERNS for mo in pat.finditer(text)]
    return [n for i, n in enumerate(ns) if n != m and n not in ns[:i]]


def scan(lines: list[str], m: int) -> list[tuple[int, int, bool]]:
    """[(lineno, disagreeing number, resolved)] over every count form."""
    nums = [said(t, m) for t in lines]
    named = {j: {int(x) for x in NAMES.findall(t)}
             for j, t in enumerate(lines, 1) if CORRECTION.search(t)}
    quoted = {j: {n for k in ns if 1 <= k <= len(lines) for n in nums[k - 1]}
              for j, ns in named.items()}
    out: list[tuple[int, int, bool]] = []
    for i, ns in enumerate(nums, 1):
        if i in named:
            out += [(i, n, n in quoted[i]) for n in ns]
        elif ns:
            ok = any(j > i and i in named[j] and set(nums[j - 1]) <= quoted[j] for j in named)
            out += [(i, n, ok) for n in ns]
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=None, help="lane repo root (default: this script's repo)")
    ap.add_argument("--receipt", default=None, help="span manifest (default: round-49 spans.tsv)")
    args = ap.parse_args(argv)
    root = pathlib.Path(args.root) if args.root else pathlib.Path(__file__).resolve().parents[3]
    receipt = pathlib.Path(args.receipt) if args.receipt else root / "corpus/evidence/round49/spans.tsv"
    if not receipt.is_file():
        print(f"RECEIPT_MISSING {receipt}")
        return 2
    m = receipt_rows(receipt)
    hits = unresolved = 0
    for rel in PROSE:
        path = root / rel
        if not path.is_file():
            print(f"PROSE_MISSING {rel}")
            return 2
        for lineno, n, ok in scan(path.read_text(encoding="utf-8").splitlines(), m):
            hits += 1
            unresolved += not ok
            print(f"{'RESOLVED' if ok else 'STALE'} {rel}:{lineno} says {n}, receipt {m}")
    print(f"STALE_HITS={hits} UNRESOLVED={unresolved} RECEIPT_ROWS={m}")
    print("STALE_COUNT=" + ("PASS" if not unresolved else "FAIL"))
    return 1 if unresolved else 0


if __name__ == "__main__":
    sys.exit(main())
