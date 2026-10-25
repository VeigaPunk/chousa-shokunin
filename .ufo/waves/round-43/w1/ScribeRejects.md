# ScribeRejects — round 43, wave 1

Seat: chousa round-43 leaf scribe. Assigned attack: state the two rejected entries and their flip conditions, from the lesson, in this seat's own words, backed by quotes. No production edit, no network, no subagent, no tool install.

Axes walked: operability (the two names are locatable and are not lane knowledge files), calibration (flip text taken from the lesson, conflicts not collapsed), depth (each flip tied to the reason that would have to become false, checked against committed captures only).

Pins: measured commit and observed `HEAD` are the same hash, `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`. Lesson subject at that commit: `round-43: split the absent class and adopt one locally re-opened search-log entry`. `git status --short` on the lesson, `corpus/SOURCES.md`, and the three knowledge paths below printed no lines. That is not a claim that the whole worktree is clean.

## The two rejected entries

The lesson's `### Rejected` block has three bullets. Two of them name entries. The third, "The rest of the package," is not an entry. `corpus/SOURCES.md` independently counts "excluded 2." Both named files are absent from the lane knowledge tree. The one admitted entry, `corpus/knowledge/search-log-method-r39.md`, is not one of these two.

### 1. `search-log-fields-r36.md`

This is the three-literatures candidate: what a search log must record, drawn from a PRISMA-S checklist, a Cochrane conduct rule, and a Japanese access-date rule. It stays rejected. The lesson's reason is that the capture it calls staged S077 is a 267-byte / 265-character Client Challenge, not the PRISMA-S article, and that the Japanese capture does not contain 参照日. A row that cites an unreopened source is not admitted.

Flip, from the lesson, not from the shorter search-log line: both of the following have to be true. The still-open fetch-scope ruling has to be answered, and a capture of each source the entry cites has to contain the sentences the entry quotes. Answering the ruling without those captures does not flip it. A capture of one article's checklist items, which is how `SOURCES.md` shortens the same flip, is not the lesson's condition. One cited source already containing its sentence does not flip it either, because the lesson's "each" is a conjunction.

The staged copy this seat read, and did not adopt, cites three sources:

```
source: S079 — https://doi.org/10.1186/s13643-020-01542-z
source: S080 — https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-04
source: S087 — https://www.jstage.jst.go.jp/article/jjsme/105/2/105_17/_article/-char/ja
```

That file lives under `/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/search-log-fields-r36.md`. It is not a lane file. This seat did not run any shokuknow tool.

### 2. `search-tracking-record-r40.md`

This is the tracking-record entry: what PRISMA-S puts in a tracking record, and in which flow-diagram column. It stays rejected because the column claim cannot be re-grounded. The lesson's reason is that "should be reported in Column 2" is not a contiguous span in the committed pdftotext capture. Two other sentences in that capture being contiguous is stated as not enough to admit the column claim.

Flip, from the lesson: a rendering in which that sentence is contiguous. The sentence is the one just named, "should be reported in Column 2." This flip does not mention the fetch-scope ruling. A whitespace collapse of the current capture is not, on this seat's read, that rendering.

The staged copy this seat read cites one source, the JMLA PDF `https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061`, and quotes "should be reported in Column 2". That file is `/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/search-tracking-record-r40.md`. It is not a lane file.

### Not one of the two entries

The third Rejected bullet keeps the rest of the package out because the round took one theme and appended only the rows an admitted entry cites. Its flip is different: a later round re-grounds another theme from local captures, or the fetch ruling opens the rest. This seat does not count that bullet as a third rejected entry.

## Quotes the flips rest on

Lesson, `corpus/lessons/round-43.md`, Rejected block, as printed by the command below:

```
- `search-log-fields-r36.md` (the three-literatures candidate). Reason: staged S077's local capture is a 267-byte / 265-character Client Challenge, not the PRISMA-S article, and the Japanese capture does not contain 参照日. A row that cites an unreopened source is not admitted. Flip: the fetch-scope ruling is answered and a capture of each cited source contains the quoted sentences.
- `search-tracking-record-r40.md`. Reason: "should be reported in Column 2" is not a contiguous span in the committed pdftotext capture, so the column claim cannot be re-grounded. Two other sentences in that capture are contiguous; they are not enough to admit the column claim. Flip: a rendering in which that sentence is contiguous.
- The rest of the package. Reason: one theme, and only the rows an admitted entry cites are appended. Flip: a later round re-grounds another theme from local captures, or the fetch ruling opens the rest.
```

