# CtlDeterminism31 — counter harness integrity

Axes: determinism, truth isolation, device independence, exit/parser integrity. Frozen base gate SHA-256: `ac1315ddaa12e79b68069d1a9866b9b1b55e3a43efef3ba0cb5ca5e665835765`.

All artifacts below are under `.ufo/waves/round-31/controls/CtlDeterminism31/`. `c1-` and `c2-` denote the respective frozen counters. Only the base gate (through a stat-only observer that execs the unchanged gate) and trivial output stubs ran; no candidate implementation ran.

## Controls and receipts

| Control | Counter | Seed(s) | Score | Receipt |
|---|---|---|---|---|
| Base; ten seeds | C1 / C2 | 31–40 | 50/120 each run | [C1 summary](CtlDeterminism31/c1-primary-summary.json), [C2 summary](CtlDeterminism31/c2-primary-summary.json); enumerate all per-seed receipts |
| Base; identical-seed repeat | C1 / C2 | 31 twice | 50/120 each | [C1](CtlDeterminism31/c1-base-repeat.json), [C2](CtlDeterminism31/c2-base-repeat.json) |
| Base; different TMPDIR | C1 / C2 | 31 | 50/120 each | [C1](CtlDeterminism31/c1-base-fast-tmpdir.json), [C2](CtlDeterminism31/c2-base-fast-tmpdir.json) |
| Constant supported, pristine | C1 / C2 | 31 | 42/120; 40/120 | [C1](CtlDeterminism31/c1-mutation-pristine.json), [C2](CtlDeterminism31/c2-mutation-pristine.json) |
| Supported then invalid, duplicate mutant | C1 / C2 | 31 | 42/120; 40/120 | [C1](CtlDeterminism31/c1-mutation-mutated.json), [C2](CtlDeterminism31/c2-mutation-mutated.json) |
| Invalid then supported | C1 / C2 | 31 | 12/120; 14/120 | [C1](CtlDeterminism31/c1-duplicate-reverse.json), [C2](CtlDeterminism31/c2-duplicate-reverse.json) |
| Constant majority: mislocated / stale | C1 / C2 | 31 | **58/120; 56/120** | [C1](CtlDeterminism31/c1-majority.json), [C2](CtlDeterminism31/c2-majority.json) |
| Supported stub, gate exit 1 | C1 / C2 | 31 | 42/120; 40/120 | [C1](CtlDeterminism31/c1-stub-exit1.json), [C2](CtlDeterminism31/c2-stub-exit1.json) |
| Supported stub, gate exit 2 | C1 / C2 | 31 | 0/120 each | [C1](CtlDeterminism31/c1-stub-exit2.json), [C2](CtlDeterminism31/c2-stub-exit2.json) |
| Externally truth-fed replay: exit-0 branch only | C1 / C2 | 31 | 120/120 each | [C1](CtlDeterminism31/c1-exit0-external-truth-replay.json), [C2](CtlDeterminism31/c2-exit0-external-truth-replay.json) |

The replay stub receives an explicit tester-generated id→truth lookup outside the fixture. It implements neither contract, is **not an admissible source-skipping control**, and its 120/120 is not evidence of a fixture leak. It exists solely to exercise the otherwise unreachable counter-exit-0 branch and a passing duplicate-output baseline.

## Pass/fail

