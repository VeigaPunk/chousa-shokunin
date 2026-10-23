# CtlIdKeyed — id-keyed shortcut and counter mutation

## Axes and scope

- Operability: exercise both constant fallbacks through the frozen executable counter.
- Calibration / gate integrity: distinguish a genuine 82/82 result from an incorrectly successful counter exit.
- Isolation / reproducibility: mutate one scratch-only line, repeat the same bounded detector, and restore exact bytes.

Lane freeze supplied by the assignment: `f9fd6d6c0982325c40c1b4a86b698859fdb1def8`.
No lane counter, claims, fixture, real tool, git index, jj state, sibling, or fleet file was edited.
No network access or tool installation/update was needed. All started commands completed; no service or background process was started.

## Control

`control.py` joins the committed `items.tsv` ids to `labels.tsv` labels, looks up each incoming id, and otherwise returns `--fallback ABSENT` (default) or `--fallback VERBATIM`. It ignores incoming source ids and quote contents. It performs no fetching, HTML extraction, normalization, token-boundary checking, length checking, or source validation. It emits the required item lines and summary, with the contract's candidate exit behavior.

The counter re-ids **all 82 cases**, not merely the 42 variants. Committed ids are eight hex characters; generated ids are twelve. Consequently this control uses its constant fallback for every scored case, including the 40 frozen items.

## Commands and frozen-counter results

All four commands ran from `/home/vgpnk/Projects/shokunin/chousa-shokunin` with a 40-second outer tool deadline. Each command itself was bounded by `timeout 30s`; the counter's candidate timeout was 10 seconds. The two required persisted receipts are for the stronger ABSENT fallback; VERBATIM outputs are retained below rather than creating additional lane files.

```sh
timeout 30s python3 corpus/evidence/round29/c1-count.py --seed 2901 --timeout 10 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlIdKeyed/receipt.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlIdKeyed/control.py --fallback ABSENT
timeout 30s python3 corpus/evidence/round29/c1-count.py --seed 2902 --timeout 10 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlIdKeyed/receipt-seed2.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlIdKeyed/control.py --fallback ABSENT
timeout 30s python3 corpus/evidence/round29/c1-count.py --seed 2901 --timeout 10 -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlIdKeyed/control.py --fallback VERBATIM
timeout 30s python3 corpus/evidence/round29/c1-count.py --seed 2902 --timeout 10 -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlIdKeyed/control.py --fallback VERBATIM
```

| Fallback | Seed | Match line, verbatim | Counter exit | Candidate exit | Receipt predicate |
|---|---:|---|---:|---:|---|
| ABSENT | 2901 | `QUOTE_REOPEN_MATCH=48/82` | 1 | 1 | false |
| ABSENT | 2902 | `QUOTE_REOPEN_MATCH=48/82` | 1 | 1 | false |
| VERBATIM | 2901 | `QUOTE_REOPEN_MATCH=28/82` | 1 | 0 | no receipt requested |
| VERBATIM | 2902 | `QUOTE_REOPEN_MATCH=28/82` | 1 | 0 | no receipt requested |

### ABSENT, seed 2901 — actual stdout

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

### ABSENT, seed 2902 — actual stdout

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

### VERBATIM, seed 2901 — actual stdout

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

### VERBATIM, seed 2902 — actual stdout

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

All four scoring commands had empty stderr. Neither constant fallback reached 82/82; this id-only shortcut did not break the committed counter.

## Scratch-only counter mutation

Scratch counter: `/fast/scratch/hyaku/chousa-r29/ctl-id/corpus/evidence/round29/c1-count.py`.
Its fixture path is a symlink to the unchanged committed fixture, preserving the original counter bytes and relative-path behavior without editing its path constants. The candidate still uses its committed id map. The scratch counter was copied byte-for-byte before the first detector run.

### Mutant and observed diff

Smallest behavior-bearing mutation: weaken only the exit gate at line 152. The separate receipt predicate at line 147 was intentionally left untouched.

`timeout 10s diff -u` of the committed and mutated scratch counters returned 1 and printed:

