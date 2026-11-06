# Round 82 — critic claims review (R82CriticClaims)

Seat: critic, leaf, no network, no lane/fleet writes. Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Revisions attacked: base `142b6f0c08e645ef9507f6d880be44e518c39043`, egress `5d792e1e953649e801d9bf1f64093b1f0d4dac8c`,
prefreeze `38f5af8268b2807811dded3d7d7221ff3f509495`, freeze `57c0d16795db97ed09b69034e335e725ce577285`, landing
`b4a41d251b488f06b4a6ab01a11bc12ce72edd20`, current tip `46dd1dc3`. All trees were `git archive <rev> | tar -x` copies under
`/fast/scratch/hyaku/chousa-r82/R82CriticClaims/`, removed before yield; every receipt named below was copied into this
folder first. No tool was installed or upgraded.

**Headline.** The frozen C1 predicate is met (K1), and the frozen C1 kill rule **K2 fires**: a record that differs from
`item2-pass.md` in exactly one claim-`sweep` cell set to a declared placeholder (`n/a`) passes the frozen item-2 Run line
at the landing revision (rc 0), because a `## Sweeps` row's `claim_id` names the claim and both gates accept that back-reference without reading the
placeholder (even the **empty** cell passes). 36/36 tested cell strings (the 26 declared values plus decorated/upper-case
variants) pass in that position;
the same 36 values are refused 36/36 when the `claim_id` back-reference is removed (the manifest's own V2C shape). A second,
weaker kill-rule path is K3 (harm): two seat-authored records that the base gate passes and that carry no K2 form are
refused at landing by the new "any heading containing reject" reader.

---

## 1. Ordering — egress, controls, freeze (all pass)

Command: `git -C <lane> log --format='%H %cI %s' 142b6f0c..b4a41d25` and an `awk` over
`corpus/evidence/round57/refetch.tsv`; receipt `ordering-receipt.txt`.

| check | observed | verdict |
|---|---|---|
| egress table committed before any round-82 fetch | egress commit `5d792e1e` at `2026-11-06T16:41:56-03:00` = `19:41:56Z`; first round-82 row `S008` `fetched_utc=2026-11-06T19:42:03Z`; the five round-82 rows are 19:42:03–19:42:10Z and all five URLs match the table's intended-target list | PASS |
| the 18:44Z rows are not round-82 | `S203`–`S208` (18:44:29–18:44:31Z) are present in base `142b6f0c:refetch.tsv` (round-81 rows) | PASS |
| egress commit carries no fetch bytes | `git diff --name-status 142b6f0c..5d792e1e` = `A .ufo/waves/round-82/census-start.txt`, `A corpus/evidence/round82/egress-approval.md` only | PASS |
| freeze diff touches only claims/pins/receipts | `git diff --name-status 38f5af82..57c0d16` = 17 `A` rows: `claims.md`, 14 control receipts, `summary.tsv`, `instrument-pins.txt` | PASS |
| freeze before any gate/entry byte | gate at freeze sha256 `d5d48128…` = the prefreeze pin; `git cat-file -e 57c0d16:corpus/knowledge/question-framing-frames-r82.md` → rc 128 (absent) | PASS |
| claims not amended after scoring | `claims.md` sha256 `9d0350d3699fc3acac34f1ab93b161a5da10f5dc2119cd468aca5a3c8e538fbe` at freeze, landing, tip `46dd1dc3`, and worktree | PASS |
| counters/manifest/base-list not changed after freeze | landing shas = `instrument-pins.txt`: `k2-gate-r82.py 4d6ba055…`, `depth-r82.py 726d3ed9…`, `run-controls-r82.sh 74940be2…`, `c1-manifest.tsv 16ab568…`, `base-knowledge.txt 9d5dcc0d…`; `git diff 38f5af82..b4a41d25 -- corpus/evidence/round82/` lists only the freeze-added claims/receipts/pins | PASS |
| controls executed against the prefreeze tree, then committed | every receipt header reads `at REV 38f5af8268b2807811dded3d7d7221ff3f509495`; I re-ran both counters on that tree — C1 `RUNLINES=2/2 K2_REFUSED=0/11 HOLD_REFUSED=9/9 CLASS_REFUSED=2/24 POSITIVE=5/6` `K2_GATE=FAIL` rc 1 (`c1-prefreeze-remeasure.txt`), C2 `DEPTH_R82 entries=0 … FAIL` rc 1 (`c2-prefreeze-remeasure.txt`) — identical to `controls/c1-k0` and `controls/c2-d0` | PASS |
| receipt ↔ summary | `controls/summary.tsv` 14 rows, expected = observed on all 14 (14/14). Minor: the driver's `CONTROLS_AS_EXPECTED=14/14` line is not itself committed; `summary.tsv` is the tally | pass with residual |

Receipts: `ordering-receipt.txt`, `freeze-and-identity-receipt.txt`, `c1-prefreeze-remeasure.txt`, `c2-prefreeze-remeasure.txt`.

## 2. Frozen predicates at the landing revision

| claim | command | observed | receipt |
|---|---|---|---|
| C1 | `D=$(mktemp -d -p <scratch>) && git archive b4a41d25 \| tar -x -C "$D" && python3 -B "$D/corpus/evidence/round82/k2-gate-r82.py" --root "$D"` | `MANIFEST_SHA256=16ab5682… RECORDS_DIGEST=7dc17486… rows=50`; `RUNLINES=2/2 K2_REFUSED=11/11 HOLD_REFUSED=9/9 CLASS_REFUSED=24/24 POSITIVE=6/6`; `K2_GATE=PASS`; **rc 0** | `c1-landing-remeasure.txt` |
| C1 selftest | `bash tools/research-gate.sh --selftest` (same archive tree) | `RESEARCH_GATE_SELFTEST: PASS (280 cases, 0 skipped)`; **rc 0** (≥ 275, 0 skipped) | `c1-selftest-remeasure.txt` |
| C2 | same form with `depth-r82.py` | `ENTRY question-framing-frames-r82.md ok=yes rows=9 quotes=11/11 fails=-`; `DEPTH_R82 entries=1 ok_entries=1 rows=9 located_quotes=11 fresh_sources=4`; `DEPTH_R82=PASS`; **rc 0** | `c2-landing-remeasure.txt` |

The landing C1 line is byte-identical to `corpus/evidence/round82/after/c1-after.txt` (including the manifest and records
digests), and the C2 line to `after/c2-after.txt`. K1 holds for both claims.

## 3. Attack 2 — the cheapest trees that reach each predicate

### 3a. C1: a manifest-keyed gate over the unmodified base gate

Cheap tree: landing archive with `tools/research-gate.sh` replaced by a 24-line dispatcher that reads
`corpus/evidence/round82/c1-manifest.tsv` from the tree, prints the row's `need` finding and exits 1 for every `refuse`
row, prints `RESEARCH_GATE: CLEAN` + both `REJECTIONS_OK=1/1` and `REJECTIONS_OK=3/3` for every `pass` row, and delegates
every other record to the **unmodified base gate `5d792e1e`**; `--selftest` is a literal banner. Source and run:
`cheap-c1-fake-gate-and-selftest.txt`; score: `cheap-c1-basefallback.txt`.

Observed: `RUNLINES=2/2 K2_REFUSED=11/11 HOLD_REFUSED=9/9 CLASS_REFUSED=24/24 POSITIVE=6/6`, `K2_GATE=PASS`, **rc 0**;
`bash tools/research-gate.sh --selftest` prints `RESEARCH_GATE_SELFTEST: PASS (280 cases, 0 skipped)`, rc 0 — without
running 280 cases. Out-of-manifest K2 records under the same frozen Run lines: `G4F-na` rc 0, `G4F-idem` rc 0,
`B-emptyflip` rc 0, `A-placeholder-cell-claimid` rc 0, `G2C-na` rc 0, `H-rejectheading-why-col` rc 0
(`cheap-c1-k2-probes-basefallback.txt`).

What it needed: the frozen manifest, which lives in the tree under test, and nothing else. Is it the claimed work in
disguise? **No** — it refuses nothing outside the manifest and would fail K2 on the records above; it is a forgery. The
point is that the frozen predicate cannot distinguish the landed general rule from this fixture-keyed forgery, because the
manifest and the expected finding ids are inside the subject tree. (Round-80's name-keyed-score defect, `round-80-verifier-
spotcheck.md:26`, is the same instrument shape; the r82 controls `c1-f2`/`c1-f3` only reject a *generic*-finding or
*Run-line*-keyed forger, not a manifest-reading one.) The landed gate is not this tree — see §4 for the generality probes
and the one position where it does fail K2.

### 3b. C2: the positive-control fixture reused as the new entry

Landing archive minus `question-framing-frames-r82.md`, plus `c2-controls/P1-positive/ctl-entry-r82.md` into
`corpus/knowledge/` and the fixture's `s008-replace.txt`/`sources-append.txt` overlay (as the prefreeze driver applies it).
Observed: `ENTRY ctl-entry-r82.md ok=yes rows=5 quotes=5/5 fails=-`; `DEPTH_R82 entries=1 ok_entries=1 rows=5
located_quotes=5 fresh_sources=4`; `DEPTH_R82=PASS`, rc 0. Receipt `cheap-c2-fixture-reuse.txt`. The landing entry is not
this fixture (9 rows / 11 quotes / 4 sources vs 5 / 5 / 4; different text), but the counter would not have known.

### 3c. C2: S-rows faked with a hand-written capture and refetch row

Landing archive minus the real entry, plus a seat-authored entry citing invented `S900`–`S902`, three hand-written
`corpus/captures/<sha256(url)[:24]>.txt` files, three appended `refetch.tsv` rows dated `2026-11-06T20:00:00Z` with matching
`txt_sha256`, and three `mined` SOURCES rows naming the entry. Observed: `ENTRY hand-written-ground-r82.md ok=yes rows=5
quotes=5/5 fails=-`; `DEPTH_R82 … PASS`, rc 0. Receipt `cheap-c2-fake-capture.txt`. The counter's FRESH rule is a committed
row coincidence; it never asks for the `.raw` bytes or for text extraction provenance, so a self-written `.txt` scores.
The landing captures are not this: all five `.raw` and `.txt` sha256 values equal their refetch rows' `raw_sha256`/
`txt_sha256` and the `.raw` files are real HTML bodies (`captures-vs-refetch-receipt.txt`). Both cheap C2 trees are
counter limitations, not landed work.

## 4. C1 kill rules — K2 fires, K3 fires

### 4.1 K2(a) — claim-`sweep` placeholder accepted through a `claim_id` back-reference (kill)

Record: `item2-pass.md` with exactly one cell changed, the `N1` claim's `sweep` cell `W1` → `n/a` (`attack-k2a-record.md`;
the one-line diff and the run are in `attack-k2a-claim-sweep-placeholder.txt`). Frozen item-2 Run line, landing tree:

```
f=<attack>.md; ! bash tools/research-gate.sh verify "$f" --root . | grep -q '^FINDING NEGATIVE_WITHOUT_SWEEP' \
  && bash tools/research-gate.sh verify-sweeps "$f" --root .
…
VERIFIED_SWEEPS=1/1 REJECTIONS_OK=1/1
RESEARCH_GATE: CLEAN (… findings=0 drift=0)
rc=0
```

K2(a) says: any record differing from `item2-pass.md` in one claim-`sweep` cell set to a declared-vocabulary value on
which the frozen item-2 Run line exits 0 → C1 falsified. This is that record, and the exit code is 0.
The mechanism: `verify`'s empty-cell check (`NEGATIVE_WITHOUT_SWEEP`) is also satisfied when a `## Sweeps` row's
`claim_id` names the claim (`research-gate.sh:1330-1350`), and the new negative-resolution block sets `nres=1` as soon as
any `## Sweeps` row's `claim_id` equals the claim id, before the placeholder cell is examined. An empty-cell variant of the
same one-cell edit also exits 0 (`attack-k2a-claim-sweep-placeholder.txt`, second case). Scope measured by `probe-driver.py` over 193 seat-authored records (`k2k3-probes.txt`,
`probe-summary.txt`):

* cell strings in the claim-`sweep` cell with a resolving `claim_id` row: **0/36 refused** (all 36 pass, including the
empty cell and `n/a`, `na`,
  `n.a`, `none`, `nil`, `null`, `tbd`, `tba`, `todo`, `?`, `??`, `...`, `…`, `x`, `unknown`, `not applicable`, `same`,
  `ditto`, `see above`, `idem`, `-`, `--`, `---`, `—`, `–`, decorated/upper-case forms and a blank-looking cell);
* the same 36 values with the `claim_id` cell cleared: **36/36 refused** (`SWEEP_NEGATIVE_UNRESOLVED`), matching the
  manifest's `V2C-*` records, which are built with a non-matching or absent `claim_id` (`v2-sweepcell-w9-withsec.md`
  points `W1` at `N7`);
* all declared values in item-4 flip **36/36 refused**, item-4 reason **36/36**, item-2 `where` **36/36**.

Smallest safe correction: in `verify_sweeps`' negative-claim loop, treat an **empty or declared-placeholder** `sweep`
cell as unresolved regardless of a `claim_id` back-reference (emit `SWEEP_NEGATIVE_UNRESOLVED`); keep the back-reference
rescue for non-placeholder prose cells. That keeps the manifest's `V2C-*` expectations and the positive controls intact —
every positive fixture's negative claim names `W1`/`W2` (and the selftest's prose-pass case names `SW1`), so none relies
on the rescue. (Changing `verify` instead would break the manifest: an item-2 `refuse` row whose stage 1 emits
`NEGATIVE_WITHOUT_SWEEP` never reaches `verify-sweeps`, and the expected `SWEEP_NEGATIVE_UNRESOLVED` would be missing.) Note the counterargument: a resolving `claim_id` genuinely identifies the sweep, so
one could argue the record is substantively resolved — but K2(a) as frozen has no such exception, and the declared class is
"a cell equal to one of …" without one.

