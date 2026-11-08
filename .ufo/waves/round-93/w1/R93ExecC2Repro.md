# R93ExecC2Repro — round-93 C2 (calibration) reproduction from a clean carrier tree

Seat: `R93ExecC2Repro` (leaf executor). Lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Claim freeze F2 `b7241252c2358613d3b22b7d0454d98c56dab373`; carrier C2
`754b62fb6adc60e44e12375af5461a0ebe302994`, cloned with
`git clone --shared /home/vgpnk/Projects/shokunin/chousa-shokunin $S/repo` and
`git -C $S/repo checkout -q 754b62fb…`; `git -C $S/repo rev-parse HEAD` = `754b62fb…`, working tree
clean before and after all runs (`git status --porcelain` empty). Scratch
`S=/fast/scratch/hyaku/chousa-r93/R93ExecC2Repro` (removed before yield). No network used, no tool
installs, no lane/git mutation, no production edits.

Instrument bytes measured (receipt `R93ExecC2Repro-hashes.txt`, copied here):
`curation-r93.py` `d9aae45d…` and `curation-controls-r93.py` `fe7dceba…` match their
`corpus/evidence/round93/instrument-pins.txt` rows exactly; the r92 counter read is
`corpus/evidence/round92/curation-r92.py` `e49fb34e…` (not a pinned row — the 16 r92-set rows do not
include it; it is the *prior* instrument, cited as evidence of the prior behaviour).

---

## (a) Clean-tree counter — `CURATION_R93=PASS` (exit 0)

Command (from `$S/repo`):

```
python3 -B corpus/evidence/round93/curation-r93.py --root .
```

Receipt: `R93ExecC2Repro-a-clean-curation.stdout.txt`. **Exit code 0.** Observed stdout (verbatim):

```
SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20 Q_ROWS=20 Q_SHAPE_FAIL=0 Q_WSQUOT=0 SOURCE_STATUS_OK=20/20 USED_BY_OK=20/20 Q_FLOORS=search-transparency-reporting-r84.md=13/13 floor13,provenance-recording-r85.md=7/7 floor7 WARRANT_OK=17/17 TFREQ_OK=17/17 TFREQ_MAX_DF=3 DUP_QIDS=0 TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 SUP_CLAUSE_CHECKED=0 SUP_UNRESOLVED=0 LEGS_MEASURED=15/15
TEACHES_FLAGGED S024 terms=publication,modification disposition=superseded by S031
VERDICT fields_hold=1 legs_ok=15/15 DETECTOR_WITNESS=11/11
CURATION_R93=PASS
```

Field-by-field against the frozen predicate and the seat's expected list:

| expected (claims.md / seat) | observed | |
|---|---|---|
| `CURATION_R93=PASS`, exit 0 | `CURATION_R93=PASS`, exit 0 | MATCH |
| `LEGS_MEASURED=15/15` | `LEGS_MEASURED=15/15` | MATCH |
| `Q_ROWS=20` | `Q_ROWS=20` (`QUOTES_LOCATED=20/20`) | MATCH |
| `Q_SHAPE_FAIL=0` | `Q_SHAPE_FAIL=0` | MATCH |
| `Q_WSQUOT=0` | `Q_WSQUOT=0` | MATCH |
| `SOURCE_STATUS_OK=20/20` | `SOURCE_STATUS_OK=20/20` | MATCH |
| `USED_BY_OK=20/20` | `USED_BY_OK=20/20` | MATCH |
| `TFREQ_OK=17/17` | `TFREQ_OK=17/17` | MATCH |
| `UNENTAILED_TERM=0` | `UNENTAILED_TERM=0` | MATCH |
| `WARRANT_OK=17/17` | `WARRANT_OK=17/17` | MATCH |
| `DUP_QIDS=0` | `DUP_QIDS=0` | MATCH |
| `Q_FLOORS` per entry | `…r84.md=13/13 floor13, …r85.md=7/7 floor7` | MATCH |
| `VERDICT fields_hold=1 … DETECTOR_WITNESS=11/11` | identical | MATCH |

## (b) Controls battery — `CONTROLS=PASS` (exit 0)

Command (from `$S/repo`):

```
python3 -B corpus/evidence/round93/curation-controls-r93.py --root . --work $S/ctl
```

Receipt: `R93ExecC2Repro-b-controls.stdout.txt`. **Exit code 0.** Observed summary (verbatim; full
ten per-case lines are in the receipt):

