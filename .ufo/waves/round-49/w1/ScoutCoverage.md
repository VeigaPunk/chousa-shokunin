# ScoutCoverage — coverage-map ground check for expansion credit

Seat: scout. Lane: chousa. Read-only on every file except this report. As-of 2026-10-25.
Lane HEAD at check `1254ab2` (adoption), freeze `fe740e7`, BASE_REV `414a2ec`. No tool installed
(per `/home/vgpnk/.omp/agent/RULES.md`: pacman transactions paused host-wide; nothing needed).
No network, no campaign tool run, no git fixture created.

## 0. What was adopted

Two lane entries, adopted by document, with registry rows S096–S103 (`corpus/SOURCES.md:106-113`),
coverage-map rows `corpus/README.md:1071-1072`, lesson `corpus/lessons/round-49.md`, evidence row
`:1074`, tool row `:1075`.
`corpus/knowledge/aggregator-vs-source-r36.md:4-7` — S096 CiNii manual, S097 J-STAGE publisher,
S098 J-STAGE FAQ, S099 ERIC/Wineburg; inference bullets `:47-52` (derived subset / matched-item
count), `:53-58` (ingest lag), `:59-64` (resolution ladder), `:65-70` (lateral reading).
`corpus/knowledge/citation-count-semantics-r37.md:4-7` — S100 CNKI 他引频次 note copy, S101 data
spec copy, S102 CNKI KNS8.0 guide, S103 CNKI AI guide; `:15-19` and `:44` (co-author self-citation
rule), `:31-38` (被引 vs 下载 as separate fields).

## 1. Theme element → held ground / frontier item / new ground

| theme element | classification | lane path:line |
|---|---|---|
| index reference lists are derived subsets | **HELD ALREADY** (rule) + new external anchor | `corpus/README.md:52` (`knowledge/contextual-source-admission-r24.md`; ladder text `corpus/knowledge/contextual-source-admission-r24.md:51-57`) — the lane's "primary > secondary > aggregator > unsourced" rule; the theme supplies the first-party statement the rule lacked |
| matched-item counts | **HELD ALREADY** (the count-is-not-the-thing shape) | `corpus/README.md:65` (`knowledge/registry-link-r26.md:11`, "a declaration relation is not semantic citation support"); `corpus/README.md:211-213` ("`refs=N` counts the tokens the extractor sees, not every reference a record carries") — an index's count is a declaration, not a census |
| ingest lag (hop unresolved because the index has not ingested) | **FRONTIER ITEM ADVANCED** | `corpus/README.md:360-363` (Round 3 Frontier: "exemption is record-declared and unverifiable, one hop at a time, no transitivity"); `corpus/README.md:986-987` (Round 32 still open: "URL hops, transitive chains and whether a local copy is the source the hop meant (C2)") |
| resolution ladder by DOI vs text inference | **HELD ALREADY** (partly) + **NEW GROUND** (route axis) | held: `corpus/README.md:51` (`knowledge/citation-chain-fidelity-r24.md:21-27` — five-item per-hop comparison proposition/scope/quantity/hedge/date, no "route" item); `corpus/README.md:10` (`knowledge/chain-resolution-r3.md`, "what anchor existence does not establish"; `corpus/knowledge/chain-resolution-r3.md:131`); new: the bottom rung "reference text parsed into bibliographic data" is an evidential class the lane's checklist does not carry |
| co-author self-citation rule | **NEW GROUND** | no lane row held it: at BASE_REV `corpus/SOURCES.md` had **0** rows matching `CNKI\|知网` and **0** naming any of the nine theme URLs (`git show 414a2ec:corpus/SOURCES.md \| grep -c` → 0, 0); `corpus/lessons/round-47.md:244-249` had already *refused* this staged entry on capture-decoding grounds |
| citation vs download counts | **HELD ALREADY** (access-vs-support split) + external anchor | `corpus/README.md:50` (`knowledge/claim-support-states-r24.md:8-11`, access/relevance/support/truth separately failable); `corpus/README.md:186-189` (known gaps: chain CLEAN "does not prove agreement … or authorship") — the theme calls the download counter an access event with no evidentiary content |
| lateral reading | **NEW GROUND**, distinct from a held row | held neighbour `corpus/SOURCES.md:13` (S003, SIFT — "Find better coverage", cited at `corpus/README.md:51-52`); S099 is the field-tested *leave-the-site* procedure, not held |
| cross-cutting: "an aggregator is never the source" | **HELD ALREADY**; the theme is its first-party anchor | `corpus/knowledge/contextual-source-admission-r24.md:53-55` ("An aggregator that *is* the artifact … can be tier-A-for-scope; a source that is primary elsewhere but off-claim stays tier-C-for-this-scope"); `PROVINCE.md:5-6` (lane owns "source hierarchy (primary / secondary / aggregator / unsourced); citation chaining and hop resolution") |

