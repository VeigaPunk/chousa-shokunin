# Auditing exempt citation-chain hops — round 32

source: `S0XX-c2` — reserved citation slot for the C2 SOURCES row (not yet present); local contract `corpus/evidence/round32/claims.md` §C2 and counter contract `corpus/evidence/round32/c2-count.py`; current behavior anchor `tools/research-gate.sh` `verify_chain`
verified-at: 2026-10-23 (draft checked against `corpus/QUALITY.md`, the frozen C2 contract, counter docstring, and current verifier branch; no C2 source row or candidate execution was observed)
recheck: on-release (from the lane root in a checkout with `corpus/` and `tools/` beneath that root, run `python3 corpus/evidence/round32/c2-count.py` against the release gate and compare with the then-current `claims.md` §C2)

## The move

Round 3's frontier records that five exempt hops were counted in the positive chain fixture, but the observable was unsaturated because “exemption is record-declared and unverifiable”; it also limits that observation to one hop at a time, with no transitivity (`corpus/README.md` §Frontier, lines 355–362). In the current gate, `verify_chain` sends `unresolved`, `blocked-no-fetch`, `rejected`, `labelled-dead`, and `not-applicable` through one exempt arm without reading the citation (`tools/research-gate.sh:1880-1882`).

Round 32 C2 proposes auditing just the statuses that say a hop could not be followed. Its frozen contract makes an otherwise resolvable local citation visible as a status mismatch, rather than accepting the record's unavailability label without checking it (`corpus/evidence/round32/claims.md:49-70`). This is a direct-hop consistency check, not transitive citation tracing.

## Contract

Let **U** be `unresolved`, `blocked-no-fetch`, and `labelled-dead`: statuses that say the hop could not be followed (`claims.md:60-61`). For a U hop, apply the same citation test that would run if that row said `resolved`: the citation parses; its source is a declared id with a pointer or a local path inside the boundary; and the anchor is found by the resolved-path check (`claims.md:61-64`).

- If that citation would verify as `resolved`, emit `observed=resolvable` with verdict `mismatch`, exactly one `FINDING CHAIN_EXEMPT_RESOLVABLE severity=warn|crit surface=chain obs=hop=<hop> ...` for that hop, and drift the record (`claims.md:63-65`).
- Other U hops stay `observed=exempt`, with no finding naming the hop. This includes no citation, an external URL, missing file, undeclared id, out-of-corpus path, or absent anchor (`claims.md:65-67`).
- `rejected` and `not-applicable` stay `observed=exempt`, unread, and finding-free regardless of citation: they record a judgment, not an unavailability (`claims.md:67-69`).
- `resolved` hops are unchanged (`claims.md:69-70`).

## What the finding tells a researcher

The finding says that the record declares this hop could not be followed, while the gate can resolve its local citation under the ordinary `resolved` rules. It is a mismatch between the recorded status and the gate-checkable citation, not a judgment that the cited material supports the researcher's claim or that the claim is true (`claims.md:60-70`; `corpus/QUALITY.md:28-31`).

**Researcher interpretation (inference):** inspect the hop's citation and recorded status against what was actually done, then reconcile the record. Do not treat the finding alone as semantic evidence, a finding of intent, or proof that the research conclusion is wrong; none of those is part of the frozen predicate (`claims.md:60-70`).

## Worked cases

These are contract illustrations, not executions.

- A `labelled-dead` hop cites a declared local source and an anchor that the resolved check finds: the expected result is `observed=resolvable`, verdict `mismatch`, and one `CHAIN_EXEMPT_RESOLVABLE` finding (`claims.md:60-65`).
- An `unresolved` hop points to a remote URL: it remains `observed=exempt` and has no finding; the URL is not fetched (`claims.md:65-70`).
- A `rejected` hop has a citation that would otherwise resolve: it remains unread and exempt with no finding, because `rejected` records a judgment rather than inability to follow (`claims.md:67-69`).

## Frozen measure — not run for this draft

C2's frozen P2 requires `EXEMPT_AUDIT_MATCH=120/120` with `predicate_holds=true` on each of two fresh-seed runs on the landed lane revision, and no round-32 run on that revision may print a lower count (`claims.md:72-81`). The counter uses 120 hops and 14 fixed classes (`c2-count.py:9-14,53-76`). This draft did not run the counter; no candidate result or P2 verdict is asserted here.

## Limits

- No network read is added: a URL source stays unread (`claims.md:69-70`). A source fetched later is outside this audit; this check does not fetch it or assess a later-fetched copy. The no-fetch boundary is contractual; the latter scope statement is an inference from that boundary (`claims.md:65-70`).
- The audit concerns the U statuses and local resolvability only. It does not audit `rejected` or `not-applicable`, which remain unread, and it does not trace multiple hops (`claims.md:67-70`; `corpus/README.md:360-362`).
- A finding is not semantic verification or claim truth (`corpus/QUALITY.md:28-31`).
- The 120-hop counter uses fixed synthetic classes; its predicate is evidence for those frozen fixture classes, not a claim that every possible chain-record form is covered (`c2-count.py:9-14,53-76`).
- At the inspected gate implementation, the five statuses still share the exempt arm and no audit is performed (`tools/research-gate.sh:1880-1882`). This entry records the frozen C2 expectation, not landed behavior or an execution result.
- **Citation slot / admission limit:** `S0XX-c2` remains reserved. The inspected SOURCES registry ends at S059 (`corpus/SOURCES.md:67-70`); no C2 row was available to cite. This draft is not an admitted `corpus/knowledge/` entry until the slot is replaced with the actual mined row, its URL or repo path and exact anchor, and its `used-by` names this entry; the row's tier and scope must support the claim (`corpus/QUALITY.md:17-27`).