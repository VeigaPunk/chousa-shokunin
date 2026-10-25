# Round 51 lesson

author: chousa L1 (hyaku run 7, `ChousaR51`)
date: 2026-10-25
base: `9ec1751a24231e899ceea4688e21c8edf6046d35`
freeze: `d603f6f00f78d64f123d3aed2dd9f8701547a4ba`

No external fetch or network egress: L0 `8d77e6c1` remains open. Every source re-opened below is an on-disk capture under the read-only campaign cache `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`, accessed 2026-10-25 (captures written 2026-10-23 and 2026-10-24). Decode form: every `char N` below is an offset into the capture's `.txt` read as UTF-8 (`pdftotext -layout` of the PDF for S107–S110 and S112; the HTML-to-text rendering for the SinoMed record S111, whose `.raw` is HTML). C1 is plumbing, C2 is ground, C3 is plumbing (QUALITY 64). This is the lane's third package-adoption round under addendum section 10. Frozen claims and controls: `corpus/evidence/round51/claims.md`; errata E1–E4: `corpus/evidence/round51/claims-erratum.md`.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| 1. scope/reference-drift: the round-50 after-measurement names no revision, and the gate registry row names the C1 candidate, not the landed tip | `corpus/evidence/round50/measure-after.txt:1` reads "at the working tree before the final commit" with no hash; `corpus/evidence/round50/measure-after-1.txt:1` says `# tip: working tree` (a moving target); `SKILL.md:132` names `ec52e632edbad7fe51a6573d29acad5a028a7158` for the counters, whose landed tip is `1d7aba0948cf`; routed defect 1, `corpus/lessons/round-50-verifier-spotcheck.md:90`; QUALITY 58 | `R50ScribeReportDraft.md:74` left this row `<PENDING>`; the spot-check's non-author read found it | header carries `lane_revision=<sha> tool_sha256=<sha>`, registry row names the landed tip. Failing now, both exit 1: `head -1 corpus/evidence/round50/measure-after.txt \| grep -qE '[0-9a-f]{7,40}'`; `! grep -q 'ec52e632' SKILL.md` — both exit 0 after the fix |
| 2. vacuous: the frozen round-50 C1 counter recognises its own six literal DIFF lines, so a 42-line tool with no adopter logic scores it full | `corpus/evidence/round50/c1-count.py:107-112` matches one literal regex per perturbation; `corpus/evidence/round50/controls/forge-tool.py:2,8-13` prints all six for any non-pinned digest; `corpus/evidence/round50/c1-supplement-receipt.txt:51-54` records `LEGS=5/5 C1=PASS` for it; QUALITY 80 | W2 `R50CritForgeC1` (`.ufo/waves/round-50/w2/R50CritForgeC1.md:7-14`) | replace the literal-DIFF search with a nonce leg plus an exclusive output set (what round-51 C1 does). Failing commands: `python3 corpus/evidence/round50/c1-count.py --tool corpus/evidence/round50/controls/forge-tool.py` prints `BASELINE=PASS rc=0 findings=26` and `PERTURB_PASS=6/6` for the cheat; with the forge's `REAL` pointed at `ec52e632:tools/assimilate-rows.py` (scratch, sha256 `bff32c11…`) the frozen counter prints `LEGS=5/5 C1=PASS` exit 0. A fixed counter must print `C1=FAIL` for both |
| 3. reference-drift: the adopter's default flip to source-only citations breaks both earlier one-shot counters, and the env switch the claims rely on does not restore them | `corpus/evidence/round51/claims.md:56-58` ("`LEGACY_ALL` is what preserves their behaviour"), contradicted by measurement at the tip; QUALITY 58, 68 | none before this row — the claims disclosed the risk but no receipt ran the earlier counters at the candidate | each one-shot counter pins the tool bytes it was measured against (QUALITY 58). Failing commands (all exit 1 today): `python3 corpus/evidence/round49/c1-count.py` → `SETS_PASS=2/3 C1=FAIL`; `python3 corpus/evidence/round50/c1-count.py` → `LEGS=3/5 C1=FAIL`; `ASSIMILATE_CITES=all python3 corpus/evidence/round50/c1-count.py` → `LEGS=4/5 C1=FAIL` (`SELFTEST_DEFAULT=FAIL`). `--tool <ec52e632 bytes>` restores both (`5/5`, `3/3`); a fixed counter passes all three |
| 4. calibration: five self-assessment evidence pointers dangle at the base, and no criterion 1–80 requires a pointer to resolve | `corpus/evidence/round51/controls/c3-before-erratum.txt:4-9` (`SCORECARD.md:1843 measure/final/`, `:2073 measure-l1/c1-s36361.json`, `:2074 measure-l1/c2-s36371.json`, `:2616 c1-supplement.py`, `SHONEN.md:10 round25-meta-differential.log`), all five absent on disk; QUALITY 37 governs numeric tallies and QUALITY 74's scan set is `corpus/evidence/round50/stale-count-check.py:18` = QUALITY.md, README.md, LOG.md, round-49.md (0 hits for SCORECARD.md/SHONEN.md); `tools/research-gate.sh` names SCORECARD.md/SHONEN.md 0 times | none — no criterion and no check read a self-assessment's pointers before round 51 | repair the five pointers (or one `correction: SCORECARD.md:<line> <ptr> -> <path>` line per row). Failing command: `python3 corpus/evidence/round51/c3-count.py` → `DANGLING=5 C3=FAIL` exit 1, identical at the tip and at the base tree |
| 5. counter-defect (vacuous): the C3 extractor stripped a leading dot, so three existing `.ufo/...` paths read as dangling, and its controls never seed the dot class | `corpus/evidence/round51/claims-erratum.md:12-16`; pre-erratum `c3-count.py:54` (`tok.strip(",;.:()")`); `corpus/evidence/round51/controls/build-c3-controls.py:34-57` derives all three controls from the counter's own `DANGLING` output (blanket line, deleted rows, zero-byte files at the *dangling* names), so no control ever adds a dot-leading pointer; QUALITY 20 is the criterion that should have caught it | none (`claims-erratum.md:27-28` states the class and that no control seeds it) | tokenizer keeps the leading dot, plus a DOTPATH control whose pointer must resolve. Failing commands: `pointers("`.ufo/waves/round-34/measure/`")` → `['ufo/waves/round-34/measure/']` at `d603f6f` vs `['.ufo/waves/round-34/measure/']` at the tip; the pre-erratum counter at the base tree prints `DANGLING=8` (3 false positives) vs `DANGLING=5` |
| 6. scope: the filename drift (`istic-…` for a 中国科学院文献情报中心 page) is recorded in the entry only, not in the coverage row a reader browses | `corpus/knowledge/istic-citation-verification-r39.md:6` carries the note ("the lane filename says istic, inherited from the staged entry"); `corpus/README.md:1078`'s row does not — `ISTIC` and `filename drift` occur 0 times in README.md; routed defect 4, `corpus/lessons/round-50-verifier-spotcheck.md:93` | round-50 spot-check section 6 item 4 | append the drift note to the coverage row. Failing command: `awk -F'\|' '/^\| `knowledge\/istic-citation-verification-r39.md`/{print ($0 ~ /ISTIC\|drift/) ? "DRIFT_NOTE" : "DRIFT_MISSING"}' corpus/README.md` → `DRIFT_MISSING` |
| 7. reference-drift: a receipt tally whose printed command does not reproduce it (`$ grep -cE rows` → `106`) | `corpus/evidence/round50/measure-after.txt:125-126`; re-run verbatim it reads stdin and prints `0`; the obvious file gives `13`; `106` is the S-row count, so the pattern or the file argument was dropped | none — QUALITY 37's own check ("run the named command and compare") was never run on the receipt | name the file and the pattern. Failing commands: `grep -cE rows < /dev/null` → `0`; `grep -cE rows corpus/SOURCES.md` → `13`; `grep -cE '^\| S[0-9]{3} ' corpus/SOURCES.md` → `106` |
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

