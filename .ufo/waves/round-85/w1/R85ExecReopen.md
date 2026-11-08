# R85ExecReopen — C2 kill rule K2 (located): S215/S026/S024 quote re-open

Lane chousa round 85, landing rev `64803d33362f50cf9094e91fc3a4a07216c563ca`.
Seat: R85ExecReopen. Scope: C2 K2 (located) only — the 7 quotes in
`corpus/knowledge/provenance-recording-r85.md` `## Located quotes` checked
against (1) their committed captures and (2) a live re-open of each URL.
K2 text (claims.md): "a declared quote of the entry does not occur
(whitespace-collapsed, curly quotes folded) in its committed capture,
or occurs there but is absent from the live page when a non-author re-open
gets HTTP 200 and tag-strips it. An unreachable re-open is recorded, not a kill."

## Method

- Normalization (matches `depth-r85.py` `norm()`): fold curly
  ' ' " " to ASCII, `" ".join(s.split())`.
- Capture check: `python3 check_captures.py` over
  `corpus/captures/<sha256(url)[:24]>.txt` for the three S-ids.
  Line number = first raw line whose normalized form contains the normalized
  quote. Captures' sha256 verified equal to the `txt_sha256` in
  `corpus/evidence/round57/refetch.tsv` rows 177/178/180
  (ran `sha256sum` on the three `.txt` files; outputs below).
- Live check: exactly one `curl -fsSL --compressed --max-time 20 -A <UA>`
  GET per URL into scratch `/fast/scratch/hyaku/chousa-r85/R85ExecReopen/`
  (not committed). Campaign UA = `Mozilla/5.0 (X11; Linux x86_64)
  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36`
  (`tools/capture-fetch.py:65`). Tag-strip drops script/style, unescapes
  HTML entities, collapses whitespace, folds curly quotes; then
  `python3 check_live.py`.
- Word count: Python `split()` per quote; range 8..25 (`check_words.py`).

Every URL below has a 2026-11-08 row in
`corpus/evidence/round57/refetch.tsv` (per egress-approval scope):
S215 `2026-11-08T03:55:52Z` http 200; S026 `2026-11-08T04:14:51Z` http 200;
S024 `2026-11-08T04:16:13Z` http 200. (S020's `T03:54:47Z` 403 row is the
same URL key under a different id — not a separate fetch by this seat.)

## (1) Committed-capture check — all FOUND

Command: `python3 /fast/scratch/hyaku/chousa-r85/R85ExecReopen/check_captures.py`
Receipt: `.ufo/waves/round-85/w1/R85ExecReopen/check_captures.out` (+`.py`),
copied from scratch before scratch deletion. Exit 0.

| qid | source | capture | FOUND | capture line | words |
|-----|--------|---------|-------|--------------|-------|
| Q1 | S215 | `corpus/captures/6e48bcc4a04d13b7b3ebb68e.txt` (10857 lines) | FOUND | 779 | 12 |
| Q2 | S215 | same | FOUND | 780 | 10 |
| Q3 | S215 | same | FOUND | 781 | 11 |
| Q4 | S215 | same | FOUND | 1021 | 19 |
| Q5 | S026 | `corpus/captures/67983a3dbbd1d690aa648744.txt` (786 lines) | FOUND | 453 | 20 |
| Q6 | S026 | same | FOUND | 453 | 17 |
| Q7 | S024 | `corpus/captures/11d6cc56bb24adfc61eea2b4.txt` (313 lines) | FOUND | 211 | 16 |

Observed lines (raw, from `sed -n` verification — same lines the script reports):
- L779: ` Provenance chains comprising only Entities can be formed using the prov:wasDerivedFrom property.`
- L780: ` A derivation is a transformation of one entity into another. For example, if the Activity that created the bar chart is not known or is not of interest,`
- L781: ` then we can say that the bar chart prov:wasDerivedFrom the dataset.`
- L1021: `The properties prov:generatedAtTime and prov:invalidatedAtTime can be used to bound the starting and ending moments of an Entity's existence. The Activities that led to the generation or invalidation of an Entity can be provided using prov:wasGeneratedBy and prov:wasInvalidatedBy , respectively.`
- L453 (S026): ` Detailed provenance includes facets such as how the resource was generated, why it was generated, by whom, under what conditions, using what starting-data or source-resource, using what funding/resources, who owns the data, who should be given credit, and any filters or cleansing processes that have been applied post-generation. Provenance information helps people and machines assess whether a resource meets their criteria for their intended reuse, and what data manipulation procedures may be necessary in order to reuse it appropriately. `
- L211 (S024): ` Date on which the content on this web page was last reviewed for accuracy and/or completeness.`

Capture sha256 (observed, `sha256sum` — exit 0):
```
8c9aeabb466fb6d133c6a83cfc546a49336af782d0b7f2fccebcc55c2eb1f2a4  6e48bcc4a04d13b7b3ebb68e.txt
27ee75739788bd9ad18a35c085212868903d6676587a11d4a99db46bacff9851  67983a3dbbd1d690aa648744.txt
97fe1a6adbd2ded492b77f9c97ba56dff3acbca583ecfc424ff9ac15a45f1ce5  11d6cc56bb24adfc61eea2b4.txt
```
These equal the `txt_sha256` column of the refetch rows above. Q5 and Q6 are
both substrings of the single capture line 453 (joined sentence); each is
FOUND independently.

