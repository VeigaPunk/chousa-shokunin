# ChousaR31.CriticAxisFit31 — axis-fit ruling input (pre-data)

Seat: axis critic, round-31 control wave. Frozen revision reviewed: lane tip
`d78d18893849cecb710f3b691ec986e1321d39ee` (claims.md, c1-count.py, c2-count.py
first committed there; read-only `git log`). This seat ran only the base
do-nothing control (8 runs: 4 on the frozen v1 counters, receipts retained; 4
on the lane working tree before the identity check, when c1 was an intermediate
v2 state — see the freeze finding below). It wrote no production lane file (no
gate, counter, claims, SKILL, or SCORECARD edit) and installed no tool. All
citations are `path:line` against the frozen revision; working-tree hash
observations are timestamped in the freeze finding. Excerpts and SHA-256 are in
`ChousaR31.CriticAxisFit31/evidence-manifest.txt` (same directory).

## Ruling summary

1. **C1 = coverage: correct.** It closes a class the lane itself records as a
   named gap ("pairing a span's occurrence with a named pointer line",
   `corpus/README.md:876-877`; the pointer-line vs span-line class "stays a
   named non-coverage", `corpus/README.md:260,565`). Frontier→core edge class,
   with the unmoved command declared (`corpus/evidence/round31/claims.md:59-60`).
2. **C2 = operability: correct label, overclaiming sentence.** The checklist
   item pre-exists (`SKILL.md:66`, unchanged since mint `02a615a:43`) and the
   base gate cannot run its revision clause. But the fixture requires 16 claims
   with **no** revision pin to pass (`corpus/evidence/round31/c2-count.py:51`),
   so 120/120 cannot show the item's stated outcome ("every claim carries …
   revision read"). Reframe the surface sentence pre-data; do not relabel.
3. **Operability is the lowest-scoring non-retired axis.** It is the only
   scored axis (3), so it is the lowest by the lane's own recorded computation;
   no axis is retired, and the stagnation nudge cannot apply because its first
   condition is false (`SCORECARD.md:7,34,488-494`). C2 satisfies the
   lowest-axis obligation only while its operability label stands.
4. **No collapse as labeled.** C1 and C2 are distinct axes and causally
   separable (`claims.md:114-118`). Relabeling C2 to coverage would collapse
   both into one claim (`AXES.md:32-33`); relabeling it to freshness would keep
   two axes but leave no claim on the mandatory lowest axis. Both alternatives
   make the round non-conforming; keep the labels.
5. **Blocking identity defect, not an axis defect.** The lane working tree no
   longer carries the frozen counters: `c1-count.py` and then `c2-count.py`
   were edited during the control wave (self-labelled "design v2"), so control
   receipts now bind at least three counter identities. This must be frozen as
   a versioned re-design (commit + `claims.md` bump + new SHAs) or reverted
   before any data seat. Details in §Freeze finding.

## Freeze finding (blocking, out of axis scope)

The frozen design commit `d78d1889` carries `c1-count.py` SHA-256
`154e09e7f73bebaf0afc2eed4d6c4c4ed8cb47d42518f764560a81fbcd7b555d`
(11931 B) and `c2-count.py`
`20ed105bf93081468934eea4265028cb1274d0115058b35cec72c9cd5694bf72`
(10003 B); the citation manifest recorded both at 04:25:17Z. During this wave
the lane working tree changed twice:

| observed at | c1-count.py | c2-count.py | size / note |
|---|---|---|---|
| 04:25:17Z (manifest) | `154e09e7…` | `20ed105b…` | frozen bytes |
| 04:26:45Z | `d201ef4b…` | `20ed105b…` | c1 11931 B; intermediate v2 |
| 04:29:06Z | `c0a0908c…` | `e26c7751…` | c1 12697 B, c2 11345 B; observed at the 04:30Z audit |

`git diff --stat d78d1889 -- corpus/evidence/round31/c1-count.py
corpus/evidence/round31/c2-count.py` at audit: **110 insertions, 40 deletions**;
the working file self-labels "design v2" (`SUBVARIANTS`; harness errors exit 2).
My receipts bind the frozen bytes (`frozen-v1-*` → `154e09e7…`/`20ed105b…`) and
the intermediate c1 state (`working-v2-c1-*` → `d201ef4b…`, no longer
reproducible from the tree). Consequence: a control receipt's `counter_sha256`
must be checked before pooling; receipts across this wave are not one
instrument. A pre-data re-design is legitimate (`claims.md:127-138`), but only
as a committed version with the predicate and SHA re-frozen in `claims.md`.
The axis ruling below is version-independent: v2 changes fixture
sub-variant draws and harness error/duplicate handling, not C1/C2's contract
surfaces or axis labels.

## Claim/axis table under review

| claim | declared axis (frozen) | surface named | fit evidence | ruling |
|---|---|---|---|---|
| C1 | coverage (`claims.md:13`) | a claim's named line range, frontier→core edge class (`claims.md:15-20`) | `corpus/README.md:186,260,375,565,876-877`; prompt item 9 (`chousa-round-31.md:361-364`); r30 C1 edge-class precedent (`corpus/lessons/round-30-verifier-spotcheck.md:19,120`) | **fit** |
| C2 | operability, lowest axis (`claims.md:62`) | checklist item 1's revision clause becomes runnable (`claims.md:64-71`) | `AXES.md:13`; `SKILL.md:64-66`; pre-existing since `02a615a:43`; `c2-count.py:2-4`; r25 C1/r29 C1/r30 C2 operability precedents (`SCORECARD.md:1343,1603,1687`) | **fit, conditional on the reframe in §C2** |

## C1 — coverage

**Case for.** (i) The moved class is named by the lane as uncovered ground, not
merely absent: `corpus/README.md:260` and `:565` call the pointer-line/span-line
class "a named non-coverage", and `:876-877` lists "pairing a span's occurrence
with a named pointer line" as still unclosed. (ii) The change adds a new input
class and verdict (`"line"` → `mislocated`, `CLAIM_LINE_MISMATCH`,
`claims.md:22-32`), i.e. a governed edge class, exactly what prompt item 9
allows a coverage claim to name (`chousa-round-31.md:363-364`). (iii) The
closest precedent is round 30's C1 — a new edge class inside an existing tool
(`quote-reopen` headless pages) — which the outside spot-check ruled
`coverage improved` (`corpus/lessons/round-30-verifier-spotcheck.md:19,120`).
(iv) The anti-re-scoring clause does not bite: the base gate cannot express
`"line"` at all, so this is not the already-held span rule re-scored on new
inputs (`chousa-round-31.md:362-363`; base before 50/120, `claims.md:54-57`).

**Strongest counterexample from local evidence.** `corpus/README.md:260` says
the class "stays a named non-coverage". Read as an axis ruling, that would say
the lane already decided this class is *not* coverage; and the change could be
called depth/calibration of the existing span check (the r4 boundary-hardening
shape, `SCORECARD.md:186-190`, where the change is filed `calibration`, not
coverage). **Rebuttal:** "named non-coverage" is ledger
status for a named gap (zero surfaces governed), so closing it is precisely
frontier→core; r4 changed matching semantics for *all* inputs (calibration of
the rule), while C1 adds a *new optional input class plus a new verdict*
(edge class) — the r30 C1 shape. The counterexample is a terminology trap, not
a fit defect.

**Ruling: coverage fits.** No relabel.

## C2 — operability vs freshness vs coverage

**Case for operability.** `AXES.md:13` defines the signal as "A checklist item
can be run and produces the stated outcome." The item pre-exists
(`SKILL.md:66`; its text is unchanged since the mint commit `02a615a:43`), and
the base gate cannot run its revision clause (`claims.md:65-67`). The frozen
counter is explicitly framed as that checklist clause made runnable
(`c2-count.py:2-4`). Lane precedent files new runnable checks on operability:
r25 C1's new `verify-metadata` mode scored operability improved at delta 0
(`SCORECARD.md:1343`), r29 C1's new tool (`SCORECARD.md:1603`), and r30 C2's
stated fetch bounds (`SCORECARD.md:1687`,
`corpus/lessons/round-30-verifier-spotcheck.md:19-20`; that claim missed its
predicate, and the closure attributed the failure to the predicate, not the
axis label).

**Strongest case against — freshness.** The new `observed=stale` verdict and
`CLAIM_SOURCE_REVISION_MISMATCH` finding are drift detection, and `AXES.md:14`
defines freshness as "Drift detection — skill claims re-verified against live
surfaces; stale items flagged or fixed." The fixture's stale classes (S1–S5,
`claims.md:87-89`) test exactly that. A hostile reviewer can say the checklist
line is post-hoc framing appended to a drift detector. **Rebuttal:** freshness
requires an actual re-verification result over the lane's claims; C2's 120
sources are synthetic temp files (`claims.md:84-86`) and the no-harm run uses
`claims-r2` with no pins (`claims.md:123-124`), so zero real claims are
re-verified and zero stale items are flagged this round. The check *enables*
freshness; it does not move it. Freshness would be the overclaim, not
operability.

