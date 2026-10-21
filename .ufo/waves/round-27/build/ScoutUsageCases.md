# ScoutUsageCases — round27 attempt1: original-187 identities and the three failing usage expectations

Seat `ChousaR27.ScoutUsageCases` (leaf, static read-only). Base
`64eec5d41c7cf7f17f5ce1e968e28b3769952596`. No selftest, gate, probe, regression, build,
lint, or formatter was run; no tool was installed. No `lsp` device is mounted
(`read xd://lsp` → “No such tool”); every location below comes from literal source reads,
not semantic proof.

**Intervening change (observed, not mine).** The live gate moved during this seat:
`.ufo/waves/round-27/baseline-research-gate.sh` still hashes
`c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6` (6351 lines), but
`tools/research-gate.sh` is now `8ee706b29a6c013db5459a70ada2c07eba387788707a3bde7c40a96c75ac4f8f`
(6376 lines, `+26/-1`) and already contains an integrated C1 repair. Original-case ordinals
below are taken from the baseline snapshot; live line numbers are labelled “now”.

Grounding quote (12 words): “Count verdict records by anchored `^RESEARCH_GATE: `, not
help-text substrings.” — `corpus/evidence/round27-claims.md:7`.

## 1. The three failing usage expectations (original ordinals 171–173)

Inherited evidence: `.ufo/waves/round-26/falsify/FNoTrade.md:115-137` names all three and
attributes them to the harness, not gate behaviour. Accepted, not rerun.

| Ord | Case name | CLI under test (fixture args) | Required diagnostic | Want rc |
|---|---|---|---|---|
| 171 | `metadata-asof-invalid` | `verify-metadata $WORK/meta-asof/current.md --root $WORK --as-of 2026-02-30` | `--as-of must be a valid YYYY-MM-DD date` | 2 |
| 172 | `metadata-asof-missing` | same path/root, trailing `--as-of` with no value | `--as-of needs YYYY-MM-DD` | 2 |
| 173 | `metadata-asof-wrong-mode` | `verify $WORK/all-pass.md --as-of 2026-10-21` | `--as-of is only valid with verify-metadata` | 2 |

Source pins (baseline `tools/research-gate.sh`): helper definition `:6010-6022`; the three
invocations `:6083-6088`. Diagnostic emitters (live gate, unchanged text): `:6307`
(`--as-of needs`), `:6321` (wrong mode), `:6322` (invalid calendar); `die_usage` `:390`;
usage text containing the literal line `Verdict: RESEARCH_GATE: CLEAN|DRIFT` at `:385`.

**Why all three fail, and why rc/diagnostic are already correct.** The helper merges stdout
and stderr (`out=$(bash "$SELF" "$@" 2>&1)`) and then required
`$out != *'RESEARCH_GATE: '*` (baseline `:6016`). Every `die_usage` path appends `usage`,
whose `:385` line contains `RESEARCH_GATE: ` as a substring, so the clause is false for
every usage exit regardless of rc or diagnostic. The failure is deterministic and confined
to the harness predicate; no invocation, expected exit 2, or expected token needs to change.

**Required counting rule.** Only records anchored at column 0 — `^RESEARCH_GATE: ` — are
verdicts. The help line is unanchored (`Verdict: …`), so it must not count; an anchored
`RESEARCH_GATE: CLEAN` or `RESEARCH_GATE: DRIFT` must still reject the usage expectation.

## 2. Original 187 case identities (static enumeration, baseline snapshot)

Reconciliation: `run_selftest` (`:3366-6250`) contains 185 runner invocations
(`tcase` 39, `tclaims` 26, `metadata_case` 26, `tsetup` 14, `tchain` 14, `tsweeps` 12,
`metadata_asof_case` 12, `tall` 11, `metadata_registry_case` 8, `tintegrity` 7, `tdrift` 7,
`r24_case` 3, `metadata_asof_usage_case` 3, `tnscase` 2, `tpin` 1) plus two inline
`cases`-increment cases (`metadata-no-content-echo` :5917, `metadata-usage` :5945) = 187.
The three conditional skip branches (`claims-root-slash-read`, `claims-root-dslash`,
`json-unreadable-manifest`) keep one ordinal each whether they run or skip. The identical
extraction from base `ba333325` yields 161, and its name sequence equals ordinals 1–161
here, so 162–187 are the 26 r26 additions.

