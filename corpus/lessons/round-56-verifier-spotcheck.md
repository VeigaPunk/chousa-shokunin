# Round 56 verifier spot-check — chousa

author: hyaku closure (non-author integrator, @m_opus)
date: 2026-10-27
scope: chousa round 56; round start `f2b15b482062b4ad60f35377f039e2a2cfe33d67`, claim base `e5a3795191601797613eb986b36fa0b1a73fe6a1` → TIP `b804147b55f17c78e082e05eca0eadbab47f3320` (== `master` == `origin/master`, ahead=0); FREEZE `41c58925580af6be22049f13cfde234c5475b858`; C1 candidate `46e1758f3d8a5d1bf30200d2ff7d909b0230feed`; report `.ufo/reports/round-56/chousa.md` (fleet `435d2d061bf96a638c825d5d4944d615835dcae9`).
Non-author: the hyaku closure judge wrote this file, not the lane. No lane gate or frozen counter was executed (`corpus/evidence/round56/c1-count.py`, `c1-gate.py`, `c2-count.py`, `tools/build-spans.py`, `tools/inference-ground.py`, `quote-substance-check.py`). PROTOCOL §Gate standard, Closure consequence, forbids it, and the capture cache those tools read no longer exists (see Re-measurement gap). Their verdicts were checked through committed receipts. Plain counts over committed bytes were re-measured by the judge. So were the C2 span bindings, against a fresh read-only re-fetch of the five PDFs; the scratch dir `/tmp/r56close` was removed after.

Driver digest (copied from the mutable `.ufo/watchdog.log`):

    2026-10-27T01:21:54-03:00 launch chousa round=56 pgid=2786557 driver=hyaku-inline attempt=1
    2026-10-27T02:33:53-03:00 complete chousa round=56; hyaku-inline attempt=1

**Re-measurement gap (host event, not lane bytes).** The read-only campaign capture cache `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/` was deleted at about 02:16:49 -03. It is git-ignored and `ls` reports `No such file or directory`. The lane filed L0 `a714799f` about it. `find /home/vgpnk/Projects /fast /tmp` found no surviving copy of the captures `b27ffd2f…`, `de9f5afc…` or `a42feae4…`. Any capture-reading counter now exits `ENV_CHANGED`, and that exit is not scored as a lane falsification. C1's after-receipt (02:08:29) and C2's (02:15:51) predate the deletion. C1 is evidence-verified only. Its gate's OLEPIN/REGRESS legs need the four pinned OLE captures, so no re-run without the cache was possible. C2 was re-measured instead. `pdftotext -layout` (26.08.0) on a fresh fetch of each URL reproduces the lane's recorded text-form digests byte for byte, so the C2 binding could be checked without the cache.

