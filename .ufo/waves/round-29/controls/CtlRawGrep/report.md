# CtlRawGrep — raw-grep shortcut

## Axes and scope

- **Operability:** C1's declared axis; does this cheap runnable substitute satisfy the frozen 82-item predicate?
- **Calibration:** review lens for false positives, false negatives, and overclaiming what a counter receipt proves; no new claim or axis score is assigned here.
- Frozen counter SHA-256, recorded in both receipts: `fc219ef871ebd24b6ef8aab7c1bb526a9d645839de8ae86557d9289521373051`.

## What the control does and skips

`control.py` reads the source registry, resolves each source cell's first HTTP(S) URL, removes its fragment and trailing `.,;)`, and applies the contract's quote normalization solely for the more-than-25-word TOO_LONG decision. NO_SOURCE precedes TOO_LONG. It fetches each distinct needed registry URL once per run with GET, a 30-second timeout, the `chousa-quote-reopen` User-Agent, no cookies or credentials, an 8-MiB limit and an accepted text content type. Fetches run concurrently; redirects outside the registry URL allowlist are refused. This control makes one attempt per URL, without retry.

It decodes each response body as UTF-8 with replacement of invalid sequences, then uses the **original, unnormalized quote string as a plain substring of the raw response HTML**. It skips HTML text extraction, dropped-element filtering, entity decoding, Unicode/quote/whitespace normalization for matching, and token-boundary checks. No label or fixture oracle is read by the control. All eight needed source URLs were reachable in both measured runs: neither receipt contains an UNREACHABLE verdict.

The only authored artifacts are this report and `control.py` under the assigned directory; the frozen counter generated `receipt.json` and `receipt-seed2.json`. No real verifier, frozen fixture/counter, registry, git index, or jj state was edited. No tool installation or update was needed. All started commands exited; no service or child process remains running.

## Seed 2901

Command, from the lane root:

```sh
timeout 120s python3 corpus/evidence/round29/c1-count.py --seed 2901 --timeout 90 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlRawGrep/receipt.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlRawGrep/control.py
```

Counter stdout, verbatim:

```text
class absent-cross-attributed 4/4
class absent-fabricated 4/4
class absent-one-word-edit 4/4
class absent-spliced 4/4
class absent-truncated-token 3/4
class no-source-own-work-row 2/2
class no-source-unregistered-id 1/1
class runtime-crossattr 14/14
class runtime-subspan 8/14
class runtime-transpose 14/14
class too-long-true-text 3/3
class verbatim-inline-markup 0/9
class verbatim-plain 3/3
class verbatim-typographic-apostrophe 0/2
seed=2901 tool_exit=1 wall_s=1.08
QUOTE_REOPEN_MATCH=64/82
```

Counter exit code: **1**. Control exit code: **1**. Receipt: `.ufo/waves/round-29/controls/CtlRawGrep/receipt.json`; `predicate_holds=false`.

## Seed 2917

Command, from the lane root:

```sh
timeout 120s python3 corpus/evidence/round29/c1-count.py --seed 2917 --timeout 90 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlRawGrep/receipt-seed2.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlRawGrep/control.py
```

Counter stdout, verbatim:

```text
class absent-cross-attributed 4/4
class absent-fabricated 4/4
class absent-one-word-edit 4/4
class absent-spliced 4/4
class absent-truncated-token 3/4
class no-source-own-work-row 2/2
class no-source-unregistered-id 1/1
class runtime-crossattr 14/14
class runtime-subspan 7/14
class runtime-transpose 14/14
class too-long-true-text 3/3
class verbatim-inline-markup 0/9
class verbatim-plain 3/3
class verbatim-typographic-apostrophe 0/2
seed=2917 tool_exit=1 wall_s=1.05
QUOTE_REOPEN_MATCH=63/82
```

Counter exit code: **1**. Control exit code: **1**. Receipt: `.ufo/waves/round-29/controls/CtlRawGrep/receipt-seed2.json`; `predicate_holds=false`.

## Exactly which classes lose

Both seeds lose the same four classes; all other ten classes match completely:

| Class | Seed 2901 matched | Seed 2917 matched | Mismatches |
|---|---:|---:|---|
| verbatim-inline-markup | 0/9 | 0/9 | 9 false ABSENT verdicts in each run |
| verbatim-typographic-apostrophe | 0/2 | 0/2 | 2 false ABSENT verdicts in each run |
| runtime-subspan | 8/14 | 7/14 | 6 / 7 false ABSENT verdicts |
| absent-truncated-token | 3/4 | 3/4 | 1 false VERBATIM verdict in each run |

Strongest counterexample: both receipts show frozen origin `4798287c`, source `S008`, quote `This is best done by clearly framing the questions the review seeks to ans`, labeled ABSENT but returned VERBATIM. The shortcut accepts a fragment ending inside `answer`, exactly the failure the frozen token-boundary rule forbids. This is an observed false-positive provenance claim, not merely missed recall.

For a false negative, both receipts show origin `076df58d`, `S038`, `Objects of the date type are always naive.`, labeled VERBATIM but returned ABSENT; both also miss the runtime subspan `Objects of the date type are`. The static origin is labeled `verbatim-inline-markup` in the frozen labels. Both typographic-apostrophe originals also fail. The receipt evidence is verdict-level; raw page bodies were not retained, so no unobserved HTML byte offset is claimed.

## Further gaming and smallest safe correction

**This assigned control did not reach 82/82.** Its 64/82 and 63/82 receipts show that the frozen counter rejects this raw-grep shortcut on both requested seeds, not that the counter is generally ungamable.

**COUNTER BROKEN BY A MEASURED NO-FETCH VARIANT.** After the raw-grep runs, the existing `CtlLabelKeyed` reviewer supplied the stronger shortcut's receipts, which I read without rerunning its control. It loads committed labels keyed by `(source_id, quote)`, accepts source-bound token-aligned contiguous subspans of the fourteen committed VERBATIM quotes, and defaults other runtime strings to ABSENT. Its `receipt.json` records seed 2901, match 82/82, `predicate_holds=true`, tool exit 1; its `receipt-seed2.json` records the same values for seed 2902. Both pin the same frozen counter digest as this control. Its report records both counter exits as 0 and no network access. Evidence: `.ufo/waves/round-29/controls/CtlLabelKeyed/report.md` and its two receipts. These are peer-produced measured artifacts, not additional raw-grep runs. The counter's `build()` constructs every new positive as such a committed-positive subspan (`c1-count.py:63-77`), so fresh IDs and shuffling do not prevent fixture-oracle replay.

Smallest safe correction to raw grep itself: use the already-declared HTML extraction, normalization and alphanumeric-boundary rule rather than changing labels to accommodate these misses. However, the independently measured no-fetch 82/82 variant triggers the frozen design's stated void-before-data rule; proceeding to data under this predicate would falsely establish operability and freshness. Preserve the counterexample receipts and refreeze a replacement design using source-backed held-out positives not derivable from committed positive spans. Merely hiding runtime labels or changing IDs/order/seeds cannot fix embedded public-fixture answers. This is a fixable measurement defect, not an admissible speed/accuracy tradeoff. No counter revision, runtime judgment or admission decision was made here.

Report: .ufo/waves/round-29/controls/CtlRawGrep/report.md
