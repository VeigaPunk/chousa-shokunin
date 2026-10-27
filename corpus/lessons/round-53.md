# Round 53 lesson

author: chousa L1 (hyaku run 9, `ChousaR53`)  
date: 2026-10-26  
base: `5b550133d79bc09c82d8965cce2e48c2598b8c3e`  
freeze: `a6ff732c70011f11c9beb681d832cedc6e75f566`; C1 candidate `32aab5edd70e43145cae72ec872278f3bc6efba7`

No external fetch or network egress: L0 `8d77e6c1` remains open. Every source re-opened below is an on-disk capture under the read-only campaign cache `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache` (key = first 24 hex of sha256 of the URL), accessed 2026-10-26 (captures written 2026-10-23/24). Text form: each capture's `.txt` sidecar read as UTF-8. The two PDF forms (S117, S118) are `pdftotext -layout` readings; every quote on them also occurs, whitespace removed, in an independent pypdf extraction (`uv run --quiet --with pypdf python corpus/evidence/round53/pdf-crosscheck.py` → `PDF_QUOTES=49 NOT_IN_INDEPENDENT=0`), so no quote is a two-column glue (W1 `R53ExecPdfForm`: 50.2 % of the JMLA body sits on paired-column lines).

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| 1. stale count: three committed sites state a `claims-erratum.md` range that stops short of the erratum's last bullet — `SCORECARD.md:2664` and `corpus/lessons/round-52.md:153` say E1–E4 against E1–E6 (`corpus/evidence/round52/claims-erratum.md:7,14,27,32,36,40`), and `SKILL.md:133` says `round51/claims-erratum.md` E1-E4 against E1–E5 (`corpus/evidence/round51/claims-erratum.md:5,31,35,39,43`) | all five files byte-identical at HEAD `6365f15` (working sha256 = HEAD sha256; `round-52.md` `fd827cf9…`, `SCORECARD.md` `c84cb2e5…`, `SKILL.md` `db1b0f42…`, `round-51.md` `b0dc9ef3…`, `claims-erratum.md` `4f423bb8…`) | round-52 closure `corpus/lessons/round-52-verifier-spotcheck.md:92` (§6.1) named the first two; the `SKILL.md:133` instance is new to this seat and nothing has carried it | three append-only `correction:` lines (verbatim below) + `corpus/evidence/round53/erratum-range-check.py` (drafted below). Shown able to fail: red `RANGES=3 STALE=3` rc 1 on the lane; green `RANGES=3 STALE=0` rc 0 on a mirror carrying only those corrections |
| 2. province framing: a refusal rests on "out of province" where `PROVINCE.md`'s own refusal list carries no such ground, while the staged entry's headline is a search-record field and so in province | `corpus/lessons/round-52.md:64` province cell `**out of province for its spine**` and reason `(PROVINCE: out of province, report, never absorb)`; repeated in prose at `:82`; inherited verbatim from `corpus/lessons/round-51.md:70`. `PROVINCE.md:10-15` refuses exactly four lanes (`kasegi`, `kengaku`, `kumitate`, `kagi`) plus live-target research — regulator currency is none of them; `PROVINCE.md:17` is the general rule, not a ground. Disputed at `round-52-verifier-spotcheck.md:77` (§4 last reject row: "the headline … is a search-record field and so in province. Guideline currency is one of its `Unknown` bullets, not its spine") and routed at `:93` (§6.2) | round-52 closure, non-author spot-check (`R52` closure); the r51 origin of the phrase was not noticed | three append-only `correction:` lines restating the durable ground (S133 duplicates the S111 URL; S130/S131 outside the frozen by-document set) + `corpus/evidence/round53/province-ground-check.py`. Shown able to fail: red `PROVINCE_ROWS=3 UNSUPPORTED=3` rc 1; green `UNSUPPORTED=0` rc 0 |
| 3. routed-defect latency: a defect routed in a closure stayed "still open" for two rounds while the fix sat in scratch, and on the real campaign package the base tool still prints the wrong label | named `.ufo/waves/round-51/w2/R51W2ReviewToolV2.md:42-45` F5 (`renumber S011→S003 held`; "`held` still covers a same-run twin though docstring L24-27 defines it as 'a Registry row already carries'"); routed `corpus/lessons/round-51-verifier-spotcheck.md:101`; patched in scratch `.ufo/waves/round-52/w1/R52ExecAdopterTwin.md:1-5`; not landed `corpus/lessons/round-52.md:26` and `round-52-verifier-spotcheck.md:95`; landed `32aab5e` (top comment `:28-34`, `twin` at `:488`, count at `:574`). In the base blob the docstring says `held` = "a URL a Registry row already carries" (`git show 5b55013:tools/assimilate-rows.py:26-28`) while `:435-436` labels an in-run twin `held`, and `:507` prints `HELD=len(cited)-len(rows)`, conflating the two | r51 W2 reviewer; r51 and r52 closures; this seat on the real package today | landed v4 + the twin-label check. Shown able to fail: base prints `S195	S118	held` with `CITED=6 APPEND=5 HELD=1` and the check exits 1; v4 prints `S195	S118	twin` with `CITED=6 APPEND=5 HELD=0 TWIN=1` and exits 0. The latency rule (lands, or re-discloses with a named blocker that quotes the naming seat, before the next closure is scored) is **not counted** — no check yet shows it able to fail |
| 4. vacuous: the frozen C1 counter accepts `--per-leg 0` (and negative values) and then prints `LEGS=8/8 C1=PASS` with no generated package — the six generated legs are `all([])` | W1 `R53SentCounters` H1: `python3 corpus/evidence/round53/c1-count.py --per-leg 0 --seed 5` → `LEGS=8/8`, `case_lines=0` | QUALITY 81 (nonce inputs) says nothing about a zero count; none | the after-measurement uses the default (`--per-leg 3`) and `--per-leg 10`, each printing one `case` line per package (`measure-after.txt`); the frozen counter is not edited (erratum E2); QUALITY 96 binds the next counter to refuse a count below 1. Shown able to fail: the receipt's case-line count is 18 per run, and the vacuous run prints 0 |
| 5. sentence-versus-tool: the frozen R53-C1 sentence says a recheck with "no leading calendar-valid date or `NNd`" is refused, while the adopter (and the census) also accept a bare symbolic cadence such as `quarterly` | W1 `R53SentCounters` H2 (`| quarterly |` → `CITED=1 APPEND=1`, rc 0); `tools/assimilate-rows.py` `RECHECK_RE` third arm; CORPUS.md recheck column (`an ISO date, NNd, or a symbolic cadence`) | none: the counter never generates a cadence value, so the gap is invisible to every leg | disclosed as erratum E3; the tool keeps the census rule (narrowing it would break the registry contract); the next frozen predicate quotes the tool's own grammar `date, NNd or cadence` |
| 6. forgeable frozen counter, fifth round running: a 189-line tool that implements the held/twin/append map passes the frozen C1 counter 8/8 while canning REAL on the pinned digest, rejecting only the generator's four bad-date shapes, and printing the round-50 self-test strings without running it | W1 `R53CritForgeC1`; `corpus/evidence/round53/controls/forge-c1.py`; `python3 corpus/evidence/round53/c1-count.py --tool corpus/evidence/round53/controls/forge-c1.py --seed 7` → `LEGS=8/8` | QUALITY 88/91 (representation variance) — met for the map legs, which the forge had to implement; not for REAL, RECHECK or the self-test pin | the post-freeze `c1-supplement.py` (erratum E1): CALENDAR (calendar-only invalid dates, a leap-day control), REAL_PERTURBED (the real package with fresh ids, names and registry maximum), SELFTEST_RAN (a dropped expected finding must fail); landed tool `SUPPLEMENT_LEGS=3/3`, forge `1/3`. `weakness-streak.py` counts the class (RW-1) |