```
1-18   tcase: pass-control, pass-hop-marked-unresolved, pass-export-chrome,
       fail-export-chrome-strict, fail-chrome-malformed-export, fail-no-question,
       fail-unranked-source, fail-chain-hop-unresolved, fail-claim-unpointed,
       fail-rejection-dropped, fail-negative-without-sweep, fail-obs-inference-collapse,
       fail-hierarchy-primary-lie, fail-pointer-ephemeral, fail-external-without-approval,
       fail-secret-shaped, fail-session-read, fail-schema
19-20  tsetup: no-record, missing-file
21-28  tclaims: claims-pass, claims-fail-tampered, claims-fail-out-of-corpus,
       claims-fail-external, claims-fail-session, claims-fail-contradicted-unmarked,
       claims-fail-stray-marker, claims-fail-counting
29-30  tsetup: claims-no-path, claims-missing-file
31-38  tchain: chain-pass, chain-fail-tampered, chain-fail-anchor-kinds,
       chain-fail-out-of-corpus, chain-fail-external, chain-fail-invalid,
       chain-fail-counting, chain-fail-no-chain
39-40  tsetup: chain-no-path, chain-missing-file
41-42  tclaims: claims-boundary-pass, claims-boundary-fail
43-44  tchain: chain-pass-boundary, chain-fail-boundary
45-52  tsweeps: sweeps-pass, sweeps-fail-planted-hit, sweeps-fail-rejection-incomplete,
       sweeps-fail-unnamed, sweeps-fail-out-of-corpus, sweeps-fail-unresolved-id,
       sweeps-fail-counting, sweeps-pass-cell-command
53-54  tsetup: sweeps-no-path, sweeps-missing-file
55-64  tall: all-pass.md, all-pass.md, all-structure.md, all-pass.md, claims-pass.jsonl,
       all-pass.md, all-pass.md, all-meta.md, all-meta-missing.md, no-such-record.md
65-71  tintegrity: integrity-pass, integrity-fail-dangling-claim,
       integrity-fail-dangling-source, integrity-fail-dangling-chain-claim,
       integrity-fail-dangling-sweep, integrity-exempt-counted, integrity-fail-counting
72-73  tsetup: integrity-no-path, integrity-missing-file
74     tall: all-dangling.md
75     tpin: pin-clean
76-81  tdrift: drift-clean, drift-volatile-churn, drift-one-field-mutant, drift-missing,
       drift-malformed, drift-volatile-list
82-85  tsetup: pin-no-path, drift-no-path, pin-unwritable, pin-drift-exclusive
86-93  tcase: scope-fail-bounty, scope-fail-model-quality, scope-fail-orchestration,
       scope-pass-declared-table, scope-pass-declared-line, scope-pass-near-miss,
       scope-pass-prose-decoy, banner-pin
94     tdrift: drift-banner-version
95-96  tclaims: claims-cap-at, claims-cap-over
97-98  tchain: chain-cap-at, chain-cap-over
99     tclaims: claims-hardlink-alias
100    tchain: chain-hardlink-alias
101-102 tclaims: claims-hardlink-family, claims-single-link
103-104 tnscase: claims-cross-device, chain-cross-device
105-110 tclaims: claims-cross-device-control, claims-lane-fallback,
       claims-root-slash-absent, claims-root-slash-read, claims-root-slash-xdev,
       claims-root-dslash
111    tsweeps: sweeps-root-slash
112-119 tcase: scope-fence-shadow, scope-fence-only, scope-fence-nested,
       scope-fence-indented, scope-fence-unclosed, scope-fail-llm-benchmarks,
       scope-fail-llm-scoring, scope-pass-benchmark-prose
120-122 tsweeps: sweeps-symlink-escape, sweeps-symlink-dir, sweeps-inroot-symlink
123    tclaims: claims-cap-eof
124-128 tcase: scope-comment-shadow, ptr-traversal, ptr-symlink, ptr-lane-abs,
       ptr-deny-symlink
129    tchain: chain-fence-anchor
130-133 tclaims: claims-config-start, claims-omp-start, claims-localstate-start,
       claims-config-adjacent
134-136 r24_case: json-unterminated-manifest, json-nul-terminated-manifest,
       json-unreadable-manifest
137-158 metadata_case: metadata-clean, metadata-no-source, metadata-no-verified,
       metadata-no-recheck, metadata-undated, metadata-unscheduled,
       metadata-unscheduled-strict, metadata-root-parent, metadata-fenced,
       metadata-after-heading, metadata-crlf, metadata-directory, metadata-missing-path,
       metadata-empty-directory, metadata-nul-refused, metadata-denylist-alias,
       metadata-nonkey-continuation, metadata-safe-symlink, metadata-hardlink-refused,
       metadata-stat-unavailable, metadata-invalid-calendar, metadata-literal-heading
159    INLINE: metadata-no-content-echo
160    metadata_case: metadata-stable-object
161    INLINE: metadata-usage
162-164 metadata_case: metadata-no-final-newline, metadata-fenced-heading,
       metadata-heading-boundary
165-170 metadata_asof_case: metadata-asof-overdue, metadata-asof-current,
       metadata-asof-date-past, metadata-asof-event, metadata-asof-unknown,
       metadata-asof-boundary
171-173 metadata_asof_usage_case: metadata-asof-invalid, metadata-asof-missing,
       metadata-asof-wrong-mode                      <-- the three r26 failures
174-179 metadata_asof_case: metadata-asof-leap-2028, metadata-asof-leap-2027,
       metadata-asof-large-cadence, metadata-asof-date-overflow,
       metadata-asof-invalid-verified-date, metadata-asof-refused
180-187 metadata_registry_case: metadata-registry-missing-row, metadata-registry-not-mined,
       metadata-registry-used-by-path, metadata-registry-verified-at-bare,
       metadata-registry-no-token-id, metadata-registry-positive-continuations,
       metadata-registry-duplicate-first-row, metadata-registry-refused-nul
```

