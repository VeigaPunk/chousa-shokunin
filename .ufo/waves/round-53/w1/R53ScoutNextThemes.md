# R53ScoutNextThemes — themes B and C re-check, ranked for round 54 (no draft)

Method: python over the read-only package `/home/vgpnk/Projects/shokuknow/merge/chousa/` (rows in `SOURCES.append.md`, entries in `knowledge/`, `amendments/`), the capture cache `.qcache` (key = first 24 hex of sha256(URL)), and the lane at HEAD `6365f15` (`git -C` not mutated; reads only). Lane-held test = the census `url_of` (copied from `tools/assimilate-rows.py:134`, same as `scripts/sources-census.sh:600`) applied to the SOURCE cell of every lane `SOURCES.md` row, plus any URL anywhere in a row. Lane registry ends at S116 (116 rows); round 53 takes S117–S121, so a round-54 theme starts at S122. No fetch, no write outside this file (scratch driver was in `/fast/scratch/hyaku/chousa-r53/R53ScoutNextThemes/`, removed at the end).

## 1. Capture, held-URL and term check (observed)

| staged id | URL (short) | key | cache files (bytes) | lane Registry row on URL | URL in lane knowledge |
|---|---|---|---|---|---|
| S137 | web.archive.org/web/timemap/link/…/list_1.pdf | `9c28bfe4` | txt 713, raw 713 | none | no |
| S138 | web.archive.org/web/20260418151432/…/list_1.pdf | `c280fdf8` | txt 10106, raw 343301 | none (the ORIGINAL URL appears in S116's row, `anyhit S116`; the original's own key `f3dbe2fe` is `.fail` 6 B) | yes — `japanese-prisma-item-wording-r40.md:25` names this exact URL and key |
| S146 | web.archive.org/cdx/search/cdx?url=…&output=json | `32401404` | txt 488, raw 488 | none | no |
| S085 | std.samr.gov.cn/gb/search/gbDetailed?id=4507… | `adf6ba93` | txt 6626, raw 76252 | none | no |
| S086 | openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE… | `b9ca2a4f` | txt 24185, raw 24185 | none | no |
| S093 | xuebaobangong.jmu.edu.cn/…/64b9ba1b-….pdf | `0f33243f` | txt 190614, raw 6209520 | none | no |
| S101 | jc.hit.edu.cn/…/1f6f2731-….doc | `6dc68fd6` | txt 157816, raw 129024 | **S101 (held)** | yes (`citation-count-semantics-r37.md`) |
| amend. S084 / S094 / S095 / S096 | rfc7089 / warp.ndl.go.jp/en/info/qanda / current.ndl.go.jp/e2867 / portico.org | `d0c4a09a` `5f54e82c` `0034b800` `226e5818` | all have txt | rfc7089, warp, current.ndl held (count 1/2/1); portico **0** | — |

(`python3 chk.py` output rows; the `.txt` of every B and C capture exists and decodes as UTF-8.)

Distinctive-term sweep of `git grep -il -- TERM -- corpus/knowledge corpus/SOURCES.md` at HEAD:
- B: `timemap` 0, `cdx` 0, `77FLJAP2` 0, `Wayback` 0 — hits only for `20260418151432`, `ba9bc9c1` (`japanese-prisma-item-wording-r40.md`), `memento` (RFC 7089 entries + S116 row), `list_1.pdf`/`lifescience` (S116, the r38 amendment).
- C: `GB/T 7714` 3 files (`citation-count-semantics-r37.md`, `citation-version-binding-r36.md` — which says "Staged S082 … is not adopted" line 21 — and SOURCES), `7714-2025` 1 file (that same sentence), `ISO 690` 2 files, `文献标志码` 2 files (the S101 content); `文献类型标识`, `本文件不适用于图书馆员`, `采标`, `不提供文本阅读`, `openstd`, `std.samr`, `附录A`, `carrier code` all **0**.

## 2. Theme B — archived-translation-currency-r41 (S137, S138, S146)

