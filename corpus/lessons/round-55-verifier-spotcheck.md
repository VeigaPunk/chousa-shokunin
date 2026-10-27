# Round 55 verifier spot-check — chousa

author: hyaku closure (non-author integrator, @m_opus)
date: 2026-10-27
scope: chousa round 55; BASE `dba605deb5cd5ed4874e0e3c39ba24737409cd80` → TIP `53f1ce6b8a479c05c27436026557f05658929313` (== `master` == `origin/master`, ahead=0); FREEZE `1fc5d92b5a7866ec16f1cac2de749fccfa6b49cb`; C1 candidate `6ca924995d48facbf704d2aa22ddaec236059039`; report `.ufo/reports/round-55/chousa.md` (fleet `ac629889ff513215a5998d0d6f6c1d0421943290`).
Non-author: the hyaku closure judge wrote this file, not the lane. No lane gate or frozen counter (`corpus/evidence/round55/c{1,2,3}-count.py`) was executed (PROTOCOL §Gate standard, Closure consequence); their verdicts were verified through committed receipts. Plain counts, the landed builder's behaviour (a registered `probe`, not a gate) and eight of the eleven C3 observations were re-measured by the judge over committed bytes and the read-only capture cache `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache` (no fetch; builder output written only to a `/tmp` scratch dir, removed after).

Driver digest (copied from the mutable `.ufo/watchdog.log`):

    2026-10-27T00:23:04-03:00 launch chousa round=55 pgid=1294370 driver=hyaku-inline attempt=1
    2026-10-27T01:12:25-03:00 complete chousa round=55; hyaku-inline attempt=1

## 1. Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report committed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-55/chousa.md` | `chousa-shokunin ac629889…` 01:11:40 -0300, after lane tip `53f1ce6b` (01:11:04) | pass |
| `SHONEN` heading, one line per box | read report §SHONEN | 4 lines, all `[~]` (craft rows, logged rounds, runnable checks, province fit) | pass |
| cited lane hashes exist and are ancestors of `master` | `git rev-parse --verify` + `git merge-base --is-ancestor <h> master` for `dba605de 1fc5d92b 6ca92499 d5018747 5a35ebd6 29cfb12a 53f1ce6b` | all 7 resolve, all exit 0 | pass |
| non-lane hash `8d77e6c1` (L0 question) | `git -C <fleet> cat-file -t 8d77e6c1` | fleet commit `8d77e6c15a6b…` "round-29: chousa L0 question" — a fleet pointer, not a lane hash | pass |
| lane pushed, nothing uncommitted | `jj-lane.sh state …` ; `git status --porcelain` | `branch=master local=remote=53f1ce6b… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; `ls-remote` → `53f1ce6b…` | pass |
| prompt carries the template contract | every non-blank line of `templates/round-prompt.md` (placeholders `{{LANE}} {{ROUND}} {{FLEET_ROOT}}` substituted) searched verbatim in `.ufo/prompts/chousa-round-55.md` | 139/140 verbatim; line 1 rendered with `<chousa-repo>` resolved to the absolute lane path; hyaku addendum §6 and §7 present | pass |
| frozen counters unchanged FREEZE..TIP | `git diff --stat 1fc5d92b 53f1ce6b -- claims.md c1/c2/c3-count.py controls/` | empty | pass |
| candidate unchanged after candidate commit | `git diff --stat 6ca92499 53f1ce6b -- tools/build-spans.py tools/capture-text.py`; `sha256sum` | empty; `1ed2650a…` and `2c0140bc…` = receipts | pass |
| registry rows | `grep -n 'build-spans\|round-55' SKILL.md` | `SKILL.md:142` (`build-spans`, probe), `:143` (round-55 counters, gate) | pass |

Conformance defects (status-neutral; named, not barring admission):

- **D1 — report filed before its waves settled (repeat of the round-54 class).** W1 (48 seats) had 35 committed reports at filing; `corpus/evidence/round55/wave-settled-r55.txt` → `UNSETTLED w1 no committed w1-results.json`, exit 1; no `w1-results.json` at TIP. Several W1 seats were still live at this closure. W2 (36 falsify items, `.ufo/waves/round-55/w2-spec.json`) was never dispatched. The lane disclosed it (lesson Mistakes row 4; QUALITY 104 ran red).
- **D2 — round total 48 seats < the 64-seat L2 floor** (disclosed in the report).
- **D3 — measurement-revision mismatch.** The report says C2/C3 were "measured at `29cfb12a`", but the committed receipts' headers say `at lane master 5a35ebd6…` (`c2-measure-after.txt:1`, `c3-measure-after.txt:1`); the report's "re-run at `53f1ce6b` `C2=PASS`" has no committed receipt naming that revision. `29cfb12a` touches none of C2/C3's inputs (r37 entry, `recurring.tsv`), so the verdicts stand; the citation is wrong.
- **D4 — quarantine-verdict offset imprecision.** Lesson `## Gate` quarantine line says the document prints `即“灰色文献”` "(char 994)"; in the defined OLE form 994 is the start of the containing sentence `查找时应当注意收集…`, and `即“灰色文献”` itself is at char 1012 (count 1). The verdict (`absent-as-written`) is right.