## 2. Registry ground: eight new rows, no prior row displaced

At BASE_REV `414a2ec`: 0 rows naming nii.ac.jp / jstage / ncpssd / eric.ed.gov / toho-shoten /
um.edu.mo, 0 rows containing a CJK script character, max id `S095`. At HEAD the new rows are
`corpus/SOURCES.md:106-113` (S096 A, S097 A, S098 A, S099 B, S100–S103 B), all `mined`, opened
2026-10-25, `used-by` naming the citing entry (`corpus/lessons/round-49.md:135-161`).
One row is refused, not adopted: the NCPSSD homepage (`corpus/lessons/round-49.md:131`;
`corpus/knowledge/aggregator-vs-source-r36.md:81-84`) — the cited homepage capture carries only the
登录/注册 header, while the access-model sentences live in the help-page capture (`:115-118`).

## 3. Frontier-naming calibration: campaign numbering is not lane-locatable

The staged `ground:` lines read "frontier items 1 and 3" / "wave-1 queue Q2"
(`/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/aggregator-vs-source-r36.md:11`,
`citation-count-semantics-r37.md:11`). Those numbers come from the campaign brief
(`/home/vgpnk/Projects/shokuknow/lanes/chousa/DOMAIN.md:38-50`: 1 claim-vs-source, 2 citation-chain
modes, 3 source-tier adjudication, 4 PRISMA search logs); the lane's own `## Frontier`
(`corpus/README.md:348` onward) is per-round prose with no such numbering. The landed entries
re-ground on lane-local authority instead: `corpus/knowledge/aggregator-vs-source-r36.md:10`
(PROVINCE.md source hierarchy + citation chaining) and
`corpus/knowledge/citation-count-semantics-r37.md:10` (source hierarchy, scoped "as these copies
state"). **That re-grounding is correct and must not be re-anchored to the campaign numbers.**

## 4. Coverage credit: rows landed; the map's own accounting is stale

Rows added: `corpus/README.md:1071` (aggregator-vs-source-r36), `:1072` (citation-count-semantics-
r37), `:1073` (lessons/round-49.md), `:1074` (evidence/round49/), `:1075` (../tools/assimilate-rows.py).
Both entries' `Sources` cells name their bound ids (S096–S099 / S100–S103), so each coverage row binds
to its rows. Three gaps, all **pre-existing, not caused by round 49**:

1. **The map's count paragraph is 22 knowledge notes and 46 lessons behind.** `corpus/README.md:81-87`
   claims "43 entries — 29 knowledge notes and 14 lessons" (dated 2026-10-21). Measured at HEAD:
   `ls corpus/knowledge/*.md | wc -l` → **65**, `ls corpus/lessons/*.md | wc -l` → **60**.
2. **Lesson coverage rows are far from complete.** 26 of 60 lesson files are named by a row; 34 are
   not (the `round-2x`…`round-4x` lessons and their verifier spot-checks). Knowledge coverage is 64
   of 65; the unindexed file is `knowledge/search-log-method-r39.md` (also unindexed at BASE_REV).
3. **No Round 41–49 Frontier prose paragraph exists.** `## Frontier` prose ends at
   `corpus/README.md:1038` (Round 40); rounds 41–48 left table rows only. The theme's frontier
   advance appears **only** in rows `:1071-1072` and in the lesson.

## 5. Calibration defect found: register-id / lane-id collision in the lesson

The `## Gate` verdict lines name ids `S082`, `S084`, `S086`, `S095`, `S096`
(`corpus/lessons/round-49.md:108-123`). Those are **campaign register ids**
(`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:39-46`),
but they now collide with **lane** ids naming different documents: lane `S082` is the AVeriTeC
README (`corpus/SOURCES.md:92`), lane `S095` is the round-47 own-work spot-check
(`corpus/SOURCES.md:105`), and lane `S096` is *the CiNii manual* (`corpus/SOURCES.md:106`) while
the lesson's "register `S096` (data-specification copy)" means the jc.hit copy. Round 48 handled
exactly this (`corpus/lessons/round-48.md:50`: "This is the campaign register id, distinct from lane
own-work S095"); round 49's lesson carries no such disambiguation (`grep -c "distinct"
corpus/lessons/round-49.md` → 0). The frozen counter is immune (`corpus/evidence/round49/c2-count.py:
202-213` matches on URL and its `VERDICT_RE` requires the literal "register" prefix), so C2 is
unaffected — but a human reader can misread five verdicts. One-line labelling repair.

## 6. Independent checks I ran (read-only)

- **Spans are exact slices under the counter's own rule.** Re-derived
  `corpus/evidence/round49/spans.tsv` (28 rows) against the capture text form chosen exactly as
  `corpus/evidence/round49/c2-count.py:102-110` does (`.txt` via `read_text` universal newlines;
  `.raw` decoded UTF-16LE): **28/28** rows satisfy `form[offset:offset+len(span)] == span`, contain
  their quote, and are longer than it. (An earlier 18/28 was my own bug: I decoded `.txt` bytes
  without newline translation.)
- **The two OLE `.doc` captures hold the quoted sentences only under UTF-16LE.** `zcmu` raw: 400,543
  chars, 11,154 U+FFFD; UTF-16LE hits 自引×2, 任一合作者×1, 他引频次×7, 中国引文数据库×3. `jc.hit`
  raw: 64,512 chars, 263 U+FFFD; UTF-16LE hits 文献标志码×14, 主要责任者×17, GB/T 7714×4, ISO 690×3.
  The `.txt` sidecars decode as UTF-8 with 308,430 / 14,486 U+FFFD and **0** hits for every one of
  those strings — exactly the flip round 47 asked for (`corpus/lessons/round-47.md:244-249`).
- **Register rows on theme URLs: 5** (`absent-defect-register.md:39-46`); the lesson carries exactly 5
  verdict lines (`:108`, `:112`, `:115`, `:119`, `:121`), none `fabricated` or `unverifiable`.

## 7. Limits

Did not run `c1-count.py` / `c2-count.py` (the falsifier seats' leg). Opened no URL. Read no
`corpus/SCORECARD.md` beyond the criterion-64 tag definition. Did not compare against the staged
package's other 56 entries. The §5 repair is a proposal to the lesson's author, not a change I made.
Frontier item numbering is the campaign's; the lane's prose rows are authoritative. No scratch
directory was created, so none needed deleting.

VERDICT: I attacked the coverage-map credit for the round-49 derived-index theme by mapping its
seven elements against `corpus/README.md` rows and `## Frontier` — five elements are HELD-ALREADY
(tier ladder, count-is-not-the-thing, access-vs-support, chain-existence limits, the SIFT
neighbour), two are NEW GROUND (co-author self-citation, lateral reading), ingest lag and the
resolution route ADVANCE the still-open chain/transitivity rows at `:986-987`, all eight registry
rows are net-new with one refused row, the campaign's frontier numbering was correctly re-grounded
to lane-local authority, and one calibration defect remains (five register ids in the lesson collide
with lane ids of different documents) — VERDICT: coverage credit is substantiated; the map's count
paragraph is stale and the lesson needs one disambiguation line.
