# CritCoverageGround — round 45 wave 2

Seat: L1Chousa45.CritCoverageGround. Item: the claim that the two adopted entries
(`corpus/knowledge/evidence-archive-field-policy-r41.md`,
`corpus/knowledge/evidence-snapshot-coverage-r40.md`, C3 rows S082–S084) are ground the
lane did not hold at `5e8c7ad2f7b8254d83358820286e3d12ca4672d1`. No fetch, no lane writes.

## Method (all committed bytes at 5e8c7ad)

```
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 5e8c7ad... | tar -x -C /tmp/chousa-r45-CritCoverageGround/tree
grep -rn --include='*.md' -iE 'AVeriTeC|FEVER' corpus/ | grep -viE 'evidence-archive-field-policy-r41|evidence-snapshot-coverage-r40'
grep -rn -iE 'cached_source_url|cached_original_claim_url|web\.archive\.org|archive\.org|wayback|warp\.ndl|archive\.ph|perma\.cc|archive\.vn|archive\.is|archive\.md' corpus/ | grep -vE 'evidence/round45|...-r41|...-r40|lessons/round-45'
cd tree && python3 corpus/evidence/round45/c3-count.py; python3 corpus/evidence/round45/c3-count.py --lane-only
```

Decisive counter output (verbatim):

```
ENTRIES=2/2  CITES_BOUND=3/3  QUOTES_IN_SPAN=4/4  QUOTES_IN_ENTRY=4/4
COUNTS_IN_ENTRY=7/7  CAPTURE_BOUND=4/4  COUNTS_REDERIVED=7/7  C3=PASS  EXIT=0
--lane-only: same first five, CAPTURE_BOUND/COUNTS_REDERIVED=skipped, C3=PASS, EXIT=0
```

## Prior held ground audited (the listed suspects)

- `citation-version-binding-r36.md` (round 44): RFC 7089 (S079) Memento-Datetime promise,
  archive-veracity out of scope, span check checks the capture not the origin. Object:
  **protocol-level archival semantics**. No corpus, no field dictionary, no AVeriTeC.
- `citation-version-binding-r37.md` (round 44): NDL WARP cadence (S080) and URL-embedded
  capture timestamp (S081). Object: one national archiver's mechanism. No corpus.
- `revision-binding-r31.md` (round 31): SHA-256 content pin of a claim's source bytes —
  a gate/plumbing mechanism (S058/S059), not corpus archive-field coverage.
- `claim-verification-r2.md` (round 2): `verify-claims` mode; URL sources refused
  unopened, fail-closed, verbatim span = support only. A gate limit, not corpus archive fields.
- `claim-support-states-r24.md` / `citation-chain-fidelity-r24.md`: support-vs-truth,
  hop-fidelity method. No archive-field object.
- AVeriTeC before round 45 appears ONLY as an unopened lead (`corpus/SOURCES.md:266`,
  "Leads (unopened)"); FEVER: zero occurrences anywhere in `corpus/` (grep: no match).

## Verdict: HOLDS (narrowed)

No prior held ground covers the object class of the two entries — a verification corpus's
archive **fields and values** (AVeriTeC `cached_source_url` / `cached_original_claim_url`,
train.json). The entries are new ground: first AVeriTeC sources (S082–S084), first
corpus-field archive semantics, first value-counted snapshot coverage (5,959/7,572
web.archive.org over real-source answers; 1,145/2,531 claim fields filled; 1,582 sourced
answers with no archive key). Committed artifacts independently verify the claims:
spans `evidence/round45/spans/{S082-1,S082-2,S083-1,S083-2}.txt`, `counts.json`,
spans.tsv, capture-bound via `C3=PASS` in both counter modes.

Narrowing (lineage, not duplication): the inference half of
`evidence-archive-field-policy-r41.md` ("a filled archive field is a link to open, not
proof of a resolving capture") inherits the held r36 limit (check the capture, not origin
output; archive veracity out of scope) applied to a new object. The intersection
double-archived-404 observation (S083 Appendix J.4.1) is new. Nothing in r2/r3/r31/r36/r37
held the corpus-field or count claims, so no substantive duplication.

## Do the two new coverage-map rows overstate?

No. The rows (`corpus/README.md` lines 1063–1064) restate only facts the notes hold and
the C3 counter re-derives; they assert no novelty/absoluteness and no resolving capture.
Minor cosmetic tokens: filenames carry r40/r41 while rows label the notes Round-45 (the
files self-declare the names are package labels, not round numbers); the r37 README row
already exists with the same convention. No correction needed.

## Pointers

- `corpus/README.md:1063` / `:1064` — the two new coverage-map rows (no overstatement).
- `corpus/SOURCES.md:92,94` — S082/S084 rows; `:266` — AVeriTeC only unopened lead before.
- `corpus/knowledge/citation-version-binding-r36.md:10-18` — held Memento limit (lineage).
- `corpus/knowledge/revision-binding-r31.md:7-13` — gate pin, unrelated object.
- `corpus/evidence/round45/c3-count.py` — both modes PASS at the commit.
- sha256 of train.json capture `ae5eda7c42ddf1695ef185a7ba1bc716928f5adf57103e4f78aae5f9afe00f9c`.
