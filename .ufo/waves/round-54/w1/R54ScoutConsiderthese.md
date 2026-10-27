# R54ScoutConsiderthese — considerthese assimilation (lane HEAD `9caf8fc`, read-only)

Read: all eight `considerthese/2026-10-26.md … 2026-10-19.md` (newest first; `git status --short considerthese` empty; newest file = commit `9b99ede`, unchanged since rounds 52/53). Lane record: `grep -rn considerthese corpus/lessons corpus/QUALITY.md LOG.md` → QUALITY 60/61/62/64/68/71, lessons r24 r44 r47 r48 r49 r50 r51 r52 r53 (`round-53.md:76-78`), LOG 1526…1850; prior sweeps `.ufo/waves/round-5{1,2,3}/w1/R5*ScoutConsiderthese.md` (31 → 38 rows). Nothing in C1/C2 attacked by this seat. No tool installed.

## Newest file (2026-10-26) "Self-improvement proposals (not acted on)", lines 41-44, re-checked at HEAD

| id (proposed) | proposal | status | evidence run now |
|---|---|---|---|
| CT-20261026-1 | stable proposal ids | **still open** (R52/R53 sweeps filed it FMT; it is lane-actionable, see pick) | `grep -rnE 'CT-[0-9]{8}' . --exclude-dir=.git` → only `considerthese/2026-10-26.md:41` and the round-54 spec files `.ufo/waves/round-54/{gen-w1-spec.py:162,w1-spec.json,w1-dispatch.json,…}` (the brief itself); no lane ledger, no check |
| CT-20261026-2 | recurring weaknesses as streaks | IMPLEMENTED r53 | `corpus/evidence/round53/weakness-streak.py` + `recurring.tsv`; `SKILL.md:138`; run now: `OK RW-1 streak=5 claimed=5 first_in_run=49 …`, `OK RW-3 streak=2 …`, `WEAKNESS_ROWS=2 FAILING=0` rc 0 |
| CT-20261026-3 | lane-vs-verifier disagreements | IMPLEMENTED r52 | `corpus/evidence/round52/verdict-gap.py --from 46 --to 53` → `R50 calibration: lane=improved verifier=unchanged`, `VERDICT_GAPS=2 UNPARSED=1`, rc 1 |
| CT-20261026-4 | one independent CJK quote spot-check per review | reflection-format only; **not implemented anywhere** | a reader outside the lane cannot be a lane artefact. Sweep: `grep -c '[一-龥]' considerthese/*.md` → 10-19…10-25 all 0, 10-26 = 2 (`:19,:20`, theme names `引文核对`, `検索式 / 检索策略`, not a spot-check). Lane-side non-author CJK re-reads exist, dispatched by the lane: `corpus/lessons/round-51-verifier-spotcheck.md:81-86` (S109 char 15310, S107 char 10234, `agree`), plus `corpus/evidence/round51/quote-substance-check.py` (substance floor only). No considerthese file carries a CJK agree/disagree. |

"Waiting on you" (lines 7-9; not proposals): L0 `8d77e6c1` operator-owned, lane age line implemented (`open-items-age.py`); round-47 polarity trade: operator ruling, none recorded; uncommitted inherited swarm-registry/QUALITY edit: stale at HEAD (`git status --short` shows only `?? .ufo/waves/round-54/…` and `?? corpus/evidence/round54/c1-after-candidate.txt`, no `M` lines).

## Tally across all eight files (35 proposal bullets; script-counted, see below)

24 IMPLEMENTED (incl. CT-20261026-1 once the pick lands) · 9 reflection-format · 1 open (CT-20261019-4: `SKILL.md` size, `wc -l SKILL.md` = 741, no threshold agreed) · 1 operator/out-of-province (CT-20261022-2 cost per gain: `PROVINCE.md` sends orchestration to kumitate). This reconciles the round-51 scout's own split (19/10/2) after the later landings: round 51 `open-items-age.py` flipped two rows (CT-20261022-1, CT-20261025-2) from open/FMT to implemented; round 52 verdict-gap and round 53 weakness-streak flipped two more; the ledger's 24 = 19 + 2 + 2 + 1 (CT-20261026-1 itself). The prior counts disagreed because rows had no id: that is exactly the bullet-1 complaint.

