# Round 78 verifier spot-check — chousa (closure)

author: hyaku closure (non-author integrator, @m_zfl)

Closed 2026-11-05T00:00:49Z against lane tip `3eb4a3cad8febf75698a017cb6c4441f763b3454` (branch
`master`, local == remote, `ahead=0 behind=0`), base `53dbd512d0ab70055338cb44898a6db70049537f`,
prefreeze controls `93e0432eb5bb9c4492d540bc6a6358ed3f8d4392`, claims freeze
`01b444b7f8d90785515e77c7ba9db5d63361329b`. Report: `.ufo/reports/round-78/chousa.md`, committed in
the fleet repo by the lane identity (`chousa-shokunin`, fleet commit
`e564246d733c6233b3e7ec6f07237730fb09838d`). Dispatch digest copied from the mutable
`.ufo/watchdog.log`: `2026-11-04T19:39:07-03:00 launch chousa round=78 pgid=3792375
driver=hyaku-inline attempt=1`; `2026-11-04T20:38:12-03:00 complete chousa round=78; hyaku-inline
attempt=1`. Both lines verified present in the live log (lines 2542 and 2570 at read time).

This closure is non-author: it wrote nothing in the lane except this file. No sibling gate or
self-test was executed; under PROTOCOL §Gate standard (Closure consequence) every lane-owned verdict
below is **committed-evidence verified**, and the before→after deltas are re-derived by plain
git/grep/sha256/regex measurements over committed bytes that this closure ran itself.

## 1. Conformance (step 1)

| check | command | observed | result |
|---|---|---|---|
| lane pushed, nothing outstanding | `scripts/hyaku/jj-lane.sh state <lane>` | `branch=master local=3eb4a3ca… remote=3eb4a3ca… ahead=0 behind=0 head=detached tracked=0 untracked=0` | PASS |
| no uncommitted round work | `git -C <lane> status --porcelain` | empty, rc 0 | PASS |
| report authored by the lane identity | `git -C <fleet> log --format='%an %H' -- .ufo/reports/round-78/chousa.md` | `chousa-shokunin e564246d733c6233b3e7ec6f07237730fb09838d` | PASS |
| report is pushed in the fleet repo | `git branch -r --contains e564246d…` | contained in `origin/main` and `origin/master` | PASS |
| `SHONEN` heading, one line per box | `grep -c '^## SHONEN'` / `grep -cE '^- \`\[~\]\`'` on the report; `git show <tip>:SHONEN.md \| grep -cE '^- \[[ x~]\]'` | heading 1; four `[~]` lines; SHONEN.md holds four boxes | PASS |
| cited commits exist and are ancestors of the branch ref | `git cat-file -e <h>^{commit}` + `git merge-base --is-ancestor <h> master` for base, controls, freeze, landing | four of four `exists=yes ancestor=yes` (tested against `master`, never `@{u}`; HEAD is detached) | PASS |
| report sections, in order | `grep -nE '^## (Work performed\|Landed changes\|Before → after measurements\|Sources & frontier\|Trend verdicts\|SHONEN)'` | lines 11, 93, 101, 141, 161, 179 — all six present, template order | PASS |
| prompt carries the template contract | rendered `templates/round-prompt.md` with the chousa substitutions (`chousa`, `78`, fleet root, lane axes, `chousa-shokunin`) compared to `.ufo/prompts/chousa-round-78.md` | the rendered template is a **byte prefix** of the dispatched prompt (8 408 chars, `startswith` true); §6 hyaku addendum follows it | PASS |
| L2 floor and round band | `w1-spec.json` `items`, `w1-dispatch.json` `counts`, policy block | 12 seats in one v1 wave; `counts {"spawn":12,"resume":0,"total":12}`; policy `waveMinLanes=8 waveMaxLanes=16`; roles executor 3, reviewer 2, critic 2, scout 1, scribe 1, connector 1, mutation-tester 1, sentinel 1 → attack 5/12 = 41.7 % | PASS |
| godspeed lead on every seat | `sum(prompt.lstrip().startswith('/skill:godspeed'))` over the spec items | 12/12 | PASS |
| report lands after the lane commit | report committer date `20:37:48-0300` vs landing committer date `20:36:34-0300`; watchdog `complete` 20:38:12; the filed bytes cite `3eb4a3ca…` twice | report commit is later than the landing commit and earlier than the driver's completion line | PASS |

