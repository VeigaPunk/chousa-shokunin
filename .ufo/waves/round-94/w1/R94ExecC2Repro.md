# R94ExecC2Repro — C2 `C2-CURATION-R94` reproduced from a clean tree (round 94, wave w1)

Seat: executor `R94ExecC2Repro`. Scope: reproduce frozen C2 at carrier C and independently measure the
punctuation class plus the digits-only named limit. No production edits, no commits, no lane mutation.
All receipts cited below are copied to `receipts-R94ExecC2Repro/` beside this report.

## Tree identity

```
git clone --shared /home/vgpnk/Projects/shokunin/chousa-shokunin \
  /fast/scratch/hyaku/chousa-r94/R94ExecC2Repro/repo
git -C $S/repo checkout 352924bbea624caf3771ef291be98fd4ec679dda
git -C $S/repo rev-parse HEAD   -> 352924bbea624caf3771ef291be98fd4ec679dda   (carrier C)
git -C $S/repo status --porcelain -> 0 lines after every run (counters write nothing)
```

sha256 of the bytes actually executed (from the clone; recorded in `MATERIAL.txt`):

| file | sha256 |
|---|---|
| `corpus/evidence/round94/curation-r94.py` | `4b9ce115e3700a7ec998c77128ad176b326ac6c126a0019709fad46eb29df144` |
| `corpus/evidence/round94/curation-controls-r94.py` | `79b76fdc14e9bc4c24e5b36e4b0076a4f0547b8a0f4afe3d81df4d0d9de0378f` |
| `corpus/evidence/round93/curation-r93.py` | `6c3c58df40b0023c7344137b36279e3f329eb695f1f5f964937823c4752101d8` |
| `corpus/SOURCES.md` | `2e99e3faa44f2f470317fd382c3ccc7b24adb00530e2fc12b8f0fbcca366ea4f` |
| `corpus/evidence/round93/controls/legs.txt` | `c03774389e483de7d2d64d44b71291c5cfae3ff4df62a5e33de092d9b89f3142` |
| `corpus/evidence/round94/controls/legs.txt` | `98731d3a9036e6806d72b6cf99550067f247b6321450e9f2b48a02ff63ac7cf9` |

Scratch was `/fast/scratch/hyaku/chousa-r94/R94ExecC2Repro` throughout; `TMPDIR` was set inside it,
nothing was written under `/tmp`. The shared clone was never repacked (S221: it owns no objects).

## (a) Frozen counter predicate — held

Command (run from the clone root):

```
cd $S/repo && python3 -B corpus/evidence/round94/curation-r94.py --root .
```

Receipt: `receipts-R94ExecC2Repro/a-curation-r94.txt`. Exit `0`. Observed lines:

```
SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20 Q_ROWS=20 Q_SHAPE_FAIL=0 Q_WSQUOT=0 Q_PUNCTQUOT=0 SOURCE_STATUS_OK=20/20 USED_BY_OK=20/20 Q_FLOORS=search-transparency-reporting-r84.md=13/13 floor13,provenance-recording-r85.md=7/7 floor7 WARRANT_OK=17/17 TFREQ_OK=17/17 TFREQ_MAX_DF=3 DUP_QIDS=0 TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 SUP_CLAUSE_CHECKED=0 SUP_UNRESOLVED=0 LEGS_MEASURED=16/16
TEACHES_FLAGGED S024 terms=publication,modification disposition=superseded by S031
VERDICT fields_hold=1 legs_ok=16/16 DETECTOR_WITNESS=17/17
CURATION_R94=PASS
EXIT=0
```

Every field the seat spec names is present with the expected value: `LEGS_MEASURED=16/16`, `Q_ROWS=20`,
`Q_SHAPE_FAIL=0`, `Q_WSQUOT=0`, `Q_PUNCTQUOT=0`, `WARRANT_OK=17/17`, `TFREQ_OK=17/17`, `DUP_QIDS=0`,
`DETECTOR_WITNESS=17/17`, `CURATION_R94=PASS`.

## (b) Controls battery — held

Command (run from the clone root):

```
cd $S/repo && python3 -B corpus/evidence/round94/curation-controls-r94.py --root . --work $S/ctl2
```

Receipt: `receipts-R94ExecC2Repro/b-curation-controls-r94.txt`. Exit `0`. All twelve case lines are
`OK`; two of them are the class witnesses:

