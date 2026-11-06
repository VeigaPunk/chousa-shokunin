# R81ExecReopen — C1 kill rule K2: every counted quote line re-opened live

Seat: attack, read-only. Landing attacked: `7e2da96a0541946e796384d42fea18e09ede9e9f`.
Frozen rule attacked: C1 K2 (`corpus/evidence/round81/claims.md`) — "a live re-open of any counted quote
(`tools/quote-reopen.py verify` for the HTML rows; one curl GET plus `pdftotext` for S203) reports `ABSENT`".
Receipts: `.ufo/waves/round-81/w1/R81ExecReopen/` (six files, listed per finding). Scratch
`/fast/scratch/hyaku/chousa-r81/R81ExecReopen/` created with `mkdir -p` and removed before yield.
No production file, capture, `refetch.tsv`, registry row, counter, fixture or receipt was written or amended.

## Result: K2 did not fire. All 14 counted quote lines re-open live.

### 1. The counted set is exactly 14 lines, and it is the set the counter counts

Command (from `/home/vgpnk/Projects/shokunin/chousa-shokunin`):

```
git show 7e2da96a0541946e796384d42fea18e09ede9e9f:corpus/knowledge/citation-searching-tarcis-r81.md > cit.md
git show 7e2da96a0541946e796384d42fea18e09ede9e9f:corpus/knowledge/correction-retraction-status-r81.md > corr.md
python3  # apply the counter's own regex, depth-r81.py line 52:  ^>\s*"([^"]+)"\s+—\s+(S\d{3,})\s*$
```

Observed: `TOTAL=14` — S203 ×7, S204 ×2 (`cit.md`), S205 ×2, S206 ×2, S207 ×1 (`corr.md`). Seat item expected 14.
Receipt `quote-extract.txt` (all 14 lines with source id, word count and full text).

Coverage cross-check (not a C1 K1 score — K1 belongs to another seat): the counter run on the landing tree prints
`DEPTH_R81 entries=2 fresh_rows=5 located_quotes=14` / `DEPTH_R81=PASS`, rc=0. `located_quotes=14` equals the 14 lines
above, so the re-open covers every line the counter counts, not a subset. Receipt `counter-coverage.txt`.

### 2. HTML rows S204, S205, S206, S207 — 7 items, all VERBATIM

Command (from `/home/vgpnk/Projects/shokunin/chousa-shokunin`, items TSV `id<TAB>source_id<TAB>quote` in scratch):

```
python3 tools/quote-reopen.py verify --items /fast/scratch/hyaku/chousa-r81/R81ExecReopen/items-html.tsv
```

Observed, every line:

```
QUOTE_REOPEN	q2	VERBATIM	matched in normalized page text
QUOTE_REOPEN	q3	VERBATIM	matched in normalized page text
QUOTE_REOPEN	q10	VERBATIM	matched in normalized page text
QUOTE_REOPEN	q11	VERBATIM	matched in normalized page text
QUOTE_REOPEN	q12	VERBATIM	matched in normalized page text
QUOTE_REOPEN	q13	VERBATIM	matched in normalized page text
QUOTE_REOPEN	q14	VERBATIM	matched in normalized page text
QUOTE_REOPEN_SUMMARY verbatim=7 absent=0 too_long=0 no_source=0 unreachable=0
```

Exit code 0 (recorded at run time). `absent=0`, `unreachable=0`. Receipt `reopen-html.txt` (command, items TSV, full
stdout, rc). Note `q14` (S207) is exactly 25 words — at the counter's limit, not over it.

### 3. PDF row S203 — 7 items, all present under both `pdftotext` modes

```
curl -fsSL --compressed --max-time 30 -A 'Mozilla/5.0 (X11; Linux x86_64)' -o s203.pdf <S203 URL>
  -> http=200 size=1061064 curl rc=0
sha256(s203.pdf) = eea13440d89c7b273709a7e8e6a3ad009066eb766a89e978486bebf51583debd
pdftotext s203.pdf s203-nolayout.txt          ; rc=0 ; sha256=a4b2be64… (173013 chars)
pdftotext -layout s203.pdf s203-layout.txt    ; rc=0 ; sha256=31493aa6… (190444 chars)
```

* Live PDF sha256 **equals** committed `corpus/captures/f2489455cc311a4de981e926.raw`
  (`eea13440…`, 1061064 bytes) and **equals** the `refetch.tsv` S203 `raw_sha256` row for 2026-11-06T18:44:29Z.