Defects and observations (all status-neutral; none is a marker predicate):

- **D1 — an unresolvable self-pointer.** Report line 7 says "report commit named at the end"; the
  report never names it (`grep -c e564246d` on the filed bytes → 0; the only 40-hex tokens are
  `53dbd512…`, `93e0432e…`, `01b444b7…`, `3eb4a3ca…`). A report cannot name its own commit without
  an erratum, so the sentence should have been dropped, not promised.
- **O1 — timestamp inversion, not a filing-order defect.** The prefreeze commit's jj *author*
  timestamp is `19:38:10-0300`, 57 s before the driver's `launch` line (`19:39:07`), while its
  committer timestamp is `19:55:19`; the prompt file itself was committed at `19:39:05`, two seconds
  before the launch line. Read together this is the run-15 inline handoff logging the launch line
  after the spawn returns, plus jj preserving the author timestamp across rewrites. No work is
  claimed before the prompt existed.
- **O2 — the wave context promises a trailer no item carries.** `w1-spec.json.context` states "Every
  `Report:` trailer path is relative to …", but no item prompt contains a `Report:` line (4/12
  mention the word only in prose). Four seats (`R78ExecA`, `R78CriticA`, `R78CriticB`, `R78ScribeA`)
  filed no seat report; the report discloses all four and names the seats that cover their items.
  Routed below as a spec defect, not a lane defect.

## 2. Claim re-checks (step 2)

Two claims, frozen in `corpus/evidence/round78/claims.md` before any seat scored. Both frozen
predicate lines hold on the committed bytes; **both frozen kill rules fired**, and the lane says so
in its report, its LOG entry, its SCORECARD verdict block and its lesson. I re-derived each
before→after myself and re-read each kill-rule receipt.

### Instrument identity (my own measurement, `git show <rev>:<path> | sha256sum`)

| instrument | freeze `01b444b7` | landing `3eb4a3ca` | claims.md |
|---|---|---|---|
| `corpus/evidence/round78/matrix-battery-v5.py` | `5545a4718690a80e…032b5af0` | same | same |
| `corpus/evidence/round78/forge-battery.py` | `ba98db41e0c82ba0…1f1c5143` | same | same |
| `corpus/evidence/round78/work-contract.py` | `e51d8917afd1c202…3d87ffa8a0` | same | same |
| `corpus/evidence/round78/selfcheck.py` | `f5acdd825ab7dcaf…2837bf9af` | same | same |
| `corpus/evidence/round77/matrix-battery-v4.py` (the superseded subject, at `53dbd512`) | — | `155fafb16b693144…25f106a3d` | same |

No instrument moved between the freeze and the landing; the frozen set is the landed set.

### C1 — operability (lowest scored non-retired axis; the historical numeric 3/10 held)

Mechanism delta re-derived from committed bytes (plain `grep -n`):

| property | v4 at `53dbd512` | v5 at `3eb4a3ca` |
|---|---|---|
| answer key | `:181 print(f"{label} ORDER {i} " + hashlib.sha256(…)` unconditional | `:231` guarded by `print_order`; flag only at `:271` (`--print-order`, "comparison only"); default run emits none |
| subject identity | `:169 target.write_bytes(source.read_bytes() + f"\n# salt {secrets.token_hex(8)}\n")` — a strippable suffix | `salted_copy()` inserts an inert statement (`import os as _r78<hex>` or `_r78<hex> = <int>`) above a random top-level statement |
| verdict receipt | no trailer (`grep -c RECEIPT_LINES` → 0) | `:329 emit(f"RECEIPT_LINES={_LINES + 2}")`; per-subject lines buffered and flushed after the scoring loop (`for line in buffered: emit(line)`) — the quiet leg |

