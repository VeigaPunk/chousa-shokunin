#!/usr/bin/env python3
"""assemble-quotes — collect the `QUOTE<TAB>staged-id<TAB>url<TAB>quote<TAB>entry` lines of the Ground* seat
reports into corpus/evidence/round50/quotes.tsv (header `id url quote entry`), mapping staged ids to lane ids BY DOCUMENT,
dropping duplicates, and listing every line that could not be used. Usage: assemble-quotes.py [--per-id N]"""
import argparse
import hashlib
import pathlib
import re

L = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin")
Q = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache")
LANE_ID = {  # staged URL -> lane id (by document)
    "https://chaxin.las.ac.cn/service/citation-search": "S104",
    "https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf": "S105",
    "https://rwxy.seu.edu.cn/_upload/article/58/cc/5a2fdc1940cfa2522e82ba8b5d81/fb75a598-a343-48f2-bb42-5c6c411506bc.pdf": "S106",
    "https://bs.bnu.edu.cn/docs/20160407183946745914.pdf": "S107",
}
ap = argparse.ArgumentParser()
ap.add_argument("--reports", default=str(L / ".ufo/waves/round-50/w1"))
ap.add_argument("--out", default=str(L / "corpus/evidence/round50/quotes.tsv"))
a = ap.parse_args()
seen, rows, bad = set(), [], []
for p in sorted(pathlib.Path(a.reports).glob("Ground*.md")):
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.startswith("QUOTE\t"):
            continue
        f = line.split("\t")
        if len(f) != 5:
            bad.append((p.name, "fields", line[:80]))
            continue
        _, _sid, url, quote, entry = (c.strip() if i != 3 else c for i, c in enumerate(f))
        lid = LANE_ID.get(url)
        if not lid:
            bad.append((p.name, "url", url))
            continue
        txt = (Q / (hashlib.sha256(url.encode()).hexdigest()[:24] + ".txt")).read_text(encoding="utf-8", errors="replace")
        n = txt.count(quote)
        if n != 1 or len(quote.split()) > 25 or len(quote) > 160:
            bad.append((p.name, f"count={n} words={len(quote.split())} chars={len(quote)}", quote[:60]))
            continue
        if (lid, quote, entry) in seen:
            continue
        seen.add((lid, quote, entry))
        rows.append((lid, url, quote, entry))
rows.sort(key=lambda r: (r[0], r[3]))
pathlib.Path(a.out).write_text("id\turl\tquote\tentry\n" + "".join("\t".join(r) + "\n" for r in rows), encoding="utf-8")
per = {}
for r in rows:
    per[r[0]] = per.get(r[0], 0) + 1
print("ROWS", len(rows), per)
for b in bad:
    print("UNUSED", *b)
