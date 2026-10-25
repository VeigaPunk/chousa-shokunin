# ScoutInheritedTree — round 47 wave 1

Item: report `git status --porcelain`, `git diff --stat`, lane tip via `jj-lane.sh state`; confirm the three modified JSON paths are the previously left-named ones (grep round-46.md / round-44.md); name every untracked path; check `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md` for an operator answer to 8d77e6c1 and the chousa round-43/44 questions. Report only. Snapshot taken 2026-10-25 ~08:43 -03, before this report file was written.

## Commands and verbatim output (trimmed)

```
$ git -C /home/vgpnk/Projects/shokunin/chousa-shokunin status --porcelain
 M .ufo/waves/round-40/w1/swarm-registry.json
 M .ufo/waves/round-41/w1/swarm-registry.json
 M corpus/evidence/round41/receipts/cells/cells.json
?? .ufo/waves/round-47/gen-w1-spec.py
?? .ufo/waves/round-47/w1-dispatch.json
?? .ufo/waves/round-47/w1-run.err
?? .ufo/waves/round-47/w1-spec.json
?? .ufo/waves/round-47/w1/

$ git -C /home/vgpnk/Projects/shokunin/chousa-shokunin diff --stat
 .ufo/waves/round-40/w1/swarm-registry.json        |  70 +--
 .ufo/waves/round-41/w1/swarm-registry.json        | 641 ++++++++++++++--------
 corpus/evidence/round41/receipts/cells/cells.json | 185 +++++--
 3 files changed, 612 insertions(+), 284 deletions(-)

$ git -C ... diff --numstat
36   34   .ufo/waves/round-40/w1/swarm-registry.json
427  214  .ufo/waves/round-41/w1/swarm-registry.json
149  36   corpus/evidence/round41/receipts/cells/cells.json

$ bash /home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/chousa-shokunin
state branch=master local=a15610a59aaeaf43b79ccc650acee4bd4da00341 remote=a15610a59aaeaf43b79ccc650acee4bd4da00341 ahead=0 behind=0 head=detached tracked=3 untracked=5

$ git -C ... log -1 --format='%H %s'
a15610a59aaeaf43b79ccc650acee4bd4da00341 round-47: C1 polarity probe in tools/inference-ground.py (INF_POLARITY_FLIP)
```

The lane tip is `a15610a5…`, the commit where C1 landed, and local matches remote. jj's `tracked=3 untracked=5` agrees with git. No tracked production file (SKILL.md, SOURCES.md, counters, entries) was modified at snapshot time.

## (1) The three modified JSONs are the previously left-named ones: CONFIRMED

```
$ sha256sum <three paths>
c4e00d1141a0faaf0dfd655b9173ef974b702d668efd9751caab78658e3fb0d0  .ufo/waves/round-40/w1/swarm-registry.json
49b059533008951e54dc2e4c03ecf0b5352e1ec30eaf7af512e516be07bc4b59  .ufo/waves/round-41/w1/swarm-registry.json
1f5c0afae8024c50013e9a9060988c14506115125e3823042e4512833f293b80  corpus/evidence/round41/receipts/cells/cells.json
$ git -C ... diff | sha256sum
30418103ec9be8b6092fcdb8bd247849c437b7556500cc24cbb9288df3f7a041  -
$ stat -c '%y %n' <three paths>
2026-10-24 04:18:06.847 -0300  round-40/w1/swarm-registry.json
2026-10-24 04:42:46.930 -0300  round-41/w1/swarm-registry.json
2026-10-25 06:36:03.613 -0300  cells.json
```

- A grep for the file names (`swarm-registry\.json|cells\.json`) over round-44.md and round-46.md returns **no match**. Neither lesson spells out the paths; both refer to them by description:
  - `corpus/lessons/round-44.md:22-23`: "3 modified JSON files are left-named with `not hunk-verified`."
  - `corpus/lessons/round-46.md:240`: "| inherited tree | unchanged: the three modified JSONs stay left-named; the round-43/44 L0 questions are still unanswered (`ScoutInheritedTree`) |"
