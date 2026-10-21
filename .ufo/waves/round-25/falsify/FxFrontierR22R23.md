# FxFrontierR22R23 — round-25 freshness falsify

Reviewed the integrated full pin `e93ac711f885a10d44fdd80a1734997419595b5a` (not the first packaging checkpoint) and the appended R22/R23 paragraphs at `corpus/README.md:743-772` against SCORECARD, LOG, both notes, round reports, and the receipts.

Axes: historical factual accuracy; evidence/receipt provenance; truthful holds and limitations.

## Findings, severity order

1. **MEDIUM — R1 hold receipt gap is not preserved in the integrated paragraph.** `corpus/README.md:751-753` says the R22 observables hold and states `VERDICT_BEARING_EXPORTS=3/3`; line 801 then says the new paragraphs preserve each receipt gap. SCORECARD R22/R23 (`:1156`, `:1205`) and LOG (`:798`, `:810`) assert 3/3, but searching all eight R22/R23 demo/selftest/battery/drift receipts for `VERDICT_BEARING_EXPORTS` returns **No matches found**. The build draft itself records this gap at `.ufo/waves/round-25/build/FrontierR22R23.md:16,31,42,49`. Correct fact: 3/3 is a scoreboard/log assertion (the draft reports private re-runs, not a retained R22/R23 receipt); label it non-receipt-backed and narrow line 801's “each receipt gap” claim accordingly.

2. **LOW — the current R22 recheck instruction still names superseded selftest cases.** `corpus/knowledge/denylist-r22.md:5` says cases 129–132 pin path-start. The actual R23 selftest receipt has `chain-fence-anchor` at line 129 and the path-start cases at lines 130–133 (`fanchor-r23-20261019T192000Z-selftest.log:129-133`). The new paragraph and README erratum correctly state the renumbering (`corpus/README.md:766-767,795-798`), and the SCORECARD/LOG 129–132 entries are correct as R22-era history. Append an erratum or revise the live `recheck:` pointer so a present-day re-run does not misidentify cases.

## Cross-checks / confirmed facts

- Gate blob prefixes match the scoreboard and round records: `git show 10083e1:tools/research-gate.sh | sha256sum` → `bfc291ef…`; `a27128e` → `dfb798b4…`; `fb70ddb` → `dfb798b4…`; `f818652` → `b5d0f93d…`. The four demo-receipt halves support the stated CLEAN→`CLAIM_SOURCE_SESSION` refusal (R22) and verified→`anchor-missing`/`CHAIN_ANCHOR_NOT_FOUND` (R23): `deny-r22-…-demo.log:1-12`; `fanchor-r23-…-demo.log:1-12`.
- R22 selftest receipt ends `PASS (132 cases, 0 skipped)`; R23 ends `PASS (133 cases, 0 skipped)`. R23 lines 129–133 substantiate the inserted case and renumbering. Both drift receipts are `GATE_DRIFT: none` at line 1. R23’s battery is literally identical to R22’s (`cmp_exit=0`, 133 lines each).
- Battery caveat is preserved outside the two paragraphs: README `:798-802` says “ALL IDENTICAL” is not a CLEAN claim. Both actual batteries use `root=.` at line 113 and end `VERIFY_ALL ... drift-sections=3 findings=13` / `RESEARCH_GATE: DRIFT` at lines 132-133. The new R22/R23 prose does not call those batteries CLEAN. The separate R25 explicit-fleet-root hold claim at README `:801-802` is supported by the R25 hold receipts (e.g. `round25-holds/holds/verify-all-full-r6.log:1,7-9`, root `/home/vgpnk/Projects/shokunin`, CLEAN).
- The formerly misfiled R22/R23 evidence rows now have their own index sections (`corpus/evidence/README.md:1021-1033,1035-1047`); draft finding 3 is resolved in the integrated tree.

## Draft-only stale statement and verification gaps

`build/FrontierR22R23.md:44` calls `752e4e38` / 5290 lines the “live gate now”; that is only the R24 gate and must not be reused as current at e93. Read-only `git show e93ac711f885a10d44fdd80a1734997419595b5a:tools/research-gate.sh | sha256sum; wc -l` returned `63a39282a15f19f5b0443212e66ad2dfc8ce0315e65697e479a7206879a598b2` and `5673` lines. This stale draft row is not copied into the integrated Frontier paragraphs.

No gate/selftest was run; inspection, receipt search, historical blob hashing, and battery `cmp` were read-only. No installs. No production files changed.

VERDICT: Two actionable provenance/freshness corrections remain; round-specific before/after, gate-sha, selftest, renumbering, and drift claims in the integrated Frontier otherwise match their cited records, and the battery DRIFT caveat is present.