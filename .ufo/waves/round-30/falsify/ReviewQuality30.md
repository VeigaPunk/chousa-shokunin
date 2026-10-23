VERDICT: defect — QUALITY 26, 27, 28 and 29 each reproduce the "shown able to fail" evidence they cite (pass); 2 defects: `rerun-check.py` exits 0 on receipts that contradict the stated result, and the criterion-29 control receipts do not pin the code they ran

All commands ran from the lane root at tip `a9d3a05a` unless a scratch path is named. Hashes checked first with `sha256sum`: `c1-count.py` 5b312d84…9d6e6, `c2-count.py` 0a59e373…f88f, `qr_harness.py` e2be0dd1…50d4, `tools/quote-reopen.py` 47a657e7…1201 (all match the frozen values). `corpus/evidence/round30/rerun-check.py` and `.ufo/waves/round-30/build/ExecRerunCount/rerun-check.py` share SHA-256 7f36e65b…acd9. New receipts are in `.ufo/waves/round-30/falsify/ReviewQuality30/`. All counter runs were loopback only. No network fetch was made.

## Per criterion

| # | result | key output |
|---|---|---|
| 26 | pass | `grep -nwi live corpus/lessons/round-29.md`: exit 0, 5 lines (1, 6, 78, 96, 98). `corpus/knowledge/quote-reopen-r30.md`: exit 1. `corpus/evidence/round30/claims.md`: exit 1 |
| 27 | pass on the cited evidence; defect in the check | `--stated 6` on the 5 receipts: `RERUN_RECEIPTS=5/6`, EXIT=1. `--stated 5`: `5/5`, EXIT=0 |
| 28 | pass | fresh seeds on the round-29 base: pristine 78/106, MutOrder 76/106, MutSkipScript 66/106, MutCasefold 72/106 (all exit 1). Landed tool: 106/106, exit 0 |
| 29 | pass when the base is pinned; defect in reproducibility | pinned DNS/header control: v2 20/20 twice (exit 0). v4: 14/27 and 15/27. Pinned quote-shape control on v4: 8/27 and 10/27 |

### 26
- The round-29 lesson gives the 5 hits the criterion states. Some of those hits are negations or have a citation next to them (line 96 "not that the answering process fetched live"; line 98 cites loopback evidence). So whether a hit "cites neither" is a reader's call, not grep output. The check can still fail (exit 0 with hits).
- I scanned the lines added in commits `a9d3a05`, `0dc6e81` and `49b2aa3` for the word. In new round-30 claim and knowledge prose, the only hits are quoted D1 references, the QUALITY text itself, and a negation ("these are not live fetches", `SimplifierHarness.md`). The other hits are in round-29 tool docstrings copied into wave scratch.
- The cited D1 receipt `.ufo/waves/round-29/falsify/DiffToolB/landed-fixture.network.json` holds 8 events, all `GET`, and 8 responses, all `200`. This matches the "8 GETs, 8 responses 200" in `lessons/round-30.md:16`.
- `round-29-verifier-spotcheck.md:143-147` is D1, as cited.

### 27
- Edge cases behave as `ExecRerunCount.md` states. A duplicated receipt gives `4/4` and a note on stderr. `SCORECARD.md` as input gives EXIT=2 (`no seed field and no seed= line`). Adding `rederive.out`, which repeats the seed in `rederive-receipt.json`, gives `5/6`, EXIT=1.
- Seed `12970099299958901445` appears only in report and correction prose (`ScoutFreshnessH.md:18`, spot-check, SCORECARD and LOG corrections). It appears in no receipt.
- Applied to round 30's own claims: `measure/after-c1-run{1,2}.json` with `--stated 2` gives `2/2`, EXIT=0. `after-c2-run{1,2}.json` gives `2/2`, EXIT=0. All 4 receipts carry the landed-tool hash 47a657e7 and the v4 counter and harness hashes.
- **DEFECT (medium).** The check counts distinct seeds and ignores the result and the counter. `--stated 2 measure/revA-c2-run1.json measure/after-c2-run1.json` prints a 24/27 line and a 27/27 line, then `RERUN_RECEIPTS=2/2`, EXIT=0. `--stated 2 after-c1-run1.json after-c2-run1.json`, one C1 and one C2 receipt, also gives EXIT=0. So a statement like "27/27 in N further runs" passes even when a cited receipt missed or comes from another counter. The criterion text ("names N committed receipts with distinct seeds") is met literally. The re-run claim it exists to audit is not.

