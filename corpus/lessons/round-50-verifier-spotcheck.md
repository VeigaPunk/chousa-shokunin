# chousa round 50 — verifier spot-check

author: hyaku closure (non-author integrator, @m_sonnet)
date: 2026-10-25
lane tip measured: `1d7aba0948cf62f6158f77e220f64320a5b6c6cc` (before: `3c51da77b3696ed884c943548ec4b4006e3ca528`)
inputs: fleet report `.ufo/reports/round-50/chousa.md`; prompt `.ufo/prompts/chousa-round-50.md`
driver lines (`.ufo/watchdog.log`): `2026-10-25T17:45:09-03:00 launch chousa round=50 pgid=2124778 driver=hyaku-inline attempt=1` · `2026-10-25T19:39:20-03:00 complete chousa round=50; hyaku-inline attempt=1`

All measurements below were run by the closure over committed bytes (a `git archive` export of the tip under `/tmp`, the lane's on-disk captures read-only). No lane gate was executed; counters (`c1-count.py`, `c2-count.py`, `c1-supplement.py`) are verified as committed evidence only.

## 1. Step-1 conformance

| check | command | observed |
|---|---|---|
| report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-50/chousa.md` (fleet repo) | `chousa-shokunin 9bcf5dcb236ffe972b3386d5f0afa54619467682` (committed 19:38:29, after the lane tip at 19:37:21) — ok |
| SHONEN heading, one line per box | `grep -n SHONEN` on the report; `SHONEN.md` has 4 boxes | `## SHONEN` once; 4 lines, all `[~]` with pointers — ok |
| every cited lane commit exists and is an ancestor of the branch | `git merge-base --is-ancestor <h> master` for `6a068f2 ec52e63 7754172 2573dc1 74794db c5b8dca 1d7aba0 4d13657` | all eight `anc ok` |
| pushed, no leftovers | `jj-lane.sh state` → `local=1d7aba09… remote=1d7aba09… ahead=0 behind=0 tracked=0 untracked=0`; `git status --porcelain` → 0 lines; `ls-remote origin refs/heads/master` → `1d7aba09…` | ok |
| prompt carries template contract | grep of `.ufo/prompts/chousa-round-50.md` (545 lines): §1 MISSION/AXES binding, §2 claims 1–3, §3 L2 floor, §4 report contract incl. SHONEN and marker rule, §5 commit/push scope/L0, §6 hyaku addendum | ok |
| append-only files | `git diff 3c51da77 1d7aba09 --stat -- LOG.md corpus/QUALITY.md corpus/README.md` → 122 insertions, 0 deletions; 8 stale-count `correction:` lines present | ok |
| report before WAVE-DONE | report states filed after both waves; `w1/` 30 files, `w2/` 44 files on disk | ok |

Defects (status-neutral): (a) 13 of 42 wave-1 seats reused round-49 seat names and returned round-49 reports (lane's own Mistakes row; `name-collision-check.py` added and `QUALITY 78`); live seats 29 + 43 = 72 ≥ 64 — the 64 floor still holds. (b) The report's pre-round commit `4d13657` (round-49 late seat reports) is dated 17:43:45, before the 17:45:09 launch — inherited work, disclosed. (c) The `SKILL.md` gate row for the round-50 counters names the C1 measured revision as candidate `ec52e632`; the later hardening (`2573dc16`) and the tip are covered only by `measure-after.txt`, whose header says "working tree before the final commit" and names no hash — the Gate standard asks a verdict to name its revision. The closure re-ran the tool self-test at the tip (below), so the claim is not affected, but the lane should pin the revision next round.

## 2. Per-claim re-check

### R50-C1 operability — `tools/assimilate-rows.py --selftest` (re-measured, not gate-executed)

| leg | command | observed |
|---|---|---|
| before: base tool has no self-test | `git show 3c51da77:tools/assimilate-rows.py > base-tool.py; python3 base-tool.py --selftest` | usage error, `rc=2` (required args missing) — matches the report's `BASELINE=FAIL rc=2` |
| after: default self-test at tip | `python3 tools/assimilate-rows.py --selftest` in the exported tip | `FIXTURES_SHA256=c5c56480e9f6a08d6a2077b6a11267a4cabf0bc0d3f726408a9bb0238283cd43`, `SELFTEST=PASS findings=26 expected=26`, `rc=0` — digest equals the digest in the SKILL.md registry row and `c1-count.py` pin |
| my own perturbation A: drop one line of `expected.json` | edit a copy of `corpus/fixtures/assimilate-selftest` | `DIFF unexpected MAP S011->S014 append`, `SELFTEST=FAIL findings=26 expected=25`, `rc=1` |
| my own perturbation B: delete the held registry row `S001` from a fixture copy | `sed -i '/^| S001 /d' …/registry.md` | 20 `DIFF missing/unexpected` lines (MAP, ENTRYCITES, ROWUSEDBY…), `SELFTEST=FAIL findings=30 expected=26`, `rc=1` |
| frozen predicate unchanged after freeze | `git diff 6a068f2a 1d7aba09 --stat -- c1-count.py c2-count.py claims.md controls c1-fixtures` | only `controls/build-c2-controls.py` (edited, disclosed as erratum item 5), plus new `controls/forge-tool.py` and `c2-controls-at-landing.txt` |
| committed gate evidence | `corpus/evidence/round50/measure-after.txt`; `controls/c1-before.txt`; `c1-supplement-receipt.txt`; SKILL.md registry rows `assimilate-rows` (r50 `--selftest`) and `chousa round-50 counters and checks` | `LEGS=5/5 PERTURB_PASS=6/6 C1=PASS`; controls base `2/5`, echo `4/5`, constant `2/5`; supplement real `5/5`, forge `1/5`, echo `2/5`, constant `0/5`, base `1/5`; registry row present with verdict map, pinned-value path, self-test spelling, scope, owner |

Re-measured: base `rc=2` vs tip `PASS rc=0` plus two independent perturbations (exit 1). Evidence-verified only: the six-perturbation tally, the do-nothing controls and the supplement. The lane's own disclosure that the frozen counter is replayable (a 42-line forge passes `LEGS=5/5`) is accurate to what the receipts show and is the reason the verdict is stated as improved on the tool, not on the frozen counter alone. **Verdict: improved** (the tool detects perturbation for the cases I tried; the counter's replay weakness is named and covered by the post-freeze supplement).

### R50-C2 depth — Chinese citation-checking theme adopted by document

| measurement | command | before (`3c51da77`) | after (`1d7aba09`) |
|---|---|---|---|
| registry rows | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 103 | 106 (S104–S106) |
| entries on 引文核对 / 引证检索 | `git grep -l -e 引文核对 -e 引证检索 <rev> -- corpus/knowledge` | none (rc 1) | the three entries `cnki-citation-check-r40.md`, `citation-matching-semantics-r41.md`, `istic-citation-verification-r39.md` |
| quote manifest | `awk` over `spans.tsv`; own script: for each of 67 rows, locate `quote` in the sha256-matched capture `.txt`, in the citing entry, `len(split)≤25`, `len≤160` | n/a | 67/67 pass, 0 bad (the lane's `CAPTURE_BOUND=67/67`, reproduced independently) |
| prior-round stale count | `git show 1d7aba09:corpus/evidence/round49/spans.tsv \| awk 'NR>1 && NF' \| wc -l` | prose said 28 | 31, with four append-only `correction:` lines |
| census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` | exit 0 `ok` | exit 0 `ok`, the same five W04 warnings (S051, S053, S073, S074, S075), none from S104–S106 |

Re-measured: row counts, coverage-before absence, all 67 quote locations, census. Evidence-verified: `c2-count.py` tally (`BOUND=3/4 REFUSED=1 … C2=PASS`), controls (`c2-before.txt`, `c2-controls-at-landing.txt`), `inference-ground` regression files. The lane states that the counter measures binding and presence, not entailment; entailment is what the spot-check below samples. **Verdict: improved.**

## 3. Axis verdicts

| axis | verdict | basis |
|---|---|---|
| operability | improved | C1, re-measured above; caveat on the frozen counter named |
| depth | improved | C2, re-measured above; spot-check agrees with admits and rejects (below) |
| coverage | improved | `git grep` at base finds no 引文核对/引证检索 in `corpus/knowledge`; three entries + three registry rows now |
| calibration | unchanged | the lane's stale-count correction is real (31, `correction:` lines, append-only verified) and its own limits are disclosed, but no calibration claim was declared and the registry row's revision gap (defect c) keeps it from a verdict beyond unchanged |
| freshness | unchanged | no freshness claim; captures dated 2026-10-23 |
| adjacency | unchanged | no sibling overlap observed (SCORECARD diff touches only the lane's own rows) |

`git diff 3c51da77 1d7aba09 -- SCORECARD.md` appends the round-50 verdict, a capabilities row and the round-51 plan; no existing score or row changed, and the report's `improved narrowly` grades on operability/calibration/coverage are compatible with the above (calibration is graded down to unchanged for the reason given). No axis is harmed.

## 4. Discernment spot-check (`corpus/lessons/round-50.md` `## Gate`)

| item | decision | re-opened source | agree / disagree | reason |
|---|---|---|---|---|
| `cnki-citation-check-r40.md` (S105) | admit, narrowed | `…/.qcache/e3ca8f4fdd15420b80096a75.txt` (UTF-8, 38,174 chars): `第二类是橙色的标识` at char 31063 ×1; `引文核对是指，以“中国知网”的文献资源为核对源内容` at 30738 ×1; `态共分为三种类型` at 30935; sweep `[匹配 算法 字段 标识符 未收录 诚信档案]` → `[0,0,0,0,0,0]`; the PDF `.raw` (sha256 prefix `d36191c7`, 57 pages) | agree | every re-located quote sits at the stated offset exactly once; the narrowing (橙色 not amber; the 诚信档案 attribution dropped; "match mechanism is not stated") is what the text supports |
| the S105 hover screenshots (r41 Observation bullet 4; the lane's request) | admit, narrowed (image-borne, not a located quote) | `pdftoppm -f 43 -l 43 -r 90` of the capture `.raw`: the page's printed folio is 38; the orange-marker tooltip reads `篇名相同,作者相同,刊名不同`, the green one `篇名相同,作者相同,刊名相同` | agree | the three compared parts (title, author, journal) and the absence of year/volume/page parts are visible on the rendered page; the text form cannot carry them; the entry correctly says so |
| CNKI 教师 manual (refused; the lane's request) | reject | `…/.qcache/275c79d45b1e9b0fd32cef93.txt` (9,914 chars): `引文核对` 0, `核对` 0, `匹配` 0, `引文` 9, `标明引文` 9; the located sentence `教师可查看的报告单包括简洁报告单、全文（标明引文）报告单、去除本人` at char 8033 ×1 | agree | all nine `引文` occurrences are inside the report-sheet name 标明引文, so the document adds no citation-checking content; the flip rule (a claim carriable only by it) cannot fire on current entries |
| `istic-citation-verification-r39.md` / S104 reuse-scope narrowing (the lane's request) | admit, narrowed | `…/.qcache/001287c436f0e6b1d166ae8d.txt` (2,288 chars): `按合作者排除自引标准统计他引次数` at char 549 ×1; `2.针对中国科学院用户：` at 684; repeat-commission `可免去相同数据的费用` sentence at 735 and `，但要收取本次检索的开库费、复核费和证明费` at 788; `将一周之内的网络检索结果打印后到我中心进行复核` at 849; `中国科学院文献情报中心` ×3, `ISTIC` ×0, `中国科学技术信息研究所` ×0 | agree | the concession sits under the 中国科学院 users heading (char 684), so scoping it to those users is right; the lane filename keeps the inherited `istic` while the entry says the capture names neither ISTIC nor 中国科学技术信息研究所 — an honest disclosure |
| `cnki-comparison-basis-r46.md` (refused) | reject | the 28,114-character capture the lane cites, `…/.qcache/9c3aca545490cdfad8428e40.txt` (found by `len(t)==28114` over the cache; HTML, begins `<!DOCTYPE html>`): `t.count('比对')` = 25; S105 capture for §6.1 as above (which staged row it belongs to was not traced) | agree | the staged tally (13,527 characters, 比对 ten times) does not reproduce on a capture of the lane's stated size (28,114 / 25), as the lane's Gate row says; the closing inference contradicts §6.1, which defines the check against 中国知网's resources |
| S104 row (newly written) | admit, tier A | the row, then the capture above | agree | cell 5 names only what the page states; the six offsets in cell 6 (char 194, 380, 549, 735, 849, 1380) re-locate in the `.txt` (549, 735, 849 checked by hand; 194, 380 and 1380 in the 67-row pass); tier A is right for an institute describing its own service |
| S105 row (newly written) | admit, tier B | S105 capture | agree | cell 6 lists `char 48, 30745, 30800, 27587, 31063, 31101, 31137, 31233`; I located all eight at those offsets, each once; `27587` sits under `3.7 仅去除第一作者本人文献`, matching cell 5's `§3.7`; tier B (vendor content on a university host) is argued and consistent |
| S106 row (newly written) | admit, tier B | `…/.qcache/28750bcdf5d36cd90a7709fb.txt`: title block at char 83; `在创建文件夹页面中第一个选项为“仅去除第一作者本人文献”` at 22511 ×1; `该文件夹下的所有检测文献在去除本人文献检测结果中` at 22549; `引文核对` 0 | agree | the row claims only the option and the absence of 引文核对 "in this copy" |

Quote-length check of the newly written rows: the SOURCES rows store offsets rather than quotes; the ≤25-word rule applies to the lesson quotes, and all 67 manifest quotes pass `≤25` whitespace words and `≤160` characters (the long CJK quotes are one whitespace token each; the 160-character cap is what bounds them). `sources-census.sh validate` → `ok`, exit 0, five pre-existing W04.

Agreement on all eight sampled decisions, admits and rejects. Nothing is left unlearned from this sample.

## 5. Trend verdicts

- **expansion: improved** — `git grep` at base finds nothing on 引文核对/引证检索; three documents (S104–S106) with three entries now hold the ground. The lane's caveat stands: r40 and r41 share one PDF, so the count is per document (three), and the verdict is on new documents, not a net entry count.
- **quality: improved** — the three entries were narrowed after attack (the 橙色/amber correction, the "undocumented" vs "not an algorithm" narrowing, the reuse concession scoped to 中国科学院 users), the closure's re-checks all hold, the stale 28→31 counts are corrected by append-only lines, and the lane reports its own counter weaknesses (replayable C1 counter, unreachable CJK polarity rule, binding-not-entailment C2) instead of hiding them. No admitted entry failed its re-check here.
- **discernment: improved** — the outside sample agrees with the gate on admits and rejects (8/8). The lane added QUALITY 73–80; `git show 1d7aba09:corpus/QUALITY.md` lines 751–850 cite `corpus/lessons/round-50.md` (e.g. criteria 73 and 74 name its `## Mistakes` rows 1 and 2), and I did not individually check that each of 73–80 maps to a Mistakes row. No disagreement to learn from.

## 6. Routed defects for next round

1. Pin the revision the C1/C2 counters were measured against in `measure-after.txt` (hash in the header) and in the `SKILL.md` registry row; the row currently names candidate `ec52e632`, not the tip.
2. Replace the frozen C1 counter's literal-DIFF search with the nonce/exclusive-set form the lane's own supplement already implements, as the lane routed; until then C1 rests on two counters.
3. Reserve seat names uniquely per round before dispatch (QUALITY 78 already requires it); 13 of 42 W1 seats were lost to resumed round-49 agents.
4. Record the lane filename drift (`istic-…` for a 中国科学院文献情报中心 page) in `corpus/README.md`'s coverage row, not only in the entry.
5. SHONEN: all four boxes are `[~]` with lane-authored evidence; operator promotion review is the next step, not a closure action. A non-author can check the tooling and decision-table boxes (the self-test and the Gate table above) but the closure does not write `[x]`.
