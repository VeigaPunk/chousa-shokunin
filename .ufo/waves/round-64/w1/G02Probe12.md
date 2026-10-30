# G02Probe12 — scoped findings

Invalid UTF-8 fixture and raw command output evidence recorded in this folder. The candidate produced a UTF-8-decodable escaped filename and exited with the expected G02 failure; frozen clause (v) is satisfied for this input.

Files: `G02Probe12/fixture-recipe.py`, `G02Probe12/report.md`.

Risks/limits: this single filename exercises the contract clause for invalid UTF-8 reporting only; it does not establish the entire G02 contract or production acceptance. The frozen C1 battery outcome remains as recorded in claims.md and is not changed by this probe.
