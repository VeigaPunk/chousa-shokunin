# R50ScribeReportDraft — round-50 report draft (chousa)

Seat: scribe (leaf, no dispatch). Lane HEAD at drafting `c5b8dca85f759c7a772225fe036e7bb9a809b91c`; my only write is this file; scratch `/dev/shm/chousa-r50-R50ScribeReportDraft-2/` deleted; no tool installs. Contract: `.ufo/prompts/chousa-round-50.md` §4.

## Draft — intended lane path `/home/vgpnk/Projects/shokunin/.ufo/reports/round-50/chousa.md`

```markdown
# chousa — round 50 report (hyaku run 7)

Lane `chousa-shokunin`. Round shape: two v1 waves, 42 + 43 = 85 seats (band 64–100). Frozen
claims: `corpus/evidence/round50/claims.md` at `6a068f2ae4847a1e4aa959f088a39ddc1b167bc0`.
No network, no live fetch (L0 `8d77e6c1` open); every source opened from the read-only capture
cache `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/`.

## Work performed

Declared claims, named first:

- **R50-C1 — operability (lowest scored axis, 3/10; capability extension):**
  `python3 tools/assimilate-rows.py --selftest [--fixtures DIR] [--expected FILE]` runs the
  adopter on an isolated fixture package and compares the observed finding lines with the
  `findings` list of a hand-written expected file: on the digest-pinned package
  `corpus/evidence/round50/c1-fixtures/` it exits 0 `SELFTEST=PASS` with 26 findings, on each of
  six perturbed copies it exits 1 naming the perturbed finding in a `DIFF` line, on an
  unparseable expected file it exits 2 `SELFTEST=ERROR`, the lane default exits 0 PASS, and the
  round-49 counter still prints `C1=PASS`.
- **R50-C2 — depth (sourced; section-10 assimilation theme):** "what a Chinese citation-checking
  feature compares, and which of CNKI's manuals document it" is adopted BY DOCUMENT as
  `corpus/knowledge/cnki-citation-check-r40.md`, `citation-matching-semantics-r41.md`,
  `istic-citation-verification-r39.md`; three of four staged documents are BOUND to new
  `SOURCES.md` rows S104–S106 with 55 located quotes, the fourth (CNKI 教师 manual) is REFUSED
  with a `refused-doc` line and flip.

Work items (each with its evidence pointer):

- C1 candidate `ec52e63` — `--selftest`, `corpus/fixtures/assimilate-selftest/` and the
  counter-owned pin `corpus/evidence/round50/c1-fixtures/` (`QUALITY.md:757-771`).
- C1 hardening after W1 falsifiers (`2573dc1`): multiset comparison, exit 2 on option clash or a
  fixture with no entry, `ENTRYCITES … -`, 120 s child timeout, tab-free findings, fixtures check
  before the expected file, `used-by` across twin staged ids — from `w1/ReviewSelftestCode.md`
  F1–F4 (repro `SELFTEST=PASS findings=26 expected=27`) and `w1/ExecSelftestEdge.md`; disclosed
  in `claims-erratum.md` item 1.
- C2 adoption (`74794db`): three entries, rows S104–S106, `quotes.tsv` → `spans.tsv` (55 rows) →
  `spans/`, `corpus/lessons/round-50.md`, `QUALITY.md:753-845` (criteria 73–79).
- Section-10 collision check in scratch only (`w1/ExecCollision.md`; `assimilation/collisions`
  22 lines, `assimilation/guard-proof.txt`): 18 hard collisions S082–S099 plus four re-staged
  rows S100–S103; renumber by document S118→S104, S124/S135→S105 (held), S136→S106; staged S145
  (教师 manual) refused, no lane id. The lane registry is never mutated.
- Refused document: 教师 manual, `.txt` 9914 chars, 引文核对 0 / 匹配 0 (`w1/GroundBnuA.md`,
  `w1/GroundBnuB.md`); lesson `refused-doc` line carries the flip condition.
- Six new checks (`stale-count-check.py`, `wave-complete-check.py`, `cited-id-check.py`,
  `name-collision-check.py`, `decode-form-check.py`, `cjk-ground-check.py`) plus the renumbered
  round-49 `quote-substance-check.py`; `QUALITY.md:757-845`; `SKILL.md:130,132`.
- Two post-freeze tool changes disclosed, none narrowed after data (`claims-erratum.md` items
  1–2): `tools/assimilate-rows.py` hardening (re-verified `C1=PASS`) and
  `tools/inference-ground.py` CJK floor (`inference-regression-before.txt` ≡ `-after.txt`;
  `cjk-ground-check.py` cases A–C).
- Misassigned wave-1 seats: 13 names collided with round-49 agents and those parked agents
  answered with their round-49 reports (`name-collision-before.txt`: 13 `NAME_COLLISION`, exit 1;
  lesson `## Mistakes` row 4). Every wave-2 seat carries the `R50` prefix and
  `python3 corpus/evidence/round50/name-collision-check.py .ufo/waves/round-50/w2-spec.json` →
  `NAME_COLLISIONS=0 ITEMS=43`, exit 0; the 13 items are re-assigned inside wave 2.
