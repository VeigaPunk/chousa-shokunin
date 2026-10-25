# ScribeGateBlock — round 43, wave 1

Seat: chousa leaf scribe. Measured commit `737f40b6aa8f37ffe2269db370fd6d65a720d9a8` (`git rev-parse HEAD` matched; subject `round-43: split the absent class and adopt one locally re-opened search-log entry`). Lesson file was read and not edited. No fetch. No shokuknow tool. No production edit. The 1/2 bound was not retuned.

Axes walked: operability (C1 and the missing-tool control), calibration (C2, `--flip S086`, offset unit, contiguity definition), depth (C3 and the admitted/rejected spans in the committed captures).

## Behavior

Read `corpus/lessons/round-43.md` Gate admitted and rejected sections and checked those sentences against local files. Ran the frozen counters from the lane root. Did not treat committed receipts, sibling seat files, or the lesson's own measurement sentences as this seat's execution.

## Gates

### Verbatim — admitted and rejected

Quoted from `corpus/lessons/round-43.md` lines 31–39 and 41–45. Not rewritten.

```
### Admitted

`corpus/knowledge/search-log-method-r39.md`, citing S078. The filename is the package's label. The source is the Europe PMC full-text XML of Bramer et al. 2018, opened from the committed capture, not fetched.

Located quote (12 words), access 2026-10-24: "to register the steps taken and to make searches accountable and reproducible."
URL: `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6148622/fullTextXML`
Capture: `.qcache/2cef078d8f9f87802e19e770.txt`, sha256 `833b13e3e80212522d016a8db9c6edeacb8965148d2334722a7a73c415d7136d`, byte offset 17383.

Also located in the same capture, not fetched: "Any change to the search strategy should be done in the log document" and "checking searches for their recall is advised".

### Rejected

- `search-log-fields-r36.md` (the three-literatures candidate). Reason: staged S077's local capture is a 267-byte / 265-character Client Challenge, not the PRISMA-S article, and the Japanese capture does not contain 参照日. A row that cites an unreopened source is not admitted. Flip: the fetch-scope ruling is answered and a capture of each cited source contains the quoted sentences.
- `search-tracking-record-r40.md`. Reason: "should be reported in Column 2" is not a contiguous span in the committed pdftotext capture, so the column claim cannot be re-grounded. Two other sentences in that capture are contiguous; they are not enough to admit the column claim. Flip: a rendering in which that sentence is contiguous.
- The rest of the package. Reason: one theme, and only the rows an admitted entry cites are appended. Flip: a later round re-grounds another theme from local captures, or the fetch ruling opens the rest.
```

Registry changes, id collision, and the non-author spot-check bullet are outside this quote. They were not edited.

### Commands this seat ran

Working directory `/home/vgpnk/Projects/shokunin/chousa-shokunin`. Exit codes are the shell `EXIT:` lines.

`python3 corpus/evidence/round43/c1-count.py`

```
TABLE_ABSENT PASS 15/15
TOOL_EXIT PASS exit=0
ABSENT_ENUMERATED PASS 15/15
CLASSED PASS 15/15
BOTH_NONEMPTY PASS misquote=9 not-carried=6
REPRODUCIBLE PASS identical=True
MUTANT_DETECTED PASS short=14 expected=15
ABSENT_ENUMERATED=15/15
CLASSED=15/15
BOTH_NONEMPTY=1/1
REPRODUCIBLE=1/1
MUTANT_DETECTED=1/1
C1=PASS
EXIT:0
```

`python3 corpus/evidence/round43/c2-count.py`

```
SPLIT_AGREES=15/15
VOCAB_OK=15/15
MISMATCHES=0
C2=PASS
EXIT:0
```

`python3 corpus/evidence/round43/c2-count.py --flip S086`

```
SPLIT_AGREES=14/15
VOCAB_OK=15/15
MISMATCHES=1
MISMATCH S086 table=misquote independent=not-carried
C2=FAIL
EXIT:1
```

`python3 corpus/evidence/round43/c3-count.py`

```
ENTRY_CITES=1/1
QUOTE_LOCATED=1/1
URL_MATCH=1/1
C3=PASS
EXIT:0
```

`python3 corpus/evidence/round43/c1-count.py --tool /tmp/no-such-absent-split.py`

