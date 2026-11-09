# R98ScribeLesson — draft: round-98 lesson `## Mistakes` and `## Gate` lines (scribe)

Draft for `corpus/lessons/round-98.md` (L1 `ChousaR98` owns the file; not edited here). Base `98b8177c`, freeze F
`aac82684`. Every path:line below was opened by this seat at F; receipts are in `.ufo/waves/round-98/w1/`
(`R98ScribeLesson-*`).

## Mistakes

One class mined this round. The fix is shown able to fail, and the residual it does not reach is stated in the row.

| class | evidence (path:line) | captured-by | fix (and how it was shown able to fail) |
|---|---|---|---|
| a guard was instrumented only on the path where it fires (an exception raised inside a case) and not on the path that reports (the recorded verdict, the count, the summary line, the exit code), so a wrong report from the guard passed every instrument | round 97 claimed "each [case] inside a guard that turns an exception … into that case's FAIL": `.ufo/waves/round-97/claims.md:10` and `:102`. The guard at BASE `98b8177c` is `tools/search-rerun.py:569-576` (`except Exception` → `ok, detail = False, …`), `:575` (`results.append((cid, bool(ok)))`) and `:587` (`return 0 if k == n else 1`). The round-97 guard mutants were crash-only: `corpus/evidence/round97/selftest-controls-r97.py:123-135` (`x1`-`x3`, each a `raise`). The verdict-path mutants g01-g05 survived the round-97 self-test and the round-95 battery: `.ufo/waves/round-97/w1/R97MutantsC1.md:45-59` and `:141-144` ("no oracle exists in the r97 battery either") | none. The round-97 self-test passed `48/48`; its battery's 34 mutants had no verdict-path guard site; the round-95 battery never runs `--selftest`. The gap was routed after landing (`corpus/lessons/round-97-verifier-spotcheck.md:110`), not caught by a criterion | Fix: `_guard_canary` (`tools/search-rerun.py:676-699`) runs `_collect` and `_summary` on one failing and one passing fixed set and compares every printed line and the exit code; `selftest()` runs it first (`:715`) and prints the FAIL summary itself if it fails. The battery requires g01-g05 KILLED (`EXTERNAL_R97_KILLED=35/37`, named survivors only `u01`, `u05`). Shown able to fail: the round-97 tool under the same battery: `corpus/evidence/round98/before/c1-base.txt:8-12` (`g01`-`g05` each `rc=0 SURVIVED`) and `:83` (`BASE_KILLED=12/37 required_killed=12/35 … expect<35 ok`). At F the same five die: `.ufo/waves/round-98/w1/R98ScribeLesson-battery-F.txt:2-6` (`CASE r97ext g0N … rc=1 KILLED failed=g00-guard-canary`), reproduced by this seat in `R98ScribeLesson-direct-g.txt`. The guard-blind oracle drops to `KILL_REQUIRED=30/35` (`R98ScribeLesson-battery-F.txt:141`), so the battery does observe the guard. **Residual, not closed:** the exit path of `selftest()` itself, `tools/search-rerun.py:723` (`return _summary(results)`). A one-site mutant that returns `0` there is not caught: on a healthy tree it prints `PASS cases=67/67` and exits 0 like F; with one failing case it prints `FAIL` and returns 0 where F returns 1 (`R98ScribeLesson-exit-probe.txt`). The canary never calls `selftest()`'s return, and no lane case fails on a healthy tree, so no frozen instrument sees it. The class is narrowed to the exit path of a run that fails, which nothing observes yet. |

## Gate

Registry (`corpus/SOURCES.md`, F): `S228`-`S230` rejected (route, not fabrication); `S231` admitted, tier A for the
abstract scope, `mined`. Access date for all four: 2026-11-09 (UTC, from `corpus/evidence/round57/refetch.tsv`).
Every line below was checked against the refetch row and, where a capture exists, its committed bytes
(`R98ScribeLesson-gate-hashes.txt`).

