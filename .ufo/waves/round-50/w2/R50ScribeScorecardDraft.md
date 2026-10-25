# R50ScribeScorecardDraft — round 50, wave 2: the round-50 verdict section for SCORECARD.md

Seat: `R50ScribeScorecardDraft` (UFO-FSD scribe, leaf; no dispatch). Lane: `chousa-shokunin`.
Freeze `6a068f2a`; W1 L1 `74794db`; tool hardening `2573dc1`; W2 spec `c5b8dca` (HEAD). Base
`3c51da77`. Read-only elsewhere; scratch `/dev/shm/chousa-r50-R50ScribeScorecardDraft/`
(`git archive 74794db` and `c5b8dca` trees, `ig-old.py` = `git show 6a068f2:tools/inference-ground.py`).
No install was needed or made; no network; no lane, fleet or campaign write. Nothing was edited
outside this file.

## 1. Shape source

`SCORECARD.md:2562-2590` read whole: the round-49 section is a lead paragraph (freeze commit,
tool→adoption commits, after-receipt, erratum, L0), a `claim / axis | before → after | counting
command | verdict | tag` table, a per-axis table for the six axes, a `Capabilities` addition, and
a `Planned — round N+1 (not started)` candidate block. `Capabilities` rows `:463-465`, `:598-601`,
`:2584-2586` confirm the four-column shape (`Capability | What it can now do | Evidence pointer |
First-working round`) and the `AXES.md` §Capabilities rule at `:467`.

## 2. Receipts re-read (not re-run unless marked RUN)

- `corpus/evidence/round50/measure-after-1.txt` — C1 `LEGS=5/5 PERTURB_PASS=6/6 C1=PASS` exit 0;
  C2 `BOUND=3/4 REFUSED=1 … QUOTE_ROWS=55 ON_BOUND=55/55 … CAPTURE_BOUND=55/55 SUBSTANCE=PASS
  ANCHOR_BOUND=3/3 INFERENCE_GROUNDED=3/3 QUARANTINE_VERDICTS=0/0 () C2=PASS` exit 0.
- `controls/c1-before.txt` — base tool `BASELINE=FAIL rc=2 PERTURB_PASS=0/6 LEGS=2/5 C1=FAIL`;
  echo control `BASELINE=PASS … LEGS=4/5`; constant control `BASELINE=FAIL rc=0 … LEGS=2/5`.
- `controls/c2-before.txt` — lane `ENTRIES=0/3 BOUND=0/4 NEW_GROUND=0/3 INFERENCE_GROUNDED=0/3`;
  staged copy `REF_ID_UNBOUND=15 BOUND=0/4`; tooled `BOUND=3/4 REF_ID_UNBOUND=8 QUOTE_ROWS=0`.
- `claims.md` (frozen predicate/kill rule/tag per claim), `claims-erratum.md` (four disclosed
  post-freeze changes), `stale-count-before.txt`, `wave-complete-before.txt`, `cited-id-before.txt`,
  `name-collision-before.txt`, `selftest-duplicates-after.txt`, `inference-regression-{before,after}.txt`.
- `corpus/QUALITY.md:750-807` (criteria 73–79), `corpus/lessons/round-50.md` (Mistakes 7 rows,
  spot-check intake, Gate decisions incl. `admit-later` for `cnki-public-surface-r43.md`).

RUN — frozen bytes unchanged since the freeze:
`git diff --stat 6a068f2a c5b8dca -- …/c1-count.py …/c2-count.py …/claims.md …/controls …/c1-fixtures`
→ no output (`diff_rc=0`); the whole round-50 dir differs only by added receipts/checks.

RUN — lane default reproduces QUALITY 73's pin:
`TMPDIR=$S python3 tools/assimilate-rows.py --selftest` → `SELFTEST=PASS findings=26 expected=26`,
`FIXTURES_SHA256=c5c56480e9f6a08d…8283cd43`, rc 0; `c1-count.py:48` `PIN = "c5c56480…"`.