## 3. Preservation requirements (all from source)

1. **Identity set and order.** All 187 names above, in that order. Legacy pin covers only the
   first 161, but the claim says “all187 original case identities preserved”
   (`corpus/evidence/round27-claims.md:7`). Keep the trio at 171–173 and put any new control
   cases after 187 if ordinal identity must stay byte-for-byte.
2. **Legacy161.** `LEGACY_CASES_SHA` is the SHA-256 of the first 161 `^ok-case` lines
   (`corpus/evidence/round26-measure.sh:229`); pinned value
   `5eac4a7e2af964f6e81631f66990426e5c8ef58fb41ba6ec6d0054ef819e01cb`
   (`corpus/evidence/round26-measure-before.log:67`, `round26-inherited-after.log:43`).
   Every edit at or below case 161’s invocation (baseline `:5945`) risks it; the helper repair
   sits below that line and does not touch it.
3. **Exit and diagnostics.** Keep expected exit 2 and the three diagnostic strings byte-identical;
   do not shorten them to help-text substrings (`--as-of`, `YYYY-MM-DD`, `verify-metadata` all
   occur in `usage()`).
4. **Verdict rule.** Accept only anchored `^RESEARCH_GATE: ` count 0. Reject anchored CLEAN and
   DRIFT; allow the unanchored help line at `:385`. Do not strip or rewrite help text in the
   harness, and do not use `2>/dev/null`.
5. **No weakening.** No deletion/rename/merge/skip of cases 171–173, no rc relaxation, no
   dropped verdict clause, no `failures++` in a subshell.
6. **Controls.** Four classes: correct usage passes (positive), exit 1 fails, missing diagnostic
   fails, actual anchored CLEAN/DRIFT fails. At least one control must fail under the old r26
   predicate; otherwise the control set cannot detect this defect.
7. **Extractor contract.** The independent harness extracts
   `^  metadata_asof_usage_accepts()` and `^  metadata_asof_usage_case()` by exact two-space
   indent and name, concatenates those two function bodies into a stub script, and supplies only
   `cases`, `failures`, `SELF` (`corpus/evidence/round27-regressions.py:73-89`). Renaming,
   re-indenting, adding an inner `^  }`, or calling any other new helper makes that harness exit 2
   (“usage selftest helper not found”) or fail scenarios spuriously. Keep both helpers
   self-contained apart from `cases`, `failures`, `SELF`.
