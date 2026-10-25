# R51ScoutCoverage — coverage-map ground check for the Japanese/Chinese search-record theme

Base `9ec1751a…` (README.md byte-identical at base and HEAD `cfe6c9f`: `cmp <(git show HEAD:corpus/README.md) <(git show 9ec1751…:corpus/README.md)` → no output). All line numbers are `corpus/README.md` (1083 lines) unless noted. Read-only; scratch deleted.

## 1. The grep: the base holds no 検索式 / 検索期間 / 检索策略 in any lane corpus file

```
$ git grep -n -I -E '検索式|検索期間|检索策略' 9ec1751… -- corpus tools PROVINCE.md SCORECARD.md SHONEN.md LOG.md | wc -l
0
$ git grep -l -I -E '検索式|検索期間|检索策略' 9ec1751… -- .
.ufo/waves/round-48/w2/QuarantineS104.md   (検索式 :20,:37,:72)
.ufo/waves/round-48/w2/QuarantineS111.md   (检索策略 :9 — a quote-lint record line, not entry text)
.ufo/waves/round-48/w2/QuarantineS112.md   (检索策略 :23,:44,:68)
.ufo/waves/round-48/w2/QuarantineS120.md   (検索期間 :43,:46,:54)
.ufo/waves/round-48/w2/QuarantineS125.md   (检索策略 :28,:29; 灰色文献 :30,:34,:40)
.ufo/waves/round-50/w1/ExecAdopt.md        (検索式 :41, a recheck line quoting S104)
```
So: 0 hits in `corpus/`, `tools/`, `PROVINCE.md`, `SCORECARD.md`, `SHONEN.md`, `LOG.md`. The only hits are round-48/50 wave work logs (quarantine of staged rows, recheck notes) — those are scratch evidence about candidate quotes, not held ground. Companion terms in `corpus tools PROVINCE.md SCORECARD.md SHONEN.md` at base, `git grep -c` files/lines: 检索式 0, 检索时限 0, 灰色文献 0, 医中誌 0, Ichushi 0, SinoMed 0, JAOHFA 0, NIPH 0; `PRISMA-S` 10 files/11 lines (all id-arithmetic or the rejected r36 candidate — table below); `J-STAGE` 16 files/30 lines (citation-link rows, §3).

## 2. Theme part → coverage verdict

| Theme part | Verdict | Where it touches (path:line) |
|---|---|---|
| Searcher / date / expression (誰が・日時・検索式) | **NEW GROUND** on the content; adjacent ground held | held neighbours: `knowledge/search-log-method-r39.md:1-40` (a log is a document the searcher controls; S078 Bramer 2018, byte 17383) and `SOURCES.md:88` (S078), `SOURCES.md:27` (S017 PRISMA 2020, "report searches with flow counts"). No held entry names searcher identity or an expression field in any language. Staged S109/S110 are the first sources the lane would hold. |
| Database, provider, window (DB名・プロバイダ・期間) | **NEW GROUND** | zero hits for 検索期間/检索时限 in the held corpus. The held `search-log-method-r39.md` says nothing about provider or window. Staged S126 (database + provider + start/end date, reason = currency) and S125 (検索期間 fixed at one point) are first. |
| Chinese reporting module incl. grey literature | **NEW GROUND** | 灰色文献 0 hits in the held corpus; "grey literature"/"gray literature" 0 at the base tree. Capture check: S116 `.txt` (fd468a36d78ff156b6200946, UTF-8) has 灰色文献 at char 15310 (module-3 item `（3）灰色文献的检索与记录`, count 3), 注册平台 at 30207, 会议 at 24113; S117 has 检索策略 ×2 (first at 11428) and no 灰色; the entry `chinese-search-record-r39.md` states grey literature at lines 17, 46-53, 81. |
| Chinese reception of PRISMA-S | **NEW GROUND** (PRISMA-S named at base only for id arithmetic; reception never held) | base PRISMA-S hits are `knowledge/search-log-method-r39.md:27`, `knowledge/citation-version-binding-r36.md:28`, `lessons/round-43.md:27,43`, `lessons/round-44.md:167`, `lessons/round-44-verifier-spotcheck.md:100`, `lessons/round-45.md:131`, `lessons/round-46.md:253`, `lessons/round-47.md:252`, `lessons/round-47-verifier-spotcheck.md:49`, `lessons/round-50.md:16` — all say "which staged id is the DOI". S119 `.txt` (42bac8830527d6f1bb125c49) has PRISMA-S ×6 (first char 38); it is the bibliographic record, not the item's text (entry `chinese-search-record-r39.md:71`, "full text remains unopened"). |

## 3. Coverage-map rows the theme touches

