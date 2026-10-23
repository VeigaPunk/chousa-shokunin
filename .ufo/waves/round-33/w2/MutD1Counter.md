# MutD1Counter — D1 v3 discrimination attack

## Scoped verdict: HOLDS

No tested control rejected by v2 was admitted by pristine v3: **64/64 paired negative-control comparisons preserved rejection** (32 distinct negative controls × two seeds). The additional metadata-only shortcut passed v2 twice and failed v3 twice. The citation-reading feasibility oracle passed both counters twice. This is a bounded discrimination result, not a round verdict or a C1 proof.

**Axes:** operability (bounded executable scoring and exact restoration); discrimination (previously rejected controls must remain below 132/132).

Evidence root `A=.ufo/waves/round-33/w2/MutD1Counter/`, relative to the lane. Scratch `S=/fast/scratch/hyaku/chousa-r33/w2/MutD1Counter`. Read `corpus/evidence/round33/claims.md:1-140`, including governing Design v2, before experimentation.

## Counter, controls, and seeds

- Unchanged v2 counter SHA-256: `8ec1a1ed44f1d3971a73eeace677cbedd0187563bea063ec6b680261dbb23c8a`.
- Unchanged v3 counter SHA-256: `6f362ece2e5e04c92212ee5a3547a69a6742c5658fd7ebc41688b68043e5a9fa`.
- Fresh generated seeds, in every table cell's order: **s1=1831745203958718229**, **s2=1783390705475396716** (`A/seeds.json`).
- Scored 34 distinct payloads: all 29 round-32 `CtlC2*` controls documented in the reports below; four additional distinct payloads from `w2/MutCounterC2v2/controls/`; and the D1 metadata shortcut from `w2/CriticAxis32/metadata-control.sh`.
- Three other w2 files are exact aliases, not extra payloads: `case-insensitive-gate.sh` = `weak-case-insensitive`; `whitespace-collapse-gate.sh` = `weak-whitespace-collapse`; `duplicate-only-gate.sh` = `duplicate-only`. Source/scored hashes and every source/target path are in `A/inventory.json`.
- Round-32 weak-reader scratch copies had been restored to base. Reconstructed grep-anywhere, skip-boundary, and file-only **only in this seat's scratch copies**, using the retained patch text. Their scored hashes exactly matched the historical report. Case-insensitive and whitespace-collapse came directly from the retained w2 snapshots. See `A/inventory.json`, historical reference W below, and `A/scored-gates/`.
- The three truth-fed output controls needed their helper/payload paths relocated at line 3. Copied the original emitter unchanged, generated private truth payloads with each unchanged counter's generator on the corresponding seed, and selected them with `D1_TRUTH`. These are intentionally white-box output-parser controls, not citation readers. Original implementation: `.ufo/waves/round-32/w2/MutCounterC2v2/emit-control-v2.py:8-17,33-38`. Inputs are retained as `A/truth-<v2|v3>-s<seed>.json`.

## Results table

Every number is the numerator of the actual label **`EXEMPT_AUDIT_MATCH=n/132`**. Pairs are s1, s2 for the fresh runs; original v2 pairs retain the historical seed ordering. Every fresh counter invocation exited **1**, except the oracle under both versions and metadata-only under v2, which exited **0**. No harness errors or gate timeouts occurred. See `A/runs-pristine.json` and the per-run stdout/receipts.

