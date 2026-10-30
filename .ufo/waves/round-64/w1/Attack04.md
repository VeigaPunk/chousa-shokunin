# Attack04 — C1 zero-gate review

Full report: [Attack04/report.md](Attack04/report.md). Exact bounded commands/output/exits: [Attack04/evidence.json](Attack04/evidence.json); reproducer: [Attack04/probe.py](Attack04/probe.py).

- **High, known frozen failure:** E12/E13 create filenames and README references using independent random draws. Confirmed frozen SHA-256 `4b3f0b658bcd3bb640cd2e6e56a28a91a72d5352f2610887db01e636fc039fe2` against freeze commit. The distinct supplement repairs those constructors but cannot satisfy the frozen C1 kill rule. No full battery pass is claimed.
- **Medium, independently reproduced oracle weakness:** frozen `c1-battery-v3.py:480–487` accepts all-SKIP exit-2 output with `PREFLIGHT=0/8`, checking numerator instead of run denominator. It also accepts false or malformed FAILED/ENV/SKIPPED sets. Actual judge calls reproduced this for frozen, supplemental and inherited v2 instruments. This is a future-instrument falsifier, not a production defect or admission.
- **Observed production behavior:** Z01/Z02/Z03 each exit 2 and truthfully print `PREFLIGHT=0/0` in production and, separately, the non-production candidate. No zero-gate production defect observed.

Probe command exited 0; each real tool invocation exited 2 as expected. Scratch removed. No installs, clones, network, commits, production/frozen edits or service operations. LSP device unavailable; source evidence uses explicit textual fallback. Full battery, nulls, G08, landing-run closure and unrelated runtime/resume contracts were not exercised. Advisory only; L1 owns integration and closure.
