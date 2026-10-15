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

**Provenance of the table above (appended 2026-10-15).** The primary > secondary >
aggregator > unsourced tiers are **this lane's own construction**, not a rule
inherited from another lane and not a statement the survey exports make — an
independent audit measured zero `proposal` tokens and zero independently cited
admissions in this skill at mint. Treat the hierarchy as the lane's working
standard, and any row whose only warrant is this table as a `proposal` until it
carries a `path:line` from a real artifact. The exports state no tier system; the
fleet gates state citation *mechanics* (resolvable, pinned, labelled), not this
ranking.

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

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| `research-gate` | gate | `bash tools/research-gate.sh verify <record> --root ..` | `0` clean (`RESEARCH_GATE: CLEAN`) · `1` failed (`DRIFT`) · `2` could-not-evaluate (setup/usage) | `bash tools/research-gate.sh --selftest` → `RESEARCH_GATE_SELFTEST: PASS (20 cases)` | expected exits/finding IDs in `tools/research-gate.sh`; archive digests/expected verdicts in `corpus/evidence/round-1/expected.json` | verify: zero writes; selftest: its own temp dir; no network | chousa |

**Verified scope, not field readiness.** At gate revision
`31b46832e56a7f095092a4a6d62b74bfaf6933e8`, the real CLI emits exactly one
DRIFT summary and exits 1 on each pinned A/B/C archive. The locally sourced
intake emits CLEAN and exits 0. Full output, exit codes and input/script
digests: `.ufo/evidence/round-1/acceptance.json` and `acceptance.txt`.

The old “unchecked grep” diagnosis is superseded: the non-strict informational
branch of `emit_finding` returned false under CLI errexit. Recording a finding
now returns success; counters determine the verdict. Informational findings
remain non-fatal unless strict mode promotes them; warn/crit findings still
drift. Selftests invoke fresh CLI processes rather than suppressing errexit
around a function call (`corpus/lessons/round-1.md`, integration errata).

**Limits.** CLEAN verifies declared record structure and file-pointer identity,
not source semantics, cited line contents, or domain truth. This gate never
opens or fetches a resolved source. The documented refused provinces above are
not yet enforced by scope finding IDs; the original landing requirement is
named debt in `LOG.md`'s interactive round-1 entry. No non-author corpus
spot-check or promotion is implied by a passing selftest.
