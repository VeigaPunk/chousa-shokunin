# R51ExecQuarantine — quarantine slice, seven theme documents

Seat R51ExecQuarantine, round 51 wave 1, leaf (no dispatch). Read-only throughout: campaign
register, `.qcache` captures, staged package. No campaign tool run. Scratch
`/dev/shm/chousa-r51-R51ExecQuarantine/` only, deleted before this file was written.

## 1. The six rows the counter names

    $ R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
    $ awk -F'|' -v l='chousa' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5, $6}' "$R" | grep -E 'S104|S105|S111|S112|S114|S120'
     S104   `payload-absent`   https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja
     S105   `payload-absent`   https://jaohfa.com/pdf/systematic_review.pdf
     S111   `payload-absent`   https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290
     S112   `payload-absent`   https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237
     S114   `payload-absent`   https://www.sinomed.ac.cn/article.do?ui=2026335073
     S120   `payload-absent`   https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx

The unfiltered awk prints 20 well-formed `chousa` rows (plus four malformed
`#### Gate — S100…S103` fragments); exactly these six name a theme URL.

    $ python3 corpus/evidence/round51/c2-count.py | grep QUARANTINE
    QUARANTINE_VERDICTS=0/6 (S104,S105,S111,S112,S114,S120)
    QUARANTINE_BLOCKED_ADOPTED=0

`0/6` is vacuous — `corpus/lessons/round-51.md` does not exist yet — so the §4 lines are what
the counter will read. All six class cells are `payload-absent`. S126 JAHBS `vol38_1_5.pdf`
has **no** register row (`grep -n 'jahbs\|vol38_1'` → no match), so it owes no verdict.

## 2. Capture keys (`sha256(url)[:24]`)

    S104 jstage-kenkokyoiku  7194acc65a18f6555e4b8893  txt=36968 raw=713922
    S105 jaohfa              62be15a474e866e4bef6c9d5  txt=61188 raw=291615
    S111 slarc-EN-5290       fd468a36d78ff156b6200946  txt=82902 raw=1156890
    S112 slarc-CN-5237       c7266931a1731db3ff6ae77d  txt=69789 raw=1140215
    S114 sinomed             42bac8830527d6f1bb125c49  txt=2969  raw=20142
    S120 niph-docx           3a8b45977cd111e45e3980a5  txt=319599 raw=178056
    S126 jahbs               34fcefc159bf2ebbd1e09540  txt=47473 raw=7787275

Verdict rule, stated before use. `present`: every document-attributed quote part occurs in the
payload **as a reader sees it**, once extraction layout is undone (line breaks, CJK/Latin
justification spaces, PDF column interleave, table-cell split), with **zero character
substitution**. `absent-as-written`: at least one part fails that (a character differs, or the
part is markup the page does not render, or the part is lane prose) while its substance is
still locatable. `fabricated`: a document-attributed part's substance is nowhere.
`unverifiable`: no text rendering of the payload exists. `DEINT(u)` = `.qcache/<key>.txt` read
as UTF-8, each line split at its widest run of ≥3 spaces into a left and a right fragment,
left fragments concatenated then right, extractor line breaks removed. Round-46's `evi-`/
`dence` join applies to none of the six (no Latin hyphen split in any located quote).

## 3. Row by row (located quotes and offsets in §4)

- **S104 (round 3), J-STAGE 日健教誌 32(2)** — `.txt` PDF text, two columns interleaved: the sentence is split across columns (`このプロセスに際して，誰が検索を行ったの` at DEINT 3225, rest at DEINT 8233), and every full stop is U+FF0E `．` where the register writes U+3002 `。` (DEINT 8264, 8300). Substance present, bytes differ. **absent-as-written.**
- **S105 (round 3), 健康食品産業協議会 別紙様式 (V)-4** — `.txt` PDF text; the page is a four-column table. Row 6's cells, read off `.txt` 3850-4500: `情報源［Information sources］` | `6` | `全てのデータベース、研究登録、Webサイト、組織、文献リスト、研究を特定するために…` | bullets. Q0 is those cells in reading order with `Information`/`sources` and `Web サイ`/`ト` joined — extractor artefacts, no character substitution. Q2 is cell C's second sentence, split by the interleaved bullet column (`それぞれの情報源が最後に調べられた` at 4192, its `日付を記載する。` continuation at 4285). Q1 (`and not, as a search engine's rendering of the same form has it,`) has count 0 and is **lane prose pasted into the quote cell**, not document text. The requirement is also printed verbatim as a bullet at 4123 (count 1): `・それぞれのデータベース毎に最後に検索した日の日付を記載する。` **absent-as-written** (Q1).
- **S111 (round 4), 实验动物与比较医学 45(4):496-507 (EN route)** — `.txt` PDF text, two columns. `报告规范，研究者可参考PRISMA框架` is the tail of the sentence at DEINT 2882 — byte-exact, count 1, 40 chars, 5 whitespace words. **present.**
- **S112 (round 4), 实验动物与比较医学 45(1):101-111** — `.txt` PDF text, two columns. Q0 byte-exact at DEINT 21691 (85 chars, 12 words, count 1); the register only removed the typesetter's CJK/Latin spaces (`Embase 和 Web of Science`, `2024 年 4 月 1 日`). Q1 likewise differs only by justification spaces (`主 题 词 （MeSH/Emtree） 和 关 键 词 。`). Q2 drops one character — the `.` after `101-111` — and joins `45`/`(1)` across a line break (`.txt` 49175 `实验动物与比较医学, 2025, 45` + 49267 `(1): 101-111. DOI: 10.12300/j.issn.1674-5817.2024.109.`). **absent-as-written** (Q2, one character).
- **S114 (round 4), SinoMed record 2026335073** — `.txt` (2969 B) HTML→text. The rendered page carries the headings as a link list under `查看主题词相同的文献，请选择：` (`.raw` 11079), not under `主题词：`. Both register strings are byte-exact from an **HTML comment** — `<!--` at `.raw` 9192, `-->` at 9908 — which also holds `学科分类号：` and `R-05;R-37;R348.3;R916.3` (`学科分类号 inside comment: True` / `主题词(表) inside: True`). Q1's field is never rendered; Q0's label is the comment's, not the page's. **absent-as-written.**
- **S120 (round 5), 国立保健医療科学院 Reporting_Format_Jap_202404.docx** — the `.txt` (319599 B) is **the ZIP bytes decoded as text** (`'PK\x03\x04…[Content_Types].xml'`), not a text rendering. `.raw` is the docx; unzipped, `word/document.xml` → 1224 `<w:p>`, `<w:t>` runs concatenated, paragraphs joined by `\n` (55839 chars): all three register quotes byte-exact, count 1 each — 39411 `SRにおける文献検索期間について明記する。`, 39435 `文献検索終了時点は、…一時点に決める。`, 39843 `ハンドサーチ等により未公表データを…`. **present.**

