# R81MutationCounters — mutation test of the two frozen round-81 counters

Seat: `R81MutationCounters` (leaf mutation tester). Round 81 (fresh start), lane `chousa-shokunin`.
Attack surface: the bytes at candidate landing `7e2da96a0541946e796384d42fea18e09ede9e9f`, never the
claims, counters, fixtures or receipts themselves — those were read and measured, not edited.

Scope: for each mutant of `corpus/evidence/round81/depth-r81.py` and
`corpus/evidence/round81/checklist-run.py`, run the **committed** control driver unchanged
against the mutated tree and ask whether any of its 16 control receipts loses its expected
exit code. 35 mutants (18 C1, 17 C2). Full table: `.ufo/waves/round-81/w1/R81MutationCounters/mutants.md`.

## Instruments and setup

```
S=/fast/scratch/hyaku/chousa-r81/R81MutationCounters
mkdir -p "$S"
git clone -q --shared /home/vgpnk/Projects/shokunin/chousa-shokunin "$S/tree"
git -C "$S/tree" checkout -q 7e2da96a0541946e796384d42fea18e09ede9e9f
```
Read-only clone (no lane git/jj mutation). Instrument hashes on the clone reproduce the values
frozen in `claims.md`:

```
10c989c0a59f94d88e03b0972378fd178bc6ee62e55bb580998751c3f2daa1e9  corpus/evidence/round81/depth-r81.py
66ca8c97c597f4b4b538322654e98f1ca83ebdde3b5d44c2b5d0bd63f295bbc2  corpus/evidence/round81/checklist-run.py
c1942bb92fc4901efcc8e82a8679c1d776fc0061f012c39afd4ea331f27ea65c  corpus/evidence/round81/run-controls.sh
```

Mutants were applied to private `git worktree` checkouts of that revision, one file at a time,
and the driver was executed from the mutated worktree:

```
HYAKU_SCRATCH=$S/drv/w<N> bash $S/wt<N>/corpus/evidence/round81/run-controls.sh \
  378fda82dc2cbcc555a0565052cc408121813cef $S/results/<mutant>
```
`run-controls.sh` derives `LANE` from its own path (`$LANE/corpus/evidence/round81/*-r81.py`), so the
mutated counter is what runs; the 16 control trees it builds stay the committed ones.

## Baseline (pristine bytes)

`receipts/baseline-controls/baseline.out`: 16/16 controls hit their `expect_rc`
(`c1-k0=1, c2-k0=1, c1-pos=0, c1-f1..f7=1, c2-pos=0, c2-g1..g3=1, c2-g4=2, c2-g5=1`), driver rc 0,
one 18.4 s battery. No baseline failure, so every mutant verdict below is interpretable.

## Result summary

| | count |
|---|---|
| mutants run | 35 |
| killed (a control left its expected rc) | 14 |
| survived | 21 |
| of which live-clause coverage gaps | 18 |
| of which equivalent (unobservable) mutants | 3 |

Killed: d02, d09, d11, d12, d13, d16 (C1); c01, c01b, c02, c03, c04, c08, c12, c13 (C2).
Survived: d01, d03, d04, d05, d06, d07, d07b, d08, d10, d14, d15, d17 (C1); c05, c06, c07, c09,
c10, c11, c14, c15, c16 (C2).

The pre-data note is **confirmed**: the `P4` shared-quote branch is not separately exercised
(d15 survives; witness W15 below). It is worse than "not separately": the two P4 branches mask
each other, so at most one of them can ever be observed (N2).

## Findings

### F1 (C1, strongest). `P4-shared-quote` has no control at all — d15 survives the full battery

Two byte-distinct, individually valid entries that share one located quote. Pristine bytes:

```
ENTRY ctl-b-r81.md counted=no reason=P4-shared-quote
DEPTH_R81 entries=1 … / DEPTH_R81=FAIL  rc=1
```
(`receipts/witness/w-shared-quote.d15.pristine.txt`)

