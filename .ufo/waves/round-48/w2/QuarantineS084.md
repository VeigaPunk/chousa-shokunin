# Quarantine hand-check — chousa S084 (`payload-absent`)

Row: `absent-defect-register.md:40` — `chousa | round1 | S084 | payload-absent |
https://www.jstage.jst.go.jp/static/pages/FAQs/TAB2/-char/ja`, two quoted payloads.
Lane file binding the same URL + quotes: `lanes/chousa/SOURCES-PROPOSED.md:104-109`,
`#### Gate — S089` (current file id; the register's `S084` matches quote-lint v4/v5
`binding:"id"` output — id namespace drift, URL+quote pair is unambiguous).

**Verdict: absent-as-written** — both quoted strings are byte-absent from every
local artifact, but the underlying passage is present verbatim; the register's
`payload-absent` (fabrication-class) label is calibration-correct yet the defect
is reformatting, not invented content.

## On-disk capture (the only artifact; gate names one URL, no companions)

`.ufo/waves/corpus-expansion-1/.qcache/fea98dc5a5a486c988dd415c`
- key = `sha256("https://www.jstage.jst.go.jp/static/pages/FAQs/TAB2/-char/ja")[:24]` — verified
  via `python3 -c "import hashlib; print(hashlib.sha256(b'...').hexdigest()[:24])"` → `fea98dc5a5a486c988dd415c`.
- `.raw` 178,654 B, sha256 `daa2c5d940fc20d0fab683e5e25b1f31a802d681d71319002449edf334029454`; `<title>FAQ（J-STAGE登載機関向け）</title>`.
- `.txt` 95,733 B, sha256 `ead3a7dd4ba97ae0ef05620f314844badf6c3fef5428988e61e4e2a146772f60`. No `.fail` marker for this key.

## Source passage (both files)

- `.raw` bytes 135381–136397: `記事に登録された引用文献の情報をもとに…` (135381),
  `リンクの付与は、以下のタイミングで検索を行っています` (135552), the list
  `1.手動検索<br>　・記事編集の原文問合わせ機能<br>　・記事一覧の引用リンク削除・問い合わせ機能<br>2.自動検索<br>　・J-STAGE公開時にシステムで引用元の所在を検索`,
  then `引用元の所在確認は…` (135944) and `1.DOI（メタデータ項目） をもとに検索　例：10.xxxx<br>2.書誌情報（メタデータ項目） をもとに検索　項目：著者名、誌名、巻号ページなど<br>3.…<br>4.…解析して検索` (136330).
- `.txt` bytes 71350–72234: same passage, `<br>`→newline, bullet `　・` kept,
  `（メタデータ項目） をもとに検索` at 71909/71988 — note the retained space.

## Match attempts (commands, observed output)

`grep -boF` of each register string and its substrings against `.raw` and `.txt`:
- `1.手動検索（記事編集の原文問合わせ機能、記事一覧の引用リンク削除・問い合わせ機能）2.自動検索（J-STAGE公開時にシステムで引用元の所在を検索）` → **no hit** in either file.
- `1.DOI（メタデータ項目）をもとに検索 2.書誌情報（メタデータ項目）をもとに検索 …` → **no hit**.
- `手動検索（記事編集` → no hit; `（メタデータ項目）をもとに検索` → no hit.
- `（メタデータ項目） をもとに検索` (source's spaced form) → hits at `.raw` 136048,136139; `.txt` 71909,71988.
- `引用文献の原文情報からDOIを検出して検索` → `.raw` 136256, `.txt` 72093 (verbatim).
- `引用文献の原文情報を書誌情報に解析して検索` → `.raw` 136330, `.txt` 72155 (verbatim).

Other qcache raws mentioning the lane: 19 J-STAGE pages checked by `<title>`;
none contains `手動検索` — the FAQ capture is the only relevant artifact.

## Reason

The register quotes are a collapsed rewrite: whitespace/bullets stripped into
`（…）` groupings, and the source's space before `を` and its `例：`/`項目：`
annotations deleted — differences no whitespace/case/markdown fold repairs, so
the quote-lint's eleven folds correctly returned ABSENT (`quote-lint-full-v5.json`
finding, `binding:"id"`). The payload is therefore **absent as written**;
`payload-absent` is the right class letter. But the defect is misquotation of
present content — the four-step resolution list exists in the source nearly
verbatim — not a fabricated passage: the smallest safe correction is to rewrite
the two gate quotes to the source's literal lines (or mark them paraphrased),
not to refuse the row.

## Impacted axes

- **calibration**: a byte-absent verdict that is semantically content-present
  shows `payload-absent` conflates two defects (misformatted quote vs invented
  quote); C1's precision/counter legs treat both identically.
- **operability**: hand-check is fully operable — cache-key derivation is
  documented in `quote-lint.py:437-438` and reproduced exactly.

No live fetch performed; no files touched outside this report.
