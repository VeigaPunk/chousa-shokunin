# chousa — round 89: plan and amendments

L1 `ChousaR89`. Base `f8fa55ec` (round-88 landing + the non-author spot-check `corpus/lessons/round-88-verifier-spotcheck.md`). The frozen claims are in `corpus/evidence/round89/claims.md` (prose) and `.ufo/waves/round-89/claims.json` (machine form the pre-file gate reads — round 88 filed no `claims.json` and its gate run ended `SETUP findings=1`). A `narrowing` cell in `.ufo/waves/round-89/claim-falsification.tsv` resolves to a section here.

## Inputs — the round-88 spot-check's routed defects

`corpus/lessons/round-88-verifier-spotcheck.md` `## Routed defects` 1–8:

1. **Prefile ledger layout.** The prefile checker reads `.ufo/waves/round-<N>/claims.json`; round 88 filed only `corpus/evidence/round88/claims.md`. Fixed by writing both forms this round.
2. **Per-format reconciliation (C1).** The `RECONCILED` conjunct searched only `detail=(\d+)/(\d+)`, so a detached `ok` on `TOOL`, on the two width legs (`3/3/1 pin3` read as `3/3`) and on the two mutant legs (`derived=0 killed=0`) survived with `PASS` (`R88ReviewerC1` E4 receipts, `R88CriticClaims` `e7b`/`e7c`/`combined`). Fixed: `rederive()` per grammar.
3. **Verdict-vs-field reconciliation (C2).** `curation-r88.py`'s verdict was `all(ok)` over the legs, never reconciled with its printed fields, so a dead detector printed `TEACHES_FLAGGED=0 … PASS` (`R88CriticClaims` `c2-dead-teaches.log`) and a detached leg printed `TEACHES_UNRESOLVED=1 … PASS`. Fixed: `fields_hold` computed from the printed tallies, plus the `VERDICT` leg.
4. **Dead superseder-own-read clause (C2).** `curation-r88.py:250` matched a case-sensitive `supersedes (S\d{3,}) —` against a lowercased cell — 10 raw matches, 0 lowercased over 218 rows (`R88ScoutRegistry` `receipt-supclause-dead.txt`). Fixed: the raw cell is matched; non-vacuity is the battery's `SUP-clause-mirror`, because no real superseding row names a date term.
5. **Control-receipt discipline.** `expected.tsv`'s `c1-do-nothing` row expected exit 1 while its own receipt printed PASS, and `c2-d0-donothing.txt` had no expectation row (`R88SentinelScope` F7/F7b). Fixed by `controls/run-controls.sh`, which runs each control and refuses to pass unless the receipt's exit code **and** every `required_fields` token agree with the `expected.tsv` row.
6. **Duplicate-qid / swapped-quote forgeries (C2).** Five in-class forgeries passed the round-88 counter green; two are closed here — the duplicate-qid cite (`DUPQID`) and the superseder clause. The quote-content swap and the ≥7-token verbatim substitution are **named limits** in the claim, not silently kept: a content oracle would need a second copy of the entry, and the floor is a measured minimum.
7. **Seat discipline.** `R88ExecForge` shipped no `VERDICT:` trailer. The wave context requires the trailer; the scribe tallies an untrailered seat as a finding, not as a hold.
8. **Operator-owned prompt corruption.** Not the lane's to fix; carried.

## Claim selection

- **C1 — operability (the lowest scored non-retired axis, historical 3/10).** The successor battery closes routed defects 2 and 5, and adds the summary cross-check that makes a printed field and its leg agree. The subject tool is unchanged (`tools/gate-records.py` sha256 `905f9da2…` at base and landing), so no domain record can move; the harm sweep is the check.
- **C2 — calibration.** The successor curation counter closes routed defects 3 and 4 and half of 6.

Rejected as claims this round: a new knowledge entry (no candidate source was opened for one; the round is instrument repair plus the frontier step); the r80 backlog Gate ids and the `S217` successful-refused record form (carried debt, QUALITY 173, no new instrument this round); the round-74 routed "source-blind order oracle" debt (a different instrument, not touched by this round — named in the report as carried, never silently repaired backwards).

## Pre-freeze repairs (before the first scored run, disclosed)

1. **`rederive()` is per-format.** Four grammars, each re-derived from its own receipt text; the fallback `got_ok and ok` (a tautology) is gone.
2. **`CROSSCHECK` compares the printed summary to each leg.** `DIV3` is now printed so the third width derivation is checkable from the summary; `D1_EXPECTED`/`D1_FORGES`/`D2_FORGES`, the mutant `derived`/`killed` fields and every `n/m` field are compared to their leg's re-derived numbers.
3. **`SUMMARY` is a leg.** It is appended, receipted, re-read and reconciled like the rest (`EXPECTED_LEGS` 15 → 16), so a removed receipt changes the verdict.
4. **Mutants carry multi-point edits.** Round 88's survivor shapes need a broken measurement *plus* the detachment that hides it; a single-point healthy-tree mutant proves nothing (its `A3`/`E4` variant). `mutate-r89.py` applies a list of edits per mutant.
5. **C2's verdict is `fields_hold`, not `all(ok)`.** `fields_hold` is computed from the same values the summary prints; the `VERDICT` leg refuses a divergence between the two in either direction.
6. **C2's superseder clause matches the raw cell** and reports `SUP_CLAUSE_CHECKED` so its vacuity on the real registry is visible rather than implied.
7. **The control driver checks receipts against expectations** (routed defect 5) instead of filing receipts beside an unread `expected.tsv`.

## Freeze

`corpus/evidence/round89/claims.md`, `.ufo/waves/round-89/claims.json`, the six instruments, `controls/expected.tsv`, `controls/run-controls.sh`, the eight pre-freeze receipts under `controls/receipts/`, `instrument-pins.txt` and the registry `used-by` updates (S216, S218) are committed together as the freeze, before the landing commit and before any scored run of the round-89 candidates.

## Amendments after the freeze

None yet. An amendment is written here only when a wave artifact falsifies a claim's stated wording (addendum §8, Amendment 59) and names the artifact plus the narrower property that may verify, or the honest stop.
