# Attack12

Scoped report: [Attack12/report.md](Attack12/report.md).
Evidence and bounded reproducer: [Attack12/evidence.txt](Attack12/evidence.txt), [Attack12/probe.py](Attack12/probe.py).

High: frozen A10's unknown-rule mutation is not covered by C7's duplicate-id check; frozen A11's changed bad-case return is bypassed by fault case 1. Both gaps demonstrated with bounded probes; full-matrix survival is inferred, not measured, because the runner creates prohibited git commits. A12 demonstrably removes both original quantifier arms, weakening attribution to C8 alone. No frozen rules or production files changed. Advisory only.
