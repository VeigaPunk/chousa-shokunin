# chousa-r38.CritC1Kill

## Verdict

C1 survives. No kill beyond its seven cells on the landed gate: the env-function channel
is closed structurally (no bare `env` on the pin path; capture runs through `"$ENV_BIN"`
absolute) and behaviorally (7/7 on fresh seeds 38201/38202; BASH_ENV-delivered env
function resisted). Every working beyond-cell attack channel is a limit `claims.md`
already names — each re-executed below with exact commands and outputs, plus two
mechanism-precision notes where the named text is imprecise (its substance holds).

## Evidence

Gate under test: `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh`,
sha256 `37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d` (matches the
frozen candidate). Base control sha256 `a7d3922c…54e8` matches. Seeds 38201–38206
(≥ 38201), `C1_TMP` pre-created; fixtures under `/tmp/critc1kill`.

Baseline (fresh seeds, landed gate): `c1-count.py --gate tools/research-gate.sh --seed 38201` →
`ENV_PIN_CAPTURE_MATCH=7/7`, exit 0; receipt binds `gate_sha256=37e2b996…`, `counter_sha256`,
`expect_sha256`, `receipt_sha256`, `predicate_holds=true`. Seed 38202 → 7/7. Control:
`--gate .ufo/waves/round-37/controls/base-gate-r37.sh`, seed 38203 → 2/7 (the five separation
cells fail as the frozen "before" describes: echo re-add `echo_lines=1`/`-GATE_GREP`, root
re-add foreign tokens, suppress rc=2 no baseline, missing/fake override ignored).

Structural check: `grep -nE '(^|[^A-Za-z0-9_/$"{}-])env (-|[A-Za-z])' tools/research-gate.sh`
→ every bare `env` invocation lies between lines 4311–8355, i.e. inside `run_selftest()`
(defined line 4225). The pin/drift/verify-all path has none; the capture (line 4002) uses
`"$ENV_BIN" -u … bash "$SELF" verify-all …`.

Beyond-cell attacks (each: pin under the hostile env, then clean-env `--drift`):

1. Exported `bash` function, suppress body, delivered the counter's way
   (`env 'BASH_FUNC_bash%%=() { :; }' bash tools/research-gate.sh --pin …`) → pin rc=0,
   baseline sections: `SECTION structure/claims/chain/sweeps/integrity state=run
   verdict=DRIFT findings=1` (all five `VERIFY_ALL_SECTION_UNAVAILABLE`). A logging body
   (`echo FIRED …; command bash "$@"`) fires exactly 5× during one real `--pin`
   (`fnlog9`: verify, verify-claims, verify-chain, verify-sweeps, verify-integrity).
   Root-move body (`CHOUSA_ROOT=/tmp/critc1kill/foreign-root command bash "$@"`) →
   `GATE_DRIFT: -FINDING:CHAIN_SOURCE_MISSING -FINDING:CLAIM_SOURCE_MISSING
   -FINDING:POINTER_UNRESOLVED …` rc=1 — the r37 root-move token signature. Echo body
   moves nothing (sub-gate `GATE_GREP` lines are swallowed by the section runner's
   VAS_OUT parsing; baseline 0 lines, drift `none`).
2. Fake `bash` binary via caller PATH (`fakebin/bash` = `CHOUSA_GREP_PIN_ECHO=1 exec
   /usr/bin/bash "$@"`, `PATH=/tmp/critc1kill/fakebin:$PATH`) → pin rc=0, baseline
   embeds 1 `GATE_GREP:` line, clean-env drift `GATE_DRIFT: -GATE_GREP` rc=1. Foreign-root
   variant (`CHOUSA_ROOT=… exec …`) → the full r37 root-move token set, rc=1.
3. LD_PRELOAD on `/usr/bin/env` (`inject3.so` interposing `execvp` to re-set
   `CHOUSA_GREP_PIN_ECHO=1` after env applies `-u`; isolation proof
   `CHOUSA_GREP_PIN_ECHO=1 LD_PRELOAD=inject3.so /usr/bin/env -u CHOUSA_GREP_PIN_ECHO
   bash -c 'echo v=${CHOUSA_GREP_PIN_ECHO:-UNSET}'` → `v=1`): full attack
   `CHOUSA_GREP_PIN_ECHO=1 LD_PRELOAD=… bash gate --pin` → rc=0, baseline 1 `GATE_GREP`
   line, drift `-GATE_GREP` rc=1.
4. `RESEARCH_GATE_ENV` wrapper that self-reports GNU (`fake-env`: `--version` prints
   `env (GNU coreutils) 9.9`; else strips `-u` pairs, execs /usr/bin/env):
   `RESEARCH_GATE_ENV=/tmp/critc1kill/fake-env CHOUSA_GREP_PIN_ECHO=1 bash gate --pin`
   → rc=0, baseline 1 `GATE_GREP` line, drift `-GATE_GREP` rc=1. Control without the echo
   var → 0 lines, capture otherwise normal.
