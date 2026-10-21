# ReviewUsageExit — round27 C1 (usage exit2 / anchored verdict count)

Seat `ChousaR27.ReviewUsageExit`, leaf member, reviewer. Author-lane advice only;
no outside-judge verdict, no gate/selftest execution (read-only seat), no
subagents, no installs. Base master `64eec5d4`; reviewed the applied
`.ufo/waves/round-27/patches/ExecUsage.patch` as present in the working tree
(`git diff HEAD -- tools/research-gate.sh`, 26 insertions / 1 deletion, all
inside `run_selftest`; no production-mode change).

## Assigned item

C1: exit2 stays mandatory for usage errors; misuse cannot be hidden; verdict
records counted by anchored `^RESEARCH_GATE: `, not help-text substrings; the
three r26-failing usage selftests repaired without deleting cases, weakening
diagnostics, or changing expected exit2. Concrete acceptance oracle requested.

## What the repair does (verified against base and applied tree)

- r26 ground truth (FNoTrade F1, `.ufo/waves/round-26/falsify/FNoTrade.md:115-137`):
  `metadata-asof-invalid/missing/wrong-mode` failed because the harness
  predicate at base `tools/research-gate.sh:6016` required
  `$out != *'RESEARCH_GATE: '*`, while `die_usage` (`:390`) prints the usage
  text, which contains the prose line `Verdict: RESEARCH_GATE: CLEAN|DRIFT`
  (base `:385`). The predicate was unsatisfiable for any usage exit; gate
  behavior itself was correct (rc 2, right diagnostics).
- Applied diff replaces the substring leg with
  `nverdict=$(grep -c '^RESEARCH_GATE: ' <<<"$out" || true)` and
  `${nverdict:-0} -eq 0` (new `metadata_asof_usage_accepts`), preserving
  `$rc -eq 2` and the exact expected diagnostic token. The three original
  cases keep names, arguments, diagnostics, and exit 2. The old substring
  form is fully gone: `grep -c "!= \*'RESEARCH_GATE: '\*"` on the tree = 0.
- Three new rejection controls (`metadata-asof-usage-{verdict,exit,diagnostic}-control`)
  assert the predicate rejects anchored-CLEAN output, rc1, and missing
  diagnostic. Verdict counting matches the pre-registered anchored form and
  the sibling-harness convention (`metadata_asof_case:5993`, `tclaims:3504`,
  `tall:4527`). `|| true` is required under `set -euo pipefail` (`:255`) and
  present. Soundness of "no anchored line on any exit-2 path": every verdict
  emitter prints `RESEARCH_GATE: …` at line start (`:1040 :1458 :1745 :2097
  :2286 :2777 :3034`), all after mode work; every `die_usage` path exits
  before them, and no printed usage line is anchored (checked `:305-386`;
  `RESEARCH_GATE_SELFTEST:` does not match the anchored pattern).

## Findings by severity

### HIGH — independent counter's helper extraction breaks on the repaired tree

`corpus/evidence/round27-regressions.py:70` extracts exactly one function:
`re.search(r'^  metadata_asof_usage_case\(\).*?^  }\n', text, re.M | re.S)`.
The patch defines the new predicate in `metadata_asof_usage_accepts` ABOVE
`metadata_asof_usage_case`, so the extracted snippet contains the CALL
(`metadata_asof_usage_accepts "$rc" "$expected" "$out"`, verified in the
extracted 495-byte snippet) but not the DEFINITION (`defines: false`). The
scenario harness (`:85-86`) defines only `cases=0; failures=0; SELF=$1` plus
that snippet, so at call time `metadata_asof_usage_accepts` is an undefined
command: the `if` is false for every scenario, `failures=1`,
`exit $failures` = 1. Predicted, static: `correct-usage-with-help` and
`nonrecord-mention-is-not-verdict` expect 0 and mismatch; the script's
summary goes nonzero. That fails the shared hold "run unchanged … on the
final integrated tree" (round27-claims.md:21-23) even though the predicate
itself is correct. `ExecUsage.patch` does not touch the counter (verified:
single `diff --git a/tools/research-gate.sh` header).

Suggested change (pick one):
- **A (preferred):** inline the anchored predicate back into
  `metadata_asof_usage_case` (`nverdict=$(grep -c '^RESEARCH_GATE: '
  <<<"$out" || true)` + condition), and have `metadata_asof_usage_control_case`
  recompute the same two lines. Both harness functions become
  self-contained; the counter runs unchanged on base and final; no other
  text moves.
