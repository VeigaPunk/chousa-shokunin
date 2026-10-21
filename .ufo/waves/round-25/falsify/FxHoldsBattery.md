# FxHoldsBattery — round 25

Checkpoint measured: `e93ac711f885a10d44fdd80a1734997419595b5a` (observed `git rev-parse HEAD` in private clone `/tmp/chousa-r25-FxHoldsBattery`). The round-25 lesson records the packaging sequence: `0fc037e` omitted `tools/research-gate.sh` and `d8c8cff` omitted `corpus/evidence/README.md` (`corpus/lessons/round-25.md:109-133`). This battery was run only at full checkpoint `e93ac711`; failed pins were not measured here.

## Finding — LOW: volatile masking can hide nonvolatile `ts=` changes

`corpus/evidence/round25-holds/battery.sh:22-30` applies unanchored substitutions to each line. A concrete probe through the same awk normalization:

```text
OLD=FINDING obs=note=ts=before
NEW=FINDING obs=note=ts=after
NORMALIZED_OLD=FINDING obs=note=ts=<MASKED>
NORMALIZED_NEW=FINDING obs=note=ts=<MASKED>
FALSE_GREEN_PROBE=EQUAL
```

Thus a meaningful `ts=` value outside the banner field can change without a diff; the `gate_sha256` substitutions are likewise not field-anchored (`:26-30`). This is a harness false-green possibility, not an observed mismatch in the frozen comparisons: the baseline search showed `ts=` only in each mode banner and no `gate_sha256` occurrence. Empty comparisons and dropped exits were not observed: all 12 baselines contain output; the selftest baseline includes case 136 and `EXIT_CODE=0` (`holds/selftest.log:136-138`), and the runner appends the observed exit before diffing (`battery.sh:42-69`).

## Battery result

Command: `bash corpus/evidence/round25-holds/battery.sh /tmp/chousa-r25-FxHoldsBattery /home/vgpnk/Projects/shokunin`

```text
MATCH selftest (exit 0)
MATCH drift-r12 (exit 0)
MATCH verify-all-A-r9 (exit 0)
MATCH verify-all-B-r9 (exit 0)
MATCH verify-all-C-r9 (exit 0)
MATCH verify-all-full-r6 (exit 0)
MATCH verify-all-full-r6-broken (exit 1)
MATCH verify-all-integrity-r7 (exit 0)
MATCH verify-all-integrity-r7-broken (exit 1)
MATCH verify-all-sweeps-r5 (exit 0)
MATCH verify-all-chain-r3 (exit 1)
MATCH verify-claims-r2 (exit 0)
BATTERY_RC=0
```

The full selftest was separately run in the same clone: `RESEARCH_GATE_SELFTEST: PASS (154 cases, 0 skipped)`; `FULL_SELFTEST_RC=0`. For `chain-r3`, the current command returned `CHAIN_R3_RC=1`, with `SECTION structure ... CLEAN` and the expected `SECTION sweeps ... DRIFT` / `FINDING SWEEP_REJECTION_INCOMPLETE severity=warn surface=sweeps obs=id=R1 missing=flip`; its frozen baseline has the same rejection and `EXIT_CODE=1` (`holds/verify-all-chain-r3.log:5-10`). This is the intentional rejection fixture, not an unexpected change. `drift-r12` matched `GATE_DRIFT: none`.

## Residual risk and verification gaps

The syntactic limits of `verify-metadata` are explicitly documented, not raised as new regressions here (`corpus/knowledge/metadata-screen-r25.md:69-83`). This seat did not measure the metadata population/export count or C2/C3 counts; those are outside the assigned holds battery.

Installs: none.

VERDICT: Holds match at the full pin; one low-severity normalization false-green risk remains because volatile masks are not field-anchored.