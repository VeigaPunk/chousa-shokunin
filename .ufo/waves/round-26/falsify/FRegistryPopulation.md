# FRegistryPopulation — C3 frozen r24+ five-entry population re-run and adjudication

Seat `ChousaR26R.FRegistryPopulation` (scout, author-lane advice only; no outside judge/SHONEN claim).
Axis judged: calibration. Date 2026-10-21.

## Verdict

**Not falsified.** On the immutable target, `C3_POP_R24PLUS_CLEAN=5/5` reproduces, with **zero C3
findings**. Adjudication: every one of the 10 (entry, S-id) links is a true negative. The base
registry has a `mined` row for each id, and each row's `used-by` lists the exact repo-relative
entry path. Each `verified-at:` carries text after its date. The clean result is **not vacuous**:
all ten links fire when mutated (10/10 sweep), and nine targeted mutants behave as the spec
predicts. The only finding in the population run is the legacy r25 `META_RECHECK_ROOT_PARENT` (info).
It is a true positive and is not C3. Frozen inputs were not changed.

## Revisions and inputs observed

- Target: `0e9784bd52eca456b24d0bc40921480a47f91a2b` (from `round26-measured-revision.json`; the lane HEAD at the time of the run was the same commit).
- Claim base: `ba3333254dd337658a4f25e7a9471f9cf4e4567e`.
- Sandbox: `/tmp/chousa-r26-falsify-FRegistryPopulation/{tree,base}` via `git archive <rev> | tar -x`.
- Archived target sha256 values all match the measured-revision JSON:
  `tools/research-gate.sh c2c813f1…abc6`, `round26-measure.sh b51c96f6…fb53`,
  `round26-claims.md dcbe2b5f…f507f1c`, `corpus/SOURCES.md 8308e629…aa9`,
  `round26-registry-oracle.py 6b2d135c…1d78`, `round26-registry-differential.sh 852a7648…76e9`.
- Frozen registry, as used by the probe: `git show ba333325:corpus/SOURCES.md`, sha256 `bfd47b5d8d34b0bb8ef5bfed4390996edd6bbac5d22086eb1c5042ade9f91532`.

## Commands and exits

| # | Command (cwd sandbox) | Exit | Result |
|---|---|---|---|
| 1 | `bash corpus/evidence/round26-measure.sh $D/tree c3` | 0 | `C3_CONTROLS_CAUGHT=5/5`, `C3_POSITIVE_CLEAN=1/1`, `c3 pop24 rc=0`, `C3_POP_R24PLUS_CLEAN=5/5` |
| 2 | `bash corpus/evidence/round26-measure.sh $D/base c3` (expected negative control) | 0 | all controls `MISS rc=2`, `0/5`, `0/1`, `pop24 rc=2`, `0/5` — matches the "before" prediction (flag absent → exit 2); not a regression |
| 3 | `bash tree/tools/research-gate.sh verify-metadata pop24/corpus/knowledge --root pop24 --registry pop24/SOURCES.md` (full, unfiltered) | 0 | 5× `verdict=clean`; sole finding `META_RECHECK_ROOT_PARENT severity=info … citation-chain-fidelity-r24.md`; `RESEARCH_GATE: CLEAN (entries=5 complete=5 findings=1 drift=0)` |
| 4 | `python3 tree/corpus/evidence/round26-registry-oracle.py pop24/corpus/knowledge --root pop24 --registry pop24/SOURCES.md` | 0 | all five `[]` |
| 5 | `python3 $D/myoracle.py …` (my own oracle, written only from the claims-file C3 spec and the spec-v1 correction; sandbox only) | 0 | all five `findings=none` |

The three-way agreement (gate, in-tree oracle, seat oracle) is zero C3 findings.

## Finding-by-finding adjudication (population run)

| Finding | Entry | Adjudication |
|---|---|---|
| `META_RECHECK_ROOT_PARENT` (info) | citation-chain-fidelity-r24.md | **True positive, outside C3.** Its `recheck:` literally contains `--root ..`. This is the r25 screen and matches the base violation that QUALITY 13 records. Severity is info, so the verdict stays `clean` and C3 is unaffected. |
| *(no C3 findings)* | all five | Hand-checked each link against base `SOURCES.md` lines 11–43 (table below). No false negatives found. |

| Entry | S-ids in `source:` | Row status | `used-by` contains exact `corpus/knowledge/<entry>` | `verified-at:` text after date |
|---|---|---|---|---|
| citation-chain-fidelity-r24.md | S005, S003 | mined, mined | yes (L15), yes (L13) | yes |
| claim-support-states-r24.md | S006, S007 | mined, mined | yes (L16, L17) | yes |
| contextual-source-admission-r24.md | S002, S004, S003 | mined ×3 | yes (L12, L14, L13) | yes |
| json-delimiter-r24.md | S001, S013 | mined, mined | yes (L11, L23) | yes |
| metadata-screen-r25.md | S029, S033 | mined, mined | yes (L39, L43) | yes |

