# R97ScoutSources — source re-open and frontier scout (chousa round 97)

Attacked tree: `9a0ce2015fa0254848f2f32f612b20caf7dc5478` (clone at `$S/repo`, `git -C "$S/repo" rev-parse HEAD` → `9a0ce2015fa0254848f2f32f612b20caf7dc5478`; receipt `w1/R97ScoutSources-fetch-hashes.txt`).
Scratch: `/fast/scratch/hyaku/chousa-r97/R97ScoutSources` (deleted before yield). Tools: `curl`, `pdftotext`/`pdfinfo` (present, no installs); no pacman, no sudo. Network: only S225, S226, S227 (2 attempts max each; see §1). Captures and `refetch.tsv` were not written.

## 1. Hashes: fetched bodies vs `corpus/evidence/round57/refetch.tsv`

| src | attempts (curl argv) | result | refetch row | verdict |
|---|---|---|---|---|
| S225 PDF | 2: #1 errored on my own `-w` format string (no body); #2 `curl -L` | HTTP 200, 137268 B, sha `56c4cdd6…c6cc0dfcc6` | raw `56c4cdd6…`, txt `abd08a93…` | raw matches |
| S225 pdftotext | `pdftotext -layout S225.pdf` | sha `abd08a93…`; `cmp` vs `corpus/captures/347c55ba…txt` rc 0, diff empty | txt `abd08a93…` | matches, byte-identical |
| S226 HTML | #1 `curl -L` (no -fsSL/UA): 200, sha `c2f9b69f…`; #2 lane argv `curl -fsSL --compressed -A <lane UA>`: 200, sha `6458281b…` | raw **does not reproduce**: logged `777b890f…` matches neither of my two fetches | raw `777b890f…` | **raw hash not reproducible** (two different raw digests from two fetches, neither the logged one) |
| S226 text form | lane `recipe_txt` on both raw bodies | txt sha `16114498…`, `txt==capture` True for both | txt `16114498…` | matches; the quoted text is stable across fetches |
| S227 PDF | #1 `curl -L`: HTTP 403, body saved = Cloudflare "Just a moment..." interstitial HTML; #2 lane argv (`-f`): HTTP 403, curl rc 22 | matches row | row: rc 22, 403 | matches (held) |

Receipts: `w1/R97ScoutSources-fetch-hashes.txt`, `w1/R97ScoutSources-S225-pdftotext-S226-recipe.txt`.
Commands: `sha256sum` over `$S/fetch/*`; `grep -P '^S22[567]\t' corpus/evidence/round57/refetch.tsv`; `python3 -B -c '<recipe_txt>'` (exit 0). Each 2 attempts max; no capture or refetch.tsv written.

## 2. Six quotes located in my own copies (C2 quote-location check)

| quote | my copy | line | result |
|---|---|---|---|
| L4 "Does the search strategy match the research question/PICO?" | S225 `pdftotext` and capture | 34 | found, one line |
| L7 "Are unconventional or complex strategies explained?" | S225 capture; S226 text (recipe line 530) and raw HTML (line 426) | 39 | found |
| L13 "…(see the following) used for each concept?" | S225 capture | 57 | found |
| L16 "Does the search capture relevant truncation (ie, …)?" | S225 capture | 62 | found |
| L21+L22 "Are there incorrect line combinations or orphan lines … statement)?" | S225 capture | **73** (entry says 74) | found on line 73; **capture line 74 is empty** |
| L27 / L28 / L29 (S226) | S226 capture | 503 / 503 / 576 | found |

All 26 S225 quotes are substrings of exactly one capture line (python check, `w1/R97ScoutSources-recount.txt`; the per-quote line-count loop printed no mismatches, exit 0). So "each quote is a substring of one line" holds (held).

**Finding F-Q1 (wrong line and word count, C2).** The entry says L21/L22 are "one 32-word question on capture line 74". Recount: capture line 74 is empty (`sed -n 74p` → empty; python `repr` `''`); the question is on line 73; word count L21=19, L22=11, total **30**. Receipt: `w1/R97ScoutSources-recount.txt` (`line 73 contains question text`, `capture line 74 is empty: ''`, `words L21=19 L22=11 total=30`), exit 0.

## 3. Is S226 an independent transcription of S225? Shared errors?

