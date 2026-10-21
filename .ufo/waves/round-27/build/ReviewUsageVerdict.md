# ReviewUsageVerdict — C1 usage-verdict oracle

**Axis:** Operability (only; freshness/calibration are out of scope for this seat).

## Finding

The round-26 failure is in the usage-test predicate, not the gate's usage behavior. `FNoTrade.md:120-128` records the three affected cases and explains that `metadata_asof_usage_case` at `tools/research-gate.sh:6016` rejects the substring `RESEARCH_GATE: `, while `die_usage` prints help containing `Verdict: RESEARCH_GATE: CLEAN|DRIFT` (`:390`, `:385`). Since that helper captures `2>&1` (`:6014-16`), the expected rc=2 usage errors match the help-text substring and fail. The round-26 receipt reports `FAIL (3/187)` and confirms `--as-of 2026-02-30` correctly exits 2 with its diagnostic (`FNoTrade.md:117-128`).

**Suggested change:** detect verdict *records* by anchored `^RESEARCH_GATE: ` lines, not arbitrary help-text substrings; preserve the rc=2 and expected-diagnostic requirements. The usage synopsis line prefixed by `Verdict:` is explanatory text, not a record.

## Concrete acceptance oracle

Keep all three existing usage cases (`metadata-asof-invalid`, `metadata-asof-missing`, `metadata-asof-wrong-mode`; `tools/research-gate.sh:6010-22,6083-88`) and require each actual invocation to have rc=2, its expected diagnostic, and zero lines beginning exactly `RESEARCH_GATE: `. Add independent controls proving the predicate is not weakened:

- Correct usage-error result (rc=2, expected diagnostic, help synopsis present, no anchored verdict record) passes.
- rc=1, missing expected diagnostic, or an anchored verdict record fails.
- In particular, with rc=2 and the expected diagnostic still present, synthetic output containing `RESEARCH_GATE: CLEAN` fails, and synthetic output containing `RESEARCH_GATE: DRIFT` fails. These controls must distinguish actual record lines from the `Verdict: RESEARCH_GATE: CLEAN|DRIFT` synopsis.
- Preserve all 187 original case identities and expected outcomes; no usage error may be accepted when it emits an actual verdict.

Source claims: `corpus/evidence/round27-claims.md:5-7` requires the anchored-record rule, independent usage/exit-1/missing-diagnostic/actual-verdict controls, and preservation of the 187 cases. Round-26 receipt: `.ufo/waves/round-26/falsify/FNoTrade.md:115-137`.

## Residual risk / verification gap

No gate, selftest, or regression suite was run, per assignment. The `lsp` route is not mounted in this session (`read xd://lsp` reported no such tool); no LSP caller/definition/diagnostic evidence is claimed. No tools were installed.
