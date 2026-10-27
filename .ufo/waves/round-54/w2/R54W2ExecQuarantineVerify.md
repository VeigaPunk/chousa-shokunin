# R54W2ExecQuarantineVerify — the three round-54 quarantine verdicts, re-derived

Leaf executor, wave 2 (FALSIFY), lane `chousa-shokunin`. HEAD at read time `178667d` (parent = the assignment's integration tip `447cf7e`); re-checked at `25abbe8`: `tools/capture-text.py` still `2c0140bc…`, `corpus/lessons/round-54.md` unchanged since `6af11e9`. Read only the register and `.qcache`; wrote this file only; claims `5a1a206` + erratum E1–E4 read first, nothing frozen proposed for change.
**Stake:** `round-54.md:55-58` calls S080/S088/S096 `absent-as-written`; those three lines are all of C2's `QUARANTINE_VERDICTS=3/3` leg (`c2-count.py:84,289`, `VERDICT_RE` over lesson text), so a mis-called label leaves the counter green and the prose wrong.

## Pins and method

```
$ sha256sum tools/capture-text.py
2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573  tools/capture-text.py  (tip, E2 in)
$ sha256sum .qcache/adf6ba934e813b2c326fa150.txt .qcache/0f33243fd7ac2fe88b85c1ba.txt \
            .qcache/6dc68fd6b32ce9c8dfcebce8.raw
4e46154f4a841d17d858eafb5c0099257030f301daadcaa30c37f2e668fb7138  adf6ba….txt  6,626 B → 3,591 chars
13a34aa9bb107eefeb8bed6a50a0d574af84ff77a66940e8b88ea895fea1182f  0f3324….txt 190,614 B → 83,061 chars
6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3  6dc68f….raw 129,024 B
$ python3 tools/capture-text.py .qcache/6dc68fd6b32ce9c8dfcebce8.raw > $S/s096.txt   # exit 0
chars: 27012  FFFD: 0  ctrl(other than tab/nl): []  sha256 a8e3e7ad213b6ec50479542cda23612e7ae7ae5f… (47,356 B)
```

Offsets are Python `str` indices into the form named. `fold(s,drop)` = NFKC → delete all whitespace → delete each char of `drop`, on **both** quote and form, so a hit means *only* those separators differ; the reported raw span is where the hit lands in the form.

## Row 1 — S080 (SAMR record) — form: S121 `.txt`

Quote (`absent-defect-register.md:38`): `标准号：GB/T 7714-2025 发布日期：2025-12-02 实施日期：2026-07-01`.

```
joined count: 0    '标准号：' 0   '发布日期：' 0   '实施日期：' 0
labels: 标准号 1  发布日期 1  实施日期 1    values: GB/T 7714-2025 2  2025-12-02 2  2026-07-01 2
S121[1029:1046] = '发布 于 2025-12-02 \n'     S121[1048:1065] = '实施 于 2026-07-01 \n'
S121[1327:1400] = '标准号 \n GB/T 7714-2025 \n \n \n 发布日期 \n 2025-12-02 \n \n \n \n \n 实施日期 \n \n 2026-07-0'
fold(NFKC+nows, ':' dropped both sides): 1 hit, raw span 1327..1400     fold(':' kept): 0
```

**Holds only literally; both offsets exact.** `1029`/`1048` are the `发布 于 …`/`实施 于 …` cells; the 基础信息 table at `1327` reads `标准号 | GB/T 7714-2025 | 发布日期 | 2025-12-02 | 实施日期 | 2026-07-01` — the register's four label/value pairs in order, same labels and values, with a fullwidth `：` (×3) where the page renders a space. Separator-only: fold hits **once**. The lesson's `标准号：`=0 holds. **Better called `present` (substance)**; the differing part is the invented `：` (count 3). The lesson's `each once` is falsified — each value occurs **twice** (标准状态 1034/1053; 基础信息 1361/1391, `GB/T 7714-2025` 1239/1333).

## Row 2 — S088 (JMU copy of GB/T 7714-2025) — form: S123 `.txt`

Quote (`absent-defect-register.md:42`): five `名称（ｌａｔｉｎ）代码` items slash-joined.

```
joined count: 0 ; each register part (name+code contiguous): 0 0 0 0 0
name offsets: 磁带… 59025  磁盘… 59073  光盘… 59116  联机网络… 59161  缩微资料… 59201  (each count 1)
rows of 表Ａ．２ at S123[59021:59242] (title at 58955, count 1):
'    磁带（ｍａｇｎｅｔｉｃ ｔａｐｅ）                     ＭＴ'      '缩微资料（ｍｉｃｒｏｆｏｒｍ ｍａｔｅｒｉａｌｓ）                 ＭＭ'
fold(nows, '/' dropped both sides): 1 hit, raw span 59025..59244 ; fold('/' kept): 0
```

**Holds only literally; both offsets exact** (59025 = name start, 59201 = 5th row). The five rows carry name **and** code on the same visual line, in the register's order, name and code split by a whitespace column, rows by newline. Separator-only → **better called `present` (substance)**. Differing parts with counts: ` / ` ×4 invented, newline ×4 → ` / `, whitespace column ×5 → deletion. Not `fabricated`: five names 1×, five codes once each on their own rows.

## Row 3 — S096 (HIT data specification `.doc`) — form: `capture-text.py` OLE output

Quote (`absent-defect-register.md:46`), three `<br>` parts, in the 27,012-char form:

```
q1 (主要责任者…文献标准编号(ISBN，ISSN，……)) count 0
q2 (根据GB3469规定，以单字母方式标识以下各种参考文献类型) count 1  @336
q3 (参考文献格式，参照 GB/T 7714，采用…顺序编码制；作者-出版年制) count 0
'参考文献格式，参照ISO 690' count 1 @25123   '参照 GB/T 7714' count 0 (folded 参照GB/T7714 also 0)
'GB/T 7714' count 4 @12802,12829,15164,21403  (@12802 = '本规范推荐采用GB/T 7714中规定的顺序编码制格式著录')
S096[25123:25140] = '参考文献格式，参照ISO 690，'
q1 segments (after NFKC+nows / also '、' dropped, both sides): 主要责任者 17/17 · 文献题名 18/18 ·
  文献类型及载体类型标志 1/1 · 其他责任者 5/5 · 版本（初版省略） 2/2 ·
  出版项（出版地出版者出版年） 0/2 · 文献出处或电子文献的可获得地址 2/2 · 文献起止页码 4/4 ·
  文献标准编号(ISBN，ISSN， 2/2
```

**Reproduces, offsets and counts exact** — the only one of the three that does. 27,012 chars and 0 U+FFFD match the lesson; `参考文献格式，参照ISO 690` sits at char **25123** as cited; q2 is verbatim. q1 splices the document's own two renderings of one 著录项目 list — the 1.2 table (`e．版本（初版省略）；`, `i. 文献标准编号(ISBN，ISSN，……)。` carrying the register's fullwidth comma and doubled ellipsis, chars ~200-300) and the 14.2 prose list (`c. 文献类型及载体类型标志；` — 标志 here, 标识 in 1.2) — with list letters and `、` elided. q3 splices 14.1's `推荐采用GB/T 7714…` into 15.7's `参考文献格式` clause and **substitutes the standard number**: nothing says `参照 GB/T 7714` (0), the row says `参照ISO 690` (1 @25123). Cosmetic: 15.7 belongs to `15 期刊基本参数(Serial parameters)` (24572), a clause not a "table".
**Kept `absent-as-written`** — a value substitution no separator rule repairs. **`fabricated` would be wrong**: every clause exists here (17× `主要责任者`, the ISO row, `GB/T 7714` 4×); the row's reason string ("the quote is in none of them") is falsified at part level for q2 and q1's tail — the prose overreach round 48 found on S093, not fabrication.

