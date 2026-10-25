ATTACKS: round-47 self-assessment (SCORECARD `## Round 47 verdict`, `## Capabilities (round-47 addition)`, LOG `## Round 47`, SHONEN.md) vs committed tree 1fc5ed193ad48a482402c862f4e4cc47e46d5b2d — counters re-run, hashes verified, axis verdicts weighed
VERDICT: defect — two recordkeeping errors in SCORECARD (stale C2 after-numbers incl. a phantom 92/92; after-measurement pointer to an uncommitted file), one stale survivor statement (double negation no longer passes), and the operability axis "improved" verdict is a trade once the fresh held-out rates are counted (miss 8/12, false-refusal 2/12); C1/C2/C3 frozen predicates themselves hold.

## 0. Commit hashes (verified)
`git cat-file -t` — all exist as commits: 22a44b8b5c923d25123a96a852c11938559bb9b2, a15610a5, 980fe43f, 7fb9a232, 3d2a0637, 9a9f94db, 1fc5ed1. `8d77e6c1` is NOT a lane commit (it is the fleet L0 question commit; `git -C …/shokunin show 8d77e6c1` = "round-29: chousa L0 question").

## 1. Counters re-run on `git archive 1fc5ed1` (verbatim)
```
c1-count.py: TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=3/3 CANARY=pass
  R46_COUNTER=pass R46_ENTRIES=2/2 C1=PASS exit=0
c2-count.py --list: ENTRY_POINTS=94 (abc=85 dependence=+2 check_named=+7)
  FLOOR=92 GATES_ROWS=51 REGISTERED=94/94 UNREGISTERED=0 DANGLING=0
  MISMATCHES=0 C2=PASS exit=0
freeze counter (git show 22a44b8b:c2-count.py, sha 36b3934e) on tip:
  ENTRY_POINTS=93 (abc=85 dependence=+1 check_named=+7) GATES_ROWS=46
  REGISTERED=93/93 MISMATCHES=0 C2=PASS exit=0
c3-count.py: ENTRIES=2/2 CITES_BOUND=6/6 QUOTE_ROWS=35 SPAN_IDS=6/6
  QUOTES_IN_SPAN=35/35 QUOTES_IN_ENTRY=35/35 SPAN_CONTEXT=35/35
  CAPTURE_BOUND=35/35 REF_ID_UNBOUND=0 ANCHOR_BOUND=6/6
  INFERENCE_GROUNDED=2/2 QUARANTINE_VERDICTS=4/4
  QUARANTINE_ABSENT_ADOPTED=0 C3=PASS exit=0 (--lane-only: CAPTURE_BOUND=skipped)
build-spans.py --check: SPANS_ROWS=35 STALE=0 exit=0
```
Before/control receipts reproduce exactly: `controls/c1-before.txt`, `c1-controls.txt` (base-tool 0/3 junk; always-exit-1 POSITIVE_PASS=0/3; neg-word-refuser 1/3), `c2-before.txt` (freeze 25/21, base 22/18 both counters), `c2-controls.txt`, `c3-before.txt`, `c3-controls.txt` (17 unbound / 0/6; invented digests 0/12).