## Spot-check intake

| round-52 routed item (`corpus/lessons/round-52-verifier-spotcheck.md` section 6) | round-53 disposition |
|---|---|
| 1. Stale erratum range E1–E4 (the erratum carries E1–E6) | Append-only `correction:` lines in `SCORECARD.md` section `Round 53 pointer corrections`, each with an `anchor:` the check reads (W1 `R53DraftCorrections`); a third site, `SKILL.md` round-51 Gates row `E1-E4` against E1–E5, was found by W1 `R53DraftMistakes` and is corrected the same way. Mistakes row 1. |
| 2. Grey-literature r40 refusal reason | Restated in this lesson's Gate (`### Decisions`): "S133 duplicates the S111 URL; outside the frozen by-document set"; the headline is a search-record field, in province; the S130 UTF-16LE decode carries `是否检索灰色文献` once at 57497 (W1 `R53DraftCorrections`, re-run). QUALITY 93. Mistakes row 2. |
| 3. Representation variance in the next frozen C1-style counter | Folded into the FROZEN round-53 C1 counter (`Gen.spell`, `Gen.registry`: scheme, host case, trailing `/`, 0–3-space rows, space/tab heading); a spelling-keyed variant of the landed tool fails 5/8 (W1 `R53DraftQuality`). QUALITY 91. W1 `R53CritRouted` notes this is an adopter counter, not a capture-text counter: item 3's literal target (an OOXML counter) is not re-frozen this round; the rule now binds every capability counter. |
| 4. Adopter twin-id and refusal order; anchored `correction:` check (round-51 routed 2 and 4) | Twin/order: landed as C1 (`32aab5e`). Anchored check: landed as `corpus/evidence/round53/pointer-anchor-check.py` (W1 `R53ExecPointerAnchor`): red-before on the lane `ANCHORED=0/4` rc 1, after the anchored successor lines `ANCHORED=7/7`. QUALITY 94. |
| 5. Inference-ground CJK polarity leg inert | Landed: `tools/inference-ground.py` CJK negator window (W1 `R53ExecCjkPolarity`), fixtures `corpus/fixtures/inference-ground-cjk/`, check `python3 corpus/evidence/round53/cjk-polarity-check.py` → base tool `CJK_POLARITY=2/6`, landed `6/6`; the nine landed CJK entries keep identical token counts. Post-freeze change to a tool the C2 counter runs: erratum E4. QUALITY 95. |
| 6. Status-neutral strays | None this round at the fleet root or the lane root (misroot sweep in the report). |

