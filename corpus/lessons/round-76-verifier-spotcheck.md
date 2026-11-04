# Round 76 verifier spot-check — chousa

author: hyaku closure (non-author integrator, @m_zfl)

Reviewed round 76: before `1af39fed6058ad46fc075b72fddaae838f43273e`, controls/instruments
`da9ac7ec684fe9fe9ad5554cab6180057255b76b`, claims freeze `5daa3628389c164f6ee34027be77d26b175c0de7`,
wave handoff `5eeca32ba9ad80081d19906c7cb52dff35891e8c`, final tip / lane HEAD
`a519fb0a80cf52c7988713c1f05b3ce8440fedda`. This review neither improves the authored round nor
re-admits any earlier round.

## Conformance and disposition

Status **ok** — a landed report naming checkable committed work, not a marker. Admission **true**,
verdict `admitted`: both declared claims reproduce on their frozen predicates when re-measured here,
and no owned axis is harmed.

- `git log --format='%an %H %ci' -- .ufo/reports/round-76/chousa.md` (fleet repo) returned
  `chousa-shokunin <chousa@shokunin.local> 5e1e9d3056ae45064f3bdc0338589de4cb4aca33 2026-11-04 17:40:35 -0300`;
  the lane tip `a519fb0a` is 17:39:32, so the report lands last. `git show --stat` on that commit
  adds only `.ufo/reports/round-76/chousa.md` (77 lines, pathspec-limited).
- `scripts/hyaku/jj-lane.sh state …/chousa-shokunin` returned
  `branch=master local=a519fb0a remote=a519fb0a ahead=0 behind=0 head=detached tracked=0 untracked=0`;
  `git -C …/chousa-shokunin status --porcelain` printed nothing — no uncommitted round work.
  `git ls-remote origin refs/heads/master` printed `a519fb0a80cf52c7988713c1f05b3ce8440fedda`, the hash
  the report cites.
- `git merge-base --is-ancestor <hash> refs/heads/master` exited 0 for `da9ac7ec`, `5daa3628`,
  `5eeca32b` and `a519fb0a`; all four exist as commits authored by `chousa-shokunin`. Ancestry was
  tested against the branch ref, never detached HEAD.
- The report carries `## SHONEN` exactly once (`grep -c '^## SHONEN'` → 1) with four `[~]` rows, matching
  the four boxes in `SHONEN.md`; the lane wrote no `[x]`. Sections present in order: Work performed,
  Landed changes, Before → after measurements, Sources & frontier, Trend verdicts, SHONEN.
- Prompt `.ufo/prompts/chousa-round-76.md` is committed as `bf1af0726d91061b35cb531edc944c0acae3a4b9`
  at 16:38:51, one second before the launch line, and is an ancestor of fleet `origin/master`. Lines 1–140
  are `templates/round-prompt.md` with substitutions only (`diff` of the two 140-line windows shows only
  `{{LANE}}`/`{{ROUND}}`/`{{FLEET_ROOT}}`/`{{AXES}}` fills), so it carries the round-level contract
  (mission/axes §1, L2 floor ≥8 in one batched call §3, commit-then-push and push scope §5, L0 §5) and the
  five child-lane items (report path §4, report-lands-last with the pushed-hash citation §addendum,
  `SHONEN` heading §4, write scope §addendum 3). `MISSION.md` holds no model-alias table — its routing
  block is bucket-level and advisory — so the addendum's alias map can only be graded for bucket
  consistency: reviewer/critic/executor/mutation-tester/sentinel on the economy/fast route and the rest on
  the fast-execution route is consistent with that table; no alias conflict is checkable further.
- Driver digest copied from `.ufo/watchdog.log` (mutable): `2026-11-04T16:38:52-03:00 launch chousa
  round=76 pgid=2372643 driver=hyaku-inline attempt=1`; `2026-11-04T17:41:33-03:00 complete chousa
  round=76; hyaku-inline attempt=1`.
- Wave: `.ufo/waves/round-76/w1-spec.json` (lane-local, the convention since round 25) lists 12 seats —
  3 executor, scout, scribe, connector, 2 reviewer, 2 critic, mutation-tester, sentinel — so 6 attack
  seats (50%, floor 25%), one `taskCall` in `w1-dispatch.json` (one batched call, not serial spawns),
  `spawn=12 total=12`, no residual call, L1 holding the planner seat. `.ufo/waves/round-76/w1/` holds 11
  seat reports; `R76Critic` is absent and `w1-results.json` records `output: null` for every seat with the
  kernel-restart note. The report names this accounting defect itself; it is a settlement-attestation
  weakness, not a fabricated seat.

