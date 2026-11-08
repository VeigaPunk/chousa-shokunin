# R89MutBattery — round-89 mutation probe (C1 operability, C2 calibration)

Seat `R89MutBattery`, lane chousa, round 89, leaf. No subagents, no network, no tool installs, no
production edits, no lane/fleet git or jj mutation. Every tree, mutant copy and work dir lived under
`/fast/scratch/hyaku/chousa-r89/R89MutBattery/` and was deleted after the receipts were copied here.

Trees (both built with `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive <rev> | tar -x -C <dir>`):

| tree | revision | role |
|---|---|---|
| `tree-land` | `ac0a0892c15de11fb28d3208f2b287687c00477e` | the freeze/landing bytes: counter mutants run here |
| `tree-base` | `f8fa55ec94cb34e7b572a9d87d7f62d88bc80bf8` | prior-round bytes: the base tool for the harm sweep |

`corpus/evidence/round89/gate-records-r89.py` and the rest of `instrument-pins.txt` hash to the pinned
values in both the extracted landing tree and the live lane worktree (`PIN_MISMATCH=0`); the subject
tool is `905f9da2fdf233b3a599f079a4c40ace730e3acf5464a2b80e1f93a616242d60` at **both** revisions
(`receipts/00-commands-and-integrity.txt`).

## Detectors and classification

The detector for each counter is the counter's own frozen predicate, read from the seat tasking
(which is a superset of the machine form in `.ufo/waves/round-89/claims.json`):

* **C1** — exit 0, `GATE_RECORDS_R89=PASS`, `LEG_REREAD=16/16 RECONCILED=16/16 CROSSCHECK=15/15
  LEGS_APPENDED=16`, `POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=362/362 EXPECTED_CODE=362/362
  D1_REFUSED=3/3 D2_REFUSED=3/3 MUT_ADMIT_KILLED=1 MUT_UNREACH_KILLED=1 DERIVE_NEG=1`; plus the
  counting command's `mutate-r89.py` line `MUTANTS_KILLED=11/11 TOOL_MUTANTS_CAUGHT=2/2 TOTAL=13/13`
  and `harm-recheck.py` `moved=0`.
* **C2** — exit 0, `CURATION_R89=PASS`, `DUP_QIDS=0 WARRANT_OK=17/17 QUOTES_LOCATED=20/20
  TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 SUP_CLAUSE_CHECKED=0 SUP_UNRESOLVED=0`; the control battery
  `CONTROLS=PASS FORGERY_REFUSED=7/7 PRIOR_ACCEPTED_FORGERY=7/7`; the mutant battery
  `MUTANTS_KILLED=6/6 COUNTER_DETECTED=5 BATTERY_DETECTED=1`.

Classification used below:

* **KILLED** — the detector exits non-zero or a required token is absent.
* **SURVIVOR** — the detector exits 0 with every required token present.
* **SURVIVOR (equivalent)** — a survivor whose printed output is byte-identical to the unmutated
  counter on the same input; the probe that distinguishes it is named.

Every survivor is an edit to an instrument whose bytes are pinned by `instrument-pins.txt`. The pins,
not the counter logic, are the landing-time guard against a rewritten instrument; the mutation probe
measures whether the logic would notice the rewrite if the pin were bypassed. This is the same framing
the frozen claims use for their named limits.

## Baselines (both trees, exit codes observed)

| run | command | observed | rc | receipt |
|---|---|---|---|---|
| C1 counter, live tree | `python3 -B corpus/evidence/round89/gate-records-r89.py --root <lane> --repo <lane> --work <scratch>` | `LEG_REREAD=16/16 RECONCILED=16/16 CROSSCHECK=15/15 LEGS_APPENDED=16` / `GATE_RECORDS_R89=PASS` | 0 | `receipts/00-commands-and-integrity.txt` |
| C1 counter, extraction | same with `--root tree-land` | identical | 0 | `receipts/c1-01-baseline.txt` |
| C1 mutants, live+extraction | `mutate-r89.py --root <tree> --repo <lane> --work <scratch>` | `MUTANTS_KILLED=11/11 TOOL_MUTANTS_CAUGHT=2/2 EQUIVALENT_ON_TREE=0/0 TOTAL=13/13` | 0 | `receipts/c1-01-baseline.txt` |
| C1 harm, live tree | `harm-recheck.py --root <lane> --repo <lane> --base-tool <scratch>/base-tool.py` | `HARM_RECHECK files=14 records=31 moved=0 base_rc=0 r88_rc=0` | 0 | `receipts/c1-05-harm.txt` |
| C1 harm, extraction | same with `--root tree-land` | `HARM_RECHECK files=13 records=29 moved=0 base_rc=0 r88_rc=0` | 0 | `receipts/00-commands-and-integrity.txt` |
| C2 counter | `curation-r89.py --root tree-land` | `CURATION_R89=PASS`, all fields above; `LEGS_MEASURED=8/8` | 0 | `receipts/c2-01-baseline.txt` |
| C2 controls | `curation-r89-controls.py --root tree-land --work <scratch>` | `CONTROLS=PASS FORGERY_REFUSED=7/7 PRIOR_ACCEPTED_FORGERY=7/7` | 0 | `receipts/c2-01-baseline.txt` |
| C2 mutants | `curation-r89-mutants.py --root tree-land --work <scratch>` | `MUTANTS_KILLED=6/6 COUNTER_DETECTED=5 BATTERY_DETECTED=1` | 0 | `receipts/c2-01-baseline.txt` |

