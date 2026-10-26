# chousa round 51 — verifier spot-check

author: hyaku closure (non-author integrator, @m_sonnet)
date: 2026-10-25
lane tip measured: `a84edcf960caec156251e5d9843afecf9ad870f4` (before: `9ec1751a24231e899ceea4688e21c8edf6046d35`)
inputs: fleet report `.ufo/reports/round-51/chousa.md`; prompt `.ufo/prompts/chousa-round-51.md`
driver lines (`.ufo/watchdog.log`): `2026-10-25T19:46:38-03:00 launch chousa round=51 pgid=3405295 driver=hyaku-inline attempt=1` · `2026-10-25T21:38:49-03:00 complete chousa round=51; hyaku-inline attempt=1`

All measurements below were run by the closure over committed bytes: `git archive` exports of the tip (`/tmp/r51chk`) and of the base (`/tmp/r51base`), plus my own scratch packages, plus the lane's read-only on-disk captures under `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache` (key = first 24 hex of sha256 of the URL, confirmed for the PRISMA-S DOI and the NIPH `.docx`). No lane gate counter (`c1-count.py`, `c2-count.py`, `c3-count.py`, `c1-supplement.py`) was executed; their committed receipts were read. The lane's tool `tools/assimilate-rows.py` was run as a capability on inputs I wrote.

## 1. Step-1 conformance

| check | command | observed |
|---|---|---|
| report committed by lane identity | `git log --format='%an %H %cI' -- .ufo/reports/round-51/chousa.md` (fleet repo) | `chousa-shokunin c7d8d09f938d53546fb6992d588b049b81d2809a 2026-10-25T21:37:52-03:00` (before the 21:38:49 complete line) — ok |
| SHONEN heading, one line per box | `grep -c '^## SHONEN'`; `grep -c '^- \[' SHONEN.md` | heading once; 4 boxes, 4 lines, all `[~]` with pointers — ok |
| every cited lane commit exists and is an ancestor of the branch | `git merge-base --is-ancestor <h> master` for `d603f6f0 2a3389da cf642c66 75a9406a cfe6c9fb 4436e279 72566c84 41b4dca8 871c0d79 a84edcf9` | all ten `anc` |
| pushed, no leftovers | `jj-lane.sh state` → `local=a84edcf9… remote=a84edcf9… ahead=0 behind=0 tracked=0 untracked=0`; `git status --porcelain` in lane → empty | ok |
| prompt carries template contract | grep of `.ufo/prompts/chousa-round-51.md` (501 lines): §1 MISSION/AXES binding, §2 claims 1–3, §2b frontier step, §3 L2 floor, §4 report contract incl. SHONEN and marker rule, §5 commit/push scope/L0, §6 hyaku addendum | ok |
| append-only files | `git diff 9ec1751a a84edcf9 -- SCORECARD.md` | one hunk `@@ -2618,3 +2618,43 @@`: 40 insertions, 0 deletions; four `correction:` lines, verdict, capability row and round-52 plan — ok |
| wave seats | `ls .ufo/waves/round-51/w1` / `w2` (lane repo, committed); `git ls-files` | w1 49 files (48 reports + 1 extra), w2 43 files (41 seats + two `-2` resumed reports) — 89 seats, above the 64 floor |
| marker rule | real committed work, three claims with counters, 10 lane commits | not a marker; status `ok` |

Defects (status-neutral): none new beyond those the lane itself names (below). The report says "unchanged pending closure" for discernment; that is a closure input, not a defect.

## 2. Per-claim re-check

### R51-C1 operability — `tools/assimilate-rows.py` cites only header `source:` ids (re-measured by a plain run; counter evidence-verified)

