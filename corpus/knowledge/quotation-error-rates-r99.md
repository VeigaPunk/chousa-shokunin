# Quotation errors — how often a cited source fails the citing sentence, and how the rate is counted (round 99)

source: S236, S233
verified-at: 2026-11-09 (round 99; capture `405a0054e1f6dbd1854a3618` — Europe PMC's core record for PMID 26528420, Jergas H, Baethge C, "Quotation accuracy in medical journal articles—a systematic review and meta-analysis", PeerJ 2015;3:e1364, carrying the authors' own published abstract, opened as S236 — and capture `4b70901ad80c513f0c2f750c`, the publisher's page of Mogull SA, "Accuracy of cited 'facts' in medical research articles: A review of study methodology and recalculation of quotation error rate", PLoS One 2017;12(9):e0184727, opened as S233)
recheck: on-release

## What this entry governs

chousa's province owns claim-vs-source verification (`PROVINCE.md`). The lane's tools check that a quote is
*located* in its source (`tools/gate-records.py`, QUOTE_ABSENT); no entry held what is known about how often a cited
source does not *support* the sentence that cites it. Before this round no capture and no knowledge entry contained
the phrase "quotation error" (`## Searches` Q1-Q4, 0 hits at the round-98 landing). This entry holds two
quantitative syntheses of that literature, the two whose text this round's GETs returned (amended at F3, B3 — it said
"the two … that this host could read", which `R99ScoutSources` showed false):

1. **Jergas & Baethge 2015 (S236, tier B).** A systematic review, meta-analysis and meta-regression of quotation
   errors in medical journal articles, read through its own published abstract in Europe PMC's index record (the
   publisher page answered http 403, S232; Europe PMC's full-text route answered http 500, S235). Eight quotes from the
   abstract (J1-J8) and the record's title (J0).
2. **Mogull 2017 (S233, tier A).** A review that re-derived the rate from the same literature's raw counts with one
   definition of an error and one denominator; read on the publisher's page (full text). Fourteen quotes (G0-G13).

A third synthesis, the authors' 2025 update (Research Integrity and Peer Review), answered the lane's publisher GET with
an http 200 whose body is a "Client Challenge" page (S234); it is rejected for route and nothing here rests on it. Its
Europe PMC record (pmid 40696441) answered a wave seat's read-only re-open with http 200 (`R99ScoutSources`); the lane
did not GET it this round, so it is not held here.

The column marked *lane* is this lane's reading; it is not what the sources say.

## Located quotes

S236's capture is the JSON record exactly as served (one line). J1-J8 are substrings of its `abstractText` field; J0
is its `title` field. S233's quotes are substrings of the publisher page's text capture; G0 is the article title as
the page prints it. Quotes are matched after `tools/gate-records.py`'s normalization (curly quotes to straight,
whitespace collapsed). J2 keeps the abstract's own decimal comma ("11,9%").

| qid | source | quote |
|---|---|---|
| J0 | S236 | "Quotation accuracy in medical journal articles-a systematic review and meta-analysis." |
| J1 | S236 | "Out of 559 studies screened we included 28 in the main analysis," |
| J2 | S236 | "and estimated major, minor and total quotation error rates of 11,9%, 95% CI [8.4, 16.6] 11.5% [8.3, 15.7], and 25.4% [19.5, 32.4]." |
| J3 | S236 | "While heterogeneity was substantial, even the lowest estimate of total quotation errors was considerable (6.7%)." |
| J4 | S236 | "Indirect references accounted for less than one sixth of all quotation problems." |
| J5 | S236 | "Readers of medical journal articles should be aware of the fact that quotation errors are common." |
| J6 | S236 | "Measures against quotation errors include spot checks by editors and reviewers, correct placement of citations in the text," |
| J7 | S236 | "and declarations by authors that they have checked cited material." |
| J8 | S236 | "taking account of differences between studies in error ascertainment." |
| G0 | S233 | "Accuracy of cited “facts” in medical research articles: A review of study methodology and recalculation of quotation error rate" |
| G1 | S233 | "Previous reviews estimated that approximately 20 to 25% of assertions cited from original research articles, or “facts,” are inaccurately quoted in the medical literature." |
| G2 | S233 | "the estimate of quotation errors calculated here is based on the ratio of quotation errors to quotations examined (a percent)" |
| G3 | S233 | "rather than the more prevalent and weighted metric of quotation errors to the references selected." |
| G4 | S233 | "a major content error was a cited assertion in which the referenced source either failed to substantiate, was unrelated to, or contradicted the assertion." |
| G5 | S233 | "a minor error was an oversimplification, a generalization, or a trivial inaccuracy that did not change the intended meaning of the original authors." |
| G6 | S233 | "I defined “content errors” as an informative or “factual” inaccuracies and distinguished these errors from “source errors,” which are secondary (or indirect) citations." |
| G7 | S233 | "The most notable difference in the criteria is that source errors are considered minor errors in approximately half of the studies." |
| G8 | S233 | "Of 43 original articles on quotation errors in the medical literature published through July 2017, 15 met the selection criteria for the primary analysis" |
| G9 | S233 | "In these 15 articles, a total of 3,337 references and 5,535 quotations (estimated) were individually evaluated for accuracy and appropriateness by subject-matter experts." |
| G10 | S233 | "I estimate that 14.5% (10.5% to 18.6% at a 95% confidence interval) of cited assertions in original research articles in medical journals are inaccurate." |
| G11 | S233 | "the distribution of content errors (64.8% major to 35.2% minor errors) is particularly concerning." |
| G12 | S233 | "experts must evaluate and categorize each quotation in the context of the referencing article and compare the assertion to information provided in the original source." |
| G13 | S233 | "the orginal studies had an inconsistent, often biased, selection of a single quotation from multiple quotations associated with a single reference." |