## Gate

### Collision check (section 10, 0–3-space pattern, scratch)

`.ufo/waves/round-53/assimilation/` (W1 `R53ExecCollision`): `reg-ids` 116 (S001–S116), `staged-ids` 114, `collisions` 35 (S082–S116); guard proved on an indented-row fixture (`guard-proof.txt`: the 0–3-space pattern catches `  | S002 |`, the column-zero pattern misses it). Renumber by document (adopter v4, `--entry` for the three admitted entries, the QCG entry without its S190 line): S134→S117 append, S185→S118 append, S186→S119 append, S193→S120 append, S195→S118 **twin** (`CITED=5 APPEND=4 HELD=0 TWIN=1`). The registry gained S117–S120 after the scratch mirror validated (W1 `R53ExecMirrorCensus`: exit 0, the five pre-existing W04 only, with S190 omitted and Cochrane renumbered S120).

### Re-opened sources (access 2026-10-26; no fetch)

| lane id | document | URL | text form | headline quote (location) |
|---|---|---|---|---|
| S117 | Rethlefsen & Page, PRISMA 2020 and PRISMA-S: common questions on tracking records and the flow diagram, JMLA 110(2) 2022 | https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061 | `.txt` UTF-8, 27,659 characters | tracking records and the flow diagram (char 447) |
| S118 | 药品临床综合评价质量控制指南（2024 年版 试行）, issued text | https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf | `.txt` UTF-8, 27,609 characters | 数据库应包括多个中、英文专业数据库。 (char 10360) |
| S119 | the society's posting of the centre's release notice | http://m.bjhea.org.cn/35/202501/1126.html | `.txt` UTF-8, 1,255 characters | 发布时间：2025年01月03日 来源：国家卫生健康委卫生发展研究中心 (char 517) |
| S120 | Cochrane Handbook chapter 4, Searching for and selecting studies (v6.5.1, last updated March 2025) | https://training.cochrane.org/handbook/current/chapter-04 | `.txt` UTF-8, 210,708 characters | the reporting aligns with the current reporting guidance for PRISMA (char 13480) |

