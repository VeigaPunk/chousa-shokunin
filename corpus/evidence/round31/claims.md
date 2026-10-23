# Round 31 — frozen claims (design v1, frozen before any data seat)

Base `be7b8d8d54962286417465a305fd9a1a7b3b1525`. Gate at base: `tools/research-gate.sh`
SHA-256 `ac1315ddaa12e79b68069d1a9866b9b1b55e3a43efef3ba0cb5ca5e665835765`.
Counters (this commit): `corpus/evidence/round31/c1-count.py`,
`corpus/evidence/round31/c2-count.py`; their SHA-256 values are recorded in every receipt
(`counter_sha256`).

Anti-loop: rounds 29 and 30 worked `tools/quote-reopen.py`. This round does not touch it.
Both claims change `tools/research-gate.sh verify-claims`, the lane's local claim-vs-source
check (no network).

## C1 — coverage: a claim's named line range (edge class)

**Surface.** `verify-claims` checks that a claim's span occurs, boundary-delimited, somewhere
in its source. It never checks *where*. A claim that names a line (as the lane's own records
do: `…A-shokunin-tradition.md:64`) passes when the span sits on any other line. Frontier item:
`corpus/README.md` Round26 disposition, "pairing a span's occurrence with a named pointer line"
(still unclosed); round 4 named "location binding" unverified. This claim moves that edge class
from frontier to held ground.

**Contract (candidate must meet).**
1. A claims JSONL record may carry the JSON string field `"line"` with value `"N"` or `"N-M"`:
   decimal, `N >= 1`, no leading zero, no spaces, and for `"N-M"` `M > N`. Any other value of
   a present `"line"` makes the record invalid (`observed=invalid`, `CLAIM_RECORD_INVALID`).
2. Span absent (no boundary-delimited occurrence): `observed=unsupported`, as today.
3. Span present and `"line"` present: the claim is **bound** iff some boundary-delimited
   occurrence of the span starts on line N and ends on line N (`"N"`), or starts on line N and
   ends on line M (`"N-M"`); the line numbers are the ones the gate already reports in `at=`.
   Bound → the existing verdict (`supported` for `expect=supported`). Not bound →
   `observed=mislocated` with a new drift finding `CLAIM_LINE_MISMATCH`.
4. `"line"` absent: behaviour unchanged.

**Counter.** `python3 corpus/evidence/round31/c1-count.py [--gate PATH] [--seed S]
[--receipt OUT.json]` (lane root). It writes a fresh temporary root with opaque source files
and 120 claims (12 classes, fixed counts, shuffled; opaque ids and file names; shuffled JSON
key order; every claim `expect=supported`, so the label carries no truth). Hidden truth:
42 supported, 58 mislocated, 12 invalid, 8 unsupported. Classes include a later delimited
occurrence on the named line (supported), a glued (non-delimited) copy on the named line, a
prefix of the span on the named line, multi-line spans named by start line only or by a wrong
range, a line past the end of the file, and two real occurrences with a third line named
(all mislocated).