```diff
--- /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round29/c1-count.py	2026-10-22 22:12:14.556062846 -0300
+++ /fast/scratch/hyaku/chousa-r29/ctl-id/corpus/evidence/round29/c1-count.py	2026-10-22 22:16:28.631099704 -0300
@@ -149,7 +149,7 @@
         with open(opts.receipt, "w", encoding="utf-8") as f:
             json.dump(rec, f, indent=1, ensure_ascii=False)
             f.write("\n")
-    return 0 if n == t == FROZEN_TOTAL else 1
+    return 0 if n >= 0 else 1
 
 
 if __name__ == "__main__":
```

### Expected detector

Invariant: the counter must exit 0 iff its printed match numerator and denominator are both 82. An intentionally inadequate candidate's counter exit 1 is expected and is **not** a baseline-detector failure.

The same command was used on pristine, mutated and restored bytes, with the same cwd and 40-second subprocess deadline:

```sh
timeout 30s python3 /fast/scratch/hyaku/chousa-r29/ctl-id/corpus/evidence/round29/c1-count.py --seed 2901 --timeout 10 -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlIdKeyed/control.py --fallback ABSENT
```

The in-memory Python detector captured stdout/stderr/returncode, parsed `^QUOTE_REOPEN_MATCH=(\d+)/(\d+)$`, calculated `expected_exit = 0 if n == total == 82 else 1`, and reported `DETECTOR_EXIT=0` only when actual and expected counter exits agreed. Missing score output or timeout would have been inconclusive (`DETECTOR_EXIT=2`). Its stage name was only an output tag and did not affect the command or expectation. The detector reported an outcome rather than terminating its host process, allowing unconditional restoration after detecting the mutant.

### Actual detector outputs

For **each** of pristine, mutated and restored, the complete counter stdout was exactly the ABSENT / seed-2901 stdout block above, including `wall_s=0.02`; stderr was empty. The detector then printed these stage-specific trailers:

```text
STAGE=pristine
COUNTER_EXIT=1
EXPECTED_COUNTER_EXIT=1
DETECTOR_EXIT=0

STAGE=mutated
COUNTER_EXIT=0
EXPECTED_COUNTER_EXIT=1
DETECTOR_EXIT=1

STAGE=restored
COUNTER_EXIT=1
EXPECTED_COUNTER_EXIT=1
DETECTOR_EXIT=0
```

(The stage tag was printed before each counter stdout block; the three exit fields followed it.)

**Verdict: KILLED.** Baseline and restoration passed the detector; the one-line mutant wrongly exited 0 at `QUOTE_REOPEN_MATCH=48/82`. This establishes that line 152's comparison is load-bearing for process success. It does **not** turn the printed match into 82/82, nor weaken the unmodified receipt predicate. No baseline failure was misclassified as a killed mutant.

### Hashes and restoration evidence

Hash command: `timeout 10s sha256sum` over the named files, before and after the probe; mutant hash taken while mutated.

| Artifact / state | SHA-256 |
|---|---|
| Committed counter, before and after | `fc219ef871ebd24b6ef8aab7c1bb526a9d645839de8ae86557d9289521373051` |
| Scratch counter, pristine | `fc219ef871ebd24b6ef8aab7c1bb526a9d645839de8ae86557d9289521373051` |
| Scratch counter, mutated | `2b43d0ce3ed63de5f98e173077392e34cde2887f66acbca742a754697844ba85` |
| Scratch counter, restored | `fc219ef871ebd24b6ef8aab7c1bb526a9d645839de8ae86557d9289521373051` |
| `claims.md`, before and after | `58b3b31b548024c9fecbd15e1b89d299e85c92b7e76bd17c401499683196e1e9` |
| Fixture `items.tsv`, before and after | `e6305beba9563fe4d37430019831610ddf7a5adf1e35de60869e3b764f939bcc` |
| Fixture `labels.tsv`, before and after | `dda1b3768f6f187736a77e5bce094b41822d8574e4798886d00964267343c7a9` |
| `control.py`, before and after | `de2857e44c6cd6ff45fa09124f13ef4fee5acee72e9907886a79386b83bbb144` |
| `receipt.json` | `7076a95b5bb64767ef419762eff315f45f9b2ef50462453c878395201bc5f8ee` |
| `receipt-seed2.json` | `b81aba6cac9648c71edba68dc66a9e7bcb96bb3e67815111d0fae106c4ef6253` |

