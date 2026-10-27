# R54W2CritEntailSta — entailment attack on source-type-taxonomy-r36.md

Scope: every bullet under `#### Observation` (O1–O7) and `#### Inference` (I1–I5) of
`corpus/knowledge/source-type-taxonomy-r36.md` vs captures
`a = .qcache/adf6ba934e813b2c326fa150.txt` (S121 record, len 3591) and
`b = .qcache/b9ca2a4fdf9455867534f144.txt` (S122 portal, len 22007), verified by
`str.find`/`str.count` and context windows (scripts run under scratch, no writes to lane or cache).

Method: `python3` on-disk reads only; all offsets/counts below are observed, not quoted from the entry.
Spelling note: every `char N` in the entry was recomputed; all match except ONE case noted at O4.

## Observation

- **O1 (record fixes number/status/dates)** — ENTAILED. `GB/T 7714-2025` count 2 @1239,1333
  (2nd inside `当前标准` block); `发布 于 2025-12-02` count 1 @1029, `实施 于 2026-07-01` count 1 @1048,
  both inside the `标准状态` block; `现行` count 2 @489,1261 (title badge + `当前标准` badge);
  `推荐性` count 1 @477 as badge `国家标准 推荐性 现行` above the title. "recommended national
  standard in force" is a sound gloss: 推荐性=recommended, 现行=in force (impl. date 2026-07-01 ≤
  today). No scope words exceeded.
- **O2 (replacement is a block, not a sentence)** — ENTAILED. `（全部代替）` count 1 @1162 sits under
  `代替了以下标准` with `GB/T 7714-2015` ~3 lines above; 2015-designator count 2 @1136,1426;
  `全部代替` count 2 @1163,1415 — BUT the second is inside field label `全部代替标准` @1415, i.e.
  the qualifier itself occurs once as qualifier and once inside a label. The bullet's point
  (neither string quotable whole/uniquely) still stands. Minor nuance, not a defect.
- **O3 (adoption basis is a labelled field)** — ENTAILED. `采标情况` @1787, sentence @1797 count 1,
  `采标中文名称:…引用指南。` @1829 count 1 on the next non-blank line; `ISO 690` count 1, `690` count 1.
- **O4 (committee vs supervising dept)** — ENTAILED, one anchor ambiguous. `由 TC4 （全国…委员会）归口`
  count 1 @537; byline continues `主管部门为 国家标准委` @569 — the bullet writes "char 575", which
  is the offset of the value `国家标准委`, not of the quoted phrase (569). Every other `char N` in
  the entry points at the start of the quoted span; this one is a quote/anchor ambiguity (off by 6).
  基础信息 triple confirmed: `归口单位`→`全国信息与文献标准化技术委员会` @1699, `执行单位` same @1730,
  `主管部门`→`国家标准委` @1759.
- **O5 (portal serves record fields, states no text reading)** — ENTAILED. Notice
  `该标准采用了ISO、IEC等国际国外组织的标准，由于涉及版权保护问题，本系统不提供文本阅读服务`
  count 1 @15188, emitted under the record table in a `text-danger` span next to the per-standard
  实施信息反馈 button — per-standard, not global chrome. `标准号：GB/T 7714-2025` @13300,
  `英文标准名称：Information and documentation—Rules…` @14082 (count 1), 发布日期/实施日期 as
  separate label/value divs with values `2025-12-02` @16105 and `2026-07-01` @16321 (count 1 each),
  `国家市场监督管理总局、国家标准化管理委员会` @17078 as `发布单位` value (count 1).
  "serves no text reading" stays within `不提供文本阅读服务` (the notice denies the *service*, and
  the bullet says exactly that).
- **O6 (different 归口 body on the two pages)** — ENTAILED. S121 `归口单位`=`全国信息与文献标准化技术委员会`
  (portal occurrence count 0); portal `归口部门` label @16726 → value `国家标准委` @16815, and
  `主管部门` value `国家标准委` @16638. `国家标准委` count 2 in b — "not quotable there" correct
  (`国家标准化管理委员会` count 3 is a different string).
- **O7 (no clause/type code in either form)** — ENTAILED. `附录, 文献类型, 文献类型标识, 载体标识,
  [M], [J], EB/OL` all count 0 in both forms (reproduced the `#### Unknown` sweep byte-for-byte:
  lengths 3591/22007 and both count vectors identical). `著录` count 5 in a: 4 inside
  `信息与文献 参考文献著录规则` (count 4 @344,511,1181,1271 — each title holds 著录 at +10) and the
  5th inside `DB44/T 751-2010 标准文献题录著录规则` @2993, under header `相近标准(计划)` @2651 —
  "a related standard's title in the 相近标准 list" exact. `著录` in b count 1 @13794 (its title line).

