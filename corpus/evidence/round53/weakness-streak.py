#!/usr/bin/env python3
"""weakness-streak — consecutive rounds a recurring weakness is named in the lane's own round record
(considerthese 2026-10-26, proposal 2). Reads corpus/evidence/round53/recurring.tsv:
id<TAB>label<TAB>regex<TAB>routed-path-or-dash<TAB>claimed-streak ; counts a round when the regex
(case-insensitive) matches corpus/lessons/round-N.md or round-N-verifier-spotcheck.md; the streak runs
back from the newest round file. Exit 1: a row's claimed streak differs from the computed one, or a row
with streak>=3 names no existing routed path."""
import argparse, pathlib, re, sys
ap = argparse.ArgumentParser(); ap.add_argument("--root", default="."); ap.add_argument("--table", required=True)
a = ap.parse_args(); root = pathlib.Path(a.root); les = root / "corpus/lessons"
rounds = sorted(int(m.group(1)) for p in les.glob("round-*.md") if (m := re.fullmatch(r"round-(\d+)\.md", p.name)))
if not rounds: print("NO_ROUNDS"); sys.exit(2)
def text(n):
    return "\n".join(p.read_text(encoding="utf-8") for p in (les / f"round-{n}.md", les / f"round-{n}-verifier-spotcheck.md") if p.exists())
txt = {n: text(n) for n in rounds}; bad = 0; rows = 0
for line in pathlib.Path(a.table).read_text(encoding="utf-8").splitlines():
    if not line.strip() or line.startswith("#"): continue
    rid, label, rx, routed, claimed = line.split("\t"); rows += 1
    hits = [n for n in rounds if re.search(rx, txt[n], re.I)]
    s = 0
    for n in reversed(rounds):
        if n in hits: s += 1
        else: break
    ok = (s == int(claimed)) and (s < 3 or (routed != "-" and (root / routed).exists()))
    bad += not ok
    print(f"{'OK  ' if ok else 'FAIL'} {rid} streak={s} claimed={claimed} first_in_run={rounds[-s] if s else '-'} routed={routed} {label}")
print(f"WEAKNESS_ROWS={rows} FAILING={bad}"); sys.exit(1 if bad else 0)