The live tree carries one extra lesson (`corpus/lessons/round-89.md`, untracked) so its harm sweep sees
14 files/31 records; the landing commit extraction sees 13/29. Both print `moved=0`. The extraction is
the authoritative revision tree for every mutation run below.

---

# C1 — `C1-BATTERY-R89` (operability)

## New counter mutants (9; six are one-point)

Command shape: `python3 -B out/c1/<id>/gate-records-r89.py --root tree-land --repo <lane> --work out/c1/<id>/w`.
Receipt: `receipts/c1-02-new-mutants.txt`.

| id | edits | rc | printed | frozen fields | committed `mutate-r89` against it | result |
|---|---|---|---|---|---|---|
| `C1-N01-credit-mutants` | 1 | 0 | `PASS` | all present | rc 0, 11/11, 2/2 | **SURVIVOR** |
| `C1-N02-reconcile-taut-E7b` | 4 | 0 | `PASS` | `MUT_ADMIT_KILLED=1`/`MUT_UNREACH_KILLED=1` absent (prints 0) | rc 2, `SETUP_MISS M2-credit-mutant` | instrument-level survivor; killed by the field pin |
| `C1-N03-coherent-width-forgery` | 4 | 0 | `PASS` | all present, output identical to baseline | rc 2, `SETUP_MISS E7c-width-detached` | **SURVIVOR of the counter**; refused only by the driver's anchor tripwire |
| `C1-N04-crosscheck-div3-dropped` | 4 | 0 | `PASS` with `DIV3=1` beside `3/3/3` legs | all present | rc 2, `SETUP_MISS E7c-width-detached` | **SURVIVOR of the counter**; driver tripwire only |
| `C1-N05-tool-witness` | 1 | 0 | `PASS` | all present | rc 0, 11/11 | **SURVIVOR (equivalent)**; dies on the tool-absent probe |
| `C1-N06-positive-set-narrowed` | 1 | 0 | `PASS` with `POSITIVE=1/1 FORGED_REFUSED=92/92` | `POSITIVE=15/15`, `FORGED_REFUSED=362/362`, `EXPECTED_CODE=362/362` absent | rc 0, 11/11 | instrument-level survivor; killed by the field pin |
| `C1-N07-expected-legs-15` | 1 | 1 | `FAIL`, `UNRECONCILED SUMMARY detail=15/15 receipt_ok=False rederived=True`, `LEG_FAIL SUMMARY 15/15` | — | — | KILLED |
| `C1-N08-rows-203-two` | 1 | 1 | `FAIL`, `LEG_FAIL D1_WIDTH 3/3/3 pin2` / `D2_WIDTH 3/3/3 pin2` | — | — | KILLED |
| `C1-N09-fresh-limit-one` | 1 | 1 | `FAIL`, `LEG_FAIL FRESH 4/5` | — | — | KILLED |

`C1-N01` is the one anchor edit that credits both admit-mutant fields and disables the build/run:

```text
            if files:
                ma = os.path.join(tmp, "tool-MUT-ADMIT.py")
                mut_admit_derived = mut_admit_killed = 1
                if False:
                    mut_admit_derived = 1
```

The counter prints `MUT_ADMIT_DERIVED=1 MUT_ADMIT_KILLED=1 … GATE_RECORDS_R89=PASS`, and the committed
`mutate-r89.py` still reports `MUTANTS_KILLED=11/11 TOOL_MUTANTS_CAUGHT=2/2` — the credited half of
`TOOL_MUTANTS_CAUGHT=2/2` is never built or run (`receipts/c1-04-tool-absent-and-second-detector.txt`).

## Named-limit attacks

