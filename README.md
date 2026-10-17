# chousa-shokunin — 調査

The craft of **source research**: how a question is framed, which source
outranks which, how a citation chain is followed, and how a claim is
checked against the words it cites.

This is the method, kept as a shonen lane. It is the research gate and
the corpus behind it. Bounty programs, model-quality claims, and
multi-agent dispatch belong to other lanes.

## The job

`PROVINCE.md` gives this lane question framing, source hierarchy
(primary, secondary, aggregator, unsourced), citation chaining and hop
resolution, claim-versus-source verification, a search-strategy taxonomy,
and the approval table for a research window. The executable form is
`SKILL.md`. The record of what has been admitted is `corpus/`.

It refuses bounty-program scope and claim packages (kasegi), model-quality
or evaluation claims (kengaku), orchestration and agent lifecycle
(kumitate), and secret values in any record (kagi keeps custody; this
lane keeps shape only). External live-target research waits for operator
approval; otherwise the gate stays on loopback. Work outside the province
is reported, and left where it belongs.

## Read this first

1. [`PROVINCE.md`](PROVINCE.md) — the boundary.
2. [`SKILL.md`](SKILL.md) — the decision table and the modes.
3. [`corpus/README.md`](corpus/README.md) — the coverage map, round by round.
4. [`LOG.md`](LOG.md) and [`SCORECARD.md`](SCORECARD.md) — what was claimed, and how it was judged.

## Check a research record

`tools/research-gate.sh` validates a Markdown research record: a declared
question, ranked sources, chain hops resolved or marked, pointed claims,
kept rejections, negative sweeps. It also enforces the hard bounds on
external fetch, secrecy, and session paths.

```sh
bash tools/research-gate.sh --selftest
```

A record run prints one verdict, `RESEARCH_GATE: CLEAN` or `DRIFT`, and
exits 0, 1, or 2 (2 is setup or usage). The header of the script lists
the modes — claims, chain, sweeps, integrity, verify-all, pin/drift —
and the finding ids. `--selftest` is the hermetic proof; it is the right
first command in a checkout that has no research record of its own yet.

## On disk

| Path | Role |
|---|---|
| `SKILL.md` | Operating manual. Frontmatter names the triggers and the anti-triggers. |
| `PROVINCE.md` | Owned surfaces and refusals. |
| `SHONEN.md` | Promotion checklist. Still present: rank is shonen. |
| `MINT.md` | Why the lane was minted. |
| `corpus/` | Knowledge, lessons, fixtures, evidence. Append-only. |
| `tools/research-gate.sh` | The method gate. |
| `LOG.md`, `SCORECARD.md` | Audit trail and axis verdicts. |

## Fleet

Protocol and roster: [shokunin](https://github.com/VeigaPunk/shokunin).
This repository is a sibling lane. It is not an object in the fleet
root's `MANIFEST.json` `roster` array (13 ids, ending at `kaidoku`,
read 2026-10-17). Rank **shonen**.