### 4.2 K3 (harm) — a complete rejection refused, and a non-rejection table read as rejections

Two seat-authored records (`probe-H-rejectheading-why-col.md`, `probe-H-criteria-section.md`) that the base gate
`5d792e1e` passes (`base_rc=0`) and the landed gate refuses (`rc=1`, `SWEEP_REJECTION_INCOMPLETE`):

* `## Rejected sources` with header `| id | ref | why | flip |` and both cells substantive. The landed reader takes only a
  `reason` column as the reason (`cell "$rrow" reason`), so the row reads "reason absent" and is refused although its
  reason is present under `why`. (The flip side already accepts `flip`, `flip_condition`, `falsifier`, `reversal`, … —
  the reason side has no synonyms.)
* `## Rejection criteria` with a `| criterion | state |` table. The new rule reads *any* table under *any* heading whose
  text contains "reject", so a criteria table is counted as kept rejections and refused. This record is not a rejection at
  all, so it carries none of K2's forms → K3 by the frozen text.

Receipt lines: `k2k3-probes.txt:192` (`H-rejectheading-why-col … rc=1 … base_rc=0`) and `:195`
(`H-criteria-section … rc=1 … base_rc=0`). The intended case still works: a complete rejection under `## Rejected
sources` passes at both (`P-rejectheading-complete … rc=0`, `:196`).