| limit (claims.md) | probe | survives? | plain statement |
|---|---|---|---|
| 1. joint rewrite of writer+receipts+reconciliation / coherent detail+ok forgery | `C1-N03` (measurement `div3=1`, forged `3/3/3 pin3` detail, forged `D1_EXPECTED/DIV3` summary) | **yes** | The counter's own predicate passes with output identical to the honest baseline. Only `mutate-r89.py`'s anchor (`SETUP_MISS`, rc 2) refuses it — not a behavioural leg. This is the disclosed boundary. |
| 1 (narrower boundary) | `C1-N04` (`E7d` detail forgery + delete `and _ints("DIV3") == [c]` from `crosscheck`) | **yes** | The summary prints `DIV3=1` beside `3/3/3` legs and still PASSes. The claim's "forging that too is a joint rewrite" understates the boundary: removing one comparison is enough, and `DIV3` is not in the frozen field set. |
| 2. `TOOL` has no numeric witness | `C1-N05` (`("TOOL", os.path.isfile(tool), …)` → `True`) | **bounded** | Survives while the tool exists (extensionally identical). On `--tool <nonexistent>` the honest counter prints `LEG_REREAD=0/2 … FAIL`; the mutant prints `UNRECONCILED TOOL detail=tool present receipt_ok=True rederived=False` / `LEG_REREAD=1/2 … FAIL`. The filesystem witness does bound it. |
| 3. reconciliation is agreement, not truth | `C1-N02`, `C1-N06` | **yes, internally** | Both print `PASS`; only the *reader's* field equality (`MUT_*_KILLED=1`, `POSITIVE=15/15`, `FORGED_REFUSED=362/362`) refuses them. The instrument does not. |

## Subject-tool mutants (beyond the committed two)

Command shape: pristine counter with `--tool out/c1/tools/<id>/gate-records.py`; receipt
`receipts/c1-03-tool-mutants.txt`.

| id | mutation | observed | rc | result |
|---|---|---|---|---|
| `T-a-unreach-eq-203` | `success = … 200 <= int(kv["http"]) < 300` → `… kv["http"] == "203"` | `LEG_FAIL MUT_UNREACH derived=0 killed=0` | 1 | CAUGHT, but **only because the literal is gone** (`derived=0`); no behavioural class sees the narrowed rule |
| `T-a2-unreach-eq-203-literal-kept` | same rule with the literal kept: `… < 300 and kv["http"] == "203"` | `GATE_RECORDS_R89=PASS`, all fields | 0 | **UNCAUGHT** |
| `T-b-admit-int-300` | `r[6] == "200"` → `int(r[6]) < 300` | `LEG_FAIL FORGED 359/362`, `LEG_FAIL D1_REFUSED 0/3`, `MUT_ADMIT derived=0 killed=0` | 1 | CAUGHT (behaviour + derivation) |
| `T-b2-admit-int-300-literal-kept` | `(r[6] == "200" or int(r[6]) < 300)` | `LEG_FAIL FORGED 359/362`, `LEG_FAIL D1_REFUSED 0/3` | 1 | CAUGHT behaviourally (D1 class) |
| `T-c-git-blob-empty` | `git_blob` returns `b""` | `LEG_FAIL POSITIVE 11/15`, `LEG_FAIL FRESH 3/5`, `LEG_FAIL RC 2/4` | 1 | CAUGHT (rev positives and fresh revs) |

Record-level witness for `T-a`/`T-a2`, built from the committed S082 refetch row
(`curl_rc=0, http=200`, `tier=A`):

```text
GATE-RECORD S082 url=https://raw.githubusercontent.com/MichSchli/AVeriTeC/main/README.md \
  fetched=2026-10-27T08:04:52Z tier=A decision=reject capture=none curl_rc=0 http=200 words=0 quote=none
```

* pristine tool: `GATE_RECORD .../d2-200.md:1 S082 FAIL REFETCH`, rc 1
* `T-a`: `... S082 OK`, rc 0
* `T-a2`: `... S082 OK`, rc 0

So the narrowed unreach rule is wrong on committed bytes, not only on an unreachable hypothetical.
The counter's D2 class is built only from `_qualifying_203` (`build_d2_203_rejects` consumes
`_qualifying_203`, source lines 268/367), so it never builds the S082 200-row reject that
distinguishes the mutant; the battery has no non-203 2xx class at all. The claim's "203 binding and
unreach repair stand unmodified" is true of the landed tool, but it is not witnessed by a non-203 2xx
class in the battery.

## Survivor analysis (c)

### S1 — `C1-N01-credit-mutants` (SURVIVOR of the full C1 predicate)

* Command: `python3 -B out/c1/C1-N01-credit-mutants/gate-records-r89.py --root tree-land --repo <lane> --work out/c1/C1-N01-credit-mutants/w`
* Receipt: `receipts/c1-02-new-mutants.txt`; second detector `receipts/c1-04-tool-absent-and-second-detector.txt`.
* Observed: `MUT_ADMIT_DERIVED=1 MUT_ADMIT_KILLED=1 … GATE_RECORDS_R89=PASS`, rc 0; committed driver rc 0,
  `MUTANTS_KILLED=11/11 TOOL_MUTANTS_CAUGHT=2/2`.
