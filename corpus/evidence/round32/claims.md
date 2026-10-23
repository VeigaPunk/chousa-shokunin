# Round 32 — frozen claims (design v1)

Base `7a7259f0ad41a68068131bfa422a829db9fd1b55` (lane `master`). Gate at base:
`tools/research-gate.sh` SHA-256 `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258`
(the landed round-31 gate). Counters (this commit): `corpus/evidence/round32/c1-count.py`,
`corpus/evidence/round32/c2-count.py`; every receipt records the counter that produced it
(`counter_sha256`). Only receipts carrying the hashes of the counters in the commit that carries
this file count for design v1.

Anti-loop: rounds 29–31 worked `verify-claims` and `tools/quote-reopen.py`. Neither claim below
touches either. The round-31 repairs routed by the outside spot-check (R1–R6) are repairs, not
claims, and are kept out of both counters.

## C1 — operability (lowest scored axis: the only scored axis, `SCORECARD.md:7`)

**Surface.** The `verify-all … --json PATH` manifest append path. The gate documents that `--json`
"appends (>>, never rewrites) one JSON line" (`tools/research-gate.sh:196`). Concurrent appenders
break it at base: the last-byte probe and the append are two operations with no lock, so two
writers that both see an unterminated last line both prefix a newline and leave a blank line
(r24 knowledge `corpus/knowledge/json-delimiter-r24.md:67-71`; r25 2/6 seeded runs). The fix was
pre-registered at round 25 (`SCORECARD.md` Planned — round 26, item 1) and never landed.

**Contract.** For `verify-all RECORD --root ROOT --json PATH`, the gate opens PATH for append
(creating it when absent), takes an exclusive flock(2) on that open file, and holds it from before
it reads the manifest's last byte until after its own line is written. A cooperating writer that
holds an exclusive flock(2) on PATH therefore excludes both the gate's last-byte probe and its
append. Bytes already in the manifest are never rewritten; the manifest keeps its inode; every
appended line is one JSON object on its own line. Nothing else in `verify-all` changes.

**Counter.** `python3 corpus/evidence/round32/c1-count.py [--gate PATH] [--seed N] [--receipt F]`
(lane root). 24 fixed trials: 12 L trials (the counter holds LOCK_EX on the manifest while 8
writers start; seeds empty / terminated / unterminated, 4 each; hold check; cooperating
unterminated fragment on empty/terminated seeds) and 12 F trials (16 free writers on an
unterminated seed). Trial predicate and checks: the counter's docstring (same text).

**P1 (frozen predicate).** C1 is met iff, on the landed lane revision, this counter prints
`APPEND_SERIALIZED=24/24` (receipt label `predicate_holds=true`) on each of two fresh-seed runs,
and no run of this counter on that revision in round 32 prints a lower count.

Code condition: `holds = matched == TOTAL` with `TOTAL = 24`. Receipt label: `predicate_holds`.

**Before (do-nothing control, L1, disclosed).** Base gate, seed 11:
`APPEND_SERIALIZED=8/24` (L 0/12: every writer appended under the cooperating lock; F 8/12: four
trials with a blank line) — `.ufo/waves/round-32/controls/L1-design/base-s11.json`. Feasibility
oracle (scratch gate `719d0b92…`, flock around probe + append): 24/24 —
`controls/L1-design/oracle-s12.json`, gate copy `controls/L1-design/oracle-gate.sh`. The oracle is
feasibility only, never a candidate.

## C2 — coverage (citation chaining: the exempt-hop class of `verify-chain`)

**Surface.** `verify-chain` reads only `resolved` hops. A hop marked `unresolved`,
`blocked-no-fetch` or `labelled-dead` is exempt and never read (`tools/research-gate.sh` verify_chain,
`unresolved|blocked-no-fetch|rejected|labelled-dead|not-applicable)` arm). The round-3 frontier
names the gap: "exemption is record-declared and unverifiable" (`corpus/README.md` Frontier,
Round 3 paragraph). A record can therefore mark a hop "could not be followed" while its cited
anchor sits in a local source under the boundary. This claim moves that edge class from frontier
(unread) to held ground (read, and a false unavailability mark drifts). The command that would
show it unmoved: the counter below on the landed gate printing R1–R3 at 0/36.

