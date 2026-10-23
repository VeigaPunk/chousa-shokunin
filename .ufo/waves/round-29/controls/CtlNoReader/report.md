# CtlNoReader — round-29 no-reader control

## Axes and scope

- Operability: frozen `QUOTE_REOPEN_MATCH` score, not a claim to have implemented quote location.
- Calibration: distinguish positive and negative class coverage rather than interpreting every rejected control as a killed mutant.
- Resource cost: zero page fetches for both controls.

`control.py` reads only the registry and the counter-supplied items. It looks for the first HTTP(S) URL in each registry row's **source cell**, strips trailing `.,;)`, and applies `NO_SOURCE` before the normalized >25-word `TOO_LONG` check. Normalization follows the frozen NFKC, punctuation, invisible-character and whitespace rules. Every remaining item is reported `ABSENT`, with detail `page fetch deliberately skipped`.

`control-verbatim.py` has identical bytes except for the one behavior-bearing constant: `FETCH_VERDICT = "VERBATIM"` instead of `"ABSENT"`. It retains the early checks and reports `VERBATIM` for fetch-needing items.

Both controls deliberately skip HTTP, status/content-type/body checks, HTML extraction, page normalization and verbatim/token-boundary matching. Neither control reads fixture labels, fixture quotes, receipts, sibling output, or any page. Python standard library only; no tools installed or updated. Existing Python: `Python 3.14.8`.

## Detector, commands and receipts

Working directory for every run: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.

Every scoring invocation had a 60-second outer `timeout`, a 20-second candidate timeout, and a 65-second tool deadline. All invocations completed; no services or background processes were started. Counter and candidate exit codes were both **1 in all eight runs**; no timeout or candidate stderr occurred in the four receipts.

The four primary commands were:

```text
timeout 60s python3 corpus/evidence/round29/c1-count.py --timeout 20 --seed 2901 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlNoReader/receipt.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlNoReader/control.py
timeout 60s python3 corpus/evidence/round29/c1-count.py --timeout 20 --seed 2902 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlNoReader/receipt-seed2.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlNoReader/control.py
timeout 60s python3 corpus/evidence/round29/c1-count.py --timeout 20 --seed 2901 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlNoReader/receipt-verbatim.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlNoReader/control-verbatim.py
timeout 60s python3 corpus/evidence/round29/c1-count.py --timeout 20 --seed 2902 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlNoReader/receipt-verbatim-seed2.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlNoReader/control-verbatim.py
```

| Control | Seed | Receipt | Counter exit | Candidate exit | Predicate |
|---|---:|---|---:|---:|---|
| no-reader / ABSENT fallback | 2901 | `receipt.json` | 1 | 1 | false |
| no-reader / ABSENT fallback | 2902 | `receipt-seed2.json` | 1 | 1 | false |
| no-reader / VERBATIM fallback | 2901 | `receipt-verbatim.json` | 1 | 1 | false |
| no-reader / VERBATIM fallback | 2902 | `receipt-verbatim-seed2.json` | 1 | 1 | false |

The receipts preserve individual randomized cases, actual verdicts and labels. All four have counter SHA-256 `fc219ef871ebd24b6ef8aab7c1bb526a9d645839de8ae86557d9289521373051` and receipt time `2026-10-23T01:15:55Z`.

## Primary stdout, verbatim

### control.py, seed 2901 — counter exit 1

```text
class absent-cross-attributed 4/4
class absent-fabricated 4/4
class absent-one-word-edit 4/4
class absent-spliced 4/4
class absent-truncated-token 4/4
class no-source-own-work-row 2/2
class no-source-unregistered-id 1/1
class runtime-crossattr 14/14
class runtime-subspan 0/14
class runtime-transpose 14/14
class too-long-true-text 3/3
class verbatim-inline-markup 0/9
class verbatim-plain 0/3
class verbatim-typographic-apostrophe 0/2
seed=2901 tool_exit=1 wall_s=0.02
QUOTE_REOPEN_MATCH=54/82
```

### control.py, seed 2902 — counter exit 1

```text
class absent-cross-attributed 4/4
class absent-fabricated 4/4
class absent-one-word-edit 4/4
class absent-spliced 4/4
class absent-truncated-token 4/4
class no-source-own-work-row 2/2
class no-source-unregistered-id 1/1
class runtime-crossattr 14/14
class runtime-subspan 0/14
class runtime-transpose 14/14
class too-long-true-text 3/3
class verbatim-inline-markup 0/9
class verbatim-plain 0/3
class verbatim-typographic-apostrophe 0/2
seed=2902 tool_exit=1 wall_s=0.02
QUOTE_REOPEN_MATCH=54/82
```

