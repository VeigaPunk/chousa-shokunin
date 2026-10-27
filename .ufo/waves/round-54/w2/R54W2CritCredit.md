# R54W2CritCredit — expansion/coverage credit at 447cf7e (integrated tip)

Axes attacked: operability (credit claims re-checkable by command), depth (does each row hold new sourced ground).
Scope: `corpus/README.md` "Round54 coverage and frontier", entries `source-type-taxonomy-r36.md`/`-r37.md`, rows S121–S123.
Base = `c49ffc6ce1c3de87c1dfa96856239ed7274bf07b`. Tip HEAD was `178667d`; `git merge-base --is-ancestor 447cf7e HEAD` → TIP_IS_ANCESTOR (W1 reports sit on top; the credit surface is unchanged since `6af11e9`).

## Base sweeps, run by this seat

URLs (whole tree at base — `git grep -l -e <frag> $B -- .`):
- `std.samr.gov.cn`, `openstd.samr.gov.cn`, `xuebaobangong.jmu.edu.cn`, `4507EFE…01F`, `C6CE52…DD14`, `64b9ba1b-…-497bd0`, `newGbInfo`, `gbDetailed` — **only** in `.ufo/waves/round-4{4,5,8,9}`/`-50`/`-53` seat logs, `staged-map.tsv`, `R53ScoutNextThemes.md`. Zero hits in `corpus/` — no Registry row, no knowledge file. Documents absent at base: TRUE (wave artifacts are not holdings; round-44 `QuarantineS080.md` re-checked the register row and the doc stayed refused).
- Terms in `corpus/knowledge` at base: `ISO 690:2021`, `文献载体标识`, `采标`, `非等效`, `全部代替`, `不提供文本阅读`, `2025-12-02`, `2026-07-01`, `TC4`, `全国信息与文献标准化技术委员会`, `附录Ａ`, `缩微资料`, `文献类型标识` — **0 files each**. Present already: `ISO 690`, `GB/T 7714`, `著录` (via `citation-count-semantics-r37.md` = HIT S101 instrument); `GB/T 7714-2025` (via `citation-version-binding-r36.md`, only as an unadopted staged row — `git show $B:corpus/knowledge/citation-version-binding-r36.md` line 21: "Staged S082… is not adopted. Round 43 classed that row not-carried"). No held ground to duplicate.

## Captures re-opened (`.qcache`, read-only)

`adf6ba93…150.txt` (S121, 3591 ch): `本标准非等效采用ISO国际标准：ISO 690:2021。`×1@1797, `发布 于 2025-12-02`×1@1029, `实施 于 2026-07-01`×1@1048, `（全部代替）`×1@1162, `由 TC4`×1@537, `查看文本`×1@3453, English title ×1@361. `不提供文本阅读`=0, `发布单位`=0, `归口部门`=0.
`b9ca2a4f…144.txt` (S122, 22007 ch): `由于涉及版权保护问题，本系统不提供文本阅读服务`×1@15212 (lead-in `该标准采用了ISO、IEC等…`@15188), `归口部门`→`国家标准委`, `发布单位`@16988→two-body issuer. `查看文本`=0.
`0f33243f…1ba.txt` (S123, 83061 ch): `文献类型标识、文献载体标识应按照附录Ａ著录。`×1@11542, `本文件不适用于图书馆员`×1@5602, `附录Ａ（规范性）`×1@2512, `图书主要贵任者`×1@21382, five carrier rows verified verbatim (`磁带（ｍａｇｎｅｔｉｃ ｔａｐｅ） ＭＴ` … `缩微资料（ｍｉｃｒｏｆｏｒｍ ｍａｔｅｒｉａｌｓ） ＭＭ` @~59025–59201).
Overlap: S122's number, English title, dates, CCS/ICS labels, both issuer names — ALL already in S121's form (`发布日期`/`实施日期`/`中国标准分类号`/`国际标准分类号`/`国家市场监督管理总局`/`国家标准化管理委员会`/`Information and documentation` each ≥1 in S121). S122's unique residue: the notice sentence + the `归口部门`/`发布单位` portal-only fields.