```
CONTROLS=PASS CARRIED_REFUSED_BOTH=4/4 WS_NAMED=2/2 WS_SHAPE_GREEN_R92=1/1 DUPCOUNT_1=1/1 PRIOR_REGRESSION=7/7
```

Against the frozen predicate (`CONTROLS=PASS CARRIED_REFUSED_BOTH=4/4 WS_NAMED=2/2
WS_SHAPE_GREEN_R92=1/1 DUPCOUNT_1=1/1 PRIOR_REGRESSION=7/7`): every token MATCH, exit 0.
Supporting case lines observed: positive `r92 rc=0 (CURATION_R92=PASS), r93 rc=0 (CURATION_R93=PASS)`;
`ws-space`/`ws-tab` `r92 rc=1 … shapes old=0 new=1 ws new=1`; the four carried classes
`c1-nonq-row`, `c2-status-rejected`, `c3-used-by-blank`, `c4-ubiquitous-warrant` all `r92 rc=1, r93 rc=1`;
`duplicate-count: r92 UNENTAILED_TERM=1 r93 UNENTAILED_TERM=1`; `regression: FORGERY_REFUSED=7/7
PRIOR_REGRESSION=7/7 rc=0`. The `--work` dir was scratch; the clone stayed clean (`git status
--porcelain` empty), so the battery wrote nothing into the tree.

## (c) Independent whitespace-quote tree (own construction, not the controls helper)

Tree `$S/mytree` built by hand: copied `corpus/SOURCES.md`, the two routed entries
(`corpus/knowledge/search-transparency-reporting-r84.md`,
`corpus/knowledge/provenance-recording-r85.md`) and symlinked `corpus/captures` to the clone's store.
One edit only, in entry A's Located-quotes table: hypothesis-independent replacement of the Q2 quote
cell with a single space — `| Q2 | S214 | "date when each source was last searched or consulted." |`
→ `| Q2 | S214 | " " |` (`diff` and tree listing in receipt
`R93ExecC2Repro-c-tree-provenance.txt`; it shows exactly that one line changed).

Commands (counters from the clean clone, `--root $S/mytree`):

```
python3 -B corpus/evidence/round92/curation-r92.py --root $S/mytree
python3 -B corpus/evidence/round93/curation-r93.py --root $S/mytree
```

### r92 counter on the whitespace tree — exit 1, `CURATION_R92=FAIL`

Receipt: `R93ExecC2Repro-c-r92-ws-tree.stdout.txt`.

- `Q_SHAPE_FAIL=0` (the class is invisible to the shape test), `Q_ROWS=20`, `QUOTES_LOCATED=20/20`,
  `WARRANT_OK=16/17 TFREQ_OK=16/17`, `LEGS_MEASURED=10/14`.
- `WARRANT_UNLINKED corpus/knowledge/search-transparency-reporting-r84.md row=Reporting when a source
  was searched warrant=Q2 (S214) resolved=1/1`
- `LEG_FAIL` lines (verbatim):

```
LEG_FAIL FLOOR search-transparency-reporting-r84.md=13/13 floor13,provenance-recording-r85.md=7/7 floor7
LEG_FAIL WARRANT 16/17 width_fail=0 count_bad=0
LEG_FAIL TFREQ 16/17 max_df=3<=3
LEG_FAIL VERDICT fields_hold=0 legs_ok=10/13
```

**Legs that refused the tree under r92: FLOOR, WARRANT, TFREQ** (VERDICT is the tally echo of the
leg results). The refusal is downstream and unnamed: the shape leg is green, `Q_SHAPE_FAIL=0`; the FLOOR
leg fails even though it prints `13/13 floor13` because the whitespace quote has 0 tokens
(`MIN_TOKENS=7`, r92 `short_rows`), and WARRANT/TFREQ fail on the Q2 row whose quote shares no term.
Mechanism confirmed in the r92 source: `q_shape_violation` tests `not cells[2].strip().strip('"')` —
whitespace is stripped *before* the quotes, so the inner single space survives the cell.

### r93 counter on the same tree — exit 1, `CURATION_R93=FAIL`

Receipt: `R93ExecC2Repro-c-r93-ws-tree.stdout.txt`.

- `Q_SHAPE_FAIL=1`, `Q_WSQUOT=1`, `Q_ROWS=19`, `QUOTES_LOCATED=19/19`,
  `Q_FLOORS=…r84.md=12/12 floor13,…r85.md=7/7 floor7`, `WARRANT_OK=16/17 TFREQ_OK=16/16`,
  `LEGS_MEASURED=10/15`.
