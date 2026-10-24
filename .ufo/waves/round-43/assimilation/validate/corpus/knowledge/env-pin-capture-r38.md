# env-pin capture — round 38

source: S072 (`/usr/share/info/bash.info.gz`, Node "Shell Functions" 3.3, decompressed
lines 1461–1464) + `corpus/evidence/round38/claims.md` (C1 body and Errata 1/5/6)
verified-at: 2026-10-24
recheck: on-release

## Mechanism

The gate's canonical pin capture spawned its child through a BARE `env` invocation.
An exported shell function is delivered to every child shell — bash.info, Node "Shell
Functions": "Functions may be exported so that child shell processes (those created when
executing a separate shell invocation) automatically have them defined" (S072, lines
1461–1463; the `BASH_FUNC_name%%` transport encoding itself is a wave measurement, not
stated in that manual). A caller-exported function named `env` therefore received the
capture call itself. Three attacks measured on the pre-round gate (both delivery
mechanisms: a raw `BASH_FUNC_env%%` env var and a real child `export -f env`):

- echo re-add: the function re-adds `CHOUSA_GREP_PIN_ECHO=1`; the baseline embeds one
  `GATE_GREP:` line and a plain `--drift` reports a phantom `-GATE_GREP` (rc 1);
- root move: the function exports `CHOUSA_ROOT=<foreign>`; the capture runs against the
  foreign root and the drift names a token list instead of `none`;
- suppress: the function discards the invocation; the capture is empty and `--pin`
  refuses (rc 2, no baseline).

The landed gate resolves ONE pinned absolute `env` at startup (default `/usr/bin/env`,
verified GNU coreutils via its own `--version`; `RESEARCH_GATE_ENV` override must be
absolute + GNU-reporting, refused exit 2 `ENV_PROVENANCE` before any mode runs) and the
capture child runs through `"$ENV_BIN"`. Measured: base gates `a7d3922c…` (pre-round-37)
and `9fcac047…` (pre-round-38, `.ufo/waves/round-38/controls/base-gate-r38.sh`) each
score `ENV_PIN_CAPTURE_MATCH=2/7` under `corpus/evidence/round38/c1-count.py`; the
landed gate scores 7/7 across construction seeds 38001/38011, wave-1 seeds
38211/38231/38251, wave-2 seeds 38411/38431 (receipts under
`corpus/evidence/round38/receipts/`, each `VERIFY: ok`).

## The frozen observable and its narrowing

The claim as landed measures function-export interposition on the capture's `env`
invocation plus the override refusal shape. What the seven cells do NOT measure (frozen
as claims.md §Errata 6, demonstrated by wave seats):

- the PATH half: a mutant capture using PATH-resolved `command env` still scores 7/7
  while being PATH-poisonable (w1/RevErrataCtx, seed 38207); MutGateC1 M3 (relative-
  override refusal removed) and M4 (hardcoded `/usr/bin/env`, override ignored) also
  pass 7/7; an unconditional-override-refusal mutant passes 7/7 (w2/W2RevC1Final) — no
  cell covers the positive override-honoured witness or the relative-refusal;
- sibling-name witnesses are NOT uniform: an exported `date` function still embeds a
  `GATE_GREP:` line (with `CHOUSA_GREP_PIN_ECHO=1` live) and moves the baseline — the
  Erratum-5 symptom on a sibling name — while exported `grep`/`sha256sum` functions are
  invoked zero times (those binaries are already pinned absolutely; w2/W2CritKillC1Final,
  w2/W2ScribeKnowledgeC1);
- the `bash` name splits: an exported `bash` FUNCTION hits only the five
  verify_all_section shell-outs (`research-gate.sh:3642`), never the capture; a PATH
  `bash` shim DOES reach the capture's grandchild lookup and poisons it
  (w2/W2LabBashFn, seed 38473);
- ambient option channels: `POSIXLY_CORRECT` was a false-kill channel (moved the landed
  gate 7/7→2/7 with bytes unchanged — the gate now unsets it at startup and the counters
  scrub it from the scenario env); `TMPDIR` remains a live named channel (r37 debt);
- loader environment: an unprivileged `LD_PRELOAD` interposer on `/usr/bin/env` strips
  the `-u` scrub (moves the verdicts to 2/7 through the harness) — the Erratum-6 class
  on a second binary, carried debt with the sha256sum-child scrub;
- `SHELLOPTS=noexec` exits 0 with no baseline — unfixable in-body (bash applies `-n`
  before the script executes), carried as named debt since the r37 residual.

## Harness hardening that carries the measurement (Errata 5/8/10)

The counter scrubs `BASH_ENV`/`ENV`/`SHELLOPTS`/`BASHOPTS`/`POSIXLY_CORRECT`/`PYTHON*`
and the attack families from the scenario env (a caller `BASH_ENV` forge moved even the
r37 gate to 7/7 pre-fix — w1/RevCounterC1 seed 38219), pins `/usr/bin/bash`, asserts the
anchored `research-gate: ENV_PROVENANCE refused:` stderr line, and hashes the frozen
expectation table before and after the run. Pre-registered r39 cells: PATH env shim,
PATH bash shim, hostile-drift coverage, positive override witness, relative-override
refusal, loader scrub, `bash`-function section calls.
