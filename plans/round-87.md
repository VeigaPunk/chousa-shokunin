# chousa — round 87: plan and amendments

L1 `ChousaR87`. Base `6495ef88` (round-86 landing + the non-author spot-check at `6495ef88`, whose five routed
defects are this round's input). The frozen claims are in `corpus/evidence/round87/claims.json` (machine form) and
`corpus/evidence/round87/claims.md` (prose); this file records the pre-freeze repairs and any post-freeze amendment.
A `narrowing` cell in `.ufo/waves/round-87/claim-falsification.tsv` resolves to a section here.

## Inputs — the five defects round 86's non-author check routed

`corpus/lessons/round-86-verifier-spotcheck.md` `## Routed defects` (all five endorsed there, none re-routed):

1. **D1 is one record wide.** `build_d1_203_admit` returns the first qualifying 203 row it finds (`S021`), and the
   predicate requires `D1_REFUSED=1/1`. The critic's `T4` mutant — `r[6] == "200" if sid == "S021" else
   r[6].startswith("2")`, a general-2xx rule with a single record-keyed exception — prints the full frozen line and
   `PASS` (`.ufo/waves/round-86/w1/R86CriticClaims.md` §T4). The class the claim names is every 203 row; the class the
   instrument enforces is one row.
2. **The mutant-derivation and SETUP duties are printed fields, not verdict conjuncts.** `M2` (replace the whole
   mutant leg with `mut17 = 1`) and `M5` (drop `and setup_ok == 1` from `passed`) both print the frozen line and `PASS`
   (`.ufo/waves/round-86/w1/R86MutCounter.md` §C1).
3. **A `decision=reject` 203 record is accepted.** The `url/unreach` form's success test is
   `curl_rc == "0" and http == "200"`, so a record claiming a failed fetch while reporting `curl_rc=0 http=203` is
   accepted on every 203 row (`R86ExecForge` F1, candidates 3/6/8). A 203 is a *successful* response
   (S216: "the request was successful but the enclosed content has been modified"), so it cannot record a failed
   transfer.
4. **C2's `QUOTES_LOCATED` has no denominator floor and no warrant linkage.** `E5b` (delete the failing quote row) →
   `19/19 PASS`; `E5c2` (keep only `Q13` and `Q7`) → `2/2 PASS`; `E6` (re-point the r84 row-9 warrant at `Q10` while
   leaving `Q13` in place) → `MODIFIED_DEF_CITED=1 PASS` (`R86ReviewerEntry` §2.3/§2.4).
5. **A registry `teaches` cell is never read against its capture.** `S024`'s frozen `teaches` asserts a comparison to
   modification dates that its superseder's capture refuses (`S031` capture contains `modified`/`modification` 0 times),
   and no instrument in the lane reads registry `teaches` against captures at all (QUALITY 178).

## Claim selection

- **C1 — operability (the lowest scored non-retired axis, historical 3/10).** It closes routed defects 1–3 on the
  battery. Capability: the round-87 battery widens the 203 class to every qualifying committed row, adds the reject-form
  203 class, and accounts its verdict by counting executed legs so a dropped leg or a credited-but-unrun mutant changes
  the verdict instead of the printed fields only. The subject tool gains the unreach-form repair (a 2xx is not a failed
  transfer).
- **C2 — calibration.** It closes routed defects 4–5 on the curation instrument: an implemented per-entry quote floor, a
  warrant-linkage leg, and a registry-`teaches`-against-capture leg over every live (non-superseded) row. The axis is
  calibration because each leg is the lane's own check on whether its self-assessment of what is mined, warranted and
  located matches the bytes.
- Rejected as claims this round: a new knowledge entry (no candidate source was opened for one; the round's one new
  registry row is `own-work`, S218, which grounds C2's contract leg), and the twelve r80 backlog Gate ids (carried debt,
  no new instrument).

## Pre-freeze repairs (before the first scored run, disclosed)

1. **`build_d1_203_admits` returns every qualifying row, and the predicate pins the expected width.** The builder walks
   the committed `refetch.tsv` for every row with `curl_rc=0`, a non-200 status, a matching capture key and a capture
   whose sha equals the row's `txt_sha256` (3 at this base: `S021`, `S032`, `S022`), and `passed` requires
   `D1_FORGES == D1_EXPECTED` and `D1_REFUSED == D1_FORGES`. A counter that rebuilds the one-row class prints
   `D1_FORGES=1` and fails on the expected-width leg (this is the `T4` kill).
2. **The verdict is leg-accounted.** Every leg appends exactly one `(name, ok, detail)` record; `passed` is
   `all(ok) and len(legs) == EXPECTED_LEGS` with `EXPECTED_LEGS` a frozen constant. A leg whose body is deleted (the
   `M5` shape) or whose mutant is credited without a build (the `M2` shape) changes the leg count and fails, so the
   predicate cannot be met by a counter that stopped executing the duty.
3. **The mutant leg carries its own derivability probe.** `MUT17_DERIVED` is true only when `build_mutant` produced
   different bytes *and* the derived copy ran; a second probe feeds `build_mutant` a copy whose literal is rewritten
   (`r[6] == "2" + "00"`) and requires it to report "not derived", so the derivation duty is exercised both ways.
4. **The reject-form 203 class (D2) is built from the same committed rows** in the `url/unreach` shape
   (`decision=reject capture=none curl_rc=0 http=203`) and its expected code is `REFETCH`.
5. **`tools/gate-records.py` unreach branch: a 2xx status is not a failed transfer.** `success = curl_rc == "0" and
   http == "200"` becomes `curl_rc == "0" and 200 <= int(http) < 300`. Harm control: the only genuine committed unreach
   record in the tree is `corpus/lessons/round-81.md:28` (S208, `curl_rc=22 http=403`), and it still verifies OK
   (`controls/receipts/c1-harm-unreach.txt`); no committed record of either url form moves.
6. **`curation-r87.py` per-entry floors are the measured base counts** (r84 entry 13 located quotes, r85 entry 7), not a
   round-sum minimum: `E5c2` keeps 2 across both entries and fails both floors, where a round-sum floor of 2 would pass.
7. **The `teaches` leg skips superseded rows by contract, not by name.** A row whose id appears as the target of
   another row's `teaches` `supersedes S0NN —` prefix is not live (CORPUS rule 2 / QUALITY 178: the superseding row's
   `teaches` is the evidence), so the leg reads only live rows and requires 0 rows whose `teaches` names a
   date-property term their own capture does not contain. `S024` is therefore neither edited nor counted.

## Freeze

`corpus/evidence/round87/claims.md`, `claims.json`, both counters, the control batteries, their receipts, the egress
table and `instrument-pins.txt` are committed together as the freeze, before the landing commit and before any scored
run of the candidate bytes.

## Amendments after the freeze

None yet. An amendment is written here only when a wave artifact falsifies a claim's stated wording (addendum §8,
Amendment 59) and names the artifact plus the narrower property that may verify, or the honest stop.
