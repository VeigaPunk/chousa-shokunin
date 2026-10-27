#!/usr/bin/env python3
"""considerthese-ledger-check — stable ids CT-YYYYMMDD-n for every bullet under a
"## Self-improvement proposals" heading of considerthese/*.md (n = 1-based bullet order),
each carrying one row in the lane ledger. Fails when a proposal has no row, a row has no
proposal, a status is unknown, or an IMPL row's pointer file is absent / its ::regex does
not match. Prints the tally from the ledger rows, so uptake is cited by id, not recounted.
Usage: considerthese-ledger-check.py [--root LANE] [--ledger TSV]
Ledger TSV: id<TAB>status<TAB>pointer<TAB>note ; status IMPL|FMT|OPEN|OPS ;
pointer = path[::regex] (re.M) for IMPL, '-' otherwise. Exit 0 all hold, 1 otherwise, 2 usage."""
import argparse, collections, pathlib, re, sys
ap = argparse.ArgumentParser(); ap.add_argument("--root", default="."); ap.add_argument("--ledger")
a = ap.parse_args(); root = pathlib.Path(a.root)
led = pathlib.Path(a.ledger) if a.ledger else root / "corpus/evidence/round54/considerthese-ledger.tsv"
try: rows = [l.split("\t") for l in led.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
except OSError as e: print(f"USAGE {e}"); sys.exit(2)
want = []
for f in sorted((root / "considerthese").glob("2026-*.md")):
    n, on = 0, False
    for line in f.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "): on = line.startswith("## Self-improvement proposals")
        elif on and line.startswith("- "): n += 1; want.append(f"CT-{f.stem.replace('-', '')}-{n}")
have = collections.Counter(r[0] for r in rows); bad = []
bad += [f"MISSING {i}" for i in want if i not in have]
bad += [f"ORPHAN {i}" for i in have if i not in want] + [f"DUP {i}" for i, c in have.items() if c > 1]
tally = collections.Counter()
for r in rows:
    if len(r) != 4: bad.append(f"COLUMNS {r[0]}"); continue
    i, st, ptr, _ = r; tally[st] += 1
    if st not in ("IMPL", "FMT", "OPEN", "OPS"): bad.append(f"STATUS {i} {st}"); continue
    if st != "IMPL": continue
    p, _, rx = ptr.partition("::"); f = root / p
    if not f.is_file(): bad.append(f"POINTER {i} {p}")
    elif rx and not re.search(rx, f.read_text(encoding="utf-8", errors="replace"), re.M): bad.append(f"REGEX {i} {p}::{rx}")
for b in bad: print("FAIL", b)
print(f"PROPOSALS={len(want)} ROWS={len(rows)} " + " ".join(f"{k}={tally[k]}" for k in ("IMPL", "FMT", "OPEN", "OPS")) + f" BAD={len(bad)}")
sys.exit(1 if bad else 0)
