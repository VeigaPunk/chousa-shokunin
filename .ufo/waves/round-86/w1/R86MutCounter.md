# R86MutCounter — mutation probe of the two round-86 counters (C1, C2)

Seat `R86MutCounter`, leaf (no subagents). Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Inputs: the frozen predicate set `corpus/evidence/round86/claims.md` (read first, with every kill rule) and
`plans/round-86.md`. Scratch root `/fast/scratch/hyaku/chousa-r86/R86MutCounter` (deleted before yield).
No network was used; no tool was installed or upgraded (python3 stdlib only).

## Revisions and bytes attacked

| role | revision | note |
|---|---|---|
| landing (attacked) | `667a5d091dc46168ed95eda0ae7f19a9bcf139a2` | extracted with `git -C $LANE archive 667a5d0… \| tar -x -C $S/land` |
| base (second tree) | `3bfb6885958ad4a674ad1896f70d1e836be609e4` | extracted with the same archive form into `$S/base` |
| repo legs | `$S/repo/land.git`, `$S/repo/base.git` | `git clone --no-hardlinks $LANE …` then `git checkout <rev>`; `rev-parse HEAD` asserted equal to the named rev |

Pristine instrument bytes equal the freeze pins `corpus/evidence/round86/instrument-pins.txt`:

```
20bc1a733bd6c79f428a16c564cdc49555d8f02c389307eb2c6a28ceeb106d66  corpus/evidence/round86/gate-records-r86.py
84a64ad48d77e63095919942ac113bbb1b54b4e7d9acd21ef85a4f58e545c5d4  corpus/evidence/round86/curation-r86.py
8c089828981bb0c8b5a0ab253bb4ec5f1537825cb84cea8964497310bb01f3c6  corpus/evidence/round86/c2-positives.tsv
fe204539b9b549ef1c6092a3963d73c7772946b027ab07da19c89961817aa287  tools/gate-records.py
```

The subject tool `tools/gate-records.py` is byte-identical at base and at landing; it was never mutated —
it is only *input* in two probes below.

## Detector (identical for pristine and every mutant)

The assigned detector is the frozen predicate each counter prints, run on both trees:

```sh
# C1 (gate-records-r86.py); mutant dirs carry a copy of c2-positives.tsv beside the counter (POS_TSV is HERE-relative)
python3 -B $S/mut/<M>/gate-records-r86.py --root $S/land --repo $S/repo/land.git --work $S/work/<M>/land
python3 -B $S/mut/<M>/gate-records-r86.py --root $S/base --repo $S/repo/base.git --work $S/work/<M>/base
# C2 (curation-r86.py)
python3 -B $S/mut/<N>/curation-r86.py --root $S/land
python3 -B $S/mut/<N>/curation-r86.py --root $S/base
```

* survivor = the mutant still prints the frozen expected verdicts on **both** trees;
* killed = it fails (verdict, field deviation, or no verdict at all) on either tree.

## Baselines (pristine, before any mutation)

| leg | command | observed line | exit |
|---|---|---|---|
| C1 land | `gate-records-r86.py --root $S/land --repo $S/repo/land.git` | `TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=355/355 EXPECTED_CODE=355/355 EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1 D1_FORGES=1 D1_REFUSED=1/1 MUT17_KILLED=1/1` / `GATE_RECORDS_R86=PASS` | 0 |
| C1 base | same counter, `--root $S/base --repo $S/repo/base.git` | identical line / `GATE_RECORDS_R86=PASS` | 0 |
| C2 land | `curation-r86.py --root $S/land` | `SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20` / `CURATION_R86=PASS` | 0 |
| C2 base | `curation-r86.py --root $S/base` | `SUPERSEDED_LIVE=1 UNENTAILED_TERM=2 MODIFIED_DEF_CITED=0 QUOTES_LOCATED=19/19` / `CURATION_R86=FAIL` | 1 |

Both baselines reproduce the frozen landing values and the committed control
(`controls/receipts/c2-d0-donothing.txt`) exactly, so every mutant below is scored against a live baseline and not
against a broken harness. Receipts: `receipts/baseline-*.txt`.
Note: the C1 predicate is met on the base tree too (the tool and the S021 203 row both predate the round); the base
tree is therefore a second, independent input for C1 rather than a "before" control — the C1 before-control is the
pre-round-85 tool, which is outside this seat's mutation scope.

## Mutants and observed output

`sha` = sha256 of the mutated counter; pristine shas are those pinned above. Full stdout/stderr and exit codes per
tree: `receipts/<mutant>.txt`.

### C1 `corpus/evidence/round86/gate-records-r86.py`

