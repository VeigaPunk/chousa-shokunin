# R57W1SimpRound — dead-weight scan of the round's landed bytes (leaf; no dispatch)

Seat: simplifier. I deleted nothing in the lane and wrote nothing but this file. Scratch
`/fast/scratch/hyaku/chousa-r57/R57W1SimpRound/` (112 K) existed only for the pyc behaviour proof and was removed
(`ls -d` → `No such file or directory`). No tool installed. Lane `git status` differs before/after my work only by
launcher/seat churn (`w1.ready.dispatched` appeared, `refetch.tsv` grew, 10 new capture files).

## 1. `*.pyc` / `__pycache__` under `corpus/evidence` + `tools`

```
$ find corpus/evidence tools -path '*__pycache__' -type d -exec du -sb {} \;
39349 round35   13959 round47   22603 round51   56208 round52   88879 round53   84736 round54   45218 round55   27069 round57   198041 tools
$ find corpus/evidence tools -name '*.pyc' | wc -l          → 19 files, 576062 B
$ git ls-files -- 'corpus/evidence/**__pycache__**' 'tools/__pycache__/*'   → count=2, 39349 B
corpus/evidence/round35/__pycache__/{c1,c2}-count.cpython-314.pyc
```

- **Landed dead weight: exactly 2 files, both round-35** (`beb04ea`, 2026-10-25). They violate the lane's *existing*
  rule — `.gitignore:3` `corpus/**/__pycache__/` landed in `7659748` on 2026-10-23, two days earlier, and
  `corpus/lessons/round-36.md:44` states the norm ("pyc removed, `corpus/**/__pycache__/` added to `.gitignore`").
  No document marks them provenance (`grep -rIn 'pyc|__pycache__' corpus/lessons QUALITY.md SCORECARD.md` → only the
  round-36 governance rows).
- **17 files / 536,713 B are ignored residue**, not landed — including this round's only residue:
  `corpus/evidence/round57/__pycache__/c3-count.cpython-314.pyc`, 27,069 B, mtime `2026-10-27 05:41:44`, i.e. a seat
  ran a counter without the spec's `PYTHONDONTWRITEBYTECODE=1`.
- **Removal is behaviour-neutral (proof, scratch copy of `corpus/evidence/round35`):** ran `c1-count.py --gate
  <lane>/tools/research-gate.sh` with the `__pycache__` present, then `rm -rf` it and ran again — both printed 9/9
  PASS, `label GREP_PIN_MATCH=9/9 matched 9 predicate_holds True`, exit 0; normalised receipts differ in 2 lines, both
  the random `"seed"`. Header check explains it: the counter runs as `__main__`, so `__pycache__` is never consulted;
  `c2-count…pyc` is stale anyway (hdr mtime 1792784735 vs src 1792784834, size 9551 vs 9554 ⇒ `=> IGNORED`), and so is
  `tools/__pycache__/capture-fetch…pyc`.

## 2. Scratch tree `/fast/scratch/hyaku/chousa-r57`

`05:40` snapshot: **27 dirs, 5.1 G**; `05:47` re-snapshot: **42 dirs, 7.2 G** (`/fast` 602 G free). Every seat-named
dir resolves to one of the 65 seats in `w1-spec.json`; **`NOT A SEAT: ['dryrun','fetch']`** at both snapshots
(set-diff in python3). No stale round-56 leftovers.

| dir | size | owner reading |
|---|---|---|
| `R57W1ExecDoNothing` 3,704 M · `ExecC2Recompute` 911 M · `SentScope` 607 M · `LabSpacing`,`CritC3Held` 401 M | — | live seats |
| `dryrun` | 582 M | **round-level, pre-dispatch** (`lane-copy/`,`lane-archive/` 05:12 vs dispatch 05:26) |
| `fetch` | 32 K | **round-level L1 staging**: `pinned-pairs.tsv`, empty `recipe/`, `refetch.append` 26,976 B @05:40 |

12 seat dirs were empty when scanned (`ScoutR2`, `ScoutR4b`, `ScoutR5b`, `Conn*`, `Distill`, `ExecRefetchTiming`,
`LabRecipe`, `ReviewFrontier/Frozen/QuarMethod`, `SonicState`) — seats needing no scratch, not dead dirs.

## 3. Capture store `corpus/captures`

```
$ ls corpus/captures | wc -l → 107 files (55 stems), 56 M ; no file that is neither .raw nor .txt
stems with no refetch row (beyond the 3 orphans): []        # python3 set-diff
raw-only stems: 53a92273…, d473754a…, d8b4f8f8…             # the three orphans, all %PDF- 1.20/1.49/1.29 MB
pinned set @ 6656f07: 47 triples / 47 ids / 47 digests — each has a refetch row and bytes
refetch: 118 rows, key = sha256(url)[:24] mismatches 0
keys with no bytes: 12 — "successful-rows-without-bytes: none (all attempts failed)" for every one
```

- **Zero unreferenced store bytes**: all 55 stems are named by `refetch.tsv`, the 47-pin set, or the three orphans.
- The 12 bytes-less keys are honest failure/pending records (412/404/503/`curl_rc=1`), not discarded successes.
- One duplicate byte pair — `6fe041ac…` and `a42feae4…` share sha256 `d01795dd60264371…`. Not removable: keys are `sha256(url)[:24]` by the frozen predicate, so two URLs to one document keep two keys.

