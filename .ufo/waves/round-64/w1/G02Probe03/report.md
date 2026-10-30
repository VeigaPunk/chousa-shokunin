# G02 unreadable/unsearchable-root probe

Candidate: `corpus/evidence/round64/controls/ref-preflight-v3.py` (reference candidate only; unchanged). Frozen requirement: claims.md R64-C1 (lines 47–52): missing, non-directory, or knowledge root not readable+searchable by running uid MUST fail; no `.md` entries MUST fail.

## Fixture and commands

Recipe retained in `G02Probe03/fixture-recipe.txt`. Scratch roots under `/fast/scratch/hyaku/chousa-r64/G02Probe03/`; each held `corpus/README.md` containing `good.md`, `corpus/knowledge/good.md`, work dir. Only difference: A root mode 000; B root mode 111. Both commands invoked candidate with `--only G02 --fleet /home/vgpnk/Projects/shokunin` and separate `--work` directories.

A initial setup attempt failed before candidate execution (`failed to redirect ... Permission denied`, rc 1); adjusted fixture creation ordering and reran successfully. Successful A command stdout: `GATE G02 knowledge-index FAIL corpus/knowledge is not readable/searchable by this uid` (other gates SKIP); summary `PREFLIGHT=0/1 FAILED=G02 ...`; rc 1.

B command stdout: `GATE G02 knowledge-index FAIL 0 entries indexed (corpus/knowledge holds no *.md entry)` (other gates SKIP); summary `PREFLIGHT=0/1 FAILED=G02 ...`; rc 1.

Commands returned exact rc 1 for both successful runs. B’s test is limited: mode 111 prevents directory listing, but also owner cannot read the markdown file under normal traversal because directory lacks read; the tool reports zero entries. Thus it confirms a failure, but does not independently isolate search-only permission behavior from traversal’s empty result.

## Result

Observed result matches the frozen expected failure for unreadable/unsearchable root in A. B fails too, but observed failure is the required zero-entry failure rather than the explicit accessibility message. No claim that the frozen fixture mismatch identified in C1 is repaired; this probe does not execute that battery. The candidate was not edited. No tools installed.

## Cleanup

Scratch removed before yield; retained recipe and this report only.