* Leg that should have killed it: `MUT_ADMIT` (and `MUT_UNREACH`). It **exists**; its `ok` is
  `mut_admit_derived == 1 and mut_admit_killed == 1`, and both fields are exactly what the mutant
  credits. The reconciliation re-derives the same fields; the summary re-prints the same fields. No leg
  asserts that `tool-MUT-ADMIT.py` exists or that a subprocess ran.
* Leg-failing probe: the committed `E7b-mutant-detached` mutant (same shape with the fields left at 0)
  is refused: `UNRECONCILED MUT_ADMIT detail=derived=0 killed=0 receipt_ok=True rederived=False`
  (`receipts/c1-01-baseline.txt`). The leg is live; it simply has no independent witness.

### S2 — `C1-N03-coherent-width-forgery` (SURVIVOR of the counter's own predicate)

* Command: `python3 -B out/c1/C1-N03-coherent-width-forgery/gate-records-r89.py --root tree-land --repo <lane> --work …`
* Receipt: `receipts/c1-02-new-mutants.txt`; second detector `receipts/c1-04-tool-absent-and-second-detector.txt`.
* Observed: rc 0, `GATE_RECORDS_R89=PASS`, every frozen token present, output identical to the
  baseline. `mutate-r89.py` with this counter: rc 2, `SETUP_MISS E7c-width-detached: anchor not found`.
* Legs that should have killed it: `D1_WIDTH`/`D2_WIDTH` and the `CROSSCHECK` cell. Both **exist** and
  both fail on isolated probes:
  * `P1-width-leg` (`div3 = 1`, detail honest): `LEG_FAIL D1_WIDTH 3/3/1 pin3`, `LEG_FAIL D2_WIDTH 3/3/1 pin3`, rc 1.
  * `P2-crosscheck-leg` (`D1_EXPECTED + 1` in the summary only): `UNCROSSCHECKED D1_WIDTH detail=3/3/3 pin3 D1_FORGES=3 D1_EXPECTED=4 DIV3=3 pin=3/3`, rc 1.
  * Receipt: `receipts/c1-02-new-mutants.txt`.
* The mutant defeats them by rewriting the measurement (`div3=1`), the leg detail/`ok`, and the
  summary together, which is the claim's named limit 1.

### S3 — `C1-N04-crosscheck-div3-dropped` (SURVIVOR of the counter's own predicate)

* Same command shape; receipt `receipts/c1-02-new-mutants.txt`.
* Observed: rc 0, `GATE_RECORDS_R89=PASS`, summary `DIV3=1` beside `3/3/3 pin3` details.
* Leg that should have killed it: the `CROSSCHECK` `DIV3` comparison at source line 667. It
  **exists** (`P2` proves it fires when a summary field is displaced) but the mutant deletes exactly
  that comparison; `mutate-r89.py` then exits 2 with `SETUP_MISS E7c-width-detached` because the
  `D1_WIDTH` anchor is gone. No behavioural leg refuses it.
* Because `DIV3` is not in the frozen field set, the claim's own predicate also cannot see it.

### S4 — `C1-N05-tool-witness` (SURVIVOR, equivalent while the tool exists)

* Command: `out/c1/C1-N05-tool-witness/gate-records-r89.py --root tree-land --repo <lane> --tool <nonexistent> --work …`
* Receipt: `receipts/c1-04-tool-absent-and-second-detector.txt`.
* Observed on the landing tree: rc 0, all tokens; the committed driver rc 0, 11/11.
* Observed on the tool-absent tree: honest `LEG_REREAD=0/2 … GATE_RECORDS_R89=FAIL`; mutant
  `UNRECONCILED TOOL detail=tool present receipt_ok=True rederived=False` / `LEG_REREAD=1/2 … FAIL`, rc 1.
* Leg that should have killed it: `TOOL`/`rederive("TOOL", …)`. It **exists** and fails on the
  tool-absent probe. The mutation is extensionally identical wherever the tool exists — the named
  limit 2, bounded as the claim says.

### S5 — `C1-N06-positive-set-narrowed` (instrument-level SURVIVOR)

* Command: `out/c1/C1-N06-positive-set-narrowed/gate-records-r89.py --root tree-land --repo <lane> --work …`
* Receipt: `receipts/c1-02-new-mutants.txt`.
* Observed: rc 0, `POSITIVE=1/1 FRESH_POSITIVE=5/5 FORGED_REFUSED=92/92 EXPECTED_CODE=92/92 … GATE_RECORDS_R89=PASS`;
  the committed driver rc 0, 11/11.
* Leg that should have killed it: `POSITIVE` exists and fails when a positive is refused (`T-c` prints
  `LEG_FAIL POSITIVE 11/15`), but it cannot see a smaller honest set. The count pin lives in the claim
  (`POSITIVE=15/15`, `FORGED_REFUSED=362/362`) and in `controls/expected.tsv`, not in the counter.
  Named limit 3.

