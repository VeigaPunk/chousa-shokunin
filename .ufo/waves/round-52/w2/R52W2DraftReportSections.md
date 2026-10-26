# R52W2DraftReportSections — 'Sources & frontier' and 'Trend verdicts' drafted and grounded

seat: scribe (wave 2, falsify). Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin` at tip `d1d972c`
(landed lane commit `e769c037`; base `00f8c7f5`; freeze `37468ead`). Scratch
`/fast/scratch/hyaku/chousa-r52/R52W2DraftReportSections` (removed). No production file written; no
network; no fetch; no tool installed or upgraded (nothing needed); no git/jj mutation outside scratch.

## What I attacked, and the result

| attacked | how | result |
|---|---|---|
| the two counters wave 1 could not pass honestly | replayed both from the lane root | `c1-count.py` → `LEGS=9/9 C1=PASS` (REAL `count=1 locate=(0, 1, 8996) chars=19682`); `c1-supplement.py` → `SUPPLEMENT_LEGS=4/4 C1_SUPPLEMENT=PASS`; `c2-count.py` → `BOUND=4/4 (min 3) REFUSED=0 … QUOTE_ROWS=38 ON_BOUND=38/38 … SUBSTANCE=PASS ANCHOR_BOUND=4/4 INFERENCE_GROUNDED=3/3 QUARANTINE_VERDICTS=1/1 (S120) C2=PASS`, exit 0 |
| the 38-row span manifest | `build-spans.py --check` and the round-51 substance checker | `SPANS_ROWS=38 STALE=0` exit 0; `IDS=4 QUOTES=38 FAILURES=0` exit 0 |
| the four headline quotes in the drafted frontier prose | re-located each in its stated form | `SRにおける文献検索期間について明記する。` → `LOCATED count=1 offset=8996`; S114 `明确说明每一项来源 的 检索或查询日期` count 1 at 1707 of 6,179; S116 `それぞれの情報源が最後に調べられた日付を記載する` count 1 at 592 of 5,328; S113 `2026-04-25 中国循证医学杂志` count 1 at 2034 of 8,804 |
| the "S113 is a second carrier" no-credit judgment | compared both carriers' text | SinoMed `42bac883…txt` (1,675 chars) stops at `并针对中文` + newlines; 梅斯 `453d492b…txt` carries `并针对中文数据库等本土化应用挑战提出实践建议` twice (offset 2477) |
| the round-end census receipt the lesson cites | `ls` + `git ls-files corpus/evidence/round52` | **absent** — `measure-after.txt` is not in the tree (defect D1) |
| the row/tier arithmetic in the drafted census bullet | `grep -cE` + `awk -F'|'` over `corpus/SOURCES.md` | 116 rows; tiers A 100, B 11, C 5; the four new rows are S113 B, S114 A, S115 A, S116 B |
| the round-52 frontier's absence at base | `git grep -l -e 文献検索期間 -e 完全な検索戦略 -e 检索报告清单 00f8c7f5 -- corpus/knowledge` | no output, rc 1 at base; at HEAD the three entries only |
| the NIPH `.txt` sidecar allegation | decoded it | 168,952 chars, 72,117 U+FFFD — not a text form |
| the open-items age in the drafted prose | `open-items-age.py <this report> --round 52` | `OPEN_ITEMS_AGE=PASS since=42 rounds=10`, exit 0 |
| the verdict-gap pick | ran it | `R47 operability: lane=improved verifier=harmed`, `R48 UNPARSED lane_axes=6 verifier_axes=0`, `R50 calibration: lane=improved verifier=unchanged`, `VERDICT_GAPS=2 UNPARSED=1`, exit 1 |
| freshness | mtime sweep of `.qcache` | 6,871 files, newest 2026-10-24 23:26; `find -newermt '2026-10-25 00:00'` → 0 files |

## Findings (all against the L1's landed round-52 artefacts; none changes a frozen predicate)

- **D1 — dangling receipt.** `corpus/lessons/round-52.md:140` states the round-end census as
  "exit 0, `ok`, the same five W04 warnings (`corpus/evidence/round52/measure-after.txt`)"; that file
  exists nowhere (`ls corpus/evidence/round52/`, `git ls-files corpus/evidence/round52 | grep -c after`
  → 0). The drafted bullet reports the re-run I made and names the gap instead of citing the file.
- **D2 — duplicated table header.** `corpus/lessons/round-52.md:57` and `:59` both carry
  `| staged entry | documents (S-ids) | capture on disk (key, size) | province fit | decision | reason | flip |`
  (line 58 is the separator), so the decisions table renders a second header as a data row.
- **D3 — no round-log entry.** `corpus/SOURCES.md`'s round list ends at
  `- Round 51 (2026-10-25): …` (line 299); rounds 41–51 each have one, round 52 has none, and the
  frontier statement that belongs there exists only in the README block.
- **D4 — alias note incomplete.** The lesson's renumber paragraph names only `S133` as the same-URL
  row for the 梅斯医学 record; W1 `R52ExecCollision` §4 names `S133`, `S181` (I confirmed
  `grep -oE 'https://www\.medsci\.cn[^ |]*' SOURCES.append.md | sort | uniq -c` → 3 rows on
  `…/guideline/show_article.do?id=23e481c0052069d3`), plus `S138`, `S137`, `S146`. The lesson's
  sentence is true as far as it goes, not exhaustive.
- **D5 — stage-package staleness (read-only, not the lane's).** `merge/chousa/MERGE-REPORT.md:8` says
  "lane registry currently holds **81** rows"; it held 112 at the freeze. Nothing to fix in the lane.
- **D6 — relative redirects into the lane tree (a wave-2 peer, not this seat).** `git status --porcelain`
  at the lane root lists untracked `forge.out` and `naive.out`, both mtime `2026-10-26 20:24`, contents
  counter leg lines (`NAIVE … REVISIONS=FAIL text differs at 12 (got 79 chars, want 38)`), i.e. another
  seat's replay of `controls/forge-shape.py` and `controls/naive-tool.py` written with relative
  redirects. I did not create, move or delete them; the L1 should remove them before any lane commit.
- Verified positives: both counters and the supplement pass as above; 38/38 quotes inside span, entry
  and lesson; QUALITY 87–90 present (`corpus/QUALITY.md:917,919,921,923`); SKILL Gates rows
  `capture-text` (`:134`) and `chousa round-52 counters and checks` (`:135`) present.

## Draft (intended lane path: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-52/chousa.md`)