| leg | command | observed |
|---|---|---|
| base behaviour, my own package (3 staged rows S301–S303; entry cites only S301 in its header, mentions S302/S303 in the body; registry max S055) | `python3 /tmp/r51base/tools/assimilate-rows.py --staged st.md --knowledge k --registry reg.md --opened 2026-10-25 --out outb --entry corpus/knowledge/e1.md` | `CITED=3 APPEND=2 HELD=1`; renumber.tsv maps S301→S056, S302→S057, S303→S040 held (the body-only ids ARE renumbered — the defect) |
| tip behaviour, same package | same command with `/tmp/r51chk/tools/assimilate-rows.py` | `CITED=1 APPEND=1 HELD=0 BODYONLY=2`; renumber.tsv only S301→S056; entry text `Alpha (S056); … (S302); old (S303)` (body-only ids unchanged); `bodyonly.tsv` lists S302 and S303; append.md 1 row |
| registry without `## Registry` heading | same, registry with the heading renamed (`reg2.md`), run at tip and at base | tip: `REFUSED registry has no \`## Registry\` heading` and `REFUSED registry rows outside the Registry section: S040, S055`, `rc=1`, no renumber.tsv / append.md written; base: `rc=0`, `APPEND=3`, ids restart at S001 (S301→S001, S302→S002, S303→S003) — silently wrong numbering over the existing S040/S055 rows |
| default self-test at tip | `python3 tools/assimilate-rows.py --selftest` | `FIXTURES_SHA256=3b7ad258…`, `SELFTEST=PASS findings=27 expected=27` |
| round-50 pinned fixture, legacy reading | `--selftest --cites all --fixtures corpus/evidence/round50/c1-fixtures --expected …/expected.json` | `FIXTURES_SHA256=c5c56480…` (equals the round-50 pin), `SELFTEST=PASS findings=26 expected=26` |
| tool digest vs receipt pin | `sha256sum tools/assimilate-rows.py`; `git diff --stat 41b4dca8 a84edcf9 -- tools` | `10af959b2b87dad565717b84e68733caab6cb7a940d68fb1c52fca793d4c86f4` equals `measure-after.txt` header `tool-rev: 41b4dca8… digest: sha256:10af959b…`; tools/ unchanged after 41b4dca8 |
| committed gate evidence | `corpus/evidence/round51/measure-after.txt`, `controls/c1-lane-before.txt`, `controls/c1-before.txt`, `c1-supplement-controls.txt`, SKILL.md Gates rows | frozen counter `LEGS=5/5 C1=PASS` (also `--seed 7`), supplement `SUPPLEMENT_LEGS=10/10`; lane tool at base `LEGS=1/5`; controls ≤2/5; the supplement fails the lane's own dirname forge 1/10 |

Re-measured: base vs tip behaviour on an independent nonce package, refusal, default self-test, round-50 pin. Evidence-verified only: the counter tallies, the do-nothing controls, the forge and the supplement. The lane discloses that the frozen counter is forgeable and that the supplement is post-freeze and does not stop a tool that reimplements the adopter; I agree and grade **improved**, narrowly stated. Side effect named by the lane, not harm: the round-49/50 one-shot counters fail or need `ASSIMILATE_CITES=all` at the new default (they were declared one-shot).

### R51-C2 depth — Japanese/Chinese search record, three entries on six documents (re-measured)

