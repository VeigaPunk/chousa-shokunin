# chousa round 82 — frozen claims

Base (round-81 tip, closed `rejected-honest-stop`): `142b6f0c08e645ef9507f6d880be44e518c39043`.
Egress table committed before any fetch: `5d792e1e953649e801d9bf1f64093b1f0d4dac8c` (commit time 2026-11-06T19:41:56Z;
first round-82 refetch row 19:42:03Z).
Prefreeze instruments, fixtures and captures: `38f5af8268b2807811dded3d7d7221ff3f509495`.
Prefreeze control receipts: `corpus/evidence/round82/controls/` (driver `run-controls-r82.sh 38f5af82…`,
`CONTROLS_AS_EXPECTED=14/14`), committed with this file, before any gate edit and before the candidate entry exists.

## Fresh-start / rejection-history reads (done before this file)

- r81 (`round-81-verifier-spotcheck.md`): C1 depth counter passed two filler entries (`r09`); C2 item-2/item-4 Run lines
  pass placeholder cells, undeclared sweep ids and `n/a` locations (eleven K2 records); routed defects 1–6.
- r80 (`round-80-verifier-spotcheck.md`): draw-dependent predicate; unopened superseded record; label drift.
- r79 (`round-79-verifier-spotcheck.md`): battery answer key in the subject table.
- Shared lesson applied here: every predicate below is a fixed command over committed bytes; every do-nothing and
  forgery control was executed and committed before freeze; positive controls are retained so blanket refusal scores
  FAIL.
- Prefreeze discovery: R81ReviewerC2's record `r4-07-alt-section.md`, described as "reason present, flip empty", carries a
  complete rejection (its flip cell is filled; `diff` against `item4-pass.md` differs only in the heading). The F4-5 defect
  form is therefore built here as `r4-07b-alt-section-noflip.md` (item4-fail with the heading renamed), and r4-07 itself is
  a positive control (`REJECTIONS_OK=1/1` required: the gate must read the rejection, not skip it).

## C1 — operability (lowest-scored non-retired axis, historical 3/10)

**Claim.** `tools/research-gate.sh` (the gate itself — the SKILL.md item-2 and item-4 Run lines stay byte-identical to
base) refuses the round-81 K2 forms and the declared placeholder class through those Run lines, keeps refusing the forms it
already refused, and still passes the well-formed records.

**Counting command (frozen, sha256 recorded below):**
`D=$(mktemp -d -p /fast/scratch/hyaku) && git archive <rev> | tar -x -C "$D" && python3 -B "$D/corpus/evidence/round82/k2-gate-r82.py" --root "$D"`
plus, for no-harm, `bash tools/research-gate.sh --selftest` in the same tree.

**Before** (`controls/c1-k0-donothing.txt`, tree = 38f5af82): `RUNLINES=2/2 K2_REFUSED=0/11 HOLD_REFUSED=9/9
CLASS_REFUSED=2/24 POSITIVE=5/6`, `K2_GATE=FAIL`, rc 1. Base selftest: `RESEARCH_GATE_SELFTEST: PASS (275 cases, 0 skipped)`.

**Predicate (target).** At the landing revision the counting command prints exactly
`RUNLINES=2/2 K2_REFUSED=11/11 HOLD_REFUSED=9/9 CLASS_REFUSED=24/24 POSITIVE=6/6` and `K2_GATE=PASS`, rc 0, AND the
gate selftest prints `RESEARCH_GATE_SELFTEST: PASS (N cases, 0 skipped)` with N ≥ 275, rc 0.

**Forgery controls (executed, committed):** `c1-f1-blanket-refuse` (refuses everything with the right finding ids →
POSITIVE=0/6, FAIL), `c1-f2-wrong-finding-keyed` (file-name-keyed refusal with a generic finding → FAIL),
`c1-f3-keyed-runline` (the round-81 fixture-keyed Run-line forger → `RUNLINE item=4 found=changed`, FAIL).

**Declared placeholder vocabulary (closed, frozen):** after lower-casing, removing backticks, quotes, `*`, `_`,
collapsing whitespace and stripping trailing periods, a cell equal to one of: empty, `-`, `--`, `---`, `—`, `–`, `n/a`,
`na`, `n.a`, `none`, `nil`, `null`, `tbd`, `tba`, `todo`, `?`, `??`, `...`, `…`, `x`, `unknown`, `not applicable`, `same`,
`ditto`, `see above`, `idem`. Values outside this set (e.g. `pending`, `no flip`) are not claimed; a wave finding of one is
recorded as a residual, not a kill.

