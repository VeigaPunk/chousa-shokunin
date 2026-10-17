# chousa-shokunin — 調査

**Deep-research method.** How a question is framed, which sources outrank
which, how a citation chain is followed, and how a claim is verified
against its source.

This is a [shokunin](https://github.com/VeigaPunk/shokunin) lane — a
domain specialist trained by verified rounds, not a generalist that
absorbs every research-shaped request. Rank: shonen.

Chousa owns the *method*. It does not own bounty-program scope (that is
[kasegi](https://github.com/VeigaPunk/kasegi-shokunin)) and it does not
own model-quality claims (that is
[kengaku](https://github.com/VeigaPunk/kengaku-shokunin)).

## What this lane answers

| Intent | Correct move | Never |
|---|---|---|
| Research a question | Frame the question, then rank sources, then chain, then check claims | Start from a search box with no question |
| Rank sources | primary > secondary > aggregator > unsourced | Treat an aggregator as a primary |
| Follow a citation | Resolve each hop at the cited artifact | Stop at a summary of the citation |
| Verify a claim | claim → source → the source's own evidence | Accept a restatement as the source |
| Reuse a finding | Cite the artifact and the revision read | Cite a memory of it |

The hierarchy is this lane's working standard
(`SKILL.md`, provenance note 2026-10-15). Treat a row whose only warrant
is the skill table as a `proposal` until it carries a `path:line` from a
real artifact.

## Province

**Owns:** question framing; source hierarchy; citation chaining and hop
resolution; claim-vs-source verification; search-strategy taxonomy; the
external-target approval table for a research window; this lane's own
corpus and gates.

**Refuses:** bounty-program scope and claim packages (→ kasegi);
model-quality or evaluation claims (→ kengaku); orchestration,
multi-agent dispatch and agent lifecycle (→ kumitate); external
live-target research without operator approval (loopback-only otherwise);
secret values in any record (→ kagi for custody; shape-only here).

Out of province → report, never absorb. Full boundary:
[`PROVINCE.md`](PROVINCE.md).

## Start here

1. [`SKILL.md`](SKILL.md) — decision table, error patterns, checklists.
2. [`PROVINCE.md`](PROVINCE.md) — owned surfaces and refusals.
3. [`corpus/README.md`](corpus/README.md) — coverage map of admitted notes.
4. [`tools/research-gate.sh`](tools/research-gate.sh) — the executable method.

## The research gate

`tools/research-gate.sh` grades Markdown research records: a declared
question, ranked sources, chain hops resolved-or-marked, pointed claims,
kept rejections, negative sweeps. It hard-bounds external fetch, secrecy,
and session paths.

```
bash tools/research-gate.sh --selftest
# RESEARCH_GATE_SELFTEST: PASS (N cases)

bash tools/research-gate.sh verify-all <record.md> --claims <claims.jsonl>
# RESEARCH_GATE: CLEAN | DRIFT
```

Exit `0` CLEAN, `1` DRIFT, `2` setup/usage. Modes include
`verify-claims`, `verify-chain`, `verify-sweeps`, `verify-integrity`,
`verify-all`, plus `--pin` / `--drift` for the gate's own behavioral
baseline. A CLEAN composed run covers only the sections that ran;
absence is reported, not treated as clean. See
`corpus/knowledge/verify-all-r6.md` and
`corpus/knowledge/reference-integrity-r7.md`.

## What's in the repo

```
chousa-shokunin/
├── SKILL.md          executable craft
├── PROVINCE.md       domain boundary
├── SHONEN.md         promotion checklist (deleted on promotion)
├── MINT.md           why this lane was minted
├── LOG.md            append-only audit trail
├── SCORECARD.md      axis verdicts
├── AGENTS.md         operating rules
├── tools/            research-gate.sh
└── corpus/           knowledge/, lessons/, fixtures/, evidence/, QUALITY.md
```

Protocol: append-only corpus; every claim separates observation /
inference / unknown; rounds are non-author-verified. See the fleet
[README](https://github.com/VeigaPunk/shokunin#readme) for how a lane
learns.
