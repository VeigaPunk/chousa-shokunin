# Round 46 w1 — ExecCounterRun (counter replay on both trees + falsifiers)

seat L1Chousa46.ExecCounterRun (leaf). Item: replay the three frozen counters on
the CURRENT tree and on a `git archive` of freeze `c2f0e9d1` in /tmp; run the two
instrument selftests; falsify the counters. Snapshots 07:30:26 and 07:31:11
(-03:00) — siblings wrote between them, so both are reported.
Frozen tree: `git archive c2f0e9d1 | sha256sum` =
`4a8b485cb8edb4bc3af9e591d474ed6e490a5756272655431cd1b51aaae24b94` →
/tmp/chousa-r46-ExecCounterRun/frozen (tools=7, no `tools/inference-ground.py`).
Scratch (frozen extract, forges, forged SKILL copies) deleted at close.

## 1. FROZEN tree (freeze commit, extracted)

```
$ python3 corpus/evidence/round46/c1-count.py --root …/frozen
TOOL=absent / POSITIVE_PASS=0/3 / JUNK_KILLED=0/3 / C1=FAIL            exit 1
$ python3 corpus/evidence/round46/c2-count.py --root …/frozen --list
16 × UNREGISTERED_PATH (round24-measure.sh … round46/c3-count.py)
ENTRY_POINTS=71 (tools=7 counters=50 named=69) / GATES_ROWS=30
REGISTERED=55/71 / UNREGISTERED=16 / C2=FAIL                          exit 1
$ python3 corpus/evidence/round46/c3-count.py --root …/frozen
ENTRIES=0/2 CITES_BOUND=0/5 QUOTE_ROWS=0/11 QUOTES_IN_SPAN=0/11 QUOTES_IN_ENTRY=0/11
CAPTURE_BOUND=0/11 REF_ID_UNBOUND=0 REF_BOUND=0/2 / C3=FAIL             exit 1
  (--lane-only: same, CAPTURE_BOUND=skipped, C3=FAIL, exit 1)
```
`named=69` vs the frozen control sheet's `named=66` is not drift: that control
tree was "round-45 landing + counters/fixtures", i.e. without `round46/claims.md`.
Measured delta = exactly the three `round46/cN-count.py`; union stays 71 (all three
already leg B). The claims' `ENTRY_POINTS ≥ 71` target still holds.

## 2. CURRENT tree, two snapshots

