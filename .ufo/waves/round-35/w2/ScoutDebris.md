# ScoutDebris — r34 w2a2 debris reconciliation

Access date: 2026-10-23. No installs. Read-only git. Nothing deleted.

## Verdict

At wave pin `e87c5d7ea2dbf3730b36a3961de3f06261d015e4`, `find -maxdepth 1 -name '*.md'` under `.ufo/waves/round-34/w2a2` is **26**, and all 26 are tracked (`git ls-files` 26). The three ExecC2Oracle texts the round-34 spot-check called untracked **are tracked**, added together in `6a3cc32cf47c9cda6b10fe8131b53d11fbef2541` (`A`, same blobs through the pin). That commit is the parent of the spot-check commit, so the "3 untracked files" sentence is false of the tree that contains it, not only of freeze tip `08be4c9e`. Not a C1/C2 counter result (those counters were not run).

## Clone

`git clone` of the lane into `/tmp/hyaku/chousa-r35/w2/ScoutDebris/clone`, then `git checkout e87c5d7ea2dbf3730b36a3961de3f06261d015e4` (`GIT_DIR` / `GIT_WORK_TREE` / `GIT_INDEX_FILE` unset). `git rev-parse HEAD` = that pin. Clone `tools/research-gate.sh` sha256 `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617` (same prefix as the landed gate).

`find …/w2a2 -maxdepth 1 -name '*.md' | wc -l` → **26**. Same 26 names from `git ls-files '.ufo/waves/round-34/w2a2/*.md'` with `NF==5`. Beside them: 23 directories, 0 non-md files at maxdepth 1. Ten further `*.md` sit deeper (witness/fixture/receipt files, not seat reports): `CritC2AxisFit/witness/{both-valid,glued}.md`, `MutC3Inject/dispositions-{empty,one,vacuous}.md`, `RevShonenA2/RECEIPTS.md`, `chousa-r34-w2a2-MutC2Trunc-7/probe-fixture/src/r{1,2,3,4}.md`.

Top-level `*.md` (sorted): ConnectorOverlap, CritC2AxisFit, CritC3Claim, ExecC1RerunA2, ExecC2Oracle, ExecC2Rerun, ExecNoHarmA2, ExecSelftestEnv, MutC2Accept, MutC2Boundary, MutC2Counter, MutC2Halves, MutC2Keyed, MutC2NoReader, MutC2Trunc, MutC2Windows, MutC3Bypass, MutC3Inject, RevC2CounterCode, RevC2Knowledge, RevC2Receipts, RevC3Set, RevGateDiff, RevShonenA2, ScoutSkillTally, ScoutSourcesA2.

`git ls-tree -r --name-only` top-level md counts (`NF==5`):

