# CtlJunk — round 29 pre-data control

## Axes and scope

- C1 axis: operability; challenge whether a no-reading candidate can satisfy the frozen 82/82 predicate.
- Detector calibration: record cheap-control rejection without treating a failing baseline as a killed mutant.
- Probe cost and integrity: no network, no source lookup, bounded processes, one-line mutation, exact-byte restoration.
- Write scope: only `.ufo/waves/round-29/controls/CtlJunk/`; no git/jj writes, real-tool implementation, fleet changes, or sibling changes.

## Controls and expected detector

`control.py` uses `random.Random(290129).choice(...)` independently for each input row over `(VERBATIM, ABSENT, TOO_LONG, NO_SOURCE, UNREACHABLE)`. `control-binary.py` differs only in the verdict tuple: `(VERBATIM, ABSENT)`. Both accept `--items PATH`, preserve input order and ids, print per-item detail and the five-field summary, and return 1 when any emitted verdict is not VERBATIM.

Both controls skip registry resolution, length classification, all fetches, HTML extraction, normalization, token-boundary matching, and quote/source evaluation. They read the supplied TSV only to obtain ids; they never read fixture labels or page bytes. Fixed control RNG seed: **290129**, unchanged across all runs. Counter variant seeds: **2901** and **2902**.

Expected detector: unchanged `corpus/evidence/round29/c1-count.py`, requiring `QUOTE_REOPEN_MATCH=82/82` and counter exit 0. Every measured invocation instead exited 1. The counter uses unseeded `secrets` for ids and item shuffling (lines 78–86), so identical counter/control seeds do not imply identical match counts on later runs. Receipts retain each measured case, verdict and label.

Under the uniform-draw model, five-way expected matches are 82/5 = 16.4, not about one quarter; binary expected matches are (28 + 48)/2 = 38. Binary cannot classify the three TOO_LONG and three NO_SOURCE items, so its absolute ceiling is 76/82 regardless of its RNG seed. These expectations/ceiling are deductions, not additional measured runs.

## Commands and bounds

All scoring ran from `/home/vgpnk/Projects/shokunin/chousa-shokunin` using this command template, with the four substitutions in the table:

```sh
timeout 60s python3 corpus/evidence/round29/c1-count.py --seed SEED --timeout 30 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlJunk/RECEIPT -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlJunk/CONTROL
```

| Control | Counter seed | Receipt | Counter exit | Tool exit |
|---|---:|---|---:|---:|
| control.py | 2901 | receipt.json | 1 | 1 |
| control.py | 2902 | receipt-seed2.json | 1 | 1 |
| control-binary.py | 2901 | receipt-binary.json | 1 | 1 |
| control-binary.py | 2902 | receipt-binary-seed2.json | 1 | 1 |

Counter child timeout: 30 s; outer timeout: 60 s; tool-call timeout: 65 s. Hash commands used `timeout 10s sha256sum ...`. All started processes exited; no services or background processes were left running. No network was used. No tools were installed or updated.

## Actual scored outputs

### Five-way junk, seed 2901 — receipt.json

```text
class absent-cross-attributed 1/4
class absent-fabricated 0/4
class absent-one-word-edit 0/4
class absent-spliced 1/4
class absent-truncated-token 1/4
class no-source-own-work-row 0/2
class no-source-unregistered-id 0/1
class runtime-crossattr 4/14
class runtime-subspan 3/14
class runtime-transpose 5/14
class too-long-true-text 0/3
class verbatim-inline-markup 2/9
class verbatim-plain 0/3
class verbatim-typographic-apostrophe 0/2
seed=2901 tool_exit=1 wall_s=0.02
QUOTE_REOPEN_MATCH=17/82
```

Counter exit: 1. Receipt `predicate_holds`: false; `stderr_tail`: empty.

### Five-way junk, seed 2902 — receipt-seed2.json

```text
class absent-cross-attributed 0/4
class absent-fabricated 0/4
class absent-one-word-edit 1/4
class absent-spliced 2/4
class absent-truncated-token 2/4
class no-source-own-work-row 0/2
class no-source-unregistered-id 0/1
class runtime-crossattr 2/14
class runtime-subspan 2/14
class runtime-transpose 4/14
class too-long-true-text 1/3
class verbatim-inline-markup 0/9
class verbatim-plain 0/3
class verbatim-typographic-apostrophe 1/2
seed=2902 tool_exit=1 wall_s=0.02
QUOTE_REOPEN_MATCH=15/82
```

Counter exit: 1. Receipt `predicate_holds`: false; `stderr_tail`: empty.

### Binary junk, seed 2901 — receipt-binary.json

```text
class absent-cross-attributed 2/4
class absent-fabricated 2/4
class absent-one-word-edit 1/4
class absent-spliced 2/4
class absent-truncated-token 1/4
class no-source-own-work-row 0/2
class no-source-unregistered-id 0/1
class runtime-crossattr 6/14
class runtime-subspan 10/14
class runtime-transpose 6/14
class too-long-true-text 0/3
class verbatim-inline-markup 2/9
class verbatim-plain 2/3
class verbatim-typographic-apostrophe 1/2
seed=2901 tool_exit=1 wall_s=0.02
QUOTE_REOPEN_MATCH=35/82
```

Counter exit: 1. Receipt `predicate_holds`: false; `stderr_tail`: empty.

### Binary junk, seed 2902 — receipt-binary-seed2.json

