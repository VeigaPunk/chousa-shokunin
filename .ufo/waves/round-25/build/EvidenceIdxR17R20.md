# Evidence-index check: rounds 17–20

Observed source: `corpus/evidence/README.md:644–659`; all 16 receipt rows currently sit below `## Round-8 gate-baseline receipts` (`README.md:580`). The following sections are a verbatim-row draft only; no lane files were changed.

## Disk existence and SHA-256 prefixes

`ls -l` and `sha256sum` run on each listed absolute path; all 16 `ls` calls succeeded. Prefixes below are the first 12 SHA-256 hex digits.

| README line | filename | exists | SHA-256 prefix |
|---|---|---|---|
| 644 | `fence-r17-20261019T171200Z-selftest.log` | yes | `db48a9021d59` |
| 645 | `fence-r17-20261019T171200Z-demo.log` | yes | `174d616433fe` |
| 646 | `fence-r17-20261019T171200Z-battery.log` | yes | `3bb217c1f9f4` |
| 647 | `fence-r17-20261019T171200Z-drift.log` | yes | `d489fb31f5eb` |
| 648 | `scope-r18-20261019T173000Z-selftest.log` | yes | `57c2474d7e8c` |
| 649 | `scope-r18-20261019T173000Z-demo.log` | yes | `a30f8d2a779f` |
| 650 | `scope-r18-20261019T173000Z-battery.log` | yes | `3bb217c1f9f4` |
| 651 | `scope-r18-20261019T173000Z-drift.log` | yes | `d489fb31f5eb` |
| 652 | `symlink-r19-20261019T174500Z-selftest.log` | yes | `4c27ede09c49` |
| 653 | `symlink-r19-20261019T174500Z-demo.log` | yes | `07dae9d93717` |
| 654 | `symlink-r19-20261019T174500Z-battery.log` | yes | `3bb217c1f9f4` |
| 655 | `symlink-r19-20261019T174500Z-drift.log` | yes | `d489fb31f5eb` |
| 656 | `verify-r20-20261019T180000Z-selftest.log` | yes | `639868a134e8` |
| 657 | `verify-r20-20261019T180000Z-demo.log` | yes | `f6656daf868b` |
| 658 | `verify-r20-20261019T180000Z-battery.log` | yes | `3bb217c1f9f4` |
| 659 | `verify-r20-20261019T180000Z-drift.log` | yes | `d489fb31f5eb` |

## Round-17 fenced-heading shadow receipts — stamp 20261019T171200Z
Gate SHA prefix `2b64a1c8…` → `c2915f24…`; selftest 111 → 116 cases, landed `PASS (116 cases, 0 skipped)` (`SCORECARD.md:863–870`; note `knowledge/fenced-heading-r17.md:4`).

| Receipt (sha256) | Shows | Key result |
|---|---|---|
| `fence-r17-20261019T171200Z-selftest.log` | r17: `PASS (116 cases, 0 skipped)`; cases 1–109 `cmp` byte-identical vs `root-r15-…-selftest.log` |
| `fence-r17-20261019T171200Z-demo.log` | before/after pair: pre-round gate (`eaa3bbd`) passes CLEAN on a fenced-shadow record; landed gate refuses `SCOPE_BOUNTY_ABSORBED` warn |
| `fence-r17-20261019T171200Z-battery.log` | masked battery (banner/ts) vs the pre-round gate: A/B/C-r9, claims-r2, chain-r3, sweeps-r5, integrity-r7, full-r6 — ALL IDENTICAL |
| `fence-r17-20261019T171200Z-drift.log` | `--drift` vs the r12 baseline → `GATE_DRIFT: none`, exit 0 (no re-pin needed) |

## Round-18 scope phrase gap receipts — stamp 20261019T173000Z
Gate SHA prefix `c2915f24…` → `6e694881…`; selftest 116 → 119 cases, landed `PASS (119 cases, 0 skipped)` (`SCORECARD.md:918–924`; note `knowledge/scope-phrase-gap-r18.md:4`).

