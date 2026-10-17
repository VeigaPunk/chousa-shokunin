# chousa-shokunin — 調査

**Deep-research method.** The reusable craft of framing a question,
ranking sources, following a citation chain, and verifying a claim
against the source you actually opened.

A **shokunin lane**: an expert agent for one domain, minted and trained
under the [shokunin skill](https://github.com/VeigaPunk/shokunin).
Rank: **shonen**. Promotion is a named non-author review of
[`SHONEN.md`](SHONEN.md), never self-attestation.

This lane answers: *can this claim be followed, hop by hop, to a local
artifact whose bytes still contain the span — and what happens when they
don't?*

## Domain

From [`PROVINCE.md`](PROVINCE.md): question framing; source hierarchy
(primary / secondary / aggregator / unsourced); citation chaining;
claim-vs-source verification; search-strategy taxonomy; the
external-target approval table. The hierarchy itself is this lane's
working standard, not an inherited law — see the provenance note in
[`SKILL.md`](SKILL.md).

**Refuses:** bounty-program scope (→
[kasegi](https://github.com/VeigaPunk/kasegi-shokunin)); model-quality
claims (→ [kengaku](https://github.com/VeigaPunk/kengaku-shokunin));
orchestration (→ [kumitate](https://github.com/VeigaPunk/kumitate-shokunin));
external live-target research without operator approval (loopback-only
otherwise); secret values (shape-only; custody →
[kagi](https://github.com/VeigaPunk/kagi-shokunin)).

A conversion that composes `CLEAN` is a property of the conversion, not
of the original archive. Ship the raw-DRIFT control beside any
conversion-CLEAN. That lesson is
`corpus/lessons/2026-10-16-verifying-conversion-not-original.md`.

## What's here

| Path | Role |
|---|---|
| [`SKILL.md`](SKILL.md) | method decision table, error patterns, gate modes |
| [`PROVINCE.md`](PROVINCE.md) | domain and refusals |
| [`tools/research-gate.sh`](tools/research-gate.sh) | research-record method gate |
| [`corpus/fixtures/`](corpus/fixtures/) | claims, chains, sweeps, integrity, archive conversions, negative controls |
| [`corpus/knowledge/`](corpus/knowledge/) · [`corpus/lessons/`](corpus/lessons/) | sourced notes and per-round lessons |
| [`corpus/evidence/`](corpus/evidence/) | run receipts |
| [`SCORECARD.md`](SCORECARD.md) · [`LOG.md`](LOG.md) · [`SHONEN.md`](SHONEN.md) | axes, trail, promotion |

## The gate

```sh
bash tools/research-gate.sh --help
bash tools/research-gate.sh --selftest
bash tools/research-gate.sh verify-all [RECORD] --claims PATH
bash tools/research-gate.sh verify-claims [CLAIMS]
bash tools/research-gate.sh verify-chain [RECORD]
bash tools/research-gate.sh verify-sweeps [RECORD]
bash tools/research-gate.sh verify-integrity [RECORD]
```

Verdict: `RESEARCH_GATE: CLEAN|DRIFT`. Exit `0` / `1` / `2`. Sources are
local files only; URLs are refused, never fetched. Spans must appear
verbatim at token boundaries.

## How a lane learns

Append-only corpus; every claim separates observation / inference /
unknown; rounds are non-author-verified. See the fleet
[README](https://github.com/VeigaPunk/shokunin#readme).
