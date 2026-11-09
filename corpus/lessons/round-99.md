# Round 99 — the gate refuses challenge pages, and the lane holds how often a cited source fails its citing sentence (2026-11-09)

Base `47ed34fa785288837f84cde9db15c41300854a78` (round-98 landing plus its non-author spot-check). Freeze F
`d41f4cd8b857c6de683e7be5c5e8125b32763a8e` (recorded in `plans/round-99.md` `## Freeze` by carrier
`f8f480ffd738cda9b427e0fe8fa8e79c78fb409d`); wave-forced re-freezes F2 `96d761eec0c006d3df100b1a5d41686568d6d1e1`
(A1-A7, B1-B2) and F3 `c3bad643c42ecd1f04620bd6acfddb01d69c4aa3` (B3-B6). Frozen claims: `.ufo/waves/round-99/claims.md` / `claims.json`. Two claims:
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
tier B, `mined`). No existing row changed. Census exit 0 before (`corpus/evidence/round99/census-start.txt`) and after
(`corpus/evidence/round99/census-end.txt`).

Web search (one query, the session's search tool, 2026-11-09): `Jergas Baethge 2015 Quotation accuracy in medical
journal articles systematic review meta-analysis PeerJ`. It returned PMC4627914 (the review), PMC5599002 (Mogull 2017),
the 2025 update on the Springer/BMC host and the PeerJ review history; the publisher routes were tried first, Europe
PMC's after the PeerJ 403.

- **S232 rejected (unreachable, not fabrication).** URL `https://peerj.com/articles/1364/`, attempted
  `2026-11-09T04:00:32Z`, curl rc 22, http 403; no bytes. Flip: a 200 carrying the article text.
- **S233 admitted (tier A).** URL `https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0184727`, accessed
  2026-11-09 (fetched `2026-11-09T04:00:33Z`, http 200, txt sha256 `60048511…`, 8,455 words, the publisher's full
  text). Located quote (Discussion, 24 words): "I estimate that 14.5% (10.5% to 18.6% at a 95% confidence interval) of
  cited assertions in original research articles in medical journals are inaccurate."
- **S234 rejected (route).** URL `https://researchintegrityjournal.biomedcentral.com/articles/10.1186/s41073-025-00173-z`,
  attempted `2026-11-09T04:00:33Z`, curl rc 0, http **200**; the body (capture key `b90988847e704a08aabc8321`, 37 words)
  is "Client Challenge … A required part of this site couldn’t load". No `GATE-RECORD`: the url/unreach form refuses a 2xx
  status and, from F, the url/admit form refuses the capture (CHALLENGE). The article's identity rests on a search
  result only. Flip: a 200 carrying the article text.
- **S235 rejected (unreachable).** URL `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4627914/fullTextXML`,
  attempted `2026-11-09T04:00:42Z`, curl rc 22, http 500. Flip: a 200 carrying the article XML. The flip condition was
  met by wave seat `R99ScoutSources`' read-only re-open later the same night (http 200, 126,445 bytes); the row keeps
  the lane's own attempt and status, and a lane GET is routed to round 100.
- **S236 admitted (tier B).** URL
  `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:26528420%20AND%20SRC:MED&resultType=core&format=json`,
  accessed 2026-11-09 (http 200, raw = txt). Located quote (`abstractText`, Results, 12 words): "Indirect references
  accounted for less than one sixth of all quotation problems." The record's `pmid` 26528420, `doi` 10.7717/peerj.1364,
  `pubYear` 2015, journal PeerJ, volume 3 (controls leg IDENTITY). Tier B: the authors' own abstract carried by a
  third-party index record (the lane's carrier rule, as S231).

Fleet cross-check (`R99ConnectorSiblings` F4; L1 re-read of tameshi `corpus/SOURCES.md`): tameshi opened Europe PMC
records of both papers on 2026-11-08 — its S327 (Jergas & Baethge, DOI query, tier **A**, `mined`) and S328 (Mogull,
tier A, `rejected` for its own question). chousa grades the same index-record abstract **B** (S236, as S231) under its
carrier rule. Not absorbed; routed as a fleet question (one tier rule for index-record abstracts, or a recorded ruling
that lanes may differ).

Assimilation: none (no `merge/chousa/` theme taken; the round's claims are a routed defect and a new province surface).
considerthese: not mined this round.

## Mistakes

| class | evidence | captured-by | fix |
|---|---|---|---|
| a lexical floor was written from the wordings already seen, so the next challenge page in other words passed it | QUALITY 229's check greps captures for `Checking your browser\|Cookies must be enabled\|Just a moment\|reCAPTCHA` (`corpus/QUALITY.md` 229); this round S234 answered http 200 with a "Client Challenge" page that carries none of the four (`corpus/captures/b90988847e704a08aabc8321.txt`), and the base gate admits a record quoting it (`corpus/evidence/round99/before/c1-base.txt`, `CASE PROD S234 rc=0 verdict=OK FAIL`) | QUALITY 229's own named limit ("a challenge page in other words passes it") — named, not enforced | C1: the gate's CHALLENGE check with 11 markers including "client challenge" and a 200-word bound, on the production path. Shown able to fail: the base tool under the battery prints `PROD_REFUSED=0/4`, `CHALLENGE_CONTROLS_R99=FAIL`, exit 1 (`before/c1-base.txt`); QUALITY 230 makes the tool the check |
| a sentence about separability was written from the design, not from what the battery reads | F claims.md: "C1's battery reads S234's capture … and no C2 file"; the battery's POS p1/p2 quote C2's S233 and S236 captures and HARM reads C2's entry (`.ufo/waves/round-99/w1/R99CriticClaims.md`) | the §8 pre-file ledger (a wave seat's artifact) | A3 (F2): the sentence names the files read, and the separability probe runs the same battery with C2's entry and captures deleted and p1/p2 on BASE captures: `PASS`, exit 0 (`corpus/evidence/round99/after-f2/c1-separability.txt`); shown able to fail: the same probe without the p1/p2 swap cannot open the deleted captures (the battery opens `CAP` files unconditionally) |
| a guard keyed a path by its spelling while the resolver reads it semantically | F tool: the rev branch checks CHALLENGE only when `CAP_RE.fullmatch(kv["path"])`; `git cat-file` resolves `./corpus/captures/<key>.txt` to the same blob, so a rev record on S230's reCAPTCHA blob spelled that way prints `OK`, exit 0 (`.ufo/waves/round-99/w1/R99SentinelC1.md` F-1, `R99SentinelC1-probe-rev-paths.txt`) | none (claims.md limit (d) was written as "not under `corpus/captures/`") | A4 (F2) narrows limit (d) to the exact spelling; the tool fix (normalize the path before the guard) is routed to round 100 — not counted as a fix this round |
| a freeze record named its commit by description because a commit cannot carry its own hash | round-98 `claims.json` `freeze.F3` = `"<the lane commit that first carries the F3 amendments>"` (round-98 spot-check §1, routed defect 1) | the round-98 non-author spot-check only | convention: the commit after F writes F's hash into `plans/round-99.md` `## Freeze`; `claims.json` names that place. Shown able to fail: `grep -c '<the lane commit' .ufo/waves/round-98/claims.json` → 1, the same over round 99's → 0 |

## Gate records

GATE-RECORD S233 url=https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0184727 fetched=2026-11-09T04:00:33Z tier=A decision=admit capture=corpus/captures/4b70901ad80c513f0c2f750c.txt capture_sha256=60048511ac1de7f034c13bd89a6dcba8bae86b1cd71993fdea60529a78f790d3 words=24 quote="I estimate that 14.5% (10.5% to 18.6% at a 95% confidence interval) of cited assertions in original research articles in medical journals are inaccurate."
GATE-RECORD S236 url=https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:26528420%20AND%20SRC:MED&resultType=core&format=json fetched=2026-11-09T04:01:07Z tier=B decision=admit capture=corpus/captures/405a0054e1f6dbd1854a3618.txt capture_sha256=6b0bcbda40de0c02268931d749701142a1e222edf679d4055577130af886ac31 words=12 quote="Indirect references accounted for less than one sixth of all quotation problems."
GATE-RECORD S232 url=https://peerj.com/articles/1364/ fetched=2026-11-09T04:00:32Z tier=A decision=reject capture=none curl_rc=22 http=403 words=0 quote=none
GATE-RECORD S235 url=https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4627914/fullTextXML fetched=2026-11-09T04:00:42Z tier=B decision=reject capture=none curl_rc=22 http=500 words=0 quote=none
