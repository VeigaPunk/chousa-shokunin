# Round 99 — the gate refuses challenge pages, and the lane holds how often a cited source fails the citing sentence (2026-11-09)

Base `47ed34fa785288837f84cde9db15c41300854a78` (round-98 landing plus its non-author spot-check). Freeze F
`d41f4cd8b857c6de683e7be5c5e8125b32763a8e` (written into `plans/round-99.md` `## Freeze` by carrier
`f8f480ffd738cda9b427e0fe8fa8e79c78fb409d`). Frozen claims: `.ufo/waves/round-99/claims.md` / `claims.json`. Two claims:
C1 operability (`tools/gate-records.py` CHALLENGE check, battery `corpus/evidence/round99/challenge-controls-r99.py`) and
C2 coverage (`corpus/knowledge/quotation-error-rates-r99.md`, sourced on S236 and S233, both opened this round).
Approval table for the round's GETs: `corpus/evidence/round99/egress-approval.md` — every row but one was written before
the first GET; the Europe PMC core-record row was appended after the GETs it names and before its own GET (disclosed in
the file).

Round-98 spot-check routed defect 1 (`claims.json` `freeze.F3` placeholder): round 98's F3 is
`1c6e01c52149c7b4d6dfc4a8cfc419243dc8c101` (its report's landed-changes table). The frozen round-98 file is not
rewritten; from this round the freeze hash is written by the commit after F (`plans/round-99.md` `## Freeze`) and
`claims.json` `freeze.F` says where.

## Gate

Registry: five rows added — `S232` (PeerJ 1364, `rejected`, http 403), `S233` (PLoS One e0184727, tier A, `mined`),
`S234` (Research Integrity and Peer Review s41073-025-00173-z, `rejected`, http 200 whose body is a "Client Challenge"
page), `S235` (Europe PMC full text PMC4627914, `rejected`, http 500) and `S236` (Europe PMC core record of PMID 26528420,
tier B, `mined`). No existing row changed. Census exit 0 before (`corpus/evidence/round99/census-start.txt`).

Web search (one query, the session's search tool, 2026-11-09): `Jergas Baethge 2015 Quotation accuracy in medical journal
articles systematic review meta-analysis PeerJ`. It returned PMC4627914 (the review), PMC5599002 (Mogull 2017), the 2025
update on the Springer/BMC host and the PeerJ review history; the publisher routes were tried first, Europe PMC's after
the PeerJ 403.

- **S232 rejected (unreachable, not fabrication).** URL `https://peerj.com/articles/1364/`, attempted
  `2026-11-09T04:00:32Z`, curl rc 22, http 403; no bytes, so no quote and no capture. Flip: a 200 carrying the article
  text.
- **S233 admitted (tier A).** URL `https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0184727`, accessed
  2026-11-09 (fetched `2026-11-09T04:00:33Z`, curl rc 0, http 200, txt sha256 `60048511…`, 8,455 words, the publisher's
  full text). Located quote (Abstract, 15 words, at `corpus/captures/4b70901ad80c513f0c2f750c.txt` line 910): "A total of
  15 studies met the criteria for inclusion in the primary quantitative analysis."
- **S234 rejected (route).** URL `https://researchintegrityjournal.biomedcentral.com/articles/10.1186/s41073-025-00173-z`,
  attempted `2026-11-09T04:00:33Z`, curl rc 0, http **200**; the body (capture key `b90988847e704a08aabc8321`, 37 words)
  is a challenge page — `corpus/captures/b90988847e704a08aabc8321.txt` line 8 reads " Client Challenge " and line 14
  "A required part of this site couldn't load." No `GATE-RECORD`: the url/unreach form refuses a 2xx status and, from
  F, the url/admit form refuses the capture (CHALLENGE). The article's identity rests on a search result only. Flip: a
  200 carrying the article text.
- **S235 rejected (unreachable).** URL `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4627914/fullTextXML`,
  attempted `2026-11-09T04:00:42Z`, curl rc 22, http 500; no bytes, so no quote and no capture. Flip: a 200 carrying the
  article XML.
- **S236 admitted (tier B).** URL
  `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:26528420%20AND%20SRC:MED&resultType=core&format=json`,
  accessed 2026-11-09 (fetched `2026-11-09T04:01:07Z`, curl rc 0, http 200, raw = txt sha256 `6b0bcbda…`, one line of
  JSON). Located quote (`abstractText`, Methods, 21 words): "We carried out a systematic review, meta-analysis and
  meta-regression of quotation errors, taking account of differences between studies in error ascertainment." The record's
  `pmid` 26528420, `doi` 10.7717/peerj.1364, `pubYear` 2015, journal PeerJ, volume 3 (controls leg IDENTITY). Tier B: the
  authors' own abstract carried by a third-party index record (the lane's carrier rule, as S231).

Assimilation: none (no `merge/chousa/` theme taken; the round's claims are a routed defect and a new province surface).
considerthese: not mined this round.

## Mistakes

| class | evidence | captured-by | fix |
|---|---|---|---|
| a lexical floor was written from the wordings already seen, so the next challenge page in other words passed it | QUALITY 229's check greps captures for `Checking your browser\|Cookies must be enabled\|Just a moment\|reCAPTCHA` (`corpus/QUALITY.md` 229); this round S234 answered http 200 with a "Client Challenge" page that carries none of the four (`corpus/captures/b90988847e704a08aabc8321.txt` line 8), and the base gate admits a record quoting it (`corpus/evidence/round99/before/c1-base.txt` line 16, `CASE PROD S234 rc=0 verdict=OK FAIL`) | QUALITY 229's own named limit ("a challenge page in other words passes it") — named, not enforced | C1: the gate's CHALLENGE check with 11 markers including "client challenge" and a 200-word bound, on the production path. Shown able to fail: the round-98 criterion's own check, run at F, prints nothing over S234's committed capture (`.ufo/waves/round-99/w1/R99ScribeLesson-quality229-at-F.txt`, `grep_rc=1` for `corpus/captures/b90988847e704a08aabc8321.txt`), and the gate refuses the same record (`CASE PROD S234 rc=1 verdict=CHALLENGE PASS`, `corpus/evidence/round99/after/c1-all.txt` line 15) |
| a freeze record named its commit by description because a commit cannot carry its own hash | round-98 `claims.json` `freeze.F3` = `"<the lane commit that first carries the F3 amendments>"` (round-98 spot-check §1, routed defect 1) | the round-98 non-author spot-check only | convention: the commit after F writes F's hash into `plans/round-99.md` `## Freeze`; `claims.json` names that place. Shown able to fail: `grep -c '<the lane commit' .ufo/waves/round-98/claims.json` → 1, the same over round 99's → 0 |

Misroot sweep (`git -C /home/vgpnk/Projects/shokunin status --porcelain`, run before the report): no file from this
round's seats at the fleet root (the only entries are orchestrator-owned `.scratch/` files, never a misroot). None found,
so no row.
