# R54ReviewProvince — province and QUALITY bar per entry and per document (round 54, w1)

Seat: non-author review of the GB/T 7714-2025 theme as landed (`corpus/knowledge/source-type-taxonomy-r36.md`,
`…-r37.md`, `corpus/SOURCES.md:131-133`, `corpus/lessons/round-54.md`). I read the frozen claims, PROVINCE.md,
QUALITY.md 1-96, the README coverage map and the two staged package entries, then re-grounded every claim
from capture bytes. Tooling: `uv run --with pypdf` (pypdf fetched into uv's cache; nothing installed system-wide,
no PATH write).

## 1. Province — per entry

- **`r36` (S121 + S122): in province.** The spine is source hierarchy — what an authority's own record proves
  about a standard and where that proof stops (`S121` gives identity/status/dates/adoption; neither form holds a
  clause or a type code: `附录`,`文献类型`,`载体标识`,`[M]`,`EB/OL` each count 0 in both). That is chousa's
  owned ground (`PROVINCE.md:5-7`: "source hierarchy …; citation chaining and hop resolution; claim-vs-source
  verification").
- **`r37` (S123): in province, spine-method only.** Its Observation is the standard's content (scope clause, code
  tables, change list, date rule); its six Inference bullets are method claims (form-vs-authority, normative vs
  informative appendix status, code-vs-edition resolution, reproduction-vs-authority typography). In province
  because the subject is cited as evidence for the lane's source hierarchy, not as bibliography.
