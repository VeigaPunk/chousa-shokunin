# R53ScoutConsiderthese — considerthese assimilation (lane tip `6365f15`, read-only)

Read: all eight `considerthese/2026-10-26.md … 2026-10-19.md` (newest first; `git status --short considerthese` empty, newest file = commit `9b99ede`, the same 46-line file round 52 swept). Lane record: `grep -rn considerthese corpus/lessons corpus/QUALITY.md LOG.md` → QUALITY 60/61/62/64/68/71, lessons r24 r44 r47 r48 r49 r50 r51 r52 (`round-52.md:84-86`), LOG 1526…1830. Prior sweep: `.ufo/waves/round-52/w1/R52ScoutConsiderthese.md` (38 rows). No file edited; nothing outside scratch written.

## Newest file (2026-10-26) — every proposal and waiting item, re-checked at tip `6365f15`

| # | Item (file:line) | Status | Evidence run now |
|---|---|---|---|
| P1 | stable ids `CT-YYYYMMDD-n` (`:41`) | reflection-format only | names no lane artefact; `grep -rn 'CT-2026' . --include=*.md` outside considerthese: none expected, not run — it is the daily file's own format |
| P2 | recurring weaknesses as streak table (`:42`) | **STILL OPEN** | `grep -n -i -E 'streak|recurring weakness' corpus/QUALITY.md SCORECARD.md SKILL.md` → only SCORECARD verdict prose / round-52 lesson line 25; no table, no script |
| P3 | lane-vs-verifier disagreement (`:43`) | IMPLEMENTED | `corpus/evidence/round52/verdict-gap.py` (exists), `SKILL.md:135` Gates row, `SCORECARD.md:2678`; run: `python3 corpus/evidence/round52/verdict-gap.py --from 46 --to 52` → `R47 operability: lane=improved verifier=harmed`, `R48 UNPARSED lane_axes=6 verifier_axes=0`, `R50 calibration: lane=improved verifier=unchanged`, `VERDICT_GAPS=2 UNPARSED=1` |
| P4 | one independent CJK quote spot-check per review (`:44`) | reflection-format only | a reader outside the lane; lane analogue `corpus/evidence/round51/quote-substance-check.py` exists |
| W1 | L0 `8d77e6c1` age (`:7`) | lane side IMPLEMENTED, item operator-owned | `corpus/evidence/round51/open-items-age.py` exists; L0 still open (task brief: "L0 `8d77e6c1` is open") |
| W2 | round-47 polarity trade moot? (`:8`) | operator-owned, no ruling | `SCORECARD.md:2513` still `improved, disputed as a trade`; `grep -rn -i 'polarity trade|moot' corpus/lessons/round-5[0-2]*.md corpus/QUALITY.md` → no output |
| W3 | uncommitted inherited swarm-registry / QUALITY edit (`:9`) | STALE at tip | `git status --short` shows only `?? .ufo/waves/round-53/{assimilation/,w1.ready,w1.ready.dispatched,w1/}` |

Older seven files: unchanged from round 52's ledger (31 rows, 19 implemented / 10 reflection-format / 2 open by its status column); open there: 10-19 "watch SKILL.md size" (`wc -l SKILL.md` = 738, no threshold in QUALITY; not picked), 10-22 cost/wall-time (out of province, `PROVINCE.md` → kumitate).

## The one pick: P2, recurring weaknesses as streaks (still open)

Why: the forgeable-frozen-counter class is the lane's longest-running defect and this round's C1 is its direct test (nonce packages + representation variance). A streak makes "did round 53 break it?" a number rather than prose. It fits calibration/adopter province (verdict honesty; the adopter C1 is the routed fix) and reuses the mined data (`corpus/lessons/round-N.md` + `round-N-verifier-spotcheck.md`). Computed now: the `forg…` class is named in rounds 49,50,51,52 (4 consecutive; round 48 has 0 hits; per-round lesson/verifier hit counts r49 2/1, r50 2/3, r51 2/3, r52 4/6). Routed fix exists (`corpus/evidence/round52/c1-count.py`, `lessons/round-52.md:25`); round 53's C1 is the next fix.

Intended paths: `corpus/evidence/round53/weakness-streak.py` and `corpus/evidence/round53/recurring.tsv` (L1 integrates; neither exists today: `ls corpus/evidence/round53/` = `build-spans.py c1-count.py c2-count.py census-start.txt claims.md controls`).

`recurring.tsv` (fields TAB-separated; claimed streak is what the table asserts, and the L1 must set RW-1 to the computed value after the round-53 lesson exists):
```
RW-1<TAB>frozen counter forgeable<TAB>forg(e|ed|able|ery)<TAB>corpus/evidence/round52/c1-count.py<TAB>4
RW-3<TAB>stray write outside scratch<TAB>relative redirect|fleet root|misroot|fleet-root<TAB>-<TAB>1
```

`weakness-streak.py`:
```python
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
```

Observed in scratch (tip `6365f15`, rounds 45-52 files):
```
OK   RW-1 streak=4 claimed=4 first_in_run=49 routed=corpus/evidence/round52/c1-count.py frozen counter forgeable
OK   RW-3 streak=1 claimed=1 first_in_run=52 routed=- stray write outside scratch
(3-row scratch table incl. a "binding not entailment" row: WEAKNESS_ROWS=3 FAILING=0, rc=0; that row had streak=0 → dropped as too noisy)
mutant claimed 4→3:           FAILING=1  rc=1
mutant routed path → missing: FAILING=1  rc=1
```
Check that shows it implemented:
```
python3 corpus/evidence/round53/weakness-streak.py --root . --table corpus/evidence/round53/recurring.tsv
# implemented = both files exist, a QUALITY row/SCORECARD line cites the output, and the run prints
#   OK RW-1 streak=<4 or 5> … / WEAKNESS_ROWS=2 FAILING=0 rc=0; a wrong claimed streak or a streak>=3 row without an existing routed path exits 1.
```
Named limits: a regex hit means the class is *named* in the round record, not that the defect recurred (a round that praises a fix mentions "forge" too); round 48 reads 0 so the streak is 4, not 5, which matches the considerthese count only from r49. Not a grade change; no operator item closed. At round-53 close the L1 should re-run: if the round-53 lesson names forgery (likely, disclosing C1 forges tested) the streak reads 5 even when C1 passes — the streak is exposure, not failure; pair it with the C1 verdict.

Tooling: none installed or upgraded. Scratch `/fast/scratch/hyaku/chousa-r53/R53ScoutConsiderthese/` removed at the end.

VERDICT: swept all eight considerthese files; newest file's 4 proposals + 3 waiting items = 1 implemented (verdict-gap, run), 2 reflection-format, 1 lane-implemented/operator-owned, 1 operator-owned, 1 stale, 1 still open; picked the open streak-table proposal (4-round forge streak computed r49-r52) with a drafted script, table and a check that fails under two mutants. Nothing in C1/C2 attacked by this seat.