Normalisation recorded here (stripped from the staged rows by the adopter, `stripped.tsv`): every staged `recheck` cell was prose (`365d — re-download the PDF and confirm …`, `180d — re-download and confirm the title block …`, `180d — re-open and confirm the posting …`, `180d — re-open the chapter …`); the lane rows carry `365d`/`180d` and each entry's `recheck:` line holds the command. Staged `opened` 2026-10-23/24 → 2026-10-26. S118's `used-by` names both citing entries (twins S185/S195; the adopter keeps the first twin's tier and scope cells, and the lane row's scope was rewritten for the issued text). The staged anchors and teaches cells were rewritten to located offsets (each `char N` in an anchor cell is a quote offset below); the S119 row's staged `1,461 characters` does not reproduce on the `.txt` (1,255) and is dropped (W1 `R53DraftGateTable`).

### Decisions (theme A, search-record instruments; W1 `R53DraftGateTable`, re-decided by the L1 where the entry drafts narrowed)

| staged entry / document | capture (key, size) | province fit | decision | reason | flip |
|---|---|---|---|---|---|
| `search-tracking-record-r40.md` (S134 → S117) | `0ae65ac01b93119d3c2f3fed`, `.txt` 27,659 chars, `.pdf` 252,991 B | in: what a tracking record counts per source and where the flow diagram puts it | **admit** | r52's admit-later flip met: this freeze names the document and the staged sentence is re-cut to its one-line piece (char 1320); the staged `should be reported in Column 2` occurs 0 times (column interleave) and is replaced by line pieces at 6355 and 6544; staged body ids S094 S114 S130 named other lane documents and were dropped | refuse if the `.txt` changes length or a quoted line is no longer unique |
| `western-instrument-alignment-r50.md` (S193 → S120, S195 → S118 twin) | `c9d1e74c3ac8d9eb332c9770` 210,708 chars; `16fe8487aa97b98576a0dbac` 27,609 chars | in: an instrument-to-instrument comparison of search reporting | **admit, narrowed** | the staged title "exists only in the western handbook's own voice" is a claim about a tradition; W1 `R53CritNegatives` found the NMPA copy (S190) names PRISMA and asks reports to be checked item by item (char 7797), so the entry is narrowed to the two documents it cites; the guideline names CHEERS and Cochrane RoB, so the staged "references list" inference is dropped | refuse if the handbook's alignment sentence stops being unique or PRISMA appears in the guideline's text form |
| `quality-control-guideline-issued-text-r48.md` (S185 → S118, S186 → S119) | `16fe8487…` as above; `cfa080b4046592eb9490a82c` 1,255 chars | in for carrier and source-hierarchy method (which carrier proves what), and for the record fields the instrument asks for; the regulator-currency question is not decided | **admit, narrowed** | the staged draft-versus-issued comparison cannot be re-derived: the staged draft string `纳入标准应基于` occurs 0 times in the capture and in 0 of the cache's 2,549 `.txt` files; the staged `可根据评价主题…` is a mis-transcription of `应根据评价主题确定纳入与排除标准，可基于“PICOS”` (W1 `R53ReviewProvince`); the entry keeps the issued wording and the notice/text split | refuse if a claim about the draft is re-added without a draft capture |
| S190 → (no lane id), 2019 NMPA notice, third-party blog print | `0435b64f65c3ea7ddc6bb92e`, `.txt` 21,573 chars, `.pdf` 960,118 B | the record field `是否检索灰色文献` is in province; the regulator's mandate is not this lane's to absorb | **refuse (document)** | no admitted claim rests on it after narrowing, and a tier-C copy may not be sole support (QUALITY 7); the original NMPA URL's capture is a `.fail` (`rc=22`), so no second carrier exists | an entry whose search-record claim needs the notice's report-field sentence, with the NMPA original or an official carrier captured |