Lane absence, same command: `LANE_PRESENT corpus/knowledge/search-log-fields-r36.md False`, `LANE_PRESENT corpus/knowledge/search-tracking-record-r40.md False`, `LANE_PRESENT corpus/knowledge/search-log-method-r39.md True`.

## Conflicts for the L1, verbatim

This seat does not pick a winner. The assigned source of the flip conditions is the lesson.

1. `corpus/SOURCES.md:250` narrows the first flip and keeps the second. Verbatim tail of that bullet:

```
Rejected `search-log-fields-r36.md`: staged S077's capture is a 267-byte Client Challenge, and the Japanese capture does not contain 参照日. Flip: the fetch-scope ruling is answered and a capture of the cited article contains the quoted checklist items. Rejected `search-tracking-record-r40.md`: the column-allocation sentence is not a contiguous span in the pdftotext capture. Flip: a rendering where "should be reported in Column 2" is contiguous.
```

Against the lesson: "each cited source" / "quoted sentences" versus "the cited article" / "quoted checklist items." The Japanese 参照日 quotes are not checklist items of one article. The second flip agrees in substance; the lesson uses "that sentence" after naming it, and `SOURCES.md` repeats the span inside the flip clause.

2. `LOG.md:1552` says the rejects have a flip and does not state either condition:

```
- Rejected, with flip: `search-log-fields-r36.md` (staged S077 capture is a 267-byte / 265-character bot wall) and `search-tracking-record-r40.md` (column sentence not contiguous). Scratch census on the mirrored registry plus the S078 row exited 0 before the append. Collision guard: indented `  | S118 |` is caught; column-zero pattern misses it. Real collision is S077 only.
```

3. The lesson and `.ufo/waves/round-43/assimilation/renumber-map.txt` call the PRISMA-S DOI staged S077. The append file this seat read does not. `renumber-map.txt` line 2:

```
staged S077 | https://doi.org/10.1186/s13643-020-01542-z | collides with lane S077 | NOT adopted (bot-wall capture) | if later adopted, next free id then, by this URL, never by overwriting lane S077
```

`/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md:7` and `/home/vgpnk/Projects/shokuknow/lanes/chousa/SOURCES-PROPOSED.md:35` both label that same DOI `S079`. A content search of `SOURCES.append.md` for `S077` hit only a prose mention inside the S093 row (`SOURCES.append.md:21`), not a `| S077 |` row. The first data row of the append file is S079, the PRISMA-S DOI. This seat does not retcon either label. The capture check below follows the URL, not the id arithmetic the lesson itself refuses.

4. Frozen `corpus/evidence/round43/claims.md:100` names only one of the two rejects: `Adoption of search-log-fields-r36.md. Staged S077's capture is a bot wall.` It does not mention `search-tracking-record-r40.md`. That is an omission in the Not-claimed list, not an admission. The tracking file is absent from `corpus/knowledge/`.

## What this seat saw in committed captures

No fetch. Cache root `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`. Capture names are sha256 of the URL, first 24 hex, plus `.txt`. These checks back the flip conditions. They are not a rescore of C1, C2, or C3, which this seat did not run.

PRISMA-S DOI `https://doi.org/10.1186/s13643-020-01542-z` → `01f657b3d0ab045c494b3f92.txt`, 267 bytes, 265 characters. Exact substring `Client Challenge` present once. Exact substring `PRISMA` absent. Exact substring `copied and pasted exactly as run` absent. The file's visible challenge lines, from a Read of that path:

```
 Client Challenge
 A required part of this site couldn’t load. This may be due to a browser
 extension, network issues, or browser settings. Please check your
 connection, disable any ad blockers, or try using a different browser.
```

The first line of that file is a single space, not the challenge title. The lesson's "Client Challenge" quote matches line 8, not line 1.