| Check | Result | Evidence |
|---|---|---|
| Same seed → byte-identical kept fixture | PASS, both: `diff -r` exit 0, empty stdout/stderr | [C1 diff](CtlDeterminism31/c1-same-seed-diff.json), [C2 diff](CtlDeterminism31/c2-same-seed-diff.json) |
| Same seed → identical score | PASS, 50/120 both times, both counters | Base receipts above |
| Class counts constant across ten seeds | PASS, all 12 C1 / 9 C2 classes; receipt denominators and directly regenerated fixtures agree | Both primary summaries, `fixtures` |
| Truth totals match claims.md | PASS: C1 supported/mislocated/invalid/unsupported = **42/58/12/8**; C2 supported/unsupported/stale/invalid = **40/10/56/14**, every seed | Both primary summaries |
| No class or varying truth label in JSONL/names | PASS across 20 fixtures; no class-name hits or truth outside constant `expect` | Both primary summaries |
| Literally no truth value anywhere in JSONL | FAIL as worded: `"supported"` appears exactly 120 times per JSONL, solely as the design's constant `expect`; not a truth leak | `literal_truth_string_counts`, `constant_expect_counts` in summaries; `c1-count.py:176`, `c2-count.py:164-165` |
| Different TMPDIR preserves bytes and score; sources share root device | PASS: `/tmp` device **66308**, sandbox TMPDIR device **66309**, lane device **56**; all 120 actual sources and claims share their declared temporary root's device | [C1 devices](CtlDeterminism31/c1-base-fast-tmpdir-devices.json), [C2 devices](CtlDeterminism31/c2-base-fast-tmpdir-devices.json), [C1 diff](CtlDeterminism31/c1-different-tmpdir-diff.json), [C2 diff](CtlDeterminism31/c2-different-tmpdir-diff.json); all per-run device receipts retained |
| Documented exits 0/1/2 on normal branches | PASS: truth-fed replay 0; mismatches 1; missing gate/temp directory 2 | Above plus `c1-error-missing-gate-run.json`, `c2-error-missing-gate-run.json`, `c1-error-missing-tempdir-run.json`, `c2-error-missing-tempdir-run.json` |
| All harness errors use documented exit 2 | **FAIL**, both counters: existing `--keep` and missing receipt parent raise tracebacks and exit **1** | `c1-error-existing-keep-run.json`, `c2-error-existing-keep-run.json`, `c1-error-missing-receipt-parent-run.json`, `c2-error-missing-receipt-parent-run.json` |
| Duplicate CLAIM results use only first line | PASS as observed parser behavior; later contradictory results are silently ignored | Duplicate controls above; `c1-count.py:218-219`, `c2-count.py:207-208` |

## Findings and mutation

- **Harness defect:** unhandled `shutil.copytree` failure at `corpus/evidence/round31/c1-count.py:229` / `c2-count.py:218`, and receipt-open failure at `c1-count.py:246` / `c2-count.py:235`, return 1 instead of documented harness-error 2 (`c1-count.py:26`, `c2-count.py:25`). A receipt failure even prints a normal score first. This confuses evaluation failure with a measured miss; it does not inflate scores.
- **Duplicate-output blind spot:** one sandbox-only mutation changed the stub's line 21 from `for observed in observations:` to `for observed in (*observations, 'invalid'):`. It emitted 240 lines for 120 ids. Constant-output scores stayed C1 **42→42→42**, C2 **40→40→40**, pristine→mutated→restored. Explicit truth replay stayed **120→120→120** for both, despite contradictory second results. **Mutant survived** output-integrity detection. The constant baselines already fail the claim predicate, so they are not killed-mutant evidence. First-line parsing can hide later contradictions, but enumerating possible labels cannot improve the first prediction; no work-skipping 120/120 bypass was found here.
- **Fixture leak sweep:** no varying truth/class label was exposed. Maximum non-truth-fed shortcut scores reached here: **C1 58/120, C2 56/120**, constant majority outputs. Determinism and cross-device-root handling held on the assigned probes.

Restoration and full hash evidence: [mutation-restoration.json](CtlDeterminism31/mutation-restoration.json). Stub pristine/restored SHA-256 `becc5b758839f0f00fdffeda881467114e6d5a6bc2db6e98442c0d23bc768057`; mutant `3f36d4391a8705700ec33dccf533e9714ea49c2a409d5064219b4286c95f3e08`. Gate, counters, and claims.md retained their initial hashes. Raw stdout/stderr and exact commands are in each `*-run.json`; initial probe sources are embedded in `c1-probe-sources.json` / `c2-probe-sources.json`.

Every counter invocation had `timeout --kill-after=5 900`, lane-root cwd, 1 GiB/process address-space, 180 s/process CPU, and a 4096 per-user process ceiling in children. At most two counter invocations ran concurrently. Process groups were killed/drained on completion; no owned process groups remain. No network, git writes, tool installs, or tool updates occurred. Report and receipts are left for Main to commit; no candidate is judged or changed.

Scoped score-bypass verdict (harness error-classification defects remain as above):

design holds
