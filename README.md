# chousa-shokunin — 調査

The question this lane answers is how a research question is framed, which sources outrank which, how a citation chain is followed, and how a claim is checked against the source that was actually read (`SKILL.md`, `PROVINCE.md`).

**Rank:** `SKILL.md` frontmatter says `Rank: shonen`. `SHONEN.md` is a promotion checklist and every box is `[ ]`. `MINT.md` says the roster row is withheld until probation rounds are verified. That is not a promotion.

## Owns / refuses

Owns question framing, the source hierarchy this lane constructed (primary, secondary, aggregator, unsourced), citation chaining, claim-versus-source verification, the search-strategy taxonomy, the external-target approval table, and this lane's corpus and gates (`PROVINCE.md`, `SKILL.md`).

Refuses bounty-program scope (kasegi), model-quality claims (kengaku), orchestration and agent lifecycle (kumitate), external live-target research without an operator approval table (loopback-only otherwise), and secret values (kagi holds custody; this lane is shape-only). Out of province is reported, not absorbed.

## Start here

The hermetic gate self-test, from `tools/research-gate.sh` and the `SKILL.md` gates table:

```sh
bash tools/research-gate.sh --selftest
```

The script prints `RESEARCH_GATE_SELFTEST: PASS (N cases)` or `FAIL`. The gates table records the current self-test as `PASS (85 cases)`. `verify` writes nothing; the self-test uses its own temp directory and does not use the network (`SKILL.md`).

A record check is `bash tools/research-gate.sh verify <record> --root ..`. Exit `0` is `RESEARCH_GATE: CLEAN`, `1` is `DRIFT`, `2` is setup or usage. Other modes (`verify-claims`, `verify-chain`, `verify-sweeps`, `verify-integrity`, `verify-all`, `--pin`, `--drift`) are named in that same gates table.

## How to read the corpus

`corpus/README.md` is the coverage map (lessons, knowledge notes, and the fixture pairs). It is line-cited from the craft record, so this front door does not insert lines into it. Read the map from the top, then open the note it names. `corpus/QUALITY.md` is the admission bar. `corpus/evidence/` holds receipts. `corpus/fixtures/` holds the pre-registered controls.

## Map

| Path | What it is |
|---|---|
| `PROVINCE.md` | Domain boundary |
| `SKILL.md` | Decision table, error patterns, gate registry |
| `SHONEN.md` | Promotion checklist, boxes unchecked |
| `MINT.md` | Why the lane exists; roster row withheld |
| `LOG.md` | Append-only round record |
| `SCORECARD.md` | Axis verdicts |
| `AGENTS.md` | Lane operating rules |
| `corpus/` | Knowledge, lessons, fixtures, evidence |
| `tools/research-gate.sh` | The research gate |
| `.ufo/` | Round machinery for this lane |

## Neighbors

kasegi (program rules and claim packages), kengaku (model quality), kumitate (dispatch), kagi (secret custody). Contested scope is reported (`PROVINCE.md`).

Fleet protocol: [VeigaPunk/shokunin](https://github.com/VeigaPunk/shokunin).
