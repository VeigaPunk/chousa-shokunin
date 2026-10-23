# Held-out generalization attack on C1 — HeldOut01

Seat: ChousaR29.HeldOut01. Wave 2 FALSIFY, chousa lane, round 29 (design v3).
Attacked: whether `tools/quote-reopen.py verify` generalizes beyond the frozen
40-item fixture to located quotes the lane itself cited in earlier Gate
sections — items h01 (S002), h02 (S003), h03 (S004) from
`.ufo/waves/round-29/build/ScoutGateQuotes/held-out.tsv` (origin:
`corpus/lessons/round-24.md:49-51`). None of these ids or quotes is in the
fixture; all three sources are pages the lane claims to have opened
2026-10-19.

## Step 1 — blind verdicts (recorded before running the tool)

Each registry URL from `corpus/SOURCES.md` was opened with the `read` tool and
judged by eye under the frozen contract (`corpus/evidence/round29/claims.md`:
NFKC; curly quotes → straight; zero-width/soft marks deleted; whitespace runs
collapse; case-sensitive; non-alphanumeric boundary; ≤25 words).

| item | source | URL | blind verdict | page text seen |
|---|---|---|---|---|
| h01 | S002 | https://ifcncodeofprinciples.poynter.org/the-commitments | VERBATIM | Principle #2 criterion 2: "The applicant uses the best available primary, not secondary, sources of evidence wherever suitable primary sources are available." Quote is a sub-span ending before `.`; preceding char `s`→ wait, boundary: char after "available" is `.` (non-alnum) → VERBATIM. 15 words. |
| h02 | S003 | https://hapgood.us/2019/06/19/sift-the-four-moves/ | VERBATIM | "Trace claims…" section: "…we'll have you trace the claim, quote, or media back to the source, so you can see it in it’s original context and get a sense…" Page uses U+2019 in `it’s` (Caulfield's own typo for `its`); contract folds U+2019→`'` so the lane's straight-quote copy matches. Ends before ` and` → VERBATIM. 20 words. |
| h03 | S004 | https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-24 | VERBATIM | §24.2.1.3: "We advise caution in assessing NRSI according to existing ‘evidence hierarchies’ for studies of effectiveness (Eccles et al 1996…)". Curly ‘ ’ fold to `'`; ends before ` for` → VERBATIM. 11 words. |

## Step 2 — tool run

`items.tsv` (header `id<TAB>source_id<TAB>quote`) written to
`.ufo/waves/round-29/falsify/HeldOut01/items.tsv`. Command from the lane root:

```
$ timeout 300 python3 tools/quote-reopen.py verify --items .ufo/waves/round-29/falsify/HeldOut01/items.tsv
QUOTE_REOPEN	h01	VERBATIM	matched in normalized page text
QUOTE_REOPEN	h02	VERBATIM	matched in normalized page text
QUOTE_REOPEN	h03	VERBATIM	matched in normalized page text
QUOTE_REOPEN_SUMMARY verbatim=3 absent=0 too_long=0 no_source=0 unreachable=0
exit 0, 1.14 s wall
```

## Comparison

| item | blind | tool | result |
|---|---|---|---|
| h01 | VERBATIM | VERBATIM | AGREE |
| h02 | VERBATIM | VERBATIM | AGREE |
| h03 | VERBATIM | VERBATIM | AGREE |

No DISAGREE items; no tool defect and no contract limit exercised beyond the
normalization rules themselves. Exit code 0 matches the contract (all
VERBATIM). Each URL fetched once; all three pages served 2xx text/html.

## Lane citation freshness check

Re-opened `corpus/lessons/round-24.md:49-51`: all three quoted strings are
byte-exact against today's live pages (modulo the contract's quote-fold for
h02/h03). Notably h02's `it's` is the *source's* typo, faithfully copied by
the lane — not a lane misquote. No held-out item is ABSENT through inexact
lane citation; no freshness finding against the lane's round-24 Gate.

## Verdict

**HOLDS** for this sample. The tool generalized correctly to 3/3 held-out
located quotes across 3 different live sources (all distinct fixture-vs-real
conditions: inline markup sub-span h01, typographic apostrophe h02, curly
quote-pair h03).

## Limits

- 3 of 33 held-out rows only (per-seat assignment); siblings cover the rest.
- Blind step used the `read` tool's text rendering, not raw HTML; a markup
  quirk invisible in rendering (e.g. an element boundary mid-quote) could in
  principle differ from the tool's own extraction, though the tool then
  fetched and matched independently, which is the stronger evidence.
- No mutations, no timing/size adversarial items — out of this seat's scope.
- No installs or updates performed; no tools needed beyond python3 + read.

Report: .ufo/waves/round-29/falsify/HeldOut01.md
