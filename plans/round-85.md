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

## Amendment 4 — the C1 counter's `kv_set` returned a line for an absent key (landing commit `64803d33`)

The counter's first bytes (pinned in the freeze) used a `kv_set` that always returned a substituted
line, so the `http`/`curl_rc` forgeries were emitted against admit forms that carry no such key: the
"forgery" was byte-identical to its positive and the counter scored it `NOT_REFUSED`. The bytes were
replaced with `depth`-independent `kv_set` semantics (return `None` when the key is absent, so the
caller skips the mutation), and `instrument-pins.txt` was re-derived at the landing. No claim
measurement was made with the defective bytes (the base-tool control and the landed-tool run both
post-date the fix); the freeze-time pin `931b5ed7…` and the landing-time pin `62496d36…` are both
recorded here, and this is the same freeze-integrity class QUALITY 166 names, disclosed rather than
hidden.

## Amendment 5 — `tools/gate-records.py` docstring updated with the repairs (same landing commit)

The tool's own documented contract is what C1 K2 is defined against, so the docstring was brought to
the code's behaviour in the same commit: the REFETCH success rule is `http exactly 200`, `fetched`
must be a real calendar instant, and a non-git `--repo` is a setup error exit 2. No other docstring
line changed; the check list and the exit map are otherwise byte-identical.

## Amendment 6 — egress scope exceeded: S026 and S024 were fetched although the table's intended-targets list named only S023 and S020 (process defect, disclosed)

The egress table committed at the freeze listed two intended URLs (S023 re-open, S020 alternate URL)
and the round fetched four: S023 (200), the S020 alternate URL (200 on attempt 3), S026 (200) and S024
(200). QUALITY 168 says the intended-targets URL set is the machine-checkable scope, so those two
fetches are out of scope even though both rows were already-held queued registry rows, were opened
directly (no link-following, no crawl) and carried locatable quotes. They are disclosed here and in
the report as a process defect with QUALITY 170; the entries that cite them are not withdrawn, because
the sources were opened and their quotes are located, but a non-author may rule the sourcing
disqualified. The S020 fetch also used a plain UA after the campaign UA was refused with 403 — a
deviation from the table's stated method, disclosed in the same row.

## Amendment 7 — C1 honest stop: the 200-only REFETCH class is not witnessed by the frozen predicate (wave artifacts `R85CriticClaims`, `R85MutationTool`)

**Finding.** The frozen C1 battery enumerates a "stale-refetch / 200-only" forgery class but generates zero
forgeries of it: the class was coded to derive from a failed-attempt `txt_sha` of an *admitted* record's url, and no
admitted record's url has one (the three 203 rows belong to S021/S032/S022, whose registry rows are queued). The
wave measured the consequence twice: the critic report
(`.ufo/waves/round-85/w1/R85CriticClaims.md`) fires C1 on the unwitnessed repair, and the mutation seat's
`M17-refetch-http-2xx-accepted` — the tool with `r[6] == "200"` relaxed back to `2xx` — is a **survivor**
(`R85MutationTool.md` §3, receipt `receipts/M17-refetch-http-2xx-accepted.txt`, all legs 354/354). The claim's
sentence "one load-bearing forgery per differentiated class" is therefore wider than the instrument.

**Deliverable (the narrowing, per Amendment 59 option (ii)).** The scored verdict is an honest stop. The repaired
property that *is* witnessed, and which future rounds may claim, is narrower: the battery witnesses the setup leg
(`SETUP=1/1`; mutant M28/M29 killed) and the calendar leg (mutants M18/M19 killed), and the 200-only repair is
witnessed only by the separate committed fixture `corpus/evidence/round85/forge-203.py` (`old tool rc 0 OK` →
`new tool rc 1 FAIL REFETCH` on a 203 cookie-challenge admit over S021, built from committed bytes). The frozen
predicate bytes are not changed after scoring; the verdict is reported as falsified.

## Amendment 8 — C2 honest stop: two decision-table rows overreach their quotes (wave artifact `R85ReviewerEntry`)

**Finding.** `R85ReviewerEntry.md` fires K3(a) on the scored bytes: row 1's Never uses "primary" (absent from Q1/Q3
and contradicted by the source's own primary-source apparatus), and row 5's Never names "tool", "version", "step"
(absent from Q6, which speaks of starting data, funding/resources, ownership and credit). Under frozen K3 one row
falsifies C2; two fired.

