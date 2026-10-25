# ReviewQuotePaper404 — paper capture quote review

Seat: L1Chousa45.ReviewQuotePaper404 (reviewer, leaf). Round 45 wave 1.
Assignment: locate `Archive.org returns a 404 page for these` in the paper capture
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/412b146a2720ce6557268d05.txt`,
report sha256, char offset (Python str.find), occurrence count, 500 chars verbatim context,
and answer what/whose/where. No fetches performed (fetch-scope L0 open); on-disk capture only.

## Commands run (verbatim, trimmed)

1. `sha256sum .../412b146a2720ce6557268d05.txt && wc -c .../412b146a2720ce6557268d05.txt`
   -> `a3ff65e0db9cc4f2178932ce53965e4cba60c6aab0ba3b1d4ce40020a8a7cf8f` / `145088` bytes.
2. grep `Archive\.org returns a 404 page for these` (capture) -> single hit at L3965-3966.
3. Python (eval): `s.find(q)` loop, case-insensitive counts, heading scan, raw line dump.

## Findings

- **sha256 (capture file):** `a3ff65e0db9cc4f2178932ce53965e4cba60c6aab0ba3b1d4ce40020a8a7cf8f`
- **Occurrences:** exactly **1** (exact string; also 1 case-insensitive; "returns a 404 page" appears once in the whole text)
- **Offset (Python str.find, 0-based):** **120884**
- **Line:** raw text line **3966** (sentence spans L3965-3967)

### Context verbatim (500 chars, 250 before + 250 after offset)

```
: For persistence, we have stored all fact-checking articles on archive.org. Fact-checking articles may feature d̈ouble-archivedl̈inks using both archive.org and archive.is, e.g.
 https://web.archive.org/web/20201229212702/https://archive.md/28fMd . Archive.org returns a 404 page for these. To view such a link, please just copy-paste the archive.is part (e.g. 
 https://archive.md/28fMd ) into your browser.




 9. 
 
 Answers should be accompanied by a hyperlink to the source, and the type of th
```
(Note: `d̈ouble-archivedl̈inks` is the capture's rendering of "double-archived links"; combining diaeresis artifacts, reproduced above.)

## Analysis

- **WHAT returns a 404:** archive.org (web.archive.org) — per the text, Archive.org returns a 404 for *double-archived links*, i.e. URLs of the form `https://web.archive.org/web/<ts>/https://archive.md/<id>` (an archive.org snapshot *of* an archive.is/archive.md page). The example given is `https://web.archive.org/web/20201229212702/https://archive.md/28fMd`. The guideline instructs annotators to copy-paste the `archive.is` part into the browser instead.
- **WHOSE links:** hyperlinks inside **fact-checking articles** — the primary evidence sources (phase-1 articles) that the campaign stored on archive.org ("we have stored all fact-checking articles on archive.org"; the links feature both archive.org and archive.is/archive.md archival copies). They are the evidence-page links annotators consult in Phase 2, not the claim URLs.
- **WHERE:** **Appendix J (Annotation Guidelines)**, section **J.4 Phase 2: Question Generation and Answering**, subsection **J.4.1 Overview**, numbered guideline item **8** (list items 1-11; item 8 = L3963-3967; item 9 follows at L3972). It is **not** main text. Appendix J begins at L3226 ("Appendix J Annotation Guidelines"); J.4 heading at L3892; J.4.1 at L3904.

## Verdict

Quote located exactly once, as assigned. The strongest reading the text supports: the annotation guidelines state that double-archived links (archive.org snapshots of archive.is/archive.md pages) found inside stored fact-checking articles yield a 404 when their archive.org URL is opened, and annotators should instead use the embedded archive.is part. That is the paper's own claim about observable link behavior; this review does not verify the real-world 404 behavior (out of scope, no fetch).

## Pointers

- Capture: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/412b146a2720ce6557268d05.txt` (sha256 `a3ff65e0db9cc4f2178932ce53965e4cba60c6aab0ba3b1d4ce40020a8a7cf8f`), str.find offset 120884, line 3966, sentence L3965-3967.
- Section anchors: Appendix J at line 3226; J.4 at 3892; J.4.1 at 3904; item 8 at 3963-3967.
- Report: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-45/w1/ReviewQuotePaper404.md`.
- No tools installed; no fetches; no writes outside this report.
