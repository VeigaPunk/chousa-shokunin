# always-VERBATIM — round 29 pre-freeze control

## Axes and scope

- **Operability:** distinguish a real quote-location command from a constant-output command.
- **Calibration:** check the frozen counter's stated 28/82 ceiling without treating rejection of one control as proof of counter soundness.
- **Freshness:** this control performs no live source reopening and supplies no freshness evidence.

Only `control.py`, `receipt.json`, `receipt-seed2.json`, and this report were written under `.ufo/waves/round-29/controls/CtlAlwaysVerbatim/`. No counter, fixture, registry, real tool, index, or jj state was edited. No judgment, admission, integration, or shipping was performed.

## What the control skips

The control reads only the supplied TSV item ids, emits `VERBATIM` for each in input order, emits the summary, and exits 0. It ignores source ids and quote contents: no registry lookup, source validation, length check, HTTP request, HTML extraction, normalization, boundary check, or quote location. It reads neither committed fixture nor labels while executing. No network requests were made.

## Commands and receipts

Both commands ran concurrently from `/home/vgpnk/Projects/shokunin/chousa-shokunin`, each capped at 60 seconds:

```sh
timeout 60s python3 corpus/evidence/round29/c1-count.py --seed 2901 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlAlwaysVerbatim/receipt.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlAlwaysVerbatim/control.py

timeout 60s python3 corpus/evidence/round29/c1-count.py --seed 2902 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlAlwaysVerbatim/receipt-seed2.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlAlwaysVerbatim/control.py
```

Both receipts identify counter SHA-256 `fc219ef871ebd24b6ef8aab7c1bb526a9d645839de8ae86557d9289521373051` and timestamp `2026-10-23T01:15:04Z`.

### Seed 2901 — verbatim counter stdout

```text
class absent-cross-attributed 0/4
class absent-fabricated 0/4
class absent-one-word-edit 0/4
class absent-spliced 0/4
class absent-truncated-token 0/4
class no-source-own-work-row 0/2
class no-source-unregistered-id 0/1
class runtime-crossattr 0/14
class runtime-subspan 14/14
class runtime-transpose 0/14
class too-long-true-text 0/3
class verbatim-inline-markup 9/9
class verbatim-plain 3/3
class verbatim-typographic-apostrophe 2/2
seed=2901 tool_exit=0 wall_s=0.02
QUOTE_REOPEN_MATCH=28/82
```

Counter/timeout command exit: **1**. Control exit: **0**. Receipt: `receipt.json`, `predicate_holds: false`.

### Seed 2902 — verbatim counter stdout

```text
class absent-cross-attributed 0/4
class absent-fabricated 0/4
class absent-one-word-edit 0/4
class absent-spliced 0/4
class absent-truncated-token 0/4
class no-source-own-work-row 0/2
class no-source-unregistered-id 0/1
class runtime-crossattr 0/14
class runtime-subspan 14/14
class runtime-transpose 0/14
class too-long-true-text 0/3
class verbatim-inline-markup 9/9
class verbatim-plain 3/3
class verbatim-typographic-apostrophe 2/2
seed=2902 tool_exit=0 wall_s=0.02
QUOTE_REOPEN_MATCH=28/82
```

Counter/timeout command exit: **1**. Control exit: **0**. Receipt: `receipt-seed2.json`, `predicate_holds: false`.

## Counterexample and evidence

The expected ceiling is **confirmed on both seeds**: 14 frozen VERBATIM labels plus 14 runtime subspans match; the other 54 cases do not. Changing fresh ids, order, or subspan selection cannot improve this constant verdict's count because the class totals remain fixed (`c1-count.py:49-87`).

A concrete false-provenance counterexample is frozen origin `76b6a43c`, source `S001`: the label is `NO_SOURCE`, but the control emits `VERBATIM`. The receipts record this mismatch at fresh ids `87b92f347b44` (2901) and `3077969af435` (2902). Evidence: `items.tsv:13`, `labels.tsv:13`, and each receipt's corresponding case. The frozen counter rejects this false positive. No 82/82 shortcut was demonstrated by this control.

## Further gaming and smallest safe correction

No variation that remains constant-VERBATIM can reach 82/82: the set contains other labels. This is an expected rejected control, not an axis trade or an admission decision. No correction is required for rejecting this specific control.

