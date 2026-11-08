# R95ScoutSources — round 95 source re-open and reading-order check for S222

Seat: `R95ScoutSources` (scout). Scope: read-only re-open of the S222 URL, reading-order extraction of the
ITEM 15 / ITEM 13 sentences, the co-publication claim, and the erratum question. Lane root
`/home/vgpnk/Projects/shokunin/chousa-shokunin`; scratch `/fast/scratch/hyaku/chousa-r95/R95ScoutSources`
(deleted on yield).

**Tree state note (read this first).** I attacked the frozen claim F `d6429e02` and the carrier C
`d27e9891` as instructed. While I worked, a parallel seat (`R95ExecC2Repro`) independently found the same
F1 defect, and the lane amended the **working tree** (uncommitted: `git status` shows `M` on
`.ufo/waves/round-95/claims.md` and `corpus/knowledge/search-rerun-record-r95.md`; HEAD is still
`bc94923b`, the wave-w1 dispatch commit, with carrier C at `d27e9891` and freeze F at `d6429e02` in
history). My F1 below is therefore a falsification of the **frozen claim F and carrier C as landed** — the
state I was asked to attack — and it is now corroborated by the lane's own amendment, which credits
`R95ExecC2Repro` F1. I re-measured the amended tree and **independently reproduce the amendment's own
enumeration** from the capture line numbers (Q7@931, Q10@932, Q11@933 | Q8@935, Q13@936, Q9@937), so the
amendment is correct on the source. My F2 has likewise been rewritten in the working tree
("cite the paper's title only" → "cite and discuss the paper (S204 has a section on it) but neither contains
that sentence"). **F3 remains live and unfixed in the amended tree** and is the actionable item from this
seat.

Tooling: **no install was needed**. Preinstalled and used: `/usr/bin/grep` = GNU grep 3.12 (modified),
`pdftotext` = poppler 26.10.0, `curl` 8.23.0, `python3` 3.14.8, `git` 2.56.0. No pacman/uv/npm transaction
was performed (the pacman guard is host-wide paused and nothing was missing).

---

## F1 — C2's "Q7–Q9 form one sentence" is FALSE as stated (fired)

**Claim wording under test.** `claims.md` C2 named limit (a):

> "Located means present in the capture's `pdftotext -layout` text after gate-records normalization; Q6–Q9 are
> single column-line fragments, and **that Q7–Q9 form one sentence** is read from layout."

and the entry `corpus/knowledge/search-rerun-record-r95.md:24` and `:59`:

> "that Q7-Q9 belong to **one ITEM 15 sentence** is read from the PDF's layout, not located."
> "Q7-Q9 are three located fragments of **one sentence** (two-column text form); their joining is read from the layout."

**What the source actually says.** Reading the publisher PDF in reading order (`pdftotext` **without**
`-layout`), the ITEM 15 explanation on page 13 contains **two** sentences, not one. Verbatim:

> S1: "If a reader tries to duplicate a search from a systematic review, one would expect to retrieve nearly
> the same results when limiting to the timeframe in the original review."
>
> S2: "If instead, the searcher locates a drastically different number of results than reported in the
> original review, this can be indicative of errors in the published search [22] or major changes to a
> database, both of which might be reasons to update a systematic review or view the systematic review's
> results with skepticism."

The fragments map as follows:

| fragment | text | sentence |
|---|---|---|
| Q7 | "If a reader tries to duplicate a search from" | **S1** (its opening clause) |
| Q8 | "drastically different number of results than reported in the" | **S2** |
| Q9 | "published search [22] or major changes to a database, both" | **S2** |

So the fragments **are** in source order (Q7 → Q8 → Q9), which is what the task asked me to check, but they
are **not one sentence**: Q7 ends S1 and Q8/Q9 sit inside S2. The word "instead" in S2 is the grammatical
give-away — S2 is a *contrast* to S1, which only makes sense as a separate sentence.

**Why this is a finding and not a quibble.** The sentence boundary is *not* only visible in the reading-order
extraction. It is visible **in the `-layout` capture itself, on a single physical line, inside one column**:

```
$ sed -n '934p' corpus/captures/1a8c36c4c24444967bd9c3ce.txt | cut -c1-68
      original review. If instead, the searcher locates a
```

The period after "original review." and the start of the next sentence ("If instead, the searcher locates a")
sit on the same layout line, in the same (left) column, with the other column's text in the right half of
that line. So the claim "that Q7–Q9 form one sentence **is read from the PDF's layout**" cannot be excused as
"the layout hides the boundary": the layout shows the boundary on line 934, and Q7 (line 931) and Q8 (line
935) sit two lines apart, with a full stop between them in between.

**Consequence for the decision rows.** The entry's decision table cites:

* row "Re-running a recorded search" — warrant "Q7, Q8 (S222, ITEM 15)", Do "expect nearly the same results
  when the search is duplicated over the original timeframe", Never "read a drastically different count as noise";
* row "Reading a different re-run count" — warrant "Q9, Q8 (S222, ITEM 15)", Do "treat it as indicating an
  error in the reported search or a major change to the database", Never "assume one cause without separating them".

Both rows lean on the "one sentence" premise to fuse Q7 (S1) with Q8/Q9 (S2). If they are one sentence, the
Do-cell "expect nearly the same results" and the Never-cell "read a drastically different count as noise" look
like they are describing two clauses of a single norm ("expect nearly the same … unless the count differs
drastically, which is then informative"). Split across S1 and S2 they are two *different* norms with different
subjects: S1 says a duplicate search "would expect to retrieve nearly the same results"; S2 says a drastically
different count "can be indicative of errors in the published search [22] **or** major changes to a database,
**both** of which might be reasons to update a systematic review **or view the systematic review's results with
skepticism**". S2's own final clause supplies a *third* consequence — skepticism about the review's results —
which no decision row carries. The "one sentence" reading is what makes the rows look like they cover the
whole passage.

**What the instrument does and does not enforce.** `tools/gate-records.py verify` passed 9/9 and
`entry-controls-r95.py` reported `LQ_BOUND=9/9 WARRANTS_OK=7/7`, `ENTRY_CONTROLS=PASS` at the carrier — because
every fragment *is* literally present in the capture. The instrument checks **location**, never sentence
unity, so it cannot catch this. `LQ_BOUND`/`WARRANTS_OK` are green on a false premise. That is exactly the
"the stated sentence says more than its instrument enforces" shape the task asked me to look for.

**Scope of the defect.** It is a wording/scope defect in the claim and the entry, not a quote-location defect:
all 9 quotes are located (verified independently below), and the 7 decision rows each have a real warrant
fragment in the right ITEM. The fix is a wording fix: "Q7–Q9 span two ITEM 15 sentences" (and either cite
the sentence boundary or drop the fused reading). No row needs withdrawal on the evidence I gathered.

**Receipts.** `.ufo/waves/round-95/w1/R95ScoutSources-B-item15.txt` (verbatim S1/S2, the mapping table, the
`sed -n '934p'` boundary line, and the reading-order source lines 1420-1437).

---

## F2 — the entry's "before" narrative about S120/S204 is FALSE as stated (secondary)

**Status: corrected in the amended working tree.** The amended entry now reads "two captures (S120's Cochrane
chapter, S204's Campbell guide) cite and discuss the paper (S204 has a section on it) but neither contains
that sentence" — accurate, and the same correction this finding argues for. What follows is the evidence
against the **frozen F / carrier C** wording that this seat was asked to attack.

**Claim wording under test.** `corpus/knowledge/search-rerun-record-r95.md:13-14` (at F and at carrier C):

> "two captures (S120's Cochrane chapter, S204's Campbell guide) **cite the paper's title only**"

**What the two captures actually contain.**

* **S120** (`corpus/captures/c9d1e74c3ac8d9eb332c9770.txt`, Cochrane handbook ch. 4) does not cite the title
  only. At line 886 it **quotes the paper's item-14 sentence and attributes it**:
  > "The PRISMA-S Extension states that authors "should strongly consider having the search strategy peer
  > reviewed by an experienced searcher, informational specialist, or librarian" ( Rethlefsen et al 2021 )"

  (the capture's own wording is "informational specialist"; PRISMA-S itself reads "information specialist"
  — the capture's quotation is thus also not perfectly accurate, which is a further reason the "title only"
  description is wrong.)
* **S204** (`corpus/captures/c52a1f15884a78028febcf43.txt`, Campbell guide) reproduces a whole
  **"Reporting Items from PRISMA-S"** list (lines 2189-2320) covering PRISMA-S items 1, 2, 3, 8, 9, 12, 13 and
  16 in substance — including "Full search strategy for each database (including all database syntax as run in
  each database)", "Limits applied to the search and justification for use; if no limits, indicate no limits
  were applied", "Dates of final search in each database", "Date of search rerun for updating the corpus",
  "Total search yield from each database", "Process for deduplicating results" — and at line 2319 it **quotes
  the paper's item-6 sentence with attribution**:
  > "As these strategies are inherently difficult to reproduce, researchers should attempt to give as much
  > detail as possible on what data or information was sought, who or what group(s) provided data or
  > information, and how the individuals or groups were identified' (Rethlefsen et al., 2021 )"
  and at line 2174 it reproduces item 8's requirement: "The search strategies for each database will need to be
  **copied and pasted exactly as run**".

Both captures therefore carry PRISMA-S **content**, not just the title. (Note the irony: S204's item-8 wording
is why the C1 record's Q2 search `exactly as run` matches S204 and S120 — the lane's own fixture depends on
these captures containing PRISMA-S wording, not just its title.)

**Why this matters beyond wording.** The sentence is doing work: it justifies why the entry needed a *new*
capture. If the two pre-existing captures already carried PRISMA-S's item-6 and item-14 sentences and a
reporting-items list, the stated reason for the gap is not "the corpus only had the title". The narrower,
accurate version is: no pre-existing capture contained the **item-15** sentence (which is what the "Before"
line and `c2-base.txt` actually test, and that *is* true — see F4).

**Receipt.** `.ufo/waves/round-95/w1/R95ScoutSources-D-title-only.txt`.

---

## F3 — the SOURCES.md row's "10:39" locator is not in the captured source — STILL LIVE (secondary)

**Status: still present in the amended working tree.** `grep -c '10:39' corpus/SOURCES.md` → 1 (one hit),
while `grep -c '10:39' corpus/captures/1a8c36c4c24444967bd9c3ce.txt` → 0, exit 1 (absent from the capture).
Neither the freeze, the carrier, nor the amendment changed this row.

`corpus/SOURCES.md:234` (S222) reads:

> "... — Journal of the Medical Library Association 109(2):174-200, 2021, doi 10.5195/jmla.2021.962
> **(co-published in Systematic Reviews 10:39)** — https://jmla.pitt.edu/ojs/jmla/article/download/962/1274"

The captured PDF **does** state the co-publication, on page 1 as a footnote to the title:

> "\* In order to encourage broad adoption of PRISMA-S, this article **will also be published in Systematic
> Reviews** (https://doi.org/10.1186/s13643-020-01542-z)."

But the string `10:39` is **nowhere** in the JMLA PDF (`grep -n '10:39'` over both extractions → exit 1, not
found). `10:39` is the Systematic Reviews *volume:article* locator; it is not a fact the cited capture
states. The lane never captured the Systematic Reviews version — `corpus/evidence/round57/refetch.tsv:190`
shows that S222's other URL (the EuropePMC `fullTextXML`) failed (`curl_rc=22`, `http=500`), which my
re-open of the same URL also failed to fetch (curl exit 28, timeout). So "10:39" is correct as an external
fact (Systematic Reviews 2021;10(1):39 is confirmed by the publisher and PubMed) but is **not sourced by the
cited capture**. The row's own source supports "co-published in Systematic Reviews" (with the DOI); it does
not support "10:39".

**Receipt.** `.ufo/waves/round-95/w1/R95ScoutSources-E-erratum.txt`.

---

## F4 — checks that HELD (no findings)

### (a) The S222 re-open is byte-identical

One read-only GET, as specified, into scratch only:

```
$ curl -fsSL --max-time 30 -o $S/jmla962_1274.pdf \
    -w 'HTTP=%{http_code} SIZE=%{size_download}\n' \
    https://jmla.pitt.edu/ojs/jmla/article/download/962/1274
HTTP=200 SIZE=532659
```

* `sha256` of the fetched PDF = `07036f03c4c08ce9eec02d17d904509a2b26431abe0bba0e3bc823d2c58d9ec2` — **identical**
  to the S222 `raw_sha256` in `corpus/evidence/round57/refetch.tsv:191`, and identical to the committed
  `corpus/captures/1a8c36c4c24444967bd9c3ce.raw` (532 659 bytes).
* `pdftotext -layout` of the fetched PDF reproduces the committed capture **byte for byte**:
  `sha256 = 86f1aacd558377129dc79b8c1bc27a686ebfc668eb78a58204dea41043db3871` = the committed `.txt` = the
  S222 `txt_sha256` in refetch.tsv; `diff -q` → identical. The capture is reproducible from the URL, and the
  `.txt` is genuinely the `-layout` form of that PDF, as the entry states.
* No network fetch was made against any other host for the corpus, and nothing under `corpus/captures` or
  `refetch.tsv` was written. The second S222 URL (EuropePMC) was attempted read-only into scratch and
  timed out (curl exit 28); it is reported here for completeness, not used as evidence.

Receipt: `.ufo/waves/round-95/w1/R95ScoutSources-A-fetch.txt`.

### (b) All 9 quotes are located, and none needs a cross-column join

Independently of `gate-records.py` I reconstructed each PDF page's left column (`xMax<=302`) and right
column (`xMin>=302`) as separate single streams from `pdftotext -bbox` output and tested each quote. Every
quote is present **within one column of one page**: Q1 p.9 L, Q2 p.12 L, Q3 p.13 L, Q4 p.11 R, Q5 p.10 L,
Q6 p.12 R, Q7 p.13 L, Q8 p.13 L, Q9 p.13 L. **K3 holds** — no quote is located only by joining across the two
columns. (Q1–Q5 also appear on the checklist pages 4–5, where the table's own cells wrap; the page-9/10/11/12/13
copies are the unwrapped ones.) The Located-quotes table equals the 9 `GATE-RECORD` quote values 9/9, in
order. All 7 rows' item numbers check out against the PDF's own checklist table (items 8, 9, 13, 15, 15, 15,
12 → 7/7 correct).

Receipt: `.ufo/waves/round-95/w1/R95ScoutSources-G-items-and-columns.txt`.

### (c) The ITEM 13 "slice" sentence

Verbatim, from PDF page 12 right column (ITEM 13 "Dates of searches"):

> "In addition, it supports reproducibility and updating by allowing other researchers to use date limits to
> view the same "slice" of the database that the original authors used or to update a systematic review by
> searching from the last time point searched."

Q6 ("to view the same "slice" of the database that the original") is a fragment of this sentence, and it
*is* in ITEM 13 — the entry's use of it there is sound.

Receipt: `.ufo/waves/round-95/w1/R95ScoutSources-C-item13.txt`.

### (d) The C1 record's 8 searches reproduce exactly at base

Re-ran all 8 with GNU grep 3.12 over a `git archive` of base's `corpus/captures` (90 `.txt` files at base).
Every recorded count, every explicit hit-set, and both sha256 digests reproduce. The Python-`re` engine (the
one `tools/search-rerun.py` actually uses) agrees on all 8 expressions and both digests — so named limit (a)
of C1 holds on these 8 expressions. At the carrier, `tools/search-rerun.py verify` prints
`SEARCH_RERUN_SUMMARY searches=8 rev_match=8/8 tree_same=3/8 findings=0` / `SEARCH_RERUN: CLEAN` (exit 0) and
the battery prints `POSITIVE=1/1 STRICT_TREE=1/1 FORGERY_REFUSED=8/8 PRIOR_ACCEPTED=8/8 SETUP_REFUSED=12/12
CLONE_TREE=2/2 DO_NOTHING_REFUSED=1/1 ORACLES_REJECTED=3/3` / `RERUN_CONTROLS=PASS` (exit 0); the C2 gate
prints `GATE_RECORDS files=1 records=9 ok=9 fail=0` and the entry battery `POSITIVE=1/1 FORGERY_REFUSED=8/8
DO_NOTHING_REFUSED=1/1 GATE_RECORDS=9/9 LQ_BOUND=9/9 WARRANTS_OK=7/7 METADATA=clean` / `ENTRY_CONTROLS=PASS`.
The 5/8 `TREE_CHANGED` rows are the designed signal that the corpus moved after base (the S222 capture was
added at the carrier) and are not drift in the recorded values.

Receipt: `.ufo/waves/round-95/w1/R95ScoutSources-F-c1-record.txt`.

### (e) No newer PRISMA-S version, no erratum

Five web searches (PRISMA-S erratum/correction; 2025 revision; Springer correction notice; JMLA publisher
record; PubMed/EuropePMC linkage) agree: **no** erratum, correction, retraction or publisher note is
attached to either the JMLA version (PMID 34285662) or the Systematic Reviews version (PMID 33499930). The
2021 16-item checklist is still the current and only PRISMA-S checklist; the "2025" that appears in
circulation is EQUATOR's `record last updated 2025-02-06` catalogue metadata, not a revision. **Nothing
changes items 8, 9, 12, 13 or 15.** The "Erratum in: Systematic Reviews" wording that surfaces near PRISMA-S
in third-party bibliographies belongs to *other* references (in the lane's own S120 capture the single
"Erratum" hit, line 1197, is O'Mara-Eves 2015;4:5 — unrelated; and PRISMA 2020 itself carries
`Erratum in: Rev Esp Cardiol 2022;75(2):192`). The lane's capture is internally consistent with this.

Receipt: `.ufo/waves/round-95/w1/R95ScoutSources-E-erratum.txt`.

---

## Independent verification of the amended working tree (added after the amendment landed)

Since the lane amended under me, I re-measured the amended artifacts so the lane knows its own fix is
source-correct:

* **The amended 13 quotes are all located** in the committed capture, and each of Q5–Q13 lies on exactly one
  physical line of the capture (`Q5`@267, `Q6`@832, `Q7`@931, `Q8`@935, `Q9`@937, `Q10`@932, `Q11`@933,
  `Q12`@269, `Q13`@936). Q1–Q4 are the checklist-table statements, which wrap inside table cells (hence no
  single physical line) — consistent with the amended entry's "Text form" paragraph, which now claims the
  single-column-line property only for "Q6–Q11 and Q13".
* **The amended reading-order enumeration is correct.** From the capture line numbers: sentence 1 = Q7(931),
  Q10(932), Q11(933); sentence 2 = Q8(935), Q13(936), Q9(937). This matches the amended
  `claims.md` named limit (a) — "Q7, Q10, Q11 are one ITEM 15 sentence and Q13, Q8, Q9 the next" — exactly,
  and it matches my own independent reading-order extraction.
* **The amended decision rows now attribute cells to the right sentence**: row "Re-running a recorded search"
  warrants "Q7, Q10, Q11 (Do), Q8 (Never)"; row "Reading a different re-run count" warrants "Q13, Q9, Q8".
  Q7/Q10/Q11 are the "expect to retrieve nearly the same results …" sentence and Q8/Q13/Q9 the "If instead …"
  sentence, so the two rows no longer fuse two sentences into one norm.
* **Q12 is real**: it is the tail of the item-9 checklist statement ("and provide justification for their
  use."), capture line 269, and the amended row "Filing where a search looked" warrants "Q5, Q12 (S222,
  item 9)" with the Do cell "…and justify them" — which the source's "provide justification for their use"
  supports. This is the one thing the frozen 9-quote entry could not have said, since Q12 was not yet quoted.

Nothing in my re-measurement contradicts the amendment. The amendment's source claims are sound.

---

## What the lane should change

1. **F3 (still live).** `corpus/SOURCES.md:234` — the S222 row's "(co-published in Systematic Reviews 10:39)"
   cites a locator that the cited capture does not contain. Either cite the Systematic Reviews version for
   "10:39" (it was never captured: `refetch.tsv:190` shows the EuropePMC attempt failed with
   `curl_rc=22`/`http=500`, and my re-open of it timed out), or drop "10:39" and keep the DOI the JMLA PDF
   itself prints (`10.1186/s13643-020-01542-z`).
2. **F1 / F2 — already amended** in the working tree on the strength of `R95ExecC2Repro` F1; my findings
   corroborate them and I have verified the amended wording against the source. No further change needed.

---

VERDICT: R95ScoutSources C2 fired — against the frozen claim F and carrier C, the named limit (a) and the entry both assert Q7–Q9 "form one sentence", but the publisher PDF in reading order shows Q7 ends ITEM 15's first explanation sentence while Q8 and Q9 sit in the second, with the boundary visible in the -layout capture itself at line 934; a parallel seat found the same defect and the lane has since amended the working tree, which I independently verified as source-correct, leaving only the SOURCES.md "10:39" locator (F3) still live.
VERDICT: R95ScoutSources C1 held — the S222 URL re-opens byte-identically to the committed capture (raw and -layout sha256 both match refetch.tsv), all 8 recorded searches reproduce exactly at base under both GNU grep 3.12 and Python re, and both predicates pass at the carrier.
