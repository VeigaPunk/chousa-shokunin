# Round 55 lesson

author: chousa L1 (hyaku run 9, `ChousaR55`)  
date: 2026-10-27  
base: `dba605deb5cd5ed4874e0e3c39ba24737409cd80`  
freeze: `1fc5d92b5a7866ec16f1cac2de749fccfa6b49cb`; C1 candidate `6ca924995d48facbf704d2aa22ddaec236059039`

No external fetch or network egress: L0 `8d77e6c1` remains open. Every source re-opened below is an on-disk capture under the read-only campaign cache `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache` (key = first 24 hex of sha256 of the URL), accessed 2026-10-27; the campaign's own quotes and dates were not reused.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| 1. report filed while a dispatched wave was still running: the round-54 report landed at 23:50:07 (fleet `86023b97`) and says it "was filed before W2 WAVE-DONE"; W2 was then killed in the orchestrator's session exit at 23:57:36 and its results reached the lane only through the orchestrator's salvage `78ebc257` (00:22:58) | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-54/chousa.md:97-98`; `.ufo/waves/round-54/w2-results.json` `note` and `settled_by`; W1 `R55DraftMistakes` §1 | the round prompt's own rule ("Do not file the report before WAVE-DONE for every wave you launched") — stated, never checked by any lane command | `python3 corpus/evidence/round55/wave-settled-check.py --round 54` → `UNSETTLED w2 results=2026-10-27T00:22:58-03:00 after report=2026-10-26T23:50:07-03:00`, `WAVES=2 SETTLED=1`, exit 1; round 52 → `SETTLED=2` exit 0 (`corpus/evidence/round55/wave-settled-check.txt`); this round's report is filed only after `--before-filing` exits 0 (QUALITY 104) |
| 2. an unrun number written as the shown-able-to-fail result: the round-54 lesson's Mistakes row 2 says the mirror without the two dumps prints `BAD=6`; run, it prints `ANCHORED=7/16 UNANCHORED=9 BAD=9` (`BAD=6` is the S101-dump-only case) | `corpus/lessons/round-54.md:15`; W2 `R54W2CritMistakes.md:17`; erratum E08 in `SCORECARD.md` "Round 55 statement errata" | none — the row's `captured-by` names a criterion, but no rule asks that a "shown able to fail" figure be pasted from a run | the observation is now recomputed by `corpus/evidence/round55/c3-count.py` (E08, a BASE mirror without both dumps); the RESTATE control that restates `BAD=6` prints `E08 WRONG` (`controls/c3-controls.txt`) |
| 3. a supplement's isolation claim stated as a boundary it was not: round 54's `c1-supplement.py` says each generated document is copied "outside the generation tree (no HTML, no sibling)", while its oracle exports and the ISOLATED leg's generation HTML sit two directories above the isolated file, so an echo tool that never opens the `.doc` scores `SUPPLEMENT_LEGS=3/3` | `corpus/evidence/round54/c1-supplement.py:9-11`; W2 `R54W2SentFinal.md` F1; erratum E11 | QUALITY 98 ("an oracle also has to be out of the tool's reach") — named, but no check ran a tool that reads the work tree | the round-55 C1 counter keeps expected offsets in memory only, deletes each generation tree before the run and audits reads (`corpus/evidence/round55/c1-count.py` HOOK); W1 `R55CritForgeEcho` and `R55CritForgeReader` scored their non-reading tools 1/4 and 0/4 under it; QUALITY 102 |

## Spot-check intake

