# Round 51 lesson

author: chousa L1 (hyaku run 7, `ChousaR51`)
date: 2026-10-25
base: `9ec1751a24231e899ceea4688e21c8edf6046d35`
freeze: `d603f6f00f78d64f123d3aed2dd9f8701547a4ba`

No external fetch or network egress: L0 `8d77e6c1` remains open. Every source re-opened below is an on-disk capture under the read-only campaign cache `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`, accessed 2026-10-25 (captures written 2026-10-23 and 2026-10-24). Decode form: every `char N` below is an offset into the capture's `.txt` read as UTF-8 (`pdftotext -layout` of the PDF for S107–S110 and S112; the HTML-to-text rendering for the SinoMed record S111, whose `.raw` is HTML). C1 is plumbing, C2 is ground, C3 is plumbing (QUALITY 64). This is the lane's third package-adoption round under addendum section 10. Frozen claims and controls: `corpus/evidence/round51/claims.md`; errata E1–E4: `corpus/evidence/round51/claims-erratum.md`.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
@@MISTAKES@@
| 8. vacuous/attribution: the frozen round-51 C1 counter passes tools that implement none of the five behaviours — its work directories are named `s`, `d1`, `d2`, `renamed-heading`, so a 94-line tool that reads the name out of `--out` and prints canned shapes scores `LEGS=5/5`; its id draws can collide and hang it (seeds 13, 182, 324); an ambient `ASSIMILATE_CITES` flips its verdict to `LEGS=3/5`; and the shipped echo control delegated to the lane tool, so at the tip it scored `LEGS=5/5` and was no control | `corpus/evidence/round51/controls/forge-dirname.py`; `corpus/evidence/round51/controls/c1-supplement-controls.txt` (frozen counter `LEGS=5/5 C1=PASS` for the forge and for `tool-candidate1.py`, supplement `1/6` and `3/6`); `.ufo/waves/round-51/w1/R51CritForgeC1.md`, `R51ExecSeedRuns.md`, `R51SentScope.md` H5, `R51DraftSkillGates.md` | QUALITY 80 (a nonce leg and an exclusive output set) named the class after round 50 and the frozen counter satisfied it only on the literal-DIFF side; none named directory names, id-draw collisions, ambient environment or a control that delegates to the code under test | `corpus/evidence/round51/c1-supplement.py` (random directory names, distinct draws, the variable scrubbed, a mutation-sensitivity leg on the round-50 package, cross-entry, source-line, unknown-source and clash legs) and controls delegating to `controls/tool-before.py`; QUALITY 85. The frozen counter, predicate and target are not changed (`claims-erratum.md` E2–E4); the verdict is stated on both |

## Spot-check intake

| round-50 routed item | round-51 disposition |
|---|---|
| 1. Pin the revision the C1/C2 counters were measured against | Done for this round: `corpus/evidence/round51/measure-after.txt` opens with a `tool-rev:` header and `receipt-check.py` (QUALITY 84) prints `RECEIPT_OK`; the `SKILL.md` rows carry the pin. The round-50 receipt is re-measured at its tip by a clean clone, not rewritten: `corpus/evidence/round51/measure-r50-at-tip.txt` (zero differing lines against `measure-after.txt`) with an append-only `correction:` line in `SKILL.md` (Mistakes row 1). |
| 2. Replace the frozen C1 counter's literal-DIFF search with the nonce form | The round-51 frozen counter generates its packages from fresh randomness; its remaining weakness (fixed directory names) is Mistakes row 8, closed by the post-freeze supplement. |
| 3. Unique seat names | `python3 corpus/evidence/round50/name-collision-check.py` run on each spec before its `.ready` file: wave 1 `NAME_COLLISIONS=0 ITEMS=48`; all names carry the `R51` prefix. |
| 4. Filename drift in the coverage row | Appended as a `correction:` line to `corpus/README.md` (Mistakes row 6). |
| 5. SHONEN: all four boxes are `[~]` | A promotion decision, not a defect; unchanged, with the two pointers C3 found repaired (`SHONEN.md:10`). |

## Gate

### Collision check (section 10, 0–3-space pattern, scratch)