RUN — two of the six new checks reproduce QUALITY 76/79:
`decode-form-check.py corpus/lessons/round-50.md` → `FORM_NAMED … DECODE_FORM=PASS` rc 0;
`… round-47.md` → `FORM_MISSING … DECODE_FORM=FAIL` rc 1.
`cjk-ground-check.py --old $S/ig-old.py` → `CASE A rc=0`, `OLD_TOOL case A rc=1 INF_UNGROUNDED`,
`CASE B rc=1 INF_TOKEN_NOT_IN_SPAN`, `CASE C rc=1 INF_UNCITED`, `CJK_GROUND=PASS` rc 0.

## 3. Findings

**F1 (defect, calibration).** `stale-count-check.py` does not pass on the round's own tree, and
QUALITY 74's cited after-receipt does not exist. RUN at the adoption commit and at HEAD:
`(cd $S/a && python3 corpus/evidence/round50/stale-count-check.py)` and the same in `$S/b` both print
`RESOLVED` ×6, `STALE corpus/README.md:1080 says 55, receipt 31`,
`STALE LOG.md:1803 says 28, receipt 31`, `STALE_HITS=8 UNRESOLVED=2 RECEIPT_ROWS=31`,
`STALE_COUNT=FAIL`, rc 1 — identical at `74794db` and `c5b8dca`. Two causes, both checkable:
`corpus/README.md:1080` is the round-50 row ("55-row manifest"), correct against the round-50
manifest and flagged because the check scans one receipt (the round-49 31-row `spans.tsv`), so the
check cannot pass once a later round writes a correct count into the same file; `LOG.md:1803`
("28 located quotes") carries no correction line (`grep -n 'correction: ' LOG.md` → only the two
unrelated prose hits at `:462`/`:508`; the `corpus/README.md:1083` line corrects README only).
QUALITY 74 states "after them `STALE_COUNT=PASS`, exit 0 (`stale-count-after.txt`)" and
`ls corpus/evidence/round50/*.txt` has no such file. So QUALITY 74's "shown able to fail" half is
receipted and its "after" half is neither receipted nor true at HEAD. Not a C1/C2 leg; both
counters are unaffected.

