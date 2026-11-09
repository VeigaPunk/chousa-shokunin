# Round 100 — the gate judges a rev record by what git returns, and the lane's held quotation-error rate meets its 2025 update (2026-11-09)

Base `929c784c63a1fd17961d21742101b2b109b7b8ff` (round-99 landing plus its non-author spot-check). Pre-freeze build P
`9683523467a1be9a9c46972f9b92bed26f44750d`; pre-freeze controls R `6f837487be6cf686bcee16902299dba34ec7f063`
(`corpus/evidence/round100/before/`); freeze F `6d4e8487ee6a16823c24a8e085c6559b92b9fec8` (recorded in
`plans/round-100.md` `## Freeze` by carrier `7d2d3abe3fd0f739049bb4d4f91c9327c054f3c0`); wave-forced re-freezes F2
`0a3da3dab7bab333fc3789b909740bb62c64da87` (A1-A4, B1-B9) and F3 `4ba51a26977813373a85b706c752cd32a58925c1` (A5-A6, after `R100SentinelC1`; `.ufo/waves/round-100/claims.md`
`## Amendments`). Two claims: C1 operability (`tools/gate-records.py` rev-form
CHALLENGE by capture identity, battery `corpus/evidence/round100/challenge-controls-r100.py`) and C2 freshness
(`corpus/knowledge/quotation-error-update-r100.md` plus the round-99 entry's `## Update`, sourced on S238, opened this
round). Approval table for the round's GETs: `corpus/evidence/round100/egress-approval.md`, written before the first GET.

## Gate

Registry: three rows added — `S237` (Europe PMC full text PMC4627914, `rejected`, http 500 ×3), `S238` (Europe PMC core
record of PMID 40696441, tier B, `mined`) and `S239` (Europe PMC full text PMC12285159, `rejected`, http 500 ×3). One
existing row changed in place: `S236` `used-by` `corpus/knowledge/quotation-error-rates-r99.md` →
`corpus/knowledge/quotation-error-rates-r99.md, corpus/knowledge/quotation-error-update-r100.md`. Census exit 0 before
(`corpus/evidence/round100/census-start.txt`) and after (`corpus/evidence/round100/census-end.txt`); one new warning,
W04 S237/S235 same URL across scopes (S235 is the round-99 attempt on the same route; both rejected).

No web search this round: every URL was named by committed round-99 artifacts (SCORECARD `## Planned — round 100`
item 2; `.ufo/waves/round-99/w1/R99ScoutSources.md`).

- **S237 rejected (unreachable, not fabrication).** URL
  `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4627914/fullTextXML`, attempted 2026-11-09T05:12:31Z, 05:18:33Z,
  05:28:38Z; curl rc 22, http 500 each; no bytes. Flip: a 200 carrying the article XML. A round-99 seat's re-open had
  answered 200; the lane's recipe got 500 three times (`R100ScoutSources` compares request headers).
- **S238 admitted (tier B).** URL
  `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:40696441%20AND%20SRC:MED&resultType=core&format=json`,
  accessed 2026-11-09 (fetched `2026-11-09T05:12:32Z`, http 200, raw = txt, sha256 `175f805d…`). Located quote
  (`abstractText`, Results, 19 words): "16.9% (95% CI: 14.1%-20.0%) of quotations were incorrect, with approximately half
  classified as major errors (8.0% [95% CI: 6.4%-10.0%])." The record's `pmid` 40696441, `pmcid` PMC12285159, `doi`
  10.1186/s41073-025-00173-z, `pubYear` 2025, volume 10 (controls leg IDENTITY). Tier B: the authors' own abstract
  carried by a third-party index record (the lane's carrier rule, as S236 and S231).
- **S239 rejected (unreachable).** URL `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12285159/fullTextXML`,
  attempted 2026-11-09T05:12:32Z, 05:18:35Z, 05:28:39Z; curl rc 22, http 500 each. Flip: a 200 carrying the article XML.

Wave corrections recorded here (`R100ScribeLesson` F-2, F-7), the approval table itself unchanged (it was written before
the first GET and is not rewritten): round 99 named the update's identifiers (pmid 40696441, PMC12285159) and the
route kind, not the exact query string; S238's URL is the lane's composition on the S236 pattern
(`EXT_ID:<pmid>%20AND%20SRC:MED&resultType=core&format=json`). The entry's three `## Searches` expressions were chosen
from S238's own text, so their 0 hits at base show the store did not hold it, not that a broad search found nothing.

Admit/reject pair for the closure's spot-check: S238 (admit) and S239 (reject).

Fleet tier question (round-99 routed defect 5, index-record abstracts: tameshi A vs chousa B) — unchanged; S238 graded B
under the lane's rule. Assimilation: none (no `merge/chousa/` theme taken; the round's claims are a routed defect and a
fired recheck). considerthese: not mined this round.