### control-verbatim.py, seed 2901 — counter exit 1

```text
class absent-cross-attributed 0/4
class absent-fabricated 0/4
class absent-one-word-edit 0/4
class absent-spliced 0/4
class absent-truncated-token 0/4
class no-source-own-work-row 2/2
class no-source-unregistered-id 1/1
class runtime-crossattr 0/14
class runtime-subspan 14/14
class runtime-transpose 0/14
class too-long-true-text 3/3
class verbatim-inline-markup 9/9
class verbatim-plain 3/3
class verbatim-typographic-apostrophe 2/2
seed=2901 tool_exit=1 wall_s=0.03
QUOTE_REOPEN_MATCH=34/82
```

### control-verbatim.py, seed 2902 — counter exit 1

```text
class absent-cross-attributed 0/4
class absent-fabricated 0/4
class absent-one-word-edit 0/4
class absent-spliced 0/4
class absent-truncated-token 0/4
class no-source-own-work-row 2/2
class no-source-unregistered-id 1/1
class runtime-crossattr 0/14
class runtime-subspan 14/14
class runtime-transpose 0/14
class too-long-true-text 3/3
class verbatim-inline-markup 9/9
class verbatim-plain 3/3
class verbatim-typographic-apostrophe 2/2
seed=2902 tool_exit=1 wall_s=0.02
QUOTE_REOPEN_MATCH=34/82
```

## Isolated mutation and exact restoration

The initial `control.py` runs above are the pristine scratch baseline. After all four primary runs completed, only line 10 of this owned scratch file was mutated from `FETCH_VERDICT = "ABSENT"` to `FETCH_VERDICT = "VERBATIM"`. The resulting bytes were identical by SHA-256 to the retained `control-verbatim.py` artifact. The same frozen detector was run on the mutated `control.py` for both seeds. Then line 10 was restored exactly and the same detector was run on the restored file for both seeds. These four additional runs omitted only `--receipt`, leaving the four primary receipts intact:

```text
timeout 60s python3 corpus/evidence/round29/c1-count.py --timeout 20 --seed 2901 -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlNoReader/control.py
timeout 60s python3 corpus/evidence/round29/c1-count.py --timeout 20 --seed 2902 -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlNoReader/control.py
```

The expected detector rejects either cheap fallback because neither performs page-based location. The observed scores move 54 -> 34 -> 54 on each seed. **Formal mutation verdict: INCONCLUSIVE, not killed**, because the pristine no-reader baseline itself fails the 82/82 predicate. As a negative control, both versions were rejected as expected; this does not establish counter soundness against other shortcuts.

### Mutated control.py, seed 2901 — counter exit 1

```text
class absent-cross-attributed 0/4
class absent-fabricated 0/4
class absent-one-word-edit 0/4
class absent-spliced 0/4
class absent-truncated-token 0/4
class no-source-own-work-row 2/2
class no-source-unregistered-id 1/1
class runtime-crossattr 0/14
class runtime-subspan 14/14
class runtime-transpose 0/14
class too-long-true-text 3/3
class verbatim-inline-markup 9/9
class verbatim-plain 3/3
class verbatim-typographic-apostrophe 2/2
seed=2901 tool_exit=1 wall_s=0.02
QUOTE_REOPEN_MATCH=34/82
```

### Mutated control.py, seed 2902 — counter exit 1

```text
class absent-cross-attributed 0/4
class absent-fabricated 0/4
class absent-one-word-edit 0/4
class absent-spliced 0/4
class absent-truncated-token 0/4
class no-source-own-work-row 2/2
class no-source-unregistered-id 1/1
class runtime-crossattr 0/14
class runtime-subspan 14/14
class runtime-transpose 0/14
class too-long-true-text 3/3
class verbatim-inline-markup 9/9
class verbatim-plain 3/3
class verbatim-typographic-apostrophe 2/2
seed=2902 tool_exit=1 wall_s=0.02
QUOTE_REOPEN_MATCH=34/82
```

### Restored control.py, seed 2901 — counter exit 1

