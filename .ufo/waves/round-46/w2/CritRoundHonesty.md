# CritRoundHonesty — round-46 record audit (overclaim)

seat: `L1Chousa46.CritRoundHonesty` (leaf). Audit target `d09fc8e7` (dispatch) plus the commits that carry the round's verdict: `3807537d` (first verdict) and `e50b388a` (tip at read time). Claims frozen `c2f0e9d1`. No lane byte written: counters run read-only (`PYTHONDONTWRITEBYTECODE=1`); every mutation on a `git archive`/`cp -r` copy under `/tmp/chousa-r46w2-CritRoundHonesty` (deleted).

## 0. The dispatch premise fails at `d09fc8e`

- `git show --name-only --format= d09fc8e | grep -E "SCORECARD|LOG.md|lessons"` → no output; `git show d09fc8e:corpus/lessons/round-46.md` → `fatal: path ... does not exist`; `git show d09fc8e:SCORECARD.md | grep -n "## Round 46"` → no output (still `## Planned — round 46 (not started)`, SCORECARD.md:2439). At the dispatch target there are **no per-axis verdicts at all**.
- HEAD was detached at `d09fc8e`, `master` = `3807537d`, and moved to `e50b388a` during the audit.
- The worktree was rewritten mid-wave (mtime 07:42:11–07:43:32 on `c1/c2/c3-count.py` and the tool); the then-worktree `c1-count.py` printed an uncommitted `CANARY=pass`, `c3-count.py` printed uncommitted `SPAN_IDS/SPAN_CONTEXT` legs, both later committed as `e50b388a`. The measured surface was non-stationary; attribution (L1 integration vs a seat) is not observable in the repo.

## 1. Re-runs — the three counter verdicts ARE supported

`git archive d09fc8e` → /tmp copy:

```
$ python3 corpus/evidence/round46/c1-count.py
TOOL=present / POSITIVE_PASS=3/3 / JUNK_KILLED=3/3 / C1=PASS                     exit=0
$ python3 corpus/evidence/round46/c2-count.py --list
ENTRY_POINTS=72 (tools=8 counters=50 named=70) / GATES_ROWS=35
REGISTERED=72/72 / UNREGISTERED=0 / C2=PASS                                     exit=0
$ python3 corpus/evidence/round46/c3-count.py
ENTRIES=2/2 CITES_BOUND=5/5 QUOTE_ROWS=11/11 QUOTES_IN_SPAN=11/11
QUOTES_IN_ENTRY=11/11 CAPTURE_BOUND=11/11 REF_ID_UNBOUND=0 REF_BOUND=2/2 C3=PASS exit=0
--lane-only → same, CAPTURE_BOUND=skipped, exit=0
build-spans.py --check → SPANS_ROWS=11 STALE=0                                  exit=0
```

Independent span re-derivation (not via the counter): 11/11 `slice_exact=True`, `span_chars − quote_chars = 160` on every row (±80 both sides), capture sha256 matches, `text.find(quote)` equals the recorded offsets (2360 1271 15269 42011 20847 171 4929 3929 2904 3022 7137). Freeze before-states reproduce: C1 `TOOL=absent 0/3 0/3 exit 1`; C3 `ENTRIES=0/2 … CAPTURE_BOUND=0/11 C3=FAIL`. At `e50b388a`: C1 `CANARY=pass`, C2 `73/73`, C3 all full. **The overclaim is in the records, not in the counter outputs.**

## 2. Sentences that would not survive a hostile closure review