## 1. Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report committed by lane identity | `git log --format='%an %H %ci' -- .ufo/reports/round-56/chousa.md` | `chousa-shokunin 435d2d06…` 02:32:32 -0300. This is after lane tip `b804147b` (02:31:28) and before the driver's `complete` (02:33:53). | pass |
| `SHONEN` heading, one line per box | read report §SHONEN | 4 lines, all `[~]`: craft rows, logged rounds, runnable checks, province fit | pass |
| cited lane hashes exist and are ancestors of `master` | `git rev-parse --verify <h>^{commit}` + `git merge-base --is-ancestor <h> master`; hashes: `f2b15b48 e5a37951 41c58925 46e1758f 0c2f4ce5 99eff0ec 2ceb4049 98977070 e129c9e4 751edb3f 9d402b0e b804147b` | all 12 resolve, all exit 0; all authored `chousa-shokunin` | pass |
| non-lane hashes `8d77e6c1`, `a714799f` | `git -C <fleet> log -1 <h>` | both resolve as fleet commits, "chousa L0 question": quote re-open fetch scope, and the capture cache deletion | pass |
| lane pushed, nothing uncommitted | `jj-lane.sh state …`; `git status --porcelain` | `branch=master local=remote=b804147b… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty | pass |
| prompt carries the template contract | `templates/round-prompt.md` rendered (`{{LANE}} {{ROUND}} {{FLEET_ROOT}}`) and diffed with lines 1–140 of `.ufo/prompts/chousa-round-56.md` | 2 differing lines. Line 1 has `<chousa-repo>` resolved to the lane path. Line 6 has `{{AXES}}` resolved to the lane's axis text. §6 hyaku addendum and §7 scratch discipline are present. No L2 route map is quoted. Fleet template = canonical (`cmp` equal). | pass |
| frozen inputs unchanged FREEZE..TIP | `git diff --stat 41c58925 b804147b -- claims.md c1-count.py c1-gate.py probes c2-count.py controls tools/build-spans.py tools/capture-text.py` | empty | pass |
| C1 inputs unchanged candidate..TIP | `git diff --stat 46e1758f b804147b -- c1-count.py c1-gate.py battery probes tools/build-spans.py` | empty; `sha256sum` of the gate, the builder and the 8 battery files at TIP = the receipt's 10 digests | pass |
| C2 inputs after the receipt | `git diff --stat 98977070 b804147b -- corpus/knowledge corpus/SOURCES.md spans.tsv spans quotes.tsv corpus/lessons/round-56.md c2-count.py tools` | `corpus/lessons/round-56.md` +3 lines only: Mistakes row 4 and the incident, appended | pass |
| wave settled before filing | `w1-results.json` `seats`/`results`; `ls .ufo/waves/round-56/w1` | 69/69 results. 64 seat reports + `swarm-registry.json`. The 5 seats without a file are exactly those the report names: `R55W2CritGate R55W2ReviewC1Claims R55W2ReviewRows R56CritC1Forge R56MutC2Counter`. Round total 69 ≥ 64 floor. | pass |
| registry home | `SKILL.md:144-145` | `build-spans` (round 56) re-registered as `gate`, with verdict map and self-test command; round-56 counters row (`gate`) | pass |
| append-only | `git diff f2b15b48 b804147b -- lessons/round-55.md QUALITY.md knowledge SOURCES.md SKILL.md LOG.md \| grep -c '^-[^-]'` | 1: the S118 row's in-place `used-by` change. That change is allowed and logged old→new in the lesson `## Gate`. | pass |
| scratch | `ls -d /fast/scratch/hyaku/chousa-r56` | absent, so the round's tree was removed as reported | pass |

Conformance defects (status-neutral; named, not barring admission):

- **D1 — corrections sweep missed one mention.** Mistakes row 3 corrected the 表 10 → 表7 misattribution in the entry body, the S129 row and the quote table. The entry's `recheck:` line (`corpus/knowledge/grey-literature-field-china-r42.md:9`) still reads "the journal's 表 10 row still carries `Ⅰ级` and `A`". The Observation bullet (line 18) mentions 表 10 legitimately, as the misleading text-form title. The recheck line, however, instructs a future re-check against the wrong table (PROTOCOL §Evidence standard, "Corrections sweep every mention").
- **D2 — the lane's own seed-test recipe failed (disclosed).** Three C1 driver attacks did not measure: `R56CritC1Forge` printed `('ENV', 2)` from a `git archive` copy, `R56MutC1Driver` was INCONCLUSIVE because of the cache deletion, and `R56MutC2Counter` left only a fragment. The lane reports them as unrun, not survived (QUALITY 110). Recorded so the next round re-runs them.

## 2. Claim re-checks

### R56-C1 — operability (lowest scored axis, 3/10): build-spans gate clause coverage + two hook probes — improved (evidence-verified)

