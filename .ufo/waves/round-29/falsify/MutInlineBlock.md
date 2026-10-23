# MutInlineBlock — round 29 mutation probe

**Scoped verdict: HOLDS; mutant KILLED.** The pristine baseline and restored run each printed `QUOTE_REOPEN_MATCH=130/130` (counter exit 0); the mutant printed `QUOTE_REOPEN_MATCH=117/130` (counter exit 1). This is evidence for the assigned detector's sensitivity, not a judgment of overall contract completeness.

Axes: frozen C1 operability, mutation sensitivity, exact restoration/isolation.

## Isolation and mutation

The only code edit was in `/fast/scratch/hyaku/chousa-r29/w2/MutInlineBlock/tools/quote-reopen.py`. The clone initially received source master `b18b3ec9d8a01f966dd81991615bac27df6d66a1`; its master was then explicitly pinned to the requested landed revision `30c9d24da1815e01e161ed2f52d5f951005cc2b8` before any detector run.

Setup commands, all exit 0:

```sh
timeout 60 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --no-hardlinks --branch master /home/vgpnk/Projects/shokunin/chousa-shokunin /fast/scratch/hyaku/chousa-r29/w2/MutInlineBlock
# cwd: the scratch clone
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git checkout -B master 30c9d24da1815e01e161ed2f52d5f951005cc2b8
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git rev-parse HEAD
# Output: 30c9d24da1815e01e161ed2f52d5f951005cc2b8
```

One behavior-bearing change adds the 5 inline tags to the existing `BLOCK` set; the existing parser therefore emits spaces at their starts, ends and self-closing forms. Actual diff, also saved in `MutInlineBlock/mutant.diff`:

```diff
--- a/tools/quote-reopen.py
+++ b/tools/quote-reopen.py
@@ -59,7 +59,7 @@
 # These elements emit one space at start and at end; every other element emits nothing.
 BLOCK = {"p", "div", "li", "ul", "ol", "table", "tr", "td", "th", "h1", "h2", "h3", "h4", "h5", "h6",
          "br", "section", "article", "header", "footer", "nav", "pre", "blockquote", "dt", "dd", "dl",
-         "figure", "figcaption", "hr", "main", "aside"}
+         "figure", "figcaption", "hr", "main", "aside", "a", "em", "code", "strong", "span"}
 # Typographic quotation marks fold to their ASCII form; soft and zero-width marks vanish.
 QMAP = str.maketrans({"\u2018": "'", "\u2019": "'", "\u201a": "'", "\u201b": "'",
                       "\u201c": '"', "\u201d": '"', "\u201e": '"', "\u201f": '"',
```

Expected detector: the frozen, unseeded C1 counter. Added inline spaces should make exact positive quotes fail when they touch punctuation or cross a token-internal inline boundary; no claim, counter, fixture or label was changed.

## Commands and actual output

All commands below ran from the pinned scratch root. The 590 s timeout plus 5 s kill grace respects the lane's at-most-600 s command bound instead of the requested 900 s. Each run used the unchanged counter and drew its own fresh seed. Stderr was empty in all 3 runs. `tool_exit=1` is the candidate's normal result when items include non-VERBATIM verdicts; the counter's exit code is reported separately.

### Pristine baseline — counter exit 0

```sh
timeout --kill-after=5 590 python3 corpus/evidence/round29/c1-count.py --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/falsify/MutInlineBlock/receipt-baseline.json -- python3 tools/quote-reopen.py verify
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
seed=17052507181688596563 tool_exit=1 wall_s=2.24
QUOTE_REOPEN_MATCH=130/130
```

### Mutant — counter exit 1

```sh
timeout --kill-after=5 590 python3 corpus/evidence/round29/c1-count.py --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/falsify/MutInlineBlock/receipt-mutant.json -- python3 tools/quote-reopen.py verify
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
class runtime-page-window 20/24
class runtime-subspan 12/14
class runtime-transpose 14/14
class too-long-true-text 3/3
class verbatim-inline-markup 3/9
class verbatim-plain 3/3
class verbatim-typographic-apostrophe 1/2
seed=16159318488230682378 tool_exit=1 wall_s=2.26
QUOTE_REOPEN_MATCH=117/130
```

The mutant receipt records 13 mismatches, all expected `VERBATIM` but actual `ABSENT`: 6 frozen inline-markup items, 1 frozen typographic-apostrophe item, 2 run-time subspans and 4 page windows. Frozen inline-markup failures include S013 item `27c5599c`, `Like the JSON standard a byte order mark (U+FEFF) must NOT be included.`, and S020 item `2cbd5af5`, `The OWL encoding of the PROV Ontology is available here.`

### Restored pristine — counter exit 0

The exact original line was restored and full-file equality with both initial bytes and the lane file was checked before this run.

```sh
timeout --kill-after=5 590 python3 corpus/evidence/round29/c1-count.py --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/falsify/MutInlineBlock/receipt-pristine.json -- python3 tools/quote-reopen.py verify
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
seed=8460833356149027892 tool_exit=1 wall_s=2.21
QUOTE_REOPEN_MATCH=130/130
```

## Restoration evidence and limits

SHA-256 of the entire tool:

| State | SHA-256 |
|---|---|
| Initial scratch and lane | `72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea` |
| Mutant, before and after its run | `7544c989897b7b2dc1b82fa34034afb1be732a59be36dc575f1fbd93bf84c440` |
| Restored, before and after its run | `72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea` |
| Lane at restoration check | `72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea` |

`MutInlineBlock/restoration.json` also records byte-for-byte equality with initial and lane bytes. The frozen counter SHA-256 is `cd50965032278c355f780d357c5672f14840fc218bb1b7dc4adaa6993b5c175d`.

Receipts and exact command/stdout/stderr/exit/hash records are under `.ufo/waves/round-29/falsify/MutInlineBlock/`: `receipt-baseline.json`, `receipt-mutant.json`, `receipt-pristine.json`, `run-baseline.json`, `run-mutant.json`, `run-pristine.json`, `mutant.diff`, and `restoration.json`.

Limits: one specified mutant, one counter run per state, independent fresh seeds and live-page fetches, no held-out fixture additions or broader coverage conclusion. No production code, lane Git index/jj state, counter, claim or fixture was edited. Each detector process group was cleaned up before returning; no server or background job was started. No tools were installed or updated.
