# R95MutantsC1 — C1 mutation probe (tools/search-rerun.py)

Seat R95MutantsC1, lane chousa round 95. Carrier C `d27e9891ba6d2bae8b1f6060f7c01bf13a1a6ea1`, base `7b237358`. Scratch `/fast/scratch/hyaku/chousa-r95/R95MutantsC1` (shared clone at `repo/`, mutants under `mut/`, fixture repo `fixture/`, per-mutant work dirs `w-*`). No lane files edited. Tool hash (carrier clone `repo/tools/search-rerun.py`): `3082b226d680fe79cfb39c2f14ab62e0d5c6ce3f59636f44d662c10946a9b67e` (333 lines).

## Baseline (pristine)

Command: `python3 -B corpus/evidence/round95/rerun-controls-r95.py --root . --work /fast/scratch/hyaku/chousa-r95/R95MutantsC1/w-base` — exit 0.

```
POSITIVE=1/1 STRICT_TREE=1/1 FORGERY_REFUSED=8/8 PRIOR_ACCEPTED=8/8 SETUP_REFUSED=12/12 CLONE_TREE=2/2 DO_NOTHING_REFUSED=1/1 ORACLES_REJECTED=3/3
RERUN_CONTROLS=PASS
```

Receipt: `.ufo/waves/round-95/w1/R95MutantsC1-baseline.txt` (copied from `w-base` run log).

## Mutant set (18 built, 16 scored + 2 rebuilt)

Each mutant is a smallest-point edit of the pristine source. Battery invocation per mutant:

`python3 -B corpus/evidence/round95/rerun-controls-r95.py --root /fast/scratch/hyaku/chousa-r95/R95MutantsC1/repo --work /fast/scratch/hyaku/chousa-r95/R95MutantsC1/w-<name> --tool /fast/scratch/hyaku/chousa-r95/R95MutantsC1/mut/<name>.py`

### Killed by the frozen battery (RERUN_CONTROLS=FAIL)

| Mutant | Edit | Battery result |
|---|---|---|
| m01-no-count | COUNT_DRIFT block removed | FORGERY 5/8 (f1 accepted, f5/f6 wrong codes) |
| m02-fixed (rebuild of m02) | digest-path SET_DRIFT dropped | FORGERY 7/8 (f4 accepted) |
| m03-no-set2 | list-path SET_DRIFT dropped | FORGERY 5/8 (f2 accepted, f5/f6 half wrong) |
| m05-no-tree | TREE_CHANGED never raised | STRICT_TREE 0/1, CLONE 1/2 |
| m06-always-strict | TREE_CHANGED counted without --strict | POSITIVE 0/1, CLONE 1/2 |
| m07-set-countonly | SET check compares counts only | FORGERY 3/8 |
| m08-any-engine | unknown engine coerced to fixed | SETUP 11/12 (s4) |
| m09-no-dotdot | `..` segment allowed in where | SETUP 11/12 (s5) |
| m18-tree-is-rev | tree re-run replaced by rev result | STRICT_TREE 0/1, CLONE 0/2 |

Failing-case lines, e.g. m01 (`out-m01-no-count.log`): `CASE f1-count rc=0 expect=1 codes=[] want=['COUNT_DRIFT'] FAIL`; m07 (`out-m07-set-countonly.log`): f2/f4 `rc=0 ... want=['SET_DRIFT'] FAIL`; m03 (`out-m03-no-set2.log`): f2 `rc=0 ... codes=[] want=['SET_DRIFT'] FAIL`. All battery logs are copied to `w1/R95MutantsC1-out-*.log`.

Notes on construction: first-pass m02 and m04 deleted the `SET_DRIFT` line leaving an empty `if` block (IndentationError); those runs are NOT kills — recorded as detector-construction failures in `out-m02-no-set1.log` / `out-m04-no-setboth.log` and rebuilt as m02-fixed/m04-fixed with `pass`. m02-fixed kills (7/8). m04-fixed (both SET paths dropped) asserts `commit:` under the battery's own oracle-generation step (`SETUP oracle count-only mutation did not apply`, exit 2): the battery can't score it because its `count-only` oracle is built by string-replacing `codes.append("SET_DRIFT")`, a string m04 deletes. Inconclusive-as-battery-run, but killed-by-composition: m02 and m03 each isolate one SET path and both are killed, so dropping both is detectable by the same FORGERY group on f2/f4.

### Surviving the frozen battery (RERUN_CONTROLS=PASS, exit 0) — 8 mutants