`corpus/lessons/round-54-verifier-spotcheck.md` section 6, item by item: (1) the uncommitted W2 output — committed by the orchestrator's salvage `78ebc257` below this round's base (22/38 outputs recovered; 16 seats null, 6 of them with report files); nothing re-committed; (2) the W2 findings — the eleven lane statements W2 falsified are C3's E01–E11 (anchored errata in `SCORECARD.md`, in-target corrections below); the remaining findings are dispositioned in the integration register (`.ufo/waves/round-55/w1/R55RegisterW2A.md`, `R55RegisterW2B.md`), the supplement and ledger hazards in QUALITY 102–103 and `corpus/evidence/round55/considerthese-ledger-check.py`; (3) RW-1, the sixth round — the round-55 C1 counter is built against each demonstrated mechanism (claims.md "Routed items"); W1 forges are recorded under the C1 verdict; (4) the r36 wording — the entry's `#### Corrections (round 55)` (E01, E03); (5) QUALITY 97 F1 — QUALITY 101 and errata E05–E07; (6) Mistakes row 2 — row 2 above and erratum E08; (7) the five W04 warnings — adjudicated below.

## Corrections

Appended corrections for statements this lane filed earlier (append-only: the statements stay; `SCORECARD.md` "Round 55 statement errata" anchors each one and `python3 corpus/evidence/round55/c3-count.py` re-derives every observation):

- E01–E04 (`corpus/knowledge/source-type-taxonomy-r36.md`): the entry's appended `#### Corrections (round 55)` section.
- E05–E07, E09, E10 (`corpus/QUALITY.md` 97 and 98): QUALITY 101.
- E08 (`corpus/lessons/round-54.md` Mistakes row 2): the mirror without both dumps prints `ANCHORED=7/16 UNANCHORED=9 BAD=9`; `BAD=6` is the case with S101's dump alone missing (S100's alone gives `BAD=3`; W2 `R54W2CritMistakes`).
- E11 (`corpus/evidence/round54/c1-supplement.py` docstring): left as filed (it is round-54 evidence and its digest is cited); its isolation sentence holds for the document file only — the work tree two levels up holds the oracle exports and the generation HTML (Mistakes row 3).

## Gate

### Collision check (section 10, 0–3-space pattern, scratch)

`.ufo/waves/round-55/assimilation/` (L1 commands; W1 `R55ExecCollision` re-derived all four files byte-identical): `reg-ids` 123 (S001–S123), `staged-ids` 114, `collisions` 42 (S082–S123), `quarantine-slice` 24. Guard proved in `guard-proof.txt`: a two-space-indented `  | S002 |` row collides under the 0–3-space pattern and not under the column-zero one. Renumber by document (the URL is the evidence, the id follows it): staged S130 → S124 (`http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc`), S131 → S125 (`http://m.cnpharm.com/201906/18/c280684.html`), S143 → S126 (`https://english.nmpa.gov.cn/2019-07/18/c_388252.htm`); staged S133 is the lane's held S113 by URL (`https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3`), not cited this round (S113's `used-by` unchanged).

### Re-opened sources (access 2026-10-27; no fetch)

| lane id | document | URL | text form | headline quote (location) |
|---|---|---|---|---|
| S124 | 《上市药品临床安全性文献评价指导原则（试行）》, a copy of the NMPA guideline hosted by gcpunion.org | http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc | the stdout of `tools/capture-text.py` on the OLE `.raw` (13,718 characters, 0 U+FFFD); the `.txt` sidecar is a UTF-8 decode of the compound file (40,252 U+FFFD) and holds none of the quotes | 应当说明是否有检索限制（如语言限制）、是否手工检索、是否检索灰色文献等关键问题。 (char 4652) |
| S125 | 中国食品药品网 report of the release, 记者 郭婷 | http://m.cnpharm.com/201906/18/c280684.html | `.txt` UTF-8, universal newlines, 1,673 characters | 6月18日，国家药品监督管理局发布通告，发布《上市药品临床安全性文献评价指导原则（试行）》 (char 371) |
| S126 | NMPA English site notice of the guideline | https://english.nmpa.gov.cn/2019-07/18/c_388252.htm | `.txt` UTF-8, universal newlines, 3,774 characters | which was issued on June 18, 2019 (char 1324) |

