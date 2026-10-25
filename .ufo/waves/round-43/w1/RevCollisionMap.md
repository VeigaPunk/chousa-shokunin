# RevCollisionMap — round 43 / w1 (leaf revenger, no dispatch)

Axes: operability (cells extract and the negative URL checks run), calibration (lane ids still name the frozen documents, not the colliding ones), depth (id-join versus document-join, frozen snapshot versus live staging).

Assigned surface: `corpus/SOURCES.md` rows S077 and S078 only. Confirm S077 is still the pdftotext manual and S078 is the Europe PMC URL, not the Cochrane URL and not the PRISMA-S DOI. Quote both source cells.

Lane root: `/home/vgpnk/Projects/shokunin/chousa-shokunin`. Measured commit and HEAD are both `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`. Parent of that commit is `15f9f3fbd3c17b2155f718c67cbef0624034cf6d` (the base named in `corpus/evidence/round43/claims.md`). No production file, git index, jj state, fleet repo, sibling repo, or `/home/vgpnk/Projects/shokuknow` was written. No network. No tool install. This seat has no semantic index. Cell extraction is a column-zero row read plus a pipe-split. Substring checks are literal. They are not semantic proof.

## Verdict

The assigned confirmation holds.

- S077 is still the Poppler `pdftotext(1)` manual. The source cell is unchanged from the parent commit. It is not a DOI.
- S078's source cell is the Europe PMC full-text URL `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6148622/fullTextXML`.
- That cell is not the PRISMA-S DOI `https://doi.org/10.1186/s13643-020-01542-z`.
- That cell is not the Cochrane chapter-04 URL `https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-04`.

No actionable defect on this surface. A live-staging id shift is recorded below as a divergence of join keys, not as a failure of the lane rows.

## Reconstructed contract

Registry header, `corpus/SOURCES.md` line 9:

```
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
```

The source cell is the second cell. A confirming read is a column-zero row (`^\| S0NN \|`), 11 cells, source cell quoted, then literal absence of the two forbidden URL strings.

Frozen collision contract, from the lane's own map (not from live staging):

```
lane S077 | Poppler pdftotext(1) manual | stays S077 | not a staged document
staged S077 | https://doi.org/10.1186/s13643-020-01542-z | collides with lane S077 | NOT adopted (bot-wall capture) | if later adopted, next free id then, by this URL, never by overwriting lane S077
staged S118 | https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6148622/fullTextXML | adopted as lane S078 | URL is the evidence; S078 is the next free lane id, not S118 and not staged S078
staged S078 | Cochrane chapter 4 URL | NOT adopted | must not be copied onto lane S078; lane S078 is the Europe PMC document
```

Source: `.ufo/waves/round-43/assimilation/renumber-map.txt` lines 1–4, read in full.

The round-43 commit may add S078. It must not rewrite S077. S078's evidence is the Europe PMC URL. The id follows the next free lane id. It is not staged S118, not staged S078, and not the PRISMA-S DOI.

## Source cells

Both cells are from `corpus/SOURCES.md` at HEAD `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`, lines 87 and 88. Working tree matches that commit (`git status --porcelain -- corpus/SOURCES.md` printed no lines, exit 0).

### S077 source cell (line 87, cell 2 of 11)

