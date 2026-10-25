# Auditing chain hops marked "could not be followed" (round 32)

source: S061 (RFC 9110 §15.5.5 and §15.5.11, 404 and 410 semantics); contract
`corpus/evidence/round32/claims.md` §C2 (design v2); frontier `corpus/README.md` Frontier, Round 3 paragraph
verified-at: 2026-10-23 (round-32 gate; counter receipts under `.ufo/waves/round-32/measure/`)
recheck: on-release (from the lane root: `python3 corpus/evidence/round32/c2-count-v2.py --seed <n>`; keep `C2_TMP` outside the gate's lane root)

## The gap

A `## Chain` hop records how a citation was followed. Until round 32 `verify-chain` read only
`resolved` hops. A hop marked `unresolved`, `blocked-no-fetch`, `labelled-dead`, `rejected` or
`not-applicable` was exempt and never read, so a record could say a hop could not be followed while
its cited anchor sat in a local source under the boundary. Round 3 named this: "exemption is
record-declared and unverifiable".

S061 (RFC 9110) defines what a server can say about availability: a 410 says the target resource
is no longer available at the origin server, and a 404 does not say whether an absence is
temporary or permanent. Both statements are about the origin server. **[INFERENCE]** (lane
reasoning, not in the RFC): a hop label such as "could not be followed" therefore says something
about one access path, and whether the cited text sits in a local copy is a separate question the
gate can answer without a network read.

## The audit

For hops marked `unresolved`, `blocked-no-fetch` or `labelled-dead`, `verify-chain` now applies the
same citation, source, boundary and anchor rules it applies to `resolved` hops, silently. If the
citation would verify, the hop prints `observed=resolvable`, verdict `mismatch`, and exactly one
`FINDING CHAIN_EXEMPT_RESOLVABLE severity=warn`, and the record drifts. Every other such hop stays
`observed=exempt` with no finding: no citation, an external URL (never fetched), a missing file, an
undeclared id, a path outside the corpus, or an anchor that is not found. `rejected` and
`not-applicable` are not read: they record a judgment, not an unavailability. The summary line
gains a `resolvable=N` count at its end.

## What a finding means

The record says the hop could not be followed, and the gate followed it locally. Reconcile the
record: either the status is stale (re-mark the hop `resolved`) or the local copy is not the source
the hop meant (say so in the notes). The finding is not a judgment that the source supports the
claim. **[INFERENCE]** reading guidance, not measured.

## How it is measured

`corpus/evidence/round32/c2-count-v2.py` writes one record with 132 hops in 16 classes: 36 audited
hops whose citation resolves (fragment quote, path with anchor columns, declared id), 12 resolved
hops, 12 judged hops (`rejected`, `not-applicable`) that would resolve, and 72 audited hops that must
stay exempt — among them anchors present only glued to another word, as a plain line instead of a
heading, as a line prefix, only in upper case, or only with doubled spaces, so a reader looser than
the resolved path fails. The record must drift with exactly one DRIFT summary and exit 1, and no
finding may be duplicated or name an unknown hop.

## Limits

- One hop at a time; no transitive tracing.
- URL sources stay unread, so a hop marked `blocked-no-fetch` with a URL is never challenged.
- The counter's classes are synthetic; the corpus records were checked separately and none flips
  (`.ufo/waves/round-32/w1/ScoutExemptCorpus32.md`).