```
TABLE_ABSENT PASS 15/15
TOOL_PRESENT FAIL missing /tmp/no-such-absent-split.py
C1=FAIL
C1_CONTROL_EXIT:1
```

`python3 corpus/evidence/round43/c3-count.py --entry /tmp/no-such-entry.md`

```
ENTRY_CITES=0/1
QUOTE_LOCATED=0/1
URL_MATCH=0/1
C3=FAIL entry-missing
C3_CONTROL_EXIT:1
```

`printf '%s\n' 'to register the steps taken and to make searches accountable and reproducible.' | wc -w` → `12`.

C1=PASS, SPLIT_AGREES=15/15, flip exit 1, and C3=PASS were observed here. The bound was not changed after those scores.

### Local capture checks (no fetch)

Europe PMC file, keyed by sha256 of the Gate URL, first 24 hex digits:

`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/2cef078d8f9f87802e19e770.txt`

- exists, 80107 bytes
- sha256 `833b13e3e80212522d016a8db9c6edeacb8965148d2334722a7a73c415d7136d` (matches the Gate)
- lane-relative `.qcache/2cef078d8f9f87802e19e770.txt` does not exist (`lane_relative_exists False`)
- the 12-word quote including the period is a raw substring
- character offset of that quote: 17383
- byte offset of that quote: 17410
- bytes at file offset 17383: `ly in the database itself, to register t`
- character slice at 17383 is the quote
- `Any change to the search strategy should be done in the log document` found at byte 17655
- `checking searches for their recall is advised` found at byte 44785
- capture contains `Bramer`, `<year>2018</year>`, `J Med Libr Assoc`, doi `10.5195/jmla.2018.283`, and `article-title>A systematic approach to searching: an efficient and complete method to develop literature searches`
- capture contains the character sequence `6. Document` (character offset 17196) and `page-range>531–541</page-range`
- `531-539` and `531–539` are absent from that capture

Staged S077 capture, sha256(`https://doi.org/10.1186/s13643-020-01542-z`)[:24]:

`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/01f657b3d0ab045c494b3f92.txt`

- 267 bytes, 265 Unicode characters
- first non-empty line: ` Client Challenge `
- `Client Challenge` is present
- this is not the PRISMA-S article text

Japanese capture named by the staged three-literatures entry (S087 URL `https://www.jstage.jst.go.jp/article/jjsme/105/2/105_17/_article/-char/ja`), key `02b3b0e812df68ca305c7bc3.txt`:

- 6333 bytes, 4076 characters
- `参照日` absent
- `参照` absent
- head is a J-STAGE shell beginning `論文執筆における引用の仕方，図表の転載，及び引用・参考文献の記載形式`, not the quoted checklist sentence

JMLA download URL from the staged `search-tracking-record-r40.md` (`https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061`), key `0ae65ac01b93119d3c2f3fed.txt`, 27737 bytes. This seat did not run `pdftotext`. The file is text: a leading page number `253` and wide column gaps.

- raw substring `should be reported in Column 2`: absent
- same string after NFKC + whitespace collapse: absent
- raw neighborhood of `should be reported`: `should be reported in which column, specifically noting`
- the two non-column observation sentences in the staged entry are not raw substrings, because the file inserts newlines and spaces:

```
including the recommendation
       to report search strategies for all databases, registries, and websites that were searched. PRISMA-S also recommends
       reporting the number of records identified from each information source.
```

- after NFKC + whitespace collapse both of those sentences are present as contiguous spans
- the Gate does not name those two sentences; they were taken from the staged file the Gate names

Commit `737f40b` vs its parent, read-only `git diff` / `git show --stat`:

```
 corpus/SOURCES.md                         |  3 ++
 corpus/knowledge/search-log-method-r39.md | 27 +++++++++++++
 corpus/lessons/round-43.md                | 66 +++++++++++++++++++++++++++++++
 3 files changed, 96 insertions(+)
```

Knowledge name-status: `A corpus/knowledge/search-log-method-r39.md` only. SOURCES additions are the S078 row, one blank line, and the Round 43 search-log bullet. No other registry row is in that diff. `search-log-fields-r36.md` and `search-tracking-record-r40.md` are not in `corpus/knowledge/`. The admitted entry's `source:` line is `source: S078 —` and does not contain `source: S118 —`. The filename matches the package amendment path `merge/chousa/amendments/corpus/knowledge/search-log-method-r39.md`. Parent of `737f40b` has no `corpus/knowledge/search-log-method-r39.md` (`git show <parent>:…` exit 128).