## Inference

- **I1 (record proves fields, not clauses)** — ENTAILED for its evidence half; the lane-scope
  negative ("no readable authority source in this lane's captures") is a lane claim, hedged
  correctly to captures, and the normative tail ("no lane row should quote…") is policy, not text.
- **I2 (dates repeat; only one page carries the block)** — ENTAILED. Portal has `GB/T 7714-2015`
  and `代替` count 0 — stronger than claimed. Nitpick: "`（全部代替）` between the two editions'
  designators" is positionally true (1162 lies between 2015@1136 and 2025@1239) but semantically
  loose: the qualifier attaches to the 2015 entry under `代替了以下标准`; the 2025 designator lives
  in the separate `当前标准` block. "beneath the 2015 designator" would be tighter.
- **I3 (notice is about the system's service)** — ENTAILED in its positive half, then OVERSTATED by
  one line. `查看文本` count 1 @3453 (bare label; markup is stripped, so "control" is a mild UI
  inference, hedged by "target this round did not open"). But "the stronger claim that the text is
  unavailable **belongs to no line here**" is falsified inside capture b itself: the embedded i18n
  map at @1712 carries `'noFullText': '该标准暂无全文，请等待更新'` (count 1; en counterpart
  'Full Text…' also present) — a line asserting precisely that the standard has no full text.
  It is a latent UI template (generic, not displayed for this standard), so the fix is scoping, not
  deletion: "belongs to no *displayed* line here" / "no rendered line".
- **I4 (fields read where printed)** — ENTAILED. `归口单位` vs `归口部门` are distinct labels;
  values differ across pages as observed in O6.
- **I5 (tier judgement about scope)** — MOSTLY ENTAILED; one unhedged presupposition. "the authority
  … issuer printed there" entailed (@17078). "the taxonomy is not in either capture" entailed
  (sweep 0s). But "the document-type taxonomy the standard **prescribes**" asserts in the indicative
  what S121/S122 never show — I1 itself hedged this as "said to prescribe". The r37 entry's S123
  (`附录Ａ（规范性） 文献类型和文献载体标识代码`, spans.tsv row 28) corroborates it from a
  non-authority copy, but the entailment target here is the two captures: mark overstated-in-mode;
  narrow "prescribes" → "said to prescribe" for internal consistency.

## Cross-cutting findings

1. `verified-at` line: "every quoted phrase re-located … (count 1 each)" is literally over-broad —
   only the 11 anchor/span quotes are count-1; other quoted tokens repeat (`国家标准委`×2 in b,
   `全国信息与文献标准化技术委员会`×3, `国家市场监督管理总局`×4 in a). All 11 span quotes verified
   count-1, single-line, at offsets consistent with spans.tsv slice starts (e.g. S121-2 457→537,
   S122-3 15108→15188). Smallest fix: "every anchor quote".
2. Anchor convention slip at O4: `主管部门为 国家标准委` is found at 569, cited "char 575"
   (the value's offset). Either cite 569 for the phrase or quote `国家标准委` for 575.
3. The S122 capture never prints `国家标准全文公开系统` (count 0); it self-labels
   `全国标准信息公共服务平台` @11716 and embeds `在线预览`/`下载标准`/`noFullText` i18n keys.
   The entry's "full-text portal" naming rests on the URL + i18n strings — defensible, but the
   latent `该标准暂无全文` string is exactly the finding in I3.
4. `废止` appears once @~1075 inside the `标准状态` block (likely a legend/status option); it does
   not defeat `现行`@489,1261 — record presents current. No action.
5. Portal carries `现行`@14510 for this standard — an extra "in force" datum the entry doesn't use;
   the claim is stronger than drafted, not weaker.

VERDICT: entailment of source-type-taxonomy-r36.md attacked — 7/7 observations entailed; inference
survives 4/5 cleanly with I3 OVERSTATED (latent i18n line `该标准暂无全文，请等待更新` @b:1712 falsifies
"belongs to no line here"; scope to displayed lines) and I5 carrying an unhedged "prescribes";
plus one 6-char anchor slip (O4) and an over-broad `verified-at` quantifier — the claim survives,
three wording narrowings recommended.
