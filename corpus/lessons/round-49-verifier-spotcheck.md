# Round 49 verifier spot-check — chousa

author: hyaku closure (non-author integrator, @m_sonnet)
date: 2026-10-25
lane round closed: 49 (report `.ufo/reports/round-49/chousa.md`, committed by lane identity `chousa-shokunin <chousa@shokunin.local>` at `3cbe92a467d4313f1d1494614afe4275571712c8`)
lane HEAD measured: `5275c892273242b5be989336f5d44ce8cbf671f9` (local=remote, ahead=0, behind=0)
base → head: `414a2ec6cde05a921dbdd9e02e7ae56b0db647ef` → `5275c892273242b5be989336f5d44ce8cbf671f9`
dispatch digest (`.ufo/watchdog.log`): `2026-10-25T16:50:02-03:00 launch chousa round=49 pgid=135352 driver=hyaku-inline attempt=1`; `2026-10-25T17:38:28-03:00 complete chousa round=49; hyaku-inline attempt=1`

No fetch was made. Every source re-opened below is an on-disk capture under the read-only campaign cache
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache` (L0 `8d77e6c1` open). I did not execute the lane's
registered gate `chousa round-49 counters and checks` (PROTOCOL §Gate standard, Closure consequence): its claims are
**evidence-verified** from committed `measure-after.txt` and **independently re-measured** by the plain commands below.

## Step-1 conformance

| check | result |
|---|---|
| report committed by lane identity | OK — `git log --format='%an %H' -- .ufo/reports/round-49/chousa.md` → `chousa-shokunin 3cbe92a4…` (17:37:18, after the lane tip 17:36:58) |
| SHONEN heading, one line per box | OK — 4 `[~]` lines with pointers; `SHONEN.md` has 4 boxes (`grep -c '^- \[' SHONEN.md` → 4) |
| cited commits exist + ancestor of `master` | OK — `fe740e78`, `65940928`, `1254ab26`, `4ce61fc5`, `87e93353`, `763b3370`, `5275c892` each pass `git merge-base --is-ancestor <h> master`. `8d77e6c1` in the report is an L0 question id, not a commit (not in the lane repo; not a defect). |
| pushed / clean lane state | pushed OK — `jj-lane.sh state` → `local=remote=5275c892… ahead=0 behind=0`; `git ls-remote origin refs/heads/master` → `5275c892…` |
| uncommitted round work | **DEFECT (status-neutral)** — `git status --porcelain` shows three untracked late seat reports `.ufo/waves/round-49/w2/{MutA05,MutSubstance,ReviewQuality}.md`. The report admits these seats were outstanding at filing (§Round shape). They are wave evidence, not claim evidence; the lane's next round commits or names them. |
| dispatched prompt carries contract | OK — `.ufo/prompts/chousa-round-49.md` (545 lines) carries §1 mission/axes, §2 claims, §2b frontier step, §3 L2 floor (≥8), §4 report contract (path, SHONEN, hash rule), §5 commit/push scope and L0 channel, write scope (line 318–320), hyaku addendum §6 |
| report-before-WAVE-DONE | **DEFECT (named by the lane)** — report filed with W1 39/40 and W2 27/35 seat reports; the lane records this itself |
| round shape | 40 + 35 = 75 seats (report §Round shape) ≥ L2 floor; connectors and scribes present in both waves |
| stale-lane | launch → complete in 48 min, lane commits progressing. OK |
| evidence-pointer hygiene | OK — the report cites the lane tip `5275c892`; `measure-after.txt` header says it was measured at `763b3370`, and `git diff --stat 763b337 5275c89 -- corpus tools SKILL.md` → only `measure-after.txt` changed (29/29 lines), so the tracked code tree measured equals the tip's |

## Per-claim re-check

### R49-C1 operability (capability; lowest scored axis 3/10) — **re-measured and evidence-verified**

`SCORECARD.md` carries exactly one scored axis, operability 3/10, so the lowest-axis duty is met
(`grep -n 'lowest scored' SCORECARD.md` → the standing C1 rows through r48).

1. Freeze integrity — `git diff --stat fe740e78 5275c892 -- corpus/evidence/round49/c1-count.py corpus/evidence/round49/c2-count.py corpus/evidence/round49/claims.md corpus/evidence/round49/controls` → empty. The frozen counters, claims and controls are byte-unchanged since the freeze; only `build-spans.py` changed (14+/1−, disclosed).
2. Before state (evidence-verified, not re-run): `controls/c1-before.txt` → `TOOL=absent C1=FAIL` exit 1; copy control `SETS_PASS=0/3`, GUARD `COLLISIONS=[]` FAIL, PIPE `CELLS=13` FAIL. Control is a real do-nothing candidate of the same interface and fails every leg for the stated reason.
3. After state, plain re-run of the tool (not the gate), set A, base registry `git show 414a2ec6:corpus/SOURCES.md`:
   `python3 tools/assimilate-rows.py --staged $PKG/SOURCES.append.md --knowledge $PKG/knowledge --registry base-sources.md --opened 2026-10-25 --out OUT --entry corpus/knowledge/aggregator-vs-source-r36.md --entry corpus/knowledge/citation-count-semantics-r37.md`
   → `COLLISIONS=14`, `CITED=9 APPEND=9 HELD=0`, exit 0; `sha256sum $PKG/SOURCES.append.md` → `a6dec4a0…` (the pinned digest). `renumber.tsv` maps staged S087/S088/S089/S091/S092/S100/S101/S102/S103 → S096…S104 contiguous from the base maximum S095, by document (S100→S101 etc., no chaining). `append.md` rows each have 13 `|`-fields (11 cells), status `mined`, opened `2026-10-25`, recheck `180d/90d/365d`, `used-by` the citing entry. Appended into a scratch registry mirror after the last registry row: `sources-census.sh validate --file <mirror>` prints no finding other than the W04 baseline and E11 (E11 only because the mirror lacks the lane's knowledge files). **Matches reported `SET_A … APPEND=9/9 BY_DOC=9/9 CONTIGUOUS=yes COLLISIONS=match`.**
4. GUARD: scratch registry `  | S002 | y |` (two leading spaces) vs staged `| S002 | x |` → tool prints `COLLISIONS=1`, `collisions` file `S002`. Matches `GUARD COLLISIONS=['S002'] -> PASS`.
5. Sets B and C and PIPE were not re-run by me (they need the lane counter's scratch mirrors); they are **evidence-verified** from `measure-after.txt` (`SET_B/SET_C … -> PASS`, `PIPE … CELLS=11 -> PASS`) with the do-nothing control failing each.

Reported limit confirmed: C1 is conformance on fixed inputs and a replay of the tool's outputs passes (W1 `CritForgeC1`); the lane names it in report, SCORECARD, SKILL row and QUALITY 72. Admitted on that scope.

### R49-C2 depth (sourced; derived-index theme) — **re-measured**

1. Registry: `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → **103**; at `414a2ec6` → **95**. Malformed rows (`NF!=13`) → 0. Tier histogram base `A=89 B=1 C=5` → head `A=92 B=6 C=5`; status `mined=71 queued=19 rejected=5` → `mined=79 queued=19 rejected=5`. All three match the report.
2. `sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → exit 0, `ok`, W04 warnings S051/S053/S073/S074/S075 only (identical to round start).
3. Binding — rows S096–S103 carry the document URLs of staged S087/S088/S089/S092/S100–S103; S096–S099 `used-by` = `corpus/knowledge/aggregator-vs-source-r36.md`, S100–S103 = `corpus/knowledge/citation-count-semantics-r37.md`; each entry opens with one `source: S### — <url>` line per bound id plus `verified-at:`/`recheck:` (`grep -n '^source:\|^verified-at\|^recheck' …`). The NCPSSD staged row is absent from the registry (`grep -c ncpssd corpus/SOURCES.md` → 0) and carried as `refused-doc` in the lesson Gate. BOUND=8, REFUSED=1 = 9 documents.
4. Quotes — I parsed the 31 `## Gate` quote rows of `corpus/lessons/round-49.md` and re-opened each capture by file name (`.txt` UTF-8; the two OLE `.doc` captures `b539a802…raw`, `6dc68fd6…raw` decoded as UTF-16LE from the bytes): **31/31** quotes sit at the recorded offset, **31/31** occur exactly once in their capture, **31/31** occur in the citing entry, all ≤25 whitespace words and ≤160 characters (`python3 /dev/shm/q.py` → `ok 31 / 31`, `multi 0`).
5. Spans — for each `spans.tsv` row I located the capture by sha256 over the cache, and compared the span file to the capture slice at the recorded offset: **31/31** equal, quote inside the span, span longer than the quote. (`.txt` forms compared with universal newlines, `.raw` forms as UTF-16LE from bytes.)
6. Inference grounding / quarantine verdicts / `quote-substance-check` are **evidence-verified** from `measure-after.txt` (`INFERENCE_GROUNDED=2/2`, `QUARANTINE_VERDICTS=5/5`, `FAILURES=0`); the lesson carries the five register verdicts at `## Gate` (S082, S084, S086, S095, S096), each `absent-as-written`, none `fabricated`/`unverifiable`.
7. **Ruling on the disclosed post-freeze `build-spans.py` change**: the frozen predicate, target, kill rule and both counters are byte-unchanged (item 1 of C1); the change affects only how span context is clipped for the UTF-16LE forms (bare CR). My own byte-level check (item 5) finds every span an exact slice and every quote located, independent of the counter's newline handling, and the S100 quote replacement kept the quote verbatim in its capture (offset 1431: `…对于合作发文的参考文献中，如果引文出现了任一合作者，那么这条引文将被认定为自引。`). **C2 stands.** The erratum's own false first draft was corrected by W2 inside the erratum; accepted.