| staged entry | documents (S-ids) | capture on disk (yes/no, key) | province fit | decision | reason | flip |
|---|---|---|---|---|---|---|
| `search-log-fields-r36.md` | S082, S083, S090 | **no for the tier-A leg**: `01f657b3d0ab045c494b3f92` (.txt, 267 chars = "Client Challenge"); `14aaa168a5cb4d833ca78b0b` (.txt, 210,708, char 112450); S090 row URL `02b3b0e8…` holds the landing page (参照 0) while the PDF is `58b1b564…` (char 3785) | in: it is the field list itself | **refuse** | its central authority is not on disk: the PRISMA-S string it quotes occurs 0 times in every `.txt` in the cache, and 2 of its 3 legs cannot be re-opened from the row as written | a PRISMA-S full-text capture (item-8 string present) plus S090's cell re-pointed to `_pdf/-char/ja`; then admit with the Cochrane leg unchanged |
| `search-tracking-record-r40.md` | S134 | yes: `0ae65ac01b93119d3c2f3fed` (.txt, 27,659, char 1334) | in: a tracking record's columns | **admit-later** | tier A; capture and quote pass; off this round's theme (the western reading) and a fourth entry sits outside the frozen three; body ids S069, S094, S114, S130 name other documents here | next round's entry set or a C2 re-freeze; no capture work left |
| `chinese-search-log-r37.md` | S102, S103, S104 | yes: `7809d5114330a60527436b07` (.txt, 17,317, 专业检索 3764), `02aefcf570a7108e699d0990` (.txt, 8,590, 溯源 780), `3d7b23e68f13add5cfae634b` (.txt, 68,091) | in | **refuse** | superseded: its lead finding (no Chinese-language search-log specification was found) is contradicted by S111/S112, which this round does admit; 2 of its 3 documents are held rows (F2); body ids S071/S072/S079 name the GNU env manual, the Bash manual and RFC 7089 | if the lane wants the superseded reading as a dated appendix: heading marked superseded, the two held-document rows de-duplicated, all body ids stripped |
| `chinese-search-log-r37-amendment-2026-10-23.md` | S111, S112 | yes: `453d492becd9a2f4632cb8dd` (.txt, 8,804, char 2463), `cacddf3bbf780a4c7582bb17` (.txt, 6,179, char 1707) | in | **admit-later** | carries the strongest on-theme field evidence the three do not (the per-source search date in Chinese), but it amends the file row 6 refuses and it is a fourth entry | either row 6 lands as a labelled superseded reading, or this entry's `ground:` cites S111/S112 directly and drops the base pointer; then next round |
| `japanese-prisma-item-wording-r40.md` | S129 | yes, at the archive: `e84bfe97808591d23fe3266f` (.txt, 5,328, char 641); the row's own URL key `f3dbe2fe59a684b1b94cfadc` is absent | in: PRISMA's own Japanese wording | **admit-later** | the document is on disk and its negative is verified (検索者 0 times), but the row's `source` cell names the dead original and its recheck says "confirm 項目7", a string that occurs 0 times in the capture (the row is labelled 検索戦略 with number 7) | row URL re-pointed at the archive with the dead original kept visible, recheck naming the 検索戦略 row; then next round |
| `grey-literature-and-chinese-search-record-r40.md` | S130, S131, S133 | yes: `bdff491a75c6abeda1d9c01d` (.raw, OLE .doc, UTF-16LE decode, char 57497), `27d4865f201e99c1fed9f79b` (.txt, 1,858, char 780), `453d492becd9a2f4632cb8dd` (= S111's document) | **out of province for its spine** (a regulator instrument's currency); in province only for the field sentence | **refuse** | the entry leaves the guideline's currency unresolved and that question is NMPA/legal ground (PROVINCE: out of province, report, never absorb); S133 and S111 hash to one key, so the package would append two rows for one page; the field claim is already carried by the admitted row 2 (S116 module 3, 灰色文献的检索与记录 at char 15310) | the owning lane settles the guideline's status and S133 merges into S111; then the field sentence returns as a dated addendum to row 2 |
| `grey-literature-and-chinese-search-record-r41.md` | S142 | yes: `be6963bbc94761282fea066e` (.txt, 19,352, char 7176) | in (methodological practice), but a conduct claim, not a record field | **refuse** | as staged it carries no located quote (1 backtick span and 0 double-quoted spans in 2,253 characters; every claim is paraphrase), it rests on one tier-B mirror of a 协和医学杂志 paper, and its own Unknown calls it "an argument for the practice, not a requirement" | a primary publisher copy in the cache and the entry rewritten with at least one located quote per claim (the definition sentence sits at char 7176) |

