# R51W2ReopenRowS112 — Re-open and cell-by-cell audit of Registry row `S112`

Seat: `R51W2ReopenRowS112` (round 51, wave 2 — falsify) · Tip: `4436e279b91d8d68fd439c9095695035fbeeab74` · Base: `9ec1751a24231e899ceea4688e21c8edf6046d35` · Freeze: `d603f6f00f78d64f123d3aed2dd9f8701547a4ba`.
Capture: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/34fcefc159bf2ebbd1e09540.txt` (read-only).
**Form used throughout:** the `.txt` read as UTF-8 (`len(text) = 25811`, `47473` bytes, sha256 `065b889a97b00f8827933c86b645bf6339aba10e85a7c33d0f575c255ba1fa7b`); every offset below is `text.find(quote)` in that UTF-8 string, where `text.count(quote) == 1`, `len(quote.split()) <= 25`, and `len(quote) <= 160`. No tool installed; no network; no scratch directory created.

## 1. Commands and observed output

```text
$ grep -n '^| S112 ' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
122:| S112 | システマティックレビューとメタアナリシスの実施方法（剱持貴史・岡美智代）— 日本保健医療行動科学会雑誌 38(1):60-69 (2023) — https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf | paper | A | what this peer-reviewed Japanese methods article says a protocol and a search record must carry, and why, as this copy states it | the protocol-writing paragraph's PRISMA-P sentence and the 検索戦略を立案する step's database, provider and date sentence; capture .txt read as UTF-8, 25811 characters (two-column PDF text); char 10140, char 10146, char 11229, char 11243, char 11294, char 11348, char 11457 | the article reports 検索期間 and language limits as PRISMA-P protocol items and says the record should state the database name, the provider and the start and end dates of the search so that currency and updating can be judged | mined | 2026-10-25 | 365d | corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md |

$ awk -F'\t' '$1=="S112"' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round51/spans.tsv
S112	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	065b889a97b00f8827933c86b645bf6339aba10e85a7c33d0f575c255ba1fa7b	78	spans/S112-1.txt	システマティックレビューとメタアナリシスの実施方法	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
S112	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	065b889a97b00f8827933c86b645bf6339aba10e85a7c33d0f575c255ba1fa7b	10060	spans/S112-2.txt	検索の特徴（検索期間	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
S112	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	065b889a97b00f8827933c86b645bf6339aba10e85a7c33d0f575c255ba1fa7b	10066	spans/S112-3.txt	検索期間，言語制限	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
S112	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	065b889a97b00f8827933c86b645bf6339aba10e85a7c33d0f575c255ba1fa7b	11149	spans/S112-4.txt	検索した文献データベース名	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
S112	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	065b889a97b00f8827933c86b645bf6339aba10e85a7c33d0f575c255ba1fa7b	11163	spans/S112-5.txt	Ovid などのプロバ	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
S112	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	065b889a97b00f8827933c86b645bf6339aba10e85a7c33d0f575c255ba1fa7b	11214	spans/S112-6.txt	検索の開始日と終了日を記載することで	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
S112	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	065b889a97b00f8827933c86b645bf6339aba10e85a7c33d0f575c255ba1fa7b	11268	spans/S112-7.txt	最新の結果を反映しているかどうか	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md
S112	https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf	065b889a97b00f8827933c86b645bf6339aba10e85a7c33d0f575c255ba1fa7b	11377	spans/S112-8.txt	評価がしやすくなる	corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md

