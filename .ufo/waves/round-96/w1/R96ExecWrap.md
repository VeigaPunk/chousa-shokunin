# R96ExecWrap — wrap probe on the C2 entry (round 96)

Probe: "the entry's per-line searches under-count statements that a layout text form wraps across lines."
Attacked tree: F `2db151c5ea0883de0b9dc8d95c6fac1755e1056a` (clone at `$S/repo`, checked out, toplevel asserted).
Base store read-only: `git -C $S/repo archive bbf64970b6c73ca64bcc5f6de2f33b0550459813 corpus/captures | tar -x -C $S/base`.
Tools used, none installed or updated: pdftotext/pdfinfo 26.10.0 (Poppler, pre-installed), GNU grep 3.12-modified (`/usr/bin/grep`), Python 3.14.8 (pre-installed). No pacman, no uv, no network.

## Text forms (S223 = `e94691f583d644da14661ec1`, S224 = `1a8c36c4c24444967bd9c3ce`)

- layout: the committed `corpus/captures/*.txt` (what the entry searches).
- reading: `pdftotext <capture>.raw` with no `-layout` (reading-order text).
- layout-joined / reading-joined: each whitespace-collapsed to one line (`\s+` to a space).

## Table 1 — the entry's 8 expressions (two captures; receipt `w1/R96ExecWrap-wrap-table.txt`)

Per-line forms report matching lines. Joined forms are one line, so they report occurrences (`grep -o | wc -l`, cross-checked with Python `re`).

| query (engine) | S224 layout | S224 reading | S224 layout-joined | S224 reading-joined | S223 layout | S223 reading | S223 layout-joined | S223 reading-joined |
|---|---|---|---|---|---|---|---|---|
| Q1 title (F) | 2 | 2 | 3 | 4 | 1 | 1 | 2 | 2 |
| Q2 PRESS Checklist (F) | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| Q3 peer review of search (P) | 5 | 5 | 5 | 5 | 2 | 2 | 2 | 2 |
| Q4 deduplicat (F) | 7 | 7 | 7 | 7 | 0 | 0 | 0 | 0 |
| Q5 duplicates removed (P) | 2 | 2 | 2 | 2 | 0 | 0 | 0 | 0 |
| Q6 MEDLINE search has been developed (F) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Q7 重複 (F) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Q8 translation (P) | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 |

Q7 hits are in other captures (store-level: 3 files), not in S224 or S223.

## Table 2 — file-level sweep over the base store (receipt `w1/R96ExecWrap-file-level-sweep.txt`)

91 layout captures, and reading-order for the 30 captures whose `.raw` is a PDF (`%PDF-` magic; the other 64 raws are not PDFs).

| query | files per-line (layout) | files layout-joined | files per-line (reading, 30 PDFs) | files reading-joined | files added by joining |
|---|---|---|---|---|---|
| Q1..Q8 | 2,2,3,4,1,0,3,0 | 2,2,3,4,1,0,3,0 | 1,1,1,3,1,0,2,0 | 1,1,1,3,1,0,2,0 | none, for all eight |

The `hits` field of the entry's `## Searches` record is a file count (`grep -l`), and it matches these file counts at base.

## Findings

### F1 — the probe's hypothesis is falsified at the level the record reports, and supported only at occurrence level

- File-level: joining whitespace adds no capture to any of the 8 hit sets, across all 91 layout captures and all 30 reading-order PDFs. Hit sets do not change. (Table 2.)
- Occurrence-level: the title (Q1) is split across lines in both captures, and the per-line search misses those occurrences.
  - S224 layout 870–871: "Authors should consider using the Peer Review of" / "Electronic Search Strategies (PRESS)".
  - S224 layout 1360: "Lefebvre C. PRESS Peer Review of Electronic Search" (the phrase continues on a line that does not contain "Strategies").
  - S223 layout 142–143: "PRESS: Peer Review of Electronic Search" / "Strategies".
  - Receipt: `w1/R96ExecWrap-grep-receipts.txt` (grep -n output, rc=0 each).
