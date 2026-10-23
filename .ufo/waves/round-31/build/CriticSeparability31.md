# CriticSeparability31 — attack on claims.md "Separability" (round 31, WAVE 1 BUILD)

Role: UFO-FSD critic. Ran nothing against candidate implementations (none exist yet).
All experiments used synthetic gate variants built in scratch
(`/fast/scratch/hyaku/chousa-r31/w1/CriticSeparability31/`, clones of frozen d78d188).
The lane's `tools/research-gate.sh` was accidentally touched mid-experiment by a bad edit
anchor and was **restored byte-identical to base** (verified by `cmp` against the frozen
clone). No lane mutation remains from this seat. No tool installed (nothing needed; tooling
directive: no installs performed).

## 1. What was attacked

The proposed-assertion (claims.md lines 114-118): "C1 adds only `line`; C2 adds only
`sha256`. Neither counter's fixture carries the other field. Each lands as its own commit.
Separability check: C1 counter on a C2-only build and C2 counter on a C1-only build must
print their before values (50/120)." Target questions: can each be verified with the other
absent? do the fixtures cross-exercise? does unknown-key rejection break the other? what
integration order/checks prove it, and which selftest-numbering conflict arises?

## 2. Evidence (all run on this host, 2026-10-23)

Fixture disjointness — read both frozen generators:
- `c1-count.py` `generate()` builds `rec = {"id","claim","source","span","expect"}` + optional
  `"line"` only (lines 176-178). `"sha256"` never emitted. 102/120 C1 claims carry `line`;
  6 (B4) do not.
- `c2-count.py` `generate()` builds the same five keys + optional `"sha256"` only (lines
  164-167). `"line"` never emitted. 104/120 C2 claims carry `sha256`; 16 (N1) do not.
So the fixture space is genuinely disjoint — the positive half of the assertion holds.

Baselines (base gate, frozen commit): `c1-count.py --seed 1` → `LINE_BINDING_MATCH=50/120`
(exit 1); `c2-count.py --seed 1` → `REVISION_BINDING_MATCH=50/120` (exit 1). Matches claims.md.

Two synthetic one-sided builds (full, contract-conformant implementations of the *other*
claim, i.e. each meets its own 120/120 predicate):

| Build | c1-count | c2-count | separator expectation |
|---|---|---|---|
| v1 (C1-only, correct C1: all-occurrence line binding; strict rejection of unknown `sha256`) | **120/120** (seed 1 and 2) | **30/120** | 50/120 → FAILS |
| v2 (C2-only, correct C2: hash-before-span, refusals first; strict rejection of unknown `line`) | **18/120** | **120/120** | 50/120 → FAILS |
| v1t (C1-only, tolerant of unknown keys) | 120/120 | **50/120** | PASSES |
| v2t (C2-only, tolerant of unknown keys) | **50/120** | 120/120 | PASSES |

So the assertion as written is only satisfiable by implementations that ignore unknown JSON
keys — a property neither frozen contract states. A strict-schema implementation, which no
contract clause forbids, fails the separator check even while its own predicate holds,
120/120. (The strict runs' matches are exactly the claims that do not carry the other field:
v1 strict c2 = 16 N1 + 14 I1 (invalid-truth coincidence) = 30; v2 strict c1 = 6 B4 + 12 I1
= 18. Confirmed by per-class output.)

Trap found while engineering v2 (real bug class for candidates): per-claim `observed` state
leaks across records — a stale verdict on one claim made the next claim stale too (first run
scored 71/120: R1 0/24, N1 1/16; after `observed=''` reset per record → 120/120). The base
gate never reads `observed` before assigning it, so a candidate that reads it pre-assignment
or fails to reset inherits this.

Second trap (C1): `tok_span_at` returns only the **first** boundary-delimited occurrence
(lines 1310-1320). C1 contract says "some occurrence" (B2 names a later occurrence, M6 a
third line). A candidate that merely compares the named line to the existing `at=` report
will score 108/120 (12 B2 misses). v1 passes 120/120 only with an all-occurrence scan
(`line_range_ok`, added to v1).

## 3. Findings (impacted axes: coverage C1, operability C2)

1. **Separability is under-specified.** Add to both contracts: "unknown JSON fields are
   ignored (never invalidate a record)" — this is already the base gate's behavior (jfield
   reads known keys only; nothing rejects extras). Then the 50/120 one-sided checks are
   well-defined and achievable (proven: v1t/v2t).