- **S228 rejected (unreachable, not fabrication).** URL
  `https://www.cda-amc.ca/sites/default/files/PRESS_Peer_Review_Electronic_Search_Strate/Report%20477_PRESS_Peer%20Review%20of%20Electronic%20Search%20Strategies_Appendices.pdf`,
  accessed 2026-11-09 (attempt 1, fetched `2026-11-09T02:47:35Z`). Refusal: curl rc 22, HTTP 403, no bytes (no
  capture file exists for key `555c86e99f6b87090f7cbd14`).

  GATE-RECORD S228 url=https://www.cda-amc.ca/sites/default/files/PRESS_Peer_Review_Electronic_Search_Strate/Report%20477_PRESS_Peer%20Review%20of%20Electronic%20Search%20Strategies_Appendices.pdf fetched=2026-11-09T02:47:35Z tier=A decision=reject capture=none curl_rc=22 http=403 words=0 quote=none

- **S229 rejected (route).** URL `https://pubmed.ncbi.nlm.nih.gov/27005575/`, accessed 2026-11-09 (fetched
  `2026-11-09T02:48:10Z`). Refusal: HTTP 203 (curl rc 0) with a cookie-challenge page: its text reads "Cookies must be
  enabled" and "Enable cookies for pubmed.ncbi.nlm.nih.gov and reload this page to continue". The bytes are stored
  at `corpus/captures/0954149536aaad411000e1fb.txt` (21 lines) and are not cited.

  GATE-RECORD S229 url=https://pubmed.ncbi.nlm.nih.gov/27005575/ fetched=2026-11-09T02:48:10Z tier=A decision=reject capture=corpus/captures/0954149536aaad411000e1fb.txt capture_sha256=7070b59c3434b67711f6a6ad723834ee1fce7a82230ac6970c1b12844c042a00 curl_rc=0 http=203 words=0 quote=none

- **S230 rejected (route).** URL `https://www.ncbi.nlm.nih.gov/books/NBK98350/`, accessed 2026-11-09 (fetched
  `2026-11-09T02:48:10Z`). Refusal: HTTP 200 (curl rc 0) but the body is a reCAPTCHA page: "Checking your browser
  before accessing www.ncbi.nlm.nih.gov". The report's identity is not confirmed from its own bytes. Bytes at
  `corpus/captures/b5b8d050eea0c638e95ba674.txt` (13 lines), not cited.

  GATE-RECORD S230 url=https://www.ncbi.nlm.nih.gov/books/NBK98350/ fetched=2026-11-09T02:48:10Z tier=A decision=reject capture=corpus/captures/b5b8d050eea0c638e95ba674.txt capture_sha256=4f25f0b14fb2450c633eefc0bfc0b09db390dab39f51e357866703da5c187802 curl_rc=0 http=200 words=0 quote=none

- **S231 admitted (tier A for the abstract scope, read through Europe PMC's index record).** URL
  `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:27005575%20AND%20SRC:MED&resultType=core&format=json`,
  accessed 2026-11-09 (fetched `2026-11-09T02:48:35Z`, curl rc 0, http 200, raw sha256 equal to txt sha256
  `4111c45a…`). The capture is one JSON line, no trailing newline; `hitCount` 1; `abstractText` of the single
  result, which carries the PRESS 2015 statement's DOI `10.1016/j.jclinepi.2016.01.021` and PMID 27005575. Located
  quote (16 words, capture line 1, inside `abstractText`): "No new search elements were identified for addition to
  the existing (2008-2010) PRESS 2015 Evidence-Based Checklist".

  GATE-RECORD S231 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:27005575%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T02:48:35Z tier=A decision=admit capture=corpus/captures/4ec85a1e83553aa272caeb69.txt capture_sha256=4111c45aa041736ed313d577bdecd6581adffa62fb26e8630ccc6f9a054f0429 words=16 quote="No new search elements were identified for addition to the existing (2008-2010) PRESS 2015 Evidence-Based Checklist"

Notes for the L1 (not lesson text):
- The S229 and S230 captures are challenge pages stored under `corpus/captures/` by the tool. The approval table says
  "a challenge page is a failed attempt, never a capture" (`corpus/evidence/round98/egress-approval.md`), and the S230
  row says "never a capture", yet both keys have a `.raw/.txt` under `corpus/captures/`. The Gate lines above say
  "bytes stored, not cited" to match what is on disk.
- The approval table's first paragraph says it "was written before any round-98 GET". Its own S229-S231 rows say
  they were added after the CADTH GET (and after the NCBI GETs). The file's mtime is `23:48:34` local, after the
  S228, S229 and S230 GETs and one second before S231. The lesson's sentence "written before the first one" should
  read "written before the first GET, with rows appended after GETs 1-3 (named in the table)".
