# R57W1SonicState — round 57 wave 1 mechanical state collection

Seat: executor. Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin` (read-only except this report). Snapshot clock `SNAP_UTC=2026-10-27T08:44:32Z` (six items captured in one atomic batch). No tool installed/upgraded (none needed; no pacman transaction). No git/jj mutating command run anywhere. Scratch only under `/fast/scratch/hyaku/chousa-r57/R57W1SonicState/` (`TMPDIR` there, `PYTHONDONTWRITEBYTECODE=1`); **deleted before yield** (Cleanup). One section per item.

## (1) `jj-lane.sh state`

```
$ /home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/chousa-shokunin
state branch=master local=e0e73e0f76163b014033e80c6ba53ed92c14113d remote=e0e73e0f76163b014033e80c6ba53ed92c14113d ahead=0 behind=0 head=detached tracked=3 untracked=40
```
Same session, earlier reads (lane written live by the L1 and siblings): `08:42:1xZ tracked=2 untracked=19` → `08:43:03Z tracked=3 untracked=30` → `08:44:00Z tracked=3 untracked=39` → `08:44:32Z tracked=3 untracked=40`; `local`/`remote`/`ahead`/`behind`/`head=detached` constant in all four. `git branch -a -v`: `* (no branch) e0e73e0`, `master e0e73e0`, `remotes/origin/master e0e73e0`.

## (2) `git ls-remote origin refs/heads/master`

```
$ git -C /home/vgpnk/Projects/shokunin/chousa-shokunin ls-remote origin refs/heads/master
e0e73e0f76163b014033e80c6ba53ed92c14113d	refs/heads/master
```
Local `HEAD` == `origin/master` == `e0e73e0f76163b014033e80c6ba53ed92c14113d` (no ahead/behind).

## (3) `git log --oneline -5`

```
$ git -C /home/vgpnk/Projects/shokunin/chousa-shokunin log --oneline -5
e0e73e0 round-57: C2 after-receipt — SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 (S083 S087 S113 S114 S121, absent=0) UNREACHABLE=1 (S105, 3 failed attempts >=600s apart) BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS; attempt-2/3 fetch rows; record-less wrap-up S105 bytes removed (named in report)
a03824d round-57: W1 spec+dispatch (65 seats, one v2 wave validated under policy v2: 12 scouts/21 executors/13 reviewers/6 critics/6 scribes/2 mutation-testers/2 connectors/sentinel/revenger/simplifier; attack share 21/65=32%); dry-run receipts (clone runs, archive env-errors, build-spans STALE=0, census exit 0); L1 fetch pass-1 counter run (43/47, 38 REPRODUCED, 5 DRIFTED absent=0)
f9736a3 round-57: L1 re-fetch pass 1 — 47 pinned captures attempted, 43 stored lane-owned (38 REPRODUCED / 5 DRIFTED / 4 pending retry); tools/capture-fetch.py (recipe-frozen, 3-attempt cap); refetch.tsv; misroot sweep of the tool's first run recorded in the round lesson
b022b13 hyaku run9 wrap-up: remaining round-57 captures
fd95724 round-57: freeze R57-C3 (normative-reference-chain counter, before receipt, controls)
```
Commit-identity checks against the frozen claims: `git cat-file -t 6656f0770a1460d6ba73d9d2976f698a35311921` → `commit`; `git log --oneline -1 c2f914c53201a8f8ee4fef823b82681051d55592` → `c2f914c round-57: freeze R57-C2 (freshness re-fetch counter, before receipt, controls, egress table, census start)`; `git log --format='%H %s' | grep 'freeze R57-C3'` → `fd95724d56a33ad150cd2638fadd2ce1f3425e6c round-57: freeze R57-C3 (normative-reference chain counter, before receipt, controls)`; `git log --oneline -1 f9736a39a0344a0aed63a65dfaddf7db624303d9` → `f9736a3 round-57: L1 re-fetch pass 1 …`.

**Discrepancy reported, not patched:** the brief names the C3 freeze `fd95724d56a33a150cd2638fadd2ce1f3425e6c`; the lane's commit is `fd95724d56a33a**d**150cd2638fadd2ce1f3425e6c` (position 13 `d`, not `1`; the brief's string is not a revision here — `git rev-parse fd95724d56a33a150cd2638fadd2ce1f3425e6c` → *unknown revision*). Same 7-hex prefix `fd95724`, same subject ⇒ transcription slip in the brief, not a different commit.

## (4) `disk-guard.sh status`

```
$ /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status
root                             use%     free
/tmp                               3%   124.6G
/var/tmp                           35%   589.3G
/fast/scratch/hyaku               26%   600.1G

top consumers /tmp
    367.3M idle=1176  /tmp/.mount_KimiCogEAx7f
    367.3M idle=5872  /tmp/.mount_KimiColz3RmH
    26.7M idle=340  /tmp/omp-agent-recovery-20261026
    24.5M idle=228  /tmp/node-compile-cache