With the shared-quote branch disabled the same tree gives
`ENTRY ctl-b-r81.md counted=yes`, `entries=2 fresh_rows=4 located_quotes=6`, `DEPTH_R81=PASS`, rc 0
(`receipts/witness/w-shared-quote.d15.mutant.txt`). The committed control `c1-f4-duplicate-entry`
cannot reach this branch: it makes the two entries byte-identical, so `P4-duplicate-bytes` fires
first (`receipts/killing/… f4` shows `reason=P4-duplicate-bytes`; under d14 the same control shows
`reason=P4-shared-quote`). Consequence: a later edit that drops the disjointness guard reads
all-green on the frozen battery. At the landing revision the guard is present and the predicate
holds (below), so this is control-coverage, not a claim failure.

### F2 (C2, strongest). `CHECKLIST=PASS` can be printed beside `CHECKLIST_RUN=5/6` — c09 survives

No control has all three legs passing while a non-leg item lacks its `Run:` line, so the
`runnable == 6` conjunct of the verdict is never exercised. Witness tree `w-item1-no-run` (item 1
has no `Run:` line, legs 2/4/5 intact), pristine:

```
CHECKLIST_RUN=5/6 DISCRIMINATE=3/3 / CHECKLIST=FAIL  rc=1
```
Mutant `c09` (`verdict = passed == 3`):

```
ITEM 1 runnable=no leg=n/a detail=-
…
CHECKLIST_RUN=5/6 DISCRIMINATE=3/3
CHECKLIST=PASS
rc=0
```
(`receipts/witness/w-item1-no-run.c09.mutant.txt`)

The frozen predicate is a printed line (`CHECKLIST_RUN=6/6 … CHECKLIST=PASS` and exit 0), but the
battery only compares exit codes, so the mutant's exit code is indistinguishable from the pristine
one on every control. On the real landing tree the printed line is `6/6` (below), so K1 does not
fire here; the finding is that the control battery cannot detect a counter that stops enforcing
its own printed counter.

### F3 (C2). The item-5 needle is unexercised — c05/c06/c16 survive

Every control that reaches item 5 runs the real `quote-reopen.py` on `item5-fail.tsv`, which prints
`QUOTE_REOPEN_SUMMARY … no_source=1`; no control makes the command exit 1 with a different summary.
Witness `w-needle` (item 5 prints `QUOTE_REOPEN_SUMMARY no_source=0` and exits 1):

pristine `ITEM 5 runnable=yes leg=fail … DISCRIMINATE=2/3 … FAIL` rc 1;
c05 `leg=pass … DISCRIMINATE=3/3 … PASS` rc 0
(`receipts/witness/w-needle.c05.{pristine,mutant}.txt`). Dropping the needle (c05), never
evaluating it (c06), or matching any summary line (c16) all leave 16/16 control rcs unchanged.
This matters because the claim's own stated limit says item 5's leg is fail-only; the needle is
the only thing that makes it more than "exit 1".

### F4 (C1). The refetch-record conjuncts are only partly covered — d10, d17 survive, d09/d11 die

`c1-f5-capture-not-recorded` (capture bytes changed) kills d09 (whole binding removed) and d11
(`txt_sha256` conjunct removed), but nothing exercises the other conjuncts:

- d10 (drop `fetched_utc` on `--date`): witness `w-refetch-date` — refetch rows dated 2026-10-21,
  registry still opened 2026-11-06 → pristine `P2-no-fetch-record-S901` rc 1, mutant
  `counted=yes … PASS` rc 0.
- d17 (drop `curl_rc == 0` and `http 2xx`): witness `w-curl-rc` — `curl_rc=22` with a matching
  sha → same pristine/mutant split (`P2-no-fetch-record-S901` rc 1 → PASS rc 0).

### F5 (C1). P1's freshness conjuncts `used_by` and `status` are unexercised — d03, d04 survive

