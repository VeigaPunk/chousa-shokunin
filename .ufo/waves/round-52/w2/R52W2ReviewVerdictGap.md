# R52W2ReviewVerdictGap — attack on `corpus/evidence/round52/verdict-gap.py`

Attacked: the considerthese pick (`verdict-gap.py`, round 52), i.e. the lane-vs-verifier
axis-grade comparison. Ran both mandated invocations, hand-confirmed every printed gap and
every UNPARSED/MISSING round against the SCORECARD `## Round N verdict` axis table and the
round's `round-N-verifier-spotcheck.md` axis table, and probed `dirn` on the two quoted
phrases. No installs; no files written outside this report; scratch removed.

## Commands run (observed output)

```
$ python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round52/verdict-gap.py --from 40 --to 51
R40 MISSING scorecard=False verifier=True
R41 MISSING scorecard=False verifier=True
R42 axes lane=6 verifier=6
R43 UNPARSED lane_axes=6 verifier_axes=0
R44 axes lane=6 verifier=6
R45 UNPARSED lane_axes=6 verifier_axes=0
R46 axes lane=6 verifier=6
R47 operability: lane=improved verifier=harmed
R47 axes lane=6 verifier=6
R48 UNPARSED lane_axes=6 verifier_axes=0
R49 axes lane=6 verifier=6
R50 calibration: lane=improved verifier=unchanged
R50 axes lane=6 verifier=6
R51 axes lane=6 verifier=6
VERDICT_GAPS=2 UNPARSED=5
exit=1

$ python3 …/verdict-gap.py --from 46 --to 51
R46 axes lane=6 verifier=6
R47 operability: lane=improved verifier=harmed
R47 axes lane=6 verifier=6
R48 UNPARSED lane_axes=6 verifier_axes=0
R49 axes lane=6 verifier=6
R50 calibration: lane=improved verifier=unchanged
R50 axes lane=6 verifier=6
R51 axes lane=6 verifier=6
VERDICT_GAPS=2 UNPARSED=1
exit=1
```

`dirn` probe (reproduced from `verdict-gap.py:24-27`):

```
'improved narrowly, disputed as a trade' -> improved
'not harmed' -> harmed
'unchanged — the axis is not harmed' -> unchanged
```

## 1. The two printed gaps are REAL (hand-confirmed)

- **R47 operability** — lane `SCORECARD.md:2513` `| operability | **improved, disputed as a trade** |`
  vs verifier `round-47-verifier-spotcheck.md:35` `| operability | **harmed** (trade; C1 — capability
  real, precision cost measured 2–3/12 false refusals, 8/12 misses, 5/7 mutants survive) |`.
  The verifier's independent ruling is explicitly `harmed` (its C1 ruling: "the axis move does
  not"); the lane's chosen verdict word is `improved` (dispute recorded in-cell). The parser's
  read — improved vs harmed — is faithful to both texts. Real disagreement.
- **R50 calibration** — lane `SCORECARD.md:2607` `| calibration | **improved narrowly** |` vs
  verifier `round-50-verifier-spotcheck.md:59` `| calibration | unchanged | … the registry row's
  revision gap (defect c) keeps it from a verdict beyond unchanged`. Real disagreement.
- All other parsed rounds (R42/44/46/47/49/50/51): lane and verifier axis rows agree direction
  for all six axes (hand-read both tables; e.g. R47 verifier lines 35–40 vs scorecard 2513–2518).
  No spurious gap.

## 2. UNPARSED/MISSING rounds — hand-confirmed; one hides a THIRD real gap

- **R40/R41 MISSING**: SCORECARD has no `## Round 40/41 verdict` heading at all (grep shows only
  `## Round 40 — measured claims`, `## Round 41 — measured claims`, `## Round 40 — routed wave
  findings`). Honest. But both verifier files DO carry parseable axis tables
  (`round-40-verifier-spotcheck.md:53-60`, `round-41-verifier-spotcheck.md:45-52`); comparison is
  impossible only because the scorecard predates the verdict-section convention. A parser future-proof
  enough to look for `## Round N` + axis table near the end of the section would compare them.
- **R43 UNPARSED — missed verifier form, and it hides a real gap.** `round-43-verifier-spotcheck.md`
  has no axis table; the axis verdicts are bullets under `### Other owned axes`:
  `round-43-verifier-spotcheck.md:112` `- **coverage: improved.**`, `:113` `- **freshness: unchanged.**`
  (explicit: "The lane's scorecard says improved narrowly … Routed below so the next scorecard does
  not repeat the inflation"), `:114` `- **adjacency: unchanged.**`. The script's docstring documents
  this only for round 48 ("round 48 writes its axes as bullets") — round 43 uses the same non-table
  form and is silently dropped. Demonstrated: a bullet-aware variant of `table()` extracts
  `{coverage: improved, freshness: unchanged, adjacency: unchanged}` from the R43 verifier, while the
  lane table (SCORECARD.md:2369-2374) says `freshness: improved`. **So R43 freshness is a third real
  gap that `VERDICT_GAPS=2` cannot see.** This is the strongest finding: the script's gap count
  under-reports by ≥1.
- **R45 UNPARSED — justified**: `round-45-verifier-spotcheck.md:27` gives no independent axis
  verdicts; it restates the scorecard's ("Axis verdicts from the round's SCORECARD: …"). Nothing to
  compare; `verifier_axes=0` is correct.
- **R48 UNPARSED — justified**: `round-48-verifier-spotcheck.md` contains no axis rows at all (its
  only direction bullets are expansion/quality/discernment trends). Matches the docstring's stated
  behavior. Not counted as agreement, as documented.

## 3. `dirn` semantics

- `'improved narrowly, disputed as a trade'` → `improved`: correct and faithful — the lane's verdict
  word is improved; the dispute is a qualifier.
- `'not harmed'` → `harmed`: negation-blind. **Latent, not currently live**: in every axis cell of
  rounds 40–51 the phrase only appears after a direction word or in the evidence column
  (e.g. `SCORECARD.md:2399`, `round-44-verifier-spotcheck.md:127`, `round-43-verifier-spotcheck.md:113`),
  so no cell is misread today. Any future cell whose verdict is literally "not harmed" would be
  inverted into a false gap.

## 4. Wrong-table reads: none in the current data; two latent hazards

- The hazard class named in the seat spec (claims table before the axis table; a `| depth |
  **improved** |` row inside prose) does not materialize for rounds 40–51: all claims-table first
  cells begin with `C1/C2/C3 …` and so fail the `^\|\s*(axis)\s*\|` anchor, and no prose/fenced
  axis-shaped row sits before a real axis table in either source.
- Latent hazards to record: (a) `table()` is first-wins (`setdefault`), so any future quoted/claims
  row shaped exactly `| <axis> | … |` placed before the real table would silently poison the parse;
  (b) the scorecard scan window ends at the next `## ` heading, so `## Capabilities` subsections are
  scanned (harmless today — capability rows don't match); (c) bold-axis rows (`| **depth** |`) would
  be invisible — none exist in the current files.

## Residual risk / verification gaps

- R40/R41 comparison is structurally impossible until the scorecard gains verdict sections; I did not
  invent one.
- I did not modify the script or any lane file (read-only), so nothing here verifies a proposed fix;
  a bullet-form extension would surface the R43 gap.

VERDICT: attacked `verdict-gap.py` — both printed gaps (R47 operability, R50 calibration) are real, and the script also misses a third real gap (R43 freshness) behind its undocumented bullet-form blindness; `dirn` misreads 'not harmed' but no live cell triggers it.
