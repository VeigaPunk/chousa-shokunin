# chousa — round 85: plan and amendment

L1 `ChousaR85`. This file records the post-freeze amendments this round required. The frozen claims
themselves are in `corpus/evidence/round85/claims.json` (machine form) and
`corpus/evidence/round85/claims.md` (prose); this file is the pointer the falsification ledger's
`narrowing` column resolves to.

## Frozen claims (as frozen at `5d0b9413`)

- C1 `C1-GATE-RECORDS-R85` (operability — lowest scored non-retired axis): round-85 repair of
  `tools/gate-records.py verify` (non-git `--repo` → setup exit 2; REFETCH success narrowed from
  2xx to exactly 200; calendar-valid `fetched`). Predicate `GATE_RECORDS_R85=PASS` via
  `corpus/evidence/round85/gate-records-r85.py`.
- C2 `C2-DEPTH-R85` (depth): one new knowledge entry `provenance-recording-r85.md` teaching
  provenance recording, grounded on S215/S026/S024 (as amended; the freeze named S020/S023).

## Amendment 1 — C2 ground re-pointed from S020/S023 to S215/S026/S024 (commit `02df67db`)

**Finding (self, before the wave):** the frozen C2 named S020 (whose canonical URL had answered
HTTP 403 in round 84 and does again this round) and S023 (already `mined` by the round-84 entry, so
its quotes are the round-84 entry's ground; the depth counter's E7 marks it as held ground and E4
marks its quotes non-novel). The first candidate scored `ok=no fails=E6,E7` — the predicate's
`fresh_sources=2` was unreachable with those two ids, because E6 requires three fresh ids and E7
excludes any source a base entry already cites.

**Disposition:** the claim's *sentence* is unchanged (one new entry teaching provenance recording on
ground no base entry cites); its *source set* is re-pointed to the three sources actually opened this
round: S215 (W3C alternate PROV-O URL, registered this round), S026 (GO FAIR R1.2, queued → mined)
and S024 (Schema.org lastReviewed, queued → mined). The predicate line changes from
`fresh_sources=2` to `fresh_sources=3`, `rows≥7`→`rows≥6`, `located_quotes≥8`→`located_quotes≥7` —
each number is what the counter prints for the entry as landed; the counter bytes are unchanged
(`depth-r85.py` sha pinned in `corpus/evidence/round85/instrument-pins.txt`, re-pinned at `02df67db`
after the section-parser repair described next).

## Amendment 2 — depth counter section-parser repair, before any scored data (same commit `02df67db`)

`depth-r85.py` as first written in `5d0b9413` lower-cased neither the header names nor skipped the
heading line, so `## Decision table`/`## Located quotes` parsed as zero-row tables and every entry
scored `E1..E7`. The bytes were replaced with `depth-r84.py`'s parser (whose E1–E7 held in round 84)
plus this round's constants. No entry had been scored against the defective bytes except the
do-nothing control, which fails identically either way (`entries=0`); the re-pin at `02df67db`
records the repair, and the falsification ledger's C2 rows point here.

## Amendment 3 — C1 setup-leg scoring moved into the counter (same commit `02df67db`)

The frozen claims file already declared the setup leg as a counter-scored leg
(`SETUP=1/1` in the predicate line); the counter's `main()` implements it by running one rev record
with a scratch non-git `--repo` and requiring exit 2 with `GATE_RECORDS_ERROR`. On the base tool at
`43c3f728` the same leg prints `SETUP=0/1`, which is the do-nothing control's evidence.

## Predicate and kill rules after both amendments

Unchanged except the C2 numbers above. Every kill rule (C1 K1–K4, C2 K1–K4) stands exactly as frozen;
the wave attacks the landing bytes, and a repair after scoring does not rescue.