## Counter re-run

`python3 corpus/evidence/round54/c2-count.py --lane-only` (PYTHONDONTWRITEBYTECODE=1, TMPDIR=scratch): `ENTRIES=2/2 BOUND=3/3 (S121,S122,S123) NEW_GROUND=2/2 QUOTE_ROWS=33 ON_BOUND=33/33 SPAN_IDS=3/3 SUBSTANCE=PASS ANCHOR_BOUND=3/3 INFERENCE_GROUNDED=2/2 QUARANTINE_VERDICTS=3/3 (S080,S088,S096) C2=PASS` exit 0. `grep -no 'S[0-9]{3}'` on entries: r36={S121,S122}, r37={S123} — S101 uncited (E3 holds; README "earns none" accurate). spans.tsv: 6/6/21 rows per id.

## Per-document verdicts

- **S121 (SAMR record) — CREDIT YES.** Never a lane document; the register S080/staged S082 row was a `payload-absent`/`absent-as-written` defect on a fabricated joined span (`QuarantineS080.md`, `W2CritS082.md` "stays refused, not-carried 19/50"), not a held row. New authority-tier facts verified above (adoption basis, two dates, 全部代替 block, TC4). README "refused as staged S082 in rounds 43-44" — accurate.
- **S122 (openstd notice) — CREDIT YES, thin.** One-unique-sentence document: the no-text-reading notice occurs 0 times in S121 and grounds r36 Obs-5, Inf-3 and the narrowed headline (portal's service statement, not "text unreadable"); plus the portal-only `归口部门` value the entry uses for the read-fields-where-printed rule. Everything else is a second carrier of S121. Defensible by the S119 precedent ("credited because it alone carries the issuance facts"); a row is warranted because merging it into S121's row would mix two URLs' provenance (spans.tsv has 6 distinct S122 quote rows). Weakest of the three — held by one sentence, but that sentence is real new ground the entry spends.
- **S123 (JMU reproduction) — CREDIT YES, strongest.** First lane carrier of the standard's operative text: scope clause + exclusions, normative `附录Ａ` vs informative `附录Ｂ`, five-row carrier table with new microform row, change-list renames, date rule, colophon, OCR witness. Held S101 only *defers to* the standard (14.1/14.4, one `文献类型及载体类型标志` element) — not a second carrier of this ground. Tier B scoped correctly.

## Does the README claim more than the entries hold?

- "Source-tier adjudication advanced": **substantively supported** (tier-A-scoped identity pages vs tier-B reproduction, adjudicated per fact — r36 Inf-6, r37 header/Obs-1). **One fixable wording defect**: "the standard's own scope clause keeps the form axis … apart from the tier axis" misattributes the separation. The scope clause separates 著录-writers from librarians/cataloguers/indexers (r37 Obs-2/Inf-2 — an applicability axis); the type-vs-tier point is r36 Inf-6 and is driven by the type table's absence from the authority pages, not by the scope clause. Smallest correction: replace "the standard's own scope clause keeps" with "its normative-appendix status and scope clause keep the form axis … apart from the tier axis" or cite r36's own observation.
- "three documents absent at the base" — true under the lane's own convention (no row, no knowledge file); caveat for the record: all three URLs existed in tracked `.ufo` wave artifacts at base (they were scouted and refused, never held). README itself discloses the refusal history — no overclaim.
- Table "Holds" cells: spot-checked verbatim against captures — all claims located (offsets within one line of stated chars; r36's `char 15188`/`char 15212` difference is lead-in vs substring, both present).

VERDICT: attacked expansion credit on README + two entries + rows S121–S123 — credit survives for all three documents (S122 thin but uniquely carrying the service-notice fact); README survives except one fixable scope-clause misattribution in the Frontier bullet.
