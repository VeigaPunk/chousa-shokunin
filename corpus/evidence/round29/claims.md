# Round 29 — frozen claim, predicate, tool contract and controls

Frozen on 2026-10-23 before any data seat ran, at lane base
`6c5eb1466f2b8abbd3de576389037f435016d07b`. This file, `c1-count.py` and the
fixture `corpus/fixtures/quote-reopen-r29/` land together in one commit before
the control wave. Nothing in them changes after that commit. A miss under this
predicate is reported as a miss.

## Claim C1 — operability (capability acquisition)

**Axis by surface:** operability. The surface is a new runnable command,
`tools/quote-reopen.py`. It re-opens located quotes against the live source
that the lane's own `corpus/SOURCES.md` registry names and returns one verdict
per quote. The lane has no such command at the base: `tools/` holds only
`research-gate.sh`, and that gate refuses any source outside the lane corpus.
Operability is the lowest scored axis (SCORECARD.md line 7, score 3). The claim
does not touch `tools/research-gate.sh`. It is a different surface from the
path-denylist and ancestor work of rounds 26 to 28.

**Predicate (one sentence, frozen):** C1 holds iff
`python3 corpus/evidence/round29/c1-count.py -- python3 tools/quote-reopen.py verify`,
run from the lane root, prints `QUOTE_REOPEN_MATCH=82/82`: every one of the 40
frozen fixture items and the 42 run-time variants gets a verdict equal to its
label.

- Counter code: `n == t == FROZEN_TOTAL` with `FROZEN_TOTAL = 82` in `c1-count.py`.
- Receipt label: `QUOTE_REOPEN_MATCH` and the receipt field `predicate_holds`.
- Before (base `6c5eb146`, tool absent): `QUOTE_REOPEN_MATCH=0/82`, exit 1.
  Receipt: `.ufo/waves/round-29/controls/before-do-nothing.json` (seed 2901).
- Target after: `QUOTE_REOPEN_MATCH=82/82`, exit 0, on the landed tool.
- Kill rule: any other value on the measured lane revision is a miss. The
  fixture, labels, counter and this contract are not edited after this commit.
  A network failure that yields `UNREACHABLE` counts as a mismatch.

**Sourced:** the fixture quotes come from registry rows S002, S003, S008,
S013, S019, S020, S038 and S044, which were re-opened on 2026-10-23 for this
fixture. New rows that the tool's normalization rests on are opened in wave 1
and cited by `corpus/knowledge/quote-reopen-r29.md`.

## Tool contract (frozen)

```
python3 tools/quote-reopen.py verify --items ITEMS.tsv [--registry SOURCES.md]
```

- `ITEMS.tsv` is UTF-8 and tab-separated, with the header `id<TAB>source_id<TAB>quote`.
- The default registry is `corpus/SOURCES.md` under the tool's lane root
  (the parent of `tools/`).
- Output: one line per item, in input order,
  `QUOTE_REOPEN<TAB><id><TAB><VERDICT><TAB><detail>`, then one line
  `QUOTE_REOPEN_SUMMARY verbatim=<n> absent=<n> too_long=<n> no_source=<n> unreachable=<n>`.
- Verdicts, checked in this order:
  1. `NO_SOURCE`: the id is not a registry row, or the row's `source` cell has
     no `http://` or `https://` URL. The tool uses the first URL in the cell and
     strips trailing `.,;)` characters.
  2. `TOO_LONG`: the normalized quote has more than 25 whitespace-separated words.
  3. `UNREACHABLE`: the fetch failed, the final status is not 2xx, the content
     type is not `text/html`, `application/xhtml+xml` or `text/plain`, or the
     body is over 8 MiB.
  4. `VERBATIM` or `ABSENT`, by the match rule below.
- Fetch bounds: the tool fetches only registry URLs, with GET only, the fragment
  removed, http and https only (redirects too), a 30 s timeout, one retry, no
  cookies or credentials, and each URL at most once per run. The User-Agent
  contains `chousa-quote-reopen`.
