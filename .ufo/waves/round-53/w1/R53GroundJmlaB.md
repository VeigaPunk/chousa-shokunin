# R53GroundJmlaB — independent second pass: staged S134 → planned lane S117

Grounder seat, round 53 wave 1 (chousa). Read the frozen claims first (`corpus/evidence/round53/claims.md` at `a6ff732c`); no predicate, target, counter or control touched. Read no other seat's report (`R53GroundJmlaA` was not opened). Lane repo read-only: `git rev-parse HEAD` in the lane printed `6365f15b64b89d1ad1ac66fe7d7b81c92e74d90f`. Nothing written outside this report; all scratch deleted (section 7).

## 1. Capture, key, identity stamp

Capture: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/0ae65ac01b93119d3c2f3fed.txt`. Key checked: `sha256("https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061")` = `0ae65ac01b93119d3c2f3fed266b0d…`; first 24 hex = the file stem. Text form read as UTF-8: 27,659 chars, 325 newlines, sha256 `1e185358c52c3c8ba90970dd79a624df1e532841aa0a9ccb7be738236be9971d` (27,737 bytes). `.raw` is byte-identical to `.pdf` (both sha256 `c2aa0e12d45f33d01739952b858259fc97c14ab43be618cf865fcb5eededaf91`, `%PDF-1.7`, `/Producer(Microsoft Word for Microsoft 365) /CreationDate(D:20220325150751-05'00')`), so the `.txt` sidecar is the only usable text form; every offset below is a character offset in it.

Identity stamp (`text.count` / `text.find`, whole file; `off` = char offset):

- **title** `PRISMA 2020 and PRISMA-S: common questions on` (count 1, L8, off 401) + `tracking records and the flow diagram` (count 1, L9, off 447) — spans a break.
- **date / edition** `110 (2) April 2022` (JMLA vol. 110 no. 2; count 5, L89, off 7033); `Received November 2021; accepted November 2021` (count 1, L308, off 26553); page markers `253`(L1 running head)/`254`/`255`/`256`/`257` → pp. 253–257.
- **host** `jmla.mlanet.org` (count 5, L89, off 6985); download host `jmla.pitt.edu` **count 0**.
- **author** `Melissa L. Rethlefsen, AHIP; Matthew J. Page` (count 1, L10, off 485); affiliations `Professor, Health Sciences Library & Informatics Center, University of` (L299, off 26197; Albuquerque NM L300) and `of Public Health and Preventive Medicine, Monash University,` (L304, off 26469; Melbourne L305); emails `mlrethlefsen@gmail.com` (L297) / `matthew.page@monash.edu` (L301); ORCIDs `…0001-5322-9368` (L298) / `…0002-4242-7526` (L302).
- **publication** `COMMENTARY` (L2, off 252); `DOI: dx.doi.org/10.5195/jmla.2022.1449` (count 5, L3, off 358); `ISSN 1558-9439 (Online)` (L321, off 27515); `This journal is published by the University Library System` (L316, off 26974) + `of the University of Pittsburgh as part of its D-Scribe` (L317, off 27122).

Reading: a two-author JMLA commentary at 110(2):253–257, April 2022, doi 10.5195/jmla.2022.1449, ISSN 1558-9439, published by the University Library System of the University of Pittsburgh (D-Scribe). The URL host `jmla.pitt.edu` is never in the text: the host the document stamps is `jmla.mlanet.org`, and only the publisher statement ties the Pitt OJS download to the text.

## 2. Eight located quotes (none is a title/abstract/headline sentence)

Each occurs exactly once in the `.txt` (`text.count == 1`), inside ONE line, ≤25 whitespace words, ≤160 chars. `off` = `text.find` on the whole file.

| # | quote | line | off | words | chars |
|---|---|---|---|---|---|
| q1 | `Best practice is to count all records identified (by` | 205 | 17488 | 9 | 52 |
| q2 | `per database across the lifespan of the systematic review` | 243 | 20387 | 9 | 57 |
| q3 | `PRISMA-S treats all results from the same search,` | 238 | 19789 | 8 | 49 |
| q4 | `Google Scholar is both a database and a citation index, and` | 160 | 12842 | 11 | 59 |
| q5 | `number of records identified for each individual database` | 204 | 17424 | 8 | 57 |
| q6 | `all records identified outside of databases and study` | 128 | 10157 | 8 | 53 |
| q7 | `records identified should be reported per search in the` | 168 | 13696 | 9 | 55 |
| q8 | `Column 1 contains all data related to records and studies` | 124 | 9768 | 10 | 57 |

Each is a line-local span whose sentence continues across the PDF break; shown so a fragment is not read as a whole sentence:

```
L204|   number of records identified for each individual database    <- q5
L205|   Best practice is to count all records identified (by         <- q1
L206|   and information source should be reported, however, in
L238|   PRISMA-S treats all results from the same search,            <- q3
L240|   regardless of whether it was the original search or an
L243|   per database across the lifespan of the systematic review    <- q2
L124|   Column 1 contains all data related to records and studies    <- q8
L126|   identified in study registries, and Column 2 now contains
L128|   all records identified outside of databases and study        <- q6
```

Substance: q5+q8+q6 = the two-column routing rule (database/registry records in Column 1, everything else in Column 2); q7 = per-search record counts in the supplementary materials; q1 = count every record from every source; q3+q2 = a rerun/update is the same data point, tallied per database across the review's lifespan; q4 = Google Scholar is a database and a citation index at once. Headline strings deliberately avoided (counted, unused): `reporting the number of records identified from each information source` (count 1, off 1320, L22) and `report search strategies for all databases, registries, and websites that were searched` (count 1, off 1199, L21) — each lead-in sits on the previous line.

## 3. Machine lines (planned LANE id S117)

```
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	Best practice is to count all records identified (by	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	per database across the lifespan of the systematic review	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	PRISMA-S treats all results from the same search,	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	Google Scholar is both a database and a citation index, and	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	number of records identified for each individual database	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	all records identified outside of databases and study	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	records identified should be reported per search in the	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	Column 1 contains all data related to records and studies	corpus/knowledge/search-tracking-record-r40.md
```

## 4. Span-build receipt (scratch root; no lane file written)

`build-spans.py --root` was pointed at a scratch evidence dir, so the derivation was run, not asserted:

```
python3 chousa-shokunin/corpus/evidence/round53/build-spans.py --root $S/lane --cache <qcache>
QUOTE S117 char 17488 spans/S117-1.txt
QUOTE S117 char 20387 spans/S117-2.txt
QUOTE S117 char 19789 spans/S117-3.txt
QUOTE S117 char 12842 spans/S117-4.txt
QUOTE S117 char 17424 spans/S117-5.txt
QUOTE S117 char 10157 spans/S117-6.txt
QUOTE S117 char 13696 spans/S117-7.txt
QUOTE S117 char 9768 spans/S117-8.txt
SPANS_ROWS=8 WRITTEN=8
exit=0
```

Every `char N` equals the section-2 `off`; every manifest row carries `capture_sha256 = 1e185358c52c3c8ba90970dd79a624df1e532841aa0a9ccb7be738236be9971d` and `offset = char − 80`. These eight rows are span-ready as they stand.

## 5. Negative sweeps — `text.count` on the UTF-8 `.txt`

Required terms, exact counts:

```
tracking record 2 | each information source 2 | number of records 11 | PRISMA-S 27
PRISMA 2020 40 | information specialist 0 | librarian 0 | unpublished 0
grey literature 0 | 检索 0 | 检索策略 0 | 检索日期 0 | 灰色文献 0 | 未发表 0
PRISMA 92 | 数据库 0
```

Variants run to keep the negatives honest:

```
tracking records 2 | information specialists 0 | specialist 0 | librarians 0 | Librarian 0
gray literature 0 | preprint 0 | search strategies 1 | search strategy 0 | last searched 0
date searched 0 | MEDLINE 0 | PubMed 0 | Embase 0 | Web of Science 0 | CNKI 0 | 知网 0
万方 0 | CiNii 0 | Cochrane 0 | http 9
```

ABSENT (count 0), hence not claimable by any entry: `information specialist`, `librarian`, `unpublished`, `grey literature`/`gray literature`, every Chinese-script term tried, every named database, and the PRISMA-S date field in words (`last searched`, `date searched`, singular `search strategy`). Two nonzero counts are substring artifacts, not extra content: `tracking record` 2 = the two plural `tracking records` (singular count equals plural count; hits at L9 and L24 only), and `each information source` 2 = L22 abstract + L118.

## 6. Findings for the L1 (reported, not patched)

1. **The packaged staged entry's quotes do not survive as spans.** The read-only package copy `merge/chousa/knowledge/corpus/knowledge/search-tracking-record-r40.md` holds 7 distinct quoted strings; against the `.txt` (markdown soft-wrap collapsed) with `text.count` and a `\s+` regex: `PRISMA-S also recommends reporting the number of records identified from each information source` raw=0/ws=1; `the recommendation to report search strategies for all databases, registries, and websites that were searched` raw=0/ws=1; `should be reported in Column 2` raw=0/ws=0; `also suggests reporting an overall number for records identified from databases and registers in Column 1` raw=0/ws=0; `the number of records identified from each information source` raw=1; `other methods` raw=4 (non-unique); `PRISMA-style search logs` raw=0 (the lane's own term, correctly not a document quote). Ported as-is, S117 yields at most one unique located quote — short of the frozen C2 bar of ≥3 per bound id. Section 2's eight quotes are line-local and clear the bar.
2. **Binding relies on the publisher statement, not the URL string.** `jmla.pitt.edu` count 0 vs `jmla.mlanet.org` count 5; the tie is L316–317 (`University Library System` / `of the University of Pittsburgh as part of its D-Scribe`).
3. **Source-generic document.** It counts records per information source and routes them by column but names no database and no librarian/information specialist (all 0 above); with every Chinese term 0, it cannot be cited for any Chinese or Japanese requirement.
4. **Cross-break traps.** Title (L8→L9), the licence name (`Creative Commons Attribution 4.0 International License`, count 0 — it breaks after `(CC BY 4.0)`), and the staged entry's recheck sentence all straddle PDF line breaks; quoted whole they are refused by `build-spans.py`. Cut at the break, as section 2 does.
5. **Baseline (read-only).** Lane `corpus/SOURCES.md` at `6365f15b` has 116 `S###` rows, max `S116`, none containing `1449/2061`; the lane has no `corpus/knowledge/search-tracking-record-r40.md`. S117 is free and the binding row would be new since `5b550133…`, consistent with the frozen C2 clause. I did not write the row.

## 7. Limits and scratch

I did not run `c1-count.py`, `c2-count.py`, `inference-ground.py` or `quote-substance-check.py` — none of them has passed by my hand; they are the L1's integration checks. The `.raw` was not decoded (byte-identical PDF) and pdftotext was not run. Offsets are characters in the UTF-8 `.txt`, not bytes. No network; every source is the on-disk capture. No tool installed or upgraded (pacman paused host-wide; nothing needed). `/fast/scratch/hyaku/chousa-r53/R53GroundJmlaB/` (TMPDIR for every command: quote probe, identity/sweep receipt, entry re-quote probe, span-build lane copy) was removed after this report was written; its receipts are pasted verbatim above.

VERDICT: attacked the S134 capture as an independent second pass and built eight line-local, exactly-once, span-verified quotes with offsets plus a full identity stamp and 16 negative sweeps — and found the packaged staged entry's own quoted strings are not byte-contiguous in the `.txt` (5 of 7 raw=0, one non-unique), so the planned S117 entry needs these quotes rather than its round-52 re-wraps.
