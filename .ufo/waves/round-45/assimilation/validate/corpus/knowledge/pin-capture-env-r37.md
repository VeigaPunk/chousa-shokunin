# Pin-capture environment — BASH_ENV cannot move a baseline

Lane: chousa. Round 37 (C2, freshness — pin/drift re-derivation independence).
Surface: `tools/research-gate.sh` (`gate_canonical_capture`, the `--pin` /
`--drift` contract), `corpus/evidence/round37/c2-count.py`.

source: S071 (coreutils `env(1)` `-u`/`--unset` semantics, opened 2026-10-23 —
`/usr/share/man/man1/env.1.gz`, decompressed lines 27–28, quote at line 28,
canonical URL `https://www.gnu.org/software/coreutils/manual/coreutils.html#env-u`
printed as the roff tty-link at line 27, file SHA-256 `4ae797e6…fb27` — the tool
the capture uses to scrub the inherited environment); S068 (bash(1) `BASH_ENV`,
the scrubbed startup-file mechanism, opened round 35 —
`/usr/share/man/man1/bash.1.gz`, INVOCATION decompressed lines 388–404, quote at
391–395, file SHA-256 `b68beb3e…dffe`); the lane gate
`tools/research-gate.sh` (landed `9fcac047…cf39`); frozen design
`corpus/evidence/round37/claims.md`; receipts
`corpus/evidence/round37/receipts/c2-{base-s37021,after-s37021,after-s37941,after-s37961,after-s37721}.json`;
wave seat reports `.ufo/waves/round-37/w1/ExecC2{Base,Landed}Rederive.md`,
`ExecMutGateC2.md`; control gate `.ufo/waves/round-37/controls/base-gate-r37.sh`.
verified-at: 2026-10-23 (landed gate SHA-256 `9fcac047…cf39`;
`PIN_CAPTURE_ENV_MATCH=7/7` on seeds 37021, 37211, 37311, 37721, 37941, 37961)
recheck: on-release (`python3 corpus/evidence/round37/c2-count.py --gate tools/research-gate.sh --seed <n>` → `7/7` with `predicate_holds=true`; any run below 7/7 against the landed gate kills the claim)

## What changed

Round 36's R1 scrubbed `CHOUSA_GREP_PIN_ECHO` from the `--pin` capture child,
but the inner bash still sourced the caller's `BASH_ENV`: a startup file that
re-exported the scrubbed variable embedded a `GATE_GREP:` receipt line in the
baseline, and a later plain `--drift` reported phantom drift on an unchanged
gate (round-36 claims §Erratum 7). The fix adds `-u BASH_ENV` (with the other
scrubs) to the capture child's `env` line: per S071 the variable is absent
from the child's environment, so the startup file is never read — the pinned
baseline is independent of the caller's `BASH_ENV`.

## The seven scenarios (counter `c2-count.py`)

`hold-plain` / `hold-benign` pin the capture contract; `env-echo-pin` /
`env-echo-drift` export a startup file re-exporting `CHOUSA_GREP_PIN_ECHO`;
`env-fn-echo-pin` plants the echo through an exported shell function;
`env-root-pin` moves `CHOUSA_ROOT` in the startup file; `env-strict-pin`
re-exports `CHOUSA_STRICT`. Every scenario asserts pin_rc=0, exactly zero
`GATE_GREP:` lines in the pinned file, and a later plain drift reporting
`GATE_DRIFT: none`. Base gate `a7d3922c…` scores 3/7 (the four separation
cells fail exactly as the vulnerability predicts); landed gate `9fcac047…`
scores 7/7 on every committed after-receipt (the committed base receipt
`c2-base-s37021.json` scores 3/7 against the base gate by design; corrected
round 38 after the round-37 receipt audit finding L1).

## Named limits (from claims.md §Limits, frozen)

- The gate process itself sourced the caller's `BASH_ENV` before its body
  ran, so a startup file can still define functions IN the gate process; C2
  asserts file contents and the drift verdict, not a byte-identical
  subprocess environment.
- `--posix`/`ENV`, `SHELLOPTS`/`BASHOPTS` and a hostile `TMPDIR` are not
  covered — named debt, not silently closed.
- Coverage is `BASH_ENV` only, by design: the kill rule names the vector.

## The no-harm note the wave surfaced

One wave seat ran the pinned no-harm battery with `--root .` (lane root)
instead of the recorded `--root ..` (fleet root) and read the resulting
out-of-corpus refusals as harm (`.ufo/waves/round-37/w1/ExecNoHarmPin.md`).
The L1 re-ran the battery with the recorded commands: claims 17/17 CLEAN,
chain 17/22 CLEAN, broken control 1/2 DRIFT, archives 3/3 — no harm (see
lesson `corpus/lessons/round-37.md` §Mistakes).
