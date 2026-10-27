# R54ExecMirrorCensus — scratch-mirror census of the three GB/T 7714-2025 Registry rows

seat R54ExecMirrorCensus (leaf; one labrat only, no dispatch) · lane chousa-shokunin · round 54 wave 1 · 2026-10-26
Write surface: this report only. No production file, no lane registry row, no lane entry, no lesson, no span
manifest, no git index, no jj state was touched by this seat. No tool installed (python3 stdlib + the lane's own
bash/gawk tools). No `soffice` run, no network. Scratch
`/fast/scratch/hyaku/chousa-r54/R54ExecMirrorCensus/` removed on exit; `pgrep -u $USER -f
"UserInstallation=file://$S"` returns nothing.

## 1. What this seat built, and a mid-seat lane change

The seat spec asked for a scratch mirror of the append: mirror the corpus, take the three candidate rows from
an adopter run, hand-normalise them, re-point S101's `used-by`, create the two entry files at the lane paths,
and run the census. I built that mirror and ran the census on it — **exit 0, five pre-existing W04 warnings,
zero E lines** (§2, §3).

**While I worked, another seat integrated the append into the live lane** (`git status` shows
`M corpus/SOURCES.md` plus untracked `corpus/knowledge/source-type-taxonomy-r36.md` and `-r37.md`; the three
rows are at `corpus/SOURCES.md:131-133` and the two entries exist). The landed rows are *not* the adopter's
mechanical rewrite — they carry located `char N` anchors and a narrowed scope/teaches, i.e. the drafting
seats' version. §4 reports both the mirror (adopter path) and the live lane; §5 is the operative verdict.

Commands (all run from the scratch, `TMPDIR=$S/tmp`):

```
S=/fast/scratch/hyaku/chousa-r54/R54ExecMirrorCensus
cp -a /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus "$S/lane/corpus"
cp -a /home/vgpnk/Projects/shokunin/chousa-shokunin/tools  "$S/lane/tools"   # census resolves used-by paths against <file>/..
python3 tools/assimilate-rows.py --staged /home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md \
  --knowledge /home/vgpnk/Projects/shokuknow/merge/chousa/knowledge \
  --registry "$S/lane/corpus/SOURCES.md" --opened 2026-10-26 --out "$S/adopt" \
  --entry corpus/knowledge/source-type-taxonomy-r36.md --entry corpus/knowledge/source-type-taxonomy-r37.md
# -> COLLISIONS=39 / CITED=4 APPEND=3 HELD=1 TWIN=0 / BODYONLY=0 / exit 0
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$S/lane/corpus/SOURCES.md" --today 2026-10-26
```

Adopter mapping (`$S/adopt/renumber.tsv`): `S085->S121 append`, `S086->S122 append`, `S093->S123 append`,
`S101->S101 held` (the HIT `.doc` URL is already in the lane registry, so no row is minted for it). Lane max id
at BASE is S120, so S121/S122/S123 are the next contiguous free ids. Hand-normalisation applied: `status`
mined, `opened` 2026-10-26, `recheck` reduced to the census-valid `180d` (the staged prose `180d — re-open …`
was stripped by the adopter and is in `$S/adopt/stripped.tsv`), `used-by` = the one lane entry citing the row.
S101 `used-by` in the mirror: `corpus/knowledge/citation-count-semantics-r37.md` →
`corpus/knowledge/citation-count-semantics-r37.md, corpus/knowledge/source-type-taxonomy-r37.md` (cell 10
only; cells 0-9 unchanged, verified cell-wise).

