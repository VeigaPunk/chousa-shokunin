# Attack09 — C2 A01/A02/A03

Scoped report: [Attack09/report.md](Attack09/report.md). Reproducible driver and full command/stdout/stderr/exit evidence: `Attack09/probe.py`, `Attack09/evidence.json`.

Ten bounded probes against committed v1/v2 bytes distinguish all three mutations: A01/A02 turn stale exit 2 into 0; A03 moves the required FLAG line off stdout. All six compared inherited artifacts exactly match freeze `bf40d99bda9eefdad3ed6276da077cfb24ba82f1`. No scoped C2 falsification found; no full-matrix closure asserted. Advisory weaknesses: runner reads working target bytes rather than enforcing committed provenance; honest stale summaries still print PASS despite exit 2. Frozen C1 E12/E13 failure is not repaired or hidden by supplements.

Driver exit 0; Python 3.14.8 preinstalled; no installs, network, git mutations, clones, or production edits. Seat scratch removed. Findings advisory only.

Report: .ufo/waves/round-64/w1/Attack09/report.md
