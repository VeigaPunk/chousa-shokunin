## Round 99 — 2026-11-09

Lane `chousa`, round 99 (attempt 1, L1 `ChousaR99`). Base `47ed34fa`; F `d41f4cd8`; carrier `f8f480ff`. Claims
`.ufo/waves/round-99/claims.md` (judged at the F sentences and predicates). One v1 wave, 12 seats (executor 2,
mutation-tester 2, reviewer 2, critic 1, sentinel 1, scout 1, revenger 1, connector 1, scribe 1).

- Motivating evidence C1: round-98 spot-check routed defect 3 — `tools/gate-records.py` admits a quote from an http-200
  challenge page (`corpus/evidence/round98/gate-records-challenge-200.txt`); round 99's own S234 answered http 200 with a
  "Client Challenge" page that QUALITY 229's four-word grep does not match. After: the gate refuses a challenge capture
  with code CHALLENGE (11 markers, 200-word bound) on url/admit and on rev records whose path is
  `corpus/captures/<key>.txt`; battery `corpus/evidence/round99/challenge-controls-r99.py` →
  `NEG_REFUSED=7/7 POS_ADMITTED=4/4 PROD_REFUSED=4/4 HARM_SAME=25/25 BASE_NEG_ADMITTED=7/7 ORACLES_REJECTED=5/5`,
  `CHALLENGE_CONTROLS_R99=PASS` (`corpus/evidence/round99/after/c1-all.txt`); base tool `NEG_REFUSED=0/7 … CHALLENGE_CONTROLS_R99=FAIL`
  (`corpus/evidence/round99/before/c1-base.txt`).
- Motivating evidence C2: SCORECARD's province ground — no entry held the measured rate of quotation errors (a cited
  source that does not support the citing sentence). Routes: PeerJ 1364 (http 403, 2026-11-09T04:00:32Z, S232 rejected),
  PLoS One e0184727 (http 200, 04:00:33Z, S233 admitted), Research Integrity and Peer Review s41073-025-00173-z (http 200
  "Client Challenge" page, 04:00:33Z, S234 rejected), Europe PMC full text PMC4627914 (http 500, 04:00:42Z, S235
  rejected), Europe PMC core record PMID 26528420 (http 200, 04:01:07Z, S236 admitted). After:
  `corpus/knowledge/quotation-error-rates-r99.md`, `GATE_RECORDS files=1 records=25 ok=25 fail=0`,
  `METADATA_COMPLETE=1/1`, `RESEARCH_GATE: CLEAN`, `rev_match=4/4`, `SEARCH_RERUN: CLEAN`, `ENTRY_CONTROLS_R99=PASS`
  (`QUOTES=23/23 FIELD=9/9 IDENTITY=2/2 WARRANTS=8/8 NUMBERS=6/6 TOPIC=1/1 NUMBERS_SOURCED=6/6 BASE_TOPIC_HITS=0
  BASE_ENTRY=absent FORGERY_REFUSED=10/10 ACCEPTED=2/2`).
- Correction (plan, A5, `R98RevenPrior`): "19 mutants no lane instrument catches" is R98MutantsC1's count; at BASE the
  round-97 battery, run with `--tool`, fails on g01, g03 and g04. The C1 sentence speaks of the self-test.
- Correction (C1 named limit (e), A6, `R98SentinelC1` F1-F2): the NO_WRITE leg does not observe writes outside its
  empty directory; the self-test's git children open `/dev/null` O_RDWR and read the global git config.
- Correction (approval table, `R98ScribeLesson` F2): its first sentence said the whole table preceded every GET;
  three rows were appended between GETs, each before its own GET. Corrected at F2 with the reason in the file.
- Correction (S231 tier, B5): A → B before landing (carrier rule; kotodama grades the same shape B).
- Found (C2 controls, `R99ScribeLesson`): the entry's NUMBERS leg tests each Do-cell number as a *substring* of its
  warrant's text, so a number that is not printed in the warrant passes — `64.8%` → `8%` and `25.4%` → `5.4%` are both
  accepted (`NUMBERS=6/6`, `ENTRY_CONTROLS_R99=PASS`), while `63.8%` is refused (`NUMBERS=5/6`, exit 1). The entry's own
  numbers are correct (all 23 quotes located in their captures; all Do-cell numbers printed in their warrants), so this
  is a control gap, not a wrong entry: the forgeries that pass do so because the leg cannot tell a printed number from
  a suffix of one.
- Found (round-98 receipt, `R99ScribeLesson`): `corpus/evidence/round98/gate-records-challenge-200.txt` records the base
  tool's `S230 OK` for a record quoting S230's reCAPTCHA page; under F that same file now prints `S230 FAIL CHALLENGE`
  (exit 1). The receipt is a historical record of the base tool, but a reader who re-runs it now gets a different verdict
  than the receipt records.
- Routed: QUALITY 126/229's lexical floor to QUALITY 230 (the round's own criterion, `corpus/QUALITY.md`); the C2
  NUMBERS-leg substring hole to the next round's controls; `R98MutantsC1` G01-G03/D05 and `R98ScribeLesson` F1
  (checker-of-the-checker survivors) to SCORECARD planned r100.
- Census: start exit 0, end exit 0 (rows 230 → 235). QUALITY 230 added; mistakes mined: 2 (`corpus/lessons/round-99.md`).