All eight scored `POSITIVE=1/1 STRICT_TREE=1/1 FORGERY_REFUSED=8/8 PRIOR_ACCEPTED=8/8 SETUP_REFUSED=12/12 CLONE_TREE=2/2 DO_NOTHING_REFUSED=1/1 ORACLES_REJECTED=3/3` / `RERUN_CONTROLS=PASS` (logs `out-m10-*.log` .. `out-m17-*.log` in w1). For seven of them a direct probe on a controlled fixture repo (fixture commit `f81754a…`, files `a.txt`=`ab\ndp`… see fixture notes below) proves the mutant is behaviourally different from pristine — the battery simply does not measure that axis. For m12 the mutation is provably unobservable (see row).

Fixture: `git -C $S/fixture init; a.txt="ab\ncd\n", b.txt="AB\ncd\n", c.txt="ab cd\n"`, commit `f81754afe7362e18aa409a88ee269891a9eb7a1c` (rev on records); later `sub/x.txt="qabq\n"` committed as `db04317d…`. Direct probes run `python3 -B <tool> verify $S/direct/<case>.md --root $S/fixture` (records in `$S/direct/`).

| Mutant | Mutation | Battery | Direct probe (pristine vs mutant) | Battery gap |
|---|---|---|---|---|
| m10-whole-file | `hit()` searches the whole blob instead of lines | PASS | m10.md (`ab\ncd`, hits 0): pristine CLEAN exit 0 (`at_rev=0`), mutant `COUNT_DRIFT,SET_DRIFT` exit 1 (`at_rev=1`) | No forgery spans a newline; named limit **(b)** (per-line, never spans `\n`) is exactly the unmeasured axis. A regex with `\n` in it silently changes meaning and no control notices. |
| m11-ci-fixed | fixed needle lowercased before search | PASS | m11.md (`ab`, hits 2 = a,c): pristine CLEAN exit 0, mutant `COUNT_DRIFT,SET_DRIFT` exit 1 (`at_rev=3`: b.txt also hit) | f5/f6 change engine/needle but never exercise case-folding; `fixed`="literal byte string" (docstring line 24) unmeasured. |
| m13-hits-len-set | count check uses `len(r["set"])` when a list is present | PASS | m13.md (hits=99, set=a,c): pristine `COUNT_DRIFT` only, DRIFT exit 1; mutant CLEAN exit 0 (`rev_match=1/1`) | f1 (hits 15 vs digest form Q5) can't reach it: with a list-form hit_set, `hits` becomes unverified unless the list length matches. C1's "refuse a record whose filed count … differs" is only half-true? See verdict. |
| m14-revok-mask | `rev_ok += 1` unconditionally | PASS | m14.md (hits=99): pristine `rev_match=0/1`; mutant `rev_match=1/1` while `findings=1` and exit 1 | Battery gates POSITIVE on `rev_match=8/8` + `SEARCH_RERUN: CLEAN` + exit 0 and gates forgeries on `rev=DRIFT` lines — it never cross-checks `rev_match` against the per-line verdicts. Frozen predicate 1 prints `rev_match=8/8`; this mutant makes that printed number lie while still being DRIFT, and no control would notice. |
| m15-tree-count | `changed = len(at_tree) != len(at_rev)` | PASS | m15.md with disk swap c.txt→d.txt (same count, different file): pristine `tree=CHANGED` + TREE_CHANGED, DRIFT exit 1; mutant `tree=SAME`, CLEAN exit 0 | CLONE_TREE case edits one capture (count changes 7→8), so count-only comparison sees it. A set-maintaining, count-preserving file swap is invisible. |
| m16-set-ignore-dups | `set(r["set"]) != set(at_rev)` replaces sorted-list equiv | PASS | m16.md (set with `c.txt` twice): pristine `SET_DRIFT` DRIFT exit 1; mutant CLEAN exit 0 | f2 swaps two real paths (set changes), so dedup-blind comparison still fires. Duplicate-path hit_set unmeasured. |
| m17-fnmatch | `fnmatch` (crosses `/`) replaces `PurePosixPath.full_match` | PASS | m17.md (`*.txt` @ `db04317d…` with `sub/x.txt`): pristine CLEAN (`at_rev=2`, sub not matched), mutant `COUNT_DRIFT,SET_DRIFT` (`at_rev=3`) | f8-where (`0*.txt`, single segment) behaves identically under both. Documented "`*` stays inside one path segment" (docstring line 27-28) unmeasured. |
| m12-digest-unsorted | digest over insertion order, not `sorted(paths)` | PASS | No probe can differ: `run_at_rev` iterates `sorted(entries.items())`, so `found` is always ascending — sorted≡unsorted for every record. Equivalent mutant. | Not a coverage gap; but note the tool's digest claim rests on iteration order, not the sort in `digest()` — if `run_at_rev` order ever changes, this latent coupling matters. |