```
Poppler `pdftotext(1)` manual — `/usr/share/man/man1/pdftotext.1.gz` (canonical project URL `http://poppler.freedesktop.org/` printed by the installed `pdftotext -v`; not fetched)
```

### S078 source cell (line 88, cell 2 of 11)

```
Bramer, de Jonge, Rethlefsen, Mast, Kleijnen, A systematic approach to searching — Europe PMC full-text XML https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6148622/fullTextXML (capture sha256 833b13e3e80212522d016a8db9c6edeacb8965148d2334722a7a73c415d7136d; not fetched this round)
```

Parent `15f9f3fb` source cell for S077 is the same string. Parent has no S078 row (registry ended at S077, 77 column-zero rows). The round-43 diff adds the S078 row and leaves the S077 line as unchanged context.

## Evidence chain

### 1. HEAD, parent, and clean tree

```
$ git rev-parse HEAD
737f40b6aa8f37ffe2269db370fd6d65a720d9a8
$ git rev-parse HEAD^
15f9f3fbd3c17b2155f718c67cbef0624034cf6d
$ git log -1 --format='%H%n%s' -- corpus/SOURCES.md
737f40b6aa8f37ffe2269db370fd6d65a720d9a8
round-43: split the absent class and adopt one locally re-opened search-log entry
$ git status --porcelain -- corpus/SOURCES.md; echo "PORCELAIN_EXIT=$?"
PORCELAIN_EXIT=0
```

Porcelain printed no path lines.

### 2. Parent cells

```
PARENT_ID S077
PARENT_SOURCE Poppler `pdftotext(1)` manual — `/usr/share/man/man1/pdftotext.1.gz` (canonical project URL `http://poppler.freedesktop.org/` printed by the installed `pdftotext -v`; not fetched)
PARENT_NCELLS 11
PARENT_N 77 LAST S077
```

`git show HEAD^:corpus/SOURCES.md` had no S078 row. That is the "still" check: S077 was not overwritten when S078 was added.

### 3. Round-43 diff, verbatim

```
$ git diff HEAD^ HEAD -- corpus/SOURCES.md
diff --git a/corpus/SOURCES.md b/corpus/SOURCES.md
index 433a3e1..3c7811d 100644
--- a/corpus/SOURCES.md
+++ b/corpus/SOURCES.md
@@ -85,6 +85,7 @@ its author opened the source and judged its tier for the stated scope only.
 | S075 | GNU coreutils `mktemp(1)` manual — `/usr/share/man/man1/mktemp.1.gz` (canonical URL `https://www.gnu.org/software/coreutils/manual/coreutils.html#mktemp-d` printed as the roff tty-link at the anchored line; not fetched) | docs | A | the documented safe-creation contract of the installed coreutils `mktemp` — the binary the capture's fixture dir depends on; not a uniqueness or hostile-path guarantee | NAME line 3 and DESCRIPTION lines 8–12 (decompressed): "Create a temporary file or directory, safely, and print its name."; `-d, --directory` `.TP` at decompressed line 16; coreutils 9.12 (September 2026), installed `coreutils 9.12-2`; file SHA-256 `9abddc15cda1e4773064a0c319bc096a64848d21deccc64229f18085857d604e` (opened locally 2026-10-24) | `mktemp -d` creates a directory safely and prints its name; the page documents creation semantics only — a printed path the caller did not request is outside the documented contract | mined | 2026-10-24 | on-release | corpus/knowledge/capture-path-pin-r41.md |
 | S076 | GNU `sed(1)` manual and `sed.info` node "The 's' Command" — `/usr/share/man/man1/sed.1.gz` + `/usr/share/info/sed.info.gz` (canonical project URL `https://www.gnu.org/software/sed/` printed at man-page line 51; not fetched) | docs | A | the documented `s/REGEXP/REPLACEMENT/FLAGS` substitution semantics of the installed GNU sed — the binary the drift normalizer depends on; not a POSIX-superset portability claim | `sed.info` node 3.3 "The 's' Command", first paragraph (decompressed lines 619–623): "The 's' command (as in substitute) is probably the most important in 'sed'"; GNU sed 4.10 (August 2026), installed `sed 4.10-1`; file SHA-256 man `06c76292824716f96bc7bbe0f071b4e6b615505c7fe25536daffe2767d0ddf95`, info `35eb9c6f8d47f872958757863fe186023f241e2c87bd9da582f6af2f5f56a95c` (opened locally 2026-10-24) | The `s` command substitutes REGEXP matches with REPLACEMENT under FLAGS; the gate's volatile-field masking is exactly this documented operation, so different sed bytes are a different normalizer | mined | 2026-10-24 | on-release | corpus/knowledge/capture-path-pin-r41.md |
 | S077 | Poppler `pdftotext(1)` manual — `/usr/share/man/man1/pdftotext.1.gz` (canonical project URL `http://poppler.freedesktop.org/` printed by the installed `pdftotext -v`; not fetched) | docs | A | the documented text-extraction contract of the exact tool whose `pdftotext -layout` output the campaign's cached PDF captures are; not a rendering-quality standard | DESCRIPTION, lines 12–13 of the decompressed roff source (`/usr/share/man/man1/pdftotext.1.gz`, sha256 `50dd56df…`); the installed binary reports `pdftotext version 26.08.0` | a PDF capture in the campaign's cache IS a text rendering, so a quote's absence in it is a statement about that rendering, while a non-PDF binary document that was never rendered cannot refute a quote at all | mined | 2026-10-24 | 180d | tools/quarantine-check.py, corpus/lessons/round-42.md |