```text
class absent-cross-attributed 4/4
class absent-fabricated 4/4
class absent-one-word-edit 4/4
class absent-spliced 4/4
class absent-truncated-token 4/4
class no-source-own-work-row 2/2
class no-source-unregistered-id 1/1
class runtime-crossattr 14/14
class runtime-subspan 0/14
class runtime-transpose 14/14
class too-long-true-text 3/3
class verbatim-inline-markup 0/9
class verbatim-plain 0/3
class verbatim-typographic-apostrophe 0/2
seed=2901 tool_exit=1 wall_s=0.02
QUOTE_REOPEN_MATCH=54/82
```

### Restored control.py, seed 2902 — counter exit 1

```text
class absent-cross-attributed 4/4
class absent-fabricated 4/4
class absent-one-word-edit 4/4
class absent-spliced 4/4
class absent-truncated-token 4/4
class no-source-own-work-row 2/2
class no-source-unregistered-id 1/1
class runtime-crossattr 14/14
class runtime-subspan 0/14
class runtime-transpose 14/14
class too-long-true-text 3/3
class verbatim-inline-markup 0/9
class verbatim-plain 0/3
class verbatim-typographic-apostrophe 0/2
seed=2902 tool_exit=1 wall_s=0.02
QUOTE_REOPEN_MATCH=54/82
```

### SHA-256 restoration evidence

Measured with `timeout 20s sha256sum` on the named paths, before scoring, after mutation, and after restoration:

| Artifact / state | SHA-256 |
|---|---|
| `control.py`, pristine | `dc4e925236213ae18f992f2310d648a6d73a5545444ee9aa4af179c3e9bcd568` |
| `control.py`, mutated | `9127f33a2ba9bcf2d8a8075ec3d5a985394800b888c70f4275e9cbc4e3fb053b` |
| `control.py`, restored | `dc4e925236213ae18f992f2310d648a6d73a5545444ee9aa4af179c3e9bcd568` |
| `control-verbatim.py`, before and after | `9127f33a2ba9bcf2d8a8075ec3d5a985394800b888c70f4275e9cbc4e3fb053b` |

Protected input hashes were identical before and after the probe:

| Lane-relative protected input | Before = after SHA-256 |
|---|---|
| `corpus/evidence/round29/claims.md` | `58b3b31b548024c9fecbd15e1b89d299e85c92b7e76bd17c401499683196e1e9` |
| `corpus/evidence/round29/c1-count.py` | `fc219ef871ebd24b6ef8aab7c1bb526a9d645839de8ae86557d9289521373051` |
| `corpus/fixtures/quote-reopen-r29/items.tsv` | `e6305beba9563fe4d37430019831610ddf7a5adf1e35de60869e3b764f939bcc` |
| `corpus/fixtures/quote-reopen-r29/labels.tsv` | `dda1b3768f6f187736a77e5bce094b41822d8574e4798886d00964267343c7a9` |
| `corpus/SOURCES.md` | `8bc103823c3a08114e3f787dca96384a6f739931ae3de8c5bdbc64b7225c64b4` |

## Findings and further gaming

The requested no-reader ceiling was reproduced exactly: **54/82** on both seeds. The six early-check cases are correct in either version; the remaining 76 labels comprise 48 ABSENT and 28 VERBATIM. Constant ABSENT therefore gets 6+48=54, and constant VERBATIM gets 6+28=34. The VERBATIM variant gains the 28 positive cases but loses the 48 negative cases: it is not a no-harm improvement. No tested control reached 82/82.

Changing only the uniform fallback cannot reach 82/82. **[INFERENCE]** A richer no-reader variant could attempt to exploit the public frozen `items.tsv`/`labels.tsv` plus the counter's disclosed token-subspan, adjacent-transposition and source-rotation constructions, classifying generated items without reopening their source pages. Randomizing IDs and order does not hide these quote/source relationships. That variant was not built or scored here, so no 82/82 bypass is claimed. The observed rejection of these two constant-fallback controls must not be presented as proof that the frozen counter requires real page location.

Writes were confined to this assigned `CtlNoReader` directory. No real `tools/quote-reopen.py`, sibling source, fleet files, git index or jj state was modified; no git/jj write command was invoked.

## v2 rescore

Design v1 was voided: the revised frozen `claims.md` records that `CtlLabelKeyed` reached 82/82 on both seeds without fetching pages. Thus the earlier section's untested fixture-derived shortcut was subsequently demonstrated by another seat. This section records the requested rescore under design v2, assigned freeze commit `12244431d636bfa615d7e8d3a0a48b85b3cba06f`, with target 130/130 and 48 additional live-page-sampled cases.