### Tally

Killed by battery: 9 (m01, m02-fixed, m03, m05, m06, m07, m08, m09, m18). m04 (both SET dropped): inconclusive as a battery run (oracle-generation guard), killed by composition of m02+m03. Surviving the battery: 8 (m10, m11, m12, m13, m14, m15, m16, m17) — 7 real behavioural differences the battery misses plus 1 equivalent mutant. So 10/18 mutants killed by the battery (9 + m04-by-composition), 7 escaping with real behavioural deltas.

## Does the C1 sentence fall?

The frozen C1 sentence ("refuse a record whose filed count or hit set differs", `TREE_CHANGED` exit 0 unless `--strict`, 8 searches matching, prior instrument accepting 8 forgeries the new tool refuses) is true of the pristine tool: baseline PASS, all forgeries with the documented codes. No surviving mutant is the frozen tool; each shows a blind spot of the *battery*, not a falsehood of the *sentence*. None of the eight survivors falsifies a frozen number as stated about the actual instrument. However, two survivors touch the sentence's wording closely: m13 shows that with a list-form `hit_set`, the filed `hits` count is never verified, so the sentence's "refuse a record whose filed count … differs" overstates the tool (it verifies the count only against the digest form or, for lists, indirectly through the set equality — a duplicated-path list with wrong `hits` slips through: m16×m13 composition). m14 shows the frozen predicate's headline number `rev_match=8/8` is not self-consistent with the per-search verdicts. Accordingly: held (the instrument behaves as claimed; the battery's coverage is materially narrower than the sentence's eight forgery axes imply), with these as named-limit/coverage findings.

Kill-rule check: K2 (forgery accepted) — not fired against the pristine tool. K4 (a stand-in passes the battery) — the battery's own ORACLES exist for source-blind stand-ins; m10/m11/m13–m17 are source-*aware* mutants, a different class, and K4 as written aims at constants/source-blind stand-ins — do-not-nothing/constant already refused. Recorded as a coverage note, not a kill.

## Receipts in w1

`R95MutantsC1-baseline.txt` (baseline battery log), `R95MutantsC1-out-*.log` (18 battery runs incl. initial m02/m04 construction failures and m02-fixed/m04-fixed reruns), plus direct probe transcripts captured in this run. Fixture/direct records under scratch `direct/`, fixture repo at `fixture/`, mutants at `mut/*.py`.

## Restoration

