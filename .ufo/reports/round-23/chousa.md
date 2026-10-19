# chousa — round 23 report (2026-10-19)

Goal-wave round (curriculum loop 1, round 12 — direct integration, no wave). Work commit `b5d0f93d…` (HEAD when filed).

## Work performed

- No opening commit — the claim's before→after was already measured live by the round-20 wave's seat-16 reproduction (the fenced-heading anchor false-positive); the fix shape was validated by that wave's design seats. Direct integration per the shokunin honest-stop rule: the claim's falsifiable evidence existed before dispatch.
- Parent integration: the inline fence tracking in `chain_anchor_at` + case 129 + receipts.

## Landed changes (each tied to LOG.md round-23 entry)

- `tools/research-gate.sh` (`dfb798b4…` → `b5d0f93d…`): `chain_anchor_at` heading arm tracks fence state inline — a `# ` inside a fence is literal, not an anchor target. Case 129 appended.
- `corpus/knowledge/fenced-anchor-r23.md`: the false-positive mechanics, the fix contract, the named limits.
- `corpus/evidence/fanchor-r23-20261019T192000Z-{demo,selftest,battery,drift}.log`: the receipts.
- `corpus/README.md` + `corpus/evidence/README.md` + `SKILL.md` + `SCORECARD.md` + `LOG.md`: the records.

## Before → after measurements

- Fenced-heading anchor: before `verified` at line 4 on a `## Phantom Heading` inside a fence → after `anchor-missing` + `CHAIN_ANCHOR_NOT_FOUND` warn + DRIFT (receipt `fanchor-r23-…-demo.log`).
- Selftest: 132 → 133 (0 skipped); cases 1–128 `cmp` byte-identical vs `deny-r22-20261019T190000Z-selftest.log`.
- Battery: r1 `3/3`; drift `none` vs the r12 baseline; masked battery vs the pre-round gate ALL IDENTICAL.

## Cross-domain evidence

None. All work confined to the chousa province.

## SHONEN

- [ ] real decision tables / error patterns / checklists with cited sources — `[~]` (knowledge notes + gate finding registry + selftest fixture tables; fresh lane review not on file)
- [ ] end-to-end domain task executed and logged — `[~]` (44 rounds of gate development with receipts; fresh lane review not on file)
- [ ] instructions executable by an agent without oral context — `[~]` (SKILL.md + `--help` + corpus README self-contained; fresh lane review not on file)
- [ ] no cross-domain bleed with `PROVINCE.md` still accurate — `[~]` (PROVINCE.md unchanged; fresh lane review not on file)

## Seat roster

No wave dispatched — direct integration. The claim's falsifiable before→after was already measured live by the round-20 wave's seat-16 reproduction (`chain heading anchors match headings inside fences`); the fix shape was validated by that wave's design seats.

## Deviations and honesty notes

- **No wave**: the claim's evidence existed before dispatch — the round-20 wave already proved the defect live and designed the fix shape. Dispatching a wave for it would burn provider quota for a fix that was already measured and designed.
- **The fix is a different function than `load_sections`**: `chain_anchor_at` is the anchor matcher, not the section parser — the wave correctly identified it as a separate site needing its own fence tracking.
- **Loop 1 closes here**: rounds 12–23 all admitted. Loop 2 begins at round 24.
