# ExecEnvFnHarness

## Verdict
Operability: the real child-Bash `export -f env` delivery reproduces all three attacks on the base gate and is blocked by the landed gate; calibration: C1 scored 2/7 on base and 7/7 landed.

## Evidence
- Second delivery harness used `/tmp/chousa-r38-envfn-final-risrcxjv`; it starts `bash -c`, defines the function in that child shell, `export -f env`, then `exec bash "$1" --pin "$2"`. The six gate paths were `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/controls/base-gate-r37.sh` and `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh`.
- Executed echo variant: `bash -c 'env() { local o=(); while (($#)); do case "$1" in -u) o+=("$1" "$2"); shift 2;; *) break;; esac; done; /usr/bin/env "${o[@]}" CHOUSA_GREP_PIN_ECHO=1 "$@"; }; export -f env; exec bash "$1" --pin "$2"' _ "$GATE" "$BASELINE"`.
- Executed root variant (foreign root is an exported environment value so the imported function receives it): `bash -c 'R38_FOREIGN_ROOT="$3"; export R38_FOREIGN_ROOT; env() { local o=(); while (($#)); do case "$1" in -u) o+=("$1" "$2"); shift 2;; *) break;; esac; done; /usr/bin/env "${o[@]}" CHOUSA_ROOT="$R38_FOREIGN_ROOT" "$@"; }; export -f env; exec bash "$1" --pin "$2"' _ "$GATE" "$BASELINE" "$FOREIGN_ROOT"`.
- Executed suppress variant: `bash -c 'env() { :; }; export -f env; exec bash "$1" --pin "$2"' _ "$GATE" "$BASELINE"`.
- For each created baseline, the control drift command was `/usr/bin/env -u BASH_FUNC_env%% -u BASH_ENV -u CHOUSA_ROOT -u CHOUSA_GREP_PIN_ECHO -u R38_FOREIGN_ROOT bash "$GATE" --drift "$BASELINE"`.

| Gate / attack | Pin and baseline observation | Drift observation |
|---|---|---|
| Base / echo | rc=0; `/tmp/chousa-r38-envfn-final-risrcxjv/base-echo.baseline`; 1 `GATE_GREP` line; `GATE_PIN: ok`, gate SHA `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8` | rc=1; `GATE_DRIFT: -GATE_GREP` |
| Base / root | rc=0; `/tmp/chousa-r38-envfn-final-risrcxjv/base-root.baseline`; foreign root `/tmp/chousa-r38-envfn-final-risrcxjv/base-root-foreign`; 0 `GATE_GREP` lines | rc=1; `GATE_DRIFT: -FINDING:CHAIN_SOURCE_MISSING -FINDING:CLAIM_SOURCE_MISSING -FINDING:POINTER_UNRESOLVED drift drift-sections drift_sections findings native refused root supported tallies tally verdict verified` |
| Base / suppress | rc=2; no baseline; `research-gate: --pin canonical capture failed (rc=0 verdict-lines=0 manifest-lines=0 schema-lines=0)` | Not run: no baseline |
| Landed / echo | rc=0; `/tmp/chousa-r38-envfn-final-risrcxjv/landed-echo.baseline`; 0 `GATE_GREP` lines; gate SHA `37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d` | rc=0; `GATE_DRIFT: none` |
| Landed / root | rc=0; `/tmp/chousa-r38-envfn-final-risrcxjv/landed-root.baseline`; 0 `GATE_GREP` lines | rc=0; `GATE_DRIFT: none` |
| Landed / suppress | rc=0; `/tmp/chousa-r38-envfn-final-risrcxjv/landed-suppress.baseline`; 0 `GATE_GREP` lines | rc=0; `GATE_DRIFT: none` |

- Independent original-channel C1 counter commands used existing `C1_TMP` directories and fresh seeds: `C1_TMP=/tmp/chousa-r38-c1-38201-adauos1d python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c1-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-37/controls/base-gate-r37.sh --seed 38201 --receipt /tmp/chousa-r38-c1-38201-adauos1d/receipt.json` and `C1_TMP=/tmp/chousa-r38-c1-38202-kd6rxerj python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c1-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 38202 --receipt /tmp/chousa-r38-c1-38202-kd6rxerj/receipt.json`.
- Observed counter output: base `FAIL env-fn-echo-scrub` (echo_lines=1, drift `GATE_DRIFT: -GATE_GREP`); `FAIL env-fn-root-move` (drift rc=1 with moved findings); `FAIL env-fn-suppress` (pin rc=2, no file); both env-override scenarios failed; `ENV_PIN_CAPTURE_MATCH=2/7`. Landed: all seven rows `PASS`, including echo/root/suppress and both `ENV_PROVENANCE` refusals; `ENV_PIN_CAPTURE_MATCH=7/7`.

## Findings
1. The harness's separately delivered Bash-exported function reproduces the base gate's echo baseline movement, foreign-root baseline drift, and suppress-induced capture failure. Base uses bare `env` at `base-gate-r37.sh:3921-3924`; the frozen C1 counter's raw `BASH_FUNC_env%%` channel and its function bodies are at `c1-count.py:60-70,131-147`.
2. All three attacks leave the landed gate with successful pins, zero captured `GATE_GREP` lines, and exact `GATE_DRIFT: none`. The landed capture invokes `$ENV_BIN` at `research-gate.sh:4001-4004`; its absolute GNU coreutils env resolution/refusal is at `research-gate.sh:458-522`.
3. Counter comparison corroborates separation on fresh seeds 38201 (base, 2/7) and 38202 (landed, 7/7); both wrote receipts only under `/tmp`.

## Limits
- C2 was not assessed. No build, lint, formatter, or full selftest was run.
- The landed gate explicitly retains the exported-`bash` function and `SHELLOPTS=noexec` limits (`research-gate.sh:469-472`); this evidence only establishes resistance to the tested exported `env` function.
