# archives-r9/controls — archive-scale negative controls (round 10)

One broken variant of an archive record per defect class — `span-not-found`,
`anchor-missing`, `dangling-ref`, `rejection-missing-flip`, `false-sweep`
(finding `SWEEP_CLAIM_FALSE`), `structure-break` — each a minimal edit of one
clean record from `corpus/fixtures/archives-r9/` with the defect isolated to
one section. Every control DRIFTs `verify-all` naming exactly its class: one
drifting section, one finding, and no other section touched (measured below).
This is a fixture-led set: **no gate change accompanies it**. The gate is the
round-8 admitted revision, sha256
`46f5ddb39d5fafa220fb584121dba2f4a15e071a91fa42728849f3c7567c6ccd`; all
numbers below were measured at that revision, from the lane root with
`--root ..`, on 2026-10-16.

## Authoring method and its asserts

Each control was generated from its clean base by scripted byte-copy plus
edits, never retyped. Generation asserts: every replacement string occurs
exactly once in its base, and every mutated value that must be absent from
the cited archive bytes (the new span, the new anchor quote) was asserted
absent from those bytes. The only diffs from the clean base are the defect
cell(s) plus the record's `## Meta` `note` row, which names the control (the
`integrity-r7-broken.md` idiom); each control's diff against its base is
enumerated in the table below. The `span-not-found` control additionally
rebinds `claims_file` to a per-control copy of `claims-r9.jsonl` that differs
in exactly one span: claims mode reads the claims surface the record binds
via its `## Meta` row, so a claim-span defect is only expressible there, and
the copy keeps the shared `claims-r9.jsonl` untouched for every other
fixture.

## Expected verdicts (and measured confirmation)

| control | class → finding id | base | defect edit (besides the note row) | expected | measured |
|---|---|---|---|---|---|
| `A-r9-span-not-found.md` (+ `A-r9-span-not-found.claims.jsonl`) | span-not-found → `CLAIM_SPAN_NOT_FOUND` | `A-r9.md` | Meta `claims_file` → the control claims copy; that copy mutates claim A07's span `keep four axes separate…` → `keep five axes separate…` (absent from archive A) | claims DRIFT; findings=1; `VERDICT_BEARING_CLAIMS=9/10`; exit 1 | as expected |
| `A-r9-anchor-missing.md` | anchor-missing → `CHAIN_ANCHOR_NOT_FOUND` | `A-r9.md` | hop 2 anchor quote `not a universal rank ladder` → `not a universal certification ladder` (absent from archive A) | chain DRIFT; findings=1; `RESOLVED_HOPS=5/7`; exit 1 | as expected |
| `B-r9-rejection-missing-flip.md` | rejection-missing-flip → `SWEEP_REJECTION_INCOMPLETE` | `B-r9.md` | R2's `flip_condition` cell emptied | sweeps DRIFT; findings=1; `REJECTIONS_OK=2/3`; exit 1 | as expected |
| `B-r9-false-sweep.md` | false-sweep → `SWEEP_CLAIM_FALSE` | `B-r9.md` | SW1's `where` cell → `research/deep-research-2026-09-28/*.md`, a glob the archive directory satisfies (3 hits) | sweeps DRIFT; findings=1; `VERIFIED_SWEEPS=0/1`; exit 1 | as expected |
| `C-r9-dangling-ref.md` | dangling-ref → `REF_UNRESOLVED` | `C-r9.md` | hop 1's `from` cell `C1` → the undeclared claim id `C9` | integrity DRIFT; findings=1; `refs=15 resolved=13 unresolved=1`; exit 1 | as expected |
| `C-r9-structure-break.md` | structure-break → `NO_QUESTION` | `C-r9.md` | the `## Question` section (heading and body) removed | structure DRIFT; findings=1; exit 1 | as expected |

In all six runs the other four sections are CLEAN and the composed line reads
`VERIFY_ALL sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1`, so
each control's drift names exactly its class and nothing else drifted.

## Measured outputs (verbatim, one run per control)

### A-r9-span-not-found

```text
research-gate research-gate-r1 — ts=2026-10-16T05:40:48Z — mode=verify-all — record=corpus/fixtures/archives-r9/controls/A-r9-span-not-found.md — claims=/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/fixtures/archives-r9/controls/A-r9-span-not-found.claims.jsonl — root=..
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=run verdict=DRIFT findings=1 drift=1 tally=VERDICT_BEARING_CLAIMS=9/10
FINDING CLAIM_SPAN_NOT_FOUND severity=warn surface=claims obs=id=A07 nearest_line=35 context=Deep research: The shokunin (職人) concept in Japanese artisan tradition — a
SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=6/7
SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=1/1 REJECTIONS_OK=4/4
SECTION integrity state=run verdict=CLEAN findings=0 drift=0 tally=INTEGRITY refs=13 resolved=12 unresolved=0
VERIFY_ALL sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1
RESEARCH_GATE: DRIFT (sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1)
```