## 2. Census result on the mirror (adopter-path rows) — exit 0

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$S/lane/corpus/SOURCES.md" --today 2026-10-26
file	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
file	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
file	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
file	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file	ok	/fast/scratch/hyaku/chousa-r54/R54ExecMirrorCensus/lane/corpus/SOURCES.md
exit=0
```

**Every E/W line: five W04, zero E lines.** All five W04 are pre-existing and unrelated to this theme (W3C
HTML 5.2 snapshot, Python socket, Python hashlib, and the coreutils manual twice — S073/S075). The identical
five W04 appear on the untouched lane registry and on a pristine mirror, so the append introduces **no new W04**.

Tier/status counts, before vs after (`census` mode, same command, `--file`):

| metric | before (lane / pristine mirror, 120 rows) | after (mirror, 123 rows) | delta |
|---|---|---|---|
| rows | 120 | 123 | +3 (S121, S122, S123) |
| tier.A | 102 | 104 | +2 (S121, S122) |
| tier.B | 13 | 14 | +1 (S123) |
| tier.C | 5 | 5 | 0 |
| tier.invalid | 0 | 0 | 0 |
| status.mined | 96 | 99 | +3 |
| status.queued | 19 | 19 | 0 |
| status.rejected | 5 | 5 | 0 |
| status.invalid | 0 | 0 | 0 |
| missing | 0 | 0 | 0 |

Both runs exit 0 (`census` prints `FLEET` rows 120 / 123 with `missing 0`).

## 3. E03 / E04 / W04 on the three new URLs — the http-vs-https question

**No E03, no E04, no new W04 — on the mirror and on the live lane alike.**

* E03 (duplicate id): S121/S122/S123 do not exist in the lane registry (max id S120) and each appears exactly
  once — `grep -c "^| S12[123] "` = 3, and a duplicate-id scan over the parsed rows returns `none`.
* E04/W04 are keyed on the census's own URL key (`sources-census.sh:600-605`, `url_of()`): the first
  `https?://…` in the source cell, **scheme stripped**, host lower-cased, path+query kept, trailing `/` and
  `#frag` dropped. The three new keys are distinct from every existing row and from each other:

```
S121 key= std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F        other rows with same key: []
S122 key= openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14      other rows with same key: []
S123 key= xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf  other rows with same key: []
```

* **Same host family? No — and it does not matter.** The two samr URLs sit on *different hosts*
  (`std.samr.gov.cn` vs `openstd.samr.gov.cn`) and different paths, so the scheme difference is irrelevant
  here: the keys differ either way. The scheme **is** stripped by the key, which is the latent hazard: a
  second row for the same host+path under the other scheme would collide. I proved the collision mode with
  scratch mutants (probes, not deliverables): the openstd URL rewritten `http://`→`https://` with the *same*
  scope gives `file E04 S124 duplicate url openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14 within scope …`;
  the same URL with a *different* scope gives `file W04 S124 duplicate url openstd.samr.gov.cn/… across scopes`.
  So re-filing the openstd record over `https://` is only a warning (W04) in a different scope, an error
  (E04) in the same one — and the append as landed trips neither.

## 4. Findings (reported, not patched) — mirror path vs live lane

