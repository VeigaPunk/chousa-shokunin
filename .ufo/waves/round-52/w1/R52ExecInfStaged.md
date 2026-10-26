# R52ExecInfStaged — inference-ground on the three staged entries, bullet by bullet

Leaf seat; wrote only this file. Scratch `/fast/scratch/hyaku/chousa-r52/R52ExecInfStaged/` created and removed; no install, no network.
Captures read read-only from `.ufo/waves/corpus-expansion-1/.qcache/` of the staged package (key = sha256(url)[:24], computed in scratch).

## 1. The run

```
$ python3 tools/inference-ground.py --entry <staged>/<entry>.md --spans /dev/null --counts /dev/null \
    --registry corpus/SOURCES.md --root /fast/scratch/hyaku/chousa-r52/R52ExecInfStaged/root
GROUND entry=japanese-search-record-r38-amendment-2026-10-23.md section=1 bullets=4 tokens=2 grounded=0
FINDING INF_UNCITED bullet=1 token=''   /   FINDING INF_UNGROUNDED bullet=1 token=''
FINDING INF_UNCITED bullet=2 token=''   /   FINDING INF_UNGROUNDED bullet=2 token=''
FINDING INF_TOKEN_NOT_IN_SPAN bullet=3 token='a field, but not in PRISMA'
FINDING INF_TOKEN_NOT_IN_SPAN bullet=3 token='2020'
FINDING INF_UNGROUNDED bullet=4 token=''
GROUND entry=japanese-prisma-item-wording-r40.md section=1 bullets=3 tokens=2 grounded=0
FINDING INF_TOKEN_NOT_IN_SPAN bullet=1 token='2020'
FINDING INF_UNCITED bullet=2 token=''   /   FINDING INF_TOKEN_NOT_IN_SPAN bullet=2 token='difference in emphasis'
FINDING INF_UNCITED bullet=3 token=''   /   FINDING INF_UNGROUNDED bullet=3 token=''
GROUND entry=chinese-search-log-r37-amendment-2026-10-23.md section=1 bullets=3 tokens=1 grounded=0
FINDING INF_UNGROUNDED bullet=1 token=''  /  FINDING INF_UNGROUNDED bullet=2 token=''
FINDING INF_TOKEN_NOT_IN_SPAN bullet=3 token='intrinsic limitations as a reporting standard'
```

Each of the three runs ended `GROUND: FAIL`, exit=1. The block is the observed stdout, with only adjacent `FINDING` lines
joined by ` / ` to save lines; 15 findings in total (7 + 5 + 3). Cite sets, from the tool's own `ID_RE`:

```
japanese-search-record-r38-amendment-2026-10-23.md  b1 []  b2 []  b3 ['S097']  b4 ['S105']
japanese-prisma-item-wording-r40.md                 b1 ['S097']  b2 []  b3 []
chinese-search-log-r37-amendment-2026-10-23.md      b1 ['S093','S111','S112']  b2 ['S112']  b3 ['S111']
```

