# Round 46 — frozen claims (chousa)

author: chousa L1 (omp in-session L1, hyaku run 6)
date: 2026-10-25
base: `6e2630a6343948b3fe5bf299901207a0619ad949` (round-45 landing, plus its
verifier spot-check `6e2630a`… tree)
freeze: this commit (claims + the three counters + their controls; no claim
work is in it)

No external fetch: the fetch-scope L0 `8d77e6c1` is still open. Every capture
this round reads is on disk (campaign capture cache
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`, file =
`sha256(url)[:24].txt`, plus the lane's committed spans).
Round tag (QUALITY 64): C1 plumbing, C2 plumbing, C3 ground.

Three claims, three axes, each verifiable without the others. C1 works the
lowest non-retired axis (operability, 3/10 — `SCORECARD.md:7`; the stagnation
nudge is dormant, `SCORECARD.md:492`). C1 and C2 are routed defects from the
round-45 closure (D7, D8); C3 is the round-45 plan's narrower AVeriTeC
entry plus the flip condition on the round-45 reject.

## R46-C1 — operability — inference grounding becomes an executable check

The round-45 wave-2 critic `CritC3Axis` demonstrated that
`corpus/evidence/round45/c3-count.py` checks that quotes and counts are
*present* in an entry: two junk entry bodies reusing the committed spans and
counts pass both of its modes. The lane's SKILL checklist item "Observation,
inference and unknown stay separate" was prose only. This claim makes it
runnable.

Predicate (one sentence, no universal clause): `tools/inference-ground.py`
exists and, run by `python3 corpus/evidence/round46/c1-count.py`, exits 0 on
each of the three `positive-*.md` fixtures and exits 1 on each of the three
`junk-*.md` fixtures of `corpus/fixtures/inference-ground-r46/` — the junk
classes being (a) an uncited bullet, (b) a cited bullet whose grounding token
is absent from the cited span, and (c) a body that reuses the correct spans
and figures while its inference asserts something else (the D7 class).

* Counting command: `python3 corpus/evidence/round46/c1-count.py`
* Before (`controls/c1-before.txt`, base tree, tool absent):
  `TOOL=absent POSITIVE_PASS=0/3 JUNK_KILLED=0/3 C1=FAIL` exit 1.
* Target: `POSITIVE_PASS=3/3 JUNK_KILLED=3/3 TOOL=present C1=PASS` exit 0.
* Controls (`controls/c1-controls.txt`): an always-exit-0 tool scores
  `POSITIVE_PASS=3/3 JUNK_KILLED=0/3` (exit 1); a citation-presence-only tool
  scores `POSITIVE_PASS=3/3 JUNK_KILLED=1/3` (exit 1).
* Kill rule: any run of the counter below `1/3` on either leg, or a fixture
  set changed after this freeze, fails the claim as declared.
* Tag: plumbing. Capability row: "inference grounding check".

## R46-C2 — calibration — the registry covers verifiers outside the name pattern

Round-45 closure D8 / wave-2 `CritC2Framing`: the frozen entry-point pattern
(`tools/*`, `corpus/evidence/round*/{c<N>-count*,verify-receipts,errata-count}.py`)
misses executable evidence verifiers the lane's own verdicts name as counting
commands — `corpus/evidence/round34/self-audit.py` is the named example. This
claim makes the registry agree with the tree the verdicts rest on, without
weakening the existing legs.

Predicate: `python3 corpus/evidence/round46/c2-count.py` prints
`UNREGISTERED=0` and `C2=PASS` (exit 0) over a set of entry points that is the
union of (A) every file directly under `tools/`, (B) the round-45 pattern
(unchanged), and (C) every existing repo-relative `*.py`/`*.sh` path named in
`SCORECARD.md` or a `corpus/evidence/round*/claims*.md`.

* Counting command: `python3 corpus/evidence/round46/c2-count.py --list`
* Before (`controls/c2-before.txt`): `ENTRY_POINTS=71 (tools=7 counters=50
  named=66) GATES_ROWS=30 REGISTERED=55/71 UNREGISTERED=16` exit 1.
* Target: `UNREGISTERED=0 C2=PASS` exit 0, with `ENTRY_POINTS` ≥ 71.
* Controls (`controls/c2-controls.txt`): paths pasted as prose in the Gates
  section, a six-cell row, an eight-pipe row without `exit`, and a valid row
  after the next `## ` heading all stay unregistered.
* Kill rule: `UNREGISTERED>0`, or an `ENTRY_POINTS` below 71, fails the claim
  as declared. Row truth is not measured — that is the named limit.
* Tag: plumbing.

## R46-C3 — depth — the evidence-pool versioning theme, re-grounded

Theme (assimilation §10, one theme): what makes a support verdict durable, and
how a later corpus binds each citation to an archived state. Staged package:
`/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/`
`evidence-pool-versioning-r39.md` (staged S120–S122) and
`evidence-pool-versioning-r39-amendment-2026-10-23.md` (staged S127, S128),
which round 45 rejected with a flip condition
(`corpus/lessons/round-45.md` `## Gate`). Both entries are adopted only if
every cited source is re-opened this round from the on-disk captures, every
prose id is re-bound **by document**, and the staged prose is corrected where
the captures disagree with it.

Predicate: `corpus/knowledge/evidence-pool-versioning-r39.md` and
`corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md` exist;
their five `source:` lines bind lane ids S085–S089 to the five URLs; each
Registry row is `mined` with the citing entry in `used-by`; the eleven rows of
`corpus/evidence/round46/spans.tsv` each carry their quote in the committed
span file and in the citing entry, and each span file is the exact slice of the
capture named `sha256(url)[:24].txt` at the recorded offset whose sha256 is the
recorded one; every `S###` token in either entry is a source id or one of the
lane's held rows S079–S084; and the two cross-references bind by document
(the S079 sentence names RFC 7089, the S081 sentence names WARP).

* Counting command: `python3 corpus/evidence/round46/c3-count.py`
  (and `--lane-only`)
* Before (`controls/c3-before.txt`): `ENTRIES=0/2 CITES_BOUND=0/5
  QUOTE_ROWS=0/11 C3=FAIL` exit 1.
* Target: `ENTRIES=2/2 CITES_BOUND=5/5 QUOTE_ROWS=11/11 QUOTES_IN_SPAN=11/11
  QUOTES_IN_ENTRY=11/11 CAPTURE_BOUND=11/11 REF_ID_UNBOUND=0 REF_BOUND=2/2
  C3=PASS` exit 0 in the default mode, and the same with
  `CAPTURE_BOUND=skipped` under `--lane-only`.
* Control (`controls/c3-controls.txt`): entries plus a self-consistent span
  manifest with invented capture digests pass `--lane-only` (the round-44 D1
  blind spot, named) and are refused by the default mode
  (`CAPTURE_BOUND=0/11`, exit 1).
* Kill rule: any leg below its target in either mode fails the claim as
  declared. A staged sentence that the captures contradict is corrected in the
  entry and recorded as a mistake; it is never silently carried.
* Tag: ground.

## Admission rule

Each claim is judged on the counter, kill rule and predicate declared here. A
rule changed after any seat has scored is not this claim's rule. A round is
admitted only when every claim verifies and no axis is harmed; every verdict is
reported.