### Quarantine slice (hand-checked this round; W1 `R51ExecQuarantine`, quotes re-located once each by the L1 in the stated forms)

Six register rows name a theme URL (`python3 corpus/evidence/round51/c2-count.py | grep QUARANTINE` lists S104 S105 S111 S112 S114 S120); all six class cells read `payload-absent`; the JAHBS article S112 has no register row. Rule stated before use: `present` = every document-attributed quote part occurs as a reader sees it with no character substitution; `absent-as-written` = a character differs or the part is markup the page does not render, while its substance is located; `fabricated` = the substance is nowhere; `unverifiable` = no text rendering exists. No verdict blocks a bound document; S114's `学科分类号` and `主题词` strings exist only inside an HTML comment, so no entry may quote them as displayed text (the Chinese entry does not).

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

### All located quotes

Every quote below is at most 25 whitespace words and 160 characters, occurs exactly once in its `.txt` read as UTF-8, inside the citing entry and inside this lesson; `corpus/evidence/round51/spans.tsv` is derived from this set by `build-spans.py`, and `quote-substance-check.py` exits 0 on it.

| lane id | form | char offset | located quote (≤25 words, exactly once in that form) | cited by |
|---|---|---:|---|---|
| S107 | `.txt` UTF-8 | 10232 | か，その日時，使用した検索式を同時に記録しておく | `corpus/knowledge/japanese-search-record-r38.md` |
| S107 | `.txt` UTF-8 | 10234 | その日時，使用した検索式を同時に記録しておく | `corpus/knowledge/japanese-search-record-r38.md` |
| S107 | `.txt` UTF-8 | 10239 | 使用した検索式 | `corpus/knowledge/japanese-search-record-r38.md` |
| S107 | `.txt` UTF-8 | 10301 | とが望ましい． | `corpus/knowledge/japanese-search-record-r38.md` |
| S107 | `.txt` UTF-8 | 10314 | 研究の透明性を保ち，他者 | `corpus/knowledge/japanese-search-record-r38.md` |
| S107 | `.txt` UTF-8 | 10370 | が同様の検索を再現できるようになる | `corpus/knowledge/japanese-search-record-r38.md` |
| S107 | `.txt` UTF-8 | 12666 | PRISMA は，日本語を含め | `corpus/knowledge/japanese-search-record-r38.md` |
| S107 | `.txt` UTF-8 | 12732 | 言語に翻訳されている | `corpus/knowledge/japanese-search-record-r38.md` |
| S107 | `.txt` UTF-8 | 12807 | 報告すべき内容のチェックリストも付録されてい | `corpus/knowledge/japanese-search-record-r38.md` |
| S107 | `.txt` UTF-8 | 12815 | チェックリストも付録されてい | `corpus/knowledge/japanese-search-record-r38.md` |
| S107 | `.txt` UTF-8 | 12873 | るため，使いやすさという点でも考慮されている． | `corpus/knowledge/japanese-search-record-r38.md` |
| S107 | `.txt` UTF-8 | 13710 | このプロセスに際して，誰が検索を行ったの | `corpus/knowledge/japanese-search-record-r38.md` |
| S107 | `.txt` UTF-8 | 13721 | 誰が検索を行った | `corpus/knowledge/japanese-search-record-r38.md` |
| S107 | `.txt` UTF-8 | 13721 | 誰が検索を行ったの | `corpus/knowledge/japanese-search-record-r38.md` |
| S107 | `.txt` UTF-8 | 17398 | 本健康教育学会誌にもシステマティックレビューの投 | `corpus/knowledge/japanese-search-record-r38.md` |
| S107 | `.txt` UTF-8 | 18441 | PRISMA-ScR | `corpus/knowledge/japanese-search-record-r38.md` |
| S108 | `.txt` UTF-8 | 809 | 機能性表示食品制度の届出資料におけるPRISMA 2020声明 システマティックレビュー記載の留意点(別紙様式 (V) -4 本文) | `corpus/knowledge/japanese-search-record-r38.md` |
| S108 | `.txt` UTF-8 | 1498 | 更新版であれば更新した旨を記載する | `corpus/knowledge/japanese-search-record-r38.md` |
| S108 | `.txt` UTF-8 | 3966 | 全てのデータベース | `corpus/knowledge/japanese-search-record-r38.md` |
| S108 | `.txt` UTF-8 | 4124 | それぞれのデータベース毎に最後に検索した日の日付を記載する。 | `corpus/knowledge/japanese-search-record-r38.md` |
| S108 | `.txt` UTF-8 | 4192 | それぞれの情報源が最後に調べられた | `corpus/knowledge/japanese-search-record-r38.md` |
| S108 | `.txt` UTF-8 | 4211 | ハンドサーチの有無を記載する。 | `corpus/knowledge/japanese-search-record-r38.md` |
| S108 | `.txt` UTF-8 | 4409 | 検索者、検索ワード、検索式 | `corpus/knowledge/japanese-search-record-r38.md` |
| S108 | `.txt` UTF-8 | 4409 | 検索者、検索ワード、検索式は別紙様式 (V) -5に示したことを記載する。 | `corpus/knowledge/japanese-search-record-r38.md` |
| S108 | `.txt` UTF-8 | 36834 | 検索ワードや検索式は実際に使用した、もしくはそれと同等の詳細なものであること。 | `corpus/knowledge/japanese-search-record-r38.md` |
| S108 | `.txt` UTF-8 | 36844 | 実際に使用した | `corpus/knowledge/japanese-search-record-r38.md` |
| S108 | `.txt` UTF-8 | 36859 | 同等の詳細なもの | `corpus/knowledge/japanese-search-record-r38.md` |
| S109 | `.txt` UTF-8 | 121 | DOI:10.12300/j.issn.1674-5817.2025.017 | `corpus/knowledge/chinese-search-record-r39.md` |
| S109 | `.txt` UTF-8 | 4113 | 1674-5817（2025）04-0496-12 | `corpus/knowledge/chinese-search-record-r39.md` |
| S109 | `.txt` UTF-8 | 14179 | 表 1 研究方案主体报告框架内容 | `corpus/knowledge/chinese-search-record-r39.md` |
| S109 | `.txt` UTF-8 | 15140 | 含动物实验特殊数据库 | `corpus/knowledge/chinese-search-record-r39.md` |
| S109 | `.txt` UTF-8 | 15240 | 检索词及逻辑关系（结合 MeSH/Emtree 主题词与自由词） | `corpus/knowledge/chinese-search-record-r39.md` |
| S109 | `.txt` UTF-8 | 15310 | 灰色文献的检索与记录 | `corpus/knowledge/chinese-search-record-r39.md` |
| S109 | `.txt` UTF-8 | 17709 | 尚无专门针对动物实验 SR 的报告规范 | `corpus/knowledge/chinese-search-record-r39.md` |
| S109 | `.txt` UTF-8 | 22932 | 至少提供一个主要数据库的完整检索策略 | `corpus/knowledge/chinese-search-record-r39.md` |
| S109 | `.txt` UTF-8 | 23097 | AND，OR 等 | `corpus/knowledge/chinese-search-record-r39.md` |
| S109 | `.txt` UTF-8 | 23180 | 参考文献追溯 | `corpus/knowledge/chinese-search-record-r39.md` |
| S109 | `.txt` UTF-8 | 23316 | 表 2 动物实验系统评价的数据库检索参考 | `corpus/knowledge/chinese-search-record-r39.md` |
| S109 | `.txt` UTF-8 | 24298 | 预印本平台 | `corpus/knowledge/chinese-search-record-r39.md` |
| S109 | `.txt` UTF-8 | 24606 | 手工查阅期刊 | `corpus/knowledge/chinese-search-record-r39.md` |
| S110 | `.txt` UTF-8 | 134 | DOI:10.12300/j.issn.1674-5817.2024.109 | `corpus/knowledge/chinese-search-record-r39.md` |
| S110 | `.txt` UTF-8 | 1633 | 1674-5817（2025）01-0101-11 | `corpus/knowledge/chinese-search-record-r39.md` |
| S110 | `.txt` UTF-8 | 11110 | 文献特征分析 | `corpus/knowledge/chinese-search-record-r39.md` |
| S110 | `.txt` UTF-8 | 11211 | 检索中国知网、万方、中国生物医学文献数据库、 | `corpus/knowledge/chinese-search-record-r39.md` |
| S110 | `.txt` UTF-8 | 11213 | 中国知网、万方、中国生物医学文献数据库 | `corpus/knowledge/chinese-search-record-r39.md` |
| S110 | `.txt` UTF-8 | 11213 | 中国知网、万方、中国生物医学文献数据库、 | `corpus/knowledge/chinese-search-record-r39.md` |
| S110 | `.txt` UTF-8 | 11404 | 从各数据库建立至 2024 年 4 月 1 日 | `corpus/knowledge/chinese-search-record-r39.md` |
| S111 | `.txt` UTF-8 | 695 | 来源出版物： 中国循证医学杂志 卷：26 期：4 | `corpus/knowledge/chinese-search-record-r39.md` |
| S111 | `.txt` UTF-8 | 702 | 中国循证医学杂志 卷：26 期：4 | `corpus/knowledge/chinese-search-record-r39.md` |
| S111 | `.txt` UTF-8 | 934 | 包含16个条目的专项规范 | `corpus/knowledge/chinese-search-record-r39.md` |
| S111 | `.txt` UTF-8 | 1078 | 查看主题词相同的文献 | `corpus/knowledge/chinese-search-record-r39.md` |
| S111 | `.txt` UTF-8 | 1138 | 质量控制 | `corpus/knowledge/chinese-search-record-r39.md` |
| S111 | `.txt` UTF-8 | 1366 | 请登录后再使用此功能 | `corpus/knowledge/chinese-search-record-r39.md` |
| S112 | `.txt` UTF-8 | 158 | システマティックレビューとメタアナリシスの実施方法 | `corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md` |
| S112 | `.txt` UTF-8 | 10140 | 検索の特徴（検索期間 | `corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md` |
| S112 | `.txt` UTF-8 | 10146 | 検索期間，言語制限 | `corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md` |
| S112 | `.txt` UTF-8 | 11229 | 検索した文献データベース名 | `corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md` |
| S112 | `.txt` UTF-8 | 11243 | Ovid などのプロバ | `corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md` |
| S112 | `.txt` UTF-8 | 11294 | 検索の開始日と終了日を記載することで | `corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md` |
| S112 | `.txt` UTF-8 | 11348 | 最新の結果を反映しているかどうか | `corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md` |
| S112 | `.txt` UTF-8 | 11457 | 評価がしやすくなる | `corpus/knowledge/japanese-search-record-r38-amendment-2026-10-23.md` |