No control varies either cell; f4 only *adds* a second entry name to `used_by`, which its
duplicate-bytes path rejects anyway. Witnesses `w-used-by` (`used_by` names another entry) and
`w-status` (opened today, status `rejected`) both go pristine `P1-fresh-rows=0` rc 1 → mutant
`counted=yes … PASS` rc 0 (`receipts/witness/w-used-by.d03.*`, `w-status.d04.*`).
`opened == --date` *is* covered (d02 dies on `c1-f3`).

### F6 (C1). Quote-form thresholds are unexercised — d05, d06, d08, d07b survive

- minimum quote lines (`< 3`): witness `w-two-quotes` → pristine `P2-quote-lines=2` rc 1,
  d05 `counted=yes … PASS` rc 0.
- the 25-word cap: witness `w-word-cap` (28-word located quote) → pristine `P2-quote-words=28`
  rc 1, d06 `counted=yes … PASS` rc 0. Control `c1-f7` does not isolate the cap: the doubled
  quote is *also* absent from the capture, so `P2-absent` would reject it with the cap removed.
- distinct fresh rows (`< 2`): witness `w-one-row` (three located quotes, all S901) → pristine
  `P2-distinct-rows<2` rc 1, d08 PASS rc 0.
- quote sid ∈ fresh set: d07b (weakened to "listed on the source line") → witness
  `w-stale-listed-row` (quote cites S906, opened 2026-10-21) → pristine
  `P2-quote-cites-non-fresh-S906` rc 1, mutant PASS rc 0.

### F7 (C2). Placeholder substitution and Run-line selection are unexercised — c11, c15 survive

- c11 (substitute *every* placeholder instead of the first) survives because every control item
  carries exactly one placeholder. Witness `w-placeholders` (item 2: two `<record.md>`, only the
  second decides rc) → pristine `DISCRIMINATE=2/3` rc 1, mutant `3/3 … PASS` rc 0.
- c15 (last Run command instead of first) survives because every control item has exactly one
  Run line. Witness `w-last-run` (real Run line plus a trailing `true <record.md>`) → pristine
  PASS rc 0, mutant `DISCRIMINATE=2/3 … FAIL` rc 1.

### F8 (C2). Usage-error and denominator guards — c14, c01b

- c14 (missing-fixture guard removed) survives: no control passes `--fixtures`. Witness with
  `--fixtures` lacking `item4-fail.md`: pristine `CHECKLIST error: missing fixture item4-fail.md`
  rc 2, mutant rc 1.
- the denominator check *is* exercised (c01b, accept any count ≥1, dies on `c2-g4-item-deleted`
  2→1), but the literal operator swap `!= 6` → `!= 0` (c01) is a malformed mutant: it refuses
  every count (`CHECKLIST error: denominator 6 != 6`, rc 2 on all controls). Recorded as killed,
  but the kill says nothing about the guard's strength; c01b is the meaningful probe.

### F9. Two survivors are rc coincidences, not predicate kills — d07, c07

The detector compares exit codes only, so an uncaught exception that exits 1 is scored as the
expected failure:

- d07 (membership check dropped): `c1-f1` raises `KeyError: 'S999'` at `depth-r81.py:117`
  (`receipts/killing/d07--c1-f1-unregistered-id.txt`), rc 1 = `expect_rc` 1.
- c07 (`r = True`): k0 raises `IndexError: list index out of range` at `checklist-run.py:114`
  (`receipts/killing/c07--c2-k0-donothing.txt`), rc 1 = `expect_rc` 1. The witness
  `w-item1-no-run` then shows the mutant printing `CHECKLIST_RUN=6/6` for a tree where item 1 has
  no `Run:` line.

Under a detector that also forbade tracebacks these two would be killed; under the frozen rc
detector they survive. Stated as such rather than counted as kills.

### Equivalences (survivors that are not gaps)