## Re-call

The lane's only adjudicated precedent is the round-48 closure ruling on S093 (`corpus/lessons/round-48-verifier-spotcheck.md:56`): *"a quote whose every word occurs verbatim, in order, with only layout interleaves between, is present"*; the byte-exact miss "mis-classifies the row under that convention". S080/S088 are stronger cases — no foreign interleaves, every part present, only joiners differ (fold hit 1 each) — so `round-54.md:55-56` labels `absent-as-written` for the reason round 48 overruled. Recorded inconsistency, not a new rule: relabel S080/S088 `present`, or retire the S093 precedent; both cannot stand.

- S080 → `present`: invented `：` ×3; four label/value cells in order; values 2× each.
- S088 → `present`: ` / ` ×4 invented, whitespace-column join ×5; five rows in order, names 1× each.
- S096 → `absent-as-written` stands: `参照 GB/T 7714` has no source (0); source `参照ISO 690` 1 @25123.

## Counter interaction (why C2 survives a relabel)

`c2-count.py:266-272` builds `reg_ids` from the register and `verdicts` from `VERDICT_RE` over the lesson, gating on `len(verdicts) == len(reg_ids)` and on no bound doc being `fabricated`/`unverifiable`. The label is never re-derived, so a mis-call passes and a correct relabel also passes. I did not run the counter (parent gate); I re-derived its slice with its own filter:

```
chousa data rows: 24
theme hits: 3    ('S080','round1','S121') ('S088','round2','S123') ('S096','round2','S101')
```

So `QUARANTINE_VERDICTS=3/3` and the lesson's "24 data rows … 3 at the freeze" reproduce. The S096 register row's URL is the `.doc` the lane holds as S101 (`c2-count.py:72 HELD`) — consistent with E3's cut, no double-cite.

## Defects, each naming what it attacks

| # | defect | attacks |
|---|---|---|
| D1 | S080 `absent-as-written` though separator-only (`：`×3), fold hit 1, parts in order | C2's verdict lines; contradicts round-48 `present`-as-substance. Fix: relabel `present` |
| D2 | S088 `absent-as-written` though separator-only (` / `×4 + column join ×5), fold hit 1 | same as D1 |
| D3 | `round-54.md:55` "each once" — each value occurs 2× (1034/1361, 1053/1391, 1239/1333) | a hand-checked count; cited offsets 1029/1048 are exact |
| D4 | "parameter table" for the ISO-690 row — 15.7 of `期刊基本参数` (24572), a clause | cosmetic; the offset is exact |
| — | S096: 27,012 chars, 0 U+FFFD, no control chars, `参照ISO 690`@25123, `参照 GB/T 7714`=0 | **survived** |

## Scratch

`/fast/scratch/hyaku/chousa-r54/R54W2ExecQuarantineVerify` held only `s096.txt` (sha256 above) and is removed (verified absent). No LibreOffice run, no fixture repo, no counter run: no `__pycache__`, no `soffice.bin`. No production file, index, jj state or PATH entry touched.

VERDICT — attacked the three round-54 quarantine verdicts: **S096 survives fully** (27,012 chars, 0 U+FFFD, `参照ISO 690`@25123, `参照 GB/T 7714`=0, not `fabricated`); **S080 and S088 do not survive their label** — both separator-only and better called `present` (fold hits 1 each, all parts in order; S080's values 2× each, so "each once" is wrong); all five cited offsets (1029, 1048, 59025, 59201, 25123) reproduce exactly.