Both existing controls were run **unchanged** on seeds 2901 and 2902. No new mutation or implementation was introduced. The controls still make zero page fetches; the v2 **counter** now fetches source pages to construct its extra cases. All four measurements completed successfully as measurements and rejected the candidate; none was a counter-side fetch error.

### Commands and receipts

Working directory remained `/home/vgpnk/Projects/shokunin/chousa-shokunin`. Every command had `timeout 590s`, a 20-second candidate timeout, and a 600-second tool deadline. All processes exited; none remained running. No installations, git/jj writes or writes outside this control directory occurred.

```text
timeout 590s python3 corpus/evidence/round29/c1-count.py --timeout 20 --seed 2901 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlNoReader/receipt-v2.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlNoReader/control.py
timeout 590s python3 corpus/evidence/round29/c1-count.py --timeout 20 --seed 2902 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlNoReader/receipt-v2-seed2.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlNoReader/control.py
timeout 590s python3 corpus/evidence/round29/c1-count.py --timeout 20 --seed 2901 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlNoReader/receipt-v2-verbatim.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlNoReader/control-verbatim.py
timeout 590s python3 corpus/evidence/round29/c1-count.py --timeout 20 --seed 2902 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlNoReader/receipt-v2-verbatim-seed2.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlNoReader/control-verbatim.py
```

| Control | Seed | Receipt | Match | Counter exit | Candidate exit | Predicate |
|---|---:|---|---|---:|---:|---|
| no-reader / ABSENT fallback | 2901 | `receipt-v2.json` | 78/130 | 1 | 1 | false |
| no-reader / ABSENT fallback | 2902 | `receipt-v2-seed2.json` | 78/130 | 1 | 1 | false |
| no-reader / VERBATIM fallback | 2901 | `receipt-v2-verbatim.json` | 58/130 | 1 | 1 | false |
| no-reader / VERBATIM fallback | 2902 | `receipt-v2-verbatim-seed2.json` | 58/130 | 1 | 1 | false |

All four receipts have empty `stderr_tail`, receipt time `2026-10-23T01:20:28Z`, and counter SHA-256 `574ffcad7a78d2fdf04b895445c1aac72537cc548b944cae62012baf4ba4e2dd`. The counter's `wall_s` measures only the candidate subprocess, not its earlier page sampling.

### control.py, seed 2901 — stdout verbatim; counter exit 1

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
class runtime-subspan 0/14
class runtime-transpose 14/14
class too-long-true-text 3/3
class verbatim-inline-markup 0/9
class verbatim-plain 0/3
class verbatim-typographic-apostrophe 0/2
seed=2901 tool_exit=1 wall_s=0.03
QUOTE_REOPEN_MATCH=78/130
```

### control.py, seed 2902 — stdout verbatim; counter exit 1

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
class runtime-subspan 0/14
class runtime-transpose 14/14
class too-long-true-text 3/3
class verbatim-inline-markup 0/9
class verbatim-plain 0/3
class verbatim-typographic-apostrophe 0/2
seed=2902 tool_exit=1 wall_s=0.02
QUOTE_REOPEN_MATCH=78/130
```

### control-verbatim.py, seed 2901 — stdout verbatim; counter exit 1

```text
class absent-cross-attributed 0/4
class absent-fabricated 0/4
class absent-one-word-edit 0/4
class absent-spliced 0/4
class absent-truncated-token 0/4
class no-source-own-work-row 2/2
class no-source-unregistered-id 1/1
class runtime-crossattr 0/14
class runtime-page-transpose 0/24
class runtime-page-window 24/24
class runtime-subspan 14/14
class runtime-transpose 0/14
class too-long-true-text 3/3
class verbatim-inline-markup 9/9
class verbatim-plain 3/3
class verbatim-typographic-apostrophe 2/2
seed=2901 tool_exit=1 wall_s=0.03
QUOTE_REOPEN_MATCH=58/130
```

### control-verbatim.py, seed 2902 — stdout verbatim; counter exit 1

