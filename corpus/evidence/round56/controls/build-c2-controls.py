#!/usr/bin/env python3
"""Build the R56-C2 controls as scratch lane roots under OUTDIR (outside the lane).

  staged/   BASE_REV tree + the package entry `grey-literature-field-china-r42.md` copied
            unchanged + the staged rows S155 S156 S157 appended to the Registry as staged (ids,
            dates and cells unchanged) — the bulk-append shortcut.
  rewrite/  BASE_REV tree + the same entry with its `source:` lines renumbered BY DOCUMENT to
            fresh ids (S155 journal copy -> S129, S156 note -> S128, S157 NHC 2020 -> S130) + the
            staged S168 standard row as S127 and the three entry rows rewritten mechanically (new
            id, `mined`, opened 2026-10-27, `used-by` = the entry) — binding without quotes,
            spans or lesson.

Score: python3 corpus/evidence/round56/c2-count.py --root OUTDIR/<name>
Usage: python3 corpus/evidence/round56/controls/build-c2-controls.py OUTDIR
"""
from __future__ import annotations

import io
import pathlib
import re
import subprocess
import sys
import tarfile

LANE = pathlib.Path(__file__).resolve().parents[4]
BASE_REV = "e5a3795191601797613eb986b36fa0b1a73fe6a1"
PKG = pathlib.Path("/home/vgpnk/Projects/shokuknow/merge/chousa")
ENTRY = "corpus/knowledge/grey-literature-field-china-r42.md"
RENUM = {"S168": "S127", "S156": "S128", "S155": "S129", "S157": "S130"}


def base_tree(dst: pathlib.Path) -> None:
    arc = subprocess.run(["git", "-C", str(LANE), "archive", BASE_REV, "corpus", "tools"], capture_output=True, check=True)
    with tarfile.open(fileobj=io.BytesIO(arc.stdout)) as t:
        t.extractall(dst, filter="data")


def staged_rows(ids: list[str]) -> list[str]:
    text = (PKG / "SOURCES.append.md").read_text(encoding="utf-8")
    out = []
    for sid in ids:
        m = re.search(r"^ {0,3}\| *" + sid + r" *\|.*$", text, re.M)
        if not m:
            sys.exit(f"staged row {sid} missing")
        out.append(m.group(0).strip())
    return out


def append_rows(root: pathlib.Path, rows: list[str]) -> None:
    p = root / "corpus" / "SOURCES.md"
    lines = p.read_text(encoding="utf-8").split("\n")
    last = max(i for i, l in enumerate(lines) if re.match(r"^\| S\d{3,} \|", l))
    lines[last + 1:last + 1] = rows
    p.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    out = pathlib.Path(sys.argv[1]).resolve()
    if out == LANE.resolve() or LANE.resolve() in out.parents:
        print("usage: OUTDIR must lie outside the lane", file=sys.stderr)
        return 2
    entry = (PKG / "knowledge" / ENTRY).read_text(encoding="utf-8")
    staged = staged_rows(["S155", "S156", "S157"])

    s = out / "staged"
    base_tree(s)
    (s / ENTRY).write_text(entry, encoding="utf-8")
    append_rows(s, staged)

    r = out / "rewrite"
    base_tree(r)
    rew = re.sub(r"^source: (S\d{3})", lambda m: "source: " + RENUM.get(m.group(1), m.group(1)), entry, flags=re.M)
    rew = re.sub(r"`(S1[56]\d)`", lambda m: "`" + RENUM.get(m.group(1), m.group(1)) + "`", rew)
    (r / ENTRY).write_text(rew, encoding="utf-8")
    rows = []
    for line in staged_rows(["S168"]) + staged:
        c = [x.strip() for x in line.split("|")[1:-1]]
        c[0] = RENUM[c[0]]
        c[7], c[8], c[9], c[10] = "mined", "2026-10-27", "180d", ENTRY
        rows.append("| " + " | ".join(c) + " |")
    append_rows(r, rows)
    print("staged rewrite")
    return 0


if __name__ == "__main__":
    sys.exit(main())
