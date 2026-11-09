# PRESS 2015 checklist questions — what a peer reviewer of a search strategy asks, element by element, as two reproductions print them (round 97)

source: S225, S226
verified-at: 2026-11-09 (round 97; capture `347c55ba9be9d63afe17986e` — Cochrane's two-page search checklist for editors, which reprints the PRESS 2015 Guideline Evidence-Based Checklist and names the guideline statement it derives from, opened as S225 — and capture `80a844fe287a1a26d4280251`, Karolinska Institutet University Library's page reprinting the same checklist, opened as S226)
recheck: on-release

## What this entry governs

The round-96 entry (`search-peer-review-dedup-r96.md`) holds that PRISMA-S asks a report to describe any search
peer review, and holds the PRESS 2015 update's six elements by name only, through its authors' abstract (S223,
tier B); its first named limit says "the checklist's own element wording ... [is] not held". This entry holds 16 of the
checklist's *questions* (of the 33 question lines S225 prints), at least two under each of the six elements, as
Cochrane reprints them for editors (S225, tier B), read against a second reprint on another host (S226, tier C; every
decision row also names an S225 quote). S225 says it is "Derived from" the guideline statement (J Clin Epidemiol
2016); S226 links CADTH's 2016 PRESS report as its source, so the two are separate transcriptions, not shown to be
independent of one upstream. The guideline statement and the CADTH Table 9 answered http 403 (S227, rejected for
route; also the round-96 attempts), so where the two reprints differ, this entry cannot say which wording is the
guideline's.

What the lane held before this round, measured by the `## Searches` record below at the base revision `c8087ac5`:
no capture holds the question "Are there any spelling errors" (Q3), the phrase "orphan lines" (Q1) or "hits per
line" (Q2); "truncation", "subject heading(s)" and "proximity operator(s)" occur in three, four and three
captures (Q4-Q6), none of them a reprint of the checklist; "PICO" occurs in twelve (Q7). The column marked *lane*
is this lane's reading; it is not what PRESS, Cochrane or Karolinska says.

Text forms: S225 is `pdftotext -layout` of a two-page landscape PDF whose question column is one line per question,
so every S225 quote is a substring of one capture line (L21 and L22 are the two halves of one 30-word question on
capture line 73 as `sed -n 73p` counts lines, split to stay within 25 words; Python's `splitlines()` also breaks at
the form feeds between pages and counts that line as 74). S226 is the recipe's HTML text form, one question per line.

## Located quotes

| qid | source | quote |
|---|---|---|
| L1 | S225 | "See PRESS checklist below" |
| L2 | S225 | "PRESS 2015 Guideline Evidence-Based Checklist" |
| L3 | S225 | "1. Translation of the research question" |
| L4 | S225 | "Does the search strategy match the research question/PICO?" |
| L5 | S225 | "Are there too many or too few PICO elements included?" |
| L6 | S225 | "Does the search retrieve too many or too few records? (Please show number of hits per line.)" |
| L7 | S225 | "Are unconventional or complex strategies explained?" |
| L8 | S225 | "2. Boolean and proximity operators (these vary based on search service)" |
| L9 | S225 | "Are Boolean or proximity operators used correctly?" |
| L10 | S225 | "If NOT is used, is this likely to result in any unintended exclusions?" |
| L11 | S225 | "3. Subject headings (database specific)" |
| L12 | S225 | "Are any relevant subject headings missing; for example, previous index terms?" |
| L13 | S225 | "Are both subject headings and terms in free text (see the following) used for each concept?" |
| L14 | S225 | "4. Text word searching (free text)" |
| L15 | S225 | "Does the search include all spelling variants in free text (eg, UK vs. US spelling)?" |
| L16 | S225 | "Does the search capture relevant truncation (ie, is truncation at the correct place)?" |
| L17 | S225 | "Should any long strings be broken into several shorter search statements?" |
| L18 | S225 | "5. Spelling, syntax, and line numbers" |
| L19 | S225 | "Are there any spelling errors?" |
| L20 | S225 | "Are there any errors in system syntax; for example, the use of a truncation symbol from a different search interface?" |
| L21 | S225 | "Are there incorrect line combinations or orphan lines (ie, lines that are not referred to in the final summation" |
| L22 | S225 | "that could indicate an error in an AND or OR statement)?" |
| L23 | S225 | "6. Limits and filters" |
| L24 | S225 | "Are all limits and filters used appropriately and are they relevant given the research question?" |
| L25 | S225 | "Are sources cited for the filters used?" |
| L26 | S225 | "PRESS Peer Review of Electronic Search Strategies: 2015 Guideline Statement. J Clin Epidemiol." |
| L27 | S226 | "This is the complete and updated PRESS checklist" |
| L28 | S226 | "a structured tool for peer review of electronic literature search strategies." |
| L29 | S226 | "Are both subject headings and terms in free text (see below) used for each concept?" |

