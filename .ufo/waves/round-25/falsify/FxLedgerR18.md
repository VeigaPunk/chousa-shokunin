# FxLedgerR18 — Round-18 addendum history attack

Scope: retrospective addendum at `corpus/knowledge/hardening-r10.md:624-629`; read-only review at full checkpoint `e93ac711f885a10d44fdd80a1734997419595b5a` (`git rev-parse HEAD`). No source edits, gate run, or selftest run.

## Reconstructed contract and evidence

- Round 16 named the `LLM benchmarks` scope-phrase gap as a debt queued for round 17 (`corpus/knowledge/verification-r16.md:9-10,26-27`, seat 02). Round 18 selected and closed that debt (`SCORECARD.md:908-912`; `LOG.md:671,679-683`). Its knowledge note states the narrow three-phrase change and residual debts (`corpus/knowledge/scope-phrase-gap-r18.md:3-5,16-33`).
- The historical round-18 gate transition is correct: read-only `git log --format='%H %ad %s' --date=iso-strict -16 -- tools/research-gate.sh` identifies r17 `6e328ce5fe088fa8c4fea96dad67084ce76cdd3b` and r18 `a80964c5a7a1843c06f131d8ed0123345cee145c`; `git show <commit>:tools/research-gate.sh | sha256sum` measured `c2915f24d73d656ca23b7f6228cbdd502c27a8c07670776fed84c70f278266f8` → `6e69488160199cc1704bd1d17b7523cd39022016ad123ecf43575467b266de0c`. This matches the prefixes in `SCORECARD.md:918-931`, `LOG.md:681`, and `hardening-r10.md:628-629`.
- Case attribution is correct: r17 receipt ends at case 116 (`evidence/fence-r17-20261019T171200Z-selftest.log:112-117`); r18 receipt adds 117 `scope-fail-llm-benchmarks`, 118 `scope-fail-llm-scoring`, 119 `scope-pass-benchmark-prose`, then PASS (119) (`evidence/scope-r18-20261019T173000Z-selftest.log:117-120`). `diff -u` between receipts showed only those three appended cases and the updated summary; cases 1–116 were unchanged. Demo receipt shows pre-change CLEAN then `SCOPE_MODEL_QUALITY_ABSORBED`/DRIFT after (`evidence/scope-r18-20261019T173000Z-demo.log:1-8`).

## Divergence / calibration

- E7's `No row/queue delta` (`hardening-r10.md:628-629`) is true only when “queue” means the original §3.9 round-11 audit queue. That queue is explicitly the ledger's row-derived 30 items (`hardening-r10.md:320-322`); the r16 phrase-gap debt is not among them. But R18 did close an item in the separate round-16 named-debt queue (`verification-r16.md:27`; `SCORECARD.md:908-912`). Thus the terse wording can falsely imply that no queue of any kind moved. More exact wording: “No §3 row or §3.9 round-11 queue item moved; the round-16 named-debt item (seat 02) is closed.” This is a wording ambiguity, not a false §3/round-11 count.
- Do not conflate this with §3 row 70: that row is “scope-refusal finding IDs,” already closed in round 12 (`hardening-r10.md:295-300,444-450`), a different claim from the r16 `LLM benchmarks` phrase gap.
- E-number mapping is consistent: E5=round 16, E6=17, E7=18, E8=19 (`hardening-r10.md:612-638`); the gate/case ranges advance without an off-by-one. R19 is also a closure of a different round-16 named debt (seat 20, symlink escape), not an original hardening-ledger row: E8 expressly says no §3 row/§3.9 queue item moved, and its knowledge note calls it round-16 named debt (`hardening-r10.md:635-638`; `knowledge/verification-r16.md:33`; `knowledge/sweep-symlink-r19.md:3-5`). E8 already makes the distinction E7 should state explicitly.

## Append-only and checkpoint provenance

- Comparing base `b820e4e40ce52deedf53b191140cd7b08ddda929` to authoritative full checkpoint `e93ac711f885a10d44fdd80a1734997419595b5a`, `git diff --stat` reports only `corpus/knowledge/hardening-r10.md`, 94 insertions and 1 deletion. The zero-context diff shows the sole edit to prior history is the disclosed line-488 `${GSHA}…` → `6b17e50c…` substitution; the r16–r25 material is appended after the prior final text (around line 601). `git log 6e328ce..a80964c -- corpus/knowledge/hardening-r10.md` and `git diff --check` produced no output. The r18 addendum is retrospective, not a contemporaneous r18 edit.
- Checkpoint note: `corpus/lessons/round-25.md:111-133` records that 0fc037e omitted the gate, d8c8cff corrected the gate but omitted `corpus/evidence/README.md`, and e93ac is the full integration. This review uses e93ac; it makes no current-gate/selftest claim based on the incomplete checkpoints.

Confidence: high on the R18 gate transition, case attribution, E-number mapping, and absence of a §3/round-11 delta; medium-high that E7's unqualified “queue” is materially ambiguous, given the separately evidenced R16 queue closure.

Installs: none.
VERDICT: E7's mapping and §3/round-11 no-delta claim hold; qualify “No row/queue delta” to distinguish the closed round-16 named debt from the unchanged original ledger queue. No E-number correction is warranted.