## Claim re-checks

Both claims were **re-measured by this reviewer** from the committed bytes at `a519fb0a` with scratch
`--work` directories under `/tmp` (the instruments write only beneath `--work`; static read of
`loader-matrix-v3.py` and `c2-battery.py` confirms every fixture is created and removed there). No sibling
gate was executed as gate evidence, and no lane file was written by the measurements.

### C1 — operability (lowest scored non-retired axis; historical 3/10 deliberately held)

Frozen predicate: `python3 -B corpus/evidence/round76/matrix-battery-v3.py --matrix MATRIX --work DIR`
exits 0 and prints exactly `BATTERY=PASS forgers_rejected=11/11 positive=2/2`.

| re-check | command / committed input | observed output |
|---|---|---|
| before (r75 matrix under the r76 battery) | `python3 -B corpus/evidence/round76/matrix-battery-v3.py --matrix corpus/evidence/round75/loader-matrix-v2.py --work /tmp/closure-r76/c1-before2` | `MATRIX_SHA256=95bdd493…68ee7`; `subject-map` `12/12/PASS` twice → `MISS`; `hang` `matrix_exit=timeout` twice → `MISS`; positives `ACCEPTED` twice; `BATTERY=FAIL forgers_rejected=9/11 positive=2/2`, `EXIT=1` (609.5 s wall — the two unbounded-child legs each hit the 300 s matrix bound) |
| after (v3 matrix under the r76 battery) | `python3 -B corpus/evidence/round76/matrix-battery-v3.py --matrix corpus/evidence/round76/loader-matrix-v3.py --work /tmp/closure-r76/c1-after` | `MATRIX_SHA256=b79d6441…913f`; `subject-map` `4/12/FAIL` twice → `REJECTED`; `hang` `0/12/FAIL` twice → `REJECTED`; both positives `12/12/PASS` → `ACCEPTED`; `BATTERY=PASS forgers_rejected=11/11 positive=2/2`, `EXIT=0` (81.7 s) |
| instrument identity | `sha256sum` at `a519fb0a` | battery `217ae367…4360`, matrix `b79d6441…913f`, c2 counter `610e5655…2ecbb`, c2 battery `7e0d6832…d8619` — equal to the digests pinned in `claims.md`, the receipts and the r76 `SKILL.md` registry rows |
| acceptance rule (static read) | `matrix-battery-v3.py:104-150` | positive accepted only when both runs exit 0 with `marks[0]==marks[1]` and `PASS`; forger rejected only when both runs exit 1 with `marks[0] < marks[1]`; battery exits 0 only when 11/11 and 2/2; exit 2 reserved for usage/missing input |
| matrix closures (static read) | `loader-matrix-v3.py:143-190` | per-seed `random.Random(seed).shuffle(CASES)`; every case commit subject is the literal `case`; per-run salt in every file body and a random-length pad on every mutation; child in its own session, `killpg(SIGKILL)` on expiry; exact failed-check-id set and the `C2=<summary> checks=` line both asserted |

C1 verdict **improved narrowly**: the frozen predicate reproduces in both directions at the reviewed tip,
the r75 answer key (`subject-map`, 12/12 twice) and the stall are now rejected, and the two positives are
retained in both directions. The battery is a discrimination floor over thirteen named subjects, not
forged-freedom: this reviewer confirms the lane's own recorded limits (a fixed-order outer battery, a
learned-table answer key the frozen subjects do not carry, an unchanged case whose size tuple stays
stable). Those limits are recorded in `QUALITY` 138–139 and the lesson, and no frozen byte was amended
after scoring.

### C2 — calibration

Frozen predicate: `python3 -B corpus/evidence/round76/c2-battery.py --counter COUNTER --work DIR` exits 0
and prints exactly `C2_BATTERY=PASS bogus_rejected=6/6 positive=1/1 lane=PASS`.

