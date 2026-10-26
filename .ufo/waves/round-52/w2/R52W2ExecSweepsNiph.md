# R52W2ExecSweepsNiph — wave-2 re-run of the S115 entry's commands, offsets and negatives

seat: W2 falsify (chousa lane). Target: `corpus/knowledge/japanese-search-record-niph-form-r52.md` (S115, NIPH form),
read through `tools/capture-text.py` on `.qcache/3a8b45977cd111e45e3980a5.raw`. No lane file written; scratch
`/fast/scratch/hyaku/chousa-r52/R52W2ExecSweepsNiph` (TMPDIR there, removed at exit). No install (nothing needed;
pacman guard untouched). Captures opened read-only; no fetch (L0 `8d77e6c1` open). Text form re-derived:
`sha256 754aae42…`, 19,682 chars; the `.raw` is `sha256 16fc8c55ee85…` (both match the entry/claim pins).

## 1. Commands in the entry — re-run

`recheck:` (verbatim, from the lane root):
```
$ python3 tools/capture-text.py /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/3a8b45977cd111e45e3980a5.raw --locate 'SRにおける文献検索期間について明記する。'
LOCATED count=1 offset=8996            → reproduces
```
The recheck's second half ("re-download the `.docx` and confirm …") is **not runnable as written**: no network, L0
`8d77e6c1` open; the two strings it would guard are pinned by the digest above instead.

`#### Unknown` sweep (verbatim pipeline):
```
$ python3 tools/capture-text.py <raw> | python3 -c "import sys;t=sys.stdin.read();print(len(t),[t.count(w) for w in ('検索者','検索担当','誰が','検索日','最終検索','灰色文献','PRISMA-S','検索戦略')])"
19682 [0, 0, 0, 0, 0, 0, 0, 0]         → reproduces exactly
```
Joined-string negative and the two occurrence counts, through the tool:
```
$ … --locate '文献検索期間2015年1月から2018年10月まで'   → LOCATED count=0 offset=-1   (exit 1)  reproduces
$ … --locate '文献検索期間'                              → LOCATED count=2 offset=9002 (exit 1)  reproduces
```

## 2. Every `char N` — re-located with `find`/`count` in the stated text form

| quote | stated | observed | verdict |
|---|---:|---:|---|
| title / `[第2.0版]` | 9 / 42 | 9 / 42, count 1 each | reproduces |
| 国立保健医療科学院 / 2024年4月 | 51 | 51 / **61** | reproduces for the block start; the date is 61 (one offset for two lines) |
| 中央社会保険医療協議会…分析ガイドライン第4版 | 1446 | 1446, count 1 | reproduces |
| 2.2節で定めた比較対照技術に対するRCTの…レビュー | 8389 | 8389, count 1 | reproduces |
| 3.1 heading: TOC / section body | (682) / 8471 | 682 / 8471, count 2 | reproduces — the body heading starts exactly 8471 |
| SRにおける文献検索期間について明記する。 | 8996 | 8996, count 1 | reproduces |
| 文献検索終了時点は、…一時点に決める。 | 9020 | 9020, count 1 | reproduces (separated from 8996 by `なお、`) |
| 2015年1月から2018年10月まで | 9189 | 9189, count 1 | reproduces; separate paragraph from the `文献検索期間` label at 9181 |
| PRISMA(…Meta-Analyses)声明 | 9257 | 9257, count 1 | reproduces (the form continues `(http://www.prisma-statement.org/)`) |
| 臨床研究の組み入れ基準や除外基準 | (9391 in quotes.tsv) | 9391, count 1 | reproduces under the manifest |
| 使用したデータベース / 使用した検索式 | 9408 / 9419 | 9408 / 9419, count 1 each | reproduces |
| ハンドサーチ等により未公表データを…含める。 | 9428 | 9428, count 1 | reproduces |
| その名前と所属、役割、利益相反等を記載すること。 | 19496 | 19496, count 1 | reproduces; section-7 body heading at 19427, so inside 実施体制 |
| 上記の協力を受けた研究者の個人名や所属については…公開しない。 | 19521 | 19521, count 1 | reproduces |

`.../round52/build-spans.py --check` → `SPANS_ROWS=38 STALE=0` (exit 0). The manifest's `offset` column is the span
slice start (quote offset − 80, `CONTEXT`; 8996 → 8916), so it must not be read as the quote offset — no defect.

## 3. Every negative — re-run

| statement | command | result |
|---|---|---|
| `提出様式`, `C2H`, `Evidence to Decision` occur 0 times | `count` | 0/0/0 — reproduces as written |
| `.txt` sidecar is not this document's text | `read_text` / decode | `文献検索` 0; 72,117 U+FFFD — reproduces |
| `.txt` is 168,952 chars | `read_text(utf-8, errors=replace)` vs `decode` | **168,952** under the builder's universal-newline read (what `build-spans.py` uses); 168,953 under a plain byte decode — reproduces with the method pinned |
| `検索式` once; `文献検索期間` twice | `count` | 1 (9423, inside 9419) / 2 (9002, 9181) — reproduces |
| `データベース` 4 occurrences, none dated | regex ±120 chars | 4 (9412, 10258, 10304, 15646), no date window — reproduces |
| the table is marked `(例)` | `find` | marker at 9100, directly before the example table (患者 9110, 文献検索期間 9181) — reproduces |