```markdown
## Sources & frontier

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`.

- **Round start:** exit 0, `ok`, five pre-existing W04 (S051, S053, S073, S074, S075), 112 rows — `corpus/evidence/round52/census-start.txt`.
- **Round end:** exit 0, `ok`, the same five W04 (re-run for this report at `d1d972c`; the lesson's cited receipt `corpus/evidence/round52/measure-after.txt` is not in the tree).
- **Rows:** 112 → 116 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`). Tiers: A 98 → 100, B 9 → 11, C 5 → 5. Added by tier: A S114 S115; B S113 S116. Rows touched old → new: none.
- **Frontier:** the theme was absent at base (`git grep -l -e 文献検索期間 -e 完全な検索戦略 -e 检索报告清单 00f8c7f5 -- corpus/knowledge` prints nothing, rc 1); the three entries each hold their own term. Credit is per document and is three: the NIPH submission template (`S115`), the archived Japanese PRISMA 2020 table (`S116`) and the 中国全科医学 Chinese checklist page (`S114`). The 梅斯医学 record (`S113`) is a second carrier of the reading the lane holds through the SinoMed row: its text stops at `并针对中文` where the portal's runs on to `提出实践建议`. Left open: searcher identity (none of the four documents makes it a field), the Chinese reading's item text, the publisher's current Japanese page (the cache holds only a failed-fetch marker), and non-OOXML capture forms.
- **Assimilation:** the section-10 search-record theme continued from the read-only `merge/chousa/` package. Collision check: 31 collisions S082–S112 between a 112-row registry and 114 staged ids (S082–S195), the guard proved on a two-space-indented fixture (`.ufo/waves/round-52/assimilation/guard-proof.txt`). Renumber by document S111→S113, S112→S114, S125→S115, S129→S116, the same four the lane adopter printed; staged S126 is lane S112 already (`held`), the same-URL rows S133 and S181, the duplicate S138 and the endpoint rows S137/S146 take no lane id, and the body-only ids S091 S092 S093 S097 S105 S106 were dropped. Three entries admitted on four documents; four staged entries refused with a flip and one deferred (`search-tracking-record-r40`, admit-later). Quarantine slice: one register row on a theme URL (`S120`), verdict `present`, its three quotes re-located in the capture-text form at char 8996, 9020 and 9428.
- **considerthese:** `considerthese/2026-10-26.md` and its seven predecessors swept (38 rows); one proposal implemented — the lane-vs-verifier verdict gap, `python3 corpus/evidence/round52/verdict-gap.py --from 46 --to 51` → `VERDICT_GAPS=2 UNPARSED=1` (R47 operability, R50 calibration), exit 1.
Open operator items: 8d77e6c1 since round 42 (10 rounds)
- **Freshness:** newest readable capture 2026-10-24 23:26 (`.qcache`, 6,871 files), none written since 2026-10-25 00:00, so no capture was taken this round; no fetch (L0 `8d77e6c1`).
- **Mined mistakes:** six in `corpus/lessons/round-52.md` `## Mistakes`; five carry a check shown able to fail (rows 1, 2, 3, 5, 6), row 4 is an incident record whose fix is not counted.
- **Sourced claim:** C2 rests on S113–S116, all opened this round: `python3 corpus/evidence/round52/c2-count.py` → `BOUND=4/4 (min 3) … QUOTE_ROWS=38 … SUBSTANCE=PASS … C2=PASS`, exit 0.

## Trend verdicts

- **expansion — improved narrowly.** Four rows, three newly credited documents, and one claim of the round's own that wave 1 narrowed: the package's four-document expansion was credited at three, `S113` a second carrier (W1 `R52CritTheme`, `R52ScoutCoverage`). The new ground is real but narrow — one public body's submission form that bounds the search's end by procedure, and PRISMA 2020 items 6 and 7 in Japanese and in Chinese that ask a date per source — and it sits on captures written 2026-10-23/24, so the frontier moved by reading, not by fetching.
- **quality — improved.** Wave 1 attacked both counters and the tool; the lane answered each in the artefact that records it: the shape forge (`SUPPLEMENT_LEGS=0/4`) is met by a disclosed supplement that passes the landed tool 4/4 (`E1`); four refusal classes were added for non-Word main parts, inflated parts and unusable members (`E2`); the two readers' divergence on an External relationship and the C2 counter's boilerplate-forgery limit are named, not hidden (`E3`, `E4`); QUALITY 87–90 record the four criteria. Six mistakes are mined, five with a check shown able to fail. Caveats: the frozen C1 counter remains forgeable in shape and its verdict stands as measured; C2 measures binding and presence, not entailment; the lesson's round-end receipt is missing, its decisions table repeats its header, and its same-URL note names one alias row of several.
- **discernment — improved narrowly, with a named limit.** The lane now measures its own grades against the non-author verifier's instead of asserting them: `VERDICT_GAPS=2 UNPARSED=1` at exit 1 over rounds 46–51 (R47 operability and R50 calibration over-graded; R48's verifier file unparseable), and the admission case refused more than it admitted — three entries from eight staged candidates, four refusals each with a flip, one deferral, and no credit for the second carrier. The limit is the check's: it compares one direction word per axis and reads the previous round's verifier file, so it cannot see an entry-level overstatement; the closure's non-author spot-check of two admits (`japanese-search-record-niph-form-r52`, `chinese-prisma-s-reception-r52`) and two rejects (`search-log-fields-r36`, the grey-literature pair) remains the outside test.
```

## Out of scope / not done

- No edit to the lesson, README, SOURCES, SKILL, QUALITY, entries, tool, counters or spans; D1–D5 are
  reported for the L1 to integrate.
- The round-52 `SCORECARD` verdict, `LOG.md` Round 52 entry and the merged `chousa.md` assembly are the
  L1's; the draft above is section text only, lines counted inside the block.
- I did not re-run the controls (`controls/*.txt`), the forge or the mutation fixtures; their claims
  are quoted from the artefacts, not re-derived.

VERDICT: attacked the C1/C2 counters, the 38-quote span manifest and four headline quote offsets, the S113 no-credit judgment, the census receipts, the tier arithmetic, the freshness sweep and the verdict-gap pick — all re-derived as stated, except three lesson/registry defects the draft reports rather than cites: the missing `measure-after.txt` receipt (D1), the duplicated decisions-table header (D2) and the absent Round 52 SOURCES round-log entry (D3); expansion improved narrowly, quality improved, discernment improved narrowly with the verdict-gap check's own limit named.
