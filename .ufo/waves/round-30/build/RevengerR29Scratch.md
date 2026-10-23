# Round 30 W1 — RevengerR29Scratch: inventory of round-29 scratch

2026-10-23. Leaf seat; no subagents, no background jobs, no network, no tool installs (none needed). Read-only on `/fast/scratch/hyaku/chousa-r29/`; writes only to my build dir and `/fast/scratch/hyaku/chousa-r30/w1/RevengerR29Scratch/` (work files `raw.tsv`, `committed-refs.txt`, `seat-a.json`).

## Deliverable
`inventory.tsv` — 24,613 lines (header + 24,612 rows), columns `path, size, sha256, seat, class`, absolute paths.

## What I did
1. Walked the whole round-29 scratch tree: 24,612 files, 293,537,873 B of file content (`du -sb` 293,537,951 including dirs). sha256 of every file; zero read errors.
2. Seat attribution from `.ufo/waves/round-29/**/*.md`: all 18 `w1/<Seat>/` dirs match build-wave report stems, all 23 `w2/<Seat>/` dirs match falsify-wave stems; `moved-page-bodies/{build,falsify}/<Seat>/` keeps its source seat; `ctl-id/` → CtlIdKeyed (`controls/CtlIdKeyed/report.md:125` "Scratch counter: `/fast/scratch/hyaku/chousa-r29/ctl-id/corpus/evidence/round29/c1-count.py`"; `:202` "cmp ... returned 0 with no output. Thus restoration was byte-exact"). `CriticPredicate` has a `w1/` dir but no report; it appears only in `build-spec.json`, `build-dispatch.json`, `build/swarm-registry.json` (assigned; report never landed).
3. Class rules, applied in order:
   - **(b) page bodies (third-party text; keep out of the lane):** everything under `pages/` and `moved-page-bodies/`; suffixes `.html .body .wire .pdf .eml .norm.txt`; `S0xx.raw` and `S0xx.independent/counter.txt`; content sniff on other unknown suffixes.
   - **(c) recoverable from the lane or throwaway:** byte-identical to a blob in lane git history (`git rev-list --objects --all`, 3,098 object ids at pass time; 9,096 files matched — the lane already holds those bytes, even for copies a report cites); the 9 embedded `.git` clones (`w1/ExecToolB/clone`, `w1/ExecTool/lane`, `w1/MutateCounter`, `w2/{MutBoundary,MutCasefold,MutInlineBlock,MutOrder,MutQuoteMap,MutSkipScript}`); `__pycache__`, `.pyc`; everything unreferenced.
   - **(a) referenced by a committed claim/report and needed to re-check it:** exact path or parent dir cited in `git grep chousa-r29 HEAD` (126 distinct cited strings → 103 exact file paths + 14 dir prefixes after dropping bare `w1`/`w2` tops), or its sha256 appears in committed wave/receipt text (1,171 64-hex tokens at HEAD) — and not lane-history-identical, not page text. `.ufo` is git-tracked (`git ls-files .ufo | wc -l` → 1,239), so wave reports are committed references.

## Result

| class | files | bytes |
|---|---|---|
| (a) keep for re-check | 24 | 898,361 |
| (b) page bodies | 384 | ~89.6 MB |
| (c) throwaway / lane-recoverable | 24,204 | ~202.7 MB |