### Non-author spot-check requested

At least one admit and one reject for the closure to re-open: admit `chinese-search-record-r39.md` (S109–S111; the closure should re-locate `灰色文献的检索与记录` at char 15310 and the S111 comment-only `学科分类号`); admit `japanese-search-record-r38.md` (S107 char 10234 and the page-footer correction 122 against the staged p.121); reject `search-log-fields-r36.md` (its PRISMA-S capture S082 is a 267-character challenge page, `01f657b3d0ab045c494b3f92.txt`) and refuse the S125 `.docx` (the zip, the 72117 U+FFFD, then `unzip -p … word/document.xml`).

## considerthese

`considerthese/2026-10-25.md` and its six predecessors were swept by W1 `R51ScoutConsiderthese` (31 proposals: 19 implemented, 9 reflection-format only, 3 open; the capture-age proposal was mined in round 49, QUALITY 71). One still-open proposal fits the province and is implemented: the lane-side "waiting on you" age. `python3 corpus/evidence/round51/open-items-age.py REPORT --round N` requires the report line `Open operator items: 8d77e6c1 since round 42 (9 rounds)`, derived from the first `## Round` heading of `LOG.md` above the first line that names the item; run against the round-50 report it prints `OPEN_ITEMS_AGE=FAIL … (8 rounds)` rc 1, against this round's report `PASS`. The operator item itself stays operator action.

