# Round 73 verifier spot-check — chousa (closure)

author: hyaku closure (non-author integrator, @m_zfl)

Closed 2026-11-04 against lane tip `4b76c7c2892bee44ee153f79a75685da9324ed97` (branch `master`, local == `ls-remote origin` == tip, `ahead=0 behind=0`), base `f748abbb6bf58388e732facd4ecec5612419c457`, freeze A `a0f094c272dcb09f1bf79e2c9057d7ea20b7ac7b`, landing B `5aec90775fc7cc1fe9ad442e0d5491731323eec1`. Report: `.ufo/reports/round-73/chousa.md` (committed in the fleet repo by the lane identity `chousa-shokunin`, fleet commit `14cd183cfb8670dd12e552556fd8466b4f47a93a`). Dispatch digest (`.ufo/watchdog.log`, mutable — copied here): `2026-11-03T23:35:21-03:00 launch chousa round=73 pgid=3440041 driver=hyaku-inline attempt=1`; `2026-11-03T23:58:03-03:00 complete chousa round=73; hyaku-inline attempt=1`. Both lines verified present in the live log verbatim. Read-only git/jj-helper only; no lane gate or counter executed (§Gate standard, Closure consequence).

## 1. Conformance (step 1)

| check | command | observed | result |
|---|---|---|---|
| lane state pushed | `scripts/hyaku/jj-lane.sh state <lane>` | `branch=master local=4b76c7c… remote=4b76c7c… ahead=0 behind=0 head=detached tracked=0 untracked=0` | PASS |
| no uncommitted round work | `git -C <lane> status --porcelain` | empty (rc 0) | PASS |
| report authored by lane identity | `git -C <fleet root> log --format='%an %H' -- .ufo/reports/round-73/chousa.md` | `chousa-shokunin 14cd183cfb8670dd12e552556fd8466b4f47a93a` | PASS |
| SHONEN heading + one line per box | awk over report | `^## SHONEN` = 1; four `- [~]` lines, each with a resolvable pointer | PASS |
| cited commits exist and are ancestors of the branch ref | `git merge-base --is-ancestor <hash> master` for base, freeze, landing, tip, `7f7ea19a…`, `6dd6c82…` | all six exist, all ancestors of `master` | PASS |
| report lands after lane push | report commit `2026-11-03T23:56:31-03:00`; `state` shows remote already at `4b76c7c…` (the report's pre-report `ls-remote` gate names it); watchdog complete 23:58:03 | report cites the pushed tip | PASS |
| prompt carries the template contract | read `.ufo/prompts/chousa-round-73.md` | report path, commit-before-report ordering, `## SHONEN` grep gate, commit-hash citation rule, write scope, frontier step, hyaku §6 addendum all present | PASS |

No conformance defects. The lane repo is jj-colocated with git HEAD detached, exactly as the closure brief warns; every ancestry test ran against the `master` branch ref, never `@{u}`.

## 2. Claim re-checks (step 2) — commands run by this closure, against committed bytes

**C1 operability (lowest non-retired axis) — IMPROVED on its frozen completing predicate; evidence-verified (the receipts are the lane's committed run evidence; this closure does not re-execute the gate battery).**

- `grep -c '^RESEARCH_GATE_SELFTEST:' corpus/evidence/round73/controls/battery-r73.txt` → **1, rc 0** (report says 1).
- `grep -c 'SKIPPED=none' corpus/evidence/round73/controls/preflight-r73.txt` → **1, rc 0**; `grep -c '^PREFLIGHT=' …` → **1, rc 0** (report says 1/1).
- Receipt contents read: battery `RESEARCH_GATE_SELFTEST: PASS (275 cases, 0 skipped)`, `SELFTEST_RC=0`, header names measured revision `a0f094c2…` and tool digest `d5d48128…`; preflight tail `PREFLIGHT=8/8 FAILED=none ENV=none SKIPPED=none`, `PREFLIGHT_RC=0`, same revision + digests. Matches the report exactly.
- Do-nothing control re-read (`controls/before-r73-greps.txt`): at base `f748abbb…` the anchored verdict count is 0 and no preflight receipt exists — a do-nothing round cannot reach the predicate. The receipts were produced at freeze `a0f094c2…` with unset budgets, disclosed.
- No owned axis harmed: `git diff f748abbb… 4b76c7c… -- SCORECARD.md` is append-only additions (frozen planned section, r72 correction note, r73 verdict); no numeric score moved; `tools/research-gate.sh` and `tools/lane-preflight.py` bytes unchanged (digest `d5d48128…` pinned in the receipt and re-derived in `before-r73-greps.txt`).

**C2 calibration — HONEST-STOP on its frozen counter; the underlying corrections independently re-measured as append-only.**

- Frozen-counter evidence verified, not executed (§Gate standard): committed receipt `controls/after-c2-r73.txt` shows `CHECK C2-6 FAIL removed lines=LOG.md:11,…` and `C2=FAIL checks=6/7 rev=5aec9077 base=f748abbb`, `EXIT=1`. Matches the report's "base 2/7 → landing 6/7, target 7/7 unmet".
- The loader defect is real, read from committed code: `c2-count.py` `load()` sets `deleted[parts[2]] = int(parts[0])` — numstat column 0 is *additions*, column 1 is deletions. A compliant append is therefore scored as removals. The frozen counter bytes at tip equal the mutation receipt's pinned sha256 `e6e22b1e…` (`git show master:corpus/evidence/round73/c2-count.py | sha256sum` matches); the counter was not amended after scoring.
- Independent plain measurement (this closure): `git diff --numstat f748abbb… 5aec9077… -- LOG.md SCORECARD.md corpus/lessons/round-72.md` → **11/0, 21/0, 6/0** — identical to the report and to `after-c2-r73.txt`'s independent block. The factual V72-1/V72-2 corrections are genuinely append-only.
- Correction substance verified against the live tree: `tools/research-gate.sh:8426` is a `grep -q … && p36_ok=0` line (set-e-exempt in `&&`), `:8435` is the unguarded `p36_out=$(bash "$SELF" --pin …)` assignment — V72-1's re-attribution is correct. `git show 6dd6c82:SCORECARD.md | grep -c '18 healthy'` → **3**; `git show 7f7ea19a:…` → **2**; the r72 receipt's own recorded `git rev-parse HEAD` is `7f7ea19a…` — V72-2's tree correction is correct. Empirical harness receipt `controls/v72-killline-harness.txt` (two runs, PASS 8/8, byte-identical) is committed.
- Claim verdict: **fails its frozen 7/7 predicate, honestly reported as such** — re-measured where possible (numstat, code, tree counts), evidence-verified where lane-owned (frozen counter, gate receipts). Round self-declares "not admitted"; the closure agrees.

**Round shape / L2 floor — PASS.** One v1 wave, 11 seats per committed `.ufo/waves/round-73/w1-results.json` (`seats: 11`; roster 2 scout, 1 connector, 3 executor, 1 scribe, 1 revenger, 1 reviewer, 1 critic, 1 mutation-tester — matches the report and the frozen plan; attack share 3/11 ≥ 25 %; no planner seat, the L1 holds it; no residual). Run-15 band 8–16 satisfied; §3 floor of 8 met. WAVE-DONE parent delivery recorded in the lesson; results.json carries all 11 seat outputs; no dead seat reported.

**Frontier step — PASS.** Census command re-run by this closure: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → rc 0, output byte-matching the committed `census-end.txt` (same five W04 duplicate-url warnings + `ok`). Row count command re-run: `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → **181**; status histogram re-run: mined=147, queued=19, rejected=15 — all match the report (179→181; mined 146→147; rejected 14→15; queued 19). `## Mistakes` carries five mined rows; C2 cites S180 (sourced-claim requirement).

**Erratum to the r72 report — verified.** r72 report line 21 says "after-counts … at the verdicts tree" and line 54 names "the unguarded grep on the never-written `r36-pin.txt` baseline" as the crash site; both attributions are what the r73 erratum corrects, and the corrections match the code and the trees.

## 3. Discernment spot-check (step 3) — I am the named non-author reviewer

| item | gate decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S180 (admit, own-work B) | mined; grounds V72-1/V72-2 | `git show a0f094c2…:corpus/lessons/round-72-verifier-spotcheck.md`, §6 V72-1 at line 90; quote "The line that actually exits is the next unguarded sub-run assignment" (10 words ≤ 25) | **agree** | the source states the exact 8426/8435 mechanism; this closure independently reproduced the line semantics and the exempt-vs-unguarded distinction from the live gate source |
| S181 (reject, own-work C) | rejected: header's tree attribution wrong; flip: correct attribution + re-derivation at the declared revision | `git show a0f094c2…:corpus/evidence/round72/controls/after-r72-corrections.txt` header line 1 + revision line 5; quote "every count line re-run fresh at the verdicts tree, immediately before the verdicts commit" (13 words ≤ 25) | **agree** | the receipt's own `rev-parse HEAD` records the landing tip `7f7ea19a…`, where the count is 2, not the verdicts tree's 3; rejecting only the attribution (not the counts) with an actionable flip is the right discernment call |

Registry rows re-opened at the tip: S180 and S181 rows parse as 11-column rows, quotes located and within the 25-word bound, statuses `mined`/`rejected` consistent with the lesson's `## Gate`. No held status/recheck/used-by cell changed (diff of `corpus/SOURCES.md` shows only the two appended rows).

## 4. Axis and trend verdicts

| axis / trend | verdict | basis |
|---|---|---|
| operability (C1) | **improved** | completing predicate met on this host: battery PASS 275/275 + preflight 8/8 receipts verified, counts 1/1/1 re-derived, tool bytes unchanged, do-nothing control shown unreachable |
| calibration (C2) | **unprovable** | the frozen 7/7 counter is invalid (loader column swap, confirmed in committed code); its verdict cannot certify anything. The underlying corrections verify append-only by independent numstat; the axis measurement instrument is broken, so no calibration improvement is provable this round |
| depth / freshness / coverage / adjacency | **unchanged** | SCORECARD diff append-only, no scores, no capability row, no tool bytes; receipts name revisions and digests |
| expansion | **unchanged** | no knowledge/ entries, no coverage-map advance, no capability; registry +2 rows only |
| quality | **improved** | first completed battery+preflight receipts on this host supersede the prior incomplete state; the invalid counter is explicitly marked, never admitted as sound; mistakes mined with criteria |
| discernment | **improved** | outside spot-check (this file) agrees with the gate on the admit (S180) and the reject (S181); disagreements: none left unlearned |

## 5. Routed defects and notes for the next round

1. **Frozen C2 counter invalid (routed, owner: chousa).** `c2-count.py load()` reads numstat additions as deletions; compliant append fails 6/7, a real deletion passes C2-6; the 7/7 selftest bypasses `load()` and cannot catch it. Before any successor calibration freeze, exercise a real committed append and a real deletion through `load()` (the lane's own lesson says exactly this). The counter stays frozen and marked invalid until then.
2. **Carried, unresolved (named in the report, re-flagged):** the old L0 fetch-scope question; the flock(1) operator decision; the historical Windows-host load question (Linux capability is not an answer for the old host); the SHONEN promotion review and non-author entailment review remain operator-schedulable. All four SHONEN boxes still look checkable by a non-author promotion review — promotion is operator-owned, recorded here per the standing instruction.
3. **Status note:** the r72 report lines 20/54/21 attributions are corrected by r73's erratum; the r72 report bytes stay untouched, as they must. No fleet-root misroot of chousa seats remains (the one seat file `ns-arm-r73s02.txt` was recovered byte-exact by the lane; unrelated fleet-root files are other lanes' in-flight work, untouched by this closure).

Round admission: **not admitted — C2 honest-stop on its frozen counter.** C1 verifies. No axis harmed.
