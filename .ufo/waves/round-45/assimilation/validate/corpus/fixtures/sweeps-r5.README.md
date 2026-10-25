# sweeps-r5.md / sweeps-r5-broken.md / sweeps-r5-hit.md — pre-registered rejection + sweep fixtures (chousa round 5)

Round-5 coverage move (dispatch 2026-10-16): the round-1 gate checks kept
rejections and negative sweeps STRUCTURALLY only. A rejection passes `verify`
as long as its `reason` cell is non-empty — no flip-condition is required; a
negative sweep passes as long as its `sweep` cell is non-empty — the sweep
never has to name where it looked, and a sweep claiming an emptiness that is
false passes just the same. These fixtures pre-register, as fixed local inputs
with fixed expected outputs, the new `verify-sweeps` mode's job: every kept
rejection carries a non-empty reason AND flip-condition, and every negative
sweep names a path set whose claimed emptiness is re-checked locally (a hit is
`SWEEP_CLAIM_FALSE` naming the hit; a non-local target stays exempt but
counted).

`sweeps-r5.md` is the positive control: 3 real kept rejections (each with
reason + flip_condition) and 2 negative sweeps. W1 is local — it names the
glob path set
`research/deep-research-2026-09-28/kotobank-*,research/deep-research-2026-09-28/saved-*`,
which the mode re-runs against the pinned revision and which matches nothing,
so the claimed emptiness verifies; W2 is non-local (`https://kotobank.jp/`) and
stays exempt but counted — expected CLEAN, exit 0.

`sweeps-r5-broken.md` is the tampered control: rejection R1 carries a reason
but no flip-condition, and local sweep W1 names
`chousa-shokunin/corpus/fixtures/sweeps-r5-hit.md`, a planted file the glob
really matches — expected DRIFT, exit 1, naming `SWEEP_REJECTION_INCOMPLETE`
and `SWEEP_CLAIM_FALSE` with the hit.

## Authoring state

Lane HEAD `45f8f65…`; the fixtures are uncommitted under `corpus/fixtures/`;
no commits by this seat. `verify-sweeps` did not exist at the round-4 revision
(gate sha256 `6b83705b02fe11e98b8b4aeb43fe718ff9910d21cee16d87366cef648a3960b2`,
also `git show HEAD:tools/research-gate.sh`), where both fixtures passed the r1
`verify` path CLEAN — the pre-move hole this round closes. Measured 2026-10-16
~00:56Z, fresh processes, `--root ..` from the lane cwd:

```text
verify corpus/fixtures/sweeps-r5.md        → CLEAN (findings=0 drift=0 questions=1 sources=4 chains=3 claims=3 negatives=2 rejections=3 approvals=1), exit 0
verify corpus/fixtures/sweeps-r5-broken.md → CLEAN (findings=0 drift=0 questions=1 sources=1 chains=1 claims=1 negatives=1 rejections=1 approvals=1), exit 0
```

The mode landed during the wave and the gate sha was observed moving while it
was written (`df7ec322…` → `ba0c1744…` → `ea673ddb…` → `0ed21cc8…` →
`f8499d0f…` → `2fd4f7c7…` → `b701bef6…` → `55adb92d…`); the Execution record
below pins the revision the receipts were taken at. Any later revision that
keeps the documented `where`/flip contract should reproduce them.

## Cited sources (pinned, read-only)

The three archived deep-research exports under
`research/deep-research-2026-09-28/` (fleet root, read-only), pinned to fleet
commit `0863746e9da95457f71b9e00a40361b88ab0df15`; sha256 re-derived
2026-10-16 and matching LOG.md:105-108:

```text
9033857d4625555c7b778dfad6df80e3e1b24ed8bffa3fee2fd445b9c5540b85  A-shokunin-tradition.md
6d8dbddd3e2d2f47dcb153c5a3347cc6321db4afc72cf07da40f0f7fe5022006  B-multiagent-knowledge.md
e48fe70ff92055c217ac6ca6ce68e403aa5689fee8717f3bd0ccf5badc92321b  C-rank-taxonomy.md
```

