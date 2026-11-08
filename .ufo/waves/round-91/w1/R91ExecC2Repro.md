# R91ExecC2Repro — round-91 C2 (calibration) reproduction from a clean tree

Seat: `R91ExecC2Repro` (leaf executor, lane `chousa-shokunin`). No task/subagent dispatch, no lane mutation, no
network, no host mutation.

- Root attacked: `/home/vgpnk/Projects/shokunin/chousa-shokunin`
- Scratch: `/fast/scratch/hyaku/chousa-r91/R91ExecC2Repro` (removed before yield)
- Tree: `git clone --shared <lane> $S/repo` + `git -C $S/repo checkout -q 67954adc599bd605705d94a1ea7abb582491a907`
  → `git -C $S/repo rev-parse HEAD` = `67954adc599bd605705d94a1ea7abb582491a907` (carrier C3; parent
  `4d00d7519290569879f853d7122b82a927cda1f3`, freeze F3)
- Receipts: `.ufo/waves/round-91/w1/receipts/R91ExecC2Repro/` (every file cited below, plus the probe source)

All commands were run with cwd `$S/repo` and `--root .`; scratch dirs passed explicitly; `$S` lives under
`/fast/scratch/hyaku/`; nothing written under `/tmp`.

## (a) r91 counter on the clean tree — PASS

```
$ python3 -B corpus/evidence/round91/curation-r91.py --root .
SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20 Q_ROWS=20 Q_SHAPE_FAIL=0 SOURCE_STATUS_OK=20/20 USED_BY_OK=20/20 Q_FLOORS=search-transparency-reporting-r84.md=13/13 floor13,provenance-recording-r85.md=7/7 floor7 WARRANT_OK=17/17 TFREQ_OK=17/17 TFREQ_MAX_DF=3 DUP_QIDS=0 TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 SUP_CLAUSE_CHECKED=0 SUP_UNRESOLVED=0 LEGS_MEASURED=13/13
TEACHES_FLAGGED S024 terms=publication,modification disposition=superseded by S031
VERDICT fields_hold=1 legs_ok=13/13 DETECTOR_WITNESS=11/11
CURATION_R91=PASS
EXIT_R91_CLEAN=0
```
Receipt: `receipts/R91ExecC2Repro/r91-clean.txt`.

Frozen expectation vs observed, field by field: `CURATION_R91=PASS` ✓ · `LEGS_MEASURED=13/13` ✓ · `Q_ROWS=20` ✓ ·
`Q_SHAPE_FAIL=0` ✓ · `SOURCE_STATUS_OK=20/20` ✓ · `USED_BY_OK=20/20` ✓ · `TFREQ_OK=17/17` ✓ · `TFREQ_MAX_DF=3` ✓ ·
`UNENTAILED_TERM=0` ✓ · also present and matching the claim: `WARRANT_OK=17/17`, `DUP_QIDS=0`,
`VERDICT fields_hold=1`, `DETECTOR_WITNESS=11/11`. No deviation.

Kill-rule K3 (the counter writes the tree): `git -C $S/repo status --porcelain` was empty both before and after all
counter runs (`STATUS_EMPTY=0`, post-run listing empty). No tree write observed.

## (b) r91 discrimination battery — PASS (line verbatim)

```
$ python3 -B corpus/evidence/round91/curation-r91-controls.py --root . --work $S/ctl
OK positive: r90 CURATION_R90=PASS r91 CURATION_R91=PASS
OK nonq-row: r91 CURATION_R91=FAIL (LEG_FAIL QSHAPE), r90 CURATION_R90=PASS
OK status-rejected: r91 CURATION_R91=FAIL (LEG_FAIL SOURCE), r90 CURATION_R90=PASS
OK used-by-blank: r91 CURATION_R91=FAIL (LEG_FAIL SOURCE), r90 CURATION_R90=PASS
OK ubiquitous-warrant: r91 CURATION_R91=FAIL (LEG_FAIL TFREQ), r90 CURATION_R90=PASS
OK duplicate-count: r90 UNENTAILED_TERM=2 r91 UNENTAILED_TERM=1
OK regression: FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7 rc=0
CONTROLS=PASS FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 DUPCOUNT_R90=2 DUPCOUNT_R91=1 PRIOR_REGRESSION=7/7
EXIT_CONTROLS=0
```
Receipt: `receipts/R91ExecC2Repro/r91-controls.txt`. Matches the frozen summary line exactly, exit 0.

## (c) prior counter on the clean tree — no regression by construction

```
$ python3 -B corpus/evidence/round90/curation-r90.py --root .
SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20
Q_FLOORS=search-transparency-reporting-r84.md=13/13 floor13,provenance-recording-r85.md=7/7 floor7
WARRANT_OK=17/17 DUP_QIDS=0 TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 SUP_CLAUSE_CHECKED=0
SUP_UNRESOLVED=0 LEGS_MEASURED=10/10 VERDICT fields_hold=1
TEACHES_FLAGGED S024 terms=publication,modification disposition=superseded by S031
VERDICT fields_hold=1 legs_ok=10/10 DETECTOR_WITNESS=8/8
CURATION_R90=PASS
EXIT_R90_CLEAN=0
```
Receipt: `receipts/R91ExecC2Repro/r90-clean.txt`. `CURATION_R90=PASS`, exit 0 — the prior counter still accepts the
clean tree. (Its own counts are 10 legs / witness 8 by construction: r90 has no QSHAPE, SOURCE, TFREQ legs.)

