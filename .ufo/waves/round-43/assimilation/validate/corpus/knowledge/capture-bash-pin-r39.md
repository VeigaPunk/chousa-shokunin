# capture-bash-pin-r39

source: corpus/evidence/round39/claims.md (C1); S071 (`env(1)` — the capture child's `-u` scrub semantics, re-opened 2026-10-24, quote re-located at decompressed lines 27–28, file SHA-256 `4ae797e6…fb27`); S072 (exported functions reach child shells — the BASH_FUNC channel)
verified-at: 2026-10-24 (gate `89022659…` working; receipts bind the landed revision)
recheck: re-run `python3 corpus/evidence/round39/c1-count.py --gate tools/research-gate.sh --seed N --receipt F` and the base/mutant controls named below

Round-39 note: the capture's grandchild and section children run through ONE
pinned absolute `bash`.

## Mechanism

`bash_pin_init` resolves and verifies `BASH_BIN` beside the round-35 grep pin
and the round-38 env pin: default probe of `/usr/bin/bash` then `/bin/bash`,
each verified by its own `--version` reporting `GNU bash` (bounded by an
absolute `timeout(1)` when one exists); `RESEARCH_GATE_BASH` overrides and
must be an absolute path to a GNU-reporting binary, else the gate refuses
exit 2 with an anchored `research-gate: BASH_PROVENANCE refused:` line before
any record is read. Three call sites consume the pin:

1. `gate_canonical_capture` — the capture grandchild (was a bare `bash`, the
   round-38 claims Erratum 6(c) measured witness).
2. `verify_all_section` — every verify-all section child (was a bare
   `bash "$SELF" "$mode" …`; reachable from the capture, and a caller PATH
   `bash` shim there made whole sections read
   `VERIFY_ALL_SECTION_UNAVAILABLE` on an unchanged gate — found by the
   round-39 construction run when the suppress cell's drift showed
   `-FINDING:VERIFY_ALL_SECTION_UNAVAILABLE +FINDING:REF_UNRESOLVED` token
   churn instead of `GATE_DRIFT: none`).
3. The `BASH_BIN` assignment is readonly-guarded like the env pin.

The capture child `env` scrub (`env -u CHOUSA_GREP_PIN_ECHO …`, S071) runs
before the pinned bash, so a PATH `bash` shim is consulted by neither.

## Measured

- Before (pre-round gate `0447ad14…`, committed at
  `.ufo/waves/round-39/controls/base-gate-r39.sh`): the r39 c1 counter scores
  `7/8` (seed 39001, `corpus/evidence/round39/receipts/c1-base-s39001.json`);
  the eighth family fails live: `path_bash_shim_echo` embeds one `GATE_GREP:`
  line and drifts `GATE_DRIFT: -GATE_GREP` (the hostile-drift vector),
  `path_bash_shim_suppress` kills the capture (`pin_rc=2`, no baseline),
  `override_relative_refused` is ignored (`pin_rc=0`).
- After (landed gate): `8/8` on seeds 39011/39111
  (`receipts/c1-after-s39011.json`, `receipts/c1-after-s39111.json`), both
  receipts `VERIFY: ok` under `round39/verify-receipts.py`.
- Discrimination: the PATH-`env` mutant (`mut-gate-path-env.sh`, sha256
  `e1251030…`, the capture's `"$ENV_BIN"` → bare `env`) scores `4/8` (seed
  39013): the three r38 `BASH_FUNC_env%%` cells re-open (bash resolves the
  function before PATH) AND `path_env_shim_echo` fails (`echo_lines=1`,
  drift `-GATE_GREP`) — the counter distinguishes a PATH-poisonable capture
  from the pinned one in both name directions.
- Gate selftest 272 → 275 (cases 273–275: `pin-bash-path-shim`,
  `bash-pin-override-missing`, `bash-pin-override-fake`), PASS on the landed
  bytes; the r1 archive observable, claims 17/17, chain 17/22, the broken
  control and the integrity-r7 composition all hold
  (`VERDICT_BEARING_EXPORTS=3/3`).

## Limits (named, per claims.md §Limits)

The pin covers the `bash` NAME only: `mktemp`, `sed` (capture and
normalization) and `rm` stay bare; the `BASH_FUNC_*` channel is closed only
for the pinned names; the children's loader environment (`LD_PRELOAD` class)
is the caller's; `SHELLOPTS=noexec` precedes the whole body; a binary that
lies about `--version` is out of reach. The PATH `env` shim cell is a HOLD on
the landed gate — the discrimination lives in the committed mutant control,
not in a gate that must resist it by itself.