Reported before→after: `ENTRIES=0/2 BOUND=0/9 C2=FAIL` → `BOUND=8/9 REFUSED=1 QUOTE_ROWS=31 … C2=PASS`: verified, with the control `REF_ID_UNBOUND=11` failing for the stated reason (staged ids name lane rows of other documents).

## Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| operability | **improved** | C1: absent → `assimilate-rows.py` runs and reproduces the by-document map, the 0–3-space guard and the census-valid append on set A (re-measured); the scale stays 3/10 and the capability is conformance on fixed inputs (named) |
| depth | **improved** | C2: two entries on eight re-opened captures; 31/31 quotes and spans re-measured; W2-narrowed overclaims (the entries state "as these copies state", `Unknown` lists what no first-party page was opened for) |
| coverage | **improved** | index derivation, link lag, resolution ladder, CNKI counter rules: not held at base (`git grep -il 'J-STAGE'`, `'CiNii'` and `'被引'` at `414a2ec6 -- corpus/knowledge` each print nothing; lane `CritTheme` agrees); the aggregator-is-not-the-source conclusion earns nothing, as the lane says |
| calibration | **improved** | a05 propagations corrected in this round's lesson (`grep -n '3/12' …`: the false "exit-level 3/12 incl. a05" lines remain in the append-only verifier files and are corrected in `round-49.md` `## Spot-check intake` row 1); the lane's disclosures (report-before-WAVE-DONE, erratum, counter limits) match observed state. One stale figure — see defect 2 |
| freshness | **unchanged** | newest readable capture 2026-10-24; this round's captures 2026-10-23; no fetch, nothing re-verified live |
| adjacency | **unchanged** | W1 `ConnSiblings`: no sibling overlap; staged `cnki-matching-modes-r42` not adopted because it widens the theme |