## (d) DF_MAX derived independently — 3

Probe `probe-df.py` (`receipts/R91ExecC2Repro/probe-df.py.txt`) is written from scratch and **does not import or
call** `curation-r91.py`; it re-parses the two routed entries and recomputes document frequency over
documents = located-quote texts + decision rows' Do/Never cells (claims.md C2 named limit 2: the entry's own units).
Terms are `[a-z]{5,}` tokens, measured twice: **raw** and **filtered** by the counter's fixed stopword list, so the
list cannot manufacture the result.

```
$ python3 -B $S/probe-df.py .
LICENSE_ROW term=source df_per_entry=[5, 2] (counter comment claims df 7)
entry                                        situation                                    warrant    min_df_raw min_df_fil             argmin shared
search-transparency-reporting-r84.md         Reporting which sources were searched        Q1 (S214)           2          2        other(df=2)      4
search-transparency-reporting-r84.md         Reporting when a source was searched         Q2 (S214)           3          3     searched(df=3)      3
search-transparency-reporting-r84.md         Reporting the search method                  Q3 (S214)           2          2      filters(df=2)      5
search-transparency-reporting-r84.md         Reporting how studies were selected          Q4 (S214)           2          2     criteria(df=2)      6
search-transparency-reporting-r84.md         Reporting the search outcome                 Q5 (S214)           2          2   identified(df=2)      4
search-transparency-reporting-r84.md         Linking a claim to its source                Q6, Q7 (S018)          3          3   supporting(df=2)      2
search-transparency-reporting-r84.md         Comparing evidence-based generation approach Q8 (S018)           2          2   benchmarks(df=2)      5
search-transparency-reporting-r84.md         Recording what a resource derives from       Q9 (S023)           2          2      derived(df=2)      5
search-transparency-reporting-r84.md         Recording when a resource changed            Q13 (S023)          2          2      changed(df=2)      3
search-transparency-reporting-r84.md         Recording when a resource is valid           Q11 (S023)          2          2        range(df=2)      3
search-transparency-reporting-r84.md         Recording when a resource became available   Q12 (S023)          2          2    available(df=2)      4
provenance-recording-r85.md                  Naming what a resource derives from          Q1 (S215)           2          2     property(df=2)      3
provenance-recording-r85.md                  Recording a derivation's direction           Q2 (S215)           2          2      another(df=2)      4
provenance-recording-r85.md                  Recording the bounds of an entity's existenc Q4 (S215)           2          2        bound(df=2)      2
provenance-recording-r85.md                  Recording a resource's provenance            Q5 (S026)           2          2   conditions(df=2)      4
provenance-recording-r85.md                  Recording the source behind a resource       Q6 (S026)           2          2       credit(df=2)      6
provenance-recording-r85.md                  Recording when content was last reviewed     Q7 (S031)           2          2     accuracy(df=2)      4
ROWS=17
MAX_OF_ROW_MINIMA_RAW=3 MAX_OF_ROW_MINIMA_FILTERED=3 MAX_PER_QID_COUNTER_SHAPE=3
PROBE_D2_DF_MAX=3
EXIT=0
```
Receipt: `receipts/R91ExecC2Repro/probe-df.txt`.

17 legitimate decision rows, every one has a shared term at df ≤ 3, and the **maximum of those minima is 3** — under
the raw token set, under the stopword-filtered set, and under the counter's per-qid shape. `DF_MAX=3` is therefore
the measured maximum, not a free parameter.

Tightness (why 3 and not more): a copy of the counter with `DF_MAX = 2` (scratch only, `$S/tight/`) run on the same
clean tree prints `TFREQ_OK=15/17 TFREQ_MAX_DF=2` with `LEG_FAIL TFREQ` / `CURATION_R91=FAIL` exit 1 — two legitimate
rows are refused at 2, so 3 is the smallest bound that passes and exactly the measured maximum. Receipt:
`receipts/R91ExecC2Repro/dfmax2.txt`.

## (e) `source`-only warrant forgery — refused by r91, accepted by r90

The controls battery's tree persists under `$S/ctl/ubiquitous-warrant` (the F4 forgery appends
`| Reporting the source | state the source | report it without the source | Q2 (S214) |` to the r84 decision table).
Both counters were run against that tree directly, independent of the battery's own `OK` lines:

