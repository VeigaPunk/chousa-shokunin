# CritC3Inference — do the two C3 entries state more than their captures support

Seat: critic (leaf). Attack every Inference bullet of the two C3 entries, the Observation bullets
carrying frozen questions (1)/(2), and any figure not verbatim in a capture. No fetch, no production
writes, no counter edits. Read: `claims.md` (`c2f0e9d`), both lane drafts, `spans.tsv`,
`SOURCES.md` S070–S084, `corpus/lessons/round-45.md` `## Gate`, five captures under
`…/corpus-expansion-1/.qcache/`. The scribe reports were still running
(`agent://L1Chousa46.ScribeEntry{Base,Amend}` empty), so this attacks the **lane drafts as they stand**.

## Evidence I ran

1. Span manifest, all four legs per row (capture sha256 == recorded; `capture[off:off+len]` == quote;
   span file == quote; quote ∈ citing entry) — my own script, not `c3-count.py`, hardened mid-run
   (path-traversal and int guards only; no leg weakened):

```
OK S085 2360 | OK S085 1271 | OK S086 15269 | OK S086 42011 | OK S086 20847 | OK S087 171
OK S087 4929 | OK S088 3929 | OK S088 2904 | OK S089 3022 | OK S089 7137   SPAN_ROWS_OK=11/11
```

First run used default CSV quoting and mis-killed the two S087 rows (my reader artifact, retracted).
**No span-leg defect.**

2. `revision` in the two captures frozen question (1) names: `5a631adb…txt` (S085 FEVER page) **0**;
   `7800e2e1…txt` (S087 Zenodo) **1** → `'"recid": "4925954", "revision": 2, "files": ['` @3667.
   `metadata` has no `version` key; `swh` is `{}`; `conceptdoi` @171.

3. Every quoted fragment tested as a substring; all 11 span fragments hit at their offset. **ABSENT
   from S086** (two-column PDF interleaves lines): `We used the June 2017 Wikipedia dump`, `91.2% of
   the examples were annotated correctly`, `all except two annotators achieved > 90% precision`,
   `in 31.75% of the claims more than one sentence was considered appropriate evidence`, `Claims
   require composition of evidence from multiple sentences in 16.82% of cases`, `Furthermore, in
   12.15% of the claims, this evidence was taken from multiple pages`. **ABSENT from S089**:
   `limited … published before the claim's date`. The drafts already demoted each of these.

4. Cross-corpus probe: `S088 (AVeriTeC page): 'temporal' 0, 'before the claim' 0, 'archive' 16`;
   `S089 (AVerImaTeC paper): 'web.archive' 0, 'cached' 0, 'cached_source_url' 0, 'temporal' 12`;
   `S089:14603` "To ensure long-term accessibility, all source pages are archived on the internet archive."

5. AVeriTeC examples (S088): `claim_date 25-8-2020` @4369 with capture `web/20230323135844/…Hunter_Biden`
   @5264; a `source_url` of `treasury.gov/…/WP81-Table2013.pdf` @7611 whose cached link is
   `https://home.treasury.gov/` @7760; `"Unanswerable"` + `"source_url": ""` with **no**
   `cached_source_url` key @9390.

## `corpus/knowledge/evidence-pool-versioning-r39.md`

- O1 binding = URL + sentence id — **holds** (tuple @2360; the dropped "and nothing else" was the overreach).
- O2 "the word 'revision' does not appear in the data-format section" — **holds narrowed**: true of
  S085 (0 hits), but S087 carries `"revision": 2` @3667, the only revision token in the opened set.
- O3 deposit versioned as an artefact — **holds** (`conceptdoi` @171, `wiki-pages.zip` @4929).
- O4 measured reliability — **holds**: 72.36 % @42011 and 91.2 % @20847 exact; 95.42 / 0.6841 / 31.75
  / 16.82 / 12.15 / 227 all present at 6741, 1869, 5534, 5842, 5929, 20637 and declared pointers.
- I1 "Durability comes from freezing the pool, not from stamping each citation" — **holds narrowed**:
  the mechanism is in the captures; the *ranking* is stated by neither, so add "no source opened here
  ranks the two; the attribution is this lane's".
- I2 different instrument from the lane pin — **holds**. I3 weaker link — **holds** (recall is stated
  against super-annotators, 42011/42123). I4 RFC 7089 (S079) + NDL/WARP (S081) — **holds**, re-bound
  by document. U2, U3 — **hold**.
- **U1 "The deposit versions the artefact, not the Wikipedia pages inside it" — FAILS,
  self-contradiction.** I1/O3 say the deposit fixes the pool as a file; the files array @4929 holds
  `wiki-pages.zip`, 1,713,485,474 bytes, `md5:ed8bfd894a2c47045dca61f0c8dc4c07`.

**U1 replacement:**
> **Whether the deposited pool is the pool the annotators read is not stated.** The deposit's
> `wiki-pages.zip` carries its own size and md5 (`ed8bfd894a2c47045dca61f0c8dc4c07`), so the deposited
> state is fixed; no source opened here says that archive is byte-identical to the pages the
> annotators labelled, so an upstream edit is excluded only if that identity holds.

## `…-amendment-2026-10-23.md`

- **O1 "Every evidence answer pairs a live URL with an archived copy" — FAILS, universal clause.**
  S088's Not Enough Evidence example has an answer with `"source_url": ""` and no `cached_source_url`
  key (@9390); one cached link points at a different path (@7760 vs @7611); lane row S084 counts
  **1,491 of 7,572** source-naming answers with no archive field.
