Axes: calibration, input integrity, reproducibility.

# FxCountC3 — independent Claim 3 count

## Finding
- **P2 — C3 count is fail-open on empty/missing inputs (measurement/spec-coverage gap).** `corpus/evidence/round25-measure.sh:8,58-79,81-85` only counts matches; it does not require the frozen `SKILL.md` content or assert the promised replacement pointer/command. In an e93-derived scratch tree with only `SKILL.md` emptied (hardening ledger intact), the same script printed `3a=0`, `3b=0 of 0`, `3c=0`, `3d=0`, `STALE_RESTATEMENTS=0`, `MEASURE_RC=0`. With `SKILL.md` absent, it raised `FileNotFoundError`, emitted no C3 summary, continued through passing holds, and still returned `MEASURE_RC=0`. Thus zero can be produced by absent evidence, not just closure. This is not a defect in the actual e93 SKILL content: `SKILL.md:434-443` contains the owning-ledger pointer and re-derive command. The measurement does not check that content.

## Independent reproduction
Private clone observed at `e93ac711f885a10d44fdd80a1734997419595b5a`; base archive observed at `d730ae4c33989ad9c8535764d4cae77b4db869f6`. Ran the landed `corpus/evidence/round25-measure.sh` from the private clone against both roots. Claim-3 blocks:

```text
base d730ae4:
3a SKILL_OPEN_CLOSED_FINDING=1
3b SKILL_LEDGER_TUPLES_STALE=3 of 3 (latest ledger 38·21·10·0·3) QUEUE_STALE=2 of 2 (latest queue 24)
3c PLACEHOLDER_GSHA=1
3d LEDGER_ADDENDA_MISSING=8 rounds=[16, 17, 18, 19, 20, 21, 22, 23]
STALE_RESTATEMENTS=15
MEASURE_RC=0

full pin e93ac711:
3a SKILL_OPEN_CLOSED_FINDING=0
3b SKILL_LEDGER_TUPLES_STALE=0 of 0 (latest ledger 38·22·8·0·3) QUEUE_STALE=0 of 0 (latest queue 24)
3c PLACEHOLDER_GSHA=0
3d LEDGER_ADDENDA_MISSING=0 rounds=[]
STALE_RESTATEMENTS=0
MEASURE_RC=0

holds on base: SELFTEST PASS (136 cases, 0 skipped); GATE_DRIFT: none (drift rc=0); VERDICT_BEARING_EXPORTS=3/3.
holds on e93: SELFTEST PASS (154 cases, 0 skipped); GATE_DRIFT: none (drift rc=0); VERDICT_BEARING_EXPORTS=3/3.
```

Both measured C3 blocks match the committed logs: `round25-measure-before.log:12-16` and `round25-measure-after.log:47-56`. The frozen C1 list has 28 names (`round25-measure.sh:14-16`); the e93 run reports `entries=28`, `METADATA_COMPLETE=25/28`, and no missing-population diagnostic.

## Checkpoint corrections and residual risk
- The first pin was not usable for the new gate: `git show 0fc037e:tools/research-gate.sh | sha256sum` prefix `752e4e38`; direct `verify-metadata corpus/knowledge` printed `research-gate: multiple record paths` and returned 2. The measurement script on the base likewise reports metadata rc=2.
- The intermediate `d8c8cff` has gate prefix `63a39282`, but its `corpus/evidence/README.md` blob remained the base blob `1701914b…`; `e93ac711` changes it to `9de288e1…` (d8→e93 diff: 154 insertions, 43 deletions). Counts above use the full e93 pin, not either incomplete packaging checkpoint.
- Residual scope: the round-25 lesson names source/span pairing as still uncovered (`corpus/lessons/round-25.md:42`); `SKILL.md:442-443` likewise says no mode pairs a ledger path/line with the span occurrence line. The 15→0 metric establishes restatement cleanup only, not semantic completeness.

## Verification gaps
No LSP device is mounted (`read xd://lsp` returned “No such tool”); no semantic references/definition/diagnostics were available. Text search was used only to locate the SKILL passage, then exact lines were read. No checks beyond the assigned measure and private scratch probes were run. Installs: none.

VERDICT: Claim 3 reproduces 15→0 with holds on full pin e93; report the empty/missing-input fail-open measurement gap.