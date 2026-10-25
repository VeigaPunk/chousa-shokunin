# GroundS103 — S102 re-ground (CNKI KNS8.0 利用ガイド, toho-shoten PDF capture)

Role: UFO-FSD scribe / leaf seat GroundS103, chousa round 49 wave 1. No subagents, no background jobs, no edits to any production file (only this report written). No installs performed: read `/home/vgpnk/.omp/agent/RULES.md` (tooling directive; channel order + pacman pause noted) — no tool needed, so no install record.

## Scope
Re-ground staged row S102: capture `…/.qcache/7809d5114330a60527436b07.txt` (and `.raw`). Staged entry: `…/merge/chousa/knowledge/corpus/knowledge/citation-count-semantics-r37.md`, source line: `source: S102 — https://www.toho-shoten.co.jp/export/sites/default/cnki/help/cnki-kns80.pdf — sections 5.4, 5.6.1 and 6.4 — PDF read 2026-10-23`. This report ground date: 2026-10-25.

## Capture inspection commands

`file …/7809d5114330a60527436b07.raw` →
`PDF document, version 1.7, 50 page(s)`; `ls -la` → `.txt` 30277 B (Oct 23 20:37), `.raw` 5066141 B (same pdf bytes). So `.raw` is a PDF, not UTF-16LE; the UTF-16LE fallback does not apply → the only text form is `.txt`.

Python (utf-8 decode, 17317 chars, 881 lines):
```
t = open('….txt','rb').read().decode('utf-8')   # OK, 17317 chars
t.count('被引频次') → 1;  t.find('被引频次') → 13027
```

## Quotes (all ≤25 whitespace words, ≤160 chars, byte-exact from .txt, each count=1)

| id | quote (byte-exact) | char offset (`text.find`) | line | words/chars |
|----|----|----|----|----|
| Q1 | 「发表时间」「被引」「下载」 | 13260 | 515 | 1 / 14 |
| Q2 | 「下载」はそれぞれ文献の公開時期、被引用回数、ダウンロード回数を示します。 | 13514 | 545 | 1 / 37 |
| Q3 | 第一单位、被引频次 20 項目を検索対象と | 13022 | 493 | 3 / 21 |
| Q4 | 当該文献を中心に年毎の参考、被引用の関係をビジュアルに提示、それぞれの文献にアクセスすることもで | 16123 | 760 | 1 / 48 |

Verified uniqueness by `t.count(q)==1` for each; offsets are Python char offsets in the decoded `.txt`. Section headings also unique: `5.4 专业检索` @12892 (line 484), `5.6.1 検索結果リスト` @13226 (line 513), `6.4 引文网络` @16113 (line 758).

Layout note: the gloss sentence spans lines 544–545; line 544 reads `\x0c「发表时间」「被引」` (page-break form feed) and line 545 has 9 leading layout spaces before `「下载」はそれぞれ…示します。`. Q2 cites the clean single-line tail; the leading span is `\x0c「发表时间」「被引」\n         「下载」はそれぞれ…示します。` (unique, not used as quote due to layout artifacts).

## Claim-by-claim verdict (staged entry vs capture)

The staged entry's claims resting on this row (Observation bullet 2, and the "被引/下载量" Inference bullet) and their support:

1. "the result list fields as 「发表时间」「被引」「下载」 giving respectively 公開時期, 被引用回数 and ダウンロード回数" — **supported**. The field tuple is verbatim in the 5.6.1 list (Q1 @13260, line 515: `検索結果には、「篇名」「作者」「刊名」「发表时间」「被引」「下载」の他…`). The Japanese gloss 公開時期 / 被引用回数 / ダウンロード回数 is the sentence whose tail is Q2 @13514 (line 545); the gloss wording matches the bullet. Minor caveat: the gloss sentence is split by a form feed/leading spaces (layout artifact), not by wording — no paraphrase needed, the doc states it.
2. "被引频次 is one of twenty searchable 专业检索 fields" — **supported**. Q3 @13022 (line 493) contains 被引频次 inside the 专业检索 field enumeration ending `被引频次 20 項目を検索対象とすることができます。` (20 fields searchable). The full enumeration wraps lines 492–494; 被引频次 occurs exactly once in the whole docs (offset 13027 within Q3).
3. "the 引文网络 view presents, for a given article, its yearly 参考 and 被引用 relations as a graph" — **supported**. Q4 @16123 (line 760): `当該文献を中心に年毎の参考、被引用の関係をビジュアルに提示、それぞれの文献にアクセスすることもできます。` — "yearly 参考/被引用 relations presented visually, centered on the article" (ビジュアルに提示 ⇒ "as a graph" is a fair reading of ビジュアル; the section is 6.4 引文网络, heading @16113). Not narrower, not contradicted.
4. Entry metadata "sections 5.4, 5.6.1 and 6.4" — all three headings present and unique (offsets above). "PDF read 2026-10-23" superseded by this ground date 2026-10-25.

No claim in the entry that rests on this row is narrower or unsupported.

## Absent-defect register check

`grep -E 'toho-shoten|7809d5114330a60527436b07|cnki-kns80' …/absent-defect-register.md` → no matches. No absent-defect register row names this URL.

## Draft Lane Gate block (row S102)

```
URL: https://www.toho-shoten.co.jp/export/sites/default/cnki/help/cnki-kns80.pdf
access: 2026-10-25
quotes:
  - "「发表时间」「被引」「下载」" @13260 (.txt)   [fields named in result list, sec 5.6.1]
  - "「下载」はそれぞれ文献の公開時期、被引用回数、ダウンロード回数を示します。" @13514 (.txt)  [gloss: 公開時期/被引用回数/ダウンロード回数]
  - "第一单位、被引频次 20 項目を検索対象と" @13022 (.txt)   [被引频次 among 20 专业检索 fields, sec 5.4]
  - "当該文献を中心に年毎の参考、被引用の関係をビジュアルに提示、それぞれの文献にアクセスすることもで" @16123 (.txt)  [引文网络 view, sec 6.4]
anchor: 5.4 专业检索 char 13022 | 5.6.1 検索結果リスト char 13260, 13514 | 6.4 引文网络 char 16113, 16123
```

## Limits
- `.raw` is the PDF itself; quotes are grounded only in the `.txt` extraction. No network; only on-disk captures (L0 question untouched).
- Q2 ignores the leading spaces / form feed on line 544 so the quote's copy stays byte-exact; the sentence-internal text is unchanged.

VERDICT: Re-grounded staged row S102 (CNKI KNS8.0 利用ガイド PDF capture) by document — drafted the Lane Gate block with 4 unique byte-exact quotes (offsets 13022/13260/13514/16123 in the .txt), verified the staged entry's three claims (result-list fields + gloss, 被引频次 among 专业检索 fields, 引文网络 view) all supported, and confirmed no absent-defect register row names this URL.
