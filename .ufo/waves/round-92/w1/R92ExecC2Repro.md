# R92ExecC2Repro — frozen C2 reproduction from clean C5 tree

Seat: R92ExecC2Repro. Scratch: `/fast/scratch/hyaku/chousa-r92/R92ExecC2Repro`
(clone `--shared`, checkout `16ccf7693c61b8ffe392fc757352304f239bfcad` =
C5 carrier; `rev-parse HEAD` verified equal). Receipts in
`.ufo/waves/round-92/w1/c2-after.txt`, `c2-controls-rerun.txt`,
`receipts-c2/`. No network. No production edits. Scratch removed
before yield.

Tooling: no installs; stock `python3`/`git` only. Nothing installed.

## (a) curation-r92 counter

Command (from `$S/repo`):
`python3 -B corpus/evidence/round92/curation-r92.py --root .`
Exit: `0`. Receipt: `c2-after.txt`.

Observed stdout (verbatim):
```
SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20 Q_ROWS=20 Q_SHAPE_FAIL=0 SOURCE_STATUS_OK=20/20 USED_BY_OK=20/20 Q_FLOORS=search-transparency-reporting-r84.md=13/13 floor13,provenance-recording-r85.md=7/7 floor7 WARRANT_OK=17/17 TFREQ_OK=17/17 TFREQ_MAX_DF=3 DUP_QIDS=0 TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 SUP_CLAUSE_CHECKED=0 SUP_UNRESOLVED=0 LEGS_MEASURED=14/14
TEACHES_FLAGGED S024 terms=publication,modification disposition=superseded by S031
VERDICT fields_hold=1 legs_ok=14/14 DETECTOR_WITNESS=11/11
CURATION_R92=PASS
```

All frozen C2 counter tokens are present with exact expected values:
`CURATION_R92=PASS` (exit 0), `LEGS_MEASURED=14/14`, `Q_ROWS=20`,
`Q_SHAPE_FAIL=0`, `SOURCE_STATUS_OK=20/20`, `USED_BY_OK=20/20`,
`TFREQ_OK=17/17`, `TFREQ_MAX_DF=3`, `UNENTAILED_TERM=0`,
`WARRANT_OK=17/17`, `DUP_QIDS=0`. Extra tokens beyond the frozen set
(`QUOTES_LOCATED`, `Q_FLOORS`, `TEACHES_*`, `DETECTOR_WITNESS`) are
superset, not deviation.

## (b) curation controls battery

Frozen command names `curation-r92-controls.py`; that file does not
exist at C5 (`ls` shows `curation-controls-r92.py` only, and
`instrument-pins.txt` row 4 pins `curation-controls-r92.py`). The
battery was therefore run as
`python3 -B corpus/evidence/round92/curation-controls-r92.py --root . --work $S/ctl`
Exit: `0`. Receipt: `c2-controls-rerun.txt`.

Observed summary line (verbatim):
```
CONTROLS=PASS FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 CARRIED_F1_F4=refused-by-both DUPCOUNT_R91=1 DUPCOUNT_R92=1 PRIOR_REGRESSION=4/4
```
plus per-class lines: positive OK (r91 PASS / r92 PASS); s1–s4 all
`OK` with r92 refusing the named leg (`QSHAPE`/`WARRANT`/`SOURCE`/
`USED_BY`) and r91 `PASS`; duplicate-count OK (`UNENTAILED_TERM=1`
both); regression line `OK regression: FORGERY_REFUSED=7/7
PRIOR_REGRESSION=7/7 rc=1`.

FINDING 1 (controls filename): `claims.md:66` and `claims.json:57,86`
name `curation-r92-controls.py`, absent at C5; the on-disk battery is
`curation-controls-r92.py` (pinned). K1-class naming deviation; the
pinned file is the one that runs and passes.

FINDING 2 (PRIOR_REGRESSION token): claims expect `PRIOR_REGRESSION=7/7`
in the summary, the battery prints `PRIOR_REGRESSION=4/4` (line 200
hard-codes `'4/4' if reg_ok`), while the regression detail line
separately attests `FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7 rc=1`.
All other expected tokens match exactly
(`CONTROLS=PASS FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4
DUPCOUNT_R91=1 DUPCOUNT_R92=1`). The r90-battery replay itself refused
7/7; only the summary token's denominator is 4. Minor claim/battery
wording deviation, substance intact.

## (c) Independent decision-count pin

Probe (read-only, inline Python, independent of the counter): parse
each routed entry's `## Decision table` to the next `## `, count
pipe-leading rows, split cells. Results (verbatim tables in working
notes; summarized):

- `corpus/knowledge/search-transparency-reporting-r84.md`: 13
  pipe-leading rows = 1 header + 1 separator + 11 data, all width 4.
- `corpus/knowledge/provenance-recording-r85.md`: 8 pipe-leading
  rows = 1 header + 1 separator + 6 data, all width 4.

Total 17 = 11 + 6, matching the pinned count and
`WARRANT_OK=17/17` from run (a). HELD.

## (d) Independent minus-self digest + two-directional used-by

Minus-self probe (read-only re-implementation mirroring
`pins_file_sha_minus_self` at control-driver lines 179–191: skip
blank/`#` lines, skip the self row `corpus/evidence/round92/instrument-pins.txt`,
sha256 over remaining lines): computed
`5f288597d4bad803cbd3ba511d06e362c99911c30782742f378a872977f03275`
= stored self row. MATCH=True. 16 non-comment rows total. HELD.

Two-directional used-by (independent grep-style parse of
`corpus/SOURCES.md`, columns id=0/status=7/used-by=10, 219 S-rows):
mined rows naming entries: `search-transparency-reporting-r84.md` →
`S018, S023, S214`; `provenance-recording-r85.md` → `S026, S031,
S215`. Located-quote citations per entry: S214 ×5 (lines 22–26),
S018 ×3 (27–29), S023 ×5 (30–34); S215 ×4 (22–25), S026 ×2
(26–27), S031 ×1 (28). UNCITED: none on either entry. Forward
(SOURCE 20/20) and reverse (USED_BY 20/20) both HELD.

## Risks / blockers

None blocking. Two wording-level findings (battery filename in
claims, `PRIOR_REGRESSION` summary denominator) for L1 to reconcile;
neither changes the C2 predicate outcome at C5.

VERDICT: R92ExecC2Repro C2 held — counter and battery pass at C5 with all substantive tokens exact, decision pin and minus-self digest independently re-derived, mod

e filename and PRIOR_REGRESSION-token wording findings.