- Wave shape: W1 42 seats (scribe 18, executor 10, critic 4, reviewer 3, mutation-tester 2,
  connector 2, scout 2, simplifier 1); W2 43 seats (reviewer 9, critic 9, executor 7, scout 6,
  mutation-tester 6, scribe 3, connector 2, simplifier 1), attack share 24/43. Dead W2 seats, W2
  verdicts and the 13 re-assigned items: <PENDING>. L1 held the planner seat. Spot-check intake
  and the seven mined mistakes: `corpus/lessons/round-50.md` `## Mistakes`, `## Spot-check intake`.

## Landed changes

| commit | change | LOG.md entry |
|---|---|---|
| `6a068f2ae4847a1e4aa959f088a39ddc1b167bc0` | frozen claims, both counters, do-nothing controls, pinned fixtures, span builder (pre-candidate) | <PENDING> |
| `ec52e632` | `assimilate-rows --selftest` + lane-default fixtures (C1 candidate); late round-49 seat reports | <PENDING> |
| `2573dc16` | C1 hardening (multiset compare, work floor, option clash, `ENTRYCITES -`, timeout, tab-free findings), `used-by` across twin staged ids; W1 reports and `w1-results.json` | <PENDING> |
| `74794db07e1b383d5c3e96ad5122fd158a541271` | C2 adoption (S104–S106, three entries, 55-quote manifest, lesson), CJK grounding fix, six checks and receipts, QUALITY 73–79, SKILL gate rows | <PENDING> |
| `c5b8dca8` | wave-2 spec and validated dispatch (`gen-w2-spec.py`, `w2-spec.json`, `w2-dispatch.json`) | <PENDING> |
| `<FINAL-HASH>` | wave-2 receipts, LOG.md round-50 entry, SCORECARD round-50 rows, report | <PENDING> |

LOG.md and SCORECARD.md round-50 rows are unwritten at `c5b8dca` (`grep -n 'Round 50' LOG.md` →
no match; `SCORECARD.md` still ends at `## Planned — round 50 (not started)`): filling them is a
landing item of `<FINAL-HASH>`, not a claim change.

## Before → after measurements

**R50-C1** — counting command `python3 corpus/evidence/round50/c1-count.py`. Before
(`corpus/evidence/round50/controls/c1-before.txt`, base tool copied to `controls/tool-before.py`,
base `3c51da77`): `BASELINE=FAIL rc=2`, `PERTURB_PASS=0/6`, `LEGS=2/5`, `C1=FAIL`, `exit=1`.
Do-nothing controls with the same interface: `echo-tool.py` (`BASELINE=PASS findings=26`,
`PERTURB_PASS=0/6`, `LEGS=4/5`, `C1=FAIL`) and `const-tool.py` (`PERTURB_PASS=0/6`, `LEGS=2/5`,
`C1=FAIL`) — only P1–P6 separate a real self-test from an echo. After
(`corpus/evidence/round50/measure-after-1.txt`, working tree after `74794db`):
`SELFTEST_DEFAULT=PASS`, `BASELINE=PASS rc=0 findings=26`, six `PERTURB … rc=1 -> PASS`,
`PERTURB_PASS=6/6`, `EXPECTED_BAD=PASS rc=2`, `R49_REGRESSION=PASS rc=0`, `LEGS=5/5`, `C1=PASS`,
`exit=0`. Binding re-measurement at `<FINAL-HASH>`: <PENDING> (the receipt is working-tree, not
commit-pinned).