## The one pick: CT-20261026-1, stable ids, implemented lane-side as a ledger plus a check

Why this one and not CT-20261026-4: 4 needs a reader the lane did not dispatch, so the lane can only mimic it (already done by every non-author verifier); 1 is fully lane-actionable, it is cheap, and it removes a defect that has recurred in three consecutive sweeps (tallies 19/9/3 in R51, "38 rows … 2 open lane" in R52, re-counted again in R53). Fits the round: wave-2 and the closure must cite which proposals this round implements; with ids, that citation is a lookup and the checker fails the day a new considerthese proposal has no row. It does not edit `considerthese/` (operator input): the lane assigns `CT-YYYYMMDD-n` (n = bullet order under `## Self-improvement proposals`) retroactively, which matches the bot's own example `CT-20261026-1`.

Intended lane paths (L1 integrates; neither exists today: `ls corpus/evidence/round54/` has no `considerthese-*`): `corpus/evidence/round54/considerthese-ledger-check.py` and `corpus/evidence/round54/considerthese-ledger.tsv` (script sha256 `1f9f01f7…`, ledger `43113504…`).

Check command that shows it implemented:
```
python3 corpus/evidence/round54/considerthese-ledger-check.py --root .
# implemented = both files exist and the run prints  PROPOSALS=35 ROWS=35 IMPL=24 FMT=9 OPEN=1 OPS=1 BAD=0  rc 0
# (PROPOSALS grows by one per new bullet; a new considerthese file without ledger rows prints FAIL MISSING CT-… and exits 1)
```
Observed in scratch (`/fast/scratch/hyaku/chousa-r54/R54ScoutConsiderthese`, lane tree rsynced into an overlay with both files placed at the intended paths; `considerthese/` byte-identical):
```
lane tree, files not yet integrated: FAIL POINTER CT-20261026-1 corpus/evidence/round54/considerthese-ledger-check.py | PROPOSALS=35 ROWS=35 IMPL=24 FMT=9 OPEN=1 OPS=1 BAD=1 | rc=1
overlay (as integrated):             PROPOSALS=35 ROWS=35 IMPL=24 FMT=9 OPEN=1 OPS=1 BAD=0 | rc=0
mutant drop row CT-20261024-3:       FAIL MISSING CT-20261024-3 | ROWS=34 BAD=1 | rc=1
mutant IMPL pointer → nope.py:       FAIL POINTER CT-20261026-3 corpus/evidence/round52/nope.py | rc=1
mutant stale QUALITY regex ^600\.:   FAIL REGEX CT-20261023-1 … | rc=1
new 2026-10-27.md with 1 bullet:     FAIL MISSING CT-20261027-1 | PROPOSALS=36 ROWS=35 | rc=1
missing ledger:                      USAGE … No such file … | rc=2
```
Named limits: the IMPL pointer proves a lane artefact exists and (with `::regex`) that a QUALITY criterion heading is present, not that it entails the proposal; the one self-referential row (CT-20261026-1 → the checker) passes only after integration; statuses of the 31 older rows are copied from R51's table with pointers re-verified by `ls` (all exist) and QUALITY headings re-grepped (`^8.`, `^9.`, `^18.`, `^23.`, `^44.`, `^60.`, `^61.`, `^68.` found at QUALITY.md:28,33,104,152,336,526,542,664); CT-20261024-4 is local-leg only (cloud-agent leg refused, `round-48.md:73`). Not a grade change; closes no operator item.

### `corpus/evidence/round54/considerthese-ledger-check.py`
```python
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
```

