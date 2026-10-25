# ExecReplayC2 — round 49 wave 2 (FALSIFY): replay C2 + score the staged-copy control

Attacked item: **C2 after-state (`C2=PASS`, `corpus/evidence/round49/measure-after.txt`) and
the staged-copy control (`corpus/evidence/round49/controls/c2-before.txt`).** No production
file written, no counter/predicate/target changed, no fetch, no installs; scratch
`/dev/shm/chousa-r49-ExecReplayC2` deleted.

## Lane state / bytes

```
$ git rev-parse master                                    87e93353d046f2d7e4f0d2f5d3b87b7008a64ef0
$ git diff --stat 4ce61fc59e30b9215514841fe658e96cc998d138 -- .
 LOG.md | 11 ++++   corpus/evidence/round49/measure-after.txt | 103 ++++++++
```
Tracked code = `4ce61fc5`; only `87e9335` (LOG.md, measure-after) on top. Counter bytes equal
the recorded ones (`c2-count.py 9d2fb3806e36…`, `inference-ground.py fa2b4eb5fc29…`,
`build-spans.py 02b2dc83de1f…`).

## Replay — 3/3 byte-identical to measure-after.txt

```
$ python3 corpus/evidence/round49/c2-count.py
ENTRIES=2/2 ; BOUND=8/9 (min 7) REFUSED=1 ; BOUND_IDS=S096..S103 ; REF_ID_UNBOUND=0
QUOTE_ROWS=28 ON_BOUND=28/28 ; SPAN_IDS=8/8 ; QUOTES_IN_SPAN=28/28 ; QUOTES_IN_ENTRY=28/28
QUOTES_IN_LESSON=28/28 ; QUOTE_SHORT=28/28 ; SPAN_CONTEXT=28/28 ; CAPTURE_BOUND=28/28
ANCHOR_BOUND=8/8 ; INFERENCE_GROUNDED=2/2 ; QUARANTINE_VERDICTS=5/5 (S082,S084,S086,S095,S096)
QUARANTINE_BLOCKED_ADOPTED=0 ; C2=PASS ; exit=0
$ python3 corpus/evidence/round49/c2-count.py --lane-only     # identical, CAPTURE_BOUND=skipped, C2=PASS, exit=0
$ python3 corpus/evidence/round49/build-spans.py --check      # SPANS_ROWS=28 STALE=0, exit=0
```
Mechanical block-by-block comparison with the recorded file: all three `IDENTICAL`.
`git status --porcelain corpus/evidence/round49/` empty after the runs (no side-writes).

## Independent legs (own code, not the counter's helpers)

```
INDEPENDENT_CAPTURE_SLICE 28/28 forms {'.txt': 20, '.raw': 8}
S101-1 span[:60] = '11.6为便于文献的统计和期刊评价，确定文献的检索范围，提高检索结果的适用性，…'
S096-1 span[:60] = 'ている論文が引用している文献です。 \n \n\n \n 被引用文献 \n 現在表示している…'
```
Every span file equals `form[offset:offset+len(span)]` byte-for-byte, quote occurs exactly
once in its capture, `len(span)>len(quote)`. Anchors (`corpus/SOURCES.md:106-113` col 6) vs
`offset+span.find(quote)`:
`S096 [3599,3707,3752] S097 [2607,2760] S098 [29482,29641,29672,29749,29775]
S099 [1235,1483,1694] S100 [1296,1431,2861] S101 [11170,11205,11993,12161,34374]
S102 [13260,13514,16123] S103 [892,953,959,3175]` — all `OK`.
URL→row uniqueness over the whole Registry:
`nii 1 ['S096'] · jstage-pub 1 ['S097'] · jstage-faq 1 ['S098'] · ncpssd 0 [] ·
eric 1 ['S099'] · zcmu 1 ['S100'] · hit 1 ['S101'] · toho 1 ['S102'] · um 1 ['S103']`.
Rows: 11 cells, `mined`/`2026-10-25`/used-by = citing entry. Refusal once
(`corpus/lessons/round-49.md:131`); no `source:` line for it (8 `^source:` lines, 4+4). Both
entries exit 0 under `tools/inference-ground.py` run directly. Register verdict completeness
without the counter filter: `absent-defect-register.md` lines 39,40,41,45,46 are the only
theme-URL rows = the counter's five; all read `absent-as-written`
(`corpus/lessons/round-49.md:108,112,115,119,121`), none fabricated/unverifiable.