**Strongest case against — coverage.** Structurally, C2 is C1's twin: an
optional JSONL field plus a new observed value in the same mode
(`claims.md:10-11,73-82`). By "name the axis by the surface the round changes",
the `sha256` edge class is a new governed surface, so both claims would be
coverage and collapse (`AXES.md:32-33`). **Rebuttal:** the distinguishing
surface is the *pre-existing checklist obligation*, which C1 does not have.
C1 closes a README named non-coverage; C2 makes an item in the lane's
"Checklist (executable)" runnable. That is `AXES.md:13`'s exact signal. This
tiebreaker is defensible but **must be stated in claims.md**; today it is
asserted (`claims.md:67-71`) without the comparison to C1 or the precedents.

**The concrete pre-data counterexample to the claim's wording.** Checklist item
1 says "Every claim carries a resolvable pointer to the artifact **and revision
read**" (`SKILL.md:66`). In the frozen contract `"sha256"` is optional and its
absence is unchanged behaviour (`claims.md:81`; `c2-count.py:23`), and the
fixture requires 16 no-pin claims to pass as `supported`
(`c2-count.py:51,161`). So even at 120/120 the gate does **not** produce the
item's stated outcome for every claim: it runs the clause only for claims that
opt in. The sentence "this claim makes that item's revision clause runnable"
(`claims.md:68`) is therefore an overclaim a closure reviewer can reject.
**This is a prose defect, not an axis defect**; fix it by reframing to
conditional runnability and naming the residual, not by relabeling.

