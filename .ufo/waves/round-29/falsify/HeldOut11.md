# HeldOut11 — held-out generalization attack on C1

Round 29, wave 2 FALSIFY. Attack: take 3 located quotes the lane cited in
earlier rounds (`h31`→S039, `h32`→S029, `h33`→S044 in
`.ufo/waves/round-29/build/ScoutGateQuotes/held-out.tsv`), judge them blind
under the frozen contract (`corpus/evidence/round29/claims.md`), then run
`tools/quote-reopen.py verify` and compare verdicts.

## Step 1 — blind verdicts (recorded before the tool ran)

| item | source | URL (registry source cell) | word count | blind verdict | page text seen |
|---|---|---|---:|---|---|
| h31 | S039 | https://www.w3.org/TR/2013/REC-prov-dm-20130430/ | 23 | VERBATIM | `...optionally expressed. To provide a completely accurate description of the derivation, the generation and usage of the generated and used entities, respectively, can be provided, so as to make the derivation path, through usage, activity, and generation, explicit.` Boundaries: space before `To`, comma after `provided` — both non-alphanumeric. |
| h32 | S029 | https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-iv | 14 | VERBATIM | §IV.1 Introduction: `All Cochrane reviews should be assessed periodically to determine whether an update is needed. Some areas of research evolve rapidly,...` Boundaries: space / space. |
| h33 | S044 | https://docs.python.org/3/library/os.path.html | 12 | VERBATIM | `commonpath` entry: `Return the longest common sub-path of each pathname in the iterable paths. Raise ValueError if paths contain both absolute and relative pathnames...` Page serves `paths` inside `em` (non-block, emits nothing), so the span survives extraction intact. Boundaries: space / space. |

All three normalized quotes are ≤ 25 whitespace-separated words, so TOO_LONG
was excluded by inspection before fetching. No PDF or challenge page among
the three; every fetch returned HTTP 200 `text/html`.

Method note (h31): the `read` tool resolved the W3C URL via the W3C API and
returned only abstract + metadata — not the served document the tool GETs.
I therefore fetched the raw bytes with one bounded GET
(`timeout 60 curl -sS ... https://www.w3.org/TR/2013/REC-prov-dm-20130430/`
→ `HTTP 200 ctype=text/html; charset=utf-8 bytes=271572`, saved under
`/fast/scratch/hyaku/chousa-r29/w2/HeldOut11/prov-dm.html`) and confirmed the
phrase occurs as contiguous plain text (no tags inside the span) in
PROV-DM §5.2.1. That is my blind reading, not the tool's.

## Step 2 — tool run

Items written to `.ufo/waves/round-29/falsify/HeldOut11/items.tsv` (header
`id<TAB>source_id<TAB>quote`). Command from lane root:

```
$ timeout 300 python3 tools/quote-reopen.py verify --items .ufo/waves/round-29/falsify/HeldOut11/items.tsv
QUOTE_REOPEN	h31	VERBATIM	matched in normalized page text
QUOTE_REOPEN	h32	VERBATIM	matched in normalized page text
QUOTE_REOPEN	h33	VERBATIM	matched in normalized page text
QUOTE_REOPEN_SUMMARY verbatim=3 absent=0 too_long=0 no_source=0 unreachable=0
EXIT=0
```

## Per-item comparison

| item | blind | tool | verdict |
|---|---|---|---|
| h31 | VERBATIM | VERBATIM | AGREE |
| h32 | VERBATIM | VERBATIM | AGREE |
| h33 | VERBATIM | VERBATIM | AGREE |

No DISAGREE items. No held-out quote came back ABSENT from an inexact
earlier citation — h31, h32 and h33 are all exact copies of current page
text (h33's `paths` italic is `em`, which the frozen contract's extractor
correctly treats as zero-emitting). The `[spans-lines-48-49]` tag on h32
refers to a line break inside `corpus/lessons/round-26.md`, not to a
multi-block span on the page; the matched text sits inside one paragraph.

## Verdict on C1 (held-out slice)

**HOLDS.** The tool generalizes to 3/3 quotes it never saw (never in the
fixture, drawn from the lane's real earlier-round citations across 3
different hosts: w3.org, cochrane.org, docs.python.org). All fetched live,
all matched under the frozen normalization+boundary rule, exit 0.

## Limits

- 3 items, all true VERBATIM by construction of the attack list — this
  slice does not exercise ABSENT/TOO_LONG/UNREACHABLE on held-out data.
- Blind judgments used the contract semantics against the `read` tool's
  extraction plus one raw-HTML grep for h31; the tool's own `html_to_text`
  may produce different boundary spacing than my manual read, but the
  matched spans are interior paragraph text where both agree.
- No tools installed; no installs needed or performed.

Report: .ufo/waves/round-29/falsify/HeldOut11.md
