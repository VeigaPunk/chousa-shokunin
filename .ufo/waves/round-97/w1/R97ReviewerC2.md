# R97ReviewerC2 — fidelity review of `corpus/knowledge/press-checklist-questions-r97.md` at F `9a0ce2015fa0254848f2f32f612b20caf7dc5478`

Attacked tree: clone `/fast/scratch/hyaku/chousa-r97/R97ReviewerC2/repo` checked out at F (`git -C ... rev-parse HEAD` = `9a0ce2015fa0254848f2f32f612b20caf7dc5478`; `--show-toplevel` = the clone). Scope: 8 decision rows (Do/Never vs warrants), `## Two reprints compared`, Lane cells vs `tools/search-rerun.py`, SOURCES.md S225–S227 vs bytes. Nothing run that writes into the lane; no network; no subagents.

Receipts (all in `.ufo/waves/round-97/w1/`):
- `R97ReviewerC2-recount.txt` — per-quote substring line numbers for L1–L29; verbatim/letters recount over S226.
- `R97ReviewerC2-searches-and-tool.txt` — Q1–Q7 re-grep at F; `search-rerun.py` run_at_rev / run_on_tree / evaluate lines.
- `R97ReviewerC2-lane-claims.txt` — controlled-vocabulary grep over captures; SKILL.md framing grep; "does not apply / says so" grep.
- `R97ReviewerC2-anchors.txt` — S225 form-feed page map; L21+L22 word count.

Commands and results (Python cells run in the kernel; grep commands `/usr/bin/grep`, GNU 3.12, `rc=0` on each):
- Quote recount: `quotes parsed: 29`; S225 verbatim-in-S226 `10/26`, letters (digits kept) `14/26`, letters (digits dropped) `20/26`. Every S225 quote is a substring of one capture line (L21 and L22 both on line 73; L1 line 21 … L26 line 82). L27–L29 are substrings of S226 `1-line` text as stated.
- Q1–Q7 at F: Q1 2, Q2 2, Q3 2, Q4 5, Q5 6, Q6 5, Q7 14 files, all `rc=0`. Each is the entry's base count plus the two round-97 captures (347c55 and 80a844), so consistent with the base record; not a finding.

## Findings (severity order)

**F1 — stated corroboration count is wrong (K5 fired).** Lane cell of row "Citing the checklist": "12 of the 26 S225 quotes are not found verbatim in S226". The entry's own control prints `VERBATIM=10/26`, so 16 are not found verbatim. Recount: `R97ReviewerC2-recount.txt` (verbatim = 10). The 12 figure is the *letters* miss count (26−14), not the verbatim miss count.

**F2 — `## Two reprints compared` misclassifies the 12 letters-misses (K5 fired).** The paragraph says "Of the 12 not found under *letters*, 5 are element headings … and five are questions where the wording itself differs", then lists L12, L20, L15, L13 (four questions). Per-quote result (`R97ReviewerC2-recount.txt`, digits kept): not found under letters = L1, L2, L3, L8, L11, L12, L13, L14, L15, L18, L20, L23. That is **six** headings (L3, L8, L11, L14, L18, L23), two pointer/title lines (L1, L2), and **four** questions (L12, L13, L15, L20). L26 is found under letters (`letters_S226=1`), so the entry's placement of it inside the 12 is also wrong. Correct breakdown: 6 + 2 + 4 = 12.

**F3 — the 14/26 "letters" figure is digit-sensitive; the entry does not say so.** The six heading misses occur only because S225 prints numerals ("1. Translation …") and S226 does not. With digits dropped, letters = **20/26**. The entry's definition ("not a letter or digit") is followed, so 14/26 is literal to its definition, but the headings-are-wording-differences reading the paragraph gives depends on that choice. Not a misstatement of the numbers; a missing qualifier.

**F4 — row 2 Lane cell overstates what the tool counts (C2 K2 fired).** Lane: "the lane's `## Searches` record files one count per expression (`hits`), which is its form of hits per line; `tools/search-rerun.py` re-derives each count". The tool's `hit()` returns a boolean per *file* (`tools/search-rerun.py:248-255`), `run_at_rev` appends one path per file (`:287-298`), and `evaluate` compares `len(at_rev)` (a file count) to the recorded `hits` (`:364-365`). So `hits` = number of files containing a match, not a count of matching lines. The checklist's ask ("show the number of hits per line") is not met; the Lane cell says it is. Receipt: `R97ReviewerC2-searches-and-tool.txt`.

