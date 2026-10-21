# Garner et al. 2016 — source opening (round 26)

## Access and duplicate check
- The prior `corpus/SOURCES.md` search log records BMJ's article URL as HTTP 403 (lines 115–119, 142–143). Official open copy opened: `https://pmc.ncbi.nlm.nih.gov/articles/PMC4955793/` — `curl -sS -L` returned HTTP 200, final URL unchanged, 238,623 bytes; the page reader returned the article itself. Europe PMC official full-text mirror `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4955793/fullTextXML` also returned HTTP 200, final URL unchanged, 129,430 bytes.
- PMC identifies “When and how to update systematic reviews: consensus and checklist,” Garner et al., *BMJ* 2016;354:i3507, published 2016-07-20, DOI 10.1136/bmj.i3507, PMCID PMC4955793. PMC marks the article as corrected; quote below is from the accessible full-text page.
- No duplicate registry row: the current observed `SOURCES.md` registry is S001–S039 (lines 7–49); Garner appears only in the old excluded-candidate note and lead (lines 115–119, 142–143). S040 was the next unused ID in that read; ID is left TBD as assigned.

## Located quote
> “How often this surveillance is done, and which approaches to use, depend on the circumstances and the topic.”

Location: “Step 2: identify relevant new methods, studies, and other information” → “Are there any new studies or other information?” in the PMC full text. (18 words.) The surrounding paragraph concerns routine surveillance for potentially relevant new studies in systematic reviews and says topic/evidence pace affects how often it occurs.

## Proposed SOURCES.md contract-v1 row
ID retained as TBD for integration; row uses the 11 contract-v1 columns (`CORPUS.md`:86–108).

| TBD | Garner et al. 2016, “When and how to update systematic reviews: consensus and checklist” — https://pmc.ncbi.nlm.nih.gov/articles/PMC4955793/ | paper | A | the paper's recommendation on how often review teams surveil for potentially relevant new studies in systematic reviews; frequency depends on circumstances and topic | Step 2: identify relevant new methods, studies, and other information → “Are there any new studies or other information?”; *BMJ* 2016;354:i3507, published 2016-07-20 | For systematic-review surveillance, search frequency depends on circumstances and topic; no universal interval is claimed | queued | 2026-10-21 | 365d | — |

Tier A is scoped to an original consensus paper's own recommendation, not general metadata policy (`CORPUS.md`:93–97). Status is queued because opened and worth mining, but no knowledge/lesson currently cites this row; flip to mined only after an in-scope citation and matching `used-by` path are recorded. `365d` is a proposed registry source-recheck cadence, not Garner's surveillance interval. The contract requires a quote with location in the round gate (`CORPUS.md`:112–115).

## Scope limits / what this source does not support
- It does not give a universal numeric interval, a generic record due-date formula, or a rule for applying systematic-review surveillance cadence to every research note or source. Its interval advice is conditional on review circumstances/topic; carrying it over to chousa metadata is an inference.
- It does not establish that a source's claim is true, nor that opening or topical relevance alone verifies a claim. Keep source existence, topicality, source statement, and truth distinct (`corpus/QUALITY.md`:24–32; criteria 7–8). It does not itself prescribe the lane's `due=`/`freshness=` fields or a 90-day cadence.

Installs: none.