Default-run output re-read from a committed seat receipt, not re-executed:
`R78ReviewA/predicate-rerun.stdout` → `grep -c ORDER` **0**; tail `FORGE_BATTERY=PASS
forgers_handled=4/4 positive=1/1`.

Receipts (evidence-verified, §Gate standard):

| side | receipt | observed |
|---|---|---|
| before (`53dbd512`, v4 `155fafb1…`) | `corpus/evidence/round78/controls/forge-battery-before-v4.txt` | `FORGE_BATTERY=FAIL forgers_handled=0/4 positive=1/1`, `# exit: 1`; every forger row `trailer=no integrity=n/a verdict=FORGED` |
| after (v5 `5545a471…`) | `corpus/evidence/round78/controls/forge-battery-after-v5.txt` | `FORGE_BATTERY=PASS forgers_handled=4/4 positive=1/1`, `# exit: 0`; a1/a2/a7 REFUSED, a5d DETECTED (`integrity=BAD`), positive ACCEPTED |
| supporting repair | `controls/work-contract-before-v4.txt` → `-after-v5.txt` | `WORK_CONTRACT=FAIL survived=no unwritable_exit=1 file_exit=1` exit 1 → `WORK_CONTRACT=PASS survived=yes unwritable_exit=2 file_exit=2` exit 0 |

**Kill rule fired — verified from the receipt and from the forger's committed source.**
`R78L1/a8-normalizer-v5.txt` reaches `BATTERY=PASS forgers_rejected=11/11 positive=2/2
oracle=REJECTED` at `# exit: 0`; the same line is reached in `R78ExecC/v5.stdout.txt` and
`R78ReviewA/v5-vs-a9-receipt.txt`. The forger is what it says it is: `R78L1/a8-normalizer.py`
deletes the salt family with a two-alternative regex, hashes the remainder, and classifies the
subject against a hard-coded two-element `POSITIVE_SHA` set while printing a fabricated twelve-line
contract table — its own docstring says "Scores nothing." C1's frozen kill rule names exactly that
event as falsifying the claim, so **C1 does not verify as written**; the claim's target sentence and
its kill rule contradict each other (`R78ReviewA` finding 1, carried as QUALITY 147).

Do-nothing control: at the base the only battery on disk is v4, whose receipt is `handled=0/4` at
exit 1, so a do-nothing round cannot reach the target. Strictly, the harness itself is round-78
work, so the control bounds the target, not the harness.

### C2 — calibration (sourced on S193/S194)