## Census

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`.

- **Round start** (`corpus/evidence/round51/census-start.txt`): exit 0, `ok`, five pre-existing W04 warnings (S051, S053, S073, S074, S075); 106 rows.
- **Round end:** exit 0, `ok`, W04 warnings S051, S053, S073, S074, S075 (the same five); tiers {'A': 98, 'B': 9, 'C': 5}.
- **Rows:** 106 → 112 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`). Added by tier: A S107 S108 S109 S110 S112; B S111. Rows touched old → new: none.
- **Sourced claim:** C2 rests on S107–S112, all opened this round.
- **Mined mistakes:** eight, in `## Mistakes`; rows 1, 5, 6 and 8 each have a check shown able to fail (QUALITY 84, 86, the README correction check, QUALITY 85).

## Disclosed post-freeze changes

All outside the frozen predicates, counters and targets; the frozen counters are unchanged after the freeze commit except E1.

- **E1** (before any seat existed): the C3 tokenizer stopped stripping a leading dot; before-state 8 → 5 (`claims-erratum.md`).
- **E2** the frozen C1 counter can hang when its first two id draws collide (1/401 per run); not changed — `c1-supplement.py` draws distinct ids and runs the frozen counter only with a seed that does not collide.
- **E3** the frozen C1 counter inherits an ambient `ASSIMILATE_CITES`; not changed — the supplement removes the variable from the tool's environment; run the frozen counter as `env -u ASSIMILATE_CITES python3 …`.
- **E4** the round-50 echo and const controls delegated to the lane tool; the round-51 copies delegate to `controls/tool-before.py` (a control pins its base, QUALITY 85); the before receipts were produced at the base, where the two were the same tool.
- **Tool v2** (`tools/assimilate-rows.py` after the W1 `R51ReviewAdopterCode` review, commit `cf642c66`): per-entry substitution and citation (F1), the id right after `source:` on header lines only (F3), refusal of a `source:` id that is neither staged nor a Registry row (F4); `corpus/fixtures/assimilate-selftest/` extended (a no-space `source:` line, a cross-entry body mention, a tail id) — digest `3b7ad258…`, 27 findings. Not fixed, named: the twin-id `held` label and the refusal ordering (F5, F6).
- **Not done:** the W1 `R51ExecCaptureForm` zip-member form and the `MutAdopter` survivors MUT04 and MUT06 (no real behaviour differs: registry identity already uses the escaped-pipe splitter, and the outside-row check refuses a registry with no heading and rows).

