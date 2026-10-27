# R53GroundJmlaA — re-ground staged S134 → planned lane S117

seat `R53GroundJmlaA` (leaf; no dispatch). Lane tip `6365f15`; claims frozen `a6ff732`; candidate `32aab5e`. Read-only sources: `.qcache/0ae65ac01b93119d3c2f3fed.{raw,txt}`; staged entry `merge/chousa/knowledge/corpus/knowledge/search-tracking-record-r40.md`; staged row `merge/chousa/SOURCES.append.md:59`. No network, no install, no lane write except this report.

## 1. Capture integrity (faithful text form; U+FFFD = 0)

```text
$ ls -l .qcache/0ae65ac0….raw .qcache/0ae65ac0….txt
-rw-r--r-- 252991 … 0ae65ac01b93119d3c2f3fed.raw
-rw-r--r--  27737 … 0ae65ac01b93119d3c2f3fed.txt
$ file ….raw            -> PDF document, version 1.7, 5 page(s)
$ pdfinfo ….raw         -> Pages: 5; Producer: Microsoft Word for Microsoft 365; 612 x 792 pts
$ python3: len(text)=27659 chars, 325 lines, text.count('\ufffd')=0
$ sha256sum ….raw ….txt
c2aa0e12d45f33d01739952b858259fc97c14ab43be618cf865fcb5eededaf91  ….raw
1e185358c52c3c8ba90970dd79a624df1e532841aa0a9ccb7be738236be9971d  ….txt
$ pdftotext -layout ….raw $S/pdftotext-layout.txt && cmp -s $S/pdftotext-layout.txt ….txt
IDENTICAL layout
$ sha256sum $S/pdftotext-layout.txt ….txt
1e185358c52c3c8ba90970dd79a624df1e532841aa0a9ccb7be738236be9971d  (both)
$ python3 -c 'sha256("https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061")[:24]'
0ae65ac01b93119d3c2f3fed
```

The `.txt` is byte-identical to `pdftotext -layout` of the `.raw` (27,737 B, same digest): a faithful text form; zero replacement characters; curly quotes and `110 (2) April 2022` footers preserved. Cache key = sha256(URL)[:24].

## 2. Staged row and staged entry

- `SOURCES.append.md:59` is the only row for this URL (`grep -c` → 1): “PRISMA 2020 and PRISMA-S: common questions on tracking records and the flow diagram (Rethlefsen ML, Page MJ)”, `Journal of the Medical Library Association 110(2):253-257, doi 10.5195/jmla.2022.1449`, tier `A`, read 2026-10-23.
- The only staged entry citing `S134` is `search-tracking-record-r40.md` (lines 4, 16, 21). No twin entry/row for this document exists in the campaign package.

## 3. Identity stamp in the `.txt`

| field | text | offset |
|---|---|---|
| title | `PRISMA 2020 and PRISMA-S: common questions on` / `tracking records and the flow diagram` | 401 / 447 |
| authors | `Melissa L. Rethlefsen, AHIP; Matthew J. Page` (once) | 485 |
| journal | `Journal of the Medical Library Association` (5×, first) | 7056 |
| volume/date | `110 (2) April 2022` (5×, first) | 7033 |
| DOI | `DOI: dx.doi.org/10.5195/jmla.2022.1449` (5×, first) | 358 |
| pages | 253 header @136; `254    Rethlefsen and Page` @7100; `…255` @12206; `256    Rethlefsen and Page` @19079; `…257` @25833 | 136-25833 |

All match the staged identity (`J Med Libr Assoc 2022;110(2):253-257`, doi `10.5195/jmla.2022.1449`, Rethlefsen & Page); `pdfinfo` 5 pages = 253-257.

## 4. Every staged-entry claim that rests on this document

