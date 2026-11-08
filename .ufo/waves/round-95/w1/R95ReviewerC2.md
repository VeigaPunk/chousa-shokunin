# R95ReviewerC2 — fidelity review: `corpus/knowledge/search-rerun-record-r95.md` at C (d27e989) against S222 capture

Seat: R95ReviewerC2. Tree: clone of `/home/vgpnk/Projects/shokunin/chousa-shokunin` checked out at
`d27e9891ba6d2bae8b1f6060f7c01bf13a1a6ea1` under `/fast/scratch/hyaku/chousa-r95/R95ReviewerC2/repo`
(`git rev-parse HEAD` → `d27e9891ba6d2bae8b1f6060f7c01bf13a1a6ea1`, exit 0 — see `R95ReviewerC2-source-table1.txt`).

Named axes (godspeed): **axis 1 — warrant fidelity** (does each Do/Never cell say only what the cited quote says?),
**axis 2 — provenance marking** (is every non-PRISMA-S statement confined to the `Lane` column?).

Instruments (all re-run, all pass — the claim's *wording* is the attack surface, not these):

- `python3 -B tools/gate-records.py verify --root <repo> corpus/knowledge/search-rerun-record-r95.md` → exit 0,
  `GATE_RECORDS files=1 records=9 ok=9 fail=0` (`R95ReviewerC2-gate-records.txt`).
- `bash tools/research-gate.sh verify-metadata corpus/knowledge/search-rerun-record-r95.md --root <repo>` →
  exit 0, `METADATA_COMPLETE=1/1`, `RESEARCH_GATE: CLEAN` (`R95ReviewerC2-research-gate-metadata.txt`).
- `python3 -B corpus/evidence/round95/entry-controls-r95.py --root <repo> --work <scratch>` → exit 0,
  `POSITIVE=1/1 FORGERY_REFUSED=8/8 DO_NOTHING_REFUSED=1/1`, `LQ_BOUND=9/9 WARRANTS_OK=7/7`,
  `ENTRY_CONTROLS=PASS` (`R95ReviewerC2-entry-controls.txt`).

Q-table/GATE-RECORD identity: the 9 `GATE-RECORD` quote strings equal the 9 Located-quotes Q1–Q9 strings
one-to-one (script-compared, all match=True); capture `sha256 86f1aacd…dea41043db3871` matches the file's
`sha256sum`. Q1–Q9 word counts (16/12/14/13/12/11/9/9/10) recomputed from the strings match `words=` on the
GATE-RECORD lines. No column-join: each Q resolves to a single column-line fragment in the two-column
`pdftotext -layout` text.

## Decision-row table (each row separately)

| row | verdict | why | minimal rewording |
|---|---|---|---|
| 1 Filing expression (Do/Never, Q1 item 8) | faithful | Do = Q1 verbatim ("for each database and information source, copied and pasted exactly as run", capture lines 262–265; Table 1 item 8). Never = contrapositive (paraphrase/summary/one example), which refusal-by-example the ITEM 8 explanation supports ("document exactly as run… accurately recorded"). Lane cell holds `expression`+`search-rerun.py` reading. | — |
| 2 Filing where (Do/Never, Q5 item 9) | overreach (Do understates) | Do quotes Q5 but Q5 is truncated: the checklist item continues "applied to a search (e.g., date or time period, language, study design) and provide justification for their use" (capture lines 267–270); the ITEM 9 line (694–695) likewise ends mid-sentence in the entry's fragment. Both Do and the warrant omit the **justification duty**, so the row licenses filing limits without the justification PRISMA-S requires for them. The Never ("leave the searched scope implicit") is otherwise a faithful contrapositive and the Lane glob reading is correctly in Lane. | Do: "state that no limits were used, or describe any limits or restrictions applied to a search (e.g., date or time period, language, study design) and provide justification for their use". Or narrow the warrant to "declare the limits as applied" and move the justification duty to a separate row / Lane cell. |
| 3 Filing when (Do/Never, Q2 item 13) | faithful on Do/Never; lane-unmarked on Lane's "slice" | Do = Q2 verbatim ("For each search strategy, provide the date when the last search occurred", lines 296/864). "For each strategy" is explicit in Q2, so Never (one date for several strategies) follows. **Lane defect:** Lane says "for a corpus under version control the revision is the same 'slice' Q6 describes". Q6's sentence is about **date limits**, not revisions: "allowing other researchers to use **date limits to view the same "slice" of the database** that the original authors used or to update a systematic review by searching from the last time point searched" (lines 826–835; ITEM 13 explanation, dated-search context). Mapping a git revision onto that sentence is the lane's analogy, presented as if Q6 itself described version control. The C2 sentence requires the Lane column to be marked as the lane's reading; here the analogy rides on a quote to make it look like PRISMA-S's. | Lane: "…the record files the date and the committed revision; the lane reads the revision as analogous to the "slice" Q6 describes, which in PRISMA-S is created by **date limits**, not by a revision." |
| 4 Filing what found (Do/Never, Q3 item 15) | overreach (Never imports item 16) | Do = Q3 verbatim ("Document the total number of records identified from each database and other information sources", lines 309/893–895). "Total" here is **per-source** ("from each database and other information sources"), so Do is faithful and the per-source reading in my brief is confirmed: Q3 mandates per-source counts, not one grand total. **Never overreaches:** "report only the deduplicated total, losing the per-source count" — Q3 says nothing about deduplication. The dedup contract is **item 16** ("Describe the processes and any software used to deduplicate records…", capture ITEM 16 block), and the ITEM 15 explanation never contrasts per-source counts with a deduped total. The Never presents the lane's (sensible) ordering of items 15 vs 16 as if it were in Q3. | Never: "report only the grand total, losing the per-source count". If the dedup point is wanted, cite item 16 and warrant it there (Q-item), or move "report per-source, not just deduped" into Lane. |
| 5 Re-running (Do/Never, Q7+Q8 ITEM 15) | overreach (Do warranted by an unquoted gap) | Do: "expect nearly the same results when the search is duplicated over the original timeframe". The **words "nearly the same" / "timeframe"** are **not in Q7 or Q8**: capture lines 931–935 read "…one would expect to retrieve **nearly / the same results when limiting to the timeframe in the / original review**." That is the **intervening line(s) between the two located fragments** — Q7 ends at "from", Q8 starts at "drastically". The Warrant cites Q7+Q8 as if they entail "nearly", but as located strings they entail the opposite (Q8's "drastically different" is the *failure* case). The entry's Text-form paragraph (entry lines 22–24) discloses that joining Q7–Q9 is "read from the PDF's layout, not located" — but the per-row Warrant does not carry that qualification forward, and the Do's "nearly" is the load-bearing word for the whole two-revision doctrine. C2 kill-rule K2 applies. | Warrant: "Q7+Q8 plus the intervening unlocated line 'one would expect to retrieve nearly the same results when limiting to the timeframe in the original review' (layout-read, not located)". Or drop "nearly" from the Do: "expect the same results… (Q7's 'duplicate a search from' + intervening line, layout-read)". |
| 6 Reading different count (Do/Never, Q9+Q8 ITEM 15) | faithful (one substitution to note) | Do: "indicating an error in the reported search or a major change to the database". Source, lines 936–937: "this can be **indicative of errors** in the **published search** [22] or **major changes to a database**". Two live compressions: plural "errors" → singular "an error"; "published search" → "reported search". The second is defensible (the lane's record *is* the reported search; the entry's own frame is reporting), the first drops the source's openness to multiple errors. Neither changes the doctrine. Never ("assume one cause without separating them") follows from the source's disjunction ("both of which might be reasons to update a systematic review"). Lane two-revision split is the lane's reading and is correctly in Lane; Named-limits also discloses it. | "indicating errors in the published (reported) search or major changes to a database" — or keep Do and note the plural in Warrant. |
| 7 Updating (Do/Never, Q4 item 12) | faithful | Do = Q4 verbatim ("Report the methods used to update the search(es) (e.g., rerunning searches, email alerts)", lines 292/777). Never ("update silently and keep the old date") is the contrapositive plus item-13's date duty; the old-date half belongs to item 13, but the composite is the lane's Never phrasing and does not attribute item 13's sentence to Q4. Lane TREE_CHANGED cue is the lane's reading, correctly confined to Lane. | — |

## Prose-pointer checks (entry lines 9–20)

| claim | verdict | why | evidence |
|---|---|---|---|
| "at the base revision `7b237358` no `.txt` capture contains the item-15 sentence (`/usr/bin/grep -l -F` over `corpus/captures/*.txt`, exit 1)" | faithful | Re-ran at base from `git archive 7b237358 corpus/captures` (183 files incl. `.raw`): `/usr/bin/grep -l -F "Document the total number of records identified" <base>/corpus/captures/*.txt` → exit 1, no file. At C the only hit is the new S222 capture `1a8c36c4c24444967bd9c3ce.txt` (exit 0). Known-unknown: entry names the search string and the exit code; reproducible. | `R95ReviewerC2-prose-base-grep.txt` |
| "two captures (S120's Cochrane chapter, S204's Campbell guide) cite the paper's **title only**" | overreach | S120 = `c9d1e74c3ac8d9eb332c9770.txt` (210,708 chars, matches SOURCES.md; `4.2.1 Role of the information specialist/librarian` present) — **contains more than the title**: line 578 cites "(Rethlefsen et al 2021)"; line 886 quotes PRISMA-S ("authors 'should strongly consider…' (Rethlefsen et al 2021)"); line 887 names the evaluation paper; line 1214 is the PRISMA-S reference-list entry. S204 = `c52a1f15884a78028febcf43.txt` — line 1992 names the PRISMA-S Extension, **§9.1.2 (lines 2167–2169, 2178, 2183–2189) is a PRISMA-S guidance section** with quoted item-6 language (line 2319), plus reference-list entries (lines 3755, 3769). What is true is that neither contains the **item-15 checklist sentence**; "cite the paper's title only" states more than that. | `R95ReviewerC2-prose-base-grep.txt` (lines quoted) |
| "the DOI route the lane tried earlier returned a `Client Challenge` page (`corpus/lessons/round-47.md:251-253`)" | faithful | Entry lines 251–253 (numbered): "`search-log-fields-r36.md` (staged) — **refused again**… the PRISMA-S DOI capture is still a 267-byte `Client Challenge` page (register S077)". Verbatim match for the lane's point. | `R95ReviewerC2-pointers.txt` |
| "the sweep re-run is a glob/existence check over the named locations, never the recorded command (`corpus/README.md:398-399`)" | faithful | README lines 398–399 (numbered): "(vacuity passes); **the sweep re-run is a glob/existence check over the named locations, never the recorded command**; section absence is still r1's to flag". | `R95ReviewerC2-pointers.txt` |
| "the pointer `corpus/README.md:390-391` at line 1108 is stale" | faithful | README line 1108 reads "`corpus/README.md:390-391` records the gap: the sweep re-run is…" — lines 390–391 are about a different move ("Round 5 ran the last registered r1 structural move… both fixtures closed CLEAN structurally under `verify` at `6b83705b…`", lines 389–392), and the glob/existence sentence is at 398–399. Line 1108's own pointer is stale; the new entry's 398-399 is the live one. | `R95ReviewerC2-pointers.txt` |
| "Neither holds PRISMA-S's own checklist text" (r84/r39) | faithful | `/usr/bin/grep -c -F` for "copied and pasted exactly as run" and "Document the total number of records identified" over both `search-transparency-reporting-r84.md` and `search-log-method-r39.md` → 0 in all four. | receipt (this report; rerun = `grep -c` above, exit 1 = no match) |
| Governance "PRISMA 2020 items 6-8 and 16a through `S214`" | faithful | SOURCES.md S214 row: "PRISMA 2020 checklist PDF… **items 6,7,8,16a**; PDF text capture a640b15…". Matches. | — |

## Cross-cutting findings

- **F1 (K2, row 5).** The entry's `WARRANTS_OK=7/7` instrument measures *that a warrant is attached*, not that the
  warrant entails the Do. Row 5 is the standing example: the two attached fragments do not contain the word
  "nearly" on which the Do and the whole two-revision split depend. The entry's own Named-limits flag this
  ("expects 'nearly' the same results") but the Warrant column does not. This is the C2 sentence's "each row's
  Do/Never is warranted by located quotes" being false *for row 5 as stated*, under the lane's own kill rule K2.
- **F2 (row 3 Lane).** The only place where a quote is affirmatively *misdescribed as to subject matter*.
  "Slice" is a date-limits concept; reading a git revision as "the slice Q6 describes" is lane analogy, and
  the Lane column does not mark it as such. Under the C2 sentence ("each row's Lane column is marked as the
  lane's reading, not a PRISMA-S requirement"), row 3's Lane is lane-unmarked on the exact point the seat
  brief flagged.
- **F3 (row 4 Never).** The dedup-total prohibition is item 16's business, not Q3's. Harmless as doctrine,
  wrong as warrant — a reader carrying the table forward will cite Q3 for an item-16 rule.
- **F4 (prose, title-only).** "Cite the paper's title only" is falsifiable in both directions: S204 has a whole
  §9.1.2 on PRISMA-S; S120 quotes its peer-review sentence. The honest sentence is "neither contains the
  item-15 checklist sentence". `r5`-style provenance prose about the corpus's contents is exactly what this
  lane attacks in others; here it overstates.

## Verification gaps

- F1 depends on the two-column join ("the intervening line is unlocated"). Verifying the *layout* (that
  Q7–Q9 really form one ITEM 15 sentence) is read from the `pdftotext -layout` columns; I confirmed the
  column reading is coherent (lines 931–937 form "If a reader tries to duplicate a search from a systematic
  review, one would expect to retrieve nearly the same results when limiting to the timeframe in the original
  review…") but no independent PDF render was run this seat (network would be needed for a re-open, and the
  brief allows a scout item only — which I did not need).
- Sources `S078`/`S214` file-level claims were checked against SOURCES.md and the two knowledge files only;
  I did not re-open every cited `search-transparency-reporting-r84.md` section heading.
- No claim was tested against a differently-composed entry; WARRANTS_OK=7/7 measures wiring, not fidelity
  (by the C2 Named-limit (b), which is accurate: "the instruments check that a warrant exists, not that the
  paraphrase is faithful — that is the wave's reviewer item").

## Receipts

All receipts in `.ufo/waves/round-95/w1/` (paths relative to lane root):
`R95ReviewerC2-gate-records.txt`, `R95ReviewerC2-research-gate-metadata.txt`,
`R95ReviewerC2-entry-controls.txt`, `R95ReviewerC2-source-table1.txt`,
`R95ReviewerC2-source-items.txt`, `R95ReviewerC2-prose-base-grep.txt`, `R95ReviewerC2-pointers.txt`.
Scratch tree under `/fast/scratch/hyaku/chousa-r95/R95ReviewerC2/` removed on exit.

VERDICT: R95ReviewerC2 C2 fired — row 5's Do ("nearly") is warranted by an unlocated intervening line, row 3's Lane mislabels a date-limits "slice" as a git revision, row 4's Never imports item 16 into Q3, and the "title only" prose overstates S120/S204.