- **Not a copy of S225 at the byte level.** Different renderers: S225 is `pdftotext -layout` (numbered element headings, parentheticals on the same line); S226 is HTML text (headings on separate lines, no numbers, stray space in "question/ PICO ?"). Receipt: `w1/R97ScoutSources-s225-s226-compare-coverage.txt`.
- **Same question set up to wording.** Question-ending lines: S225 = 33, S226 = 34. Letter-level differences: S226-only 6 and S225-only 5; each is a wording or punctuation variant ("for example" ↔ "e.g.", "eg" ↔ "e.g.", "see the following" ↔ "see below", "vs." ↔ "versus", "Are there any errors…"), plus the S226 page line "Did you find the information on this page useful?" (page furniture). No S226 question is absent from S225.
- **Shared errors:** none found among the 26 located quotes. Verbatim-identical lines include "Does the search retrieve too many or too few records? (Please show number of hits per line.)", "Are unconventional or complex strategies explained?", "Should any long strings be broken…", "Are there any spelling errors?".
- **Provenance is shared, not independent of the checklist.** S226's preamble links `https://www.cadth.ca/sites/default/files/pdf/CP0015_PRESS_Update_Report_2016.pdf` as "This is the complete and updated PRESS checklist" (receipt `w1/R97ScoutSources-provenance-coverage.txt`, S226 href block; `grep -o 'href=…' fetch/S226.html` exit 0). So S226 is a second transcription of one upstream (the PRESS 2015 checklist as CADTH publishes it), not a second witness. Agreement counts measure transcription agreement, not independent confirmation.

**Finding F-P1 (provenance, C2 — fired).** The entry (lines 13–15) says: "The guideline statement itself and the CADTH Table 9 that both reprints derive from answered http 403". The captures do not say that:
- S225 says only `Derived from: McGowan J … PRESS Peer Review … 2015 Guideline Statement. J Clin Epidemiol. 2016 Jul;75:40-6` (capture lines 81–82).
- S226 names no Table 9; it links the CADTH 2016 Update Report (above).
- `grep -c -i 'table 9\|Table_9'` on both captures → `0` and `0`, exit 1 (receipt `w1/R97ScoutSources-provenance-coverage.txt`).
The Table 9 link lives only in S227's SOURCES row (the lane's own claim). "Both reprints derive from Table 9" is not in the opened bytes.

## 4. Frontier: other reachable routes (web search only, nothing fetched)

Receipt `w1/R97ScoutSources-web-leads.txt` (two queries, search results only):
- Guideline statement, J Clin Epidemiol 2016;75:40–46, DOI `10.1016/j.jclinepi.2016.01.021`, PMID 27005575: `https://www.jclinepi.com/article/S0895-4356(16)00058-5/fulltext`; `https://www.sciencedirect.com/science/article/pii/S0895435616000585`; `https://pubmed.ncbi.nlm.nih.gov/27005575/` (reported free article).
- CADTH PRESS E&E / Update Report 2016 (open PDF, the route S226 cites): `https://www.cda-amc.ca/sites/default/files/pdf/CP0015_PRESS_Update_Report_2016.pdf`; resource page `https://www.cda-amc.ca/press-peer-review-electronic-search-strategies`.
- **CADTH Table 10** (Search Submission and Peer Review Assessment; the operational reviewer form, not Table 9): `https://www.cda-amc.ca/sites/default/files/PRESS_Peer_Review_Electronic_Search_Strate/Table_10_PRESS.pdf`. The lane's round-97 pre-table probe of Table 10 answered http 403 (`corpus/SOURCES.md:421`, read by `sed -n 421p`, exit 0), so this route is likely blocked; not fetched.
- **CADTH report 477 appendices**, snippet "APPENDIX G: PRESS CHECKLIST": `https://www.cda-amc.ca/sites/default/files/PRESS_Peer_Review_Electronic_Search_Strate/Report%20477_PRESS_Peer%20Review%20of%20Electronic%20Search%20Strategies_Appendices.pdf` — a CADTH route to the checklist wording independent of Cochrane and Karolinska.
- Repository and archive copies (leads, unverified): `https://core.ac.uk/download/pdf/82048291.pdf` (the lane's round-97 "core.ac.uk copy" probe answered 403 at `corpus/SOURCES.md:421`, but SOURCES does not record that probe's URL, so whether it is this URL is unknown); `https://scholar.archive.org/fatcat/release/bf1fef9f-838c-4f92-b2f6-8aad9203be20`; `https://www.scribd.com/document/465338921/SEARCH-strategies-PIIS0895435616000585` (third-party upload, non-authoritative).

Not reached by search: the content of Table 9 (S227) itself.

## 5. Findings on the C2 entry (`corpus/knowledge/press-checklist-questions-r97.md`)