+| S078 | Bramer, de Jonge, Rethlefsen, Mast, Kleijnen, A systematic approach to searching — Europe PMC full-text XML https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6148622/fullTextXML (capture sha256 833b13e3e80212522d016a8db9c6edeacb8965148d2334722a7a73c415d7136d; not fetched this round) | paper | A | how a search log is kept as a working document, distinct from a checklist of fields a log must carry | section 6 of the Europe PMC full-text XML, byte offset 17383 of the committed capture | Design and keep the complete search strategies in a log document rather than in the database, so the steps taken stay accountable and reproducible | mined | 2026-10-24 | 365d | corpus/knowledge/search-log-method-r39.md |
 
 ## Paths
 
@@ -246,6 +247,8 @@ its author opened the source and judged its tier for the stated scope only.
   URL of the man page and fetching any of the 20 cited sources — flip: the operator
   answers the fetch-scope L0 question `8d77e6c1`. Opened this round: S077.
 
+- Round 43 (2026-10-24): question — what must a search log record, and which of those requirements can be re-opened from committed captures without a fetch? Where: the campaign's committed capture cache only; no URL was fetched (L0 `8d77e6c1` still open). Identified 3 candidate entries on the search-log theme, screened 3, included 1 (S078, Europe PMC full-text XML of Bramer et al. 2018, staged id S118 re-pointed by document), excluded 2. Rejected `search-log-fields-r36.md`: staged S077's capture is a 267-byte Client Challenge, and the Japanese capture does not contain 参照日. Flip: the fetch-scope ruling is answered and a capture of the cited article contains the quoted checklist items. Rejected `search-tracking-record-r40.md`: the column-allocation sentence is not a contiguous span in the pdftotext capture. Flip: a rendering where "should be reported in Column 2" is contiguous. Stop rationale: one opened capture contains the three located sentences; the other two entries cannot be re-grounded without a fetch or a cleaner rendering.
+
 ## Leads (unopened)
 
 - TREC RAG track website — https://trec-rag.github.io/ — task data, qrels, and
```

The S077 line is context (leading space). The S078 registry row is the only added registry line. `git diff --stat HEAD^ HEAD -- corpus/SOURCES.md corpus/knowledge/search-log-method-r39.md` printed:

```
 corpus/SOURCES.md                         |  3 +++
 corpus/knowledge/search-log-method-r39.md | 27 +++++++++++++++++++++++++++
 2 files changed, 30 insertions(+)
```

### 4. Literal negative checks on the two source cells

```
LANE_N 78 FIRST S001 LAST S078
CELL S077
  'pdftotext' -> True
  'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6148622/fullTextXML' -> False
  'https://doi.org/10.1186/s13643-020-01542-z' -> False
  'https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-04' -> False
  'cochrane.org' -> False
  'doi.org' -> False
CELL S078
  'pdftotext' -> False
  'https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6148622/fullTextXML' -> True
  'https://doi.org/10.1186/s13643-020-01542-z' -> False
  'https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-04' -> False
  'cochrane.org' -> False
  'doi.org' -> False
```

An earlier extractor on the same file printed `LINE 87 N_CELLS 11` and `LINE 88 N_CELLS 11`, and the same two source-cell strings. The PRISMA-S DOI string occurs in the lane only at `.ufo/waves/round-43/assimilation/renumber-map.txt` line 2. A lane-tree search for `handbook/current/chapter-04` returned no file. The Cochrane URL used in the negative check is the current staging cell quoted in section 6, not a string stored in the lane registry.

### 5. C3 reads this same URL out of the S078 row

Not the assigned check. Run because a wrong source cell would fail it. Do not treat this as a C1 or C2 score.

```
$ python3 corpus/evidence/round43/c3-count.py; echo "C3_EXIT=$?"
ENTRY_CITES=1/1
QUOTE_LOCATED=1/1
URL_MATCH=1/1
C3=PASS
C3_EXIT=0
```

`c3-count.py` line 30 hardcodes the Europe PMC URL. Line 57 requires that URL to be in the S078 row. The admitted entry's first source line is `source: S078 — https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6148622/fullTextXML — ...`. That agrees with the registry cell. It is not `source: S118`.

## Collision map

| label | where observed | document | relation to lane S077 / S078 |
|---|---|---|---|
| lane S077 | `corpus/SOURCES.md:87`, unchanged since parent | Poppler `pdftotext(1)` manual, `/usr/share/man/man1/pdftotext.1.gz` | stays; not a staged document |
| lane S078 | `corpus/SOURCES.md:88`, added in `737f40b6` | Europe PMC full-text XML of Bramer et al. | the adopted row |
| frozen staged S077 | `renumber-map.txt` line 2 | `https://doi.org/10.1186/s13643-020-01542-z` | must not overwrite lane S077 |
| frozen staged S078 | `renumber-map.txt` line 4, URL not pasted there | "Cochrane chapter 4 URL" | must not be copied onto lane S078 |
| frozen staged S118 | `renumber-map.txt` line 3 | same Europe PMC URL as lane S078 | adopted by URL as lane S078, not by id arithmetic |
| live staged S079 | `/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md` line 7 | PRISMA-S DOI `https://doi.org/10.1186/s13643-020-01542-z` | same document as frozen staged S077; id is not S077 |
| live staged S080 | same file, line 8 | Cochrane Handbook chapter 4, `https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-04` | the chapter-04 URL absent from both lane source cells |
| live staged S120 | same file, line 48 | same Europe PMC URL as lane S078 | document overlap, different id |
| live staged S118 | same file | FEVER NAACL-HLT 2018 PDF, `https://aclanthology.org/N18-1074.pdf` | not the Europe PMC document |