| id | one-point mutation | land | base | verdict |
|---|---|---|---|---|
| M1 | delete `forged.append((d1_label, d1_sid, d1_line, d1_code))` | exit 1, **no verdict**, `ValueError: list.index(x): x not in list` at `ffiles[[…].index(d1_label)]` | same | **killed** (crash, not a graceful FAIL) |
| M2 | replace the whole mutant leg (`mut17 = 0 … print("MUT17_NOT_RELAXED …")`) with `mut17 = 1` — no mutant is built or run | `… D1_FORGES=1 D1_REFUSED=1/1 MUT17_KILLED=1/1` / `PASS`, exit 0 | identical | **SURVIVOR** |
| M3 | `and d1 is not None and d1_refused == 1` → `and (d1 is None or d1_refused == 1)` | full frozen line / `PASS`, exit 0 | identical | **SURVIVOR** (semantically equivalent — see below) |
| M4 | `build_d1_203_admit` builds `decision=reject` instead of `decision=admit` | exit 1, `WRONG_CODE g0354.md D1-203-admit S021 expected=REFETCH got=PARSE`, `GATE_RECORDS_R86=FAIL` | identical | **killed** |
| M5 | drop `and setup_ok == 1` from the `passed` conjunction | full frozen line / `PASS`, exit 0 | identical | **SURVIVOR** |

Mutant shas: M1 `b2cae713…`, M2 `0907b0b6…`, M3 `74a4c73c…`, M4 `ae5c97b8…`, M5 `27fc0982…` (full values in receipts).

### C2 `corpus/evidence/round86/curation-r86.py`

| id | one-point mutation | land | base | verdict |
|---|---|---|---|---|
| N1 | supersession append guarded by `if False:` (loop runs, never records) | `SUPERSEDED_LIVE=0 … QUOTES_LOCATED=20/20` / `PASS`, exit 0 | exit 1 `SUPERSEDED_LIVE=0 UNENTAILED_TERM=2 MODIFIED_DEF_CITED=0 QUOTES_LOCATED=19/19` / `FAIL` | **survives the verdict detector**, field deviation on base only (`SUPERSEDED_LIVE` 1→0) |
| N2 | `if MODIFIED_DEF in q.lower():` → `if MODIFIED_DEF in q:` (the pre-freeze case bug) | `MODIFIED_DEF_CITED=0` / `FAIL`, exit 1 | `MODIFIED_DEF_CITED=0` / `FAIL`, exit 1 | **killed** |
| N3 | `if cap is not None and norm(quote) in cap:` → `if cap is None or …` (a missing capture counts as located) | `SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20` / `PASS`, exit 0 | full base control line / `FAIL`, exit 1 | **SURVIVOR** |
| N4 | `pred = (not superseded_live and not unentailed and …` → drop `not unentailed` | full frozen line / `PASS`, exit 0 | full base control line / `FAIL`, exit 1 | **SURVIVOR** |

Mutant shas: N1 `d2a3c3eb…`, N2 `dd79e79f…`, N3 `317c0d35…`, N4 `b915f46b…`.

## Survivor table and the leg that should have killed it

Supplementary probes (`receipts/probe-*.txt`) put each survivor's missing input in front of the **pristine** counter
first, to prove the leg exists and that the pristine instrument would fail on it; the mutant then runs on the same
input.

