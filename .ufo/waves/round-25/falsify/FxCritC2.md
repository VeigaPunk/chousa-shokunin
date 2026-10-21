# FxCritC2 — Claim 2 falsification

**Axis:** freshness. Advisory review only; L1 retains the verdict.

## Checkpoint and receipts

- Frozen base `d730ae4c33989ad9c8535764d4cae77b4db869f6`: the landed measure script reproduced `STALE_INDEX_ITEMS=66` (2+13+43+8); recorded before receipt agrees (`corpus/evidence/round25-measure-before.log:5-10`).
- Packaging corrections matter: exact `0fc037e6b07f3820ead8c9207a8034ac854197a1` had gate SHA prefix `752e4e38`, `verify-metadata rc=2`, and selftest 136; its C2 rerun was 43, not the committed after receipt's 0. At `d8c8cff3923f10481ac9ced66d0af7c41d38130c`, gate SHA was `63a39282`, selftest 154, but C2 still reran as 43 because the evidence index was absent. `LOG.md:882-896` and `corpus/lessons/round-25.md:111-133` record both omissions.
- Full authoritative pin `e93ac711f885a10d44fdd80a1734997419595b5a`, observed in private clone; gate digest is `63a39282a15f19f5b0443212e66ad2dfc8ce0315e65697e479a7206879a598b2`. Its pristine full measure rerun returned C2 `2a=0, 2b=0, 2c=0, 2d=0`, `STALE_INDEX_ITEMS=0`; holds were selftest 154, drift none, exports 3/3. The final after receipt agrees (`round25-measure-after.log:40-56`). Actual round-specific evidence-index sections/rows are present in `corpus/evidence/README.md:937-1047` (e.g. Round-23 section and its selftest row at e93 line 1044 before the mutation below).
- Scorecard calls C2 freshness “improved” at `SCORECARD.md:1344`; LOG says 43 rows moved and `66→0` at `LOG.md:849-853`. These are accurate descriptions of the pristine e93 tree, but the counter has a decisive blind spot.

## Decisive counterexample — omitted evidence row still passes

- `round25-measure.sh:34-42` increments 2c only for *present* recognized receipt rows under the wrong heading; it never compares the observed rows against the frozen 43 receipt identities. This is the same failure identified in `CriticClaim2.md:6-8`; the script was not hardened in the full checkpoint. `ConnectorSpotcheckMap.md:28` also acknowledges that C2 lexical counters can be gamed.
- In a separate private clone of e93, I removed only `fanchor-r23-20261019T192000Z-selftest.log` from the Round-23 table (the receipt file remains). Rerunning the full measure script still reported `2c EVIDENCE_MISFILED_ROWS=0` and `STALE_INDEX_ITEMS=0`. Thus the registered “improved” count can pass with a required index row missing. This is a failure-capable counterexample to the freshness acceptance, not evidence that the pristine e93 index actually lacks that row.
- The legitimate scope limit is different: C2 is index freshness, not a coverage/expansion measure. That qualification is explicit in `ConnectorSpotcheckMap.md:10` and `SCORECARD.md:1357-1369`; it does not cure the omitted-row false pass.
- Other CriticClaim2 concerns also remain in the unmodified counter: 2a uses path substring membership, 2b checks only a round-heading regex, and 2d uses mutable LOG claims / permissive row shape (`CriticClaim2.md:4-8`, `round25-measure.sh:26-53`). Human review notes in `CriticClaim2.md:60` are useful but are not an executable acceptance guard.

## Smallest safe correction / advisory

Replace 2c's present-row error count with a frozen round→receipt-identity map: require each expected receipt exactly once, under its actual round heading, with nonempty Shows/Key-result cells and an existing target file; count missing, duplicate, and misplaced rows. For complete closure, apply the same frozen-population discipline to 2a/2b/2d. On observed e93 files freshness repair is present, but `STALE_INDEX_ITEMS=0` alone does not prove completeness; treat the C2 verdict as advisory until the omission control fails.

[INFERENCE] `SCORECARD.md:1387-1392` names d8c8cff as the corrected measured checkpoint, while `LOG.md:892-896` says d8c8cff still lacked the evidence index and identifies the later full checkpoint. Name e93 explicitly in the scorecard erratum to avoid competing checkpoint authorities.

Private-clone mutations only (not lane files): `/tmp/chousa-r25-FxCritC2/corpus/evidence/README.md` SHA-256 `b7e839bb72ed8387263a09cf645147144fc22bc60f36bcdc49ee059aa1b1f258` (43-row deletion probe); `/tmp/chousa-r25-FxCritC2-e93/corpus/evidence/README.md` SHA-256 `cdbf8921e3634b1b1da29c084ed338a652b281a19edfeb1d4a0d03e7bf0646a8` (single-row omission probe). No installs.

VERDICT: Freshness repair is observed in full checkpoint e93, but its counter can still report zero after an indexed receipt is deleted; C2 improvement is advisory, not established by that count alone. Installs: none.