1. **`SCORECARD.md:2460` "freeze tree `ENTRY_POINTS=71 (… named=66)`" — false.** The freeze commit `c2f0e9d` (claims.md present) prints `ENTRY_POINTS=71 (tools=7 counters=50 named=69)`. `named=66` is a base+counters tree *without* `claims.md` (reproduced as such).
2. **`SCORECARD.md:2460` "(`ReviewerC2Set`, and `controls/c2-before.txt` tree C)" — no such block.** `grep -c "tree C" controls/c2-before.txt` → `0`. The 68/13 number is real (rerun on `6e2630a6`: `ENTRY_POINTS=68 (7/47/66) REGISTERED=55/68 UNREGISTERED=13`) but is cited to a receipt without it.
3. **`controls/c2-before.txt` labels contradict their numbers.** "tree A: … (the frozen-before tree)" prints `named=66` (the no-claims tree); "tree B: the bare base tree … (no round-46 counters)" prints `counters=50 named=69` (it has the counters and is the freeze tree). The true bare base is absent. Lesson mistake 10 says the fix gave "three labelled trees (A: freeze tree, B: base + the whole round-46 dir, C: bare base)" — **two blocks, both mislabelled, no C**.
4. **The recorded after-number is not what its command prints.** `SCORECARD.md:2460` "→ 72 … `REGISTERED=72/72`", `LOG.md:1715`, lesson `## Claims` "after `REGISTERED=72/72`" — at `3807537d` and `e50b388a` the cited command prints `ENTRY_POINTS=73 (8/50/71) REGISTERED=73/73`. The 73rd is `corpus/evidence/round46/build-spans.py`, absent from the `d09fc8e` set and admitted only because `SCORECARD.md:2480` names it: the verdict's prose enlarges the set it measures.
5. **`SCORECARD.md:2468` "cheap gates (fence, comment, suffix) closed" / `LOG.md:1719` "HTML-comment row" refused — half closed.** Comments are stripped line-by-line (`re.sub(r"<!--.*?-->", "", line)`), so a **multi-line** block `<!--` / `| c2 | instrument | <all 16 unregistered paths> | exit 1 | a | b | c | d |` / `-->` scores `GATES_ROWS=31 REGISTERED=71/71 UNREGISTERED=0 C2=PASS` **exit=0**; the single-line variant is refused (`C2=FAIL`). A block comment is the ordinary way to comment out a row.
6. **One row satisfies the registry, and the round's own control proves it silently.** A single 9-pipe row naming all 16 unregistered paths in one cell → `REGISTERED=71/71 C2=PASS exit=0`. `controls/c2-controls.txt`, committed at `d09fc8e`, records `--skill <SKILL-7pipe.md>` → `REGISTERED=71/71 UNREGISTERED=0 C2=PASS exit=0` among six refusals, with no caption; neither `claims.md` (four controls) nor `SCORECARD.md:2460` (six) lists it. The tip lesson now names row format as a limit, but `SCORECARD.md:2468`/`:2479` still read as closures.
7. **`measure-after.txt` is stale against the tip's own blobs.** At `e50b388a` it still pins `c1 819287e2075c3f5b` and `tool 3018b1d25d762054`; committed blobs are `c1 8473abf6c4437bed` and `tool 7736688bdefe9df0`. Tip `c1-count.py` prints `CANARY=pass`, absent from the record.
8. **Lesson (tip) "The same holds for `build-spans.py` …" — false.** `build-spans.py` **is** an entry point at the tip; removing its Gates-row path from a tip copy gives `UNREGISTERED_PATH corpus/evidence/round46/build-spans.py / UNREGISTERED=1 / C2=FAIL exit=1`. The premise holds for `round45/tag-count.py` (verified not an entry point) but not for `build-spans.py`.
9. **Tree identities precede the commits they name.** `d09fc8e`'s record: "landing tree on lane branch master; measured 07:32:33" vs that commit's committer time 07:32:44. Revised record: "… the wave-2 corrections; measured 07:37:21" vs `3807537`'s committer time 07:37:22, and **no sha names the measured tree**. Both after-states were measured on a working tree; round 45 bound its receipt to `git archive 2738202b`.
10. **`measure-after.txt` census block is not verbatim.** It shows one W04 line (S075); the command emits **five** (S051, S053, S073, S074, S075), exit 0, and SOURCES.md holds 89 rows — which `lessons/round-46.md` §Census correctly says ("the same five W04").
11. **Every "Controls:" sentence cites an unrecoverable input.** `c1-controls.txt` / `c2-controls.txt` replaced the frozen commands with placeholders (`$ ... --tool <always-exit-0 forge>`, `$ ... --skill <SKILL-7pipe.md>`), and `corpus/evidence/round46/controls/` holds only `.txt` transcripts — no forge bytes. Round 45 committed forge inputs (`corpus/evidence/round45/controls/c3-control-forged-span.txt`).