| survivor | leg that should have killed it | pristine on that leg | mutant on that leg |
|---|---|---|---|
| **M2** (mutant credited without a run) | a tool whose bytes contain no `r[6] == "200"` literal, so `build_mutant` must report "no mutant derived" (claims K4: a counter that cannot derive one prints `MUT17_KILLED=0/1`) | probe A: tool copy with `r[6] == "2" + "00"` → `MUT17_KILLED=0/1` / `FAIL`, exit 1 | `MUT17_KILLED=1/1` / **`PASS`, exit 0** |
| **M3** (accept `d1 is None`) | none exists: the mutation is **logically equivalent**. `mut17` is only assigned inside `if d1 is not None:`, so with `d1 is None` the surviving conjunct `mut17 == 1` is false anyway; with `d1` present the two forms are textually different and semantically identical | probe C: tree whose 203 rows carry a non-matching `txt_sha256` (D1 unbuildable) → `D1_FORGES=0 D1_REFUSED=0/1 MUT17_KILLED=0/1` / `FAIL` | identical `FAIL`, exit 1 — the weakened guard cannot fake a pass |
| **M5** (drop `SETUP` from `passed`) | a tool that does not exit 2 with `GATE_RECORDS_ERROR` on a non-git `--repo` (the SETUP leg) | probe B: tool copy with the not-a-git `return 2` replaced by `pass` → `SETUP=0/1` / **`FAIL`**, exit 1 | `SETUP=0/1` but **`PASS`, exit 0** — the field still tells, the verdict does not |
| **N1** (supersession loop skipped) | a tree that carries the live inversion while nothing else fails — i.e. the base control minus the other two defects. No such tree exists in this round; on base the tell is field-level only (`SUPERSEDED_LIVE` 1→0, verdict `FAIL` either way) | base tree: `SUPERSEDED_LIVE=1` (control value) | base tree: `SUPERSEDED_LIVE=0`, verdict unchanged |
| **N3** (missing capture counted as located) | a routed entry quoting a row whose committed capture is absent (claims K2: a quote "located" must be verbatim in the capture of the row's own URL) | probe D: landing tree without `corpus/captures/f5545a194c06ab421875b047.txt` (S023) → `QUOTES_LOCATED=15/20` / **`FAIL`**, exit 1 | `QUOTES_LOCATED=20/20` / **`PASS`, exit 0** |
| **N4** (`UNENTAILED_TERM` not in `pred`) | a tree with an unentailed warrant term and everything else clean (the landing tree plus the round-85 row-6 comparison restored) | probe E: `UNENTAILED_TERM=1` / **`FAIL`**, exit 1 | `UNENTAILED_TERM=1` printed but **`PASS`, exit 0** |

Probe inputs are scratch-only: A and B are tool copies passed via `--tool`; C, D and E are `cp -al` hardlink copies of
the landing tree (`C-no-d1`, `D-no-capture`, `E-unentailed-cell`) with one committed predicate input changed. The
landing tree itself was never written.

## What the survivors mean for the two claims

- **C1.** `MUT17_KILLED=1/1` is not self-certifying: a counter that never derives the mutant prints `1/1`
  (M2) and a counter that prints `SETUP=0/1` can still print `PASS` (M5). The frozen predicate therefore depends on
  reading the individual fields, not on `GATE_RECORDS_R86=PASS`; claims K4 names the derivation duty but the
  predicate has no leg that fails when the duty is dropped. The D1 legs themselves are tight: removing the D1 forge
  crashes (M1), and a D1 record that is not an admit is refused with the wrong code and kills the run (M4).
- **C2.** `QUOTES_LOCATED` and `UNENTAILED_TERM` never decide a verdict on either tree this round: on landing both are
  at their good values and on base the run already fails on supersession and `MODIFIED_DEF_CITED`. N3 and N4 are
  survivors of the *verdict* detector for that reason, and only a probe tree (D, E) exposes them. `MODIFIED_DEF_CITED`
  is the one calibrated field whose removal is caught at landing (N2).

A surviving mutant is a coverage finding against the counters, not a defect in the landed repair or the claims'
wording; no counter byte, claim, plan or tool was changed by this seat.

## Restoration evidence

Every mutation was written only to `$S/mut/<id>/`, never over a pristine file. After all runs and probes:

```
20bc1a733bd6c79f428a16c564cdc49555d8f02c389307eb2c6a28ceeb106d66  $S/land/corpus/evidence/round86/gate-records-r86.py
84a64ad48d77e63095919942ac113bbb1b54b4e7d9acd21ef85a4f58e545c5d4  $S/land/corpus/evidence/round86/curation-r86.py
8c089828981bb0c8b5a0ab253bb4ec5f1537825cb84cea8964497310bb01f3c6  $S/land/corpus/evidence/round86/c2-positives.tsv
fe204539b9b549ef1c6092a3963d73c7772946b027ab07da19c89961817aa287  $S/land/tools/gate-records.py
fe204539b9b549ef1c6092a3963d73c7772946b027ab07da19c89961817aa287  $S/base/tools/gate-records.py
# lane checkout, read-only, never written by this seat
20bc1a733bd6c79f428a16c564cdc49555d8f02c389307eb2c6a28ceeb106d66  $LANE/corpus/evidence/round86/gate-records-r86.py
84a64ad48d77e63095919942ac113bbb1b54b4e7d9acd21ef85a4f58e545c5d4  $LANE/corpus/evidence/round86/curation-r86.py
8c089828981bb0c8b5a0ab253bb4ec5f1537825cb84cea8964497310bb01f3c6  $LANE/corpus/evidence/round86/c2-positives.tsv
fe204539b9b549ef1c6092a3963d73c7772946b027ab07da19c89961817aa287  $LANE/tools/gate-records.py
```

(before = after = the freeze pins; `receipts/hashes-before-after.txt`). Scratch
`/fast/scratch/hyaku/chousa-r86/R86MutCounter` removed after this report and its receipts were copied here; the temp
directories the counter creates live only under `$S/work`, and the two clones are `--no-hardlinks` copies of the lane,
never the lane.

## Counter compliance

Every row above names the exact command (`## tree=` section of its receipt), the receipt written
(`.ufo/waves/round-86/w1/R86MutCounter/receipts/<name>.txt`), the observed output line and the exit code. Nine mutants
(5 C1, 4 C2) and five kill-leg probes were executed; the two runs that produced no verdict line (M1) print the
exception and exit 1, recorded as such rather than as a pass.

VERDICT: R86MutCounter C1 held — the landed counter prints the full frozen C1 line unchanged on both trees and M1/M4 kill it, but M2, M3 and M5 survive, so `GATE_RECORDS_R86=PASS` alone does not witness mutant derivation or the SETUP gate.
VERDICT: R86MutCounter C2 held — the landed counter prints the frozen C2 line on both trees and N2 kills it, while N1 (field-level tell only), N3 and N4 survive the verdict detector, so only probes D and E expose the `QUOTES_LOCATED` and `UNENTAILED_TERM` calibration.
