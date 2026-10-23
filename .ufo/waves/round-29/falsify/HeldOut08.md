# Falsify C1 — held-out generalization attack (HeldOut08)

## What I attacked
Claim C1 (`tools/quote-reopen.py verify`) on 3 held-out items from
`.ufo/waves/round-29/build/ScoutGateQuotes/held-out.tsv` that were never in the
frozen fixture: h22 (S023, DCMI terms), h23 (S024, schema.org/lastReviewed),
h24 (S025, RFC 9111). Blind verdict first under the frozen contract
(corpus/evidence/round29/claims.md), then tool run, then per-item compare.

## Verdict: HOLDS (on this slice)
Tool agreed with all 3 blind verdicts. No disagreement, no tool defect found,
no freshness finding (every held-out quote is still verbatim at its registry
URL — the lane's earlier-round citations were exact, trailing periods included).

## Evidence

### STEP 1 — blind reads (verdict written before running the tool)
- h22 / S023: `read https://www.dublincore.org/specifications/dublin-core/dcmi-terms/`
  (content-negotiated text/markdown over the HTML page). `<dd>` under
  `### source` reads `A related resource from which the described resource is
  derived.` — twice (lines ~1737 `/terms/` and ~2237 `/elements/1.1/` in the
  served doc), plain text inside `<dd>`. Quote = 10 words → not TOO_LONG.
  Blind verdict: **VERBATIM**.
- h23 / S024: `read https://schema.org/lastReviewed` (text/html, 200). Visible
  body text `Date on which the content on this web page was last reviewed for
  accuracy and/or completeness.` between the property header and
  `### Values expected…`. Quote = 16 words → not TOO_LONG. (The meta-description
  copy is inside `<head>`; the contract drops it, but the body copy suffices.)
  Blind verdict: **VERBATIM**.
- h24 / S025: `read https://www.rfc-editor.org/rfc/rfc9111` (RFC Editor
  rendering, line ~644 of the text): `response_is_fresh = (freshness_lifetime >
  current_age)` as a standalone line in §4.2 Freshness — whitespace on both
  sides, `>` decodes via convert_charrefs. Quote = 5 words → not TOO_LONG.
  Blind verdict: **VERBATIM**.

### STEP 2 — tool run
```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin
$ timeout 300 python3 tools/quote-reopen.py verify --items .ufo/waves/round-29/falsify/HeldOut08/items.tsv
QUOTE_REOPEN	h22	VERBATIM	matched in normalized page text
QUOTE_REOPEN	h23	VERBATIM	matched in normalized page text
QUOTE_REOPEN	h24	VERBATIM	matched in normalized page text
QUOTE_REOPEN_SUMMARY verbatim=3 absent=0 too_long=0 no_source=0 unreachable=0
EXIT=0
```
items.tsv: `.ufo/waves/round-29/falsify/HeldOut08/items.tsv` (verified tab-
separated via `cat -A`).

### Per-item comparison
| item | blind | tool | result |
|---|---|---|---|
| h22 | VERBATIM | VERBATIM | AGREE |
| h23 | VERBATIM | VERBATIM | AGREE |
| h24 | VERBATIM | VERBATIM | AGREE |

0 DISAGREE → no defect attribution needed. No inexact lane citation found.

## Limits
- 3 items, all positive-side; this slice exercises only VERBATIM and the
  fetch/extract path on real registry URLs. It does not probe ABSENT,
  TOO_LONG, NO_SOURCE or UNREACHABLE on held-out data.
- The tool fetched live pages once each; transient 2xx HTML success observed,
  nothing about redirect/challenge robustness beyond this run.
- My blind reads used the `read` tool's rendered text; for h24 the exact char
  sequence in raw HTML is `freshness_lifetime &gt; current_age`, which the
  contract's convert_charrefs rule decodes — the tool's VERBATIM confirms the
  pipeline handles it.

## Tool installs
None. Used preinstalled python3 and the built-in `read` tool. No installs or
updates performed.