I re-implemented the three classes with plain reads over committed bytes (no execution of the
lane's counter), then compared with the committed receipts.

| class | base `53dbd512` | landing `3eb4a3ca` |
|---|---|---|
| S1 registry cell parity | header 8 cells, row 168 **7** cells, corrections `[132]` → unresolved `[168]` | row 168 still 7 cells (append-only), correction `SKILL.md:168` present naming the owner `chousa`; successor row 169 has 8 cells; corrections `[132,168]` → unresolved `[]` |
| S2 QUALITY pointers | `committed path matching '02c-work-unwritable'` → **[]** (criterion 142 cites `receipts/02c-work-unwritable.*`, nothing on disk) | audited window `[144,145,146,147,148]`, `missing pointers {}`, `superseders {142: [144, 146]}` → unresolved `[]` |
| S3 stranded `## Mistakes` row | `stranded [73]`, `errata []` → unresolved `[73]` | `stranded [73]` (filed bytes untouched), `errata [73]` naming line 73 → unresolved `[]` |

So the axis state moved **3/3 unresolved → 0/3 unresolved** by my own counting, and the committed
receipts say the same: `controls/selfcheck-before.txt` `SELFCHECK=FAIL unresolved=3/3` exit 1 at
`53dbd512`; `controls/selfcheck-after.txt` `SELFCHECK=PASS unresolved=0/3` exit 0 at `93e0432e`.
The repairs are truthful on inspection: QUALITY 144 opens `supersedes: 142`, the SKILL correction
line names row 168 and its missing cell, and the round-77 erratum names the stranded row at line 73.

**Kill rule fired — verified, and corroborated structurally from committed source.**
`R78ReviewB/ALL-three-hollow.txt` prints `SELFCHECK=PASS unresolved=0/3` at exit 0 on a mirror
carrying all three defects plus three hollow repair lines, with an honest control pair per class
(`ctrlA-defect-no-correction.txt`, `ctrlB-base-quality.txt`, `ctrlC-defect-no-erratum.txt`, each
`unresolved=1/3`, exit 1). That is not an accident of one probe: `selfcheck.py`'s resolution
regexes are `^correction: SKILL\.md:(\d+)`, `supersedes: (\d+)` and `erratum: round-77\.md:(\d+)`
— presence only, and the module docstring states "The counter is lexical: it proves presence,
position and reachability, not that a correction states the truth". `check_quality()`'s audit window
is the *last* `## Round-\d+ addition` block (the loop keeps overwriting `start`), which is exactly
`R78ReviewB/atkB2-new-block-window.txt`'s finding. C2's frozen kill rule names this as falsifying
the claim, so **C2 does not verify as written**; QUALITY 146 carries the successor requirement.

## 3. Discernment spot-check (step 3) — I am the named non-author reviewer

Sampled the round's `## Gate` decisions: two admits and one reject, each source re-opened at the
revision the row pins.

| item | gate decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S193 (own-work B) | admit, mined; grounds C2's S1 class | `git show 53dbd512:corpus/lessons/round-77-verifier-spotcheck.md`, line 156 of that blob (within the row's stated 156–160 span): "`SKILL.md` registry row `round77 order-and-content battery` is missing its owner cell." — verbatim modulo the surrounding bold markers and the list numeral; **11 words** | **agree** | the quote is on the stated line, inside the stated span, within the 25-word bound, and it grounds the class it is admitted for; the row's own caveat (a closure record is not independent truth that the successor repairs it) is the correct tier reading |
| S194 (own-work B) | admit, mined; grounds C1's target | `git show 53dbd512:corpus/QUALITY.md`, line 1046 = criterion 143: "An outer battery prints no invertible answer key, no strippable subject identity and no receipt a child can append to" — verbatim, cut at the semicolon; **20 words** | **agree** on the decision; the location label is imprecise (defect 11) | the line number, the quote and the word count all check out and the quote does ground C1's target; the row honestly scopes it as a requirement, not a measurement. But both the row and the lesson say "quote inside the Check sentence", and the quote is the criterion's **opening bold requirement** — the `Check before a successor freeze:` sentence sits later in the same line. A quote must name its location (`CORPUS.md`), so the label needs the successor's correction |
| S195 (own-work C) | reject, kept with reason and flip | `git show 93e0432e:corpus/evidence/round78/controls/forge-battery-after-v5.txt`, line 9: "FORGE_BATTERY=PASS forgers_handled=4/4 positive=1/1" — verbatim; the row states lines 1–12, quote on line 9 | **agree** | rejecting a receipt that prints the predicate as a *source about verification method* is the right taste call (it is the predicate's own evidence), the flip is actionable, and the tier C / status `rejected` combination is consistent with contract v1 |

Registry re-check (my own census, not the lane's): rows 192 at `53dbd512` → 195 at `3eb4a3ca`
(`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`), three rows appended and no existing
`status`/`recheck`/`used-by` cell touched (`git diff` shows three `+` rows only); malformed rows
`NF!=13` → **0**; duplicate ids → **none**; tiers B/B/C and statuses `mined`/`mined`/`rejected` as
reported. `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` re-run by
this closure → `EXIT=0`, the same five pre-existing `W04` duplicate-url warnings
(S051/S053/S073/S074/S075) and `ok` on `corpus/SOURCES.md`, byte-matching `census-end.txt`.

## 4. Axis and trend verdicts

`git diff --numstat 53dbd512 3eb4a3ca` over the owned surfaces: `LOG.md` 45/0, `SCORECARD.md` 54/0,
`SKILL.md` 3/0, `corpus/QUALITY.md` 12/0, `corpus/SOURCES.md` 3/0, `corpus/lessons/round-77.md` 9/0,
`corpus/lessons/round-78.md` 132/0 — every one append-only, no frozen sentence rewritten.
`PROVINCE.md`, `corpus/README.md` and `corpus/knowledge/` are untouched (0 files in the diff).

| axis | verdict | basis |
|---|---|---|
| operability (C1) | **improved** | measured, not asserted: the four round-77 channels go `handled=0/4` exit 1 → `handled=4/4` exit 0 on the same forged bytes, the answer key, the strippable salt and the appendable receipt are each gone from the committed v5 bytes, and the `--work` contract goes FAIL→PASS. The claim as written does not verify (its kill rule fired on the normalizer channel) and no numeric score moved — the historical 3/10 is held, so this is a narrow artifact delta, not a field-readiness claim |
| calibration (C2) | **improved** | the three routed self-assessment mismatches resolve, re-derived by this closure 3/3 → 0/3 over committed bytes (cell parity, pointer resolution, heading position). Scope is those three classes: the counter that was to certify them is falsified as non-discriminating, so the improvement rests on direct inspection, not on the lane's PASS line |
| depth | **unchanged** | no knowledge entry, no decision-table row, no domain fact; the registry gained a gate row and a correction line |
| freshness | **unchanged** | no drift pin added or re-verified beyond the instruments' own digests; `SOURCES.md` `recheck` cells all `on-release`, none advanced |
| coverage | **unchanged** | no province surface added; `PROVINCE.md` untouched |
| adjacency | **unchanged** | `R78ConnectorA` reports the sibling rows it compared (tsukuroi 90, kasegi R39, souji Q102, kama KQ112, mado 132) and absorbs none; no sibling file touched |

| trend | verdict | evidence |
|---|---|---|
| expansion | **unchanged** | no admitted `knowledge/` entry, no capability row (`SCORECARD.md` capabilities table untouched), no `corpus/README.md` or `PROVINCE.md` ground. The three registry rows are curation (two admits, one rejection), and a rejection is taste, not expansion |
| quality | **improved** | a weaker instrument is superseded by a stronger one on the same forged bytes (`0/4` → `4/4`), the positive control still passes, the `--work` contract defect is repaired with a failing-before receipt, and QUALITY 144–148 carry the requirements forward. Nothing is weakened: every change to a frozen artifact is append-only (numstat above), and the surviving normalizer channel is measured and recorded, never certified sound |
| discernment | **improved** | the round falsified both of its own frozen claims with honest control pairs (`R78L1`/`R78ExecC`/`R78ReviewA` for C1; `R78ReviewB` + three class controls for C2), mined three of its own defects with what caught each, and this closure's spot-check agrees on all three sampled gate decisions — an agreement on admits *and* a reject |

Round shape, frontier and stale-lane: one v1 wave of 12 seats (verified above), `## Mistakes` carries
three rows with evidence, control and fix, and C2 cites S193/S194 (sourced-claim requirement met).
The respawn-per-round driver has no other chousa mission open; the report's stale-lane section says
so and the watchdog shows a single launch/complete pair for round 78.

## 5. Routed defects (owner chousa, next round)

1. **C1's claim text and its kill rule contradict each other** (`R78ReviewA` finding 1). QUALITY 147
   carries the requirement; round 79 must restate the claim so the target sentence and the kill rule
   name the same event.
2. **`selfcheck.py`'s escape hatches are lexical** (`correction:` / `supersedes:` / `erratum:`
   presence only) and its QUALITY window is the newest block only. QUALITY 146 carries it; the
   counter is not admissible as a calibration certificate until it validates the bytes each line
   claims to repair.
3. **`forge-battery.py` maps a missing `cc` to exit 1 with a traceback** instead of its
   could-not-evaluate exit (`:110 subprocess.run(["cc", …])` with no handler; QUALITY 148,
   `R78SentinelA/battery.stderr`).
4. **`work-contract.py` never compares Case A's matrix exit.** Confirmed by this closure:
   `grep -n rc_a corpus/evidence/round78/work-contract.py` → only `:62` (assignment) and `:64`
   (print); a battery that refuses to run still passes Case A (`R78ConnectorA/receipts/wc-probe.out`).
5. **The round-78 registry row is registered as a gate with no `--selftest`.** `grep -ci
   'selftest|self-test'` over `matrix-battery-v5.py`, `forge-battery.py` and `selfcheck.py` → 0/0/0;
   the row's self-test cell names the twins and the forge battery, which §Gate standard (Self-test)
   treats as a helper. The round-77 routed defect 2 is therefore not visibly closed for the
   successor — the lane must either add an isolated-fixture self-invocation asserting a stable
   expected finding-id or state in the row why the forge battery satisfies the clause.
6. **`selfcheck.py` has no registry row at all** (only a prose mention inside the row-168 correction
   line), although it is a committed, re-runnable verdict script with a 0/1 map — a §Gate standard
   (Registry) gap at the lane's registry home.
7. **Freeze-check drift, not a wave defect.** `python3 tools/freeze-check.py` on the round-78 pair
   reports `FAILED_CHECKS=CONTEXT_DIGEST,DIGEST_STRAY,BODY_RENDER`; `CONTEXT_DIGEST` and
   `BODY_RENDER` fail identically on the round-77 pair with the same tool, and `DIGEST_STRAY` is the
   two deliberately cited public positive digests. The gate has drifted behind the current
   `ufo-swarm-wave.mjs` renderer; the lane routed it rather than repairing after dispatch, which is
   correct.
8. **Wave spec: the context promises a `Report:` trailer that no item carries** (O2), and 4/12 seats
   filed no report. Items should carry the trailer path the context names.
9. **Two "after" control receipts carry a revision label they were not measured at**
   (`controls/forge-battery-after-v5.txt` and `controls/work-contract-after-v5.txt` both print
   `# lane rev: 53dbd512… (controls)`). The receipts are frozen and must not be amended; the round
   already mined this as its third mistake and needs the successor rule in QUALITY.
10. **Carried instrument debt** (recorded, not repaired): the settle race (`--settle 0` prints 4/4
    before the a5d receipt is forged), the same-count in-place receipt rewrite, and the digest-keyed
    UUT battery that passes the harness. QUALITY 147 and the lesson carry them; round 79's planned
    row names them.
11. **S194's location label is wrong.** The row and the lesson say "quote inside the Check sentence";
    the quote is criterion 143's opening bold requirement and the `Check before a successor freeze:`
    sentence follows it on the same line (`git show 53dbd512:corpus/QUALITY.md | sed -n 1046p`). The
    line number, quote and word count are right, so the admit stands; `SOURCES.md` rows are
    append-only, so the correction is a new row whose `teaches` opens `supersedes S194 —`.

## 6. Operator note

The four `SHONEN` boxes look checkable by a non-author from committed artifacts (SKILL decision
tables and the gates registry for box 1; the round's end-to-end instrument work and `LOG.md` entry
for box 2; the pasteable commands and exit maps for box 3; the untouched `PROVINCE.md` plus
`R78ConnectorA`'s non-absorption for box 4). Promotion remains operator-owned; this closure wrote no
`[x]` anywhere.

**Closure ruling.** Lane status `ok` (a real report with checkable committed work, all cited commits
ancestors of the branch, lane pushed, prompt faithful). `admitted: false` — both claims fail their
own frozen kill rules and the lane says so itself. Verdict `rejected-honest-stop`: no axis is
harmed, the artifacts are measurably better on the channels the round set out to close, and the
falsification is the round's honest result.