Run from `.ufo/waves/round-51/assimilation/` by W1 `R51ExecCollision` and re-read by the L1: registry ids `reg-ids` 106 lines (S001–S106, contiguous), staged ids `staged-ids` 114 lines (S082–S195, contiguous), `collisions` 25 lines (S082–S106). Three are identity collisions (S100–S102 carry the same URLs as lane rows), 22 are numbering collisions (same number, another document, e.g. staged S105 and S106 are lane own-work entries while lane S105 and S106 are the CNKI manuals). The staged file digest is the package's own. Guard proof (`assimilation/guard-proof.txt`): a two-space-indented `  | S002 | y |` registry row against a column-zero staged `| S002 | x |` gives collisions `S002` under the 0–3-space pattern and an empty list under the column-zero pattern `^\|`; the adopter's own splitter agrees with the former (`COLLISIONS=1`). Against the landed registry (S001–S112) the count is 31 (S082–S112) by the same command.

Renumber map by document (`R51ExecAdopt`; ids continue the lane registry, ascending staged id, never by arithmetic): staged S109 → S107, S110 → S108, S116 → S109, S117 → S110, S119 → S111, S126 → S112; staged S125 refused (no lane id). Body-only ids in the staged entries (S097 FEVER, S105 and S106 lane own-work rows, S116-as-lane-id) were dropped or replaced by the lane file path after opening that file; the adopter at the candidate lists them in `bodyonly.tsv` and flags the five clashes in `bodyclash.tsv` (W1 `R51ExecAdopt`; with `--cites all` it refuses S105/S106, with the registry's S097 silently held — the class QUALITY 77 and 82 describe).

Scratch validation before the append (W1 `R51ExecMirrorCensus`): `sources-census.sh validate --file` on a mirror of the base registry plus the adopter's `append.md`, the lane's `tools/` and the entries — exit 0, the five pre-existing W04 warnings only, no E03/E04, `NF!=13` count 0. The seat's mirror held seven rows (S107–S113, before the NIPH `.docx` was refused); the landed census is in `## Census` below.

### Re-opened sources (access 2026-10-25; no fetch)

| lane id | document | URL | decode form | headline quote (location) |
|---|---|---|---|---|
| S107 | システマティックレビューの基礎（喜屋武 享）, 日本健康教育学会誌 32(2) 2024 | https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja | `.txt` UTF-8, 21216 characters (two-column PDF text) | その日時，使用した検索式を同時に記録しておく (char 10234) |
| S108 | 機能性表示食品制度の届出資料におけるPRISMA 2020声明 … (別紙様式 (V)-4), 健康食品産業協議会, 2026年6月5日 第2版 | https://jaohfa.com/pdf/systematic_review.pdf | `.txt` UTF-8, 39676 characters | 検索者、検索ワード、検索式は別紙様式 (V) -5に示したことを記載する。 (char 4409) |
| S109 | 动物实验系统评价与Meta分析报告的规范撰写建议, 实验动物与比较医学 2025;45(4) | https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290 | `.txt` UTF-8, 52208 characters | 灰色文献的检索与记录 (char 15310, 表 1 row 3 — the staged `表3` is 表1 in this copy) |
| S110 | 提高动物实验系统评价/Meta分析的证据确定性：GRADE方法的实证研究, 实验动物与比较医学 2025;45(1) | https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237 | `.txt` UTF-8, 50952 characters | 从各数据库建立至 2024 年 4 月 1 日 (char 11404; the staged unspaced form is absent from the capture) |
| S111 | 系统评价/Meta分析中文献检索报告清单（PRISMA-S）解读, SinoMed record ui=2026335073 | https://www.sinomed.ac.cn/article.do?ui=2026335073 | `.txt` UTF-8, 1675 characters (HTML to text; the `学科分类号` and `主题词` rows are in an HTML comment, absent here) | 来源出版物： 中国循证医学杂志 卷：26 期：4 (char 695) |
| S112 | システマティックレビューとメタアナリシスの実施方法（剱持・岡）, 日本保健医療行動科学会雑誌 38(1) 2023 | https://www.jahbs.info/journal/pdf/vol38_1/vol38_1_5.pdf | `.txt` UTF-8, 25811 characters (two-column text; 40 glyphs lost at chars 101–140) | 検索の開始日と終了日を記載することで (char 11294) |

Refused document (no lane row): 国立保健医療科学院 費用対効果評価 分析結果の記載様式と手引 [第2.0版] 2024年4月 (staged S125), https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx — opened 2026-10-25 from its `.raw` (a `.docx`): its text exists only inside the DEFLATE member `word/document.xml`; the cache's `.txt` is the zip bytes decoded with replacement (168952 characters, 72117 of them U+FFFD; the document's phrases occur 0 times in it) and neither text form the span builder and the frozen C2 counter read (the `.txt` as UTF-8, the `.raw` as UTF-16LE) contains any quote, so a span for it can only be a slice of the zip bytes (W1 `R51DraftEntryJa2` F1, `R51ExecCaptureForm`, `R51ExecQuarantine` §6). The text itself is real and quotable from the unzipped member (W1 `R51GroundNiphA`: eight quotes once each; the staged worked-example string `文献検索期間2015年1月から2018年10月まで` is a join of two table cells; `PRISMA flow chart` is not in the document; its `Company` metadata names 厚生労働省 and its 提出者 fields name a submitting manufacturer).