- The named shape line (verbatim):

```
Q_SHAPE search-transparency-reporting-r84.md quote=<whitespace> row=| Q2 | S214 | " " |
```

- `LEG_FAIL` lines (verbatim):

```
LEG_FAIL FLOOR search-transparency-reporting-r84.md=12/12 floor13,provenance-recording-r85.md=7/7 floor7
LEG_FAIL QSHAPE search-transparency-reporting-r84.md quote=<whitespace>
LEG_FAIL WARRANT 16/17 width_fail=0 count_bad=0
LEG_FAIL WSQUOTE search-transparency-reporting-r84.md Q2
LEG_FAIL VERDICT fields_hold=0 legs_ok=10/14
```

**Legs that refused the tree under r93: QSHAPE (naming `quote=<whitespace>`), WSQUOTE (naming Q2),
FLOOR, WARRANT** (VERDICT echoes). This is the classification the claim asserts: the same bytes that r92
only refused downstream are refused at the shape leg with the class named, and the independent WSQUOTE
population leg counts the row (`Q_WSQUOT=1`). `Q_WSQUOT` counts the row *before* the shape filter — the
append precedes the `q_shape_violation` continue in `curation-r93.py` — so it is not a restatement of
the shape drop, and it is 0 on the clean tree (see (a)).

Difference summary for the same forged bytes: r92 `Q_SHAPE_FAIL=0` / no class named / `Q_ROWS=20`;
r93 `Q_SHAPE_FAIL=1` / `quote=<whitespace>` + `Q_WSQUOT=1` / `Q_ROWS=19`. The committed Before receipt
`corpus/evidence/round93/evidence-before/c2-prior-accepts.txt` (copied here as
`R93ExecC2Repro-evidence-before-c2-prior-accepts-asfound.txt`) reports the same r92 and r93 lines
field-for-field; my run is independent of it and of the controls helper.

## (d) Hand count of the two routed entries (receipt `R93ExecC2Repro-d-hand-count.txt`)

| entry | Located-quotes data rows | width | Decision-table data rows | width |
|---|---|---|---|---|
| `corpus/knowledge/search-transparency-reporting-r84.md` | **13** (Q1–Q13: S214×5, S018×3, S023×5) | **3** (qid/source/quote) | **11** | **4** (Situation/Do/Never/Warrant) |
| `corpus/knowledge/provenance-recording-r85.md` | **7** (Q1–Q7: S215×4, S026×2, S031×1) | **3** | **6** | **4** |

Totals: 13+7 = 20 located-quote rows (matches `Q_ROWS=20`), 11+6 = 17 decision rows (matches
`WARRANT_OK=17/17` / `TFREQ_OK=17/17`). Independent corroboration (not the counter): pipe-leading lines
per section are 15/13 in entry A and 9/8 in entry B; minus header+separator gives 13/11 and 7/6.

## Kill-rule / limit observations (my measurement, scoped to C2)

- **K1**: not triggered — predicate met at C2, exit 0, every expected field present ((a), (b)).
- **K2**: not triggered — the positive is accepted by both counters, the four carried classes are refused
  by both, the two whitespace trees are refused by r93, and the r90 regression line is
  `FORGERY_REFUSED=7/7`.
- **K3**: not triggered — the clean run locates all 20 quotes, keeps both floors (`13/13 floor13`,
  `7/7 floor7`) and all 17 warranted rows; nothing genuine moved.
- **K4**: not vacuous by construction and by measurement — `Q_WSQUOT` is 0 on the clean tree and 1 on the
  forged tree, and the leg is counted: `EXPECTED_LEGS=15` and `passed` requires `len(legs) ==
  EXPECTED_LEGS`, so deleting the WSQUOTE leg yields 14 legs and a FAIL. The WSQUOTE population is
  appended before the QSHAPE filter, so the count is independent of the shape drop.
- Named limits left untested by this seat (by design, not claimed): an unresolvable whitespace quote
  would report at FLOOR; `DECISION_WIDTH` is observability only. No leg vocabulary beyond the observed
  15 (`10/14` → `10/15` on the same bytes) was assumed.

## Findings (deviations recorded, not hidden)

