# MutPre5Main — mutation test of the reference preflight (G05 + main())

Seat: mutation-tester (leaf, no dispatch). Target: `corpus/evidence/round63/controls/pos-ref-preflight.py`
(sha256 prefix `07683086fd6c6b41`, unchanged before and after; verified by the driver's `REF_AFTER ... unchanged=True`).
Battery: `corpus/evidence/round63/c1-battery.py` (sha256 prefix `0073fba73c89aaf8`, run unmodified). No lane,
fleet or git writes. Mutants were built in scratch copies only.

## Method

- Read the frozen controls (`controls/run-c1-controls.py` M01–M16) and the battery (`c1-battery.py`, legs CLEAN, D01–D15,
  B01–B06). None of my 18 mutants duplicates M01–M16 (M11 is the known equivalent survivor there).
- Driver: `/fast/scratch/hyaku/chousa-r63/MutPre5Main/mutate.py` (scratch, now deleted). Each mutant is one
  `str.replace` on an anchor that must occur exactly once (the driver asserts the count). The battery runs with
  `--only CLEAN,<killers>` (partial, `BATTERY=PARTIAL`), `--jobs 2`, `--fleet /home/vgpnk/Projects/shokunin`.
- Survivors of the partial pass got one full battery run (`--only` absent; `BATTERY=PASS` means it survived all 22 legs).
- Probes (direct runs of the reference and the mutant on a 1-gate fixture, `--only G0x`) decide whether a survivor is
  equivalent or a control gap.

## Reference receipt

    $ python3 -B c1-battery.py --tool .../pos-ref-preflight.py --only CLEAN --jobs 2 ...
    LEG CLEAN clean ok ok
    CLEAN=1/1 DEFECTS=0/15 BENIGN=0/6 BATTERY=PARTIAL      (real 17.8 s)

## Results: 18 new single-defect mutants

| id | defect (anchor → change) | partial legs run | result | killed by / verdict under full battery |
|---|---|---|---|---|
| N01 g05-wrong-cell | G05 scans the What cell (`cells[1]`) | CLEAN, D08 | KILLED | D08 |
| N02 g05-no-ufo-prefix | G05 pattern drops `.ufo` | CLEAN | **SURVIVED** | full: `BATTERY=PASS` → gap |
| N03 g05-no-missing-check | G05 `miss = []` | CLEAN, D08 | KILLED | D08 |
| N04 g05-exists-to-isfile | G05 `.is_file()` instead of `.exists()` | CLEAN | KILLED | CLEAN (live `.ufo/waves/round-34/measure/` is a directory) |
| N05 g05-cwd-relative | G05 resolves `pathlib.Path(w)` not `root/w` | CLEAN | KILLED | CLEAN (cwd is empty in the battery) |
| N06 exit-codes-swapped | main returns `2` for FAIL, `1` for ENV | CLEAN, D01, D12 | KILLED | D01, D12 |
| N07 env-exit-zero | main returns 0 when only ENV | CLEAN, D12 | KILLED | D12 |
| N08 usage-exit-1 | usage error exits 1 | CLEAN, D13 | KILLED | D13 |
| N09 env-counted-failed | summary FAILED includes ENV | CLEAN, D12 | KILLED | D12 |
| N10 skipped-empty | summary always `SKIPPED=none` | CLEAN | KILLED | CLEAN |
| N11 order-reversed | gate lines printed in reverse | CLEAN | KILLED | CLEAN |
| N12 crash-is-pass | crashing gate reported `PASS` | CLEAN | **SURVIVED** | full: `BATTERY=PASS` → gap |
| N13 no-work-cleanup | main never removes its own temp dir | CLEAN | **SURVIVED** | full: `BATTERY=PASS` → gap |
| N14 always-deletes-work | main removes a caller-supplied `--work` | CLEAN | **SURVIVED** | full: `BATTERY=PASS` → gap |
| N15 g01-env-becomes-fail | missing census script reported FAIL | CLEAN, D12 | KILLED | D12 |
| N16 none-fallback-dropped | empty sets print `""` not `none` | CLEAN | KILLED | CLEAN |
| N17 skip-printed-as-pass | `SKIP` lines printed as `PASS` | CLEAN | KILLED | CLEAN |
| N18 gate-names-faked | every gate line prints the name `gate` | CLEAN | **SURVIVED** | full: `BATTERY=PASS` → named limit |

Partial pass: KILLED 13/18, SURVIVED 5/18. Full battery on the 5 survivors (`out/full-survivors.txt`, exit 0):

    N02-g05-no-ufo-prefix      SURVIVED  legs_run=FULL  verdict=CLEAN=1/1 DEFECTS=15/15 BENIGN=6/6 BATTERY=PASS
    N12-main-crash-is-pass     SURVIVED  legs_run=FULL  verdict=CLEAN=1/1 DEFECTS=15/15 BENIGN=6/6 BATTERY=PASS
    N13-main-no-work-cleanup   SURVIVED  legs_run=FULL  verdict=CLEAN=1/1 DEFECTS=15/15 BENIGN=6/6 BATTERY=PASS
    N14-main-always-deletes-work SURVIVED legs_run=FULL verdict=CLEAN=1/1 DEFECTS=15/15 BENIGN=6/6 BATTERY=PASS
    N18-main-gate-names-faked  SURVIVED  legs_run=FULL  verdict=CLEAN=1/1 DEFECTS=15/15 BENIGN=6/6 BATTERY=PASS

Full battery wall time for five survivors: 1075 s total (host loaded; ~215 s each, `--jobs 2`).

## Survivors: classification and probes

None of the five is an equivalent mutant. Each changes behaviour the contract or the tool's own docstring states.
The reference discriminates each one on a direct probe, so the battery is the weak point, not the reference.

### N02 — G05 ignores `.ufo/` pointers → CONTROL GAP
- Why it matters: the live SCORECARD evidence cells do carry `.ufo/` pointers (e.g. `.ufo/waves/round-34/measure/`,
  `.ufo/waves/round-34/measure-a2/`), so G05's `.ufo` branch is live. The battery's `cap_pointers()` collects only
  `corpus|tools` (`c1-battery.py` line ~123), and no defect leg plants a missing `.ufo/` pointer.
- Probe (fixture root, SCORECARD row `` `.ufo/waves/gone.md` ``, `--only G05`):

      reference:  GATE G05 scorecard-paths FAIL 1 unresolved: .ufo/waves/gone.md   PREFLIGHT=0/1 FAILED=G05   rc=1
      N02:        GATE G05 scorecard-paths PASS 0 capability pointers resolve       PREFLIGHT=1/1 FAILED=none  rc=0

- Kill leg needed: D-leg that plants a missing `.ufo/…` pointer in a Capabilities evidence cell; expect `FAILED={G05}`, rc 1.

### N12 — a crashing gate is reported PASS → CONTROL GAP
- The reference's crash wrapper in `main()` is never exercised by any battery leg. No leg makes a gate raise.
- Probe: `corpus/lessons/round-900.md` created as a directory (glob matches; `read()` raises):

      reference:  GATE G03 lesson-gate FAIL gate crashed: IsADirectoryError: ...round-900.md   FAILED=G03   rc=1
      N12:        GATE G03 lesson-gate PASS gate crashed: IsADirectoryError: ...round-900.md   FAILED=none   rc=0

- Kill leg needed: D-leg with a directory named `corpus/lessons/round-<N>.md`; expect `FAILED={G03}`, rc 1, and the
  G03 detail `gate crashed`. Also one for G05 or G04 would test the wrapper on a second gate (INFERENCE: one suffices).

### N13 — main() leaves its own temp directory behind → CONTROL GAP
- Battery sets `TMPDIR` and `HYAKU_SCRATCH` to `work/tmp` for every leg, and `run_leg()` removes only the variant,
  cwd and tool directories, never `work/tmp`. So residue from the tool is never inspected (and the battery's final
  `rmtree(work)` removes it silently).
- Probe (same env the battery uses, `--only G07`, 1-gate fixture):

      reference:  residue=[]
      N13:        residue=['lane-preflight-odiez3bc']

- Kill leg needed: after each leg, `os.listdir(work/"tmp")` must be empty (or the default-work case must leave nothing).
  Note the rc is 1 in both probes only because the fixture lacks `tools/assimilate-rows.py`; irrelevant to residue.

### N14 — main() deletes a caller-supplied `--work` → CONTROL GAP
- The battery never passes `--work` to the tool (`run_leg()` argv carries only `--root`, `--skip`/`--only`, `--fleet`),
  so the contract's `--work` clause is unexercised. (Contract: "no write outside `--work`"; the reference never deletes it.)
- Probe (sentinel file inside a caller `--work` dir, `--only G05`):

      reference:  sentinel survives caller --work run? yes
      N14:        sentinel survives caller --work run? NO

- Kill leg needed: a leg that passes `--work <dir>` containing a sentinel and requires it to survive.

### N18 — every GATE line carries the same fake gate name → NAMED LIMIT (not a gap to close now)
- The claims file names this limit verbatim: "it does not check the gate names printed on the GATE lines (only ids,
  statuses and counts)". The judge (`judge()`) parses ids, statuses and counts only. Killing it would need a name
  check the freeze does not carry. Routed as a limit for the next round's battery, not a refutation.