No axis harmed: `git diff 414a2ec6 5275c892 -- SCORECARD.md` → 30 insertions, 0 deletions (append-only).

## Discernment spot-check (≥1 admit, ≥1 reject)

| item · decision | re-opened source | agree? | reason |
|---|---|---|---|
| `citation-count-semantics-r37.md` S100 quote (self-citation rule, 高级检索 zero-row note) · admit (narrowed) | capture `b539a80218080da56a75b624.raw` (UTF-16LE decode), offsets 1296/1431/2843; contexts printed | **agree** | the self-citation sentence is in the paragraph headed 关于自引的说明; the zero-count note sits in the 高级检索 step (followed by 高级检索按钮 …图4), exactly the scope the narrowed entry claims; the entry says the copy is third-party-hosted and lists the currency as Unknown |
| S101 row/quote (`.doc`, GB/T 7714 in 14.1 vs ISO 690 in 14.4 and the parameter table) · admit | `6dc68fd6b32ce9c8dfcebce8.raw` as UTF-16LE, offsets 11993 and 34374 | **agree** | 14.1 reads 本规范推荐采用GB/T 7714中规定的顺序编码制格式著录; the parameter table reads 参考文献格式，参照ISO 690; the entry records the split and its register-quote correction |
| S096 CiNii quote and the row · admit | capture `09fc63de41f293d43d631c46.txt`, offsets 3599/3707/3752/3801 | **agree** | all four quotes exact and once; the "matched items, not the paper's list" reading is the page's own words |
| NCPSSD homepage staged row S091 · **refuse** | homepage capture `76914d78c20094f677dea77d.txt` and help capture `c4e1446a42d0a709c34097be.txt` | **agree** | the two access-model strings count 0 in the homepage and 1 each in the help-page capture (`utf-8-sig`); the homepage supports only `中国社会科学院图书馆承建` (168) and `请 登录 注册` (110); `全文下载` and `注册用户` count 0. Adopting the row would have bound unsupported statements to the wrong URL. (My help-page offsets are 24556/24953; the lane's W1 note gives 24872/25269 — a constant 316-char decode offset difference, the quotes are present once; the registry row was refused, so nothing rests on them.) |
| `cnki-matching-modes-r42.md` · reject this round | staged entry `/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/cnki-matching-modes-r42.md` | **agree** | the entry's own Observation says the three modes govern the search platform "not the 引文核对 feature"; it is another feature from the citation-count theme, and its source row (S149) was not re-grounded this round |
| `cnki-citation-check-r40.md` · not adopted (admit-later) | not re-opened (reasoning on the staged entry's theme only) | **agree, unverified** | a feature entry adjacent to the theme; a deferral with a flip condition rather than a rejection is the safer call. Not graded beyond the lane's reason |

Result: 5 of 5 sampled decisions I re-opened agree with the gate; no disagreement to learn from this round. The sixth was not re-opened.

Newly written `SOURCES.md` row re-opened: **S101** (`jc.hit.edu.cn … 1f6f2731….doc`): quote `本规范推荐采用GB/T 7714中规定的顺序编码制格式著录,也可采用GB/T 7714中规定的作者-出版年制。` is 1 string, ≤25 words/≤160 chars, present at char 11993 of the capture (UTF-16LE form), located in the lesson, spans and entry.

## Trend verdicts

- **expansion — improved.** Two admitted entries on ground the coverage map did not hold, each `source:` citing a `mined` new row (S096–S103); registry 95 → 103; the held aggregator conclusion is not credited. Evidence: items 1–4 of C2; `git diff --stat 414a2ec6 5275c892 -- corpus/knowledge` → two new files.
- **quality — improved.** Admitted entries were attacked and narrowed by W2 on six overclaims each; QUALITY 71/72 were each shown able to fail; the inherited QUALITY 69 sentence was verified before it landed. No admitted entry failed its re-check under my sample. Defect 2 (below) is a stale count in a criterion, not an admitted entry.
- **discernment — improved.** The non-author spot-check agrees with the gate on the admits and on both rejections I re-opened, including the refusal of NCPSSD that carried the larger risk; the lane asked for exactly these two re-opens and had not self-graded them.

## Routed defects (the lane fixes next round)

1. Late seat reports `.ufo/waves/round-49/w2/{MutA05,MutSubstance,ReviewQuality}.md` (and any other outstanding seat) are uncommitted: commit them under the round-49 wave directory or record why not.
2. **Stale quote count.** `corpus/QUALITY.md:746` (QUALITY 72) prints `IDS=8 QUOTES=28 FAILURES=0`; `corpus/README.md:1074` says "28-row manifest"; `LOG.md:1803` says "28 located quotes … `CAPTURE_BOUND=28/28`". The committed `measure-after.txt` and `spans.tsv` carry **31** (`wc -l spans.tsv` → 32 incl. header). Append a correction entry (LOG is append-only) and fix QUALITY 72/README by a superseding row or a named correction.
3. **Gate standard — self-test.** The `chousa round-49 counters and checks` registry row lists controls but no self-invocation mode over isolated fixtures (`grep -n -i 'selftest\|self-test' corpus/evidence/round49/*.py` → no match); the do-nothing controls are a before/after pair, not the §Gate standard self-test. The counters also have no `expected.json` digest pin for a frozen snapshot. Status-neutral this round (routed under Closure consequence); a counter that is to be reused as a gate needs a `--selftest` with committed expected finding-ids.
4. Report-before-WAVE-DONE is named by the lane and recorded; repeat is a defect.
5. The lane report's NCPSSD help-page offsets (W1 note 24872/25269) differ from the offsets under plain `open(..., encoding='utf-8-sig')` (24556/24953); the refusal reason does not depend on them. State the decode form next to offsets in a future Gate.
6. Prompt commit attribution: `git log -1 --format='%an' -- .ufo/prompts/chousa-round-49.md` → `chousa-shokunin` (`e45aede9`); the protocol-lane integrator normally commits `.ufo/prompts/*.md`. Attribution defect only.

## SHONEN

All four boxes are `[~]` (asserted by the author). The pointers resolve: `SKILL.md` Gates rows `assimilate-rows` and `chousa round-49 counters and checks` (lines 130–131), `LOG.md` Round 49, `tools/assimilate-rows.py` docstring, `PROVINCE.md`. A non-author could check boxes 1–3 from this round's evidence; I do not write `[x]` (promotion is operator-owned); noted for the operator.