- **Capture:** all three readable. `sha256sum` of `c280fdf8….raw` and `e84bfe97….raw` (S116's capture) both `ba9bc9c14cd0b89f9de559f20b074398333c67ed86c0b5d6ffd64c0118399732`; `cmp` of the two `.txt` prints `txt-identical`. The timemap text lists `rel="first memento"` at char 486 (20250218234744) and `rel="memento"` at char 657 (20260418151432, `datetime="Sat, 18 Apr 2026 15:14:32 GMT"` char 672). The 2025-02-18 memento URL's key `7149f8ef` has **no** cache file — only the 2026 memento and the 2024-timegate capture are on disk.
- **New fact found here (not in the staged entry):** `base64.b32encode(sha1(c280fdf8….raw))` = `77FLJAP2BJCPHEZR6LAWRPWKM2BUBH4J` (run; 343301 bytes) = exactly the CDX digest of **both** S146 rows. So the CDX digest ties both archive rows to the bytes held in S116, rather than to a size match. CDX `length` differs (296572 vs 300917) while digest is equal — a WARC-record length, not payload size; an entry should not read it as a size disagreement.
- **Province fit:** in (version binding; sits next to `citation-version-binding-r36/r37`), low risk.
- **New vs lane:** modest. `japanese-prisma-item-wording-r40.md:25` already records the 2026-04-18 memento, its key, the identical sha256, and "whether the publisher has revised … is open". New: S137 and S146 as the closing index evidence (two mementos; two CDX rows, same digest) — i.e. two documents. S138 is a second URL for bytes the lane already holds (S116 holds them), so under the claims' rule "a document a lane entry already holds earns none" its credit is doubtful.
- **Quote locations ready (raw `.txt`, one line each, exactly once):** S137 `rel="first memento"` char 486, `rel="memento"` char 657; S146 `"200","77FLJAP2BJCPHEZR6LAWRPWKM2BUBH4J","296572"` (49 chars) char 231 and `…","300917"` char 436 (the bare digest occurs twice, so the quote must carry the length cell). Tiny captures give few distinct quotable lines: a ≥3-quotes-per-document target is tight for S137/S146.
- Ids/URLs held by a lane row: none of S137/S138/S146 by URL; S138's original URL is inside S116's row.

## 3. Theme C — GB/T 7714 source-type r36/r37 + amendments

- **Capture:** S085, S086, S093 all present and readable. Located: S086 `本系统不提供文本阅读服务` 1× char 15223; S085 `采标情况` 1× char 1787, `ISO 690` char 1813, `非等效` char 1800; S093 `本文件不适用于图书馆员、文献目录编制者以及索引编制者著录参考文献。` on one line (line span 5595–5635 → char 5602 is the start of the quotable sentence), once.
- **Quote-form hazards (observed):** S093's text form is **fullwidth** (`ＭＴ`, `附录Ａ`, `“预印本”… 代码“ＰＰ”`; `MT` count 0, `表A.1`/`表A.2` count 0), and PDF-wrapped (`……其标识\n      代码“ＰＰ”`): the entry's ASCII codes (M, PP, MM) are NFKC-folded, so located quotes must be copied in fullwidth form and cut at line breaks. S085's text puts the dates as `发布 于 2025-12-02` / `实施 于 2026-07-01` on separate lines: the quote `标准号：GB/T 7714-2025 发布日期：2025-12-02 实施日期：2026-07-01` is **absent** (0 raw, 0 collapsed).
- **Register risk (read of `absent-defect-register.md`, no campaign tool run):** two `payload-absent` rows sit on theme-C URLs — register line 38 (`chousa` round1 S080, the SAMR detail URL, exactly the quote above) and line 42 (`chousa` round2 S088, the jmu PDF, the fullwidth carrier-code quote). Under a C2-style claim ("a re-check verdict line for each absent-defect row on a theme URL") C would start with 2 such rows; the verdicts there are likely `absent` for the register's own quotes while the entries' own sentences can be located — a verdict line is required, not a free pass.
- **Province fit:** weaker than B. The standard's scope clause (authors, not librarians/indexers) and the type-vs-tier axis serve "source hierarchy" only by analogy; no search-conduct claim. PROVINCE.md owns source hierarchy and search-strategy taxonomy; a citation-format standard is adjacent, so each entry would need the Gate to argue province.
- **New vs lane:** larger than R52ScoutPackageRest §4 assumed. The lane has no row for the SAMR record, openstd notice or the jmu copy, and no text for the scope clause, the Appendix A type/carrier codes or the 7714-2025 version pivot; only the ISO/GB-T split in `citation-count-semantics-r37.md` (S101, already held) overlaps. The r37 entry cites S101, which is lane-held — an adopter v4 `held` row, no new id. Three wholly new documents (S085, S086, S093).
- **Amendments:** `citation-version-binding-r36.md` (S084 RFC 7089 held, S085) and `-r37.md` (S094 warp held, S095 current held, S096 portico.org **not held**, key `226e5818` txt 4205) append to existing lane files (the r36 lane file line 21 already says "Staged S082 … is not adopted" — a flip it itself names: "a text capture of that record contains the issued and effective dates as a contiguous span", which S085's txt does not give as a contiguous span, see above). Amendment text is therefore a separate adoption-by-append path, not a new-file entry.

## 4. Ranking for round 54

1. **C first** for depth: three documents with zero lane footprint (term sweep above), richest new claims (scope clause; 17 types / 5 carriers; version pivot 2015→2025; "authoritative on identity, unreadable on content"). It meets a "≥3 of N bound" shape only with all three of S085/S086/S093, so the tight-quote hazards (fullwidth, wraps, S085 dates split) and the 2 register rows must be written into the frozen counter before data. Province argument needed in the Gate.
2. **B second:** lowest risk and best fit, but only two documents earn expansion credit (S137, S146; S138 re-keys held bytes), the ground is mostly a closure of the open item at `japanese-prisma-item-wording-r40.md:25`, plus my digest finding above. It cannot meet a ≥3-document bound; better as a companion paragraph/entry inside a round that also lands C, or as an operability-friendly small claim.
3. If both: B's amendment-free entry plus C's two entries, ids from S122; S101 `held`, S096 (portico) the only unheld amendment source.

VERDICT: re-checked B (S137/S138/S146) and C (S085/S086/S093 + S101 + amendments) against capture, province, lane terms and held URLs — all captures readable, no lane Registry row holds any of S137/S138/S146/S085/S086/S093 by census URL; C ranks above B for round 54 on new ground (3 new documents, term sweep 0) with named quote-form and register-row hazards, B is lower risk but earns credit for 2 documents at most.
