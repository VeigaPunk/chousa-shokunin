# Round 46 w1 — ExecCounterRun (counter replay on both trees + falsifiers)

seat L1Chousa46.ExecCounterRun (leaf). Item: replay the three frozen counters on the CURRENT tree and on a
`git archive` of freeze `c2f0e9d1` in /tmp; run the two instrument selftests; falsify the counters.
Snapshots 07:30:26 / 07:31:11 / 07:32:37 / 07:34:18 (-03:00), each pinned to the counter and tool sha in force.
Frozen tree `git archive c2f0e9d1` = `4a8b485cb8edb4bc3af9e591d474ed6e490a5756272655431cd1b51aaae24b94` →
/tmp/chousa-r46-ExecCounterRun/frozen (tools=7, no `tools/inference-ground.py`); scratch deleted at close.

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
**Receipt errata, measured.** (E1) `claims.md:66` prints `named=66`; the freeze commit it rests on prints `named=69`.
Stripping only the three `round46/cN-count.py` mentions from its own `claims.md` reproduces `71 (tools=7 counters=50
named=66) GATES_ROWS=30 REGISTERED=55/71 UNREGISTERED=16`; union and `UNREGISTERED` are identical either way, because
those three enter via leg B. (E2) `claims.md:40` labels `controls/c1-before.txt` "base tree" while that file's header
says "6e2630a + this round's counters and fixtures": bare `6e2630a` measures `REGISTERED=55/68 UNREGISTERED=13`
(debt 13), the augmented tree 16. `ENTRY_POINTS ≥ 71` holds in every reading.

## 2. CURRENT tree, three snapshots