8. **Mechanism count.** `corpus/evidence/round27-mechanisms.py` counts the literal
   `$out != *'RESEARCH_GATE: '*` occurrence; the final tree must show C1 = 0
   (baseline `corpus/evidence/round27-mechanisms-before.json` has 1).
9. **Frozen score.** Existing numeric operability score 3 stays at r26; no numeric
   resource-safety inference from this repair.

## 4. Current integrated state and remaining calibration findings

Live gate `8ee706b2…` (observed; it may move again). The repair adds
`metadata_asof_usage_accepts RC EXPECTED OUT` at `:6010-6014` using
`grep -c '^RESEARCH_GATE: '` and `rc -eq 2`, rewires the three cases at `:6101-6106`, and adds
`metadata_asof_usage_control_case` (`:6029-6042`) with three controls at `:6107-6113`.

- **Behaviour is correct on static reading.** The two C1 predicates now agree with the
  independent scenarios: valid usage with help text is accepted; anchored CLEAN and DRIFT are
  rejected; rc 1 is rejected; a missing diagnostic is rejected; the mid-line mention
  `note RESEARCH_GATE: not a record` is not counted. No rerun performed.
- **S1 — ordinal shift (operability/identity).** Controls are inserted after case 173, so the
  suite is now 190 cases and original 174–187 print as 177–190
  (`metadata-asof-leap-2028` 174→177 … `metadata-registry-refused-nul` 187→190). Names survive,
  ordinals do not. Move the three control calls below `metadata-registry-refused-nul`
  (live `:6259-6263`) and above the summary check (live `:6266`); the suite stays 190 cases but
  1–187 keep their ordinals.
- **S2 — in-gate controls are non-discriminating.** All three use `want_accept=0` and only a
  CLEAN verdict; they all pass under the old r26 predicate too, so they do not cover the
  “correct usage passes” class or DRIFT. The independent harness currently carries the positive
  and DRIFT controls; if in-gate evidence is wanted, add a `want_accept=1` control whose output
  contains the real help line `Verdict: RESEARCH_GATE: CLEAN|DRIFT`, plus an anchored DRIFT
  control — after 187.
- **S3 — external harness dependency.** `corpus/evidence/round27-regressions.py` is untracked
  round prep and was edited concurrently during this seat; the extractor now includes both
  helper bodies (`:73-89`). Any later rewrite of the helper shape can break it before C1 is
  measured. Record the harness digest actually used with the final receipt.
- **S4 — expected summary.** With the current 190 cases and no failures the line is
  `RESEARCH_GATE_SELFTEST: PASS (190 cases)`; `SKIPPED` is still printed by `${SKIPPED:+…}` even
  when zero. A PASS with skips is not evidence for the skipped cases (legacy161 hash shifts if a
  `skip-case` replaces an `ok-case` in the first 161).

## 5. Unrun checks (main agent, once after integration)

- `bash tools/research-gate.sh --selftest`: PASS, exit 0, with 1–187 identical by ordinal and
  name, the three usage cases `ok-case`, and the skipped count recorded.
- `LEGACY_CASES_SHA` equals `5eac4a7e…` under matching namespace availability.
- `python3 corpus/evidence/round27-regressions.py --gate tools/research-gate.sh`: 0 mismatches,
  including the six C1 controls.
- `python3 corpus/evidence/round27-mechanisms.py tools/research-gate.sh`:
  `C1_faulty_usage_substring = 0`.
- Isolated-copy mutation: swapping the repaired predicate back to the r26 substring form must
  turn the positive control red (do not edit production for this).

## Trailer

Always-relative paths read or written by this seat:
`corpus/evidence/round27-claims.md`,
`corpus/evidence/round27-regressions.py`,
`corpus/evidence/round27-mechanisms.py`,
`corpus/evidence/round27-mechanisms-before.json`,
`corpus/evidence/round26-measure.sh`,
`corpus/evidence/round26-measure-before.log`,
`corpus/evidence/round26-inherited-after.log`,
`.ufo/waves/round-26/falsify/FNoTrade.md`,
`.ufo/waves/round-27/baseline-research-gate.sh`,
`.ufo/waves/round-27/patches/ExecUsage.patch`,
`tools/research-gate.sh` (read only), and this report
`.ufo/waves/round-27/build/ScoutUsageCases.md` (written once). No product code, fixture, test,
or harness was changed; no tool was installed.
