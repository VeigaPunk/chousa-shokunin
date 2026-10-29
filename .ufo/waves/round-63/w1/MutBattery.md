# MutBattery — mutation test of `corpus/evidence/round63/c1-battery.py` (round 63, wave w1)

Lane `chousa-shokunin`, base `c8bfcc6`. Battery sha256 prefix `0073fba73c89aaf8` (verified, unmodified; the lane tree was not changed).
Scope: 12 single-point mutants of the frozen battery, each run as `--only` partials (plus one full run where the mutant changes the aggregate line) against `controls/pos-ref-preflight.py`, `controls/null-pass.py`, `controls/null-diff-oracle.py`. Four candidate killer controls were built in scratch to name the controls that would kill the survivors. Mutants and killers lived only in scratch; nothing under `corpus/evidence/round63/`, `tools/`, `corpus/`, `SKILL.md` was written.

## Findings (first)

- **6 of 12 mutants are killed by the three named controls** (bm01, bm02, bm03, bm04, bm07, bm10). Each flips a control's leg or aggregate verdict relative to the unmutated battery.
- **4 more are killed by candidate controls I built** (kM05, kM13g8, kRcOne, kOrder). These are not in the frozen control set, so they are gaps, not refutations of the frozen battery.
- **bm08 (constant per-leg pick) survives** every control I ran, including the one candidate built to expose it, in the one seeded run I could afford.
- **bm11 (GATE-duplicate check removed) is an equivalent mutant**: removing the check changes no verdict, because the order check still fails the duplicated output (kDup: both battery and mutant print FAIL).
- **bm10 (aggregate ignores benign legs) is visible only in the full run.** The `--only` path returns `BATTERY=PARTIAL` before the aggregate line, so no partial run can see it.
- **Gap count (survivors of the three named controls that need a new control): 5** (bm05, bm06, bm08, bm09, bm12). bm11 is equivalent, not a gap.

## Baselines (unmutated battery, the reference for every flip)

Command: `python3 -B corpus/evidence/round63/c1-battery.py --tool <T> --lane <lane> --fleet /home/vgpnk/Projects/shokunin --work <scratch>/w --jobs 2` (full run).

| tool | observed last line | per-leg |
|---|---|---|
| `pos-ref-preflight.py` | `CLEAN=1/1 DEFECTS=15/15 BENIGN=6/6 BATTERY=PASS` (exit 0, wall 1m54s, user 14m31s) | all ok |
| `null-pass.py` | `CLEAN=1/1 DEFECTS=0/15 BENIGN=6/6 BATTERY=FAIL` (exit 1) | CLEAN ok; D01–D15 FAIL; B01–B06 ok |
| `null-diff-oracle.py` | `CLEAN=1/1 DEFECTS=15/15 BENIGN=0/6 BATTERY=FAIL` (exit 1) | CLEAN ok; D01–D15 ok; B01–B06 FAIL |

These match the committed receipts (`controls/c1-controls.txt`, lines for `positive-ref`, `null-pass`, `null-diff-oracle`).

## Mutant table

Each row: the change (line in the unmutated battery), then the leg verdict on each named control. "base" is the baseline verdict for that leg. A flip is a verdict that differs from base.