### S6 — `C1-N02-reconcile-taut-E7b` (instrument-level survivor)

* Command: `out/c1/C1-N02-reconcile-taut-E7b/gate-records-r89.py --root tree-land --repo <lane> --work …`
* Receipt: `receipts/c1-02-new-mutants.txt`.
* Observed: rc 0, `MUT_ADMIT_DERIVED=0 MUT_ADMIT_KILLED=0 MUT_UNREACH_DERIVED=0 MUT_UNREACH_KILLED=0 … GATE_RECORDS_R89=PASS`
  (0 occurrences of the required `…_KILLED=1` tokens). The reconciliation tautology counts the
  rederived-false values as reconciled and the crosscheck agrees with the zeroed measurements.
* Leg that should have killed it: the reconciliation and the `MUT_*` legs; both exist and both fail on
  the committed `E7b` shape (`UNRECONCILED MUT_ADMIT …`, `receipts/c1-01-baseline.txt`). The frozen
  field equality is the remaining guard.

---

# C2 — `C2-CURATION-R89` (calibration)

## Probe trees (honest counter; each shows the leg that detects the shape)

Command: `python3 -B tree-land/corpus/evidence/round89/curation-r89.py --root out/c2/trees/<kind>`.
Receipt: `receipts/c2-02-probe-trees.txt`.

| tree | shape | observed honest line | rc |
|---|---|---|---|
| `dup` | `Q1, Q1` warrant | `LEG_FAIL DUPQID … warrant=Q1, Q1 (S215)` | 1 |
| `sup` | S031 contrast+`publication`, mined S219 superseder | `TEACHES_SUP_UNRESOLVED S031 terms=publication` / `LEG_FAIL TEACHES … sup_unresolved=1` | 1 |
| `s031` | S031 `mined`→`queued` | `LEG_FAIL TEACHES … unresolved=1` | 1 |
| `f2` | S031 `mined`→`rejected` | `LEG_FAIL TEACHES … unresolved=1` | 1 |
| `a1c` | Q11 deleted, one-word `Q99` | `LEG_FAIL FLOOR` | 1 |
| `a1d` | Q11 → `"range"` | `LEG_FAIL FLOOR` | 1 |
| `caseg` | Q10 deleted, Q13 duplicated as Q14 | `LEG_FAIL FLOOR` | 1 |
| `b1b` | `Q1, Q3` padding qid | `WARRANT_UNLINKED … resolved=2/2` / `LEG_FAIL WARRANT 16/17` | 1 |
| `nv` | Q2 paraphrase (not verbatim) | `QUOTES_LOCATED=19/20` / `LEG_FAIL FLOOR` + `LEG_FAIL WARRANT 16/17` | 1 |
| `unentailed` | decision cell carries `modified`, no located quote does | `UNENTAILED_TERM=1` / `LEG_FAIL UNENTAILED … term=modified` | 1 |
| `sub6` | Q2 six-token verbatim suffix | `LEG_FAIL FLOOR` (warrant 17/17) | 1 |
| `swap` | Q10/Q11 quote texts exchanged | `CURATION_R89=PASS`, all fields | 0 |
| `sub7` | Q1 eight-token verbatim prefix | `CURATION_R89=PASS`, all fields | 0 |
| `reorder` | two Decision-table rows swapped | `CURATION_R89=PASS`, all fields | 0 |

## Named-limit attacks (input side)

| limit | probe | survives? | plain statement |
|---|---|---|---|
| 1. `MIN_TOKENS=7` is a floor, not a content check | `sub7` (8-token verbatim prefix) and `sub6` (6-token verbatim suffix) | **yes at 8, no at 6** | 8 tokens PASS; 6 tokens FAIL on FLOOR alone (warrant 17/17). The floor is exactly 7 and content-blind, as disclosed. |
| 1 (constant moved) | `C2-N2` (`MIN_TOKENS = 1`) | **silent on landing** | On the landing tree the mutant's output is identical to the baseline; only the `a1d` tree (and the battery's A1d case) distinguishes it. A frozen measured constant has no self-check in the counter; `instrument-pins.txt` is the guard. |
| 2. qid-set pin guards label identity, not content | `swap` (Q10/Q11 texts exchanged) | **yes** | All 13 r84 quotes still located, set pinned, `WARRANT_OK=17/17`, rc 0. Disclosed. |
| 3. row reorder | `reorder` | **yes (benign)** | rc 0, all fields. Disclosed. |
| 4. superseder clause vacuous on the real registry, non-vacuity via the battery mirror | landing `SUP_CLAUSE_CHECKED=0`; `sup` mirror; `C2-N6` | **confirmed** | The mirror fires `sup_unresolved=1` (rc 1). A counter edit that kills the clause and detaches the leg (`C2-N6`) accepts the mirror; the control battery then refuses it (`CASE_DEVIATION SUP-clause-mirror`, `FORGERY_REFUSED=6/7`, rc 1). The battery is load-bearing for the clause. |

