# Round 37 — non-author verifier spot-check (closure)

author: hyaku closure (non-author integrator, @m_kfc)
date: 2026-10-24 (UTC). Report under judgment: `.ufo/reports/round-37/chousa.md`.
Lane tip: `e85ea218deaf7deb6c46721572e71889c359d1b6`; freeze: `b905217a7dfdcf58be1f0a4c0bf5f2d2d32a2d65`.

## Dispatch / completion digest (from `.ufo/watchdog.log`, mutable)

2026-10-23T19:47:47 lane-dead-no-report chousa r37 (attempt=2: dispatch error — executor leaf role);
19:47:59 launch attempt=3; 19:57:07 dead (parent froze, L1 never ran); 19:57:16 launch attempt=1;
20:17:39 dead (second freeze); 20:17:48 launch attempt=2; 20:33:23 dead (parent SIGSEGV);
20:33:25 launch attempt=3; 23:24:29 launch attempt=1; 23:58:19 complete chousa r37 attempt=1.
Underlying round: multiple inherited attempts; attempt 5 landed the report. Orchestrator deaths, not lane refusals.

## Step-1 conformance (all pass)

- Report committed by lane identity: `git log --format='%an %H' -- .ufo/reports/round-37/chousa.md` → `chousa-shokunin 638965e9e03283f68018426da1967051638bc885`.
- `SHONEN` heading present, one `[~]` line per box (4 boxes).
- Both cited commits exist in the lane repo and are ancestors of branch `master`
  (`git merge-base --is-ancestor b905217a… master` → 0; same for `e85ea218…`; HEAD detached at `e85ea218…` = `master`).
- Lane state: `jj-lane.sh state` → `ahead=0 behind=0 tracked=0 untracked=0` (pushed, no leftovers);
  `git status --porcelain` empty.
- Prompt `.ufo/prompts/chousa-round-37.md` carries the template contract: report path (l.101),
  landed-changes-tied-to-hash + commit-before-report (l.107, 271+), SHONEN heading (l.118),
  write scope/pathspec commit (l.323). No defect.

## Claims (re-measured from committed bytes; gate never executed — §Gate standard closure consequence)

- **C1 operability** — `git show e85ea21:tools/research-gate.sh | sha256sum` → `9fcac047…cf39` = landed
  gate hash cited in report/claims.md ✓. Receipts via `jq`: base `c1-base-s37001.json`
  `matched=2 predicate_holds=false`; after receipts s37701/s37901/s37921 `matched=7
  predicate_holds=true`, each `gate_sha256=9fcac047ddad` ✓ → **2/7 → 7/7 confirmed**.
  Predicate P1 stands on every committed receipt. Claim-text general clause falsified beyond cells
  (unprivileged `LD_PRELOAD` moved verdicts 4/7 forge, 3/7 false-stale — `residual/CritC1Kill.md`),
  frozen as claims.md §Erratum 6, narrowing to PATH-independence with r38 fix direction. Claims body
  frozen at `b905217` (20:10:24 -03) **before** any after-receipt (all land in `e85ea21`, 23:56:30 -03);
  errata appended, never an edit (`git log -S'Erratum 5'` → only `e85ea21`). Handling conforms:
  the falsified clauses name pre-existing defects, not round-introduced harm.
- **C2 freshness** — base `c2-base-s37021.json` `matched=3 predicate_holds=false`; after s37721/s37941/s37961
  `matched=7 predicate_holds=true`, `gate_sha256=9fcac047ddad` ✓ → **3/7 → 7/7 confirmed**.
  P2 stands. `BASH_FUNC_date%%` startup-export leak falsified the general wording
  (`residual/RevC2FreshSeed.md`); frozen as §Erratum 5 narrowing to variable re-export independence.