Live id intersection, computed this seat:

```
STAGED_N 111 FIRST S079 LAST S189
ID_INTERSECTION []
FROZEN_STAGED_N 109 FIRST S077 LAST S185
FROZEN_REG_N 77 FIRST S001 LAST S077
FROZEN_INTERSECTION ['S077']
```

`assimilation/collisions` is the single line `S077`. That matches the frozen intersection. It does not match the live append, which has no shared ids with the lane registry.

`assimilation/guard/fixture-collisions` is `S077` then `S118`. That pair is the indented fixture (`indented-registry.md` has `  | S118 |`), not a column-zero row of the live append. `column-zero-ids` is `S077` only. Do not read fixture S118 as the live Europe PMC row.

`MERGE-REPORT.md` line 9: "lane registry currently holds **78** rows; first staged id is **S079**". Line 91 maps live staged `` `S120` `` to lane `` `S078` `` as a page the lane already holds. That is a document overlap after the lane adoption, not an id collision.

## Divergences

1. Frozen staged ids are not live join keys. The lane map and `assimilation/staged-ids` describe a package whose first id was S077 and whose S118 was the Europe PMC URL. The append read this seat starts at S079, has no S077 or S078 row, puts the PRISMA-S DOI at S079, the Cochrane chapter-04 URL at S080, and the Europe PMC URL at S120. Live S118 is the FEVER paper. Using the frozen label "staged S118" against the live append would select the wrong document. Inference, not fully checked: a +2 shift of the 109-id snapshot plus two appended rows would explain the endpoints (S077–S185 versus S079–S189). This seat did not join every old id to a current URL. The older append body is not in the lane. The three named documents were checked by URL, not by assuming the shift.

2. The Cochrane URL is not stored in the lane registry. The frozen map says "Cochrane chapter 4 URL" and does not paste it. The chapter-04 string above is from live staged S080. Absence of `cochrane.org` and of that full URL from both lane source cells is observed. That live S080 is exactly the map's "staged S078" is an inference from the name, the chapter-04 path, and the +2 id offset. It is not a quote from `renumber-map.txt`.

3. Advisory, outside the assigned kill: the package amendment `amendments/corpus/knowledge/search-log-method-r39.md` line 6 says `source: S120 —` plus the Europe PMC URL. The lane entry says `source: S078 —` plus the same URL. C3 kills `source: S118 —`, not `source: S120 —`. Copying the amendment's citation onto the lane entry would not by itself change the S078 source cell. It is not a present defect in `corpus/SOURCES.md`.

None of these divergences move the lane source cells off the confirmed documents.

## Confidence

- Lane S077 still the pdftotext manual: high. Parent cell, HEAD cell, and diff context are the same string. Literal checks reject the DOI, the Cochrane URL, and the Europe PMC URL.
- Lane S078 is the Europe PMC URL and not the other two: high. The URL is a substring of the source cell. Both forbidden URLs are absent. C3 `URL_MATCH=1/1` agrees.
- Frozen map versus live staging ids: high that the live append does not contain S077 or S078 and that the three URLs sit at S079, S080, and S120. Medium that every frozen staged id shifted by +2. That universal shift was not joined row by row.

## Not run

- No fetch, curl, or wget. The cells say the canonical Poppler URL and the Europe PMC URL were not fetched this round. This seat did not reopen them.
- C1 and C2 counters were not run. They do not read these source cells.
- shokuknow tools were not run. The append and merge report were read only.