### A-r9-anchor-missing

```text
research-gate research-gate-r1 — ts=2026-10-16T05:40:57Z — mode=verify-all — record=corpus/fixtures/archives-r9/controls/A-r9-anchor-missing.md — claims=/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/fixtures/claims-r9.jsonl — root=..
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=10/10
SECTION chain state=run verdict=DRIFT findings=1 drift=1 tally=RESOLVED_HOPS=5/7
FINDING CHAIN_ANCHOR_NOT_FOUND severity=warn surface=chain obs=hop=2 source=research/deep-research-2026-09-28/A-shokunin-tradition.md anchor=quote:"The sources point to craft-specific apprenticeship systems, " nearest_line=47 context=The sources point to craft-specific apprenticeship systems, not a universal rank
SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=1/1 REJECTIONS_OK=4/4
SECTION integrity state=run verdict=CLEAN findings=0 drift=0 tally=INTEGRITY refs=13 resolved=12 unresolved=0
VERIFY_ALL sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1
RESEARCH_GATE: DRIFT (sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1)
```

### B-r9-rejection-missing-flip

```text
research-gate research-gate-r1 — ts=2026-10-16T05:41:08Z — mode=verify-all — record=corpus/fixtures/archives-r9/controls/B-r9-rejection-missing-flip.md — claims=/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/fixtures/claims-r9.jsonl — root=..
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=10/10
SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=6/7
SECTION sweeps state=run verdict=DRIFT findings=1 drift=1 tally=VERIFIED_SWEEPS=1/1 REJECTIONS_OK=2/3
FINDING SWEEP_REJECTION_INCOMPLETE severity=warn surface=sweeps obs=id=R2 missing=flip
SECTION integrity state=run verdict=CLEAN findings=0 drift=0 tally=INTEGRITY refs=14 resolved=13 unresolved=0
VERIFY_ALL sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1
RESEARCH_GATE: DRIFT (sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1)
```

### B-r9-false-sweep

```text
research-gate research-gate-r1 — ts=2026-10-16T05:41:19Z — mode=verify-all — record=corpus/fixtures/archives-r9/controls/B-r9-false-sweep.md — claims=/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/fixtures/claims-r9.jsonl — root=..
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=10/10
SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=6/7
SECTION sweeps state=run verdict=DRIFT findings=1 drift=1 tally=VERIFIED_SWEEPS=0/1 REJECTIONS_OK=3/3
FINDING SWEEP_CLAIM_FALSE severity=warn surface=sweeps obs=id=SW1 where=research/deep-research-2026-09-28/*.md hits=3 first=research/deep-research-2026-09-28/A-shokunin-tradition.md listed=research/deep-research-2026-09-28/A-shokunin-tradition.md research/deep-research-2026-09-28/B-multiagent-knowledge.md research/deep-research-2026-09-28/C-rank-taxonomy.md
SECTION integrity state=run verdict=CLEAN findings=0 drift=0 tally=INTEGRITY refs=14 resolved=13 unresolved=0
VERIFY_ALL sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1
RESEARCH_GATE: DRIFT (sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1)
```

### C-r9-dangling-ref

```text
research-gate research-gate-r1 — ts=2026-10-16T05:41:30Z — mode=verify-all — record=corpus/fixtures/archives-r9/controls/C-r9-dangling-ref.md — claims=/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/fixtures/claims-r9.jsonl — root=..
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=10/10
SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=7/8
SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=1/1 REJECTIONS_OK=4/4
SECTION integrity state=run verdict=DRIFT findings=1 drift=1 tally=INTEGRITY refs=15 resolved=13 unresolved=1
FINDING REF_UNRESOLVED severity=warn surface=integrity obs=kind=claim id=C9 section=chain row=1 cell=from
VERIFY_ALL sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1
RESEARCH_GATE: DRIFT (sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1)
```

### C-r9-structure-break

```text
research-gate research-gate-r1 — ts=2026-10-16T05:41:42Z — mode=verify-all — record=corpus/fixtures/archives-r9/controls/C-r9-structure-break.md — claims=/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/fixtures/claims-r9.jsonl — root=..
SECTION structure state=run verdict=DRIFT findings=1 drift=1
FINDING NO_QUESTION severity=crit surface=question obs=missing ## Question section
SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=10/10
SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=7/8
SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=1/1 REJECTIONS_OK=4/4
SECTION integrity state=run verdict=CLEAN findings=0 drift=0 tally=INTEGRITY refs=15 resolved=14 unresolved=0
VERIFY_ALL sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1
RESEARCH_GATE: DRIFT (sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1)
```