```
07:30:26  c1 96833e22 c2 60ad448e c3 234e2272
          C1 TOOL=present 3/3 3/3 PASS exit 0
          C2 ENTRY_POINTS=72 (tools=8 counters=50 named=70) GATES_ROWS=30
             REGISTERED=55/72 UNREGISTERED=17 FAIL exit 1   (17th=tools/inference-ground.py)
          C3 ENTRIES=2/2 CITES_BOUND=5/5 QUOTE_ROWS=11/11 QUOTES_IN_SPAN=11/11
             QUOTES_IN_ENTRY=11/11 CAPTURE_BOUND=11/11 REF_ID_UNBOUND=0 REF_BOUND=2/2
             PASS exit 0   (--lane-only identical, CAPTURE_BOUND=skipped)
07:31:11  C1 PASS exit 0 · C2 REGISTERED=72/72 UNREGISTERED=0 GATES_ROWS=35 PASS exit 0 · C3 PASS exit 0
07:32:37  c1 819287e2 c2 60ad448e c3 234e2272 · all three PASS exit 0 (shas of the c1 edit in F2)
```
C3 flipped 0/5→5/5 between 07:29 and 07:30 (ScribeRows' SOURCES rows); C2 flipped 55/72→72/72 between the first
two snapshots (ScribeGates* rows, +5 Gates rows). Safe defaults: a root without the fixtures dir → `C1=FAIL
no-fixtures` exit 2; a missing `--skill` → `REGISTERED=0/72` exit 1.

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
On the command as assigned, `| tail -2` makes `GATE_EXIT` tail's status; the gate's own exit is the separate run (0).

## 4. Falsifiers

**F1 — C1's cheapest gate is undefeated: a filename oracle scores full marks.** Re-measured on pinned counter
`819287e2`: `--tool <exit 0 iff basename startswith "positive-">` → `POSITIVE_PASS=3/3 JUNK_KILLED=3/3 C1=PASS
exit 0`. Declared controls reproduce exactly: always-0 → 3/3,0/3 FAIL; cite-presence-only (every `#### Inference`
bullet carries a `(\`S###\`)` token) → 3/3,1/3 FAIL (junk-ungrounded, junk-borrowed survive). Exit-codes-only
predicate, so this is a **control-set gap, not a predicate violation**: C1=PASS alone does not show grounding work.
Mitigation at both tool shas: renamed fixtures (zeta/alpha/kappa, omega/beta/yotta) → 3 positives exit 0, 3 junk
exit 1 with `INF_UNCITED`/`INF_TOKEN_NOT_IN_SPAN`; rewriting a positive's token to `the pool is reissued nightly` →
exit 1; grounding the junk-ungrounded token in a real span → exit 0 (correct: it is no longer junk).

**F2 — the freeze did not hold: all three counters were edited after `c2f0e9d1` (c1 twice).**
```
file      frozen sha256[:16]  worktree sha256[:16]  mtime (worktree)
c1-count   e7686236c811df49   96833e22b0eb3617    2026-10-25 07:27:37.272   → second edit 07:31:17.028 = 819287e2075c3f5b
c2-count   06c9e9bc3865b60e   60ad448e99b15cb6    2026-10-25 07:28:28.152
c3-count   5018d7b04eba6bdf   234e2272e8e21e82    2026-10-25 07:29:33.421
```
`git diff c2f0e9d1 -- …/cN-count.py`: c1 junk `!= 0` → `== 1` **plus** a `PINNED` table of eight fixture digests
enforcing the frozen "fixture set changed after this freeze fails the claim" clause; c2 fence-aware `gates_rows`,
`<!-- -->` strip, delimiter-bounded `names()`; c3 `span_file` traversal and non-integer `offset` guards. The c1
repair closes a real hole: a tool exiting 0 on positives and **crashing (2)** on junk scores
`FROZEN → JUNK_KILLED=3/3 C1=PASS exit 0` but `WORKTREE → JUNK_KILLED=0/3 C1=FAIL exit 1`.
Pin check: all eight `PINNED` digests equal `git show c2f0e9d1:corpus/fixtures/…` **and** the live bytes (8/8), so the pins bind the frozen fixtures. Gap: they cover `spans.tsv` but not the span files it names (`spans/S901-1.txt`, `S902-1.txt`), so editing a span file changes the tool's verdict without tripping `FIXTURES_CHANGED`.
Both readings agree on the 07:30:26 tree (C1 PASS 0, C2 55/72 17 FAIL 1, C3 PASS 0), so no verdict flipped. **L1 decision:** admit under the repaired rules with an errata line, or re-freeze.

**F3 — C2's row test is format-only, and two comment/fence routes remain.** One junk row under `## Gates` registers
an unregistered path: `| x | x | x | x | x | x | x | x | corpus/evidence/round34/self-audit.py exit |` →
`GATES_ROWS=31 REGISTERED=56/72` (baseline 55/72). Hardening holds elsewhere: fenced copy not registered (30 rows);
`…/self-audit.py.bak` not registered; no `exit` not registered. Live hazards in `60ad448e` (also measured by
`MutC2Forge`): a row inside a **multi-line** `<!-- … -->` is still a row (`GATES_ROWS` 35→36, `C2=PASS`); one
**unterminated** ` ``` ` inside `## Gates` → `GATES_ROWS=0 REGISTERED=0/72` exit 1 (fail-closed, but a
whole-registry false negative). New: the ≥8-pipe threshold counts **escaped** pipes —
`| a | b | c | x\|y\|z\|w\|q | corpus/evidence/round34/self-audit.py exit 0 |` (10 pipes, 5 real cells) counts as a
Gates row; the docstring's named limit therefore understates.

**F4 — C2 blind spot: 10 executable scripts are invisible to A∪B∪C.** 82 `.py`/`.sh` files exist in the lane; the
union is 72: `round25-holds/battery.sh`, `round25-meta-oracle.py`, `round25-sources-census.sh`,
`round26-registry-oracle.py`, `round29/prose-check.py`, `round30/rerun-check.py`, `round32/q33-check.py`,
`round45/build-spans.py`, `round45/tag-count.py`, `round46/build-spans.py` (all under `corpus/evidence/`). Not a C2
failure (entry point is defined as A/B/C only), but the round's own span builder is in it although a new Gates row
names it: registration ≠ membership. Round-47 question.