## Staged-copy control — fails

Scratch root: lane `SOURCES.md` + `tools/inference-ground.py` + staged
`aggregator-vs-source-r36.md` (`29b9ad256f30…`) and `citation-count-semantics-r37.md`
(`68a8db1a34fd…`) from `/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/`
(lane copies differ: `e5b3cdaf82e7…`, `19c27ccb6227…`). With the **pre-adoption** registry
(`git show 414a2ec6:corpus/SOURCES.md`, 95 rows) the recorded line reproduces exactly:
`ENTRIES=2/2 ; BOUND=0/9 ; REFUSED=0 ; REF_ID_UNBOUND=11 ; QUOTE_ROWS=0 ; CAPTURE_BOUND=0/0 ;
INFERENCE_GROUNDED=0/2 ; QUARANTINE_VERDICTS=0/5 ; C2=FAIL ; exit=1`.
With **today's** `SOURCES.md` the same copy still fails: `BOUND=4/9 REFUSED=0
BOUND_IDS=S100,S101,S102,S103 REF_ID_UNBOUND=7 … C2=FAIL exit=1`. Calibration: the recorded
`BOUND=0/9 REF_ID_UNBOUND=11` is reproducible only against the pre-adoption registry; the four
CCS staged ids `S100–S103` now coincide with the adopted lane ids, so an unchanged copy binds
4 of 9 — still a fail (4+0≠9, 7 unbound tokens, no spans, no grounding). Control conclusion
holds in both roots.

## Post-freeze span-builder change — judged

Frozen builder (`git show fe740e7:…/build-spans.py`) replayed on the committed `quotes.tsv`:
`CAPTURE_BOUND=21/28`, `C2=FAIL`, exit 1; `frozen fails 7 ['S100','S101'] ['raw']`, current
builder `fails 0` — the erratum's number reproduces. Frozen-built vs committed `spans.tsv`
differs in **offsets only** (S100 1216→1296, 1351→1423; S101 11125→11166, 11090→11166,
11913→11945, 34294→34370); every quote string identical. CR clip keeps each span an exact
slice with `len(span)>len(quote)`. S100 arithmetic: `spans/S100-2.txt` 48 chars,
`find(quote)=8`, `1423+8=1431` = `corpus/SOURCES.md:110` cell — erratum accurate. The
shortened S100 quote is the paragraph body; the entry still carries the full paragraph
(`citation-count-semantics-r37.md:18,44`). Judgement: read-side mismatch repair against the
frozen universal-newline read; counter, target, kill rule, document set and verdicts
untouched, and disclosed — C2's after-state stands on it.

## New limit found (erratum omits it; after-state unaffected)

`CAPTURE_BOUND` compares `form[o:o+len(span)] == span`, so it is **prefix tolerant**. All 28
span files trimmed to `quote+1` char in a scratch root:
`QUOTES_IN_SPAN=28/28 SPAN_CONTEXT=28/28 CAPTURE_BOUND=28/28 C2=PASS exit=0`, while
`build-spans.py --check` prints `SPANS_ROWS=28 STALE=26` exit 1. Faithful to the frozen
wording (`claims.md` records no span extent), so it is a limit of the rule, not a counter bug;
the 80-char context is builder-enforced and the committed manifest satisfies it (`STALE=0`).
Confirmed disclosed limits: fabricated digest passes `--lane-only`, fails full mode
(`CAPTURE_BOUND=27/28 C2=FAIL`); a 13-cell registry row is not a URL hit. Operability: the
verdict leg reads host-side `absent-defect-register.md` (shape-only, not run) — a host edit
could move `QUARANTINE_VERDICTS` with no lane byte change.

## Risks / blockers

None blocking; no installs; scratch removed. C1 (`c1-count.py`) not run by this seat.

VERDICT: C2 after-state replay + staged-copy control — holds — all three replays are byte-identical to measure-after.txt, every leg reproduces independently (28/28 capture slices, 8 anchors, one row per URL, 5/5 verdicts), the staged copy fails under both registry versions, and the post-freeze builder change reproduces 21/28→28/28 without touching quotes, target or counter.
