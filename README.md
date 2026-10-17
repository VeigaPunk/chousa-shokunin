# chousa-shokunin — 調査

The deep-research method. This lane answers how a question is framed,
which source outranks which, how a citation chain is followed, and how a
claim is checked against the source it names.

Rank: **shonen**. Promotion checklist: [`SHONEN.md`](SHONEN.md). Every
box still open; a lane does not check its own boxes.

Fleet: [shokunin](https://github.com/VeigaPunk/shokunin).

## The question

> Is this claim pointed at a source that was actually read, at the hop the
> citation names?

The hierarchy this lane works with — primary, then secondary, then
aggregator, then unsourced — is the lane's own working standard. `SKILL.md`
records that it was constructed here, and that a row whose only warrant is
the decision table stays a proposal until a real artifact cites it.

## Boundary

**Owns:** question framing, source hierarchy, citation chaining and hop
resolution, claim-vs-source verification, search-strategy taxonomy, the
external-target approval table, and this lane's corpus and gates.

**Hands off:** bounty-program scope and claim packages (kasegi); model
quality (kengaku); orchestration and agent lifecycle (kumitate); secret
values (kagi — shape only here). External live-target research waits for
operator approval. Loopback is the default.

Out of province is reported, never absorbed. Full text:
[`PROVINCE.md`](PROVINCE.md).

## Run the gate

From this repository:

```sh
bash tools/research-gate.sh
```

`tools/research-gate.sh` validates a Markdown research record: a declared
question, ranked sources, chain hops resolved or marked, pointed claims,
kept rejections, negative sweeps. Verdict line `RESEARCH_GATE: CLEAN|DRIFT`.
Exit `0` clean, `1` drift, `2` setup or usage. The header in that file is
the contract, including the claims, chain, sweeps, integrity, and
verify-all modes.

## Map

| Path | What it is |
|---|---|
| [`SKILL.md`](SKILL.md) | decision table, error patterns, checklists |
| [`PROVINCE.md`](PROVINCE.md) | owned surfaces and refusals |
| [`corpus/`](corpus/) | knowledge, lessons, fixtures, evidence, `QUALITY.md` |
| [`corpus/README.md`](corpus/README.md) | coverage index |
| [`LOG.md`](LOG.md) | round audit trail |
| [`SCORECARD.md`](SCORECARD.md) | axis verdicts |
| [`MINT.md`](MINT.md) | why this lane exists |
| [`.ufo/`](.ufo/) | round reports |

## How a round lands

One axis-move. A non-author verifier. Verdicts in `SCORECARD.md`, the
story in `LOG.md`. Append-only corpus: a correction is a new block, and
a rejection stays in the record.
