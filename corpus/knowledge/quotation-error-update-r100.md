# Quotation errors, updated — the 2025 meta-analysis, what changed since 2015, and what did not (round 100)

source: S238, S236
verified-at: 2026-11-09 (round 100; capture `b5eec205612ee5f138cf065d` — Europe PMC's core record for PMID 40696441, Baethge C, Jergas H, "Systematic review and meta-analysis of quotation inaccuracy in medicine", Research Integrity and Peer Review 2025;10(1), doi 10.1186/s41073-025-00173-z, PMCID PMC12285159, carrying the authors' own published abstract, opened as S238 — and capture `405a0054e1f6dbd1854a3618`, the same authors' 2015 abstract, S236, held since round 99)
recheck: on-release
updates: corpus/knowledge/quotation-error-rates-r99.md

## What this entry governs

Round 99 held how often a cited source fails the sentence that cites it (`corpus/knowledge/quotation-error-rates-r99.md`),
through Jergas & Baethge 2015 (S236: 28 studies in the main analysis, total 25.4%, major 11,9% as printed) and Mogull
2017 (S233: 14.5%). That entry's `recheck: on-release` names its own trigger: a newer synthesis by the same authors.
The 2025 update is that release. Round 99 could not read it — the publisher answered with a "Client Challenge" page
(S234) — and its Europe PMC record was reached only by a wave seat, not by a lane GET. This round's GET of that record
answered http 200 (S238), so this entry holds what the update's own abstract says, and what it changes in the round-99
entry's reading:

1. **Baethge & Jergas 2025 (S238, tier B).** A systematic review, meta-analysis and meta-regression of quotation
   errors in medicine with no date or language restriction, read through its own published abstract in Europe PMC's
   index record (the full-text route, PMC12285159, answered http 500 to both of this round's GETs, S239). Thirteen
   quotes from the abstract (U1-U13) and the record's title (U0).
2. **Jergas & Baethge 2015 (S236, tier B)**, held since round 99, quoted again here (J1, J2) only to compare it with
   the update.

The column marked *lane* is this lane's reading; it is not what the sources say.

## Located quotes

S238's capture is the JSON record exactly as served (one line). U1-U13 are substrings of its `abstractText` field; U0
is its `title` field. J1 and J2 are substrings of S236's `abstractText` (round 99's quotes of the same ids). Quotes are
matched after `tools/gate-records.py`'s normalization (curly quotes to straight, whitespace collapsed).

| qid | source | quote |
|---|---|---|
| U0 | S238 | "Systematic review and meta-analysis of quotation inaccuracy in medicine." |
| U1 | S238 | "Quotation errors, that is, a reference not supporting the authors' claim, may still be a significant issue in scientific medical writing." |
| U2 | S238 | "This study aimed to examine the quotation error rate and trends over time in the medical literature." |
| U3 | S238 | "A systematic search of PubMed, Web of Science, and reference lists for quotation error studies in medicine and without date or language restrictions" |
| U4 | S238 | "identified 46 studies analyzing 32,000 quotations/references." |
| U5 | S238 | "Literature search, data extraction, and risk of bias assessments were performed independently by two raters." |
| U6 | S238 | "Random-effects meta-analyses and meta-regression were used to analyze error rates and trends (protocol pre-registered on OSF)." |
| U7 | S238 | "16.9% (95% CI: 14.1%-20.0%) of quotations were incorrect, with approximately half classified as major errors (8.0% [95% CI: 6.4%-10.0%])." |
| U8 | S238 | "Heterogeneity was high, and Egger's test for small study effects remained negative throughout." |
| U9 | S238 | "Meta-regression showed no significant improvement in quotation accuracy over recent years (slope: -0.002 [95% CI: -0.03 to 0.02], p = 0.85)." |
| U10 | S238 | "Neither risk of bias, nor the number of references were statistically significantly associated with total error rate, but journal impact factor was:" |
| U11 | S238 | "Spearman's ρ = -0.253 (p = 0.043, binomial test, N = 25)." |
| U12 | S238 | "Quotation errors remain a problem in the medical literature, with no improvement over time." |
| U13 | S238 | "Addressing this issue requires concerted efforts to improve scholarly practices and editorial processes." |
| J1 | S236 | "Out of 559 studies screened we included 28 in the main analysis," |
| J2 | S236 | "and estimated major, minor and total quotation error rates of 11,9%, 95% CI [8.4, 16.6] 11.5% [8.3, 15.7], and 25.4% [19.5, 32.4]." |

## Decision table

| Situation | Do | Never | Warrant | Lane |
|---|---|---|---|---|
| Stating how often a citation in medicine fails its source | cite the update's pooled rate as printed: 16.9% (95% CI: 14.1%-20.0%) of quotations incorrect, major errors 8.0% [95% CI: 6.4%-10.0%], over 46 studies analyzing 32,000 quotations/references | (none stated by the sources) | U4, U7 | the round-99 entry's first row cites the 2015 rates; it now carries a pointer to this entry (`## Update`), and this row is the current reading |
| Reading the 2015 rate next to the 2025 rate | keep each rate with its own study set: the earlier review included 28 studies in the main analysis (total 25.4%, major 11,9% as printed); the update identified 46 studies (total 16.9%, major 8.0%); the gap between them is not a measured trend | (none stated by the sources) | J1, J2, U4, U7 | the lane does not subtract one pooled rate from another; the trend is the next row's slope |
| Asking whether quotation accuracy has improved | answer from the meta-regression: no significant improvement over recent years (slope: -0.002 [95% CI: -0.03 to 0.02], p = 0.85) | (none stated by the sources) | U9, U12 | a lower pooled rate in a later synthesis is not, alone, evidence of improvement |
| Using a journal's standing as a proxy for citation accuracy | record the association only as printed: journal impact factor was associated with total error rate (Spearman's ρ = -0.253, p = 0.043, binomial test, N = 25); risk of bias and the number of references were not | (none stated by the sources) | U10, U11 | the lane's tier rules grade a source's route and kind, not its journal's impact factor; this row does not change them |
| Defining what is counted | count a reference that does not support the authors' claim; about half of incorrect quotations were classed major | (none stated by the sources) | U1, U7 | major and minor are defined in the round-99 entry (S233, G4/G5); the update's abstract does not define them |
| Weighing the pooled estimate | treat it as an estimate over heterogeneous studies: heterogeneity was high; Egger's test for small study effects remained negative throughout | (none stated by the sources) | U8 | the abstract states the test's result, not its statistic |
| Judging how the synthesis was made | note the method the abstract states: search without date or language restrictions, two independent raters for search, extraction and risk of bias, random-effects meta-analysis and meta-regression, protocol pre-registered on OSF | (none stated by the sources) | U3, U5, U6 | the lane did not open the OSF protocol |
| Deciding what to do about quotation errors | treat them as a standing problem that needs concerted efforts on scholarly practices and editorial processes | (none stated by the sources) | U12, U13 | the 2015 abstract named specific measures (round-99 entry, J6/J7); the 2025 abstract names none |

