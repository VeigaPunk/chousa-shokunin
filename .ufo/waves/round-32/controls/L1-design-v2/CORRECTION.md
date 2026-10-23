# Correction (round 32, after ReceiptCensus32)

The L1 receipts `c1-appendonly-s3201.json`, `c1-cached-s3201.json`, `c1-probeonly-s3201.json` and
`c1-shared-s3201.json` in this directory, and the gate copies `a-append-only.sh`,
`c-cached-probe.sh`, `c1-probeonly-control-gate.sh` and `d-shared-lock.sh`, are NOT control
evidence. CtlC1PartialLockB had restored its scratch gates to the base bytes before the L1 copied
and scored them: every one of these files has gate SHA-256 `0bc318b3…` (the base gate), so the
four receipts are base-gate reruns (0/24 each), named after controls they did not run.

The control evidence for C1 under v2 is the seat's own re-score with the mutated bytes, committed
before any candidate receipt (`f43dd5a3`):
`.ufo/waves/round-32/w1/CtlC1PartialLockB/v2/mutated-{a-append-only,b-probe-only,c-cached-probe,d-shared-lock}-s*.json`
— gates `4a39b997…`, `034f786b…`, `59ea2a22…`, `76c4c073…`, each 0/24 on two seeds, counter
`e6bf9531…`. The probe-only gate bytes (`034f786b…`) are also reconstructed at
`.ufo/waves/round-32/w2/MutCounterC1v2/reconstructed-probe-only-gate.sh`.
The C1 oracle receipts (`c1-oracle-s320{1,2}.json`, gate `719d0b92…`) and every `c2-*` file here
are what their names say.