- Statement-level, Q6: the joined forms do not recover the statement. The exact phrase has 0 hits in all eight forms (rc=1, receipt `w1/R96ExecWrap-grep-receipts.txt`). A 300-char tolerant regex recovers it, but only by skipping intervening text (F2). So "join the lines" is not the remedy.

### F2 — the Q6 miss is a PDF page break, not a "wrap between two column lines"

The sentence "that peer review should occur after the MEDLINE search" / "has been developed but before other database searches are" is split across PDF page 3 and page 4 of the S223 raw.

- `pdfinfo` Pages: 5. Per-page grep (receipt `w1/R96ExecWrap-page-and-linecount-receipts.txt`):
  - page=3: "after the MEDLINE" = 1, "Survey respondents and forum participants recommended" = 1.
  - page=4: "has been developed" = 1.
- Layout lines 167 and 170 hold the halves. Between them are line 168, a full-width running header ("LIGHTNING TALKS / PRÉSENTATIONS ÉCLAIR … 99"), and a blank line.
- Reading order: lines 226 and 230, with the same header at 228 (`w1/R96ExecWrap-wrap-sites.txt`).

Consequences:
- The entry's named limit (c) and the TREE_CHANGED bullet ("it wraps between two column lines") describe the Q6 miss incorrectly. The mechanism is a page break with a running header. The result (0 hits per line, not an absence of the statement) is right.
- The entry's rule (d) — consecutive column-line fragments are read as one sentence from line order — does not hold for L24–L25. Their fragments are not consecutive in line order (167 and 170), and a page furniture line separates them.

### F3 — decision row 3's Do cell attributes the timing sentence to PRESS 2015; its own warrant attributes it to survey and forum participants

Row 3 (timing) Do cell: "review the search strategy prior to executing the search; under PRESS 2015, after the MEDLINE search has been developed and before the other database searches are developed". Its warrant is L24–L25 (S223).

The source sentence is introduced by "Survey respondents and forum participants recommended":
- layout line 166 (right column) "Survey respondents and forum participants recommended", then line 167 "that peer review should occur after the MEDLINE search" (receipt `w1/R96ExecWrap-grep-receipts.txt`, the grep for "Survey respondents…").
- reading line 225 → 226.
- PDF page 3.

The abstract reports the recommendation as survey/forum output. The Do cell calls it "under PRESS 2015". The quotes do not make that attribution on their face, and the guideline statement was not opened (403, per the entry). This is a K2 narrowing: the Do cell should say "survey respondents and forum participants recommended …, reported in the PRESS 2015 abstract", or the row should be narrowed.

### F4 — which Do cells rely on sentences that exist only after column/page reconstruction

Fragment adjacency (receipt `w1/R96ExecWrap-fragment-adjacency.txt`; "contiguous" = the concatenated fragments occur in the whitespace-joined text):

| group | source | layout lines | reading lines | contiguous in layout-joined | contiguous in reading-joined |
|---|---|---|---|---|---|
| L4–L6 | S224 | 876, 877, 878 | 1335–1337 | no | yes |
| L7–L8 | S224 | 879, 880 | 1338, 1339 | no | yes |
| L9–L10 | S224 | 313, 314 | 466, 467 | yes | yes |
| L11–L13 | S224 | 915–917 | 1408–1410 | no | yes |
| L14–L16 | S224 | 912–914 | 1405–1407 | yes | yes |
| L17–L18 | S224 | 922, 924 | 1440, 1441 | no | yes |
| L19–L23 | S223 | 159–163 | 218–222 | no | yes |
| L24–L25 | S223 | 167, 170 | 226, 230 | no | no |
| L26–L29 | S223 | 171–174 | 231–234 | no | yes |

