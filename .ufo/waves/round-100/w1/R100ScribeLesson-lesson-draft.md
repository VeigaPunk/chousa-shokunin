# Round 100 — the gate judges a rev record by what git returns, and the lane's held quotation-error rate meets its 2025 update (2026-11-09)

Base `929c784c63a1fd17961d21742101b2b109b7b8ff` (round-99 landing plus its non-author spot-check). Pre-freeze build P
`9683523467a1be9a9c46972f9b92bed26f44750d`; pre-freeze controls R `6f837487be6cf686bcee16902299dba34ec7f063`
(`corpus/evidence/round100/before/`); freeze F `6d4e8487ee6a16823c24a8e085c6559b92b9fec8` (recorded in
`plans/round-100.md` `## Freeze` by carrier `7d2d3abe3fd0f739049bb4d4f91c9327c054f3c0`). Two claims: C1 operability
(`tools/gate-records.py` rev-form CHALLENGE by capture identity, battery
`corpus/evidence/round100/challenge-controls-r100.py`) and C2 freshness (`corpus/knowledge/quotation-error-update-r100.md`
plus the round-99 entry's `## Update`, sourced on S238, opened this round). Approval table for the round's GETs:
`corpus/evidence/round100/egress-approval.md`, written before the first GET.

## Gate

Registry: three rows added — `S237` (Europe PMC full text PMC4627914, `rejected`, http 500 ×3), `S238` (Europe PMC core
record of PMID 40696441, tier B, `mined`) and `S239` (Europe PMC full text PMC12285159, `rejected`, http 500 ×3). One
existing row changed in place: `S236` `used-by` `corpus/knowledge/quotation-error-rates-r99.md` →
`corpus/knowledge/quotation-error-rates-r99.md, corpus/knowledge/quotation-error-update-r100.md`. Census exit 0 before
(`corpus/evidence/round100/census-start.txt`); the census after the three new rows adds one warning, W04 `S237` same URL
across scopes (S235 is the round-99 attempt on the same route; both rejected) and still exits 0 — but **the after-census
receipt is not yet committed** (`corpus/evidence/round100/census-end.txt` does not exist at the time of writing; the
lesson must not cite a receipt that is absent).

No web search this round: every URL was named by committed round-99 artifacts (SCORECARD `## Planned — round 100`
item 2; `.ufo/waves/round-99/w1/R99ScoutSources.md`). The S238 URL string itself (`…/search?query=EXT_ID:40696441%20AND%20SRC:MED&resultType=core&format=json`)
appears nowhere in the base tree — round 99 named the DOI form of that endpoint and the pmid `40696441`; the lane
composed the EXT_ID form from the round-99 pmid plus the round-98/99 route pattern. The route and the document are
named; the exact query string is the lane's own composition.

- **S237 rejected (unreachable, not fabrication).** URL
  `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4627914/fullTextXML`, attempted 2026-11-09T05:12:31Z, 05:18:33Z,
  05:28:38Z; curl rc 22, http 500 each; no bytes, no capture file. Flip: a 200 carrying the article XML. A round-99 seat's
  re-open had answered 200; the lane's recipe got 500 three times (`R99ScoutSources` compares request headers).
- **S238 admitted (tier B).** URL
  `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:40696441%20AND%20SRC:MED&resultType=core&format=json`,
  accessed 2026-11-09 (fetched `2026-11-09T05:12:32Z`, http 200, raw = txt, sha256 `175f805d…`). Located quote
  (`abstractText`, Results, 19 words): "16.9% (95% CI: 14.1%-20.0%) of quotations were incorrect, with approximately half
  classified as major errors (8.0% [95% CI: 6.4%-10.0%])." The record's `pmid` 40696441, `pmcid` PMC12285159, `doi`
  10.1186/s41073-025-00173-z, `pubYear` 2025, volume 10 (controls leg IDENTITY). Tier B: the authors' own abstract
  carried by a third-party index record (the lane's carrier rule, as S236 and S231).
- **S239 rejected (unreachable).** URL `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12285159/fullTextXML`,
  attempted 2026-11-09T05:12:32Z, 05:18:35Z, 05:28:39Z; curl rc 22, http 500 each; no bytes, no capture file. Flip: a
  200 carrying the article XML.

Admit/reject pair for the closure's spot-check: S238 (admit) and S239 (reject).

**One row the round opened carries no GATE-RECORD line at the freeze.** At F, S237 has no `GATE-RECORD` line anywhere in
the frozen tree (`git grep -n "GATE-RECORD S237" 6d4e8487 -- .` → exit 1, no match; receipt
`.ufo/waves/round-100/w1/R100ScribeLesson-receipt-record-coverage.txt`), while S238 has 14 and S239 has 1 — and no
round-100 lesson existed at F to carry it. QUALITY 173 (`corpus/QUALITY.md:1110`) requires that every registry row the
round opened is recorded in a `GATE-RECORD` line at this round's `fetched` time, *or* that the lesson names the schema
gap that prevents one. Round 99 met the same clause for its two rejected rows (S232 and S235 each have a `url/unreach`
line in the r99 entry *and* the r99 lesson), and the form fits S237 exactly — the `url/unreach` line below verifies `OK`
against the frozen tool (`R100ScribeLesson-receipt-S237-no-record.txt`), so there is no schema gap to name. The frozen C2
counting command 1 (`python3 -B tools/gate-records.py verify --root . corpus/knowledge/quotation-error-update-r100.md`)
cannot see the gap: it reads one file and counts the records that are there (`records=17 ok=17 fail=0`), and the missing
line is on a row it never asks about. This lesson carries the S237 `url/unreach` line (in `## Gate records` below); with
it committed, the coverage walk over the rows added since the base reports `rows_without_record=0`, exit 0
(`R100ScribeLesson-receipt-record-coverage.txt`). The after-census receipt must land with it.

Fleet tier question (round-99 routed defect 5, index-record abstracts: tameshi A vs chousa B) — unchanged; S238 graded B
under the lane's rule. Assimilation: none (no `merge/chousa/` theme taken; the round's claims are a routed defect and a
fired recheck). considerthese: not mined this round.

## Mistakes

| class | evidence | captured-by | fix |
|---|---|---|---|
| a guard keyed a path by its spelling while the resolver reads it semantically (round-99 Mistakes 3, carried) | round-99 tool: `CAP_RE.fullmatch(kv["path"])` gates the rev CHALLENGE call; `before/c1-base.txt` `REV=3/11`, `BASE_REV_ADMITTED=8/11` | `R99SentinelC1` F-1 only (no lane criterion) | `rev_capture_text` judges by object identity; QUALITY 231; shown able to fail: `before/c1-base.txt` FAIL exit 1 vs `before/c1-candidate.txt` PASS, and oracle o1 (spelling-keyed guard) `battery=FAIL` |
| a battery that crashes on a missing fixture reports a traceback instead of a setup error, so a broken setup reads as a broken assertion | round-99 battery opens each lane capture unguarded (`corpus/evidence/round99/challenge-controls-r99.py:139`); with `corpus/captures/b90988847e704a08aabc8321.txt` removed it dies `FileNotFoundError` and exits 1, while the round-100 battery prints `CHALLENGE_CONTROLS_SETUP missing lane capture …` and exits 2 (`corpus/evidence/round100/before/c1-setup.txt:4-9`) | none (the round-99 spot-check routed it as defect 2; no lane criterion names it) | round-100 battery raises `Setup` on a missing lane capture (`challenge-controls-r100.py:218`) and exits 2; shown able to fail: the same missing file still makes the *round-99* battery crash with exit 1, so the two paths are distinguishable (`R100ScribeLesson-receipt-setup-repro.txt`) |
| a count written into an artifact from the shape of a plan instead of from the instrument that recorded the events | the frozen entry says S239's full-text route "answered http 500 to **both** of this round's GETs" and "to this round's **two** GETs" (`corpus/knowledge/quotation-error-update-r100.md:20,89`), while `corpus/evidence/round57/refetch.tsv` holds **three** S239 attempts (05:12:32Z, 05:18:35Z, 05:28:39Z) and three S237 attempts | QUALITY 173 (the record must carry the round's own `fetched` time) and the round-99 spot-check's routed defect 1 (a receipt whose echo must match the blob it ran) — named, not enforced by any counter | the entry's GET count re-read from `refetch.tsv`; shown able to fail: `before/c2-candidate.txt` carries no GET count, and the anchors themselves were wrong the same way until `after-f2/anchor-times.txt` (`ANCHOR_TIMES rev=96835234 logged=2/6` exit 1) — the same defect in the registry's own anchor cells |
| a row the round opened can be left with no record and no counter notices, because every counter reads the file it was pointed at | S237 has no `GATE-RECORD` line anywhere in the frozen tree while S238 has 14 and S239 has 1; QUALITY 173 (`corpus/QUALITY.md:1110`) asks for a record per opened row, and the round-99 `url/unreach` form fits S237 exactly (it verifies `OK`) | none — the C2 counters read `corpus/knowledge/quotation-error-update-r100.md` only, and `entry-controls-r100.py` never consults `corpus/SOURCES.md`, so a missing row is invisible to all of them | the lesson carries the S237 `url/unreach` line, and a coverage check that walks the rows added since the base and counts their records; shown able to fail: `R100ScribeLesson-receipt-record-coverage.txt` (`RECORD_COVERAGE rev=6d4e8487 rows_added=3 rows_without_record=1`, exit 1) — the same walk over the working tree reports `rows_without_record=0`, exit 0 |
| a counter that reads one revision's tree cannot tell a tool that reads a different revision's tree | the round-100 battery's fixture repo has one commit, so a stand-in that builds the capture set at `HEAD` instead of at the record's `rev` prints the frozen PASS line unchanged (`R100ScribeLesson-receipt-M1-head-tree.txt`: `REV=11/11 … CHALLENGE_CONTROLS_R100=PASS`, exit 0) — while the two tools give **different** verdicts on a two-commit fixture where the capture exists at the record's rev and was deleted at `HEAD` (frozen tool `FAIL CHALLENGE,REGISTRY,WORDS` vs mutant `FAIL REGISTRY,WORDS`) | none in the lane; the §8 wave ledger (`R100CriticClaims` F-1, `R100ExecC1Repro` finding 1, `R100MutantsC1` survivor `n-cache-repoonly`) | sentence narrowed at F2 (A1, named limit (f)); fix routed to round 101: a two-commit fixture with cross-rev legs and a two-rev single-file record — not yet shown able to fail |

## Gate records

GATE-RECORD S238 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:40696441%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T05:12:32Z tier=B decision=admit capture=corpus/captures/b5eec205612ee5f138cf065d.txt capture_sha256=175f805d6460acd61f2a8c979388a500e35b9c85217d3531ae1fb4418c613a98 words=19 quote="16.9% (95% CI: 14.1%-20.0%) of quotations were incorrect, with approximately half classified as major errors (8.0% [95% CI: 6.4%-10.0%])."
GATE-RECORD S237 url=https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4627914/fullTextXML fetched=2026-11-09T05:12:31Z tier=B decision=reject capture=none curl_rc=22 http=500 words=0 quote=none
GATE-RECORD S239 url=https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12285159/fullTextXML fetched=2026-11-09T05:12:32Z tier=B decision=reject capture=none curl_rc=22 http=500 words=0 quote=none
