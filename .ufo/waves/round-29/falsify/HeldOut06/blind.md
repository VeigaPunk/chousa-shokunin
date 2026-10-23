# HeldOut06 — STEP 1 blind verdicts (recorded before running the tool)

Contract applied (frozen claims.md): normalize NFKC, curly quotes to straight,
soft/zero-width marks deleted, whitespace runs collapse to one space, ends
stripped; match = case-sensitive substring at non-alphanumeric boundary;
TOO_LONG if > 25 normalized words; UNREACHABLE if fetch/non-2xx/bad-type/over-8MiB.
Sources opened via the `read` tool (one GET per registry URL) on 2026-10-22,
before ever running tools/quote-reopen.py.

## h16 — S017 — https://www.prisma-statement.org/prisma-2020

Quote: `an expanded checklist that details reporting recommendations for each item/sub-item`
(10 words). Page text seen (first paragraph):

> PRISMA 2020 consists of a statement paper, which includes a description of how
> the reporting guideline was developed and presents a checklist of items and
> sub-items, an expanded checklist that details reporting recommendations for
> each item/sub-item, an abstract checklist, and template flow diagrams ...

The quote appears verbatim inside that sentence; "each item/sub-item" is followed
by a comma in the page. Before the span: space after "an ". After the span: ","
(comma, non-alnum). Boundary rule satisfied.

Blind verdict: **VERBATIM** (page reachable, text/html, quote present verbatim).
Caveat noted: raw HTML may place the phrase inside an `<a>` element; `<a>` is not
in the frozen block list so it emits no spaces — the phrase stays inline under
the contract either way.

## h17 — S018 — https://aclanthology.org/2026.acl-long.1430/

Quote: `we systematically analyze 134 papers, introduce a unified taxonomy`
(9 words). Page text seen (Abstract):

> To bridge this gap, we systematically analyze 134 papers, introduce a unified
> taxonomy of evidence-based text generation with LLMs, and investigate 300
> evaluation metrics across seven key dimensions.

The quote is a verbatim sub-span of that sentence. Before the span: space after
"gap, ". After the span: " of" (space, non-alnum). Boundary satisfied. The same
abstract string also appears inside the BibTeX/MODS export blocks on the page,
so at least two occurrences exist.

Blind verdict: **VERBATIM** (page reachable, text/html, abstract rendered
server-side, quote present verbatim).

## h18 — S019 — https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-iv

Quote: `All Cochrane reviews should be assessed periodically to determine whether an update is needed.`
(14 words). Page text seen, two relevant passages:

Key Points bullet (DIFFERENT wording — no leading "All"):
> - Cochrane reviews should be assessed periodically to determine whether an
>   update is needed. The decision to update should be based on ...

Section IV.1 Introduction, first sentence of the second paragraph:
> All Cochrane reviews should be assessed periodically to determine whether an
> update is needed. Some areas of research evolve rapidly, whereas others are
> more stable, ...

The quote matches the IV.1 sentence exactly, including the final period; it does
NOT match the Key Points bullet (that bullet omits "All"). Before the span:
start of paragraph text (preceding char is whitespace or nothing — non-alnum).
After the span: space before "Some". Boundary satisfied.

Freshness note (about the lane's own citations): lessons/round-25.md:68 records
the located quote for S019 as `Key Points: "All Cochrane reviews should be
assessed periodically ..."` attributing the "All ..." wording to the Key Points
section. The live page's Key Points bullet reads without "All"; the quoted
sentence lives in IV.1. So the quote text is still VERBATIM-locatable on the
page, but the lane's recorded location ("Key Points:") is inexact — a small
freshness/attribution finding about the lane's citation, not about the tool.

Blind verdict: **VERBATIM** (page reachable, text/html, sentence present
verbatim in IV.1).

## Summary of blind verdicts

| id | source_id | blind verdict |
|---|---|---|
| h16 | S017 | VERBATIM |
| h17 | S018 | VERBATIM |
| h18 | S019 | VERBATIM |