## New counter mutants (9; six are one-point)

Command: `python3 -B out/c2/<id>/curation-r89.py --root out/c2/trees/<tree>`; second detector
`python3 -B tree-land/.../curation-r89-controls.py --root <lane> --work <dir> --counter out/c2/<id>/curation-r89.py`.
Receipt: `receipts/c2-03-new-mutants.txt`.

| id | tree | edits | counter | battery | result |
|---|---|---|---|---|---|
| `C2-N1-set-pin-removed` | `caseg` | 2 | PASS | rc 1, `CASE_DEVIATION caseG-relabel`, `FORGERY_REFUSED=6/7` | killed by the battery |
| `C2-N2-min-tokens-one` | `a1d` | 1 | PASS | rc 1, `CASE_DEVIATION A1d-truncate`, `6/7` | killed by the battery; silent on landing |
| `C2-N3-warrant-shares-true` | `b1b` | 1 | PASS | rc 1, `CASE_DEVIATION B1b-padding-qid`, `6/7` | killed by the battery |
| `C2-N4-dup-detection-deleted` | `dup` | 1 | PASS | rc 1, `CASE_DEVIATION D1-duplicate-qid`, `6/7` | killed by the battery |
| `C2-N5-teaches-unresolved-off` | `s031` | 2 | PASS with `TEACHES_UNRESOLVED=1` | rc 1, `CASE_DEVIATION F2-rejected-superseder`, `6/7` | killed by the battery and the field pin |
| `C2-N6-sup-clause-dead` | `sup` | 2 | PASS with `SUP_UNRESOLVED=0` (honest 1) | rc 1, `CASE_DEVIATION SUP-clause-mirror`, `6/7` | killed by the battery |
| `C2-N7-quote-locate-relaxed` | `nv` | 1 | PASS, `QUOTES_LOCATED=20/20 WARRANT_OK=17/17` | rc 0, `CONTROLS=PASS 7/7` | **SURVIVOR (all three detectors)** |
| `C2-N8-def-constant-moved` | `base` | 1 | FAIL, `LEG_FAIL DEF_CITED 0` | n/a | KILLED |
| `C2-N9-unentailed-off` | `unentailed` | 1 | PASS with `UNENTAILED_TERM=0` (honest 1) | rc 0, `CONTROLS=PASS 7/7` | **SURVIVOR (all three detectors)** |

`C2-N7` is one expression (source line 195):
`if cap is not None and norm(quote) in cap:` → `if cap is not None:`.

`C2-N9` is one expression (source line 206):
`for term in DEFECT_TERMS:` / `if term in … and term not in joined:` → `if False:`.

## Survivor analysis (c)

### S7 — `C2-N7-quote-locate-relaxed` (SURVIVOR of all three detectors)

* Commands and receipts (`receipts/c2-06-N7-all-detectors.txt`):
  * counter on the `nv` tree: rc 0, `CURATION_R89=PASS`, `QUOTES_LOCATED=20/20 WARRANT_OK=17/17`.
  * control battery with `--counter <mutant>`: rc 0, `CONTROLS=PASS FORGERY_REFUSED=7/7 PRIOR_ACCEPTED_FORGERY=7/7`.
  * committed `curation-r89-mutants.py` with the mutant counter: rc 0, `MUTANTS_KILLED=6/6 COUNTER_DETECTED=5 BATTERY_DETECTED=1`.
* Leg that should have killed it: the `FLOOR` leg's located-count (`loc == tot`) and the `WARRANT`
  resolution. Both **exist** and the honest counter fails on the same tree:
  `QUOTES_LOCATED=19/20` / `WARRANT_UNLINKED … Q2 (S214) resolved=0/1` / `LEG_FAIL FLOOR` /
  `LEG_FAIL WARRANT 16/17`, rc 1 (`receipts/c2-02-probe-trees.txt`).
* After the edit, the paraphrase is stored as located (`quotes[qid] = norm(quote)`), the warrant
  resolves, and every printed field matches the landing values. Neither battery contains a
  non-verbatim quotation case, so nothing else notices. This is the strongest C2 coverage finding:
  K2's "a quote counted as located is not verbatim" has a single-expression guard.

### S8 — `C2-N9-unentailed-off` (SURVIVOR of all three detectors)

* Commands and receipts (`receipts/c2-07-N9-all-detectors.txt`):
  * honest counter on `unentailed`: rc 1, `UNENTAILED_TERM=1`, `LEG_FAIL UNENTAILED … term=modified`, `CURATION_R89=FAIL`.
  * mutant counter on `unentailed`: rc 0, `UNENTAILED_TERM=0`, `CURATION_R89=PASS`.
  * control battery with `--counter`: rc 0, `CONTROLS=PASS 7/7`.
  * committed mutant battery with the mutant counter: rc 0, `MUTANTS_KILLED=6/6`.