- Frozen predicate = `c1-count.py` docstring (`claims.md:53-75`). `MUTANTS` at `c1-count.py:70-84` holds the nine named edits M1–M9. The battery has 8 files and `probes/` has 2 (`git ls-tree … | wc -l` → 10). `c1-gate.py:95` adds `_posixsubprocess.fork_exec` and `os.chdir` to the hooked events.
- Before (`controls/c1-before.txt`): `CANDIDATE=2/2 KILLED=1/9 DENIED=0/2 C1=FAIL`, exit 1. Controls (`controls/c1-controls.txt`): HOOKONLY, JUNK (with the FLIP forge) and EMPTY each print `KILLED=1/9 … C1=FAIL`, exit 1. No control met the target.
- After (`c1-measure-after.txt`, header `at lane master 99eff0eca3d7…`): two runs, each `RUNS=124 CANDIDATE=2/2 KILLED=9/9 DENIED=2/2 C1=PASS exit=0`. Each kill line names the clause's own reason: M1 `span is not a slice`, M2 `S901 char`, M3 `capture_sha256`, M4 `QUOTE line`, M5 `extra or missing span files`, M6 `NOFORM: spans.tsv written`, M7 `rc=97 … AUDIT_FORBIDDEN`, M8 `('ENV', 2)` vs mutant PASS, M9 by CANDIDATE. P1/P2 are `(1, FAIL×4)` at both seeds. Receipt digests equal the TIP bytes (table above). Revision cited = receipt header, so round-55 D3 does not recur.
- Not re-executed: the gate is the lane's (§Gate standard), and its pinned captures are gone. Lane seats `R56ExecC1Measure` and `R56SentC1` reproduced `KILLED=9/9 DENIED=2/2 C1=PASS` before the deletion, but they are the lane and are cited as corroboration only.
- Open beyond the frozen predicate, disclosed in SCORECARD "improved narrowly" and the round-57 plan: `dir_fd` without `chdir` (`R56SentC1` F1), native-extension `import` (`R56CritC1Hook`), and six uncovered gate clauses. These do not falsify the predicate, which names exactly two probes.

### R56-C2 — depth (sourced): the 灰色文献 row of 药品临床综合评价工作流程指南, by document — improved (re-measured)

Commands run by the judge over `git show b804147b:<path>`, in Python unless shown otherwise:

| predicate part | observed | result |
|---|---|---|
| entry exists, new | `git cat-file -e e5a37951:corpus/knowledge/grey-literature-field-china-r42.md` → absent; present at TIP (35 lines) | pass |
| NEW_GROUND | `git grep -c 中国循证医学中心 e5a37951 -- corpus/knowledge` → exit 1; at TIP `…r42.md:6` | pass |
| rows new, mined, opened, used-by | registry 126 (`f2b15b48`) = 126 (`e5a37951`) → 130 (TIP); new ids exactly `S127 S128 S129 S130`. Each row has 11 cells, `mined`, opened `2026-10-27`, `used-by` = the entry; tiers B/B/A/B. | pass (BOUND 4/4) |
| source lines | entry lines 3–7: `source: S127|S128|S129|S130|S118 — <the row's first URL>` | pass |
| S118 held | `used-by` at base names r48 and r50; at TIP it adds `…grey-literature-field-china-r42.md` | pass |
| S### tokens in entry | `{S118,S127,S128,S129,S130}` only | pass |
| quote rows | `spans.tsv`: 23 rows (S127 9, S128 5, S129 6, S130 3); every quote ≤25 words and ≤160 chars; 23/23 in the entry and 23/23 in the lesson | pass |
| CAPTURE_BOUND (re-measured without the cache) | Each URL was re-fetched and run through `pdftotext -layout`. sha256 of the forms: S127 `23306b9f…`, S128 `7e3e3cf4…`, S129 `beac2b7f…`, S130 `71fed1a3…`, equal to every `capture_sha256` in `spans.tsv` and to the row anchors' recorded prefixes. `form[offset:offset+len(span)] == span` and quote ∈ span for 23/23 rows. Held S118: form `927ff71c…` = manifest; span exact; quote at char 17840. | pass |
| ANCHOR_BOUND | every `char N` in the S127–S130 anchor cells (9+5+6+3 = 23) equals `offset + span.find(quote)` of a row of that id | pass 4/4 |
| SUBSTANCE, INFERENCE_GROUNDED | not re-executed (lane gates); receipt `c2-measure-after.txt` (header `at lane master 98977070…`) prints `SUBSTANCE=PASS INFERENCE_GROUNDED=1/1 … C2=PASS exit=0` | evidence-verified |

