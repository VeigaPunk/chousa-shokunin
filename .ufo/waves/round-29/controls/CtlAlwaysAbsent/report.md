# CtlAlwaysAbsent — always-ABSENT (all-false)

## Axes and counterexample

Claim C1's declared axis is **operability** (`corpus/evidence/round29/claims.md:9-24`). This control reviews the discrimination of that measurement, not the lane's axis score or admission. Seed robustness and provenance are review concerns, not replacement axes.

`control.py` reads only the supplied TSV to copy each item ID, emits `ABSENT` for every item in input order, prints the required summary, and exits 1 because the verdicts are not all VERBATIM. It performs no source lookup, quote inspection, length check, page fetch, HTML extraction, normalization, or verbatim location. It does not read fixture labels or the source registry.

The strongest observed counterexample is that zero quote-location work still earns **48/82**: all 20 frozen ABSENT cases and all 28 runtime negative cases. It misses all 28 VERBATIM cases, three TOO_LONG cases, and three NO_SOURCE cases. The expected 48/82 ceiling is confirmed on both seeds. The generator preserves those label counts independently of seed (`c1-count.py:49-77`), so changing IDs, order, or sampled subspans cannot improve this constant control.

## Frozen counter and commands

Both receipts record counter SHA-256 `fc219ef871ebd24b6ef8aab7c1bb526a9d645839de8ae86557d9289521373051` and `predicate_holds: false`.

Working directory for both commands: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.

```sh
timeout 60s python3 corpus/evidence/round29/c1-count.py --seed 2901 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlAlwaysAbsent/receipt.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlAlwaysAbsent/control.py
timeout 60s python3 corpus/evidence/round29/c1-count.py --seed 2902 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlAlwaysAbsent/receipt-seed2.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlAlwaysAbsent/control.py
```

## Seed 2901 output

```text
class absent-cross-attributed 4/4
class absent-fabricated 4/4
class absent-one-word-edit 4/4
class absent-spliced 4/4
class absent-truncated-token 4/4
class no-source-own-work-row 0/2
class no-source-unregistered-id 0/1
class runtime-crossattr 14/14
class runtime-subspan 0/14
class runtime-transpose 14/14
class too-long-true-text 0/3
class verbatim-inline-markup 0/9
class verbatim-plain 0/3
class verbatim-typographic-apostrophe 0/2
seed=2901 tool_exit=1 wall_s=0.02
QUOTE_REOPEN_MATCH=48/82
```

Counter exit: **1**. Control exit: **1**. Receipt: `receipt.json`; recorded stderr is empty.

## Seed 2902 output

```text
class absent-cross-attributed 4/4
class absent-fabricated 4/4
class absent-one-word-edit 4/4
class absent-spliced 4/4
class absent-truncated-token 4/4
class no-source-own-work-row 0/2
class no-source-unregistered-id 0/1
class runtime-crossattr 14/14
class runtime-subspan 0/14
class runtime-transpose 14/14
class too-long-true-text 0/3
class verbatim-inline-markup 0/9
class verbatim-plain 0/3
class verbatim-typographic-apostrophe 0/2
seed=2902 tool_exit=1 wall_s=0.02
QUOTE_REOPEN_MATCH=48/82
```

Counter exit: **1**. Control exit: **1**. Receipt: `receipt-seed2.json`; recorded stderr is empty.

## Further gaming and smallest safe correction

The all-false control does **not** reach 82/82 and does not invalidate the counter by the frozen control rule. Partial accuracy must not be represented as proof of quote-location capability. No counter edit is warranted by this observed control alone; retain the exact 82/82 predicate and per-class evidence.

[INFERENCE] A variant adding only the three NO_SOURCE and three TOO_LONG prechecks could reach 54/82 without page reading; those six misses are shown above and the corresponding no-reader ceiling is already declared in `claims.md:115`.