**R50-C2** — counting command `python3 corpus/evidence/round50/c2-count.py`. Before
(`controls/c2-before.txt`, pre-freeze tree): `ENTRIES=0/3`, `BOUND=0/4`, `NEW_GROUND=0/3`,
`INFERENCE_GROUNDED=0/3`, `C2=FAIL`, `exit=1`. Controls (`controls/build-c2-controls.py`): three
staged entries unchanged → `REF_ID_UNBOUND=15`, `BOUND=0/4`, `C2=FAIL`; the same entries rewritten
by the adopter with its append block but no quote, span or lesson → `BOUND=3/4`,
`REF_ID_UNBOUND=8`, `QUOTE_ROWS=0`, `C2=FAIL`. After (`measure-after-1.txt`): `ENTRIES=3/3`,
`BOUND=3/4 (min 3) REFUSED=1`, `BOUND_IDS=S104,S105,S106`, `REF_ID_UNBOUND=0`,
`NEW_GROUND=3/3`, `QUOTE_ROWS=55 ON_BOUND=55/55`, `SPAN_IDS=3/3`, `QUOTES_IN_SPAN=55/55`,
`QUOTES_IN_ENTRY=55/55`, `QUOTES_IN_LESSON=55/55`, `QUOTE_SHORT=55/55`, `SPAN_CONTEXT=55/55`,
`CAPTURE_BOUND=55/55`, `SUBSTANCE=PASS`, `ANCHOR_BOUND=3/3`, `INFERENCE_GROUNDED=3/3`,
`QUARANTINE_VERDICTS=0/0`, `C2=PASS`, `exit=0`. Same caveat: working-tree receipt; `<FINAL-HASH>`
re-run <PENDING>. Named limit from the freeze: the counter proves binding and presence, not
entailment.

## Sources & frontier

Census command `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin chousa`. Before (round start, `3c51da77`;
`.ufo/waves/round-50/lesson-head.md:96`): exit 0, `chousa ok`, five W04 warnings (S051, S053,
S073, S074, S075), 103 rows. After (`c5b8dca`): exit 0, `chousa ok`, the same five W04 warnings,
no new one.

Row count: `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → **106**
(`git show 3c51da77:corpus/SOURCES.md | …` → 103). Rows added by tier: S104 **A**, S105 **B**,
S106 **B**; `git diff 3c51da77..HEAD --stat -- corpus/SOURCES.md` → 5 insertions, 0 deletions
(three rows, one chain line, one search-log line). Rows touched old→new: **none**.

Collision and renumber: the staged package `shokuknow/merge/chousa` reuses lane ids S082–S195;
the scratch collision list is 22 lines — 18 hard collisions (same id, different document,
S082–S099) and four re-staged rows (S100–S103, same URL as the round-49 rows). Adopted ids
continue the lane registry by document: S118→S104, S124/S135→S105 (one document, held),
S136→S106; staged S145 refused; body-only ids S076/S109/S111 removed from the entries rather
than renumbered (`cited-id-check.py`; lesson `## Mistakes` row 3). The lane registry was never
mutated by the adopter.

considerthese: `corpus/lessons/round-50.md:148` — `considerthese/2026-10-25.md` holds no unmined
lane-artefact proposal (its capture-age proposal was mined as QUALITY 71 in round 49); the sweep
is recorded there. Assimilation this round: the `merge/chousa` citation-checking theme (C2), not
a considerthese proposal.

Freshness: unchanged — the newest capture the lane may read is dated 2026-10-24
(`275c79d45b1e9b0fd32cef93.txt`, refused 教师 manual; `28750bcdf5d36cd90a7709fb.txt`, S106);
this round's bound captures were written 2026-10-23 (S104 `001287c436f0e6b1d166ae8d`, S105
`e3ca8f4fdd15420b80096a75`) and 2026-10-24 (S106); L0 `8d77e6c1` still bars fetch.
`python3 corpus/evidence/round49/capture-age-check.py <report>` → `FRESHNESS_CAPTURE_AGE=PASS`,
exit 0.

## Trend verdicts

- **expansion — improved.** Registry 103 → 106 rows, three adopted entries, a 55-row quote
  manifest, and a chain line naming S104 → S105 → S106; the adoption adds documents the lane
  could not read before (a paid verification service's own price/workflow page and two CNKI
  manuals), not restatements. Evidence: the census pair above; `74794db`.
- **quality — <PENDING> (W2).** The round adds QUALITY 73–79 and six checks, but `improved`
  cannot be written yet: `python3 corpus/evidence/round50/stale-count-check.py` exits 1 at
  `c5b8dca` (`STALE_HITS=8 UNRESOLVED=2`: `corpus/README.md:1080` "55-row manifest" read against
  the round-49 31-row receipt; `LOG.md:1803` "28 located quotes" with no resolving correction
  line), and QUALITY 74's cited after-receipt `corpus/evidence/round50/stale-count-after.txt` is
  not in the tree (`git log --all -- …` empty). Either the check is scoped per receipt, the
  missing correction line is appended, or criterion 74's "after them `STALE_COUNT=PASS`" is
  corrected — the W2 verdict names which.
