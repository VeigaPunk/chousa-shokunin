# CtlCasefoldNoBoundary — round-29 C1 negative control

## Scope and axes

- Assigned control only: registry lookup, ordered NO_SOURCE/TOO_LONG handling, live bounded GETs, html.parser extraction and frozen normalization are retained. The only behavioral defect is the matching function: `quote.casefold() in text.casefold()`, with no alphanumeric boundary checks. No labels or committed fixture items are read by the control.
- Probe axes: detector sensitivity to the matching rule; per-class coverage; exact restoration/isolation; bounded runtime/network. C1 itself is the declared operability claim.
- Frozen reference supplied by task: `f9fd6d6c0982325c40c1b4a86b698859fdb1def8`. Measurements ran from the lane root against the hashes below; no git/jj write commands were used.
- Only this seat's `control.py`, `receipt.json`, `receipt-seed2.json` and this report were written. No production tool or sibling source was changed. No installations or tool updates.

## Expected detector and observed verdict

The unchanged frozen `corpus/evidence/round29/c1-count.py` should accept the pristine case-sensitive/bounded match at 82/82, reject this mutant below 82, then accept exact restored pristine bytes again. Expected loss: the four frozen `absent-truncated-token` cases, whose proper-subword occurrences must not count as verbatim.

**KILLED.** Pristine seed 2901: 82/82, counter exit 0. Mutant seeds 2901 and 2902: 78/82, counter exit 1 each. Restored pristine seed 2901: 82/82, counter exit 0. The baseline passed, so this is not a baseline-failure/inconclusive result. The only lost class on both mutant runs is `absent-truncated-token` (0/4); all other classes remain perfect.

The candidate itself exits 1 even for the pristine/restored passing counters, as the tool contract requires whenever any input verdict is not VERBATIM. Counter exit and tool exit are distinct.

## Exact counter commands and outputs

Each command had an outer GNU `timeout --kill-after=5s 120s`; the counter also used `--timeout 110`. GETs use a 30-second timeout and one retry, at most one fetch operation per distinct URL per run. The eight distinct source URLs are fetched concurrently, with no on-disk page cache. Redirects are additionally confined to the registry URL allowlist to obey the task's network restriction. All eight source fetches succeeded in both mutant receipts; there were no UNREACHABLE verdicts.

### Mutant seed 2901

```sh
timeout --kill-after=5s 120s python3 corpus/evidence/round29/c1-count.py --seed 2901 --timeout 110 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlCasefoldNoBoundary/receipt.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlCasefoldNoBoundary/control.py
```

```text
class absent-cross-attributed 4/4
class absent-fabricated 4/4
class absent-one-word-edit 4/4
class absent-spliced 4/4
class absent-truncated-token 0/4
class no-source-own-work-row 2/2
class no-source-unregistered-id 1/1
class runtime-crossattr 14/14
class runtime-subspan 14/14
class runtime-transpose 14/14
class too-long-true-text 3/3
class verbatim-inline-markup 9/9
class verbatim-plain 3/3
class verbatim-typographic-apostrophe 2/2
seed=2901 tool_exit=1 wall_s=1.09
QUOTE_REOPEN_MATCH=78/82
COUNTER_EXIT=1
```

Receipt: `receipt.json`; `predicate_holds=false`, `tool_exit=1`.

### Mutant seed 2902

```sh
timeout --kill-after=5s 120s python3 corpus/evidence/round29/c1-count.py --seed 2902 --timeout 110 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlCasefoldNoBoundary/receipt-seed2.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlCasefoldNoBoundary/control.py
```

```text
class absent-cross-attributed 4/4
class absent-fabricated 4/4
class absent-one-word-edit 4/4
class absent-spliced 4/4
class absent-truncated-token 0/4
class no-source-own-work-row 2/2
class no-source-unregistered-id 1/1
class runtime-crossattr 14/14
class runtime-subspan 14/14
class runtime-transpose 14/14
class too-long-true-text 3/3
class verbatim-inline-markup 9/9
class verbatim-plain 3/3
class verbatim-typographic-apostrophe 2/2
seed=2902 tool_exit=1 wall_s=1.09
QUOTE_REOPEN_MATCH=78/82
COUNTER_EXIT=1
```

Receipt: `receipt-seed2.json`; `predicate_holds=false`, `tool_exit=1`.

## Exactly which items lose

Both seeds lose these same four frozen origins, always expected ABSENT but observed VERBATIM. Fresh randomized run IDs and shuffling do not affect this result.

