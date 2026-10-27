# R54W2CritEntailStb — entailment attack on source-type-taxonomy-r37.md (S123)

Seat: R54W2CritEntailStb. Attack: for every bullet under `#### Observation` and
`#### Inference` of `corpus/knowledge/source-type-taxonomy-r37.md`, is it entailed by the
quoted capture text form `0f33243fd7ac2fe88b85c1ba.txt` (83,061 chars, `wc -m` agrees with
the entry's "83,061 characters")? Method: verbatim substring checks (`t.count`, `t.find`)
plus context windows around every anchor; every `char N` in the `source:` line resolves
(`5576,5602,8881,11542,14096,4736,4812,4852,21382,2512,57965,58840,59201,2655,82465,82834`
— all OK; `21382` sits inside the `８．３．２ 著录格式` template opened at `21295`).

## Observation

- O1 reproduction/colophon/wrong glyph — ENTAILED. `２０２５－１２－０２发布` 1× @424,
  `２０２６－０７－０１实施` 1× @490, `本文件代替ＧＢ／Ｔ ７７１４—２０１５…` 1× @3602,
  `中国标准出版社出版发行` 1× @82465, `２０２５年１２月第１版`/`第１次印刷` 1× @82834/82846;
  `图书主要贵任者` 1× @21382 vs `主要责任者` 31×. Two narrowings (same fix as I6, below):
  "journal office's reproduction" is provenance (tier B), not on the text's face — its face
  is the issued print (title page + colophon); "it is an OCR" rests on one wrong glyph.
- O2 scope — ENTAILED. `本文件适用于作者和编制者著录参考文献。` 1× @5576;
  `本文件不适用于图书馆员、文献目录编制者以及索引编制者著录参考文献。` 1× @5602.
  Disclaimed triad = librarian / catalogue compiler / indexer, verbatim.
- O3 normative carrier after slash — ENTAILED. `文献类型标识、文献载体标识应按照附录Ａ著录。电子资源既应著录…文`
  1× @11542 (continuation `献载体标识。` confirmed next line); `“／”用于…、文献载体标识前。` 1× @8881;
  `附录Ａ（规范性）` 1× @2512 vs `附录Ｂ（资料性）` 1× @2655 — normative code appendix vs
  informative examples.
- O4 five carrier rows, microform new — ENTAILED. `电子资源载体和标识代码应按照表Ａ．２著录。` 1× @58840;
  table body @59025–59201 carries exactly 磁带 MT / 磁盘 DK / 光盘 CD / 联机网络 OL /
  `缩微资料（ｍｉｃｒｏｆｏｒｍ ｍａｔｅｒｉａｌｓ）` MM (five rows); `增加了电子资源载体“缩微资料”及其标识代码` 1× @4812;
  exact spaced `图书                          Ｍ` 1× @57965.
- O5 date rule — ENTAILED. `电子资源的创建日期、发布日期、修改日期、引用日期应按照“ＹＹＹＹ－ＭＭ－ＤＤ”格式，用阿拉伯数字` 1× @14096.

## Inference

- I1 same letter, differently named type — ENTAILED, hot spot cleared. The change list is a
  type RENAME list, not a letter reassignment — and that is what the bullet claims:
  `将“ＥＢ”代表的文献类型更改为“网站、网页”` 1× @4852 keeps the code ＥＢ while its named
  type changes; table Ａ．１ rows `网站、网页 ＥＢ` and `图书 Ｍ` @57965 show the same letters
  persisting in the current table. Two code-stable rename instances (ＥＢ; Ｍ for
  普通图书→图书 per `将文献类型“普通图书”“舆图”分别更改为“图书”“地图”` @4736, 1×).
- I2 scope separates writing from counting — OVERSTATED (one clause). `disclaims … what an
  index counts` is entailed (索引编制者 @5602), but "or for how a reference list is matched"
  is not: the scope sentence itself ends `…以及参考文献标引体系编制法。` @5561, and ch9
  `参考文献标引体系编制法` @50566 prescribes the in-text match conventions (`９．２ 顺序编码制`
  14×/first @2418; `著者－出版年制` 9×) — the standard DOES govern how citations are matched
  to list entries. Charitable reading ("matched" = deduped for counting) saves it; literal
  reading is contradicted by the quoted chapter. Smallest fix: delete `or for how a
  reference list is matched,` (and the mirror phrase stays correct: it says nothing about
  what a count is a count of).
- I3 normative vs informative evidence — ENTAILED. `附录Ａ（规范性）`/`附录Ｂ（资料性）` 1× each
  (@2512/@2655); TOC glosses B as `顺序编码制参考文献表著录格式示例` — an example table.
- I4 "carrier code describes storage, not access" — OVERSTATED (headline only). The
  definition `…信息存储在磁、光、电介质上` 1× @5982 covers storage media, but table Ａ．２'s
  `联机网络（ｏｎｌｉｎｅ） ＯＬ` 1× @59161 names a network/distribution carrier, not a storage
  medium — the bullet's own body concedes "one networked entry". The follow-on clause
  ("a carrier code alone carries no claim about how a lane read it") is fine. Smallest fix:
  headline → `A carrier code describes the resource's medium, not the reader's access`.
- I5 citation needs its year — ENTAILED. `２０２５－１２－０２发布`/`２０２６－０７－０１实施` 1× each;
  `本文件代替ＧＢ／Ｔ ７７１４—２０１５…` 1× @3602 plus title-page `代替ＧＢ／Ｔ ７７１４—２０１５`.
  The bare number ＧＢ／Ｔ ７７１４ is genuinely ambiguous without its year.
- I6 wrong glyph / "occasional" — ENTAILED but narrowed; OCR claim is the thinnest link.
  `贵` occurs 3× total: 贵州省 (10679, place name), 于贵瑞 (78811, surname), and the single
  wrong glyph @21386 — so "occasional" = n=1; "a wrong glyph" is the accurate wording. And
  one confusable substitution is consistent with a print typo as well as OCR; the Unknown
  section already concedes "OCR can lose or alter a glyph" as a possibility. Fixable wording,
  not a fabric.
- I7 normative references — ENTAILED. `ＧＢ／Ｔ ４８９４ 信息与文献 基础和术语` 1× @5751 inside
  ch2 `规范性引用文件` (plus two definitional uses @5836/@6865); `3469` 0×, `ＩＳＯ ６９０` 0×,
  `690` 0×, `文献载体标识` 32× — all four counts of the Unknown sweep reproduced exactly.

## Summary

Per bullet: O1–O5 entailed (O1 carries the two narrowings above); I1, I3, I5, I7 entailed;
I2 overstated in one clause ("how a reference list is matched" — contradicted by ch9
标引体系编制法 which the standard's own scope claims); I4 overstated in its headline only
(ＯＬ is a network carrier); I6 entailed with "occasional" narrowed to n=1 and "it is an OCR"
resting on one glyph. No fabricated quote, no wrong anchor, no invented count; every attack
the seat spec flagged survives the verbatim-substring test except the three flagged
wordings, all fixable in place without touching predicate, counter, or spans.

VERDICT: S123's entailment survives — 9/12 bullets fully entailed; I2 (one clause), I4
(headline) and I6 ("occasional", n=1) are narrowed-wording fixes, none fatal.
