# MutC1Counter — mutation test of the frozen C1 counter (round 61, wave w1)

Seat: MutC1Counter (mutation-tester, leaf, no subagents). Lane writes: this report only.
Counter under test: `corpus/evidence/round61/c1-count.py`, sha256 `f1d8b6fd…cfff9ef` (matches the claims).

## Findings

1. **The frozen control set kills 10 of 23 counter mutants** (`k=10/23`). The other **13 survive every frozen control** — these are control gaps.
2. The 13 gaps are behaviours no frozen control exercises: exact exit codes (6), victim mtime / leaked-marker / healed-link checks (3), nothing-written clauses in big legs (2), the H16 traceback clause (1), and the seeded leg shuffle (1). Eleven scratch controls (§5) close all 13. **With them added, 23/23 mutants die.** They are candidates for L1; I did not touch the frozen controls.
3. The shuffle (amendment A1) is only defended by an order-keyed forger. The frozen controls are order-blind: unshuffled, a forger that knows the leg order passes the counter at three seeds (§4).
4. Baseline is sound: the unmutated counter reproduces all 20 rows of `controls/c1-controls.txt` exactly (rc, legs, failing list), and a repeat run is identical.
5. Removing the RSS clause (X01) flips base's H15 from fail to pass, so base's H15 failure rests on the RSS clause alone; its H14 failure is carried by another clause.

## 1. Mutant table

"Frozen" = the 20 rows of the frozen runner output plus its exit code. "Scratch" = §5 controls.

| id | mutant (one edit to the frozen counter) | frozen controls that change | scratch controls that change | status |
|---|---|---|---|---|
| X01 | drop RSS bound in big legs | M02-capsize, base, forge-token, naive-guard, runner | – | KILLED_FROZEN |
| X02 | drop victim mtime comparison (H10–H12) | – | E_touch | GAP → scratch |
| X03 | skip leaked-marker scan (H13) | – | E_leak1 | GAP → scratch |
| X04 | H09 accepts any non-zero exit (not only 2) | – | E_exit1, E_exit3, E_hang | GAP → scratch |
| X05 | H16 accepts any non-zero exit (not only 2) | – | E_exit1, E_exit3, E_partial1, E_leak1, E_hang, E_split | GAP → scratch |
| X06 | H19 accepts any non-zero exit (not only 2) | – | E_exit1, E_exit3, E_hang, E_split | GAP → scratch |
| X07 | P05 accepts any non-zero exit (not only 1) | always2 | E_exit3, E_trace2 | KILLED_FROZEN |
| X08 | H18 accepts any non-zero exit (not only 1,2) | – | E_exit3 | GAP → scratch |
| X09 | H17 drops the no-Traceback check | M13, base, forge-token, naive-guard, runner | E_trace2 | KILLED_FROZEN |
| X10 | skip seeded leg shuffle (A1) | – | E_forge | GAP → scratch |
| X11 | P01 drops golden-tree equality | noop0 | – | KILLED_FROZEN |
| X12 | P06 drops golden-tree equality | noop0 | – | KILLED_FROZEN |
| X13 | H08 drops golden-tree equality | M08, M11, noop0, runner | – | KILLED_FROZEN |
| X14 | P04 accepts any non-zero `--check` exit after tamper | – | E_check2 | GAP → scratch |
| X15 | H10–H12 drop the "healed" alternative | – | E_heal | GAP → scratch |
| X16 | H13 ignores the child's exit code | M03, base, forge-token, naive-guard, noop0, runner | – | KILLED_FROZEN |
| X17 | big legs drop the non-zero exit requirement | noop0 | – | KILLED_FROZEN |
| X18 | big legs drop the nothing-written check | – | E_partial1, E_leak1 | GAP → scratch |
| X19 | P02 drops golden-tree equality | noop0 | – | KILLED_FROZEN |
| X20 | P03 drops the NOPYC tools-listing check | M01, base, forge-token, naive-guard, runner | – | KILLED_FROZEN |
| X21 | H07 first probe accepts any non-zero exit (not only 2) | – | E_split | GAP → scratch |
| X22 | H16 drops the no-Traceback check | – | E_trace2 | GAP → scratch |
| X23 | H20 drops the nothing-written check | – | E_partial1, E_leak1 | GAP → scratch |

Result: `KILLED_FROZEN` 10; `GAP → scratch` 13 (all killed by scratch controls); `SURVIVES_ALL` 0.

## 2. Method and commands (scratch `/fast/scratch/hyaku/chousa-r61/MutC1Counter`, deleted before yield)