```
OK x1-punct-dash: r93 rc=1 (CURATION_R93=FAIL), r94 rc=1 (CURATION_R94=FAIL) shapes old=0 new=1 punct new=1
OK x2-punct-dots: r93 rc=1 (CURATION_R93=FAIL), r94 rc=1 (CURATION_R94=FAIL) shapes old=0 new=1 punct new=1
OK punct-classification: r93 Q_SHAPE_FAIL=0 on both punctuation trees (the class the r94 shape leg names)
OK regression: FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7 rc=0
CONTROLS=PASS CARRIED_REFUSED_BOTH=4/4 WS_NAMED=2/2 PUNCT_NAMED=2/2 PUNCT_SHAPE_GREEN_R93=1/1 DUPCOUNT_1=1/1 PRIOR_REGRESSION=7/7
EXIT=0
```

## (c) Independent punctuation measurement (own tree, not the controls mirror)

Construction (my own, from the clone; the controls script was not reused to build it): a tree holding
copies of `corpus/knowledge/search-transparency-reporting-r84.md`,
`corpus/knowledge/provenance-recording-r85.md`, `corpus/SOURCES.md` and both leg tables
(`corpus/evidence/round93/controls/legs.txt`, `corpus/evidence/round94/controls/legs.txt`), with
`corpus/captures` a symlink to the clone's capture store. Clean control `v0-clean` (same construction,
no mutation) passes both counters — `CURATION_R93=PASS` rc 0 and `CURATION_R94=PASS` rc 0
(`v0-clean-r93.txt`, `v0-clean-r94.txt`) — so a red result on a mutated tree is the mutation, not the
mirror.

Each variant replaces the `## Located quotes` Q2 row of
`corpus/knowledge/search-transparency-reporting-r84.md` and runs both counters with `--root <tree>`.

### v1 — assigned mutation: `| Q2 | S214 | "—" |` (S214 capture `a640b15abf781e5c583d7088` has **no** em dash)

r93 (`v1-dash-S214-r93.txt`, exit 1):

```
SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=19/20 Q_ROWS=19 Q_SHAPE_FAIL=0 Q_WSQUOT=0 SOURCE_STATUS_OK=19/19 USED_BY_OK=19/19 Q_FLOORS=search-transparency-reporting-r84.md=12/13 floor13,provenance-recording-r85.md=7/7 floor7 WARRANT_OK=16/17 ...
LEG_FAIL FLOOR search-transparency-reporting-r84.md=12/13 floor13,provenance-recording-r85.md=7/7 floor7
LEG_FAIL WARRANT 16/17 width_fail=0 count_bad=0
LEG_FAIL VERDICT fields_hold=0 legs_ok=12/14
CURATION_R93=FAIL
```

`Q_SHAPE_FAIL=0`: the r93 shape leg is green on the punctuation-only cell. The tree is refused only
downstream (FLOOR ratio, WARRANT), and no field names the punctuation class.

r94 (`v1-dash-S214-r94.txt`, exit 1):

```
Q_SHAPE search-transparency-reporting-r84.md quote=<punctuation> row=| Q2 | S214 | "—" |
LEG_FAIL FLOOR search-transparency-reporting-r84.md=12/12 floor13,provenance-recording-r85.md=7/7 floor7
LEG_FAIL QSHAPE search-transparency-reporting-r84.md quote=<punctuation>
LEG_FAIL WARRANT 16/17 width_fail=0 count_bad=0
LEG_FAIL PUNCTQUOT search-transparency-reporting-r84.md Q2
LEG_FAIL VERDICT fields_hold=0 legs_ok=11/15
CURATION_R94=FAIL
```

Summary line: `QUOTES_LOCATED=19/19 Q_ROWS=19 Q_SHAPE_FAIL=1 Q_WSQUOT=0 Q_PUNCTQUOT=1 ...`.
The class is named at the shape leg (`quote=<punctuation>`), counted (`Q_PUNCTQUOT=1`) and refused as
its own leg (`LEG_FAIL PUNCTQUOT`).

### v2 — same punctuation cell citing a source whose capture **does** contain an em dash

`| Q2 | S018 | "—" |`; S018's capture `248b43277f376e437a356909.txt` contains U+2014. S018 is
`status=mined` with `used-by=corpus/knowledge/search-transparency-reporting-r84.md`, so the SOURCE leg
is not confounding.

r93 (`v2-dash-S018-r93.txt`, exit 1):