## Decision table

| Situation | Do | Never | Warrant | Lane |
|---|---|---|---|---|
| Checking that a strategy answers the question it serves | check that the search strategy matches the research question/PICO, that it has neither too many nor too few PICO elements, and that unconventional or complex strategies are explained | leave an unconventional or complex strategy unexplained | L3, L4, L5, L7 (S225) | chousa frames the question before it searches (SKILL.md question framing); a reviewer seat is handed the framed question with the record, not the record alone |
| Judging how much a search retrieves | show the number of hits per line, so the reviewer can ask whether the search retrieves too many or too few records | leave out the number of hits per line | L6 (S225) | the lane's `## Searches` record files one count per expression (`hits`), but that count is the number of *files* with at least one matching line (`tools/search-rerun.py` re-derives it as a file count), not hits per line; the lane does not yet meet this question, it only keeps each expression in its own row |
| Checking Boolean and proximity operators | check that Boolean or proximity operators are used correctly (they vary by search service) and whether a NOT causes unintended exclusions | add a NOT without checking what it excludes | L8, L9, L10 (S225) | the lane's local searches are single GNU grep expressions with no NOT; an exclusion would be a second expression, filed as its own row, so its effect is countable |
| Checking subject headings | check that relevant subject headings are not missing (for example previous index terms) and that both subject headings and free-text terms are used for each concept | rely on subject headings alone for a concept | L11, L12, L13 (S225); L29 (S226) | the capture store holds text *about* controlled vocabularies (`git grep -l -i -E 'emtree|mesh|thesaurus'` finds 12 captures at the freeze), but the lane's local searches are GNU grep expressions over plain text with no subject-heading index, so this element does not apply to them; no lane record yet says so, which is a gap, not a pass |
| Checking free-text words | check spelling variants (UK vs. US), that truncation is at the correct place, and whether long strings should be broken into several shorter search statements | leave out spelling variants, or place truncation where it misses relevant endings | L14, L15, L16, L17 (S225) | a `regex` row can carry variants (`[Ss]ubject headings?`, Q5 below); a `fixed` row matches one spelling only, so a variant needs its own row |
| Checking spelling, syntax and line numbers | check for spelling errors, for syntax from a different search interface (such as another interface's truncation symbol), and for incorrect line combinations or orphan lines | leave a line that the final combination never refers to | L18, L19, L20, L21, L22 (S225) | `tools/search-rerun.py` refuses a POSIX bracket class in a `regex` row because Python reads that syntax differently from the PCRE that recorded it — the lane's case of another interface's syntax; its records have no combined lines, so orphan lines cannot occur in them |
| Checking limits and filters | check that limits and filters are appropriate and relevant to the research question, and that sources are cited for the filters used | apply a filter without citing where it comes from | L23, L24, L25 (S225) | PRISMA-S items 9 and 10 (round-95 entry, S222) ask the same of a report; a chousa record's only limit is its `where` glob, filed in the row |
| Citing the checklist | cite the guideline statement that the reprint says the checklist is derived from, and name the reprint as the route the wording was read through | (none stated by the sources; the lane's guard is in the Lane column) | L1, L2, L26 (S225); L27, L28 (S226) | the lane holds two reprints, not the guideline (S227 and the round-96 routes answered 403); 16 of the 26 S225 quotes are not found verbatim in S226 and 12 not even after deleting non-alphanumerics (`## Two reprints compared`), so the lane never cites a reprint's wording as the guideline's |

## Two reprints compared

Each S225 quote was looked up in the S226 capture under two readings, by `corpus/evidence/round97/entry-controls-r97.py`
(group CORROBORATION): *verbatim* — the quote, whitespace-collapsed as `tools/gate-records.py` normalizes it, is a
substring of the whitespace-collapsed S226 text; *letters* — after lowercasing and deleting every character that is
not a letter or digit from both. At round 97: verbatim 10/26, letters 14/26 — so 16 are not found verbatim and 12
not under *letters*. Of those 12, six are element headings (L3, L8, L11, L14, L18, L23: S225 numbers them, S226 does
not — with digits also deleted, 20/26 are found, so the headings differ only by their numbers), one is S225's own
pointer (L1), one the PRESS checklist title (L2), and four are questions whose wording differs: S225 "for example"
where S226 has "e.g." (L12, L20), S225 "eg," for S226 "e.g.," and "vs." for "versus" (L15), and S225 "see the
following" for S226 "see below" (L13 against L29). Four more (L4, L16, L21, L26) are found under *letters* but not
verbatim: spacing and abbreviation points ("question/ PICO ?", "i.e.," for "ie,", "Statement ." with a space and
"2016 Jul;75:40–46."). Which wording is the guideline statement's is not decidable from these two bytes; the
guideline is not held.

## As run

Every search in `## Searches` ran on 2026-11-09 against the lane's committed capture store at revision `c8087ac529003e667505bcc624f9a7bde0cffbce`
(the round-96 landing, round 97's base), materialised read-only with
`git archive c8087ac529003e667505bcc624f9a7bde0cffbce corpus/captures | tar -x -C <scratch>` and searched from `<scratch>` with GNU grep 3.12
(`/usr/bin/grep`):

    /usr/bin/grep -l -F -e '<expression>' corpus/captures/*.txt | LC_ALL=C sort        # engine fixed
    /usr/bin/grep -l -P -e '<expression>' corpus/captures/*.txt | LC_ALL=C sort        # engine regex

`python3 -B tools/search-rerun.py verify corpus/knowledge/press-checklist-questions-r97.md --root .` re-runs each
one at `c8087ac5` and over the current tree.

## Searches

| id | engine | where | expression | rev | searched | hits | hit_set |
|---|---|---|---|---|---|---|---|
| Q1 | fixed | corpus/captures/*.txt | `orphan lines` | c8087ac529003e667505bcc624f9a7bde0cffbce | 2026-11-09 | 0 | - |
| Q2 | fixed | corpus/captures/*.txt | `hits per line` | c8087ac529003e667505bcc624f9a7bde0cffbce | 2026-11-09 | 0 | - |
| Q3 | fixed | corpus/captures/*.txt | `Are there any spelling errors` | c8087ac529003e667505bcc624f9a7bde0cffbce | 2026-11-09 | 0 | - |
| Q4 | fixed | corpus/captures/*.txt | `truncation` | c8087ac529003e667505bcc624f9a7bde0cffbce | 2026-11-09 | 3 | corpus/captures/1a8c36c4c24444967bd9c3ce.txt, corpus/captures/c52a1f15884a78028febcf43.txt, corpus/captures/c9d1e74c3ac8d9eb332c9770.txt |
| Q5 | regex | corpus/captures/*.txt | `[Ss]ubject headings?` | c8087ac529003e667505bcc624f9a7bde0cffbce | 2026-11-09 | 4 | corpus/captures/1a8c36c4c24444967bd9c3ce.txt, corpus/captures/371c55117727d526805f030d.txt, corpus/captures/c52a1f15884a78028febcf43.txt, corpus/captures/c9d1e74c3ac8d9eb332c9770.txt |
| Q6 | regex | corpus/captures/*.txt | `proximity operators?` | c8087ac529003e667505bcc624f9a7bde0cffbce | 2026-11-09 | 3 | corpus/captures/c52a1f15884a78028febcf43.txt, corpus/captures/c9d1e74c3ac8d9eb332c9770.txt, corpus/captures/e94691f583d644da14661ec1.txt |
| Q7 | fixed | corpus/captures/*.txt | `PICO` | c8087ac529003e667505bcc624f9a7bde0cffbce | 2026-11-09 | 12 | sha256:6ea7657c5cb1cb200c6d6a83932c796ae60f8b1f67399d0ac613ae3c6c35c849 |

## Named limits

- The checklist is held through two reprints, not through the guideline statement (J Clin Epidemiol
  2016;75:40-46) or the CADTH E&E and its Table 9, all of which answered http 403 to this host (S227 and the
  round-96 attempts); `web.archive.org` did not accept a TCP connection from this host on 2026-11-09. Where the
  reprints differ, neither is taken as the guideline's wording.
- S225 is tier B for the scope "the checklist questions as Cochrane reprints them for editors"; it says it is
  "derived from" the guideline statement, which is a citation, not a statement that the text is verbatim.
- S226 is tier C: a university library's guide page; it corroborates, and every decision row also names an S225
  quote (the controls check that an S225 quote is named, not that it carries the row's point). S226 links CADTH's
  2016 report as its source, so its agreement with S225 is two transcriptions agreeing, not two independent witnesses.
- `## Two reprints compared` is a string test: *letters* can match across a line break in S226 and cannot see a
  reordering; its numbers depend on keeping digits (14/26 with digits, 20/26 without).
- The checklist's assessment form, the E&E's explanation of each element and the evidence behind each element are
  not held.
- The searches are over the lane's own capture store, per line; Q1-Q3's zero counts say the store held no line
  with those strings at the base, not that no earlier round read the checklist elsewhere.
- The *lane* column's statements about `tools/search-rerun.py` describe the tool at this round's revision.

## Gate records

GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=4 quote="See PRESS checklist below"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=5 quote="PRESS 2015 Guideline Evidence-Based Checklist"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=6 quote="1. Translation of the research question"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=8 quote="Does the search strategy match the research question/PICO?"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=10 quote="Are there too many or too few PICO elements included?"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=17 quote="Does the search retrieve too many or too few records? (Please show number of hits per line.)"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=6 quote="Are unconventional or complex strategies explained?"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=11 quote="2. Boolean and proximity operators (these vary based on search service)"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=7 quote="Are Boolean or proximity operators used correctly?"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=13 quote="If NOT is used, is this likely to result in any unintended exclusions?"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=5 quote="3. Subject headings (database specific)"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=11 quote="Are any relevant subject headings missing; for example, previous index terms?"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=16 quote="Are both subject headings and terms in free text (see the following) used for each concept?"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=6 quote="4. Text word searching (free text)"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=15 quote="Does the search include all spelling variants in free text (eg, UK vs. US spelling)?"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=13 quote="Does the search capture relevant truncation (ie, is truncation at the correct place)?"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=11 quote="Should any long strings be broken into several shorter search statements?"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=6 quote="5. Spelling, syntax, and line numbers"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=5 quote="Are there any spelling errors?"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=20 quote="Are there any errors in system syntax; for example, the use of a truncation symbol from a different search interface?"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=19 quote="Are there incorrect line combinations or orphan lines (ie, lines that are not referred to in the final summation"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=11 quote="that could indicate an error in an AND or OR statement)?"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=4 quote="6. Limits and filters"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=15 quote="Are all limits and filters used appropriately and are they relevant given the research question?"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=7 quote="Are sources cited for the filters used?"
GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=13 quote="PRESS Peer Review of Electronic Search Strategies: 2015 Guideline Statement. J Clin Epidemiol."
GATE-RECORD S226 url=https://kib.ki.se/en/search-evaluate/systematic-reviews/press-2015-checklist-search-strategies fetched=2026-11-09T01:59:45Z tier=C decision=admit capture=corpus/captures/80a844fe287a1a26d4280251.txt capture_sha256=161144983ec5b3b882afca0bbf83a1e1662ab95c85fc8e869d5441325b0c8ee4 words=8 quote="This is the complete and updated PRESS checklist"
GATE-RECORD S226 url=https://kib.ki.se/en/search-evaluate/systematic-reviews/press-2015-checklist-search-strategies fetched=2026-11-09T01:59:45Z tier=C decision=admit capture=corpus/captures/80a844fe287a1a26d4280251.txt capture_sha256=161144983ec5b3b882afca0bbf83a1e1662ab95c85fc8e869d5441325b0c8ee4 words=11 quote="a structured tool for peer review of electronic literature search strategies."
GATE-RECORD S226 url=https://kib.ki.se/en/search-evaluate/systematic-reviews/press-2015-checklist-search-strategies fetched=2026-11-09T01:59:45Z tier=C decision=admit capture=corpus/captures/80a844fe287a1a26d4280251.txt capture_sha256=161144983ec5b3b882afca0bbf83a1e1662ab95c85fc8e869d5441325b0c8ee4 words=15 quote="Are both subject headings and terms in free text (see below) used for each concept?"
GATE-RECORD S227 url=https://www.cda-amc.ca/sites/default/files/PRESS_Peer_Review_Electronic_Search_Strate/Table_9-PRESS.pdf fetched=2026-11-09T01:59:45Z tier=A decision=reject capture=none curl_rc=22 http=403 words=0 quote=none