Japanese URL `https://www.jstage.jst.go.jp/article/jjsme/105/2/105_17/_article/-char/ja` → `02b3b0e812df68ca305c7bc3.txt`, 6333 bytes, 4076 characters. Exact substring `参照日` absent, including after NFKC was not required: the search was the exact characters 参照日, and they do not occur. This capture is not the Client Challenge page. Its head contains the article title `論文執筆における引用の仕方，図表の転載，及び引用・参考文献の記載形式`. A page that looks like the article and still lacks 参照日 does not meet the lesson's flip.

Cochrane chapter-4 URL → `14aaa168a5cb4d833ca78b0b.txt`, 211326 bytes. Exact substring `the sources searched, when, by whom, and using which terms` is present. Exact substring `Document the search process in enough detail to ensure that it can be reported correctly in the review` is present. That is one cited source, not each cited source, and the fetch-scope ruling is still the other conjunct. This observation does not flip `search-log-fields-r36.md`. Limit: this seat did not match every phrase in the staged entry, only those three strings.

JMLA PDF URL → `0ae65ac01b93119d3c2f3fed.txt`, 27737 bytes. Exact substring `should be reported in Column 2` is absent in the raw text and still absent after NFKC plus whitespace collapse. `Column 2` occurs 9 times. `reported in Column 2` occurs once, without `should` joined to it. The nearest `should` before that hit is 187 characters earlier, and the gap is the other column of the pdftotext rendering, not whitespace:

```
should be\nwants us to list the number of records identified from         considered as an additional information source and\nother methods, like browsing reference lists, email            reported in Column 2.\nalerts identifying citing articles, we
```

Two other sentences quoted by the staged tracking entry are absent as raw spans and present after whitespace collapse: `PRISMA-S also recommends reporting the number of records identified from each information source`, and `the recommendation to report search strategies for all databases, registries, and websites that were searched`. The lesson says two other sentences are contiguous and are not enough. This seat did not identify which two sentences the lesson meant. It does not treat the raw-versus-collapsed difference as a lesson failure. It does observe that collapsing whitespace does not create `should be reported in Column 2`, which is the sentence the flip names.

## Behavior

Read-only. Commands were `git rev-parse`, a path-scoped `git status --short`, `git log -1` on the lesson, and local Python reads of the lesson, `SOURCES.md`, `claims.md`, the staged knowledge copies, and the `.qcache` files named above. No `curl`, `wget`, fetch, or socket client. No pacman. No package install. No shokuknow tool. No counter. No edit of the lesson, the registry, the captures, or a sibling report.

## Gates

This seat did not run `c1-count.py`, `c2-count.py`, or `c3-count.py`. Those checks are unrun here and have not passed here. The reject statement does not depend on them. No do-nothing control was run by this seat.

## Touched surfaces

Only this report: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/w1/ScribeRejects.md`. No product file, lane git index, jj state, fleet repo, sibling repo, or `/home/vgpnk/Projects/shokuknow` path was written. `LOG.md` was not appended. The seat contract forbids that write; `AGENTS.md`'s append rule is recorded here as not executed.

## Out of scope

C1/C2/C3 reruns, the 1/2 bound, census, collision-guard re-execution, admitting either rejected entry, renaming `search-log-method-r39.md`, and resolving staged S077 versus S079.

## Findings

- The two rejected entries are `search-log-fields-r36.md` and `search-tracking-record-r40.md`. Their lesson flips are, respectively, an answered fetch-scope ruling plus a capture of each cited source containing the quoted sentences, and a rendering in which "should be reported in Column 2" is contiguous.
- `SOURCES.md:250` is not a faithful restatement of the first flip. Quoted above for the L1. This seat uses the lesson.
- `LOG.md:1552` names both rejects and does not state the flip conditions.
- The DOI the lesson calls staged S077 is labeled S079 in the append file this seat read. The 267-byte Client Challenge is the capture of that URL either way.
- Cochrane's quoted sentence is already in the committed capture. That does not satisfy "each cited source," and it does not answer L0 `8d77e6c1`.
- The column sentence is absent even after whitespace collapse. The current pdftotext interleaves the other column between `should be` and `reported in Column 2`.

## Artifact paths

- Lesson: `corpus/lessons/round-43.md`
- Search-log bullet: `corpus/SOURCES.md:250`
- Frozen not-claimed line: `corpus/evidence/round43/claims.md:100`
- Admitted entry, present: `corpus/knowledge/search-log-method-r39.md`
- Rejected entries, absent from the lane: `corpus/knowledge/search-log-fields-r36.md`, `corpus/knowledge/search-tracking-record-r40.md`
- Staged copies, read only: `/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/search-log-fields-r36.md`, `/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/search-tracking-record-r40.md`
- Captures: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/01f657b3d0ab045c494b3f92.txt`, `02b3b0e812df68ca305c7bc3.txt`, `14aaa168a5cb4d833ca78b0b.txt`, `0ae65ac01b93119d3c2f3fed.txt`
- This report: `.ufo/waves/round-43/w1/ScribeRejects.md`