Recheck prose stripped from the staged rows (the rows keep `180d`): S130 "re-download the .doc, decode its UTF-16 body …" — the UTF-16 decode is the undefined form round 54 retired; the entry's `recheck:` runs `tools/capture-text.py --locate`; S131 "re-open the page and confirm the body still …"; S143 "re-open the page and confirm it still reads …".

### Decisions (theme: the NMPA grey-literature search-record field; W1 `R55DraftGate`, re-decided by the L1)

| staged entry | documents | capture on disk | province fit | decision | reason | flip |
|---|---|---|---|---|---|---|
| `grey-literature-and-chinese-search-record-r40.md` | S130→S124, S131→S125, S143→S126; S133 (= held S113) | `bdff491a75c6abeda1d9c01d` (.raw 243,929 B); `27d4865f201e99c1fed9f79b`; `d663d66e2d39f868d84b1781` | in: search-record method — which fields a report must state (W1 `R55ReviewProvinceC2`; the drug-safety evaluation practice is adjacent, report-only) | **admit, narrowed** | the `.doc` carries the field and the reason, but no date or issuer stamp (2019 0×, 发布 0×), so issuer and date are bound to S125/S126; 应当 is rendered "should"; the four unpublished kinds are examples; the S133 price leg and the "three literatures" and "Q15" inferences are cut (W1 `R55CritEntailObs`, `R55CritEntailInf`); currency stays Unknown (W1 `R55CritCurrency`) | — |
| `grey-literature-field-boundary-r43.md` | S161 (Guizhou provincial page) | not opened this round | adjacent: a provincial implementation of a different national quality-control guideline | **refuse (this round)** | it argues a boundary (a document with no grey-literature wording), which does not bear on the NMPA field; no quote set exists in a defined form | its own round, with the document opened and the boundary claim located in its form |

refused-doc https://wjw.guizhou.gov.cn/zwgk/zdlyxx/ywgl/202505/t20250530_87947626.html — staged S161, cited only by the refused r43 entry; not bound this round.

### Quarantine slice (hand-checked this round)

The lane's register slice has 24 data rows (`quarantine-slice`); one names a theme URL (W1 `R55ExecQuarantine`: whole-register scan for gcpunion, cnpharm, english.nmpa and medsci finds only it):

- register `S125` (round6) — http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc — verdict: absent-as-written — of its three quoted strings, the 文献检索策略 sentence occurs once (char 4625) and the 检索策略包括 sentence once (char 761) in the defined OLE form, but the third, `…即灰色文献，如会议论文…`, occurs 0 times as written: the document prints `即“灰色文献”` with curly quotes (char 994). The register's `payload-absent` is wrong for two quotes and right only as written for the third; nothing is fabricated. (The `.txt` sidecar holds 0/0/0 of them and the UTF-16LE decode 1/1/0 — neither is the defined form.)

### Admit and reject for the non-author spot-check

Admit `grey-literature-and-chinese-search-record-r40.md` (S124): run `python3 tools/capture-text.py /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/bdff491a75c6abeda1d9c01d.raw --locate '是否检索灰色文献'` → `LOCATED count=1 offset=4678`, and check that the entry renders 应当 as "should" and binds the issue date to S125/S126, not to the `.doc`. Reject the S133 leg: check that the entry carries no `source: S113` line and no price inference, and that S113's `used-by` is unchanged; the medsci capture (`453d492becd9a2f4632cb8dd.txt`) shows `paymentAmount=10` as a page field only.

### W04 duplicate-url adjudication (carried since round 51; W1 `R55ScoutW04`)

`scripts/sources-census.sh validate` warns W04 for S051, S053, S073, S074 and S075 (same URL across scopes). All five are kept, no status changed: S050/S051 cite different sections of the HTML 5.2 syntax page (optional tags vs in-head tree construction); S052/S053 different sections of the Python socket page (timeout modes vs `create_connection`); S071/S075 different coreutils commands (`env -u` vs `mktemp -d`); S074 is already a `rejected` duplicate proposal of S059's hashlib scope; S073 is the appended correction that `supersedes S070` (anchor label only — S070's quote and offsets stand, and two entries still cite it, so S070 stays `mined`). W04 is a warning about URL reuse, and here each reuse is a distinct scope or a recorded supersession.

