# chousa-shokunin — 調査

The craft of source research, made into a gate.

Chousa answers a narrow question: does this research record do what it
claims — a question, ranked sources, citation hops that resolve, claims
whose spans are actually in the cited file, rejections that say how they
would flip, sweeps that are empty where they say they are? A clean record
is a property of that structure. It is not a proof that the world is as
the prose says.

Rank: **shonen**. `SHONEN.md` is still here. `MANIFEST.json` in the fleet
root minted this lane on 2026-10-14 and withheld the roster row.

## Province

**Owns.** Question framing. Source hierarchy (primary, secondary,
aggregator, unsourced). Citation chaining and hop resolution.
Claim-versus-source verification. Search-strategy taxonomy. The
external-target approval table for a research window. This lane's corpus
and gates.

**Hands off.** Bounty-program scope and claim packages (kasegi). Model
quality (kengaku). Orchestration and agent lifecycle (kumitate). External
live-target research without operator approval — loopback only otherwise.
Secret values in any record (kagi keeps custody; this lane keeps shape).

The full boundary is `PROVINCE.md`.

## Start here

1. `PROVINCE.md` — the boundary, one page.
2. `corpus/README.md` — the coverage map: which note holds which mode.
3. `SKILL.md` — the distilled method.
4. `tools/research-gate.sh` — the instrument. The header states the
   verdict line and the exit map.
5. `SCORECARD.md` and `LOG.md` — axis claims and the append-only trail.
   A later entry corrects an earlier one by pointing at it.

## The tree

| Path | What it is |
|---|---|
| `tools/research-gate.sh` | The research-record gate |
| `corpus/knowledge/` | One note per mode the gate learned |
| `corpus/lessons/` | What a CLEAN result does and does not establish |
| `corpus/fixtures/` | Pre-registered records, including the archive conversions and their negative controls |
| `corpus/evidence/` | Receipts for those runs |
| `corpus/QUALITY.md` | The admission bar |
| `MINT.md` | Why this lane exists |

## Run the gate

From the repository root:

```sh
bash tools/research-gate.sh --help
bash tools/research-gate.sh --selftest
```

The script's own header is the contract: one `RESEARCH_GATE: CLEAN|DRIFT`
summary when a record is actually evaluated, exit 0 / 1 / 2. `--selftest`
prints `RESEARCH_GATE_SELFTEST`. A CLEAN on a converted archive record
verifies the conversion and the spans you selected. `corpus/lessons/`
keeps the rounds that measured that difference.

## How to read a score

`SCORECARD.md` binds each number to a counting command. The card itself
says the missing-at-baseline sheet started with one measured axis and
refused to invent the other five. Trust the latest entry's command, then
re-run it.

## Fleet

Minted under [shokunin](https://github.com/VeigaPunk/shokunin). Contested
scope is reported, never absorbed.