Pointer cells are fleet-root-relative; the re-run passes `--root ..` from the
lane cwd (the round-1 convention). The record also cites the lane's own round-1
intake `corpus/knowledge/archived-export-intake.md` as S4 (the source of the
kept rejections and of sweep W1's observed cell). No URL source is opened; the
single URL string in `sweeps-r5.md` (hop 3, `https://kotobank.jp/`) is
pre-marked `blocked-no-fetch` — exempt and counted, never fetched.

## Rejections — provenance and flip-conditions

All three are real kept rejections from this lane's round-1 intake
(`corpus/knowledge/archived-export-intake.md`, RJ-02/RJ-03/RJ-04), reduced to
the fixture row shape; the flip-condition column is round 5's addition and
states what evidence would un-reject the item.

| id | ref | reason (from the method) | flip_condition |
|---|---|---|---|
| R1 | research/README.md:12 | the gloss asserts jin'i-ryu is not an attested artisan rank while A:47/A:64 record only failed substantiation (intake RJ-02) | an attested Japanese spelling carried by a local source |
| R2 | B-multiagent-knowledge.md:79 | the ACE numerals are kengaku-province model-quality claims (intake RJ-03) | a kengaku-lane adjudication of those numerals |
| R3 | B-multiagent-knowledge.md:63 | the work table is an export-unverified bibliography whose only onward hop is citation furniture (intake RJ-04) | locators resolving inside the corpus boundary |

## Sweeps — provenance and ground truth

The landed `verify-sweeps` contract reads a `where`-style cell and re-runs a
local path set as a GLOB against `--root` (`cd "$ROOT"`, `nullglob`): zero
matches = `observed=verified`; any match = `SWEEP_CLAIM_FALSE` naming the
match; non-local targets (`http(s)://…`, `local://…`, `external:…`,
`session:…`) and declared source ids are exempt but counted. A local sweep is
therefore phrased as a path-set absence — the class the mode can re-check.

W1 (`where=research/deep-research-2026-09-28/kotobank-*,research/deep-research-2026-09-28/saved-*`)
is a real provenance negative from this lane's method: nothing external was
ever fetched or cached, so no saved copy of a cited external page sits in the
archive directory. Measured emptiness under the re-run's own resolution:

```bash
cd ..
shopt -s nullglob globstar
for m in research/deep-research-2026-09-28/kotobank-* research/deep-research-2026-09-28/saved-*; do echo "$m"; done
```

→ no output (zero matches). The intake's own content census (its W2, "no URL
locator exists in the archive set", remeasured there) is the same negative
family; the mode re-runs the path-set half only — the content half stays a
recorded census (Honest boundaries).

W2 is non-local by construction: the attestation sought for jin'i-ryū sits
behind an external dictionary (`https://kotobank.jp/`), outside the corpus
boundary and outside the loopback window; the sweep is recorded, exempt, and
never re-run — it is counted, not trusted.

`sweeps-r5-hit.md` is the planted hit for the broken control: it exists under
`corpus/fixtures/`, so the broken control's W1 glob
`chousa-shokunin/corpus/fixtures/sweeps-r5-hit.md` matches it (one hit). The
file carries the token `ghost-sweep-token` on its line 4 as a human marker; the
mode's re-run is an existence check and never reads those bytes.

## The broken control is the round's falsification

`sweeps-r5-broken.md` differs from the positive control in exactly two
structural ways: R1's flip-condition cell is empty (its reason stays present),
and W1 names a path set that really matches — the planted
`corpus/fixtures/sweeps-r5-hit.md`. Both are indistinguishable from a healthy
record to the r1 `verify` path (measured CLEAN, exit 0). Under `verify-sweeps`
the record must DRIFT, exit 1, with `SWEEP_REJECTION_INCOMPLETE` on R1
(`missing=flip`) and `SWEEP_CLAIM_FALSE` on W1 naming the hit
(`first=chousa-shokunin/corpus/fixtures/sweeps-r5-hit.md`). If a future
revision passes either fixture CLEAN, the round-5 claim is falsified.

## Execution record

Gate revision `55adb92d0ba5ac958907fac6c4d5d6b0b50129703e866a5befbd9a32789f2ff2`
(sha256, re-checked identical before and after every run below), lane cwd,
fresh processes, `--root ..`, no network. Verbatim stdout:

```text
$ bash tools/research-gate.sh verify-sweeps corpus/fixtures/sweeps-r5.md --root ..
research-gate research-gate-r1 — ts=2026-10-16T01:12:02Z — mode=sweeps — record=corpus/fixtures/sweeps-r5.md
SWEEP id=W1 where=research/deep-research-2026-09-28/kotobank-*,research/deep-research-2026-09-28/s looked=local hits=0 at=- observed=verified verdict=match
SWEEP id=W2 where=https://kotobank.jp/ looked=non-local hits=- at=- observed=exempt verdict=exempt
REJECTION id=R1 ref=research/README.md:12 reason=present flip=present observed=complete verdict=match
REJECTION id=R2 ref=research/deep-research-2026-09-28/B-multiagent-knowledge.md:79 reason=present flip=present observed=complete verdict=match
REJECTION id=R3 ref=research/deep-research-2026-09-28/B-multiagent-knowledge.md:63 reason=present flip=present observed=complete verdict=match
VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3
RESEARCH_GATE: CLEAN (sweeps=2 verified=1 exempt=1 hit=0 refused=0 invalid=0 rejections=3 rejections-ok=3 findings=0 drift=0)
exit=0

$ bash tools/research-gate.sh verify-sweeps corpus/fixtures/sweeps-r5-broken.md --root ..
research-gate research-gate-r1 — ts=2026-10-16T01:12:02Z — mode=sweeps — record=corpus/fixtures/sweeps-r5-broken.md
SWEEP id=W1 where=chousa-shokunin/corpus/fixtures/sweeps-r5-hit.md looked=local hits=1 at=chousa-shokunin/corpus/fixtures/sweeps-r5-hit.md observed=hit verdict=mismatch
REJECTION id=R1 ref=research/README.md:12 reason=present flip=absent observed=incomplete verdict=mismatch
FINDING SWEEP_REJECTION_INCOMPLETE severity=warn surface=sweeps obs=id=R1 missing=flip
FINDING SWEEP_CLAIM_FALSE severity=warn surface=sweeps obs=id=W1 where=chousa-shokunin/corpus/fixtures/sweeps-r5-hit.md hits=1 first=chousa-shokunin/corpus/fixtures/sweeps-r5-hit.md listed=chousa-shokunin/corpus/fixtures/sweeps-r5-hit.md
VERIFIED_SWEEPS=0/1 REJECTIONS_OK=0/1
RESEARCH_GATE: DRIFT (sweeps=1 verified=0 exempt=0 hit=1 refused=0 invalid=0 rejections=1 rejections-ok=0 findings=2 drift=2)
exit=1
```

The W1 display above is cut at the mode's own 80-character `where=` cap
(`…/s`); the cell itself names both globs.

r1 and chain regressions at the same revision (both fixtures, `--root ..`):

```text
verify  sweeps-r5.md        → RESEARCH_GATE: CLEAN (findings=0 drift=0 questions=1 sources=4 chains=3 claims=3 negatives=2 rejections=3 approvals=1), exit 0
verify  sweeps-r5-broken.md → RESEARCH_GATE: CLEAN (findings=0 drift=0 questions=1 sources=1 chains=1 claims=1 negatives=1 rejections=1 approvals=1), exit 0
chain   sweeps-r5.md        → RESOLVED_HOPS=2/3  CLEAN (hops=3 verified=2 exempt=1 anchor-missing=0 refused=0 invalid=0 findings=0 drift=0), exit 0
chain   sweeps-r5-broken.md → RESOLVED_HOPS=1/1  CLEAN (hops=1 verified=1 exempt=0 anchor-missing=0 refused=0 invalid=0 findings=0 drift=0), exit 0
```

`--selftest` at the same revision: `RESEARCH_GATE_SELFTEST: PASS (54 cases)`,
exit 0 (the 44 prior cases plus the 8 sweeps cases and 2 sweeps setup cases the
round added).

## Honest boundaries

- CLEAN from `verify-sweeps` proves the declared flip-condition is present and
  the named local path set re-measures empty. It does not prove the
  flip-condition is *good* (a placeholder string would pass), that a non-local
  sweep was ever really run, or that an empty sweep is the right sweep.
- The mode re-runs path-set EMPTINESS (glob existence), not a content grep:
  `sweeps-r5.md`'s W1 is phrased as a path-set absence because that is the
  class the mode can re-check. A content census such as the intake's W2 ("no
  URL locator exists in the archive set") is not re-run by the gate; the record
  keeps that census as a chain anchor, not as a re-check.
- W1's emptiness is a property of the pinned revision; the fixture pins the
  revision in this README, not in the record's bytes.
- Root sensitivity: the broken control's hit is a property of the pinned
  `--root ..` resolution — its `where` names the fleet-root-relative
  `chousa-shokunin/corpus/fixtures/sweeps-r5-hit.md`. Under a different root
  the same literal path names nothing and the row verifies vacuously (measured:
  `--root .` → `VERIFIED_SWEEPS=1/1`, DRIFT only from R1's missing flip); that
  is the same mode rule that lets a sweep naming a nonexistent literal path
  verify. The re-run command is pinned for this reason.
- The rejections are cited from the lane's own round-1 intake, not
  re-adjudicated here; the flip-conditions are this fixture's formulation of
  what the intake's reasons imply.
- No scalar score, no promotion, no field-readiness claim.

## Re-run

```bash
cd chousa-shokunin
bash tools/research-gate.sh verify-sweeps corpus/fixtures/sweeps-r5.md --root ..
bash tools/research-gate.sh verify-sweeps corpus/fixtures/sweeps-r5-broken.md --root ..
bash tools/research-gate.sh verify corpus/fixtures/sweeps-r5.md --root ..
bash tools/research-gate.sh verify corpus/fixtures/sweeps-r5-broken.md --root ..
bash tools/research-gate.sh --selftest
```