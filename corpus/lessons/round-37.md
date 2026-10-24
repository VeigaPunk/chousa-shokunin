# Round 37 — claim-pin provenance and pin-capture environment

Dates are UTC. Attempt 5 of the round (watchdog `lane-dead-no-report chousa round=37` ×5,
orchestrator deaths, not refusals). Attempt 4 landed the freeze at
`b905217a7dfdcf58be1f0a4c0bf5f2d2d32a2d65` (counters, gate fixes, selftest 262-267, frozen
`corpus/evidence/round37/claims.md`, base control) and dispatched wave 1 (39 seats) before
dying; attempt 5 inherited its spec, dispatch and 8 returned seat reports under
`.ufo/waves/round-37/`, re-verified them, ran the L1 re-derivation, and landed the frontier.

- **C1 operability** (lowest scored axis, 3/10; surface: the `verify-claims` revision pin) —
  a claim's `sha256` pin is hashed through one pinned absolute `sha256sum`, never the caller's
  PATH. Before `CLAIM_PIN_PROVENANCE_MATCH=2/7` (base gate `a7d3922c…`, seed 37001, re-derived
  by the wave on 37101/37123), after 7/7 on seeds 37001, 37701 (L1), 37901, 37921 (wave) with
  committed after-receipts `gate_sha256=9fcac047…` (landed gate), plus report-only wave
  re-derivations on 37111/37133 (`w1/ExecC1LandedRederive.md`).
- **C2 freshness** (surface: the `--pin` capture environment) — a `--pin` baseline is
  independent of the caller's `BASH_ENV`: the capture child now runs `env -u BASH_ENV` (S071).
  Before `PIN_CAPTURE_ENV_MATCH=3/7` (base gate, seed 37021, re-derived by the wave on
  37201/37223), after 7/7 on seeds 37021, 37721 (L1), 37941, 37961 (wave) with committed
  after-receipts `gate_sha256=9fcac047…`, plus report-only wave re-derivations on 37211/37311.