```text
class absent-cross-attributed 0/4
class absent-fabricated 0/4
class absent-one-word-edit 0/4
class absent-spliced 0/4
class absent-truncated-token 0/4
class no-source-own-work-row 2/2
class no-source-unregistered-id 1/1
class runtime-crossattr 0/14
class runtime-page-transpose 0/24
class runtime-page-window 24/24
class runtime-subspan 14/14
class runtime-transpose 0/14
class too-long-true-text 3/3
class verbatim-inline-markup 9/9
class verbatim-plain 3/3
class verbatim-typographic-apostrophe 2/2
seed=2902 tool_exit=1 wall_s=0.03
QUOTE_REOPEN_MATCH=58/130
```

### Unchanged-byte evidence and conclusion

Before and after the v2 rescore, `timeout 20s sha256sum` returned identical hashes for every input and control:

| Lane-relative path | Before = after SHA-256 |
|---|---|
| `.ufo/waves/round-29/controls/CtlNoReader/control.py` | `dc4e925236213ae18f992f2310d648a6d73a5545444ee9aa4af179c3e9bcd568` |
| `.ufo/waves/round-29/controls/CtlNoReader/control-verbatim.py` | `9127f33a2ba9bcf2d8a8075ec3d5a985394800b888c70f4275e9cbc4e3fb053b` |
| `corpus/evidence/round29/claims.md` | `870664d210549f3b15b8d105d8d300d2084c9cbd73d2cb07ea10b34eb439134e` |
| `corpus/evidence/round29/c1-count.py` | `574ffcad7a78d2fdf04b895445c1aac72537cc548b944cae62012baf4ba4e2dd` |
| `corpus/fixtures/quote-reopen-r29/items.tsv` | `e6305beba9563fe4d37430019831610ddf7a5adf1e35de60869e3b764f939bcc` |
| `corpus/fixtures/quote-reopen-r29/labels.tsv` | `dda1b3768f6f187736a77e5bce094b41822d8574e4798886d00964267343c7a9` |
| `corpus/SOURCES.md` | `8bc103823c3a08114e3f787dca96384a6f739931ae3de8c5bdbc64b7225c64b4` |

The no-reader result equals v2's expected 78/130 ceiling: its earlier 54 matches plus 24 page transpositions. The VERBATIM variant gets its earlier 34 matches plus 24 page windows, or 58/130. Neither unchanged control reaches 130/130. This rescore introduces no new mutant and does not turn the v1 baseline-failing mutation probe into a killed mutant. No v2 bypass was demonstrated by this seat.

## v3 rescore

Design v3 is assigned frozen commit `aa5e1a3187955fa923de14e11c150bf1c526efc6`. Its `claims.md` records that the v2 label-keyed warmed variant reached 130/130 by replaying receipts for caller-selected seeds, voiding v2. The v3 counter removes `--seed` and selects a fresh 64-bit seed for each run. Its 130-case predicate and sampling rules are otherwise unchanged.

Both controls were rescored twice **without changing their bytes**. No caller-selected seed or receipt-replay logic was used. The controls still fetch no pages; only the counter performs page sampling. All four runs completed, each with counter exit **1**, candidate exit **1**, empty candidate stderr and `predicate_holds: false`. No counter-side fetch error occurred.

### Commands, seeds and receipts

Working directory: `/home/vgpnk/Projects/shokunin/chousa-shokunin`. Each command had a 590-second outer timeout, a 20-second candidate timeout and a 600-second tool deadline. All processes exited; no services or background processes remained. No installations or git/jj writes occurred.

```text
timeout 590s python3 corpus/evidence/round29/c1-count.py --timeout 20 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlNoReader/receipt-v3.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlNoReader/control.py
timeout 590s python3 corpus/evidence/round29/c1-count.py --timeout 20 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlNoReader/receipt-v3-run2.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlNoReader/control.py
timeout 590s python3 corpus/evidence/round29/c1-count.py --timeout 20 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlNoReader/receipt-v3-verbatim.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlNoReader/control-verbatim.py
timeout 590s python3 corpus/evidence/round29/c1-count.py --timeout 20 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlNoReader/receipt-v3-verbatim-run2.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlNoReader/control-verbatim.py
```

| Control / run | Fresh seed printed by counter | Receipt | Match | Counter exit | Candidate exit |
|---|---:|---|---|---:|---:|
| no-reader 1 | 11232930774115120281 | `receipt-v3.json` | 78/130 | 1 | 1 |
| no-reader 2 | 6091423367872663604 | `receipt-v3-run2.json` | 78/130 | 1 | 1 |
| VERBATIM variant 1 | 17119390874933931641 | `receipt-v3-verbatim.json` | 58/130 | 1 | 1 |
| VERBATIM variant 2 | 6999734400005532175 | `receipt-v3-verbatim-run2.json` | 58/130 | 1 | 1 |

