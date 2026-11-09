# Round 98 — the search re-run self-test checks its own guard, and PRESS 2015 is held through its statement's own abstract (2026-11-09)

Base `98b8177c1e8b39cdf1167928e4f5d609f6fa81b6` (round-97 landing plus its non-author spot-check). Freeze F
`aac826848dda5029ba459568b29d9a92176dc2b6`. Frozen claims: `.ufo/waves/round-98/claims.md` / `claims.json`. Two
claims: C1 operability (`tools/search-rerun.py --selftest` with a guard canary and cases r17-r34, scored against the
37 mutants round-97 seat `R97MutantsC1` wrote) and C2 depth (`corpus/knowledge/press-2015-statement-questions-r98.md`,
sourced on S231, opened this round, and S225). Approval table for the round's GETs: `corpus/evidence/round98/egress-approval.md` — its first rows were written before
the first GET and three rows were appended between GETs, each before its own GET (wording corrected at F2).

## Gate

Registry: four rows added — `S228` (CADTH report 477 appendices, `rejected`, http 403), `S229` (PubMed record of
PMID 27005575, `rejected`, http 203 cookie-challenge page), `S230` (NCBI Bookshelf NBK98350, `rejected`, http 200
whose body is a reCAPTCHA page) and `S231` (Europe PMC's core record of PMID 27005575, tier B (amended from A at F2, B5),
`mined`). One existing row changed: `S225` `used-by` old→new
`corpus/knowledge/press-checklist-questions-r97.md` → `corpus/knowledge/press-checklist-questions-r97.md,
corpus/knowledge/press-2015-statement-questions-r98.md`; its `status` (`mined`) and `recheck` (`on-release`)
unchanged. Census exit 0 before (`corpus/evidence/round98/census-start.txt`) and after
(`corpus/evidence/round98/census-end.txt`).

Web search (one query, the session's search tool, 2026-11-09): `PRESS Peer Review of Electronic Search Strategies
2015 Guideline Explanation and Elaboration ncbi bookshelf OR europepmc full text`. It returned the CADTH E&E PDF
and landing page (both on the host that answered 403 to S227 and S228), the PubMed record, NCBI Bookshelf NBK98350
and the core.ac.uk copy (403 in round 97); it named no Europe PMC full text. The Europe PMC REST route was the
lane's own choice after both NCBI routes returned challenge pages (round 95 used the same API for PMC7839230).

- **S228 rejected (unreachable, not fabrication).** URL
  `https://www.cda-amc.ca/sites/default/files/PRESS_Peer_Review_Electronic_Search_Strate/Report%20477_PRESS_Peer%20Review%20of%20Electronic%20Search%20Strategies_Appendices.pdf`,
  attempted `2026-11-09T02:47:35Z`, curl rc 22, http 403; no bytes. Flip: a 200 from the agency host or a readable
  archived copy.

GATE-RECORD S228 url=https://www.cda-amc.ca/sites/default/files/PRESS_Peer_Review_Electronic_Search_Strate/Report%20477_PRESS_Peer%20Review%20of%20Electronic%20Search%20Strategies_Appendices.pdf fetched=2026-11-09T02:47:35Z tier=A decision=reject capture=none curl_rc=22 http=403 words=0 quote=none

- **S229 rejected (route).** URL `https://pubmed.ncbi.nlm.nih.gov/27005575/`, attempted `2026-11-09T02:48:10Z`,
  curl rc 0, http 203; the body (capture key `0954149536aaad411000e1fb`) is "Cookies must be enabled". No
  `GATE-RECORD`: `tools/gate-records.py` accepts the unreachable form only for a non-success status, and 203 is
  inside capture-fetch's 200-299 store range. Flip: a 200 carrying the record's abstract.
- **S230 rejected (route).** URL `https://www.ncbi.nlm.nih.gov/books/NBK98350/`, attempted `2026-11-09T02:48:10Z`,
  curl rc 0, http **200**; the body (capture key `b5b8d050eea0c638e95ba674`) is a reCAPTCHA page: "Checking your
  browser before accessing www.ncbi.nlm.nih.gov ...". No `GATE-RECORD` (see `## Mistakes` 2). The document's
  identity as an AHRQ report comes from a search result only and was not confirmed from its own bytes. Flip: a 200
  carrying the report's text.
- **S231 admitted (tier B).** URL
  `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:27005575%20AND%20SRC:MED&resultType=core&format=json`,
  accessed 2026-11-09 (fetched `2026-11-09T02:48:35Z`, http 200, raw = txt sha256 `4111c45a…`). Located quote
  (`abstractText`, Results, 13 words): "The seventh (skilled translation of the search strategy to additional databases)
  was removed,". The record's `title`, `authorString`, `doi` (10.1016/j.jclinepi.2016.01.021), `pmid` (27005575),
  journal volume 75 and pages 40-46 (S225 prints the elided "40-6") agree with S225's "Derived from" citation. Tier B,
  not A (amended at F2, B5): the abstract is the statement's authors' own published text, but the lane read it
  through a third-party index record, and the lane's carrier rule grades third-party carriers B (kotodama grades the
  same Europe PMC shape B, `R98ConnectorSiblings` R6; `R98ReviewerC2` F5); its scope excludes the statement's body.