- Scratch copy of `tools/build-spans.py` (sha256 `1ed2650a…c80bf6`; `git hash-object` = `072415ad…`, the claimed base blob), `tools/capture-text.py`, and `corpus/evidence/round61/` incl. `controls/`. Lane files only read.
- Mutants: 23 exact string edits built by `harness.py`; each asserts its anchor count and `ast.parse`s the result. For each mutant, `controls/run-c1-controls.py` was copied with its `COUNTER` constant replaced by the mutant's absolute path, run with `--base` = the scratch base builder and `--seed 61001`. Compared: each row's rc, legs and failing list, `CONTROLS_UNEXPECTED`, and the runner exit.
- Baseline check (`analyze.py`): `ORIG frozen rows vs lane receipt c1-controls.txt: 20 rows, mismatches=[]`; `ORIG runner rc=0 ['CONTROLS_UNEXPECTED=0']`; `ORIG_vs_ORIG_b frozen_stable=True extras_stable=True`.
- Harness pass 1: `python3 -B harness.py` → `HARNESS_DONE 250`, wall 649.6 s (250 counter runs, 10 workers).
- Harness pass 2: `python3 -B harness2.py` → `derived action table entries: 23`, `ORIG.E_split LEGS=12/20 C1=FAIL`, `X21.E_split LEGS=13/20`, `X10.E_forge LEGS=20/20 C1=PASS`, `ORIG.E_forge LEGS=18/20 C1=FAIL`.
- Final: `python3 -B analyze.py` → `n=23 k_frozen=10 gaps_frozen=13 residual_survivors_after_extras=0`.
- Lane digests: `sha256sum claims.md` → `9afec8d4…ce0acec` (matches). Lane HEAD observed `9f32ac05…` (≠ freeze commit `2b0e17b2…`; ancestry not checked, not needed for this test; counter, builder and reference sha256s match the claims).
- Installs: none. Nothing written in the lane, `~/.local/bin`, or any PATH directory.

## 3. Gap families (why the frozen set misses them)

- **Exit codes not pinned** (X04, X05, X06, X08, X14, X21): frozen controls emit only exit 0 (noop0), exit 2 (always2), and the base/forge/naive variants. None exits 1 with an untouched tree on H09/H19/H07, exits 3 on H18, or exits 2 on `--check` drift.
- **Victim and leak checks** (X02, X03, X15): no control rewrites a victim's mtime with identical bytes, prints a leaked marker with a non-zero exit, or heals a link with exit 0.
- **Nothing-written clauses in big/huge legs** (X18, X23): no control writes output then exits non-zero for a big or 70 MiB capture.
- **H16 traceback clause** (X22): no control prints `Traceback` on exit 2 for OUTFILE.
- **Order** (X10): frozen controls are order-blind. Unshuffled, an order-keyed forger passes; shuffled, it fails (§4).

## 4. Order-keyed forger (X10) — the shuffle's only detector

- Logger run (base builder delegating, X10 counter, seed 61001) logged 23 invocations in 18 leg groups in plan order, matching counts `[1,1,3,1,2,3,1×12]`.
- Forger: reference builder run in-process (so it finds `capture-text.py` in the fixture's `tools/`), with per-invocation actions silent-exit-1, silent-exit-2 or delegate, chosen by global invocation index. The action table is derived from the logger run, so it is tailored to the unshuffled order (disclosed).
- Observed: `X10.E_forge LEGS=20/20 C1=PASS` (rc 0); `ORIG.E_forge LEGS=18/20 C1=FAIL` (P02, P06 fail).
- Seeds: `ORIG` at 61002 and 61003 → `LEGS=15/20 C1=FAIL`; `X10` at 61002 and 61003 → `LEGS=20/20 C1=PASS`.

## 5. Scratch controls (not frozen; candidates only; 11 in total)

E_exit1 (exit 1, no writes) · E_exit3 (exit 3, no writes) · E_trace2 (Traceback on stderr, exit 2) · E_partial1 (writes partial output, exit 1) · E_leak1 (copies cache contents into out, exit 1) · E_hang (sleeps when a capture is ≥100 MiB, else exit 1) · E_touch (reference builder after mtime-only touches of symlink targets) · E_heal (reference builder after unlinking symlinks) · E_check2 (reference builder with stale `--check` exit 2) · E_split (silent 1 when `DIR/spans` absent, silent 2 when present) · E_forge (§4).

Extra-control verdicts compare only: counter rc, the LEGS line, and per-leg pass/fail with rc (RSS, fixture paths and random names stripped). E_touch, E_heal and E_check2 wrap or copy the reference builder (sha256 `86d64c31…eccfd`).

## 6. Counter observations (not mutants)

- O1 (INFERENCE, not run): as root, `leg_h17` raises `SystemExit`, so the counter aborts with a message rather than returning 2 (`c1-count.py` lines 504–506). Run as vgpnk only.
- O2 (observed): a builder that writes nothing makes P04 raise `FileNotFoundError` on `out/spans` (`ORIG.E_exit1`: `LEG P04 CHECK fail counter exception FileNotFoundError …`). The verdict is still a fail; the detail is an exception, not a check. Harmless to the verdict.
- O3 (observed): X01 removes the RSS clause; base's H15 flips to pass. Base's H15 failure is therefore the RSS clause alone.

VERDICT: COUNTER_MUTANTS_KILLED=10/23 control_gaps=13