refused-doc https://pharmwyp.com/posts/56814/6.%E7%89%B9%E5%88%AB%E4%B8%93%E9%A2%98/6.10%E8%8D%AF%E7%89%A9%E8%AD%A6%E6%88%92/20190618_NMPA_%E5%85%B3%E4%BA%8E%E5%8F%91%E5%B8%83%E4%B8%8A%E5%B8%82%E8%8D%AF%E5%93%81%E4%B8%B4%E5%BA%8A%E5%AE%89%E5%85%A8%E6%80%A7%E6%96%87%E7%8C%AE%E8%AF%84%E4%BB%B7%E6%8C%87%E5%AF%BC%E5%8E%9F%E5%88%99%EF%BC%88%E8%AF%95%E8%A1%8C%EF%BC%89%E7%9A%84%E9%80%9A%E5%91%8A%EF%BC%882019%E5%B9%B4%E7%AC%AC27%E5%8F%B7%EF%BC%89.pdf — tier-C third-party print of the 2019 NMPA notice; no admitted claim rests on it; the original's capture is `.fail rc=22`

Neighbours (re-decided this round):

| staged entry | decision | reason | flip |
|---|---|---|---|
| `search-log-fields-r36.md` (S082, S083, S090) | **refuse** (third time) | S082 is still a 267-byte challenge page; `copied and pasted exactly as run` occurs 0 times in 2,549 `.txt` files; the newest capture is 2026-10-24 23:26 (no fetch under L0 `8d77e6c1`); S083 is the same chapter as lane S120 at another host (identical 210,708-character text form), so it would be S120's twin, not a document | a readable capture of S082 plus the S090 row re-pointed to its `_pdf` form |
| `grey-literature-and-chinese-search-record-r40.md` (S130, S131, S133) | **refuse** | S133 duplicates the S111 URL; outside the frozen by-document set. The headline (a report must state whether grey literature was searched) is a search-record field and in province — round 52's "out of province for its spine" reason is withdrawn (closure section 6 item 2). The S130 `.doc` has no defined text form: its UTF-16LE decode (121,964 chars, 887 U+FFFD) carries `是否检索灰色文献` once at 57497, the `.txt` sidecar 0 times | a defined OLE `.doc` text form and the regulator field decided on its own source, currency kept as an Unknown |
| `archived-translation-currency-r41.md` (S137, S138, S146) | **refuse** | the document is lane S116 already (same raw bytes, sha256 `ba9bc9c1…`), so no per-document credit; S138's first URL has only a `.fail` capture | a third capture state in the timemap or a live publisher copy |

### Quarantine slice (hand-checked this round; W1 `R53ExecQuarantine`)

The lane's register slice has 24 data rows (`awk` of section 10 over `absent-defect-register.md`, every line carrying an S-id); 0 name a theme URL, also under scheme, `www.`/`m.`, percent-encoding, query and trailing-slash normalisation over all 325 register rows (0 occurrences of any theme host). `python3 corpus/evidence/round53/c2-count.py | grep QUARANTINE` → `QUARANTINE_VERDICTS=0/0`. Every slice row carries a verdict statement in some earlier lesson; 18 of 24 lack the canonical `register S… verdict:` line and three ids carry contradicting verdicts across lessons (S104, S114 present in round 48 vs absent-as-written in round 51; S077 unverifiable in the round-42 spot-check, superseded by present in round 48) — recorded, not re-adjudicated: none is a theme document this round.

