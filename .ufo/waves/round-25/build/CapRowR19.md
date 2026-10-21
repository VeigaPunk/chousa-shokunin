# Round 19 capability-row backfill

Axes: freshness, calibration.

## Finding

The Round 19 capability is identifiable and its demonstration passes; a row is warranted, not pre-claimed. `SCORECARD.md:1278-1280` explicitly lists rounds 15 and 17–23 as capability acquisitions still lacking rows, including round 19.

LOG claim (`LOG.md:701`): “**Verdicts** (SCORECARD §Round 19): coverage/operability/depth/calibration(narrow) **improved**; freshness/adjacency **unchanged**; none harmed. **ADMIT.** Capabilities +1.”

Round 19 SCORECARD text (`SCORECARD.md:975-980`): “`verify_sweeps` now canonicalizes every glob match and refuses the whole sweep if any match resolves outside both allowed roots — `SWEEP_LOCATION_OUT_OF_CORPUS` crit, `observed=refused`, no match paths reported. Cases 120–122 pin the escape class (outside leaf symlink, outside dir symlink, in-root symlink control unaffected).”

## Re-run demonstration

Private clone created from `/home/vgpnk/Projects/shokunin/chousa-shokunin`; observed base: `b820e4e40ce52deedf53b191140cd7b08ddda929`. Ran `bash tools/research-gate.sh --selftest` in `/tmp/chousa-r25-CapRowR19`; it passed (`RESEARCH_GATE_SELFTEST: PASS (136 cases, 0 skipped)`). Round 19's cases:

```text
ok-case  120 sweeps-symlink-escape        exit=1
ok-case  121 sweeps-symlink-dir           exit=1
ok-case  122 sweeps-inroot-symlink        exit=1
```

The current suite preserves those three cases; `tools/research-gate.sh` defines 120–121 as outside leaf/directory symlink refusals checking `SWEEP_LOCATION_OUT_OF_CORPUS` and `observed=refused` (lines 4934–4963), and 122 as the in-root symlink control (lines 4964–4978). The registered Round 19 receipt index also records `PASS (122 cases)` and the before/after symlink demo (`corpus/evidence/README.md:652-653`).

## Draft capability row

```text
| sweep symlink-escape refusal | Refuses a whole sweep if any expanded glob match canonicalizes outside both allowed roots. | selftest cases 120–122; `corpus/knowledge/sweep-symlink-r19.md` | 19 |
```

The note describes the fix and the in-root control (`corpus/knowledge/sweep-symlink-r19.md:22-28`). No source files were written. Installs/updates: none.