| mutant | change (line) | pos-ref | null-pass | null-diff-oracle | result |
|---|---|---|---|---|---|
| bm01 | D01 plants nothing (137 → `pass`) | FAIL rc=0 want 1 (base ok) | FAIL (base FAIL) | FAIL rc=0 want 1 (base ok) | **KILLED** |
| bm02 | D01 expects exit 0 (242) | FAIL rc=1 want 0 (base ok) | ok (base FAIL) | FAIL rc=1 want 0 (base ok) | **KILLED** |
| bm03 | CLEAN drops `--skip G08` (241) | FAIL ran …G08 want …G07 (base ok) | ok | FAIL ran …G08 (base ok) | **KILLED** |
| bm04 | B01 plants status `bogus` (210) | FAIL rc=1 want 0 (base ok) | ok | FAIL (base FAIL) | **KILLED** (pos-ref) |
| bm05 | judge drops both summary cross-checks (301, 306 → `if False:`) | ok | ok | ok | survived → killer kM05 |
| bm06 | judge drops `ran`-list check (294 → `if False:`) | ok (D14) | FAIL (base) | ok (D14) | survived → killer kM13g8 |
| bm07 | golden copy skips `tools/` (69) | FAIL rc=1 want 0 (CLEAN, base ok) | ok | FAIL `summary lines=0` (base ok) | **KILLED** |
| bm08 | per-leg pick constant (D01 136 → `registry_rows(src)[0]`; D05 162 → `names[0]`) | ok | FAIL (base) | ok | survived; no killer in one seeded run (see below) |
| bm09 | CLEAN accepts exit 1 (286) | ok | ok | ok | survived → killer kRcOne |
| bm10 | aggregate `good` ignores benign (396) | not run (aggregate needs full run) | — | full run `BATTERY=PASS` (base FAIL) | **KILLED** (full run only) |
| bm11 | GATE-duplicate check removed (278 → `if False:`) | ok | ok | ok | equivalent (kDup: both FAIL, order check) |
| bm12 | gate-order check removed (290 → `if False:`) | ok | ok | ok | survived → killer kOrder |

Killed by the three named controls: **6/12**. Killed with the candidate controls added: **10/12** (bm05, bm06, bm09, bm12 added). bm08 survives. bm11 is equivalent.

## Named controls that would kill each survivor (candidates, scratch only, not in the lane)

Each candidate was run through the mutant battery and the unmutated battery with the same `--only` set (evidence in the table above and `logs-kill/`, see Evidence).

- **kM05** (for bm05): copy of pos-ref whose summary prints `/{len(IDS)}` instead of `/{len(ran)}`. Unmutated: `CLEAN=0/1 … FAIL summary 7/8 but lines say 7/7`. bm05: `CLEAN ok`. Killed. Lane analogue: `controls/run-c1-controls.py` mutant M05-summary-counts-skip.
- **kM13g8** (for bm06): copy of pos-ref that ignores `--only` (`if gid in skip or gid == "G08":`). Unmutated, leg D14: `FAIL ran G01,…,G07 want G03`. bm06: `D14 ok`. Killed. Note: this copy adds a G08 guard so that D14 does not start the G08 selftest. The committed M13-only-ignored (no guard) would run G08 on every D14 leg; I did not run it.
- **kRcOne** (for bm09): copy of null-pass that exits 1 with all gates PASS. Unmutated, CLEAN: `FAIL rc=1 want 0`. bm09: `CLEAN ok`. Killed.
- **kOrder** (for bm12): copy of null-pass with G02 printed before G01. Unmutated, CLEAN: `FAIL gate lines G02,G01,G03,…`. bm12: `CLEAN ok`. Killed.
- **kDup** (for bm11, equivalence check): copy of null-pass with G01 printed twice. Unmutated: `FAIL gate G01 printed twice`. bm11: `FAIL gate lines G01,G01,G02,…`. Both fail, so bm11 is equivalent.
- **kHole** (for bm08): copy of pos-ref whose G02 skips the second sorted knowledge entry. One seeded run each: unmutated D05 `ok`, bm08 D05 `ok`. The hole is reached only when the random pick lands on entry 2 (about 1/84 per leg, from 84 knowledge entries), so one run cannot separate the two. No killer found; **gap**.

## Evidence (commands and observed output)

Scratch logs (deleted before yield; key lines quoted here):