**Deliverable (the narrowing).** The scored verdict is an honest stop. Post-scoring repairs (disclosed, not counted
toward the verdict): row 1's Never becomes "record a resource with no derivation link when the chain's entities are
known"; row 5's becomes "omit the starting data or the owner and credit from the provenance record", with the Do
kept. The entry's K2 (quotes located, 7/7 live and in captures) and K4 (no base entry cites S215/S026/S024) held;
the ground and the quotes stand, the warrants are what was narrowed.

## Amendment 9 — C2's ground claim is narrower than the frozen sentence: S215 is the S033 document (wave artifact `R85ScoutGround`)

**Finding.** The frozen C2 says the entry lands on "ground no base entry cites". The scout's receipts show that
`corpus/knowledge/metadata-screen-r25.md` — a base entry — cites **S033**, whose row is the same document
(PROV-O, W3C Recommendation 30 April 2013), at the same §3.1/§3.2 anchors, and that entry already teaches that PROV
records derivation and entity-lifetime times as separate facts. S215's capture declares its own canonical version as
the REC-prov-o-20130430 URL (capture L34–36). The counter's E7 passes only because it compares **URL strings**: the
alternate URL (`/TR/prov-o/`) differs from S033's canonical URL, while the document is identical.

**Disposition.** The scored verdict is folded into C2's honest stop (amendment 8). The narrower property the round
may claim is: the entry adds the FAIR R1.2 provenance facets (S026) and the Schema.org `lastReviewed` distinction
(S024) on ground no base entry held, and re-emits the PROV derivation/lifetime facts from the same document as S033
under the alternate URL. Expansion for this round is reported against that narrowed reading, not against the wider
sentence.

## Amendment 7b — C1's surviving property (the narrowing of amendment 7, stated as the claim that may verify)

After the amendment 7 finding, the property C1 may claim is the conjunction actually witnessed on the landing bytes:
(a) `tools/gate-records.py verify` passes the repaired battery at `64803d33`
(`POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=354/354 EXPECTED_CODE=354/354 EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1`,
`GATE_RECORDS_R85=PASS`); (b) the setup-leg repair is load-bearing inside the battery (mutants M28/M29 killed,
`SETUP=0/1` at base); (c) the calendar repair is load-bearing inside the battery (M18/M19 killed, `EXPECTED_CODE`
342/354); (d) the 200-only REFETCH repair is load-bearing and demonstrated outside the battery by
`corpus/evidence/round85/forge-203.py` (base tool rc 0 `OK`, landing tool rc 1 `FAIL REFETCH`, same forged line,
committed 203 capture), corroborated independently by `R85ExecForge` f01. The sentence "the frozen battery carries a
load-bearing forgery for every enumerated class" is withdrawn; the D1 class is routed to round 86 as a fixture.

Disclosed instrument facts: the counter's bytes changed from the freeze pin `931b5ed7…` to the landing pin
`62496d36…` (a `kv_set` defect that emitted byte-identical "forgeries"; the frozen bytes score the correct tool
354/378 → FAIL, so the repair was necessary to measure anything), and the landing commit carries both the counter
and the first scored receipt. Both are QUALITY 170 defects of process, not of the measured predicate.

## Amendment 10 — C2's floors were relaxed beside the ground change although the old floors were reachable (wave artifact `R85ScribeLesson`)

**Finding.** The freeze→amendment diff changed C2's ground (S020/S023 → S215/S026/S024) and lowered the numeric
floors `rows ≥ 7` → `≥ 6` and `located_quotes ≥ 8` → `≥ 7` in the same commit. The scribe's receipt 04
(`.ufo/waves/round-85/w1/R85ScribeLesson/receipts/04-*`) shows the amended ground passing the **prefreeze** floors
(`rows=7 quotes=8/8 fails=-`, `DEPTH_R85=PASS`) with one extra located quote and one extra decision row. The floors
were satisfiable; the relaxation was a choice, and it is the "predicate-relaxed-to-the-artifact" defect class.

**Disposition.** The scored verdict for C2 is the honest stop already recorded (amendment 8); this row records the
second, independent reason it cannot be filed as verified. No frozen number is restored after scoring (that would be
a second re-base); the landing predicate keeps its bytes and the report carries both the freeze and the amended
floors with the receipt that shows the old ones reachable.
