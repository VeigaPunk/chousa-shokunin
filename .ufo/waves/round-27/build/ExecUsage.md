# Round 27 — ExecUsage (C1 only)

- **Assigned change:** Replaced the faulty help-text substring rejection in `work/ExecUsage/tools/research-gate.sh:6010-6028` with a shared usage-result predicate requiring exit 2, the original expected diagnostic substring, and zero verdict records counted by anchored `^RESEARCH_GATE: `.
- **Retained assertions:** `metadata-asof-invalid`, `metadata-asof-missing`, and `metadata-asof-wrong-mode` remain at `work/ExecUsage/tools/research-gate.sh:6102-6107`; their diagnostic strings, command arguments, and expected exit 2 are unchanged.
- **Adversarial controls:** Added counted controls at `work/ExecUsage/tools/research-gate.sh:6108-6113`. Synthetic `RESEARCH_GATE: CLEAN` output with exit 2 and the diagnostic must be rejected; exit 1 with the diagnostic must be rejected; exit 2 without the diagnostic must be rejected. The shared predicate drives both controls and the three actual usage cases.
- **Patch:** `.ufo/waves/round-27/patches/ExecUsage.patch` (unified diff from base `64eec5d41c7cf7f17f5ce1e968e28b3769952596`). Working-copy source is `.ufo/waves/round-27/work/ExecUsage/tools/research-gate.sh`.
- **Expected outcome:** The help text's descriptive `Verdict: RESEARCH_GATE: CLEAN|DRIFT` is not mistaken for a verdict record, while an actual line beginning `RESEARCH_GATE: ` is rejected. No C2/C3 changes.
- **Checks:** No selftest, build, lint, formatter, or other verification was run; parent integration checks remain pending. No tools installed. No LSP facility for shell was exposed; the function was located by exact source search.
- **Risks/blockers:** None identified in this scoped implementation; behavior remains unverified until the parent runs the assigned gate.

## Integration refinement

The case predicate is now inline in `metadata_asof_usage_case` (`work/ExecUsage/tools/research-gate.sh:6015-6030`) so isolated extraction needs only `SELF`, `cases`, and `failures`; the count remains anchored at `^RESEARCH_GATE: `. The three original usage cases and their diagnostics/exit-2 expectations are unchanged.

The synthetic control calls were moved after original case 187 (`work/ExecUsage/tools/research-gate.sh:6260-6279`) so the original 1–187 case ordinals are retained. Five new counted controls exercise the actual case function: accepted help containing `Verdict: RESEARCH_GATE: CLEAN|DRIFT`, rejected CLEAN and line-1 DRIFT records, rejected wrong exit, and rejected missing diagnostic. The source regression's separately extracted `metadata_asof_usage_accepts` helper remains available.

No verification was run; parent integration checks remain pending.

The separately named `metadata_asof_usage_accepts` function is retained because the persisted round27 regression source extractor looks up that exact function name; the actual usage case now evaluates its anchored predicate inline.

Final source anchors: retained usage cases are at `work/ExecUsage/tools/research-gate.sh:6105-6110`; controls are at `:6260-6279`. These supersede the earlier line references in this report.