**Kill rules (frozen):**
- K1: the predicate is not met at the landing revision.
- K2 (generalization): any record, authored by anyone, that (a) differs from `item2-pass.md`, `item4-pass.md` or
  `sweeps-r5.md` in one reason, flip-condition, `where` or claim-`sweep` cell set to a declared-vocabulary value, or (b)
  keeps a rejection with an empty or declared-vocabulary reason or flip under a `##` heading whose text contains
  `reject` (case-insensitive), or (c) carries a `negative` claim whose sweep cell names no declared `## Sweeps` row id
  while no `## Sweeps` row's `claim_id` names that claim (and no `## Negatives` sweep row carries it), on which the frozen
  item-2 or item-4 Run line exits 0 at the landing revision → C1 falsified.
- K3 (harm): a record that the base gate (`5d792e1e`) passes under a Run line and that carries none of K2's forms, which
  the landed gate refuses under the same Run line → C1 falsified.
- K4: the selftest at landing is not PASS, or skips a case, or has fewer than 275 cases.

## C2 — depth (sourced on S209, S210, S211 and re-opened S008)

**Claim.** One new `corpus/knowledge/` entry on question framing (review question frames — PICO levels, PCC, alignment of
objective, question and eligibility criteria, protocol deviations) — ground no base entry holds — whose decision table rows
are each warranted by a verbatim quote located in a capture fetched this round.

Near neighbours examined before freeze: `archived-export-intake.md:89` (names "question framing before search" as an
archive claim, CL-02, no decision rows) and `quality-control-guideline-issued-text-r48.md:26` (PICOS optional in one
Chinese instrument's inclusion rule). Neither holds a decision table on choosing or aligning a question frame.

**Counting command (frozen):**
`D=$(mktemp -d -p /fast/scratch/hyaku) && git archive <rev> | tar -x -C "$D" && python3 -B "$D/corpus/evidence/round82/depth-r82.py" --root "$D"`

**Before** (`controls/c2-d0-donothing.txt`): `DEPTH_R82 entries=0 ok_entries=0 …`, `DEPTH_R82=FAIL`, rc 1.

**Predicate (target).** At the landing revision the command prints `DEPTH_R82 entries=1 ok_entries=1` with `rows=` ≥ 5,
`located_quotes=` ≥ 5 and `fresh_sources=` ≥ 3, then `DEPTH_R82=PASS`, rc 0.

**Controls (executed, committed):** do-nothing `c2-d0` FAIL; round-81 filler pair `c2-d1` FAIL (E1,E6,E7); fabricated
quotes `c2-d2` FAIL (E3); r81-era (pre-egress) sources `c2-d3` FAIL (E3,E4,E6,E7); duplicate cells `c2-d4` FAIL (E5);
four rows `c2-d5` FAIL (E1); placeholder cells `c2-d6` FAIL (E5); unregistered sources `c2-d7` FAIL (E3,E6); positive
`c2-p1` PASS. **Stated boundary:** `c2-b1-salad-boundary` — real fresh quotes with Do/Never cells unrelated to them —
PASSES the counter. The counter certifies grounding, novelty and form; whether a row follows from its quote is K3's
reviewer check, declared here before data.

**Kill rules (frozen):**
- K1: the predicate is not met at the landing revision.
- K2: a counted quote is absent from its committed capture text, or the capture's sha256 differs from its refetch row
  (re-derived by a seat). A live re-open that no longer shows a quote the capture holds is recorded as drift, not a kill.
- K3: a non-author reviewer seat finds one decision row whose Do or Never is contradicted by, or not supported by, its
  warranting quote read in context in the capture → C2 falsified. A repair after scoring does not rescue the claim.
- K4: a base-list entry is shown to already hold a decision table or decision list on choosing or aligning a review
  question frame (PICO levels, PCC, objective–question–eligibility alignment) → C2 falsified (ground already held).

## Frontier step (not a claim)

- Disposition S028 (Crossmark; queued since round 21) from its round-82 capture (`dedff231…`).
- Mine one mistake into `corpus/lessons/round-82.md` `## Mistakes` (candidate: the r81 seat record description that
  did not match its bytes — r4-07).
- Close round-81 routed defects 3 (egress ordering: this file's header) and 4 (G02 receipt committed at the final tip).

## Instrument pins (sha256 at 38f5af82)

Filled by the freeze commit from `sha256sum`; see `instrument-pins.txt` beside this file.
