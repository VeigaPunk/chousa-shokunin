# COUNTER BROKEN: label-keyed shortcut reaches 82/82 without reopening sources

Control: `CtlLabelKeyed` (`label-keyed shortcut`). Best measured score: **82/82**, on both seeds 2901 and 2902. Both counter exits were **0**; both candidate exits were **1**, as the tool contract requires when any verdict is not VERBATIM. The frozen rule in `corpus/evidence/round29/claims.md:122-123` says a control reaching 82/82 voids this design before data. This is counterexample evidence, not a native-judge verdict or admission.

## Axes and skipped work

- **Operability (C1's declared axis):** the counter accepts a runnable label-replay command as if it demonstrated real verbatim location.
- **Freshness:** no source is reopened, so the successful receipt contains no evidence about current page bytes.
- **Calibration:** a perfect score is attainable without the capability; treating it as saturation would be false confidence.

`control.py` reads only the committed fixture `items.tsv`, committed `labels.tsv`, and the counter-supplied incoming items. It constructs `(source_id, quote) -> label` and a source-keyed list of known VERBATIM token sequences. It answers exact fixture keys from the labels; unknown items are VERBATIM only when their whitespace-token sequence is a contiguous span of a known positive for that same source, and ABSENT otherwise. Input ids and order are irrelevant.

This skips all network access, registry validation, source reopening, HTML extraction, Unicode normalization, live-page token-boundary matching, and independent truth assessment. TOO_LONG and NO_SOURCE are replayed labels, not independently implemented checks. Output details explicitly identify the cheat and never claim a page was fetched.

## Strongest local counterexample and cause

The seed-2901 receipt contains runtime-subspan item `d294e93f3340`, source S002, quote `Signatories want their readers to be`, origin `b948e65f`: expected VERBATIM, predicted VERBATIM, match true. It was accepted only because it is a token span of a committed positive, not because the source was reopened. All 14 runtime subspans matched on each seed.

`c1-count.py:49-77` generates every case from the public fixture: the 40 originals are directly keyed; subspans are recoverable from known positives; transpositions and source rotations fall through to ABSENT. Fresh ids and shuffled order at lines 78-86 do not hide `(source_id, quote)`. The measured per-class results below show that these three cheap branches cover all 82 cases on both seeds.

Both receipts pin the frozen counter SHA-256:
`fc219ef871ebd24b6ef8aab7c1bb526a9d645839de8ae86557d9289521373051`.
Both record `predicate_holds: true`.

## Seed 2901: command, verbatim output, exits

Cwd: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.

```sh
timeout 60s python3 corpus/evidence/round29/c1-count.py --seed 2901 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlLabelKeyed/receipt.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlLabelKeyed/control.py
```

```text
class absent-cross-attributed 4/4
class absent-fabricated 4/4
class absent-one-word-edit 4/4
class absent-spliced 4/4
class absent-truncated-token 4/4
class no-source-own-work-row 2/2
class no-source-unregistered-id 1/1
class runtime-crossattr 14/14
class runtime-subspan 14/14
class runtime-transpose 14/14
class too-long-true-text 3/3
class verbatim-inline-markup 9/9
class verbatim-plain 3/3
class verbatim-typographic-apostrophe 2/2
seed=2901 tool_exit=1 wall_s=0.02
QUOTE_REOPEN_MATCH=82/82
```

Counter/timeout exit: **0**. Candidate exit: **1**. Receipt: `receipt.json`.

## Seed 2902: command, verbatim output, exits

Same cwd. These two seed runs were launched concurrently, using separate receipt paths.

```sh
timeout 60s python3 corpus/evidence/round29/c1-count.py --seed 2902 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlLabelKeyed/receipt-seed2.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlLabelKeyed/control.py
```

```text
class absent-cross-attributed 4/4
class absent-fabricated 4/4
class absent-one-word-edit 4/4
class absent-spliced 4/4
class absent-truncated-token 4/4
class no-source-own-work-row 2/2
class no-source-unregistered-id 1/1
class runtime-crossattr 14/14
class runtime-subspan 14/14
class runtime-transpose 14/14
class too-long-true-text 3/3
class verbatim-inline-markup 9/9
class verbatim-plain 3/3
class verbatim-typographic-apostrophe 2/2
seed=2902 tool_exit=1 wall_s=0.02
QUOTE_REOPEN_MATCH=82/82
```

Counter/timeout exit: **0**. Candidate exit: **1**. Receipt: `receipt-seed2.json`.

## Smallest safe correction and further gaming

This is a fixable measurement defect, not an unavoidable tradeoff in live quote verification. Do not use this frozen predicate to establish C1: preserve these receipts, withdraw the design before the data seat, and refreeze a replacement counter whose positive runtime cases include source-backed holdouts that cannot be recovered as spans of the public labeled quotes. Re-run this same shortcut against the replacement before data. Merely changing ids/order/seeds or denying access to `labels.tsv` is insufficient: the current keys and labels can be embedded in the control.

Further gaming cannot improve the observed numeric score: it is already 82/82. [INFERENCE] A variant can embed the committed key table and positive quotes, removing runtime reads of both fixture files while retaining the same shortcut; this variant was not executed. No additional variants or seeds are claimed measured.

## Scope and tooling

Only `control.py`, `receipt.json`, `receipt-seed2.json`, and this `report.md` were written under `.ufo/waves/round-29/controls/CtlLabelKeyed/`. The real tool, frozen counter, fixtures, git index, and jj state were not edited. No git/jj commands, network requests, installs, updates, background jobs, or services were used. Both timeout-bounded scoring commands completed; no started process remains running. No admission, integration, shipping, or other runtime invocation was performed.

Report: .ufo/waves/round-29/controls/CtlLabelKeyed/report.md

## v2 rescore

**130/130 WITHOUT CANDIDATE FETCHING: a receipt-warmed label-keyed variant reaches the v2 target on both requested seeds.** The unchanged, committed-fixture-only control scores **106/130** on each seed. The stronger variant deliberately consumes the labels disclosed by those two prior v2 counter receipts. This is a same-seed replay counterexample, not evidence of success on an independent unseen seed. The original v1 findings above remain historical; this section records the separately frozen v2 measurement.

Assignment revision: lane commit `12244431d636bfa615d7e8d3a0a48b85b3cba06f`. Both unchanged-control receipts pin v2 counter SHA-256 `574ffcad7a78d2fdf04b895445c1aac72537cc548b944cae62012baf4ba4e2dd`.

### Unchanged control, seed 2901

```sh
timeout 180s python3 corpus/evidence/round29/c1-count.py --seed 2901 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlLabelKeyed/receipt-v2.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlLabelKeyed/control.py
```

```text
class absent-cross-attributed 4/4
class absent-fabricated 4/4
class absent-one-word-edit 4/4
class absent-spliced 4/4
class absent-truncated-token 4/4
class no-source-own-work-row 2/2
class no-source-unregistered-id 1/1
class runtime-crossattr 14/14
class runtime-page-transpose 24/24
class runtime-page-window 0/24
class runtime-subspan 14/14
class runtime-transpose 14/14
class too-long-true-text 3/3
class verbatim-inline-markup 9/9
class verbatim-plain 3/3
class verbatim-typographic-apostrophe 2/2
seed=2901 tool_exit=1 wall_s=0.03
QUOTE_REOPEN_MATCH=106/130
```

Counter/timeout exit **1**; candidate exit **1**. Receipt: `receipt-v2.json`, `predicate_holds: false`.

### Unchanged control, seed 2902

```sh
timeout 180s python3 corpus/evidence/round29/c1-count.py --seed 2902 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlLabelKeyed/receipt-v2-seed2.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlLabelKeyed/control.py
```

```text
class absent-cross-attributed 4/4
class absent-fabricated 4/4
class absent-one-word-edit 4/4
class absent-spliced 4/4
class absent-truncated-token 4/4
class no-source-own-work-row 2/2
class no-source-unregistered-id 1/1
class runtime-crossattr 14/14
class runtime-page-transpose 24/24
class runtime-page-window 0/24
class runtime-subspan 14/14
class runtime-transpose 14/14
class too-long-true-text 3/3
class verbatim-inline-markup 9/9
class verbatim-plain 3/3
class verbatim-typographic-apostrophe 2/2
seed=2902 tool_exit=1 wall_s=0.03
QUOTE_REOPEN_MATCH=106/130
```

Counter/timeout exit **1**; candidate exit **1**. Receipt: `receipt-v2-seed2.json`, `predicate_holds: false`.

### Strongest measured no-fetch variant

`control-v2.py` is the **receipt-warmed label-keyed shortcut**. It keeps the fixture map and source-bound token-subspan fallback, and additionally reads every `(source_id, quote, label)` from this directory's `receipt-v2.json` and `receipt-v2-seed2.json`. Those files were generated by the unchanged-control rescores above. It does not read the receipt being written during its own run, use item ids or input order, fetch pages, inspect another process, or implement a real verifier. Its output details explicitly say that answers came from fixtures or prior receipts.

The counter itself performs its authorized live GETs during every v2 run. Therefore the precise skipped work is **all candidate-side source reopening and live-page verification**, not all network activity in the measurement. The two warmed scores reuse seeds whose labels are already exposed. No claim is made for fresh hidden seeds or for a control restricted to committed fixture bytes.

### Receipt-warmed variant, seed 2901

```sh
timeout 180s python3 corpus/evidence/round29/c1-count.py --seed 2901 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlLabelKeyed/receipt-v2-warmed.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlLabelKeyed/control-v2.py
```

```text
class absent-cross-attributed 4/4
class absent-fabricated 4/4
class absent-one-word-edit 4/4
class absent-spliced 4/4
class absent-truncated-token 4/4
class no-source-own-work-row 2/2
class no-source-unregistered-id 1/1
class runtime-crossattr 14/14
class runtime-page-transpose 24/24
class runtime-page-window 24/24
class runtime-subspan 14/14
class runtime-transpose 14/14
class too-long-true-text 3/3
class verbatim-inline-markup 9/9
class verbatim-plain 3/3
class verbatim-typographic-apostrophe 2/2
seed=2901 tool_exit=1 wall_s=0.03
QUOTE_REOPEN_MATCH=130/130
```

Counter/timeout exit **0**; candidate exit **1**. Receipt: `receipt-v2-warmed.json`.

### Receipt-warmed variant, seed 2902

```sh
timeout 180s python3 corpus/evidence/round29/c1-count.py --seed 2902 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlLabelKeyed/receipt-v2-warmed-seed2.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlLabelKeyed/control-v2.py
```

```text
class absent-cross-attributed 4/4
class absent-fabricated 4/4
class absent-one-word-edit 4/4
class absent-spliced 4/4
class absent-truncated-token 4/4
class no-source-own-work-row 2/2
class no-source-unregistered-id 1/1
class runtime-crossattr 14/14
class runtime-page-transpose 24/24
class runtime-page-window 24/24
class runtime-subspan 14/14
class runtime-transpose 14/14
class too-long-true-text 3/3
class verbatim-inline-markup 9/9
class verbatim-plain 3/3
class verbatim-typographic-apostrophe 2/2
seed=2902 tool_exit=1 wall_s=0.03
QUOTE_REOPEN_MATCH=130/130
```

Counter/timeout exit **0**; candidate exit **1**. Receipt: `receipt-v2-warmed-seed2.json`.

### Interpretation, impacted axes, and smallest safe correction

The strongest measured score is **130/130 on both seeds**, reached without candidate-side verbatim location. The strongest committed-fixture-only score remains **106/130 on both seeds**: independent page samples do defeat that narrower cheat. The additional success is specifically answer-bearing receipt leakage combined with deterministic sample replay. It must not be described as fresh-seed generalization or genuine source reopening.

Impacted axes remain **operability**, **freshness**, and **calibration**. The counter verifies answer equality, not the provenance of the candidate's answer or evidence that it fetched the current page. Reusing exposed seed-specific samples makes a full score attainable by label replay. This is a fixable measurement/isolation defect, not a capability gain. [INFERENCE] Merely preventing runtime receipt reads is insufficient once their labels can be embedded into a candidate.

Under the already-frozen v2 rule at `claims.md:149-151`, this full-score control is evidence to surface before data; no third numeric target or design change was made here. For any future non-contaminated measurement, the smallest safe procedural correction is to freeze the candidate before drawing a fresh unexposed sample and keep answer-bearing artifacts inaccessible to it for that evaluation. A same-seed receipt-warmed pass must not be admitted as evidence of live reopening. Native judgment remains with the assigned judge; none was invoked here.

### Supplemental scope and tooling

The rescore adds only `control-v2.py`, `receipt-v2.json`, `receipt-v2-seed2.json`, `receipt-v2-warmed.json`, `receipt-v2-warmed-seed2.json`, and this appended section, all inside the assigned control directory. `control.py` was left unchanged. No git/jj commands, installs, updates, services, or background jobs were used. Each scoring command had a 180-second external timeout and completed. Seed pairs were run concurrently; warm runs followed the necessary receipt-producing baseline runs. No process started for this rescore remains running.

Report: .ufo/waves/round-29/controls/CtlLabelKeyed/report.md

## v3 rescore

**Best measured no-fetch score: 115/130. No v3 run in this review reached 130/130.** The unchanged fixture-only control and the unchanged two-seed receipt-warmed control each scored 106/130 twice on fresh seeds. A stronger committed-receipt lookup plus paired-transposition contrast cheat scored 111/130 and 115/130. These are different fresh samples, not paired measurements on identical items.

V3 revision: `aa5e1a3187955fa923de14e11c150bf1c526efc6`.
Counter SHA-256: `cd50965032278c355f780d357c5672f14840fc218bb1b7dc4adaa6993b5c175d`.
The counter no longer accepts `--seed`; every command below omitted it. All counter exits and all candidate exits were **1**. Counter-side page fetches still occur; no candidate fetches pages.

### Exact commands and printed results

All commands ran from `/home/vgpnk/Projects/shokunin/chousa-shokunin` with the following form, substituting the receipt and control paths from the table:

```sh
timeout 180s python3 corpus/evidence/round29/c1-count.py --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlLabelKeyed/RECEIPT -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlLabelKeyed/CONTROL
```

| Run | CONTROL | RECEIPT | Counter exit | Candidate exit |
|---|---|---|---|---|
| Original 1 | control.py | receipt-v3.json | 1 | 1 |
| Original 2 | control.py | receipt-v3-run2.json | 1 | 1 |
| Warmed 1 | control-v2.py | receipt-v3-warmed.json | 1 | 1 |
| Warmed 2 | control-v2.py | receipt-v3-warmed-run2-corrected.json | 1 | 1 |
| Stronger contrast 1 | control-v3.py | receipt-v3-contrast.json | 1 | 1 |
| Stronger contrast 2 | control-v3.py | receipt-v3-contrast-run2.json | 1 | 1 |

Original 1, verbatim:

```text
seed=12187084370757010200 tool_exit=1 wall_s=0.03
QUOTE_REOPEN_MATCH=106/130
```

Original 2, verbatim:

```text
seed=15029045972482942506 tool_exit=1 wall_s=0.03
QUOTE_REOPEN_MATCH=106/130
```

Warmed 1, verbatim:

```text
seed=13147126367667633711 tool_exit=1 wall_s=0.03
QUOTE_REOPEN_MATCH=106/130
```

Warmed 2, verbatim:

```text
seed=11845952919065769099 tool_exit=1 wall_s=0.03
QUOTE_REOPEN_MATCH=106/130
```

Stronger contrast 1, verbatim:

```text
seed=2334536872557442231 tool_exit=1 wall_s=0.16
QUOTE_REOPEN_MATCH=111/130
```

Stronger contrast 2, verbatim:

```text
seed=1299540907271872818 tool_exit=1 wall_s=0.16
QUOTE_REOPEN_MATCH=115/130
```

One extra invocation was retained honestly: `receipt-v3-warmed-run2.json` was accidentally produced with `control.py`, not `control-v2.py`. It is an additional original-control run, not evidence for the warmed variant; the correctly invoked second warmed run is the separately named `receipt-v3-warmed-run2-corrected.json` above. The accidental invocation also exited counter 1 / candidate 1 and printed:

```text
seed=9915015428490296762 tool_exit=1 wall_s=0.03
QUOTE_REOPEN_MATCH=106/130
```

### Per-class output

Every v3 run above, including the retained accidental original-control run, printed these common per-class lines:

```text
class absent-cross-attributed 4/4
class absent-fabricated 4/4
class absent-one-word-edit 4/4
class absent-spliced 4/4
class absent-truncated-token 4/4
class no-source-own-work-row 2/2
class no-source-unregistered-id 1/1
class runtime-crossattr 14/14
class runtime-subspan 14/14
class runtime-transpose 14/14
class too-long-true-text 3/3
class verbatim-inline-markup 9/9
class verbatim-plain 3/3
class verbatim-typographic-apostrophe 2/2
```

Both original runs, both correctly invoked warmed runs, and the accidental extra original-control run printed:

```text
class runtime-page-transpose 24/24
class runtime-page-window 0/24
```

Stronger contrast run 1 printed:

```text
class runtime-page-transpose 22/24
class runtime-page-window 7/24
```

Stronger contrast run 2 printed:

```text
class runtime-page-transpose 24/24
class runtime-page-window 9/24
```

### Stronger no-fetch control: what it uses and skips

`control-v3.py` reads all receipt-named JSON and before-do-nothing JSON artifacts committed under `.ufo/` at the fixed v3 revision, using read-only, timeout-bounded `git ls-tree` and `git show`. It never loads the new uncommitted v3 receipts or follows a moving HEAD. It builds exact `(source_id, quote) -> label` keys and source-bound positive token-span membership from those historical labels, including the committed receipt of L1's fresh-seed test.

It then exploits the batch construction: a positive window and its adjacent-token transposition have the same source, token count and token multiset. For two incoming quotes differing by one adjacent swap, a known label can orient the pair. Otherwise receipt-derived 2–4-gram frequencies, learned positive-versus-transposed contrast counts, and a small fixed list of common English bigrams guess which ordering is positive. Unsupported or tied unknowns default to ABSENT. Exact known answers are not overridden by the contrast guesses.

This control still skips registry validation, every candidate-side GET, page extraction, normalization against page bytes, source freshness checks, and actual verbatim location. Its diagnostic details describe label lookup, known spans, or contrast guesses rather than invented page provenance. It does not import the counter's reference implementation, inspect another process, modify the counter, or run a real verifier.

### Counterexample status, axes and smallest safe correction

V3 defeats the measured two-seed replay shortcut on fresh draws: its score dropped from the v2 warmed 130/130 to 106/130 twice. The strongest added no-fetch attempt reached 115/130, not the target. Thus this review supplies no full-score v3 counterexample and makes no admission or native-judge decision.

The remaining distinction is still on **operability**, **freshness**, and **calibration**: matching labels is not direct evidence that the candidate reopened current sources. [INFERENCE] Receipt accumulation can increase source-text coverage, and paired positive/negative samples expose an orientation problem that a sufficiently strong offline model or cache could solve without live source verification. The measured contrast control demonstrates partial exploitation, not complete saturation.

The smallest safe handling of these results is to preserve the misses as misses and describe the measured capability narrowly; do not call 115/130 a pass or call a no-fetch guesser a verifier. If actual candidate-side reopening is to be proven in a future measurement, it needs independently observable provenance or controlled fresh content rather than answer equality alone. No counter, predicate, axis, route, or judgment was edited here.

### V3 scope and tooling

New writes were limited to this directory: `control-v3.py`, the seven named `receipt-v3*.json` artifacts, and this appended section. Existing `control.py` and `control-v2.py` were unchanged. Only read-only git commands were used; no git/jj writes, installs, updates, services, or background jobs were used. Independent rescores were launched concurrently. Every scoring command was capped at 180 seconds, and every control-side git command at 10 seconds. All started commands completed; no process remains running.

Report: .ufo/waves/round-29/controls/CtlLabelKeyed/report.md
