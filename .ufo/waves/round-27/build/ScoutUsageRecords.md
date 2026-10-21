# ScoutUsageRecords — C1 usage-helper predicates and anchored verdict convention

- **Seat / method:** `ChousaR27.ScoutUsageRecords` (leaf). Static source reading only:
  no gate, selftest, regression, probe, or build was executed. No tools installed.
- **Base:** HEAD `64eec5d41c7cf7f17f5ce1e968e28b3769952596` (verified with `git rev-parse`).
  Base line numbers below come from `git show HEAD:tools/research-gate.sh`.
- **Worktree is live:** `tools/research-gate.sh` was dirty during this pass (integration
  applying C1 changes). Snapshot analyzed atomically:
  sha256 `045c073e70c78103e14189350bb06a15ce622ae539fe2b1732f8adad77f7a3f1`,
  6381 lines, mtime `2026-10-21 11:41:20 -0300`. It grew from the 6351-line base
  while I read (6376 → 6381), so re-check line numbers if integration has moved on.
  `corpus/evidence/round27-regressions.py` also changed during the pass; latest
  snapshot sha256 `07ab5199f85cfdcac2299debc0f6f6e64c12b54f961108c99990dc1a7026c082`,
  200 lines. Base line refs are canonical; snapshot refs are labelled `snap`.

## 1. Every usage-helper predicate

All selftest helpers live inside `run_selftest()` (`tools/research-gate.sh:3366` base).

| Helper / site | Base lines | Predicate asserted | Call sites / identities |
|---|---|---|---|
| `tsetup` | 4008-4027; predicate 4019 | fresh process; **split streams**: `rc==want`, stdout **empty**, stderr **non-empty** | 14 calls: `no-record` 4028, `missing-file` 4029, `claims-no-path` 4076, `claims-missing-file` 4077, `chain-no-path` 4201, `chain-missing-file` 4202, `sweeps-*` 4439-4440, `integrity-*` 4811-4812, `pin-no-path`/`drift-no-path`/`pin-unwritable`/`pin-drift-exclusive` 4969-4972 |
| inline `metadata-usage` | 5945-5952; predicate 5947 | `--help` rc 0 **and** substring `verify-metadata PATH [--root PATH]` | 1, case name `metadata-usage` |
| `metadata_asof_usage_case` | 6010-6023; **faulty** predicate 6016 | merged `2>&1`; `rc==2`; `*"$expected"*`; rejects any occurrence of substring `RESEARCH_GATE: ` | 3 (the r26 failures): `metadata-asof-invalid` 6083, `-missing` 6085, `-wrong-mode` 6087 |
| `metadata_case` rc2 branch | count 5723; branch 5727-5731 | `want_rc==2` ⇒ **anchored count 0** | `metadata-missing-path` 5861, `metadata-empty-directory` 5864 |
| `metadata_asof_case` rc2 branch | count 5993; branch 5997-6001 | `want_rc==2` ⇒ anchored count 0 | branch present; no rc2 call site today |
| `metadata_registry_case` rc2 branch | count 6148 (snap 6167); branch 6152-6156 (snap 6177-6181) | `want_rc==2` ⇒ anchored count 0 | `metadata-registry-refused-nul` 6235 base / 6254 snap |
| `tall` | 4512; count 4527 | exact expected `nverdict` (`want_nv`) | usage-ish case `tall no-such-record.md 2 0 0` 4627 (requires 0) |
| `tpin` | 4872; marker count 4881 | exactly one `^GATE_PIN: ` line | pin cases |
| `tdrift` | 4899; marker count 4916 | rc≤1 ⇒ exactly one `^GATE_DRIFT: `; rc2 ⇒ zero | drift cases |
| `tnscase` | 5166; count 5180 | exactly one anchored verdict (or skip when namespace unavailable) | ns cases |

Root cause of r26 FAIL3/187: base line 6016 is
`if [[ $rc -eq 2 && $out == *"$expected"* && $out != *'RESEARCH_GATE: '* ]]; then`.
`die_usage` (390) always appends `usage` to stderr, and `usage()` contains the literal
line `Verdict: RESEARCH_GATE: CLEAN|DRIFT` (385). With merged capture the rejection
clause is always false. Receipt: `.ufo/waves/round-26/falsify/FNoTrade.md:115-137`
(accepted ground truth, not rerun).

`tsetup` does **not** anchored-count verdicts; its split-stream oracle already fails an
actual verdict on stdout. A verdict printed to stderr would not fail it. It is not one of
the three failing cases and its call identities are outside the C1 patch scope.

## 2. Existing anchored verdict convention

The file-wide idiom is exactly:

```sh
nverdict=$(grep -c '^RESEARCH_GATE: ' <<<"$out" || true)
```

`|| true` is mandatory: `set -euo pipefail` is active (`tools/research-gate.sh:255`), and
`grep` exits 1 on a zero count. Usage/setup exits then require `${nverdict:-0} -eq 0`;
normal runs require exactly 1.

Base sites: `verify_all_section` 2832 (exactly 1, plus full-record parse 2839),
`gate_canonical_capture` 3147 (exactly 1), `tcase` 3467, `tclaims` 3504, `tchain` 3534,
`tsweeps` 3564, `tintegrity` 3594, `tall` 4527, `tnscase` 5180, `metadata_case` 5723,
`metadata_asof_case` 5993, `metadata_registry_case` 6148. Also anchored by different
labels: `tpin` 4881, `tdrift` 4916, `gate_drift_line_id` case `RESEARCH_GATE:*` 3173.
Production emitters all print at column 0: 1040, 1458, 1745, 2097, 2286, 2777, 3034.