**F5 — C3's REF_BOUND is co-occurrence, so a denial binds.** Forge lane root at /tmp with the five real `source:`
lines, five 11-cell `mined` registry rows, 11 span rows that are exact slices of the five real captures with their
real digests, and `S079 is not RFC 7089; it is an unrelated note.` / `S081 is not WARP either.`
```
ENTRIES=2/2 CITES_BOUND=5/5 QUOTE_ROWS=11/11 QUOTES_IN_SPAN=11/11 QUOTES_IN_ENTRY=11/11 CAPTURE_BOUND=11/11
REF_ID_UNBOUND=0 REF_BOUND=2/2 / C3=PASS                                 exit 0
```
CAPTURE_BOUND passes because the forge used real bytes — declared design. REF_BOUND should not: the claim says the
two references "bind by document". Kill rules do work on variants: `S090` in an entry → `REF_ID_UNBOUND=1 FAIL`;
12th quote row → `FAIL`; one corrupted digest → `CAPTURE_BOUND=10/11 FAIL`.

**F6 — the real entries pass the check F5 says the counter cannot make.** `r39.md:23` and `amendment:21` read
"… RFC 7089 (`S079`) makes an archived state addressable by date, and the NDL note on WARP's URL renewal (`S081`)
shows a capture timestamp …"; `amendment:29` records the re-binding ("RFC 7089 is lane `S079` and the NDL E2867
WARP note is lane `S081`"). Polarity positive, documents right; S085–S089 rows each 11 cells, `status=mined`, `used-by` = the citing entry, URL in the source cell.

**F7 — the span ground is real, verified without the counter.** Re-derived from the five captures
(`sha256(url)[:24].txt`; 4146/60153/5676/12775/126093 bytes; digests e18eeb26…, c508913a…, dfc3e0f5…, 603f9b42…,
35bdf1c1…): `{'n': 11, 'sha': 11, 'slice': 11, 'in_span': 11, 'in_entry': 11}`. Quotes read like the documents
(`A list of evidence sets`, `recall of 72.36%`, `"conceptdoi": "10.5281/zenodo.4925953"`, `An archive.org link for the source url`). Two rows are second spans of S085/S086 — allowed; 11 rows ≠ 11 distinct documents.

**F8 — the five new Gates rows are substantive, not filler.** Diffed against frozen SKILL.md: 5 rows with real
verdict maps (`inference-ground (r46)` → exit 0 grounded / 1 findings / 2 usage; `chousa round-46 counters` names
c1/c2/c3 plus build-spans). One row shows F3's escaped-pipe looseness (14 naive fields, 8 real cells; renders fine); C2=PASS was not obtained with junk rows.

## 5. Verdict at close (07:34:18: c1 `819287e2`, c2 `60ad448e`, c3 `234e2272`, tool `3018b1d2`, all PASS exit 0)

- **C1 PASS** (exit 0). Real tool does lexical grounding — at sha `397d9878` and again at the current `3018b1d2`
  the renamed-fixture run gives 3 positives exit 0 / 3 junk exit 1, and the mutation checks behave (F1). Residual:
  the counter cannot tell it from a filename oracle; the tool review is a seated read.
- **C2 PASS** (exit 0, 72/72, GATES_ROWS=35). Was FAIL(17) five minutes earlier; target ≥71 holds. Residual:
  format-only row test with the two live hazards (F3), invisible set (F4).
- **C3 PASS** (exit 0, both modes). Binding independently verified (F7), polarity read (F6). Semantic support of
  each quote remains the reviewers' judgement — the counter binds bytes, not meaning.
- **Freeze integrity (F2)** is the one open decision: three counters changed after `c2f0e9d1` (c1 twice) and the tool
  itself changed at 07:33:33; every version agrees on today's tree, but the admission rule now has five edits to
  answer for.

## 6. Bounds

No fetch, no network, no installs. No writes to lane production files, the lane git index/jj, the fleet repo or
shokuknow; the only file I wrote is this report. `git status` at close carries only siblings' work (`M SKILL.md`,
`M corpus/SOURCES.md`, `M round46/{c1,c2,c3}-count.py`, `M tools/inference-ground.py`, `?? knowledge/
evidence-pool-versioning-r39*.md`, `?? round46/{build-spans.py,spans.tsv,spans/}`, plus the pre-existing
wave-registry/cells edits).