**Predicate P1 (frozen; the same sentence is in the `c1-count.py` docstring, where "this
counter" is `c1-count.py`; receipt label `predicate_holds`).** "C1 is met iff, on the landed
lane revision, this counter prints LINE_BINDING_MATCH=120/120 (receipt label
predicate_holds=true) on each of two fresh-seed runs, and no run of this counter on that
revision in round 31 prints a lower count." Code condition: `holds = matched == TOTAL` with
`TOTAL = 120`, written to the receipt as `predicate_holds`.

**Kill rule.** Any run of the frozen counter on the landed revision below 120/120 is a miss.
It is reported, never re-scaled, and the counter is never edited after a data seat.

**Before (do-nothing control, base gate).** `LINE_BINDING_MATCH=50/120` (L1 smoke runs, seeds
1 and 2; the committed control receipts come from the control wave). The base gate ignores
`"line"`, so every supported and unsupported item matches and every mislocated and invalid item
misses.

**Command that would show C1 unmoved:** the same counter on a revision without the change
prints 50/120.

## C2 — operability (lowest scored axis): checklist item 1's revision clause becomes runnable

**Surface.** `SKILL.md` "Checklist (executable)" item 1 reads "Every claim carries a resolvable
pointer to the artifact **and revision read**." No lane command can run the revision clause:
`verify-claims` resolves the path and the span, never which bytes the claim was made against.
AXES.md defines operability by "A checklist item can be run and produces the stated outcome";
this claim makes that item's revision clause runnable. The landing also names the command on
the checklist line. (The check also flags stale claims, which overlaps freshness; the surface
moved is the checklist item's runnability, so the claim is filed on operability. The control
wave's axis critic rules on this before data.)

**Contract (candidate must meet).**
1. A claims JSONL record may carry the JSON string field `"sha256"`: exactly 64 lowercase
   hexadecimal characters. Any other value of a present `"sha256"` makes the record invalid
   (`observed=invalid`, `CLAIM_RECORD_INVALID`).
2. `"sha256"` present and different from the SHA-256 of the exact bytes of the claim's source
   file → `observed=stale` with a new drift finding `CLAIM_SOURCE_REVISION_MISMATCH`, before
   and regardless of the span check.
3. `"sha256"` equal → the existing span verdict (`supported` / `unsupported`).
4. `"sha256"` absent: behaviour unchanged. Boundary refusals keep precedence (refused sources
   are never read or hashed).

**Counter.** `python3 corpus/evidence/round31/c2-count.py [--gate PATH] [--seed S]
[--receipt OUT.json]` (lane root). 120 claims in 9 classes, same opacity rules as C1, about a
quarter of the source files with CRLF line ends. Hidden truth: 40 supported, 10 unsupported,
56 stale, 14 invalid. Stale classes: one byte changed on another line, a newline variant
(final newline stripped or added, CRLF and LF swapped), the hash of the span alone, a mismatch
with the span absent, and the hash of another fixture file. Invalid: uppercase, 63 or 65
characters, a `sha256:` prefix, a non-hex character, a leading space.

**Predicate P2 (frozen; the same sentence is in the `c2-count.py` docstring, where "this
counter" is `c2-count.py`; receipt label `predicate_holds`).** "C2 is met iff, on the landed
lane revision, this counter prints REVISION_BINDING_MATCH=120/120 (receipt label
predicate_holds=true) on each of two fresh-seed runs, and no run of this counter on that
revision in round 31 prints a lower count." Code condition: `holds = matched == TOTAL` with
`TOTAL = 120`, written to the receipt as `predicate_holds`.

**Kill rule.** As C1.

**Before (do-nothing control, base gate).** `REVISION_BINDING_MATCH=50/120` (L1 smoke runs,
seeds 1 and 2).

**Command that would show C2 unmoved:** the same counter on a revision without the change
prints 50/120.

## Timing and harness capacity (declared before data)

Neither predicate is a timing predicate. Each counter runs the gate once per run with a
600 s timeout; a run that exceeds it, or a gate exit other than 0 or 1, scores every claim
`none`. Fixture generation is deterministic per seed; there is no server, no listen queue and
no network. Expected wall time on this host: about 2 s per run for the base gate.

## Separability

C1 adds only the `"line"` field; C2 adds only `"sha256"`. Neither counter's fixture carries the
other field. Each lands as its own commit. Separability check: the C1 counter on a C2-only build
and the C2 counter on a C1-only build must print their before values (50/120).

## No harm (checked after landing; not part of P1 or P2)

`bash tools/research-gate.sh --selftest` PASS (154 cases at base, plus the new cases);
`verify-claims corpus/fixtures/claims-r2.jsonl --root ..` stays `VERDICT_BEARING_CLAIMS=17/17`
CLEAN; `verify-chain corpus/fixtures/chain-r3.md --root ..` stays `RESOLVED_HOPS=17/22`; the
round-1 observable stays `VERDICT_BEARING_EXPORTS=3/3`; `tools/quote-reopen.py` is unchanged.

## Pre-data controls (control wave, receipts under `.ufo/waves/round-31/controls/`)

For each counter: do-nothing (base gate), junk (random observed values), all-one-value stubs
(each truth value), label-keyed (`observed := expect`), no-reader (decides from the claims file
alone, never opening a source), and shortcuts keyed on fixture features (C1: first occurrence,
raw substring on the named line, first token on the named line, any-occurrence count; C2:
uppercase accepted, line-end normalized before hashing, hash of the file read through `$(cat)`
which drops trailing newlines, hash of the span, membership in the set of fixture hashes). A
full-contract Python oracle is built only as a feasibility control (it must reach 120/120, or
the counter would reject a correct tool), with one-rule-dropped mutants that must each score
below 120; it is disclosed as a reference, never as a candidate. A claim whose counter any
control meets is re-designed before data, as a new version, or declared exploratory.

## Not claimed

Semantics or truth of a span; that a named line is the *right* line for the claim's meaning;
git-revision binding (the pin is a content hash of the bytes read, not a commit); records'
`## Claims` table pointers (`path:N`) in `verify` mode; `verify-chain` hops; races between
hashing and reading a file that changes during the run.
