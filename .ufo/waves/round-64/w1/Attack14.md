# Attack14 — C2 selftest fault injection

Full scoped report and reproducible evidence: [Attack14/report.md](Attack14/report.md), [Attack14/probe.py](Attack14/probe.py).

High: frozen fault-1 handling returns 1 before reaching the real selftest failure guard. The exact frozen A11 mutant changes that real guard to return 0, yet still satisfies R6 (exit 1 plus FAULT). Bounded probe observed genuine bad-fixture failure exiting 1 in frozen v2 and incorrectly exiting 0 in A11; fault 1 made both exit 1 with identical FAULT output.

The ordinary frozen CLI fault leg reproduced exit 1. This refutes the injection's claimed guard coverage; the full 12/12 count was not executed because the full runner creates git-mutating fixtures forbidden to this seat. No full count is asserted. Frozen-byte comparison and SHA-256s are in the detailed report. No supplements or production edits. C1 E12/E13 frozen failure remains unrepaired. Scratch was removed by the probe; no tools installed.