Two claims, distinct axes (operability / freshness), causally separable: each counter reads the
other's surface not at all, and the wave's single-hunk gate mutants isolate each fix
(`w1/ExecMutGateC1.md` C1 2/7 & C2 7/7; `w1/ExecMutGateC2.md` C2 3/7 & C1 7/7).

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| scope (a counting command was run with a different corpus root than the recorded pin, and the refusal output was read as harm) | `w1/ExecNoHarmPin.md`: the seat ran the no-harm battery with `--root .` (lane root) instead of the recorded `--root ..` (fleet root); every claim/chain source refused `*_SOURCE_OUT_OF_CORPUS` (0/17, 0/22, 0/2) and the seat reported "Harm" on all six rows; the per-input archive DRIFTs it also flagged are exactly the pinned round-1 observable (exit 1 + one DRIFT summary each) | the wave's own seat output, caught by the L1's re-run before any report cited it; the recorded battery commands live in `w1/SentNoHarm.md` (round 36) lines 22–25 (cwd line 18) — **no in-round rule** pins a battery's corpus root against drifted invocation | the L1 re-ran the battery with the recorded commands: claims 17/17 CLEAN, chain 17/22 CLEAN, broken control 1/2 DRIFT, archives 3/3 (`VERDICT_BEARING_EXPORTS=3/3`) — no harm; QUALITY 53 added (a no-harm battery's commands must be re-used verbatim from their pinned record, and a refusal-class result is a signal to check the invocation, never itself harm) |
| number-drift (a wave brief's expected seat count vs the returned reports) | the inherited `w1-spec.json` declares 39 seats; only 8 seat reports returned before the orchestrator died (31 dead seats, never replaced) | **none in-round** — the dispatch registry records spawns, not returns; the report's wave section must count returned reports separately from dispatched seats | this lesson and the report state both numbers (39 dispatched / 8 returned) with the counting command `ls .ufo/waves/round-37/w1/*.md \| wc -l` |
| scope (two claim texts' general clauses outran their counters' cells) | C1's "no PATH shim can move a pin verdict" held on all seven cells while unprivileged `LD_PRELOAD` interposition moved verdicts 4/7 and 3/7 on the landed gate (`residual/CritC1Kill.md` C27/C18); C2's "independent of the caller's `BASH_ENV`" held on all seven cells while a startup-exported `date` function reached the capture child through `BASH_FUNC_date%%` (`residual/RevC2FreshSeed.md`) | **none in-round** — no criterion required a claim text's general sentence to enumerate its counter's vectors or its child processes' inherited environment; QUALITY 54 added | claims.md §Erratum 6 (C1 narrowed to PATH-independence; loader-environment scrub + counter cell carried to r38) and §Erratum 5 (C2 narrowed to variable re-export independence; `BASH_FUNC_*` scrub + a genuinely-exported-function counter scenario carried to r38); the predicates P1/P2 are unaffected and every after-receipt stands |

## Gate

Rows added this round: **S071** (70 → 71 rows; census `validate` exit 0, W04 ×2 standing for
S051/S053). Opened locally 2026-10-23; no network.

- **S071** GNU coreutils `env(1)` manual, `-u`/`--unset=NAME` —
  `/usr/share/man/man1/env.1.gz`, decompressed lines 27–28, quote at line 28; canonical URL
  `https://www.gnu.org/software/coreutils/manual/coreutils.html#env-u` (printed as the roff
  tty-link at line 27, not fetched); coreutils 9.12
  (September 2026), installed `coreutils 9.12-2`; file SHA-256
  `4ae797e6e280da9d514bc94f3fbceffac5d0ceb62c197f78bb04bee84a78fb27`. Located quote (5 words
  by `printf '%s\n' '<quote>' | wc -w`): "remove variable from the environment". The page states
  the option's effect; the gate's choice to scrub `BASH_ENV` there is the lane's policy
  [INFERENCE].
- **Rejected candidates** (kept as reasoning, no row written): (a) a second `bash(1)` row for
  the `BASH_ENV` parameter-expansion paragraph (decompressed lines 2371–2382) — S068 already
  anchors `bash(1)` for the `BASH_ENV` scope; a second row would be a duplicate URL without a
  distinct scope. (b) The round-36 spot-check's S068 anchor-label supersede — a cosmetic
  anchor-cell nit, and this round's frontier budget went to the C2 mechanism source instead;
  carried as a round-38 candidate.
- **Status / recheck / used-by changes:** S068 used-by
  `corpus/knowledge/grep-pin-r35.md` → `corpus/knowledge/grep-pin-r35.md, corpus/knowledge/pin-capture-env-r37.md`;
  S070 used-by `corpus/knowledge/engine-swap-canary-r36.md` →
  `corpus/knowledge/engine-swap-canary-r36.md, corpus/knowledge/claim-pin-provenance-r37.md`
  (both old→new logged here per contract rule 2; the residual reviewer flagged the omission —
  `residual/RevFrontier.md` H1 — before this commit). Draft-time corrections before the row's
  first commit, logged for the record: S071's anchor label `OPTIONS` → `DESCRIPTION, -u option
  entry` (the page names no OPTIONS section) and the canonical URL added to the source cell
  (both `residual/RevFrontier.md` L1/L2).
- **Census receipt (this round):** `sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`
  → exit 0; after: 71 rows (A 65 / B 1 / C 5; mined 48 / queued 19 / rejected 4),
  malformed 0, W04 ×2. Before (round start): exit 0, 70 rows (A 64 / B 1 / C 5; mined 47 /
  queued 19 / rejected 4).
- **Knowledge admission candidates:** `corpus/knowledge/claim-pin-provenance-r37.md` (C1) and
  `corpus/knowledge/pin-capture-env-r37.md` (C2), admitted by the L1 after the wave's
  re-derivation and mutation evidence plus the L1's own fresh-seed runs.
- **Spot-check pointer (pending, not satisfied):** the non-author round-37 spot-check is the
  hyaku closure's; its verdict is not this lesson's to write. Marked **pending**, not satisfied.

Sourced claim: C2 rests on S071 (opened this round; the knowledge entry cites it as the
mechanism source for the `-u BASH_ENV` scrub). C1 additionally cites S070 (opened round 36).