| # | claim (first 80 chars) | verdict | located quote @ offset |
|---|---|---|---|
| 1 | PRISMA-S asks for the strategy for every source, and a count for each source. | located | `to report search strategies for all databases, registries, and websites that were searched.` @1196 + `reporting the number of records identified from each information source.` @1320 (two pieces; no one-line quote carries both) |
| 2 | The paper records the change from PRISMA 2009 as "the recommendation to report s | located-narrower | `to report search strategies for all databases, registries, and websites that were searched.` @1196; “the recommendation” sits on the previous line |
| 3 | and states that "PRISMA-S also recommends reporting the number of records identi | located-narrower | `PRISMA-S also recommends` @1288 + `reporting the number of records identified from each information source.` @1320; wraps after `recommends` |
| 4 | The flow diagram's columns are allocated by where the record came from. | located-narrower | `different columns: identification of studies via databases` @5272 + `and registers (Column 1) and identification of studies via` @5453 |
| 5 | Records identified from websites, organizations, citation searching and other me | located-narrower | `that records identified from websites, organizations,` @6180 + `citation searching, and other methods should be reported` @6355 + `in Column 2. The flow diagram template also suggests` @6544 |
| 6 | while the flow diagram template "also suggests reporting an overall number for r | located-narrower | `in Column 2. The flow diagram template also suggests` @6544 + `reporting an overall number for records identified from` @6720 + `databases and registers in Column 1.` @6893 |
| 7 | This is the answer to a question the lane could not previously answer: a trackin | located-narrower | two-column tracking @5272/@5453; “routed”/“flat list” are lane terms, not paper words |
| 8 | PRISMA 2020's flow diagram separates what the databases and registers returned f | located-narrower | @6180 + @6355 + @6544 + `databases and registers in Column 1.` @6893 (split over column lines) |
| 9 | The count and the strategy are per source, which is what makes a sweep re-runnab | located-narrower | @1196 + @1320; “re-runnable” is the entry’s inference |
| 10 | "the number of records identified from each information source" is a per-source | located | `reporting the number of records identified from each information source.` @1320 |
| 11 | PRISMA-S's per-strategy date (round 1's S069) makes the tally meaningful at a p | absent | `per-strategy`/`strategy date`/`search date` all 0 in the `.txt`; the sentence attributes the date to S069 |
| 12 | Column 2 is where the lane's unverifiable hops live. | located-narrower | `in Column 2. The flow diagram template also suggests` @6544 + `other methods (Column 2). The flow diagram itself` @5636; “unverifiable hops” is lane framing |
| 13 | Citation searching and "other methods" are reported in the column the flow diag | located-narrower | @6180 + @6355 + @6544; the “structural reason … cannot be closed” clause is not in the paper |
| 14 | Whether the paper gives a field-level specification of a tracking record was no | located-narrower | `In the rest of this commentary, we` @10046 (+ `will answer some of the most common ones.` @line 130); “not a checklist” is the entry’s negative check |
| 15 | The paper is the PRISMA-S authors' own commentary and is not itself a reporting | located-narrower | `COMMENTARY` @252 + `Melissa L. Rethlefsen, AHIP; Matthew J. Page` @485; “not itself a reporting standard” is inference |
| 16 | recheck: re-download the PDF and confirm the sentence still reads "PRISMA-S als | located-narrower | byte-exact 0; whitespace-collapsed 1; break-free pieces @1288 and @1320 |
| 17 | That split is the same distinction the lane's own corpus keeps drawing between a | absent | rests on S094/S114/S130; no local-copy/URL or Chinese/Japanese sentence here |
| 18 | No non-Western analogue of a tracking-record allocation was found; the Chinese a | absent | a negative claim about the corpus, not a statement in this paper |

## 5. QUOTE machine lines (planned lane id S117; entry path that will cite it)

```text
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	to report search strategies for all databases, registries, and websites that were searched.	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	PRISMA-S also recommends	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	reporting the number of records identified from each information source.	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	that records identified from websites, organizations,	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	citation searching, and other methods should be reported	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	in Column 2. The flow diagram template also suggests	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	reporting an overall number for records identified from	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	databases and registers in Column 1.	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	In the rest of this commentary, we	corpus/knowledge/search-tracking-record-r40.md
QUOTE	S117	https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061	Best practice is to count all records identified (by	corpus/knowledge/search-tracking-record-r40.md
```

Each checked with `python3 text.find(q)` on the whole `.txt`: count 1, on one line, 7-13 whitespace words, 34-91 characters. Line 130 (`will answer some of the most common ones.`, count 1) continues #14.

## 6. Conflicts / findings (reported, not patched)

1. **Recheck quote still not located.** The full sentence occurs **0** times byte-exact in the `.txt` and 1 whitespace-collapsed; re-cut to @1320 (+@1288), as r52 concluded.
2. **Offset conflict, verbatim.** `corpus/lessons/round-52.md:62`: “sentence located once at char 935 (`number of records identified from each information source`)”; `R52DraftGateTable.md:54`: “`0ae65ac0….txt` char 935 = `number of records identified from each information source`, count 1”. On the `.txt` sidecar the string is at **1334** (`reporting the number … source.` at 1320); 935/936 is the *default* `pdftotext` form (936 and 922). Any span built from 935 over the `.txt` is wrong.
3. **Claims 11 and 17-18 are not grounded in S134.** The per-strategy date is S069’s; the local-copy/URL and Chinese/Japanese splits are S094/S114/S130’s; the non-Western absence is the entry’s sweep. The entry keeps those ids explicit — attribution note, not a false citation.
4. **Identity/page range confirmed**; the staged row’s source cell needs no change. `COMMENTARY` @252 supports #15’s “commentary” but not “not itself a reporting standard” (inference).
5. **No contradiction.** Every substantive S134-pointing claim has its wording present; absent items are attributed elsewhere or are absence claims.

## 7. Touched surfaces / limits

- Wrote only this report; no entry, registry, lesson, counter, adopter or capture modified; no git/jj mutation; no network; no install. Scratch `/fast/scratch/hyaku/chousa-r53/R53GroundJmlaA/` removed before finishing.
- Not run (out of scope): `c1-count.py`, `c2-count.py`, `build-spans.py`, `inference-ground.py`. Entry still cites `S134`; integration to `S117` is the L1’s edit.
- Limit: quote verdicts are string-level (binding/presence, not entailment); `located-narrower` marks support split across `.txt` line breaks, not a claim the paper fails to make.

VERDICT: re-grounded JMLA S134 → S117 — identity, 10 located break-free quotes and 18 claim verdicts recorded; the recheck sentence is not byte-locatable and r52’s “char 935” is an offset in the wrong text form (default pdftotext, not the `-layout` sidecar, where it is 1334).