- HTML to text: Python `html.parser` semantics with character references
  decoded. The content of `script`, `style`, `noscript`, `template` and `head`
  is dropped, and comments are dropped. Block-level elements (at least `p div
  li ul ol table tr td th h1-h6 br section article header footer nav pre
  blockquote dt dd dl figure figcaption hr main aside`) emit one space at start
  and end. Inline elements emit nothing.
- Normalization, applied to page text and quote alike: Unicode NFKC; U+2018,
  U+2019, U+201A and U+201B become `'`; U+201C, U+201D, U+201E and U+201F
  become `"`; U+00AD, U+200B, U+200C, U+200D and U+FEFF are deleted; every
  whitespace run (Python `str.split()`) becomes one space; ends are stripped.
- Match: `VERBATIM` iff the normalized quote occurs in the normalized page text
  at an offset where the character before it (if any) and the character after
  it (if any) are not alphanumeric (`str.isalnum`). Matching is case-sensitive.
  Otherwise `ABSENT`.
- Exit codes: 0 if every item is `VERBATIM`, 1 if any item has another verdict,
  2 on a usage or I/O error.

## Fixture (frozen)

`corpus/fixtures/quote-reopen-r29/items.tsv` holds 40 items with random hex
ids. `labels.tsv` holds their labels and classes. The labels are true by
construction, not by running an implementation:

| class | n | label | construction |
|---|---:|---|---|
| verbatim-inline-markup | 9 | VERBATIM | copied from page text whose HTML has a tag or line break inside the span |
| verbatim-plain | 3 | VERBATIM | copied from plain paragraph text |
| verbatim-typographic-apostrophe | 2 | VERBATIM | copied with `'` where the page has U+2019 |
| too-long-true-text | 3 | TOO_LONG | true page text of 34 to 35 words |
| no-source-unregistered-id | 1 | NO_SOURCE | id S999, which has no registry row |
| no-source-own-work-row | 2 | NO_SOURCE | S001 and S045, whose source cells hold no URL |
| absent-fabricated | 4 | ABSENT | plausible sentences written for the fixture |
| absent-one-word-edit | 4 | ABSENT | one word of a true quote changed or deleted |
| absent-cross-attributed | 4 | ABSENT | a true quote attributed to another registry row |
| absent-spliced | 4 | ABSENT | two true fragments joined with words omitted, no ellipsis |
| absent-truncated-token | 4 | ABSENT | a true quote cut inside a word (3 at the end, 1 at the start) |

The run-time variants are described in the `c1-count.py` docstring: 14
sub-spans labeled VERBATIM, 14 adjacent-token transpositions labeled ABSENT and
14 rotation cross-attributions labeled ABSENT. The ids are fresh and the order
is shuffled on every run. So a candidate that keys on fixture ids or on the
committed item order cannot reach 82/82.

## Pre-freeze controls (scored by the control wave with this counter)

| control | what it skips | expected ceiling |
|---|---|---|
| do-nothing | no tool at all | 0/82 (measured: 0/82 above) |
| always-VERBATIM | all reading and judging | 28/82 |
| always-ABSENT (all-false) | all reading and judging | 48/82 |
| no-reader | never fetches; registry, length and NO_SOURCE logic only, ABSENT otherwise | 54/82 |
| junk | random verdicts | about 1/4 of 82 |
| raw-grep shortcut | fetch, then substring search over raw HTML with no text extraction or normalization | below 82 |
| casefold, no token boundary | normalized text, case-folded substring search with no boundary rule | below 82 |
| label-keyed shortcut | reads the committed `labels.tsv` and `items.tsv` and answers by quote text | below 82 |
| id-keyed shortcut | answers from fixture ids | below 82 |

Any control that reaches 82/82 voids this design before data. The control wave
commits each receipt under `.ufo/waves/round-29/controls/`.

## Not claimed

The claim covers only verbatim location under the rules above. It does not
cover whether a quote supports a claim, whether the source is true, or whether
the source is still the same page later. It also does not cover PDF sources,
pages rendered by JavaScript, quotes with an ellipsis, case-folded or
paraphrased matches, or a quote that spans two block elements as a reader would
see them. The operability score stays 3 on its round-1 scale. The new
observable is reported beside it and does not replace it.