Before: `controls/c2-before.txt` `BOUND=0/4 … C2=FAIL`. Controls: STAGED `BOUND=0/4`, REWRITE `QUOTE_ROWS=0`, both FAIL. Content checks on the re-fetched forms:

- S127 prints `T/CLPA XXXX—2025` and `（征求意见稿）`.
- S130 has `灰色` ×0 and S118 has `灰色` ×0, as the entry says.
- In S129 every source row of 表7 prints `Ⅰ级  A` (10/10 rows: 文献数据库 … 灰色文献, 搜索引擎), so the entry's narrowing holds: the grade does not single out grey literature.

### Axis-harm check

`git diff f2b15b48 b804147b -- SCORECARD.md` contains additions only: the round-56 verdict, capability row, post-wave notes and round-57 plan. No score was lowered and no number was invented; operability stays 3/10 with the gate counter named as a separate observable. Census at TIP: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → five pre-existing W04 (S051 S053 S073 S074 S075) and `ok`, exit 0. The output is identical to `census-end.txt` apart from its `exit=0` line. No sibling file was touched (`R56ConnSiblings` 0 overlaps; the entry's `#### Unknown` reports grading systems and evaluation content as adjacent).

## 3. Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| operability | improved | C1, evidence-verified: receipts ×2 at `99eff0ec`, digests = TIP, inputs unchanged; controls fail. The gap is a host event, not lane bytes. |
| depth | improved | C2 re-measured: 4 rows bound, 23/23 spans exact slices of the re-fetched forms with matching digests, anchors 23/23 |
| coverage | improved | observed: `中国循证医学中心` absent from `corpus/knowledge` at base (exit 1), present at TIP; one admitted entry on new ground |
| calibration | improved | closure D3/D4 corrected by appended lines in `corpus/lessons/round-55.md`; QUALITY 106–110 each cite a Mistakes row; the round's own 表7 misattribution was caught and fixed before filing. D1 is a residual sweep miss and is routed. |
| freshness | unchanged | no lane fetch; capture dates ≤2026-10-24. The judge's re-fetch shows the four documents and S118 unchanged byte-for-byte in text form. |
| adjacency | unchanged | adjacent ground reported, not absorbed; no sibling write |

## 4. Discernment spot-check (non-author re-open; live read-only re-fetch, cache gone)

| item | gate decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| `grey-literature-field-china-r42.md` (staged r42 → S127–S130) | admit, narrowed | the four URLs via `curl` + `pdftotext -layout`, forms equal to the recorded digests | agree | The S127 item `（9）灰色文献：未公开发表研究信息…` is at char 24624 and is a draft (placeholder number and dates). In the S129 layout, `表7    药品临床综合评价的信息来源情况` heads the left column. The 灰色文献 row sits under it, above `表8`, and `表 10` is the right column's title, so the lane's 表7 fix is right. All 10 source rows of 表7 print Ⅰ级/A, and 表2 defines A as `推荐，证据极有效（证据等级为Ⅰ级）`. The "grades the recommendation to use the source, not the literature" narrowing is therefore supported. S130's text form has `灰色` ×0 and is dated `二〇二〇年十一月`. |
| `grey-literature-national-route-r44.md` (staged, `shokuknow/merge/chousa/knowledge/corpus/knowledge/`) | refuse | the staged file; S127 §2 and S128 参考文献 in the re-fetched forms | agree (decision); reason incomplete | It is a duplicate theme on S127/S128, already bound by document into r42, so refusing it is right. It also carries errors: it calls the 征求意见稿 "the group's own published copy" and frames 中国循证医学中心's grading as "a national centre's system". It also says the centre's quality-control guideline host "does not answer", yet the lane holds S118 and the judge fetched it (HTTP 200). However, its "inputs" claim has more support than the refusal states. S127's `2 规范性引用文件` normatively cites the 2021 管理指南, the centre's 2022 技术指南 and the `药品临床综合评价质量控制指南（2024 年版 试行）`, and S128 参考文献 [3]–[6] cite the centre's documents. The flip condition ("binds the note's reference list") is right but should name S127 §2 as the stronger anchor. |
| new SOURCES row S128 (≤25-word quote) | admitted row, tier B | re-fetched S128 form (7031 chars, `7e3e3cf4…`, = row) | agree | The quote `（2）2024 年 6 月-8 月，工作组采用中国循证医学中心中国循证医学中心的` occurs at char 3064, as stated in the row anchor, lesson `## Gate` and spans.tsv. It is a single sentence fragment, ≤25 whitespace words and ≤160 chars. Tier B for a drafters' note scoped to provenance is honest. |
| new SOURCES row S130 (quote) | admitted row, tier B | re-fetched S130 form (6930 chars, `71fed1a3…`, = row) | agree | `二〇二〇年十一月` is at char 129 and `国家卫生健康委药具管理中心` at 103. Scoping the tier to the 2020 text's identity, with an explicit refusal to speak for the 2021 管理指南, matches what the document shows. |

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → exit 0; the 5 × W04 are pre-existing.

## 5. Trend verdicts

- **expansion — improved.** One admitted `knowledge/` entry stands on ground absent at base (git grep exit 1). It cites four new `mined` rows, S127–S130, bound by document, plus held S118. One capability row was added (gate clause coverage by clause-reason mutation kills) and demonstrated running in two receipts.
- **quality — improved.** The 36 never-run round-55 W2 items ran, and their narrowings were appended (r40 `#### Corrections (round 56)`, round-55 `## Corrections`). Closure D3/D4 were corrected. The round's own table misattribution was fixed before filing. `build-spans` is now a registered gate whose round-55 clauses are each shown able to fail. No admitted entry failed the judge's re-check. D1 is a stale instruction line, not a false observation.
- **discernment — improved** (the lane self-graded `unprovable-but-better`). The outside spot-check agrees with the gate on one admit, one reject and two new rows. The round's mistakes became lessons with grounded QUALITY criteria (106–110). The one partial note, that the r44 refusal reason understates the reference-list evidence, does not reverse a decision and is routed below as a lead.

## 6. Routed defects (lane fixes next round)

1. **D1 — stale `recheck:` instruction.** Append a correction to `grey-literature-field-china-r42.md` (a new `#### Corrections (round 57)` block; no rewrite), so that its re-check targets the 灰色文献 row of 表7. Then sweep every lane file for any other "表 10 row" instruction.
2. **Re-run the unmeasured C1 attacks.** Run `R56CritC1Forge`, `R56MutC1Driver` (eight driver mutations) and the `R56MutC2Counter` item once the capture cache is restored (L0 `a714799f`), or on a recipe proven per QUALITY 110. Report each as survived/killed, not inherited.
3. **Hook classes beyond the two frozen probes.** Cover `dir_fd` without `chdir` (`R56SentC1` F1), native `import` (`R56CritC1Hook`) and `sqlite3.connect`, as the round-57 SCORECARD plan already names. A new frozen probe set needs its own red-before.
4. **r44 lead, not a defect in the decision.** S127 `2 规范性引用文件` normatively cites the national centre's 2022 技术指南 and its 2024 质量控制指南 (held S118). A future entry on "the national centre's instruments as the workflow guideline's normative inputs" should bind that clause by document; the refusal's flip condition should name it.
5. **Capture-cache dependency.** Every C1/C2 counter fails closed (`ENV_CHANGED`) without the git-ignored campaign cache. Until L0 `a714799f` is answered, the judge's live re-fetch shows `pdftotext -layout` 26.08.0 reproduces the four PDF forms byte for byte. Consider committing a digest-pinned re-fetch recipe beside the receipts; OLE captures have no such route.

## 7. Note for the operator

The SHONEN boxes can each be checked by a non-author from committed pointers:

- craft rows: `SKILL.md:144-145`, QUALITY 106–110;
- logged rounds: LOG "Round 56" with two after-receipts;
- runnable checks: the counters and controls with receipts;
- province fit: adjacent ground reported, 0 sibling overlaps.

Promotion is operator-owned; this file writes no `[x]`. Separately, prior-round scratch dirs `/fast/scratch/hyaku/chousa-r53`, `-r54` and `-r55` are still present. They are not round-56 debt.
