# W2CritSweep — committing the three modified JSON files without a hunk review fails C2

Seat: critic. Axes: operability, calibration, depth.
Milestone: Round 44 wave 2.
Measured at HEAD `043f19a1db91288947493d9f879e61e7a9f07241`. Counter and claims were clean (`git status --porcelain` on those two paths printed nothing). No commit was made. No production file was edited. Probe tables were written only under `/tmp/w2critsweep/`.

## Axes

- operability: name the check that rejects the commit, and show it fail on a table that records the commit.
- calibration: do not treat a whole-file sha256 match as a hunk review, and do not claim the counter itself runs `git`.
- depth: the dirty diffs are content changes, not mode bits. A blind commit would land them.

## The three paths

From `MODIFIED` in `corpus/evidence/round44/c2-count.py` (lines 59–63), not from porcelain:

1. `.ufo/waves/round-40/w1/swarm-registry.json`
2. `.ufo/waves/round-41/w1/swarm-registry.json`
3. `corpus/evidence/round41/receipts/cells/cells.json`

Tuple length 3. The other 36 paths in that file are `UNTRACKED` markdown reports. These three are not in that tuple.

## Why the commit fails C2

Predicate R44-C2 (`corpus/evidence/round44/claims.md`) allows only two classes. The 36 untracked reports may be `reverified-commit` when the file contains its stem, contains a round token for its directory, is longer than 80 characters, and the row digest equals the file sha256. Each of the three modified paths must be `left-named`, and its reason must contain `not hunk-verified`. No other class is allowed.

The kill rule in the same file:

> a missing path, a reverified row whose stem, round token, or sha256 does not match, or a modified path marked `reverified-commit`, is a miss. Committing a path without that match is a blind sweep and fails.

The counter implements that split. Untracked rows are content-checked. Modified rows are not. Digest, stem, and round token are ignored for `MODIFIED`:

```
ok = cls == 'left-named' and 'not hunk-verified' in reason and reason.strip()
```

(`c2-count.py` lines 108–112). `C2=PASS` requires `LEFT_NAMED=3/3` as well as `REVERIFIED=36/36` (line 117). The file never calls `git`, never reads a diff, and never searches for the word `hunk` except in that reason substring (grep of the counter: the only `hunk` hit is the docstring and line 110).

Committing the three JSON files and recording that commit as verification is therefore a miss even when the bytes would satisfy the untracked checks. Each dirty file already contains its stem, already contains its round token (`40` or `41`), and is longer than 80 characters. A row that copies the working-tree sha256 matches. That match is not a hunk review. The class is still wrong, so `LEFT_NAMED` stays 0 and C2 fails.

## Measured rejection

Default counter, no `disposition.tsv` on disk (`ls` → `No such file or directory`):

```
CONSISTENT=0/39
REVERIFIED=0/36
LEFT_NAMED=0/3
C2=FAIL table-missing
EXIT:1
```

That is the missing-table miss, not the commit miss. The commit miss is the next three probes. Each probe gave the 36 untracked reports `reverified-commit` plus their real sha256, so `REVERIFIED` could reach 36/36. Only the three JSON rows changed.

Blind commit: class `reverified-commit`, digest = working-tree sha256, reason `committed without hunk review`.

```
CONSISTENT=36/39
REVERIFIED=36/36
LEFT_NAMED=0/3
C2=FAIL
exit=1
```

Same digests, class still `reverified-commit`, reason kept the required phrase (`not hunk-verified but class reverified-commit`):

```
CONSISTENT=36/39
REVERIFIED=36/36
LEFT_NAMED=0/3
C2=FAIL
exit=1
```

Class `left-named`, phrase omitted (`committed after reading the file, hunks not reviewed`):

```
CONSISTENT=36/39
REVERIFIED=36/36
LEFT_NAMED=0/3
C2=FAIL
exit=1
```

Control that does not record a commit: same 36 reverified rows, three rows `left-named` with reason `not hunk-verified; diff left uncommitted`:

```
CONSISTENT=39/39
REVERIFIED=36/36
LEFT_NAMED=3/3
C2=PASS
exit=0
```

So the three paths are not an obstacle to C2. Recording a commit of them as `reverified-commit`, or dropping `not hunk-verified`, is the obstacle. The naming-only gate is a different miss: `controls/all-left.tsv` scores `LEFT_NAMED=3/3` and `REVERIFIED=0/36`, `C2=FAIL`, exit 1. That fails because the 36 reports were not content-checked. It does not license committing the JSON files.