```text
class absent-cross-attributed 2/4
class absent-fabricated 1/4
class absent-one-word-edit 1/4
class absent-spliced 0/4
class absent-truncated-token 1/4
class no-source-own-work-row 0/2
class no-source-unregistered-id 0/1
class runtime-crossattr 5/14
class runtime-subspan 6/14
class runtime-transpose 8/14
class too-long-true-text 0/3
class verbatim-inline-markup 3/9
class verbatim-plain 1/3
class verbatim-typographic-apostrophe 1/2
seed=2902 tool_exit=1 wall_s=0.02
QUOTE_REOPEN_MATCH=29/82
```

Counter exit: 1. Receipt `predicate_holds`: false; `stderr_tail`: empty.

## Single-point mutation and exact restoration

Mutation: temporarily replace only `control.py` line 9, the five-element `VERDICTS` tuple, with the two-element tuple used by `control-binary.py`. No frozen counter/fixture bytes changed. The seed-2901 pristine run above, temporary-mutant run below, and restored run below used the same bounded counter command and candidate path; the latter two omitted `--receipt` so the primary receipt was not overwritten:

```sh
timeout 60s python3 corpus/evidence/round29/c1-count.py --seed 2901 --timeout 30 -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlJunk/control.py
```

### Temporary-mutant output

```text
class absent-cross-attributed 2/4
class absent-fabricated 1/4
class absent-one-word-edit 1/4
class absent-spliced 2/4
class absent-truncated-token 2/4
class no-source-own-work-row 0/2
class no-source-unregistered-id 0/1
class runtime-crossattr 5/14
class runtime-subspan 6/14
class runtime-transpose 5/14
class too-long-true-text 0/3
class verbatim-inline-markup 4/9
class verbatim-plain 1/3
class verbatim-typographic-apostrophe 0/2
seed=2901 tool_exit=1 wall_s=0.02
QUOTE_REOPEN_MATCH=29/82
```

Counter exit: 1. Tool exit: 1.

### Restored-byte output

```text
class absent-cross-attributed 1/4
class absent-fabricated 1/4
class absent-one-word-edit 2/4
class absent-spliced 1/4
class absent-truncated-token 0/4
class no-source-own-work-row 0/2
class no-source-unregistered-id 0/1
class runtime-crossattr 6/14
class runtime-subspan 2/14
class runtime-transpose 3/14
class too-long-true-text 1/3
class verbatim-inline-markup 2/9
class verbatim-plain 1/3
class verbatim-typographic-apostrophe 1/2
seed=2901 tool_exit=1 wall_s=0.02
QUOTE_REOPEN_MATCH=21/82
```

Counter exit: 1. Tool exit: 1. Different restored score is consistent with the counter's fresh secret shuffle; source bytes were restored exactly.

SHA-256 obtained with bounded `sha256sum` before mutation, while mutated, and after restoration:

| Path/state | SHA-256 |
|---|---|
| control.py pristine | f6d64324269677674edb2be36a52edb5368d27bccc0aa97e7532fcab0e129864 |
| control.py temporary mutant | 8e5c6a369303a51aad564274730fbcd4400cf4abb59dc10fa3fb82adbf64f09b |
| control.py restored | f6d64324269677674edb2be36a52edb5368d27bccc0aa97e7532fcab0e129864 |
| control-binary.py before/after (unchanged) | 8e5c6a369303a51aad564274730fbcd4400cf4abb59dc10fa3fb82adbf64f09b |

Frozen input SHA-256 values measured before the scored controls and after restoration were identical:

| Path | Before = after SHA-256 |
|---|---|
| corpus/evidence/round29/claims.md | 58b3b31b548024c9fecbd15e1b89d299e85c92b7e76bd17c401499683196e1e9 |
| corpus/evidence/round29/c1-count.py | fc219ef871ebd24b6ef8aab7c1bb526a9d645839de8ae86557d9289521373051 |
| corpus/fixtures/quote-reopen-r29/items.tsv | e6305beba9563fe4d37430019831610ddf7a5adf1e35de60869e3b764f939bcc |
| corpus/fixtures/quote-reopen-r29/labels.tsv | dda1b3768f6f187736a77e5bce094b41822d8574e4798886d00964267343c7a9 |

## Verdict and further-gaming limits

**Both assigned junk controls were rejected; none reached 82/82.** This is not a claim that the whole counter is sound. Formal mutation-test verdict: **inconclusive**, not killed or survived, because the pristine five-way junk baseline already failed the same detector. Exact restoration succeeded regardless of the detector's nonzero exit.

The binary variant raised the observed scores from 17 to 35 and from 15 to 29 while still doing no source work, but it necessarily misses six out-of-pool items (three TOO_LONG and three NO_SOURCE). It cannot reach 82/82 through an RNG-seed change alone. The five-way control can in principle get a lucky all-match assignment; under independent uniform draws its one-trial probability is 5^-82. Repeated/cherry-picked runs would therefore not establish real quote-location capability. No successful random-only gaming variant was found or claimed here, and no seed search was run.

[INFERENCE] A candidate command is not sandboxed away from the committed fixture labels or counter source, so these random probes do not rule out a label/oracle-assisted variant. That is outside this assigned random-control probe; it was not implemented or scored here. No additional runtime, judging, integration, or shipping action was invoked.

Report: .ufo/waves/round-29/controls/CtlJunk/report.md
