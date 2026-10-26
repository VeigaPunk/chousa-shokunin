# R52W2ReopenRowS115 — falsify: Registry row S115 (NIPH `.docx` reporting form)

Attacked: the Registry row `S115` in `corpus/SOURCES.md` line 125 (NIPH 費用対効果評価 reporting form) — re-opened its capture as a non-author, checked every cell, re-located every quote, replayed the counters.

## Re-open (operability)

- `python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/capture-text.py /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/3a8b45977cd111e45e3980a5.raw` → exit 0, prints 19,682 characters; sha256 of that text = `754aae4266a19af9518a4bb46bcd484078baeb095df048d171cfc8cc2f24b0d9`. Raw file sha256 = `16fc8c55ee856fefbbfc88b391b08233106b337e43aaf9f7a7bd825adeb09763` (= spans.tsv col.3 = `c1-count.py` `REAL_SHA`; row's "raw sha256 prefix 16fc8c55" holds). `sha256("https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx")[:24]` = `3a8b45977cd111e45e3980a5` = the `.raw` filename (URL↔capture binding, no network).
- `--locate` agrees: `SRにおける文献検索期間について明記する。` → `LOCATED count=1 offset=8996`; title → offset=9; `[第2.0版]` → offset=42; `上記の協力を受けた研究者の個人名や所属については原則として公開しない。` → offset=19521; staged joined string `文献検索期間2015年1月から2018年10月まで` → `count=0` (disclosed correction stands).

## Anchor cells (all 14 manifest quotes re-located)

Command: python loop over `quotes.tsv` × `spans.tsv` × `spans/S115-N.txt`, abs = offset + span.find(quote), vs text.find.

```
1 start 0 abs 9  text_find 9  count 1 OK      (title)
2 start 0 abs 42 text_find 42 count 1 OK      ([第2.0版])
3 start 1366 abs 1446 text_find 1446 count 1 OK (guideline 第4版)
4 start 8309 abs 8389 text_find 8389 count 1 OK (RCTのSR)
5 start 8916 abs 8996 text_find 8996 count 1 OK (期間明記)
6 start 8940 abs 9020 text_find 9020 count 1 OK (終了時点)
7 start 9109 abs 9189 text_find 9189 count 1 OK (2015…2018年10月)
8 start 9177 abs 9257 text_find 9257 count 1 OK (PRISMA声明)
9 start 9311 abs 9391 text_find 9391 count 1 OK (組み入れ基準)
10 start 9328 abs 9408 text_find 9408 count 1 OK (データベース)
11 start 9339 abs 9419 text_find 9419 count 1 OK (検索式)
12 start 9348 abs 9428 text_find 9428 count 1 OK (ハンドサーチ)
13 start 19416 abs 19496 text_find 19496 count 1 OK (名前と所属)
14 start 19441 abs 19521 text_find 19521 count 1 OK (公開しない)
```

Section 3.1 heading `3.1システマティックレビューのリサーチクエスチョン` occurs exactly twice (682 TOC, 8471 section — entry's "section itself starts at char 8471" holds); issuer at 51, date at 61. `build-spans.py --check` (lane root): `SPANS_ROWS=38 STALE=0`, exit 0.

## Cell verdicts

| cell | verdict | evidence |
|---|---|---|
| title | HOLD | text chars 9/42/51/61 carry title, edition, issuer `国立保健医療科学院`, `2024年4月` |
| url | HOLD | single URL; key↔file, raw sha matches row/c1-count |
| kind `docs` | HOLD | raw is OOXML zip (`PK\x03\x04`), main part readable; sidecar `.txt` is zip bytes decoded with replacement (168,953 chars by my read, 72,117 U+FFFD — lesson/entry say 168,952; ±1, immaterial), not the document text |
| tier A | HOLD | argued: the document itself is the template and is primary for what the row scopes ("as the template states it") |
| scope | HOLD | every clause of the scope is a located quote of this capture; the "not a reporting standard for every review" limitation is faithful (document only binds this procedure's submission) |
| anchor | DEFECT (minor) | the 5 listed `char N` are all correct located quotes (8996/9020/9408/9419/9428), but the manifest carries 14; the row omits 9 (9, 42, 1446, 8389, 9189, 9257, 9391, 19496, 19521) — builder contract (`build-spans.py` docstring): every written `QUOTE <id> char <N>` is a value an anchor cell's `char N` must equal; the citing entry itself labels all 14 with `S115` chars |
| teaches | HOLD | all 5 clauses carried by capture: period (8996), end-window (9020), databases/expressions under PRISMA lead (9257/9408/9419), hand-search counted in flow chart (9428); negation clause verified by sweep: `[0,0,0,0,0,0,0,0,1,2]` for 検索者/検索担当/誰が/検索日/最終検索/灰色文献/PRISMA-S/検索戦略/検索式/文献検索期間 — no searcher, no search date |
| status `mined` | HOLD | |
| opened `2026-10-26` | HOLD | = today |
| recheck `180d` | HOLD | matches entry's `recheck: 180d` |
| used-by | HOLD | `grep -ln '^source: S115 ' corpus/knowledge/*.md` → exactly `japanese-search-record-niph-form-r52.md` |

## Counter replay

- `c1-count.py`: `REAL=PASS rc=0 count=1 locate=(0, 1, 8996) chars=19682`, `LEGS=9/9`, `C1=PASS`.
- `c1-supplement.py`: `REAL_TEXT=PASS rc=0 chars=19682`, `SUPPLEMENT_LEGS=4/4`, `C1_SUPPLEMENT=PASS` — pinned `TEXT_SHA=754aae42…` equals my computed text digest.
- `c2-count.py`: `ENTRIES=3/3`, `BOUND=4/4 (S113..S116)`, `QUOTE_ROWS=38`, `QUOTES_IN_SPAN=38/38`, `ANCHOR_BOUND=4/4`, `SUBSTANCE=PASS`, `C2=PASS`.

## Observations (not blockers)

- Entry source-line "sha256 `16fc8c55…`" sits beside the text-form mention but is the raw-capture digest; the text form's digest is `754aae42…` (E1) — ambiguous labeling only.
- Sidecar char count: my read 168,953 vs lesson/entry 168,952 (±1; FFFD 72,117 matches exactly).

## Verdict

Row S115 survives a non-author re-open: the capture re-opens (19682 chars, exit 0), all 14 located quotes are unique and at their stated offsets (--locate agrees), every cell holds except the anchor cell listing 5 of 14 manifest quotes (minor defect); counters C1, C1-supplement, C2 all PASS.
