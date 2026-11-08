# R93CriticClaims — round-93 claim critic (C1/C2/C3, assigned freeze F2/C2)

Seat `R93CriticClaims` (leaf, lane chousa round 93). Assigned target: freeze
`b7241252c2358613d3b22b7d0454d98c56dab373` (F2), carrier `754b62fb6adc60e44e12375af5461a0ebe302994`
(C2), pinned claims blobs `bc2bc360a08baf48…` (`claims.md`) and `db82f98cb7b7b089…` (`claims.json`).
Scratch `S=/fast/scratch/hyaku/chousa-r93/R93CriticClaims`, clone
`git clone --shared /home/vgpnk/Projects/shokunin/chousa-shokunin`, checked out at C2; every command
ran from the clone or a worktree/copy of it. No network, no tool installs, no lane/fleet git
mutation, no production edits; scratch removed before yield. "Observed" below means stdout+exit code
in the receipt named next to it.

## 0. Target bytes, and carrier drift observed during the seat

The assigned C2 claims are quoted from the **pinned blobs** (`git show 754b62fb:… | sha256sum` =
`bc2bc36…` / `db82f98…`), not from the live path. At report time the lane is at
`881a541fc3fcfb8717959a47331720d8ebf6f892` (carrier C5, 2026-11-08 11:25:01 -0300) and the path
`.ufo/waves/round-93/claims.md` hashes `a09f70db…`, i.e. **not** the pinned freeze. The lane added
C3 `d740760e` 11:12:06, F3 `d5c19c54` 11:18:57, C4 `94fbf892` 11:26, F4 `596eabc9` 11:24:24 (message:
"wave findings applied (WSQUOTE witness + named ARITY, tally head scan, range index sets, claims
narrowed)") and C5 `881a541f`; `git diff --stat 754b62fb 881a541f` changes 14 files under
`.ufo/waves/round-93/` + `corpus/evidence/round93/` (claims, claims.json, all three instruments,
forgeries, pins, receipts). This seat attacked the assigned C2 bytes only; the C5 amendments are
**not** verified here. Receipt `R93CriticClaims-lane-drift.txt`.

## 1. Freeze integrity (task 1) — HELD

Command: a scratch re-derivation of every row of `corpus/evidence/round93/instrument-pins.txt`
against `git show F:rel` and `git show C:rel`, plus the minus-self digest by both the disk algorithm
(`pins_file_sha_minus_self`, driver line 155) and the blob algorithm (`self_pin`, lines 366–378).
Receipt `R93CriticClaims-pins-audit.out`.

- 22 rows: 15 instrument/expectation/claims rows (6 r93 scripts, `controls/expected.tsv`,
  `controls/selftest-r93.txt`, `claims.md`, `claims.json`, 5 r89/r90 instruments), 6 receipt rows,
  1 self row. `BAD=0`.
- Every one of the 15 instrument rows matches its blob at F; all 15 are byte-identical at C.
- Every one of the 6 receipt rows matches only its C blob (the F versions pinned the superseded
  `84998563…`); all six C receipts carry `# computed_against=b7241252…`, which is the driver's
  `PIN_OK` leg.
- Self row: stored `2733d572…` = disk-minus-self = blob-C-minus-self; whole-file sha is
  `09e85ae0…` ≠ stored, so the row is the minus-self digest, not a whole-file sha. The F table's own
  self row `f805867c…` equals that file's minus-self digest too.
- No row has a wrong base and none fails to re-derive. The one structural caveat is that the two
  minus-self implementations agree only because the file has no comment/blank lines and ends with the
  self row (disk skips comments/blanks; the blob path hashes every non-self line). Not a defect at C2.
- Stale text only: the driver docstring still says `PINNED_FILES=16/16` (line 12) while the landing
  table is 22 rows; the landed line prints 22/22 (line 509: `RECEIPT PINS OK {checked}/{len(pins)} …`).

