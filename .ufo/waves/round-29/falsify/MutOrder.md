# MutOrder — fetch/length precedence mutation

## Verdict

**HOLDS for the observed pristine C1 predicate; mutant SURVIVED.** Both pristine runs and the mutant printed `QUOTE_REOPEN_MATCH=130/130`. This is a coverage finding, not evidence that the frozen contract permits fetch-before-length ordering, and not a falsification of the landed tool.

Axes: operability, detector discrimination, isolation, exact-byte restoration.

## Scope and mutant

Cloned `/home/vgpnk/Projects/shokunin/chousa-shokunin` into `/fast/scratch/hyaku/chousa-r29/w2/MutOrder/`, with `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` unset. The clone initially followed the newer master, so its scratch-only master was explicitly pinned using:

```sh
timeout 600 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/chousa-r29/w2/MutOrder checkout -B master 30c9d24da1815e01e161ed2f52d5f951005cc2b8
```

Exit 0; `rev-parse HEAD` returned `30c9d24da1815e01e161ed2f52d5f951005cc2b8`.

Applied exactly one behavior change to the scratch tool: retain `NO_SOURCE` first, but fetch and check `UNREACHABLE` before checking `TOO_LONG`.

```diff
--- a/tools/quote-reopen.py
+++ b/tools/quote-reopen.py
@@ -390,9 +390,6 @@
             detail = ("no registry row %s" % source_id if cell is None
                       else "registry row %s has no http(s) URL" % source_id)
             verdict = "NO_SOURCE"
-        elif len(norm(quote).split()) > MAX_WORDS:
-            verdict = "TOO_LONG"
-            detail = "%d words, limit %d" % (len(norm(quote).split()), MAX_WORDS)
         else:
             if url not in cache:
                 cache[url] = fetch_page(url)
@@ -400,6 +397,9 @@
             if text is None:
                 verdict = "UNREACHABLE"
                 detail = detail or "unreachable"
+            elif len(norm(quote).split()) > MAX_WORDS:
+                verdict = "TOO_LONG"
+                detail = "%d words, limit %d" % (len(norm(quote).split()), MAX_WORDS)
             elif found(text, quote):
                 verdict = "VERBATIM"
                 detail = "matched in normalized page text"
```

## Detector and commands

Ran the same frozen, unseeded counter from the clone root on baseline, mutated, and exactly restored bytes. Expected kill: mutant below `130/130` while pristine is `130/130`; a failing baseline would be inconclusive. The requested 900 s outer timeout was reduced to 590 s with a 5 s kill grace to respect the seat's 600 s command ceiling; no detector code, options controlling sampling, or fixture changed.

```sh
timeout --kill-after=5s 590s python3 corpus/evidence/round29/c1-count.py --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/falsify/MutOrder/receipt-baseline.json -- python3 tools/quote-reopen.py verify

timeout --kill-after=5s 590s python3 corpus/evidence/round29/c1-count.py --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/falsify/MutOrder/receipt-mutant.json -- python3 tools/quote-reopen.py verify

timeout --kill-after=5s 590s python3 corpus/evidence/round29/c1-count.py --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/falsify/MutOrder/receipt-pristine.json -- python3 tools/quote-reopen.py verify
```

All three commands exited 0, with empty stderr. Candidate `tool_exit=1` is expected because the fixture includes non-VERBATIM verdicts; counter exit 0 is the scored result. Total elapsed times were respectively 6.58 s, 6.79 s, and 6.74 s.

### Baseline stdout

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
seed=16172387223767840433 tool_exit=1 wall_s=2.23
QUOTE_REOPEN_MATCH=130/130
```

### Mutant stdout

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
seed=6720475085274850445 tool_exit=1 wall_s=2.28
QUOTE_REOPEN_MATCH=130/130
```

### Restored pristine stdout

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
seed=13704728832739408635 tool_exit=1 wall_s=2.34
QUOTE_REOPEN_MATCH=130/130
```

## Coverage limit

The frozen fixture's three `too-long-true-text` items use S008, S019, and S013, which were reachable in these probes. No frozen class combines an over-25-word normalized quote with a registered source whose fetch fails; generated variants and page windows do not add that class.

[INFERENCE] The discriminating class would be **too-long-unreachable-source / length-precedence-over-fetch-error**: a normalized quote longer than 25 words with a valid registry URL whose fetch deterministically fails or returns a rejected status/content type. The contract expects `TOO_LONG`; this mutant would emit `UNREACHABLE`. To yield a scored measurement rather than a counter-side fetch error, that unavailable source must not also be required for the counter's page sampling. This names the absent class only; the frozen claim, counter, fixture, and scale were not changed.

## Restoration evidence and bounds

SHA-256 of `tools/quote-reopen.py`:

| State | SHA-256 |
|---|---|
| Before mutation, scratch | `72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea` |
| Lane source before mutation | `72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea` |
| Mutant | `9049f2a3c660bc4b4d5076a28ffba0f7e345e4a0ef1f399a5811d6ad841d02d3` |
| Restored scratch | `72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea` |
| Lane source at restoration | `72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea` |

Before the final run, direct byte equality against the retained pristine bytes and hash equality against the lane tool both passed (`EXACT_BYTES_RESTORED=True`). The final run also recorded the restored hash. Counter SHA-256 matched in clone and lane before execution: `cd50965032278c355f780d357c5672f14840fc218bb1b7dc4adaa6993b5c175d`.

No lane production files, frozen inputs, lane index, or lane jj state were edited. Only the assigned scratch tool was mutated and restored; lane writes were the three receipts and this report. No subagents, other runtime, background jobs, or test servers were invoked. All foreground subprocesses exited normally. No tools were installed or updated. This probe does not establish behavior for the absent overlap class or for other live-network conditions.