### Non-author spot-check requested

Admit `search-tracking-record-r40.md` (S117): re-open the `.txt` and check `reporting the number of records identified from each information source.` once at char 1320, and that the staged joined sentence occurs 0 times. Admit `western-instrument-alignment-r50.md`: check `the reporting aligns with the current reporting guidance for PRISMA` once at 13480 in the Cochrane `.txt`, and `PRISMA` 0 times in the guideline's `.txt`. Reject S190 (the NMPA blog print): check that no admitted entry cites it and that the NMPA original's cache key `b5c2c7c891a79ecbc9317cd8` holds only a `.fail`. Reject `search-log-fields-r36.md`: `01f657b3d0ab045c494b3f92.txt` is still a challenge page.

## considerthese

`considerthese/2026-10-26.md` proposal 2 (recurring weaknesses as streaks; W1 `R53ScoutConsiderthese` picked it as the one still-open proposal in province) implemented as `corpus/evidence/round53/weakness-streak.py` with `recurring.tsv`: `python3 corpus/evidence/round53/weakness-streak.py --root . --table corpus/evidence/round53/recurring.tsv`. The forgeable-frozen-counter class (RW-1) reads a streak of 5 with this lesson (rounds 49–53): the streak is exposure, not failure — pair it with each round's C1 verdict.

## All located quotes

Every quote below is ≤25 whitespace words and ≤160 characters, on one line of its `.txt` form, occurring there exactly once at the stated offset (`python3 corpus/evidence/round53/build-spans.py --check` → `STALE=0`).

