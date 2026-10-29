# CritC1Skip — round 63 wave w1 — critic on `--skip`/`--only` (C1)

Scope: the reference candidate `corpus/evidence/round63/controls/pos-ref-preflight.py` (sha256 prefix `07683086fd6c6b41`,
matches claims.md) and the C1 "The tool's contract" text in `claims.md` (prefix `6c46b2cc193e1a44`), against the frozen
`corpus/evidence/round63/c1-battery.py` (prefix `0073fba73c89aaf8`, matches). The lane was read only. Probes ran on a
golden copy (lane minus `.git`) in `/fast/scratch/hyaku/chousa-r63/CritC1Skip`, deleted before yield. No installs.
Lane HEAD is `c8bfcc6`; `git merge-base --is-ancestor 62876ef... HEAD` succeeds, so the freeze commit is intact.

## Findings

1. **A run that selects zero gates exits 0 (defect; the claim permits it, the battery does not catch it).**
   The loop skips every gate, so `ran=[]`, `failed=[]`, `envs=[]`, and `return 1 if failed else (2 if envs else 0)`
   returns 0. The summary still prints `PREFLIGHT=0/0`.
   The claim's rule "Exit 0 when every gate that ran passed" is vacuously true with no gate run. That contradicts the
   docstring's own principle, "a gate that could not run is never counted as a pass".
   Zero-gate inputs measured (all exit 0):
   - `--skip G01,G02,G03,G04,G05,G06,G07,G08` → `PREFLIGHT=0/0 FAILED=none ENV=none SKIPPED=G01,...,G08`, EXIT=0
   - `--only G01 --skip G01` → `PREFLIGHT=0/0 ... SKIPPED=G01,...,G08`, EXIT=0
   - `--only G08 --skip G08` → `PREFLIGHT=0/0 ... SKIPPED=G01,...,G08`, EXIT=0
   - `--skip G08 --only G08` → `PREFLIGHT=0/0 ... SKIPPED=G01,...,G08`, EXIT=0

2. **`--skip` beats `--only`.** Code: `if (only and gid not in only) or gid in skip`. A gate named in both is SKIP.
   Measured: `--skip G08 --only G01` runs G01 (PASS) and skips G02–G08, `PREFLIGHT=1/1`, EXIT=0. The claim text does
   not state this precedence.

3. **An empty `--only` silently widens to all gates.** `idlist("")` returns `[]`, which is falsy, so `only` is ignored.
   Measured: `--only "" --skip G08` and `--only , --skip G08` both run G01–G07 → `PREFLIGHT=7/7 FAILED=none ENV=none
   SKIPPED=G08`, EXIT=0. An explicit empty selection should not mean "all".
   INFERENCE (code, not run): `--only ""` with no `--skip` runs G08 too (minutes).

4. **Duplicate ids are accepted and count once.** `--skip G08,G08` → `PREFLIGHT=7/7 ... SKIPPED=G08`, EXIT=0.
   `--only G01,G01 --skip G08` → `PREFLIGHT=1/1`, EXIT=0.

5. **Ids are exact upper case; unknown ids exit 2 before any gate runs.**
   `--skip g08` → stderr `lane-preflight: unknown gate id for --skip: g08`, EXIT=2, no GATE or PREFLIGHT line.
   `--skip G99` → same, EXIT=2 (the battery's D13 leg).
   INFERENCE (code): `--only g08` takes the same `idlist` path, so it exits 2.
   INFERENCE (code, not run): `idlist` strips only spaces (`.replace(" ", "")`), so a tab in an id is an unknown id, exit 2.
   Spaces are stripped: `--skip " G08 "` → `PREFLIGHT=7/7`, EXIT=0.

6. **Claim-text gaps.** `claims.md` says "a gate not selected: `GATE <id> <name> SKIP`" but does not say:
   (i) what a run with zero selected gates means; (ii) that `--skip` wins over `--only`; (iii) that an empty or comma-only
   `--only` selects all gates; (iv) that repeated ids count once. The lowercase case is covered only by implication through
   "unknown gate id: no summary line" (exit 2).

## Battery coverage

- Frozen battery on the reference: `CLEAN=1/1 DEFECTS=15/15 BENIGN=6/6 BATTERY=PASS`, EXIT=0 (37.7 s wall). The reference
  exits 0 on zero gates and still passes, so a zero-gate exit-0 tool is not caught.
- No frozen leg selects zero gates. CLEAN is `--skip G08` (seven gates run), D13 is `--skip G99` (exit 2 before any gate),
  D14 is `--only G03` (one gate), and the rest are `--skip G08`. The battery has no `--only ""` leg either.
  Answer to the CLEAN question: a tool that exits 0 on zero gates still runs seven gates in CLEAN, so it cannot be
  caught there. `battery_catches=no`.
- Scratch copy of the battery with two added legs (scratch only, frozen file untouched):
  - Z01 `--skip G01,...,G08`, expect rc=2 and no PREFLIGHT line.
  - Z02 `--only G01 --skip G01`, expect rc=2 and no PREFLIGHT line.
  These use the existing `usage=True` path of `judge()`, so no judge change is needed.
  Run against the reference: `LEG Z01 defect FAIL rc=0 (want 2, no PREFLIGHT line)`,
  `LEG Z02 defect FAIL rc=0 (want 2, no PREFLIGHT line)`, so the battery would read FAIL.
- Scratch variant of the reference with the zero-gate rule (below): Z01 ok, Z02 ok, CLEAN ok. The unmodified frozen
  battery on that variant: `CLEAN=1/1 DEFECTS=15/15 BENIGN=6/6 BATTERY=PASS`, EXIT=0. So the rule regresses no frozen leg.
- The zero-gate variant's probes: all-skip → `no gate selected`, EXIT=2; `--only G01 --skip G01` → EXIT=2;
  `--skip G08 --only G08` → EXIT=2; `--only ,  --skip G08` → `--only names no gate`, EXIT=2; `--skip G08 --only G01`
  → `PREFLIGHT=1/1`, EXIT=0.

## Three-line rule the claims file should state (zero-gate case)

1. A run that selects no gate (every id skipped by `--skip`, by `--only`, or both; `--skip` wins over `--only`; an empty or
   comma-only `--only` selects none, not all) exits 2 with no PREFLIGHT line and stderr `lane-preflight: no gate selected`.
2. Exit 0 needs `PREFLIGHT=n/n` with n ≥ 1, `FAILED=none` and `ENV=none`; a summary with `run=0` never exits 0.
3. Ids are exact upper-case `G01`–`G08`; a repeated id counts once; an unknown id (lower case included) exits 2 before any
   gate runs.

**Battery needs a leg: yes.** Add at least Z01 (all ids skipped, expect rc 2, usage) and Z02 (`--only G01 --skip G01`,
expect rc 2, usage), and optionally Z03 (`--only ""`, expect rc 2, usage). The judge needs no change. The frozen
`c1-battery.py` must not change this round, so this is a named limit: the zero-gate defect is uncovered by the frozen
battery and goes to the next round's battery as a supplement. The L1 can still land the rule in the tool, which the
frozen battery accepts (verified above).

## Limits of this critic run

- Only the probes above were executed. Lines 4–5 (lowercase `--only`, tab ids) and Z03 were code-read or not run, and are marked INFERENCE.
- `tar` warned about future mtimes in `.ufo/` while copying the golden tree. The contents were copied, and no gate result depended on mtimes.
- The scratch variant is a critic probe, not a landed change. The L1 owns the landed tool.

VERDICT: ZERO_GATE_EXIT=0 battery_catches=no