GATE-RECORD S231 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:27005575%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T02:48:35Z tier=B decision=admit capture=corpus/captures/4ec85a1e83553aa272caeb69.txt capture_sha256=4111c45aa041736ed313d577bdecd6581adffa62fb26e8630ccc6f9a054f0429 words=13 quote="The seventh (skilled translation of the search strategy to additional databases) was removed,"

Assimilation: none (no `merge/chousa/` theme taken; the round's claims are the routed defects and planned depth item).
considerthese: not mined this round (the latest file's proposals were not reopened; no item rides on them).

## Mistakes

| class | evidence | captured-by | fix |
|---|---|---|---|
| a guard was instrumented on the path where it fires (an exception inside a case) and not on the path that reports (recorded verdict, count, summary line, exit code), so a wrong report passed every self-test case | round 97 claimed each case runs "inside a guard that turns an exception … into that case's FAIL" (`.ufo/waves/round-97/claims.md`); its scored guard mutants `x1`-`x3` were crash-only (`corpus/evidence/round97/selftest-controls-r97.py:123-135`); `R97MutantsC1` g01-g05 (verdict, count, summary, exit) all survived the round-97 self-test (drafted by `R98ScribeLesson`) | round-97 named limit (b), which excluded the guard machinery instead of checking it | C1: guard canary `g00` runs `_collect`/`_summary` on four fixed case sets and, when it fails, the run prints its FAIL line itself. Shown able to fail: the base tool under the F2 battery prints `KILL_REQUIRED=12/35`, `CASE base g01…g05 … SURVIVED`, `SELFTEST_CONTROLS_R98=FAIL`, exit 1 (`corpus/evidence/round98/before-f2/c1-base.txt`). Residual, named (A4): a weakened comparison inside the canary and a `return 0` after `_summary` in `selftest()` (`R98ScribeLesson` F1) |
| an http 200 was taken to mean the body is the document | S230 (NCBI Bookshelf) answered http 200 with a reCAPTCHA page; `tools/capture-fetch.py` stored it and `tools/gate-records.py` accepts a GATE-RECORD quoting it (`OK`, exit 0: `corpus/evidence/round98/gate-records-challenge-200.txt`); the round-85 repair narrowed admission to "http exactly 200" because a 203 carries a cookie wall | none (the 200-only rule is the check, and it passes this) | QUALITY 229: no capture cited by a GATE-RECORD matches the challenge-page pattern; shown able to fail: the same pattern over every stored capture lists four challenge pages, S230's among them (same receipt). The tool rule (refuse a challenge body at admission) is routed to round 99 |
| a quote's field inside a structured capture was not recorded, so a title was presented as abstract text | F entry: "Every S231 quote below is a substring of that string [`abstractText`]"; M1 is the record's `title` (`R98ReviewerC2` F1, `R98ExecC2Repro`, `R98ScoutSources`, `R98CriticClaims`); `gate-records.py` and the F controls matched the whole capture | the claim's kill rule K2, by a reviewer only | B1: the F2 controls' FIELD leg checks each S231 quote against its JSON field; shown able to fail: forgery f11 (an S231 quote from the journal field, present in the capture) is refused `field_bad=['M15']` (`corpus/evidence/round98/after-f3/c2-all.txt`) |
| a checker's own exit-code and one-failure paths were stated in its docstring without a fixed set that exercised them | F canary docstring: a summary that "returns 0 for one [failure]" fails it; its failing set had three failures, so S03 (`k >= n-1` returns 0) and X4 survived, and the direct FAIL path never ran (D01-D04) (`R98MutantsC1` §1-2) | none | A1-A2: one-failure and four-failure canary sets; the battery's DIRECT_PATH leg forces the canary to fail and to raise. Shown able to fail: `after-f2/c1-rescore-r98mutants.txt` — S02, S03 `KILLED`; D01-D04 survive the self-test alone and each fails the F2 battery's DIRECT_PATH leg (`battery_rc=1`) |

Misroot sweep (`git -C /home/vgpnk/Projects/shokunin status --porcelain`, run before the report): no file from this round's seats at the fleet root (the only
entries are orchestrator-owned `.scratch/` files, never a misroot). None found, so no row.