Smallest safe correction: read a reject-containing section only when its table is rejection-shaped (a reason/flip-ish
column or a ref/id pair), and accept `why`/`rationale`/`justification`/`basis` as reason synonyms — the same permissiveness
the flip side already has. Blank or placeholder reason/flip cells under those headings stay refused, so K2(b)'s intended
refusals (`B-emptyflip`, `B-placeholder-reason`, `B-nested-heading`: 3/3 refused) are unaffected. One reading of K2(b)
could treat the missing `reason` column as "an empty reason cell" and call this the intended refusal; the record's reason
is not empty, so I report it as harm and let the judge rule.

### 4.3 K2(b)/K2(c) — held

New reject headings with a blank or placeholder flip/reason are refused 3/3; a negative claim naming an undeclared sweep
id with no matching `claim_id` is refused (`C-undeclared` rc 1). The `C-undeclared-withsec` record (sweep `SW9`, but a
`## Sweeps` row's `claim_id` names the claim) passes — that is the K2(c) exception, not a violation.

## 5. C2 kill rules — held

* K1: predicate met (§2).
* K2: all 11 counted quotes occur verbatim (normalized) in the committed captures; all five capture `.txt` sha256 values
  equal their round-82 refetch rows' `txt_sha256` (and the `.raw` values equal `raw_sha256`); `captures-vs-refetch-receipt.txt`.
* K3 (semantic review, this seat is non-author): every row read against its quote in context (Cochrane ch.2 around
  chars 14.8k–16.0k and 50.4k; JBI 10.2.3 around 3.1k–4.5k; 10.2.4 around 2.8k; 10.2.2 around 3.6k). No row is
  contradicted. Weakest row: "define each element only as precisely as the question needs" (Q4, S008) — the quote says
  equal emphasis and equal precision "is not necessary", which supports the Do; the paired Never ("pad every element to
  the same level of detail") is a strengthening, not a contradiction. Recorded, not scored as a kill.
* K4: no base entry holds a decision table or decision list on choosing/aligning a review question frame. The four
  `## Decision table` headings in the tree are `citation-searching-tarcis-r81.md`, `correction-retraction-status-r81.md`,
  `recheck-due-r26.md` and the new entry; `PICO`/`PCC` occur only in the r48 entry (one instrument's optional PICOS
  sentence) and the new entry; no base entry cites the S008 chapter-02 URL or names `S008`; the two claimed near
  neighbours match (`archived-export-intake.md:89` is CL-07's "question framing before search" archive claim with no
  decision rows; `quality-control-guideline-issued-text-r48.md:26` is the PICOS-optional bullet). Receipt
  `k4-novelty-receipt.txt`.

## 6. Attack 4 — causal separability (pass)

* C1 on the landing tree with `corpus/knowledge/` and `corpus/SOURCES.md` at `38f5af82` (no candidate entry): the C1
  counting command prints the full predicate line, `K2_GATE=PASS`, rc 0 — `causal-c1-prefreeze-knowledge.txt`.
* C2 on the landing tree with `tools/research-gate.sh` and `SKILL.md` at `38f5af82` (the base gate): `ENTRY
  question-framing-frames-r82.md ok=yes rows=9 quotes=11/11`, `DEPTH_R82=PASS`, rc 0 — `causal-c2-prefreeze-gate.txt`.

Each claim verifies without the other's landed surface.

## 7. Attack 3 — axis labels

* **C1 = operability is defensible.** `AXES.md:13` defines operability as "Runnable artifacts: checklists that are
  executable, commands that exist, scripts that run", signal "A checklist item can be run and produces the stated
  outcome". Before the change the item-2/item-4 Run lines ran but produced the *opposite* of the stated outcome on the K2
  forms; the landing makes the item produce its stated refusal, and the selftest grew 275 → 280 with the five new cases
  (53–57). That is the operability surface. Calibration (`AXES.md:15`) is self-assessment quality (gaps named honestly,
  SHONEN/SCORECARD matching repo state) — not this change. The lane's round-4 row used "calibration" for a
  matching-semantics fix (`SCORECARD.md:165`), which is an internal label inconsistency, not a defect here. Caveat: the
  SCORECARD's operability number (3/10) is the round-1 construct over three archived inputs (`SCORECARD.md:7`) and is not
  re-measured by this round; the verdict is "improved narrowly" with the number frozen, precedented by the round-81 row.
* **C2 = depth is correct by the §9 surface rule.** The surface changed is a `corpus/knowledge/` entry: a decision table
  with cited sources — exactly `AXES.md:11`'s depth definition. Coverage is "fraction of the domain's real surfaces"
  (`AXES.md:12`); this round does not measure a fraction of PROVINCE. Naming it coverage would be label drift of the r80
  class. Defensible.
* The r80 lesson "name the draw by path" does not apply: both round-82 counters are fixed commands over committed bytes,
  with no draw or seed.

## 8. Attack 5 — is the closed vocabulary a narrow, list-memorizing fix?

* **For:** the fix is a 26-value closed list (`sweep_is_placeholder`), and the frozen predicate's class family is a fixed
  24-row sample. My manifest-keyed forgery scores the exact predicate line, so the measurement certifies a fixture
  response, not a concept. Values outside the list (`pending`, `no flip`) still pass and are declared residuals. Within
  the class the gate is position-limited: the claim-`sweep` + `claim_id` position is not refused at all (§4.1). A user
  can still evade with "pending".
* **Against:** the list was declared and frozen before data, so it is a specification, not a guess; the gate applies it
  to any record from any author (my 36-value × 4-position scan shows no per-fixture keying: 36/36 refused in flip, reason,
  `where`, and 36/36 in the sweep cell without a `claim_id`); the heading and negative-resolution changes are structural,
  not a list; the one gap is a bug in the resolution order, not memorization. The honest statement: the *implementation*
  generalizes within the declared class (minus §4.1), while the *predicate* cannot separate it from a fixture-keyed
  forgery, because the answer key lives in the subject tree.
* Residual on "any record": the K3 harm cases (§4.2) show the new heading rule is broader than the class, which is the
  opposite failure mode.

## 9. Attack 6 — frozen rules changed after scoring

None found. `claims.md` is byte-identical at freeze, landing, tip and worktree (`9d0350d3…`); counters, manifest and
`base-knowledge.txt` at landing equal `instrument-pins.txt`; the item-2/item-4 Run lines are byte-identical to the frozen
base text (the counter prints `RUNLINE item=2 found=yes` / `item=4 found=yes`, and `SKILL.md`'s only changes are prose,
`SKILL.md` sha `f34e8b33…` → `43e9b5ed…`); the selftest case count changed only upward (275 → 280, allowed). Receipt
`freeze-and-identity-receipt.txt`.

## 10. Frontier items (declared "not a claim", reviewed for completeness)

* **`corpus/lessons/round-82.md` is absent at the landing revision and at the current tip** (`git cat-file -e
  b4a41d25:corpus/lessons/round-82.md` → rc 128), while the landing's README section already points at it
  (`corpus/README.md`, round-82 block: "- `lessons/round-82.md` — S008 re-opened … gate fix"). The frontier step "Mine one
  mistake into `corpus/lessons/round-82.md` `## Mistakes`" is therefore unlanded at the reviewed tip and the README carries
  a dangling path. (An untracked `corpus/evidence/round82/mistake-r4-07.txt` exists in the worktree — someone is mid-work;
  the finding is the state at the landing/tip I reviewed.)
* **No G02/PREFLIGHT receipt is committed for this round** — `grep -rn 'G02\|PREFLIGHT' corpus/evidence/round82/` finds
  only the claims-file sentence claiming the closure. The G02 behavior itself is green: `python3 tools/lane-preflight.py
  --root <landing tree> --only G02` → `GATE G02 knowledge-index PASS 94 entries indexed`, rc 0 (`g02-landing.txt`), and
  the full worktree preflight at the tip is `PREFLIGHT=8/8 … rc=0` (`preflight-worktree-8of8.txt`). Round-81 routed defect
  4 asked for the *receipt* at the final tip; the behavior is restored, the receipt is not committed.

## 11. Controls and no-harm

The 14 prefreeze controls are real and reproducible: the four C1 controls (k0 do-nothing, f1 blanket refuse, f2
wrong-finding-keyed, f3 keyed Run line) and the ten C2 controls (d0–d7, p1, b1) all re-derive the committed before/after
numbers on the prefreeze tree (§1), and the landing positives 6/6 include the alt-heading complete rejection. The
`c2-b1-salad-boundary` PASS is a declared boundary (grounding/form, not entailment), not overclaiming. My one no-harm
result against the landed gate is §4.2.

## 12. Verdicts

VERDICT: R82CriticClaims C1 fired — kill rule K2(a): `item2-pass.md` with exactly one claim-`sweep` cell set to `n/a` exits 0 under the frozen item-2 Run line at landing because a ` ## Sweeps` row's `claim_id` resolves the claim; 36/36 tested cell strings (the 26 declared values plus decorated variants, including the empty cell) pass in that position, and the same 36 are refused once the back-reference is removed, plus K3 harm on reject-heading tables (`why`-column rejection, criteria table: base 0 → landing 1).
VERDICT: R82CriticClaims C2 held — K1 met (`rows=9 located_quotes=11 fresh_sources=4`, rc 0), K2 quote/capture-sha checks hold, K3 found no row contradicted by its quote in context (weakest: the Q4 "pad every element" Never), K4 no base entry holds a question-framing decision table/list.

Limits of this review: no network was used, so no live re-open was performed — C2's K2 was re-derived from the committed
capture bytes and their refetch rows only; the gate selftest was run once at landing (and once more inside the worktree
preflight), within the seat's two-run cap; no lane, fleet or fixture git state was mutated.