**Ruling: operability fits, conditionally.** Keep the label; apply §Correction.

## Collapse check

| labeling | axes | consequence |
|---|---|---|
| **C1 coverage + C2 operability (frozen)** | distinct | two claims; lowest-axis obligation met by C2; **compliant** |
| C2 → coverage | one (coverage) | C1+C2 count as one claim (`AXES.md:32-33`); no claim on the lowest axis (`AXES.md:33-34`); round non-conforming |
| C2 → freshness | distinct | no claim on the lowest axis, because operability stays at 3 and the nudge cannot apply (`SCORECARD.md:488-493`); round non-conforming, and freshness overclaimed |

"Do not strengthen C2" note: renaming the `sha256` field as a new edge class
would make it coverage by the same argument as C1 and collapse the round. The
checklist item must remain C2's declared measured surface.

## Lowest-axis check

- Scored axes: operability only, 3, last-change round 1 (`SCORECARD.md:7`).
- Retired: none (`SCORECARD.md:34`).
- The lane's own computability note: operability is the only scored axis; an
  unscored axis is not counted at/above the 8.0 line; "by the only recorded
  score the lowest non-retired axis is operability"; nudge dormant
  (`SCORECARD.md:488-494`). The nudge's first condition ("every axis at or
  above 8.0") is false while operability is 3, so the waiver cannot apply at
  round 31 regardless of the capability window.
- Precedent: r25 "operability (lowest measured, 3/10)"
  (`SCORECARD.md:1373`), r29/r30 "lowest scored axis"
  (`SCORECARD.md:1603,1687`).
- **Answer: yes.** Caveat: it is lowest because it is the *only* scored axis;
  claims.md:62 asserts this without citing the computation. Cite
  `SCORECARD.md:488-494` so the closure can re-derive it.

## Smallest safe correction (before any data seat; prose only)

All four edits are in `corpus/evidence/round31/claims.md` / the landing note;
no counter, gate, or predicate byte changes.

1. **Reframe `claims.md:68`**: "this claim makes that item's revision clause
   runnable" → "this claim makes the revision clause **executable for every
   claim that carries a revision pin**; claims without a pin are unchanged and
   remain a named limit."
