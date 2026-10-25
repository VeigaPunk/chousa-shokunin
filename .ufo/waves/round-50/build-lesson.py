#!/usr/bin/env python3
"""Write corpus/lessons/round-50.md: the prose below plus the generated located-quote table (one row per quotes.tsv row)."""
import csv
import hashlib
import pathlib

L = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin")
Q = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache")
rows = list(csv.reader((L / "corpus/evidence/round50/quotes.tsv").read_text(encoding="utf-8").splitlines()[1:], delimiter="\t"))
caps = {}
for _id, url, _q, _e in rows:
    caps.setdefault(url, (Q / (hashlib.sha256(url.encode()).hexdigest()[:24] + ".txt")).read_text(encoding="utf-8", errors="replace"))
table = ["| lane id | form | char offset | located quote (≤25 words, exactly once in that form) | cited by |", "|---|---|---:|---|---|"]
for sid, url, q, e in rows:
    table.append(f"| {sid} | `.txt` UTF-8 | {caps[url].find(q)} | {q} | `{e}` |")
head = (L / ".ufo/waves/round-50/lesson-head.md").read_text(encoding="utf-8")
(L / "corpus/lessons/round-50.md").write_text(head.replace("@@QUOTES@@", "\n".join(table)), encoding="utf-8")
print("rows", len(rows))
