# R59Reviewer47 — adversarial calibration review

## Finding — positive verdict-path calibration is ungrounded in the available frozen package

**Severity: High (calibration/operability).** The assignment requires `corpus/evidence/round59/claims.md`, but a direct read of that exact path returned “not found.” The round59 evidence directory lists only `census-start.txt` and `controls/c1-before.txt`. `census-start.txt` lines 1–7 is a source-census receipt, not a claim definition or verdict receipt: it records duplicate URLs for W04 S051/S053/S073/S074/S075 and successful reading of `corpus/SOURCES.md`. The only counter output available, `controls/c1-before.txt` lines 3–9, records seven failing refusal legs; lines 14–16 summarize `REFUSE=0/7`, `C1=FAIL`, `EXIT=1`. Its passing empty/rebuild and escape/heldout legs do not establish a positive target verdict. Therefore the intended positive-path predicate, claim-to-source mapping, and report acceptance contract cannot be independently assessed. A positive verdict based on these artifacts would be uncalibrated; the missing input is not evidence that a particular claim is false.

**Falsifier:** Supply the authoritative pre-wave round59 claims bytes (or a traceable corrected location), naming the predicate, evidence boundary, and expected counter/report contract; then provide a receipt for the exact frozen counter and conforming fixture that produces the specified positive verdict, alongside negative controls demonstrating rejection of adjacent invalid cases. Assess each claim only against its mapped captured source evidence. This review did not run tests or fetch sources.

## Scope and residual risk

The context explicitly prohibits live external fetches and identifies open L0 fetch-scope question `8d77e6c1`. Accordingly, the duplicate-URL census observations are provenance/reconciliation leads only—not proof of source-content defects, live-source validity, or source completeness. No claim-level source-grounding conclusion or broad offline-reconnaissance completeness claim is warranted from the census receipt alone. The frozen claims absence and failing-only control receipt leave exact intended behavior and post-change state unknown.

No source/control edits, runtime invocation, external fetch, or installs were performed. No LSP server availability/status was established, so no semantic references/definition/diagnostics were claimed. Verification gap: this is artifact-level review only; no claim bytes or positive-path receipt were available.

Report trailer: `.ufo/waves/round-59/w1/R59Reviewer47.md`