- Every one of the 30 quotes is located on a single physical layout line (no quote needs a join). K3 held.
- L17–L18 is consecutive in line order within the right column (layout line 923 has no right-column text), so rule (d) holds for it. Only L24–L25 breaks rule (d).
- Decision rows (numbered in the entry's table order) and their dependence:
  - Row 1 (Do: "document the review of this search specifically") rests on L7+L8 — needs reading-column reconstruction.
  - Row 2 (Do: "strongly consider … peer reviewed by an experienced searcher, information specialist or librarian") rests on L4–L6 — needs reading-column reconstruction.
  - Row 3 (Do: timing) rests on L24–L25, which exists only across a page break and a running header — see F2 and F3.
  - Row 4 (Do: six PRESS elements) rests on L19–L23 — needs reading-column reconstruction.
  - Row 5 (Never/Do on "complete or high recall"; Do: use peer review to identify errors) rests on L3 and L30, each on one line — not affected.
  - Row 6 (Do: describe deduplication processes) rests on L9–L10 (contiguous in layout) and L11–L13 (reading only).
  - Row 7 (Do: report the method so readers can evaluate) rests on L14–L16 (contiguous in layout).
  - Row 8 (Do: total after deduplication) rests on L17–L18 — needs reading-column reconstruction.

## Answers to the probe's questions

1. Does the entry's Q6 note and named limit (c) describe the result exactly? No.
   - Named limit (c) reports the correct result (per-line 0 hits) but misdescribes the mechanism: it is a PDF page break with a running header, not a wrap between two column lines, and joining whitespace does not recover the exact phrase. It under-states the limit.
   - The TREE_CHANGED bullet's "wraps between two column lines" is wrong on the same point.
2. Does any decision row's Do cell rely on a sentence that exists only across a column line break? Yes. Row 3 relies on a sentence that exists only across a PDF page break (and a running header); the Do cell also attributes it to PRESS 2015 where the warrant attributes it to survey and forum participants (F3). Rows 1, 2, 4, 6 (L11–L13) and 8 rely on sentences that exist in whole only after column reconstruction.
3. Does the probe's per-line under-count hypothesis hold? Partly: occurrences of the title (Q1) are under-counted per line. File-level hit sets are not changed by joining, and the Q6 statement is not recovered by joining.

## Named-limit check (C2)

- Limit (c) "a sentence wrapped across two layout lines is not found (the entry's Q6)": result correct; mechanism and remedy under-stated (F2).
- Rule (d) "consecutive column-line fragments are read as one sentence from line order": false for L24–L25 (F2); true for the other eight groups.
- K2 (a Do cell asserting what its warrant does not say): fired for row 3's PRESS 2015 attribution (F3).
- K3 (a quote located only by joining across columns): held — each quote is on one layout line.
- K4 (S223 tier/scope): not checked beyond the attribution in F3; the S223 scope cell was out of this probe.

VERDICT: R96ExecWrap C2 fired — the Q6 mechanism is a PDF page break with a running header, not a two-column-line wrap, and decision row 3's Do cell attributes to "PRESS 2015" a timing sentence whose warrant opens "Survey respondents and forum participants recommended"; the line-order rule (d) fails for L24–L25.
VERDICT: R96ExecWrap C1 n/a — not touched by this probe.

## Receipts (all in `.ufo/waves/round-96/w1/`)

- `R96ExecWrap-wrap-table.txt` — Table 1 counts (Python `re`, cross-checked with grep -c / grep -o|wc -l on the same files; grep-run values in the next receipt).
- `R96ExecWrap-grep-receipts.txt` — Q1 wrap sites (grep -n, rc=0), Q6 proximity and exact-phrase checks (rc=0/1), the attribution grep (rc=0), the LIGHTNING TALKS header grep (rc=0).
- `R96ExecWrap-page-and-linecount-receipts.txt` — pdfinfo (Pages 5), per-page location of the timing sentence, grep -c per-line table.
- `R96ExecWrap-wrap-sites.txt` — S223 layout 157–175, S223 reading 224–234, S224 layout 874–881 and 910–925.
- `R96ExecWrap-fragment-adjacency.txt` — table of F4.
- `R96ExecWrap-file-level-sweep.txt` — Table 2.

Scratch `/fast/scratch/hyaku/chousa-r96/R96ExecWrap` to be deleted before yield.
