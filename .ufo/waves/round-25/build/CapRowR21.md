# Round 21 capability-row backfill

## Evidence

- `LOG.md:782` claims: “**Verdicts** (SCORECARD §Round 21): coverage/operability/depth/calibration(narrow) **improved**; freshness/adjacency **unchanged**; none harmed. **ADMIT.** Capabilities +1.”
- `SCORECARD.md:1078-1081` identifies the capability: “coverage/operability = the `ptr_resolves_meta` boundary gap (round-20 named debt): relative pointer paths check `-f` without canonicalization — `..` traversal and symlinks escape.” Its verdict at `SCORECARD.md:1103` says coverage **improved** because “the pointer-boundary escape class is closed” and the `.config` canonical-target check closes the benign-symlink arm.
- `SCORECARD.md:1278-1280` explicitly says the acquisitions claimed for rounds 15 and 17–23 still have no row. The round-21 entry is therefore missing from the capabilities table.

## Fresh demonstration

- Private clone: `/tmp/chousa-r25-CapRowR21`, observed HEAD `b820e4e40ce52deedf53b191140cd7b08ddda929`.
- Ran `bash tools/research-gate.sh --selftest` in that clone. The round-21 cases passed:

```text
ok-case  125 ptr-traversal                exit=1
ok-case  126 ptr-symlink                  exit=1
ok-case  127 ptr-lane-abs                 exit=0
ok-case  128 ptr-deny-symlink             exit=1
RESEARCH_GATE_SELFTEST: PASS (136 cases, 0 skipped)
```

## Draft row (not applied to SCORECARD.md)

`| canonical pointer-boundary screening | canonicalizes relative pointer targets and checks them against both roots, refusing traversal/symlink escapes and denylisted canonical targets | selftest cases 125–128; `corpus/knowledge/pointer-boundary-r21.md` | 21 |`

## Residual risk and verification gaps

The capability is bounded to canonical-target checks: `corpus/knowledge/pointer-boundary-r21.md:25-32` retains direct `.config/foo` path-start bypass and fenced-heading anchor false-positive as separate debt. The requested selftest was rerun; the historical standalone before/after demo receipt was not rerun.

No installs. No persistent clone files modified; no SCORECARD or live lane files modified.