* Leg that should have killed it: `UNENTAILED` (source line 272) and the `fields_hold` conjunct
  `len(unentailed) == 0`. Both **exist** and the honest counter fails on the probe tree.
* The printed field `UNENTAILED_TERM` is **not** in the frozen C2 predicate and no battery case
  populates it, so the detector cannot see the dead leg. This is a K4 "dead detector" shape for a
  leg outside the claimed field set.

## Predicate observability (C2) — finding, not a survivor

`receipts/c2-05-predicate-observability.txt`:

* On a PASS run the counter prints **zero** occurrences of `VERDICT`. The VERDICT leg's detail is
  printed only when the leg fails, and then as `LEG_FAIL VERDICT fields_hold=0 legs_ok=…` (observed on
  every probe tree); the passing value `VERDICT fields_hold=1 legs_ok=8/8` never appears in stdout.
* `LEGS_MEASURED=8/8` is printed before the ninth (`VERDICT`) leg is appended; the internal `passed`
  requires `len(legs) == 9`. Thus "nine legs" is true of the accounting but the only printed leg count
  says 8/8.
* `claims.json` `C2.predicate.counter_fields` lists six fields and omits `SUP_CLAUSE_CHECKED` and the
  verdict token; `claims.md` and the seat tasking require both; `controls/expected.tsv`'s `c2-landing`
  row also omits them. The substantive property holds (the verdict is `fields_hold`; `C2-N5`/`M2`/`M3`
  show it gates PASS), but the frozen prose token `VERDICT fields_hold=1` cannot be read from stdout.

---

# Findings (ranked)

Every finding names the command, the receipt and the observed line/exit code.

**F1 — C1: the tool-mutant ledger has no independent witness; a one-anchor edit credits it and the
full C1 predicate still passes.**
`python3 -B out/c1/C1-N01-credit-mutants/gate-records-r89.py --root tree-land --repo <lane> --work …`
→ rc 0, `MUT_ADMIT_DERIVED=1 MUT_ADMIT_KILLED=1 … GATE_RECORDS_R89=PASS`; and
`python3 -B out/c1/C1-N01-credit-mutants/mutate-r89.py --root tree-land --repo <lane> --work …`
→ rc 0, `MUTANTS_KILLED=11/11 TOOL_MUTANTS_CAUGHT=2/2 EQUIVALENT_ON_TREE=0/0 TOTAL=13/13`.
Receipts: `receipts/c1-02-new-mutants.txt`, `receipts/c1-04-tool-absent-and-second-detector.txt`.
`TOOL_MUTANTS_CAUGHT=2/2` is only as strong as the counter that reports it; a check that
`tool-MUT-ADMIT.py` exists (or a subprocess count) would close it.

**F2 — C1: `unreach` narrowed to exactly `http == "203"` with the derivation literal kept is caught
by no leg, and the mutated tool accepts a reject record over a committed 200 row.**
`... --tool out/c1/tools/T-a2-unreach-eq-203-literal-kept/gate-records.py ...` → rc 0,
`GATE_RECORDS_R89=PASS`, all fields. Record-level: the pristine tool prints
`GATE_RECORD .../d2-200.md:1 S082 FAIL REFETCH` (rc 1) and the mutant prints `... S082 OK` (rc 0).
Receipt: `receipts/c1-03-tool-mutants.txt`.
The D2 class is built only from `_qualifying_203`, so it cannot build the S082 200-row reject that
distinguishes the mutant; the literal-removing `T-a` is caught only by `MUT_UNREACH derived=0`.

**F3 — C2: the verbatim-location check is a single expression; removing it makes a non-verbatim
paraphrase count as located and PASS all three detectors.**
Counter on `nv`: rc 0, `CURATION_R89=PASS`, `QUOTES_LOCATED=20/20 WARRANT_OK=17/17`; control battery
rc 0, `CONTROLS=PASS FORGERY_REFUSED=7/7`; committed mutant battery rc 0, `MUTANTS_KILLED=6/6`.
Honest counter on the same tree: rc 1, `QUOTES_LOCATED=19/20`, `LEG_FAIL FLOOR`, `LEG_FAIL WARRANT 16/17`.
Receipts: `receipts/c2-06-N7-all-detectors.txt`, `receipts/c2-02-probe-trees.txt`.

**F4 — C2: the `UNENTAILED` detector can be turned off with one expression; its printed field is
outside the frozen predicate and no battery case populates it.**
Honest counter on `unentailed`: rc 1, `UNENTAILED_TERM=1`, `LEG_FAIL UNENTAILED … term=modified`.
Mutant: rc 0, `UNENTAILED_TERM=0`, `CURATION_R89=PASS`; control battery rc 0, `CONTROLS=PASS 7/7`;
committed mutant battery rc 0, `MUTANTS_KILLED=6/6`.
Receipt: `receipts/c2-07-N9-all-detectors.txt`.

