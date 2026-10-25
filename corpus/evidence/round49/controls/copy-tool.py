#!/usr/bin/env python3
"""copy-tool — round-49 C1 do-nothing control: the cheapest adopter that skips
the claimed work. Same interface as tools/assimilate-rows.py; it appends the
cited staged rows byte-exact (no renumbering, no normalisation), copies the
entries unchanged, writes an identity renumber map, and builds `collisions`
with a column-zero-only pattern (the false-green the section-10 guard names).
"""
import argparse
import pathlib
import re
import shutil

ap = argparse.ArgumentParser()
ap.add_argument("--staged", required=True)
ap.add_argument("--knowledge", required=True)
ap.add_argument("--registry", required=True)
ap.add_argument("--opened", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--entry", action="append", default=[])
a = ap.parse_args()
out = pathlib.Path(a.out)
out.mkdir(parents=True, exist_ok=True)
col0 = re.compile(r"^\|\s*(S\d{3,})")
reg = sorted({m.group(1) for l in open(a.registry, encoding="utf-8") if (m := col0.match(l))})
st_lines = open(a.staged, encoding="utf-8").read().splitlines()
st = {m.group(1): l for l in st_lines if (m := col0.match(l))}
(out / "reg-ids").write_text("".join(i + "\n" for i in reg))
(out / "staged-ids").write_text("".join(i + "\n" for i in sorted(st)))
(out / "collisions").write_text("".join(i + "\n" for i in sorted(set(reg) & set(st))))
if a.entry:
    cited = set()
    for e in a.entry:
        src = pathlib.Path(a.knowledge) / e
        (out / e).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, out / e)
        cited |= {t for t in re.findall(r"\bS\d{3,}\b", src.read_text(encoding="utf-8")) if t in st}
    order = sorted(cited, key=lambda s: int(s[1:]))
    (out / "append.md").write_text("".join(st[s] + "\n" for s in order))
    (out / "renumber.tsv").write_text("staged_id\tlane_id\taction\turl\n" +
                                      "".join(f"{s}\t{s}\tappend\t-\n" for s in order))
    (out / "stripped.tsv").write_text("lane_id\tcolumn\tstripped\n")
