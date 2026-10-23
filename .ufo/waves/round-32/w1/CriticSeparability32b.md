# CriticSeparability32b — C1/C2 separability review

Axes: **operability** (manifest append serialization) and **coverage** (exempt-hop citation audit). This is a static critic review, not an admission or canonical-runtime judgment. Read `corpus/evidence/round32/claims.md` first, then both frozen counter docstrings. Below, `G` means `tools/research-gate.sh`, `C1`/`C2` mean `corpus/evidence/round32/c1-count.py` / `c2-count.py`; line numbers refer to the fingerprinted inputs below.

## Can the other claim move a counter?

- **C1-only → C2:** [INFERENCE] A valid patch confined to `verify_all`'s JSON setup/append cannot change the C2 hop score: C2 invokes only `verify-chain`, without `--json` (`C2:262-265`); dispatch goes directly to `verify_chain` (`G:6961-6964`), not `verify_all` (`G:6977-6980`). Thus the frozen expected separator is **84/120**, not an observed result of this review (`claims.md:83-97`). Adding an unconditional dependency check or breaking shared shell parsing would break this conclusion, but would be an out-of-surface operability defect, not a legitimate C1 coverage improvement.
- **C2-only → C1:** [INFERENCE] A patch confined to the `verify_chain` exempt arm cannot repair C1's append behavior. C1 generates a one-row claims JSONL (`C1:89-99`) and launches `verify-all … --json` (`C1:113-119`). `verify_all` recognizes that JSONL and does not enable the chain section (`G:3079-3089,3133-3139`). Its integrity invocation also has no Chain rows to traverse (`G:2372-2389`). The unlocked append remains `G:3192-3202`.
- **Do not claim numerical invariance for C1.** [INFERENCE] Its twelve free-writer trials still race (`C1:31,238-245`), so `k` may differ without a C1 fix; a seed controls fixtures/order, not process scheduling (`C1:265,287-295`). Without a manifest flock, every locked trial either modifies the held manifest or misses the lock deadline (`C1:210-226`); successful execution therefore cannot reach 24/24 merely through C2. The required separator is **below 24**, not a promise to reproduce the disclosed 8/24 (`claims.md:42-44,94-97`). No such candidate result was measured here.
- **Identity is not score.** Both receipts fingerprint the whole gate (`C1:309-316`, `C2:307-315`); C1's manifest also contains `gate_sha256` (`G:3161-3162,3182-3184`). Either edit changes that provenance field even on the other command. C1's manifest matcher checks framing, object count and schema, not an unchanged gate hash (`C1:157-195`); C2 scores observed labels/finding ids (`C2:268-289`). A changed fingerprint must not be presented as counter movement or as evidence of unchanged bytes.

## Exact edit boundaries

| Base region | What it is | Required relation to C1/C2 |
|---|---|---|
| `G:3060-3072` | `verify_all` JSON-only setup: parent-directory, existing regular-file, and nonempty-manifest readability checks. | C1 may need narrowly related open/lock/validation plumbing here; preserve these refusals. It need not change this region if the append fix is self-contained. C2 has no reason to touch it. |
| `G:3185-3203` | JSON delimiter comment, last-byte probe, optional newline prefix, append and append-failure exit. | C1's required implementation surface. The opened manifest's exclusive flock must cover both probe and append, retaining inode and existing bytes (`claims.md:23-28`). Keep unrelated section selection/roll-up unchanged. |
| `G:1880-1883` | `verify_chain`'s current combined exemption arm: all five statuses increment exempt and emit one exempt CHAIN line without reading the citation. | C2's required surface. Distinguish U = unresolved/blocked-no-fetch/labelled-dead from rejected/not-applicable. Only a U citation that verifies under existing resolved semantics becomes resolvable/mismatch with the one new finding (`claims.md:60-70`). |
| `G:1027-1046`, especially `1035-1040` | `verify_record`'s structural/metadata chain checks: unresolved/blocked-no-fetch require notes; rejected/labelled-dead/not-applicable are accepted structurally. This is not the source-anchor reader. | **C2 need not and should not touch it.** The gate explicitly distinguishes structural `verify` from citation `verify-chain` (`G:93-98`). Adding the audit here would create another authority; `verify_all` runs both structural and chain sections (`G:3087-3089,3135-3137`). |
| `G:2152-2155` | `verify_sweeps` exempts sweep/negative-search rows by status before location parsing. Not Chain hops. | **C2 must not repurpose it.** Existing `sweeps-pass` expects an empty-location blocked-no-fetch sweep to remain exempt (`G:4477,4489-4497`). |
| `G:2380-2388`, especially `2383` | `verify_integrity` marks Chain **reference tokens** exempt by declared status before cross-section id checking. It does not verify citation anchors. | **C2 need not and should not touch it.** A resolvable citation finding does not redefine whether declared cross-references are exempt in this separate mode. |
| `G:2403-2416`, especially `2412` | Integrity reference-token exemptions for **Negatives** rows. | **No C2 change.** Different row class and observable (`REF`, not `CHAIN`). |
| `G:2418-2431`, especially `2427` | Integrity reference-token exemptions for **Sweeps** rows. | **No C2 change.** Same status spellings do not make this the exempt-hop audit. |