| Receipt (sha256) | Shows | Key result |
|---|---|---|
| `scope-r18-20261019T173000Z-selftest.log` | r18: `PASS (119 cases, 0 skipped)`; cases 1–116 `cmp` byte-identical vs `fence-r17-…-selftest.log` |
| `scope-r18-20261019T173000Z-demo.log` | before/after pair: pre-round gate (`e3c556e`) passes CLEAN on `domain: LLM benchmarks`; landed gate refuses `SCOPE_MODEL_QUALITY_ABSORBED` warn |
| `scope-r18-20261019T173000Z-battery.log` | masked battery (banner/ts) vs the pre-round gate: A/B/C-r9, claims-r2, chain-r3, sweeps-r5, integrity-r7, full-r6 — ALL IDENTICAL |
| `scope-r18-20261019T173000Z-drift.log` | `--drift` vs the r12 baseline → `GATE_DRIFT: none`, exit 0 (no re-pin needed) |

## Round-19 sweep symlink escape receipts — stamp 20261019T174500Z
Gate SHA prefix `6e694881…` → `9f163807…`; selftest 119 → 122 cases, landed `PASS (122 cases, 0 skipped)` (`SCORECARD.md:969–976`; note `knowledge/sweep-symlink-r19.md:4`).

| Receipt (sha256) | Shows | Key result |
|---|---|---|
| `symlink-r19-20261019T174500Z-selftest.log` | r19: `PASS (122 cases, 0 skipped)`; cases 1–119 `cmp` byte-identical vs `scope-r18-…-selftest.log` |
| `symlink-r19-20261019T174500Z-demo.log` | before/after pair: pre-round gate (`5499cef`) reports `SWEEP_CLAIM_FALSE` hit on an outside symlink; landed gate refuses `SWEEP_LOCATION_OUT_OF_CORPUS` crit |
| `symlink-r19-20261019T174500Z-battery.log` | masked battery (banner/ts) vs the pre-round gate: A/B/C-r9, claims-r2, chain-r3, sweeps-r5, integrity-r7, full-r6 — ALL IDENTICAL |
| `symlink-r19-20261019T174500Z-drift.log` | `--drift` vs the r12 baseline → `GATE_DRIFT: none`, exit 0 (no re-pin needed) |

## Round-20 HTML-comment heading shadow receipts — stamp 20261019T180000Z
Gate SHA prefix `9f163807…` → `49b36759…`; selftest 122 → 124 cases, landed `PASS (124 cases, 0 skipped)` (`SCORECARD.md:1020–1028`; note `knowledge/html-comment-r20.md:4`).

| Receipt (sha256) | Shows | Key result |
|---|---|---|
| `verify-r20-20261019T180000Z-selftest.log` | r20: `PASS (124 cases, 0 skipped)`; cases 1–119 `cmp` byte-identical vs `scope-r18-…-selftest.log` |
| `verify-r20-20261019T180000Z-demo.log` | before/after pair: pre-round gate (`2bb556b`) passes CLEAN on an HTML-comment shadow; landed gate refuses `SCOPE_BOUNTY_ABSORBED` warn |
| `verify-r20-20261019T180000Z-battery.log` | masked battery (banner/ts) vs the pre-round gate: A/B/C-r9, claims-r2, chain-r3, sweeps-r5, integrity-r7, full-r6 — ALL IDENTICAL |
| `verify-r20-20261019T180000Z-drift.log` | `--drift` vs the r12 baseline → `GATE_DRIFT: none`, exit 0 (no re-pin needed) |

## Unindexed / round 16

The evidence-directory inventory has no unindexed round-stamped r17–r20 receipt. In the full `.log` inventory, `round25-measure-before.log` is the sole file without a README row; it is the preregistered measurement output, not a stamped receipt (`round25-claims.md:6–7`; inventory also contains `round25-measure.sh`). Round 16 has no r16-named receipt file and no r16 receipt row; its knowledge note records a 111-case selftest but points to r15 receipts (`knowledge/verification-r16.md:4–5`).

VERDICT: All requested r17–r20 indexed rows are verified on disk and drafted verbatim under round-specific headings; no r17–r20 receipt is unindexed. No installs.