| commit | date (-0300) | top-level md |
|---|---|---|
| `fc93dc5e` (spot-check's named HEAD) | 16:20:04 | 23 |
| `8bc930a9` (parent of the add) | — | 23 |
| `6a3cc32c` | 16:23:56 | 24 |
| `b8b0af76` (spot-check commit) | 16:27:36 | 24 |
| `08be4c9e` (claims.md freeze tip) | 16:32:27 | 26 |
| `e87c5d7e` (this pin) | 16:51:03 | 26 |

`08be4c9e` is an ancestor of `e87c5d7e` (`merge-base --is-ancestor` rc 0). The +1 at `6a3cc32` is `ExecC1RerunA2.md`. The +2 at `08be4c9e` are `ExecC2Oracle.md` and `ExecNoHarmA2.md` (`git show --name-status`, both `A`).

## The three texts

Tracked at the pin (`git ls-tree -r e87c5d7e --name-only` lists them) and at `08be4c9e` and `b8b0af76`, same blobs:

| path | git blob | worktree sha256 |
|---|---|---|
| `…/ExecC2Oracle/boundary-diff.txt` | `688222f8d3ec7a25415c99c15ca933234178e187` | `be41537bb69297c5466764d863c8a54b07dbae977d5c43ba1163638e14ad3ea6` |
| `…/ExecC2Oracle/diff-fuzz.txt` | `ce360a40823df07dc18d80675eb29aca9401e799` | `4a2baa9dd27fbebb01d2c37b027b4e5a0ab164786b5dcf617205b09dbdbe1928` |
| `…/ExecC2Oracle/pcre-boundary.txt` | `7e0159db7b7d224c8363a3e573ce3a550586b47b` | `0a6dfb451c0f481600cc98063006671b61b05ad3843ae0e43152e5c2da0bc117` |

`git hash-object` on the clone worktree matched those blobs. `git log --reverse` for each path has one commit: `6a3cc32cf47c9cda6b10fe8131b53d11fbef2541` "round-34 attempt2: final late wave artifacts" (parent `8bc930a9`). `git show --name-status` marks all three `A` in that commit, with `ExecC1RerunA2.md`. `git cat-file -e 8bc930a9:<boundary-diff.txt>` and the same for `fc93dc5e` exit 128 (not in those trees). `6a3cc32` is an ancestor of `b8b0af76`, `08be4c9e`, and the pin (rc 0); it is not an ancestor of `fc93dc5e` (rc 1). `fc93dc5e` is an ancestor of `6a3cc32` (rc 0).

`ExecC2Oracle.md` is absent at `b8b0af76` (`cat-file -e` rc 128) and present at `08be4c9e` (rc 0). The spot-check line "the seat's report never landed" (`corpus/lessons/round-34-verifier-spotcheck.md:16`, accessed 2026-10-23) matches the tree through `b8b0af76` and is false from `08be4c9e` onward, including this pin.

## Why the spot-check count does not match 26

`corpus/lessons/round-34-verifier-spotcheck.md:15` records a defect of "3 untracked files" at those three paths, and line 83 says to reconcile a report's "23 of 33 committed" against "the 24 `.md` reports on disk". That 23 equals top-level md at the HEAD it names (`fc93dc5e`). That 24 equals top-level md at `6a3cc32` and at the spot-check commit `b8b0af76`. The pin is 26 because `08be4c9e` later added `ExecC2Oracle.md` and `ExecNoHarmA2.md`.

The spot-check commit's parent is `6a3cc32`, which already stores the three blobs. `claims.md` R3 (lines 126–129) is right that the untracked finding is stale at `08be4c9e`; it is already stale inside `b8b0af76`.

The quoted report path `.ufo/reports/round-34/chousa.md` is not in the pin (`git cat-file -e` fatal) and not in live `HEAD`. A whole-tree `git grep -F '23 of 33' e87c5d7e` hits only the spot-check's own line 83. The original "23 of 33" sentence was not re-read.

## `git status --porcelain`

**Clone** at the pin: `git status --porcelain` and `git status --porcelain --ignored --untracked-files=all` produced no lines (rc 0). Snapshot `.ufo/waves/round-35/w2/ScoutDebris/clone-status.txt` is 0 bytes, sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. No untracked or ignored debris under the clone's `.ufo/`.

**Live lane** (not the pin): `git rev-parse HEAD` = `2b2e0171153f63c2fb657ba601d74c7830662c1b`, and the pin is an ancestor (rc 0). The same three blobs are in live `HEAD`. A porcelain snapshot at 2026-10-23T17:00:03-03:00 (`git status --porcelain --ignored --untracked-files=all -- .ufo`) is 50 lines: 47 `??`, 3 `!!`. sha256 `08e8070dfa77b9adfd5e8a340bcf28e4ae02619f295b0d644b59f4e6923cdd76`. Copies: `/tmp/hyaku/chousa-r35/w2/ScoutDebris/live-ufo-status.txt` and `.ufo/waves/round-35/w2/ScoutDebris/live-ufo-status.txt`. Earlier in the same scout the live `??` count was 4, then 36, then 47, so this list is a point in time, not a closed set.

Ignored (all three; `.gitignore:1` is `.ufo/interactive-sessions/`, confirmed with `git check-ignore -v`):

- `.ufo/interactive-sessions/20261015T050057Z/2026-10-15T05-04-00-611Z_01a13df2-2063-75e3-b2a5-ce74040c1857.jsonl`
- `…/3.bash-original.log`
- `…/__advisor.jsonl`

Untracked seats in that snapshot (none are the r34 ExecC2Oracle texts): `CritC2AxisFit/`, `CritGrepClaimScope/`, `ExecC1Control/`, `ExecC1Fresh1/`, `ExecC2Fresh1/`, `ExecC2Fresh2/`, `ExecCounterC1Timing/`, `ExecR34C1V3/`, `MutWitnessThreshold/`, `ScoutManBash/`, `ScoutManExecvp.md`, `ScoutManExecvp/`, `ScoutManGrep.md`, `ScoutManGrep/`, `ScoutSourcesCensus/`. A round-35 report should name these as live worktree debris, not as committed evidence, and should not revive the three r34 texts as untracked.

This file and `.ufo/waves/round-35/w2/ScoutDebris/` were written after that snapshot, so a later live status will also show them. They are not in `e87c5d7e`.

## Limits

Did not re-run C1 or C2 counters. Did not open the fleet commit the spot-check cites for the missing round-34 report. Live `??` set was still growing; only the hashed snapshot is evidence for the list above.