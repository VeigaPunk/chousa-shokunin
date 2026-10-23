# CriticClaimsAfter31 — wave-2 falsify critic on the two round-31 claims as landed

Scope: `corpus/evidence/round31/claims.md` (design v2, P1/P2), landings c17948a (C1, gate
`3b5279eb…`), 6d0ae19 (C2, gate `c23d7537…`), tip ee1024f, then HEAD ad20a66 and, mid-review,
HEAD 65d00cf (gate `ed3b9125…`). Read-only on the lane; experiments in
`/fast/scratch/hyaku/chousa-r31/w2/CriticClaimsAfter31/clone`; all receipts, probes and mutants in
`.ufo/waves/round-31/falsify/CriticClaimsAfter31/`. No tool installed. `[INFERENCE]` marks claims
that rest on reading code rather than an execution.

## Per-claim verdict

**C1 (coverage) — holds under P1.** Two fresh-seed runs exist on the landed revision
(`measure/after-c1-run{3,4}-tip.json`, gate `c23d7537…`, 120/120) and two on C1's own landing
(`after-c1-run{1,2}.json`, gate `3b5279eb…`, 120/120). My fresh seeds `20261023011/12` on
`c23d7537…`: 120/120 (`c1-seed1.json`, `c1-seed2.json`). Across 838 round-31 receipts carrying
`matched/total`, min C1 count on the landed gate = 120 (165 receipts); the only C1 sub-120 receipts
are on other gates (base `ac1315dd…` 50/120; mutated gates), which P1's "on that revision"
excludes and design `## Separability` itself mandates. After the gate moved to `ed3b9125…`, my
fresh seed `20261023051` is still 120/120 (`c1-seed51-head65d.json`).

**C2 (operability) — holds under P2, and the landed text is runnable.** Two fresh-seed runs on
`c23d7537…` (`measure/after-c2-run{1,2}.json`); my seeds `20261023021/22` = 120/120
(`c2-seed*.json`); min C2 count on the landed gate = 120; on `ed3b9125…`, seed `20261023061` =
120/120 (`c2-seed61-head65d.json`). The SKILL.md added line is **byte-identical** to the frozen
landing text; `SKILL.md:66` (item 1) is unchanged from base `be7b8d8`. The exact command line
`bash tools/research-gate.sh verify-claims <claims.jsonl> --root ..` from the lane root on a
2-claim file re-run against the shipped gate `ed3b9125…`: correct pin → `observed=supported
at=line:9`; wrong pin → `observed=stale` + `FINDING CLAIM_SOURCE_REVISION_MISMATCH severity=warn
surface=claims obs=id=PIN-STALE …`, exit 1 (`skill-run-current-gate.txt`). Selftest on the shipped
gate: `PASS (228 cases, 0 skipped)`; case numbers match SKILL.md's claim exactly (216–219 c1-*,
220–228 claims-sha-*).

P1/P2 are count predicates and both are satisfied, on both the measured gate and the shipped gate.
The defects below are outside what the predicates can see.

## Counterexample 1 — a rule-dropped mutant meets both counters (coverage of contract item 1)

**A gate that treats a present non-string `"line"` / `"sha256"` as absent scores 120/120.**
Mutants `gate-c1-nonstring-absent.sh` / `gate-c2-nonstring-absent.sh` differ from the landed gate by
one block each. Probe `probe.jsonl`: landed → `{"line":9}` `observed=invalid`, `{"sha256":123}`
`observed=invalid`; mutants → both `observed=supported`. Frozen counters on the mutants:
`LINE_BINDING_MATCH=120/120` (`c1-mutant-nonstring-seed31.json`) and `REVISION_BINDING_MATCH=120/120`
(`c2-mutant-nonstring-seed41.json`), both exit 0. The survivors are already in the wave's own
receipts: `falsify/MutC1Grammar/nonstring-absent.mutated.c1-{1,2}.json` 120/120 and
`falsify/MutC2Parse/m1-nonstring-absent.seed{1,2}.receipt.json` 120/120.

Cause: v2 fixed sub-variant *counts*, but the non-string sub-variant has count **0** in both
invalid classes (`c1-count.py:68` `INVALID_VALUES` = 12 JSON strings; `c2-count.py:68-70` I1 kinds
= 14 JSON strings). This is the v1 defect class QUALITY 31 addresses, re-entering through a
sub-variant nobody draws. Consequence: P1/P2 do not certify contract item 1's non-string arm, and
the design's "one-rule-dropped mutants must each score below 120" fails for that rule. The landed
gate is correct here; the C1 selftest covers `"line":5` (`tools/research-gate.sh:6778`), but **no
selftest and no counter case anywhere covers a non-string `"sha256"`** — the C2 commit's "non-string
pin invalid" is untested.

## Counterexample 2 — the tool under test changed after the predicates were scored

At 02:16Z HEAD moved to `65d00cf` ("C2 falsify fixes (CriticEdgeC2 D-A raw pin validation, D-B hash
via stdin)"), gate `c23d7537…` → `ed3b9125…`, two behaviour changes. Every citing document still
names `6d0ae19f` / gate `c23d7537…` (knowledge entries, the working-tree SCORECARD Round 31 section,
the README disposition), and the receipts that establish P1/P2 bind `c23d7537…`; the receipts for
the shipped gate (`measure/after-c{1,2}-run{5,6}-fixab.json`) are **untracked**. So "landed
revision … gate SHA-256 `c23d7537…`" no longer identifies the code in the lane. P1/P2 survive only
because I re-ran them on the new gate (above); no design version was declared for the change,
although the counter freeze discipline ("a miss is reported, never re-scaled") exists precisely to
stop post-data movement.