| Control | Original v2 | Fresh v2 | Pristine v3 | Original evidence |
|---|---:|---:|---:|---|
| statusblind-a: audit judgment statuses too | 120, 120 | 120, 120 | 120, 120 | S |
| statusblind-b: audit only judgment statuses | 84, 84 | 84, 84 | 84, 84 | S |
| statusblind-c: skip blocked-no-fetch | 120, 120 | 120, 120 | 120, 120 | S |
| weak-grep-anywhere | 114, 114 | 114, 114 | 114, 114 | W |
| weak-skip-boundary | 126, 126 | 126, 126 | 126, 126 | W |
| weak-case-insensitive | 126, 126 | 126, 126 | 126, 126 | W |
| weak-whitespace-collapse | 126, 126 | 126, 126 | 126, 126 | W |
| weak-file-only | 120, 120 | 120, 120 | 120, 120 | W |
| noreader-a: file exists | 78, 78 | 78, 78 | 78, 78 | R |
| noreader-b: exists and inside boundary | 84, 84 | 84, 84 | 84, 84 | R |
| noreader-c: anchor cell/non-URL | 60, 60 | 60, 60 | 60, 60 | R |
| noisy-findings | 60, 60 | 60, 60 | 60, 60 | N |
| noisy-observed | 60, 60 | 60, 60 | 60, 60 | N |
| noisy-duplicate | 24, 24 | 24, 24 | 24, 24 | N |
| duplicate-only | 96, 96 | 96, 96 | 96, 96 | N |
| alltrue-a: parseable U citation | 66, 66 | 66, 66 | 66, 66 | T |
| alltrue-b: parseable citation/all exempt statuses | 54, 54 | 54, 54 | 54, 54 | T |
| alltrue-c: nonempty U destination | 60, 60 | 60, 60 | 60, 60 | T |
| junk-random-labels | 52, 51 | 52, 48 | 52, 53 | J |
| junk-hop-id-shape | 60, 60 | 60, 60 | 60, 60 | J |
| junk-filename-shape | 66, 66 | 66, 66 | 66, 66 | J |
| junk-declared-id-shape | 102, 102 | 102, 102 | 102, 102 | J |
| junk-declared-id-member | 108, 108 | 108, 108 | 108, 108 | J |
| junk-generator-union | 120, 120 | 120, 120 | 120, 120 | J |
| junk-row-position | 86, 85 | 85, 85 | 85, 85 | J |
| junk-notes-shape | 60, 60 | 60, 60 | 60, 60 | J |
| junk-from-shape | 60, 60 | 60, 60 | 60, 60 | J |
| junk-random-valid-labels | 87, 83 | 86, 84 | 72, 75 | J |
| do-nothing | 0, 0 | 0, 0 | 0, 0 | B |
| w2-clean-exit | 0, 0 | 0, 0 | 0, 0 | O |
| w2-no-verdict | 0, 0 | 0, 0 | 0, 0 | O |
| w2-stray-unknown | 0, 0 | 0, 0 | 0, 0 | O |
| w2-oracle, feasibility only | 132, 132 | 132, 132 | 132, 132 | O |
| metadata-only, additional D1 attack | 132 reported | 132, 132 | **97, 90** | M |

Historical references, all lane-relative:

- **S:** `.ufo/waves/round-32/w1/CtlC2StatusBlindB/v2-rescore.md:31-38`.
- **W:** `.ufo/waves/round-32/w1/CtlC2WeakReaderB/v2-rescore.md:9-17,28-32`.
- **R:** `.ufo/waves/round-32/w1/CtlC2NoReaderB/v2-rescore.md:19-28`.
- **N:** `.ufo/waves/round-32/w1/CtlC2NoisyB/v2-rescore.md:22-29`.
- **T:** `.ufo/waves/round-32/w1/CtlC2AllTrueB/v2-rescore.md:9-15`.
- **J:** `.ufo/waves/round-32/w1/CtlC2JunkB/v2-rescore.md:17-28,44` (random controls also use independent Bash RANDOM).
- **B:** `.ufo/waves/round-32/w1/CtlC2DoNothingB/v2-rescore.md:38` explains the zero global-record score.
- **O:** `.ufo/waves/round-32/w2/MutCounterC2v2.md:27-37`.
- **M:** `corpus/evidence/round32/c2-count-v3.py:4-20`; shortcut implementation `.ufo/waves/round-32/w2/CriticAxis32/metadata-control.sh:28-37,41-58`.

The strongest rejected readers remain at 126/132, not admitted. V3's E11 and E12 negative classes remain discriminating. Counts for random-label controls are samples, not deterministic equality claims. Metadata-only's decline is the intended D1 repair effect, not a v2 rejection that v3 reversed.

Record-level rejection stayed active: do-nothing and clean-exit reported `gate-rc=0,drift-summary-lines=0`; no-verdict reported `drift-summary-lines=0`; stray-unknown reported `stray-finding-hops=1`. Their original output defects were not masked by stale truth IDs: private seed/version-specific truth payloads supplied all 132 known ids. Evidence: those controls' `A/*-pristine-s<seed>.json` receipts and `record_fails` in `A/runs-pristine.json`.

## Assigned mutation probe

**Mutant:** one behavior-bearing line in the scratch v3 counter, original line 378:

```python
# pristine
            got = sorted(named.get(hid, []))
# mutant: collapse finding multiplicity
            got = sorted(set(named.get(hid, [])))
```

**Expected detector:** the known-defective duplicate-only gate must be rejected: counter exit 1, score below 132, gate exit 1, no timeout, and successful record checks. This is a negative-control-rejection detector; its baseline is successful when the defective gate is rejected. It does not mislabel a failed candidate baseline as a killed mutant.

Ran the same bounded v3 command and duplicate-only gate on the same two seeds in pristine, mutated, and restored phases. Only phase-specific receipt/output names and the deliberate counter bytes differed.

| Seed | Pristine output / exit | Mutated output / exit | Restored output / exit | Rejection expectation | Verdict |
|---|---|---|---|---|---|
| 1831745203958718229 | 96/132 / 1 | 132/132 / 0 | 96/132 / 1 | PASS → FAIL → PASS | **KILLED** |
| 1783390705475396716 | 96/132 / 1 | 132/132 / 0 | 96/132 / 1 | PASS → FAIL → PASS | **KILLED** |

