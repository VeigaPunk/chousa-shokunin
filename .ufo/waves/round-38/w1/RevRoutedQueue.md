# RevRoutedQueue

Seat: chousa-r38.RevRoutedQueue (revenger, leaf). Lane tip read-only: `git rev-parse master` →
`504c1d2a1257a9ac6e5d752dcaf3f0bb0a35d05f` (dispatch tip). Candidate gate sha256
`37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d` = frozen value
(`corpus/evidence/round38/claims.md:14-15`). Sources: round-37 closure routed list
`corpus/lessons/round-37-verifier-spotcheck.md:81-89` (6 items) and `SCORECARD.md` §Planned —
round 38 (:2117-2136, 11 candidates). No counter end-to-end run of my own; no seeds consumed
(seat evidence below cites sibling fresh seeds). No tools installed (pacman pause honored).

## Verdict

C2 lands routed item 1's F1+F4 halves and C1 lands item 3's exported-`env` witness half with
named remainders (F2, `SHELLOPTS=noexec`, parent-function class, `LD_PRELOAD`) — but the carry
chain for item 2 mis-points BOTH the row id (S068; actual S070) and the defect number (8; r36 has
no defect 8, the anchor-label item is #4), the spans-≥32768 debt is untouched yet its naming drops
out of r38 claims.md, and three traps (uncommitted wave receipts, a post-freeze claims.md edit,
the planned-list wording) are where the round report would overstate.

## Evidence

- SHELLOPTS=noexec re-run, both gates, baseline path in `/tmp/rrq38.W45Cqv/`:
  `SHELLOPTS=noexec bash /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --pin $W/cand.baseline`
  → rc=0, `ls: cannot access 'cand.baseline': No such file or directory`; same for the r37 landed
  gate (`git show 95e33de8…:tools/research-gate.sh` → `$W/gate-r37landed.sh`, sha a7-prefix family
  9fcac047 tree bytes): rc=0, no baseline. The defect is still live on the r38 candidate gate.
- Receipt binding matrix (verify-receipts.py, committed bytes only): c1-after-s38001/s38011 ok
  (--gate tools/research-gate.sh --counter corpus/evidence/round38/c1-count.py); c1-base-s38001 ok
  against `--gate .ufo/waves/round-37/controls/base-gate-r37.sh`; c2-base/after-s3810{1,1}*/s38111 ok
  against `--counter corpus/evidence/round38/c2-count.py` → 6/6 VERIFY: ok under correct identity.
  Cross-identity probes refuse: c1-base vs candidate gate → `VERIFY-FAIL: gate-sha256-mismatch`;
  c2 receipts vs c1 counter → `VERIFY-FAIL: counter-sha256-mismatch`. Legacy r37 receipt
  (corpus/evidence/round37/receipts/c1-after-s37701.json) → `VERIFY-FAIL: missing-field
  counter_sha256`, exit 1 (fail-closed holds; named field differs from the docstring's example).
- Gate diff vs r37 closure tree 95e33de8: `git diff` → 1 file, +170/−1; hunks at
  sha256_hex_file (+66 env-pin/provenance helpers), `gate_canonical_capture` (−1: the bare
  `env -u …` scrub line replaced by the pinned absolute env invocation), selftest (+66 r38 cases),
  tail (+3). ZERO hunks touch any span-matcher line (grep of diff ± lines for span/LONGSPAN: none).
- `grep -rnE '32768' corpus/evidence/round38/` → no output; `grep -nE '32768|span'
  corpus/evidence/round38/claims.md` → NONE. r38 claims.md nowhere names the carried spans debt.
- `git diff 504c1d2a -- corpus/evidence/round38/claims.md` → one hunk, +6 lines: the new
  LD_PRELOAD loader-env limit bullet (§Limits). Worktree claims.md ≠ freeze-commit claims.md.
- Committed receipts = construction seeds only (`git ls-tree 504c1d2 …/round38/receipts/` →
  c1-base-s38001, c1-after-s38001/s38011, c2-base-s38101, c2-after-s38101/s38111). No wave-seed
  receipt is committed.
- corpus/SOURCES.md: 71 rows, last S071 (`ScoutFrontier.md` census re-run; my grep of S068/S070
  rows agrees); no S072/S073 rows landed. ScribeSources drafts S072 (bash.info `Shell Functions`)
  and S073 (`supersedes S070 —` label correction) inside `.ufo/waves/round-38/w1/ScribeSources.md`.
- Sibling fresh-seed re-derivations (their reports, w1/): ExecC1Rederive — base 2/7 → landed 7/7,
  seeds 38211 and 38231; ExecC2Rederive — r37 counter 0/7 → r38 counter 7/7, seeds 38221 and 38241;
  ExecF1Replay — r38 counter exit 2 `RECEIPT=ABSENT` on the self-rewriting shim (seed 38238) while
  the r37 counter accepts the same shim 7/7 (seed 38239); ExecNoHarm — selftest
  `PASS (272 cases, 0 skipped)`, claims/chain fixtures CLEAN, archive battery 3/3.

## Findings

1. **Routed item 1 (counter-strength debt, `round-37-verifier-spotcheck.md:83-84`) — LANDED IN
   PART by C2.** F1 (post-run-only gate hash): closed — pre==post binding, changed gate refuses
   exit 2 with no receipt; my matrix + ExecF1Replay's shim (r38 refuses, r37 accepts) demonstrate
   both directions. F4 (no counter identity): closed — `counter_sha256` bound and re-derived
   (plus `expect_sha256`, `receipt_sha256`); cross-identity probes refuse. **Overstatement trap:**
   item 1's second half — F2, "counters score gate self-report" — is NOT fixed;
   `claims.md` §Limits names it ("a hostile gate that prints the expected strings still scores").
   The r37 lesson item 1 cites F1/F2; only F1 (and F4) are closed. A report saying item 1
   "landed" without the F2 remainder overstates.
2. **Routed item 2 (anchor-label supersede row, `:85`) — IN FLIGHT, mis-pointered upstream.**
   Ground truth: `round-36-verifier-spotcheck.md:160-161` — defect **4**, row **S070** (sha256sum
   `-c, --check` labelled SYNOPSIS, sits under DESCRIPTION); the r36 defect list has items 1-6
   only (:149-168), no defect 8. The r37 lesson says "S068 … defect 8" and `SCORECARD.md`
   §Planned — round 38 repeats "S068 … defect 8"; S068 is the unrelated bash(1) BASH_ENV row.
   r38 got it right: `claims.md` names "the carried S070 anchor-label supersede row" and
   ScribeSources drafts S072/S073 with `supersedes S070 —`. **Overstatement traps:** (a) any
   report sentence quoting the planned list propagates S068; (b) as of now the rows are drafts in
   a seat report — SOURCES.md still ends at S071, so "landed" is only true after the L1
   integration commits.
3. **Routed item 3 (`SHELLOPTS=noexec` + exported-`env` witness, `:86`) — SPLIT.** Witness half:
   LANDED by C1 (pinned absolute `env`; `BASH_FUNC_env%%` cannot interpose; P1 7/7 on construction
   seeds 38001/38011 committed as receipts, wave seeds 38211/38231 in ExecC1Rederive; base gate
   2/7 control). SHELLOPTS half: EXPLICITLY DEFERRED with the boundary reason — bash applies `-n`
   before the gate body, no in-body fix exists (`claims.md` §Limits bullet); my probe re-demonstrates
   exit 0 / no baseline on the r38 candidate gate itself. **Overstatement trap:** `claims.md`'s
   routed-work sentence names the "pair" together; a report that credits the pair to C1 overstates —
   only the witness half closed, and even that closes "that one witness, not the parent-function
   class" (SCORECARD wording; claims.md §Limits names exported `bash` as next-witness debt).
4. **Routed item 4 (answering models not recorded, `:87`) — NOT ADDRESSED.** No model-recording
   mechanism anywhere in the w1 spec (`gen-w1-spec.py` assigns no such task; seat reports record
   no models). Unchanged disclosure practice; nothing claims otherwise — low overstatement risk
   unless the report claims the routed queue "worked" without saying this item was skipped.
5. **Routed item 5 (SHONEN boxes, `:88-89`) — NOT ADDRESSED, correctly.** `SHONEN.md`: all four
   boxes still `[~]`; no `[x]` written; promotion operator-owned. Box-3 underlying evidence got
   stronger this round (selftest 267→272 cases, re-executed by ExecNoHarm) without a flip — the
   honest state; a report noting "box 3 evidence re-verified at 272 PASS" must not slide into a box flip.
6. **Routed item 6 (tool installs none, `:90`) — HOLDS.** No pacman/uv/cargo/npm transaction by
   this seat; ExecNoHarm/ScribeSources/ScoutFrontier each state none; host-wide pacman pause
   observed. No risk.
7. **Planned-38 candidates with NO r38 disposition (all NOT ADDRESSED this round; the report must
   carry them as open, not silently drop):** prefix-64 attribution bypass (r36 Erratum 8);
   S7-S9 per-scenario assertion tightening (QUALITY 52); the three `tools/argv-witness.py` dead
   fields (SimpDiff D1-D3 — the w1 spec cites D1-D3 only as a YAGNI review *pattern* for the new
   artifacts, `gen-w1-spec.py:360-364`, not as a fix); metadata-screener locale seam (r36
   Erratum 13); call-for-show engine measurement (r36 Erratum 9); the pin-child loader-env
   `LD_PRELOAD` scrub + counter cell (r37 Erratum 6 — `claims.md` explicitly carries it); the
   capture-side `BASH_FUNC_*` full scrub / genuinely-exported counter scenario beyond the
   env-named function (Erratum 5 remainder). None has a seat, a claims clause, or a receipt.
8. **Carried C1 debt (spans ≥ 32768): UNTOUCHED but NAMING GAP.** Untouched: the gate diff's four
   hunks contain no span-matcher line (see Evidence). Named: SCORECARD §Planned — round 38 closes
   with "the carried C1 debt (spans ≥ 32768) stays open" (:2136) — but r38 claims.md, unlike r35
   (`claims.md:136-138`) and r36 (`claims.md:153-155`), carries NO such scope/naming sentence, and
   nothing under `corpus/evidence/round38/` mentions 32768. The claim stays open de facto (the
   r34 capability rides the unchanged matcher); the round report should re-state the debt
   explicitly, since the claims body alone no longer names it.
9. **Post-freeze claims.md edit — discipline flag.** The worktree adds the LD_PRELOAD limit bullet
   (+6 lines) on top of freeze commit 504c1d2, whose claims.md declares "Nothing in this file
   changes after the first wave receipt: a later change is an erratum appended below, never an
   edit" (claims.md:7-9). Construction receipts are IN 504c1d2; wave receipts postdate the edit.
   The edit narrows the claim (a limit), so the honest direction, but as git-visible bytes it is
   an edit, not an appended erratum. Needs either jj-history folding into the freeze generation
   before the round commit or an erratum note naming the superseded text — otherwise the round
   report's "frozen before any wave run" line overstates.
10. **Wave receipts uncommitted — QUALITY-27 exposure.** P1/P2 require the predicate on "two fresh
    seeds" with committed receipts and no lower committed run. Committed receipts today are
    construction-seeded only; the fresh-seed evidence (38211/38231, 38221/38241, 38238/38239)
    lives in `/tmp` and w1 seat reports. If the round lands citing fresh-seed verification without
    committing those receipts under `corpus/evidence/round38/receipts/`, the SCORECARD row
    overstates its own evidence set.
11. **Nit (docstring vs behavior).** `verify-receipts.py` docstring says a legacy receipt fails as
    `VERIFY-FAIL: missing-field gate_sha256_pre`; actual first-named field is `counter_sha256`
    (REQUIRED-tuple order). Fail-closed exit 1 unaffected; fix the example text at the next touch.

## Limits

- Read-only leaf: I re-executed verify-receipts, the SHELLOPTS probe, and all git/grep facts; I
  did not run c1-count/c2-count end-to-end myself — fresh-seed predicate counts cite sibling w1
  reports (ExecC1Rederive, ExecC2Rederive, ExecF1Replay), not my own runs.
- The claims.md worktree edit may already be folded into a jj amendment invisible to `git diff`
  by the time the round commits; my observation is on git-visible bytes at report time.
- SHELLOPTS probe ran with the baseline path under `/tmp/rrq38.W45Cqv/`; the noexec body never
  ran, so nothing was written into the lane; scratch stays in that temp dir.
- Dispositions for w1 sibling seats are as-of-now snapshots; integration (SOURCES S072/S073,
  wave receipts) may land after this report.
