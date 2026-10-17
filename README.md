# chousa-shokunin — 調査

**Deep-research method.** How a question is framed, which sources outrank
which, how a citation chain is followed, and how a claim is checked against
the artifact it cites — not the topic being researched, the *method*.

This is a **shokunin lane** of the [shokunin fleet](https://github.com/VeigaPunk/shokunin):
one province, one skill, one corpus, iterated by verified craft rounds.
Rank: **shonen** (probation; roster row withheld in `MANIFEST.json` until
the protocol bar is met).

## The craft

Chousa (調査) owns the reusable research method:

- **Question framing** — start from a declared question, never a search box.
- **Source hierarchy** — primary > secondary > aggregator > unsourced claim.
  The tiers are this lane's working standard (`SKILL.md`); treat a row whose
  only warrant is the table as a proposal until it carries a `path:line`.
- **Citation chaining** — follow each hop to the cited artifact and resolve
  its anchor there. Stopping at a summary is a broken chain.
- **Claim-vs-source verification** — verified / contradicted / unresolved.
  Two sources that disagree are both reported; they are never averaged.
- **Negative claims** — a "not found" carries the sweep that looked, naming
  where.

Every claim in this repo is supposed to carry a resolvable pointer to the
artifact and revision that was read. Observation, inference, and unknown
stay separate. A rejected source is kept, with a reason and a flip-condition.

## Province

Owns: question framing; source hierarchy; citation chaining and hop
resolution; claim-vs-source verification; search-strategy taxonomy; the
external-target approval table for a research window; this lane's own
corpus and gates.

**Refuses** (report, never absorb):

- bounty-program scope and claim packages → [kasegi](https://github.com/VeigaPunk/kasegi-shokunin)
- model-quality or evaluation claims → [kengaku](https://github.com/VeigaPunk/kengaku-shokunin)
- orchestration, multi-agent dispatch, agent lifecycle → [kumitate](https://github.com/VeigaPunk/kumitate-shokunin)
- external live-target research without operator approval (loopback-only otherwise)
- secret values in any record (shape-only; custody → [kagi](https://github.com/VeigaPunk/kagi-shokunin))

See [`PROVINCE.md`](PROVINCE.md).

## What's in this repository

```
chousa-shokunin/
├── SKILL.md          executable method: decision table, error patterns, checklist
├── PROVINCE.md       owned surfaces and refusals
├── SHONEN.md         promotion checklist (non-author [x] only)
├── LOG.md            append-only round trail
├── SCORECARD.md      per-axis verdicts
├── MINT.md           why this lane exists; roster scan; rejected fits
├── AGENTS.md         operating rules for anyone writing here
├── tools/
│   └── research-gate.sh   method gate (claims / chain / sweeps / integrity / verify-all)
└── corpus/
    ├── QUALITY.md    admission bar
    ├── knowledge/    sourced method notes
    ├── lessons/      per-round lessons
    ├── evidence/     receipts
    └── fixtures/     hermetic records the gate replays
```

## Start here

From this repo root:

```sh
bash tools/research-gate.sh --selftest
```

The gate validates Markdown research records: declared question, ranked
sources, chain hops resolved-or-marked, pointed claims, kept rejections,
negative sweeps. It also hard-bounds external fetch, secrecy, and session
paths. Verdict line is `RESEARCH_GATE: CLEAN|DRIFT` (exit 0 / 1); setup
or usage errors exit 2.

Modes documented in `SKILL.md` include claims, chain, sweeps, integrity,
verify-all, and pin-drift. A negative claim without a named sweep is a
defect, not a finding.

Then read [`SKILL.md`](SKILL.md) as the operating manual and
[`corpus/`](corpus/) as the craft record.

## How a round works

One axis-move against `depth` / `coverage` / `operability` / `freshness` /
`calibration` / `adjacency`. Declare a falsifiable before→after, land one
verifiable improvement, judge every axis, append `LOG.md` + `SCORECARD.md`.
A round admits only if at least one axis improved and none were harmed.
Lane identity on commits: `chousa-shokunin <chousa@shokunin.local>`.

## Fleet

Protocol, roster, and round history live in
[VeigaPunk/shokunin](https://github.com/VeigaPunk/shokunin). The portable
Kimi plugin is [kimi-shokunin](https://github.com/VeigaPunk/kimi-shokunin).