- `logs-mut/bm01-pos-ref.log`: `LEG D01 defect FAIL rc=0 want 1`, `CLEAN=0/1 DEFECTS=0/15 …`
- `logs-mut/bm03-null-diff-oracle.log`: `LEG CLEAN clean FAIL ran G01,…,G08 want G01,…,G07`
- `logs-mut/bm03-pos-ref.log`: `LEG CLEAN clean FAIL ran G01,…,G08 want G01,…,G07` (the reference's real G08 ran inside the leg)
- `logs-mut/bm07-pos-ref.log`: `LEG CLEAN clean FAIL rc=1 want 0`
- `logs-mut/bm07-null-diff-oracle.log`: `LEG CLEAN clean FAIL rc=1 summary lines=0`
- `logs-mut/bm10-null-diff-oracle.log`: `CLEAN=1/1 DEFECTS=15/15 BENIGN=0/6 BATTERY=PASS` (baseline `BATTERY=FAIL`)
- `logs-kill/pristine-on-kM05.log`: `LEG CLEAN clean FAIL summary 7/8 but lines say 7/7`; `logs-kill/bm05-on-kM05.log`: `LEG CLEAN clean ok ok`
- `logs-kill/pristine-on-kM13.log`: `LEG D14 defect FAIL ran G01,…,G07 want G03`; `logs-kill/bm06-on-kM13.log`: `LEG D14 defect ok ok`
- `logs-kill/pristine-on-kRcOne.log`: `LEG CLEAN clean FAIL rc=1 want 0`; `logs-kill/bm09-on-kRcOne.log`: `LEG CLEAN clean ok ok`
- `logs-kill/pristine-on-kOrder.log`: `LEG CLEAN clean FAIL gate lines G02,G01,…`; `logs-kill/bm12-on-kOrder.log`: `LEG CLEAN clean ok ok`
- `logs-kill/pristine-on-kDup.log`: `LEG CLEAN clean FAIL gate G01 printed twice`; `logs-kill/bm11-on-kDup.log`: `LEG CLEAN clean FAIL gate lines G01,G01,G02,…`
- `logs-kill/pristine-on-kHole.log` and `logs-kill/bm08-on-kHole.log`: `LEG D05 defect ok ok` (both)
- Mutant source check: `python3 -B` `ast.parse` on the 12 mutant files: `SYNTAX_OK 12`.
- Reference alone: `base-ref.log` `CLEAN=1/1 DEFECTS=15/15 BENIGN=6/6 BATTERY=PASS`.

## Errors and corrections

- **My first mutant matrix used the unmutated battery.** The shell variable I set for the battery pointed at `c1-battery.py`, not at each `mutants/bmNN.py`. The first matrix's logs (`logs/`) therefore show pristine verdicts, and I misread them as a flaky census. I found it when `bm02` on pos-ref read `ok` with expected rc 0, and a debug copy of bm01 gave `FAIL rc=0 want 1`. I discarded `logs/` and re-ran the full matrix with `$M/bmNN.py`. Every verdict in this report comes from `logs-mut/`, `logs-kill/` and the baseline runs, all of which used the mutant or killer file they name.
- A minimal fixture copy (`SOURCES.md` alone) made the census report `E11 missing used-by`. That is my fixture, not the lane (the lane census exits 0). Not a finding.
- kHole and bm08: I do not claim a kill from one run. The hole is reached about 1/84 of the time; that is inference from the entry count and the random pick, not measured over seeds.

## Named limits (for the L1)

- `--only` never reaches the aggregate: any defect confined to the `BATTERY=` line (bm10) is invisible to partial runs. Only the full run shows it.
- G08 timing: `bash tools/research-gate.sh --selftest` run standalone under the host load did not finish within the 900 s bash cap (background job bg_27227, "Command timed out after 900 seconds"). Inside the battery, the pos-ref leg of bm03 ran G08 to completion; the stream of three legs took 597.96 s wall. I did not measure G08 exactly. The battery's tool timeout is 600 s, so a slower G08 would turn bm03's pos-ref leg into a timeout (also a kill, for a different reason).
- The frozen battery's per-leg random picks give coverage only through randomness; a constant pick (bm08) is not caught by the three controls.

## Install / host record

No tools installed or upgraded. No git, jj or index writes. No pacman. Scratch `/fast/scratch/hyaku/chousa-r63/MutBattery/` (mutants, killers, logs) deleted before yield; the evidence above is quoted from it.

VERDICT: BATTERY_MUTANTS_KILLED=6/12 control_gaps=5