**Contract.** U = {`unresolved`, `blocked-no-fetch`, `labelled-dead`} (statuses that say the hop
could not be followed). A U hop whose citation the gate would verify if the same row said
`resolved` (the citation parses; the source is a declared id with a pointer or a local path inside
the boundary; the anchor is found as the resolved path finds it) prints `observed=resolvable`
(verdict `mismatch`) and exactly one `FINDING CHAIN_EXEMPT_RESOLVABLE severity=warn|crit
surface=chain obs=hop=<hop> …` line, and the record drifts. Every other U hop (no citation,
external URL, missing file, undeclared id, out-of-corpus path, anchor absent) stays
`observed=exempt` and no FINDING line names it. `rejected` and `not-applicable` hops stay
`observed=exempt`, unread, with no finding, whatever their citation (they record a judgment, not
an unavailability). `resolved` hops are unchanged. No network read is added: a URL source stays
unread.

**Counter.** `python3 corpus/evidence/round32/c2-count.py [--gate PATH] [--seed N] [--receipt F]
[--keep DIR]` (lane root). 120 hops in one record, 14 fixed classes (truth resolvable 36,
verified 12, exempt 72), random hop ids and file names; matching rule in the counter's docstring
(same text).

**P2 (frozen predicate).** C2 is met iff, on the landed lane revision, this counter prints
`EXEMPT_AUDIT_MATCH=120/120` (receipt label `predicate_holds=true`) on each of two fresh-seed
runs, and no run of this counter on that revision in round 32 prints a lower count.

Code condition: `holds = matched == TOTAL` with `TOTAL = 120`. Receipt label: `predicate_holds`.

**Before (do-nothing control, L1, disclosed).** Base gate, seed 21: `EXEMPT_AUDIT_MATCH=84/120`
(R1–R3 0/36; every other class full) — `controls/L1-design/c2-base-s21.json`. Truth check (L1,
seed 1, kept fixture): the same 120 hops with every status rewritten to `resolved` verify exactly
the 60 hops of R1–R3, F1 and E5 on the base gate (anchor-missing 30 = E1+E8+E9+E10, refused 24 =
E2+E3+E6+E7, invalid 6 = E4), so the hidden truth matches the gate's own resolved semantics.
Cheap controls the control wave must score under this counter: flag every U hop; flag a U hop
when its local file exists, without reading it; status-blind (flag any resolvable hop, including
`rejected`/`not-applicable`); junk labels; a reader that greps the anchor bytes anywhere.

## Separability

C1 changes only the `--json` append block of `verify_all`; the C1 counter's record is a claims
JSONL (no `## Chain`). C2 changes only the exempt arm of `verify_chain`; its counter runs
`verify-chain` only. Receipts required before admission: C2 counter on the C1-only build prints
84/120; C1 counter on the C2-only build prints a count below 24.

## Kill rule

A miss under P1 or P2 is reported as a miss. Neither predicate, counter, class list nor target is
amended after any candidate has been scored; a later design version is legal only before the
first candidate receipt and must say what control forced it.

## Sourced claim (frontier step 2b.4)

At least one of C1/C2 cites a `corpus/SOURCES.md` row opened this round, on a host already
registered in that file (the fetch-scope L0 question `8d77e6c1` is open; no new host is opened).
The citation is in the claim's knowledge entry; it is not part of P1 or P2.

## No harm

Measured at base and after, on the named gate revision: `--selftest` PASS count with the base case
lines byte-identical; `verify-claims corpus/fixtures/claims-r2.jsonl` 17/17; `verify-chain
corpus/fixtures/chain-r3.md` `RESOLVED_HOPS=17/22` CLEAN; `chain-r3-broken.md` 1/2 DRIFT; the
round-1 observable `VERDICT_BEARING_EXPORTS=3/3`; the round-31 counters (`c1-count.py`,
`c2-count.py` under `corpus/evidence/round31/`) 120/120 each.
