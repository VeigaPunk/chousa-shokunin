# MutQuoteMap — typographic quote-map mutation

**Scoped verdict: HOLDS for this attack; mutant KILLED.** The pristine baseline and restored tool each printed `QUOTE_REOPEN_MATCH=130/130`; removing only typographic quotation-mark mappings printed `QUOTE_REOPEN_MATCH=126/130`. This is mutation-detector evidence, not an overall correctness judgment or a falsification of pristine C1.

## Axes and scope

Axes: operability (C1), detector sensitivity, exact restoration/lane isolation. One mutant, in `/fast/scratch/hyaku/chousa-r29/w2/MutQuoteMap/` only. The frozen counter, claims and fixture were not edited. No other mutant, runtime, subagent or production change was attempted.

The local clone initially checked out `master` at `b18b3ec9d8a01f966dd81991615bac27df6d66a1`. Its scratch-only branch was pinned with `git -C /fast/scratch/hyaku/chousa-r29/w2/MutQuoteMap checkout -B master 30c9d24da1815e01e161ed2f52d5f951005cc2b8` (exit 0); `rev-parse HEAD` returned the assigned commit. Clone, checkout and hash command outputs are retained in the session; probe commands, hashes, diff and full detector outputs are retained in `MutQuoteMap/probe-evidence.json`.

## Mutant and expected detector

Deleted the eight U+2018–U+201F-to-ASCII quotation-mark entries from `QMAP`. Kept Unicode NFKC, soft/zero-width deletion, whitespace normalization and every other behavior unchanged. Expected the existing `verbatim-typographic-apostrophe` class to miss quotes using ASCII apostrophes where the live page uses U+2019, reducing the frozen score below 130/130.

Actual scratch diff (captured before restoration, command exit 0):

```diff
diff --git i/tools/quote-reopen.py w/tools/quote-reopen.py
index be0ce00..89de053 100755
--- i/tools/quote-reopen.py
+++ w/tools/quote-reopen.py
@@ -61,9 +61,7 @@ BLOCK = {"p", "div", "li", "ul", "ol", "table", "tr", "td", "th", "h1", "h2", "h
          "br", "section", "article", "header", "footer", "nav", "pre", "blockquote", "dt", "dd", "dl",
          "figure", "figcaption", "hr", "main", "aside"}
 # Typographic quotation marks fold to their ASCII form; soft and zero-width marks vanish.
-QMAP = str.maketrans({"\u2018": "'", "\u2019": "'", "\u201a": "'", "\u201b": "'",
-                      "\u201c": '"', "\u201d": '"', "\u201e": '"', "\u201f": '"',
-                      "\u00ad": None, "\u200b": None, "\u200c": None, "\u200d": None, "\ufeff": None})
+QMAP = str.maketrans({"\u00ad": None, "\u200b": None, "\u200c": None, "\u200d": None, "\ufeff": None})
 URL_RE = re.compile(r"https?://\S+")
```

## Detector commands and outputs

All runs used the same bounded detector from the pinned clone root, without a supplied seed. The wrapper was `timeout --signal=TERM --kill-after=5 570`, not the requested 900-second wrapper, because the lane command limit is at most 600 seconds. No run reached that bound. `TMPDIR` was the clone's `.tmp` directory and `PYTHONDONTWRITEBYTECODE=1`; Git environment overrides were unset. Each run drew its own fresh seed.

### Before mutation — pristine baseline

Command: `timeout --signal=TERM --kill-after=5 570 python3 corpus/evidence/round29/c1-count.py --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/falsify/MutQuoteMap/receipt-baseline.json -- python3 tools/quote-reopen.py verify`

Counter exit: 0; stderr: empty.

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
seed=16812408728131377606 tool_exit=1 wall_s=2.36
QUOTE_REOPEN_MATCH=130/130
```

### Mutant

Command: `timeout --signal=TERM --kill-after=5 570 python3 corpus/evidence/round29/c1-count.py --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/falsify/MutQuoteMap/receipt-mutant.json -- python3 tools/quote-reopen.py verify`

Counter exit: 1; stderr: empty.

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
class runtime-page-window 23/24
class runtime-subspan 13/14
class runtime-transpose 14/14
class too-long-true-text 3/3
class verbatim-inline-markup 9/9
class verbatim-plain 3/3
class verbatim-typographic-apostrophe 0/2
seed=15948892071251740581 tool_exit=1 wall_s=2.23
QUOTE_REOPEN_MATCH=126/130
```

All 4 mutant mismatches were expected VERBATIM but observed ABSENT:

| Source | Origin / kind | Evidence |
|---|---|---|
| S003 | `c258f7c8` / frozen | `Since 2017, we've been teaching students with something called the Four Moves.` |
| S044 | `3406c3dc` / frozen | `On Unix and Windows, return the argument with an initial component of ~ or ~user replaced by that user's home directory.` |
| S044 | `3406c3dc` / runtime-subspan | `Unix and Windows, return the argument with an initial component of ~ or ~user replaced by that user's` |
| S003 | `page:S003` / runtime-page-window | `One method he's devised is known as SIFT,` |

### Restored pristine

Command: `timeout --signal=TERM --kill-after=5 570 python3 corpus/evidence/round29/c1-count.py --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/falsify/MutQuoteMap/receipt-pristine.json -- python3 tools/quote-reopen.py verify`

Counter exit: 0; stderr: empty.

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
seed=1031361805420515392 tool_exit=1 wall_s=2.25
QUOTE_REOPEN_MATCH=130/130
```

The candidate's `tool_exit=1` in every run is distinct from the counter exit: the tool contract returns 1 when its item batch includes non-VERBATIM verdicts; the fixture intentionally includes such items.

Receipts: `MutQuoteMap/receipt-baseline.json`, `MutQuoteMap/receipt-mutant.json`, `MutQuoteMap/receipt-pristine.json`. All name frozen counter SHA-256 `cd50965032278c355f780d357c5672f14840fc218bb1b7dc4adaa6993b5c175d`.

## Restoration and no-harm evidence

Restoration ran in a `finally` block immediately after the mutant detector, using `timeout --signal=TERM --kill-after=5 5 git -C /fast/scratch/hyaku/chousa-r29/w2/MutQuoteMap restore --source=HEAD --worktree -- tools/quote-reopen.py`; exit 0. Before the restored detector, `sha256sum` returned the same exact SHA-256 for the scratch file and the lane production file:

| State | SHA-256 |
|---|---|
| Lane and scratch before mutation | `72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea` |
| Mutant scratch file | `242c48efb880836088329b739f8df3f0cfb26c209a1e34d80dc0353d38e93e02` |
| Restored scratch file and lane file | `72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea` |

All commands were bounded by `timeout` at 570 seconds or less. Started subprocesses had isolated process groups; the wrapper attempted whole-group SIGKILL cleanup in `finally` after each command, ignoring only already-absent groups. No background job or loopback server was started. No Git/JJ write command ran in the lane or fleet repository. Lane writes were restricted to this report and the assigned evidence directory. Tools installed or updated: none.

## Limits

The 2 existing frozen typographic-apostrophe fixtures killed this mutant independently of the extra randomized misses. This probe does not individually test every deleted quotation-mark mapping (for example, curly double quotes). Live source content and randomized page windows may differ between runs. No fixture changes or counter re-scaling are proposed.