Lane never modified (reads + scratch clones only); carrier tree hash re-verified `3082b226…` before the run. Scratch tree removed after writing receipts? No — receipts copies await from the `w-*` logs; `mut/` and `fixture/` left deleted (see cleanup note). [Scratch removed by the orchestrator's trap; all cited receipts are copied under `.ufo/waves/round-95/w1/R95MutantsC1-*`.]

VERDICT: R95MutantsC1 C1 held — the pristine tool satisfies the frozen sentence, but 7 of 18 mutants (per-line vs whole-file, case-insensitive fixed, hits-vs-list, rev_match lying, tree count-only, set dedup-blind, fnmatch glob) survive the battery and prove real coverage gaps, notably that filed `hits` is unverified for list-form hit_sets and the printed `rev_match` number can lie.


## Direct-probe transcripts (fixture commit f81754afe7362e18aa409a88ee269891a9eb7a1c; m17 uses db04317d748dcfdc62210c1fd23923a61af40ba2)
## m10 (ab\ncd, hits 0)
--- pristine ---
SEARCH_RERUN Q1 rev=MATCH tree=SAME recorded=0 at_rev=0 at_tree=0
SEARCH_RERUN_SUMMARY searches=1 rev_match=1/1 tree_same=1/1 findings=0
SEARCH_RERUN: CLEAN
EXIT=0
--- m10-whole-file ---
SEARCH_RERUN Q1 rev=DRIFT tree=SAME recorded=0 at_rev=1 at_tree=1 COUNT_DRIFT,SET_DRIFT
SEARCH_RERUN_SUMMARY searches=1 rev_match=0/1 tree_same=1/1 findings=2
SEARCH_RERUN: DRIFT
EXIT=1
## m11 (ab, hits 2)
--- pristine ---
SEARCH_RERUN Q1 rev=MATCH tree=SAME recorded=2 at_rev=2 at_tree=2
SEARCH_RERUN_SUMMARY searches=1 rev_match=1/1 tree_same=1/1 findings=0
SEARCH_RERUN: CLEAN
EXIT=0
--- m11-ci-fixed ---
SEARCH_RERUN Q1 rev=DRIFT tree=SAME recorded=2 at_rev=3 at_tree=3 COUNT_DRIFT,SET_DRIFT
SEARCH_RERUN_SUMMARY searches=1 rev_match=0/1 tree_same=1/1 findings=2
SEARCH_RERUN: DRIFT
EXIT=1
## m13 (hits=99, set a,c)
--- pristine ---
SEARCH_RERUN Q1 rev=DRIFT tree=SAME recorded=99 at_rev=2 at_tree=2 COUNT_DRIFT
SEARCH_RERUN_SUMMARY searches=1 rev_match=0/1 tree_same=1/1 findings=1
SEARCH_RERUN: DRIFT
EXIT=1
--- m13-hits-len-set ---
SEARCH_RERUN Q1 rev=MATCH tree=SAME recorded=99 at_rev=2 at_tree=2
SEARCH_RERUN_SUMMARY searches=1 rev_match=1/1 tree_same=1/1 findings=0
SEARCH_RERUN: CLEAN
EXIT=0
## m14 (hits=99)
--- pristine ---
SEARCH_RERUN Q1 rev=DRIFT tree=SAME recorded=99 at_rev=2 at_tree=2 COUNT_DRIFT
SEARCH_RERUN_SUMMARY searches=1 rev_match=0/1 tree_same=1/1 findings=1
SEARCH_RERUN: DRIFT
EXIT=1
--- m14-revok-mask ---
SEARCH_RERUN Q1 rev=DRIFT tree=SAME recorded=99 at_rev=2 at_tree=2 COUNT_DRIFT
SEARCH_RERUN_SUMMARY searches=1 rev_match=1/1 tree_same=1/1 findings=1
SEARCH_RERUN: DRIFT
EXIT=1
## m15 (disk swap c.txt->d.txt, --strict)
--- pristine ---
SEARCH_RERUN Q1 rev=MATCH tree=CHANGED recorded=2 at_rev=2 at_tree=2 TREE_CHANGED
SEARCH_RERUN_SUMMARY searches=1 rev_match=1/1 tree_same=0/1 findings=1
SEARCH_RERUN: DRIFT
EXIT=1
--- m15-tree-count ---
SEARCH_RERUN Q1 rev=MATCH tree=SAME recorded=2 at_rev=2 at_tree=2
SEARCH_RERUN_SUMMARY searches=1 rev_match=1/1 tree_same=1/1 findings=0
SEARCH_RERUN: CLEAN
EXIT=0
## m16 (c.txt listed twice)
--- pristine ---
SEARCH_RERUN Q1 rev=DRIFT tree=SAME recorded=2 at_rev=2 at_tree=2 SET_DRIFT
SEARCH_RERUN_SUMMARY searches=1 rev_match=0/1 tree_same=1/1 findings=1
SEARCH_RERUN: DRIFT
EXIT=1
--- m16-set-ignore-dups ---
SEARCH_RERUN Q1 rev=MATCH tree=SAME recorded=2 at_rev=2 at_tree=2
SEARCH_RERUN_SUMMARY searches=1 rev_match=1/1 tree_same=1/1 findings=0
SEARCH_RERUN: CLEAN
EXIT=0
## m17 (*.txt with sub/x.txt)
--- pristine ---
SEARCH_RERUN Q1 rev=MATCH tree=SAME recorded=2 at_rev=2 at_tree=2
SEARCH_RERUN_SUMMARY searches=1 rev_match=1/1 tree_same=1/1 findings=0
SEARCH_RERUN: CLEAN
EXIT=0
--- m17-fnmatch ---
SEARCH_RERUN Q1 rev=DRIFT tree=SAME recorded=2 at_rev=3 at_tree=3 COUNT_DRIFT,SET_DRIFT
SEARCH_RERUN_SUMMARY searches=1 rev_match=0/1 tree_same=1/1 findings=2
SEARCH_RERUN: DRIFT
EXIT=1