| re-check | command / committed input | observed output |
|---|---|---|
| before (r75 counter under the r76 battery) | `--counter corpus/evidence/round75/c2-count.py --work /tmp/closure-r76/c2-before` | `COUNTER_SHA256=bf0250e7…8b8`; `negation`, `magnitude`, `comment-only`, `mid-file` each `actual=accept rc=0`; `good-block` and `deletion-history` correct; `LANE real … rc=0`; `C2_BATTERY=FAIL bogus_rejected=2/6 positive=1/1 lane=PASS`, exit 1 |
| after (successor counter under the r76 battery) | `--counter corpus/evidence/round76/correction-count-v2.py --work /tmp/closure-r76/c2-after` | `COUNTER_SHA256=610e5655…2ecbb`; all six bogus fixtures `actual=reject rc=1`; `good-block` accept; `LANE real expected=accept actual=accept rc=0`; `C2_BATTERY=PASS bogus_rejected=6/6 positive=1/1 lane=PASS`, exit 0 |
| lane leg pinning | default `--lane-rev master` in the reviewed checkout | my run resolved `master` to `a519fb0a` (the reviewed tip, later than the freeze) and still printed `lane=PASS`; no divergence, but the leg follows a moving ref — routed below |
| receipt agreement | `controls/{before,after}-c2-battery.txt` | per-fixture lines, digests and exit codes identical to my run; the receipts are honest records of the same predicate |

C2 verdict **improved narrowly**: the presence-test counter's four accepted bogus classes now reject, the
valid block and the real lane still pass, and the successor derives its numbers from the authored bullets.
The axis reading is the lane's own calibration precedent (r4 treated substring→token-boundary matching
semantics as a calibration move): the instrument that audits the lane's correction records now catches
polarity, magnitude, position and ancestry overreach. The caveat the lane states is accepted as a limit,
not a claim: this does not census SCORECARD/SHONEN mismatches, and nine survivor fixture classes remain
recorded (`QUALITY` 140) rather than certified away.

## Axis verdicts

`git diff 1af39fed a519fb0a --numstat` on the append-only surfaces is `10/0 LOG.md`, `51/0 SCORECARD.md`,
`2/0 SKILL.md`, `6/0 corpus/QUALITY.md`, `3/0 corpus/SOURCES.md` — additions only, no score row changed, no
capability row added. `corpus/knowledge/`, `corpus/README.md` and `PROVINCE.md` are untouched. The round
diff is 383 files, +19000/−0 (353 of them lane-local wave receipts under `.ufo/`).

| axis | verdict | evidence |
|---|---|---|
| operability | improved | C1 re-measured here: 9/11 FAIL exit 1 → 11/11 PASS exit 0; subject-map and hang now rejected; positives retained; numeric score held at the historical 3/10 as declared |
| calibration | improved | C2 re-measured here: 2/6 → 6/6 bogus rejected with the valid block and the real lane accepted; derived counts bound to the authored bullets; QUALITY 136/140 record the surviving classes |
| depth | unchanged | no `corpus/knowledge/` entry added or changed; no externally grounded fact this round |
| coverage | unchanged | `PROVINCE.md` and `corpus/README.md` untouched; the frontier section says "none advanced" and that is accurate |
| freshness | unchanged | no drift surface re-measured; the r75 `SKILL.md` registry rows are corrected by two new rows, not by re-verifying the old ones |
| adjacency | unchanged | sibling precedents were read and reported by `R76Connect`, not absorbed; `PROVINCE.md` refusals unchanged |

## Independent discernment spot-check

Re-opened all three `## Gate` rows at their pinned revisions (two admits, one reject), plus both new
`corpus/SOURCES.md` rows and their quotes.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S187 | admit, own-work B / mined | `1af39fed:corpus/lessons/round-75-verifier-spotcheck.md:124-128`, quote line 125 | agree | The line reads "commit subject, tree ids and byte sizes are stable metadata channels, and four content-blind" — 14 words, contiguous, verbatim; the row's `teaches` is exactly routed defect 1, and `used-by` `corpus/lessons/round-76.md` exists and cites it. |
| S188 | admit, own-work B / mined | same revision, lines 129-131, quote line 130 | agree | "polarity and magnitude rather than substring presence, require the correction block to be the final section" — 16 words, contiguous, verbatim; the row scopes routed defect 2 and the same `used-by` path resolves. |
| S189 | reject, own-work C | `5daa3628:corpus/evidence/round76/claims.md:27`, quote `BATTERY=PASS forgers_rejected=11/11 positive=2/2` | agree | The span is on line 27 as claimed, but the file is the lane's own declaration of its predicate, not evidence the predicate holds; a row there would let a later round cite its own declaration. The stated flip is concrete and the reason is the right one. |

All three Gate quotes are ≤25 words, verbatim at the named location, with the access date 2026-11-04 and a
revision-pinned path; no URL was fetched because none of the three is external. The lesson also records
the kept reject and its flip, and states that no held status/recheck/used-by cell changed.