## 2. False / stale / unverifiable assertions
1. **SCORECARD:2506 C2 after-numbers are stale and one is false.** Row claims after `ENTRY_POINTS=93 REGISTERED=93/93 … C2=PASS` for the named command `c2-count.py --list`. The named counter prints 94/94 at tip (matches the lane's own `measure-after.txt` 94/94). 93/93 is the *freeze* counter's output. The row also claims "the freeze counter `92/92 MISMATCHES=0` too" — 92 appears nowhere: freeze counter at tip prints 93/93 (FLOOR=92 is the freeze-tree count, not an after-state). Predicate (MISMATCHES=0, ENTRY_POINTS≥FLOOR) holds, so C2 passes; the printed numbers are recordkeeping errors.
2. **SCORECARD:2500/LOG:1752 after-measurement pointer is unverifiable from the committed tree.** Both cite `corpus/evidence/round47/measure-after.txt`; it is untracked and never committed (`git log -- corpus/evidence/round47/measure-after.txt` empty; absent from `git archive 1fc5ed1`; `git status` `??`). Every prior round's measure file is tracked. Content (verified) matches my re-runs including 94/94 — the defect is the pointer, not the numbers.
3. **SCORECARD:2505 survivor list is stale: double negation no longer passes.** "… double negation or a second bullet still passes (`CritC1Survivors`)". At tip, `Since \`the release ships a frozen pool\`, the pool is not unfrozen at release` → `FINDING INF_POLARITY_FLIP`, exit 1 (un- branch fires before negator-window logic). Wave-2 `CritC1Claim` reproduces; the survivor statement measured at a15610a5 no longer holds at tip.
4. **SCORECARD:2524 capability row overstates figure-leg reachability.** "or re-denominate a counts figure against its key" — in lane practice every entry runs `--counts /dev/null` (SKILL.md Gates row; c3-count.py:174), so the figure leg fires only on the three fixtures. Also, the same leg has real-corpus false positives: `SweepC1Corpus` ran 63 entries × 3 configs × 2 tools (378 runs, 0 exit diffs) and found 2 false `INF_POLARITY_FLIP` on `evidence-snapshot-coverage-r40.md` (r45 counts) — `extra_not_frozen` group label poisons affirmative figures `7,572`/`5,959`. This is a calibration defect on real corpus text the frozen fixtures cannot reach.
5. **SHONEN.md**: no round-47 assertion (promotion checklist only); all cited artifacts exist in the committed tree (SKILL.md Gates table at :76, metadata-screen-r25.md, archives-r9, research-gate.sh, round25-measure-after.log, round25-meta-differential.log, PROVINCE.md; LOG Round 9 at :455). Zero mismatches.

## 3. Axis verdicts disputed
- **operability ("improved") — trade, not net improvement.** Counter leg holds (C1=PASS; D7 body at a156 exits 1). But: fresh held-out rates (wave 2) = misses 8/12 on genuine natural flips (`HeldOutB`), false refusals 2/12 on correct bullets (`HeldOutA`); tuning-set 5/10 is disclosed as non-held-out; `RevC1Regex` shows `free`/attributive `un-`/`fail`/`missing` mask or over-tag (accepts a real flip; refuses a correct bullet); `MutC1Refined`: 5 of 7 refinement mutants survive the frozen counter (fixture-set coverage gap, not tool defect). "Correct bullets with a negator outside the window are refused" is exact only for the tuning set; QUALITY 67's equivalent sentence was inverted in wave-2 testing (passes).
- **calibration ("improved narrowly") — honest, but the row's numbers are wrong** (item 2.1); the 8 real mismatches + 3 re-categorized controls + 10 parser-artifact split is correctly disclosed in the lesson (mistake 3).
- **depth ("improved") — holds** with two entry-word overclaims flagged by wave 2: amendment bullet 4 "measures pool-dependence" overstates ("demonstrates"; no dependence metric in S094), base bullet 26's "error rate of this order" does not follow from CFEVER figures (needs S090's model-quality gate). 35 spans, anchors, quarantine 4/4, entries grounded — all re-verified.
- **coverage ("improved narrowly") — holds** (`ScoutCoverageGround`: support DEFINITION, annotator decision rule, per-step reliability are new; map did not hold; four-state frame and 0.6841 already held).
- **freshness (unchanged) — holds**: all six captures mtime 2026-10-23 20:36–20:39 −03 < launch 2026-10-25T08:25:52.
- **adjacency (unchanged) — holds**: no sibling holds the ground (`ConnectSiblings` scanned 20 lanes); PEOPLEPROFILES model-agreement left to kengaku (`ScoutProvinceFit`).

## 4. Commands (decisive output above)
`git cat-file -t` on all hashes; `git archive 1fc5ed1|tar` → counters and controls as §1; `c2-count.py --root` × freeze/base/tip under both counters; round-40 counter at a15610a5/b173b094/tip = 2/6 / 6/6 / 2/6 (exit 1/0/1; receipts bind gate_sha256 4253c187…, a156/tip hold 2cb04bdd…); `sources-census.sh validate` exit 0, same five W04; `build-spans.py --check` exit 0; `git log` on measure-after.txt → no commits; capture mtimes via stat. No installs, no fetch, no lane production edits (report file is the only write).

## 5. Smallest safe corrections (no frozen predicate/counter/fixture/floor change)
- SCORECARD:2506: 93/93 → 94/94 (final counter), freeze-counter after 92/92 → 93/93.
- Commit `corpus/evidence/round47/measure-after.txt` (all rounds' measure files are tracked).
- SCORECARD:2505: drop double negation from the survivor list (it is now refused); phrase the false-refusal cost with the wave-2 held-out numbers when the round report lands.
- C2 row's T tag: keep "improved narrowly" but name the false `92/92` and the 93-vs-94 slot mix.
- Capability row 2524: add "fixture-only in lane practice" to the figure leg.