**F1 — the C2 Before receipt cited by the frozen claims is not carried by the carrier.** `claims.md`
line 71 names `corpus/evidence/round93/evidence-before/c2-prior-accepts.txt` as the Before measurement.
At C2, `git ls-tree -r 754b62fb… -- corpus/evidence/round93` contains no `evidence-before` path at all,
and the lane tree shows the whole directory as untracked (`git status --porcelain` →
`?? corpus/evidence/round93/evidence-before/`; directory contents at first inspection were only
`.keep`). The file now present in the lane (mtime `2026-11-08 11:11:42 -0300`, written after C2 was
committed) is an untracked round artifact, not a carrier receipt; its r92/r93 lines match my independent
measurement field-for-field. Impact: the Before citation is not auditable from committed bytes at C2;
the Before behaviour itself is fully reproducible from committed instruments (my (c) run). Not a C2
predicate failure. Same untracked status applies to the sibling `c3-prior-accepts.txt`; `c1-prior-accepts`
was absent at inspection time (outside my seat's claim scope; flagged for the sink/scribe).

**F2 — the machine-form claim's control tokens drift from the shipped battery.** `.ufo/waves/round-93/
claims.json` (committed at C2) states `C2.predicate.controls = ["CONTROLS=PASS", "FORGERY_REFUSED=4/4",
"PRIOR_ACCEPTED=4/4", "FORGERY_REFUSED=7/7"]`, but the shipped `curation-controls-r93.py` never prints
`FORGERY_REFUSED=4/4` or `PRIOR_ACCEPTED=4/4` as summary fields; it prints
`CARRIED_REFUSED_BOTH=4/4 WS_NAMED=2/2 WS_SHAPE_GREEN_R92=1/1 DUPCOUNT_1=1/1 PRIOR_REGRESSION=7/7`
(claims.md's canonical line, observed in (b)). Impact: a scorer token-matching claims.json's controls
list would find `FORGERY_REFUSED=4/4` and `PRIOR_ACCEPTED=4/4` absent, and `FORGERY_REFUSED=7/7` only on
the inner regression diagnostic line (`OK regression: FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7 rc=0`),
not in the CONTROLS summary line.
The canonical claims.md predicate and the seat's expected line match the binary exactly; measured C2
outcome unaffected. Documentation drift for the freeze's machine form.

## Receipts copied into this wave folder

- `R93ExecC2Repro-a-clean-curation.stdout.txt` — (a) clean counter stdout, exit 0.
- `R93ExecC2Repro-b-controls.stdout.txt` — (b) battery stdout, exit 0.
- `R93ExecC2Repro-c-r92-ws-tree.stdout.txt` — (c) r92 on my whitespace tree, exit 1.
- `R93ExecC2Repro-c-r93-ws-tree.stdout.txt` — (c) r93 on my whitespace tree, exit 1.
- `R93ExecC2Repro-c-tree-provenance.txt` — tree construction, the one-cell `diff -u`, file listing.
- `R93ExecC2Repro-d-hand-count.txt` — (d) hand tables and totals.
- `R93ExecC2Repro-hashes.txt` — C2 rev, instrument sha256 vs `instrument-pins.txt` rows.
- `R93ExecC2Repro-frozen-c2-prior-controls.txt`, `R93ExecC2Repro-frozen-c2-prior-landing.txt` — the two
  committed C2 receipts (`computed_against=b7241252…`, read from the C2 clone).
- `R93ExecC2Repro-evidence-before-c2-prior-accepts-asfound.txt` — as-found untracked lane copy of the
  Before receipt named by claims.md (see F1).

Scratch `/fast/scratch/hyaku/chousa-r93/R93ExecC2Repro` deleted before yield; no files written outside
this folder.

VERDICT: R93ExecC2Repro C2 held — at carrier C2 the counter prints CURATION_R93=PASS (exit 0, LEGS_MEASURED=15/15 Q_SHAPE_FAIL=0 Q_WSQUOT=0 over 20 located quotes and 17 warranted rows), the battery prints CONTROLS=PASS with CARRIED_REFUSED_BOTH=4/4 WS_NAMED=2/2 WS_SHAPE_GREEN_R92=1/1 DUPCOUNT_1=1/1 PRIOR_REGRESSION=7/7 (exit 0), an independently built whitespace-quote tree shows r92 Q_SHAPE_FAIL=0 with only FLOOR/WARRANT/TFREQ refusals while r93 names quote=<whitespace> with Q_SHAPE_FAIL=1 and Q_WSQUOT=1, and the hand counts (13/7 quote rows at width 3, 11/6 decision rows at width 4) match the counter, with the two findings (untracked Before receipt, claims.json control-token drift) recorded above.