**Cited receipts that do not exist in any commit (P1, provenance).** All four are named as
measurement evidence and none is in the C2 tree or in `git log --all -- <path>` (empty; the C tree
`git ls-tree -r` has no `evidence-before/` or `after/` directory):
`corpus/evidence/round93/census-start.txt` (claims.md:6),
`corpus/evidence/round93/evidence-before/c1-prior-accepts.txt` (claims.md:18),
`…/c2-prior-accepts.txt` (claims.md:71), `…/c3-prior-accepts.txt` (claims.md:120),
`corpus/evidence/round93/after/c1-procedure.txt` (driver docstring line 15). Receipt
`R93CriticClaims-lane-drift.txt` (tree listing) and `R93CriticClaims-pins-audit.out`.
Impact: the Before-state of all three claims is asserted "measured in" bytes that were never
carried; only reproduction can ground it (and C1's before does not reproduce, §7/F3).

## 2. Claim values vs counter print statements (task 2)

`claims.md` matches the instruments token-for-token, with one C1 exception (§7/F1–F3). `claims.json`
does not; see §7/F6. The print statements that own each token:

- C1 / `control-driver-r93.py:509` `RECEIPT PINS OK {checked}/{len(pins)}`; `:518`
  `RECEIPT SELF_PIN OK rev={a.rev} receipts_rev={a.receipts_rev or a.rev}`; `:530-533`
  `print(f"COMMITTED_OK={committed_ok}/{len(rows)} EXACT_OK={exact_only}/{len(rows)} "
  f"PIN_OK={pin_ok}/{len(rows)} FRESH_OK={fresh_ok}/{len(rows)} PINNED_FILES={checked}/{len(pins)} "
  f"RECEIPT_PINS={rchecked}/{rtotal} CONTROL_DRIVER_R93={'PASS' if passed else 'FAIL'}")`.
- C1 / `forgeries-r93.py:138` `print(f"FORGERY_REFUSED={refused_n}/2 PRIOR_ACCEPTED={prior_n}/2
  DERIVE_OK={int(derive_ok)}/1 POSITIVE={'pass' if positive else 'fail'}")`.
- C2 / `curation-r93.py:515-525` (`… Q_ROWS=… Q_SHAPE_FAIL=… Q_WSQUOT=… WARRANT_OK=… TFREQ_OK=…
  DUP_QIDS=… LEGS_MEASURED=…`), `:537` (`VERDICT fields_hold=… legs_ok=… DETECTOR_WITNESS=…`),
  `:543` (`CURATION_R93=…`); `curation-controls-r93.py:173` (`CONTROLS=… CARRIED_REFUSED_BOTH=…
  WS_NAMED=… WS_SHAPE_GREEN_R92=… DUPCOUNT_…=… PRIOR_REGRESSION=…`).
- C3 / `skill-tally-r93.py:193-201` (`TALLY_ROWS=… STALE_TALLIES=… … HIST_DERIVED=… HIST_PRESENT=…
  TAIL_TALLIES=… OTHERS_OK=… TAIL_OK=… LEGS=…/4`), `:212`; `skill-tally-r93-controls.py:116-124`
  (`CONTROLS=… OLDPROSE_REFUSED=… PRIOR_ACCEPTED=… STALE_REFUSED_BOTH=… HIST_REFUSED_BOTH=…
  TAIL_REFUSED=…/2 …`).

Token audit receipt `R93CriticClaims-claimsjson-token-check.out`. Results:

| claim | claim source | token | printed? |
|---|---|---|---|
| C2 | claims.json `predicate.controls` | `FORGERY_REFUSED=4/4` | **NO** |
| C2 | claims.json `predicate.controls` | `PRIOR_ACCEPTED=4/4` | **NO** |
| C2 | claims.json `predicate.controls` | `FORGERY_REFUSED=7/7` | yes (regression diagnostic line only) |
| C3 | claims.json `predicate.controls` | `TAIL_REFUSED=1/1` | **NO** (printed `TAIL_REFUSED=2/2`) |
| C1 | claims.md + claims.json | verify fields | yes (`R93CriticClaims-c1-verify.out`) |
| C1 | claims.md + claims.json | forgeries fields | **NO** — command crashes / prints 0/2,0/2,0/1,fail (§7/F1) |

C2's `LEGS_MEASURED=15/15 Q_SHAPE_FAIL=0 Q_WSQUOT=0 Q_ROWS=20 WARRANT_OK=17/17 TFREQ_OK=17/17
DUP_QIDS=0 …` and `DETECTOR_WITNESS=11/11` are exactly printed (`c2-curation.out`);
`CARRIED_REFUSED_BOTH=4/4 WS_NAMED=2/2 WS_SHAPE_GREEN_R92=1/1 DUPCOUNT_1=1/1 PRIOR_REGRESSION=7/7`
is exactly printed (`c2-controls.out`). C3's full line in claims.md:122-124 is exactly printed
(`c3-tally.out`), as is the controls line at claims.md:142-144 (`c3-controls.out`).

## 3. Do-nothing reachability (task 3)

- **C1 — no (as a driver), but the frozen battery is unreachable.** The verify field needs six real
  instrument executions (`FRESH_OK=6/6`), the full 22-row disk walk (`PINNED_FILES=22/22`), and the
  git blob/base walk; a do-nothing print cannot pass `--repo` without the bytes, and the pin walk was
  independently shown to discriminate: on a copy at C2 with one receipt body appended, the tree-only
  r92 driver returns rc 0 `CONTROL_DRIVER_R92=PASS` with `PINNED_FILES=7` while r93 returns rc 1
  `PIN_DISK_MISMATCH … RECEIPT_MISMATCH… SELF_DRIFT … PINNED_FILES=21/22 RECEIPT_PINS=5/6`
  (`R93CriticClaims-c1-r92-treeonly-tampered-receipt.out`, `…-c1-r93-tampered-receipt.out`). The
  second counting command is nevertheless unreachable on this host — see §7/F1.
- **C2 — YES.** A copy of the landed counter with the WSQUOTE population removed
  (`curation-r93.py:326` `ws_quote_rows.append((rel, cells[0]))` → `pass  # STUB`) still prints
  `CURATION_R93=PASS` with `LEGS_MEASURED=15/15 Q_SHAPE_FAIL=0 Q_WSQUOT=0 …` on the clean tree and
  makes the **unmodified** controls battery print the identical claimed line
  `CONTROLS=PASS CARRIED_REFUSED_BOTH=4/4 WS_NAMED=2/2 WS_SHAPE_GREEN_R92=1/1 DUPCOUNT_1=1/1
  PRIOR_REGRESSION=7/7` (rc 0). Only the battery's diagnostic column changes (`ws new=1` → `ws
  new=0`), and `case()` does not test it (`curation-controls-r93.py:107` tests only rc and a
  `LEG_FAIL` needle; the needle `quote=<whitespace>` is matched by the **QSHAPE** leg,
  `curation-r93.py:397-399`, not by the WSQUOTE leg). Receipts `…-c2-stub-counter.out`,
  `…-c2-stub-controls.out`; landed-vs-stub on the same whitespace tree:
  `…-c2-landed-ws-tree.out` (`Q_SHAPE_FAIL=1 Q_WSQUOT=1`, `LEG_FAIL WSQUOTE …`) vs
  `…-c2-stub-ws-tree.out` (`Q_SHAPE_FAIL=1 Q_WSQUOT=0`, both `CURATION_R93=FAIL`).
  Answer to the explicit question: the after-state *naming* (`Q_SHAPE_FAIL=1`, `quote=<whitespace>`,
  rc 1) **is reachable without the new leg** — it is produced by the five-line `q_shape_violation`
  change (`curation-r93.py:229-231` adds `.strip()` and the `quote=<whitespace>` branch); the
  `Q_WSQUOT` field exists only with landed code, but it is the same expression as the shape branch
  (`cells[2].strip().strip('"').strip()`, `:326` vs `:231`) and is gated by nothing.
- **C3 — no.** The tail cases flip the verdict (`deleted-tail`: r92 rc 0 PASS, r93 rc 1 FAIL; `added-tail`:
  r92 rc 0, r93 rc 1 with `HIST_SCOPE_BLEED`), and the ungrounded receipt flips `HIST_DERIVED` 2/2 → 1/2
  (`R93CriticClaims-c3-controls.out`). A stub tail/hist check cannot pass the battery.

## 4. Causal separability (task 4)

- C2 and C3 are each verifiable with C1's instruments absent: with `control-driver-r93.py`,
  `forgeries-r93.py` and `instrument-pins.txt` deleted from an archive tree, `curation-r93.py` prints
  `CURATION_R93=PASS` (rc 0) and `skill-tally-r93.py --selftest …` prints `SKILL_TALLY_R93=PASS`
  (rc 0) — `R93CriticClaims-c2-c1absent.out`, `…-c3-c1absent.out`. Neither counter reads C1 files
  (`grep` for `control-driver|instrument-pins|expected.tsv|receipts` in both: no data reads).
- C1 is **not** separable one-way: its pins table includes C2's and C3's instruments and both claims
  files, so with `curation-r93.py` removed from a C2 worktree the driver prints
  `RECEIPT PINS FINDING PIN_MISSING path=corpus/evidence/round93/curation-r93.py` and
  `PINNED_FILES=21/22 … CONTROL_DRIVER_R93=FAIL` (rc 1) —
  `R93CriticClaims-c1-coupling2-c2absent.out`. This is the pins-table design ("the pins table is the
  population") doing what it says, but C1's named limits do not declare that its PASS is evidence
  about the C2/C3 instrument bytes. Recorded as a tradeoff (F8), not a kill: reverting a sibling
  after landing is exactly what the walk should catch.

## 5. Universal clauses (task 5)

- C1 "every one of its rows is byte-checked on disk" (claims.md:25): the walk enumerates all 22 rows,
  but a self-row mismatch is `INSTRUMENT_PIN_MISMATCH:{rel}` (line 311), not the claimed
  `PIN_DISK_MISMATCH path=<rel>`; the universal is true, the named code is not universal.
  "the sixteen r92-set rows plus one row per committed receipt (six)" (lines 26-27) is 15 named +
  self + 6 = 22; the arithmetic is right only if "r92-set" includes the self row. The Before's "nine
  pinned instruments are never compared" (line 16) is fifteen on the committed 22-row table (22 − 7).
- C2 "all 20 located quotes, the 17 warranted decision rows and the two quote floors" (lines 101-102):
  enumerated by `QID_SETS` (13 + 7), `WARRANT_OK=17/17`, `Q_FLOORS=…=13/13,…,=7/7`; held.
- C3 "all four tallies must hold" (lines 149-150): `TALLY_ROWS=8 STALE_TALLIES=0/8 HIST_PRESENT=2/2
  TAIL_TALLIES=2 TAIL_OK=1 LEGS=4/4`; enumerated; held.
- Round shape (claims.md:164): "One v1 wave of 12 seats (8 attack: 3 reviewer, 1 critic, 1
  mutation-tester, 1 sentinel, 1 revenger, 1 labrun) … one connector seat, three executors, one
  scout, one scribe." The dispatch registry has 12 members and no labrun and no scribe
  (roles: reviewer 3, critic 1, mutation-tester 1, sentinel 1, revenger 1, connector 1, executor 3,
  scout 1); the sentence enumerates 8 + 1 + 3 + 1 + 1 = 14. Band 8–16 is satisfied by 12; the
  composition is not the registry's. Receipt `R93CriticClaims-wave-census.out`. (At C5 the sentence
  is reworded to "8 attack … plus 1 mutation seat counted as attack; 3 executors, 1 scout, 1
  scribe-class connector", which still enumerates 13 against the 12-member registry and invents a
  second mutation seat; F10 remains live at C5.)

## 6. §9 discipline (task 6)

- Predicate frozen before scoring: `claims.md`/`claims.json` blobs are **identical** at `84998563`,
  F2 and C2 (`bc2bc36…`/`db82f98…`, §0). The F2→C2 diff is only the six receipts (regenerated
  against F) and the pins table; the F1→F2 diff is only the `self_pin` parameter plumbing
  (`control-driver-r93.py` 8499 vs F: `self_pin(..., pins)` → `self_pin(..., pins_rows, pins_path)`,
  four hunks, no predicate change). The six C2 receipts all pin F. So no target was narrowed between
  the freeze and the assigned carrier.
- The letter holds; the content did not. Frozen before scoring: (a) the machine form asserts tokens
  no instrument prints (F6), (b) the C1 battery cannot be executed at C2 (F1), (c) all Before
  measurements cite receipts never carried (P1). Freezing early cannot ground those; only measuring
  before the freeze can.
- Post-freeze: the lane's C3–C5 (11:12–11:25) rewrite claims and instruments explicitly from wave
  findings ("claims narrowed", F4). That is outside the assigned C2 attack; noted, not scored.

## 7. Findings

**F1 — C1 fired (K1, K2). The frozen forgeries command does not produce its predicate.**
Claim: "the battery prints `FORGERY_REFUSED=2/2 PRIOR_ACCEPTED=2/2 DERIVE_OK=1/1 POSITIVE=pass` and
exits 0" (claims.md:39-40). Counterexample, exact command in the C2 clone:

```
python3 -B corpus/evidence/round93/forgeries-r93.py --root . --repo . \
  --rev b7241252c2358613d3b22b7d0454d98c56dab373 \
  --receipts-rev 754b62fb6adc60e44e12375af5461a0ebe302994 --work $S/work/forg
```

Observed rc **1**, no summary line, traceback ending
`tarfile.AbsoluteLinkError: '.ufo/waves/round-35/w2/MutGrepShimPath/shims/b/grep' is a link to an
absolute path` (`forgeries-r93.py:51 tf.extractall(dest)` under host Python 3.14.8, whose default
filter is `data`). Receipt `R93CriticClaims-c1-forgeries.out` + `.rc`.
With the extraction filter bypassed in a scratch copy (`filter="tar"`, sha of the copy recorded in
the report index), the same command prints rc 1:
`FORGERY_REFUSED=0/2 PRIOR_ACCEPTED=0/2 DERIVE_OK=0/1 POSITIVE=fail` —
`R93CriticClaims-c1-forgeries-patched.out` + `.rc`. Cause (measured, not inferred): the pristine and
forgery trees are `git archive` extractions with no `.git`, so `c1-gate-r89` and `c1-harm` fail their
fresh legs on every tree (`FRESH_OK=4/6`, `FRESH_EXIT:1`, `FRESH_EXIT:128`) and r93 can never print
`PASS` on the derive/positive trees (`R93CriticClaims-c1-pristine-archive.out`: `FRESH_OK=4/6 …
CONTROL_DRIVER_R93=FAIL`); on the r92 side the battery passes `--repo`, and r92's pins walk compares
the six round-93 receipt rows at `--rev F` where they do not exist as C bytes → SELF_DRIFT → r92
refuses every tree (`PRIOR_ACCEPTED=0/2`; my clean-tree reproduction
`R93CriticClaims-c1-r92-on-r93tree.out` = `RECEIPT PINS OK 7/22 … CONTROL_DRIVER_R92=FAIL`). The r92
acceptance the claim needs exists only in the **tree-only** form on a real clone (no `--repo`):
rc 0, `PINNED_FILES=7 CONTROL_DRIVER_R92=PASS` (`R93CriticClaims-c1-r92-treeonly-clean.out`), and it
survives a tampered receipt (`…-c1-r92-treeonly-tampered-receipt.out`). So K2's "the positive
refused, or the r92 driver refusing both forgeries" is observed, and the frozen command is not the
command that measures the claim.
Smallest safe correction: build fixture trees from a git-bearing source (`git clone --shared` at C,
as my clone/worktree runs did) instead of `git archive`+`extractall`, and run the r92 comparison in
the tree-only form the claim actually relies on; re-emit the six receipts and re-freeze the token
line. This is a battery redesign, not a one-line fix — the frozen C1 claim must be rejected as
written.

**F2 — C1, counter integrity. `FOREGERY_REFUSED` is not a refusal counter.**
`forgeries-r93.py:135` `refused_n = sum(1 for r in results if r)` where `results` stores
`ok = prior and refused` (line 97/100); the observed run refused both forgeries (the per-case lines
carry `PIN_DISK_MISMATCH path=corpus/evidence/round93/curation-controls-r93.py` and
`RECEIPT_MISMATCH:c2-prior-landing`) and still printed `FORGERY_REFUSED=0/2`
(`R93CriticClaims-c1-forgeries-patched.out`). The claim's "the two refusals are …" (claims.md:42-44)
are not what the field counts; it cannot assert a refusal independently of the r92 prior. Smallest
fix: keep two lists (`refused`, `prior`) and print both sums; the claim's `FORGERY_REFUSED=2/2`
cannot be met by a genuine refusal, only by a prior-acceptance pair.

**F3 — C1, Before value. `RECEIPT PINS OK 7/16` is not what the committed fixture set produces.**
Claim: "**Before** (r92 driver … on the round-93 fixture set): `RECEIPT PINS OK 7/16 pinned files
byte-identical`, `PINNED_FILES=7`" (claims.md:15-16). Observed on the committed 22-row table:
`RECEIPT PINS OK 7/22 pinned files byte-identical`, `PINNED_FILES=7` (both the tree-only rc 0 run and
the `--repo` rc 1 run: `R93CriticClaims-c1-r92-treeonly-clean.out`,
`R93CriticClaims-c1-r92-on-r93tree.out`). `7/16` is the r92 table's denominator; the "nine …
never compared" is 22−7 = fifteen here. With its own 16-row table the r92 driver instead reports
`INSTRUMENT_UNPINNED:corpus/evidence/round93/controls/expected.tsv` and `PINNED_FILES=6`
(`R93CriticClaims-c1-r92-owntable.out`), so no r92-table choice reproduces the sentence either.
Smallest fix: quote the measured 7/22, or move the Before to the r92 tree where 7/16 is true and say
so.

**F4 — C2 fired (K4 first clause; do-nothing leg).**
Claim: `WS_NAMED` are "the two whitespace trees (space and tab inside the quotes) that r93 refuses at
the shape leg as `quote=<whitespace>` with `Q_WSQUOT=1` while r92 reports `Q_SHAPE_FAIL=0` on the
same bytes" (claims.md:93-96); "The fifteenth leg is `WSQUOTE`: … counted from the located-quote
population and refused, independently of the cell parser" (claims.md:77-79). Counterexample: the
stub run (§3). The battery's `ok` is rc + needle only (`curation-controls-r93.py:107`), the needle is
the QSHAPE leg's text, and the clean-tree predicate only fixes `Q_WSQUOT=0`; therefore `Q_WSQUOT=1`
is not measured anywhere in the claim's predicate. K4: the population is the same expression as the
shape test's whitespace branch (`:326` vs `:231`) and counts a row `q_shape_violation` already drops
(the claim says so itself), so the leg's verdict force is only `EXPECTED_LEGS` (:98) against literal
deletion, not against a disabled population. Receipts `…-c2-stub-counter.out`,
`…-c2-stub-controls.out`, `…-c2-landed-ws-tree.out`, `…-c2-stub-ws-tree.out`.
Smallest safe correction: make the two ws cases assert `Q_WSQUOT=1` (extend `case()` with an expected
field map and gate `ok` on it), and either derive the population from raw row text (not
`table_cells`' `cells[2]`) or drop the "independently of the cell parser" clause and name the leg as
a second witness whose only force is arity. (C5/F4 already adopts the latter wording; the control
gap — no `Q_WSQUOT=1` assertion — survives the C5 controls diff.)

**F5 — C2, wording. "independently of the cell parser" is false as written.**
The count is `len(cells) == 3 and not cells[2].strip().strip('"').strip()` over `cells` yielded by
`quote_lines` → `table_cells` (`curation-r93.py:322-326`); it is the same parse and the same
expression as `q_shape_violation`'s whitespace branch (`:229-231`). What is independent is the count's
position before the shape `continue`. Evidence: source quote and the stub run. Smallest fix: replace
the clause with "counted before the shape filter, so a reverted shape test cannot silence it".

**F6 — C2/C3, machine form. `claims.json` asserts tokens the landed counters never print.**
C2 `predicate.controls` = `["CONTROLS=PASS","FORGERY_REFUSED=4/4","PRIOR_ACCEPTED=4/4",
"FORGERY_REFUSED=7/7"]`; the controls print `CONTROLS=PASS CARRIED_REFUSED_BOTH=4/4 WS_NAMED=2/2
WS_SHAPE_GREEN_R92=1/1 DUPCOUNT_1=1/1 PRIOR_REGRESSION=7/7`
(`curation-controls-r93.py:173`), and `FORGERY_REFUSED=7/7` only inside the regression diagnostic
line; `FORGERY_REFUSED=4/4` and `PRIOR_ACCEPTED=4/4` occur nowhere. C3 `predicate.controls` contains
`TAIL_REFUSED=1/1`; the controls print `TAIL_REFUSED=…/2` (`skill-tally-r93-controls.py:121`), 2/2 on
the clean tree. Both blobs are pinned rows and unchanged since 8499. Receipt
`R93CriticClaims-claimsjson-token-check.out`. Impacted: C2, C3, freeze integrity (a gate that reads
the machine form fails on correct output). Smallest fix: regenerate `claims.json` from the printed
field lists at freeze time. (C5 replaces both token lists with the instrument vocabulary; the defect
is closed only after the assigned freeze.)

**F7 — P1, provenance. Four cited measurement receipts were never carried.**
See §1. Impacted: all three claims (Before) and the round's census sentence. Smallest fix: commit the
captured stdout under the cited paths in the freeze commit and add them to the pins table (or cite
nothing and re-measure in the counting command).

**F8 — coupling tradeoff (not a kill).** C1's PASS is a function of C2/C3 instrument bytes (§4).
Smallest correction: name it in C1's named limits ("the pin walk includes the sibling instruments, so
C1's fields are also evidence about their bytes") — or accept the coupling as the pins-table design.

**F9 — C3 held.** `SKILL_TALLY_R93=PASS` with every claims.md:122-124 and :142-144 token observed;
the two HIST quotes are present (round25 line 53 `…PASS (161 cases, 0 skipped)`, round34 line 5
`…PASS (256 cases, 0 skipped)`); the deleted-tail/added-tail/ungrounded cases change the verdict;
C3 is separable from C1. The only C3 defect is the machine-form token (F6).

**F10 — sizing, minor.** §5's Round shape: 12 declared, 14 enumerated, registry 12 with no labrun
and no scribe. Band satisfied. Smallest fix: freeze the registry census, not a role plan.

## 8. Receipts (copied into this folder, prefix `R93CriticClaims-`)

`pins-audit.out`; `c1-verify.out/.rc`; `c1-verify-status.txt`; `c1-forgeries.out/.rc`;
`c1-forgeries-patched.out/.rc`; `c1-pristine-archive.out/.rc`; `c1-r92-on-r93tree.out/.rc`;
`c1-r92-owntable.out/.rc`; `c1-r92-treeonly-clean.out/.rc`; `c1-r92-treeonly-tampered-receipt.out/.rc`;
`c1-r93-tampered-receipt.out`; `c1-coupling2-c2absent.out/.rc`; `c2-curation.out/.rc`;
`c2-controls.out/.rc`; `c2-stub-counter.out/.rc`; `c2-stub-controls.out/.rc`;
`c2-landed-ws-tree.out`; `c2-stub-ws-tree.out`; `c2-c1absent.out`; `c3-tally.out/.rc`;
`c3-controls.out/.rc`; `c3-c1absent.out`; `claimsjson-token-check.out`; `wave-census.out`;
`lane-drift.txt`.

Scratch note: the patched forgeries copy (one line: `tf.extractall(dest, filter="tar")`) and the
stubbed curation copy (one line: `ws_quote_rows.append(...)` → `pass`) lived only under
`S/patch1`, `S/patch2`; they were derived from the C2 blobs, not edited into the lane or the clone,
and are removed with `S`.

Report: `.ufo/waves/round-93/w1/R93CriticClaims.md`

VERDICT: R93CriticClaims C1 fired — the frozen verify command prints the claimed line (rc 0), but the frozen forgeries command crashes on the host Python 3.14.8 and, with that bypassed, prints FORGERY_REFUSED=0/2 PRIOR_ACCEPTED=0/2 DERIVE_OK=0/1 POSITIVE=fail (rc 1) because the archive trees lack .git and the r92 side is run with --repo; the claimed before-receipt is not committed and 7/16 is 7/22 on this fixture set.
VERDICT: R93CriticClaims C2 fired — the counter and controls print the claimed lines, but a copy with the WSQUOTE population stubbed to a no-op still prints CURATION_R93=PASS and the byte-identical CONTROLS line, so the claim's distinguishing Q_WSQUOT=1 is gated nowhere; "independently of the cell parser" is false, and claims.json asserts two control tokens the instrument never prints.
VERDICT: R93CriticClaims C3 held — the tally counter and controls print every claims.md token, the deleted-tail/added-tail/ungrounded cases flip the verdict, and C3 is separable from C1; the only C3 defect is the pinned machine form's unprinted TAIL_REFUSED=1/1 (recorded as F6).
