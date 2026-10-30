# Attack06 — Unicode mirror review

Full report and reproducible evidence: [Attack06/report.md](Attack06/report.md), [probe output](Attack06/probe-output.txt), [driver](Attack06/probe.py).

- High: frozen E12/E13 independently drawn names prevent honest C1 full-pass closure; the distinct supplement cannot replace the frozen kill rule.
- Medium: inherited `controls/ref-preflight-v3.py` ignores Unicode and nested phantom paths. Minimal NFC/NFD/nested Unicode phantom fixtures return PASS/exit 0; ASCII phantom control fails/exit 1.
- Observed current `tools/lane-preflight.py` rejects those phantoms and accepts both valid NFC/NFD directions. No current Unicode mirror defect reproduced; no landing or full-battery success inferred.

12 bounded G02 CLI probes; driver exit 0. LSP unavailable. No installs, production edits, clone, or network. Scratch removed. Advisory only.
