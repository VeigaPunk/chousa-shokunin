# R57W1ReviewRows — registry-row contract review for the rows R57-C3 will add

Reviewed: `corpus/SOURCES.md` (lane tip), `/home/vgpnk/Projects/shokunin/CORPUS.md` §"SOURCES.md contract v1"
(frozen), `corpus/evidence/round57/c3-count.py` (frozen counter — what it actually enforces on a row),
`corpus/lessons/round-56.md`, and `git show` of round-56 commits `99eff0e`/`9897707` on SOURCES.md.

## 1. The 11-column shape and enum values each new row must carry

Row grammar (contract §Shape): `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`
— 11 cells ⇒ `awk -F'|' … NF==13`; no `|` inside any cell (a bare `|` breaks the row; the S116 row shows `-` and `/`
are used instead).

- `id` — `S` + ≥3 digits, next unused, never reused. S001–S130 exist; the first free id is S131
  (`grep -cE '^\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` → 130; census printed no duplicate ids).
- `source` — title — canonical URL or DOI. c3-count.py:107 `first_url` takes the *first* `https?://` of this
  cell; that URL U is what the entry must cite (`source: X — U`), what `refetch.tsv` must record, and what
  `key(U)=sha256(U)[:24]` names under `corpus/captures/`.
- `kind` — enum: `spec docs paper code tool dataset talk book community own-work`. Precedent for C3-style
  documents: Chinese guideline/notice copies are `docs` (S118, S124, S127-S130), journal articles `paper`,
  standards-record pages `docs`.
- `tier` — `A`/`B`/`C`, scoped to `scope`, never global; `community` is never A.
- `scope` — the claim/topic the tier applies to. Must be narrow and carry an explicit negative bound (§4 below).
- `anchor` — exact section/line/char offsets + revision; never a bare homepage. c3-count.py:250-253 adds a hard
  requirement for a *new bound row*: `CHAR_RE.findall(r[5])` must be non-empty and every `char N` must be a
  located quote offset of that id in `corpus/evidence/round57/c3/spans.tsv` (`ANCHOR_BOUND`). So at least one
  `char N`, and no `char N` that isn't a manifest quote offset.
- `teaches` — one grounded learner benefit; rejected rows read `REJECTED: <reason>; flip: <…>`.
- `status` — enum `queued|mined|rejected`. c3-count.py:210: a row new since BASE_REV must be `mined`;
  a mined row needs `used-by` naming ≥1 path.
- `opened` — ISO date the row's author opened the source. For a new row this must be `2026-10-27` (counter
  constant `OPENED`, c3-count.py:45). Do not copy a campaign-cache access date into `opened`.
- `recheck` — ISO date or cadence `90d`/`180d`/`365d`/`on-release`.
- `used-by` — comma-separated repo-relative paths or `—`. For a bound row it must contain the exact entry path
  `corpus/knowledge/normative-reference-chain-china-r57.md` (c3-count.py:197 splits on `,` and compares the
  stripped cell — so comma+space formatting is required, no `;`).

## 2. used-by in-place change rule

Contract rule 2 (frozen, CORPUS.md): *"Only `status`, `recheck` and `used-by` change in place, and each change is
logged old→new in the round lesson. A correction is a new row whose `teaches` opens `supersedes S0NN —`."*

What C3 needs touched: **S127** `used-by` must gain the new entry (c3-count.py:194 `used_by(s127)`), and **S118**
(held, binds R7) must also name it. S118's current cell (SOURCES.md:128) quotes:

`corpus/knowledge/quality-control-guideline-issued-text-r48.md, corpus/knowledge/western-instrument-alignment-r50.md, corpus/knowledge/grey-literature-field-china-r42.md`

S127's current cell (SOURCES.md:137): `corpus/knowledge/grey-literature-field-china-r42.md`. Precedent for the log
line — `corpus/lessons/round-56.md:41`:

> `Row touched: S118 `used-by` old `…quality-control-guideline-issued-text-r48.md, …western-instrument-alignment-r50.md` → new `…, corpus/knowledge/grey-literature-field-china-r42.md`; its status (`mined`) and recheck unchanged.`

The round-57 lesson must carry the same `old … → new …` line for each row touched.

## 3. Gate requirements per new row

