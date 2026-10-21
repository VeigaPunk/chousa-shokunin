# Round 22 capability-row evidence

## Findings (by severity)

- **INFO — capability identified and demonstrated.** LOG.md:796 says the round-22 fix adds bare-start alternatives for `.config/`, `.omp/`, and `.local/state/` so those path-start forms refuse; LOG.md:800 records: “**ADMIT. Capabilities +1.**” SCORECARD.md:1132–1136 names the capability as “the `.config` path-start denylist bypass”; SCORECARD.md:1150–1155 describes the added bare-start alternatives and the adjacent-path control.
- **INFO — capability table omission confirmed.** SCORECARD.md:1278–1280 explicitly lists the missing capability backfills for rounds 15 and 17–23, including round 22. No first-working-round-22 capability row is present.

## Demonstration rerun

Private clone HEAD: `b820e4e40ce52deedf53b191140cd7b08ddda929` (observed with `git rev-parse HEAD`). Ran `bash tools/research-gate.sh --selftest` in `/tmp/chousa-r25-CapRowR22`; it passed:

```text
ok-case 130 claims-config-start        exit=1
ok-case 131 claims-omp-start           exit=1
ok-case 132 claims-localstate-start    exit=1
ok-case 133 claims-config-adjacent     exit=0
RESEARCH_GATE_SELFTEST: PASS (136 cases, 0 skipped)
```

The current run's numbering is 130–133: the round-23 `chain-fence-anchor` case occupies 129. The round-22 evidence index records the original `deny-r22-20261019T190000Z-selftest.log` as PASS (132 cases), and its demo receipt as CLEAN before / `CLAIM_SOURCE_SESSION` refusal after (`corpus/evidence/README.md:664–665`). The historical round-22 range 129–132 is documented in LOG.md:796 and `corpus/knowledge/denylist-r22.md:5`.

## Draft SCORECARD row

```text
| denylist path-start refusal | refuses claim sources beginning `.config/`, `.omp/`, or `.local/state/` as `CLAIM_SOURCE_SESSION`, while allowing `.config-adjacent/` | selftest cases 130–133 (current rerun; round-22 receipt cases 129–132); `corpus/knowledge/denylist-r22.md` | 22 |
```

## Residual risk and verification gaps

`corpus/knowledge/denylist-r22.md:5,28` still says cases 129–132 and calls the adjacent-path test case 132; those are the historical round-22 numbers. The rerun at the pinned round-25 base shows 130–133 and adjacent case 133. The draft distinguishes current rerun from the original receipt. The demonstration and selftest pass; no verification gap remains for this row.

VERDICT: Round-22 capability is identifiable and demonstrated; the row is supportable. No installs.