**F-C1 — stated corroboration count is wrong (K5 fired).** Lane cell of row "Citing": "12 of the 26 S225 quotes are not found verbatim in S226". Recount over the committed captures: verbatim 10/26 ⇒ **16 not verbatim**; 12 is the count not found under *letters* (14/26). Command: `python3 -B -c '<recount>'` in `repo` (exit 0). Receipt `w1/R97ScoutSources-recount.txt` (`verbatim in S226: 10 / 26   not verbatim: 16`; `letters in S226: 14 / 26   not letters: 12`).

**F-C2 — the stated breakdown of the 12 is miscounted (K5 fired).** "Of the 12 not found under letters, 5 are element headings … one is S225's own pointer (L1), one the PRESS checklist title (L2), and five are questions where the wording itself differs". Recount of the 12: element headings **6** (L3, L8, L11, L14, L18, L23), L1 and L2 (2), wording **4** (L12, L13, L15, L20). Sum 12 is right, the split is wrong, and the entry's own list names only four wording items. Receipt `w1/R97ScoutSources-recount.txt` (not-letters list, exit 0).

**F-C3 — coverage overstated (scope).** The entry says "This entry holds the checklist's questions under each of the six elements" and its title promises "what a peer reviewer … asks, element by element". S225 prints **33** question-ending lines (grep: 36 lines contain `?`); the entry locates **16** of them. Unquoted S225 questions include "Are the search concepts clear?" (line 35), "Is the use of nesting with brackets appropriate…?" (43), "Does the search include all synonyms or antonyms (eg, opposites)?" (61), "Are major headings … used?" (53), "Are the keywords specific enough…?" (65) and "Are any potentially helpful limits or filters missing?" (78) — 18 lines (17 questions and one continuation). No named limit says the 26 quotes are a selection. Receipt `w1/R97ScoutSources-s225-s226-compare-coverage.txt` (`S225 question-ending lines NOT among entry's located quotes: 18`), exit 0. The rows' Do/Never cells do not claim completeness; the title and the scope sentence do.

**F-C4 — one line numbers and word count (see F-Q1)**: "capture line 74" → 73; "32-word" → 30.

**F-C5 — "independent reprint" (see §3).** Entry line 13: "a second, independent reprint (S226)". S226 links CADTH's 2016 update report as its source; independence holds only from Cochrane's host, not from the checklist's origin.

**F-C6 — row 1 Never is not in its warrants (K2 borderline).** Never: "review the syntax of a strategy without first reading the question it is meant to answer". Warrants L3, L4, L5, L7 say the strategy must match the question and be explained; none gives an order of reading. This is a lane gloss, not a quote. Not counted as K2-fired in this verdict, noted for the wave reviewer.

**Observation (not a finding against a claim):** Lane cell "the lane's `## Searches` record files one count per expression (`hits`), which is its form of hits per line" equates one count per single-expression search with "hits per line". It holds only where a record has no combined lines, which the same row concedes; a reviewer may read it as a stretch.

## 6. What held

- S225 `pdftotext -layout` = capture, byte-identical (`cmp` rc 0; `w1/R97ScoutSources-S225-pdftotext-S226-recipe.txt`).
- Raw sha for S225 matches refetch row; S227 HTTP 403 / rc 22 matches refetch row; S226 text form matches capture across two fetches.
- Predicate numbers 10/26 verbatim and 14/26 letters recompute exactly (recount receipt).
- All 26 S225 quotes each occur on exactly one capture line; no quote is joined across lines except as the entry states for L21/L22 (line number aside).
- "two-page landscape PDF": `pdfinfo` → `Pages: 2`, `Page size: 841.68 x 595.2 pts (A4)` (landscape), exit 0.
- S227 is correctly rejected as unreachable for the stated reason (Cloudflare challenge page; http 403).

## 7. Caveats

- S226 raw hash cannot be reproduced; I did not find which fetch argv produced `777b890f…`. The entry's raw hash is not a reliable identity marker; the text form is.
- I did not open any web lead; leads are search-result text only.
- Ran nothing against the lane's gate or search tools (other seats hold predicate 1–4 and C1).

## Claims touched

VERDICT: R97ScoutSources C1 n/a — not in this seat's source re-open scope; the self-test battery was not run and no C1 receipt is cited.
VERDICT: R97ScoutSources C2 fired — the entry states a corroboration count (12 not verbatim; the correct figure is 16) and a split of the 12 (5 headings / 5 wording; correct 6 / 4), locates L21/L22 on line 74 with 32 words (correct line 73, 30 words), says both reprints derive from CADTH Table 9 (neither capture names it; S225 derives from the McGowan guideline statement), and presents 16 of 33 S225 question lines as "the checklist's questions … element by element"; the quoted text itself reproduces and the 10/26 and 14/26 predicate numbers hold.