| origin | source | truncated edge | quote |
|---|---|---|---|
| `4798287c` | S008 | end: ans within answer | This is best done by clearly framing the questions the review seeks to ans |
| `98406fc4` | S013 | end: incl within included | Like the JSON standard a byte order mark (U+FEFF) must NOT be incl |
| `ad795e73` | S044 | end: pat within paths | Return the longest common sub-path of each pathname in the iterable pat |
| `f98e78ae` | S020 | start: he within The | he OWL encoding of the PROV Ontology is available here. |

The fixture therefore makes token-boundary handling load-bearing. This combined mutation does not establish independent case-sensitivity coverage: there is no declared case-only negative class.

## Pristine / mutation / exact restoration evidence

The retained `control.py` is intentionally the submitted cheap mutant and was never changed after creation. To avoid leaving a real implementation or extra scratch files, the isolated pristine scratch copy was a Python byte string derived from that file by replacing only the matching function below. That source was passed directly to `python3 -c`, with `__file__` set to the persisted control path. The same frozen counter, seed 2901, cwd and time bounds were used for pristine, mutated and restored behavior. During mutation, the scratch bytes were replaced with the exact persisted control bytes; both required mutant receipts invoke the persisted path, not a different implementation. A `finally` block restored the scratch bytes exactly, after which the restored source was re-executed.

Pristine matching function (all other source bytes identical to the control):

```python
def matches(quote, text):
    start = text.find(quote)
    while start != -1:
        end = start + len(quote)
        if (start == 0 or not text[start - 1].isalnum()) and (end == len(text) or not text[end].isalnum()):
            return True
        start = text.find(quote, start + 1)
    return False
```

Mutated matching function:

```python
def matches(quote, text):
    return quote.casefold() in text.casefold()
```

| scratch stage | SHA-256 |
|---|---|
| before / pristine | `8f94a25b68ec581e5849984e084494e06d3efe586a845555bf0110c9e72afa76` |
| mutated / persisted control | `c2b823bf0c1e837bc345a8a1a07de4fd6fabc65e0f98711e063d1b9d4f1b4bc8` |
| after / restored pristine | `8f94a25b68ec581e5849984e084494e06d3efe586a845555bf0110c9e72afa76` |

`scratch_bytes == pristine_bytes` was True after restoration. The persisted mutant control's before/after hash is unchanged, as recorded below. No original lane file needed restoration because none was modified.

### Pristine detector output

The candidate command was `python3 -c` with `__file__ = '/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlCasefoldNoBoundary/control.py'` followed by the pristine source bytes described above. Counter flags: `--seed 2901 --timeout 110`; no separate receipt path was requested for this scratch stage.

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
seed=2901 tool_exit=1 wall_s=1.21
QUOTE_REOPEN_MATCH=82/82
COUNTER_EXIT=0
```

### Restored detector output

The candidate command was `python3 -c` with `__file__ = '/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlCasefoldNoBoundary/control.py'` followed by the pristine source bytes described above. Counter flags: `--seed 2901 --timeout 110`; no separate receipt path was requested for this scratch stage.

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
seed=2901 tool_exit=1 wall_s=1.13
QUOTE_REOPEN_MATCH=82/82
COUNTER_EXIT=0
```

## Before / after file hashes

| file (lane-relative) | before SHA-256 | after SHA-256 |
|---|---|---|
| `corpus/evidence/round29/claims.md` | `58b3b31b548024c9fecbd15e1b89d299e85c92b7e76bd17c401499683196e1e9` | `58b3b31b548024c9fecbd15e1b89d299e85c92b7e76bd17c401499683196e1e9` |
| `corpus/evidence/round29/c1-count.py` | `fc219ef871ebd24b6ef8aab7c1bb526a9d645839de8ae86557d9289521373051` | `fc219ef871ebd24b6ef8aab7c1bb526a9d645839de8ae86557d9289521373051` |
| `corpus/fixtures/quote-reopen-r29/items.tsv` | `e6305beba9563fe4d37430019831610ddf7a5adf1e35de60869e3b764f939bcc` | `e6305beba9563fe4d37430019831610ddf7a5adf1e35de60869e3b764f939bcc` |
| `corpus/fixtures/quote-reopen-r29/labels.tsv` | `dda1b3768f6f187736a77e5bce094b41822d8574e4798886d00964267343c7a9` | `dda1b3768f6f187736a77e5bce094b41822d8574e4798886d00964267343c7a9` |
| `corpus/SOURCES.md` | `8bc103823c3a08114e3f787dca96384a6f739931ae3de8c5bdbc64b7225c64b4` | `8bc103823c3a08114e3f787dca96384a6f739931ae3de8c5bdbc64b7225c64b4` |
| `.ufo/waves/round-29/controls/CtlCasefoldNoBoundary/control.py` | `c2b823bf0c1e837bc345a8a1a07de4fd6fabc65e0f98711e063d1b9d4f1b4bc8` | `c2b823bf0c1e837bc345a8a1a07de4fd6fabc65e0f98711e063d1b9d4f1b4bc8` |