Held (adjacent, not the same ground):
- `SOURCES.md` row — README:54 (registry; S078 at `SOURCES.md:88`, S017 at `:27`).
- `knowledge/archived-export-intake.md` — README:8 (record-shape specimen; no search fields).
- `knowledge/aggregator-vs-source-r36.md` — README:1071 (J-STAGE S097/S098, CiNii S096): Japanese citation-index facts, not a search record. Same hosts as S109 (`jstage.jst.go.jp`) — a different document.
- `knowledge/citation-version-binding-r37.md` — README:1062 (NDL WARP, non-Western version anchor).
- `knowledge/citation-count-semantics-r37.md`, `cnki-citation-check-r40.md`, `citation-matching-semantics-r41.md`, `istic-citation-verification-r39.md` — README:1072, 1076-1078 (CNKI/ISTIC citation checking: Chinese, but citation counts, not searching).
- `knowledge/claim-support-test-r37.md` — README:1067 (CFEVER, Chinese-Wikipedia claims; support relation, not search).
- PROVINCE: `PROVINCE.md:7` lists "search-strategy taxonomy" under Owns — the theme is in province (deep-research method), not a refusal.

Not in the map but relevant (map defects found): `grep -c 'search-log-method\|lessons/round-43' corpus/README.md` → **0**. `knowledge/search-log-method-r39.md` and `lessons/round-43.md` both exist at base (`git ls-tree`) and are unindexed; the nearest held entry to this theme has no coverage row. Adopting the theme should add its row AND an index row for `search-log-method-r39.md` so the three new rows do not sit beside an invisible neighbour.

## 4. `## Frontier` (README:348-1040) and dispositions (863-1083)

- The Frontier section's items are gate/counter/receipt debts (README:350-1040: claims, chain, boundary, sweeps, manifest append, argv spans, pins, receipts). `awk` over lines 348-1083 for `search|Japan|Chinese|CNKI|PRISMA|grey|J-STAGE` hits only 871 (Cochrane as design analogy), 1067-1078 (the held rows above). **No Frontier item or disposition names the search record.** The theme advances no *listed* frontier item; it is new ground outside the Frontier's debt list.
- It **does** advance a registered round-43 refusal: `lessons/round-43.md:43` — rejected `search-log-fields-r36.md` (the three-literatures candidate), "Flip: the fetch-scope ruling is answered and a capture of each cited source contains the quoted sentences"; echoed at `SOURCES.md:279` and `lessons/round-47.md:252`. The seven on-disk captures (each cited source's own capture, no fetch) are the flip's second half — satisfiable without the L0 ruling (README:953,970,988,1015 carry the fetch-scope question open). The flip text says "the fetch-scope ruling is answered **and** …" — reading it as met by on-disk captures alone needs the stated reading in the adoption Gate, not silence.
- Related frontier-adjacent carry: round-43's second rejection `search-tracking-record-r40.md` (`lessons/round-43.md:44`, flip: a rendering where "should be reported in Column 2" is contiguous) — untouched by this theme; staged `search-tracking-record-r40.md` is NOT among the three entries. Also not among them: staged `search-log-fields-r36.md`, `chinese-search-log-r37*.md`, `grey-literature-*.md`, `chinese-prisma-s-access-r41.md`, `prisma-s-*.md` (`ls …/knowledge/corpus/knowledge/`). The C2 claim covers only the three; the rest stay out of this round's credit.

## 5. Gaps against the C2 reading

- `chinese-search-record-r39.md:55` (S097) and amendment `:50` (S097), `:56,:72` (S105, S106), `japanese-search-record-r38.md:54` (S105) are body-only ids. At the lane registry, S097 = J-STAGE publisher page (`SOURCES.md:107`), S105 = CNKI 管理员 manual (`:115`), S106 = 子账号 manual (`:116`) — wrong documents; drop or name by path. Notably amendment `:56` calls S105 "Round 4's Chinese reporting module (`S105`)" — in the lane, S105 is not that; the module is S116 (staged) → S109 (planned lane id).
- Grey literature rests on one table cell (S116 char 15310); entry line 81 already says one module table. A "Chinese reporting module incl. grey literature" claim is single-source at best; S117 has no grey-literature statement.
- The Chinese reception of PRISMA-S rests on the SinoMed bibliographic record only (S119 `.txt` 2969 chars; abstract/keywords), not the interpretation's text.

## 6. Expansion-credit read

Net new ground: 4 of 4 theme parts. Held-and-already-covered: 0. Advances a listed Frontier item: none; advances one registered refusal flip (`lessons/round-43.md:43`). The coverage-map count line (README:70-87 plus the later corrections) must be re-derived with `ls corpus/knowledge/*.md | wc -l` at adoption (68 knowledge files at HEAD per `ls corpus/knowledge | wc -l`); it is stale-count-prone (round-49/50 precedent README:1083).

Tooling: no install; no network; no write outside this report. Lane-path draft for the L1 (rows, not applied): README coverage rows for `knowledge/japanese-search-record-r38.md`, `knowledge/chinese-search-record-r39.md`, `knowledge/japanese-search-record-r38-amendment-2026-10-23.md` (sources S107–S113 by document), plus an index row for `knowledge/search-log-method-r39.md`.

VERDICT: Attacked the claim that this theme is new ground — confirmed: 0 hits for 検索式/検索期間/检索策略/灰色文献 in the base corpus; all four theme parts new, none on the Frontier list, one registered refusal flip (`lessons/round-43.md:43`) advanced; also found `search-log-method-r39.md` unindexed (README grep 0) and four body-only ids (S097, S105, S106) naming wrong lane documents.