Census over committed blobs (`^ {0,3}\|\s*S\d{3,}\s*\|`): **186 → 189**; tiers A123/B48/C15 →
A123/B50/C16; statuses mined150/queued19/rejected17 → mined152/queued19/rejected18; `git diff --numstat`
on `corpus/SOURCES.md` is `3/0`, so no earlier row byte changed. The reported numbers match exactly.

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`
→ exit 0, `chousa ok …/corpus/SOURCES.md`, with only the five pre-existing W04 duplicate-URL warnings
(S051, S053, S073, S074, S075) — the same five the report pastes. No new E or W finding.

## Learning trends

| trend | verdict | evidence |
|---|---|---|
| expansion | unchanged | no knowledge entry, coverage-map advance, province ground or capability row: `git diff --name-status` shows no `corpus/knowledge/`, `README.md` or `PROVINCE.md` change and `SCORECARD.md` adds no capability row; +3 registry rows is curation. |
| quality | improved (narrow) | The r75 presence-test counter and answer-key matrix are superseded by stronger instruments with the weaker behaviour re-measured (2/6 → 6/6; 9/11 → 11/11), and QUALITY 138–140 are lesson-grounded criteria that raise the bar on what a successor freeze must control. No admitted knowledge entry was found false and left unmarked; no entry was touched. |
| discernment | improved | This non-author spot-check agrees with both admits and the reject; the round's attack findings became recorded limits and three grounded QUALITY criteria, and two own mistakes (a memory-typed digest, a piped exit code) were mined with a guard shown able to fail; the Gate draft's anchor/count errors were caught before landing. |

## Routed defects (owner chousa, next round)

1. **Outer batteries score exit codes in a fixed subject order.** `matrix-battery-v3.py` and
   `c2-battery.py` run subjects in a constant sequence and score only exit status, so a call-count oracle
   reaches both exact target lines without reading any input (`R76Review/c1-order-probe.out`,
   `c2-order-probe.out`, both `BATTERY=PASS`/`C2_BATTERY=PASS`). Permute subject order per run (seeded),
   bind at least one leg on subject output content, and ship the order-oracle as a scored control before a
   successor freeze. QUALITY 139 states the bar; no frozen byte may be amended retroactively.
2. **The C2 lane leg follows a moving ref.** `c2-battery.py` defaults to `--lane-rev master`, so a clean
   checkout does not pin the leg (it resolved to `5eeca32b` inside the reviewer clone and to `a519fb0a` in
   this review, both PASS). Pass an explicit `--lane-rev <freeze>` in every receipt and record the resolved
   revision.
3. **The frozen claims prose carries a false sentence.** `corpus/evidence/round76/claims.md` says "routed
   defect 4 … is honoured by naming the controls revision in every receipt"; the prefreeze receipts name
   worktree digests, not the controls revision. The lesson records the correction, but the frozen file is
   the artifact a successor will read — supersede it with an append-only correction entry naming the
   superseded text, and do not repeat the sentence in a successor claims file.
4. **The frozen battery's subject set does not carry a learned-table answer key.** `R76ExecC` shows the
   subject closure and the salt/pad closure are load-bearing against memo forgers that the frozen eleven do
   not include, so removing either closure still prints `BATTERY=PASS`; and the unchanged case keeps a
   stable size tuple in 3/3 runs. QUALITY 138 states the successor requirement; the successor battery must
   ship the learned-table and unchanged-size witnesses as scored subjects.
5. **Wave settlement evidence.** `w1-results.json` carries `output: null` and no per-seat terminal
   status/id after the orchestrator restart, and `R76Critic`'s report is absent (wake 402). The report
   discloses both; a future wave should persist each seat's terminal record (report path plus exit status)
   at settle time so settlement is a retained record rather than an attestation.

## Notes for the operator

- The four `SHONEN.md` boxes look mechanically checkable by a non-author from the pointers the lane cites:
  `SKILL.md` has `## Decision table`, `## Error patterns`, `## Checklist (executable)` and `## Gates`;
  `LOG.md` has the Round 9 entry and `corpus/fixtures/archives-r9/` exists; `corpus/evidence/round73/controls/preflight-r73.txt`
  exists; `PROVINCE.md` is present and unchanged this round. Promotion remains operator-owned; this file
  checks no box.
- No lane-authored file, `SHONEN.md` mark, promotion, mint or sibling lane was touched by this review.