## 4. `.ufo/waves/round-57/` vs the dispatch (spec | dispatch | ready | reports)

24 files. Reports: **17 in `w1/`, every name in the 65-seat spec, zero foreign or duplicate**. Non-report files:

| file | size | verdict |
|---|---|---|
| `w1-spec.json` / `w1-dispatch.json` / `w1.ready` | 91 K / 228 K / 156 B | spec+dispatch+ready — in scope |
| `gen-w1-spec.py` | 51,837 B | generator of the 65-item spec; round-56 keeps the same file ⇒ **KEEP** |
| `w1/swarm-registry.json` | 107,926 B | referenced twice in `w1-dispatch.json` ⇒ **KEEP** |
| `w1.ready.dispatched` | 2,633 B | launcher's timestamped seat→seat map; round-56 tracks the same name ⇒ **KEEP** |
| `w1.ready.partial` | tracked, **absent on disk** | **REMOVE (already deleted)** — hazard (§6b) |
| `w1-run.err` | **0 B**, tracked | **REMOVE** — empty, read by nothing (`grep -n 'run.err' gen-w1-spec.py w1.ready` → no hit); also 0 B in round 56, so inertia, not evidence |

## 5. One line per item (L1 decides; I deleted nothing)

1. `round35/__pycache__/{c1,c2}-count…pyc` — **REMOVE** (39,349 B; derived, rule-violating, behaviour-neutral per §1).
2. `{round47,51,52,53,54,55,57}/__pycache__`, `tools/__pycache__` — **KEEP** (536,713 B ignored residue; `.gitignore` is the existing authority; deleting mid-wave races live counters for no landed-byte gain).
3. `round57/__pycache__/c3-count…pyc` — **KEEP, flag** (seat skipped `PYTHONDONTWRITEBYTECODE=1` at 05:41:44).
4. All 55 capture stems / 107 files — **KEEP** (0 unreferenced; 3 orphans carry RevOrphans/C3 work in flight).
5. `6fe041ac…` + `a42feae4…` — **KEEP** (two URL keys, one document, frozen key rule).
6. 25 seat scratch dirs — **KEEP** (live seats; each removes its own). `dryrun` 582 M + `fetch` 32 K — **REMOVE at close by their owner** (round-level; `refetch.append` is live).
7. `w1.ready.partial` — **REMOVE/untrack** (superseded by `w1.ready.dispatched`). `w1-run.err` — **REMOVE** (0 B).
8. `gen-w1-spec.py`, `w1/swarm-registry.json`, `w1.ready.dispatched` — **KEEP** (each load-bearing).

## 6. Two live hazards (reported, not patched)

**(a) A frozen historical manifest is rewritten in the working tree.** `corpus/evidence/round45/spans.tsv` shows
`2 insertions, 2 deletions`, replacing **S083's pin** (one of the 5 DRIFTED ids) with today's drift digest:

```
-S083 … arxiv.org/html/2305.13117v3  a3ff65e0db9cc4f2178932ce53965e4cba60c6aab0ba3b1d4ce40020a8a7cf8f  14415 120724
+S083 … arxiv.org/html/2305.13117v3  d37b64ed18a860f8e7795b8dcc1b808e788f0643e4936f9dbcaf6e61bbf3b101  14332 120641
```

`sha256(corpus/captures/412b146a2720ce6557268d05.txt) = d37b64ed18a860f8…`, so the substituted digest *is* today's
drifted text. The new offsets locate neither quote in it (`find` → char 14493 / bytes 14671 and 121576; 14332 and
120641 land on unrelated words), so the rewrite is anchored to neither the old pin nor the new bytes.
`c2-count.py` reads manifests via `git show 6656f07:…`, so today's `C2=PASS` is unaffected — but committing this
rewrites an immutable round-45 record and erases exactly the S083 drift the claim measures. **Recommendation: restore
the file (`git checkout -- corpus/evidence/round45/spans.tsv`) or move the experiment into scratch, before receipt.**

**(b) `w1.ready.partial` is tracked and deleted on disk** (`git status` → ` D`), while `w1.ready.dispatched` is
untracked — two names for one seat→seat map. Round-56 tracks `w1.ready.dispatched` only. **Recommendation: commit the
deletion / untrack `ready.partial`; keep `ready.dispatched`.**

## 7. Freshness datum observed (not a claim verification)

```
$ python3 corpus/evidence/round57/c2-count.py
SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS
```

47/47 at 05:43 (dispatch state 43/47); no `MISSING`, no `FLAGGED` — consistent with §3's "no dead bytes".

**Tradeoff:** I left the 17 ignored pyc files and all scratch trees alone (removing them changes no landed byte, and
mid-wave `tools/__pycache__` deletion races seats importing those tools); the round-35 pyc are the only removable bytes whose removal changes nothing observable (§1 proof).

VERDICT: attacked the round's landed bytes for dead weight — survived with 5 removal candidates (2 tracked pyc, 0-byte `w1-run.err`, `w1.ready.partial`, round-level `dryrun`/`fetch` at close) and zero unreferenced captures, plus one live dirty-state hazard (`round45/spans.tsv` S083 pin substituted with the drift digest) reported for the L1 to revert, not patched by me.
