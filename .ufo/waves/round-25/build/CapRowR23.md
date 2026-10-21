# Round-23 capability row evidence

Axes: freshness (the claimed acquisition is unindexed) and calibration (scope the capability to the tested heading-anchor behavior).

## Claim and verdict

- `LOG.md:808` claim: “**Claim (coverage/operability) — the fenced-heading anchor false-positive**: `chain_anchor_at` scanned raw lines with `^#+` and matched headings inside fences — a `## Phantom Heading` inside a code block verified as a real anchor.” The same line records the before/after demo: landed behavior is `anchor-missing` + `CHAIN_ANCHOR_NOT_FOUND` warn + DRIFT.
- `LOG.md:812`: “**Capabilities +1.**”
- `SCORECARD.md:1189-1192` names the claim as “the fenced-heading anchor false-positive” and describes the fenced `## Phantom Heading` being accepted as a real anchor before the fix. `SCORECARD.md:1209` verdict: “the fenced-heading anchor class is closed: before `verified` on a fenced heading → after `anchor-missing` + `CHAIN_ANCHOR_NOT_FOUND` warn.”
- `SCORECARD.md:1278-1280` acknowledges the missing row: “the 8 capability acquisitions `LOG.md` claims for rounds 15 and 17–23 still have no row”.

## Demonstration rerun

Created the permitted private clone and observed its HEAD as `b820e4e40ce52deedf53b191140cd7b08ddda929`.

Command in `/tmp/chousa-r25-CapRowR23`:

```text
bash tools/research-gate.sh --selftest
ok-case  129 chain-fence-anchor           exit=1
RESEARCH_GATE_SELFTEST: PASS (136 cases, 0 skipped)
```

The `exit=1` is the expected test result: the selftest asserts DRIFT, `CHAIN_ANCHOR_NOT_FOUND`, `observed=anchor-missing`, and `RESOLVED_HOPS=0/1` for a heading inside a fence (`tools/research-gate.sh:5107-5111`). The r23-specific test is case 129; the note says “case 129 pins the fenced-anchor arm” (`corpus/knowledge/fenced-anchor-r23.md:5`), and the round-23 verdict says “Case 129 pins it” (`SCORECARD.md:1201-1205`). This is a later tree than the r23 landing: the evidence index records r23 at 133 cases and r24 at 136 with cases 1–133 unchanged (`corpus/evidence/README.md:668-669, 948`).

## Proposed SCORECARD row

```markdown
| fenced-heading chain anchors | rejects a heading inside a fenced code block as a chain `heading` anchor, reporting missing-anchor drift rather than accepting a false match | selftest cases 129–129; `corpus/knowledge/fenced-anchor-r23.md` | 23 |
```

## Residual / verification gaps

- The current source comment at `tools/research-gate.sh:5094` labels the fenced-anchor case “133 (r23)”, but the rerun prints it as case 129 and both the knowledge note and SCORECARD call it case 129. Treat the comment ordinal as stale; clarify it during integration.
- LSP is unavailable in this tool environment (`read xd://lsp` returned “No such tool”). Evidence here is direct file-line reads plus the permitted selftest run, not LSP semantic analysis.
- No tools installed or updated.

VERDICT: The round-23 capability is identifiable and its demonstration passes; the proposed row is supported for backfill, with the stale case-number comment retained as a calibration note.