[INFERENCE, untested] A fixture-aware derivative could use committed `(source_id, quote, label)` pairs and the positive fixture quotes as surrogate pages: exact fixture lookup first, then source-aware contiguous token-span lookup against positive quotes, ABSENT otherwise. The counter's generated positives are exclusively subspans of those same positive fixtures; generated negatives are transpositions and rotated source ids (`c1-count.py:49-77`). This creates a plausible path toward 82/82 without fetching or locating any live source. Randomized ids/order do not close that information leak. This derivative was not implemented or scored; its 82/82 result is not claimed.

The smallest safe design correction to consider for that separate weakness is candidate-inaccessible, independently sourced evaluation cases, rather than more id randomization. Any counter change belongs to a separately frozen revision, not an edit to this round's frozen counter. Operability and freshness would otherwise be falsely inferred from fixture memorization; calibration would overstate what a perfect score proves.

## Tooling and process cleanup

No tools were installed or updated. Both scored commands and their child controls completed; no services or persistent processes were started. No extra checks or alternative controls were run.

## v2 rescore

The parent supplied frozen v2 commit `12244431d636bfa615d7e8d3a0a48b85b3cba06f`. The v2 claim header records that a different control voided v1 at 82/82; the preceding report remains the historical v1 measurement. This rescore used the existing `control.py` **unchanged**. Only `receipt-v2.json`, `receipt-v2-seed2.json`, and this appended section were added for v2. The earlier four-file/no-network scope statements describe v1: the v2 counter itself now GETs the registry pages to construct 48 additional cases; this constant control still makes no network requests.

Both commands ran concurrently from `/home/vgpnk/Projects/shokunin/chousa-shokunin`, capped at 600 seconds:

```sh
timeout 600s python3 corpus/evidence/round29/c1-count.py --seed 2901 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlAlwaysVerbatim/receipt-v2.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlAlwaysVerbatim/control.py

timeout 600s python3 corpus/evidence/round29/c1-count.py --seed 2902 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlAlwaysVerbatim/receipt-v2-seed2.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlAlwaysVerbatim/control.py
```

Both receipts identify counter SHA-256 `574ffcad7a78d2fdf04b895445c1aac72537cc548b944cae62012baf4ba4e2dd` and timestamp `2026-10-23T01:20:26Z`.

### v2 seed 2901 — verbatim counter stdout

```text
class absent-cross-attributed 0/4
class absent-fabricated 0/4
class absent-one-word-edit 0/4
class absent-spliced 0/4
class absent-truncated-token 0/4
class no-source-own-work-row 0/2
class no-source-unregistered-id 0/1
class runtime-crossattr 0/14
class runtime-page-transpose 0/24
class runtime-page-window 24/24
class runtime-subspan 14/14
class runtime-transpose 0/14
class too-long-true-text 0/3
class verbatim-inline-markup 9/9
class verbatim-plain 3/3
class verbatim-typographic-apostrophe 2/2
seed=2901 tool_exit=0 wall_s=0.02
QUOTE_REOPEN_MATCH=52/130
```

Counter/timeout command exit: **1**. Control exit: **0**. Receipt: `receipt-v2.json`, `predicate_holds: false`.

### v2 seed 2902 — verbatim counter stdout

```text
class absent-cross-attributed 0/4
class absent-fabricated 0/4
class absent-one-word-edit 0/4
class absent-spliced 0/4
class absent-truncated-token 0/4
class no-source-own-work-row 0/2
class no-source-unregistered-id 0/1
class runtime-crossattr 0/14
class runtime-page-transpose 0/24
class runtime-page-window 24/24
class runtime-subspan 14/14
class runtime-transpose 0/14
class too-long-true-text 0/3
class verbatim-inline-markup 9/9
class verbatim-plain 3/3
class verbatim-typographic-apostrophe 2/2
seed=2902 tool_exit=0 wall_s=0.02
QUOTE_REOPEN_MATCH=52/130
```

Counter/timeout command exit: **1**. Control exit: **0**. Receipt: `receipt-v2-seed2.json`, `predicate_holds: false`.

The v2 expected ceiling **52/130 is confirmed on both seeds**: the original 28 matches plus 24 page-window positives. The 24 new page transpositions are all mismatches. Constant VERBATIM still cannot satisfy the predicate, regardless of ids, order, or sampled text. No 130/130 shortcut was demonstrated or alternative variant implemented. No correction is needed to reject this specific control; these results do not establish broader counter soundness. The reviewed axes remain operability, calibration, and freshness, not an admission judgment.

No tools were installed or updated. Both bounded v2 commands and their child controls completed; no services or persistent processes were started.