## considerthese

W1 `R55ScoutConsiderthese`: `python3 corpus/evidence/round54/considerthese-ledger-check.py --root .` → `PROPOSALS=35 ROWS=35 IMPL=24 FMT=9 OPEN=1 OPS=1 BAD=0`; no considerthese file or bullet is newer than the round-54 ledger, and none of the two non-implemented rows (CT-20261019-4 OPEN, CT-20261022-2 OPS) fits this round's claims. Mined: none this round (sweep above). The round-54 checker's own hazards (W2 `R54W2SentFinal` F5: an absolute pointer escapes the root, a regex cell can backtrack without bound, a read is uncapped, an empty tree passes) are fixed in its round-55 successor `corpus/evidence/round55/considerthese-ledger-check.py`.

## All located quotes

Every quote below is ≤25 whitespace words and ≤160 characters, on one line of its defined text form, occurring there exactly once at the stated offset (`python3 tools/build-spans.py --quotes corpus/evidence/round55/quotes.tsv --out corpus/evidence/round55 --check` → `STALE=0`).

| id | char | quote |
|---|---:|---|
| S124 | 4625 | 文献检索策略：检索途径、检索数据库、检索时限及检索式。 |
| S124 | 4652 | 应当说明是否有检索限制（如语言限制）、是否手工检索、是否检索灰色文献等关键问题。 |
| S124 | 761 | 检索策略包括检索的数据库、检索范围（如主题等）、检索词、检索式（即检索词组合方式）和时间范围等 |
| S124 | 994 | 查找时应当注意收集未公开发表的文献，即“灰色文献”，如会议论文、未发表的学位论文、产业报告、咨询报告等。 |
| S124 | 1046 | 灰色文献中可能包含阴性研究结果 |
| S124 | 1082 | 若文献评价中只纳入已公开发表的文献会引入发表偏倚 |
| S124 | 4 | 上市药品临床安全性文献评价指导原则 |
| S124 | 22 | （试行） |
| S124 | 33 | 国家药品监督管理局《关于药品上市许可持有人直接报告不良反应事宜的公告》（2018年第66号）第四款规定 |
| S124 | 5428 | 四、本指导原则所依据的参考文献 |
| S124 | 340 | 引进了Cochrane系统评价规范化操作流程和全程质量控制的方法 |
| S125 | 242 | 作者：郭婷 2019-06-18 来源：中国健康传媒集团-中国食品药品网 |
| S125 | 371 | 6月18日，国家药品监督管理局发布通告，发布《上市药品临床安全性文献评价指导原则（试行）》 |
| S125 | 780 | 指导原则分为概述、方法学要点、报告撰写规范、指导原则所依据的参考文献和附录五个方面 |
| S125 | 951 | 引进了Cochrane系统评价规范化操作流程和全程质量控制的方法 |
| S126 | 1204 | NMPA organized the formulation of the Guidelines for Clinical Safety Literature Evaluation of Marketed Drugs (Interim) |
| S126 | 1324 | which was issued on June 18, 2019 |
| S126 | 777 | Updated: 2019-07-18 |
| S126 | 2528 | the Guidelines introduces the standardized operation process and the whole process of quality control methods of Cochrane Systematic Review |

## Census

Round start (`corpus/evidence/round55/census-start.txt`): exit 0, `ok`, five pre-existing W04 (S051 S053 S073 S074 S075, adjudicated above). Round end: `corpus/evidence/round55/census-end.txt`. Rows 123 → 126 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`); added S124 (B), S125 (B), S126 (A); no existing row touched (S113's `used-by` unchanged; S070 unchanged).