- **C:** widen the extractor to
  `r'(^  metadata_asof_usage_accepts\(\).*?^  }\n)?\s*^  metadata_asof_usage_case\(\).*?^  }\n'`
  (optional group), keeping one script text valid on both trees. Touches the
  declared-unchanged file — weaker against the hold's optics.

### LOW — in-script controls are 3 of the 4 promised; add the missing two

Claim C1 names four controls: correct usage passes, exit1 fails, missing
diagnostic fails, actual CLEAN/DRIFT verdict fails. In-script: exit1,
missing-diagnostic, CLEAN-verdict (all want_accept=0). Correct-usage accept
and DRIFT-verdict reject exist only in the independent counter
(`correct-usage-with-help`, `reject-drift-verdict`), and correct usage is
covered transitively by the three real cases. Anchoring is still proven:
the three real cases pass while the help text mentions `RESEARCH_GATE: `
mid-line, which the base substring predicate could not allow. Suggested:
two 2-line `metadata_asof_usage_control_case` calls (accepted=1 correct
usage; `RESEARCH_GATE: DRIFT` rejected) if Option A keeps the helper
self-contained; not required for the claim since the independent counter
carries them.

### INFO — selftest total becomes 190

187 original identities preserved + 3 new controls →
`RESEARCH_GATE_SELFTEST: PASS (190 cases)`. The committed r26 receipt
(3/187, exit 1) stays valid; records citing the post-fix total should say
190. Legacy 1–161 order is untouched (new cases append in the metadata-asof
section), and no in-gate hash pins legacy case output (no `LEGACY_CASES_SHA`
in the gate — that identity is external to `corpus/evidence/round25-holds/`),
so nothing in-tree can go stale.

## Acceptance oracle (concrete)

1. `bash tools/research-gate.sh --selftest`: exit 0; stdout contains
   `RESEARCH_GATE_SELFTEST: PASS (190 cases)`; ok-case lines for
   `metadata-asof-invalid`, `metadata-asof-missing`, `metadata-asof-wrong-mode`
   print `exit=2`; `metadata-asof-usage-{verdict,exit,diagnostic}-control`
   print `accepted=0`; no FAIL-case lines.
2. Per original usage case (fresh process, merged `2>&1`): rc == 2; output
   contains the exact diagnostic (`--as-of must be a valid YYYY-MM-DD date` /
   `--as-of needs YYYY-MM-DD` / `--as-of is only valid with verify-metadata`);
   `grep -c '^RESEARCH_GATE: '` == 0; unmerged stdout empty (tsetup leg).
3. Predicate-branch truth table, driven through the shipped helper text:
   (rc2, diag, help-text mention, no anchored line) → accept; (rc1, diag) →
   reject; (rc2, no diag) → reject; (rc2, diag + anchored `RESEARCH_GATE:
   CLEAN`/`DRIFT`) → reject; (rc2, diag + mid-line `note RESEARCH_GATE: not a
   record`) → accept. First and last rows distinguish anchored from substring.
4. Misuse-hide check: no exit-2 path may print an anchored verdict line; any
   output with `grep -c '^RESEARCH_GATE: '` ≥ 1 must be rejected by the
   harness regardless of rc or diagnostics.
5. `python3 corpus/evidence/round27-regressions.py --gate tools/research-gate.sh`
   on the final tree: exit 0, `C1 mismatches: 0` (all four claim controls plus
   the nonrecord-mention anchoring proof pass). **Predicted today: exit 1 with
   ≥2 C1 mismatches until the HIGH finding is resolved.**
6. No production-mode diff outside `run_selftest`; `--pin`/`--drift` still
   print no `RESEARCH_GATE` line (`:200-203` contract unchanged).

## Cross-seat coupling (C2)

The C2 locale repair must keep the three usage contracts byte-exact — exit 2,
the diagnostic strings above, zero anchored verdicts under any inherited
locale (`--as-of 2026-02-30`, missing value, non-metadata mode). The r27
counter's `ascii-cli-*` scenarios (`:114-119`) pin the same triple. Any C2
edit to `metadata_iso_date` or `die_usage` wording lands inside this oracle.

## Residual risk and verification gaps

- I did not execute the gate, selftest, or counter (read-only seat); findings
  1 and the oracle are static, derived from the exact applied bytes (regex
  re-run in Python on the tree; function-resolution semantics of bash).
- L1 runs the once-only verification: selftest, counter on isolated base
  archive and final tree, legacy battery, frozen receipts; record all exit
  codes and the 190-case total.
- Tools installed: none.