```
QUOTES_LOCATED=20/20 Q_ROWS=20 Q_SHAPE_FAIL=0 Q_WSQUOT=0 ...
Q_FLOORS=search-transparency-reporting-r84.md=13/13 floor13,provenance-recording-r85.md=7/7 floor7
LEG_FAIL FLOOR search-transparency-reporting-r84.md=13/13 floor13,provenance-recording-r85.md=7/7 floor7
LEG_FAIL WARRANT 16/17 width_fail=0 count_bad=0
LEG_FAIL TFREQ 16/17 max_df=3<=3
LEG_FAIL VERDICT fields_hold=0 legs_ok=11/14
CURATION_R93=FAIL
```

**r93 accepts the row as located**: `QUOTES_LOCATED=20/20` and the entry ratio is `13/13 floor13` —
one more located quote than in v1. Its FLOOR leg still fails, but on the `not short` conjunct
(`"—"` is 1 token < `MIN_TOKENS=7`, code: `floors_ok = ... and not short`, r93 line 415), not on
location. Its refusal is downstream (MIN_TOKENS inside FLOOR, WARRANT, TFREQ) and still names nothing.

r94 (`v2-dash-S018-r94.txt`, exit 1):

```
Q_SHAPE search-transparency-reporting-r84.md quote=<punctuation> row=| Q2 | S018 | "—" |
LEG_FAIL FLOOR search-transparency-reporting-r84.md=12/12 floor13,provenance-recording-r85.md=7/7 floor7
LEG_FAIL QSHAPE search-transparency-reporting-r84.md quote=<punctuation>
LEG_FAIL WARRANT 16/17 width_fail=0 count_bad=0
LEG_FAIL PUNCTQUOT search-transparency-reporting-r84.md Q2
LEG_FAIL VERDICT fields_hold=0 legs_ok=11/15
CURATION_R94=FAIL
```

Summary: `QUOTES_LOCATED=19/19 Q_ROWS=19 Q_SHAPE_FAIL=1 Q_WSQUOT=0 Q_PUNCTQUOT=1`. The row is **not**
counted located: r94's `locates()` refuses it outright before the substring test.

Direct detector probe (`detector-probe.txt`) confirms the mechanism on the same bytes:

```
r94 locates('—',cap18)  -> False     r93 locates('—',cap18)  -> True
r94 locates('—',cap214) -> False     r93 locates('—',cap214) -> False
r93 locates('2026',cap18)-> True
```

C2's classification claim reproduces independently: r93 fails both punctuation trees with
`Q_SHAPE_FAIL=0` and cannot name the class; r94 names it at the shape leg and counts it, and the row is
never located by r94 even in a capture that carries the em dash.

## (d) Named limit: a digits-only quote passes the r94 shape leg — confirmed

Probe against the carrier code (`detector-probe.txt`):

```
r94 shape '2026' -> None            (no shape violation)
r94 punct '2026' -> False           (not in the punctuation class)
r94 shape '—'    -> quote=<punctuation>
r94 punct '—'    -> True
```

Two whole-tree measurements:

- `v3-digits-S214` (`| Q2 | S214 | "2026" |`, S214 capture lacks `2026`): r94 summary
  `Q_SHAPE_FAIL=0 Q_PUNCTQUOT=0`, `Q_FLOORS ...=12/13`; `LEG_FAIL FLOOR`, `LEG_FAIL WARRANT`;
  `CURATION_R94=FAIL`, exit 1 (`v3-digits-S214-r94.txt`). r93 behaves the same (`v3-digits-S214-r93.txt`).
- `v4-digits-S018` (`| Q2 | S018 | "2026" |`, S018 capture contains `2026`): r94 summary
  `QUOTES_LOCATED=20/20 Q_ROWS=20 Q_SHAPE_FAIL=0 Q_WSQUOT=0 Q_PUNCTQUOT=0`, `Q_FLOORS ...=13/13 floor13`;
  `LEG_FAIL FLOOR ...=13/13 floor13`, `LEG_FAIL WARRANT 16/17`, `LEG_FAIL TFREQ 16/17`;
  `CURATION_R94=FAIL`, exit 1 (`v4-digits-S018-r94.txt`).

