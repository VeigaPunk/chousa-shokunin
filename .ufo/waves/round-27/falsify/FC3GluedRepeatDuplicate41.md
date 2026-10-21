# FC3GluedRepeatDuplicate41 — falsify C3 control `glued-repeat-duplicate`

Target: `corpus/evidence/round27-regressions.py:157` at `dd72641e574679c4f7882dd43de072b4c8892d6f`.
Gate: `tools/research-gate.sh` sha256 `ca39d14d…992f84` (matches the required gate hash; lane working tree identical).
Base for mutation: `64eec5d4…` scanner body (sha256 of base gate `c2c813f1…abc6`).
Sandbox: `/tmp/chousa-r27-falsify-FC3GluedRepeatDuplicate41` (archive of dd72641e; base read via read-only `git archive`). Lane files, index, and git state untouched.

## Verdict

- **Named control `glued-repeat-duplicate`: HOLDS.** Expectation derives from the contract, is independent of gate code, and reverting the targeted fix makes it fail for the intended reason. No landed counterexample found in the S-id class.
- **Surrounding S-id control group as a calibration set: FALSIFIED for sufficiency.** Three mutants that violate the governing contract pass all seven S-id controls (digit length, punctuation boundaries, UTF-8 locale). Each yields a false CLEAN at the CLI where landed yields DRIFT. Axis: calibration (fail-open) and operability (control group locale-blind). Freshness not touched.

## (1) Expectation provenance — HOLDS

- Control literal: `('glued-repeat-duplicate', 'ref S002S002 and S002', 1, 1)`, with registry `S002 | queued`. Expected: rc 1, exactly one `META_SOURCE_NOT_MINED … source_id=S002`.
- Contract: C3 "standalone ASCII S-ids without invented or duplicate occurrences" (`round27-claims.md:15`); spec-v1 "`S` + three or more digits (standalone ASCII alphanumeric/underscore boundaries)" (`round26-claims.md:133-135`).
- Independent oracle (`work/fn_diff.py`, `(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])`, no gate code) returns exactly one id for that input. Literal `1` is consistent.

## (2) Mutation — control fails for the intended reason — HOLDS

- M1 = landed gate with `metadata_registry_check_source` replaced by the base body (regex + `source_scan=${source_scan#*"$source_match"}`). `sed`-extracted function blocks are identical (`diff` empty); `bash -n` OK.
- Control replicated verbatim (`work/subset_runner.py`: same fixture text, env with `LC_ALL=C`, same patterns):
  - `MISMATCH glued-repeat-duplicate exit=1 count '^FINDING META_SOURCE_NOT_MINED…source_id=S002': 3 != 1; count '^FINDING META_SOURCE_': 3 != 1`
  - Exit 1 matches expectation; stderr empty; three findings emitted. Not a parse or setup error.
- Mechanism: the literal `" S002"` first occurs inside glued `S002S002`; the rescan leaves `S002 and S002`, `^` re-anchors and invents an id, then the real occurrence is re-found.
- Same-family M1 failures: `glued-before-terminal` (invented S002, exit 1≠0), `glued-missing-before-terminal` (1≠0), `nonstandalone-duplicate` (2≠1). `two-real-occurrences` and `adjacent-real-ids` pass.
- Function-level base scanner vs oracle (3055 cases, C env): 1 mismatch, the control input itself. The random generator seldom produces this shape, so the hand control is the sensitive probe.

## (3) Counterexamples and vacuity

Landed gate: 0 mismatches over 3055 synthetic values (55 hand + 3000 random) in C and UTF-8 locales. CLI stress: 2 MB glued token → exactly 1 finding; 20,000 real standalone `S002` → exactly 20,000 findings. Landed passes all seven S-id controls under both `LC_ALL=C` and `LANG=en_US.UTF-8`.

Mutants (each a single-rule change in a sandbox copy of landed):