## Mistakes

| class | evidence | captured-by | fix |
|---|---|---|---|
| a test leg meant to show a normalization step live fed the tool text that was already normalized upstream, so the mutant it targeted was invisible | first battery draft: NORM legs k1/k2 are url/admit records, and the url/admit branch calls `norm()` before `is_challenge`, so oracle o12 (`norm` dropped inside `is_challenge`) printed `battery=PASS` (`plans/round-100.md` P0) | QUALITY 126 (the pre-freeze forger battery) — the oracle row itself | rev leg r11 (a capture whose marker is split by a newline and a tab; the rev text is not pre-normalized) added before P; shown able to fail: `corpus/evidence/round100/before/c1-candidate.txt` `CASE ORACLE o12-no-norm battery=FAIL PASS` |
| a guard keyed a path by its spelling while the resolver reads it semantically (round-99 Mistakes 3, carried) | round-99 tool: `CAP_RE.fullmatch(kv["path"])` gates the rev CHALLENGE call; `before/c1-base.txt` `REV=3/11`, `BASE_REV_ADMITTED=8/11` | `R99SentinelC1` F-1 only (no lane criterion) | `rev_capture_text` judges by object identity; QUALITY 231; shown able to fail: `before/c1-base.txt` FAIL exit 1 vs `before/c1-candidate.txt` PASS, and oracle o1 (spelling-keyed guard) `battery=FAIL` |
| a registry anchor cited fetch times from the shell's clock line, not from the fetch log | P's S237/S239 anchors said "05:18:32Z and 05:28:37Z" (the `date -u` printed before each fetch); `refetch.tsv` rows are 05:18:33Z/05:18:35Z and 05:28:38Z/05:28:39Z | none (the census does not read anchors against `refetch.tsv`) | anchors rewritten from `refetch.tsv`; shown able to fail: `corpus/evidence/round100/after-f2/anchor-times.txt` (`ANCHOR_TIMES rev=96835234 logged=2/6` exit 1 at P; `logged=6/6` exit 0 after) |
| a fixture with one state cannot show which state a tool reads | the battery's fixture repo has one commit; a HEAD-tree stand-in and a repo-keyed cache both print the frozen PASS line (`.ufo/waves/round-100/w1/R100CriticClaims.md` F-1, `R100ExecC1Repro.md` finding 1, `R100MutantsC1.md` survivor `n-cache-repoonly`) | none in the lane; the §8 ledger (wave artifacts) | sentence narrowed at F2 (A1, named limit (f)); fix routed to round 101: a two-commit fixture with cross-rev legs and a two-rev single-file record — not yet shown able to fail |
| a presence check was taken as evidence that a flag's content is true | FRESH checks that the round-99 `## Update` names the new entry and S238; an Update stating "has NOT fired" passes (`R100ConnectorSiblings.md` F2, `R100CriticClaims.md` F-6) | none; the §8 ledger | sentence narrowed at F2 (B4, named limit (e)); routed: the Update must carry one checkable warrant numeral, and an `on-release` names its watcher (kagi QM70/QM73 via `R100ConnectorSiblings` R1) — not yet shown able to fail |

## Gate records

GATE-RECORD S238 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:40696441%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T05:12:32Z tier=B decision=admit capture=corpus/captures/b5eec205612ee5f138cf065d.txt capture_sha256=175f805d6460acd61f2a8c979388a500e35b9c85217d3531ae1fb4418c613a98 words=19 quote="16.9% (95% CI: 14.1%-20.0%) of quotations were incorrect, with approximately half classified as major errors (8.0% [95% CI: 6.4%-10.0%])."
GATE-RECORD S237 url=https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4627914/fullTextXML fetched=2026-11-09T05:12:31Z tier=B decision=reject capture=none curl_rc=22 http=500 words=0 quote=none
GATE-RECORD S239 url=https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12285159/fullTextXML fetched=2026-11-09T05:12:32Z tier=B decision=reject capture=none curl_rc=22 http=500 words=0 quote=none