| leg | command | observed |
|---|---|---|
| SOURCES rows before → after | `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` on base and tip exports | 106 → 112 (S107–S112); matches the report |
| theme absent at base | the report's `git grep -l -e 検索式 -e 検索期間 -e 检索策略 9ec1751a… -- corpus/knowledge` | nothing at base; the three new entries hold them at the tip |
| all 70 manifest quotes located | python over `corpus/evidence/round51/spans.tsv`: capture found by its sha256 in the qcache, quote counted in that `.txt` read as UTF-8, quote present in the citing entry, ≤25 whitespace words | `70 quotes 0 bad` — each occurs exactly once in its sha-matched capture and in its entry; none exceeds 25 words |
| census | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` | exit 0, `ok`, five pre-existing W04 (S051 S053 S073 S074 S075) only — matches the report |
| committed gate evidence | `measure-after.txt` (receipt), `c2-before.txt`, `c2-controls.txt` | `ENTRIES=0/3 BOUND=0/7 C2=FAIL` → `ENTRIES=3/3 BOUND=6/7 REFUSED=1 QUOTE_ROWS=70 CAPTURE_BOUND=70/70 ANCHOR_BOUND=6/6 INFERENCE_GROUNDED=3/3 QUARANTINE_VERDICTS=6/6 C2=PASS` |

Re-measured: rows, theme absence, all 70 quotes, census, plus the §3 spot-checks. Evidence-verified only: the C2 counter's control scores and the wave-2 entailment sweep. The counter measures presence and binding, not entailment (disclosed; 30+ prose overstatements were narrowed in the lane); my sampled entailment checks in §3 found no overstatement. Grade **improved**.

### R51-C3 calibration — every repo-path pointer in SCORECARD capability rows and SHONEN evidence lines resolves (re-measured with my own extractor)

| leg | command | observed |
|---|---|---|
| base | my script `/tmp/r51_c3.py /tmp/r51base` (same pointer definition as the claim: backtick spans in `## Capabilities` third cells and indented SHONEN lines; resolves = non-empty file/dir, or a `correction:` line) | `rows 36 pointers 74 dangling 5` — SCORECARD:1843 `measure/final/`, :2073 `measure-l1/c1-s36361.json`, :2074 `measure-l1/c2-s36371.json`, :2616 `c1-supplement.py`, SHONEN:10 `round25-meta-differential.log` |
| tip | `/tmp/r51_c3.py /tmp/r51chk` | `rows 37 pointers 77 dangling 0` (neither count below base) |
| repair form | `git diff 9ec1751a a84edcf9 -- SHONEN.md` | the only SHONEN change is `round25-meta-differential.log` → `corpus/evidence/round25-meta-differential.log` on the evidence line; no `[x]` written; four append-only `correction:` lines in SCORECARD |

Re-measured. The lane's disclosed limit holds: existence, not truth. Grade **improved**, narrowly.

## 3. Axis verdicts

| axis | verdict | evidence |
|---|---|---|
| operability | improved | C1: base tool renumbers body-only ids and restarts ids at S001 on a registry with no heading; tip cites header ids only, refuses that registry, self-tests 27/27 and keeps the round-50 pin (26/26, digest c5c56480) |
| depth | improved | C2: three entries, 70 located quotes all single-occurrence in sha-matched captures |
| coverage | improved | theme absent at base; six documents (three JA, three ZH) now |
| calibration | improved | C3: 5 dangling pointers → 0 by my own count; limits disclosed; the wave-2 narrowings of the round's own prose |
| freshness | unchanged | no fetch; newest capture 2026-10-24; SOURCES rows are first-open of existing captures |
| adjacency | unchanged | the lane's two connector seats report no sibling overlap; not independently re-read by the closure, so I carry the lane's reading without upgrading it |

No axis harmed: SCORECARD diff is append-only; prior rows untouched.