2. **Add to `claims.md:140-145` (Not claimed)**: "that every claim carries a
   revision pin; `sha256` is optional and its absence is not drift."
3. **Freeze the exact SKILL.md edit in claims.md**: append the command to item
   1 without altering the obligation bytes, e.g. `- [ ] Every claim carries a
   resolvable pointer to the artifact and revision read (run: bash
   tools/research-gate.sh verify-claims <claims.jsonl> --root .).` The frozen
   text must be in claims.md before data so the landing cannot move the
   goalpost; item 1 already pre-exists at base and mint.
4. **Cite the lowest-axis basis and the delta-0 convention**: add
   `SCORECARD.md:488-494` beside "lowest scored axis" (`claims.md:62`); after
   landing, record operability **3→3, delta 0** with the new observable beside
   it, as r25 C1 (`SCORECARD.md:1343`) and r29 C1 (`SCORECARD.md:1603`) did.
   Do not claim a numeric increase.

Optional, recommended: add one sentence to the C2 surface paragraph stating
why freshness is not the surface (no live re-verification of existing claims;
synthetic fixture only) and why coverage is not (the pre-existing checklist
obligation, not the new field, is the moved surface). This makes the ruling
re-derivable by the outside closure.

## Control/counter evidence table

The axis ruling does not depend on scores, but the base do-nothing control was
run to check the declared before values and the counter identity. All seeds and
receipts below are this seat's, under
`.ufo/waves/round-31/controls/ChousaR31.CriticAxisFit31/`.

| control | counter (identity) | seed(s) | score | receipt path |
|---|---|---|---|---|
| C1 do-nothing, base gate | `corpus/evidence/round31/c1-count.py` at d78d1889, SHA `154e09e7…` (frozen v1) | 31, 32 | 50/120 both, exit 1 | `ChousaR31.CriticAxisFit31/frozen-v1-c1-seed31.json`, `…-seed32.json` |
| C2 do-nothing, base gate | `corpus/evidence/round31/c2-count.py` at d78d1889, SHA `20ed105b…` (frozen v1) | 31, 32 | 50/120 both, exit 1 | `ChousaR31.CriticAxisFit31/frozen-v1-c2-seed31.json`, `…-seed32.json` |
| C1 do-nothing, base gate | working-tree c1 SHA `d201ef4b…` (intermediate v2; superseded) | 31, 32 | 50/120 both, exit 1 | `ChousaR31.CriticAxisFit31/working-v2-c1-seed31.json`, `…-seed32.json` — identity evidence only, not the frozen counter |
| seat run total | 8 runs | — | — | 4 frozen-v1 receipts + 2 intermediate-v2 c1 receipts retained; 2 intermediate-v2 c2 receipts removed (same counter hash and score as the frozen c2 runs) |

The frozen-v1 receipts bind `gate_sha256 = ac1315dd…` and
`counter_sha256 = 154e09e7…`/`20ed105b…`, matching `claims.md:3-7`; the
declared before `50/120` (`claims.md:54-57,101-102`) is reproduced on seeds 31
and 32. Fixture-leak / 120-approach findings: **none claimed by this seat** —
that is the control seats' remit. The blocking pre-data defect is the
counter-identity churn in §Freeze finding; the axis defect is C2's
full-runnability overclaim above.

## Impacted axes

coverage (C1), operability (C2), freshness (C2 side effect: enabled, not
moved), calibration (label accuracy — this review; a mislabel would harm it).
adjacency/depth: no change claimed.

## Verdict

**Design holds on axis naming** — C1 coverage and C2 operability are correctly
distinct and should be kept; apply the four pre-data prose corrections (C2
conditional-runnability reframe + named limit + frozen SKILL edit + delta-0
citation). Do **not** relabel C2 to coverage (collapses the round to one claim
and removes the mandatory lowest-axis claim) or to freshness (no live
re-verification; same lowest-axis failure).

**The counter freeze does not hold** — `c1-count.py` and `c2-count.py` are
modified in the working tree and changed during the wave (110+/40− versus
d78d1889; self-labelled v2). The L1 must commit/re-freeze a versioned re-design
with updated `claims.md` SHAs (or revert) and group control receipts by
`counter_sha256` before any data seat. This is independent of the axis ruling.