## Clean bases still CLEAN (same gate revision, same run window)

```text
A-r9.md  exit=0
VERIFY_ALL sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0
RESEARCH_GATE: CLEAN (sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0)
B-r9.md  exit=0
VERIFY_ALL sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0
RESEARCH_GATE: CLEAN (sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0)
C-r9.md  exit=0
VERIFY_ALL sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0
RESEARCH_GATE: CLEAN (sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0)
```

Full clean-base outputs are in `archives-r9/README.md`.

## Why structure-break is `NO_QUESTION`, not `RECORD_SCHEMA_INVALID`

A measured probe (a scratch record carrying no Meta/Sources/Claims sections
and no banner, run through `verify` on 2026-10-16) showed
`RECORD_SCHEMA_INVALID` cannot fire alone: it drags `SOURCE_TABLE_ABSENT`,
`CLAIM_TABLE_ABSENT` and `REJECTION_DROPPED` into the same run (4 findings,
exit 1) — not an isolated class. Removing the `## Question` section is the
smallest edit that isolates exactly one structure finding, so the control
uses `NO_QUESTION` (severity crit) as its structure class.

## Pins

| file | sha256 |
|---|---|
| `A-r9-span-not-found.md` | `5dedb73b4828f8120b1d7538aea49711dc56b2776bc9490e29727979ff4d7671` |
| `A-r9-span-not-found.claims.jsonl` | `0edb78ee0040bd77af6b1618ca9888f6676eb8082e9aabb9b4c498016664b126` |
| `A-r9-anchor-missing.md` | `e3490cf4bc9dd778311c19949287be93dd2b17690e1bb7f2d1cf77c38d7e82a0` |
| `B-r9-rejection-missing-flip.md` | `b0d488aae5fbfe5aef6b9eaa5f5cf45ba7381abebf1fc51f77af92509b5a0206` |
| `B-r9-false-sweep.md` | `69b7b08f8b1d3362b7848fe6776fd237226a645589c767c9d5cfe11abad85a47` |
| `C-r9-dangling-ref.md` | `b24be0f0768d6b6848b9fa13fe6f862464007322ae52653b42ef0fac09f986f7` |
| `C-r9-structure-break.md` | `21d77e6c4de99719c557d14b105d2b795147f40bc724f4105d041587107c290c` |

Bases at authoring: `A-r9.md`
`338918fcb8ed5d6c5f15dc64e5eb8a3ae7a005d51b5c03e7e377c1dab9173c78` (the pre-fix
revision; round 12 corrected A-r9 row C3's pointer `:76`→`:86`, moving the live
record to `dfd2ae1a…` — these controls stay byte-copies of the pre-fix base,
and their `:76` C3 cell is outside every gate check; the desync from the
current record is exactly that one cell),
`B-r9.md` `abfa5290deda4d1708ba97028853b8a770f16ecda6f377dddda53d49cb2e3e86`,
`C-r9.md` `97be0e69ccfb8a701bc5556f738553be8e7179c9b41110fe61c4a3cab4f2d1da`;
shared claims surface `claims-r9.jsonl`
`f6f0d1ab6b6cbd045035951c7eb4653406dc0853234a8077a8685509bfc94ff5`;
gate `46f5ddb39d5fafa220fb584121dba2f4a15e071a91fa42728849f3c7567c6ccd`.

## Re-run recipe

```sh
cd chousa-shokunin
for c in A-r9-span-not-found A-r9-anchor-missing B-r9-rejection-missing-flip \
         B-r9-false-sweep C-r9-dangling-ref C-r9-structure-break; do
  bash tools/research-gate.sh verify-all corpus/fixtures/archives-r9/controls/$c.md \
    --root .. ; echo "exit=$?"
done
```

Expected at the pins above: every run DRIFTs with `drift-sections=1
findings=1` and exactly the class's finding id, exit 1. These runs pass no
`--json`, so they write no manifest lines. The false-sweep control's `hits=`
and `listed=` values reflect the archive directory at run time (3 hits
measured); the class and the finding id are directory-independent.

## What this set does not cover (named)

- Multi-defect interaction inside one record: each control isolates one class
  by construction.
- Out-of-corpus / URL / session refusals at archive scale: the small r2/r3
  fixtures own those refusal classes; these controls stay in-corpus.
- Semantic drift inside stable fields: the set catches id/verdict-level
  defects; the r8 note (`gate-baseline-r8.md`) owns that cannot-catch.
- Coverage fraction: six controls are one existence proof per class, not a
  measured fraction of defect space.