- **discernment — improved.** One of four staged documents was refused after being opened (教师
  manual: 引文核对 0, 匹配 0; flip recorded), S106's 引文核对 absence is scoped to "this copy
  only", and S104 is named by the page's own institution (中国科学院文献情报中心) rather than
  the `istic` path it was staged under; seven staged entries were refused or deferred. Evidence:
  `c2-count.py` `BOUND=3/4 REFUSED=1`; lesson `## Gate` refused-doc line.

## SHONEN

- `[~]` SKILL.md decision tables / cited sources — `SKILL.md:130,132`; non-author verifier:
  <PENDING> (W2).
- `[~]` one end-to-end domain task logged — the S104–S106 adoption and its receipts (`74794db`;
  `corpus/evidence/round50/measure-after-1.txt`); non-author verifier: <PENDING>.
- `[~]` instructions executable without oral context — `python3 tools/assimilate-rows.py
  --selftest` exit 0 `SELFTEST=PASS findings=26` on the pinned fixtures; non-author verifier:
  <PENDING>.
- `[~]` no cross-domain bleed — `PROVINCE.md` unchanged; the three entries stay on
  citation-checking (CNKI 引文核对 / 中国科学院 引证检索); non-author verifier: <PENDING>.
```

## What this draft attacks, and what it found

1. `python3 corpus/evidence/round50/stale-count-check.py` at `c5b8dca` → `STALE_HITS=8 UNRESOLVED=2 RECEIPT_ROWS=31`, `STALE_COUNT=FAIL`, exit 1. Unresolved: `corpus/README.md:1080` (a **round-50** "55-row manifest" read against the round-49 31-row receipt — cross-round false positive of the named one-receipt limit) and `LOG.md:1803` (round-49 "28 located quotes", no `correction: … superseded by …` line in `LOG.md`; `grep -n "LOG.md:1803"` over LOG/README/QUALITY/round-49 lesson → no match). QUALITY 74 claims "after them `STALE_COUNT=PASS`, exit 0" and cites `corpus/evidence/round50/stale-count-after.txt`; `git log --oneline --all -- corpus/evidence/round50/stale-count-after.txt` prints nothing and `git ls-files` lists only `stale-count-before.txt` and the check. **Defect: the cited after-receipt does not exist and the criterion's check fails on the landed tree**; not repaired here (no production writes), so the draft marks `quality` `<PENDING>`.
2. `name-collision-check.py .ufo/waves/round-50/w2-spec.json` → `NAME_COLLISIONS=0 ITEMS=43`, exit 0, all names `R50`-prefixed; wave-1 `name-collision-before.txt` prints 13 `NAME_COLLISION`, exit 1. Caveat: the declared `"report"` fields of `w1-results.json` show 8 seats naming a round-49 path outright (the rest answer in prose), so the 13 rests on the check and lesson row 4, not my re-derivation.
3. Freshness: the drafted line passes `capture-age-check.py` → `FRESHNESS_CAPTURE_AGE=PASS`, exit 0 (tested in scratch and on this file). Cache `ls -l`: S104 2026-10-23, S105 2026-10-23, S106 2026-10-24, refused 教师 2026-10-24.
4. Peer flag `R50ReopenRowS105` (spans.tsv offsets −80/−48 vs quote positions): I re-derived all 55 rows — `offset + span.index(quote)` lands the quote in the capture and `capture[offset:offset+len(span)] == span_file` for **55/55, 0 bad**; the column is the span block start (CONTEXT=80, `build-spans.py` docstring 17–18, 25). The peer retracted; row S105 survives, `ANCHOR_BOUND` unaffected.
5. Census after-state and row count re-run by me: exit 0, five W04, 106 rows; `git diff 3c51da77..HEAD -- corpus/SOURCES.md` → 5 insertions, 0 deletions.

Not run by me, therefore not asserted: `c1-count.py` / `c2-count.py` at HEAD (I quote `measure-after-1.txt` verbatim and mark commit binding `<PENDING>`), any wave-2 verdict, QUALITY 73 and 75–79's own checks, and the report's final filing.

VERDICT: attacked the round-50 measurement and quality receipts — defect found: QUALITY 74's after-receipt `corpus/evidence/round50/stale-count-after.txt` is uncommitted and its check exits 1 at `c5b8dca` with `UNRESOLVED=2` (`corpus/README.md:1080`, `LOG.md:1803`), so the draft marks `quality` `<PENDING>`; the wave-2 name-collision, freshness and 55/55 span-offset checks I ran survived.