* Live `pdftotext -layout` output is **byte-identical** to the committed
  `corpus/captures/f2489455cc311a4de981e926.txt` (`31493aa6…`, 190627 bytes) — i.e. the counter's grounding text is
  exactly what the URL serves today, and the committed `.txt` is the `-layout` extraction, not the default one.
* Quote presence after whitespace collapse (NFKC + quote folding), both modes: **7/7 PRESENT, 7/7 PRESENT**.
  `nolayout` and `layout` agree on every one; a de-hyphenation variant was also computed and agrees.

Receipt `reopen-s203.txt` (GET result, both hashes, both `cmp` outcomes, per-quote table).

### 4. Live bytes vs committed captures for all five rows (a difference is a finding, not a failure)

One `curl` GET per HTML row, sha256 compared to the committed `.raw`:

| row | live sha256 | committed `.raw` | verdict |
|---|---|---|---|
| S203 | `eea13440…` | `eea13440…` | IDENTICAL |
| S204 | `204fcde1…` | `20c27fd2…` | **DIFFERS** |
| S205 | `7f2ca105…` | `7f2ca105…` | IDENTICAL |
| S206 | `5537d03b…` | `4c73b648…` | **DIFFERS** |
| S207 | `e518a644…` | `e518a644…` | IDENTICAL |

Both differences are **per-request tokens only, at identical byte length**:

* S204 (387054 bytes both): 88 differing bytes in two runs — `<meta name="ncbi_phid">` session id (offset 4060) and a
  `csrfmiddlewaretoken` hidden-input value (offset 357863). No article text differs.
* S206 (22898 bytes both): 26 differing bytes in three runs — Cloudflare `window.__CF$cv$params` `r`/`t` values in an
  inline challenge script (offsets 21952–22193). No page text differs.

Because the article text is unchanged, all seven HTML quotes still verify VERBATIM against today's live pages (§2).
Receipts `sha-compare.txt` (full table) and `drift-s204-s206.txt` (the differing spans with context).

All five committed `.raw` and all five committed `.txt` match their `refetch.tsv` 2026-11-06 rows on both hash columns —
the captures are faithful to their fetch record; the drift is the live page's, not the capture's.

## Deviation disclosed

`corpus/evidence/round81/egress-approval.md` seat row allows "`tools/quote-reopen.py verify` **or** a single curl GET".
This seat's item (4) requires both a verify run and a curl GET per HTML row for the sha256 comparison, so each of the
four HTML URLs received **two** GETs (one by the tool, one by curl), and S203 received one. All GETs: `-fsSL
--compressed --max-time 30`, campaign UA, no POST, no cookies, no credentials, no redirect off the registry URL, bytes
into scratch only. Nothing written to `corpus/captures/` or `refetch.tsv`. Total: 5 URLs, 9 GETs.

## Risks (for the closure, not findings against the landing)

1. **S204/S206 can never be byte-identical again.** Any future check that compares a live `.raw` to
   `c52a1f15884a78028febcf43.raw` or `f221c90f69188f775e32cd34.raw` will fail on session tokens, not on content. A
   later seat that reads such a mismatch as capture drift would be wrong; the `.txt` surface is the stable one.
2. **The counter grounds on `.txt`, not `.raw`** (`depth-r81.py` `located()` opens `corpus/captures/<key>.txt` and
   requires its sha256 to equal the refetch `txt_sha256`). That is consistent here for all five rows, but it means a
   `.raw` that drifted while its `.txt` stayed fixed would be invisible to C1. For S203 I closed that gap directly
   (live `-layout` output == committed `.txt`); for the HTML rows I verified quote presence in live text, not byte
   equality of a re-extraction, because `capture-fetch.py`'s HTML-to-text step was not re-run (it would write a
   capture, which this seat may not do).
3. **S207's quote sits exactly on the 25-word limit.** One added word turns it into `P2-quote-words=26`; the margin is
   zero. Not a defect at this revision.
4. S203 is the accepted manuscript, not the version of record, and the entry says so; the correction (S208) remains
   unreadable (HTTP 403, rejected row). K2 says nothing about that, and this seat did not fetch bmj.com.

## Blockers

None. No tool installed; `pdftotext` (poppler 26.10.0) and `python3` were already present. No pacman transaction.

VERDICT: R81ExecReopen C1 held — K2 did not fire: all 14 counted quote lines re-opened live, 7 VERBATIM via `tools/quote-reopen.py verify` (rc 0, absent=0) and 7 PRESENT in the live S203 PDF under both `pdftotext` modes, with the live PDF byte-identical to its committed capture and refetch record.
VERDICT: R81ExecReopen C2 n/a — not touched by this seat.