[INFERENCE] A more aggressive always-ABSENT-default variant could read the public fixture/labels, recognize frozen cases by `(source_id, quote)`, and recognize every allowed 5-to-n-1-token contiguous subspan of each known VERBATIM quote under its original source. The frozen counter generates positives only from these accessible quotes and generates the remaining runtime cases as ABSENT (`c1-count.py:63-77`). This exposes a plausible route to 82/82 without real live-source location, unlike an ID-only or exact-quote-only lookup. This variant was **not implemented or scored in this assignment**; no 82/82 bypass is claimed as observed. If independently confirmed, the smallest safe design correction is a new pre-data freeze with independently held-out positive source/quote material, rather than additional seeds over the same public positive basis. The current frozen files remain untouched.

## Scope and tooling

Only the four assigned artifacts under `.ufo/waves/round-29/controls/CtlAlwaysAbsent/` were written. No network access, git/jj commands, real-tool implementation, or runtime judgment was performed. Both bounded counter processes completed with exit 1; no started process remains running. No tools were installed or updated.

## v2 rescore

The preceding sections preserve the v1 experiment. The rescore assignment identifies the v2 freeze as lane commit `12244431d636bfa615d7e8d3a0a48b85b3cba06f`; the revised predicate is exactly `QUOTE_REOPEN_MATCH=130/130` (`claims.md:31-53`). `control.py` was left unchanged. Both new receipts record counter SHA-256 `574ffcad7a78d2fdf04b895445c1aac72537cc548b944cae62012baf4ba4e2dd`, `predicate_holds: false`, and empty stderr.

Working directory: `/home/vgpnk/Projects/shokunin/chousa-shokunin`. The two independent rescoring commands were run concurrently:

```sh
timeout 600s python3 corpus/evidence/round29/c1-count.py --seed 2901 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlAlwaysAbsent/receipt-v2.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlAlwaysAbsent/control.py
timeout 600s python3 corpus/evidence/round29/c1-count.py --seed 2902 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlAlwaysAbsent/receipt-v2-seed2.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlAlwaysAbsent/control.py
```

### v2 seed 2901

```text
class absent-cross-attributed 4/4
class absent-fabricated 4/4
class absent-one-word-edit 4/4
class absent-spliced 4/4
class absent-truncated-token 4/4
class no-source-own-work-row 0/2
class no-source-unregistered-id 0/1
class runtime-crossattr 14/14
class runtime-page-transpose 24/24
class runtime-page-window 0/24
class runtime-subspan 0/14
class runtime-transpose 14/14
class too-long-true-text 0/3
class verbatim-inline-markup 0/9
class verbatim-plain 0/3
class verbatim-typographic-apostrophe 0/2
seed=2901 tool_exit=1 wall_s=0.02
QUOTE_REOPEN_MATCH=72/130
```

Counter exit: **1**. Unchanged control exit: **1**. Receipt: `receipt-v2.json`.

### v2 seed 2902

```text
class absent-cross-attributed 4/4
class absent-fabricated 4/4
class absent-one-word-edit 4/4
class absent-spliced 4/4
class absent-truncated-token 4/4
class no-source-own-work-row 0/2
class no-source-unregistered-id 0/1
class runtime-crossattr 14/14
class runtime-page-transpose 24/24
class runtime-page-window 0/24
class runtime-subspan 0/14
class runtime-transpose 14/14
class too-long-true-text 0/3
class verbatim-inline-markup 0/9
class verbatim-plain 0/3
class verbatim-typographic-apostrophe 0/2
seed=2902 tool_exit=1 wall_s=0.02
QUOTE_REOPEN_MATCH=72/130
```

Counter exit: **1**. Unchanged control exit: **1**. Receipt: `receipt-v2-seed2.json`.

### v2 review

The expected **72/130** all-false ceiling (`claims.md:141`) is confirmed on both seeds: 48 previous ABSENT matches plus all 24 new page-transpose negatives, with all 24 new page-window positives missed. This control does not reach 130/130 and supplies no reason to alter the v2 predicate. Its impacted claim axis remains operability; partial classification accuracy is not evidence of real quote location.