## 4. Widened negatives (five-plus synonyms each, in Japanese)

**A. "the form names neither a searcher"** — added `検索実施者 0, サーチャー 0, 文献検索担当 0, 検索を担当した者 0,
図書館員 0, 司書 0, 情報専門家 0, 検索補助者 0` (also `担当者 0, 作成者 0, 実施者 0, 記入者 0, 責任者 0`). The negative
**holds and is strengthened**; the only person fields stay in section 7 (`名前` 1, `個人名` 1).

**B. "nor grey literature by that name, nor PRISMA-S"** — added `灰色資料 0, グレー文献 0, 未発表 0, 会議録 0, 抄録集 0`
and `PRISMA for Searching 0, 検索のためのPRISMA 0` (`PRISMA` occurs once, only at 9257). The literal-name negative
**holds**, but widening finds the concept: `未公表` twice — 9438 (the quoted sentence) and **9485
「承認申請に用いたデータは未公表のものでも含めることを推奨する。」** — plus `公表されていない` at 5373 (price negotiation).
9485 is in neither Observation, sweeps nor Inference: the form *recommends* including unpublished approval-application
data, the stronger grey-literature statement a wider sweep would have surfaced. Bullet 3 ("counted in the flow chart,
not hidden") is narrower than the form and renders `含める` (include) as "counted", which the sentence does not say.

**C. (extra) the staged title strings** — `提出様式 0` widened to `記載様式 1 (34), 報告様式 0, 提出用様式 0, ひな形/雛形 0,
テンプレート 0, フォーマット 0`: the absence is name-scoped — the document calls itself a 記載様式 in its title and again at
1767 (`本様式の1ページ目は削除`), so "0 times" must not be read as "not a submission form". `C2H` is 0 case-sensitively,
but `c2h` occurs once at 1612 inside `https://c2h.niph.go.jp/…`: the negative is case-sensitive.

## 5. `inference-ground.py` on the entry, and a negated bullet

```
$ python3 tools/inference-ground.py --entry …/japanese-search-record-niph-form-r52.md \
    --spans …/round52/spans.tsv --counts /dev/null --registry …/corpus/SOURCES.md --root …/chousa-shokunin
GROUND entry=corpus/knowledge/japanese-search-record-niph-form-r52.md section=1 bullets=5 tokens=9 grounded=9
GROUND: PASS                              (exit 0)
```
Rule 5 is what this seat attacks. In scratch copies I negated one Inference bullet at a time and re-ran the same command:
```
mut1  "carries a start and an end date … end is bounded"  → "carries no start date … not bounded"          PASS (exit 0)
mut2  "unpublished data is counted … not hidden."         → "… is excluded from the flow chart."          PASS (exit 0)
mut3  "The form does not make the searcher a field"       → "The form makes the searcher a required field" PASS (exit 0)
mut4  bullet 3 lead-in "`S115` says"                      → "`S115` does not say" (negator glued to quote) PASS (exit 0)
```
Not a broken tool — the English control fires:
```
fx (span "… the form requires a search date …", bullet "The form does not require a search date.")
FINDING INF_POLARITY_FLIP bullet=1 token='requires a search date / require'   GROUND: FAIL   (exit 1)
```
Mechanism, measured: `words()` on a CJK quote returns **0 tokens** (`ハンドサーチ等…含める。` → `words(): 0 []`,
`content: 0 []`, `stems: set()`); `polarity_flips` returns `[]` at `if not stems: return []`. All five Inference bullets
quote CJK-only phrases, so **rule 5 gives zero coverage on this entry**: the PASS is presence + citation only. Not a claim
violation (the tool announces itself lexical), but the entry must not be read as polarity-checked.

## 6. What I attacked → result

- recheck command, Unknown sweep, joined-string `--locate`, both occurrence counts, all 16 offset assertions and five
  negatives → **reproduce** (imprecision: `2024年4月` at 61, not 51; `.txt` 168,952 is the universal-newline read).
- The "no searcher" negative survives eight added Japanese synonyms; the grey-literature negative survives only as a
  literal name and **misses 9485**, the form's own recommendation to include unpublished approval data.
- `inference-ground` PASSes the entry (9/9 tokens) and PASSes four semantic negations of its Inference bullets; rule 5 is inert for CJK quotes by construction.
- **Blocked/not runnable:** the recheck's re-download half (no network). No blocker on the rest.

Files changed: none in the lane. Receipts: every output above was produced in `/fast/scratch/hyaku/chousa-r52/R52W2ExecSweepsNiph` and pasted here before that directory was removed.
VERDICT: attacked the S115 entry's two commands, 16 char offsets, five 0-times/not-in-capture negatives and its
`inference-ground` PASS — commands and offsets reproduce (one offset at 61 not 51), the searcher negative widens clean,
the grey-literature negative holds only by name and omits the 9485 recommendation, and rule 5 cannot detect any
negation of a CJK-quoted bullet (4/4 mutations PASS, English control FAILs as designed).