**F2 (observation, depth).** The C2 leg `QUARANTINE_VERDICTS=0/0 ()` is vacuous: the lesson says so
itself ("No register row names a theme URL, so there is no row to re-check and the counter's
`QUARANTINE_VERDICTS=0/0` is vacuous by construction; the record is the sweep, not a verdict").
The draft below therefore credits the sweep, not the leg.

**F3 (conflict, reported verbatim; resolved).** `R50ReopenRowS105` messaged at draft time: "spans.tsv
records every S105 quote at offsets uniformly −80 in the tail … and −48 at the head", then retracted
("spans.tsv's `offset` column is the span-block start, not the quote position"). My own check,
independent of the seat, agrees with the retraction: for the 34 S105 rows,
`int(offset) + span.find(quote)` = 48 (head row, span offset 0), then 27587, 30661, 30738, 30745,
30778, 30793, 30880, … — and `capture[off:off+len(span)] == span_file` is `True` for S105-1/2/3/5
(`span_len` 143/193/170/178). Those quote offsets are exactly the `anchor` chars of
`corpus/SOURCES.md:115` (48, 30745, 30800, 31063, 31101, 31137, 31233). No defect; the residual is
the bare column name `offset`.

**F4 (conflict of scope, reported).** `w1/CritAxisC1.md:100-120` falsifies `claims.md`'s
separability sentence ("never reads lane bytes": leg 5 runs the round-49 counter over the lane
corpus) and finds the frozen counter passes a date-hardcoding adopter (M2) and an unpinned
`renumber.tsv` `url` column (M4); it also keeps the operability score at 3/10. The draft below
follows the score and marks C1 `plumbing`, and carries M2/M4 as round-51 candidates rather than
silently closing them.

**F5 (lane state at draft time).** `wave-complete-check.py .ufo/waves/round-50/w2-spec.json
.ufo/waves/round-50/w2` → `OK 16/43 reports present`, rc 1 — wave 2 is still returning, so every
wave-2-dependent cell of the draft is marked `<AFTER>`. W1: `name-collision-before.txt` prints 13
`NAME_COLLISION` and `wave-complete-before.txt` prints `OK 29/42` — 29 + 13 = 42, i.e. the 13 absent
names are exactly the misdirected ones.

## 4. DRAFT — round-50 verdict section

Intended lane path: `chousa-shokunin/SCORECARD.md`, inserted after the round-49 `Capabilities`
addition (`:2584-2586`) and superseding the `Planned — round 50 (not started)` block (`:2588-2590`).
Fenced as Markdown; no measurement below is invented, and `<AFTER>` marks a cell whose seat or
report is still in flight.

```markdown
## Round 50 verdict — 2026-10-25 (second section-10 adoption; the CNKI 引文核对 theme adopted by document; six new checks)

Claims frozen in `corpus/evidence/round50/claims.md` at `6a068f2ae4847a1e4aa959f088a39ddc1b167bc0` after scoring do-nothing controls. C1 candidate `ec52e632`, hardened `2573dc16` (multiset comparison, work floor, option clash, `ENTRYCITES … -`, 120 s child timeout, tab-free findings, `used-by` across twin staged ids); C2 adoption `74794db0` (S104–S106, three entries, 55-quote manifest, lesson, QUALITY 73–79, gate rows); wave-2 spec `c5b8dca8`. After-measurement: `corpus/evidence/round50/measure-after-1.txt`. Post-freeze tool changes (adopter self-test hardening; `inference-ground` CJK floor) disclosed in `corpus/evidence/round50/claims-erratum.md`. No fetch; L0 `8d77e6c1` open.

Wave: W1 42 seats, 29/42 reports — the 13 absent names are exactly the round-49 name collisions, re-assigned under `R50…` names in W2 (`name-collision-before.txt`: 13 `NAME_COLLISION`). W2 43 seats, report completeness <AFTER> (`wave-complete-check.py` printed `OK 16/43` at draft time).

| claim / axis | before → after | counting command | verdict | tag |
|---|---|---|---|---|
| C1 operability (lowest scored axis, 3/10; capability extension) | `BASELINE=FAIL rc=2 PERTURB_PASS=0/6 LEGS=2/5 C1=FAIL` exit 1; echo control `BASELINE=PASS … LEGS=4/5 C1=FAIL`; constant control `LEGS=2/5 C1=FAIL` → `SELFTEST_DEFAULT=PASS BASELINE=PASS rc=0 findings=26 PERTURB_PASS=6/6 EXPECTED_BAD=PASS rc=2 R49_REGRESSION=PASS LEGS=5/5 C1=PASS` exit 0 | `python3 corpus/evidence/round50/c1-count.py` | **improved narrowly**: conformance against a hand-written expected file on a digest-pinned package (`FIXTURES_SHA256=c5c56480…`, reproduced by the lane default); the score stays 3/10 (W1 `CritAxisC1`: rerun 3/3, no axis move) | plumbing |
| C2 depth (sourced) | `ENTRIES=0/3 BOUND=0/4 NEW_GROUND=0/3 INFERENCE_GROUNDED=0/3 C2=FAIL` exit 1; staged-copy control `REF_ID_UNBOUND=15 BOUND=0/4`; tooled control `BOUND=3/4 REF_ID_UNBOUND=8 QUOTE_ROWS=0` → `BOUND=3/4 REFUSED=1 QUOTE_ROWS=55 ON_BOUND=55/55 CAPTURE_BOUND=55/55 SUBSTANCE=PASS ANCHOR_BOUND=3/3 INFERENCE_GROUNDED=3/3 C2=PASS` exit 0 | `python3 corpus/evidence/round50/c2-count.py` | **improved**: three entries on three bound rows plus one refused document, 55 located quotes each the exact capture slice at its recorded span offset; the `QUARANTINE_VERDICTS=0/0` leg is vacuous by construction (no register row names a theme URL — the lesson's sweep is the record) | ground |

The numeric operability scale remains 3/10; no other score is invented.

| axis | verdict | evidence |
|---|---|---|
| operability | **improved narrowly** | C1; `tools/assimilate-rows.py --selftest` (lane default `SELFTEST=PASS findings=26 expected=26`, digest = the counter's pin) |
| depth | **improved** | C2; three entries on four re-opened documents (3 bound, 1 refused), 55 located quotes; the counter measures binding and presence, not entailment (declared before data) |
| calibration | **improved narrowly, one check red** | QUALITY 73–79 + six checks; `decode-form-check.py` `FORM_NAMED`/`FORM_MISSING` and `cjk-ground-check.py` `CJK_GROUND=PASS` (old tool `INF_UNGROUNDED` on case A) reproduced; **`stale-count-check.py` prints `STALE_COUNT=FAIL` exit 1 at `74794db` and at HEAD** (`STALE corpus/README.md:1080 says 55, receipt 31`; `STALE LOG.md:1803 says 28, receipt 31`) and QUALITY 74's cited `stale-count-after.txt` is not on disk |
| coverage | **improved narrowly** | `NEW_GROUND=3/3`; registry 103 → 106 (S104–S106); base `3c51da7` holds no 引证检索 and only unadopted 引文核对 lines (W2 `R50ScoutCoverage`); no frontier item advanced |
| freshness | **unchanged** | newest readable capture 2026-10-24 23:26 -03; this round's captures 2026-10-23 |
| adjacency | **unchanged** | no sibling lane's `corpus/` names 引文核对 or 引证检索 (`grep -rl` over `../*/corpus/`, no match); W2 `R50ConnSiblings` <AFTER> |

## Capabilities (round-50 addition)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| self-testing package adopter (`assimilate-rows --selftest`) | runs the adopter on an isolated fixture package and compares its finding lines with a hand-written `expected.json` as multisets, printing the fixture digest the counter pins; exits 2 on an option clash, an unparseable expected file, a fixture with no entry, or a package with no `knowledge/`; 120 s child timeout; tab-free findings | `tools/assimilate-rows.py --selftest` → `SELFTEST=PASS findings=26 expected=26`, `FIXTURES_SHA256=c5c56480…`; `python3 corpus/evidence/round50/c1-count.py` → `LEGS=5/5`; controls `corpus/evidence/round50/controls/c1-before.txt` | 50 |

## Planned — round 51 (not started)

Candidates, not commitments:

1. a seventh C1 perturbation that duplicates an expected line (the multiset fix landed after the freeze, so no frozen leg carries it), plus legs varying the row's `--opened` date and its `url` column (W1 `CritAxisC1` M2/M4 pass the frozen counter).
2. make the adopter rewrite only `source:`-line ids (W1 `ExecAdopt` §2: body cross-references shift every real document by two), record `tier`/`scope` in `stripped.tsv`, and normalise a literal tab with a `cell6-tab` record as the pipe already gets (W1 `ExecSelftestEdge` f2).
3. repair QUALITY 74's check to take the receipt path (the round-49 31-row receipt flags the round's own correct 55-row row) and add `LOG.md:1803`'s correction line; file the missing `stale-count-after.txt`.
4. one home for the self-test fixtures: the lane default tree is a byte-identical copy of the pinned package at a second inode (W1 `SimplifySelftest` D1), so the default can read the pinned one.
5. adopt `cnki-public-surface-r43.md` with a re-grounded S160 row (Gate `admit-later`), and wire `name-collision-check.py` into the dispatch validator instead of a manual pre-`.ready` run.
```

## 5. Out of scope / not touched

No edit to `SCORECARD.md`, `QUALITY.md`, `LOG.md`, `SOURCES.md`, `tools/`, any counter or receipt;
no fix to F1 (the scribe records, the lane owner repairs); no C1/C2 counter rerun beyond the single
lane-default `--selftest`; no `merge/chousa` write; no campaign tool run; no wave-2 verdict for a
seat that has not returned.

VERDICT: attacked the round-50 verdict-section draft against the receipts — one defect found outside both claims (F1: `stale-count-check.py` `STALE_COUNT=FAIL` rc 1 at `74794db` and HEAD, and QUALITY 74's cited `stale-count-after.txt` absent), the peer's spans.tsv offset flag reproduced-and-refuted (F3), and both frozen claims' receipts re-read and their frozen bytes confirmed unchanged since `6a068f2a`.
