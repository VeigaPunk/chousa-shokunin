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

## v2 rescore

The parent froze design v2 at lane commit `12244431d636bfa615d7e8d3a0a48b85b3cba06f` after v1 was voided. The new predicate is 130/130, including 24 live-page windows and 24 live-page transpositions. I read the v2 claims and counter, then rescored the **existing `control.py` unchanged** with seeds 2901 and 2902. Both receipts record counter SHA-256 `574ffcad7a78d2fdf04b895445c1aac72537cc548b944cae62012baf4ba4e2dd`. The v1 evidence and conclusions above remain historical; the v1 no-fetch 82/82 result is not a v2 measurement.

### Seed 2901

Command from the lane root:

```sh
timeout 540s python3 corpus/evidence/round29/c1-count.py --seed 2901 --timeout 90 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlRawGrep/receipt-v2.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlRawGrep/control.py
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
class runtime-page-transpose 24/24
class runtime-page-window 12/24
class runtime-subspan 8/14
class runtime-transpose 14/14
class too-long-true-text 3/3
class verbatim-inline-markup 0/9
class verbatim-plain 3/3
class verbatim-typographic-apostrophe 0/2
seed=2901 tool_exit=1 wall_s=1.07
QUOTE_REOPEN_MATCH=100/130
```

Counter/timeout exit: **1**. Control exit: **1**. Receipt: `.ufo/waves/round-29/controls/CtlRawGrep/receipt-v2.json`; `predicate_holds=false`; zero UNREACHABLE verdicts.

### Seed 2902

Command from the lane root, run concurrently with the first rescore:

```sh
timeout 540s python3 corpus/evidence/round29/c1-count.py --seed 2902 --timeout 90 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlRawGrep/receipt-v2-seed2.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlRawGrep/control.py
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
class runtime-page-transpose 24/24
class runtime-page-window 11/24
class runtime-subspan 8/14
class runtime-transpose 14/14
class too-long-true-text 3/3
class verbatim-inline-markup 0/9
class verbatim-plain 3/3
class verbatim-typographic-apostrophe 0/2
seed=2902 tool_exit=1 wall_s=1.07
QUOTE_REOPEN_MATCH=99/130
```

Counter/timeout exit: **1**. Control exit: **1**. Receipt: `.ufo/waves/round-29/controls/CtlRawGrep/receipt-v2-seed2.json`; `predicate_holds=false`; zero UNREACHABLE verdicts.

### v2 counterexample and impacted axes

The unchanged control loses exactly five classes on both seeds: `absent-truncated-token` (3/4), `verbatim-inline-markup` (0/9), `verbatim-typographic-apostrophe` (0/2), `runtime-subspan` (8/14), and `runtime-page-window` (12/24 and 11/24). All other eleven classes match completely. Total mismatches are 30 and 31; they are not network failures.

The prior inside-token false positive persists. A new seed-2901 example is the S013 page window `is not. See json.org for a definition of JSON values. 3. Line`, expected VERBATIM but returned ABSENT. This demonstrates that the raw-byte shortcut also fails source-derived runtime positives, beyond the committed fixture's markup and typography cases.

Impacted axes remain operability and calibration: this cheap command cannot replace the declared verifier, and a partial score must not be presented as the acquired capability. Smallest safe correction remains implementing the declared extraction, normalization and boundary rule rather than weakening the contract. No 130/130 shortcut was measured by this seat, and rejection of this control does not establish general v2 soundness.

Only the two requested v2 receipts and this appended section were added. `control.py` was not changed; no git/jj commands, tool installs, other-runtime invocation or out-of-scope edits occurred. Both scoring processes exited; none remains running.

Report: .ufo/waves/round-29/controls/CtlRawGrep/report.md

## v3 rescore

The parent froze design v3 at lane commit `aa5e1a3187955fa923de14e11c150bf1c526efc6`, removing caller-selected seeds after the v2 warmed-receipt shortcut reached 130/130. I read the v3 header and invocation contract, then rescored the **existing `control.py` unchanged** twice, concurrently. Neither invocation supplied a seed; both seeds below were generated and printed by the counter. Earlier sections remain historical measurements of their named designs.

### Run 1 — seed 9666967667187893005

Command from the lane root:

```sh
timeout 540s python3 corpus/evidence/round29/c1-count.py --timeout 90 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlRawGrep/receipt-v3.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlRawGrep/control.py
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
class runtime-page-transpose 24/24
class runtime-page-window 9/24
class runtime-subspan 9/14
class runtime-transpose 14/14
class too-long-true-text 3/3
class verbatim-inline-markup 0/9
class verbatim-plain 3/3
class verbatim-typographic-apostrophe 0/2
seed=9666967667187893005 tool_exit=1 wall_s=1.07
QUOTE_REOPEN_MATCH=98/130
```

Counter/timeout exit: **1**. Control exit: **1**. Receipt: `.ufo/waves/round-29/controls/CtlRawGrep/receipt-v3.json`.

### Run 2 — seed 3111698841853131484

Command from the lane root:

```sh
timeout 540s python3 corpus/evidence/round29/c1-count.py --timeout 90 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlRawGrep/receipt-v3-run2.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlRawGrep/control.py
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
class runtime-page-transpose 24/24
class runtime-page-window 6/24
class runtime-subspan 7/14
class runtime-transpose 14/14
class too-long-true-text 3/3
class verbatim-inline-markup 0/9
class verbatim-plain 3/3
class verbatim-typographic-apostrophe 0/2
seed=3111698841853131484 tool_exit=1 wall_s=1.06
QUOTE_REOPEN_MATCH=93/130
```

Counter/timeout exit: **1**. Control exit: **1**. Receipt: `.ufo/waves/round-29/controls/CtlRawGrep/receipt-v3-run2.json`.

### v3 result

Both fresh-seed runs reject this raw-grep shortcut. It loses exactly `absent-truncated-token` (3/4 in both), `verbatim-inline-markup` (0/9 in both), `verbatim-typographic-apostrophe` (0/2 in both), `runtime-subspan` (9/14 and 7/14), and `runtime-page-window` (9/24 and 6/24). All other eleven classes match completely. The raw-substring boundary false positive and extraction/normalization false negatives remain relevant to operability and calibration; the smallest safe correction remains the declared match contract, not weaker expected labels. No 130/130 v3 shortcut was measured by this seat, and these two rejected controls do not prove general counter soundness.

Only the two requested v3 receipts and this appended section were added. The control was unchanged; no tool installation, git/jj operation, other-runtime invocation or out-of-scope write occurred. Both scoring processes exited; none remains running.

Report: .ufo/waves/round-29/controls/CtlRawGrep/report.md

