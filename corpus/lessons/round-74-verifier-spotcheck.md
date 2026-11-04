# Round 74 verifier spot-check — chousa

author: hyaku closure (non-author integrator, @m_zfl)

Reviewed round landing `5f754bd12ec5d0d006ca05751250d5ee1caaf29e`, before `8a28732b3c1591b52449a982849b758cda6f4c45`; instrument freeze `1eaa30ad248bbd3bd7469b2c17295fcda5fc02bb`. This review neither improves the authored round nor re-admits r73.

## Conformance and disposition

Status **ok**: a real, landed report with checkable work, not a marker. Admission **false**, `rejected-honest-stop`: the narrow C1 predicate is met, but QUALITY 126's required prefreeze detection-forger evidence is absent. This is a quality-bar honest rejection, not a failed conjunct or a harmed axis.

- `git log --format='%an %H' -- .ufo/reports/round-74/chousa.md` in the fleet returned `chousa-shokunin 664dc11222b43d9e414844895664e948b68e4ddd`. Report has `## SHONEN` and four `[~]` assessment rows. Lane integration committed at 12:33:18-03:00; report committed at 12:34:40-03:00, after the lane work.
- `jj-lane.sh state /home/vgpnk/Projects/shokunin/chousa-shokunin` returned `branch=master local=5f754bd12ec5d0d006ca05751250d5ee1caaf29e remote=5f754bd12ec5d0d006ca05751250d5ee1caaf29e ahead=0 behind=0 head=detached tracked=0 untracked=0`. `git status --porcelain` returned no output before this verifier file was written.
- `git merge-base --is-ancestor HASH master` succeeded (exit 0) for freeze, landing, before, and the historical base `f748abbb6bf58388e732facd4ecec5612419c457` and target `5aec90775fc7cc1fe9ad442e0d5491731323eec1`. Ancestry tested against branch `master`, not detached HEAD or upstream syntax.
- Dispatched `.ufo/prompts/chousa-round-74.md` is committed (`7783967df8fb401fcc46ad9e82b858fc1b958eca`), and carries mission/axes, 1–3 claims, L2 floor, report path/sections/SHONEN, hash citations, commit-before-report, write/push scope and L0 channel. Campaign amendments and the L1 planner substitution are explicit. Settled `w1-results.json` carries ten seats, four attack roles; no promotion authority is assigned to those author-lane seats.
- Durable driver digest: `2026-11-04T12:15:32-03:00 launch chousa round=74 pgid=4138930 driver=hyaku-inline attempt=1`; `2026-11-04T12:34:55-03:00 complete chousa round=74; hyaku-inline attempt=1`.

## C1 re-check: observations versus binding admission

No sibling gate or selftest was executed. Under PROTOCOL Gate standard, its numerical outcomes below are **committed-evidence verified**, not fresh gate runs. The closure judge independently ran plain Git/regex/hash measurements on committed bytes. Read-only reviewer seats Chousa74GateReview and Chousa74SourceReview supplement, not replace, this review.

Measurement commands used Python's `subprocess.check_output(['git','-C',LANE,'show',REV+':'+PATH])` to obtain exact committed blobs; regular expressions counted anchored rows/cases, and `hashlib.sha256(blob).hexdigest()` computed digests. The following are observed results, not quotations from the report alone:

| re-check | command / committed input | observed output |
|---|---|---|
| Public-path selftest before/positive/after | Count `^CASE (\\S+) (PASS\|FAIL)` in `corpus/evidence/round74/{before-matrix,positive-matrix,after-matrix}.txt` at landing | nine cases each; PASS/FAIL = 3/6, 9/0, 9/0; summary 3/9 exit 1 → 9/9 exit 0 |
| Historical frozen run | Open `before-historical.txt`, `after-historical.txt` at landing | `C2=FAIL checks=6/7`, EXIT=1 → `C2=PASS checks=7/7`, EXIT=0; both name instrument freeze and the same historical base/target |
| Independent real historical edits | `git diff --numstat f748abbb6bf58388e732facd4ecec5612419c457 5aec90775fc7cc1fe9ad442e0d5491731323eec1 -- LOG.md corpus/lessons/round-72.md SCORECARD.md` | LOG 11 additions/0 deletions; SCORECARD 21/0; lesson 6/0 — the original loader's addition-as-deletion result is wrong |
| Instrument identity | SHA256 of frozen and landing `correction-count.py` | both `9334721a5e7a4080255b478771bf5443739738fb1936b40c116da28d7fa8ac41`, equal to receipts |
| Actual repair | Compare `landing:corpus/evidence/round73/c2-count.py` to `landing:corpus/evidence/round74/correction-count.py` | functional delta line 131: `parts[0]` → `parts[1]`, nonnumeric fallback `0` → `1`; title/mode change only otherwise; Python-invoked command unaffected by executable mode |
| Missing prefreeze admission evidence | `git ls-tree -r --name-only 1eaa30ad248bbd3bd7469b2c17295fcda5fc02bb -- corpus/evidence/round74` plus frozen QUALITY 126 and claims | only claims, matrix, successor, before and positive receipts; no qualifying detection-forger battery. Matrix invokes candidate via subprocess |
| Adversarial limitations | Open committed `R74Critic/forge-order-oracle.log` and mutation logs beneath lane `.ufo/waves/round-74/w1/` | oracle 9/9 exit 0 with its distinct digest; reversion 3/9 and zero-deletions 5/9, both killed |

