# R56GroundQcg — does S118 answer the staged entries' `#### Unknown`?

Seat: ground (chousa lane, round 56 W1). Scope: read-only grounding of the 灰色文献 question against the lane's held
`S118` (the issued 药品临床综合评价质量控制指南（2024 年版 试行）), not a C1/C2 measurement. Lane worktree observed at
`0c2f4ce5b846526ad3d7f384cd517fb5470806db` (read; no write); frozen claims read first
(`corpus/evidence/round56/claims.md`, lane commit `41c58925`). No production file, index, jj state or sibling lane touched.

## Question

Staged `grey-literature-field-china-r42.md` (r42 package) `#### Unknown`, lines 48–51:

> Whether the 2024 试行 质量控制指南 — whose host times out from here — lists
> 灰色文献 the same way and with the same grade.

Staged `grey-literature-national-route-r44.md` `#### Unknown`, line 47: `Whether the national centre's own 2024 试行
质量控制指南 lists the same field.` — with the premise (line 48) that its text `is known only through a search index`.

S118 is the same document; the lane holds it and has read it. Answer given below, with counts, completeness and quotes.

## Method (commands as run)

```
python3 -c "p='.../.qcache/16fe8487aa97b98576a0dbac.txt';s=open(p,encoding='utf-8',errors='replace').read();
 print('chars',len(s),'lines',s.count(chr(10))+1);[print(t,s.count(t)) for t in ('灰色文献','灰色','未公开发表','会议','检索')]"
chars 27609 lines 1525
灰色文献 0 / 灰色 0 / 未公开发表 0 / 会议 2 / 检索 12
```

```
uv run --with pypdf python -c "...PdfReader('.qcache/16fe8487aa97b98576a0dbac.pdf'); pages=42; empties=0;
 chars=21560; {灰色文献:0, 灰色:0, 未公开发表:0, 会议:2, 检索:12}"
pages 42 empty_pages [] chars 21560
```

Wider sweep, both forms (`灰`, `未发表`, `未公开`, `内部资料`, `会议论文`, `会议摘要`, `检索策略`, `Ⅰ级`, `GRADE`):

| term | form (`.txt`, 27,609 ch) | pypdf 6.21.2 (21,560 ch) |
|---|---|---|
| 灰色文献 / 灰色 / 灰 | 0 / 0 / 0 | 0 / 0 / 0 |
| 未公开发表 / 未发表 / 未公开 / 内部资料 | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 |
| 会议 (both = 会议日程, 会议纪要 at char 16515/16537) | 2 | 2 |
| 检索 (methodology/checklist; no source-class list) | 12 | 12 |
| 公开发表 (10131: `应获取最新的、权威的且已公开发表`) | 1 | 1 |
| Ⅰ级 / Ⅱ级 | 0 / 0 | 0 / 0 |
| GRADE | 1 | 1 |

