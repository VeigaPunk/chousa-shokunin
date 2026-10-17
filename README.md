# chousa-shokunin — 調査

**The reusable craft of source research.**

A **shokunin lane** minted and trained under the
[shokunin](https://github.com/VeigaPunk/shokunin) skill. Chousa owns *how*
a question is framed, which sources outrank which, how a citation chain
is followed, and how a claim is checked against the source itself — not
the subject matter of any other lane.

**Wiki:** [lane overview](https://app.devin.ai/org/veigapunk/wiki/VeigaPunk/chousa-shokunin?branch=master)

## Domain

From `PROVINCE.md` and `SKILL.md`:

- question framing
- source hierarchy (primary / secondary / aggregator / unsourced)
- citation chaining and hop resolution
- claim-vs-source verification
- search-strategy taxonomy
- the external-target approval table for a research window
- this lane's own corpus and gates

A research window without an approval table is **loopback-only**. The
approval table is itself a chousa deliverable.

## What it refuses

| Out of province | Owner |
|---|---|
| bounty-program scope and claim packages | [kasegi](https://github.com/VeigaPunk/kasegi-shokunin) |
| model-quality or evaluation claims | [kengaku](https://github.com/VeigaPunk/kengaku-shokunin) |
| orchestration, multi-agent dispatch, agent lifecycle | [kumitate](https://github.com/VeigaPunk/kumitate-shokunin) |
| secret values in any record | [kagi](https://github.com/VeigaPunk/kagi-shokunin) (shape-only here) |
| external live-target research without operator approval | operator |

Out of province → report, never absorb.

## In this repository

```
PROVINCE.md     owned boundary and refusals
SKILL.md        decision table, error patterns, checklists
SHONEN.md       promotion checklist (deleted on promotion)
SCORECARD.md    axis verdicts
LOG.md          append-only audit trail
MINT.md         mint record (2026-10-14)
corpus/         knowledge/, lessons/, fixtures/, evidence/, QUALITY.md
tools/
  research-gate.sh    claim / chain / sweep / integrity gate
```

## Run the research gate

From this repository root:

```bash
bash tools/research-gate.sh --selftest
```

`verify` grades a research record. The gate must never echo planted secret
material; the selftest includes a secrecy case for that. Exit 0/1/2 —
CLEAN / DRIFT / setup or policy failure.

A stranger can also replay the three archived baseline exports named in
`SCORECARD.md` (read-only under the fleet-root research tree) through
`tools/research-gate.sh verify`.

## How a lane learns

Append-only corpus; every claim separates observation / inference /
unknown; rounds are non-author-verified. See the fleet
[README](https://github.com/VeigaPunk/shokunin#readme).
