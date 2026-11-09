# Round 96 — the search re-run tool tests itself, and search peer review and deduplication are held in their sources' words (2026-11-09)

Base `bbf64970b6c73ca64bcc5f6de2f33b0550459813` (round-95 landing + its non-author spot-check). Freeze F
`2db151c5ea0883de0b9dc8d95c6fac1755e1056a`; wave-forced re-freeze F2 (`plans/round-96.md` § Amendments). Frozen
claims: `.ufo/waves/round-96/claims.md` / `claims.json`. Two claims: C1 operability (`tools/search-rerun.py
--selftest` + gate registration, round-95 spot-check D1) and C2 depth (`corpus/knowledge/search-peer-review-dedup-r96.md`,
sourced on S223 and S224, both opened this round). Approval table for the round's GETs:
`corpus/evidence/round96/egress-approval.md`.

## Gate

Registry: two rows added, `S223` (PRESS 2015 updated guideline statement, the authors' JCHLA abstract, tier B) and
`S224` (PRISMA-S publisher PDF, re-opened under a second scope, tier A), both `mined`, `used-by:
corpus/knowledge/search-peer-review-dedup-r96.md`. No existing row's `status`, `recheck` or `used-by` cell changed.
Census exit 0 before (`corpus/evidence/round96/census-start.txt`, 221 rows) and after
(`corpus/evidence/round96/census-end.txt`, 223 rows); the after run adds one `W04` (S224 shares S222's URL across
scopes — by design, CORPUS rule 2: S222's scope cell excludes search quality and names items 8, 9, 12, 13, 15 only,
so a second scope is a second row, not an edit).

- **S223 admitted (tier B).** URL
  `https://journals.library.ualberta.ca/jchla/index.php/jchla/article/download/28195/20695/73210`, accessed
  2026-11-09 (fetched `2026-11-09T00:35:55Z`, http 200, raw sha256 `0bcdbf0e…`, txt sha256 `ce72c920…`). Located
  quote (page 98, right column, 9 words): "that peer review should occur after the MEDLINE search". Tier B, not A:
  it is the guideline authors' conference abstract summarising the 2015 update, not the guideline statement or
  its checklist. It grounds C2 rows 3 and 4 (timing, elements, translation removed) and row 5's Lane note.

GATE-RECORD S223 url=https://journals.library.ualberta.ca/jchla/index.php/jchla/article/download/28195/20695/73210 fetched=2026-11-09T00:35:55Z tier=B decision=admit capture=corpus/captures/e94691f583d644da14661ec1.txt capture_sha256=ce72c9202cca6fb24c2040b176e58de8f3ebecf9de09701855b8f96ff2f02243 words=9 quote="that peer review should occur after the MEDLINE search"

- **S223 route rejected (unreachable, not a source rejection).** The first route to PRESS material, the CADTH
  PRESS 2015 Explanation and Elaboration PDF, answered http 403 (curl rc 22) at `2026-11-09T00:35:47Z`; no bytes.
  Flip: a 200 on a later attempt (≤3 per URL) — the E&E would then be the tier-A carrier of the element wording
  this round reads from an abstract.

GATE-RECORD S223 url=https://www.cda-amc.ca/sites/default/files/pdf/CP0015_PRESS_Update_Report_2016.pdf fetched=2026-11-09T00:35:47Z tier=B decision=reject capture=none curl_rc=22 http=403 words=0 quote=none

- **The guideline statement route rejected (unreachable).** `https://www.jclinepi.com/article/S0895-4356(16)00058-5/pdf`
  answered http 403 at `2026-11-09T00:36:09Z`. Its `refetch.tsv` row carries the id `S224` because the attempt was
  logged before the registry ids were assigned; `S224` then became the PRISMA-S re-open row. No GATE-RECORD is
  written for this attempt (its tier would be checked against S224's row, a different document); the attempt is
  recorded here and in `## Mistakes` row 3. Flip: as the CADTH route.
- **S224 admitted (tier A).** URL `https://jmla.pitt.edu/ojs/jmla/article/download/962/1274`, accessed
  2026-11-09 (fetched `2026-11-09T00:43:50Z`, http 200; raw sha256 `07036f03…` and txt sha256 `86f1aacd…`, both
  equal to S222's round-95 capture, so the store is unchanged). Located quote (Table 1, item 14, 6 words):
  "Describe any search peer review process." Tier A for the scope in the row: the standard's own checklist,
  explanations and glossary, by its authors, in the journal that published it.

GATE-RECORD S224 url=https://jmla.pitt.edu/ojs/jmla/article/download/962/1274 fetched=2026-11-09T00:43:50Z tier=A decision=admit capture=corpus/captures/1a8c36c4c24444967bd9c3ce.txt capture_sha256=86f1aacd558377129dc79b8c1bc27a686ebfc668eb78a58204dea41043db3871 words=6 quote="Describe any search peer review process."

- **S222 locator (round-95 spot-check D4) — route still intermittent; external confirmation recorded, row
  unchanged.** The lane's second Europe PMC attempt (PMC7839230 full-text XML) answered http 500 at
  `2026-11-09T00:35:48Z` (`refetch.tsv`, attempt 2). The locator "Systematic Reviews 10:39" is confirmed outside
  the lane's capture store by two non-author re-opens of that URL: the round-95 closure
  (`corpus/lessons/round-95-verifier-spotcheck.md:180-183`, `<volume>10</volume>`, `<elocation-id>39</elocation-id>`)
  and this round's `R96ScribeCorrections` (third attempt http 200, same elements;
  `.ufo/waves/round-96/w1/R96ScribeCorrections-D4-locator-external-confirmation.txt`). The cell stays as committed.
- **Re-open by non-author seats.** `R96ScoutSources` re-fetched S223 and S224 into its own scratch (see its report).

`python3 -B tools/gate-records.py verify --root . corpus/lessons/round-96.md` → landing receipt
`corpus/evidence/round96/after-f2/lesson-gate.txt`.

## Mistakes

| class | evidence | captured-by | fix |
|---|---|---|---|
| a refactor of a gated tool silently disabled the previous round's battery | first draft of the C1 refactor moved `at_rev = run_at_rev(root, r, cache)` into a lambda; `rerun-controls-r95.py` printed `SETUP oracle rev-blind mutation did not apply` and `mutants-r95.py` `MUTANTS_KILLED=0/10` (`corpus/evidence/round96/prefreeze/c1-run1-transcript.txt`, P0) | none at the time (the r95 instruments were not run against a changed tool); now QUALITY 222 and the `REGRESSION_R95` leg | the line is restored verbatim in `verify`'s `at_rev_of` closure; shown able to fail: the P0 run above, then `REGRESSION_R95=2/2` (`corpus/evidence/round96/prefreeze/c1-run2.txt`) |
| a sentence-reconstruction method described as "consecutive lines" without measuring the lines | the F entry: "Consecutive fragments (… L24-L25 …) are read as one sentence from the text form's line order"; L24 is layout line 167 (right column, page 98) and L25 line 170 (left column, page 99), with the running header between (`R96ExecWrap` F2/F4, `R96ConnectorSiblings` F3, `R96CriticClaims` §Ec) | none (`gate-records.py` matches the normalized whole text; no instrument reads fragment positions) | the entry now cites the reading-order form and names both layout exceptions; QUALITY 223; shown able to fail: `R96ExecWrap-fragment-adjacency.txt` lists L24-L25 as not contiguous in either joined form |
| a Do cell dropped the agent its quote's sentence names | F row 3: "under PRESS 2015, after the MEDLINE search …"; the abstract opens the sentence "Survey respondents and forum participants recommended" (layout line 166) (`R96ReviewerC2` row 3, `R96ExecWrap` F3) | the claim's kill rule K2, through the wave's reviewer item | row 3 names the survey and forum and quotes L31; QUALITY 224; shown able to fail: `/usr/bin/grep -c -F 'Survey respondents and forum participants recommended' corpus/captures/e94691f583d644da14661ec1.txt` → 1, a line the F row's warrant (L24, L25) did not include |
| a refetch attempt filed under an id whose registry row is another document | `refetch.tsv` row `S224 https://www.jclinepi.com/article/S0895-4356(16)00058-5/pdf … 403` (the PRESS guideline statement), while `S224` is the PRISMA-S re-open; `S223` carries the CADTH E&E attempt beside the JCHLA abstract | none (`capture-fetch.py` accepts any id) | QUALITY 225 and this lesson's Gate name both attempts; shown able to fail: the QUALITY 225 command lists `S224` with two URLs of two different documents |
| a gate's self-test claimed to score "the same function" the CLI runs, with no instrument tying the two | F claim C1 sentence; a shim whose `verify` discards `evaluate`'s verdict passes `--selftest` 32/32 and every non-regression leg (`R96CriticClaims` §Aa, `R96CriticClaims-E1b-shim-noreg.txt`) | the round-95 battery inside `REGRESSION_R95` (`FORGERY_REFUSED=0/10` on the shim) | amendment A1 narrows the sentence to what is checked; shown able to fail: the shim fails `rerun-controls-r95.py` (`R96CriticClaims-E1b-r95.txt`) |
| a side-effect check whose baseline is taken after the subject has already run | `selftest-controls-r96.py` NO_WRITE snapshots `git status --porcelain` only around its own run, after the POSITIVE leg ran the self-test in the lane; a self-test that writes `tools/lane-side-effect.txt` scores `NO_WRITE=1/1` and `SELFTEST_CONTROLS=PASS` (`R96SentinelC1` F2, `R96SentinelC1-no-write-ordering-detail.txt`) | none (the leg was written by the L1 and scored by itself) | amendment A6 narrows the sentence to what the leg sees; QUALITY 226; shown able to fail: the same leg run alone on a clean clone reports the write (`before != after`, same receipt) |
| a repair kept a universal its own cited receipt contradicts | amendment B4 (F2) rewrote the fragment-group paragraph to "read as one sentence from the reading-order text form" for all groups, citing `R96ExecWrap-fragment-adjacency.txt`, which records `concat_in_reading_joined=False` for L24-L25; the paragraph also kept "30/30 measured" after B1-B2 raised the quotes to 32 (`R96ScoutSources` §3) | the wave's scout item (re-reading the entry against its own receipts) | B7 names the exception and re-cites a 32/32 measurement; re-freeze F3 `31810b4e`; shown able to fail: `R96ScoutSources-fragment-order.txt` prints `L31+L24-L25 contiguous_in_reading_order FALSE` for the F2 wording |