## Commands and verbatim output

Command 1, cwd `/home/vgpnk/Projects/shokunin/chousa-shokunin`:

```
git rev-parse HEAD && git status --short -- corpus/lessons/round-43.md corpus/SOURCES.md corpus/knowledge/search-log-fields-r36.md corpus/knowledge/search-tracking-record-r40.md corpus/knowledge/search-log-method-r39.md && git log -1 --format='%H%n%s' -- corpus/lessons/round-43.md && python3 - << 'PY'
# presence of the three knowledge paths, then the lesson Rejected block,
# then SOURCES.md and claims.md lines that name either rejected entry
PY
```

The Python body printed the Rejected block and the hit lines. Combined stdout, `git status --short` included and empty:

```
737f40b6aa8f37ffe2269db370fd6d65a720d9a8
737f40b6aa8f37ffe2269db370fd6d65a720d9a8
round-43: split the absent class and adopt one locally re-opened search-log entry
LANE_PRESENT corpus/knowledge/search-log-fields-r36.md False
LANE_PRESENT corpus/knowledge/search-tracking-record-r40.md False
LANE_PRESENT corpus/knowledge/search-log-method-r39.md True
---LESSON_REJECTED_BEGIN---
### Rejected

- `search-log-fields-r36.md` (the three-literatures candidate). Reason: staged S077's local capture is a 267-byte / 265-character Client Challenge, not the PRISMA-S article, and the Japanese capture does not contain 参照日. A row that cites an unreopened source is not admitted. Flip: the fetch-scope ruling is answered and a capture of each cited source contains the quoted sentences.
- `search-tracking-record-r40.md`. Reason: "should be reported in Column 2" is not a contiguous span in the committed pdftotext capture, so the column claim cannot be re-grounded. Two other sentences in that capture are contiguous; they are not enough to admit the column claim. Flip: a rendering in which that sentence is contiguous.
- The rest of the package. Reason: one theme, and only the rows an admitted entry cites are appended. Flip: a later round re-grounds another theme from local captures, or the fetch ruling opens the rest.
---LESSON_REJECTED_END---
SOURCES:250:- Round 43 (2026-10-24): question — what must a search log record, and which of those requirements can be re-opened from committed captures without a fetch? Where: the campaign's committed capture cache only; no URL was fetched (L0 `8d77e6c1` still open). Identified 3 candidate entries on the search-log theme, screened 3, included 1 (S078, Europe PMC full-text XML of Bramer et al. 2018, staged id S118 re-pointed by document), excluded 2. Rejected `search-log-fields-r36.md`: staged S077's capture is a 267-byte Client Challenge, and the Japanese capture does not contain 参照日. Flip: the fetch-scope ruling is answered and a capture of the cited article contains the quoted checklist items. Rejected `search-tracking-record-r40.md`: the column-allocation sentence is not a contiguous span in the pdftotext capture. Flip: a rendering where "should be reported in Column 2" is contiguous. Stop rationale: one opened capture contains the three located sentences; the other two entries cannot be re-grounded without a fetch or a cleaner rendering.
---CLAIMS_HITS---
CLAIMS:97:## Not claimed
CLAIMS:100:- Adoption of `search-log-fields-r36.md`. Staged S077's capture is a bot wall.
```

Command 2, local Python over the campaign `.qcache`, no network. Stdout:

```
QCACHE_IS_DIR True
URL_SHA24 prisma_doi 01f657b3d0ab045c494b3f92.txt exists=True size=267
URL_SHA24 cochrane 14aaa168a5cb4d833ca78b0b.txt exists=True size=211326
URL_SHA24 jstage 02b3b0e812df68ca305c7bc3.txt exists=True size=6333
URL_SHA24 jmla 0ae65ac01b93119d3c2f3fed.txt exists=True size=27737
URL_SHA24 europepmc 2cef078d8f9f87802e19e770.txt exists=True size=80107
NAMED staged_s077_named 01f657b3d0ab045c494b3f92.txt exists=True size=267
NAMED europepmc_named 2cef078d8f9f87802e19e770.txt exists=True size=80107
FILE 01f657b3d0ab045c494b3f92.txt bytes=267 chars=265
FIRST_LINE ' '
NEEDLE 'Client Challenge' present=True count=1
NEEDLE 'PRISMA' present=False count=0
NEEDLE 'copied and pasted exactly as run' present=False count=0
FILE 02b3b0e812df68ca305c7bc3.txt bytes=6333 chars=4076
FIRST_LINE ' '
NEEDLE '参照日' present=False count=0
FILE 0ae65ac01b93119d3c2f3fed.txt bytes=27737 chars=27659
FIRST_LINE '                                                                                                                                        253'
NEEDLE 'should be reported in Column 2' present=False count=0
NEEDLE 'Column 2' present=True count=9
NEEDLE 'PRISMA-S also recommends reporting the number of records identified from each information source' present=False count=0
```

Command 3, same cache, raw versus whitespace-collapsed, plus Cochrane and the Japanese head. Stdout:

```
JMLA path=0ae65ac01b93119d3c2f3fed.txt bytes=27737
RAW 'should be reported in Column 2' False
COLLAPSED 'should be reported in Column 2' False
RAW 'PRISMA-S also recommends reporting the number of records identified from each information source' False
COLLAPSED 'PRISMA-S also recommends reporting the number of records identified from each information source' True
RAW 'the recommendation to report search strategies for all databases, registries, and websites that were searched' False
COLLAPSED 'the recommendation to report search strategies for all databases, registries, and websites that were searched' True
RAW 'also suggests reporting an overall number for records identified from databases and registers in Column 1' False
COLLAPSED 'also suggests reporting an overall number for records identified from databases and registers in Column 1' False
RAW 'identification of studies via other methods' False
COLLAPSED 'identification of studies via other methods' False
RAW 'Column 2' True
COLLAPSED 'Column 2' True
COCHRANE path=14aaa168a5cb4d833ca78b0b.txt bytes=211326
COCH_RAW 'the sources searched, when, by whom, and using which terms' True
COCH_COLLAPSED 'the sources searched, when, by whom, and using which terms' True
COCH_RAW 'Document the search process in enough detail to ensure that it can be reported correctly in the review' True
COCH_COLLAPSED 'Document the search process in enough detail to ensure that it can be reported correctly in the review' True
COCH_RAW 'Documenting and reporting the search process' True
COCH_COLLAPSED 'Documenting and reporting the search process' True
JSTAGE path=02b3b0e812df68ca305c7bc3.txt bytes=6333 chars=4076
JP '参照日' raw=False collapsed=False
JP 'インターネット' raw=False collapsed=False
JP 'Client Challenge' raw=False collapsed=False
JP 'Just a moment' raw=False collapsed=False
JP 'cf-browser-verification' raw=False collapsed=False
```

The command's `JP_HEAD` repr and the nine `WINDOW` lines are not re-pasted here. This seat will not reconstruct their escape sequences and call that verbatim. The verbatim lines above are the ones this seat relies on: `参照日` is absent raw and collapsed, and the head that was printed contains the title `論文執筆における引用の仕方，図表の転載，及び引用・参考文献の記載形式`. Command 4 stdout, the span this seat quotes:

```
be\nwants us to list the number of records identified from         considered as an additional information source and\nother methods, like browsing reference lists, email            reported in Column 2.\nalerts identifying citing articles, we
---
nearest should before 187 chars earlier
'should be\nwants us to list the number of records identified from         conside'
```

Tools installed or updated: none.

Report: .ufo/waves/round-43/w1/ScribeRejects.md
