# G02Probe10 — percent-encoded spaces

- Frozen contract: `corpus/evidence/round64/claims.md`, R64-C1 G02 index normalization requires percent-encoding in link targets to be unquoted before matching; a valid indexed entry therefore passes.
- Candidate: `corpus/evidence/round64/controls/ref-preflight-v3.py` (not production; not modified).
- Isolated fixture: file `corpus/knowledge/space name.md`; README link target `knowledge/space%20name.md`.
- Command: `python3 /fast/scratch/hyaku/chousa-r64/G02Probe10/probe.py`
- Output: `FIXTURE=percent-encoded-space-link-target`; `OBSERVED=PASS 1 entries indexed`; `EXPECTED=PASS 1 entries indexed`; `MATCH=1`.
- Exit: 0.
- Result: observed behavior matches the exact expected G02 verdict and detail for this fixture. Recipe preserved in `fixture-recipe.md`.
- Frozen failure caveat: claims.md records E12/E13 as failures of the frozen before-tool (both `rc=1 want 0`); this probe is narrow evidence about the candidate only and does not revise or cure that recorded frozen result.
- Tool installs/updates: none.
- Risk/scope: this single case does not establish the full G02 contract or production readiness.