5 of 10 bullets cite no source; 2 more cite only the aside document (E1 b3's evidence is the NIPH form and the methods
journal and it cites `S097`; E1 b4's is the same form, cited as `S105`).

## 2. Findings and one located candidate phrase per bullet

| entry · bullet first 60 chars | finding | candidate phrase | capture key | form (chars) | offset |
|---|---|---|---|---|---|
| E1 b1 `The Japanese search record is now specified, and it is specified by` | `INF_UNCITED`, `INF_UNGROUNDED` | `SRにおける文献検索期間について明記する` | `3a8b4597…` | capture-text (19,682) | 8996 |
| E1 b2 `The rationale is the lane's own rationale, stated first in Japanese.` | `INF_UNCITED`, `INF_UNGROUNDED` | `最新の結果を反映しているかどうか` | `34fcefc1…` | `.txt` UTF-8 (25,811) | 11348 |
| E1 b3 `On Q12, the Japanese answer is "a field, but not in PRISMA".` | `INF_TOKEN_NOT_IN_SPAN` ×2 (`a field, but not in PRISMA`; `2020`) | `文献検索期間について明記` | `3a8b4597…` | capture-text (19,682) | 9002 |
| E1 b4 `The hand-search clause is the second literature to ask for the` | `INF_UNGROUNDED` | `ハンドサーチ等により` | `3a8b4597…` | capture-text (19,682) | 9428 |
| E2 b1 `Q12's Japanese half is now settled from the primary source, and it is a` | `INF_TOKEN_NOT_IN_SPAN` (`2020`) | `それぞれの情報源が最後に調べられた日付を記載する` | `e84bfe97…` | `.txt` UTF-8 (5,328) | 592 |
| E2 b2 `The three literatures now agree on what PRISMA itself asks for, and the` | `INF_UNCITED`, `INF_TOKEN_NOT_IN_SPAN` (`difference in emphasis`) | `検索した文献データベース名` | `34fcefc1…` | `.txt` UTF-8 (25,811) | 11229 |
| E2 b3 `The archive is the general answer to this lane's dead-host problem, and` | `INF_UNCITED`, `INF_UNGROUNDED` | `PRISMA 2020 チェックリスト` | `e84bfe97…` | `.txt` UTF-8 (5,328) | 0 |
| E3 b1 `Q5 now has an answer, and the answer is a category, not a document.` | `INF_UNGROUNDED` | `guiderFrom=中国循证医学杂志` | `453d492b…` | `.txt` UTF-8 (8,804) | 2863 |
| E3 b2 `The one field the lane most wanted is the one that travelled best.` | `INF_UNGROUNDED` | `检索或查询日期` | `cacddf3b…` | `.txt` UTF-8, text mode (6,179; raw decode 7,585) | 1719 |
| E3 b3 `The Chinese reception carries its own critique, and the critique is the` | `INF_TOKEN_NOT_IN_SPAN` (`intrinsic limitations as a reporting standard`) | `作为“报告规范”的内在局限` | `453d492b…` | `.txt` UTF-8 (8,804) | 2463 |

Every candidate satisfies `text.count(q) == 1`; the offset is `text.find(q)`. NIPH candidates located by the tool itself:

```
$ python3 tools/capture-text.py …/3a8b45977cd111e45e3980a5.raw --locate 'SRにおける文献検索期間について明記する'  -> LOCATED count=1 offset=8996
$ … --locate '文献検索期間について明記'  -> LOCATED count=1 offset=9002     $ … --locate 'ハンドサーチ等により'  -> LOCATED count=1 offset=9428
```

The S126 offsets reproduce the round-51 lane entry's own chars (`corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md:9-12`: 11229, 11243, 11294, 11348, 11457) — same capture, same form, so §2 is in the lane's existing convention.

## 3. Shown able to ground — and shown able to fail

Ten-bullet scratch entry over a scratch 7-column spans manifest of the five captures, run with the same tool:

```
GROUND entry=probe/probe.md section=1 bullets=10 tokens=10 grounded=10
GROUND: PASS
```

A 12-bullet variant, same manifest:

```
GROUND entry=probe2/probe2.md section=1 bullets=12 tokens=12 grounded=11
FINDING INF_TOKEN_NOT_IN_SPAN bullet=12 token='用いたフィルターや制限も含め，すべてのデータベース，試験登録，Webサイトの完全な検索戦略を記載する'
GROUND: FAIL
```

- bullet 11 (`包含16个条目的专项规范`, `S113`) **passed** although it occurs **twice** in that capture (the 简要介绍 block and
  the page's JSON `summary` field, `t.count == 2`): `INF_TOKEN_NOT_IN_SPAN` is substring containment, so it cannot enforce
  the once-only located-quote rule — uniqueness has to be checked with `find`, as in §2.
- bullet 12 is staged entry 2's own `recheck:` phrase and is **not** in the capture: pdftotext wrapped it
  (`'用いたフィルターや制限も含め，\n …すべてのデータベース，\n …試験登録，We'`, at 641). The fragment
  `用いたフィルターや制限も含め` (count=1, off 641) is re-locatable; the whole sentence is not.

## 4. Every staged citation must be re-bound — the id spaces disagree

| id | staged row (`SOURCES.append.md`) | lane row (`corpus/SOURCES.md`) |
|---|---|---|
| S091/S092/S093 | NSSD; Lateral Reading; GB/T 7714—2025 | CFEVER; FEVER paper; climate-fever |
| S105/S106 | lane-local chain-resolution entry; citation-chain-fidelity entry | CNKI 学术不端检测手册; CNKI 大学生论文管理系统手册 |
| S097 | FEVER dataset page | J-STAGE 出版社向け citation links |
| S125/S126/S129 | NIPH .docx; JAHBS 38(1); PRISMA JA archive | absent (S112 is the JAHBS article) |

Mapping: staged `S126`→lane **S112**, `S111`→**S113**, `S112`→**S114**, `S125`→**S115**, `S129`→**S116**. The
"functional-foods notification form" both staged entries call `S097` is lane **S108** (`corpus/SOURCES.md:118`;
`corpus/knowledge/japanese-search-record-r38.md:5` binds 別紙様式 (V)-4/-5 to S108). The Chinese reporting module the staged
text calls `S105` has no lane row at all — dropping it is the only honest option. E3 b3's `S091`/`S092`/`S093` ("CNKI
guides", "Chinese evidence-based nursing review") name FEVER-family papers in the lane: carrying them is exactly the
QUALITY 77 `BODY_CROSSREF` defect.

## 5. Form traps, and what the drafts need

1. **CRLF.** `cacddf3bbf780a4c7582bb17.txt` has 1,406 CRLF pairs: `检索或查询日期` is at **1719** in text mode and **2171** in
   `bytes.decode('utf-8')`; QUALITY 76 wants the form named — say "`.txt` read as UTF-8, universal newlines".
2. **Duplicated abstract.** The 梅斯医学 capture carries the abstract twice and only the quote marks differ (`作为“报告规范”…`
   at 2463 vs `作为&ldquo;报告规范&rdquo;…` at 3570) — that is why 2463 is unique and `包含16个条目的专项规范` is not.
3. **The NIPH worked-example string is not quotable as written.** `文献検索期間2015年1月から2018年10月まで` has count=0 in
   both forms; the halves do (`2015年1月` 9189, `2018年10月` 9198).
4. **`2020` cannot be grounded from the staged rows.** They carry no such designator, which is why the tool refused it; lane
   S116's title does carry "PRISMA 2020", so a bullet citing `S116` grounds the figure from that row only.
5. **The negatives hold.** `t.count('検索者') == 0` in the 19,682-char NIPH form and in the 5,328-char S129 form, matching
   both staged entries; a negative cannot be a quote token, so the affirmative half of each bullet needs §2's phrase.
6. **Minimum for the drafts:** one lane `S` id per Inference bullet (§4 mapping) and one findable token per bullet (§2);
   without them E1 b1/b3, E2 b1 and E3 b1 keep the `2020` / English-quote tokens that ground nowhere.

VERDICT: attacked all ten staged Inference bullets with `inference-ground.py` (3 entries, 15 findings, 0 grounded, exit 1
each) and built ten count-1 located candidate phrases, proven to ground 10/10 by the same tool — while exposing that
containment does not enforce once-only, that staged entry 2's own recheck phrase cannot be re-located across a pdftotext
wrap, and that every staged id names a different document in the lane.