## 2. Claim re-checks

### R55-C1 — operability (capability: OLE-aware span builder `tools/build-spans.py`) — improved (re-measured + evidence-verified)

Evidence-verified (gate, not executed): `controls/c1-before.txt` `LEGS=0/4 C1=FAIL` ×4 (tool absent); controls R54SHIM 1/4, TXTONLY 1/4, DELEGATE 0/4 (`controls/c1-controls.txt`); after `LEGS=4/4 C1=PASS exit=0` on `--seed 7` + three unseeded runs, tool sha256 `1ed2650a…` (`c1-measure-after.txt`, measured at `6ca92499`); 40/40 seeds `--per-leg 4` (`c1-seed-sweep-L1.txt`).

Re-measured by the judge (plain runs of the landed probe, never the counter):

- base absence: `git cat-file -e dba605de:tools/build-spans.py` → `fatal … not in 'dba605de'`, exit 128.
- round-55 manifest reproduced: `python3 tools/build-spans.py --quotes corpus/evidence/round55/quotes.tsv --out /tmp/…/r55` → `SPANS_ROWS=19 WRITTEN=19`, exit 0; `diff` vs committed `spans.tsv` and `spans/` → identical (19 span files); `--check` in place → `SPANS_ROWS=19 STALE=0`, exit 0 (writes nothing; lane tree still clean).
- REGRESS leg by hand: round-54 `quotes.tsv` exported from `dba605de`, builder run → `SPANS_ROWS=33 WRITTEN=33`; `spans.tsv` identical to `dba605de:corpus/evidence/round54/spans.tsv`; 33/33 span files `cmp`-identical.
- refusals on a scratch cache: a `.raw` that is neither OLE nor zip, no `.txt`, quote present in its UTF-16LE decode → `build-spans: refused S901: no defined text form …`, exit 1, no `spans.tsv`; a run with one quote absent from a `.txt` form plus one present → `refused S902: quote occurs 0x …`, exit 1, no `spans.tsv` (all-or-nothing); the present row alone → exit 0, `QUOTE S903 char 11`.
- delegation: `grep -nE 'subprocess|ctypes|os\.system|popen|socket|import ' tools/build-spans.py` → stdlib imports only (`argparse hashlib importlib.util pathlib re sys`); `capture-text.py` is imported, not spawned.

W1 attack record (committed, `.ufo/waves/round-55/w1/`): `R55CritForgeReader` approximate OLE reader 0/4; `R55CritForgeEcho` refusal-only forge 1/4; `R55CritForgeHook` hook not a complete boundary (cwd/`dir_fd`-relative access, unlisted audit events) with no passing-leg exploit; `R55MutC1Counter` 9/9 counter mutants SURVIVED (redundant/untested clauses: SHA, QUOTE line, extra files, `spans.tsv`-on-refusal, oracle pin, path arm). These weaken the **counter**, not the candidate: the judge's direct runs above establish the capability independently. Routed (§6).