Contract rule 1: *"A row is a claim. Write it only after opening the source in the round that writes the row. The
round lesson's `## Gate` records, for every new row, the URL, the access date, and a ≤25-word quote with its
location grounding `teaches`."* Round-56 shape (lesson lines 36-39) is the template:

`- S127 — https://www.ttbz.org.cn/upload/file/20250407/…pdf — accessed 2026-10-27 — `（9）灰色文献：…能够研究` (char 24624).`

Per new row: URL · access date `2026-10-27` · one quote ≤25 whitespace-words with its `char N` location.
C3 additionally makes every bound row's manifest row `≤25 words and ≤160 chars` (c3-count.py:243 `short`) and
requires ≥2 manifest rows per bound id, one quote containing the reference title (c3-count.py:220-225).

## 4. Three tier/scope honesty checks a B-tier row for a Chinese regulatory document must pass

From the contract + the round-56 rows' own reasoning:

- **Tier follows the carrier, scope names the authority chain.** Issuer ≠ host ⇒ B, with the reason written in
  scope: S118 "the document is the centre's but the carrier is a professional society's file host, so the tier
  is B"; S124 "a third-party host's copy … so tier B"; S123 "a university journal office's upload … so tier B".
  Tier A is reserved for the issuer's own record (S121/S122 samr.gov.cn record pages; S126 NMPA english site).
  Watch S130: hosted on nhc.gov.cn yet still B — the *unestablished relation to the 2021 guideline*, not the
  carrier, drove B. An issuer-hosted copy is not automatically A when the row can't establish which edition it is.
- **Scope names what the document is authoritative FOR — a narrow claim, never global — and carries an explicit
  "never for" bound matching the document's status.** S127: "for the draft's wording only, never for an issued
  standard" (征求意见稿, placeholder T/CLPA XXXX—2025). S124: "never to the issued guideline's legal force".
  S129: "tier A for the published wording, not for the group standard's issued status". A new bound row's scope
  must not imply more than the copy states — e.g., a draft-for-comments copy must never scope to the issued
  standard.
- **Pin the edition token; state the sibling-edition relation or admit it is unestablished.** S130 scopes itself
  to the 2020 text with "the relation to the 2021 管理指南 named elsewhere is not established". C3's heading/token
  rule encodes exactly this: S130 cannot bind R3 because it lacks the `2021年版` token (claims.md). A new row for
  e.g. R4-R6 must hold its `2022年版` token in the defined text form and scope to that edition only.

## 5. Defect candidates in round-56 rows

Census on the live registry (lane root, 2026-10-27): rows=130, malformed=0, tier `A=106 B=19 C=5`, status
`mined=106 queued=19 rejected=5`, no duplicate ids, no enum violations, no missing mined `used-by` paths —
frozen census block, CORPUS.md. Round-56 rows proper (S127-S130, added `99eff0e`) are shape-clean.

- **DEFECT CANDIDATE — S129 `scope`/`anchor`/`teaches` rewritten in place at `9897707`.** Cell diff
  `99eff0e→9897707` changed cells 4, 5, 6 (`表 10`→`表7` correction; verified by the python `git show` cell diff
  above). Contract rule 2 allows only `status`/`recheck`/`used-by` to change in place; corrections are new
  `supersedes` rows. The round-56 lesson records it only as `## Mistakes` row 3 (line 11), not as a row-touched
  or superseding row. Intra-round correction, so low severity — but the same mistake on a C3 bound row this
  wave would be a shape violation under the frozen rule.
- S118's round-56 `used-by` edit (cell 10 only) is rule-conformant and logged at lesson line 41. No defect.
- Residual: S127-S130 `opened=2026-10-27` matches the commits' date and the "opened in the round that writes the
  row" rule; checked, conformant.

Bounds: leaf member — no dispatch. No scratch dir was created (read-only audit; the counter was read, not run,
and not modified). No tool installs; pacman untouched. A transient `/tmp/r57rows_*.txt` (<50MB) was deleted.
No network fetches.

VERDICT: attacked the R57-C3 row shape against the frozen SOURCES v1 contract and `c3-count.py` — the 11-column
shape, enums, `used-by` in-place rule, Gate record, and three B-tier honesty checks all survive with one
defect candidate (S129's round-56 in-place `scope/anchor/teaches` rewrite); reported, not patched.