Independent oracle (`corpus/evidence/round27-regressions.py`):
`observe()` counts declared regexes with `re.findall(..., re.MULTILINE)` (line 39);
C2/C3 pass `r'^RESEARCH_GATE: '` counts (snap 115, 145, 170, 175).

Snapshot predicate (`snap 6010-6014`) follows the convention exactly:

```sh
nverdict=$(grep -c '^RESEARCH_GATE: ' <<<"$out" || true)
[[ $rc -eq 2 && $out == *"$expected"* && ${nverdict:-0} -eq 0 ]]
```

## 3. Calibration-critical extraction contract

`round27-regressions.py` does **not** run the gate for C1. It extracts the shipped helper
text and drives it with a stub CLI (`SELF=$1`, `FAKE_RC`/`FAKE_OUTPUT`):

- extraction regex: `r'^  ' + name + r'\(\).*?^  }\n'` (snap 74-78; regex line 75);
- names required, in this order: `metadata_asof_usage_accepts`, then
  `metadata_asof_usage_case` (snap 74);
- extracted texts are concatenated (snap 78, 88) so the predicate must be defined
  **before** the helper that calls it;
- six scenarios (snap 79-86): correct usage (accept), anchored CLEAN (reject), anchored
  DRIFT (reject), rc1 (reject), missing diagnostic (reject), unanchored
  `note RESEARCH_GATE:` mention (accept).

Consequences for any C1 repair:

1. Both functions must remain **top-level inside `run_selftest`, exact names, two-space
   indent, closing line exactly `  }`**. Inlining, nesting under the case helper, or
   renaming the predicate makes the counting command abort with
   `parser.error('usage selftest helper not found: …')` (exit 2 setup) before any C2/C3
   observation.
2. The fixture shell defines only the extracted functions plus `cases=0; failures=0;
   SELF=$1`; the helper must not reference any other gate function.
3. The helper must return 0 on both accept and reject; only `failures` encodes the
   verdict. The current helper satisfies this (ok branch printf; fail branch ends with
   an assignment).
4. Static trace of the current snapshot against all six scenarios: 6/6 match
   `[INFERENCE — not executed]`. Base 64eec5d has no `metadata_asof_usage_accepts`, so
   the snap script exits 2 on the pristine base archive; if a baseline run is required,
   record that as an explicit C1 setup-skip (like the accepted long-token baseline skip)
   rather than a C1 mismatch, or the whole baseline run aborts before C2/C3.

## 4. Snapshot state vs the claim's controls

- Three original identities retained, expected exit 2 and diagnostics byte-identical
  (snap 6102-6107). Faulty substring clause gone; no unanchored `RESEARCH_GATE`
  glob predicate remains in the snapshot.
- Five controls appended **after** case 187 (`metadata-registry-refused-nul`, snap
  6254-6256) at snap 6257-6267: anchored CLEAN reject, rc1 reject, missing-diagnostic
  reject, correct-usage accept (`Verdict:` help line present), anchored DRIFT on line 1
  reject. Together with the independent script's six scenarios they cover the claim's
  four required controls plus the unanchored-mention guard.
- Placement preserves ordinals 1-187; new total is 187 + 5 = 192 absent skips
  `[INFERENCE]`. Any later C2/C3 case inserted before `metadata-registry-refused-nul`
  would shift 174-187; append new cases after it.
- `ExecUsage.patch` on disk has only three controls; the shared snapshot has five.
  Both versions keep the two-function extraction contract. The two extra controls close
  the mutation-detection gap (the r26 predicate passes the three negatives but fails the
  positive help control) already raised in `CriticHarness.md` D1/D3.
- Residual, not required by the claim: the helper's failure line does not print
  `verdict-lines=<n>/0` (other helpers do); optional diagnosability hardening only.

## 5. Suggested change / expected outcome

No further predicate change is required by this scout. Keep the snapshot design:
anchored count, rc==2, expected diagnostic, two top-level extractable helpers, controls
after case 187. Expected after integration `[INFERENCE]`: full selftest PASS with
1-187 identical and five new controls ok; `round27-regressions.py` exit 0 with C1 6/6;
mechanism probe C1 count 0 (base probe receipt: `round27-mechanisms-before.json`
`C1_faulty_usage_substring: 1`).

## 6. Unrun checks (L1, once, after integration)

- `bash tools/research-gate.sh --selftest` — PASS, ordinals/names 1-187 unchanged,
  five controls `ok-case`, skipped count recorded.
- `python3 corpus/evidence/round27-regressions.py --gate tools/research-gate.sh` —
  exit 0, 0 mismatches, C1 6/6.
- `python3 corpus/evidence/round27-mechanisms.py tools/research-gate.sh` — C1
  mechanism count 0.
- Do not rerun the r26 unsafe long-token reproduction; use the committed receipt.

## 7. Remaining unknowns

- Final integrated line numbers and case total after C2/C3 patches land (worktree churn
  observed; snapshot refs may drift).
- Whether the verification environment skips namespace cases (affects `skipped` count,
  not case identities).
- All runtime outcomes above are static inferences; no execution was performed by this
  seat. `lsp` was not needed for shell source here; no semantic-server claim is made.
