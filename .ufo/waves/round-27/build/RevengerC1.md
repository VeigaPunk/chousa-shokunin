# RevengerC1 — round27 attempt1

- **Assigned item / axes:** C1 usage selftest reconstruction; operability. C2 freshness and C3 calibration were not investigated.
- **Grounding quote:** `.ufo/waves/round-26/falsify/FNoTrade.md:127`: “The predicate is unsatisfiable for any usage exit.” (8 words.)

## Reconstructed failure

The accepted r26 receipt identifies target `0e9784bd`, `FAIL (3/187 cases)`, and exactly `metadata-asof-invalid`, `metadata-asof-missing`, and `metadata-asof-wrong-mode` (`FNoTrade.md:8–14, 115–137`). The 161 legacy case identities matched base; the failures were the three new as-of usage assertions.

In that target, `metadata_asof_usage_case` captured `bash "$SELF" "$@" 2>&1` and accepted only when exit was 2, the expected diagnostic appeared, **and** `$out != *'RESEARCH_GATE: '*` (`tools/research-gate.sh:6010–6022`, r26 target). The three diagnostic expectations correspond to real `die_usage` paths: invalid calendar date (`:6295–6297`), missing `--as-of` argument (`:6282–6283`), and `--as-of` used outside metadata mode (`:6295–6296`). Thus their required exit and message were compatible with the gate's argument checks.

The remaining clause made each assertion impossible. `die_usage` prints the diagnostic, calls `usage` on stderr, and exits 2 (`:390`). The help text includes `Verdict: RESEARCH_GATE: CLEAN|DRIFT` (`:385`), so the merged capture always contains the tested substring on a usage error. That help line is explanatory text, not a verdict record: actual records begin at column zero with `RESEARCH_GATE: `; other selftest helpers count those with anchored `grep -c '^RESEARCH_GATE: '` (e.g. `:2832`, `:3467`, `:5993`). All three cases fail the same final check regardless of the correct rc and diagnostic. The unaffected setup helper separates stdout from stderr (`:4005–4025`), and the metadata help case positively checks its usage entry (`:5945–5952`). This accounts for why the defect is limited to those three assertions rather than a gate usage failure or broad regression.

## Suggested outcome and limits

Retain all three cases, expected diagnostics, and exit 2; require zero **anchored verdict records**, not absence of the substring anywhere in help text. Keep independent predicate controls for a valid usage error, exit 1, absent diagnostic, and actual anchored CLEAN/DRIFT record. This preserves the asserted failure conditions while distinguishing help from a verdict.

The shared source changed during this review. Its final source-only read shows an anchored `metadata_asof_usage_accepts` predicate and synthetic rejection controls (`tools/research-gate.sh:6010–6041, 6102–6113`). This reconstruction is specifically of the r26 target; no conclusion is made about the changed helper's runtime behavior. No gate, selftest, build, lint, or formatter was run; the FAIL3/187 result is inherited receipt evidence, not a rerun. No tools were installed.