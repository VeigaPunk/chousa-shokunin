# W3CritScope — write scope and adjacency audit (chousa r44 w3, critic)

Axes: operability, calibration, depth.
Milestone: Round 44 wave 3 — falsify the landed round-44 state.
Seat: leaf, no dispatch. Commands used this session, all read-only: `git status --porcelain`,
`git rev-parse --show-toplevel`, `stat`, `ls`, `find`, one `Read` of w3-spec.json.
Writes made by this seat: exactly one file, this report. Scratch: none anywhere (not even /tmp needed).

## 1. Lane audit clock

Quoted command output (this seat's own clock anchors):

```
now: 2026-10-24 22:29:28 -0300
toplevel: /home/vgpnk/Projects/shokunin/chousa-shokunin
2026-10-24 22:28:08.769558107 -0300 | .ufo/waves/round-44/w3-spec.json
2026-10-24 22:28:21.116421161 -0300 | .ufo/waves/round-44/w3-launcher.log
```

This round's w3 wave began when `w3-spec.json` was written: **22:28:08 -0300**. "Modified by
this round" is judged against that instant and against the seat transcript.

## 2. `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin status --porcelain` — every path, classified

Verbatim output (snapshot taken 22:29:28 -0300, i.e. before this report was written):

```
 M .ufo/waves/round-40/w1/swarm-registry.json
 M .ufo/waves/round-41/w1/swarm-registry.json
 M corpus/QUALITY.md
 M corpus/SOURCES.md
 M corpus/evidence/round41/receipts/cells/cells.json
 M tools/parent-lifetime.sh
?? .ufo/waves/round-40/w1/ConnectorSiblingScan.md
?? .ufo/waves/round-40/w1/CriticC1Control.md
?? .ufo/waves/round-40/w1/CriticC1Predicate.md
?? .ufo/waves/round-40/w1/CriticC1Scope.md
?? .ufo/waves/round-40/w1/CriticC2Calibration.md
?? .ufo/waves/round-40/w1/CriticR4Disposition.md
?? .ufo/waves/round-40/w1/CriticSourceClaim.md
?? .ufo/waves/round-40/w1/ExecC1BaseReceipt.md
?? .ufo/waves/round-40/w1/ExecC1Count.md
?? .ufo/waves/round-40/w1/ExecC1LandedReceipt.md
?? .ufo/waves/round-40/w1/ExecC1MutantReceipt.md
?? .ufo/waves/round-40/w1/ExecC2Count.md
?? .ufo/waves/round-40/w1/ExecNoHarm.md
?? .ufo/waves/round-40/w1/MutateExpectDigest.md
?? .ufo/waves/round-40/w1/MutateGateDigest.md
?? .ufo/waves/round-40/w1/MutateVerifierSubject.md
?? .ufo/waves/round-40/w1/RevengerR1History.md
?? .ufo/waves/round-40/w1/RevengerR2R5History.md
?? .ufo/waves/round-40/w1/ReviewActivePopulation.md
?? .ufo/waves/round-40/w1/ReviewC2Bindings.md
?? .ufo/waves/round-40/w1/ReviewR2CommitTruth.md
?? .ufo/waves/round-40/w1/ReviewR3Counts.md
?? .ufo/waves/round-40/w1/ReviewR4RoleMix.md
?? .ufo/waves/round-40/w1/ReviewReplacementBindings.md
?? .ufo/waves/round-40/w1/ScoutFrontierOverlap.md
?? .ufo/waves/round-40/w1/ScoutHashSource.md
?? .ufo/waves/round-40/w1/ScoutProvinceBoundary.md
?? .ufo/waves/round-40/w1/ScribeClaimSurfaces.md
?? .ufo/waves/round-40/w1/ScribeKnowledgeEntry.md
?? .ufo/waves/round-40/w1/ScribeLessonGate.md
?? .ufo/waves/round-40/w1/SentinelFetchScope.md
?? .ufo/waves/round-40/w1/SentinelWriteScope.md
?? .ufo/waves/round-40/w1/SimplifierAudit.md
?? .ufo/waves/round-41/w1/ConnectorSiblingScan.md
?? .ufo/waves/round-41/w1/ExecC2Before.md
?? .ufo/waves/round-41/w1/MutateC2Join.md
?? .ufo/waves/round-44/assimilation/
?? .ufo/waves/round-44/launcher-outer.log
?? .ufo/waves/round-44/make-w3-spec.py
?? .ufo/waves/round-44/seat-logs/
?? .ufo/waves/round-44/slot-grant.txt
?? .ufo/waves/round-44/w2-dispatch.json
?? .ufo/waves/round-44/w2-launcher-outer.log
?? .ufo/waves/round-44/w2-parent-lifetime.receipt
?? .ufo/waves/round-44/w2-plan.json
?? .ufo/waves/round-44/w2-slot-grant.txt
?? .ufo/waves/round-44/w2-spec.json
?? .ufo/waves/round-44/w2/
?? .ufo/waves/round-44/w3-dispatch.json
?? .ufo/waves/round-44/w3-launcher-outer.log
?? .ufo/waves/round-44/w3-launcher.log
?? .ufo/waves/round-44/w3-plan.json
?? .ufo/waves/round-44/w3-spec.json
?? .ufo/waves/round-44/w3/
?? corpus/evidence/round44/controls/errata-two.txt
?? corpus/evidence/round44/controls/errata-zero.txt
?? corpus/evidence/round44/disposition.tsv
?? corpus/evidence/round44/errata-count.py
?? corpus/evidence/round44/parent-lifetime.receipt
?? corpus/evidence/round44/receipts/census-end.txt
?? corpus/evidence/round44/seat-logs/
?? corpus/knowledge/citation-version-binding-r36.md
?? corpus/knowledge/citation-version-binding-r37.md
?? corpus/lessons/round-44.md
```

Classification — 70 entries total: 6 tracked-modified (` M`), 64 untracked (`??`), of which
5 are git-collapsed untracked directories (`assimilation/`, round-44 `seat-logs/`, `w2/`, `w3/`,
`corpus/evidence/round44/seat-logs/`).

| Group (paths as listed above) | Count | Inside / outside lane tree |
|---|---|---|
| ` M` tracked-modified: round-40/w1 and round-41/w1 `swarm-registry.json`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/evidence/round41/receipts/cells/cells.json`, `tools/parent-lifetime.sh` | 6 | **INSIDE** |
| `??` `.ufo/waves/round-40/w1/*.md` (33 seat reports) | 33 | **INSIDE** |
| `??` `.ufo/waves/round-41/w1/*.md` (3 seat reports) | 3 | **INSIDE** |
| `??` `.ufo/waves/round-44/*` incl. collapsed dirs `assimilation/`, `seat-logs/`, `w2/`, `w3/` | 18 | **INSIDE** |
| `??` `corpus/evidence/round44/*` incl. collapsed `seat-logs/` | 7 | **INSIDE** |
| `??` `corpus/knowledge/citation-version-binding-r36.md`, `...-r37.md` | 2 | **INSIDE** |
| `??` `corpus/lessons/round-44.md` | 1 | **INSIDE** |

**Paths outside the lane tree: none (0/70).** Basis, quoted from the run:
`toplevel: /home/vgpnk/Projects/shokunin/chousa-shokunin`. Every porcelain path is repo-relative
to that toplevel; no path contains `..`; no status path is or traverses a symlink (symlink scan
in §4). Nothing in the working tree points the status surface outside `/home/vgpnk/Projects/
shokunin/chousa-shokunin`.

Falsification notes on the dirty set (mtimes quoted from `stat`):

```
2026-10-24 04:18:06.847655142 -0300 | .ufo/waves/round-40/w1/swarm-registry.json
2026-10-24 04:42:46.930808667 -0300 | .ufo/waves/round-41/w1/swarm-registry.json
2026-10-24 04:46:02.530856414 -0300 | corpus/evidence/round41/receipts/cells/cells.json
2026-10-24 21:49:24.365738999 -0300 | tools/parent-lifetime.sh
2026-10-24 21:54:49.477737224 -0300 | corpus/QUALITY.md
2026-10-24 21:58:34.770832888 -0300 | corpus/SOURCES.md
```

- Three ` M` files date 04:18–04:46 — stale dirt from rounds 40/41, untouched by round 44.
- Three ` M` files date 21:49–21:58 — round-44 wave-1/wave-2 landing window (tools + corpus
  edits), all before w3 spec (22:28:08). Wave-3 crit scope added none of them; this seat added
  none of them.
- The `??` round-40 and round-41 seat reports are uncommitted prior-round work still sitting in
  the tree — an uncommitted-backlog finding for the operator, not a wave-3 violation.
- `corpus/QUALITY.md` and `corpus/SOURCES.md` are lane production files, modified by earlier
  waves (before freeze, per mtimes), correctly unmodified by wave 3.

## 3. Nothing under /home/vgpnk/Projects/shokuknow was modified by this round

### 3a. Requested paste #1 — `.qcache` mtime

`.qcache` is a directory; quoted `stat` output:

```
directory | 2026-10-24 22:24:19.009414133 -0300 | /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache
```

That is **3 m 49 s before** the w3 spec existed (22:28:08) and **4 m 02 s before** the launcher
log (22:28:21). Its newest inner entry is `9b85983279c78f6d9c9907cb.txt` at
`2026-10-24 22:24:19.0099909480`, consistent with the directory mtime. Verdict: `.qcache` was
not touched by this round.

### 3b. Requested paste #2 — merge/chousa package files

All 63 files under `/home/vgpnk/Projects/shokuknow/merge/chousa` carry mtime
`2026-10-24 21:17:10` (one atomic package copy, ~71 min before w3 start). The package-level
files and the three r44 knowledge entries this round's siblings read:

```
2026-10-24 21:17:10.4062839810 | 144266 B | merge/chousa/SOURCES.append.md
2026-10-24 21:17:10.4075093410 |  14222 B | merge/chousa/MERGE-REPORT.md
2026-10-24 21:17:10.4076176710 |  25726 B | merge/chousa/MERGE-REPORT.json
2026-10-24 21:17:10.4071740410 |   2656 B | merge/chousa/knowledge/corpus/knowledge/chinese-journal-issue-toc-r44.md
2026-10-24 21:17:10.4071885410 |   3145 B | merge/chousa/knowledge/corpus/knowledge/repeal-decision-series-r44.md
2026-10-24 21:17:10.4072046310 |   3459 B | merge/chousa/knowledge/corpus/knowledge/grey-literature-national-route-r44.md
```

Verdict: the merge/chousa package was not modified by this round.

### 3c. Full-window sweep and attribution boundary

`find /home/vgpnk/Projects/shokuknow -type f -newermt '2026-10-24 00:00:00'` shows today's
writes; the tail of that listing, 22:24:11 → 22:29:24, includes:

```
2026-10-24 22:24:19 | .ufo/waves/corpus-expansion-1/.qcache/9b85983279c78f6d9c9907cb.txt
2026-10-24 22:24:39 | lanes/kotodama/round16/.deepresearch/.../final_turn_001.md
2026-10-24 22:24:52 | .ufo/scopes/corpus-expansion-16/ScoutKotodama.md
2026-10-24 22:25:04 | lanes/kotodama/round16/KNOWLEDGE-PROPOSED.md
2026-10-24 22:25:06 | lanes/kotoba/round16/{KNOWLEDGE,SOURCES}-PROPOSED.md
2026-10-24 22:26:37 | .ufo/scopes/corpus-expansion-16/ScoutKotoba.md
2026-10-24 22:27:28 | .ufo/waves/corpus-expansion-1/round13-tool-findings.md
2026-10-24 22:27:29 | lanes/tameshi/round16/*.md (7 files)
2026-10-24 22:28:07 | lanes/mado/round16/SOURCES-PROPOSED.md
2026-10-24 22:28:47 | lanes/tabi/round8/.work/ratelimit-series.tsv
2026-10-24 22:28:53 | lanes/mado/round16/KNOWLEDGE-PROPOSED.md
2026-10-24 22:29:16 | .ufo/waves/corpus-expansion-1/round13-handles.json
2026-10-24 22:29:24 | lanes/tameshi/round16/evidence/agentprocessbench-ja.html
```

**Calibration — what this proves and what it does not.** This seat executed only read-only
commands (full transcript above in §1–§3) and wrote exactly one file inside the lane tree, so
nothing under shokuknow was modified *by this round's W3CritScope seat*: proven by transcript
plus the fact that every chousa-relevant shokuknow surface (`.qcache`, `merge/chousa/*`)
predates 22:28:08. The concurrent 22:24–22:29 traffic above belongs to the `corpus-expansion-16`
/ `corpus-expansion-1` scopes (other lanes' round-16 dirs), i.e. a different wave writing into
shokuknow by design; whether that traffic is authorized is outside this seat's scope and is
flagged here only as observation, not as a violation finding. No chousa/round-44 path appears
in the shokuknow write traffic.

## 4. Adjacency: symlink escape scan

```
.ufo/waves/round-29/build/MutateCounter/report.md -> ../MutateCounter.md        (relative, stays in tree)
.ufo/waves/round-35/w2/MutGrepShimPath/shims/b/grep -> /bin/false               (absolute, test fixture)
```

Only two symlinks exist under `.ufo/`, `corpus/`, `tools/`. Neither appears in the porcelain
list, neither is a production file, and the second is a round-35 mutation-test fixture pointing
at a system binary. Neither gives status paths or round-44 writes a route outside the lane tree.
No production path is a symlink.

## 5. Verdict

- 70/70 porcelain paths are inside the lane tree; 0 outside. No wave-3 write scope breach by
  this seat; the only wave-3 write is this report.
- Nothing under `/home/vgpnk/Projects/shokuknow` was modified by this round: `.qcache` mtime
  22:24:19 and all merge/chousa mtimes 21:17:10 both predate the wave start 22:28:08, and this
  seat made no writes outside its own report.
- Residual findings for the operator (not wave-3 faults): (a) rounds 40/41 seat reports and
  registries are still uncommitted in the tree; (b) `tools/parent-lifetime.sh`, `corpus/QUALITY.md`,
  `corpus/SOURCES.md` sit modified-uncommitted since the 21:49–21:58 wave-2 window; (c) shokuknow
  carries live concurrent write traffic from the corpus-expansion scopes during this round's window.

Unrun checks have not passed; all claims above rest only on the quoted command outputs.
