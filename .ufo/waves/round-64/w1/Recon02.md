# Recon02

Full scoped findings and command/output/exit evidence: [Recon02/report.md](Recon02/report.md).

Opened installed GNU coreutils 9.12 `realpath(1)` and Info node `realpath invocation`. Exact `-e` paragraph: “Fail if the named file does not exist. A trailing slash requires that the name resolve to a directory.” The man page states “all components of the path must exist”.

Caveat: unqualified `realpath` resolves to a shell builtin reporting 0.8.0; `/usr/bin/realpath` is GNU coreutils 9.12. Use the absolute executable for GNU-specific behavior claims. Confidence: high. No behavioral probes or claim-closure measurements; no installs or scratch created.

Report: .ufo/waves/round-64/w1/Recon02.md
