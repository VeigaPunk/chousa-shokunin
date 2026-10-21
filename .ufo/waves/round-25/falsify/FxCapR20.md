# FxCapR20 — round-25 capability-row review

Axes checked: freshness (current case IDs) and calibration (capability scope / first-working round).

Checkpoint: private clone started at `0fc037e6b07f3820ead8c9207a8034ac854197a1` (observed), then fetched and tested full integration pin `e93ac711f885a10d44fdd80a1734997419595b5a`. No live-lane mutation. `corpus/lessons/round-25.md:111-133` records the initial packaging failure: 0fc prose claimed 154 cases but carried the old 136-case gate; d8c fixed the gate but still omitted `corpus/evidence/README.md`; e93 is the full-pin used here.

R20 claim and row: `LOG.md:759-764` describes the HTML-comment `## Meta` shadow as distinct from r17's fenced-heading case, reports pre-fix CLEAN → post-fix `SCOPE_BOUNTY_ABSORBED` + DRIFT, and says case 124 pins the comment arm. The R20 verdict admits that narrow fix and points to `corpus/knowledge/html-comment-r20.md`. `SCORECARD.md:1320` accurately records that HTML-comment headings are literal during scope parsing, preventing a fake `## Meta` from shadowing the real declaration; it assigns first-working round 20. The knowledge note's mechanism and named limits are at `corpus/knowledge/html-comment-r20.md:9-32`.

All eight knowledge pointers in the reconciliation table resolve in the private pin. R20's four cited receipt files (demo, selftest, battery, drift) also resolve; the R15, R22, and R23 selftest receipts resolve. Historical receipt IDs agree with the table's distinction between original and current numbering: R15 receipt 107–110 (`corpus/evidence/root-r15-20261019T152000Z-selftest.log:107-111`), R22 receipt 129–132 (`corpus/evidence/deny-r22-20261019T190000Z-selftest.log:129-133`), R23 receipt 129 (`corpus/evidence/fanchor-r23-20261019T192000Z-selftest.log:129-134`), and R20 receipt 124 (`corpus/evidence/verify-r20-20261019T180000Z-selftest.log:124-125`).

Assigned current-pin run: `bash tools/research-gate.sh --selftest` in `/tmp/chousa-r25-FxCapR20` at e93. Relevant output only:

```text
ok-case  107 claims-root-slash-absent     exit=1
ok-case  108 claims-root-slash-read       exit=0
ok-case  109 claims-root-slash-xdev       exit=1
ok-case  111 sweeps-root-slash            exit=0
ok-case  124 scope-comment-shadow         exit=1
ok-case  129 chain-fence-anchor           exit=1
ok-case  130 claims-config-start          exit=1
ok-case  131 claims-omp-start             exit=1
ok-case  132 claims-localstate-start      exit=1
ok-case  133 claims-config-adjacent       exit=0
RESEARCH_GATE_SELFTEST: PASS (154 cases, 0 skipped)
```

The current case IDs therefore match `SCORECARD.md:1316,1320,1322-1323`; the round-20 behavior is still case 124. Historical first-working round 20 does not overclaim: LOG's demonstrated defect and fix are the HTML-comment shadow specifically, while r17 remains the distinct fence case. The row can be retained unchanged.

Findings: none. Residual risk: the row is only a scope-parser capability, not a general Markdown/HTML parser claim; the knowledge note names CDATA, processing instructions, and other HTML constructs as limits. Verification gap: no LSP device/status endpoint is exposed in this runtime; the earlier text search was used only to locate documentation lines, not as semantic proof. No installs.

VERDICT: Retain the round-20 capability row unchanged; observed behavior and current case IDs support its historical first-working attribution.