| id | char | quote | entry |
|---|---:|---|---|
| S117 | 447 | tracking records and the flow diagram | `corpus/knowledge/search-tracking-record-r40.md` |
| S117 | 401 | PRISMA 2020 and PRISMA-S: common questions on | `corpus/knowledge/search-tracking-record-r40.md` |
| S117 | 485 | Melissa L. Rethlefsen, AHIP; Matthew J. Page | `corpus/knowledge/search-tracking-record-r40.md` |
| S117 | 1605 | flow diagram and tracking records through the systematic review process | `corpus/knowledge/search-tracking-record-r40.md` |
| S117 | 1320 | reporting the number of records identified from each information source. | `corpus/knowledge/search-tracking-record-r40.md` |
| S117 | 1288 | PRISMA-S also recommends | `corpus/knowledge/search-tracking-record-r40.md` |
| S117 | 9058 | records retrieved from each information source should be | `corpus/knowledge/search-tracking-record-r40.md` |
| S117 | 9183 | tracked, which aligns with PRISMA-S’s guidelines. | `corpus/knowledge/search-tracking-record-r40.md` |
| S117 | 6355 | citation searching, and other methods should be reported | `corpus/knowledge/search-tracking-record-r40.md` |
| S117 | 6544 | in Column 2. The flow diagram template also suggests | `corpus/knowledge/search-tracking-record-r40.md` |
| S117 | 6893 | databases and registers in Column 1. | `corpus/knowledge/search-tracking-record-r40.md` |
| S117 | 7694 | represents the “Additional records identified through | `corpus/knowledge/search-tracking-record-r40.md` |
| S117 | 13633 | Citation indexes are indeed databases and can be included | `corpus/knowledge/search-tracking-record-r40.md` |
| S117 | 14417 | combine them in Column 1 in the flow diagram. | `corpus/knowledge/search-tracking-record-r40.md` |
| S117 | 10646 | PRISMA-S does recommend that, if space is available, | `corpus/knowledge/search-tracking-record-r40.md` |
| S117 | 11685 | records per individual information source should go in the | `corpus/knowledge/search-tracking-record-r40.md` |
| S117 | 12842 | Google Scholar is both a database and a citation index | `corpus/knowledge/search-tracking-record-r40.md` |
| S117 | 15089 | reported in Column 2. | `corpus/knowledge/search-tracking-record-r40.md` |
| S117 | 17488 | Best practice is to count all records identified (by | `corpus/knowledge/search-tracking-record-r40.md` |
| S117 | 17083 | When records are all centrally | `corpus/knowledge/search-tracking-record-r40.md` |
| S117 | 17114 | tracked, regardless of source, it is easier to produce this | `corpus/knowledge/search-tracking-record-r40.md` |
| S117 | 14231 | records identified per search in the supplementary | `corpus/knowledge/search-tracking-record-r40.md` |
| S117 | 19789 | PRISMA-S treats all results from the same search, | `corpus/knowledge/search-tracking-record-r40.md` |
| S117 | 20115 | update, as a single data point [3]. In the PRISMA 2020 | `corpus/knowledge/search-tracking-record-r40.md` |
| S117 | 20387 | per database across the lifespan of the systematic review | `corpus/knowledge/search-tracking-record-r40.md` |
| S117 | 8863 | PRISMA-S was released slightly before PRISMA 2020, so | `corpus/knowledge/search-tracking-record-r40.md` |
| S117 | 8993 | the styles do not entirely align, but they are compatible | `corpus/knowledge/search-tracking-record-r40.md` |
| S120 | 7432 | Chapter 4: Searching for and selecting studies [last updated March 2025] | `corpus/knowledge/western-instrument-alignment-r50.md` |
| S120 | 7647 | version 6.5.1 Cochrane, 2025 | `corpus/knowledge/western-instrument-alignment-r50.md` |
| S120 | 7735 | Cochrane reviews take a systematic and comprehensive approach | `corpus/knowledge/western-instrument-alignment-r50.md` |
| S120 | 9949 | Medical/healthcare librarians and information specialists have an integral role in the production of Cochrane reviews. | `corpus/knowledge/western-instrument-alignment-r50.md` |
| S120 | 13480 | the reporting aligns with the current reporting guidance for PRISMA | `corpus/knowledge/western-instrument-alignment-r50.md` |
| S120 | 35599 | Initiatives to provide access to ongoing studies and unpublished data constitute a fast-moving field | `corpus/knowledge/western-instrument-alignment-r50.md` |
| S120 | 36552 | Finding out about unpublished studies, and including their results in a systematic review when eligible and appropriate | `corpus/knowledge/western-instrument-alignment-r50.md` |
| S120 | 36693 | is important for minimizing bias | `corpus/knowledge/western-instrument-alignment-r50.md` |
| S118 | 78 | 二〇二四年十二月 | `corpus/knowledge/western-instrument-alignment-r50.md` |
| S118 | 9938 | 1.文献研究的质量控制 | `corpus/knowledge/western-instrument-alignment-r50.md` |
| S118 | 10119 | 应获取最新的、权威的且已公开发表 | `corpus/knowledge/western-instrument-alignment-r50.md` |
| S118 | 10360 | 数据库应包括多个中、英文专业数据库。 | `corpus/knowledge/western-instrument-alignment-r50.md` |
| S118 | 10394 | 如遇分歧，则由第三方协助判断。 | `corpus/knowledge/western-instrument-alignment-r50.md` |
| S118 | 10459 | 根据文献筛选流程制定流程图，注明每环节 | `corpus/knowledge/western-instrument-alignment-r50.md` |
| S118 | 11148 | （4）证据质量评价 | `corpus/knowledge/western-instrument-alignment-r50.md` |
| S118 | 17860 | 在同行评议期刊已发表 | `corpus/knowledge/western-instrument-alignment-r50.md` |
| S118 | 18046 | 指标 4：在文献检索和筛选阶段，是否参照 Cochrane 等组织制定的 | `corpus/knowledge/western-instrument-alignment-r50.md` |
| S118 | 18091 | 相应规范或指南开展文献检索，提供系统检索策略和文献筛选流程 | `corpus/knowledge/western-instrument-alignment-r50.md` |
| S118 | 24614 | Cochrane RoB 等 | `corpus/knowledge/western-instrument-alignment-r50.md` |
| S118 | 25343 | 卫生经济学评价报告标准共识 | `corpus/knowledge/western-instrument-alignment-r50.md` |
| S118 | 78 | 二〇二四年十二月 | `corpus/knowledge/quality-control-guideline-issued-text-r48.md` |
| S118 | 3334 | 内容，形成《药品临床综合评价质量控制指南（2024 年版 讨论 | `corpus/knowledge/quality-control-guideline-issued-text-r48.md` |
| S118 | 3549 | 控制指南（2024 年版 试行）》。 | `corpus/knowledge/quality-control-guideline-issued-text-r48.md` |
| S118 | 9938 | 1.文献研究的质量控制 | `corpus/knowledge/quality-control-guideline-issued-text-r48.md` |
| S118 | 10109 | 对于循证指南类证据，应获取最新的、权威的且已公开发表 | `corpus/knowledge/quality-control-guideline-issued-text-r48.md` |
| S118 | 10167 | 证据，应根据评价主题确定纳入与排除标准，可基于“PICOS” | `corpus/knowledge/quality-control-guideline-issued-text-r48.md` |
| S118 | 10360 | 数据库应包括多个中、英文专业数据库。由两名研究人员独立筛 | `corpus/knowledge/quality-control-guideline-issued-text-r48.md` |
| S118 | 10390 | 选文献，如遇分歧，则由第三方协助判断 | `corpus/knowledge/quality-control-guideline-issued-text-r48.md` |
| S118 | 10450 | 确定最终是否纳入。根据文献筛选流程制定流程图，注明每环节 | `corpus/knowledge/quality-control-guideline-issued-text-r48.md` |
| S118 | 27444 | 提供项目主要的技术附件，如检索策略、检索结果和纳入/排除研究列表、 | `corpus/knowledge/quality-control-guideline-issued-text-r48.md` |
| S119 | 517 | 发布时间：2025年01月03日 来源：国家卫生健康委卫生发展研究中心 | `corpus/knowledge/quality-control-guideline-issued-text-r48.md` |
| S119 | 695 | 我中心联合相关领域专家 | `corpus/knowledge/quality-control-guideline-issued-text-r48.md` |
| S119 | 755 | 现予以发布 | `corpus/knowledge/quality-control-guideline-issued-text-r48.md` |
| S119 | 764 | 药品临床综合评价质量控制指南（2024年版 试行）》采用开放式动态修订机制，长期接受来自社会各界的建议。 | `corpus/knowledge/quality-control-guideline-issued-text-r48.md` |
| S119 | 841 | 附件： 药品临床综合评价质量控制指南（2024年版 试行）.pdf | `corpus/knowledge/quality-control-guideline-issued-text-r48.md` |
| S119 | 920 | 2024年12月31日 | `corpus/knowledge/quality-control-guideline-issued-text-r48.md` |

## Census

Round start (`corpus/evidence/round53/census-start.txt`): exit 0, `ok`, five pre-existing W04 (S051 S053 S073 S074 S075). After the append: exit 0, the same five W04. Rows 116 → 120 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`).

## Disclosed post-freeze changes

`corpus/evidence/round53/claims-erratum.md` E1–E6: the C1 supplement (E1), the vacuous `--per-leg 0` (E2), the cadence gap between sentence and tool (E3), the CJK polarity window added to a tool the C2 counter runs (E4), the unexercised `ENTRIES` minimum (E5) and the in-round narrowing (E6).

