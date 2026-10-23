# ReviewFixtureVerbatimA — fixture ground-truth attack, VERBATIM items of S002/S003/S008/S013 (round 29, wave 1)

Scope: from `corpus/fixtures/quote-reopen-r29/items.tsv` joined with `labels.tsv`, the VERBATIM items
whose `source_id` is S002, S003, S008 or S013 — 7 of the 14 committed VERBATIM items
(selection copy: `.ufo/waves/round-29/build/ReviewFixtureVerbatimA/sel.tsv`).
Fixture, counter and claims.md untouched (frozen).

## Method

1. Opened each registry row's live page with the `read` tool (native reader):
   S002 `https://ifcncodeofprinciples.poynter.org/the-commitments`,
   S003 `https://hapgood.us/2019/06/19/sift-the-four-moves/`,
   S008 `https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-02`,
   S013 `https://jsonlines.org/`.
2. Crawled the same 4 URLs once each, GET only, bound 60 to 120 s
   (`curl -sS -L --max-time N -A 'chousa-quote-reopen-review' -o <file> <url>`), exit 0.
   `curl -w` check: all four returned `200`, `text/html`; sizes 4510 B (jsonlines),
   150128 B (cochrane), 19482 B (ifcn), 1171355 B (hapgood) — all far under the 8 MiB bound,
   so a contract-following tool reaches the VERBATIM/ABSENT stage on these pages, not UNREACHABLE.
3. Checked contiguity by reading, then re-verified with a scratch checker
   (`/fast/scratch/hyaku/chousa-r29/w1/ReviewFixtureVerbatimA/`) that re-implements the frozen
   normalization from claims.md: html.parser, script/style/noscript/template/head dropped,
   fixed block list emitting one space, NFKC, curly quotes to straight, zero-width deleted,
   whitespace collapsed, case-sensitive alnum-boundary match. Cross-checked against the frozen
   counter's reference functions: `corpus/evidence/round29/c1-count.py` lines 63 to 112 use the
   same block list, same quote/zero-width map, same normalization order and the same boundary rule
   (`(i == 0 or not text[i-1].isalnum()) and (j == len(text) or not text[j].isalnum())`).

## Verdicts — 7 of 7 LABEL-OK, none LABEL-WRONG

| id | src | class | page quote found (access date 2026-10-23) | words | occurrences | boundary |
|---|---|---|---|---:|---:|---|
| 27c5599c | S013 | verbatim-inline-markup | "Like the JSON standard a byte order mark (U+FEFF) must NOT be included." — https://jsonlines.org/ | 13 | 1 | space both sides |
| ca473d99 | S013 | verbatim-inline-markup | "JSON Lines files may be saved with the file extension .jsonl." — https://jsonlines.org/ | 11 | 1 | space both sides |
| f81a9ce8 | S008 | verbatim-plain | "This is best done by clearly framing the questions the review seeks to answer." — cochrane.org chapter-02, section 2.1 | 14 | 1 | space both sides |
| bcc95dda | S008 | verbatim-inline-markup | "A novel review will address a genuine gap in knowledge, so review authors should be aware of any related or overlapping reviews." — cochrane.org chapter-02 | 22 | 1 | space both sides |
| 3b00b111 | S008 | verbatim-inline-markup | "These state that questions should be Feasible, Interesting, Novel, Ethical, and Relevant (Cummings et al 2007)." — cochrane.org chapter-02 | 16 | 1 | space both sides |
| b948e65f | S002 | verbatim-plain | "Signatories want their readers to be able to verify findings themselves." — ifcncodeofprinciples.poynter.org/the-commitments, Principle #2 | 11 | 1 | space both sides |
| c258f7c8 | S003 | verbatim-typographic-apostrophe | "Since 2017, we've been teaching students with something called the Four Moves." — hapgood.us SIFT post | 12 | 1 | space both sides |

Raw-HTML confirmation for the inline-markup class (why the quote stays contiguous once tags emit nothing):

- jsonlines.html lines 59 to 60: `Like the JSON standard <a href="...rfc8259#section-8.1">` /
  `a byte order mark (U+FEFF) must NOT be included</a>.` — inline anchor, href is attribute-only text.
- jsonlines.html line 92: `file extension <code>.jsonl</code>.` — inline code element.
- cochrane-ch02.html line 420: `These state that questions should be <strong>F</strong>easible,
  <strong>I</strong>nteresting, <strong>N</strong>ovel, <strong>E</strong>thical, and
  <strong>R</strong>elevant (Cummings et al 2007).` — inline strong initials; the bcc95dda sentence
  carries `<em>novel</em>` the same way (reader text shows `A *novel* review`).
- hapgood.html line 543: `Since 2017, we&#8217;ve been teaching students with something called the Four Moves.` —
  the character reference decodes to U+2019, which the frozen map turns into the straight apostrophe
  the fixture stores. This is exactly the verbatim-typographic-apostrophe construction.

All 7 quotes are at most 22 words, so none trips the TOO_LONG stage. Each page text contains exactly
one occurrence and each has a non-alnum character (a space) on both sides, so every one returns
VERBATIM under the frozen match rule on these page states.

## Fixture-integrity probes run on the way

- Byte-level duplicate scan over all 40 items keyed on (source_id, quote): no group carries more
  than one label — the fixture has no contradictory pair. Suspicion checked and resolved:
  13fe59fb stores byte-identical quote text to 27c5599c (the S013 BOM sentence) but its
  `source_id` is S020, not S013 (rendered TSV is visually ambiguous; `repr` settled it).
  13fe59fb is an ABSENT cross-attribution against S020, outside my source set, so I did not
  verify that absence on the PROV-O page — flagged for whoever holds S020.
- The only fixture `source_id` outside the 45 registry rows is S999 on d3909bba, which is the
  designed no-source-unregistered-id case. All other source ids resolve to real rows.

## Verdict

No miss found in this slice: all 7 in-scope VERBATIM labels match the live pages under the frozen
normalization, so these items cannot by themselves push QUOTE_REOPEN_MATCH below 130/130. The fixture
was not edited and no change is proposed.

## Limits and notes

- Single fetch per page during this review; pages can change later — the claim explicitly excludes
  later page drift, so this is not a defect.
- My checker is an independent re-implementation of the claims.md contract, validated by reading
  `c1-count.py`'s reference functions (same semantics), not by running the counter.
- Fetch wall clock on the seat read 2026-10-22 22:26 local; the round labels this access as
  2026-10-23 per assignment.
- No tool installs (nothing needed beyond curl and Python 3). No subagents, no background jobs.
  No LSP server applies: the reviewed surface is fixture data and fetched page text, not code.
  Scratch files live only in `/fast/scratch/hyaku/chousa-r29/w1/ReviewFixtureVerbatimA/`;
  the only lane writes are this report and `sel.tsv` inside my build directory.