### `corpus/evidence/round54/considerthese-ledger.tsv` (TAB-separated; first line is a comment)
```
# id	status	pointer	note
CT-20261019-1	IMPL	corpus/evidence/round40/c1-count.py	selftest/drift re-run: QUALITY 15, 42, 68
CT-20261019-2	IMPL	corpus/evidence/round25-ledger-recount.py	round-25 debt queue recount
CT-20261019-3	IMPL	SCORECARD.md::^## Capabilities	saturation line / Capabilities rows
CT-20261019-4	OPEN	-	SKILL.md size; wc -l = 741; no threshold agreed
CT-20261020-1	FMT	-	the bot's own QUALITY 9/10 hygiene
CT-20261020-2	FMT	-	cursor: lines done by the author
CT-20261020-3	IMPL	tools/quote-reopen.py	second verifier for registry rows; QUALITY 25
CT-20261020-4	IMPL	corpus/evidence/round25-ledger-recount.py	round-25 debt queue
CT-20261020-5	IMPL	corpus/knowledge/recheck-due-r26.md	recheck calendar, SKILL.md --as-of
CT-20261020-6	FMT	-	permission question to the operator
CT-20261021-1	IMPL	corpus/evidence/round26-claims.md	pre-registration scored in round 27
CT-20261021-2	IMPL	corpus/lessons/round-27-verifier-spotcheck.md	verifier ran the digest comparison; dropped by 10-22
CT-20261021-3	IMPL	corpus/QUALITY.md::^9\. \*\*One home	same-file restatements
CT-20261021-4	IMPL	corpus/QUALITY.md::^8\. \*\*Support states	support states
CT-20261021-5	IMPL	corpus/QUALITY.md::^18\. \*\*A bound names its unit	resource bounds
CT-20261022-1	IMPL	corpus/evidence/round51/open-items-age.py	waiting-on line, lane side (round 51)
CT-20261022-2	OPS	-	seats / wall time / cost: kumitate's (PROVINCE.md refuses orchestration)
CT-20261022-3	IMPL	corpus/QUALITY.md::^23\. \*\*Lane prose keeps digits	prose regex scan
CT-20261022-4	FMT	-	read the verifier first; QUALITY 14 intake already requires it
CT-20261023-1	IMPL	corpus/QUALITY.md::^60\. \*\*Every frozen counter names the cheapest	cheapest gate per counter
CT-20261023-2	FMT	-	not a lane artefact (300-file page)
CT-20261023-3	IMPL	corpus/QUALITY.md::^44\. \*\*A held control is never re-authored	stricter than proposed
CT-20261023-4	FMT	-	cursor: line done by the author
CT-20261024-1	IMPL	corpus/evidence/round45/tag-count.py	plumbing/ground tag, QUALITY 64
CT-20261024-2	IMPL	corpus/QUALITY.md::^61\. \*\*A validated wave spec	undispatched waves
CT-20261024-3	IMPL	corpus/evidence/round44/errata-count.py	errata per round, QUALITY 62
CT-20261024-4	IMPL	corpus/QUALITY.md::^68\. \*\*A committed receipt is re-verified	local leg only; cloud-agent leg refused (round-48.md:73, L0 8d77e6c1)
CT-20261025-1	FMT	-	retires two earlier ideas
CT-20261025-2	IMPL	corpus/evidence/round51/open-items-age.py	open-items age, round 51
CT-20261025-3	IMPL	corpus/evidence/round49/capture-age-check.py	capture-age line, QUALITY 71
CT-20261025-4	FMT	-	reviewer pacing
CT-20261026-1	IMPL	corpus/evidence/round54/considerthese-ledger-check.py	this ledger and checker
CT-20261026-2	IMPL	corpus/evidence/round53/weakness-streak.py	recurring.tsv, round 53
CT-20261026-3	IMPL	corpus/evidence/round52/verdict-gap.py	round 52
CT-20261026-4	FMT	-	independent reader outside the lane; lane analogue quote-substance-check.py
```

VERDICT: swept all eight considerthese files (35 proposals: 24 implemented, 9 reflection-format, 1 open, 1 out of province); CT-20261026-1 (ids) and -4 (CJK spot-check) implemented nowhere before this report; picked CT-20261026-1, drafted ledger + checker that print BAD=0 rc 0 as integrated and fail under four mutants.
