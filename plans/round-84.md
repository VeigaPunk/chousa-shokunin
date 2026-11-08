# chousa — round 84: plan and amendment

L1 `ChousaR84`. This file records the post-freeze amendments and honest-stop dispositions this
round required. The frozen claims themselves are in `.ufo/waves/round-84/claims.json` (machine
form) and `corpus/evidence/round84/claims.md` (prose); this file is the pointer the
falsification ledger's `narrowing` column resolves to.

## Frozen claims (as frozen at `3b616420`)

- C1 `C1-GATE-RECORDS-R84` (operability — lowest scored non-retired axis): successor battery
  for repaired `tools/gate-records.py verify` (post-scoring repair `c7d29e1c`). Predicate
  `GATE_RECORDS_R84=PASS` via `corpus/evidence/round84/gate-records-r84.py`.
- C2 `C2-DEPTH-R84` (depth): one new knowledge entry
  `search-transparency-reporting-r84.md` teaching PRISMA 2020 search-reporting requirements,
  grounded on S214/S018/S023. Predicate `DEPTH_R84=PASS` via
  `corpus/evidence/round84/depth-r84.py`.

## Amendment 1 — post-freeze rewrite of `claims.md` (commit `3a17f4da`)

**Finding:** `R84SentinelScope.md` Finding 1 — `corpus/evidence/round84/claims.md` and every
control receipt under `controls/receipts/` were rewritten inside the fetch commit `3a17f4da`,
after freeze `3b616420`. Freeze-time sha `f6f032a6…` vs landing-time `19d68274…`. The counters
(`depth-r84.py`, `gate-records-r84.py`) were byte-identical, so the measured predicates did not
move — but the *rulebook* the wave attacked was not the one frozen: fresh positives 6→5,
`RC=3/3`→`4/4`, C2 sources S017→S214/S018/S023, `c2-k0-donothing` semantics moved from
"tool absent" to "pre-repair tool `81b81173`".

**Disposition:** recorded as a process defect (QUALITY 166), not a scoring rescue. The
amendment made the frozen text match what was actually measured; it did not change any
predicate or counter. Both claims are filed on their **post-amendment wording**, which is the
wording the wave seats read and attacked.

## Amendment 2 — honest-stop dispositions (no rescues)

Per PROTOCOL and claims.md kill rules ("Repairs after scoring do not rescue"), both claims
stand falsified by their own kill rules at the scored landing `03bbb458`:

- **C1 falsified (K2 setup leg + mutation thinness).** The frozen K2 setup leg requires a
  non-git `--repo` to print `GATE_RECORDS_ERROR` on stderr with exit 2; the tool prints
  `FAIL LINE,REV` with exit 1. Fired independently by `R84ExecRepro`, `R84ExecForge`,
  `R84CriticClaims`, `R84ReviewerTool`, `R84SentinelScope`, `R84ScribeLesson`. The
  mutation-tester additionally showed the counter PASSes 11/34 single-point mutants of
  `tools/gate-records.py`, six of which accept real forgeries the pristine tool refuses —
  including the claims' own enumerated class-1 items `stale-refetch txt_sha256 drift` and
  `short-rev` — and seven of eight enumerated r83 classes have no forgery of their own in the
  288 (`R84MutationTool.md`). The predicate `GATE_RECORDS_R84=PASS` itself held at landing and
  at HEAD `5e66c854`; the kill rule fired on the contract wording, not the counter output.
- **C2 falsified (K3 warrant, row 9).** Decision-table row 9's Do/Never do not follow from Q10
  alone; the needed `modified` Definition is unique at S023 capture ~L8786 and was never
  quoted (`R84ReviewerEntry.md`; corroborated by `R84ConnectorSiblings.md` occurrence counts).
  K2 held (all 12 quotes located in captures and on three HTTP-200 re-opens, byte-identical);
  K4 held (no base entry cites S214/S018/S023).

**Narrowing recorded for the ledger:** for every `falsifies-wording` row the narrowing is this
file — the amendment log. The claims are not narrowed further; they are filed falsified
(honest stop), matching the r82/r83 precedent where post-scoring repairs land with receipts but
do not rescue.