Verdict: **yes — a quote of only digits passes the r94 shape leg.** `PUNCT_RE = [A-Za-z0-9]` is
alphanumeric by definition, so `"2026"` is outside the punctuation class: `Q_SHAPE_FAIL=0`,
`Q_PUNCTQUOT=0`, and when the cited capture contains the digits the row is counted located
(`20/20`, `13/13`). The row is refused only by the pre-existing downstream conjuncts (`MIN_TOKENS`
inside FLOOR, WARRANT, TFREQ), never by a named punctuation-class line. This is the measured edge of
C2's class ("no alphanumeric character"), not a kill-rule breach: K2 concerns punctuation trees, which
this is not. It is recorded here as the named limit the frozen claim states.

## Findings

F1 — (a) the frozen counter predicate holds at C. Command
`cd $S/repo && python3 -B corpus/evidence/round94/curation-r94.py --root .`; receipt
`receipts-R94ExecC2Repro/a-curation-r94.txt`; observed `CURATION_R94=PASS` with
`LEGS_MEASURED=16/16 ... DUP_QIDS=0` and `DETECTOR_WITNESS=17/17`; exit `0`. No deviation.

F2 — (b) the controls battery holds at C. Command
`cd $S/repo && python3 -B corpus/evidence/round94/curation-controls-r94.py --root . --work $S/ctl2`;
receipt `receipts-R94ExecC2Repro/b-curation-controls-r94.txt`; observed
`CONTROLS=PASS CARRIED_REFUSED_BOTH=4/4 WS_NAMED=2/2 PUNCT_NAMED=2/2 PUNCT_SHAPE_GREEN_R93=1/1 DUPCOUNT_1=1/1 PRIOR_REGRESSION=7/7`;
exit `0`. No deviation.

F3 — (c) classification claim reproduces independently. Commands
`python3 -B corpus/evidence/round93/curation-r93.py --root <tree>` and
`python3 -B corpus/evidence/round94/curation-r94.py --root <tree>` over my own tree, variants v1/v2;
receipts `v1-dash-S214-r93.txt`, `v1-dash-S214-r94.txt`, `v2-dash-S018-r93.txt`, `v2-dash-S018-r94.txt`;
observed r93 `Q_SHAPE_FAIL=0` on both, with `LOCATED=20/20` (13/13) on the em-dash capture, versus r94
`Q_SHAPE_FAIL=1 Q_PUNCTQUOT=1` plus `Q_SHAPE ... quote=<punctuation>` and `LEG_FAIL PUNCTQUOT`; both
exit `1`. Clean control `v0-clean` passes both counters (exit `0` each). No deviation from the claim.

F4 — (d) digits-only quote: shape leg green, measured limit. Receipts `v3-digits-S214-r94.txt`,
`v4-digits-S018-r94.txt`, `detector-probe.txt`; observed `Q_SHAPE_FAIL=0 Q_PUNCTQUOT=0` on both and
`QUOTES_LOCATED=20/20` on v4, exit `1` from downstream legs. No deviation from the frozen text; the
frozen claim does not assert digits are refused at the shape leg.

## Residuals and risks (reported, not remediated)

- v2 shows r93's acceptance of a punctuation-only quote as *located* (`20/20`) is what makes the class
  dangerous: its only catch is the incidental `MIN_TOKENS` conjunct. If a future tree carries a
  punctuation-only quote and that conjunct were relaxed, r93 would count it located while r94 refuses it
  at the shape leg. Observed on the bytes, not inferred.
- r94's `locates()` is a global refusal (probe: False against both captures), matching named limit (3)
  of C2; no path was found where a punctuation-only quote locates a source under r94.
- `[INFERENCE]` A multi-token digits-only quote would clear `MIN_TOKENS` but has no `[a-z]{5,}` term, so
  WARRANT/TFREQ would still refuse any row that warrants on it; not measured in this seat (out of the
  assigned `"2026"` case).

## Tooling

No tool installs or upgrades; no pacman transactions (guard respected). Only `python3` stdlib and the
installed `git` were used. Scratch deleted at seat end.

VERDICT: R94ExecC2Repro C1 n/a — no C1 command was in this seat's assignment; the pins/driver walk was not executed here.
VERDICT: R94ExecC2Repro C2 held — both frozen counters meet their predicates at carrier C with exit 0, and the independent tree reproduces the classification split (r93 `Q_SHAPE_FAIL=0` / r94 `quote=<punctuation>` + `Q_PUNCTQUOT=1`) plus the digits-only named limit.
VERDICT: R94ExecC2Repro C3 n/a — no C3 command was in this seat's assignment; the tally walk was not executed here.