```
$ python3 -B corpus/evidence/round91/curation-r91.py --root $S/ctl/ubiquitous-warrant
... WARRANT_OK=18/18 TFREQ_OK=17/18 TFREQ_MAX_DF=3 ... LEGS_MEASURED=11/13
VERDICT fields_hold=0 legs_ok=11/13 DETECTOR_WITNESS=11/11
LEG_FAIL TFREQ 17/18 max_df=3<=3
LEG_FAIL VERDICT fields_hold=0 legs_ok=11/12
CURATION_R91=FAIL
EXIT_R91=1
```
`receipts/R91ExecC2Repro/forgery-ubiquitous-warrant-r91.txt`

```
$ python3 -B corpus/evidence/round90/curation-r90.py --root $S/ctl/ubiquitous-warrant
... WARRANT_OK=18/18 ... LEGS_MEASURED=10/10 VERDICT fields_hold=1
CURATION_R90=PASS
EXIT_R90=0
```
`receipts/R91ExecC2Repro/forgery-ubiquitous-warrant-r90.txt`

The discrimination is real in both directions: the forged row resolves its qid and shares words (r90 counts it, so
`WARRANT_OK=18/18` for both), and only r91's `TFREQ` leg refuses it because its only shared term is `source`, whose
per-entry token df exceeds `DF_MAX`. The other three forgeries were re-run the same way (not only through the
battery's wrapper):

| forgery | r91 | r90 |
|---|---|---|
| nonq-row | `LEG_FAIL QSHAPE ... qid=note`, `CURATION_R91=FAIL`, exit 1 | `CURATION_R90=PASS`, exit 0 |
| status-rejected | `LEG_FAIL SOURCE status_fail=5 used_by_fail=0 rows=20`, exit 1 | `CURATION_R90=PASS`, exit 0 |
| used-by-blank | `LEG_FAIL SOURCE status_fail=0 used_by_fail=5 rows=20`, exit 1 | `CURATION_R90=PASS`, exit 0 |
| ubiquitous-warrant | `LEG_FAIL TFREQ 17/18`, exit 1 | `CURATION_R90=PASS`, exit 0 |

Receipts: `forgery-<name>-r91.txt` / `forgery-<name>-r90.txt`. Pristine mirror accepted by both
(`pristine-r91.txt`, `pristine-r90.txt`: `CURATION_R91=PASS` / `CURATION_R90=PASS`, exit 0 each), so the refusals are
not blanket refusals.

## Observations (non-blocking, no claim moves)

1. **`df 7` is a pooled figure, not the per-entry figure the code measures.**
   `corpus/evidence/round91/curation-r91.py` comment block (R3) and `claims.md` C2 (forgery F4, "a warrant sharing
   only `source`, df 7") name `source` at df 7. Measured token df over the entry's own units is **5** for r84 (clean)
   / **6** (forged) and **2** for r85; 7 is the sum across the two entries, which named limit 2 ("the entry's own
   units") excludes. Receipt: `df-detail.txt`. The refusal stands (5 > DF_MAX=3) and no leg changes, but the comment's
   number is the pooled count, so a reader re-deriving the figure from one entry gets 5.
2. **`TFREQ_MAX_DF` is a max of per-qid minima, not of per-row minima.** The counter updates `tfreq_max` inside the
   per-qid loop, so the two-qid row "Linking a claim to its source" contributes 3 (Q7/`evidence`, df 3) although the
   row's own minimum shared df is 2 (Q6/`supporting`). Consequence is nil here — the probe measures 3 under both the
   per-row and the per-qid shape — but a future multi-qid row whose second quote shares only a df-3+ term would move
   the printed maximum for a reason the field name does not suggest.
3. The probe takes every `Q<n>` three-cell row as located rather than re-verifying capture containment; that
   assumption rests on the counter's own `QUOTES_LOCATED=20/20`, which this reproduction confirms. A tree with an
   unlocated quote would make the probe's document set and the counter's differ.

## Limits of this evidence

- Everything above is one clean clone at C3; the C2 predicate is reproduced for the tree C3 carries, not for F3 in
  isolation (the two commits differ only by the receipt files the claim set scopes to C1).
- The probe shares the markdown shape (`## Located quotes`, `## Decision table`, four-cell rows) with the counter; it
  is independent of the counter's code and legs, not of the document format the claims pin.
- `DETECTOR_WITNESS=11/11` and `PRIOR_REGRESSION=7/7` were read from the counter's/battery's own emitted lines; the
  two-directional detectors were not re-implemented independently.

No tool installs or upgrades were needed this round.

VERDICT: R91ExecC2Repro C2 held — r91 prints `CURATION_R91=PASS` (13/13 legs, TFREQ 17/17, max df 3) on the clean C3 tree, the battery prints `CONTROLS=PASS FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 DUPCOUNT_R90=2 DUPCOUNT_R91=1 PRIOR_REGRESSION=7/7`, r90 still prints `CURATION_R90=PASS` there, an independent probe re-derives `DF_MAX=3` as the maximum of 17 per-row minima (and 2 refuses two legitimate rows), and the `source`-only forgery prints `LEG_FAIL TFREQ` under r91 against `CURATION_R90=PASS` under r90.
VERDICT: R91ExecC2Repro C1 n/a — not this seat's claim; not run.
VERDICT: R91ExecC2Repro C3 n/a — not this seat's claim; not run.