Actual labels are `EXEMPT_AUDIT_MATCH=96/132`, `EXEMPT_AUDIT_MATCH=132/132`, and `EXEMPT_AUDIT_MATCH=96/132`. Gate exits stayed 1 and record checks stayed successful. Evidence: `A/duplicate-only-v3-<pristine|mutated|restored>-s<seed>.stdout.txt`, `.json`, and `.run.json`; aggregate `A/summary.json` and `A/runs-{mutated,restored}.json`. The summary's rejection-detector exit values are derived from those recorded runs, not additional process invocations.

Before/restored SHA-256: `6f362ece2e5e04c92212ee5a3547a69a6742c5658fd7ebc41688b68043e5a9fa`.
Mutated SHA-256: `4ff6a815cc79a39f193320b97f00a9557d4712e095b4a11c7e3747a719131ee5`.
The exact mutant is retained as `A/mutant-counter.py`.

Restoration ran in `finally`, including if the mutated detector failed:

```text
timeout 20s cp S/counters/c2-count-v3.pristine S/counters/c2-count-v3.py
```

Actual exit **0**; `exact_bytes_restored=true` (`A/counter-restoration.json`). Restored behavioral runs followed that byte restoration. All 34 scratch gate copies were also returned to their exact initially copied bytes after preserving their scored snapshots; this includes the three rebuilt weak readers and three relocated launchers (`A/restoration.json`). Every original control source remained unchanged by hash.

## Commands and complete evidence

Setup actually ran, exit **0**:

```text
timeout --kill-after=3s 30s prlimit --nproc=2000 --as=4000000000 --fsize=1048575 -- python3 S/setup.py
```

Main batch actually ran, exit **0**, elapsed **230.218 s**:

```text
timeout --kill-after=5s 900s prlimit --nproc=2000 --as=4000000000 --fsize=1048575 -- env C1_TMP=S/tmp C2_TMP=S/tmp TMPDIR=S/tmp python3 S/rescore.py
```

Its actual final line was `RUNS=136 HARNESS_ERRORS=0`. Four finite foreground workers were joined. Mutated and restored batches used that same wrapper plus `--only duplicate-only --versions v3 --phase mutated` or `--phase restored`; each exited **0** and printed `RUNS=2 HARNESS_ERRORS=0`. Thus **140 scored counter invocations**, all recorded, including the intentionally admitted mutant outputs.

Every individual scoring command used this actual shape (all expansions are stored verbatim in `.run.json`):

```text
timeout --signal=TERM --kill-after=3s 90s prlimit --nproc=2000 --as=4000000000 --fsize=1048575 -- python3 S/counters/c2-count-<v2|v3>.py --gate S/gates/<control>/tools/research-gate.sh --seed <seed> --receipt A/<control>-<version>-<phase>-s<seed>.json
```

Cwd was S. C1_TMP/C2_TMP/TMPDIR were `S/tmp`, outside every gate lane root `S/gates/<control>`. GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE were absent from subprocess environments. `D1_TRUTH` named the private seed/version payload. The counters themselves scrubbed CHOUSA_* variables (`c2-count-v3.py:341-343`). Stdout and stderr went directly to the adjacent `.stdout.txt` and `.stderr.txt` files, never through head/tail.

For every table control and seed, `A/<control>-<version>-pristine-s<seed>.json` is the receipt; `.stdout.txt` is actual complete counter output; `.run.json` holds the exact argv/environment, PID/process group, exit code, paths, and before/after hashes. `A/runs-pristine.json` aggregates all 136 runs (SHA-256 `70843cdf91c98c21b1fd9ac9ef855635485d74059b5b8b25564768d0fff986b6`). `A/restoration.json` SHA-256 is `c34e0b355ee4d2e9819a6254cf7878e65495d8b5adafbd80032ec373bcac14e1`. Reproduction drivers are retained as `A/setup.py` and `A/rescore.py`; replay requires restoring the scored gate snapshots/layout first, because scratch gate copies were deliberately restored.

## Bounds and limits

`timeout 20s df -h /fast` exited 0 before setup: 179G available, 78% used. All individual invocations had a 90 s wall bound, 4 GB address-space cap, nproc=2000, and file-size cap below 1 MiB. All 140 recorded process groups were reaped; none required residual-group cleanup. Largest accounted artifact: `runs-pristine.json`, 340237 bytes; all 749 accounted evidence files were under 1 MiB (`A/cleanup-evidence.json`).

No installs, network, subagents, background jobs, lane production/index/jj writes, or fleet/sibling edits. No landed gate or C1 counter was executed; C1 and other repair/source/knowledge/quality tasks are outside this probe. Two seeds and this retained control set do not prove discrimination against every possible shortcut. This seat neither integrates nor ships changes. Its scoped D1 attack is complete.