| mutant | change | 7-control S-id subset | function diff vs oracle | fail-open CLI case |
|---|---|---|---|---|
| M2 | exact `S[0-9]{3}` | 7/7 PASS | 345 mismatches (`S0021`, `S0002`) | `source: S0021`: landed rc1 ROW_MISSING; M2 rc0 NO_ROW_ID (CLEAN) |
| M4 | boundaries = space/comma only (`grep -oE '[^ ,]+'`) | 7/7 PASS | 581 mismatches (`(S002)`, `S002:`, `S002;`, …) | `source: (S002)`: landed rc1 NOT_MINED; M4 rc0 (CLEAN) |
| M5 | drop explicit `LC_ALL=C` on grep | 7/7 PASS in C and UTF8 | C 0; UTF8 115 mismatches (`éS002`, `S002é`, `٢S002`) | `LANG=en_US.UTF-8`, `source: éS002`: landed rc1 NOT_MINED; M5 rc0 (CLEAN) |
| M6 | dedupe per id | 6/7 PASS: glued-repeat passes, `two-real-occurrences` FAILS 1≠2 | 19 mismatches (`S002,S002`, `S002-S002`) | `S002,S002`: landed 2 findings; M6 1 finding (both rc1) |
| M3 | boundary-blind `grep -oE 'S[0-9]{3,}'` | 5/7 FAIL | 871 mismatches | — |

Why the group is blind: every S-id fixture uses three-digit ids with only space, comma, underscore, or letter neighbours. `run()` hard-codes `LC_ALL=C`, so no locale case exists. Dedupe is caught only by `two-real-occurrences`; `glued-repeat-duplicate` alone does not reject a dedupe fix.

Contract resolution for M2: `round26-claims.md:97` (`\bS[0-9]{3}\b`) is superseded by the spec-v1 correction at `:133-135` ("three or more digits"), and `registry-link-r26.md:29` agrees. Landed follows `{3,}`, so landed is correct and M2 violates the contract. Line 97 is a stale doc contradiction.

Scope note on locale: the explicit `LC_ALL=C` prefix on the grep is what makes tokenization ASCII. The function-level `local LC_ALL=C` does not reach the child process when the outer environment has no `LC_ALL` (checked with `env -i`), so the prefix is load-bearing and must stay.

## Commands and exit codes (sandbox only)

- `python3 work/subset_runner.py work/L.sh C` → `mismatches=0 of 7`, exit 0. Same under `UTF8`, exit 0.
- `python3 work/fn_diff.py work/L.sh C` → `mismatches=0`, exit 0. `… UTF8` → `mismatches=0`, exit 0.
- `python3 work/fn_diff.py work/B0.sh C` → `mismatches=1` (control input: 3 findings vs 1).
- `python3 work/subset_runner.py work/M1.sh C` → `mismatches=4 of 7`, exit 1 (control: count 3≠1, exit 1 as expected).
- M2 subset → 0 of 7, exit 0. M4 → 0 of 7, exit 0. M5 → 0 of 7 (C), 0 of 7 (UTF8), exit 0. M6 → 1 of 7, exit 1. M3 → 5 of 7, exit 1.
- CLI single runs (synthetic `root/`, `--registry`, `env -i`): rows in the table above. Landed rc1 in every case; each mutant rc0 where listed.
- Install/update record: none. No pacman, uv, npm, or cargo. Tools: bash 5.3.20; `/usr/bin/grep` = GNU grep 3.12-modified (pacman `grep 3.12-2`, the one the gate uses via subprocess); python3; read-only `git archive`/`show`. The interactive tool shell exposes a builtin `grep` (pi-uu-grep 0.2.0) that the gate subprocess does not see (`bash -c 'type -t grep'` → file).

## Limits

- Random corpus is synthetic token strings (3000) plus 55 hand cases; not exhaustive.
- The seven-control check is a verbatim replica of the regression script's S-id group, not the script. No other group was run; no full `--selftest`.
- M1 is the base scanner function pasted into the landed gate, not the full base gate. The r26 unsafe long-token input was not run.
- Observation, not a correctness failure: a 2 MB glued token takes 7.8 s on landed (48 KB takes 35 ms). No resource claim is made; the 8 MiB ceiling was not tested.
- If the lane later adopts exact-three digits, M2 becomes correct and landed would be wrong on `S0021`-style rows. The contract text should be fixed first.

## Author-lane advice (not an outside admission)

1. Add S-id controls: `ref S0021` → ROW_MISSING (pins `{3,}`); `see (S002).` or `S002:` → NOT_MINED (ASCII punctuation boundary); `éS002` run with `LANG=en_US.UTF-8` and `LC_ALL` unset (the locale case `run()` currently forces away).
2. Correct or annotate `round26-claims.md:97` (`\bS[0-9]{3}\b`) as superseded by the `:133-135` spec-v1 text.
3. Keep `glued-repeat-duplicate` as is. It is the correct discriminator for the rescan defect. Dedupe coverage belongs to `two-real-occurrences`.
