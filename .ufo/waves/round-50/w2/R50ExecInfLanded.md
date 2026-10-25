# R50ExecInfLanded — `inference-ground` probe of the three landed C2 entries

Seat: R50ExecInfLanded, chousa round 50 wave 2 (falsify). Lane commit `74794db`, claims frozen at `6a068f2`.
**Attacks** the C2 leg *"all three entries exit 0 under `tools/inference-ground.py`"*: whether exit 0 on
`corpus/knowledge/{cnki-citation-check-r40,citation-matching-semantics-r41,istic-citation-verification-r39}.md`
means what the tool's own rule 5 promises. Lane writes: none (this report only). No install/upgrade: none needed.

## 1. Pristine run, lane bytes and lane tool

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && for e in corpus/knowledge/cnki-citation-check-r40.md \
  corpus/knowledge/citation-matching-semantics-r41.md corpus/knowledge/istic-citation-verification-r39.md; do
  python3 tools/inference-ground.py --entry "$PWD/$e" --spans "$PWD/corpus/evidence/round50/spans.tsv" \
  --counts /dev/null --registry "$PWD/corpus/SOURCES.md" --root "$PWD"; echo rc=$?; done
GROUND entry=corpus/knowledge/cnki-citation-check-r40.md section=1 bullets=5 tokens=10 grounded=10
GROUND: PASS                                    rc=0
GROUND entry=corpus/knowledge/citation-matching-semantics-r41.md section=1 bullets=4 tokens=7 grounded=7
GROUND: PASS                                    rc=0
GROUND entry=corpus/knowledge/istic-citation-verification-r39.md section=1 bullets=4 tokens=13 grounded=13
GROUND: PASS                                    rc=0
```
No `FINDING` line in any of the three runs. The same three GROUND lines reproduce byte-identically from the
scratch root (`--root` scratch, copies of entries + `spans.tsv` + `spans/` + `SOURCES.md` + the tool).

## 2. What those 30 tokens are (dumped through the tool's own functions)

| entry | bullets | tokens | CJK quote tokens | numeral tokens |
|---|---|---|---|---|
| r40 | 5 | 10 | 5 | 5 × `2020` (one occurrence, offset 53) |
| r41 | 4 | 7 | 7 | 0 |
| r39 | 4 | 13 | 8 | 5 (`300`×3, `200`×2) |

**All 20 quote tokens in the three entries are CJK; there is no Latin quote token anywhere.** Rule 5's
polarity machinery (`tools/inference-ground.py:325-365`) therefore runs on zero quote tokens here, because
`words()` is `[a-z]`-only (`:253-257`), `content(inner)` is empty for a CJK phrase, and `polarity_flips`
returns `[]` at `:340 if not stems: return []`. The tool declares this (`:95-96`); §4 shows it is reachable.

## 3. Fifteen edits, five per entry, on scratch copies (lane untouched)

Each edit is one exact string replacement, asserted to occur exactly once in the landed file; mutated copies
written to `corpus/knowledge/<entry>.mutN.md` under the scratch root and run with `--root` scratch.

| # | edit (old → new, abbreviated) | rc | findings | refused? |
|---|---|---|---|---|
| r40 E1 | delete the id token S105 from Inference b1 | 1 | `INF_UNCITED` b1; `INF_TOKEN_NOT_IN_SPAN` b1 ×2 (`但是引文中有某一部分的信息与源内容不同`, `2020`) | **refused** |
| r40 E2 | b1 quote → `引文核对并不比对任何文献资源` (absent from every S105 span) | 1 | `INF_TOKEN_NOT_IN_SPAN` b1 | **refused** |
| r40 E3 | b2 `第一类是“没找到”` → `表示系统经过核对已经找到了该条引文记录` (in span, char 31079) | 0 | — | **passes** |
| r40 E4 | b4 quote → `按合作者排除自引标准统计他引次数` (S104 capture, char 549; b4 cites S105) | 1 | `INF_TOKEN_NOT_IN_SPAN` b4 | **refused** |
| r40 E5 | b3 loses its only quote (`列表中的“篇名”…`) | 0 | — (residual token `2020`) | **passes** |
| r41 E1 | `S105 gives` → `The copy gives` (drops b1's only S-id) | 1 | `INF_UNCITED` b1; `INF_TOKEN_NOT_IN_SPAN` b1 ×3 | **refused** |
| r41 E2 | b1 `各项内容都相同` (char 31218) → `各项内容完全不同` | 1 | `INF_TOKEN_NOT_IN_SPAN` b1 | **refused** |
| r41 E3 | b1 "finds every item equal (`各项内容都相同`)" → same slot quoted as `但是引文中有某一部分的信息与源内容不同` (char 31101) | 0 | — | **passes** |
| r41 E4 | b4 S106 quote → `论文收录引用检索（简称引证检索）指通过检索SCI、SSCI、EI、ESI、CSCD等国内外评价类数据库` (S104 capture) | 1 | `INF_TOKEN_NOT_IN_SPAN` b4 | **refused** |
| r41 E5 | b2 loses its only quote (`以核对引文内容的正确性`) | 1 | `INF_UNGROUNDED` b2 | **refused** |
| r39 E1 | delete the id token S104 from Inference b3 | 1 | `INF_UNCITED` b3; `INF_TOKEN_NOT_IN_SPAN` b3 ×3 | **refused** |
| r39 E2 | b1 `所有文章必须包括全部作者（全拼）…完整信息` (char 1380) → `所有文章必须包括全部作者、标题和摘要` | 1 | `INF_TOKEN_NOT_IN_SPAN` b1 | **refused** |
| r39 E3 | b2 quote `按合作者排除自引标准统计他引次数， 1 元/篇次` → `所有文章必须包括全部作者（全拼）、标题、期刊、年、卷、页码、DOI等完整信息` (char 1380) | 0 | — | **passes** |
| r39 E4 | b3 quote → `系统会将搜索到的有关引用文献的详细情况以列表形式展示在下方` (S105 capture, char 30844) | 1 | `INF_TOKEN_NOT_IN_SPAN` b3 | **refused** |
| r39 E5 | b2 loses its only quote (`按合作者排除自引标准统计他引次数， 1 元/篇次`) | 0 | — (residual token `300`) | **passes** |

**10 of 15 refused, 5 pass.** The refusals are the ones the rules name: missing id (`INF_UNCITED`), phrase
absent from the cited spans, and phrase present only in a *different* capture (S104↔S105↔S106 are cleanly
separated by `span_texts`, `:186-227`). The five passes are the two classes in §4 and §5.

## 4. Named limit — the CJK polarity path is untested by these entries (all three flips pass)

Every E3 above replaces a quoted phrase with a phrase **inside the same span** that supports the **opposite**
claim, and the tool exits 0: r40 b2 now reads "The first state is `表示系统经过核对已经找到了该条引文记录`"
(the span says the record *was found*) while the bullet calls that state nothing-matched; r41 b1 now supports
"finds every item equal" with `但是引文中有某一部分的信息与源内容不同` (char 31101, a *difference* phrase);
r39 b2 asserts "the page never says how a reference is resolved" while quoting the page's complete-metadata
requirement (char 1380) — an absence claim now carrying presence evidence. r39 E3 also shows the tool does not
check a bullet's own `char N` against its quote: the quote sits at 1380, the bullet still says `char 549`.

Control that isolates the cause (same flip, Latin): scratch entry quoting `the record was not found in the
index` while asserting the record was found —
`GROUND entry=ctl/entry.md section=1 bullets=1 tokens=1 grounded=1`
`FINDING INF_POLARITY_FLIP bullet=1 token='the record was not found in the index / found'` rc=1.
So rule 5 works and is simply unreachable for CJK quotes. For these three entries the C2 leg's exit 0 is a
**presence** result only, exactly as `claims.md` says of the counter ("measures binding and presence, not
entailment") — but note the entry-level gate inherits the same hole, and 20/20 of its quote tokens are CJK.

## 5. Numeral leg — quote removal is masked, and r40 b5 is grounded by a year alone

r40 E5 and r39 E5 pass because rule 3 accepts *any* numeral ≥3 digits: r40 b3 keeps `2020` (the edition line
`更新时间：2020 年 7 月`, char 48), r39 b2 keeps `300`. r41 E5 is refused only because r41 carries no numeral.
Sharper: **r40 Inference b5 has no quote token at all** — its only token is that same year. Probe (sixth edit,
labelled, not one of the five): `the 2020 copy keeps access and relevance` → `the copy keeps access and
relevance` gives `FINDING INF_UNGROUNDED bullet=5` rc=1, tokens 10→9. So a bullet about the lane's
four-observation frame is "grounded" by an incidental numeral from the capture's title block; the numeral leg
is position-blind and claim-blind. Not a rule violation, a calibration defect the Gate should see.

## 6. Cross-check of the span rows this probe leaned on

`spans.tsv` `offset` is the span *block* start, not the quote position (`tools/inference-ground.py:196`
unpacks it as `_off` and never reads it, so §1-§5 are unaffected either way). Verified per capture:
`python3 -` over all 55 rows, `capture[off:off+len(span)] == span` and `quote in span` → `rows 55 mismatches []`,
quote index histogram `{80: 53, 48: 2}` (the two clamped head rows are S105-1/S105-14, edition line char 48).
This independently confirms `R50ReopenRowS105`'s retraction of the "−80 drift" flag; no defect.
Sections the tool never parses: it reads only `#### Inference` (`:115-152`), so r40's 7 and r41's Observation
bullets (42/40 backticks) are outside this leg; `--counts /dev/null` leaves the counts/figure leg inert.

## 7. Cleanup

`rm -rf /dev/shm/chousa-r50-R50ExecInfLanded` → `ls: cannot access …: No such file or directory`, count 0.
No file outside `.ufo/waves/round-50/w2/` was written by this seat.

VERDICT: attacked the three landed C2 entries with 15 refusable edits plus a Latin polarity control — 10/15 refused as designed and the entries survived those legs, but defect found at the declared CJK-polarity limit (a real polarity flip passes in **all three** entries, rc=0) and in r40 Inference bullet 5, whose only grounding token is the edition year `2020` with no span quote at all.