refused-doc: https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx — 国立保健医療科学院 submission form (staged S125, quarantine row S120); refused this round for its capture form, not for its source quality; flip: a counter and span builder that read a zip member (`word/document.xml` concatenated `w:t` runs, one form named in the lesson), after which the staged claims narrowed as above can be re-grounded and bound. The one-branch `form_texts` change W1 `R51ExecCaptureForm` verified in scratch is the starting point; it is not applied, because the C2 counter is frozen.

### Decisions (every unadopted staged entry in the search-record neighbourhood; W1 `R51DraftGateTable`, re-checked by the L1 against the rows it names)

Admitted as narrowed: `japanese-search-record-r38.md`, `chinese-search-record-r39.md` and `japanese-search-record-r38-amendment-2026-10-23.md` (S126 only — the amendment's NIPH half is refused above). The package's other entries in the neighbourhood:

@@DECISIONS@@

### Quarantine slice (hand-checked this round; W1 `R51ExecQuarantine`, quotes re-located once each by the L1 in the stated forms)

Six register rows name a theme URL (`python3 corpus/evidence/round51/c2-count.py | grep QUARANTINE` lists S104 S105 S111 S112 S114 S120); all six class cells read `payload-absent`; the JAHBS article S112 has no register row. Rule stated before use: `present` = every document-attributed quote part occurs as a reader sees it with no character substitution; `absent-as-written` = a character differs or the part is markup the page does not render, while its substance is located; `fabricated` = the substance is nowhere; `unverifiable` = no text rendering exists. No verdict blocks a bound document; S114's `学科分类号` and `主题词` strings exist only inside an HTML comment, so no entry may quote them as displayed text (the Chinese entry does not).

```
@@VERDICTS@@
```

### All located quotes

Every quote below is at most 25 whitespace words and 160 characters, occurs exactly once in its `.txt` read as UTF-8, inside the citing entry and inside this lesson; `corpus/evidence/round51/spans.tsv` is derived from this set by `build-spans.py`, and `quote-substance-check.py` exits 0 on it.

@@QUOTES@@

### Non-author spot-check requested

At least one admit and one reject for the closure to re-open: admit `chinese-search-record-r39.md` (S109–S111; the closure should re-locate `灰色文献的检索与记录` at char 15310 and the S111 comment-only `学科分类号`); admit `japanese-search-record-r38.md` (S107 char 10234 and the page-footer correction 122 against the staged p.121); reject `search-log-fields-r36.md` (its PRISMA-S capture S082 is a 267-character challenge page, `01f657b3d0ab045c494b3f92.txt`) and refuse the S125 `.docx` (the zip, the 72117 U+FFFD, then `unzip -p … word/document.xml`).

## considerthese

`considerthese/2026-10-25.md` and its six predecessors were swept by W1 `R51ScoutConsiderthese` (31 proposals: 19 implemented, 9 reflection-format only, 3 open; the capture-age proposal was mined in round 49, QUALITY 71). One still-open proposal fits the province and is implemented: the lane-side "waiting on you" age. `python3 corpus/evidence/round51/open-items-age.py REPORT --round N` requires the report line `Open operator items: 8d77e6c1 since round 42 (9 rounds)`, derived from the first `## Round` heading of `LOG.md` above the first line that names the item; run against the round-50 report it prints `OPEN_ITEMS_AGE=FAIL … (8 rounds)` rc 1, against this round's report `PASS`. The operator item itself stays operator action.

@@TAIL@@