## Touched surfaces

This seat writes only this report. It does not modify the lesson, the counters, the registry, the knowledge entry, the git index, jj, the fleet repo, or `/home/vgpnk/Projects/shokuknow`.

Surfaces the measured commit added, observed by `git show` and not edited here: `corpus/lessons/round-43.md`, `corpus/knowledge/search-log-method-r39.md`, `corpus/SOURCES.md` (S078 row and the Round 43 search-log bullet).

## Out of scope

- Gate sections after Rejected (registry changes, id collision, spot-check, sources census). Not quoted as the assignment. Census was not re-run; `receipts/census-end.txt` was not executed.
- Non-author spot-check. The lesson says it is pending. This seat is the lane. No sibling report was used as evidence.
- Cochrane capture cited by the staged three-literatures entry. The Gate's stated reason was the bot wall and the missing 参照日; those two were checked. The Cochrane file was not opened.
- Full package inventory. Only the two named rejects and the one admitted filename were checked against the lane tree.
- Live-web truth. No URL was fetched. "Not fetched" in the Gate is the lesson's claim plus this seat's non-fetch, not a network log.
- Retuning R43-SPLIT. C2 agreed 15/15, so there was no disagreement to absorb. The bound stayed 1/2.

## Findings

Holds, from this seat's commands:

- C1=PASS exit 0; missing-tool control exits 1.
- SPLIT_AGREES=15/15 exit 0; `--flip S086` prints `SPLIT_AGREES=14/15` and exits 1.
- C3=PASS exit 0; missing-entry control exits 1. The entry cites S078 and not `source: S118 —`.
- The 12-word quote, including the period, is in the Europe PMC capture. `wc -w` is 12. The two "also located" sentences are raw substrings. sha256 matches.
- Staged S077 capture is 267 bytes / 265 characters and its first non-empty line is ` Client Challenge `.
- The Japanese capture for the staged S087 URL does not contain 参照日.
- `should be reported in Column 2` is absent as a raw span and absent after NFKC + whitespace collapse.
- The measured commit appends one knowledge file and one new registry row, S078, which that file cites. The two rejected filenames are not in `corpus/knowledge/`.

Conflicts, verbatim, for the L1. Not resolved here.

1. Gate (and the same number in `corpus/SOURCES.md` and `corpus/knowledge/search-log-method-r39.md`): `byte offset 17383`. File: the 12-word quote starts at byte offset 17410 and at Unicode character offset 17383. Bytes at 17383 are `ly in the database itself, to register t`. C3 does not check the offset, so C3=PASS does not confirm the unit.
2. Gate path `.qcache/2cef078d8f9f87802e19e770.txt` does not exist in the lane. The file that matches the sha256 and the URL key is `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/2cef078d8f9f87802e19e770.txt`, which is the path the admitted entry prints.
3. Gate: `Two other sentences in that capture are contiguous`. Raw file: those staged sentences contain newlines and indentation, so they are not raw contiguous spans. After NFKC + whitespace collapse they are contiguous. The column sentence is absent under both readings, so the rejection of the column claim holds either way. Whether "contiguous" in that sentence means raw bytes or collapsed whitespace is for the L1.
4. Not a Gate sentence. The admitted entry's source line says `J Med Libr Assoc 2018;106(4):531-539`. The capture says `page-range>531–541</page-range>`. `531-539` is not in the capture.

## Known limits

- Did not fetch, so historical non-fetch is not independently logged here.
- Did not run `pdftotext`; the JMLA file was read as the committed cache object for that URL.
- Did not re-run `sources-census.sh`.
- Did not open the Cochrane capture or list every package file.
- Committed receipts `corpus/evidence/round43/receipts/c1-after.txt`, `c2-after.txt`, and `c3-after.txt` were read. They match this seat's later runs. They are not a substitute for those runs; the runs above are the execution evidence.

## Artifact paths

- Report: `.ufo/waves/round-43/w1/ScribeGateBlock.md`
- Lesson quoted, not edited: `corpus/lessons/round-43.md`
- Counters: `corpus/evidence/round43/c1-count.py`, `corpus/evidence/round43/c2-count.py`, `corpus/evidence/round43/c3-count.py`

Report: .ufo/waves/round-43/w1/ScribeGateBlock.md
