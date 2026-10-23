# RevengerR26Intent — intent of "pairing a span's occurrence with a named pointer line" and r4 "location binding" (round 31, WAVE 1)

Scope: reconstruction only. No lane file outside this report was written; no gate run, no
counter run, no network, no installs. Lane HEAD observed `d78d18893849cecb710f3b691ec986e1321d39ee`
(`git rev-parse HEAD`) = the frozen design-v1 commit; all `claims.md` line refs below are to
`corpus/evidence/round31/claims.md` at that commit.

## 1. The frontier item and its original meaning

- Owning statement: `corpus/README.md:861-880` "## Round26 frontier disposition (2026-10-21)";
  lines 875-877: "Still unclosed: concurrent JSON appenders, filesystem races, parent-root
  legacy rechecks, receipt gaps, and pairing a span's occurrence with a named pointer line."
- The item is the surviving *class* half of hardening-ledger row 56
  (`corpus/knowledge/hardening-r10.md:281`): "`A-r9.md:50` row C3 pointer `A:76` vs span
  occurrence `A:86`; no mode pairs a row's `path:line` with its span's occurrence line".
  Row 56 is filed as a **finding**, not by-design — the only such row in its table.
- What was meant, in the lane's own earliest words:
  - r2 (`corpus/knowledge/claim-verification-r2.md:94-96`): "Not location binding or
    uniqueness. The check is 'the span occurs somewhere in the file'; the reported `at=` line
    is the first occurrence. The fixture pre-registers expectations, not expected lines."
  - r3 (`corpus/knowledge/chain-resolution-r3.md:107-110`): "The mode verifies anchor
    EXISTENCE, not line binding or uniqueness. The reported `at=` is the first occurrence,
    informational."
  - r4 (`corpus/knowledge/anchor-boundaries-r4.md:133-136`): "no support adjudication, no
    location binding or uniqueness (the first delimited occurrence is informational)";
    lesson `corpus/lessons/2026-10-15-anchor-token-boundaries.md:172` "Location binding and
    uniqueness remain unverified (round-3 bounds)" and `:210-211`.
  - r10 queue (`hardening-r10.md:323-331`): item 1 — "decide whether the pointer/span class
    (including a `:99999`-style pointer probe, r9 lesson m5) ever deserves a gate check";
    item 2 — "decide whether any in-record label/span or pointer/line pairing is checkable
    **without semantics**".
  So the intent: extend the span check from "occurs boundary-delimited somewhere" to
  "the occurrence is bound to the line the record names", using only mechanical line
  comparison — explicitly *without* semantics (no judgement that the named line is the right
  line for the claim's meaning). Uniqueness is a sibling limit, always named alongside but
  distinct ("location binding **or** uniqueness", r2/r3/r4).

## 2. Was any code attempted?

No — never, in the landed gate or its history.

- Base gate `tools/research-gate.sh` (lane HEAD d78d1889) `verify_claims` parses exactly
  `id`, `source`, `span`, `expect`, `marker` (+ `marker_default`) (`:1366-1370`); no `"line"`
  and no `"sha256"` key is read; a grep for `CLAIM_LINE_MISMATCH|CLAIM_SOURCE_REVISION_MISMATCH|
  "sha256"|"line"` in the file returns no claims-field hits. The occurrence lines the gate
  computes (`TOK_L1`/`TOK_L2` → `TOK_AT`, `:1316-1317`) are used only for the `at=` report
  and the contradicted region slice (`:1409-1411`) — never compared to anything the claim says.
- History (read-only): `git log --all -S 'CLAIM_LINE_MISMATCH' -- tools/research-gate.sh`
  → empty; `git log --all -S '"line"' -- tools/research-gate.sh` → empty; the only broad
  `-G 'json_str .*\bline\b'` hit is r2 commit `c3df458` (the `line` shell local), not a field.
- The r10 decision was deliberate non-action: "was deliberately not acted on ('no gate change
  without a reported defect')" (`hardening-r10.md:91-95`); r11 answered the queue question
  "not this round" (`hardening-r10.md:438-441`; `audit-r11.md:335-341` "only the instance is
  closed"). No scratch/candidate attempt appears in any wave tree either — r26/r27 wave
  artifacts only re-enumerate the debt (`.ufo/waves/round-26/build/ScoutCarriedDebt.md:46,151`;
  `FNoTrade.md:250-252`).

## 3. Why it stayed open (full chain, append-only)

Instance closed, class kept: r12 corrected the A:76→A:86 pointer and re-pinned the record sha
(`dfd2ae1a…`) while "the class — no mode pairs a pointer line with its span's occurrence
line — stays a named non-coverage" (`corpus/README.md:259-261`; r12 status also
`corpus/README.md:565`, `SKILL.md:463-466`, `corpus/fixtures/claims-r9.README.md:121-122`,
`corpus/evidence/README.md:775-777` "the gate adjudicates spans, not pointer line numbers").
Then carried verbatim every round: r25 (`corpus/lessons/round-25.md:42` "source/span pairing
remains uncovered"), r26 carried table (`corpus/lessons/round-26.md:23`) and the Round26
frontier disposition (`README.md:875-877`), r27 (`corpus/lessons/round-27.md:117-120`
"source/span location pairing … stay open"). Each round re-declared it carried rather than
silently repaired; the rounds that could have taken it were spent elsewhere (r26's build
falsified its own C2/C3 and was NOT ADMITTED, `SCORECARD.md:1446-1492`; r27 repaired the
r26 falsifications). The r10/r11 precondition for acting — a reported defect plus a decision
that the class deserves a gate check — was only ever half-met until round 31's claims.md
cited the class as its target.

## 4. Does claims.md C1 match the intent? — verdict

C1 contract (`claims.md:14-60`): optional JSONL string `"line"` = `"N"`/`"N-M"` (strict
grammar); bound iff **some** boundary-delimited occurrence starts and ends on the named
line(s), lines being "the ones the gate already reports in `at=`"; unbound →
`observed=mislocated`, new finding `CLAIM_LINE_MISMATCH`; malformed → `observed=invalid`;
`"line"` absent → unchanged.

**Verdict: MATCH in substance, NARROWER in surface.** Not a different reading.

Matches:
- The core mechanical pairing is exactly row 56's class: named line vs the gate's own
  occurrence-line accounting (`claims.md:29-30` "the line numbers are the ones the gate
  already reports in at="; mechanism = existing `TOK_AT`, gate `:1316-1317`). No semantics —
  the "Not claimed" list (`claims.md:85-88`) refuses "that a named line is the *right* line
  for the claim's meaning", matching r10 queue item 2's "checkable without semantics".
- The occurrence side keeps the r4 boundary-delimited definition (via `tok_span_at`), so the
  r4 "location binding" limit — the same note that pinned `at=` as informational — is the
  one being closed; r2's "expectations, not expected lines" gap is directly filled.
- It moves the exact frontier item (`README.md:876-877`) to held ground and adds the missing
  verdict vocabulary (mislocated/invalid) without touching span semantics.

Narrower (all by C1's own text, not silent):
1. **Surface**: the historical class statement is about records' `path:N` pointers (row 56's
   `A-r9.md:50 → A:76`, checked by no mode — `verify`/`verify-all`/chain). C1 binds a *new*
   opt-in `"line"` field on the claims-JSONL surface only and explicitly does not claim
   "records' `## Claims` table pointers (`path:N`) in `verify` mode" (`claims.md:87`). The
   record-table and chain-anchor instances of the class remain uncovered; SKILL.md:466's
   "no mode pairs a row's `path:line` …" becomes false only for JSONL claims carrying `line`.
2. **Opt-in**: `"line"` absent → "behaviour unchanged" (`claims.md:31`), so untagged claims
   keep the anywhere-in-file pass; the class closes only where a line is named. [INFERENCE:
   this follows from the counter classes and the frozen before-state 50/120, not from the
   older notes.]
3. **Extensions beyond the old wording**: `"N-M"` end-line binding and the mislocated/invalid
   observed classes are new (r2-r4 only ever said `at=` is informational). Consistent with
   intent; strictly more than "pairing".
4. **Uniqueness stays open**: r2/r3/r4 always name "location binding **or** uniqueness";
   C1 binds on *some* occurrence on the named line(s); duplicates elsewhere are neither
   reported nor required, matching r4's informational-first-occurrence bound but leaving the
   sibling named non-coverage untouched.

Net: C1 is a faithful instantiation of the r26 frontier item and the r4 location-binding
limit on the verify-claims surface, deliberately narrower than ledger row 56's class wording
(JSONL field, not `path:N` record pointers; no chain mode; no uniqueness). Nothing in the
frozen contract redefines an occurrence, relaxes r4 boundaries, or claims semantics/truth.

## 5. C2 adjacency (one line, since round 4 is cited)

Round 4's note and r2/r3 never tie line binding to revision bytes; C2's `"sha256"` pin comes
from a different lineage (SKILL.md "Checklist (executable)" item 1, operability axis,
`claims.md:62-70`). It neither fulfils nor narrows the row-56 class; the two claims are
separable as designed (`claims.md:81-83`).

## Limits

Reconstruction from committed lane artifacts and read-only git at d78d1889 only; I did not
execute the gate, either counter, or any control (control wave and L1 own scoring). The
"no scratch attempt in any wave tree" claim covers r25-r27 and r9/r10 goal-wave artifacts I
grepped, not an exhaustive sweep of all 30 round directories. Two items marked [INFERENCE].
