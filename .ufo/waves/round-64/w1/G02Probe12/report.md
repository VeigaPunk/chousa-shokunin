# G02 invalid UTF-8 filename probe

Frozen claim: R64-C1 lines 60–61 requires reported invalid-UTF8 names be backslash-replaced so stdout remains strictly decodable.

Fixture: temporary root with corpus/knowledge/bad_<byte-ff>.md and corpus/README.md containing only `Index`. Recipe: `fixture-recipe.py`; run from a fresh scratch location. Candidate: `corpus/evidence/round64/controls/ref-preflight-v3.py` (read only).

Command: `python3 <candidate> --root <fixture> --only G02` (probe driver created the filename and invoked the candidate via subprocess).

Observed: exit 1; stdout bytes: `GATE G02 knowledge-index FAIL 1 not named in corpus/README.md: bad_\\xff.md` with all other gates SKIP, and final summary `PREFLIGHT=0/1 FAILED=G02 ...`; stderr empty. Stdout strictly decodes as UTF-8. This matches the frozen requirement for the reported name. No candidate edits. No tools installed.
