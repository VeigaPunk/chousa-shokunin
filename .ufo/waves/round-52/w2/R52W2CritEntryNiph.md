# R52 W2 critic — attack on `japanese-search-record-niph-form-r52.md` entailment

Attacked: every `#### Observation` / `#### Inference` bullet of `corpus/knowledge/japanese-search-record-niph-form-r52.md` against the NIPH `.docx` text form (`capture-text.py` of `.qcache/3a8b45977cd111e45e3980a5.raw`, sha256 `16fc8c55ee856fefbbfc88b391b08233106b337e43aaf9f7a7bd825adeb09763`). All work in `/fast/scratch/hyaku/chousa-r52/R52W2CritEntryNiph/` (lump).

## Evidence base (commands run)
- `python3 tools/capture-text.py <raw> --locate` for every quoted phrase. Output (all `count=1`): `SRにおける文献検索期間について明記する。`→8996; `文献検索終了時点は、分析枠組みが決定された後から製造販売業者による分析提出までの一時点に決める。`→9020; `2015年1月から2018年10月まで`→9189; `PRISMA(Preferred Reporting Items for Systematic Reviews and Meta-Analyses)声明`→9257; `使用したデータベース`→9408; `使用した検索式`→9419; `ハンドサーチ等により未公表データを収集した場合は、そのことを上記のフローチャートに含める。`→9428; `上記の協力を受けた研究者の個人名や所属については原則として公開しない。`→19521; `医薬品及び医療機器の費用対効果評価に係る分析結果の記載様式と手引`→9; `中央社会保険医療協議会における費用対効果評価の分析ガイドライン第4版`→1446; `2.2節で定めた比較対照技術に対するRCTのシステマティックレビュー`→8389; `その名前と所属、役割、利益相反等を記載こと。`→**`count=0 offset=-1`**; `その名前と所属、役割、利益相反等を記載すること。`→`count=1 offset=19496`.
- `len(t)=19682`; 3.1 heading first at 682 (TOC), body heading at 8471; `実施体制` body at 19430; `名前` occurs once (19498), `個人名` once (19534), `氏名/氏/参考人/作成者/担当者` 0; `検索者/検索担当/誰が/検索日/最終検索/灰色文献/PRISMA-S/検索戦略` all 0; `検索式` 1 (9423); `文献検索期間` 2 (9002 sentence, 9181 example label); `データベース` 4, none dated; `提出様式/C2H/Evidence to Decision` 0; cover `【】` fields include `【提出者名】`; sidecar `.txt` decoded len **168,953**, U+FFFD **72,117**, first bytes `PK\x03\x04`.
- Span manifest: `spans.tsv` S115 rows offsets are quote_offset−80 (clamped 0); span files `spans/S115-5/6/13/14.txt` equal `t[start:start+80+len(q)+80]` exactly (True). `quotes.tsv` line 29 already carries the correct name phrase.

## Defects (narrowed wording for each)

1. **Obs 6: quote not verbatim (mangled).** The bullet quotes `その名前と所属、役割、利益相反等を記載こと。` at 19496; that string is absent (`--locate` count=0). The capture has `その名前と所属、役割、利益相反等を記載すること。` at 19496 (count=1), and `quotes.tsv`/`spans.tsv` already hold the correct form. Wording: quote `その名前と所属、役割、利益相反等を記載すること。` (`S115`, char 19496).
2. **Obs 6: "The only named-person field is for outside experts" overclaims.** The cover has a submitter-name field `【提出者名】`; the capture's only name-asking sentence (名前 occurs once, in §7) supports only a body-scoped claim. Wording: "In the report body, the only field that asks for an individual's name is the section-7 outside-expert item (the cover separately records the submitter name `【提出者名】`), and those names are 原則として not published."
3. **Inf 4: "the people it names are outside experts" same overreach.** Wording: "the people the report body asks to name are outside experts, and privately; the cover's `【提出者名】` is a separate submitter field."
4. **Obs 1: date offset mislabelled.** `国立保健医療科学院` is at char 51 but `2024年4月` is at char 61; the bullet's "(char 51)" covers both. Wording: "(char 51, char 61)".
5. **Obs 7: sidecar character total off by one.** Decoded length is 168,953, not 168,952 (U+FFFD 72,117 correct; `PK\x03\x04` zip bytes confirmed). Wording: "168,953 characters, 72,117 of them U+FFFD".

## Verdicts per bullet (rest support)
Obs 1 supports (defect 4); Obs 2 supports (TOC 682 / body 8471 / rct 8389 verified); Obs 3 supports (8996/9020 exact); Obs 4 supports (9189 exact; label separate paragraph; `(例)` before rows); Obs 5 supports (9257/9391/9408/9419/9428 exact); Obs 6 weaker (defects 1–2); Obs 7 supports (defect 5); Inf 1–3, 5 support; Inf 4 weaker (defect 3). Unknown bullets 29–32 check out (sweep numbers reproduced; staged run-on example / "PRISMA flow chart" mislabel / per-database date all confirmed absent or as stated in the staged `japanese-search-record-r38-amendment-2026-10-23.md`).

VERDICT: attacked the entailment of `japanese-search-record-niph-form-r52.md` — 4 bullets weaker/misworded (Obs 1, 6; Inf 4), 1 quote corrupted (Obs 6), 2 numeric slips (Obs 1, 7); all other Observation/Inference bullets supported exactly by the NIPH text form.