- The paths themselves are named in `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md:144` (chousa round-43): "modified `.ufo/waves/round-40/w1/swarm-registry.json`, `.ufo/waves/round-41/w1/swarm-registry.json`, `corpus/evidence/round41/receipts/cells/cells.json`". That is an exact match for today's three ` M` lines.
- The bytes have not changed since round 46. The `cells.json` hash `1f5c0afae802…` is the same value `.ufo/waves/round-46/w1/ScoutInheritedTree.md:36-37` recorded, which in turn matches the round-45 restore (`round-45.md:70-73`, cited there). The per-file diffstat (70 / 641 / 185) equals round-46's figure "diffstat 70 / 641 / 185" (r46 report, line ~27). Both registry mtimes date from 2026-10-24, before rounds 45–47. The `cells.json` mtime of 06:36:03 is the round-45 restore write that the r46 report ledgers (line 49).
- [INFERENCE] The two registry hashes were not recorded in round 46, so their stability rests on unchanged mtime and diffstat, not on matching hashes. The round-44 status "not hunk-verified" still applies.

## (2) Untracked paths (all created by round 47 wave 1)

| path | bytes | sha256 |
|---|---|---|
| `.ufo/waves/round-47/gen-w1-spec.py` | 38469 (mode 755) | a393de73ef1190da08d06233876b5fa3b210d388e34bea8feade3f04c574a843 |
| `.ufo/waves/round-47/w1-dispatch.json` | 178880 | 8287f257e1244b1152c9383a8fc25bb78a02bbd68b6cd78d99cc25fb1cc86dba |
| `.ufo/waves/round-47/w1-run.err` | 0 (empty) | e3b0c442…b855 (empty-file hash) |
| `.ufo/waves/round-47/w1-spec.json` | 77085 | 38cce07ae0ad34d7ee7af414ad975fc57caa3c92684e2cd48bae2ba41c186536 |
| `.ufo/waves/round-47/w1/` | contained only `swarm-registry.json` (83261 B, mode 600) at snapshot time; seat reports, including this one, land here later | — |

All five are timestamped 2026-10-25 08:42. `.ufo/waves/round-47/assimilation/` is **tracked**: `git ls-files` lists census-start.txt, collisions, reg-ids, staged-ids and guard-proof/*. No untracked path exists outside `.ufo/waves/round-47/`; in particular there are no leftover r40/r41 seat reports and nothing from round 46. Because seats are still writing, treat this list as a snapshot.

## (3) Operator answers in `.ufo/l0-questions.md`: NONE for chousa

```
$ wc -l; sha256sum   -> 160 lines, 792f3239a53cc59fe599ec038900f333c370cc4f120ffa8247ca20fc94a4be54
$ git -C /home/vgpnk/Projects/shokunin cat-file -t 8d77e6c1; git log -1 8d77e6c1
commit
8d77e6c15a6be12a24013b909f2b074ad7cc7e65 Thu Oct 22 22:51:06 2026 -0300 round-29: chousa L0 question (quote re-open fetch scope)
$ git show -U0 8d77e6c1 -- .ufo/l0-questions.md | grep '^+chousa'
+chousa | round-29 | Does the frontier duty to open registered sources (CORPUS.md SOURCES rule 1) cover credential-free GET re-opens of publ…
$ grep -c ANSWERED .ufo/l0-questions.md
1
126:- 2026-10-23T03:52:34Z ANSWERED (operator, 03:53Z): "keep starting rounds". The six-closure second-trip wrap is overridden for this leg.
```

- **8d77e6c1** is the fleet commit that filed the round-29 fetch-scope question (now `l0-questions.md:121`). It has **no answer**. Lines 136 (round 41) and 140 (round 42) still describe it as "still-open". The only ANSWERED line in the file (126) is hyaku's drift-sentinel override and does not address fetch scope.
- **Round-43 questions**: register staleness at :143 and the inherited working-tree debt at :144 (the three JSONs). Both are **unanswered**.
- **Round-44 question**: wave shape and seat accounting at :148, filed in fleet commit `44479ed6`. **Unanswered.**
- Other chousa questions (:30 round-1, :51 round-12, :86 round-27, :95 and :121 round-29, :136 round-41, :140 round-42) also have no answer. The file was last changed by `80d22f76` (2026-10-25 07:20, revenger round-69), and none of the 18 commits since 2026-10-24 adds an answer for chousa.

## Verdict

- The inherited tree is unchanged from round 46. The three modified JSONs are exactly the round-43 left-named set, and `cells.json` is byte-identical to the round-45/46 hash.
- Every untracked path is round-47 wave-1 scaffolding under `.ufo/waves/round-47/`.
- 8d77e6c1 and the chousa round-43/44 questions remain unanswered, so the no-fetch bound stays in force. Confidence: high. The only open gap is that the two registry hashes have no earlier baseline to compare against.

No tools installed. No scratch directory was created. Nothing was written except this report.