1. **E11 is a coupling between the rows and the two entry files.** With the rows in place but the lane paths
   absent, the census reports (probe on a copy with the entries deleted): `E11 S101 missing used-by
   corpus/knowledge/source-type-taxonomy-r37.md`, `E11 S121 missing used-by
   corpus/knowledge/source-type-taxonomy-r36.md`, `E11 S122 …r36.md`, `E11 S123 …r37.md`. The live lane now
   has both entry files, so it shows no E11 — the coupling is satisfied there. (A pre-existing E11 for S077
   `tools/quarantine-check.py` appears only when the mirror lacks the lane's `tools/` directory; the census
   resolves `used-by` paths against the registry's parent directory, so the mirror carries `tools/` too.)
2. **The adopter's rows have no `char N` anchors → `ANCHOR_BOUND` would read 0/3 on the adopter path.**
   `CHAR_RE = \bchar\s+(\d+)` finds `[]` in each of S121/S122/S123's anchor cells in the adopter output, so
   the anchor leg ("every `char N` in a bound row's `anchor` cell (at least one) is the offset of a quote of
   that id") contributes nothing. **Resolved on the live lane**: the landed rows carry `char 1029, char 1048,
   char 1797` (S121), `char 15188, char 16105, char 16321` (S122), `char 5576, char 5602, char 11542` (S123),
   and the counter now prints `ANCHOR_BOUND=3/3`.
3. **The stale `S075` token in the staged r37 is gone on the live lane.** In the *adopter* output (the staged
   campaign entry, renumbered) the counter's own regex `ID_RE = \bS\d{3,}\b` finds
   `['S075','S101','S123']` in r37 and `['S121','S122']` in r36; `S075` is neither a bound id nor `S101`, so it
   contributes 1 to the unbound count (and in the *lane* `S075` is an unrelated row — the GNU coreutils
   `mktemp(1)` manual at `corpus/SOURCES.md:85`). The **landed** r37 carries no `S075` at all
   (`grep -c S075` = 0) and the live counter prints `REF_ID_UNBOUND=0`. (Same defect class R54ExecCollision
   reported from the staged side; my measurement is independent, on the adopter's renumbered output.)
4. **The landed r37 does not cite S101, so S101's `used-by` must NOT gain r37.** The live
   `source-type-taxonomy-r37.md` has exactly one `source:` line (`source: S123 — <JMU pdf>`) and no HIT URL
   anywhere (`grep -c "jc.hit.edu.cn/_upload"` = 0); its `adopted:` header says the data-specification half is
   "not carried this round". The live S101 `used-by` is therefore correctly just
   `corpus/knowledge/citation-count-semantics-r37.md` (which does cite S101). The frozen C2 predicate's HELD
   leg is satisfied vacuously: the counter's HELD loop `continue`s when no entry cites the HIT URL, printing
   `HELD_CITED=- HELD_BAD=0`. **My mirror's S101 `used-by` edit (§1) was the right move for the adopter path
   — where r37 *does* carry `source: S101 — <HIT url>` — but it must not be applied to the landed entry.**
   Applying it to the live lane would name an entry that does not cite the row, and the gate's
   `META_SOURCE_USEDBY_MISSING` check runs the other way (entry → row), so it would not be caught. The L1's
   own `corpus/evidence/round54/claims-erratum.md` E3 records the same cut ("no `source: S101` line; S101's
   `used-by` unchanged"), which confirms this reading of the landed state.
5. **Live-lane `verify-metadata` flags the landed r37: `FINDING META_VERIFIED_AT_BARE … key=verified-at has
   date only`** (r37's `verified-at: 2026-10-26` is bare; r36's carries a trailing clause). The gate prints
   `RESEARCH_GATE: DRIFT` for r37 and `CLEAN` for r36. This is a lane-wide pattern (15 of 79 entries have a
   bare `verified-at`, 14 of them pre-existing), not new to this round — but the two new entries are now 2 of
   the 15. Full-directory run: `RESEARCH_GATE: DRIFT (entries=79 complete=75 findings=86 drift=26)`. Not a
   census finding; flagged because the landed r37 is the round's own new entry.

## 5. Operative verdict on the **live** lane (post-integration), and the counter's current read

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md --today 2026-10-26
file	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
file	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
file	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
file	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
exit=0
$ bash …/sources-census.sh census --file …/corpus/SOURCES.md
file	rows	123   tier.A	104   tier.B	14   tier.C	5   status.mined	99   status.queued	19   status.rejected	5
exit=0        # identical counts to my mirror's after-state
$ bash …/sources-census.sh overdue --file …/corpus/SOURCES.md --today 2026-10-26 | grep S12[123]
file	cadence	S121 recheck=180d opened=2026-10-26
file	cadence	S122 recheck=180d opened=2026-10-26
file	cadence	S123 recheck=180d opened=2026-10-26      # symbolic cadence, never overdue; 0 overdue rows lane-wide
```

The live census verdict equals my mirror's: **exit 0, five pre-existing W04, zero E lines, no E03/E04 and no
new W04 from the three new URLs**, rows 120→123, tier.A 102→104, tier.B 13→14, status.mined 96→99.

The frozen counter on the live lane (`python3 corpus/evidence/round54/c2-count.py`, `--lane-only` off so
`CAPTURE_BOUND` runs) prints:

```
ENTRIES=2/2 (min 2) REFUSED_ENTRIES=0     HELD_CITED=- HELD_BAD=0
BOUND=3/3 (min 2) REFUSED=0                BOUND_IDS=S121,S122,S123
REF_ID_UNBOUND=0                            NEW_GROUND=2/2
QUOTE_ROWS=33 ON_BOUND=33/33                SPAN_IDS=3/3 (min 3 each)
QUOTES_IN_SPAN=33/33                        QUOTES_IN_ENTRY=33/33
QUOTES_IN_LESSON=0/33                       QUOTE_SHORT=33/33
SPAN_CONTEXT=33/33                          CAPTURE_BOUND=33/33
SUBSTANCE=PASS                              ANCHOR_BOUND=3/3
INFERENCE_GROUNDED=2/2                      QUARANTINE_VERDICTS=0/3 (S080,S088,S096)
QUARANTINE_BLOCKED_ADOPTED=0                C2=FAIL   # §5: FAIL is the lesson + quarantine legs only
```

Every registry-shaped leg is green (BOUND 3/3, no unbound id, anchors bound, capture-bound 33/33, both
entries ground). `C2=FAIL` on the live lane rests on exactly two open legs, both owned elsewhere and both
**not** registry rows: `QUOTES_IN_LESSON=0/33` (there is no `corpus/lessons/round-54.md` yet) and
`QUARANTINE_VERDICTS=0/3` (no re-check verdict lines for the register rows S080/S088/S096). §4.4 says the S101
`used-by` must not gain r37 on the landed r37 — an entry decision, not a row decision; it does not affect the
numbers above (the HELD leg is vacuous either way).

## 6. The rows now in the lane (`corpus/SOURCES.md:131-133`, verbatim from the file)

```
| S121 | GB/T 7714-2025 信息与文献 参考文献著录规则 — 全国标准信息公共服务平台 (国家市场监督管理总局 / 国家标准化管理委员会) — https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F | docs | A | for what the record itself states about this standard — number and title, kind and status, issue and effective dates, the standard it wholly replaces, and its adoption basis — the standards administration's own record page, so tier A for that scope only | the 标准状态 block (发布 于 2025-12-02, 实施 于 2026-07-01), the 采标情况 block (本标准非等效采用ISO国际标准：ISO 690:2021。 and its 采标中文名称), the 基础信息 rows 标准号 / 标准状态 / 全部代替标准 / 中国标准分类号 / 国际标准分类号, and the 归口单位 and 主管部门 rows; capture .txt adf6ba934e813b2c326fa150.txt read as UTF-8 with newline normalisation, 3591 characters, sha256 prefix 4e46154f4a841d17; char 1029, char 1048, char 1797 | GB/T 7714-2025 is a 推荐性 现行 national standard for bibliographic references, published 2025-12-02 and effective 2026-07-01, wholly replacing GB/T 7714-2015; it is a non-equivalent adoption (非等效采用) of ISO 690:2021, whose Chinese title the record gives as 信息与文献 参考文献和信息资源引用指南; CCS A14, ICS 01.140.20, 归口单位 全国信息与文献标准化技术委员会, 主管部门 国家标准委 | mined | 2026-10-26 | 180d | corpus/knowledge/source-type-taxonomy-r36.md |
| S122 | 国家标准 GB/T 7714-2025 在线预览 — 全国标准信息公共服务平台 (openstd) — http://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14 | docs | A | for what the full-text portal itself serves for this standard and why it serves no text — the same authority's portal notice about its own service, so tier A for that scope only | the 标准号 heading, the 中文标准名称 and 英文标准名称 rows, 标准状态, the 中国标准分类号（CCS） and 国际标准分类号（ICS） rows, the 发布日期 and 实施日期 rows, and the notice paragraph standing where a text would be; capture .txt b9ca2a4fdf9455867534f144.txt read as UTF-8 with newline normalisation, 22007 characters, sha256 prefix 2d68faf7c724eb1b (the sidecar is the served HTML itself: that digest is also the .raw's); char 15188, char 16105, char 16321 | the portal shows this standard as 现行, with 中文标准名称 信息与文献 参考文献著录规则, an English title, CCS A14 and ICS 01.140.20, published 2025-12-02 and effective 2026-07-01; where a text would stand it states that, because the standard adopts ISO and IEC standards, the portal's own system serves no text-reading service for copyright reasons — a statement about this portal's service for this standard, not that the text is unavailable elsewhere | mined | 2026-10-26 | 180d | corpus/knowledge/source-type-taxonomy-r36.md |
| S123 | GB/T 7714—2025《信息与文献 参考文献著录规则》full text, a PDF copy on the 集美大学学报 journal office's file host — https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf | docs | B | for what this reproduced copy carries of the standard's own clauses — scope, type and carrier identifiers, date rules — a university journal office's upload rather than the issuing authority, so tier B, scoped to the reproduction and never to the issued standard | the title page (ＧＢ／Ｔ ７７１４—２０２５, 代替ＧＢ／Ｔ ７７１４—２０１５), clause １ 范围, clause ７．３ 文献类型标识、文献载体标识, clause ７．６ 创建／发布或修改日期、引用日期, and the 附录Ａ 表A.1 rows marked 电子资源必备; capture .txt 0f33243fd7ac2fe88b85c1ba.txt (the PDF text form; full-width digits throughout) read as UTF-8 with newline normalisation, 83061 characters, sha256 prefix 13a34aa9bb107eef; char 5576, char 5602, char 11542 | the copy's scope clause limits the standard to 作者和编制者 and excludes 图书馆员、文献目录编制者以及索引编制者; 7.3 requires a type identifier and a carrier identifier, the carrier one 必备 for electronic resources; 7.6 fixes 创建／发布或修改日期 and 引用日期 in ＹＹＹＹ－ＭＭ－ＤＤ form | mined | 2026-10-26 | 180d | corpus/knowledge/source-type-taxonomy-r37.md |
```

## 7. Risks and blockers

* The live lane is census-clean; the two open `C2=FAIL` legs (`QUOTES_IN_LESSON=0/33`, no
  `corpus/lessons/round-54.md`; `QUARANTINE_VERDICTS=0/3` for register S080/S088/S096) belong to the lesson
  and quarantine seats, not to the registry.
* Do **not** apply the mirror's S101 `used-by` edit to the landed r37 (§4.4): the landed r37 does not cite
  S101, and naming it in S101's `used-by` would assert a citation that does not exist. The frozen HELD leg
  does not need it (`HELD_CITED=- HELD_BAD=0`).
* If the openstd record is ever re-filed over `https://`, the census key ignores the scheme: same host+path
  in the same scope is E04, in a different scope W04 (§3).
* The landed r37 trips `META_VERIFIED_AT_BARE` in `verify-metadata` (§4.5) — a lane-wide pattern (15 of 79
  entries), but the round's own new entry.

VERDICT: built the scratch mirror of the three GB/T 7714-2025 rows (+S101 `used-by`) and ran the census on it
— exit 0, five pre-existing W04 and zero E lines, rows 120→123, tier A 102→104 / B 13→14, mined 96→99, no
E03/E04 and no new W04 (the samr and openstd URLs sit on different hosts and paths, so the http-vs-https
difference cannot collide); the lane was then integrated mid-seat with the same census verdict on the live
file (exit 0, identical counts) and the counter's registry legs green (BOUND 3/3, REF_ID_UNBOUND=0,
ANCHOR_BOUND 3/3, CAPTURE_BOUND 33/33, SUBSTANCE PASS, INFERENCE_GROUNDED 2/2), with `C2=FAIL` resting only
on the not-yet-written round-54 lesson (QUOTES_IN_LESSON 0/33) and the three missing quarantine verdicts.