### 28
- The scratch mutants in `/fast/scratch/hyaku/chousa-r30/w1/CriticD3Classes/` match the hashes in `CriticD3Classes.md` (c19f927a, 9049f2a3, 92b404eb, 72a3ad47).
- The committed receipts hold 78, 76, 66 and 72 of 106 on counter 5b312d84. My fresh runs used seeds 8291450021083815248, 9545053757715525040, 11747642413914436631 and 14017974619703235452, and gave the same 4 scores (`receipt-c28-r29-*.json`).
- Timing: the D3 receipts are stamped `2026-10-23T03:16:26Z`. The first data-seat receipt is `build/ExecC1Head/c1-run1.json` at `03:22:04Z`. The classes were in the counter from v1, before any data seat ran.
- The criterion rests on the round-29 base. I did not apply the mutants to the landed tool; that is the work of the MutR29* seats.

### 29
- The committed receipts match the criterion text: `CtlShapeKeyed/receipt-dns-header-c2-run1.json` 20/20 (counter 7823eef5, v2); `L1Rescore` v3 13/27 and 16/27; v4 16/27.
- **DEFECT (low-medium, reproducibility).** `dns_header_keyed.py:16` and `quote_shape.py` load `Path(__file__).parents[5]/"tools"/"quote-reopen.py"`, which is whatever lane tool is checked out at the time. The receipt's `tool_sha256` hashes only the wrapper (a5129f0f, a2271d7b), so it does not record the code that did the work.
  - Re-run at the tip, these controls now wrap the landed tool. They scored DNS/header 14/27 twice and quote-shape 22/27 and 20/27 (`receipt-c29-*-c2-v4-run*.json`), against the cited 16/27 and 11/27.
  - No other control has this problem. The `CtlDeadlineShortcuts`, `CtlParseShortcuts` and `CtlTrivial*` controls are full copies of the tool that name `tools/quote-reopen.py` only in their docstrings, so their wrapper hash pins them.
- To reproduce the cited numbers, I cloned the lane into `/fast/scratch/hyaku/chousa-r30/w2/ReviewQuality30/`:
  - `v4` at `abfdf93`. Its tool is the round-29 tool, hash 72a3ad47, with the v4 counter and harness.
  - `v2`: `abfdf93` with `corpus/evidence/round30/` taken from `6b1c517`. Hashes match the cited v2 values: 7823eef5 and 06237f36.
- Pinned results, all of which agree with the criterion:
  - DNS/header on v2: 20/20 twice, exit 0 (seeds 11659674340538417460 and 14716922467014271196). The v2 void reproduces.
  - DNS/header on v4: 14/27 and 15/27, exit 1.
  - Quote-shape on v4: 8/27 and 10/27, exit 1.
- The criterion lists URLs, ids, host names, order, response heads and quote shapes. I found keyed controls for DNS, response heads and quote shape (`CtlShapeKeyed`), item shape (`CtlNoReader/relational.py`) and bootstrap metadata (`CriticHarnessIntegrity/leak-map.py`). I did not find a control keyed on item order or registry ids alone. I did not open every control report to confirm this. [INFERENCE] The order and id shortcuts may be covered inside `leak-map.py` or `metadata-audit.py`.

## Residual risk and gaps
- Nothing I found voids a claim. C1 106/106 and C2 27/27 on the landed tool are unaffected: the fresh C1 run on the landed tool gave 106/106.
- Fresh C2 runs per control: 2 each. Each draws its own DEADLINE in [2.0, 6.0] s, so these control scores vary from run to run (DNS/header on v4 so far: 13 to 16 of 27).
- I did not fix either defect. The counters, harness and claims are frozen, and the controls are committed evidence.
- Tools installed or updated: none. Scratch clones were made with `git clone` (read-only on the lane). No processes remain (`pgrep -af ReviewQuality30` is empty).
