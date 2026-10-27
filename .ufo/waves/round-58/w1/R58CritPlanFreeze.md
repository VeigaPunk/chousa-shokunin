# Round 58 plan/freeze critique

## Scope and comparison
- `SCORECARD.md:2889-2891` labels Round 58 “(not started)” and lists candidates including the build-spans hardening set and S101, alongside other routed items. `LOG.md:1904` names `b13ca7b5c8bbb40d2d29a37fb443c64ca043f791` as claim base and says claims were frozen before wave data.
- Frozen `claims.md:5-11,13-21` narrows the work to the declared C1 build-spans battery and C2 S101 entry; it explicitly disclaims general security and truth beyond the located source text. This is consistent with selecting two candidates from the plan, not evidence that the other planned candidates were completed.
- `git show b13ca7b5c8bbb40d2d29a37fb443c64ca043f791:tools/build-spans.py | sha256sum` → `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  -`, matching the declared r55 pin. The r55 control file hashes to the same value.

## Frozen controls actually exercised
Command: `python3 corpus/evidence/round58/c1-count.py --builder tools/build-spans.py --work /fast/scratch/hyaku/chousa-r58/R58CritPlanFreeze/c1-base-run --controls corpus/evidence/round58/controls` (run from lane root; exit 1).
Observed exact lines:
```text
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)
BEFORE_FOREIGN=deleted
CONTROL_REFUSEALL=denied
CONTROL_build-spans-r55=denied
DENIED=2/2
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=FAIL
```
Thus neither named control reached full C1=PASS; the base exhibits the declared FOREIGN failure. I also ran a zero-output no-op builder; its exact result included `EMPTY_OK=fail(no spans.tsv)` and ended `C1=FAIL`. No full do-nothing control reached C1=PASS.

## Predicate-sizing counterexamples
1. **C1 under-enforces the SYMLINK_OUT reason.** `c1-count.py:231-236` first checks for nonzero exit and a `SYMLINK` reason, but then unconditionally replaces that result with `SYMLINK_OUT=pass(refused)` whenever the symlink target directory is empty. A scratch builder that detects the output symlink, silently exits 0, and prints no refusal reason produced the exact line `SYMLINK_OUT=pass(refused)`; its full run still ended `C1=FAIL` on other legs. So this is a leg-level false pass, not evidence a no-op meets the full C1 target. It contradicts `claims.md:9,11` / counter docstring `c1-count.py:15-19`, which require a named refusal reason and kill on a missing reason.
   - Smallest safe correction for a re-freeze: do not overwrite `expect_refuse` failure; require nonzero rc plus `SYMLINK` reason and untouched target.
2. **C2 NEW_GROUND checks the wrong Unicode character.** `c2-count.py:153-154` searches the base for traditional `載体类型标识` but checks the entry for simplified `载体类型标识`; the frozen claim at `claims.md:19` names the simplified form. In the claim base, `git grep -l '载体类型标识' b13ca7b -- corpus/knowledge` and the corresponding search for traditional `載体类型標识` each returned rc=1 (no matches); the pinned S101 text form has 3 simplified occurrences and 0 traditional. Therefore the base fact is true today, but the counter would not detect simplified ground already present in a future/base tree: its “new ground” absence predicate is weaker than the frozen claim.
   - Smallest safe correction for a re-freeze: make the base search use the same simplified literal as the claim/entry check. Do not reinterpret the frozen claim to fit the counter.
3. **Control-name documentation overstates coverage.** `c1-count.py:10-11,169` names `NAIVE.py`, but its actual loop at `:362-380` checks only `REFUSEALL.py` and `build-spans-r55.py`; `build-c1-controls.py` generates those two, not NAIVE. The claim itself names the r55 and always-refuse controls, and both were denied in the run above; this is stale counter documentation, not a third measured control.

## Freeze discipline and before receipts
- `git diff --name-status 9e73a031ab1ac3bac343de008850d7d87f9e5634..HEAD` showed only additions: `controls/REFUSEALL.py`, `controls/build-spans-r55.py`, `controls/c1-controls.txt`, `controls/c2-before-frozen.txt`, `controls/c2-controls.txt`, and `s101-open.txt`. The frozen claims, counters, quote set, and SCORECARD have no post-freeze edits. The commit sequence was 9e73a03 (14:07:54), 718e8d2 (14:11:58), 5da0a63 (14:18:14); no rule change after scoring is evidenced.
- **Freeze completeness defect, not a rule change:** at 9e73a03, `c1-count.py` already required `controls/build-spans-r55.py` to set `BEFORE_FOREIGN=deleted` and requires that exact value for C1 PASS (`:392-394`), but that file was only added in 718e8d2. I copied the unchanged counter to owned scratch without that later-added control and ran it; observed `BEFORE_FOREIGN=absent`, `DENIED=0/0`, `C1=FAIL`. Thus the named freeze tree could not score C1=PASS until the follow-up control artifact landed. It landed before the recorded dispatch (14:24:35); no rule file changed.
- C2 receipts represent different roots, not a demonstrated rule edit: `c2-before.txt` includes `QUOTES_MISSING` (base has no frozen quote file), while `c2-before-frozen.txt` records a lane-root run with quotes present and `BUILDER_REBUILD_MISMATCH`. My exact frozen command, `python3 corpus/evidence/round58/c2-count.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin --work /fast/scratch/hyaku/chousa-r58/R58CritPlanFreeze/c2-before-run`, exited 1 and included `ERROR BUILDER_REBUILD_MISMATCH`, `ERROR ENTRY_MISSING`, `ERROR REF_ID_UNBOUND`, and `C2=FAIL`, matching the latter state. Both before states fail; the receipts should not be conflated.

## Assessment
The claim scope/base comparison survives: the r55 pin is correct, the two named C1 controls fail, and the frozen rule artifacts did not change after the freeze commit. The freeze was incomplete at commit 9e73a03 because a required control artifact landed afterward, though before dispatch. The frozen C1 and C2 predicates each have the bounded enforcement defects above; neither was shown to make a full do-nothing control pass. No live fetch, lane source edit, git mutation, or install was performed.

VERDICT: Round-58 claim sizing against the planned row and claim base survives; no post-score rule change is evidenced. The claim-level C1/C2 gates are not falsified by the named no-op controls, but the C1 SYMLINK_OUT leg and C2 new-ground absence check are falsified as faithful implementations of their frozen criteria; C1 freeze completeness at 9e73a03 is also falsified.