The v1 public-fixture lookup risk above is now historical: revised `claims.md:3-10` records that `CtlLabelKeyed` actually reached 82/82 and voided v1. [INFERENCE] Adding only NO_SOURCE/TOO_LONG prechecks to this constant control raises its v2 ceiling to 78/130, not 130/130; public fixture/positive-span lookup alone still lacks the 24 page-window positives. No full-score v2 bypass was implemented or observed in this assigned rescore.

The control itself still performs no network access. The v2 counter made the prescribed source-registry GETs to generate page cases. Only the two v2 receipts and this appended report section were written by the rescore; no git/jj writes, control changes, real-tool implementation, tool installation/update, or runtime judgment occurred. Both bounded commands terminated with exit 1; no started process remains running.

## v3 rescore

The v3 assignment identifies the freeze as lane commit `aa5e1a3187955fa923de14e11c150bf1c526efc6`. The counter now draws its own fresh 64-bit seed and no longer accepts `--seed`; the predicate remains exactly 130/130. `control.py` remains unchanged. Both new receipts record counter SHA-256 `cd50965032278c355f780d357c5672f14840fc218bb1b7dc4adaa6993b5c175d`, `predicate_holds: false`, and empty stderr.

Working directory: `/home/vgpnk/Projects/shokunin/chousa-shokunin`. The two independent runs were started concurrently, without any seed override:

```sh
timeout 600s python3 corpus/evidence/round29/c1-count.py --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlAlwaysAbsent/receipt-v3.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlAlwaysAbsent/control.py
timeout 600s python3 corpus/evidence/round29/c1-count.py --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlAlwaysAbsent/receipt-v3-run2.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlAlwaysAbsent/control.py
```

### v3 run 1

```text
class absent-cross-attributed 4/4
class absent-fabricated 4/4
class absent-one-word-edit 4/4
class absent-spliced 4/4
class absent-truncated-token 4/4
class no-source-own-work-row 0/2
class no-source-unregistered-id 0/1
class runtime-crossattr 14/14
class runtime-page-transpose 24/24
class runtime-page-window 0/24
class runtime-subspan 0/14
class runtime-transpose 14/14
class too-long-true-text 0/3
class verbatim-inline-markup 0/9
class verbatim-plain 0/3
class verbatim-typographic-apostrophe 0/2
seed=3871257233662363416 tool_exit=1 wall_s=0.02
QUOTE_REOPEN_MATCH=72/130
```

Counter exit: **1**. Control exit: **1**. Receipt: `receipt-v3.json`.

### v3 run 2

```text
class absent-cross-attributed 4/4
class absent-fabricated 4/4
class absent-one-word-edit 4/4
class absent-spliced 4/4
class absent-truncated-token 4/4
class no-source-own-work-row 0/2
class no-source-unregistered-id 0/1
class runtime-crossattr 14/14
class runtime-page-transpose 24/24
class runtime-page-window 0/24
class runtime-subspan 0/14
class runtime-transpose 14/14
class too-long-true-text 0/3
class verbatim-inline-markup 0/9
class verbatim-plain 0/3
class verbatim-typographic-apostrophe 0/2
seed=17511954584760813018 tool_exit=1 wall_s=0.02
QUOTE_REOPEN_MATCH=72/130
```

Counter exit: **1**. Control exit: **1**. Receipt: `receipt-v3-run2.json`.

### v3 review and scope

Both fresh seeds confirm the unchanged all-false ceiling of **72/130**: every ABSENT class matches, but all 52 VERBATIM cases and the six NO_SOURCE/TOO_LONG cases fail. This control does not meet the v3 predicate and reveals no new full-score bypass. The impacted claim axis remains operability; no correction follows from this constant control alone.

The preceding v2 assessment is historical: current `claims.md:3-18` records that warmed receipt replay reached 130/130 for the publicly selectable v2 seeds, prompting v3's fresh-seed-only interface. No replay variant was implemented in this seat.

Only the two v3 receipts and this appended section were written for the rescore. The unchanged control made no network requests; the counter made its prescribed source-registry GETs. Both bounded commands completed with exit 1, and no started process remains running. No git/jj writes, tool installs/updates, real-tool implementation, or runtime judgment occurred.
