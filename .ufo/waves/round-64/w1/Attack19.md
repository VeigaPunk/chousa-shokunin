# Attack19

Full scoped report and reproducible evidence: [Attack19/report.md](Attack19/report.md).

- All seven frozen instrument digest prefixes, plus v1 checker identity, match committed and inherited bytes; frozen claims are unchanged.
- First-add history places original R5 round64 instruments and claims in the same commit. The next commit substitutes older round63 audit subjects and records PASS; that result cannot establish the original round64 provenance assertion. This is a calibration/scope weakness, not a demonstrated C2 kill-rule failure.
- Frozen E12/E13 fixture mismatch remains visible and distinct from the post-freeze supplement; no supplemental result can count as frozen C1 success.
- Read-only git/hash probes only. No installs, production edits, network, clone, scratch, or battery/runtime execution. No cleanup remains.