**F5 — row 4 Lane cell: "the lane's capture store has no controlled vocabulary" is false as written (K2-adjacent wording overreach).** `grep -n -i -E 'emtree|mesh|thesaurus' corpus/captures/*.txt` (rc=0) returns 12 captures, several with MeSH/Emtree/thesaurus text (e.g. `c9d1e74c3ac8d9eb332c9770.txt:722` "Identify appropriate controlled vocabulary (e.g. MeSH, Emtree …)", `c52a1f15884a78028febcf43.txt:1670` "Databases often have their own thesaurus of controlled vocabulary terms"). The intended claim (the lane's *searches* use no subject-heading vocabulary) is plausible from the seven expressions, but the cell asserts something about the capture store that the store contradicts. Also "a record says so rather than counting the element as passed": no record in `## Searches` states that the element does not apply; the sentence appears only in this Lane cell (`grep "does not apply|says so"` → 2 matches, both in the row-4 Lane cell). Receipt: `R97ReviewerC2-lane-claims.txt`.

**F6 — L21/L22 locator and length are wrong in the entry prose.** `## Located quotes` says L21 and L22 "are the two halves of one 32-word question on capture line 74". The substring search places both on **line 73** (`R97ReviewerC2-recount.txt`, `L21 … line=[73]`, `L22 … line=[73]`; line 74 is blank in the capture). The joined question is **30** words (`R97ReviewerC2-anchors.txt`, `L21+L22 words … 30`). Not a quote-fidelity failure; a wrong locator and a wrong count in prose.

**F7 — SOURCES S225 page anchor is partly wrong.** SOURCES row S225: "page 2, PRESS 2015 Guideline Evidence-Based Checklist, elements 1-6 and the 'Derived from' citation; page 1 PRISMA-S item 14 pointer". The capture's form-feed pages (`R97ReviewerC2-anchors.txt`): page 1 contains "See PRESS checklist below", the "PRESS 2015 Guideline Evidence-Based Checklist" heading and "Translation of the research question" (element 1); page 2 contains element 5's L21 and "Derived from"; page 3 empty. So the checklist heading and element 1 are on page 1, not page 2. Tier, scope and capture key of S225 otherwise match the bytes.

**F8 — Never cells that the warranting quotes do not say (C2 K2 fired).** Quotes checked against `corpus/captures/347c55…txt` lines 32–82 and `80a844…txt` lines 516–637 (the warrant quotes are located at those lines; the Do cells match them).
- Row "Checking that a strategy answers the question": Never "review the syntax of a strategy without first reading the question it is meant to answer" — no warrant quote (L3–L7) says this. Overreach (inferred prohibition).
- Row "Judging how much a search retrieves": Never "file only a final total, which hides the line that over- or under-retrieves" — L6 asks for hits per line; it does not mention a "final total" or say a total "hides" anything. Overreach (added rationale; the Do cell is faithful).
- Row "Checking free-text words": Never "assume one spelling or one word ending covers a concept" — L15 asks about spelling variants and L16 about truncation placement; no quote says "assume one ... covers". Overreach (mild).
- Row "Citing the checklist": Never "cite a reprint's wording as the guideline's own where reprints differ" — warrants L1, L2, L26, L27, L28 do not speak to differing reprints. The point rests on the `## Two reprints compared` paragraph and the named limits, not on the row's warrant. Overreach by warrant (the row's Never is defensible from the entry's own limits, not from its quotes).
- Faithful with a paraphrase gloss (not flagged as overreach): row "Boolean and proximity" Never "add a NOT without checking what it excludes" (paraphrase of L10); row "Subject headings" Never "rely on subject headings alone for a concept" (paraphrase of L13); row "Spelling, syntax" Never "leave a line that the final combination never refers to" (paraphrase of L21); row "Limits and filters" Never "apply a filter without citing where it comes from" (paraphrase of L25).

## Per-row verdicts

1. Translation of the research question — Do: **faithful** (L4, L5, L7). Never: **overreach** ("review the syntax … without first reading the question"; no quote). Lane: "SKILL.md question framing" is real (`R97ReviewerC2-lane-claims.txt`, SKILL.md:17); the "reviewer seat is handed the framed question" process claim is **[INFERENCE]**, not checked.
2. Hits per line — Do: **faithful** (L6). Never: **overreach** ("file only a final total, which hides …"). Lane: **fired** (F4) — `hits` is a file count, not hits per line.
3. Boolean and proximity — Do: **faithful** (L8, L9, L10). Never: faithful with paraphrase gloss. Lane: "single GNU grep expressions with no NOT" — true of Q1–Q7 (none contains NOT; `R97ReviewerC2-searches-and-tool.txt`).
4. Subject headings — Do: **faithful** (L11, L12, L13 / S226 L29). Never: faithful with paraphrase gloss. Lane: **fired** (F5) — "no controlled vocabulary" contradicted by 12 captures; "a record says so" has no record behind it.
5. Free-text words — Do: **faithful** (L14–L17). Never: **overreach, mild** ("assume one … word ending covers a concept"). Lane: "`[Ss]ubject headings?` … Q5" is accurate (`regex` row, tool accepts it).
6. Spelling, syntax, line numbers — Do: **faithful** (L18–L22). Never: faithful with paraphrase gloss. Lane: tool refuses POSIX bracket classes in `regex` rows (`tools/search-rerun.py:184-185`, `POSIX_CLASS_RE`) — **held**. "its records have no combined lines, so orphan lines cannot occur" is a by-construction statement about the record form, not checked further.
7. Limits and filters — Do: **faithful** (L23, L24, L25). Never: faithful with paraphrase gloss. Lane: PRISMA-S items 9–10 are in the round-95 entry (not reopened here); "only limit is its `where` glob" **[INFERENCE]**.
8. Citing the checklist — Do: **faithful** (L26 supports "cite the guideline statement the checklist is derived from"; L1, L2 are a pointer and a title, so they support the route only weakly). Never: **overreach by warrant** (F8). Lane: **fired** — "12 of the 26 … not found verbatim" should be 16 (F1); the same cell's "12 not found" is the letters count and is not what the cell says.

Misattributed: **none**. All 29 located quotes are substrings of a line of their own source capture (`R97ReviewerC2-recount.txt`). L27–L29 are S226 text (L27 line 503, L28 line 503, L29 line 576 of `80a844…txt`).

## SOURCES.md rows S225–S227

- **S225 (B)**: tier and scope match the bytes ("derived from" citation at capture lines 81–83; the scope excludes the guideline's own text). Page anchor wrong in part (F7).
- **S226 (C)**: tier C and "never sole support" hold for every row I checked (each row with an S226 quote also carries S225 quotes). "Independent reprint" is not checked by me: the capture names McGowan 2016 and CADTH E&E but I did not establish independence; **[INFERENCE]**. Scope "six element sections and the reference to McGowan et al. 2016" matches the capture (lines 516–634).
- **S227 (A, rejected)**: rejected-for-route, `curl rc 22, HTTP 403` consistent with `GATE-RECORD S227 … curl_rc=22 http=403` in the entry. No quote is taught from it; nothing in the rows cites it. Held.

## Residual risk / verification gaps

- The Q1–Q7 recount was run at F, not at base `c8087ac5`; the difference to the entry's base counts is exactly the two new captures (receipt `R97ReviewerC2-searches-and-tool.txt`). The base re-run is the tool's job (`search-rerun.py verify`), not run by me.
- I did not run `gate-records.py`, `search-rerun.py verify`, `entry-controls-r97.py` or the battery; those belong to the main agent's verification pass.
- The row warrants are the lane's paraphrase; my fidelity check is against the quotes and captures as instructed, not against the guideline statement (not held).

VERDICT: R97ReviewerC2 C1 n/a — not in scope for this seat; the self-test is not touched by the entry-fidelity review.
VERDICT: R97ReviewerC2 C2 fired — the stated corroboration count "12 of 26 not verbatim" should be 16 (verbatim 10/26), the "Two reprints" breakdown misnames 6 headings and 4 questions for the 12 letters-misses, the row-2 Lane cell claims `hits` is hits-per-line when the tool counts files, the row-4 Lane cell's "no controlled vocabulary" is contradicted by 12 captures, and Never cells in rows 1, 2, 5 and 8 assert prohibitions their quotes do not state.
