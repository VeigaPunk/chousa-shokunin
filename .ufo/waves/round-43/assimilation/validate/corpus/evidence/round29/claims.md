# Round 29 — frozen claim, predicate, tool contract and controls (design v3)

**Design v3 (latest; frozen before data).** The v2 control rescore found one
more way to meet the counter. The label-keyed seat's "warmed" variant replays
the labels stored in the committed v2 control receipts for seeds 2901 and
2902. With `--seed 2901` or `--seed 2902` it printed
`QUOTE_REOPEN_MATCH=130/130` and exited 0, without fetching anything
(`controls/CtlLabelKeyed/receipt-v2-warmed*.json`). With a fresh seed it scored
106/130. Under this file's own rule, any control that meets the counter voids
the design. The L1 first read the seed-pinned runs as outside the predicate
command, which passes no seed, and committed the receipts at `8026fe60`. That
reading was wrong, and it is recorded as a mistake in the round-29 lesson.
Before any data seat had run the counter (both executor seats confirmed this
in writing), v3 removed the `--seed` option. The caller can no longer choose a
seed; every run draws a fresh 64-bit seed. Nothing else changes: the
predicate, items, labels, contract and `FROZEN_TOTAL = 130` are the same. The
control wave re-scores every control under v3 (receipts `receipt-v3*.json`)
before data.


Design v1 was frozen on 2026-10-23 at lane commit
`f9fd6d6c0982325c40c1b4a86b698859fdb1def8` (base
`6c5eb1466f2b8abbd3de576389037f435016d07b`), before any data seat. The
pre-data control wave then voided it. The label-keyed shortcut control
(`.ufo/waves/round-29/controls/CtlLabelKeyed/`) reached `QUOTE_REOPEN_MATCH=82/82`
on seeds 2901 and 2902 without fetching any page, because every v1 item could be
derived from committed bytes. Under the rule that a design any control meets is
re-designed before data, design v2 below replaces it. v2 adds 48 page-sampled
items that the counter draws from the live pages at run time, and it fixes the
block-element list to an exact list. One more disclosure: while building its
mutant baseline, the control seat `CtlCasefoldNoBoundary` wrote a
contract-following scratch implementation, which scored 82/82 under v1. That
scratch code is not the claim's tool, and v2 is stricter than v1. Design v2 is
frozen in the commit that lands this text, before any data seat (the wave-1
executor). From then on, nothing in this file, `c1-count.py` or the fixture
changes. A miss under the v2 predicate is reported as a miss.

## Claim C1 — operability (capability acquisition)

**Axis by surface:** operability. The surface is a new runnable command,
`tools/quote-reopen.py`. It re-opens located quotes against the live source
that the lane's own `corpus/SOURCES.md` registry names and returns one verdict
per quote. The lane has no such command at the base: `tools/` holds only
`research-gate.sh`, and that gate refuses any source outside the lane corpus.
Operability is the lowest scored axis (SCORECARD.md line 7, score 3). The claim
does not touch `tools/research-gate.sh`. It is a different surface from the
path-denylist and ancestor work of rounds 26 to 28.

**Predicate (one sentence, frozen, v2):** C1 holds iff
`python3 corpus/evidence/round29/c1-count.py -- python3 tools/quote-reopen.py verify`,
run from the lane root, prints `QUOTE_REOPEN_MATCH=130/130`: every one of the 40
frozen fixture items, the 42 fixture-derived run-time variants and the 48
page-sampled run-time items gets a verdict equal to its label.

- Counter code: `n == t == FROZEN_TOTAL` with `FROZEN_TOTAL = 130` in `c1-count.py`.
- Receipt label: `QUOTE_REOPEN_MATCH` and the receipt field `predicate_holds`.
- Before (tool absent, counter v2): `QUOTE_REOPEN_MATCH=0/130`, exit 1.
  Receipt: `.ufo/waves/round-29/controls/before-do-nothing-v2.json` (seed 2901).
  The v1 before receipt `before-do-nothing.json` (0/82) is kept as history.
- Target after: `QUOTE_REOPEN_MATCH=130/130`, exit 0, on the landed tool.
- Kill rule: any other value on the measured lane revision is a miss. A network
  failure that yields `UNREACHABLE` counts as a mismatch. A counter-side fetch
  failure (exit 2) is a failed measurement; it is re-run, never scored as a pass.
- Page-sampled items: for each of the 8 fixture source ids, the counter fetches
  the registry URL twice and extracts text with the reference functions in
  `c1-count.py`, which follow this contract. It then samples 3 token windows
  of 6 to 20 tokens that are present in both fetches (label VERBATIM), and for
  each window one adjacent-token transposition that is absent from both
  fetches (label ABSENT). These labels come from the contract's reference
  functions, not from construction alone. That is the cost of items that
  cannot be read from committed bytes.

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
  is dropped, and comments are dropped. Exactly these block-level elements
  emit one space at start and end (v2 fixes this list; v1 said "at least"):
  `p div li ul ol table tr td th h1 h2 h3 h4 h5 h6 br section article header
  footer nav pre blockquote dt dd dl figure figcaption hr main aside`. Every
  other element emits nothing.
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
sub-spans labeled VERBATIM, 14 adjacent-token transpositions labeled ABSENT,
14 rotation cross-attributions labeled ABSENT, and (v2) 24 page windows
labeled VERBATIM plus 24 page-window transpositions labeled ABSENT. The ids
are fresh and the order is shuffled on every run. So a candidate that keys on
fixture ids, on the committed item order or on committed quote text cannot
reach 130/130.

## Pre-freeze controls

Design v1 was scored by the control wave (receipts under
`.ufo/waves/round-29/controls/<Control>/receipt*.json`; the v1 counter SHA-256 is
`fc219ef871ebd24b6ef8aab7c1bb526a9d645839de8ae86557d9289521373051`):

| control | what it skips | v1 measured (seeds 2901, 2902) | v2 expected ceiling |
|---|---|---|---|
| do-nothing | no tool at all | 0/82 | 0/130 |
| always-VERBATIM | all reading and judging | 28/82, 28/82 | 52/130 |
| always-ABSENT (all-false) | all reading and judging | 48/82, 48/82 | 72/130 |
| no-reader | never fetches; registry, length and NO_SOURCE logic only, ABSENT otherwise | 54/82, 54/82 | 78/130 |
| junk | random verdicts (five-way; binary variant 35/82, 29/82) | 17/82, 15/82 | about 1/4 |
| raw-grep shortcut | fetch, then substring search over raw HTML | 64/82, 63/82 (other seed) | below 130 |
| casefold, no token boundary | case-folded substring search with no boundary rule | 78/82, 78/82 | below 130 |
| label-keyed shortcut | answers from committed labels and spans of committed positives, no fetch | **82/82, 82/82 — voided v1** | 106/130 |
| id-keyed shortcut | answers from fixture ids, constant fallback | 48/82 (ABSENT), 28/82 (VERBATIM) | below 130 |

The control wave re-scores every control under the v2 counter before any data
seat. Those receipts are named `receipt-v2*.json`. Any control that reaches
130/130 voids v2 too: C1 would then be declared exploratory, never re-scaled.

## Not claimed

The claim covers only verbatim location under the rules above. It does not
cover whether a quote supports a claim, whether the source is true, or whether
the source is still the same page later. It also does not cover PDF sources,
pages rendered by JavaScript, quotes with an ellipsis, case-folded or
paraphrased matches, or a quote that spans two block elements as a reader would
see them. The operability score stays 3 on its round-1 scale. The new
observable is reported beside it and does not replace it.