D-A also **narrows frozen contract item 1**: the pin is now validated as the raw JSON body, so a
JSON-escaped value whose decoded value is exactly 64 lowercase hex characters reads `invalid`.
Verified: pin `"\u003719233fe…"` (decodes to the file's real hash) → pre-fix gate `supported`,
shipped gate `observed=invalid`. The frozen contract says the field must be "exactly 64 lowercase
hexadecimal characters" with no escape clause, and the knowledge entry still says only that. No
counter or selftest case covers an escaped pin. The fix closes a real hole (bash drops NULs on
decoding) but the narrowing is undocumented and post-data.

## Overclaim / provenance defects

1. **Dangling pointer in both committed knowledge entries.**
   `corpus/knowledge/line-binding-r31.md:4,38` and `revision-binding-r31.md:4,30` say the measured
   result is in `SCORECARD.md, section "Round 31"`. At ee1024f and at ad20a66/65d00cf,
   `git show HEAD:SCORECARD.md | grep -c "## Round 31"` = 0; the section exists only as an
   **uncommitted** working-tree edit (+52 lines). The frozen C2 requirement "score recorded 3 → 3
   (delta 0) with this observable beside it" therefore has no committed record. At ee1024f the
   entries also cited `corpus/lessons/round-31.md` `## Gate`, absent at that commit (added at
   ad20a66) — a landing-order defect, now resolved.
2. **Committed knowledge entry inaccurate.** `revision-binding-r31.md` (committed) says "A source
   whose digest cannot be measured reads `stale` (`actual=unreadable`), never a match", omitting
   that the gate refuses first: a missing source with a valid pin → `observed=refused` +
   `CLAIM_SOURCE_OUT_OF_CORPUS` (`missing.jsonl`), never hashed. The working tree already repairs
   the sentence (uncommitted).
3. **SKILL.md self-contradiction left by the ee1024f edit.** Rows now say `PASS (228 cases)`, but
   `SKILL.md:88-90` still says "The shared `154 cases` tally in the rows above… the final shared
   selftest is `PASS (161 cases, 0 skipped)`". No row says 154; the final is 228.
4. **Axis blur in the uncommitted README.** `corpus/README.md` working-tree "Round31 frontier
   disposition" says C2 "moved from frontier to held ground"; design v2 files C2 on operability and
   says its surface is the pre-existing checklist obligation, "not the new field" (why not
   coverage). As written it asserts a coverage-shaped move the design disclaims.

Not an overclaim: `claims.md` and the landed prose keep "a claim without a pin is not checked for
revision" and list "that every claim carries a pin" under Not claimed — and the lane's own claims
fixtures carry **zero** pins (`claims-r2.jsonl` 17 lines, 0 `sha256`). Running the command on them
yields CLEAN with no revision check, so checklist item 1's stated outcome is still not produced;
the 3 → 3 delta 0 is honest and the item stays unchecked.

## Axes

Distinct. C1's commit touches only `tools/research-gate.sh`; C2's adds the one checklist run line.
Separability receipts agree: C1 counter on the C2-only build 50/120, C2 counter on the C1-only
build 50/120 (`measure/sep-*`). Caveat: P2's 120/120 measures gate behaviour, not the SKILL run
line, so the operability half rests on the manual run above, not on the predicate.

## Smallest safe correction

1. Declare a v3 counter (never editing the frozen bytes) adding one non-string sub-variant to each
   invalid class, plus a non-string `"sha256"` selftest case; until then read P1/P2 as certifying
   everything except contract item 1's non-string arm.
2. Declare the two falsify fixes as a versioned post-data change and re-bind the docs: cite
   `65d00cf` / gate `ed3b9125…`, commit the run5/run6 receipts, and state D-A's raw-pin narrowing
   in the contract's successor (the frozen text cannot be edited).
3. Commit the SCORECARD Round 31 section and README/SOURCES rows already drafted in the working
   tree; move the C2 sentence out of the README frontier disposition.
4. Fix `SKILL.md:88-90` to name 228 (or scope 154/161 to the round-25 checkpoint) and keep the
   repaired refusal-precedence sentence in the commit.

## What I ran

`bash tools/research-gate.sh --selftest` (both gates) → PASS 228, exit 0. `c1-count.py` seeds
20261023011/12/51, `c2-count.py` seeds 20261023021/22/61 on the landed and shipped gates →
120/120, exit 0. Both counters on the two non-string mutants → 120/120, exit 0. Exact SKILL.md
command line on `small-claims.jsonl` (correct + wrong pin), shipped gate → supported / stale +
finding, exit 1. `probe.jsonl` (both fields, non-string, null, unbound), `missing.jsonl` (refusal
precedence), `escaped-pin` probe on both gates (supported → invalid). `verify-claims claims-r2` →
17/17 CLEAN; `verify-chain chain-r3` → 17/22 CLEAN; `tools/quote-reopen.py` untouched
(`git diff be7b8d8..HEAD -- tools/quote-reopen.py` empty). Receipt scan over 838 round-31 receipts.
Two probe files were briefly written to `/tmp` and deleted; no other write outside this directory.
