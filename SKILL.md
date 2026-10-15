---
name: chousa-shokunin
description: "Deep-research method (調査) — question framing, source hierarchy, citation chaining, claim-vs-source verification. Triggers: 'research this', 'deep research', 'verify this claim', 'primary source', 'citation chain'. Anti-trigger: NOT bounty-program scope (kasegi), NOT model-quality claims (kengaku), NOT external live-target fetching without operator approval. Rank: shonen."
---

# chousa-shokunin — deep-research method (調査)

Domain: the reusable METHOD of source research — how a question is framed, which
sources outrank which, how a citation chain is followed, and how a claim is
verified against its source. Not the bounty programs (kasegi) and not model
quality (kengaku).

## Decision table

| Intent | Correct surface | Never | Expected output |
|---|---|---|---|
| Research a question | question framing → source hierarchy → chain → claim check | starting from a search box with no question | a research record with a declared question |
| Rank sources | primary > secondary > aggregator > unsourced claim | treating an aggregator as a primary source | hierarchy row per source |
| Follow a citation chain | follow each hop to the cited artifact | stopping at a summary of the citation | chain with each hop resolved or marked unresolved |
| Verify a claim | claim → source → the source's own evidence | accepting a restatement as the source | verified / contradicted / unresolved |
| Reuse a finding | cite the artifact + the revision read | citing a memory of it | resolvable pointer |

## Error patterns

| Observation | Reading |
|---|---|
| source cited but not read | the claim is unsupported; record as unresolved |
| aggregator quoted as primary | hierarchy violation — re-derive from the primary |
| chain ends at a dead link | chain broken; record the hop and stop |
| two sources disagree | report both; do not average them |

## Boundaries (hard)

- **Refuses external live-target research without operator approval.** A window
  without an approval table is loopback-only. The approval table is itself a
  chousa deliverable.
- **Refuses bounty-program scope** — that is kasegi (program rules, claim packages).
- **Refuses model-quality claims** — that is kengaku.
- **Refuses orchestration and multi-agent dispatch** — swarm waves, agent
  lifecycle, dispatch mechanism are kumitate; a survey that finds such material
  routes it out rather than absorbing it.
- Credentials/session material shape-only; no secret values in any record.

## Checklist (executable)

- [ ] Every claim carries a resolvable pointer to the artifact and revision read.
- [ ] A negative claim carries its search sweep.
- [ ] Observation, inference and unknown stay separate.
- [ ] A rejected source is kept with its rejection reason.

## Gates

`tools/research-gate.sh` — validates a research record against the method
contract (question declared, sources ranked, chain hops resolved-or-marked,
claims pointed). `verify` → `RESEARCH_GATE: CLEAN|DRIFT` exit 0/1, `--selftest`
over fixtures, exit 2 setup/usage.

## Gates

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| `research-gate` | gate | `bash tools/research-gate.sh verify <record>` | `0` clean (`RESEARCH_GATE: CLEAN`) · `1` failed (`DRIFT`) · `2` could-not-evaluate (setup/usage) | `bash tools/research-gate.sh --selftest` → `RESEARCH_GATE_SELFTEST: PASS (17 cases)` | hermetic cases in the script (`/tmp/chousa-research-gate-selftest.*`) | live: zero writes; selftest: its own temp dir; no network | chousa |

**NOT FIELD-READY — named defect.** The suite is green (17/17) but the gate exits
**1 with no verdict line** on a real chat-export input: an unchecked `grep` under
`set -e` terminates the script before the summary prints (reproduced on
`research/deep-research-2026-09-28/A-shokunin-tradition.md`). Two design bugs were
already fixed during landing (a `local` unbound-variable abort that killed 13 of 17
cases, and `ROOT` not honouring `CHOUSA_ROOT` per call). Unblock: guard every `grep`
whose non-match is not fatal with `|| true`, then re-run the suite **and** the real
artifact before treating this row as live.