## Kill-attribution calibration (observations)

- Four mutants (N04, N05, N10, N11, N16, N17) are killed only by CLEAN. Their kill depends on the live lane's contents
  (N04 needs a directory-valued `.ufo/` pointer in the golden; N05 needs cwd ≠ root). Those kills are real but thin:
  a lane edit that removes the pointer pattern would silently weaken them (INFERENCE from the golden contents).
- Summary and exit-code logic (N06–N09) is covered by D01/D12/D13 — good coverage of the exit contract.
- `main()`'s work-directory handling (N13, N14) has no battery coverage at all; the contract only says "no write outside
  --work", which the battery never checks.

## Gaps to route (for the next round's battery; the frozen battery is not edited here)

1. A leg with a missing `.ufo/…` pointer in a Capabilities evidence cell → kills N02 (G05 FAIL).
2. A leg that makes a gate raise (directory named `round-<N>.md`) → kills N12 (G03 FAIL `gate crashed`).
3. A leg that checks `work/tmp` is empty after each tool run → kills N13.
4. A leg that passes `--work <dir>` with a sentinel and checks it survives → kills N14.
5. (Named limit, not routed as a gap) GATE-name checking → N18.

## Host and tooling

- No installs or upgrades. No pacman. The operator's RULES file (`/home/vgpnk/.omp/agent/RULES.md`) read; no tool added.
- Git: no mutating commands; only `rev-parse` on the lane.
- Scratch `/fast/scratch/hyaku/chousa-r63/MutPre5Main/` removed before yield.
- Battery and tool runs used `--jobs 2`; no full battery was run on the 13 killed mutants (the partial kill is already
  definitive for them).

VERDICT: KILLED=13/18 survivors_that_are_gaps=4