## As run

Every search in `## Searches` ran on 2026-11-09 against the lane's committed capture store at revision
`929c784c63a1fd17961d21742101b2b109b7b8ff` (the round-99 landing, round 100's base, before S238 was captured),
materialised read-only with `git archive 929c784c63a1fd17961d21742101b2b109b7b8ff corpus/captures | tar -x -C <scratch>`
and searched from `<scratch>` with GNU grep 3.12 (`/usr/bin/grep`):

    /usr/bin/grep -l -F -e '<expression>' corpus/captures/*.txt | LC_ALL=C sort        # engine fixed

`python3 -B tools/search-rerun.py verify corpus/knowledge/quotation-error-update-r100.md --root .` re-runs each one at
`929c784c` and over the current tree (where S238's capture now matches: `tree=CHANGED`, not a finding without
`--strict`).

## Searches

| id | engine | where | expression | rev | searched | hits | hit_set |
|---|---|---|---|---|---|---|---|
| Q1 | fixed | corpus/captures/*.txt | `quotation inaccuracy` | 929c784c63a1fd17961d21742101b2b109b7b8ff | 2026-11-09 | 0 | - |
| Q2 | fixed | corpus/captures/*.txt | `32,000 quotations` | 929c784c63a1fd17961d21742101b2b109b7b8ff | 2026-11-09 | 0 | - |
| Q3 | fixed | corpus/captures/*.txt | `40696441` | 929c784c63a1fd17961d21742101b2b109b7b8ff | 2026-11-09 | 0 | - |

## Named limits

- S238 is the abstract, not the article; its numbers are read as the abstract states them. The full text (S239,
  PMC12285159) answered http 500 to this round's two GETs, so nothing here rests on the article body: not the list of
  46 studies, not how "major" is defined there, not the heterogeneity statistic.
- Both syntheses are about medicine. Nothing here says how often a citation fails in another field, in web sources, or
  in this lane's own corpus; the lane has not measured its own rate.
- The 2015 and 2025 pooled rates come from different study sets (28 and 46 studies); the abstracts do not say how many
  studies they share. This entry does not compute a difference between them.
- The impact-factor association is a correlation over 25 data points as the abstract prints it; its direction is
  recorded only as the printed sign.
- The decision rows' *Do* cells paraphrase their warrant quotes; every numeral a *Do* cell states is printed, with the
  same sign and form, in one of that row's own warrant quotes (the controls check this), but a paraphrase can still
  narrow or widen a quote's meaning. Spelled-out quantities ("about half") are not checked.

## Gate records

GATE-RECORD S238 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:40696441%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T05:12:32Z tier=B decision=admit capture=corpus/captures/b5eec205612ee5f138cf065d.txt capture_sha256=175f805d6460acd61f2a8c979388a500e35b9c85217d3531ae1fb4418c613a98 words=9 quote="Systematic review and meta-analysis of quotation inaccuracy in medicine."
GATE-RECORD S238 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:40696441%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T05:12:32Z tier=B decision=admit capture=corpus/captures/b5eec205612ee5f138cf065d.txt capture_sha256=175f805d6460acd61f2a8c979388a500e35b9c85217d3531ae1fb4418c613a98 words=21 quote="Quotation errors, that is, a reference not supporting the authors' claim, may still be a significant issue in scientific medical writing."
GATE-RECORD S238 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:40696441%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T05:12:32Z tier=B decision=admit capture=corpus/captures/b5eec205612ee5f138cf065d.txt capture_sha256=175f805d6460acd61f2a8c979388a500e35b9c85217d3531ae1fb4418c613a98 words=17 quote="This study aimed to examine the quotation error rate and trends over time in the medical literature."
GATE-RECORD S238 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:40696441%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T05:12:32Z tier=B decision=admit capture=corpus/captures/b5eec205612ee5f138cf065d.txt capture_sha256=175f805d6460acd61f2a8c979388a500e35b9c85217d3531ae1fb4418c613a98 words=23 quote="A systematic search of PubMed, Web of Science, and reference lists for quotation error studies in medicine and without date or language restrictions"
GATE-RECORD S238 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:40696441%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T05:12:32Z tier=B decision=admit capture=corpus/captures/b5eec205612ee5f138cf065d.txt capture_sha256=175f805d6460acd61f2a8c979388a500e35b9c85217d3531ae1fb4418c613a98 words=6 quote="identified 46 studies analyzing 32,000 quotations/references."
GATE-RECORD S238 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:40696441%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T05:12:32Z tier=B decision=admit capture=corpus/captures/b5eec205612ee5f138cf065d.txt capture_sha256=175f805d6460acd61f2a8c979388a500e35b9c85217d3531ae1fb4418c613a98 words=15 quote="Literature search, data extraction, and risk of bias assessments were performed independently by two raters."
GATE-RECORD S238 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:40696441%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T05:12:32Z tier=B decision=admit capture=corpus/captures/b5eec205612ee5f138cf065d.txt capture_sha256=175f805d6460acd61f2a8c979388a500e35b9c85217d3531ae1fb4418c613a98 words=16 quote="Random-effects meta-analyses and meta-regression were used to analyze error rates and trends (protocol pre-registered on OSF)."
GATE-RECORD S238 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:40696441%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T05:12:32Z tier=B decision=admit capture=corpus/captures/b5eec205612ee5f138cf065d.txt capture_sha256=175f805d6460acd61f2a8c979388a500e35b9c85217d3531ae1fb4418c613a98 words=19 quote="16.9% (95% CI: 14.1%-20.0%) of quotations were incorrect, with approximately half classified as major errors (8.0% [95% CI: 6.4%-10.0%])."
GATE-RECORD S238 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:40696441%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T05:12:32Z tier=B decision=admit capture=corpus/captures/b5eec205612ee5f138cf065d.txt capture_sha256=175f805d6460acd61f2a8c979388a500e35b9c85217d3531ae1fb4418c613a98 words=13 quote="Heterogeneity was high, and Egger's test for small study effects remained negative throughout."
GATE-RECORD S238 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:40696441%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T05:12:32Z tier=B decision=admit capture=corpus/captures/b5eec205612ee5f138cf065d.txt capture_sha256=175f805d6460acd61f2a8c979388a500e35b9c85217d3531ae1fb4418c613a98 words=21 quote="Meta-regression showed no significant improvement in quotation accuracy over recent years (slope: -0.002 [95% CI: -0.03 to 0.02], p = 0.85)."
GATE-RECORD S238 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:40696441%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T05:12:32Z tier=B decision=admit capture=corpus/captures/b5eec205612ee5f138cf065d.txt capture_sha256=175f805d6460acd61f2a8c979388a500e35b9c85217d3531ae1fb4418c613a98 words=22 quote="Neither risk of bias, nor the number of references were statistically significantly associated with total error rate, but journal impact factor was:"
GATE-RECORD S238 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:40696441%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T05:12:32Z tier=B decision=admit capture=corpus/captures/b5eec205612ee5f138cf065d.txt capture_sha256=175f805d6460acd61f2a8c979388a500e35b9c85217d3531ae1fb4418c613a98 words=12 quote="Spearman's ρ = -0.253 (p = 0.043, binomial test, N = 25)."
GATE-RECORD S238 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:40696441%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T05:12:32Z tier=B decision=admit capture=corpus/captures/b5eec205612ee5f138cf065d.txt capture_sha256=175f805d6460acd61f2a8c979388a500e35b9c85217d3531ae1fb4418c613a98 words=14 quote="Quotation errors remain a problem in the medical literature, with no improvement over time."
GATE-RECORD S238 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:40696441%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T05:12:32Z tier=B decision=admit capture=corpus/captures/b5eec205612ee5f138cf065d.txt capture_sha256=175f805d6460acd61f2a8c979388a500e35b9c85217d3531ae1fb4418c613a98 words=13 quote="Addressing this issue requires concerted efforts to improve scholarly practices and editorial processes."
GATE-RECORD S236 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:26528420%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T04:01:07Z tier=B decision=admit capture=corpus/captures/405a0054e1f6dbd1854a3618.txt capture_sha256=6b0bcbda40de0c02268931d749701142a1e222edf679d4055577130af886ac31 words=12 quote="Out of 559 studies screened we included 28 in the main analysis,"
GATE-RECORD S236 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:26528420%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T04:01:07Z tier=B decision=admit capture=corpus/captures/405a0054e1f6dbd1854a3618.txt capture_sha256=6b0bcbda40de0c02268931d749701142a1e222edf679d4055577130af886ac31 words=22 quote="and estimated major, minor and total quotation error rates of 11,9%, 95% CI [8.4, 16.6] 11.5% [8.3, 15.7], and 25.4% [19.5, 32.4]."
GATE-RECORD S239 url=https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12285159/fullTextXML fetched=2026-11-09T05:12:32Z tier=B decision=reject capture=none curl_rc=22 http=500 words=0 quote=none
