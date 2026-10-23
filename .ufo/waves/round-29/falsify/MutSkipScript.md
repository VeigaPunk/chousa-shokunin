# MutSkipScript — round 29 C1 mutation probe

## Verdict and scope

**Mutant: SURVIVED. Frozen C1 predicate: HOLDS in the pristine baseline and restored run.** The same counter also accepted the deliberately defective mutant at `130/130`. This is a coverage finding, not a demonstrated defect in the landed implementation and not permission to alter the frozen claim, counter or fixture.

Axes: operability; detector sensitivity to hidden HTML content; isolated, byte-exact restoration.

## Isolation and one mutation

Local clone: `/fast/scratch/hyaku/chousa-r29/w2/MutSkipScript/`.

The clone initially inherited a newer `master` (`b18b3ec9d8a01f966dd81991615bac27df6d66a1`), so only the scratch branch was reset to the assigned landed commit. Commands, all exit `0`:

```sh
timeout 30 mkdir -p /fast/scratch/hyaku/chousa-r29/w2
timeout 90 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --no-hardlinks /home/vgpnk/Projects/shokunin/chousa-shokunin /fast/scratch/hyaku/chousa-r29/w2/MutSkipScript
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/chousa-r29/w2/MutSkipScript checkout master
# Remaining commands run from the clone root:
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git checkout -B master 30c9d24da1815e01e161ed2f52d5f951005cc2b8
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git rev-parse HEAD
# 30c9d24da1815e01e161ed2f52d5f951005cc2b8
```

Exactly one behavior-bearing line was changed, in scratch only:

```diff
--- i/tools/quote-reopen.py
+++ w/tools/quote-reopen.py
@@ -55,7 +55,7 @@
 MAX_WORDS = 25
 
 # Content of these elements is dropped, and comments are dropped.
-SKIP = {"script", "style", "noscript", "template", "head"}
+SKIP = {"noscript", "template"}
 # These elements emit one space at start and at end; every other element emits nothing.
 BLOCK = {"p", "div", "li", "ul", "ol", "table", "tr", "td", "th", "h1", "h2", "h3", "h4", "h5", "h6",
          "br", "section", "article", "header", "footer", "nav", "pre", "blockquote", "dt", "dd", "dl",
```

The mutant stops suppressing `script`, `style` and `head` text while retaining suppression of `noscript` and `template`. This contradicts the frozen HTML extraction contract at `corpus/evidence/round29/claims.md:103-105`.

## Detector and actual runs

Expected detector: the unchanged, unseeded `corpus/evidence/round29/c1-count.py` running `python3 tools/quote-reopen.py verify` from the pinned clone root. Kill requires mutant `< 130/130` and pristine `130/130`. A failing pristine baseline would make attribution inconclusive; the baseline here passed.

All runs used `TMPDIR=/fast/scratch/hyaku/chousa-r29/w2/MutSkipScript/.probe-tmp` and `PYTHONDONTWRITEBYTECODE=1`; Git override variables were removed. No seed was supplied. The requested outer `timeout 900` was reduced to `timeout --kill-after=5s 580s` to respect the assignment's command bound of at most `600 s`; no run approached that deadline.

Exact commands, in execution order:

```sh
timeout --kill-after=5s 580s python3 corpus/evidence/round29/c1-count.py --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/falsify/MutSkipScript/receipt-baseline.json -- python3 tools/quote-reopen.py verify
timeout --kill-after=5s 580s python3 corpus/evidence/round29/c1-count.py --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/falsify/MutSkipScript/receipt-mutant.json -- python3 tools/quote-reopen.py verify
# The original line was restored and its SHA-256 checked before this run:
timeout --kill-after=5s 580s python3 corpus/evidence/round29/c1-count.py --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/falsify/MutSkipScript/receipt-pristine.json -- python3 tools/quote-reopen.py verify
```

| Bytes | Counter exit | Tool exit | Supervisor elapsed | Counter output |
|---|---:|---:|---:|---|
| Pristine baseline | 0 | 1 | 6.638 s | `QUOTE_REOPEN_MATCH=130/130` |
| Mutant | 0 | 1 | 6.673 s | `QUOTE_REOPEN_MATCH=130/130` |
| Restored pristine | 0 | 1 | 6.544 s | `QUOTE_REOPEN_MATCH=130/130` |

The candidate's exit `1` is expected with negative items; the counter exits `0` because every verdict matches its label. Stderr was empty in all three runs.

### Mutant stdout (complete)

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
seed=5949113470864853822 tool_exit=1 wall_s=2.3
QUOTE_REOPEN_MATCH=130/130
```

### Restored pristine stdout (complete)

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
seed=17239294528927159831 tool_exit=1 wall_s=2.21
QUOTE_REOPEN_MATCH=130/130
```

Baseline stdout had the same class counts, followed by:

```text
seed=6552652943291673613 tool_exit=1 wall_s=2.26
QUOTE_REOPEN_MATCH=130/130
```

## Coverage finding and limits

[INFERENCE] A discriminating fixture class would be `absent-hidden-element-only`: a nonempty quote of at most `25` words, present at valid matching boundaries only inside `script`, `style` or `head` in an allowed source page, and absent from that page's correctly extracted visible text. The contract labels it `ABSENT`; this mutant would report `VERBATIM`. This describes the missing adversarial class, not a proposed change to the frozen fixture; no such fixture or extra probe was created.

The frozen classes listed in `labels.tsv` do not explicitly include this class. Runtime negatives are transpositions of visible-text windows or existing fixture quotes, not deliberately sampled hidden-only content. This single surviving run does not establish survival for every fresh seed or future page version. The three runs used different fresh seeds and live pages; their individual JSON receipts retain the cases and labels.

## Restoration and frozen-input evidence

`timeout 30 sha256sum tools/quote-reopen.py /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/quote-reopen.py` exited `0` before mutation and again after restoration, before the final detector run. Both times scratch and lane tool hashes were identical:

```text
pristine-before  72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea
mutant           92b404eb0813cf109414c9b1ef26bcbb91c2a51020a761e9d44dc1d3913a5550
restored-after   72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea
lane-tool        72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea
```

Frozen counter and fixture SHA-256 values were recorded before mutation and after restoration; they were unchanged:

```text
cd50965032278c355f780d357c5672f14840fc218bb1b7dc4adaa6993b5c175d  corpus/evidence/round29/c1-count.py
e6305beba9563fe4d37430019831610ddf7a5adf1e35de60869e3b764f939bcc  corpus/fixtures/quote-reopen-r29/items.tsv
dda1b3768f6f187736a77e5bce094b41822d8574e4798886d00964267343c7a9  corpus/fixtures/quote-reopen-r29/labels.tsv
```

The restored scratch claim and lane claim also had identical SHA-256 `19ea5fbe2d52e42eff8c96096f543b818c37cf773fdfd22af6011fbf1cf47cfc`. No claim, counter, fixture, production source, lane index or lane jj state was edited. The only lane writes were this scoped report and the three receipts in `falsify/MutSkipScript/`.

Each counter ran synchronously in its own process group with a bounded supervisor. The supervisor attempted process-group `SIGKILL` cleanup in `finally` after each run, ignoring only an already-absent process group. No background job, test server or service was started. No tools were installed or updated.
