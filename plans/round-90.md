# chousa — round 90: plan and amendments

L1 `ChousaR90`. Base `f54a45ed197dd475af50d82e43a22df3d2e99782` (round-89 landing + its non-author spot-check).
Frozen claims: `corpus/evidence/round90/claims.md` (prose) and `.ufo/waves/round-90/claims.json` (machine form the
pre-file gate reads). A `narrowing` cell in `.ufo/waves/round-90/claim-falsification.tsv` resolves to a section here.

## Inputs — round 89's routed defects and the Gate-standard item

`corpus/lessons/round-89-verifier-spotcheck.md`:

1. C2's after-line quotes an unprinted token (`VERDICT fields_hold=1`) → C2 here appends the verdict leg before the
   summary and requires the whole line.
2. Attack-share arithmetic (7/12 vs 6/12) → conformance; this round states the ledger's count.
3. Work-performed frontier bullet undercount → conformance; this round states the counts it measured.
4. Amendment 8's `LEGS_MEASURED=8/9` vs printed `8/8` → conformance; the r90 summary prints the full leg set.
5. `SKILL.md` tallies at 275 vs the tool's 283 → C3.
6. Carried debt: (a) round-74 source-blind order oracle — **not touched** (a different instrument); (b) QUALITY 173's
   successful-refused record form — **not touched**; (c) r80 backlog Gate ids — **not touched**; (d) Amendment 7's
   control-driver discipline — C1; (e) Amendment 9's detector-substitution witness — C2.
7. Named limits stay named in the frozen claims (C1 limits 1–3, C2 limits 1–4, C3 limit 1).

Cross-checked against `considerthese/2026-11-07.md` proposal 1 (the "duplicate wins" watch): the receipt driver's
`DUPLICATE_KEY` leg is that proposal applied to the receipt surface, and the `C-duplicate-key` forgery is its
witness. No other proposal is acted on.

## Claim selection

- **C1 — operability (lowest scored non-retired axis, historical 3/10).** The control-receipt driver's four
  spot-checked defects (B1–B4) plus the duplicate-key class. The subject `tools/gate-records.py` is unchanged, so no
  domain record can move; the driver verifies receipts that already exist at the base.
- **C2 — calibration.** The curation counter's verdict leg is printed on the passing path, and each detector gains a
  two-directional witness that kills the two constant-substituted detectors round 89 left alive.
- **C3 — freshness.** The `SKILL.md` self-test tallies re-derive to the tool's own selftest verdict.

Rejected as claims: a new knowledge entry (the one source opened this round grounds C1's token rule, not a domain
fact); the round-74 order oracle and the r80 Gate-id backlog (carried debt, no instrument in this round touches
them); the `S217` successful-refused record form (QUALITY 173; carried).

## Pre-freeze repairs (before the first scored run, disclosed)

1. **C1 driver emits, then verifies.** `emit` writes the receipt with a four-line header; `verify` never writes under
   the receipts directory (B1). The token leg is exact-token, with `TOKEN_DETACHED` for a key carried with a
   different value (B2). `# computed_against=` is required and checked against `--rev`, and the driver/expectation
   bytes are self-pinned at that revision while the receipts are self-pinned at their carrier commit (B3). The harm
   row requires `records>=1` and a setup negative (`exit 2`) exists (B4).
2. **C2 verdict leg order.** The `VERDICT` leg is computed and appended before the summary; `LEGS_MEASURED` counts
   the same ten legs the verdict was taken over; the passing path prints `VERDICT fields_hold=1` (Amendment 8).
3. **C2 detector functions.** `locates`, `unentailed_row`, `teaches_miss`, `dup_qid` are named functions called by
   the legs and by `witness()`, which asserts each fires and stays silent (eight assertions). The witness is part of
   `fields_hold`, so a substituted detector refuses PASS (Amendment 9).
4. **C2 controls frame.** The seven tree-forgery classes were closed by round 89, so the frame is now regression
   (both counters must refuse) and the new detection credit is the mutant battery's prior-survivor leg.
5. **C3 check runs the tool.** The tally check runs `--selftest` itself; the expected number is never a literal in the
   check.
6. **Registry id.** The new row is `S220`, not `S219`: `S219` is the round-89 control fixture's mirror-row id, and a
   real row there renames the fixture's row inside the parsed registry (measured: the r89 control battery's SUP case
   stops being accepted by r88). `S219` stays reserved to the fixture; the failed gnu.org attempt is logged under
   `S219` in `refetch.tsv` and is not a registry row.

## Freeze

`corpus/evidence/round90/claims.md`, `.ufo/waves/round-90/claims.json`, the five instruments
(`control-driver-r90.py`, `control-forgeries-r90.py`, `harm-recheck-r90.py`, `curation-r90.py`,
`curation-r90-controls.py`, `curation-r90-mutants.py`, `skill-tally-r90.py`), `controls/expected.tsv`, the before
receipts under `controls/receipts/`, `instrument-pins.txt`, the egress table and the registry change (S220 row) are
committed as the freeze, before any scored run of the round-90 candidates and before the wave.

## Amendments after the freeze

None yet. An amendment is written here only when a wave artifact falsifies a claim's stated wording (addendum §8,
Amendment 59) and names the artifact plus the narrower property that may verify, or the honest stop.