- **Gate evidence verified, not executed**: selftest `PASS 267 cases 0 skipped` committed at
  SCORECARD.md:2094 and LOG.md:1388; no-harm battery 17/17 CLEAN, chain 17/22, broken 1/2 DRIFT,
  archives 3/3 recorded in SCORECARD/LOG; the wave seat `w1/ExecNoHarmPin.md` `--root .`
  mis-invocation correctly demoted to a lesson mistake (QUALITY 53).
- **No axis harmed**: `git diff b905217… e85ea21 -- SCORECARD.md` is additive (round-37 section +
  planned-38); prior axis rows untouched; wave seat evidence (`residual/RevSeparability.md`,
  mutants) committed.

Per-axis verdicts: operability **improved**, freshness **improved**, depth **improved**,
coverage **unchanged**, calibration **unchanged**, adjacency **unchanged** — all re-derived
against committed bytes; agree with SCORECARD.

## Discernment spot-check (LEARNING.md — checked from outside)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S071 (admit) | admit | `/usr/share/man/man1/env.1.gz` (sha256 `4ae797e6…fb27` ✓ matches row); `zcat \| sed -n '27,29p'`: line 27 roff tty-link `…coreutils.html#env-u`, line 28 `remove variable from the environment` | **agree** | quote located verbatim at the cited line; row quote 25 words = ≤25 boundary ✓; tier/scope/used-by accurate |
| Reject (a): second `bash(1)` row for BASH_ENV paragraph | reject | `/usr/share/man/man1/bash.1.gz` `zcat \| sed -n '2371,2373p'` → `.B BASH_ENV` paragraph as cited | **agree** | S068 already anchors `bash(1)` for BASH_ENV scope; a second row is a duplicate URL without a distinct scope |
| Reject (b): S068 anchor-label supersede | reject (carry to r38) | `corpus/SOURCES.md` S068 row (anchor label `OPTIONS`-class nit) | **agree** | cosmetic; frontier budget legitimately went to the C2 mechanism source; carried debt is named, not dropped |

`bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → exit 0,
`ok` for `chousa-shokunin/corpus/SOURCES.md`, standing W04 ×2 (S051/S053) — exactly as reported
(70 → 71 rows, A 64→65, mined 47→48, malformed 0).

## Trend verdicts (agree)

- expansion **improved** — two knowledge entries on new measured ground, README index/frontier updated, S071 opened+mined (verified rows).
- quality **improved** — both fixes measured 2/7→7/7, 3/7→7/7 across committed receipts; selftest 261→267; residual wave did real falsification with named errata instead of absorption.
- discernment **improved** — first in-round self-falsifications of frozen claim texts, honestly frozen as §Errata 5-6 with predicates' standing receipts distinguished (verified in claims.md bytes).

## Erratum-handling judgment (operator ruling support)

The round's admission is ADMIT-with-errata. Frozen predicates P1/P2 verify on every committed
receipt; no axis harmed (falsified clauses are pre-existing-defect descriptions, not round
regressions); claims body frozen before receipt data; errata appended in a later commit naming
the superseded text — conformant with the protocol's erratum mechanism. The overreach itself is
recorded as a lesson mistake (QUALITY 54). **Satisfies the contract.**

## Routed defects / notes for the operator and round 38

1. Counter-strength debt (receipts bind `gate_sha256` post-run; counters score gate self-report —
   `residual/RevC1FreshSeed.md` F1/F2) — lane already carries to r38; keep on routed queue.
2. S068 anchor-label supersede row (r36 spot-check defect 8) — carried to r38 by the lane.
3. Witnessed `SHELLOPTS=noexec` false pin success (`residual/CritC2Kill.md`) — named limit, r38 candidate.
4. Seats' answering models not individually recorded (lane discloses; no claim depends on a model).
5. SHONEN: all four boxes remain `[~]`. Box 3 evidence (`--selftest` 267 PASS) verified from
   committed bytes; boxes 1/2/4 rest on lane assertions with resolvable pointers. Promotion
   review is operator-owned — the pending external check this file satisfies is the non-author
   spot-check only; no `[x]` was written.
6. Tool installs this round: none (none by the lane; none by this closure pass).
