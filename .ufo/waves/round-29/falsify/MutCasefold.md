# MutCasefold — round 29 C1 mutation probe

**Scoped verdict: HOLDS for the measured frozen C1 predicate; mutant SURVIVED.** Both pristine runs and the case-insensitive mutant printed `QUOTE_REOPEN_MATCH=130/130`. This is a case-sensitivity coverage finding, not evidence that the pristine implementation violates the contract. The frozen claim, counter and fixtures were not changed or re-scaled.

Axes: operability of the frozen command; detector discrimination of case-sensitive matching; exact-byte restoration and lane isolation.

## Mutation and expected detector

The sole source mutation was in `found()` in the isolated clone's `tools/quote-reopen.py`: casefold the normalized quote and page text before the existing boundary-aware search. This deliberately contradicts `corpus/evidence/round29/claims.md` lines 114–117, which require case-sensitive matching. Boundary checks, normalization, fetching and verdict handling were otherwise unchanged.

Actual diff (also saved as `MutCasefold/mutant.diff`):

```diff
diff --git i/tools/quote-reopen.py w/tools/quote-reopen.py
index be0ce00..7d884bd 100755
--- i/tools/quote-reopen.py
+++ w/tools/quote-reopen.py
@@ -111,7 +111,8 @@ def html_to_text(doc):
 
 def found(text, quote):
     """True iff the normalized quote occurs in the normalized text at a non-alphanumeric boundary."""
-    q = norm(quote)
+    q = norm(quote).casefold()
+    text = text.casefold()
     if not q:
         return False
     i = 0
```

Expected detector: the unchanged, unseeded `c1-count.py` wrapping `python3 tools/quote-reopen.py verify`. Assigned kill rule: mutant below 130/130 and restored pristine at 130/130. The initial pristine run additionally establishes that a baseline failure is not being counted as a kill.

## Isolation and commands

Scratch: `/fast/scratch/hyaku/chousa-r29/w2/MutCasefold/`.

Cloned with `timeout 60 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --no-checkout /home/vgpnk/Projects/shokunin/chousa-shokunin /fast/scratch/hyaku/chousa-r29/w2/MutCasefold`, then pinned scratch master with `timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/chousa-r29/w2/MutCasefold checkout -B master 30c9d24da1815e01e161ed2f52d5f951005cc2b8`. Both exited 0; read-only `git rev-parse HEAD` returned that exact revision. The lane's current master/HEAD was `b18b3ec9d8a01f966dd81991615bac27df6d66a1`; the clone was explicitly pinned rather than assuming that newer master was the assigned revision.

From the scratch root, each phase executed this exact command with its respective receipt basename:

```sh
timeout --signal=TERM --kill-after=5s 590 python3 corpus/evidence/round29/c1-count.py --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/falsify/MutCasefold/RECEIPT -- python3 tools/quote-reopen.py verify
```

`RECEIPT` was `receipt-baseline.json`, `receipt-mutant.json`, then `receipt-pristine.json`. No seed was supplied. The 590 s bound replaces the requested 900 s wrapper to obey the lane's mandatory command bound of at most 600 s; no run approached the bound. `TMPDIR` was the scratch `.probe-tmp/`, `PYTHONDONTWRITEBYTECODE=1`, and Git environment overrides were removed. Each foreground subprocess was waited for, and its isolated process group received a cleanup SIGKILL attempt before returning. No background job or server was launched.

| Phase | Counter exit | Counter output | Counter-selected seed | Candidate exit | Whole run seconds |
|---|---:|---|---:|---:|---:|
| Initial pristine | 0 | `QUOTE_REOPEN_MATCH=130/130` | 3269687085777028217 | 1 | 6.626 |
| Casefold mutant | 0 | `QUOTE_REOPEN_MATCH=130/130` | 13068190470962577386 | 1 | 6.584 |
| Restored pristine | 0 | `QUOTE_REOPEN_MATCH=130/130` | 11137935564475480489 | 1 | 6.695 |

Candidate exit 1 is expected because the counter includes negative-label items. All three counter stderr streams were empty; all three actual receipts have `predicate_holds: true`, `match: 130`, `total: 130`, and 130 case records.

### Mutant stdout, complete

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
seed=13068190470962577386 tool_exit=1 wall_s=2.2
QUOTE_REOPEN_MATCH=130/130
```

### Restored-pristine stdout, complete

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
seed=11137935564475480489 tool_exit=1 wall_s=2.26
QUOTE_REOPEN_MATCH=130/130
```

Initial-pristine stdout had the same class scores and ended with `seed=3269687085777028217 tool_exit=1 wall_s=2.26` and `QUOTE_REOPEN_MATCH=130/130`. Full stdout, stderr and execution metadata for each phase are in `MutCasefold/{baseline,mutant,pristine}.{stdout.txt,stderr.txt,run.json}` beside the three receipts.

## Restoration evidence

Only the scratch tool was edited. The two-line mutant was reversed before the restored-pristine run. `timeout 20 sha256sum ...` and `timeout 20 cmp -- tools/quote-reopen.py /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/quote-reopen.py` were run both immediately after restoration and after the restored measurement. Both `cmp` checks exited 0 with no output.

| Tool bytes | SHA-256 |
|---|---|
| Initial scratch pristine | `72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea` |
| Scratch mutant | `c19f927aeee2dd1ec68b074049886dc810cfc6597869b9881716f8d4fc1527e1` |
| Restored scratch, before and after final run | `72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea` |
| Lane tool, before/mutant/after observations | `72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea` |

The following scratch hashes matched their initial pristine and lane-input hashes before and after the experiment:

```text
cd50965032278c355f780d357c5672f14840fc218bb1b7dc4adaa6993b5c175d  corpus/evidence/round29/c1-count.py
19ea5fbe2d52e42eff8c96096f543b818c37cf773fdfd22af6011fbf1cf47cfc  corpus/evidence/round29/claims.md
e6305beba9563fe4d37430019831610ddf7a5adf1e35de60869e3b764f939bcc  corpus/fixtures/quote-reopen-r29/items.tsv
dda1b3768f6f187736a77e5bce094b41822d8574e4798886d00964267343c7a9  corpus/fixtures/quote-reopen-r29/labels.tsv
d8aa0454b50bbe229f255885c970660540f8ecf5bac633ec136165b3425819be  corpus/SOURCES.md
```

## Finding and limits

The mutant survived the assigned kill rule. The detector accepted this forbidden matching behavior in the measured run, while both pristine controls passed.

[INFERENCE] A discriminating fixture class would be **absent-case-only-edit**: change only letter case in an otherwise present, boundary-valid quote, confirm that changed-case text is absent under the frozen case-sensitive reference match but present after casefolding, and label it `ABSENT`. This mutant would answer `VERBATIM`. This identifies missing coverage; no fixture, label, predicate or contract was edited, and no additional held-out probe was run.

The runs use independent fresh seeds and live pages, not identical generated items. These observations do not establish behavior for every future seed or page revision, do not show a production casefold defect, and do not falsify C1's literal 130/130 predicate on the tested pristine bytes. No integration or runtime judgment was performed. No tool was installed or updated. The shell tool reported that requested PTY support was unavailable during cloning; that tooling discrepancy was reported through `xd://report_issue`, and the successful clone/checkouts are grounded in their command output and pinned revision.