The public-path matrix has persisted independent expectations for unchanged, three appends, three deletions, equal replacement and receipt change, and compares exits and failed check IDs. Both C1 conjuncts are met on the reviewed implementation. However, a digest establishes implementation identity, not discrimination against a forger; the order oracle reads no sources and still scores 9/9. QUALITY 126 was already present before freeze and prohibits binding a candidate-running counter without the committed prefreeze battery. The lane disclosed that omission and withheld admission: that boundary is upheld. No post-data remedy, universal robustness, nonnumeric/binary certification, semantic entailment, or calibration gain is inferred. Historical r73 rejection stands.

## Axis verdicts

`git diff 8a28732b3c1591b52449a982849b758cda6f4c45 5f754bd12ec5d0d006ca05751250d5ee1caaf29e -- SCORECARD.md` shows twelve appended lines, no old score changes or new capability row. Spot reads of claim, lesson, registry and source delta show no harmed axis.

| axis | verdict | scope |
|---|---|---|
| operability | improved | Narrow runnable numeric-loader evidence only; C1 predicate met. Numeric score remains historical 3/10, delta 0; quality-bar admission withheld separately. |
| depth | unchanged | No depth claim or score move. |
| freshness | unchanged | No general freshness claim or score move. |
| calibration | unchanged | Inherited C2 label is not a new calibration claim; r73 remains rejected. |
| coverage | unchanged | No new coverage-map ground or knowledge entry. |
| adjacency | unchanged | No province expansion or sibling-domain absorption. |

## Independent discernment spot-check

Reopened both source files and checked their exact committed blobs at the source pin; each is byte-identical at the round landing. The registry rows S182/S183 and lesson Gate were also reopened.

| item | decision | re-opened source | agreement | reason |
|---|---|---|---|---|
| S182 | admit, B/mined scoped to routed loader defect | `8a28732b3c1591b52449a982849b758cda6f4c45:corpus/lessons/round-73-verifier-spotcheck.md:67`, section 5 item 1 | agree | Explicitly identifies addition/deletion inversion and requires real committed append/deletion exercises through load. This supports those controls, not arbitrary prose truth. |
| S183 | reject, C scoped to helper selftest as loader certification | same pin, `corpus/evidence/round73/c2-count.py:125–134,162–179` | agree | `selftest()` calls `check()` directly with in-memory dictionaries and never exercises the defective Git loader. Successor controls do not erase this historical rejection. |

Located S182 quote “Before any successor calibration freeze, exercise a real committed append and a real deletion through `load()`” is verbatim (16 whitespace tokens, ≤25). S183 quote `base = check({k: v for k, v in FIXTURE.items()}, {}, set())` is verbatim at line 163 (11 whitespace tokens, ≤25). The lesson's parenthetical 18/13 counts are inaccurate; quotes themselves and limits pass. Route that minor count correction append-only, not by rewriting the authored lesson.

Own row measurement over `git show REV:corpus/SOURCES.md`, regex `^ {0,3}\\|\\s*S\\d{3,}\\s*\\|`, gives before→after **181→183**; tiers A123/B45/C13→A123/B46/C14; statuses mined147/queued19/rejected15→mined148/queued19/rejected16. All first 181 row bytes remain identical.

Ran `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`: exit 0, `chousa ok .../corpus/SOURCES.md`; only existing W04 cross-scope duplicate-URL warnings S051, S053, S073, S074, S075. No new error.

## Learning trends

| trend | verdict | evidence |
|---|---|---|
| expansion | unchanged | Registry +2 is curation, not new knowledge/capability/coverage. |
| quality | improved | Numeric loader repair strengthens known work and the surviving forge is explicitly marked, never certified sound; bounded improvement does not waive QUALITY 126. |
| discernment | improved | This independent spot-check agrees with both admit and reject; prior loader disagreement yields grounded QUALITY 134 and the real red-before receipt. |

## Routed defects / operator notes

1. **Owner chousa — admission debt:** before any future successor binds a candidate-running counter, meet existing QUALITY 126 with committed prefreeze detection-forger controls and record limits; address the surviving order oracle rather than treating digest identity as a kill. Never amend this frozen matrix or re-admit this round from a later result.
2. **Owner chousa — minor corpus count defect:** append a correction to the lesson's quoted-word counts (16/11 whitespace tokens, not 18/13). No quote absence or source disagreement; status-neutral.
3. **Carried operator questions:** external-fetch approval, historical Windows flock/load questions, promotion and non-author entailment review remain unanswered. SHONEN boxes look checkable by a separately scheduled non-author promotion review, not checked by this closure; promotion remains operator-owned. No capability added, no mint/promotion.
4. General robustness, binary/nonnumeric coverage and semantic verification remain disclosed limits, not newly claimed fixes. No tool installs/updates. No gate execution, network fetch or lane-authored-file edits by this judge.

Self-evaluation: accuracy 4/5 (gate outcomes necessarily evidence-verified, not rerun); completeness 4/5 (promotion intentionally not in scope); clarity 4/5 (three-layer predicate/axis/admission distinction is essential); actionability 4/5 (future freeze debt remains lane-owned); conciseness 4/5 (audit commands retained for replay). Overall 4.0; key improvement is to preserve narrow evidence separately from admission, as done here.