All six measured file hashes were identical before/after. Both receipts also record the same frozen counter SHA-256. The in-memory baseline/restored variants were the only reference implementation; no baseline file, cache or throwaway script was created. All subprocesses completed and were reaped; the fetch thread pools joined. No service or background process remains from this probe.

## Can this control be gamed further?

No measured shortcut in this seat reached 82/82: the assigned mutant was killed on both seeds. The strict pristine/restored runs are reference implementations, not cheap-control successes.

[INFERENCE, not run] A quote/source-keyed ABSENT override for exactly the four strings above, with the mutant unchanged otherwise, would turn the four observed misses into matches and rescore these two observed case sets to 82/82 without implementing the real boundary rule. This would be fixture memorization, not a valid contract implementation; it still fetches and searches page text. Also, casefolding with genuine boundary checks may evade this fixture's case-sensitivity coverage because no case-only negatives are declared; that separate variant was not executed. Neither inference is claimed as an observed 82/82 no-location control. The frozen counter and contract were not changed.

Report: .ufo/waves/round-29/controls/CtlCasefoldNoBoundary/report.md

## v2 rescore

Design v1 was voided by the separate label-keyed control, not by this seat's control. Design v2 reference supplied by Main: lane commit `12244431d636bfa615d7e8d3a0a48b85b3cba06f`, target 130/130. The existing casefold/no-boundary `control.py` was re-scored unchanged; its SHA-256 remains `c2b823bf0c1e837bc345a8a1a07de4fd6fabc65e0f98711e063d1b9d4f1b4bc8`, identical to the v1 recorded artifact. The v2 counter SHA-256 measured before execution and recorded in both receipts is `574ffcad7a78d2fdf04b895445c1aac72537cc548b944cae62012baf4ba4e2dd`; v2 claims SHA-256 is `870664d210549f3b15b8d105d8d300d2084c9cbd73d2cb07ea10b34eb439134e`. Fixture items, labels and source-registry hashes still equal the v1 values above.

Only the assigned persisted mutant was executed. The scratch pristine baseline was not re-scored, and no control source, counter, fixture, registry, index or jj state was edited. Both independent seeds ran concurrently from the lane root with an outer 590-second timeout (5-second kill grace), and a 90-second candidate timeout. Both counter subprocesses completed and were reaped. No tools were installed or updated.

### Seed 2901

```sh
timeout --kill-after=5s 590s python3 corpus/evidence/round29/c1-count.py --seed 2901 --timeout 90 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlCasefoldNoBoundary/receipt-v2.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlCasefoldNoBoundary/control.py
```

```text
class absent-cross-attributed 4/4
class absent-fabricated 4/4
class absent-one-word-edit 4/4
class absent-spliced 4/4
class absent-truncated-token 0/4
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
seed=2901 tool_exit=1 wall_s=1.09
QUOTE_REOPEN_MATCH=126/130
COUNTER_EXIT=1
```

Receipt: `receipt-v2.json`; `predicate_holds=false`. Outer command wall time: 5.52 seconds.

### Seed 2902

```sh
timeout --kill-after=5s 590s python3 corpus/evidence/round29/c1-count.py --seed 2902 --timeout 90 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlCasefoldNoBoundary/receipt-v2-seed2.json -- python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/controls/CtlCasefoldNoBoundary/control.py
```

```text
class absent-cross-attributed 4/4
class absent-fabricated 4/4
class absent-one-word-edit 4/4
class absent-spliced 4/4
class absent-truncated-token 0/4
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
seed=2902 tool_exit=1 wall_s=1.08
QUOTE_REOPEN_MATCH=126/130
COUNTER_EXIT=1
```

Receipt: `receipt-v2-seed2.json`; `predicate_holds=false`. Outer command wall time: 5.61 seconds.

### v2 finding

The unchanged control remains rejected: 126/130 on both seeds, counter exits 1 and tool exits 1. It loses exactly the same four frozen `absent-truncated-token` origins (`4798287c`, `98406fc4`, `ad795e73`, `f98e78ae`), all ABSENT misclassified as VERBATIM. Every other class is perfect, including both newly sampled page classes (24/24 each). Token-boundary coverage remains load-bearing; this combined mutation still does not isolate independent case-sensitivity coverage.

[INFERENCE, not executed] The same four exact quote/source-keyed ABSENT overrides described for v1 would rescore these two observed v2 case sets to 130/130 without implementing the actual token-boundary rule. This remains a fixture-specific exception scheme that fetches/searches page text, not a measured no-fetch success or a correct verbatim implementation. No additional control variant was run.

