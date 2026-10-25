# GroundS098 — round 49 w1, chousa slice

Seat: `GroundS098` (leaf, godspeed). Date: 2026-10-25. No tool installs (RULES.md read; none expected). No network, no live fetch, no scratch dir created, no writes outside this report.

## Row and capture identity

- Staged row **S089** -> lane id **S098** after renumbering (`adopt/renumber.tsv:4`: `S089 S098 append www.jstage.jst.go.jp/static/pages/FAQs/TAB2/-char/ja`). Cited by staged entry `merge/chousa/knowledge/corpus/knowledge/aggregator-vs-source-r36.md:6` (`source: S089 — https://www.jstage.jst.go.jp/static/pages/FAQs/TAB2/-char/ja …`).
- Capture `fea98dc5a5a486c988dd415c.txt` / `.raw` (key = `sha256(url)[:24]`, verified). Both forms are UTF-8 (`file`: "Unicode text, UTF-8 text"); the `.txt` is **not** a lossy decode, so quotes are taken from the `.txt` form. Digests recomputed:

```
txt 95733 ead3a7dd4ba97ae0ef05620f314844badf6c3fef5428988e61e4e2a146772f60
raw 178654 daa2c5d940fc20d0fab683e5e25b1f31a802d681d71319002449edf334029454
```

## Gate block draft — row S098

- URL: `https://www.jstage.jst.go.jp/static/pages/FAQs/TAB2/-char/ja`
- Access date: 2026-10-25 (lane opened date per C2 `OPENED`; staged entry's own read date 2026-10-23 unchanged in the entry).
- Quotes (each occurs EXACTLY ONCE in the `.txt` form; verified by `txt.find(q)` and `txt.find(q, i+1) == -1`; all ≤25 whitespace words and ≤160 chars):

Q1 (offset 29462, 52 chars, 1 ws word):
```
記事に登録された引用文献の情報をもとに、システムが引用元の所在を特定できた文献にリンクを付与しています。
```

Q2 (offset 29641, 28 chars, 1 ws word):
```
引用元の所在確認は、次の順で解析・検索を実施しています。
```

Q3 — the four-step resolution list, byte-exact slice of the `.txt` at offset 29672, 126 chars, 8 ws words (repr: `'1.DOI（メタデータ項目） をもとに検索\u3000例：10.xxxx\n\n 2.書誌情報（メタデータ項目） をもとに検索\u3000項目：著者名、誌名、巻号ページなど\n\n 3.引用文献の原文情報からDOIを検出して検索\n\n 4.引用文献の原文情報を書誌情報に解析して検索'`):
```
1.DOI（メタデータ項目） をもとに検索　例：10.xxxx

 2.書誌情報（メタデータ項目） をもとに検索　項目：著者名、誌名、巻号ページなど

 3.引用文献の原文情報からDOIを検出して検索

 4.引用文献の原文情報を書誌情報に解析して検索
```

Observed offsets (python `text.find`): Q1=29462, Q2=29641, step1=29672, step2=29706, step3=29749, step4=29775; all single occurrences. The same strings also exist in `.raw` (Q1 at 92972, steps at 93290/93429), but the `.txt` is the canonical non-lossy form.

## Per-claim support (staged entry vs capture)

Entry `aggregator-vs-source-r36.md` Observation bullet 2: *"J-STAGE's publisher FAQ states that a citation link is attached only where the system could locate the reference's source, and confirms the location in this order: DOI from the metadata item; bibliographic metadata; a DOI extracted from the reference text; then the reference text parsed into bibliographic data."*

- "citation link is attached only where the system could locate the reference's source" — **supported** (Q1): `システムが引用元の所在を特定できた文献にリンクを付与しています` = "links are attached to references whose source location the system could identify".
- "confirms the location in this order" — **supported** (Q2): `引用元の所在確認は、次の順で解析・検索を実施しています`.
- Step 1 "DOI from the metadata item" — **supported** (Q3 line 1): `1.DOI（メタデータ項目） をもとに検索`.
- Step 2 "bibliographic metadata" — **supported** (Q3 line 2): `2.書誌情報（メタデータ項目） をもとに検索`.
- Step 3 "a DOI extracted from the reference text" — **supported** (Q3 line 3): `3.引用文献の原文情報からDOIを検出して検索`.
- Step 4 "the reference text parsed into bibliographic data" — **supported** (Q3 line 4): `4.引用文献の原文情報を書誌情報に解析して検索`.
- Entry note "Steps 3 and 4 are inference from text, not identifier resolution" — consistent with the capture (steps 3–4 operate on 原文情報 = reference text; no identifier database is named).

Inference bullet's "an index's reference list is derived … an aggregator is never the source" — for **S089's share**: supported (the FAQ makes link attachment contingent on system-side location success, i.e. a derived artefact). The "not necessarily the same as the paper's references / neither equal nor superset" wording itself is S087's (CiNii) passage, not this row's. Unknown bullet ("whether the ladder records which rung produced each link — not observed") is consistent: the capture describes the ladder but no per-link rung field.

## anchor cell draft

`引用文献のリンクは、いつ、どのような仕組みで行われているのですか。（FAQ回答） — char 29462, char 29641, char 29672` (all `.txt` offsets of the quotes above; the question heading `引用文献のリンクは、いつ、どのような仕組みで行われているのですか。` sits at `.txt` line 2901, answer at line 2907).

## Register row S084 re-check (absent-defect-register.md:40)

Own re-check (python, both forms): register quote A `1.手動検索（記事編集の原文問合わせ機能、記事一覧の引用リンク削除・問い合わせ機能）2.自動検索（J-STAGE公開時にシステムで引用元の所在を検索）` and quote B `1.DOI（メタデータ項目）をもとに検索 2.書誌情報（メタデータ項目）をもとに検索 …` both return `find == -1` in `.txt` and `.raw`. All fragments are present (`手動検索` @29549, `記事編集の原文問合わせ機能` @29558, `記事一覧の引用リンク削除・問い合わせ機能` @29576, `J-STAGE公開時にシステムで引用元の所在を検索` @29610; the spaced form `（メタデータ項目） をもとに検索` @29672/29706).

**Verdict: absent-as-written.** Reason: the register quotes are collapsed rewrites of present content — they strip the `　例：10.xxxx` / `　項目：著者名、誌名、巻号ページなど` annotations, drop the source's space before `を`, insert ASCII-space separators between items, and fold the `　・` bullet lines into `（…）` groupings; none of that punctuation/layout exists in either capture form. The passage itself is present nearly verbatim (the correct gate quotes above), so this is a misquotation defect, not fabrication and not `unreachable` (the capture exists and was checked). Matches round-48's Gate verdict for S084.

VERDICT: re-grounded staged S089→lane S098 against the J-STAGE FAQ capture with three unique located `.txt` quotes (offsets 29462/29641/29672); all entry claims resting on this row supported; register S084 re-checked absent-as-written.
