# RevRowR31 — SKILL.md Gates row `research-gate round-31 counters` (round 45 w2 falsify)

Target: `/home/vgpnk/Projects/shokunin/chousa-shokunin/SKILL.md` line 100 at commit
`5e8c7ad2f7b8254d83358820286e3d12ca4672d1`. All work measured over the archive tree at
`/tmp/chousa-r45-RevRowR31/tree` (`git archive 5e8c7ad…`). Counters run from inside that tree.
No lane files modified; receipts written only to `/tmp` scratch.

Row cell count: **8** (name / kind / entry / self-test / observed / contract-pinned / safety / owner). Verified by splitting line 100 on `|`.

## Cell-by-cell verdict

### 1. Name — holds
`research-gate round-31 counters` — matches row name.

### 2. Kind — holds
`gate`.

### 3. Entry — holds
Row: `` `python3 corpus/evidence/round31/c1-count.py` · `python3 corpus/evidence/round31/c1-count-v3.py` · `python3 corpus/evidence/round31/c2-count.py` · `python3 corpus/evidence/round31/c2-count-v3.py` (lane root; `--gate PATH`, `--seed N`, `--receipt OUT.json`) ``
Observation: all four scripts exist in the archive tree and run; CLI accepts `--gate/--seed/--receipt/--keep`. Counters exit 0 with full 120/120 (v2) and 132/132 (v3) on the landed gate (`tools/research-gate.sh`, sha256 `2cb04bdd…`); receipts record `predicate_holds=true`.

### 4. Self-test / verdict map — holds (all branches exercised)
Row: `` `LINE_BINDING_MATCH=120/120` (c1-count.py v2) · `REVISION_BINDING_MATCH=120/120` (c2-count.py v2), exit `0` iff matched==120; any other count exit `1`; harness error (fixture gen, missing gate, `--keep`/`--receipt` failure) exit `2`; … v3 counters … TOTAL 132, labels `LINE_BINDING_MATCH=n/132`/`REVISION_BINDING_MATCH=n/132`, exit `0` iff matched==132; v2 counters stay frozen and are superseded for that class only ``
Observation:
- c1-count.py (v2), seeds 1 and 2: `LINE_BINDING_MATCH=120/120`, exit 0, `predicate_holds=true`.
- c2-count.py (v2), seeds 1 and 2: `REVISION_BINDING_MATCH=120/120`, exit 0, `predicate_holds=true`.
- c1-count-v3.py seed 1: `LINE_BINDING_MATCH=132/132`, exit 0.
- c2-count-v3.py seed 1: `REVISION_BINDING_MATCH=132/132`, exit 0.
- exit 1 on any other count: c1-count-v3.py on `MutC1Grammar/nonstring-absent.mutant.sh` printed `LINE_BINDING_MATCH=120/132`, exit 1.
- exit 2 harness error: `--gate /nonexistent` and uncreatable `C1_TMP` both exit 2 on all four counters.
- v3 counters do include the 12 non-string claims (I2 classes visible in per-class output; 120+12=132).

### 5. Observed (before/control values) — holds in value, one wrong path citation
Row: `` before on the base gate `be7b8d8d`: 50/120 each (do-nothing controls, `controls/CtlBaselineJunk/`); best v2 queues C1 116/120 (start-line-only binding, `controls/CtlShortcutC1/v2/`), C2 118/120 (whitespace-trimming, `controls/CtlShortcutC2/v2/`); no-reader C1 88/120, C2 86/120 (`controls/CtlNoReaderC1/v2/`); the v3 counters fail the round-31 nonstring-absent mutants (MutC1Grammar gate `85d85a7b`, MutC2Parse gate `f9da8257`) ``
Observation:
- Base-gate 50/120 each: confirmed by committed control receipts (`CtlBaselineJunk/c{1,2}_base_seed*.json`, `ChousaR31.CriticClaimDesign31/base-*` = 50/120).
- C1 best v2 queue 116/120: `CtlShortcutC1/v2/range-ignored-seed9340{11,12,13}.json` = 116/120 ✓ (path exists).
- C2 best v2 queue 118/120: `ChousaR31.CtlShortcutC2/v2/trim-spaced-seed900{1,2,3}.json` = 118/120 ✓ — **but the cited path `controls/CtlShortcutC2/v2/` does not exist**; the actual control directory is `controls/ChousaR31.CtlShortcutC2/v2/` (no `CtlShortcutC2` directory exists at all).
- No-reader C1 88/120: `CtlNoReaderC1/v2/control_noreader-seed-7300{1,2,3}.json` = 88/120 ✓; C2 86/120: `CtlNoReaderC2/v2/receipt-seed910{1,2,3}.json` = 86/120 ✓.
- v3 fails MutC1Grammar gate `85d85a7b`: reproduced — sha256 of `falsify/MutC1Grammar/nonstring-absent.mutant.sh` = `85d85a7b…`; c1-count-v3.py against it prints 120/132, exit 1 ✓.
- v3 fails MutC2Parse gate `f9da8257`: **not reproducible from committed artifacts** — the mutant gate script is not in the tree (it lived at `/fast/scratch/hyaku/chousa-r31/w2/MutC2Parse/…`, now deleted). Committed receipts `falsify/MutC2Parse/m1-nonstring-absent.seed{1,2}.receipt.json` bind `gate_sha256=f9da8257…` with the v2 counter (1064fdb3…) at 120/120; the v3 run itself is unobserved here.

