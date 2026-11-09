# Round 97 — the search re-run self-test answers its round-96 attackers, and the PRESS 2015 checklist is held question by question through two reprints (2026-11-09)

Base `c8087ac529003e667505bcc624f9a7bde0cffbce` (round-96 landing). Freeze F
`9a0ce2015fa0254848f2f32f612b20caf7dc5478`; carrier `4de41332` (after receipts at F). Frozen claims:
`.ufo/waves/round-97/claims.md` / `claims.json`. Two claims: C1 operability (`tools/search-rerun.py --selftest`
scored against the 30 mutants round-96 seats wrote) and C2 depth (`corpus/knowledge/press-checklist-questions-r97.md`,
sourced on S225 and S226, both opened this round). Approval table for the round's GETs:
`corpus/evidence/round97/egress-approval.md`.

## Gate

Registry: three rows added — `S225` (Cochrane's checklist for editors, which reprints the PRESS 2015 checklist,
tier B, `mined`), `S226` (Karolinska Institutet University Library's reprint, tier C, `mined`, corroboration only)
and `S227` (CADTH Table 9, tier A for its scope, `rejected` for route); `used-by` of S225 and S226:
`corpus/knowledge/press-checklist-questions-r97.md`. No existing row's `status`, `recheck` or `used-by` cell changed.
Census exit 0 before (`corpus/evidence/round97/census-start.txt`, 223 rows) and after
(`corpus/evidence/round97/census-end.txt`).

Routes tried before the approval table was written (browser-UA GET from this host, 2026-11-09, bytes discarded):
CADTH E&E PDF 403, CADTH Table 9 PDF 403, CADTH Table 10 PDF 403, `core.ac.uk/download/pdf/82048291.pdf` 403,
Europe PMC record for PMID 27005575 (no PMC copy; full-text links point at the publisher), `web.archive.org`
TCP connect timeout (archive.org's availability API answered and lists 200 snapshots of the E&E, unreachable from
here). Web searches: `PRESS Peer Review of Electronic Search Strategies 2015 Guideline Explanation and Elaboration
CADTH PDF`; `"orphan lines" "PRESS 2015" checklist "Are there any spelling errors" "Translation of the research question"`.

- **S225 admitted (tier B).** URL
  `https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf`,
  accessed 2026-11-09 (fetched `2026-11-09T01:59:44Z`, http 200, raw sha256 `56c4cdd6…`, txt sha256 `abd08a93…`).
  Located quote (page 2, element 5, capture line 72, 5 words): "Are there any spelling errors?" Tier B, not A: a
  methods organisation's reprint that says it is "Derived from" the guideline statement, not the statement.

GATE-RECORD S225 url=https://work.cochrane.org/sites/work.cochrane.org/files/uploads/checklist_searches_for_editors_cochrane_work.pdf fetched=2026-11-09T01:59:44Z tier=B decision=admit capture=corpus/captures/347c55ba9be9d63afe17986e.txt capture_sha256=abd08a9333c7f1ef8306032e4d1dc05a54e751d61ddfb3eb5b7d7861c6d3c9c8 words=5 quote="Are there any spelling errors?"

- **S226 admitted (tier C, corroboration only).** URL
  `https://kib.ki.se/en/search-evaluate/systematic-reviews/press-2015-checklist-search-strategies`, accessed
  2026-11-09 (fetched `2026-11-09T01:59:45Z`, http 200, raw sha256 `777b890f…`, txt sha256 `16114498…`). Located
  quote (capture line 503, 11 words): "a structured tool for peer review of electronic literature search strategies."
  Tier C: a library guide page; no decision row rests on it alone (`SOLE_SUPPORT=8/8`).

GATE-RECORD S226 url=https://kib.ki.se/en/search-evaluate/systematic-reviews/press-2015-checklist-search-strategies fetched=2026-11-09T01:59:45Z tier=C decision=admit capture=corpus/captures/80a844fe287a1a26d4280251.txt capture_sha256=161144983ec5b3b882afca0bbf83a1e1662ab95c85fc8e869d5441325b0c8ee4 words=11 quote="a structured tool for peer review of electronic literature search strategies."

- **S227 rejected (unreachable, not fabrication).** URL
  `https://www.cda-amc.ca/sites/default/files/PRESS_Peer_Review_Electronic_Search_Strate/Table_9-PRESS.pdf`,
  attempted `2026-11-09T01:59:45Z`, curl rc 22, http 403; no bytes. Its registry row exists with the same id the
  `refetch.tsv` row carries, so the round-96 id-collision mistake (spot-check D1) does not repeat. Flip: a 200 from
  the agency host or a readable archived copy.

GATE-RECORD S227 url=https://www.cda-amc.ca/sites/default/files/PRESS_Peer_Review_Electronic_Search_Strate/Table_9-PRESS.pdf fetched=2026-11-09T01:59:45Z tier=A decision=reject capture=none curl_rc=22 http=403 words=0 quote=none

Status / recheck / used-by changes: none on existing rows (old→new: —).

## Mistakes

| class | evidence | captured-by | fix |
|---|---|---|---|
| a self-test's pass count was taken as its grip, measured only against mutants its author chose | round 96: `--selftest` printed `PASS cases=32/32` while 19 of 29 applied `R96MutantsC1` mutants survived it, 4 of them (n11, n12, n13, n26) by crashing with a traceback and no summary (`.ufo/waves/round-96/w1/R96MutantsC1-mutprobe-out.txt`; drafted by `R97ScribeLesson`) | the round-96 battery's own mutant set (`selftest-controls-r96.py` MUTANTS), which were the author's sites | C1: the self-test is scored against the mutants non-author seats wrote; shown able to fail — the base tool scored by the F2 battery prints `EXTERNAL_KILLED=10/34`, `SELFTEST_CONTROLS_R97=FAIL`, exit 1 (`corpus/evidence/round97/before-f2/c1-base.txt`) |
| an equivalence verdict on a mutant was accepted on its author's word | F excluded `n30-sep-row-lenient` as "equivalent" citing `R96MutantsC1.md:154-159`; a 7-cell separator row is refused `TABLE` by the tool and parsed by the mutant (`.ufo/waves/round-97/w1/R97ConnectorSiblings-n30-witness.txt`), and n30 survived F's 47-case self-test | none (no criterion asked for a witness search before an exclusion) | case `r16-sep-width`, n30 scored at F2; QUALITY 227. Shown able to fail: n30 survives the base tool (`before-f2/c1-base.txt`, `CASE base n30-sep-row-lenient rc=0 SURVIVED`) |
| a guard placed around case bodies was described as closing a crash class that also lives in shared set-up | F's `case()` guard; `raise` in `git_env`, in `st_row` or in `case` after its guard still ended the run with a traceback and no summary (`.ufo/waves/round-97/w1/R97ScribeLesson-unguarded-residue.txt`) | the claim's named limit (b) named only the guard itself | outer guard around `_selftest_cases`, mutants `x1`-`x3` scored; shown able to fail: all three survive the base tool (`before-f2/c1-base.txt`, `CASE base x1-…`, `x2-…`, `x3-…` `SURVIVED`) |
| a prose count confused two measured quantities, and the instrument checked only the other place the numbers were stated | F entry, Citing row Lane cell: "12 of the 26 S225 quotes are not found verbatim" — 12 is the *letters* miss count; verbatim misses are 16 (`R97ReviewerC2` F1, `R97ScoutSources` F-C1, `R97CriticClaims` F1); CORROBORATION at F checked only the `## Two reprints compared` sentence | none | B1: the F2 controls check the Lane cell's counts against the recount; QUALITY 228. Shown able to fail: `CASE corroboration-lane-forged lane_misses=(12, 12, 26) ok` (the F text's own number, refused) in `corpus/evidence/round97/after-f2/c2-all.txt` |
| a seat read a receipt while the L1's background job was still writing it | `R97ScribeLesson` F4: `after/c1-all.txt` ended at `regression-rerun-controls-r95` when read; the committed bytes (`git show 4de41332:corpus/evidence/round97/after/c1-all.txt`) end with the tally and `exit=0` | none | the F2 C1 receipt is written to scratch and moved into the lane only when complete (`after-f2/c1-all.txt`) |

Misroot sweep: see the round report (`git -C /home/vgpnk/Projects/shokunin status --porcelain`).

Misroot sweep (`git -C /home/vgpnk/Projects/shokunin status --porcelain`, run before the report): 16 untracked files
`R97RevenPrior-r95-*.txt` and `R97RevenPrior-r96-*.txt` at the fleet root — this round's `R97RevenPrior` seat wrote its
per-mutant battery outputs with relative paths (8 name its scratch `chousa-r97/R97RevenPrior` in their header; the
other 8 are the same seat's round-96-battery runs over the same mutant names n02-s2). Each copied byte-exact to the
same relative path under the lane, verified with `cmp`, and the fleet copy deleted. Class: a seat's relative path
resolves from the fleet root (prompt §3); captured-by: the wave context's absolute-path rule; fix: none new — the
rule existed and the seat broke it, recorded here.
