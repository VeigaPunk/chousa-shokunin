# HeldOut03 — held-out generalization attack on C1 (blind then tool), items h07–h09

## What I attacked

Whether `tools/quote-reopen.py verify` generalizes beyond the frozen fixture to
located quotes the lane cited in earlier Gate sections (origin
`lessons/round-24.md:55-57`), which were never part of the fixture or
counter. Items h07 (S008), h08 (S009), h09 (S010) from
`.ufo/waves/round-29/build/ScoutGateQuotes/held-out.tsv`.

## STEP 1 — blind verdicts (before running the tool)

Registry URLs resolved from `corpus/SOURCES.md` rows 18–20; each opened once
with the `read` tool on 2026-10-22.

- **h07 / S008** — `https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-02`
  (text/html, 200). Page text seen, section 2.1: *"As with any research, the
  first and most important decision in preparing a systematic review is to
  determine its focus. This is best done by clearly framing the questions…"*
  The quote is a contiguous sub-span; preceding char is a space (after
  "research,"), following char is "." → both non-alphanumeric. Word count 15
  ≤ 25. **Blind: VERBATIM.**
- **h08 / S009** — `https://www.cochrane.org/authors/handbooks-and-manuals/mecir-manual/standards-conduct-new-cochrane-intervention-reviews-c1-c75/performing-review-c24-c75/assessing-risk-bias-included-studies-c52-c60`
  (text/html, 200). Page text seen, standard C53 table row: *"Use (at least)
  two people working independently to apply the risk-of-bias tool to each
  included study, and define in advance the process for resolving
  disagreements."* The quote is a prefix of that sentence cut at "tool"
  followed by " to" (space) → boundary clean; "Use" sits at the start of the
  td text → preceding char is the block-emitted space. Word count 12.
  **Blind: VERBATIM.**
- **h09 / S010** — `https://aclanthology.org/2025.acl-long.1574/` (text/html,
  200). Page text seen, Abstract paragraph: *"Current evaluation frameworks,
  both human and automatic, mainly rely on Natural Language Inference (NLI)
  to assess binary or ternary supportiveness from cited sources, which we
  argue is a suboptimal proxy for citation evaluation."* The quote is an
  interior sub-span starting at "mainly" (preceded by space) and ending at
  "proxy" (followed by " for", space). Word count 22 ≤ 25. The same sentence
  also appears inside the page's BibTeX/MODS/EndNote export blocks — multiple
  valid occurrences do not change the verdict. **Blind: VERBATIM.**

None of the three pages is a PDF, a challenge page, or non-2xx, so no
UNREACHABLE candidates in this slice.

## STEP 2 — tool run

`items.tsv` (header `id<TAB>source_id<TAB>quote`) written to
`.ufo/waves/round-29/falsify/HeldOut03/items.tsv`. From the lane root:

```
$ timeout 300 python3 tools/quote-reopen.py verify --items .ufo/waves/round-29/falsify/HeldOut03/items.tsv
QUOTE_REOPEN	h07	VERBATIM	matched in normalized page text
QUOTE_REOPEN	h08	VERBATIM	matched in normalized page text
QUOTE_REOPEN	h09	VERBATIM	matched in normalized page text
QUOTE_REOPEN_SUMMARY verbatim=3 absent=0 too_long=0 no_source=0 unreachable=0
EXIT=0   (2.18 s)
```

## Comparison

| item | blind | tool | result |
|---|---|---|---|
| h07 | VERBATIM | VERBATIM | AGREE |
| h08 | VERBATIM | VERBATIM | AGREE |
| h09 | VERBATIM | VERBATIM | AGREE |

No DISAGREE. No held-out quote came back ABSENT, so there is no
inexact-citation freshness finding in this slice: all 3 located quotes cited
at `lessons/round-24.md:55-57` reproduce verbatim from the live registry
URLs today. Note h08 and h09 are mid-sentence sub-spans the lane cut at word
boundaries; both still land on non-alphanumeric boundaries, so they are
verbatim-true under the frozen contract rather than citation defects.

## Verdict

**HOLDS** for this slice — the tool reproduced the contract-derived verdict on
all 3 held-out items (3/3 agreement, exit 0).

## Limits

- Only 3 items, all true VERBATIM: no held-out coverage of ABSENT, TOO_LONG,
  NO_SOURCE or UNREACHABLE paths.
- Blind verdicts were made on `read`-tool renderings; the tool fetches and
  extracts per its own contract implementation, which is exactly what the
  comparison checks.
- Reported as evidence, not a re-measurement of the frozen 130/130 predicate.

## Tooling installs

None. No pacman/uv/npm transactions were run; the system python3 and the
lane tool sufficed.