## 4. Machine lines (verdict line + located quote / char offset)

```
register S104 (round 3) verdict: absent-as-written
か，その日時，使用した検索式を同時に記録しておくことが望ましい．これにより，研究の透明性を保ち，他者が同様の検索を再現できるようになる．	char 8233	form DEINT	https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja
register S105 (round 3) verdict: absent-as-written
それぞれの情報源が最後に調べられた	char 4192	form .txt read as UTF-8	https://jaohfa.com/pdf/systematic_review.pdf
register S111 (round 4) verdict: present
由于目前尚无专门针对动物实验 SR 的报告规范，研究者可参考 PRISMA 框架	char 2882	form DEINT	https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290
register S112 (round 4) verdict: absent-as-written
检索中国知网、万方、中国生物医学文献数据库、PubMed、Embase 和 Web of Science 数据库，检索时间从各数据库建立至 2024 年 4 月 1 日。	char 21691	form DEINT	https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237
register S114 (round 4) verdict: absent-as-written
R-05;R-37;R348.3;R916.3	char 9302	form .raw decoded UTF-8	https://www.sinomed.ac.cn/article.do?ui=2026335073
register S120 (round 5) verdict: present
SRにおける文献検索期間について明記する。	char 39411	form .raw unzipped → word/document.xml UTF-8	https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx
```

Each quote checked `count == 1`, `len ≤ 160`, `≤ 25` whitespace words, offset from `text.find`
in the stated form: `S104 unique: 1 at 8233` · `S111 unique: 1 at 2882 chars 40 words 5` ·
`S112 unique: 1 at 21691` · `S105 count 1 find 4192` · `S114 count 1 find 9302` · `S120
count 1 find 39411`. All six lines parse under the counter's own `VERDICT_RE` (c2-count.py:85)
— verified by re-running that regex over the six lines.

## 5. Which verdicts block a bound document

`blocked = sum(... if v in ("fabricated", "unverifiable") and reg_ids[rid] in bound.values())`
(c2-count.py:247-249). Only `fabricated` and `unverifiable` block, and only when the row's
theme URL belongs to a document the lane **bound**; `present` and `absent-as-written` never
block. None of the six is fabricated or unverifiable — every quote's substance is in its
payload — so **no register verdict blocks any of the six documents.** Two rows are one step
from blocking and must not be quoted as displayed text: S114's `学科分类号` line exists only
inside the HTML comment (the staged entry's `source:` line already names `学科分类号` as a
field), and S105's Q1 is lane prose inside the quote cell. Either, carried into an entry as a
document span, would be fabrication on a re-check.

## 6. Two findings outside the register

1. **The docx cannot pass `CAPTURE_BOUND`.** `form_text` (c2-count.py:117-126) accepts only
   `.txt` read as UTF-8 or `.raw` decoded UTF-16LE. Simulated on the NIPH capture:
   `digest=txt 471e558969d4… returned=len=168952 quote_found= False`,
   `digest=raw 16fc8c55ee85… returned=len=89007 quote_found= False` — both return garbage,
   neither contains any quote. `SPAN_IDS` needs ≥3 span rows per bound id and `CAPTURE_BOUND`
   needs `ft[o:o+len(span)] == span`, so an honest span on S125 cannot pass; the only way to
   make it pass is a span file that is itself a slice of the ZIP bytes, i.e. a faked capture.
   Bind the other six (JSTAGE, JAOHFA, SLARC_A, SLARC_B, SINOMED, JAHBS ≥ `MIN_BOUND` 5) and
   refuse S125, or C2 cannot pass. The docx text itself is real and quotable (§3); only the
   frozen `form_text` cannot see it.
2. **S126 JAHBS is bindable**: `.txt` 25811 chars of PDF text carries 検索戦略 ×11 (5260),
   検索式 ×11 (6436), 検索期間 ×2 (10146); no register row, so no verdict is owed.

VERDICT: attacked the six theme-URL quarantine rows by hand against their `.qcache` captures — 2 `present` (S111, S120), 4 `absent-as-written` (S104, S105, S112, S114), 0 `fabricated`, 0 `unverifiable`, no register verdict blocks a bound document, and the NIPH `.docx` cannot be `CAPTURE_BOUND` under the frozen `form_text`.