For C2, reuse the existing citation parser (`G:1646-1686`), declared-source-id resolution semantics (`G:1837-1854`), guarded local-source resolution (`G:1167-1270`) and anchor matcher (`G:1689-1734`), rather than introducing another parser or raw anchor grep. The guarded resolver refuses URLs without fetching (`G:1181-1184`). Failed U probes must remain quiet; invoking the resolved arm's failure-emitting behavior wholesale would violate `claims.md:65-68`. Rejected/not-applicable must remain unread. The existing `emit_finding` supplies warn/crit drift (`G:415-425`). These are implementation constraints, not inspected candidate behavior.

## Strongest local counterexamples and smallest safe correction

1. **A global edit of matching status arms can pass the cross-counter separators yet regress another authority.** The existing `integrity-exempt-counted` fixture contains `from=C9`, `to=S7`, `status=blocked-no-fetch`, no anchor, and neither id is declared (`G:4941-4954`). Its committed expectations are CLEAN with those two references exempt (`G:4956-4962`; expectations opened, not executed). [INFERENCE] Removing the U exemption at `G:2383` would make those tokens unresolved through `G:2307-2315`, emit `REF_UNRESOLVED` at `G:2295-2297`, and drift at `G:2445`. Neither cross-counter exercises that integrity fixture. **Impacted axes:** coverage fidelity and operability/no-harm. **Smallest safe correction:** change only the `verify_chain` exempt behavior, preserving structural, sweeps and integrity status arms. Such a broadened edit would be a fixable scope/no-harm defect, not a coverage-versus-operability tradeoff to waive because a separator holds.
2. **The commands are not globally independent.** C2's generated record has `## Chain` plus resolvable U citations (`C2:174-184,224-231`). [INFERENCE] Running `verify-all` on such a record would invoke `verify-chain` and propagate C2's findings/verdict/counts into its JSON manifest (`G:3087-3089,3133-3146,3152-3155,3173-3184`). Thus “C2 never changes verify-all output” would be false; only the particular **C1 counter's claims-only surface** is isolated. **Impacted axes:** both, through aggregation. **Smallest safe correction:** qualify the separability statement to the frozen counters and retain the normal aggregation; do not suppress chain findings to manufacture broader independence.

No frozen predicate/counter amendment is warranted by this static review. The separators in `claims.md:94-97` are cross-predicate checks, not complete no-harm evidence. Their candidate receipts remain for L1 only after the control receipts are committed, under the assigned pre-data rule. Round-31 R1–R6 remain separate repairs (`claims.md:10-12`; `corpus/lessons/round-31-verifier-spotcheck.md:201-234`).

## Evidence, commands and limits

Executed from the lane root:

```text
timeout 20s sha256sum tools/research-gate.sh corpus/evidence/round32/claims.md corpus/evidence/round32/c1-count.py corpus/evidence/round32/c2-count.py
```

Exit 0; output:

```text
0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258  tools/research-gate.sh
b6641e862c5d7b89df61f45daea7e67702ad1054eb547a7375534814764dfa26  corpus/evidence/round32/claims.md
9e787e80b215f6522335c639d5e1b2e60d0a5812b83a9760daf8be9f78415885  corpus/evidence/round32/c1-count.py
b6626b2cb81b2aeaf66a8ff11a06c030612bf4e264dc128f290021c4aa71f54c  corpus/evidence/round32/c2-count.py
```

Also executed `timeout 10s mkdir -p /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CriticSeparability32b`, exit 0, no output. Source evidence was opened with ranged `read` and targeted `grep`, as cited above.

Zero scratch probes; no gate/counter/selftest execution, no candidate inspection/scoring, no receipts, no network, no installs, no production/index/jj changes, no processes left running. This report is the only file written. All predicted execution effects are marked [INFERENCE]; committed selftest expectations are not claimed as exercised passes.