- **Sibling ground: none.** `grep -nEi '参考文献|著录|bibliograph|reference format|citation standard|ISO 690|7714|citation chaining'` over every
  sibling `*/PROVINCE.md` returns no hit (the only "standard" hits elsewhere are kaidoku's SquashFS/ISO filesystem
  standards and kengaku's preregistration standard — unrelated). kengaku's own PROVINCE hands the ground here:
  `kengaku-shokunin/PROVINCE.md:137` — "the question → source-hierarchy → citation-chain → claim-vs-source
  method stays chousa's". No sibling competing claim; not out-of-province.

## 2. Per document — verdicts

| doc | id | tier | verdict |
|---|---|---|---|
| SAMR detail record | S121 | A | **register, A for identity/status/adoption basis.** Verified in `adf6ba934e813b2c326fa150.txt` (3,591 chars): `发布 于 2025-12-02` (1029), `实施 于 2026-07-01` (1048), `（全部代替）` (1163), `本标准非等效采用ISO国际标准：ISO 690:2021。` (1797), `采标中文名称:…引用指南。` (1829), CCS `A14` (1517), ICS `01.140.20`. Scope must stay identity-only — no clause text is in the form. |
| openstd portal page | S122 | A | **register, A for "what the portal itself serves and why".** `该标准采用了ISO、IEC等国际国外组织的标准，由于涉及版权保护问题，本系统不提供文本阅读服务` once at 15188 in a 22,007-char form that is the served HTML itself (`.txt` digest `2d68faf7…` = the `.raw`'s; the row and lesson both say so). The landed narrowing — the notice is about `本系统`, not the document — is correct and is the round's best QUALITY-8 move. |
| JMU journal-office PDF | S123 | **B** | **register, B, scoped to the reproduction and never to the issued standard** — see §3. |
| HIT data specification `.doc` | S101 (held) | B | **not carried this round is correct, but the stated reason is only half true.** `tools/capture-text.py <6dc68fd6…raw>` → rc 0, 27,012 chars, 0 U+FFFD, and it locates S101's quotes at 11972/12007/12795/12963/14049/25123. So the *form* is defined at this landing (C1); what is missing is the C2 **builder** (`build-spans.raw_form` still decodes UTF-16LE). `r37`'s Unknown says "the round-54 span builder has no OLE text form" (true) but also "the form round 54 found undefined" — that is true only of the UTF-16LE whole-file decode, not of the OLE form. Reword to "the builder does not read the OLE form". |

## 3. The seat's tier question — is a journal office's copy of a copyrighted standard a carrier to register, B or C, and what supports fidelity?

**Verdict: register it, tier B; never A, and C would be wrong.** Evidence, all from on-disk bytes:

- The copy is a complete reproduction of the issued print, not a summary: title page `ＧＢ／Ｔ ７７１４—２０２５`,
  `代替ＧＢ／Ｔ ７７１４—２０１５`, `２０２５－１２－０２发布` (424) / `２０２６－０７－０１实施` (490); preface
  `本文件代替ＧＢ／Ｔ ７７１４—２０１５《信息与文献 参考文献著录规则》` (3602); publisher colophon
  `中国标准出版社出版发行` (82465) and `２０２５年１２月第１版 ２０２５年１２月第１次印刷` (82834); appendices
  marked `附录Ａ（规范性）` (2512) vs `附录Ｂ（资料性）` (2655).
- **What supports fidelity to the issued text:** (i) the copy's identity fields agree field-for-field with the
  tier-A authority record (number, both dates, replacement relation, ICS 01.140.20, CCS A14, issuing bodies) —
  two independent carriers agreeing; (ii) the colophon and imprint line show it is a rendering of the printed
  edition; (iii) **and that is all** — the copy is an *OCR* of that print: `图书主要贵任者` at 21384 (责 misread)
  while `主要责任者` occurs 31×, and two extractors disagree on width (`pdftotext` fullwidth vs pypdf halfwidth).
  No collation against an entitled copy exists, and the authority serves none. So B for "what this copy carries",
  never A, and the clause text may not be presented as the authority's typography (the entry says so).
- **Why not C:** the lane grades a third-party-hosted copy of an authoritative document B by precedent —
  S100/S101/S103/S105/S106 (university-hosted Chinese copies) and S118/S119 ("the document is the centre's but
  the carrier is a professional society's file host, so the tier is B"). C would also make the entry's clause
  claims inadmissible under QUALITY 7 (no A source serves this text), i.e. it would refuse the entry rather than
  grade it. The copyright position is the carrier's, not the lane's: the lane registers a URL and ≤25-word spans,
  and the row's scope already says "scoped to the reproduction and never to the issued standard".

## 4. QUALITY-bar findings on the landed bytes (actionable, none of them a request to change the frozen predicate)

1. **S123's anchor cell misdescribes its location (criterion 6, exact anchor).** `corpus/SOURCES.md:133` says
   "the 附录Ａ 表A.1 rows marked 电子资源必备". `电子资源必备` occurs 25× in the form and **none** inside
   表A.1(57879)–表A.2(58955); the marker belongs to the per-type 著录项目 tables (first at 17653, `表１ 图书著录项目`).
   表A.1 has a 类型/代码 pair, no 必备性 column. The three offsets (5576/5602/11542) are correct; the descriptive
   clause is not. Fix the cell text.
2. **QUALITY 96 is met only with an added NFKC fold, and the round must say so.** `pdf-crosscheck.py` prints
   `PDF_QUOTES=21 NOT_IN_INDEPENDENT=0 RAW_NOT_IN=14` — 14 of 21 S123 quotes do **not** occur in the independent
   pypdf extraction as printed; they occur only after width folding (`磁带（ｍａｇｎｅｔｉｃ ｔａｐｅ）` → pypdf `-1`;
   附录Ａ → pypdf `-1`). The tool prints `RAW_NOT_IN`, which is honest, but criterion 96 does not name a fold —
   record the fold as a QUALITY narrowing, or the criterion reads as satisfied when it is satisfied modulo NFKC.
3. **One S123 quote is an extractor artefact by construction.** `图书                          Ｍ` (span row) carries
   26 spaces that only `pdftotext -layout` produces; its substance is 3 characters. It survives the cross-check
   only whitespace-removed. Acceptable as a table row, but it is a layout reading, not the PDF's print run — the
   entry's own Unknown already concedes the general point.
4. **One S121 claim has an offset but no span.** The entry asserts `现行` twice (chars 489, 1261) for "in force",
   yet the six S121 span rows are `推荐性`, `由 TC4…归口`, `发布 于…`, `实施 于…`, `（全部代替）`,
   `本标准非等效采用…` — no `现行` row, and `推荐性` (3 chars) sits exactly on the QUALITY-72 substance floor.
   The claim is re-derivable from the stated offsets; it is not span-backed.
5. **The nine re-anchoring corrections are indirection, not repair.** `SCORECARD.md:2740-2748` carries nine
   `correction: corpus/SOURCES.md:110|111 charN->charM -> corpus/evidence/round54/S1xx-text-form.txt` lines; I
   re-ran each anchor and all nine land exactly (`11972` `为便于文献的统计和期刊评价`; `12963`
   `文献类型及载体类型标志；`; `14049` `参照ISO 690及ISO 690-2`; `16` `中国知网他引频次的查询需要使用《中国引文数据库》。`).
   Residual risk: `SOURCES.md:110-111` still **print** the undefined-form offsets, so a reader of the registry
   alone gets wrong numbers, and the corrections name rows by line number (criterion 83's known limit — an
   insertion above shifts them).
6. **Recheck commands are host-absolute.** Both entries' `recheck:` commands hardcode
   `/home/vgpnk/Projects/shokuknow/...`; criterion 13's named check does not fire (no `--root` argument), but
   the commands are not placement-independent. Both reproduce: r36 prints `1 1797 1 15212`, r37 prints `11542 32`.

## 5. What I re-derived and found correct (so the L1 need not re-check these)

- Every `char N` in both entries lands exactly on its claimed string: 23 in `r36` (S121 537/1029/1048/1162/1787/
  1797/1829/575/1759/2993/477/489/1261/3453; S122 13300/14082/15188/17078/16726/16815/16638/16105/16321) and
  16 in `r37` (5576/5602/8881/11542/14096/4736/4812/4852/21382/2512/57965/58840/59201/2655/82465/82834).
- `r36`'s sweep prints `3591 22007` and the two count vectors as written; `著录`'s five record contexts are the
  title ×4 (354, 521, 1191, 1281) plus `标准文献题录著录规则` (2993) — as claimed.
- `r37`'s counts: `主要责任者` 31×, `主要贵任者` 1× (21384), `文献载体标识` 32×, `ＧＢ／Ｔ ４８９４` present,
  `3469`/`ISO 690` 0× — as claimed; `ＹＹＹＹ－ＭＭ－ＤＤ` is the capture's own rendering (not ＭＯＮＴＨ).
- `python3 corpus/evidence/round29/prose-check.py` on both entries + the lesson → `TOTAL hits=0 files=3`, rc 0.
- `python3 corpus/evidence/round54/c2-count.py` → `C2=PASS` rc 0 (`BOUND=3/3`, `REF_ID_UNBOUND=0`,
  `SUBSTANCE=PASS`, `ANCHOR_BOUND=3/3`, `INFERENCE_GROUNDED=2/2`, `QUARANTINE_VERDICTS=3/3`,
  `QUARANTINE_BLOCKED_ADOPTED=0`), and `--lane-only` likewise. No stray `S###` token: `r36`={S121,S122},
  `r37`={S123} only (the staged `S075` body token is gone).
- Quarantine verdicts agree with my own hand-check of the three register rows (`S080`/`S088`/`S096` all
  `absent-as-written`: the register quotes are cell/row/ellipsis glues, each component present once — e.g.
  `磁带（ｍａｇｎｅｔｉｃ ｔａｐｅ）` 59025, `缩微资料（ｍｉｃｒｏｆｏｒｍ ｍａｔｅｒｉａｌｓ）` 59201; the S080 joined string
  occurs 0× and `标准号：` 0×). None is `fabricated` or `unverifiable`.

VERDICT — attacked the province/tier question for the GB/T 7714-2025 theme and both staged entries against the
landed bytes: both entries are in province with no sibling claim; the JMU copy is correctly tier B (register,
scoped to the reproduction — fidelity rests on identity agreement with the tier-A record plus imprint/colophon,
and the copy is a disclosed OCR, so never A; C would refuse the entry, not grade it); six QUALITY-bar defects are
reported unfixed (S123 anchor-cell misdescription, the unrecorded NFKC fold under criterion 96, the layout-only
`图书 … Ｍ` quote, the unspanned `现行` claim, registry anchors still printing undefined-form offsets, host-absolute
recheck commands); every offset, sweep, count and the frozen C2 counter check as claimed.