After restoring line 152, `timeout 10s cmp /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round29/c1-count.py /fast/scratch/hyaku/chousa-r29/ctl-id/corpus/evidence/round29/c1-count.py` returned 0 with no output. Thus restoration was byte-exact, not merely behaviorally similar.

## Further gaming boundary

No path to 82/82 was **exercised** by this assigned id-only control. Changing only its constant fallback cannot succeed: all scored ids miss the lookup, leaving at most 48/82 for these two constants.

[INFERENCE] A broader fixture-memorization variant could key on `(source_id, quote)` instead of id and enumerate the public generator's token-aligned subspans, adjacent-token swaps and rotated cross-attributions, using the committed labels. That is a concrete no-network gaming surface despite fresh ids; its collision behavior and an 82/82 result were not tested here. It is outside this assigned control and must not be reported as an observed 82/82 success. The scratch mutation demonstrated a false exit-0 only after deliberately weakening the counter, not a bypass of the committed counter.

Report: .ufo/waves/round-29/controls/CtlIdKeyed/report.md

## v2 rescore

Design v2 freeze supplied by the parent: lane commit `12244431d636bfa615d7e8d3a0a48b85b3cba06f`.
The new frozen target is `QUOTE_REOPEN_MATCH=130/130`; v1 was voided by the label-keyed control, not by this id-keyed control.

Both existing fallbacks were re-scored **without changing `control.py`**. Its SHA-256 remains `de2857e44c6cd6ff45fa09124f13ef4fee5acee72e9907886a79386b83bbb144`. The v2 counter SHA-256 is `574ffcad7a78d2fdf04b895445c1aac72537cc548b944cae62012baf4ba4e2dd`; v2 `claims.md` SHA-256 is `870664d210549f3b15b8d105d8d300d2084c9cbd73d2cb07ea10b34eb439134e`.

Axes remain operability, calibration/gate integrity, and isolation/reproducibility. All four runs completed successfully as measurements (no counter-side fetch error). The counter performed its prescribed registry-page GETs; this control itself still fetched nothing. No v2 mutation or additional runtime was invoked. No tools were installed or updated.

### Commands and receipts

Each run used this command shape from the lane root, with a 590-second tool deadline, `timeout 580s` on the command, and a 10-second candidate deadline:

```sh
timeout 580s python3 corpus/evidence/round29/c1-count.py --seed SEED --timeout 10 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlIdKeyed/RECEIPT -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlIdKeyed/control.py --fallback FALLBACK
```

Actual substitutions and outcomes:

| Fallback | Seed | Receipt | Match line, verbatim | Counter exit | Candidate exit |
|---|---:|---|---|---:|---:|
| ABSENT | 2901 | `receipt-v2.json` | `QUOTE_REOPEN_MATCH=72/130` | 1 | 1 |
| ABSENT | 2902 | `receipt-v2-seed2.json` | `QUOTE_REOPEN_MATCH=72/130` | 1 | 1 |
| VERBATIM | 2901 | `receipt-v2-verbatim.json` | `QUOTE_REOPEN_MATCH=52/130` | 1 | 0 |
| VERBATIM | 2902 | `receipt-v2-verbatim-seed2.json` | `QUOTE_REOPEN_MATCH=52/130` | 1 | 0 |

### ABSENT, seed 2901 — actual stdout

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

### ABSENT, seed 2902 — actual stdout

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

### VERBATIM, seed 2901 — actual stdout

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

### VERBATIM, seed 2902 — actual stdout

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

All four commands had empty stderr and counter exit 1. Neither unchanged fallback reached 130/130. Fresh ids still defeat the lookup; the 48 page-sampled cases add 24 matches for each constant. The v1 fixture-expansion concern above is historical and does not establish a v2 bypass. No way to reach 130/130 without real verbatim location was exercised here.

Report: .ufo/waves/round-29/controls/CtlIdKeyed/report.md