Class (a), paths relative to `/fast/scratch/hyaku/chousa-r29/`:
`w2/AttackRowS047/probe.py`; `w2/CriticClaimDesign/audit_receipts.py`, `snapshots.json`; `w2/CriticHeadOmission/{audit_cached,head_sweep,replay_cli}.py`; `w1/ExecTool/receipt-v3-run{2,3,4,5,6,7}.json` (runs 1 and 8 are committed, 2-7 exist only here); `w2/HeldOut04/blind.py`; `w2/HeldOut10/blind_extract.py`; `w1/MutateBlockInline/extractor.py`; `w1/MutateCounter/.mutation-probes/{control,probe}.py`; `w2/OfflineConformance/extra-conformance.py`, `redirect-target.txt`; `w1/ReviewFixtureAbsentEdits/checker.py`; `w1/ReviewFixtureAbsentSplice/check.py`; `w1/ScoutGateQuotes/{inventory.py,rows.json}`; `w2/SimplifierTool/lane/tools/quote-reopen.py` (the simplifier's candidate copy, 15,891 B vs 16,423 landed).

Class (b): `moved-page-bodies/` 280 (CriticHeadOmission 102, DiffToolB 176, CriticRuntimeVariants `checked-variants.jsonl`, others); `pages/` 10 — every one sha256-identical to a `moved-page-bodies/falsify/CriticHeadOmission` body (staging duplicates); in-clone payloads: `w2/ReviewKnowledge/wicg.html`, `w2/HeldOut11/prov-dm.html`, `w2/HeldOut04/s011.pdf` (`file`: "PDF document, version 1.7, 21 page(s)"), `w2/HeldOut10/s037.pdf`, CriticRuntimeVariants cache 25 (`S0xx.raw` binary captures, `S0xx.independent/counter.txt` normalized page text — sample `S002.counter.txt` head: "AboutSignatoriesAssessorsComplaints ... Code of Principles ..."), ReviewFixture `*.norm.txt` 16+5+4+4, ExecToolSelfAudit 8, MutateBlockInline 8, HeldOut 02/04/07/09/10 fixtures. Nothing unique is lost: committed receipts carry the hashes.

Class (c): 9,096 lane-history-identical copies (clone worktrees of `corpus/`, `.ufo/`, `tools/`; e.g. the largest, `build-spawn-result.json` 353,425 B × 9 clones, all identical to a round-26 blob), ~15,000 `.git` object/pack files, caches. History spot-checks confirm several cited scratch copies were re-committed into the lane this round: `git log --all --find-object` puts `quote-reopen-offline-test.py` bytes in `2ed2d27`, `network_guard.py` in `0dc6e81` ("round-30: after receipts on 49b2aa30 ..."), and the DiffToolB mutated tool bytes in `33dd643` ("round-30: C2 fetch layer ... ExecC2Fetch") — so "(c) recoverable from the lane" is current, not merely historical.

Unattributed orphans (seat `unattributed`, 13 files):
- `census.sh` (1,180 B): a SOURCES.md census script; zero lane references to that path in `.ufo/waves/round-29`, `round-30`, `corpus`, `LOG.md`, `SCORECARD.md`; byte-different from the fleet `scripts/sources-census.sh`. [INFERENCE] written by the round-29 wrap-up, not by a seat.
- `v2-before-2901.json`, `v2-before-2902.json`: receipts, schema `chousa-r29-c1-receipt/v1`, `counter_sha256` `574ffcad…` (the round-29 v1 counter cited in CtlAlwaysVerbatim receipts), seeds 2901/2902, `tool_exit` 2, stderr "can't open file '.../tools/quote-reopen.py'" — pre-tool baseline attempts; `cmp` against committed `.ufo/waves/round-29/controls/before-do-nothing.json` differs. No lane file cites them; superseded by the committed before receipts → throwaway.
- `pages/` (10 files): no lane reference; content-identical subset of CriticHeadOmission fetches. [INFERENCE] staging copies.

## Verdict (scoped to this item)
- No round-29 scratch file is an input to the round-30 counters or harness (both generate every item at run time; no committed byte holds an item, per `corpus/evidence/round30/claims.md`), so nothing here blocks C1 or C2. If the L1 wants offline re-checkability of round-29 reports, only the 24 class (a) files carry unique value; all 384 class (b) files are third-party page payloads that must not enter the lane; class (c) is droppable.
- D1 discipline kept: nothing in this report calls any run network-live; payloads are described only as captured artifacts of round-29 seat runs.

## Limits
- The lane's git state moved during the pass (round-30 build commits landing while I ran); the history-blob set is from my pass moment. Labels stay correct as the lane only grows.
- `moved-page-bodies/` seat names are inherited from subdirectories; the move itself is described in no round-29 report — [INFERENCE] wrap-up action by the L1.
- Commands (all `timeout`-bounded ≤ 600 s): `find … -type f | wc -l` → 24,612; `du -sb` → 293,537,951; `git grep -c "chousa-r29" HEAD` (207 tracked files with references); hashing and classification in one Python pass; `git log --all --find-object=…` spot-checks; `file`, `cmp`, `head` samples as quoted above.