5. BASH_ENV delivery, env function (`be-envfn.sh` defines+exports `env` re-adding the
   echo var): pin rc=0, 0 `GATE_GREP` lines, drift `none` — RESISTED (pin is absolute;
   `-u BASH_ENV` scrubs the child). BASH_ENV echo-var file (`CHOUSA_GREP_PIN_ECHO=1`):
   outer gate echoes `GATE_GREP` to its own stderr but the baseline has 0 lines and
   drift under the same BASH_ENV is `none` — RESISTED.

Counter-harness runs (ambient hostile env around `c1-count.py` itself):
`env LD_PRELOAD=/tmp/critc1kill/inject3.so … c1-count.py --seed 38204` →
`ENV_PIN_CAPTURE_MATCH=2/7` (all five capture cells FAIL with `echo_lines: 1`; the two
override-refusal cells pass). `env 'BASH_FUNC_bash%%=() { :; }' … c1-count.py --seed
38205` → `ENV_PIN_CAPTURE_MATCH=7/7` (the counter's `base_env()` scrubs `BASH_FUNC_*`;
`LD_PRELOAD` is not scrubbed).

## Findings

1. No kill of the frozen C1 claim. The claim's scope is the caller-exported `env`
   function; it cannot interpose on the capture: 7/7 on fresh seeds, and delivery via
   `BASH_ENV` (a channel the seven cells do not exercise) is equally resisted. The r37
   base gate scores 2/7 on the same fresh seed, so the separation is live.
2. Named limit "caller-exported function named `bash`" — CONFIRMED. It fires on all five
   capture section calls; suppress distorts every section to
   `VERIFY_ALL_SECTION_UNAVAILABLE`; root-move reproduces the exact r37 token signature.
   Mechanism precision: the echo vector is invisible through this channel (section
   runner re-emits only parsed verdict/tally/finding lines; each sub-gate's stderr
   `GATE_GREP` echo is discarded), so a function moves the capture via suppress/root,
   not via echo. The claims.md text names the limit without a vector, so this is a
   clarification, not a defect.
3. The grandchild-`bash` residual the limit carries is real and, via the caller's PATH,
   stronger than the function vector: a fake `bash` binary is what the capture child
   itself is exec'd as, so it poisons the child's own startup echo (baseline `GATE_GREP`
   line + phantom `-GATE_GREP`) and reproduces the root move. The claims.md limit names
   the *function* class; the PATH-binary mechanism is the same residual debt witnessed
   from another angle — limit-confirmation either way, frontier fix must pin/scrub the
   child's `bash` lookup (absolute bash resolved at gate startup, or PATH scrub on the
   capture env), not just refuse functions.
4. Named limit "LD_PRELOAD could strip the `-u` flags" — CONFIRMED end-to-end on the
   landed gate (`inject3.so`: `execvp` interposition re-injecting the var after env's
   scrub; `-u` argv surgery and `unsetenv` interposition do not bite coreutils env, but
   the exec-path interposition does — same named class, scrub defeated). Run through the
   counter harness this scores 2/7, i.e. the measurement instrument itself is exposed to
   the named loader channel; per claims.md this is the gate's carried debt
   (`env -u LD_PRELOAD …` scrub direction), not a C1 kill.
5. Named limit "a binary that lies about `--version`" — CONFIRMED: the GNU-reporting
   wrapper is accepted as `RESEARCH_GATE_ENV` and moves the baseline.
6. Tooling note (harness, not gate): a `BASH_FUNC_*` exported from my own shell between
   commands did NOT reach gate children (0 fires); the same string passed via `env VAR=…`
   or the counter's `subprocess env=` fired 5× — delivery must cross exec via the
   environment; all conclusions use env-delivery.
7. Install record: no tools installed/upgraded; gcc 16.2.1 (already present) built only
   `/tmp/critc1kill/inject3.so` (plus discarded `strip.so`/`inject.so` attempts).

## Limits

- SHELLOPTS=noexec and hostile TMPDIR were not re-run: both are named limits (noexec
  re-demonstrated in claims.md; hostile TMPDIR fails closed at mktemp, exit 2).
- The counter-harness 2/7 under ambient LD_PRELOAD is reported as the named loader-env
  limit; whether the counter *should* scrub `LD_PRELOAD` in `base_env()` is a
  calibration call for the C2 seats.
- All attack fixtures live under `/tmp/critc1kill`; nothing outside my report file
  and temp dirs was written. Receipts in `/tmp/critc1kill/`: `c1-s38201.json`,
  `c1-s38202.json`, `c1-base-s38203.json`, `c1-s38204-ldpreload.json`,
  `c1-s38205-bashfn.json`, `c1-s38206-ldpreload.json`.