G13 keeps the page's own misspelling "orginal".

## Decision table

| Situation | Do | Never | Warrant | Lane |
|---|---|---|---|---|
| Deciding whether a cited claim needs its source re-opened | treat an unchecked citation as unreliable: a meta-analysis that included 28 studies in its main analysis put total quotation errors at 25.4% and major ones at 11,9% (as printed), and a re-count put 14.5% of cited assertions in original research articles in medical journals inaccurate | (none stated by the sources) | J1, J2, J5, G10 | the lane re-opens every source it cites (CORPUS.md rule 1); these rates are why a located quote is the floor, not the proof |
| Classifying a mismatch between a citing sentence and its source | call it major when the source fails to substantiate, is unrelated to, or contradicts the assertion; minor when it is an oversimplification, a generalization or a trivial inaccuracy that keeps the intended meaning | (none stated by the sources) | G4, G5 | `tools/gate-records.py` checks that the quote is in the capture (QUOTE_ABSENT); it cannot tell a supporting quote from one that is unrelated to the sentence citing it |
| Citing a source through another source | record it as a source error, kept apart from a content error (the cited source was not read); indirect references were less than one sixth of all quotation problems | (none stated by the sources) | G6, J4 | the lane's carrier rule grades a third-party carrier B (S236 itself is such a carrier) |
| Reporting or comparing an error rate | state the denominator: quotation errors per quotation examined (a percent), not per reference selected | (none stated by the sources) | G2, G3, G9 | a lane count names its unit in the counter (rows, records, lines), the same discipline |
| Comparing rates across studies | account for differences in how studies ascertain errors; criteria differ (source errors counted as minor in about half the studies), heterogeneity is substantial, and the lowest total estimate was still 6.7% | (none stated by the sources) | J3, J8, G7 | the lane does not pool its own rounds' counts across instruments that changed |
| Choosing what to check in a citing text | sample quotations, not only references, and judge each assertion in the context of the citing article against the original source | (none stated by the sources) | G12, G13 | a GATE-RECORD binds one quote to one capture; the citing sentence is in the entry, so a reviewer can compare the two |
| Weighing how serious the errors are | report the major/minor split: 64.8% of content errors were major | (none stated by the sources) | G11 | — |
| Preventing quotation errors | spot checks by editors and reviewers, correct placement of citations in the text, and an author's declaration of having checked cited material | (none stated by the sources) | J6, J7 | the hyaku closure's non-author spot-check re-opens a sample of the lane's sources (LEARNING.md) |

## As run