2. **The separator check as written rejects a plausible, contract-compliant implementation
   family** (strict unknown-key validation) — 30/120 and 18/120 instead of 50/120, despite
   each predicate passing. This is a hidden acceptance-criterion trap, not a fixable
   candidate bug: the frozen design must pin tolerance.
3. **Ordering is only specified piecewise.** C2's "stale before and regardless of the span
   check" combined with C1's mislocated-verdict gives a deterministic combined order only if
   C2's hash check sits after `claim_source_path` (refusal precedence) and before the span
   check; C1's bound check sits inside the span-present branch. No counter exercises both
   fields, so the intersection is uncharted — must be probed (checklist item 4).
4. **Selftest numbering: no numeric conflict.** Case numbers are a runtime counter
   (`cases=$((cases+1))` in tcase/tclaims/tchain/…); the final line is
   `RESEARCH_GATE_SELFTEST: PASS (%d cases)` — nothing asserts 154. "154 cases at base,
   plus the new cases" is informational. The real integration conflicts are textual:
   both claims edit the same regions (record-read anchor near `marker=$(…)`, the drift-ID
   header comment block around lines 17-42, and the tail of `run_selftest`), and both add
   new finding IDs (`CLAIM_LINE_MISMATCH`, `CLAIM_SOURCE_REVISION_MISMATCH`) to the same
   comment block. Under "each lands as its own commit", one of the two one-sided builds is
   naturally an intermediate commit; the other requires applying the second diff alone to
   base (what v1/v2 did in scratch). Recommend: land C1 first (intermediate = C1-only
   build), verify C1-only, then land C2; verify C2-only via a temporary base+C2 diff (as
   here) or a second leaf commit; both diffs must use namespaced selftest fixture filenames
   (`claims-line-*`, `claims-sha-*`) and disjoint insertion anchors to avoid hunk overlap.
5. **Baseline numbers double as regression checks.** On either one-sided build, the other
   counter MUST print exactly 50/120; anything else means either a span-behavior regression
   or unknown-key intolerance.

## 4. Minimal separability check list for the falsify wave

1. Static fixture disjointness: assert `c1-count.py` output never contains `"sha256"` and
   `c2-count.py` output never contains `"line"` (grep the generated claims JSONL, any seed).
2. C1-only build (base + C1 diff): `c1-count.py` 120/120 on two fresh seeds AND
   `c2-count.py` = 50/120.
3. C2-only build (base + C2 diff): `c2-count.py` 120/120 on two fresh seeds AND
   `c1-count.py` = 50/120.
4. Unknown-key + combined-field probe (hand-made JSONL, full merged build):
   - record with an extra unknown key + valid fields → supported (not invalid);
   - record with both fields: wrong sha256 + wrong line → stale (C2 precedence);
     correct sha256 + wrong line → mislocated; malformed sha256 + correct line → invalid;
     correct both → supported; correct sha256 + absent span → unsupported.
     This pins the stale-before-mislocated order neither counter covers.
5. State-leak probe: two-record file, first stale, second correct-sha/no-sha → second must
   be supported (guards the `observed`-remnant bug class).
6. Multi-occurrence binding: a later-occurrence named line (B2 shape) must be supported —
   i.e. candidates must scan all boundary-delimited occurrences, not only `at=`'s first.
7. After integration: `--selftest` PASS with expected total = 154 + (#C1 cases + #C2
   cases) (assert the count by parsing the PASS line, not a hardcoded 154); `verify-claims
   corpus/fixtures/claims-r2.jsonl --root ..` = 17/17 CLEAN; `verify-chain` = 17/22;
   round-1 exports = 3/3; `tools/quote-reopen.py` unchanged.

## 5. Limits

- No candidate implementation existed; nothing was run against candidates. v1/v2/v1t/v2t
  are synthetic probes in scratch.
- The lane's `corpus/evidence/round31/c1-count.py` currently differs from the frozen commit
  (a "design v2" sub-variant patch with `SUBVARIANTS`, authored by another actor mid-run).
  Not touched by this seat; noted because it changes the "frozen counter" premise if it
  lands before data. The lane `tools/research-gate.sh` is byte-identical to base.
- Reading `tok_span_at`/`jfield`/`json_str` and the counter generators is the basis for all
  static claims; all runnable numbers above are from executed commands (quoted exit codes).