### 6. Contract / pinned values — holds in hashes, two receipt paths missing
Row: `` contract `corpus/evidence/round31/claims.md` (design v2; base `be7b8d8d`, v1 `d78d1889`, v2 `8070f92b`, control re-score `86188116`); landed C1 `c17948a7` (gate `3b5279eb`), C2 `6d0ae19f` (gate `c23d7537`), final gate `0bc318b3` (post-falsify fixes `65d00cfc`); receipts `.ufo/waves/round-31/measure/after-c{1,2}-run{1,2}.json`, `after-c{1,2}-run{3,4}-tip.json`, `after-c{1,2}-run{7,8}-final.json`; controls `.ufo/waves/round-31/controls/`; falsify re-runs `.ufo/waves/round-31/falsify/Rerun*` ``
Observation:
- `corpus/evidence/round31/claims.md` exists at the commit.
- All pinned commits exist: `be7b8d8d`, `d78d1889`, `8070f92b`, `86188116`, `c17948a7`, `6d0ae19f`, `65d00cfc` resolve in the lane git history.
- Gate pins match file sha256 at those commits: gate at `c17948a7` = `3b5279eb…`; gate at `6d0ae19f` = `c23d7537…`; `0bc318b3…` is the gate hash of the final fix commits (235365909e/7b828305/d27157bb) and matches the final receipt gates. Committed measure receipts confirm every hash chain: `after-c1-run{1,2}.json` gate `3b5279eb`, `after-c1-run{3,4}-tip.json` gate `c23d7537`, `after-c{1,2}-run{7,8}-final.json` gate `0bc318b3`.
- Receipt paths: `after-c{1,2}-run{1,2}.json` (4/4 exist) ✓; `after-c{1,2}-run{7,8}-final.json` (4/4 exist) ✓; **`after-c{1,2}-run{3,4}-tip.json` — only the C1 pair exists (`after-c1-run3-tip.json`, `after-c1-run4-tip.json`); `after-c2-run3-tip.json` and `after-c2-run4-tip.json` do not exist** (C2 measure sequence is run1, run2, run5-fixab, run6-fixab, run7-final, run8-final — no runs 3/4 for C2). The brace expansion over-cites by two files.
- `controls/` and `falsify/Rerun*` (RerunC1A/B, RerunC2A/B, RerunSeedSweep31) all exist. ✓

### 7. Safety — holds
Row: `` temp dirs only (mkdtemp under `C1_TMP`/`C2_TMP` or system tmp); writes a receipt only when `--receipt` is given; no network ``
Observation: with `C1_TMP` set to a fresh scratch dir, a no-`--receipt` run exits 0, leaves the archive tree byte-identical (pre/post sha256 of full file listing equal), and the temp dir is cleaned. Missing-gate/`--keep` failures exit 2 without side effects.

### 8. Owner — holds
`chousa`.

## Findings

1. **[wrong, low] Cell 6 pinned receipt paths over-cite** — `after-c2-run3-tip.json` and `after-c2-run4-tip.json` do not exist at 5e8c7ad…; the C2 receipt sequence has no runs 3/4. Only the C1 tip pair exists. Resolvable pointer: `corpus/evidence/round31/claims.md` vs `.ufo/waves/round-31/measure/` listing.
2. **[wrong, low] Cell 5 wrong control path for C2 shortcut queue** — `controls/CtlShortcutC2/v2/` does not exist; actual dir is `controls/ChousaR31.CtlShortcutC2/v2/` (118/120 values verify there). No `CtlShortcutC2` directory exists anywhere under `controls/`.
3. **[verification gap] Cell 5 v3-fails-MutC2Parse claim not reproducible** — `f9da8257` mutant gate script is uncommitted and deleted from scratch; only its bound receipts exist. Direct v3 run impossible with committed artifacts. No contrary evidence found.

## Residual risk
All zero/mismatch/error exit-code branches of the verdict map were exercised and match. The only un-re-runnable claim is the MutC2Parse v3 failure (mutant artifact absent); its pin is present in committed receipts. The two path defects are citation-level, not behavioral.

## Method note
Counters were executed from the archive tree only; all receipts written under `/tmp/chousa-r45-RevRowR31/scratch/`. No lane files were touched; scratch removed.