Every search in `## Searches` ran on 2026-11-09 against the lane's committed capture store at revision
`47ed34fa785288837f84cde9db15c41300854a78` (the round-98 landing, round 99's base, before S233-S236 were captured),
materialised read-only with `git archive 47ed34fa785288837f84cde9db15c41300854a78 corpus/captures | tar -x -C <scratch>`
and searched from `<scratch>` with GNU grep 3.12 (`/usr/bin/grep`):

    /usr/bin/grep -l -F -e '<expression>' corpus/captures/*.txt | LC_ALL=C sort        # engine fixed

`python3 -B tools/search-rerun.py verify corpus/knowledge/quotation-error-rates-r99.md --root .` re-runs each one at
`47ed34fa` and over the current tree (where the new captures now match: `tree=CHANGED`, not a finding without
`--strict`).

## Searches

| id | engine | where | expression | rev | searched | hits | hit_set |
|---|---|---|---|---|---|---|---|
| Q1 | fixed | corpus/captures/*.txt | `quotation error` | 47ed34fa785288837f84cde9db15c41300854a78 | 2026-11-09 | 0 | - |
| Q2 | fixed | corpus/captures/*.txt | `Jergas` | 47ed34fa785288837f84cde9db15c41300854a78 | 2026-11-09 | 0 | - |
| Q3 | fixed | corpus/captures/*.txt | `Mogull` | 47ed34fa785288837f84cde9db15c41300854a78 | 2026-11-09 | 0 | - |
| Q4 | fixed | corpus/captures/*.txt | `failed to substantiate` | 47ed34fa785288837f84cde9db15c41300854a78 | 2026-11-09 | 0 | - |

## Named limits

- Both sources are about medical journal articles. Nothing here says how often a citation fails in another field,
  in web sources, or in this lane's own corpus; the lane has not measured its own rate.
- S236 is the abstract, not the article; its pooled estimates are read as the abstract states them. Its numbers are
  the authors' pooled rates over heterogeneous studies (J3), not a property of any one article.
- S233 re-derives a rate from 15 studies of original research articles; it excludes reviews and preliminary data, so
  its 14.5% and S236's 25.4% count different things and are not a contradiction. The entry does not reconcile them.
- The decision rows' *Do* cells paraphrase their warrant quotes; every number a *Do* cell states is printed in one of
  its own warrant quotes (the controls check this), but a paraphrase can still narrow or widen a quote's meaning.
- Major/minor are S233's definitions (G4, G5); S236's abstract uses the same words without defining them.
- S236's abstract ties all three rates to "28 in the main analysis" (J1, J2). The article body, which the lane does not
  hold, pools the major and minor rates over 27 studies and the total over 28 (`R99ScoutSources`' re-open of
  PMC4627914, not a lane capture; amendment B5). The first decision row follows the abstract.
- The controls read numerals only: a spelled-out quantity ("one sixth", "about half") in a Do cell is not checked
  against its warrants (amendment B6, `R99ScoutSources` F-4).

## Update

Round 100 (2026-11-09): this entry's `recheck: on-release` fired. The authors' 2025 update (Baethge & Jergas,
Research Integrity and Peer Review, pmid 40696441) was opened through its Europe PMC record as S238 and is held in
`corpus/knowledge/quotation-error-update-r100.md`: a search that identified 46 studies, 16.9% of quotations
incorrect, major errors 8.0%, and no significant improvement over time by meta-regression. Read the first decision row
above as the 2015 synthesis's reading, not the current pooled rate; the abstracts print 28 and 46 studies and state no
comparison between the two rates, and the update's own trend estimate is its meta-regression slope. Nothing above is
changed by the update. The 2025 abstract does not define major and minor, so the rows that use them still stand on
S233 (G4, G5, G11); the update's article body, which the lane does not hold, defines both and reports the 46 studies
as 18 new plus this entry's 28 (`.ufo/waves/round-100/w1/R100ScoutSources.md` F-2; a seat's re-open, routed to a lane
GET in round 101).

## Gate records

GATE-RECORD S236 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:26528420%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T04:01:07Z tier=B decision=admit capture=corpus/captures/405a0054e1f6dbd1854a3618.txt capture_sha256=6b0bcbda40de0c02268931d749701142a1e222edf679d4055577130af886ac31 words=10 quote="Quotation accuracy in medical journal articles-a systematic review and meta-analysis."
GATE-RECORD S236 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:26528420%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T04:01:07Z tier=B decision=admit capture=corpus/captures/405a0054e1f6dbd1854a3618.txt capture_sha256=6b0bcbda40de0c02268931d749701142a1e222edf679d4055577130af886ac31 words=12 quote="Out of 559 studies screened we included 28 in the main analysis,"
GATE-RECORD S236 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:26528420%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T04:01:07Z tier=B decision=admit capture=corpus/captures/405a0054e1f6dbd1854a3618.txt capture_sha256=6b0bcbda40de0c02268931d749701142a1e222edf679d4055577130af886ac31 words=22 quote="and estimated major, minor and total quotation error rates of 11,9%, 95% CI [8.4, 16.6] 11.5% [8.3, 15.7], and 25.4% [19.5, 32.4]."
GATE-RECORD S236 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:26528420%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T04:01:07Z tier=B decision=admit capture=corpus/captures/405a0054e1f6dbd1854a3618.txt capture_sha256=6b0bcbda40de0c02268931d749701142a1e222edf679d4055577130af886ac31 words=15 quote="While heterogeneity was substantial, even the lowest estimate of total quotation errors was considerable (6.7%)."
GATE-RECORD S236 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:26528420%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T04:01:07Z tier=B decision=admit capture=corpus/captures/405a0054e1f6dbd1854a3618.txt capture_sha256=6b0bcbda40de0c02268931d749701142a1e222edf679d4055577130af886ac31 words=12 quote="Indirect references accounted for less than one sixth of all quotation problems."
GATE-RECORD S236 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:26528420%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T04:01:07Z tier=B decision=admit capture=corpus/captures/405a0054e1f6dbd1854a3618.txt capture_sha256=6b0bcbda40de0c02268931d749701142a1e222edf679d4055577130af886ac31 words=16 quote="Readers of medical journal articles should be aware of the fact that quotation errors are common."
GATE-RECORD S236 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:26528420%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T04:01:07Z tier=B decision=admit capture=corpus/captures/405a0054e1f6dbd1854a3618.txt capture_sha256=6b0bcbda40de0c02268931d749701142a1e222edf679d4055577130af886ac31 words=18 quote="Measures against quotation errors include spot checks by editors and reviewers, correct placement of citations in the text,"
GATE-RECORD S236 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:26528420%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T04:01:07Z tier=B decision=admit capture=corpus/captures/405a0054e1f6dbd1854a3618.txt capture_sha256=6b0bcbda40de0c02268931d749701142a1e222edf679d4055577130af886ac31 words=10 quote="and declarations by authors that they have checked cited material."
GATE-RECORD S236 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:26528420%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T04:01:07Z tier=B decision=admit capture=corpus/captures/405a0054e1f6dbd1854a3618.txt capture_sha256=6b0bcbda40de0c02268931d749701142a1e222edf679d4055577130af886ac31 words=9 quote="taking account of differences between studies in error ascertainment."
GATE-RECORD S233 url=https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0184727 fetched=2026-11-09T04:00:33Z tier=A decision=admit capture=corpus/captures/4b70901ad80c513f0c2f750c.txt capture_sha256=60048511ac1de7f034c13bd89a6dcba8bae86b1cd71993fdea60529a78f790d3 words=19 quote="Accuracy of cited “facts” in medical research articles: A review of study methodology and recalculation of quotation error rate"
GATE-RECORD S233 url=https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0184727 fetched=2026-11-09T04:00:33Z tier=A decision=admit capture=corpus/captures/4b70901ad80c513f0c2f750c.txt capture_sha256=60048511ac1de7f034c13bd89a6dcba8bae86b1cd71993fdea60529a78f790d3 words=24 quote="Previous reviews estimated that approximately 20 to 25% of assertions cited from original research articles, or “facts,” are inaccurately quoted in the medical literature."
GATE-RECORD S233 url=https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0184727 fetched=2026-11-09T04:00:33Z tier=A decision=admit capture=corpus/captures/4b70901ad80c513f0c2f750c.txt capture_sha256=60048511ac1de7f034c13bd89a6dcba8bae86b1cd71993fdea60529a78f790d3 words=20 quote="the estimate of quotation errors calculated here is based on the ratio of quotation errors to quotations examined (a percent)"
GATE-RECORD S233 url=https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0184727 fetched=2026-11-09T04:00:33Z tier=A decision=admit capture=corpus/captures/4b70901ad80c513f0c2f750c.txt capture_sha256=60048511ac1de7f034c13bd89a6dcba8bae86b1cd71993fdea60529a78f790d3 words=15 quote="rather than the more prevalent and weighted metric of quotation errors to the references selected."
GATE-RECORD S233 url=https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0184727 fetched=2026-11-09T04:00:33Z tier=A decision=admit capture=corpus/captures/4b70901ad80c513f0c2f750c.txt capture_sha256=60048511ac1de7f034c13bd89a6dcba8bae86b1cd71993fdea60529a78f790d3 words=24 quote="a major content error was a cited assertion in which the referenced source either failed to substantiate, was unrelated to, or contradicted the assertion."
GATE-RECORD S233 url=https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0184727 fetched=2026-11-09T04:00:33Z tier=A decision=admit capture=corpus/captures/4b70901ad80c513f0c2f750c.txt capture_sha256=60048511ac1de7f034c13bd89a6dcba8bae86b1cd71993fdea60529a78f790d3 words=23 quote="a minor error was an oversimplification, a generalization, or a trivial inaccuracy that did not change the intended meaning of the original authors."
GATE-RECORD S233 url=https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0184727 fetched=2026-11-09T04:00:33Z tier=A decision=admit capture=corpus/captures/4b70901ad80c513f0c2f750c.txt capture_sha256=60048511ac1de7f034c13bd89a6dcba8bae86b1cd71993fdea60529a78f790d3 words=23 quote="I defined “content errors” as an informative or “factual” inaccuracies and distinguished these errors from “source errors,” which are secondary (or indirect) citations."
GATE-RECORD S233 url=https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0184727 fetched=2026-11-09T04:00:33Z tier=A decision=admit capture=corpus/captures/4b70901ad80c513f0c2f750c.txt capture_sha256=60048511ac1de7f034c13bd89a6dcba8bae86b1cd71993fdea60529a78f790d3 words=21 quote="The most notable difference in the criteria is that source errors are considered minor errors in approximately half of the studies."
GATE-RECORD S233 url=https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0184727 fetched=2026-11-09T04:00:33Z tier=A decision=admit capture=corpus/captures/4b70901ad80c513f0c2f750c.txt capture_sha256=60048511ac1de7f034c13bd89a6dcba8bae86b1cd71993fdea60529a78f790d3 words=24 quote="Of 43 original articles on quotation errors in the medical literature published through July 2017, 15 met the selection criteria for the primary analysis"
GATE-RECORD S233 url=https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0184727 fetched=2026-11-09T04:00:33Z tier=A decision=admit capture=corpus/captures/4b70901ad80c513f0c2f750c.txt capture_sha256=60048511ac1de7f034c13bd89a6dcba8bae86b1cd71993fdea60529a78f790d3 words=23 quote="In these 15 articles, a total of 3,337 references and 5,535 quotations (estimated) were individually evaluated for accuracy and appropriateness by subject-matter experts."
GATE-RECORD S233 url=https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0184727 fetched=2026-11-09T04:00:33Z tier=A decision=admit capture=corpus/captures/4b70901ad80c513f0c2f750c.txt capture_sha256=60048511ac1de7f034c13bd89a6dcba8bae86b1cd71993fdea60529a78f790d3 words=24 quote="I estimate that 14.5% (10.5% to 18.6% at a 95% confidence interval) of cited assertions in original research articles in medical journals are inaccurate."
GATE-RECORD S233 url=https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0184727 fetched=2026-11-09T04:00:33Z tier=A decision=admit capture=corpus/captures/4b70901ad80c513f0c2f750c.txt capture_sha256=60048511ac1de7f034c13bd89a6dcba8bae86b1cd71993fdea60529a78f790d3 words=14 quote="the distribution of content errors (64.8% major to 35.2% minor errors) is particularly concerning."
GATE-RECORD S233 url=https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0184727 fetched=2026-11-09T04:00:33Z tier=A decision=admit capture=corpus/captures/4b70901ad80c513f0c2f750c.txt capture_sha256=60048511ac1de7f034c13bd89a6dcba8bae86b1cd71993fdea60529a78f790d3 words=25 quote="experts must evaluate and categorize each quotation in the context of the referencing article and compare the assertion to information provided in the original source."
GATE-RECORD S233 url=https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0184727 fetched=2026-11-09T04:00:33Z tier=A decision=admit capture=corpus/captures/4b70901ad80c513f0c2f750c.txt capture_sha256=60048511ac1de7f034c13bd89a6dcba8bae86b1cd71993fdea60529a78f790d3 words=21 quote="the orginal studies had an inconsistent, often biased, selection of a single quotation from multiple quotations associated with a single reference."
GATE-RECORD S232 url=https://peerj.com/articles/1364/ fetched=2026-11-09T04:00:32Z tier=A decision=reject capture=none curl_rc=22 http=403 words=0 quote=none
GATE-RECORD S235 url=https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4627914/fullTextXML fetched=2026-11-09T04:00:42Z tier=B decision=reject capture=none curl_rc=22 http=500 words=0 quote=none