## 3. Per-axis verdicts

| axis | recorded | support |
|---|---|---|
| operability (score 3, `SCORECARD.md:7`) | improved; "3 → 3" | **supported.** Uncited bullet inside the section's fence → `bullets=2 / FINDING INF_UNCITED / exit=1`; one appended fixture byte → `FIXTURES_CHANGED=positive-a.md / C1=FAIL`; exit-2 stub → `JUNK_KILLED=0/3 / exit=1`. Caveat: no fixture covers the fence class, so the fix cannot be regress-detected. |
| calibration | improved | **predicate supported; evidence partly false.** `UNREGISTERED=0` holds everywhere; items 1–6 do not survive. Axis verdict stands on the counter alone. |
| depth | improved | **supported.** Both modes pass; 11/11 spans independently re-derived with ±80 context and matching digests; the `status == mined`/`used-by` leg (`c3-count.py:100`) fails closed — S085 `mined`→`held` gives `CITES_BOUND=4/5 C3=FAIL exit=1`; before-state reproduces. |
| coverage | improved narrowly | **supported.** `git diff 6e2630a d09fc8e -- corpus/README.md` → two added `…-r39*.md` rows; `ConnectSiblings` §2 "C3 absorbs no sibling's held ground". |
| freshness | unchanged | **supported**, nit: all five captures are mtime `2026-10-23 20:36–20:40` (before the 07:10:05 launch), but "written 2026-10-23/24" implies a 10-24 capture — none. S085 cadence accurate: staged `SOURCES.append.md:45` row says `180d`, lane row `365d`. |
| adjacency | unchanged | **supported.** `ConnectSiblings` §3 names six lanes (lore, kaidoku, tameshi, kagi, kumitate, revenger). |

## 4. Smallest safe corrections (no predicate, target or kill rule touched)

1. `SCORECARD.md:2460`: `named=66`→`69`; drop or commit the "tree C" citation; `72`→`73`, `REGISTERED=72/72`→`73/73`, `named=70`→`71` in SCORECARD, `LOG.md:1715`, lesson `## Claims`.
2. `controls/c2-before.txt`: relabel to A = base+counter files without `claims.md` (71, 7/50/66), B = freeze `c2f0e9d` (71, 7/50/69), add C = bare `6e2630a` (68, 7/47/66) — then mistake 10 is true.
3. `c2-count.py`: strip comments with a state machine (the round-20 lane already does this for `load_sections`, `SCORECARD.md:1022-1031`) and add a block-comment forge; until then change `SCORECARD.md:2468`/`:2479` and `LOG.md:1719` to "single-line comment refused; block comment survives (recorded)".
4. Caption the `SKILL-7pipe` block as a **survivor** ("one row naming every path registers all — row truth unmeasured"), matching the tip lesson; commit forge inputs (or a generator) beside the transcripts.
5. `measure-after.txt`: name the measured commit sha, re-emit at `e50b388a` (revision line + `CANARY=pass`), and restore all five W04 lines or mark the block "excerpt".
6. Lesson (tip): remove `build-spans.py` from the non-entry-point list, or state the circularity — the SCORECARD capability table is what makes it an entry point.

## 5. Verdict

C1, C2 and C3 reproduce at `d09fc8e` and at the tip; every frozen predicate is met and no per-axis verdict is contradicted by a counter. The overclaim is in the record layer: a mislabelled before-receipt cited to a missing block (1–3), an after-number its own command no longer prints (4), a comment forge closed only for single-line comments (5), a passing forge transcribed among refusals (6), a revision pin stale at its own commit (7), a lesson limit falsified by its own instrument (8), tree identities that precede the commits they name (9), and a census transcript four lines short (10). Items 1–4, 7–10 are mechanical; 5–6 need a code change or a downgraded sentence. No claim needs re-scoring.