- O2 claim-level archive conditional — **holds** (`Where possible` @3185 attaches to
  `cached_original_claim_url` only; matches S082). O3 claim_date — **holds** (@2904).
- O4 four labels — **holds narrowed**: intro @1142 spells `Cherry-picking`, the record `label` values
  spell `Cherrypicking` (2 hits), yet the token is backticked as if literal.
- **O5 "the restriction is operational in the pipeline" — holds narrowed**: true (@20128 "All
  retrieved pages from the interface are restricted to dates prior to the claim date"), but the paper
  states its leaks @42300 — "the exact dates of a small portion of claims ( **5%** ) were unavailable …
  we relied on Google Search and … htmldate.find_date to estimate publication dates … coarse approximations."
- I1 — **holds narrowed**: drop "of the cited page" (the field records a link, not a verified capture
  of that URL). I3 same instrument — **holds**. I4 — **holds narrowed** (spelling split; "the lane's
  chain mode has never had" needs a pointer). U2, U3 — **hold**.
- **I2 "that date is what makes the archive meaningful … the constraint the pipeline enforces" —
  FAILS, cross-corpus splice.** `claim_date` is AVeriTeC (S088: 0 hits "temporal"/"before the claim");
  the date rule is AVerImaTeC (S089). S088 pairs 2020 claims with **2023** captures, so the archive is
  the annotation-time state, not the claim-time state.
- **U1 "how large that share is was not measured" — FAILS as an unknown**: S084 counts 1,145 of 2,531
  claim fields filled and 1,491 of 7,572 answers with no archive field.
- Missed warrant (strengthening, not a fail): S089 @14603 says the archiving directly — "To ensure
  long-term accessibility, all source pages are archived on the internet archive" — but the amendment's
  `source:` line lists only 3022 / 3204 / 3239 / 7137, so Q14 for the newer corpus is answered by
  splicing another corpus's field description.

**O1 replacement:**
> **An evidence answer carries `source_url` and a `cached_source_url` described as "An archive.org
> link for the source url".** The examples show a live Wikipedia URL beside a `web.archive.org`
> capture, and also an answer with an empty `source_url` and no archive field, and a cached link
> whose path differs from its `source_url`; this lane's S084 count finds 1,491 of 7,572 source-naming
> answers with no archive field.

**I2 replacement:**
> **The corpus dates the claim, and the date constrains which pages may be used as evidence.** In
> AVerImaTeC evidence is `published before the claim’s date` (`S089`); in AVeriTeC the archive field
> records the page's state at annotation time — the examples pair 2020 claims with 2023 captures — so
> the archive fixes what the annotator read, not what was published.

**U1 replacement:**
> **The archive fields are unevenly filled, and the reason is unstated here.** S084 counts 1,145 of
> 2,531 claim archive fields filled and 1,491 of 7,572 answers with no archive field; this page does
> not say why the rest are empty.

## Frozen-question answers

1. FEVER page: nothing about revisions (0 hits). Zenodo: exactly one — `"revision": 2`, a *deposit*
   revision. The negative half ("no per-citation stamp") is supported; the causal half ("durability
   comes from freezing") is stated by no source. Main I1 holds narrowed; O2 must name the token.
2. Per citation: yes. Best-effort *by the dictionary*: **no** — "Where possible" is on
   `cached_original_claim_url` only. Best-effort *by the data*: yes, and worse than the draft says.
   S089 says the constraint **is** operational, and states its 5 % fallback and `htmldate` in-paper.
3. No unsupported figure survives: every number resolves at a stated offset (72.36 / 91.2 / 95.42 /
   0.6841 / 31.75 / 16.82 / 12.15 / 227 / 0.742 / 74.7 / four labels); every staged string with no
   verbatim basis is absent, and the "Staged material corrected on adoption" bullets are accurate.

## Impacted axes

- **depth (C3)** — entry content only; the four FAILS are the class the frozen kill rule already
  covers ("A staged sentence that the captures contradict is corrected in the entry and recorded as a
  mistake"), so no predicate, counter, fixture or target change is proposed.
- **operability (C1)** / **calibration (C2)** — untouched, no harm.
- **C3 counter sufficiency** — all 11 span legs pass while three bullets overstate, because the counter
  measures presence, not entailment: the D7 blind spot reproduced one level up, at entry level.

## Smallest safe correction

Apply the four replacements as text. **Do not touch the 11 quote strings** — that invalidates a
`spans.tsv` row. All four narrowings sit outside the quotes, so `SPAN_ROWS_OK` stays 11/11 and
`--lane-only` is unaffected. Zero-risk additions: `"revision": 2` @3667 into main O2/O3, char 14603
into the S089 anchors.

## Pointers

- `…/.qcache/7800e2e1e2df3bc124b6b83e.txt:3667` `"revision": 2`; `…/b73f7e8dd5b0ace740e48046.txt:9390`
  unanswerable answer; `:7760` vs `:7611` cached link ≠ `source_url`; `:3185` `Where possible`;
  `:1142` `Cherry-picking`; `…/78761b633aee2289e5874ce9.txt:14603` archiving, `:20128` date
  restriction, `:7137`, `:42300` 5 % / `htmldate`
- `corpus/SOURCES.md:92` S082 "evidence-level archive without condition"; `:94` S084 counts;
  `corpus/knowledge/evidence-pool-versioning-r39.md:24` U1; `…-amendment-2026-10-23.md:11,20,26` O1, I2, U1

Verdict: **no counter or claim falsified; four entry sentences must be narrowed before adoption.**
The current text carries a universal ("Every") the lane's own S084 row refutes, and a self-
contradiction between main I1 and U1.
