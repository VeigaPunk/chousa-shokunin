# Citation searching — terminology, when to run it, what to report (TARCiS, round 81)

source: S203, S204
verified-at: 2026-11-06 (round 81; captures `f2489455cc311a4de981e926`, `c52a1f15884a78028febcf43`)
recheck: 365d — and at once if the version of record's erratum (BMJ 2024;387:q2458, S208, rejected unreachable) becomes readable

## What this entry governs

The lane's decision table says "Follow a citation chain" — one hop at a time, to verify a claim. That is
**chain verification**. Citation *searching* is a different act: using citation links to *find* more evidence
for a question. The TARCiS statement (Terminology, Application and Reporting of Citation Searching; Hirt et al.,
BMJ 2024;385:e078384) is a Delphi-consensus guideline for it. This entry is read from the authors' accepted
manuscript (S203), not the version of record; see *Version caveat*.

## Terms

> "Backward and forward citation searching are known as direct citation searching (Figure 1)." — S203

Backward = screen what the seed cites; forward = screen what cites the seed. Indirect methods are co-citing
(shares cited references with the seed) and co-cited (shares citing references with the seed). A Campbell methods guide uses the same split (it cites Hirt et al. 2024, so
it is not independent of S203):

> "by searching the references of identified relevant studies (backwards citation searching) or by searching for studies that cite relevant papers" — S204

and names where forward links live:

> "Citation indexes are bibliographic databases that record citations in addition to the usual article record." — S204

## Decision table

| Situation | Do | Never | Warrant |
|---|---|---|---|
| The review team judges its topic difficult to search for with database queries | seriously consider backward **and** forward citation searching as a supplement to the database search | drop citation searching without recording why | S203 recommendation 2 |
| The search must aim at completeness of recall | database search first; citation searching only as a supplement | stand-alone citation searching | S203 recommendation 9 |
| Choosing the forward-link source | combine two citation indexes when access allows | trust one index to hold every seed and every citing record | S203 recommendation 6 (S204 §4.2.2 only defines an index) |
| Results arrive from several directions and indexes | deduplicate before screening | screen the same record twice and count it twice | S203 recommendation 7 |
| A citation-searching round finds new eligible records | consider another iteration with them as seeds | stop after one pass without saying so | S203 recommendation 8 |
| Writing the methods | state seeds, directionality, dates, iterations and indexes/tools | report "references were checked" | S203 recommendation 10 |
| Citing a TARCiS recommendation's exact wording | cite the version of record and check its correction (a search snippet, recorded in `corpus/lessons/round-81.md` `## Gate`, says rec 5 was corrected) | cite the accepted-manuscript wording as final | S208 (rejected, unreachable) — lane inference |

The recommendations, located:

> "backward and forward citation searching should be seriously considered as supplementary search techniques." — S203

> "Stand-alone citation searching should not be used for literature searches that aim at completeness of recall." — S203

> "Using the combined coverage of two citation indexes for citation searching to achieve more extensive coverage should be considered if access is available." — S203

> "Before screening, the results of supplementary backward and forward citation searching should be deduplicated." — S203

> "If citation searching finds additional eligible records, another iteration of citation searching should be considered using these records as new seed references." — S203

> "the directionality of searching (backward, forward, co-cited, co-citing)," — S203

## Version caveat (observation, then inference)

Observation: S203 is the White Rose accepted manuscript (CC BY 4.0). A web search this round returned a BMJ correction,
BMJ 2024;387:q2458, whose search-result snippet (not the page) says a small error in recommendation 5 was corrected; the BMJ host answered
HTTP 403 to the lane's fetch (S208, rejected, `refetch.tsv` 2026-11-06T18:44:31Z), so its text is unread here.
Inference (not verified): the accepted manuscript's recommendation 5 wording may be the uncorrected one, which is why
this entry cites no recommendation-5 wording at all.

## Relation to existing lane knowledge

- `corpus/knowledge/citation-chain-fidelity-r24.md` — verifying one hop faithfully; this entry is about *finding*
  records through citation links, not verifying them.
- `corpus/knowledge/search-log-method-r39.md` — what a search log records; recommendation 10's items are the
  citation-searching rows such a log needs.

## Correction (round 81, after scoring)

Repaired after the wave (`R81ReviewerEntries.md` items 2–5): S204 is not independent of S203; the two-index row rests on
S203 rec 6 alone; recs 2 and 8 say "consider", not "run"; the rec-5 row names its snippet warrant. The round's claim
verdict is unchanged by this repair.