All four receipts have counter SHA-256 `cd50965032278c355f780d357c5672f14840fc218bb1b7dc4adaa6993b5c175d` and receipt time `2026-10-23T01:28:54Z`.

### control.py, run 1 — stdout verbatim; counter exit 1

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
class runtime-subspan 0/14
class runtime-transpose 14/14
class too-long-true-text 3/3
class verbatim-inline-markup 0/9
class verbatim-plain 0/3
class verbatim-typographic-apostrophe 0/2
seed=11232930774115120281 tool_exit=1 wall_s=0.03
QUOTE_REOPEN_MATCH=78/130
```

### control.py, run 2 — stdout verbatim; counter exit 1

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
class runtime-subspan 0/14
class runtime-transpose 14/14
class too-long-true-text 3/3
class verbatim-inline-markup 0/9
class verbatim-plain 0/3
class verbatim-typographic-apostrophe 0/2
seed=6091423367872663604 tool_exit=1 wall_s=0.03
QUOTE_REOPEN_MATCH=78/130
```

### control-verbatim.py, run 1 — stdout verbatim; counter exit 1

```text
class absent-cross-attributed 0/4
class absent-fabricated 0/4
class absent-one-word-edit 0/4
class absent-spliced 0/4
class absent-truncated-token 0/4
class no-source-own-work-row 2/2
class no-source-unregistered-id 1/1
class runtime-crossattr 0/14
class runtime-page-transpose 0/24
class runtime-page-window 24/24
class runtime-subspan 14/14
class runtime-transpose 0/14
class too-long-true-text 3/3
class verbatim-inline-markup 9/9
class verbatim-plain 3/3
class verbatim-typographic-apostrophe 2/2
seed=17119390874933931641 tool_exit=1 wall_s=0.03
QUOTE_REOPEN_MATCH=58/130
```

### control-verbatim.py, run 2 — stdout verbatim; counter exit 1

```text
class absent-cross-attributed 0/4
class absent-fabricated 0/4
class absent-one-word-edit 0/4
class absent-spliced 0/4
class absent-truncated-token 0/4
class no-source-own-work-row 2/2
class no-source-unregistered-id 1/1
class runtime-crossattr 0/14
class runtime-page-transpose 0/24
class runtime-page-window 24/24
class runtime-subspan 14/14
class runtime-transpose 0/14
class too-long-true-text 3/3
class verbatim-inline-markup 9/9
class verbatim-plain 3/3
class verbatim-typographic-apostrophe 2/2
seed=6999734400005532175 tool_exit=1 wall_s=0.03
QUOTE_REOPEN_MATCH=58/130
```

### Unchanged-byte evidence and conclusion

Before and after the v3 runs, `timeout 20s sha256sum` returned the same hashes:

| Lane-relative path | Before = after SHA-256 |
|---|---|
| `.ufo/waves/round-29/controls/CtlNoReader/control.py` | `dc4e925236213ae18f992f2310d648a6d73a5545444ee9aa4af179c3e9bcd568` |
| `.ufo/waves/round-29/controls/CtlNoReader/control-verbatim.py` | `9127f33a2ba9bcf2d8a8075ec3d5a985394800b888c70f4275e9cbc4e3fb053b` |
| `corpus/evidence/round29/claims.md` | `19ea5fbe2d52e42eff8c96096f543b818c37cf773fdfd22af6011fbf1cf47cfc` |
| `corpus/evidence/round29/c1-count.py` | `cd50965032278c355f780d357c5672f14840fc218bb1b7dc4adaa6993b5c175d` |
| `corpus/fixtures/quote-reopen-r29/items.tsv` | `e6305beba9563fe4d37430019831610ddf7a5adf1e35de60869e3b764f939bcc` |
| `corpus/fixtures/quote-reopen-r29/labels.tsv` | `dda1b3768f6f187736a77e5bce094b41822d8574e4798886d00964267343c7a9` |
| `corpus/SOURCES.md` | `8bc103823c3a08114e3f787dca96384a6f739931ae3de8c5bdbc64b7225c64b4` |

Both unchanged controls remain below 130/130 on both fresh-seed runs. This is another negative-control rejection, not a newly killed mutant; no v3 bypass was demonstrated by this seat. The controls and previous receipts were retained unchanged; only the four new v3 receipts and this appended section were written.