Completeness (the seat's check): the PDF is **42 pages**, pypdf extracts text from **all 42** (no empty page), 21,560
characters; the form is **27,609 characters with 42 U+000C page breaks, 0 U+FFFD, 1,525 lines**; and the two agree on
**20,390 non-whitespace characters each** (form whitespace 7,219, pypdf 1,170 — the whole 6,049-character gap is layout
whitespace). Marker coverage spans the document: p.1 title, p.3 目录, p.19–20 文献研究的质量控制, p.33 the 指标 2 table,
p.41–42 附件. Provenance: `.pdf` and `.raw` are one object, sha256 `7b600fe3ee9bda2bd59f437a689451486f746af0c1daf2774aab2aec56b67e26`,
415,245 bytes; `.txt` sha256 `927ff71c6d499477c9cc7a3acf9ed7e335cd63b802850e5f39f5aa86a398d3a4`; cache key
`16fe8487aa97b98576a0dbac` = first 24 hex of sha256 of the URL (recomputed). The zeros are document facts, not
extraction gaps.

## What the guideline says about evidence sources and retrieval (form offsets, `form.find`)

- char 9953 `目前可用于药品临床综合评价的文献证据总体分为两类：循` — the taxonomy: 循证指南 (临床指南、药品使用规范、专家共识, 9976–10072) and 学术研究 (系统评价/Meta 分析、干预性研究、观察性研究、卫生技术评估). No third class, and no grey-literature class.
- char 10109 `对于循证指南类证据，应获取最新的、权威的且已公开发表` (`的临床指南…`, char 10137) — published-source floor for guideline evidence.
- char 10167 `证据，应根据评价主题确定纳入与排除标准，可基于“PICOS”` — inclusion criteria belong to the theme; PICOS optional (可).
- char 10360 `数据库应包括多个中、英文专业数据库。由两名研究人员独立筛`; 10390 `选文献，如遇分歧，则由第三方协助判断。`; 10450 `确定最终是否纳入。根据文献筛选流程制定流程图，注明每环节`.
- char 17840 `指标 2：纳入的学术研究类证据来源是否为在同行评议期刊已发表` — continues on the next line at 17871 `的全文文章或政府/官方机构发布的报告全文`. This is 附件一's checklist question, not a source list.
- char 11940 `质量评价的基础上，可使用证据质量分级和推荐强度系统（The` — the only grading clause: `…（The Grading of Recommendations Assessment, Development and Evaluation，GRADE）` (GRADE at 12071), and it is permissive (可使用). Ⅰ级 never occurs; 推荐强度 otherwise appears at 20416 (指标 12, about 诊疗指南 recommendations) and 26497 (report template).
- 检索 occurrences: 3044 (技术摸底), 14503 (附件 must carry `数据库检索策略`), 17226 (指标 6 `提供系统检索策略和文献筛选流程`), 18054/18102/18109 (指标 4, Cochrane methods), 22103 (指标 31), 27457 (六、附件). None enumerates a source class.
- 会议 occurrences: 16515 and 16537, both inside `会议日程、参会人员名单、会议纪要` for 主题遴选论证会 — meeting records, not conference literature.

## QUOTE machine lines (lane id S118, entry `corpus/knowledge/grey-literature-field-china-r42.md`)

Each verified in the run: occurs exactly once in the form, no newline, inside one line (674, 688, 692, 701, 1167, 797),
≤25 whitespace words and ≤160 characters, offset = `form.find(quote)`.

```
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	目前可用于药品临床综合评价的文献证据总体分为两类：循	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	对于循证指南类证据，应获取最新的、权威的且已公开发表	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	证据，应根据评价主题确定纳入与排除标准，可基于“PICOS”	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	数据库应包括多个中、英文专业数据库。由两名研究人员独立筛	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	指标 2：纳入的学术研究类证据来源是否为在同行评议期刊已发表	corpus/knowledge/grey-literature-field-china-r42.md
QUOTE	S118	https://www.bjhea.org.cn/ueditor/php/upload/file/20250115/1736907153935975.pdf	质量评价的基础上，可使用证据质量分级和推荐强度系统（The	corpus/knowledge/grey-literature-field-china-r42.md
```

Offsets in the same order: 9953, 10109, 10167, 10360, 17840, 11940.

**Placement constraint (operability, checked in code).** These rows must NOT go into `corpus/evidence/round56/spans.tsv`:
`c2-count.py:255` computes `on_bound += bound.get(sid) == url` and `:327` requires `on_bound == n`, while `bound` only
holds rows new since `BASE_REV`; S118 is an older row, so one S118 row in that manifest turns `ON_BOUND` short of `n`
and `C2=FAIL`. `tools/inference-ground.py` reads span files only for ids an **Inference bullet** cites
(`span_texts`, tool lines 190–215; `inference_bullets`, line 110 — Observation bullets are not grounded), so an S118
quote belongs in `#### Observation` prose (as the entry's 指标 2 quote already is), or in the lesson, never in the
manifest. `quotes-held.tsv` is read by nothing in `tools/` or the round-56 counters (grep: no hits outside itself).

## Answer

**No — S118 does not answer the staged question affirmatively; it answers it negatively, and the answer is stronger
than silence.** The centre's issued 2024 试行 质量控制指南 neither lists 灰色文献 nor grades it: 灰色 in any form occurs
0 times in the whole 42-page document in both extractions; its literature section uses a two-class taxonomy with no
grey-literature class; its only source-status test is the published-source floor for guideline evidence and 指标 2's
question whether an included 学术研究类 source is a peer-reviewed full article or a government/official report; and it
prints no Ⅰ级 label at all (its single grading clause is the optional GRADE route). So the staged phrasing "the same way
and with the same grade" has no counterpart in this document.

Exact wording the entry may carry (grounded, calibrated; drop-in for the Observation section):

> **The issued quality-control guideline does not list the field at all.** In the centre's 2024 试行 质量控制指南 the
> strings 灰色文献, 灰色, 未公开发表 and 内部资料 each occur 0 times across a 27,609-character text form (42 pages), and the
> same zero counts return from an independent extraction of the same 42-page PDF (21,560 characters; the two forms agree
> on 20,390 non-whitespace characters). Its literature section divides the evidence an evaluation may use into two
> classes only — 循证指南 (临床指南、药品使用规范、专家共识) and 学术研究 (系统评价/Meta 分析、干预性研究、观察性研究、卫生技术
> 评估) — requires guideline-type evidence to be 已公开发表, and at 指标 2 asks whether an included 学术研究类 source is a
> peer-reviewed published full article or a government/official report. It prints no Ⅰ级 grade (0 occurrences) and its
> only grading clause is permissive — 可使用证据质量分级和推荐强度系统（…GRADE）— so this document neither lists the field
> nor ranks it.

Wording that is NOT available to the entry (overreach, each checked against the text):

- ✗ "S118 excludes / bars grey literature" — 指标 2 asks about `纳入的学术研究类证据`, and the text never classifies
  unpublished material at all; it states a published-source floor for 循证指南类证据 and a checklist question elsewhere.
  The entry's existing "asks the opposite question of a source" is the defensible form; "excludes" is not.
- ✗ attributing Ⅰ级 / A to S118 — both occur 0 times; GRADE appears once at 12071 and its use is 可, not 应.
- ✗ "the requirement lives in the quality-control guideline" (below).
- ✗ calling S118 "the national management guideline" — that is `S130` (nhc.gov.cn 2020); S118 is the national centre's
  quality-control guideline. The staged r44 wording ("the national centre's own 2024 试行 质量控制指南") is the right one.
- △ the entry's Inference bullet 3 ("two pulls on the same unpublished study") is sound as an inference but should keep
  its conditional shape: S118 has no grey-literature class, so 指标 2 reaches an unpublished study only if the reviewer
  classes it as 学术研究类证据. The entry already places this in `#### Inference`.

## Findings against the staged entries (reported, not patched)

1. **FALSIFIED — staged r42 Inference, lines 41–42:** `The requirement lives instead in the quality-control guideline and
   the working group's workflow standard.` The quality-control guideline half is wrong: 灰色/灰色文献 = 0 in both forms of
   a document shown complete (42 pages, identical non-whitespace character count), and its own checks ask the published
   question. The requirement lives in the workflow guideline (`S127` draft 7.2.3.3 item （9）, `S129` journal 表 10) and
   its note (`S128`) only. The lane entry already omits the false sentence; making the negative explicit is what closes
   the staged claim.
2. **RESOLVED — staged r42 Unknown (48–51) and r44 Unknown (47–51):** the premises "whose host times out from here" and
   "known only through a search index, which is not an opened source" no longer hold — the lane holds the document as
   S118 and has read it. Both Unknowns can be closed with "no; it does not list the field at all", the wording above.
3. **SURVIVES — the lane entry's S118 material:** `corpus/knowledge/grey-literature-field-china-r42.md` Observation
   bullet 6 quotes `指标 2：纳入的学术研究类证据来源是否为在同行评议期刊已发表` at char 17840 — verified: once, one line,
   30 characters, and its continuation at 17871 is a separate line (`的全文文章或政府/官方机构发布的报告全文`), which the
   entry's prose correctly notes. Its sentence "its text form holds 灰色 zero times" is confirmed and now strengthened by
   the independent extraction. `python3 tools/inference-ground.py --entry corpus/knowledge/grey-literature-field-china-r42.md
   --spans corpus/evidence/round56/spans.tsv --counts /dev/null --registry corpus/SOURCES.md --root .` prints
   `GROUND entry=… section=1 bullets=3 tokens=6 grounded=6` / `GROUND: PASS`, exit 0 (observed on the worktree rev above).
4. **Cross-check artefact worth knowing:** pypdf renders the checklist cell as `指标2：` (no space) on its page 33 while
   the defined `.txt` form prints `指标 2：` — a quote valid in the form can fail against a pypdf-only text. The DEFINED
   form for this capture is the `.txt` (its `.raw` is a PDF, not OLE or zip), so the quotes above are form-exact.
5. **Entry's Unknown "Completeness of the PDF text forms"** can now be narrowed for S118 with this seat's numbers (42
   pages both, 20,390 non-whitespace characters both, identical term counts); the other four documents were not in scope.

## Touched surfaces / out of scope

- Written: this report only. Read-only: the two staged entries, the lane entry, `corpus/SOURCES.md:128` (S118 row: tier B,
  mined 2026-10-26, used-by r48/r50/r42), `corpus/evidence/round56/{claims.md,c2-count.py,spans.tsv,quotes-held.tsv}`,
  `tools/inference-ground.py`, the cache captures.
- Not run (not this seat's measurement): `c1-count.py`, `c2-count.py`, `controls/*`. No gate, battery, probe or fixture
  repo touched; no git/jj mutation anywhere; no network or source fetch; no writes under `/home/vgpnk/Projects/shokuknow`
  or any PATH directory.
- Tooling: `uv run --with pypdf python` (pypdf 6.21.2) in scratch `/fast/scratch/hyaku/chousa-r56/R56GroundQcg`, removed
  at exit; no install or upgrade (pacman paused host-wide; nothing needed). Scratch receipts are inlined above. This seat
  ran no LibreOffice; `pgrep -a soffice.bin` at cleanup showed one live converter under a sibling scratch
  (`R56ExecDeterminism/runs2/…`), which I did not touch.

VERDICT: attacked the lane's held S118 as the answer to both staged entries' Unknown — the document is complete (42/42
pages, 20,390 non-whitespace characters in both extractions) and holds 灰色/灰色文献/未公开发表/内部资料 zero times with no
Ⅰ级 grade, so "it lists 灰色文献 the same way and with the same grade" SURVIVES as FALSE (S118 answers the Unknown
negatively) while the staged Inference "the requirement lives instead in the quality-control guideline" is FALSIFIED, and
the lane entry's 指标 2 quote at char 17840 SURVIVES verbatim.
