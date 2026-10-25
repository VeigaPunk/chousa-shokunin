#!/usr/bin/env python3
"""Write corpus/lessons/round-51.md from lesson-head.md: seat tables, verdict lines, the generated located-quote table, the census tail."""
import csv, hashlib, pathlib, re, subprocess

L = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin")
Q = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache")
W = L / ".ufo/waves/round-51"
rows = list(csv.reader((L / "corpus/evidence/round51/quotes.tsv").read_text(encoding="utf-8").splitlines()[1:], delimiter="\t"))
caps = {}
for _id, url, _q, _e in rows:
    caps.setdefault(url, (Q / (hashlib.sha256(url.encode()).hexdigest()[:24] + ".txt")).read_text(encoding="utf-8", errors="replace"))
table = ["| lane id | form | char offset | located quote (≤25 words, exactly once in that form) | cited by |", "|---|---|---:|---|---|"]
for sid, url, q, e in rows:
    table.append(f"| {sid} | `.txt` UTF-8 | {caps[url].find(q)} | {q} | `{e}` |")
head = (W / "lesson-head.md").read_text(encoding="utf-8")
mist = (W / "mistakes-rows.md").read_text(encoding="utf-8").rstrip("\n")
gate = (W / "gate-table.md").read_text(encoding="utf-8").split("\n")
dec = gate[:2] + [r for r in gate[2:] if r.startswith("|") and not any(k in r.split("|")[1] for k in ("japanese-search-record-r38", "chinese-search-record-r39"))]
qm = (W / "w1/R51ExecQuarantine.md").read_text(encoding="utf-8")
verd = re.search(r"## 4\. Machine lines.*?```\n(.*?)\n```", qm, re.S).group(1)
tail = (W / "lesson-tail.md").read_text(encoding="utf-8") if (W / "lesson-tail.md").exists() else ""
cen = subprocess.run(["/home/vgpnk/Projects/shokunin/scripts/sources-census.sh", "validate", "--root", "/home/vgpnk/Projects/shokunin", "chousa"], capture_output=True, text=True)
warns = sorted({m for m in re.findall(r"\bW04\t(S\d+)", cen.stdout.replace(" ", "\t", 0))} | set(re.findall(r"W04\s+(S\d+)", cen.stdout)))
reg = (L / "corpus/SOURCES.md").read_text(encoding="utf-8")
nrows = len(re.findall(r"^[ ]{0,3}\|[ \t]*S\d{3,}[ \t]*\|", reg, re.M))
tiers = {}
for l in reg.splitlines():
    if re.match(r"^\|[ \t]*S\d{3,}[ \t]*\|", l):
        f = [c.strip() for c in l.split("|")]
        if len(f) == 13:
            tiers[f[4]] = tiers.get(f[4], 0) + 1
tail = tail.replace("@@CENSUS_END@@", f"exit {cen.returncode}, `ok`, W04 warnings {', '.join(warns)} (the same five); tiers {dict(sorted(tiers.items()))}.").replace("@@ROWS@@", f"106 → {nrows}")
out = head.replace("@@MISTAKES@@", mist).replace("@@DECISIONS@@", "\n".join(dec)).replace("@@VERDICTS@@", verd).replace("@@QUOTES@@", "\n".join(table)).replace("@@TAIL@@", tail)
(L / "corpus/lessons/round-51.md").write_text(out, encoding="utf-8")
print("rows", len(rows), "decisions", len(dec) - 2)