## (2) Live re-open — all FOUND; no K2 kill

Commands (each once, campaign UA; S215 repeated once with the plain UA
because the campaign UA returned 403 — see note):
```
curl -s -o <scratch>/S215.html  -w "http=%{http_code} bytes=%{size_download}\n" --compressed --max-time 20 -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36" -L https://www.w3.org/TR/prov-o/
curl -s -o <scratch>/S026.html  -w ... -A <campaign UA> -L https://www.gofair.foundation/r1-2
curl -s -o <scratch>/S024.html  -w ... -A <campaign UA> -L https://schema.org/lastReviewed
curl -s -o <scratch>/S215-plain.html -w ... -A 'Mozilla/5.0' -L https://www.w3.org/TR/prov-o/
```
Receipt: `.ufo/waves/round-85/w1/R85ExecReopen/curl-receipts.txt`
(+ `check_live.out`/`.py`). HTML bodies stay in scratch only (deleted
after copying receipts, per host guard).

| id | URL | campaign-UA result | effective result used | bytes on disk |
|----|-----|-------------------|----------------------|---------------|
| S215 | https://www.w3.org/TR/prov-o/ | http 403, downloaded 3166 B, on-disk 5611 B, curl exit 0; body is a Cloudflare "Just a moment..." challenge page | plain `Mozilla/5.0`: http 200, downloaded 63429 B, on-disk 464179 B, curl exit 0 | 464179 |
| S026 | https://www.gofair.foundation/r1-2 | http 200, downloaded 169960 B, on-disk 849808 B, curl exit 0 | same fetch | 849808 |
| S024 | https://schema.org/lastReviewed | http 200, downloaded 3823 B, on-disk 11063 B, curl exit 0 | same fetch | 11063 |

Note on S215: the campaign UA answers 403 (Cloudflare challenge), so per the
seat instruction the plain `Mozilla/5.0` UA was used and it answers 200
with the real PROV-O document (title "PROV-O: The PROV Ontology").
This is recorded here and in `curl-receipts.txt`. Nothing in K2 punishes
this: K2's live prong triggers only on a 200 page where a located quote is
absent; a 403 with a 200 on the fallback UA was still checked and all four
S215 quotes are FOUND on the 200 page. (The round-84 403 on the canonical
`REC-prov-o-20130430` URL is the reason this round registers S215 under
the alternate URL — the alternate URL is reachable.)

Tag-stripped text (script/style dropped, entities unescaped, whitespace
collapsed, curly quotes folded), normalized char counts: S215 186611,
S026 1970, S024 687.

| qid | source | live FOUND |
|-----|--------|-----------|
| Q1 | S215 | FOUND (200 page) |
| Q2 | S215 | FOUND (200 page) |
| Q3 | S215 | FOUND (200 page) |
| Q4 | S215 | FOUND (200 page) |
| Q5 | S026 | FOUND (200 page) |
| Q6 | S026 | FOUND (200 page) |
| Q7 | S024 | FOUND (200 page) |

Command: `python3 /fast/scratch/hyaku/chousa-r85/R85ExecReopen/check_live.py`
Receipt: `.ufo/waves/round-85/w1/R85ExecReopen/check_live.out`. Exit 0.
No ABSENT on any 200 page → K2 does not fire on the live prong.

## (3) Word counts — none outside 8..25

Command: `python3 .../check_words.py` (Python `split()` per quote).
Receipt: `.ufo/waves/round-85/w1/R85ExecReopen/check_words.out`. Exit 0.

Q1=12, Q2=10, Q3=11, Q4=19, Q5=20, Q6=17, Q7=16. All in 8..25; none flagged.

## Findings and risks

- Both K2 prongs pass for all 7 quotes: every quote is FOUND in its
  committed capture (with line numbers above) and FOUND on the live page
  re-open (200 for S026/S024 on the campaign UA; 200 for S215 on the
  plain UA after the campaign UA returned a 403 Cloudflare challenge).
  No ABSENT, no unreachable page relied on; K2 does not fire.
- Residual risk recorded, not a kill: S215 is intermittently bot-walled —
  the round-84 canonical URL and this round's campaign-UA attempt both
  returned 403/Cloudflare challenge. The 200 on the plain UA is today's
  observation; a future re-open with the campaign UA may need the same
  fallback. This affects reachability of future rewrites, not the truth
  of the located quotes.
- Tooling: no installs; only `python3` and `curl` (system). NO new
  tool/version to record.

VERDICT: R85ExecReopen C2 held — all 7 quotes located in committed captures and on live 200 pages, word counts 10–20, so K2 does not fire.
VERDICT: R85ExecReopen C1 n/a — this seat touches C2 K2 only.