Base registry: no duplicate S-ids, and no S-id rows below `## Paths` (line 45).

## Non-vacuity attacks (isolated fixtures under `$D/mut`, `$D/sweep`; frozen inputs copied, never edited)

**Per-id sweep (`SWEEP=10/10`).** Each of the 10 distinct ids was flipped to `queued` one at a time.
Every run exited 1, `META_SOURCE_NOT_MINED` fired on exactly the citing entries (S003 fired on
both of its entries), and no other C3 finding appeared. This covers first-, second- and
third-position ids, including ids after URL fragments, `→`, and backtick parentheticals.

Targeted mutants:

| Mutant | Exit | Finding | Spec-expected? |
|---|---|---|---|
| m1 S005 → queued | 1 | `META_SOURCE_NOT_MINED` ccf/S005 | yes |
| m2 S003 used-by drops ccf | 1 | `META_SOURCE_USEDBY_MISSING` ccf/S003 only (contextual stays clean) | yes |
| m3 S013 row deleted | 1 | `META_SOURCE_ROW_MISSING` json/S013 | yes |
| m4 S029 used-by `corpus/other/metadata-screen-r25.md` (same basename, other dir) | 1 | `META_SOURCE_USEDBY_MISSING` meta/S029 | yes (spec-v1 exact path) |
| m11 S033 used-by bare basename | 1 | `USEDBY_MISSING` meta/S033 | yes (spec-v1) |
| m5a duplicate S006 `queued` row **before** the mined row | 1 | `NOT_MINED` css/S006 | yes (first row wins) |
| m5b duplicate S006 `queued` row **after** | 0 | clean | yes (first row wins) |
| m7 S013 used-by `./corpus/knowledge/json-delimiter-r24.md` | 0 | clean | yes (leading `./` normalized) |
| m8 css `verified-at: 2026-10-19` (bare) | 1 | `META_VERIFIED_AT_BARE` css | yes |
| m10 json `source:` id moved to a continuation line as `S999` | 1 | `ROW_MISSING` json/S999 | yes (continuation lines are read) |
| m9 header `used-by` → `users` | 2 | stderr `metadata registry has no table with id, status, and used-by columns` | yes (exit 2) |

My oracle produced the same per-entry finding sets for every mutant except m9, which is out of
the oracle's scope.

## Calibration observations (not defects in the frozen result)

1. **The relation depends on `--root`.** The same five entries and the same registry produce `DRIFT findings=12 drift=11` in two cases:
   - with `--root $D` (the parent directory; m6);
   - in a simulated fleet-root layout (`--root fleet` with entries under `fleet/chousa-shokunin/`).

   In both cases all 11 links report `USEDBY_MISSING`. This is the spec-v1 behaviour (paths are taken relative to `--root`), but it means the population figure holds only when root is the lane root. QUALITY 13's role name for recheck roots, `"$SHOKUNIN_ROOT"`, is the fleet root, and using it here would give 11 false positives. The r26 entries' recheck lines say `cwd=lane root; … --root .`, which states the assumed layout. Low risk; documentation already covers it.
2. **Entry outside `--root` (m12).** When `--root` points at an unrelated directory, the gate reports `USEDBY_MISSING` for every link instead of a distinct "entry outside root" diagnostic. It fails closed, so this cannot create a false negative. It is a diagnostic-quality note only.
3. **Wider context (not graded by C3).** Frozen five against the target's own `corpus/SOURCES.md`: CLEAN rc=0, same result. Whole target corpus (32 entries) with `--root . --registry corpus/SOURCES.md`: rc=1.
   - The 3 drift entries come from legacy `META_RECHECK_ABSENT`: archives-verified-r9, audit-r11, gate-baseline-r8.
   - There are 24 legacy `META_SOURCE_NO_ROW_ID` info findings. Legacy entries are outside criterion 6.
   - All three r26 entries are clean. My oracle confirms their ids (S034–S039 and S029) have no findings.

   A date or registry metadata result is not citation support or truth (QUALITY 8).
4. **m9 output.** After the one-line error, the refusal prints the full usage text. This is cosmetic, and the exit code is correct.

## Remaining unknowns

- Neither oracle exercises CRLF or Unicode-whitespace variants of `used-by` separators in the frozen registry; the frozen rows have none, so the population result does not depend on them.
- I did not run selftest, build, lint, `--drift` or the 8 MiB probe; these were not authorized for this seat. L1 owns the integrated verification.

Tools installed or updated: none. No production, lane-index, jj, or frozen-input writes; only this report.