```
Top scratch consumer `4.4G → 7.2G /fast/scratch/hyaku/chousa-r57` over the session (sibling fixtures, not mine: `du -sh …/R57W1SonicState` = `4.0K`); 600 G free.

## (5) Counts

```
$ find /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/captures -maxdepth 1 -type f | wc -l   → 111
$ find /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/captures -type f | wc -l              → 111  (no subdirs)
$ find …/corpus/captures -type f -printf '%f\n' | sed 's/.*\.//' | sort | uniq -c                → 57 raw / 54 txt
$ wc -l < …/corpus/evidence/round57/refetch.tsv                                                 → 123  (1 header + 122 data rows)
$ find …/.ufo/waves/round-57/w1 -maxdepth 1 -type f -name '*.md' | wc -l                        → 26
```
Live and rising during the wave (L1 fetches + sibling reports land) — `utc / captures / refetch lines / refetch sha256[0:16] / w1 .md reports`: `08:41:2xZ 105 115 56eb112bb8fec9a4 14` → `08:42:1xZ 107 119 88e6bf88c4677b2b 17` → `08:43:0xZ 107 121 969e1fa9bf98276a 19` → `08:43:4xZ 107 121 969e1fa9bf98276a 21` → `08:44:0xZ 111 123 3f01c401c036f0e1 24` → `08:44:32Z 111 123 3f01c401c036f0e1 26`.

Key split of the store (08:42Z, 55 keys): 52 keys carry `.raw`+`.txt`; 3 keys are `.raw`-only — `53a92273a452a58f28368691`, `d473754a0cbf8d3095255d5a`, `d8b4f8f8829b813f16227893` (`file -b` → `PDF document, version 1.4, 31 page(s)`, `version 1.5, 66 page(s)`, `version 1.7, 68 page(s)`); no `.txt`-only key. These are the "three orphans" named in `.ufo/waves/round-57/gen-w1-spec.py:120,248`: `53a92273…` was committed by `b022b13` with **no** `refetch.tsv` row, while `d473754a…`/`d8b4f8f8…` appear there only as failed attempts (`curl_rc=28`, `raw_sha256=-`) — their bytes predate this round's fetch record.

## (6) sha256 of `refetch.tsv`

```
$ sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round57/refetch.tsv
3f01c401c036f0e1f53587d57b932791d23553711329b27368178cc96934d8ef  …/corpus/evidence/round57/refetch.tsv
```
Earlier digests this session (file appended to live): `56eb112bb8fec9a4…c34a` (115 lines, 08:41Z) → `88e6bf88c4677b2b…254a` (119) → `969e1fa9bf98276a…cfe6` (121) → `3f01c401c036f0e1…d8ef` (123, 08:44Z). Header: `id url key attempt fetched_utc curl_rc http_code raw_sha256 txt_sha256`.

## Frontier state of the two frozen claims (read-only runs of the unmodified frozen counters, from the lane root)

```
$ cd <lane> && python3 corpus/evidence/round57/c2-count.py
SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS
exit=0
$ cd <lane> && python3 corpus/evidence/round57/c3-count.py
ENTRY=no S127_CITED=no NEW_GROUND=no CLAUSE=no
BOUND=0/7 (min 4) -
SWEPT=0/7 -
QUOTE_ROWS=0 IN_SPAN=0 IN_ENTRY=0 IN_LESSON=0 SHORT=0 CONTEXT=0 CAPTURE_BOUND=0
SUBSTANCE=FAIL ANCHOR_BOUND=0/0 INFERENCE_GROUNDED=no STRAY_IDS=-
C3=FAIL
exit=1
```
Deltas vs the dispatch brief, for the L1's integration: **C2 moved 43/47 → 47/47** and prints `C2=PASS` (41 REPRODUCED / 5 DRIFTED / 1 UNREACHABLE), not the brief's 38/5/0 — `S100 S103 S106` are now REPRODUCED, `S105` ended UNREACHABLE (3 failed attempts). **C3 is still at its before-state** (`BOUND=0/7`, `C3=FAIL`) — its build has not started in the lane. S105 spacing from `refetch.tsv` (all three `curl_rc=28`, `raw_sha256=-`): attempt1 08:06:12Z → attempt2 08:30:12Z = **1440 s** ≥ 600 s; attempt2 → attempt3 08:33:48Z = 216 s; the counter's ≥600 s rule is met by the 1↔2 pair (its own `UNREACHABLE` line confirms it), so the 216 s second gap is an observation, not a predicate defect.

## Cleanup / boundaries

- Wrote exactly one file: this report. No other lane file created/modified/deleted; no fleet-root file touched; `/home/vgpnk/Projects/shokuknow` never written or executed.
- No `git commit/add/stash/checkout/reset/push` and no mutating `jj` command anywhere, incl. scratch. No external network fetch: every byte inspected came from the committed lane store.
- Scratch `/fast/scratch/hyaku/chousa-r57/R57W1SonicState/` (2 snapshot text files) **removed before yield** (`rm -rf -- "$S"`; post-delete `ls` → *No such file or directory*).

**VERDICT: mechanical state collection for round-57 w1 (lane state, ls-remote, log -5, disk-guard, capture-store / refetch.tsv / seat-report counts, refetch.tsv sha256) COMPLETED and pasted above — items 1-4 stable and unchanged, items 5-6 live-moving artifacts (captures 105→111, refetch 115→123 rows, reports 14→26 during the session); one brief/repo discrepancy found and reported (C3 freeze `fd95724d56a33a150c…` vs actual `fd95724d56a33ad150c…`); no frozen predicate, counter, target or recipe touched.**
