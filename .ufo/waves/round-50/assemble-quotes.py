#!/usr/bin/env python3
"""assemble-quotes — build corpus/evidence/round50/quotes.tsv (header `id url quote entry`) from the three lane
entries: every candidate quote (the `QUOTE<TAB>staged<TAB>url<TAB>quote<TAB>entry` machine lines of the W1 reports plus
every backticked span of an entry) that occurs EXACTLY ONCE in a theme capture's `.txt` and inside the entry is kept for
that entry, with its lane id BY DOCUMENT. Duplicates are dropped; `--min` ids short of rows are reported. Run from anywhere."""
import argparse
import hashlib
import pathlib
import re

L = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin")
Q = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache")
DOC = {  # url -> lane id
    "https://chaxin.las.ac.cn/service/citation-search": "S104",
    "https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf": "S105",
    "https://rwxy.seu.edu.cn/_upload/article/58/cc/5a2fdc1940cfa2522e82ba8b5d81/fb75a598-a343-48f2-bb42-5c6c411506bc.pdf": "S106",
    "https://bs.bnu.edu.cn/docs/20160407183946745914.pdf": "S107",
}
ENTRIES = ["corpus/knowledge/cnki-citation-check-r40.md", "corpus/knowledge/citation-matching-semantics-r41.md",
           "corpus/knowledge/istic-citation-verification-r39.md"]
ap = argparse.ArgumentParser()
ap.add_argument("--out", default=str(L / "corpus/evidence/round50/quotes.tsv"))
ap.add_argument("--min", type=int, default=3)
a = ap.parse_args()
caps = {u: (Q / (hashlib.sha256(u.encode()).hexdigest()[:24] + ".txt")).read_text(encoding="utf-8", errors="replace") for u in DOC}
cands = set()
for p in sorted((L / ".ufo/waves/round-50/w1").glob("*.md")):
    for line in p.read_text(encoding="utf-8").splitlines():
        f = line.split("\t")
        if f[0] == "QUOTE" and len(f) == 5:
            cands.add(f[3])
texts = {e: (L / e).read_text(encoding="utf-8") for e in ENTRIES}
for t in texts.values():
    cands.update(re.findall(r"`([^`\n]{4,})`", t))
rows, seen = [], set()
for q in sorted(cands):
    if len(q.split()) > 25 or len(q) > 160 or "\n" in q:
        continue
    homes = [u for u, t in caps.items() if t.count(q) == 1]
    if len(homes) != 1 or any(t.count(q) > 1 for t in caps.values()):
        continue
    u = homes[0]
    for e in ENTRIES:
        if q in texts[e] and (DOC[u], q, e) not in seen:
            seen.add((DOC[u], q, e))
            rows.append((DOC[u], u, q, e))
rows.sort(key=lambda r: (r[0], r[3], caps[r[1]].find(r[2])))
pathlib.Path(a.out).write_text("id\turl\tquote\tentry\n" + "".join("\t".join(r) + "\n" for r in rows), encoding="utf-8")
per = {}
for r in rows:
    per[r[0]] = per.get(r[0], 0) + 1
print("ROWS", len(rows), dict(sorted(per.items())))
for i in DOC.values():
    if per.get(i, 0) < a.min:
        print("SHORT", i, per.get(i, 0))