- **d01** (P1 min fresh rows 2→1): an entry with one fresh row is rejected one clause later by
  `P2-distinct-rows<2`. Empirical: witness `eq-d01` → pristine `P1-fresh-rows=1` rc 1, mutant
  `P2-distinct-rows<2` rc 1 — same counted set, same rc, only the printed reason moves.
- **d14** (duplicate-bytes branch removed): identical bytes imply identical quote lines and P2
  requires ≥3 quote lines, so the shared-quote branch always fires when duplicate-bytes would;
  the mutant's own f4 run prints `reason=P4-shared-quote` rc 1. The two branches mask each other.
- **c10** (no-placeholder refusal removed): a placeholder-free command gets no per-leg argument,
  so it exits the same way on the pass and the fail fixture and the leg fails either way. No leg
  verdict can change.

## What this does and does not say about the frozen claims

Both counting commands were run on the landing tree (read-only) as a cross-check of the verdicts:

- `receipts/landing-c1-depth.txt`: `DEPTH_R81 entries=2 fresh_rows=5 located_quotes=14`,
  `DEPTH_R81=PASS`, rc 0 — the predicate line of C1 holds, K1 does not fire.
- `receipts/landing-c2-checklist.txt`: `CHECKLIST_RUN=6/6 DISCRIMINATE=3/3`, `CHECKLIST=PASS`,
  rc 0 — the predicate line of C2 holds, K1 does not fire.

The mutation result is therefore a statement about the *batteries*, not about the landing data:
14 of 35 single-clause defects are caught; 18 defects that change what the counters accept are
not. The two sharpest are F1 (C1) and F2 (C2): each lets a counter keep every expected control
exit code while accepting input the frozen predicate rejects. That is a coverage finding against
`controls/`, not permission to change the contract — no counter, control, fixture, claim or
`SKILL.md` byte was touched.

Limits of this probe: the detector is the committed driver's rc comparison (16 controls, one
tree family), so mutants masked by another clause (d01, d14), by an expected-failure control
(d07, c07), or by the leg model (c10) are reported as survivors rather than proven safe;
`c01` was mis-specified as an operator swap and is flagged as such (c01b is its meaningful form).

## Reproducibility

- Harness: `run_mutants.py` + `spec.py` (35 definitions, three parallel worktrees).
- Baseline: `receipts/baseline-controls/baseline.out` and the 16 pristine receipts beside it.
- Per-mutant data: `receipts/mutant-runs.tsv` (verdict, killing controls, crash controls,
  `mutant_sha16` / `pristine_sha16` / `restored_sha16`), `receipts/summary-all.json` (per-control
  expect/got), `receipts/killing/<mutant>--<control>.txt`.
- Witnesses: `receipts/witness/<tree>.<mutant>.{pristine,mutant}.txt`, raw stdout + `rc=`.

Restoration: the mutated file in every worktree was restored with
`git -C <worktree> checkout -- <file>` after the battery and re-hashed; `restored_sha ==
pristine_sha` in all 35 entries, and the three instrument files in the unmutated tree still match
the frozen hashes. The scratch root `/fast/scratch/hyaku/chousa-r81/R81MutationCounters` was
removed after these receipts were copied here.

Tooling: nothing installed or upgraded (pacman transactions are paused host-wide; no tool was
needed beyond git, python3, tar, bash).

VERDICT: R81MutationCounters C1 held — at the landing revision the counting command prints `DEPTH_R81=PASS` rc 0, and mutation testing changes no claim; 12 of 18 C1 single-clause defects survive the frozen battery, including the previously flagged `P4-shared-quote` branch, which no control exercises (d15, witness W15).
VERDICT: R81MutationCounters C2 held — at the landing revision the counting command prints `CHECKLIST_RUN=6/6 DISCRIMINATE=3/3` and `CHECKLIST=PASS` rc 0; 9 of 17 C2 defects survive the frozen battery, the sharpest being that `CHECKLIST=PASS` can be printed beside `CHECKLIST_RUN=5/6` with rc 0 (c09, witness C9).