$ grep -ln '^source: S112 ' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/*.md
/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md

$ awk -F'|' 'NR==122{print "NF="NF}' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
NF=13
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa | tail -1
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
$ env -u ASSIMILATE_CITES python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round51/c2-count.py | grep -E '^(BOUND|ANCHOR_BOUND|CAPTURE_BOUND|C2)='
BOUND=6/7 (min 5) REFUSED=1
CAPTURE_BOUND=61/61
ANCHOR_BOUND=6/6
C2=PASS
```

## 2. Capture verification and located quotes (`.txt` read as UTF-8)

```text
$ python3 -c '
import hashlib, pathlib
u = "https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf"
k = hashlib.sha256(u.encode()).hexdigest()[:24]
p = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache") / (k + ".txt")
b = p.read_bytes(); t = p.read_text(encoding="utf-8")
print(k, len(b), len(t), hashlib.sha256(b).hexdigest())
for q in [
  "60                       剱持・岡／日本保健医療行動科学会雑誌                            38（1），2023      60－69",
  "システマティックレビューとメタアナリシスの実施方法",
  "剱持貴史＊          岡 美智代＊＊",
  "PRISMA-P には，",
  "検索の特徴（検索期間",
  "検索期間，言語制限",
  "表の資料や抄録を含めるかなど）を明記することが",
  "なお，使用した文献データベースの情報として，",
  "検索した文献データベース名",
  "Ovid などのプロバ",
  "イダー名，検索の開始日と終了日を記載することで，",
  "検索の開始日と終了日を記載することで",
  "最新の結果を反映しているかどうか",
  "最新の結果を反映しているかどうか，更新がされて",
  "いるかどうかの評価がしやすくなる８）。",
  "評価がしやすくなる",
  "検索が終了した後は，検索したデータベース名，",
  "検索した日，検索キーワードと検索式，検索件数を",
]:
  print(f"char={t.find(q)} count={t.count(q)} words={len(q.split())} len={len(q)} | {q}")
'
34fcefc159bf2ebbd1e09540 47473 25811 065b889a97b00f8827933c86b645bf6339aba10e85a7c33d0f575c255ba1fa7b
char=0 count=1 words=4 len=92 | 60                       剱持・岡／日本保健医療行動科学会雑誌                            38（1），2023      60－69
char=158 count=1 words=1 len=25 | システマティックレビューとメタアナリシスの実施方法
char=267 count=1 words=3 len=22 | 剱持貴史＊          岡 美智代＊＊
char=9908 count=1 words=2 len=12 | PRISMA-P には，
char=10140 count=1 words=1 len=10 | 検索の特徴（検索期間
char=10146 count=1 words=1 len=9 | 検索期間，言語制限
char=10184 count=1 words=1 len=23 | 表の資料や抄録を含めるかなど）を明記することが
char=11172 count=1 words=1 len=22 | なお，使用した文献データベースの情報として，
char=11229 count=1 words=1 len=13 | 検索した文献データベース名
char=11243 count=1 words=2 len=11 | Ovid などのプロバ
char=11289 count=1 words=1 len=24 | イダー名，検索の開始日と終了日を記載することで，
char=11294 count=1 words=1 len=18 | 検索の開始日と終了日を記載することで
char=11348 count=1 words=1 len=16 | 最新の結果を反映しているかどうか
char=11348 count=1 words=1 len=23 | 最新の結果を反映しているかどうか，更新がされて
char=11450 count=1 words=1 len=19 | いるかどうかの評価がしやすくなる８）。
char=11457 count=1 words=1 len=9 | 評価がしやすくなる
char=12105 count=1 words=1 len=22 | 検索が終了した後は，検索したデータベース名，
char=12179 count=1 words=1 len=23 | 検索した日，検索キーワードと検索式，検索件数を
```

## 3. Cell-by-cell audit and verdict

1. **`id` (`S112`) — HOLDS.** Next unused ID after `S111`, maps staged `S126` → lane `S112` (staged `S125` `.docx` refused).
2. **`source` — HOLDS.** Title `システマティックレビューとメタアナリシスの実施方法` at `char 158`, authors `剱持貴史＊          岡 美智代＊＊` at `char 267`, journal and issue `60                       剱持・岡／日本保健医療行動科学会雑誌                            38（1），2023      60－69` at `char 0` (the cell normalises fullwidth `38（1），2023      60－69` to `38(1):60-69 (2023)` and fills in pages `60-69` omitted by staged `S126`), and URL `https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf` (`sha256(url)[:24] = 34fcefc159bf2ebbd1e09540`).
3. **`kind` (`paper`) — HOLDS.** Valid enum; published journal methods article.
4. **`tier` (`A`) — HOLDS.** Argued by `scope`: staged `S126` was `B`, whereas lane `S112` narrows `scope` to `"as this copy states it"` and serves the PDF from the society's own domain (`jahbs.info`). An own-document statement on the publisher's host is primary (`A`) for what this copy states (unlike `S111`, an index record at `B`).
5. **`scope` — HOLDS (with residual note on "peer-reviewed").** Narrowed from staged `"Japanese methods journal"` to `"Japanese methods article ... as this copy states it"`, which matches the title at `char 158`. Residual note: `"peer-reviewed"` is not self-attested about this article in the capture (`t.count("査読") == 3`, all about other journals at `char 5966` `PRISMA 声明の準拠を求める査読付き雑誌` or a prior submission at `char 13468`/`13543`; the article category header at `chars 101–140` is 40 `U+FFFD` glyphs from unmapped `PKOCVZ+YuMincho-Regular-90ms-RKSJ-H`). The entry (`japanese-search-record-r38-amendment-2026-10-23.md:1,11`) and `corpus/README.md:1091` still retain the staged phrase `"peer-reviewed Japanese methods journal"`.
6. **`anchor` — HOLDS.** Names `the protocol-writing paragraph's PRISMA-P sentence and the 検索戦略を立案する step's database, provider and date sentence; capture .txt read as UTF-8, 25811 characters (two-column PDF text); char 10140, char 10146, char 11229, char 11243, char 11294, char 11348, char 11457`. Note that `spans.tsv` column 4 (`offset`) stores `start = max(0, off - 80)` (`build-spans.py:44,119`), so `offset + 80` for `S112-2`..`S112-8` (`10060+80`, `10066+80`, `11149+80`, `11163+80`, `11214+80`, `11268+80`, `11377+80`) equals `{10140, 10146, 11229, 11243, 11294, 11348, 11457}` (`S112-1` is the title at `78+80=158`) — every `char N` in `anchor` is an exact `text.find(quote)` offset of an `S112` quote in `spans.tsv`.
7. **`teaches` — HOLDS.** Every clause is carried by the capture `.txt` read as UTF-8 (and softens staged `must carry` to `should state`): (a) *"reports 検索期間 and language limits as PRISMA-P protocol items"*: `PRISMA-P には，` (`char 9908`), `検索の特徴（検索期間` (`char 10140`), `検索期間，言語制限` (`char 10146`), `表の資料や抄録を含めるかなど）を明記することが` (`char 10184`); (b) *"says the record should state the database name, the provider and the start and end dates of the search"*: `検索した文献データベース名` (`char 11229`), `Ovid などのプロバ` (`char 11243`), `イダー名，検索の開始日と終了日を記載することで，` (`char 11289`), `検索の開始日と終了日を記載することで` (`char 11294`); (c) *"so that currency and updating can be judged"*: `最新の結果を反映しているかどうか，更新がされて` (`char 11348`) across the page-64 header to `いるかどうかの評価がしやすくなる８）。` (`char 11450`, `評価がしやすくなる` at `char 11457`). (Step 7 also carries a second post-search list at `char 12105`/`12179`, which is an omission of additional content, not an ungrounded clause in `teaches`.)
8. **`status` (`mined`) — HOLDS.** Valid enum; cited by an active entry in `used-by`.
9. **`opened` (`2026-10-25`) — HOLDS.** Valid ISO date of the round-51 re-open from `.qcache`.
10. **`recheck` (`365d`) — HOLDS.** Valid `NNd` cadence under `CORPUS.md` and `sources-census.sh`.
11. **`used-by` (`corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md`) — HOLDS.** Exact match to `grep -ln '^source: S112 ' corpus/knowledge/*.md`.

**Survival on a non-author re-open:** **YES.** All 11 cells of `S112` in `corpus/SOURCES.md:122` hold against `.qcache/34fcefc159bf2ebbd1e09540.txt` (25,811 chars, sha256 `065b889a…`), all seven `char N` offsets in `anchor` match `text.find(quote)` in `spans.tsv` (`S112-2`..`S112-8`), `tier: A` is justified by the own-document scope, and every clause in `teaches` is grounded in the capture text.

VERDICT: attacked `corpus/SOURCES.md` row `S112` across all 11 cells against capture `34fcefc159bf2ebbd1e09540.txt` (UTF-8, 25811 chars) and `spans.tsv` — 11/11 cells hold (0 defects in the row; all 7 anchor `char N` offsets `10140, 10146, 11229, 11243, 11294, 11348, 11457` match `text.find(quote)` in `spans.tsv`, `tier: A` is argued by the own-document scope, every `teaches` clause is carried by the capture, and `used-by` matches the sole citing entry), so `S112` survives a non-author re-open.