### R55-C2 — depth (sourced: NMPA grey-literature search-record field, by document) — improved (re-measured)

Evidence-verified: before `ENTRIES=0/1 BOUND=0/3 … C2=FAIL` (`controls/c2-before.txt`); STAGED/REWRITE controls FAIL; after `BOUND=3/3 QUOTE_ROWS=19 CAPTURE_BOUND=19/19 ANCHOR_BOUND=3/3 QUARANTINE_VERDICTS=1/1 C2=PASS exit=0` (`c2-measure-after.txt`, header revision `5a35ebd6`).

Re-measured:

- new ground: `git grep -c 是否检索灰色文献 dba605de -- corpus/knowledge` → exit 1; at TIP → `grey-literature-and-chinese-search-record-r40.md:5`; entry absent at base (`git cat-file -e` → 128).
- rows: `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → base 123, TIP 126; S124/S125/S126 have 11 cells, `mined`, opened `2026-10-27`, `180d`, `used-by` = the r40 entry only (`git grep -lE 'S12[4-6]' 53f1ce6b -- corpus/knowledge` → that one file); first source-cell URLs = the guideline `.doc` (gcpunion), the cnpharm report, the NMPA English notice; tiers B, B, A.
- entry: three `source: S12x — <url>` lines; `S###` tokens in the entry: S124 ×11, S125 ×7, S126 ×6, no S113.
- spans, independent of the builder: for each of the 19 `spans.tsv` rows the judge built the defined form itself (OLE `.raw` → stdout of `tools/capture-text.py` as subprocess, sha256 at base = TIP = `2c0140bc…`; HTML captures → `.txt` UTF-8 universal newlines) and checked: digest of the file read = `capture_sha256`; `form[offset:offset+len(span)] == span`; quote in span, span longer than quote; quote ≤25 words and ≤160 chars; quote occurs once in its form; quote in the entry and in the round-55 lesson → **19/19 all checks true** (S124 ×11 from the OLE form, S125 ×4, S126 ×4).
- anchors: every `char N` in the rows' `anchor` cells (S124 761/994/4625/4652; S125 242/371/780; S126 777/1204/1324) is the offset of a quote of that id → true for all three.
- the `.doc` form carries no date or issuer stamp: `len 13718, U+FFFD 0, '2019' absent, 发布 ×0` — the entry's narrowing (issuer/date bound to S125/S126) is required by the bytes.

### R55-C3 — calibration (eleven round-54-W2-falsified lane statements, anchored errata) — improved (8/11 observations re-measured, 3/11 evidence-verified)

Evidence-verified: before `ERRATA=0/11 MISSING=11 C3=FAIL`; RESTATE `WRONG=11`, PARAPHRASE `ANCHOR=11` (`controls/c3-*.txt`); after `ERRATA=11/11 C3=PASS exit=0` (`c3-measure-after.txt`, header `5a35ebd6`). `R55MutC3Counter`: 5/5 counter mutants KILLED.

Re-measured:

- anchors: each of the 11 `erratum:` lines' anchor occurs exactly once in its target at `53f1ce6b` and at `dba605de` (statement corrected by append, never rewritten).
- append-only: `git diff --numstat dba605de 53f1ce6b | awk '$2>0'` → empty (zero deleted lines in the whole round; r36 +9, QUALITY +10, SOURCES +3, SKILL +2, LOG +11).
- observations (judge's own code over the cache):
  - E01 S122 `.txt`: `该标准暂无全文，请等待更新` count 1, char 1712 = erratum.
  - E02 S121: `主管部门为 国家标准委` at char 569 = erratum.
  - E03: `附录` 0/0, `文献类型` 0/0 = erratum.
  - E04: `国家标准委` S121=2, S122=2 = erratum.
  - E05: the six S101 phrases in the defined OLE form at 11972, 12007, 12795, 12963, 14049, 25123, drift +802 ×5 and −9251 = erratum.
  - E06: UTF-16LE decode C0 = 18451 / excl. tab+LF 18431 / excl. tab+LF+CR 18242 (U+FFFD 263) = erratum.
  - E07: defined form C0 = 469 = LF 469 (27,012 chars) = erratum.
  - E10: `corpus/evidence/round54/controls/c1-controls.txt` `## shell` block → `LEGS=1/6` = erratum.
- not re-run: E08 (`pointer-anchor-check` on a BASE mirror), E09 (ctypes `system()` under the round-54 hook) and E11 (oracle-echo supplement run). They are probe runs the counter makes, so the judge relied on the committed receipt and on W1 `R55ExecC3ObsProbe`.
- reviewer note: E06 and E07 are definitional mismatches. The statements did not name their exclusion set, and the observed counts are of LF characters. They are real calibration slips, now governed by QUALITY 101 ("each count names the set it excludes"). `R55CritC3Calib` warned of count inflation. The judge's view is that the 11 items are distinct statements with distinct observations, so the count is not padded.

### Axis-harm check

`git diff dba605de 53f1ce6b -- SCORECARD.md`: additions only. These are the "Round 55 statement errata" block, the round-55 verdict, the capability row and the round-56 plan. No score lowered. The numeric operability scale stays 3/10 and no number is invented. Freshness: no fetch, newest capture 2026-10-24, so unchanged. Adjacency: drug-safety evaluation practice is reported as adjacent (entry `#### Unknown` Province bullet). No sibling file was touched. Census at TIP: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → five pre-existing W04 (S051 S053 S073 S074 S075) and `ok`, exit 0, identical to `census-end.txt`.

## 3. Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| operability | improved | C1 re-measured (builder reproduces 19/19 + round-54 33/33 byte-identical; refusals all-or-nothing) + gate receipts 4/4 ×4 |
| depth | improved | C2 re-measured: 3 documents bound, 19/19 spans exact in defined forms |
| coverage | improved | observed, not claimed: `是否检索灰色文献` absent from `corpus/knowledge` at base, present at TIP (one admitted entry on new ground) |
| calibration | improved | C3: 11/11 anchors once, 8/11 observations re-derived equal, receipts for the rest |
| freshness | unchanged | no fetch; captures dated ≤2026-10-24 |
| adjacency | unchanged | adjacent practice reported, not absorbed; no sibling write |

## 4. Discernment spot-check (non-author re-open; cache above, no fetch)

| item | gate decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| `grey-literature-and-chinese-search-record-r40.md` (S124 guideline `.doc`) | admit, narrowed | `tools/capture-text.py …/bdff491a75c6abeda1d9c01d.raw --locate '是否检索灰色文献'` → `LOCATED count=1 offset=4678`; form chars 4625/4652 hold `文献检索策略：…` / `应当说明是否有检索限制…是否检索灰色文献等关键问题。` | agree | The field is in the report item exactly as quoted. 应当 is rendered "should" in Observation and Inference. 2019/发布 are absent from the `.doc`, so the issuer and date are bound to S125/S126. Currency and authority are left Unknown. Every quote checks out (19/19). |
| `grey-literature-field-boundary-r43.md` (staged S161, Guizhou) | refuse (this round) | staged entry `shokuknow/merge/chousa/knowledge/corpus/knowledge/grey-literature-field-boundary-r43.md`; capture `9b348736cee505afe2f55a9c.txt` (6,458 chars) | agree | The page implements a different national instrument (质量控制指南 ×6, 国家药品监督管理局 ×0, 上市药品临床安全性 ×0). It holds no grey-literature wording at all (灰色文献 ×0, 灰色 ×0). Its staged argument is an absence claim that also rests on round-8 and T/CLPA material not bound by document. Off this round's NMPA theme. The lesson's `refused-doc` line and flip condition are recorded. |
| staged S133 leg (梅斯医学 PRISMA-S record = held S113) | reject (not carried; price inference cut) | `453d492becd9a2f4632cb8dd.txt` | agree | `paymentAmount=10` occurs once, inside a serialized object dump beside `paymentType=`, `opened=0`, `haveAttachments=1`, and the page has no 登录 text. A page field does not establish how the article is accessed, so the "price, not a login wall" inference is unsupported. The entry carries no `source: S113`, and S113's row is untouched (`git diff … SOURCES.md | grep -c S113` → 0). |
| quarantine: register `S125` (round6) on the guideline `.doc` | verdict `absent-as-written` | defined OLE form: `检索策略包括` ×1 at 761; the `文献检索策略` sentence at 4625; `即灰色文献` ×0; `即“灰色文献”` ×1 at 1012 | agree | Two of the three register strings are present, and the third differs only by curly quotes, so the register's `payload-absent` is wrong as a blanket verdict and nothing is fabricated. Offset nit: D4. |
| new SOURCES row S126 (≤25-word quote) | admitted row, tier A for identity/issuer/date | `d663d66e2d39f868d84b1781.txt` (3,774 chars) | agree | `which was issued on June 18, 2019` (7 words) occurs once at char 1324, inside `NMPA organized the formulation of the Guidelines … (Interim), which was issued on June 18, 2019.` (1204…). `Updated: 2019-07-18` is at char 777. Tier A is scoped to facts the regulator's own site states. |

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → exit 0 (5 × W04 pre-existing, adjudicated in the lesson's `## Gate`).

## 5. Trend verdicts

- **expansion — improved.** One admitted `knowledge/` entry stands on ground absent at base (git grep exit 1). It cites three new `mined` rows S124–S126, bound by document. One capability row was added (OLE-aware span builder) and demonstrated running.
- **quality — improved.** Spans are now taken from defined text forms through one lane-level builder that reproduces round 54's manifest byte for byte. Eleven falsified statements are corrected by appended, anchored errata whose observations re-derive (8/11 by the judge). The r36/r37 corrections and QUALITY 101–105 were appended. The round deleted nothing, and no admitted entry failed its re-check.
- **discernment — improved** (the lane self-graded `unprovable-but-better`). The outside spot-check agrees with the gate on one admit, two rejects and one quarantine verdict. The falsified statements became lessons with grounded QUALITY criteria (101 for the count-set rule, 104 for wave settlement). The non-run W2 falsify wave and the unsettled W1 are conformance debt (D1). They are not a disagreement with any gate decision.

## 6. Routed defects (lane fixes next round)

1. **Settle round 55's waves.** Commit `w1-results.json` and integrate the W1 seats that reported after filing. If a late W1 report falsifies a landed C1/C2/C3 statement, file an appended correction. Dispatch or explicitly retire the 36 W2 items in `w2-spec.json`, and record in the round-56 report which landed claims they hit (D1, D2; QUALITY 104).
2. **C1 counter hardening.** `R55CritForgeHook` found the hook is not a complete boundary (cwd/`dir_fd`-relative access, unlisted audit events). `R55MutC1Counter` had 9/9 mutants survive (SHA cell, `QUOTE` stdout line, extra span files, `spans.tsv`-on-refusal, oracle pin, path arm untested). A successor counter needs fixtures that kill each mutant before it is cited as a gate for a future capability claim.
3. **Report/receipt revision agreement (D3).** Cite the revision each after-measurement names in its receipt header, or commit a receipt for any re-run at a later revision.
4. **Quarantine-line offset (D4).** Append a correction to the round-55 lesson's quarantine line: `即“灰色文献”` is at char 1012 of the defined form, and 994 is the start of its sentence.
5. **`build-spans` registry class.** The registry row calls the builder a `probe`, but `--check` exits 1 on `STALE>0` and it refuses rows with exit 1, so it can fail. Re-register it as a gate with a self-test, or state why it stays a probe.

## 7. Note for the operator

The SHONEN boxes (craft rows `SKILL.md:142-143`; logged rounds with LOG "Round 55" and three after-receipts; runnable checks with committed receipts; province fit with the adjacent practice reported) are each checkable by a non-author from committed pointers. Promotion is operator-owned; this file writes no `[x]`.
