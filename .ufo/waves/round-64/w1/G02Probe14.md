# G02Probe14 — directory symlink/cycle probe

## Scope and frozen contract
Read frozen `corpus/evidence/round64/claims.md` before probing. This was an isolated call to the candidate's `g02()`; the candidate was not edited and no lane-preflight production code was run. Frozen R64-C1 clause (claims.md lines 47–52): recursive walk of `corpus/knowledge/`; every non-directory entry must be a regular `.md` (except `.gitkeep`), and symlinks are judged by target; a symlink to a regular `.md` passes, while a dangling or non-file symlink FAILs.

## Fixture recipe
Using Python 3.14.8, the scratch fixture driver created an isolated `lane/corpus/knowledge/` with (1) `symlink.md` pointing to a regular `outside.md` file and (2) directory symlink `cycle` pointing back to `knowledge/`; README contained `symlink.md cycle.md`. It invoked candidate `g02(root, argparse.Namespace(), os.environ.copy(), base/'work')` directly. Fixture root: `/fast/scratch/hyaku/chousa-r64/G02Probe14/fixture/lane`. Recipe retained here (driver used for run): `probe.py` in the seat scratch root; equivalent actions: make the directories and README, create `outside.md`, symlink `knowledge/symlink.md` to it, symlink `knowledge/cycle` back to `knowledge`, then call g02.

## Exact command and observed result
Command (cwd `/fast/scratch/hyaku/chousa-r64/G02Probe14`): `python3 probe.py`
stdout:
```
FIXTURE_ROOT=/fast/scratch/hyaku/chousa-r64/G02Probe14/fixture/lane
SYMLINK_TARGET_IS_FILE=True
CYCLE_POINTS_TO_ROOT=True
RESULT=('PASS', '1 entries indexed')
```
Exit: 0.

## Finding
The valid file symlink was counted and passed, matching the explicit contract. The directory symlink back to the root was silently omitted: candidate uses `os.walk(..., followlinks=False)` and iterates `fs` only, not directory entries `ds`. Thus the README's `cycle.md` did not cause failure and the gate passed with one indexed entry. Under the frozen condition that a symlink whose target is not a regular `.md` file FAILs, this directory symlink should fail rather than be silently ignored; observed result does not match that reading of the frozen contract. Cycle traversal itself was avoided (no recursion hang), but omission means no validation of the symlink target. This is advisory evidence only; no candidate or production edits made.

Tools installed/updated: none.