## What a hunk review would have had to read

Porcelain, unstaged (cached numstat empty):

```
 M .ufo/waves/round-40/w1/swarm-registry.json
 M .ufo/waves/round-41/w1/swarm-registry.json
 M corpus/evidence/round41/receipts/cells/cells.json
```

`git diff --numstat`:

```
36	34	.ufo/waves/round-40/w1/swarm-registry.json
427	214	.ufo/waves/round-41/w1/swarm-registry.json
149	36	corpus/evidence/round41/receipts/cells/cells.json
```

`git diff --stat`: 3 files changed, 612 insertions, 284 deletions.

HEAD sha256 is not the worktree sha256. A commit would replace the index bytes.

```
.ufo/waves/round-40/w1/swarm-registry.json
  HEAD c799d343c7b61bc7eef83ef26ac589a6066a11c538361a9997908001026c0cdd bytes 18010
  WORK c4e00d1141a0faaf0dfd655b9173ef974b702d668efd9751caab78658e3fb0d0 bytes 18572
.ufo/waves/round-41/w1/swarm-registry.json
  HEAD 9e0e9d171b3207e550a01d4ac9760f67aa3aa40bd990557ebb8735f55dba3680 bytes 7745
  WORK 49b059533008951e54dc2e4c03ecf0b5352e1ec30eaf7af512e516be07bc4b59 bytes 23757
corpus/evidence/round41/receipts/cells/cells.json
  HEAD 226b8907a3db0722c1f8a2283f41d4783ff0a8a31fe2c86bece80d35aec27b3e bytes 2291
  WORK 1f5c0afae8024c50013e9a9060988c14506115125e3823042e4512833f293b80 bytes 8122
```

The r40 hunk is not whitespace. It replaces `"path"` with `"wave"` / `"createdAt"` / `"updatedAt"`, and it replaces `"agentId": null` with the seat name. `git diff -U0` counts 33 removed `"agentId": null` lines and 33 added `"agentId"` lines. First hunk, abbreviated:

```
-  "path": ".ufo/waves/round-40/w1/swarm-registry.json",
+  "wave": "chousa-r40-w1",
+  "createdAt": "2026-10-24T07:16:35.766Z",
+  "updatedAt": "2026-10-24T07:18:06.849Z",
...
-      "agentId": null,
+      "agentId": "ExecC1BaseReceipt",
```

The r41 registry is one large rewrite (HEAD 7745 bytes, worktree 23757). `git diff -U0` shows 35 removed `"agentId": null` lines. The added-line pattern used for r40 did not match r41, so this report does not claim a 35-for-35 agentId rename there. The byte growth alone is an unreviewed content change.

`cells.json` is the round-41 receipt artifact. The committed receipt and the dirty file disagree on the gate, on `k`, and on a predicate. First hunks:

```
- "gate": "/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh",
- "k": 12,
+ "gate": "/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-41/controls/base-gate-r41.sh",
+ "k": 1,
...
    "cell": "S2-trap-inventory",
-   "predicate_holds": true,
+   "predicate_holds": false,
...
-    "count": 0,
+    "count": 1454,
```

A whole-file sha256 of that dirty file would bless the gate swap and the predicate flip. That is the blind sweep. Round 42's spot-check already named these leftovers and said they were left, not swept (`corpus/lessons/round-42-verifier-spotcheck.md`, routed defect 3). Round 44 froze that refusal: the three modified JSON files are required `left-named` with `not hunk-verified` (`LOG.md` round-44 freeze).

## Calibration limit

The counter does not see a commit. It sees the disposition class. I did not run `git commit`, so this report does not claim an index change. What was run is the frozen counter against tables that record the commit the way C2 would have to score it. Those tables fail. A later table that still says `left-named` / `not hunk-verified` after someone had committed would still pass line 110, because the counter never reads `git status`. That lie is not a hunk review, and the claims kill rule still calls the commit a miss. The counter will not catch it unless the row class or the reason phrase changes. Do not retune the predicate to close that gap inside this seat.

Counter sha256, unchanged before and after the probes:

```
343ba2366e8b448062dfd262d23d8f3d4801bbea5936dbc7f4d8d7e19b8b26ad  corpus/evidence/round44/c2-count.py
```

No network. No tool installed. No lane production file modified.

Report: .ufo/waves/round-44/w2/W2CritSweep.md