```
07:30:26  C1 TOOL=present 3/3 3/3 PASS exit 0
          C2 ENTRY_POINTS=72 (tools=8 counters=50 named=70) GATES_ROWS=30
             REGISTERED=55/72 UNREGISTERED=17 FAIL exit 1   (17th=tools/inference-ground.py)
          C3 ENTRIES=2/2 CITES_BOUND=5/5 QUOTE_ROWS=11/11 QUOTES_IN_SPAN=11/11
             QUOTES_IN_ENTRY=11/11 CAPTURE_BOUND=11/11 REF_ID_UNBOUND=0
             REF_BOUND=2/2 PASS exit 0  (--lane-only identical, CAPTURE_BOUND=skipped)
07:31:11  C1 PASS exit 0 · C2 REGISTERED=72/72 UNREGISTERED=0 GATES_ROWS=35 PASS exit 0
          · C3 unchanged PASS exit 0
```
C3 flipped 0/5→5/5 between 07:29 and 07:30 (ScribeRows' SOURCES rows); C2 flipped
55/72→72/72 between the two snapshots (ScribeGates* rows, +5 Gates rows).
Safe defaults measured: a root without `corpus/fixtures/inference-ground-r46/` →
`C1=FAIL no-fixtures` exit 2; a missing `--skill` file → `REGISTERED=0/72` exit 1.

## 3. Instruments (regression evidence — neither was touched this round)

```
$ bash tools/research-gate.sh --selftest 2>&1 | tail -2
ok-case  275 bash-pin-override-fake       exit=2
RESEARCH_GATE_SELFTEST: PASS (275 cases, 0 skipped)                    (78.2 s)
$ bash tools/research-gate.sh --selftest >/dev/null 2>&1; echo $?       0
$ bash tools/parent-lifetime.sh --selftest --receipt /tmp/…/st.receipt; echo $?   0
  receipt: start parent_pid=3578586 timeout_s=0 / spawn SelfA,SelfB /
  reap SelfA exit_code=0 / reap SelfB exit_code=0 / end n_spawned=2 n_reaped=2
sha256 research-gate.sh 2cb04bddfd5601d7c113a9b532a25895ce475847ff65f5672afc22586f5ffc34
       parent-lifetime.sh c0b213113bb145dee4177d87a2c118b405b898f2e612cad553ae5298619eb7f1
```
On the command as assigned: `| tail -2` makes `GATE_EXIT` tail's status; the gate's
own exit is the separate run above (0).

## 4. Falsifiers

**F1 — C1's cheapest gate is undefeated: a filename oracle scores full marks.**
`c1-count --tool <exit 0 iff basename startswith "positive-">` →
`POSITIVE_PASS=3/3 JUNK_KILLED=3/3 C1=PASS exit 0`. Declared controls re-measured
and reproduced exactly: always-0 → 3/3,0/3 FAIL; always-1 → 0/3,3/3 FAIL;
cite-presence-only (every `#### Inference` bullet carries `(\`S###\`)`) → 3/3,1/3
FAIL (junk-ungrounded, junk-borrowed survive) — the declared 1/3 is exact. The
predicate is exit-codes-only, so this is a **control-set gap, not a predicate
violation**: C1=PASS alone does not show grounding work. Mitigation measured:
fixtures copied to zeta/alpha/kappa and omega/beta/yotta → 3 positives exit 0,
3 junk exit 1 with `INF_UNCITED` / `INF_TOKEN_NOT_IN_SPAN`; a positive whose token
became `the pool is reissued nightly` → exit 1 with that token; junk-ungrounded
with its invented token replaced by a real span token → exit 0 (correct: it is no
longer junk). The tool's review stays a seated read.

**F2 — the freeze did not hold: all three counters were edited after `c2f0e9d1`.**
```
file      frozen sha256[:16]  worktree sha256[:16]  mtime
c1-count   e7686236c811df49   96833e22b0eb3617    2026-10-25 07:27:37.272
c2-count   06c9e9bc3865b60e   60ad448e99b15cb6    2026-10-25 07:28:28.152
c3-count   5018d7b04eba6bdf   234e2272e8e21e82    2026-10-25 07:29:33.421
```
`git diff c2f0e9d1 -- …/cN-count.py`, three substantive rule changes: c1 junk
`!= 0` → `== 1`; c2 fence-aware `gates_rows` + `<!-- -->` strip + delimiter-bounded
`names()` instead of substring; c3 `span_file` traversal/absolute-path guard and
non-integer `offset` guard. The c1 repair closes a real hole — a tool exiting 0 on
positives and **crashing (2)** on junk scores `FROZEN → JUNK_KILLED=3/3 C1=PASS
exit 0` but `WORKTREE → JUNK_KILLED=0/3 C1=FAIL exit 1`; the frozen sentence says
"exits 1", so the repair measures the declared predicate, but it landed after
scoring began. Both readings agree on the current tree at 07:30:26 (`C1 PASS 0`,
`C2 55/72 UNREGISTERED=17 exit 1`, `C3 PASS 0`), so no verdict flipped.
**L1 decision needed:** admit under the repaired rules with an errata line, or
re-freeze.

**F3 — C2's row test is format-only.** One junk row under `## Gates` registers an
unregistered path: `| x | x | x | x | x | x | x | x | corpus/evidence/round34/
self-audit.py exit |` → `GATES_ROWS=31 REGISTERED=56/72` (baseline 55/72). The
hardening elsewhere holds: fenced copy not registered (30 rows); `…/self-audit.py.bak`
not registered; no `exit` not registered; missing `--skill` → 0/72 exit 1. New:
the ≥8-pipe threshold counts **escaped** pipes —
`| a | b | c | x\|y\|z\|w\|q | corpus/evidence/round34/self-audit.py exit 0 |`
(10 pipes, 5 real cells) counts as a Gates row (`GATES_ROWS=36`). The docstring's
named limit ("a *plausible* row whose verdict map is wrong passes") understates:
an implausible row, or a 5-cell one, passes too.

**F4 — C2 blind spot: 10 executable scripts are invisible to A∪B∪C.** 82 `.py`/
`.sh` files exist in the lane; the union is 72:
`round25-holds/battery.sh`, `round25-meta-oracle.py`, `round25-sources-census.sh`,
`round26-registry-oracle.py`, `round29/prose-check.py`, `round30/rerun-check.py`,
`round32/q33-check.py`, `round45/build-spans.py`, `round45/tag-count.py`,
`round46/build-spans.py` (all under `corpus/evidence/`). Not a C2 failure (the
predicate defines entry point as A/B/C only), but the round's own span builder is
in the list even though a new Gates row names it: registration ≠ membership.
Round-47 question, not fixable under this freeze.

**F5 — C3's REF_BOUND is co-occurrence, so a denial binds.** Forge lane root at
/tmp: five real `source:` lines, five 11-cell `mined` registry rows, 11 span rows
that are exact slices of the five real captures with their real digests, and the
cross-ref sentences `S079 is not RFC 7089; it is an unrelated note.` /
`S081 is not WARP either.`
```
ENTRIES=2/2 CITES_BOUND=5/5 QUOTE_ROWS=11/11 QUOTES_IN_SPAN=11/11
QUOTES_IN_ENTRY=11/11 CAPTURE_BOUND=11/11 REF_ID_UNBOUND=0 REF_BOUND=2/2
C3=PASS                                                               exit 0
```
CAPTURE_BOUND is satisfiable because the forge used real bytes — declared design.
REF_BOUND is not: the claim says the two references "bind by document". Kill rules
do work, on variants: `S090` in an entry → `REF_ID_UNBOUND=1 FAIL`; 12th quote row
→ `FAIL` (`len(rows)!=11`); one corrupted digest → `CAPTURE_BOUND=10/11 FAIL`.

**F6 — the real entries pass the check F5 says the counter cannot make.**
`r39.md:23` and `amendment:21` both read "… RFC 7089 (`S079`) makes an archived
state addressable by date, and the NDL note on WARP's URL renewal (`S081`) shows a
capture timestamp …"; `amendment:29` records the re-binding ("RFC 7089 is lane
`S079` and the NDL E2867 WARP note is lane `S081`"). Polarity positive, documents
right. Registry rows field-checked: S085–S089 each 11 cells, `status=mined`,
`used-by` = the citing entry, URL in the source cell.

**F7 — the span ground is real, verified without the counter.** Re-derived from
the five captures (`sha256(url)[:24].txt`; 4146 / 60153 / 5676 / 12775 / 126093
bytes; digests e18eeb26…, c508913a…, dfc3e0f5…, 603f9b42…, 35bdf1c1…):
`{'n': 11, 'sha': 11, 'slice': 11, 'in_span': 11, 'in_entry': 11}`. Quotes read
like the documents (`A list of evidence sets`, `recall of 72.36%`,
`"conceptdoi": "10.5281/zenodo.4925953"`, `An archive.org link for the source url`,
`published before the claim’s date`). Two of the eleven rows are second spans of
S085/S086 — allowed (no uniqueness rule), recorded so 11 is not read as 11 distinct
documents.

**F8 — the five new Gates rows are substantive, not filler.** Diffed `## Gates`
rows against frozen SKILL.md: 5 new rows, real verdict maps with exit codes
(`inference-ground (r46)` → `exit 0` grounded / `exit 1` findings / `exit 2` usage;
`chousa round-46 counters` names c1/c2/c3 plus build-spans). One row exhibits F3's
escaped-pipe looseness (14 fields naively split, 8 real cells — it renders
correctly). C2=PASS was not obtained with junk rows.

## 5. Verdict at close (07:31:11; re-run 07:32:03 unchanged)

- **C1 PASS** (exit 0). Real tool does lexical grounding (renamed fixtures,
  mutation checks). Residual: the counter cannot tell it from a filename oracle;
  the tool review is a seated read.
- **C2 PASS** (exit 0, 72/72, GATES_ROWS=35). Was FAIL(17) five minutes earlier;
  target ≥71 holds. Residual: format-only row test (F3), invisible set (F4).
- **C3 PASS** (exit 0, both modes). Binding independently verified (F7), polarity
  read (F6). Semantic support of each quote remains the reviewers' judgement — the
  counter binds bytes, not meaning.
- **Freeze integrity (F2)** is the one open decision: three counters changed after
  `c2f0e9d1`; both versions agree on today's tree, but the admission rule now has
  three edits to answer for.

## 6. Bounds

No fetch, no network, no installs. No writes to lane production files, the lane git
index/jj, the fleet repo or shokuknow; the only file I wrote is this report.
`git status` at close carries only siblings' work (`M SKILL.md`,
`M corpus/SOURCES.md`, `M round46/{c1,c2,c3}-count.py`, `?? knowledge/
evidence-pool-versioning-r39*.md`, `?? round46/{build-spans.py,spans.tsv,spans/}`,
`?? tools/inference-ground.py`, plus the pre-existing wave-registry/cells edits).