**F5 — C1 named limit 1 is real, and its boundary is narrower than stated.**
`C1-N03` (coherent detail+summary forgery) passes with output identical to the baseline; `C1-N04`
(deleting `and _ints("DIV3") == [c]`) passes with `DIV3=1` beside `3/3/3`. Both are refused only by
`mutate-r89.py`'s anchor tripwire (`SETUP_MISS …`, rc 2), not by a leg. `DIV3` is not in the frozen
field set, so the claim's predicate cannot see `C1-N04` either. Receipts:
`receipts/c1-02-new-mutants.txt`, `receipts/c1-04-tool-absent-and-second-detector.txt`.

**F6 — C1 named limit 2 is bounded exactly as described.**
`C1-N05` passes while the tool exists (rc 0, all fields; driver 11/11) and dies on the tool-absent tree
(`UNRECONCILED TOOL detail=tool present receipt_ok=True rederived=False`, rc 1). Receipt:
`receipts/c1-04-tool-absent-and-second-detector.txt`.

**F7 — C2 predicate observability: `VERDICT fields_hold=1` is unprintable on PASS; the printed leg
count is 8/8 for a nine-leg counter; `claims.json` omits two prose fields.**
`curation-r89.py --root tree-land` prints `LEGS_MEASURED=8/8 … CURATION_R89=PASS` and zero `VERDICT`
lines (rc 0). `claims.json` lists `DUP_QIDS=0 WARRANT_OK=17/17 QUOTES_LOCATED=20/20 TEACHES_FLAGGED=1
TEACHES_UNRESOLVED=0 SUP_UNRESOLVED=0` and neither `SUP_CLAUSE_CHECKED` nor the verdict token.
Receipt: `receipts/c2-05-predicate-observability.txt`.

**F8 — C2 named limits 1–3 reproduce exactly as disclosed; no surprise.**
`swap` rc 0 (all fields), `sub7` rc 0 (8 tokens), `sub6` rc 1 (`LEG_FAIL FLOOR`), `reorder` rc 0.
Receipt: `receipts/c2-04-named-limits.txt`.

**Calibration notes.**
* `FRESH` is count-pinned inside the counter (`C1-N09` prints `LEG_FAIL FRESH 4/5`, rc 1), while
  `POSITIVE` is not (`C1-N06` prints `POSITIVE=1/1 … PASS`); the pin for the latter lives in the claim
  and `controls/expected.tsv`, not in the instrument.
* `ROWS_203` is live (`C1-N08` prints `LEG_FAIL D1_WIDTH 3/3/3 pin2`, rc 1); `EXPECTED_LEGS` is live
  (`C1-N07` prints `UNRECONCILED SUMMARY …` / `LEG_FAIL SUMMARY 15/15`, rc 1).
* `C2-N2` (`MIN_TOKENS = 1`) prints output byte-identical to the honest baseline on the landing tree
  (`python3 -B out/c2/C2-N2-min-tokens-one/curation-r89.py --root tree-land`, rc 0, diff `IDENTICAL`;
  `receipts/c2-09-N2-silent-on-landing.txt`); only the `a1d` tree and the battery's A1d case expose it.
  A frozen constant moved inside the counter has no self-check.

# Restoration and cleanup

* No lane file was modified. The six instrument/tool hashes are `UNCHANGED` against `HEAD` after the
  probe (`receipts/00-commands-and-integrity.txt`); `PIN_MISMATCH=0` over all ten pinned files.
* All mutants were written under the scratch `out/` tree; the lane `tools/gate-records.py` and
  `corpus/evidence/round89/*.py` were only read.
* The scratch tree `/fast/scratch/hyaku/chousa-r89/R89MutBattery` was deleted after this report and
  `receipts/` were written; the durable evidence is in this folder (18 receipt files plus
  `MANIFEST.sha256`).

# Tooling

No tool was installed or upgraded (none was needed; the host pacman guard was respected, no network
was used; every check read committed bytes).

# Verdicts

VERDICT: R89MutBattery C1 held — the landing predicate, the committed 11+2 mutant batteries and the harm sweep all pass at `ac0a0892`, and the probe's survivors (a credited tool-mutant ledger that passes the full predicate, and an unreach rule narrowed to exactly 203 that is uncaught once its literal is kept) are mutation-coverage findings under the claim's named limits, not landing failures.

VERDICT: R89MutBattery C2 held — every frozen field, the control battery (7/7) and the mutant battery (6/6) hold at `ac0a0892` and both disclosed input-side named limits reproduce, while two single-expression counter edits remove the verbatim-locate and UNENTAILED detectors without any of the three detectors noticing, and the frozen prose token `VERDICT fields_hold=1` is never printed on PASS.
