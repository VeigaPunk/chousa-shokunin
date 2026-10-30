# G02Probe10 — scoped finding

The isolated percent-encoded-space fixture against candidate `corpus/evidence/round64/controls/ref-preflight-v3.py` matched frozen R64-C1 G02 expected behavior: `PASS 1 entries indexed` (expected exact tuple; observed exact tuple; `MATCH=1`), command exit 0. The fixture used `corpus/knowledge/space name.md` and README target `knowledge/space%20name.md`. The candidate was not edited. Repro recipe and full report are in `.ufo/waves/round-64/w1/G02Probe10/fixture-recipe.md` and `report.md`.

Claims.md frozen before-receipts remain honest and unchanged: E12/E13 are recorded as `rc=1 want 0` against the before-tool. This narrow candidate probe does not repair that frozen result or establish broader contract/production readiness. Tool installs: none. No blockers.