## 4. Discernment spot-check

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| `chinese-search-record-r39.md` S109 `灰色文献的检索与记录` | admit | qcache `fd468a36d78ff156b6200946.txt` (sha256 of the S109 URL) | agree | occurs once, at char 15310, `（3）灰色文献的检索与记录`; matches the entry and the lesson |
| `chinese-search-record-r39.md` S111 comment-only `学科分类号` | admit as narrowed (field not claimed as rendered) | `42bac8830527d6f1bb125c49.txt` and `.raw` | agree | `.txt` holds 0 occurrences of `学科分类号`; `.raw` holds one, at char 8997, inside an HTML comment (`<!--`), so the entry's "not rendered" framing is correct and the S114 quarantine verdict `absent-as-written` is right |
| `japanese-search-record-r38.md` S107 char 10234 and page footer | admit as narrowed (p.122 not staged p.121) | `7194acc65a18f6555e4b8893.txt` | agree | the sentence occurs once, at 10234; the page's footer `121` sits at char 10178, i.e. before it, and the next footer is `122 日健教誌 第 32 巻 第 2 号` at 13787, so the sentence is on the page whose footer reads 122; the lane's correction is right |
| `search-log-fields-r36.md` | **reject** (refuse) | PRISMA-S DOI capture `01f657b3d0ab045c494b3f92.txt` | agree | key = sha256(`https://doi.org/10.1186/s13643-020-01542-z`)[:24]; the file is 265 characters of `Client Challenge`; the quoted `copied and pasted exactly as run` and `guide reporting, not conduct` occur in no `.txt` in the cache (0 files) — the entry's central authority is not on disk |
| NIPH `.docx` (staged S125) | **refuse** (capture form) | `3a8b45977cd111e45e3980a5.txt` / `.raw` | agree, with a note | `.txt` is 168952 characters with 72117 U+FFFD and 0 occurrences of `検索`; `.raw` unzips to `word/document.xml` whose `w:t` text (18478 characters) holds `SRにおける文献検索期間について明記する` once. So the source is readable; the refusal rests on the frozen span form, as the lesson says ("for capture form, not source quality"), with a stated flip — a decision I accept as honest and reversible, not a source rejection |
| SOURCES row S107 (newly written) | admit | S107 row, `7194acc6….txt` | agree | row headline quote `その日時，使用した検索式を同時に記録しておく` is one run (20 characters), located once at char 10234; offsets in the row's anchor cell match the manifest |
| SOURCES rows S108–S112 | admit | qcache keys from `spans.tsv` | agree | every manifest quote of each row passes the §2 C2 sweep (70/70); S111 is tier B with an explicit "not the item text" scope, appropriately weak |
| quarantine slice (six register rows) | `payload-absent`, none blocking a bound document | register S114 (the `学科分类号` row) via the S111 capture `.raw` | agree for that one row; the other five not re-opened | the register's `R-05;R-37;R348.3;R916.3` is in the raw HTML only inside a comment, so `absent-as-written` is right |

Eight items listed; seven re-opened in full and agree (one with a note); the quarantine slice is re-opened for one of six rows and agrees. No source I re-opened contradicts the lane's decisions.

## 5. Trend verdicts

- **expansion — improved.** SOURCES 106 → 112 and six documents on previously unheld ground; one document refused on form, not counted.
- **quality — improved.** The lane's wave-2 narrowings are visible in the entries (the S107 page, S111 field status, S109 表1 note), and the two tool defects (cites, registry structure) are fixed and self-tested; the C1/C3 counters' weaknesses are reported, not hidden.
- **discernment — improved.** Non-author re-opening agrees on every sampled admit and reject (8/8); the refusal of a challenge-page capture and the correction of the staged page number were both right and checkable from bytes.

## 6. Routed defects and notes for the lane

1. **Frozen C1 counter forgeable** (lane's own finding): make the next counter nonce-only with no fixed directory names, or fold the supplement's random-name legs into the frozen counter before any claim cites it.
2. **Adopter twin-id `held` label and refusal ordering** (named open defects in the report; wave-2 F5/F6): fix with a self-test row each.
3. **NIPH `.docx` refusal** is a capture-form refusal; the source is readable from `.raw` (`word/document.xml`). A zip-member form in the span builder and counter is the lane's own flip; do it before refusing a `.docx` again.
4. **C3 reads corrections in any order and only for SCORECARD rows**; pointers to files that exist but do not show the behaviour pass. Add a content-anchor check, not just existence.
5. **Round-49/50 one-shot counters** fail at the new default unless `ASSIMILATE_CITES=all`; the SKILL Gates row should say so next to them.
6. Status-neutral: one W1 seat wrote `corpus/evidence/round51/zero.txt` into the lane through a symlinked scratch root (removed, disclosed).

SHONEN boxes: all four are `[~]`; the evidence pointers resolve, but the Province-fit and cross-domain-bleed boxes rest mainly on lane-dispatched reviewers. Nothing here is a `[x]` I assert; promotion is operator-owned.
