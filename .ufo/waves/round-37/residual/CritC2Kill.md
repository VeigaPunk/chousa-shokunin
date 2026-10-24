# CritC2Kill — residual C2 falsification

## Finding

**No in-scope C2 kill established by the assigned vectors.** This is a residual critic finding, not a claim judgment or admission. I ran 28 attack variants plus one clean control, each as `--pin` followed by an independent plain `--drift` (58 gate invocations). Five variants produced a changed baseline and phantom drift; all five fall under limits already frozen in `claims.md:114-117`. Four further variants produced no baseline, also under named limits. Nineteen attack variants, plus the control, held the capture invariant.

The source and byte-exact scratch gate both hashed to `9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39`. The required read-only `git rev-parse master` returned `b905217a7dfdcf58be1f0a4c0bf5f2d2d32a2d65`. These tests did not modify the gate and did not rerun or redefine the frozen seven-cell counter.

## Strongest counterexamples and impacted axes

1. **Exported `env` function survives the outer startup.** `BASH_ENV-exportf-env-reinsert` defines `env()`, uses `export -f env`, preserves the capture's `-u` arguments, then inserts `CHOUSA_GREP_PIN_ECHO=1` after those arguments. The capture's bare `env` at gate lines 3935-3938 dispatches to that function before any external scrub can help. Observed: pin 0, one embedded `GATE_GREP:` line, plain drift 1 with exactly `GATE_DRIFT: -GATE_GREP`. An independent exported-function launcher with **no BASH_ENV at all** produces the same body hash and result. This confirms the named parent-function limit, not an unexcluded C2 kill.
2. **`SHELLOPTS=noglob` invents a sweep hit.** The unchanged canonical fixture reports literal `lib/ghost*.md` as a hit, changing sweeps from CLEAN to DRIFT and composed findings from 1 to 2. Pin 0, plain drift 1. This is the named SHELLOPTS limit.
3. **Writable hostile `TMPDIR` needs no race.** Placing capture temp directories under a `.config` component triggers existing session-path refusal logic. Pin 0, claims and chain refuse `lib/primary.md`, and plain drift 1. A startup that merely re-exports this TMPDIR reproduces the same capture hash: using BASH_ENV as the delivery channel does not erase the explicitly named TMPDIR exclusion.
4. **`SHELLOPTS=noexec` gives false pin success.** Both alone and with `BASHOPTS=extglob`, pin exits 0 with no stdout, no stderr, and **no baseline file**. Plain drift exits 2 for the missing baseline, not a phantom drift verdict. This is an operability defect inside the named shell-option exclusion. Missing/unwritable TMPDIR correctly refuses pin with exit 2.

Impacted declared axes: **freshness** for the five polluted-baseline cases; **operability** for the false-success/no-baseline and setup-failure cases. No C1 measurement, axis score, trade acceptance, or Rust-judge verdict is asserted.

## Smallest safe correction

For the frozen C2 claim, these observations require **no scope expansion and no gate edit**: retain its exact Limits qualifier and carry the witnessed debt forward. Do not describe seven-cell C2 success as arbitrary startup/environment hermeticity or safe pinning under hostile shell options.

For the specific exported-`env` witness, calling one fixed absolute `env` executable instead of the bare function-resolvable name would close that witness [INFERENCE]; it would **not** solve arbitrary functions already installed in the parent shell. Likewise `noexec` is applied before the script body executes, so adding another in-body scrub cannot repair that witness [INFERENCE]. A broad guarantee would need a separately specified, evidenced pre-startup boundary; none is proposed as an admission substitute here. These are fixable debt items, not grounds to silently redefine the frozen claim or credit an unmeasured improvement.

## Method and scope controls

- All executions use the exact scratch copy; its own gate SHA in successful pin output matches the landed digest.
- Each case has its own working directory, capture temp parent, and baseline path under /tmp. `env -i` supplies a fixed PATH, empty scratch HOME, C locale, and that case's temp parent; only the specified attack variables/options are added to pin. Plain drift does not retain those attack additions.
- I compared the normalized canonical **body**, not volatile baseline-header timestamps, against the plain control, and separately counted lines beginning exactly `GATE_GREP: `. The canonical JSON manifest is expected baseline content; the extra grep receipt is the pollution under test.
- Bash readonly option variables are injected through real process environments, not assigned unsuccessfully inside an already-running Bash.
- ENV startup has an on-disk execution marker. It was not read by either noninteractive POSIX variant, and was read by the interactive variant. The interactive outer shell printed terminal/history diagnostics and a grep receipt, but its pinned body still matched the control; outer diagnostics are not embedded-capture failures.
- Unreadability is real: uid/euid 1000, mode-000 startup reports `os.access(..., R_OK)=false`; mode-000 TMPDIR reports `os.access(..., W_OK)=false`.
- The CHOUSA_ROOT startup is itself reached through a symlink and names a 16-hop directory-symlink chain terminating in a farm whose lib/noise entries point to foreign material. That capture remained byte-identical to the control.
- Extdebug could not start because this host lacks `/usr/share/bashdb/bashdb-main.inc`; Bash explicitly disabled debugging. Its unchanged capture is not evidence about an active debugger. No tool installation was needed or performed.
- No network, delegation, other agent/judge runtime, git/jj mutation, or index mutation. This seat's only lane write is this report. Fixtures, runner, captures, and receipt remain under the named /tmp workspace.

## Per-vector table

`same` means byte-equal normalized body; echo is the number of embedded grep-receipt lines. `missing` means there is no pinned baseline, so the following exit-2 drift is not called phantom drift.

| Vector | Pin rc / baseline / body / echo | Plain drift rc / result | Kill-or-limit classification |
|---|---|---|---|
| `control-plain` | 0 / yes / same / 0 | `0 / GATE_DRIFT: none` | Control; no kill |
| `ENV-posix-noninteractive` | 0 / yes / same / 0 | `0 / GATE_DRIFT: none` | No kill; invariant held in this excluded vector, not confirmation of a general guarantee |
| `ENV-posix-interactive` | 0 / yes / same / 0 | `0 / GATE_DRIFT: none` | No kill; invariant held in this excluded vector, not confirmation of a general guarantee |
| `ENV-SHELLOPTS-posix` | 0 / yes / same / 0 | `0 / GATE_DRIFT: none` | No kill; invariant held in this excluded vector, not confirmation of a general guarantee |
| `SHELLOPTS-posix` | 0 / yes / same / 0 | `0 / GATE_DRIFT: none` | No kill; invariant held in this excluded vector, not confirmation of a general guarantee |
| `SHELLOPTS-noexec` | 0 / no / missing / 0 | `2 / no GATE_DRIFT line; baseline missing` | CONFIRMED NAMED LIMIT: SHELLOPTS (claims.md:114-117); no baseline, not phantom drift |
| `SHELLOPTS-noexec-extglob` | 0 / no / missing / 0 | `2 / no GATE_DRIFT line; baseline missing` | CONFIRMED NAMED LIMIT: SHELLOPTS (claims.md:114-117); no baseline, not phantom drift |
| `SHELLOPTS-noglob` | 0 / yes / changed / 0 | `1 / GATE_DRIFT: -FINDING:SWEEP_CLAIM_FALSE drift drift-sections drift_sections findings hit native tally verdict verified` | CONFIRMED NAMED LIMIT: SHELLOPTS (claims.md:114-117); not a kill |
| `SHELLOPTS-errtrace-functrace` | 0 / yes / same / 0 | `0 / GATE_DRIFT: none` | No kill; invariant held in this excluded vector, not confirmation of a general guarantee |
| `BASHOPTS-failglob` | 0 / yes / same / 0 | `0 / GATE_DRIFT: none` | No kill; invariant held in this excluded vector, not confirmation of a general guarantee |
| `BASHOPTS-nullglob` | 0 / yes / same / 0 | `0 / GATE_DRIFT: none` | No kill; invariant held in this excluded vector, not confirmation of a general guarantee |
| `BASHOPTS-inherit_errexit` | 0 / yes / same / 0 | `0 / GATE_DRIFT: none` | No kill; invariant held in this excluded vector, not confirmation of a general guarantee |
| `BASHOPTS-extdebug` | 0 / yes / same / 0 | `0 / GATE_DRIFT: none` | No kill; invariant held in this excluded vector, not confirmation of a general guarantee |
| `BASHOPTS-nocasematch` | 0 / yes / same / 0 | `0 / GATE_DRIFT: none` | No kill; invariant held in this excluded vector, not confirmation of a general guarantee |
| `TMPDIR-missing` | 2 / no / missing / 0 | `2 / no GATE_DRIFT line; baseline missing` | CONFIRMED NAMED LIMIT: TMPDIR (claims.md:114-117); no baseline, not phantom drift |
| `TMPDIR-no-permission` | 2 / no / missing / 0 | `2 / no GATE_DRIFT line; baseline missing` | CONFIRMED NAMED LIMIT: TMPDIR (claims.md:114-117); no baseline, not phantom drift |
| `TMPDIR-session-path` | 0 / yes / changed / 0 | `1 / GATE_DRIFT: -FINDING:CHAIN_SOURCE_SESSION -FINDING:CLAIM_SOURCE_SESSION -FINDING:POINTER_UNRESOLVED drift drift-sections drift_sections findings native refused supported tallies tally verdict verified` | CONFIRMED NAMED LIMIT: TMPDIR (claims.md:114-117); not a kill |
| `TMPDIR-symlink` | 0 / yes / same / 0 | `0 / GATE_DRIFT: none` | No kill; invariant held in this excluded vector, not confirmation of a general guarantee |
| `TMPDIR-newline` | 0 / yes / same / 0 | `0 / GATE_DRIFT: none` | No kill; invariant held in this excluded vector, not confirmation of a general guarantee |
| `CDPATH-decoy` | 0 / yes / same / 0 | `0 / GATE_DRIFT: none` | No kill; invariant held |
| `CDPATH-newline` | 0 / yes / same / 0 | `0 / GATE_DRIFT: none` | No kill; invariant held |
| `BASH_ENV-directory` | 0 / yes / same / 0 | `0 / GATE_DRIFT: none` | No kill; invariant held |
| `BASH_ENV-unreadable` | 0 / yes / same / 0 | `0 / GATE_DRIFT: none` | No kill; invariant held |
| `BASH_ENV-root-symlink-farm` | 0 / yes / same / 0 | `0 / GATE_DRIFT: none` | No kill; invariant held |
| `BASH_ENV-exportf-benign` | 0 / yes / same / 0 | `0 / GATE_DRIFT: none` | No kill; invariant held |
| `BASH_ENV-exportf-env-reinsert` | 0 / yes / changed / 1 | `1 / GATE_DRIFT: -GATE_GREP` | CONFIRMED NAMED LIMIT: parent-shell functions (claims.md:114-117); not a kill |
| `exportf-env-without-BASH_ENV` | 0 / yes / changed / 1 | `1 / GATE_DRIFT: -GATE_GREP` | CONFIRMED NAMED LIMIT: parent-shell functions (claims.md:114-117); not a kill |
| `BASH_ENV-sets-TMPDIR-session-path` | 0 / yes / changed / 0 | `1 / GATE_DRIFT: -FINDING:CHAIN_SOURCE_SESSION -FINDING:CLAIM_SOURCE_SESSION -FINDING:POINTER_UNRESOLVED drift drift-sections drift_sections findings native refused supported tallies tally verdict verified` | CONFIRMED NAMED LIMIT: TMPDIR (claims.md:114-117); not a kill |
| `BASH_ENV-exports-BASHOPTS-failglob` | 0 / yes / same / 0 | `0 / GATE_DRIFT: none` | No kill; invariant held in this excluded vector, not confirmation of a general guarantee |

## Local evidence references

- Frozen C2: `corpus/evidence/round37/claims.md:60-96`; exact named limits at `107-121`, especially `114-119`.
- Landed canonical capture: `tools/research-gate.sh:3922-3956`; bare env call and BASH_ENV scrub at `3935-3938`.
- Pin/drift public contract: gate `221-260`; body capture validity checks `3939-3952`; pin and drift output/exit handling `4063-4156`.
- Prior landed-wave report was read only for context: `.ufo/waves/round-37/w1/ExecC2LandedRederive.md:1-31`. Its successful measurements were not rerun.
- Initial read of the residual report directory returned "Path ... not found"; no existing seat report was overwritten during testing.

Scratch workspace: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx`

Machine-readable command records and capture bodies: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/vectors.json`. The exact runner source is embedded below so the report does not depend on retaining /tmp.

## Commands, outputs, and exit codes

These are all externally executed top-level commands, including every gate subprocess spawned by the runner. Commands are rendered verbatim as shell-quoted argv, with cwd recorded separately; stdout and stderr are preserved separately, not silently merged or trimmed. An `(empty)` annotation denotes an empty stream and is not process output. Read tools and in-process Python file/fixture preparation do not expose a process exit code and are recorded separately below.

### Required lane-tip read

cwd: `/tmp`

```sh
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master
```

stdout:
```text
b905217a7dfdcf58be1f0a4c0bf5f2d2d32a2d65
```
stderr: (empty). Exit code: **0**.

### Vector runner

cwd: `/tmp`

```sh
/usr/bin/python3 /tmp/chousa-r37-CritC2Kill-jx8vuxvx/run_vectors.py
```

stdout:
```text
GATE_SHA256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
CASES=29
{"baseline_echo_lines": [], "baseline_exists": true, "capture_matches_control": true, "drift_lines": ["GATE_DRIFT: none"], "fixture_checks": {}, "id": "control-plain"} pin_rc=0 drift_rc=0
{"baseline_echo_lines": [], "baseline_exists": true, "capture_matches_control": true, "drift_lines": ["GATE_DRIFT: none"], "fixture_checks": {"ENV_startup_ran": false}, "id": "ENV-posix-noninteractive"} pin_rc=0 drift_rc=0
{"baseline_echo_lines": [], "baseline_exists": true, "capture_matches_control": true, "drift_lines": ["GATE_DRIFT: none"], "fixture_checks": {"ENV_startup_ran": true}, "id": "ENV-posix-interactive"} pin_rc=0 drift_rc=0
{"baseline_echo_lines": [], "baseline_exists": true, "capture_matches_control": true, "drift_lines": ["GATE_DRIFT: none"], "fixture_checks": {"ENV_startup_ran": false}, "id": "ENV-SHELLOPTS-posix"} pin_rc=0 drift_rc=0
{"baseline_echo_lines": [], "baseline_exists": true, "capture_matches_control": true, "drift_lines": ["GATE_DRIFT: none"], "fixture_checks": {}, "id": "SHELLOPTS-posix"} pin_rc=0 drift_rc=0
{"baseline_echo_lines": [], "baseline_exists": false, "capture_matches_control": null, "drift_lines": [], "fixture_checks": {}, "id": "SHELLOPTS-noexec"} pin_rc=0 drift_rc=2
{"baseline_echo_lines": [], "baseline_exists": false, "capture_matches_control": null, "drift_lines": [], "fixture_checks": {}, "id": "SHELLOPTS-noexec-extglob"} pin_rc=0 drift_rc=2
{"baseline_echo_lines": [], "baseline_exists": true, "capture_matches_control": false, "drift_lines": ["GATE_DRIFT: -FINDING:SWEEP_CLAIM_FALSE drift drift-sections drift_sections findings hit native tally verdict verified"], "fixture_checks": {}, "id": "SHELLOPTS-noglob"} pin_rc=0 drift_rc=1
{"baseline_echo_lines": [], "baseline_exists": true, "capture_matches_control": true, "drift_lines": ["GATE_DRIFT: none"], "fixture_checks": {}, "id": "SHELLOPTS-errtrace-functrace"} pin_rc=0 drift_rc=0
{"baseline_echo_lines": [], "baseline_exists": true, "capture_matches_control": true, "drift_lines": ["GATE_DRIFT: none"], "fixture_checks": {}, "id": "BASHOPTS-failglob"} pin_rc=0 drift_rc=0
{"baseline_echo_lines": [], "baseline_exists": true, "capture_matches_control": true, "drift_lines": ["GATE_DRIFT: none"], "fixture_checks": {}, "id": "BASHOPTS-nullglob"} pin_rc=0 drift_rc=0
{"baseline_echo_lines": [], "baseline_exists": true, "capture_matches_control": true, "drift_lines": ["GATE_DRIFT: none"], "fixture_checks": {}, "id": "BASHOPTS-inherit_errexit"} pin_rc=0 drift_rc=0
{"baseline_echo_lines": [], "baseline_exists": true, "capture_matches_control": true, "drift_lines": ["GATE_DRIFT: none"], "fixture_checks": {}, "id": "BASHOPTS-extdebug"} pin_rc=0 drift_rc=0
{"baseline_echo_lines": [], "baseline_exists": true, "capture_matches_control": true, "drift_lines": ["GATE_DRIFT: none"], "fixture_checks": {}, "id": "BASHOPTS-nocasematch"} pin_rc=0 drift_rc=0
{"baseline_echo_lines": [], "baseline_exists": false, "capture_matches_control": null, "drift_lines": [], "fixture_checks": {}, "id": "TMPDIR-missing"} pin_rc=2 drift_rc=2
{"baseline_echo_lines": [], "baseline_exists": false, "capture_matches_control": null, "drift_lines": [], "fixture_checks": {"tmpdir_writable": false}, "id": "TMPDIR-no-permission"} pin_rc=2 drift_rc=2
{"baseline_echo_lines": [], "baseline_exists": true, "capture_matches_control": false, "drift_lines": ["GATE_DRIFT: -FINDING:CHAIN_SOURCE_SESSION -FINDING:CLAIM_SOURCE_SESSION -FINDING:POINTER_UNRESOLVED drift drift-sections drift_sections findings native refused supported tallies tally verdict verified"], "fixture_checks": {}, "id": "TMPDIR-session-path"} pin_rc=0 drift_rc=1
{"baseline_echo_lines": [], "baseline_exists": true, "capture_matches_control": true, "drift_lines": ["GATE_DRIFT: none"], "fixture_checks": {}, "id": "TMPDIR-symlink"} pin_rc=0 drift_rc=0
{"baseline_echo_lines": [], "baseline_exists": true, "capture_matches_control": true, "drift_lines": ["GATE_DRIFT: none"], "fixture_checks": {}, "id": "TMPDIR-newline"} pin_rc=0 drift_rc=0
{"baseline_echo_lines": [], "baseline_exists": true, "capture_matches_control": true, "drift_lines": ["GATE_DRIFT: none"], "fixture_checks": {}, "id": "CDPATH-decoy"} pin_rc=0 drift_rc=0
{"baseline_echo_lines": [], "baseline_exists": true, "capture_matches_control": true, "drift_lines": ["GATE_DRIFT: none"], "fixture_checks": {}, "id": "CDPATH-newline"} pin_rc=0 drift_rc=0
{"baseline_echo_lines": [], "baseline_exists": true, "capture_matches_control": true, "drift_lines": ["GATE_DRIFT: none"], "fixture_checks": {}, "id": "BASH_ENV-directory"} pin_rc=0 drift_rc=0
{"baseline_echo_lines": [], "baseline_exists": true, "capture_matches_control": true, "drift_lines": ["GATE_DRIFT: none"], "fixture_checks": {"bash_env_readable": false}, "id": "BASH_ENV-unreadable"} pin_rc=0 drift_rc=0
{"baseline_echo_lines": [], "baseline_exists": true, "capture_matches_control": true, "drift_lines": ["GATE_DRIFT: none"], "fixture_checks": {"farm_lib_resolves_to": "/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-root-symlink-farm/foreign-root/lib", "root_resolves_to": "/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-root-symlink-farm/symlink-farm", "root_symlink_hops": 16}, "id": "BASH_ENV-root-symlink-farm"} pin_rc=0 drift_rc=0
{"baseline_echo_lines": [], "baseline_exists": true, "capture_matches_control": true, "drift_lines": ["GATE_DRIFT: none"], "fixture_checks": {}, "id": "BASH_ENV-exportf-benign"} pin_rc=0 drift_rc=0
{"baseline_echo_lines": ["GATE_GREP: path=/usr/bin/grep source=default version=\"grep (GNU grep) 3.12-modified\""], "baseline_exists": true, "capture_matches_control": false, "drift_lines": ["GATE_DRIFT: -GATE_GREP"], "fixture_checks": {}, "id": "BASH_ENV-exportf-env-reinsert"} pin_rc=0 drift_rc=1
{"baseline_echo_lines": ["GATE_GREP: path=/usr/bin/grep source=default version=\"grep (GNU grep) 3.12-modified\""], "baseline_exists": true, "capture_matches_control": false, "drift_lines": ["GATE_DRIFT: -GATE_GREP"], "fixture_checks": {}, "id": "exportf-env-without-BASH_ENV"} pin_rc=0 drift_rc=1
{"baseline_echo_lines": [], "baseline_exists": true, "capture_matches_control": false, "drift_lines": ["GATE_DRIFT: -FINDING:CHAIN_SOURCE_SESSION -FINDING:CLAIM_SOURCE_SESSION -FINDING:POINTER_UNRESOLVED drift drift-sections drift_sections findings native refused supported tallies tally verdict verified"], "fixture_checks": {}, "id": "BASH_ENV-sets-TMPDIR-session-path"} pin_rc=0 drift_rc=1
{"baseline_echo_lines": [], "baseline_exists": true, "capture_matches_control": true, "drift_lines": ["GATE_DRIFT: none"], "fixture_checks": {}, "id": "BASH_ENV-exports-BASHOPTS-failglob"} pin_rc=0 drift_rc=0
RECEIPT=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/vectors.json
```
stderr: (empty). Exit code: **0**.

### 1. control-plain

Classification: Control; no kill

hostile --pin; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/control-plain`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/control-plain/captures /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --pin baseline.txt
```

stdout:
```text
GATE_PIN: ok path=baseline.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
```

stderr: (empty).

Exit code: **0**.

plain --drift; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/control-plain`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/control-plain/captures /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --drift baseline.txt
```

stdout:
```text
GATE_DRIFT: none
```

stderr: (empty).

Exit code: **0**.

Capture SHA-256: `236c2c657f13cc0642ee3ac0ab76f80fae66fd10b670b04ed519a35078db411f`; exact embedded grep receipts: `[]`.

### 2. ENV-posix-noninteractive

Classification: No kill; invariant held in this excluded vector, not confirmation of a general guarantee

Observed fixture checks:
```json
{
  "ENV_startup_ran": false
}
```

Fixture `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/ENV-posix-noninteractive/posix-startup.sh`, mode `0o600`:
```sh
printf "ENV_STARTUP_RAN\n" >>/tmp/chousa-r37-CritC2Kill-jx8vuxvx/ENV-posix-noninteractive/startup-ran
export CHOUSA_GREP_PIN_ECHO=1
export CHOUSA_ROOT=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/ENV-posix-noninteractive/foreign-root
```

hostile --pin; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/ENV-posix-noninteractive`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/ENV-posix-noninteractive/captures ENV=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/ENV-posix-noninteractive/posix-startup.sh /usr/bin/bash --posix /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --pin baseline.txt
```

stdout:
```text
GATE_PIN: ok path=baseline.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
```

stderr: (empty).

Exit code: **0**.

plain --drift; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/ENV-posix-noninteractive`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/ENV-posix-noninteractive/captures /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --drift baseline.txt
```

stdout:
```text
GATE_DRIFT: none
```

stderr: (empty).

Exit code: **0**.

Capture SHA-256: `236c2c657f13cc0642ee3ac0ab76f80fae66fd10b670b04ed519a35078db411f`; exact embedded grep receipts: `[]`.

### 3. ENV-posix-interactive

Classification: No kill; invariant held in this excluded vector, not confirmation of a general guarantee

Observed fixture checks:
```json
{
  "ENV_startup_ran": true
}
```

Fixture `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/ENV-posix-interactive/posix-startup.sh`, mode `0o600`:
```sh
printf "ENV_STARTUP_RAN\n" >>/tmp/chousa-r37-CritC2Kill-jx8vuxvx/ENV-posix-interactive/startup-ran
export CHOUSA_GREP_PIN_ECHO=1
export CHOUSA_ROOT=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/ENV-posix-interactive/foreign-root
```

hostile --pin; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/ENV-posix-interactive`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/ENV-posix-interactive/captures ENV=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/ENV-posix-interactive/posix-startup.sh /usr/bin/bash --posix -i /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --pin baseline.txt
```

stdout:
```text
GATE_PIN: ok path=baseline.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
```

stderr:
```text
bash: cannot set terminal process group (2087366): Inappropriate ioctl for device
bash: no job control in this shell
bash: !-: event not found
GATE_GREP: path=/usr/bin/grep source=default version="grep (GNU grep) 3.12-modified"
```

Exit code: **0**.

plain --drift; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/ENV-posix-interactive`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/ENV-posix-interactive/captures /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --drift baseline.txt
```

stdout:
```text
GATE_DRIFT: none
```

stderr: (empty).

Exit code: **0**.

Capture SHA-256: `236c2c657f13cc0642ee3ac0ab76f80fae66fd10b670b04ed519a35078db411f`; exact embedded grep receipts: `[]`.

### 4. ENV-SHELLOPTS-posix

Classification: No kill; invariant held in this excluded vector, not confirmation of a general guarantee

Observed fixture checks:
```json
{
  "ENV_startup_ran": false
}
```

Fixture `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/ENV-SHELLOPTS-posix/posix-startup.sh`, mode `0o600`:
```sh
printf "ENV_STARTUP_RAN\n" >>/tmp/chousa-r37-CritC2Kill-jx8vuxvx/ENV-SHELLOPTS-posix/startup-ran
export CHOUSA_GREP_PIN_ECHO=1
export CHOUSA_ROOT=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/ENV-SHELLOPTS-posix/foreign-root
```

hostile --pin; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/ENV-SHELLOPTS-posix`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/ENV-SHELLOPTS-posix/captures ENV=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/ENV-SHELLOPTS-posix/posix-startup.sh SHELLOPTS=posix /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --pin baseline.txt
```

stdout:
```text
GATE_PIN: ok path=baseline.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
```

stderr: (empty).

Exit code: **0**.

plain --drift; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/ENV-SHELLOPTS-posix`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/ENV-SHELLOPTS-posix/captures /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --drift baseline.txt
```

stdout:
```text
GATE_DRIFT: none
```

stderr: (empty).

Exit code: **0**.

Capture SHA-256: `236c2c657f13cc0642ee3ac0ab76f80fae66fd10b670b04ed519a35078db411f`; exact embedded grep receipts: `[]`.

### 5. SHELLOPTS-posix

Classification: No kill; invariant held in this excluded vector, not confirmation of a general guarantee

hostile --pin; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/SHELLOPTS-posix`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/SHELLOPTS-posix/captures SHELLOPTS=posix /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --pin baseline.txt
```

stdout:
```text
GATE_PIN: ok path=baseline.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
```

stderr: (empty).

Exit code: **0**.

plain --drift; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/SHELLOPTS-posix`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/SHELLOPTS-posix/captures /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --drift baseline.txt
```

stdout:
```text
GATE_DRIFT: none
```

stderr: (empty).

Exit code: **0**.

Capture SHA-256: `236c2c657f13cc0642ee3ac0ab76f80fae66fd10b670b04ed519a35078db411f`; exact embedded grep receipts: `[]`.

### 6. SHELLOPTS-noexec

Classification: CONFIRMED NAMED LIMIT: SHELLOPTS (claims.md:114-117); no baseline, not phantom drift

hostile --pin; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/SHELLOPTS-noexec`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/SHELLOPTS-noexec/captures SHELLOPTS=noexec /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --pin baseline.txt
```

stdout: (empty).

stderr: (empty).

Exit code: **0**.

plain --drift; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/SHELLOPTS-noexec`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/SHELLOPTS-noexec/captures /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --drift baseline.txt
```

stdout: (empty).

stderr:
```text
research-gate: --drift baseline missing: baseline.txt
```

Exit code: **2**.

Capture SHA-256: `no baseline`; exact embedded grep receipts: `[]`.

### 7. SHELLOPTS-noexec-extglob

Classification: CONFIRMED NAMED LIMIT: SHELLOPTS (claims.md:114-117); no baseline, not phantom drift

hostile --pin; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/SHELLOPTS-noexec-extglob`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/SHELLOPTS-noexec-extglob/captures SHELLOPTS=noexec BASHOPTS=extglob /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --pin baseline.txt
```

stdout: (empty).

stderr: (empty).

Exit code: **0**.

plain --drift; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/SHELLOPTS-noexec-extglob`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/SHELLOPTS-noexec-extglob/captures /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --drift baseline.txt
```

stdout: (empty).

stderr:
```text
research-gate: --drift baseline missing: baseline.txt
```

Exit code: **2**.

Capture SHA-256: `no baseline`; exact embedded grep receipts: `[]`.

### 8. SHELLOPTS-noglob

Classification: CONFIRMED NAMED LIMIT: SHELLOPTS (claims.md:114-117); not a kill

hostile --pin; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/SHELLOPTS-noglob`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/SHELLOPTS-noglob/captures SHELLOPTS=noglob /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --pin baseline.txt
```

stdout:
```text
GATE_PIN: ok path=baseline.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
```

stderr: (empty).

Exit code: **0**.

plain --drift; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/SHELLOPTS-noglob`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/SHELLOPTS-noglob/captures /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --drift baseline.txt
```

stdout:
```text
GATE_DRIFT: -FINDING:SWEEP_CLAIM_FALSE drift drift-sections drift_sections findings hit native tally verdict verified
```

stderr: (empty).

Exit code: **1**.

Capture SHA-256: `4b4a24aeeaf62c2ea71e335ec8d9bb2d582648f9ed8ce77fe26d1a0eb31a017a`; exact embedded grep receipts: `[]`.

Full normalized-body difference from the control:
```diff
--- plain-control
+++ SHELLOPTS-noglob
@@ -2,10 +2,11 @@
 SECTION structure state=run verdict=CLEAN findings=0 drift=0
 SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=1/1
 SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=1/1
-SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=1/1 REJECTIONS_OK=1/1
+SECTION sweeps state=run verdict=DRIFT findings=1 drift=1 tally=VERIFIED_SWEEPS=0/1 REJECTIONS_OK=1/1
+FINDING SWEEP_CLAIM_FALSE severity=warn surface=sweeps obs=id=SW1 where=lib/ghost*.md hits=1 first=lib/ghost*.md listed=lib/ghost*.md
 SECTION integrity state=run verdict=DRIFT findings=1 drift=1 tally=INTEGRITY refs=4 resolved=3 unresolved=1
 FINDING REF_UNRESOLVED severity=warn surface=integrity obs=kind=claim id=C9 section=sweeps row=SW1 cell=claim_id
-VERIFY_ALL sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1
-RESEARCH_GATE: DRIFT (sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1)
+VERIFY_ALL sections=5 run=5 absent=0 drift-sections=2 findings=2 drift=2
+RESEARCH_GATE: DRIFT (sections=5 run=5 absent=0 drift-sections=2 findings=2 drift=2)
 # --- json manifest line follows ---
-{"schema":"chousa-verify-all/v1","ts":"<V>","record":"record.md","record_sha256":"c22a6c3d8acf345a4b2a5b9b8ece388c596648cee84c7f9ba3002a75a95f3f84","gate_sha256":"<V>","sections":[{"name":"structure","state":"run","verdict":"CLEAN","findings":0,"drift":0,"tallies":{"findings":0,"drift":0,"questions":1,"sources":1,"chains":1,"claims":1,"negatives":1,"rejections":1,"approvals":1}},{"name":"claims","state":"run","verdict":"CLEAN","findings":0,"drift":0,"tallies":{"claims":1,"supported":1,"contradicted":0,"unsupported":0,"mismatched":0,"unproven":0,"refused":0,"invalid":0,"findings":0,"drift":0},"native":"VERDICT_BEARING_CLAIMS=1/1"},{"name":"chain","state":"run","verdict":"CLEAN","findings":0,"drift":0,"tallies":{"hops":1,"verified":1,"exempt":0,"anchor-missing":0,"refused":0,"invalid":0,"findings":0,"drift":0,"resolvable":0},"native":"RESOLVED_HOPS=1/1"},{"name":"sweeps","state":"run","verdict":"CLEAN","findings":0,"drift":0,"tallies":{"sweeps":1,"verified":1,"exempt":0,"hit":0,"refused":0,"invalid":0,"rejections":1,"rejections-ok":1,"findings":0,"drift":0},"native":"VERIFIED_SWEEPS=1/1 REJECTIONS_OK=1/1"},{"name":"integrity","state":"run","verdict":"DRIFT","findings":1,"drift":1,"tallies":{"refs":4,"resolved":3,"unresolved":1,"exempt":0,"findings":1,"drift":1},"native":"INTEGRITY refs=4 resolved=3 unresolved=1"}],"verdict":"DRIFT","sections_run":5,"sections_absent":0,"drift_sections":1}
+{"schema":"chousa-verify-all/v1","ts":"<V>","record":"record.md","record_sha256":"c22a6c3d8acf345a4b2a5b9b8ece388c596648cee84c7f9ba3002a75a95f3f84","gate_sha256":"<V>","sections":[{"name":"structure","state":"run","verdict":"CLEAN","findings":0,"drift":0,"tallies":{"findings":0,"drift":0,"questions":1,"sources":1,"chains":1,"claims":1,"negatives":1,"rejections":1,"approvals":1}},{"name":"claims","state":"run","verdict":"CLEAN","findings":0,"drift":0,"tallies":{"claims":1,"supported":1,"contradicted":0,"unsupported":0,"mismatched":0,"unproven":0,"refused":0,"invalid":0,"findings":0,"drift":0},"native":"VERDICT_BEARING_CLAIMS=1/1"},{"name":"chain","state":"run","verdict":"CLEAN","findings":0,"drift":0,"tallies":{"hops":1,"verified":1,"exempt":0,"anchor-missing":0,"refused":0,"invalid":0,"findings":0,"drift":0,"resolvable":0},"native":"RESOLVED_HOPS=1/1"},{"name":"sweeps","state":"run","verdict":"DRIFT","findings":1,"drift":1,"tallies":{"sweeps":1,"verified":0,"exempt":0,"hit":1,"refused":0,"invalid":0,"rejections":1,"rejections-ok":1,"findings":1,"drift":1},"native":"VERIFIED_SWEEPS=0/1 REJECTIONS_OK=1/1"},{"name":"integrity","state":"run","verdict":"DRIFT","findings":1,"drift":1,"tallies":{"refs":4,"resolved":3,"unresolved":1,"exempt":0,"findings":1,"drift":1},"native":"INTEGRITY refs=4 resolved=3 unresolved=1"}],"verdict":"DRIFT","sections_run":5,"sections_absent":0,"drift_sections":2}
```

### 9. SHELLOPTS-errtrace-functrace

Classification: No kill; invariant held in this excluded vector, not confirmation of a general guarantee

hostile --pin; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/SHELLOPTS-errtrace-functrace`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/SHELLOPTS-errtrace-functrace/captures SHELLOPTS=errtrace:functrace /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --pin baseline.txt
```

stdout:
```text
GATE_PIN: ok path=baseline.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
```

stderr: (empty).

Exit code: **0**.

plain --drift; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/SHELLOPTS-errtrace-functrace`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/SHELLOPTS-errtrace-functrace/captures /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --drift baseline.txt
```

stdout:
```text
GATE_DRIFT: none
```

stderr: (empty).

Exit code: **0**.

Capture SHA-256: `236c2c657f13cc0642ee3ac0ab76f80fae66fd10b670b04ed519a35078db411f`; exact embedded grep receipts: `[]`.

### 10. BASHOPTS-failglob

Classification: No kill; invariant held in this excluded vector, not confirmation of a general guarantee

hostile --pin; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASHOPTS-failglob`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASHOPTS-failglob/captures BASHOPTS=failglob /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --pin baseline.txt
```

stdout:
```text
GATE_PIN: ok path=baseline.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
```

stderr: (empty).

Exit code: **0**.

plain --drift; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASHOPTS-failglob`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASHOPTS-failglob/captures /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --drift baseline.txt
```

stdout:
```text
GATE_DRIFT: none
```

stderr: (empty).

Exit code: **0**.

Capture SHA-256: `236c2c657f13cc0642ee3ac0ab76f80fae66fd10b670b04ed519a35078db411f`; exact embedded grep receipts: `[]`.

### 11. BASHOPTS-nullglob

Classification: No kill; invariant held in this excluded vector, not confirmation of a general guarantee

hostile --pin; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASHOPTS-nullglob`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASHOPTS-nullglob/captures BASHOPTS=nullglob /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --pin baseline.txt
```

stdout:
```text
GATE_PIN: ok path=baseline.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
```

stderr: (empty).

Exit code: **0**.

plain --drift; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASHOPTS-nullglob`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASHOPTS-nullglob/captures /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --drift baseline.txt
```

stdout:
```text
GATE_DRIFT: none
```

stderr: (empty).

Exit code: **0**.

Capture SHA-256: `236c2c657f13cc0642ee3ac0ab76f80fae66fd10b670b04ed519a35078db411f`; exact embedded grep receipts: `[]`.

### 12. BASHOPTS-inherit_errexit

Classification: No kill; invariant held in this excluded vector, not confirmation of a general guarantee

hostile --pin; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASHOPTS-inherit_errexit`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASHOPTS-inherit_errexit/captures BASHOPTS=inherit_errexit /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --pin baseline.txt
```

stdout:
```text
GATE_PIN: ok path=baseline.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
```

stderr: (empty).

Exit code: **0**.

plain --drift; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASHOPTS-inherit_errexit`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASHOPTS-inherit_errexit/captures /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --drift baseline.txt
```

stdout:
```text
GATE_DRIFT: none
```

stderr: (empty).

Exit code: **0**.

Capture SHA-256: `236c2c657f13cc0642ee3ac0ab76f80fae66fd10b670b04ed519a35078db411f`; exact embedded grep receipts: `[]`.

### 13. BASHOPTS-extdebug

Classification: No kill; invariant held in this excluded vector, not confirmation of a general guarantee

hostile --pin; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASHOPTS-extdebug`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASHOPTS-extdebug/captures BASHOPTS=extdebug /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --pin baseline.txt
```

stdout:
```text
GATE_PIN: ok path=baseline.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
```

stderr:
```text
/tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh: /usr/share/bashdb/bashdb-main.inc: No such file or directory
/tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh: warning: cannot start debugger; debugging mode disabled
```

Exit code: **0**.

plain --drift; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASHOPTS-extdebug`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASHOPTS-extdebug/captures /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --drift baseline.txt
```

stdout:
```text
GATE_DRIFT: none
```

stderr: (empty).

Exit code: **0**.

Capture SHA-256: `236c2c657f13cc0642ee3ac0ab76f80fae66fd10b670b04ed519a35078db411f`; exact embedded grep receipts: `[]`.

### 14. BASHOPTS-nocasematch

Classification: No kill; invariant held in this excluded vector, not confirmation of a general guarantee

hostile --pin; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASHOPTS-nocasematch`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASHOPTS-nocasematch/captures BASHOPTS=nocasematch /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --pin baseline.txt
```

stdout:
```text
GATE_PIN: ok path=baseline.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
```

stderr: (empty).

Exit code: **0**.

plain --drift; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASHOPTS-nocasematch`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASHOPTS-nocasematch/captures /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --drift baseline.txt
```

stdout:
```text
GATE_DRIFT: none
```

stderr: (empty).

Exit code: **0**.

Capture SHA-256: `236c2c657f13cc0642ee3ac0ab76f80fae66fd10b670b04ed519a35078db411f`; exact embedded grep receipts: `[]`.

### 15. TMPDIR-missing

Classification: CONFIRMED NAMED LIMIT: TMPDIR (claims.md:114-117); no baseline, not phantom drift

hostile --pin; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/TMPDIR-missing`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/TMPDIR-missing/missing-parent /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --pin baseline.txt
```

stdout: (empty).

stderr:
```text
mktemp: failed to create directory via template '/tmp/chousa-r37-CritC2Kill-jx8vuxvx/TMPDIR-missing/missing-parent/chousa-gate-pin.XXXXXX': No such file or directory
research-gate: --pin canonical capture failed (mktemp-failed): baseline.txt
```

Exit code: **2**.

plain --drift; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/TMPDIR-missing`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/TMPDIR-missing/captures /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --drift baseline.txt
```

stdout: (empty).

stderr:
```text
research-gate: --drift baseline missing: baseline.txt
```

Exit code: **2**.

Capture SHA-256: `no baseline`; exact embedded grep receipts: `[]`.

### 16. TMPDIR-no-permission

Classification: CONFIRMED NAMED LIMIT: TMPDIR (claims.md:114-117); no baseline, not phantom drift

Observed fixture checks:
```json
{
  "tmpdir_writable": false
}
```

hostile --pin; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/TMPDIR-no-permission`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/TMPDIR-no-permission/no-permission /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --pin baseline.txt
```

stdout: (empty).

stderr:
```text
mktemp: failed to create directory via template '/tmp/chousa-r37-CritC2Kill-jx8vuxvx/TMPDIR-no-permission/no-permission/chousa-gate-pin.XXXXXX': Permission denied
research-gate: --pin canonical capture failed (mktemp-failed): baseline.txt
```

Exit code: **2**.

plain --drift; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/TMPDIR-no-permission`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/TMPDIR-no-permission/captures /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --drift baseline.txt
```

stdout: (empty).

stderr:
```text
research-gate: --drift baseline missing: baseline.txt
```

Exit code: **2**.

Capture SHA-256: `no baseline`; exact embedded grep receipts: `[]`.

### 17. TMPDIR-session-path

Classification: CONFIRMED NAMED LIMIT: TMPDIR (claims.md:114-117); not a kill

hostile --pin; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/TMPDIR-session-path`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/TMPDIR-session-path/.config /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --pin baseline.txt
```

stdout:
```text
GATE_PIN: ok path=baseline.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
```

stderr: (empty).

Exit code: **0**.

plain --drift; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/TMPDIR-session-path`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/TMPDIR-session-path/captures /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --drift baseline.txt
```

stdout:
```text
GATE_DRIFT: -FINDING:CHAIN_SOURCE_SESSION -FINDING:CLAIM_SOURCE_SESSION -FINDING:POINTER_UNRESOLVED drift drift-sections drift_sections findings native refused supported tallies tally verdict verified
```

stderr: (empty).

Exit code: **1**.

Capture SHA-256: `3f8ef77f5ad9a099ada68326bd70fa75101c2d945f5a629dac2a5389b9f716f7`; exact embedded grep receipts: `[]`.

Full normalized-body difference from the control:
```diff
--- plain-control
+++ TMPDIR-session-path
@@ -1,11 +1,15 @@
 research-gate v2 — ts=<V> — mode=verify-all — record=record.md — claims=claims.jsonl — root=.
-SECTION structure state=run verdict=CLEAN findings=0 drift=0
-SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=1/1
-SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=1/1
+SECTION structure state=run verdict=DRIFT findings=2 drift=2
+FINDING POINTER_UNRESOLVED severity=warn surface=sources obs=ctx=source:S1 ptr=lib/primary.md:1 missing under CHOUSA_ROOT
+FINDING POINTER_UNRESOLVED severity=warn surface=claims obs=ctx=claim:C1 ptr=lib/primary.md:1 missing under CHOUSA_ROOT
+SECTION claims state=run verdict=DRIFT findings=1 drift=1 tally=VERDICT_BEARING_CLAIMS=0/1
+FINDING CLAIM_SOURCE_SESSION severity=crit surface=claims obs=id=P1 source=lib/primary.md obs=path=lib/primary.md denied (not opened)
+SECTION chain state=run verdict=DRIFT findings=1 drift=1 tally=RESOLVED_HOPS=0/1
+FINDING CHAIN_SOURCE_SESSION severity=crit surface=chain obs=hop=1 source=lib/primary.md obs=path=lib/primary.md denied (not opened)
 SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=1/1 REJECTIONS_OK=1/1
 SECTION integrity state=run verdict=DRIFT findings=1 drift=1 tally=INTEGRITY refs=4 resolved=3 unresolved=1
 FINDING REF_UNRESOLVED severity=warn surface=integrity obs=kind=claim id=C9 section=sweeps row=SW1 cell=claim_id
-VERIFY_ALL sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1
-RESEARCH_GATE: DRIFT (sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1)
+VERIFY_ALL sections=5 run=5 absent=0 drift-sections=4 findings=5 drift=5
+RESEARCH_GATE: DRIFT (sections=5 run=5 absent=0 drift-sections=4 findings=5 drift=5)
 # --- json manifest line follows ---
-{"schema":"chousa-verify-all/v1","ts":"<V>","record":"record.md","record_sha256":"c22a6c3d8acf345a4b2a5b9b8ece388c596648cee84c7f9ba3002a75a95f3f84","gate_sha256":"<V>","sections":[{"name":"structure","state":"run","verdict":"CLEAN","findings":0,"drift":0,"tallies":{"findings":0,"drift":0,"questions":1,"sources":1,"chains":1,"claims":1,"negatives":1,"rejections":1,"approvals":1}},{"name":"claims","state":"run","verdict":"CLEAN","findings":0,"drift":0,"tallies":{"claims":1,"supported":1,"contradicted":0,"unsupported":0,"mismatched":0,"unproven":0,"refused":0,"invalid":0,"findings":0,"drift":0},"native":"VERDICT_BEARING_CLAIMS=1/1"},{"name":"chain","state":"run","verdict":"CLEAN","findings":0,"drift":0,"tallies":{"hops":1,"verified":1,"exempt":0,"anchor-missing":0,"refused":0,"invalid":0,"findings":0,"drift":0,"resolvable":0},"native":"RESOLVED_HOPS=1/1"},{"name":"sweeps","state":"run","verdict":"CLEAN","findings":0,"drift":0,"tallies":{"sweeps":1,"verified":1,"exempt":0,"hit":0,"refused":0,"invalid":0,"rejections":1,"rejections-ok":1,"findings":0,"drift":0},"native":"VERIFIED_SWEEPS=1/1 REJECTIONS_OK=1/1"},{"name":"integrity","state":"run","verdict":"DRIFT","findings":1,"drift":1,"tallies":{"refs":4,"resolved":3,"unresolved":1,"exempt":0,"findings":1,"drift":1},"native":"INTEGRITY refs=4 resolved=3 unresolved=1"}],"verdict":"DRIFT","sections_run":5,"sections_absent":0,"drift_sections":1}
+{"schema":"chousa-verify-all/v1","ts":"<V>","record":"record.md","record_sha256":"c22a6c3d8acf345a4b2a5b9b8ece388c596648cee84c7f9ba3002a75a95f3f84","gate_sha256":"<V>","sections":[{"name":"structure","state":"run","verdict":"DRIFT","findings":2,"drift":2,"tallies":{"findings":2,"drift":2,"questions":1,"sources":1,"chains":1,"claims":1,"negatives":1,"rejections":1,"approvals":1}},{"name":"claims","state":"run","verdict":"DRIFT","findings":1,"drift":1,"tallies":{"claims":1,"supported":0,"contradicted":0,"unsupported":0,"mismatched":0,"unproven":0,"refused":1,"invalid":0,"findings":1,"drift":1},"native":"VERDICT_BEARING_CLAIMS=0/1"},{"name":"chain","state":"run","verdict":"DRIFT","findings":1,"drift":1,"tallies":{"hops":1,"verified":0,"exempt":0,"anchor-missing":0,"refused":1,"invalid":0,"findings":1,"drift":1,"resolvable":0},"native":"RESOLVED_HOPS=0/1"},{"name":"sweeps","state":"run","verdict":"CLEAN","findings":0,"drift":0,"tallies":{"sweeps":1,"verified":1,"exempt":0,"hit":0,"refused":0,"invalid":0,"rejections":1,"rejections-ok":1,"findings":0,"drift":0},"native":"VERIFIED_SWEEPS=1/1 REJECTIONS_OK=1/1"},{"name":"integrity","state":"run","verdict":"DRIFT","findings":1,"drift":1,"tallies":{"refs":4,"resolved":3,"unresolved":1,"exempt":0,"findings":1,"drift":1},"native":"INTEGRITY refs=4 resolved=3 unresolved=1"}],"verdict":"DRIFT","sections_run":5,"sections_absent":0,"drift_sections":4}
```

### 18. TMPDIR-symlink

Classification: No kill; invariant held in this excluded vector, not confirmation of a general guarantee

hostile --pin; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/TMPDIR-symlink`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/TMPDIR-symlink/temp-alias /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --pin baseline.txt
```

stdout:
```text
GATE_PIN: ok path=baseline.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
```

stderr: (empty).

Exit code: **0**.

plain --drift; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/TMPDIR-symlink`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/TMPDIR-symlink/captures /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --drift baseline.txt
```

stdout:
```text
GATE_DRIFT: none
```

stderr: (empty).

Exit code: **0**.

Capture SHA-256: `236c2c657f13cc0642ee3ac0ab76f80fae66fd10b670b04ed519a35078db411f`; exact embedded grep receipts: `[]`.

### 19. TMPDIR-newline

Classification: No kill; invariant held in this excluded vector, not confirmation of a general guarantee

hostile --pin; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/TMPDIR-newline`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C 'TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/TMPDIR-newline/capture
GATE_GREP: tmpdir-marker' /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --pin baseline.txt
```

stdout:
```text
GATE_PIN: ok path=baseline.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
```

stderr: (empty).

Exit code: **0**.

plain --drift; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/TMPDIR-newline`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/TMPDIR-newline/captures /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --drift baseline.txt
```

stdout:
```text
GATE_DRIFT: none
```

stderr: (empty).

Exit code: **0**.

Capture SHA-256: `236c2c657f13cc0642ee3ac0ab76f80fae66fd10b670b04ed519a35078db411f`; exact embedded grep receipts: `[]`.

### 20. CDPATH-decoy

Classification: No kill; invariant held

hostile --pin; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/CDPATH-decoy`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/CDPATH-decoy/captures CDPATH=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/CDPATH-decoy/cd-decoy:.:/tmp /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --pin baseline.txt
```

stdout:
```text
GATE_PIN: ok path=baseline.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
```

stderr: (empty).

Exit code: **0**.

plain --drift; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/CDPATH-decoy`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/CDPATH-decoy/captures /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --drift baseline.txt
```

stdout:
```text
GATE_DRIFT: none
```

stderr: (empty).

Exit code: **0**.

Capture SHA-256: `236c2c657f13cc0642ee3ac0ab76f80fae66fd10b670b04ed519a35078db411f`; exact embedded grep receipts: `[]`.

### 21. CDPATH-newline

Classification: No kill; invariant held

hostile --pin; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/CDPATH-newline`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/CDPATH-newline/captures 'CDPATH=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/CDPATH-newline/cd-decoy:.:/tmp
GATE_GREP: cdpath-marker' /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --pin baseline.txt
```

stdout:
```text
GATE_PIN: ok path=baseline.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
```

stderr: (empty).

Exit code: **0**.

plain --drift; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/CDPATH-newline`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/CDPATH-newline/captures /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --drift baseline.txt
```

stdout:
```text
GATE_DRIFT: none
```

stderr: (empty).

Exit code: **0**.

Capture SHA-256: `236c2c657f13cc0642ee3ac0ab76f80fae66fd10b670b04ed519a35078db411f`; exact embedded grep receipts: `[]`.

### 22. BASH_ENV-directory

Classification: No kill; invariant held

hostile --pin; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-directory`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-directory/captures BASH_ENV=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-directory/startup-directory /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --pin baseline.txt
```

stdout:
```text
GATE_PIN: ok path=baseline.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
```

stderr:
```text
/tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh: /tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-directory/startup-directory: is a directory
```

Exit code: **0**.

plain --drift; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-directory`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-directory/captures /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --drift baseline.txt
```

stdout:
```text
GATE_DRIFT: none
```

stderr: (empty).

Exit code: **0**.

Capture SHA-256: `236c2c657f13cc0642ee3ac0ab76f80fae66fd10b670b04ed519a35078db411f`; exact embedded grep receipts: `[]`.

### 23. BASH_ENV-unreadable

Classification: No kill; invariant held

Observed fixture checks:
```json
{
  "bash_env_readable": false
}
```

Fixture `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-unreadable/unreadable-startup.sh`, mode `0o0`:
```sh
export CHOUSA_GREP_PIN_ECHO=1
```

hostile --pin; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-unreadable`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-unreadable/captures BASH_ENV=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-unreadable/unreadable-startup.sh /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --pin baseline.txt
```

stdout:
```text
GATE_PIN: ok path=baseline.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
```

stderr:
```text
/tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh: /tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-unreadable/unreadable-startup.sh: Permission denied
```

Exit code: **0**.

plain --drift; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-unreadable`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-unreadable/captures /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --drift baseline.txt
```

stdout:
```text
GATE_DRIFT: none
```

stderr: (empty).

Exit code: **0**.

Capture SHA-256: `236c2c657f13cc0642ee3ac0ab76f80fae66fd10b670b04ed519a35078db411f`; exact embedded grep receipts: `[]`.

### 24. BASH_ENV-root-symlink-farm

Classification: No kill; invariant held

Observed fixture checks:
```json
{
  "root_symlink_hops": 16,
  "root_resolves_to": "/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-root-symlink-farm/symlink-farm",
  "farm_lib_resolves_to": "/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-root-symlink-farm/foreign-root/lib"
}
```

Fixture `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-root-symlink-farm/foreign-root/lib/primary.md`, mode `0o600`:
```sh
FOREIGN PRIMARY MATERIAL
```

Fixture `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-root-symlink-farm/foreign-root/noise/chat-export-sources.md`, mode `0o600`:
```sh
foreign noise
```

Fixture `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-root-symlink-farm/root-startup.sh`, mode `0o600`:
```sh
export CHOUSA_ROOT=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-root-symlink-farm/root-link-15
```

hostile --pin; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-root-symlink-farm`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-root-symlink-farm/captures BASH_ENV=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-root-symlink-farm/startup-link.sh /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --pin baseline.txt
```

stdout:
```text
GATE_PIN: ok path=baseline.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
```

stderr: (empty).

Exit code: **0**.

plain --drift; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-root-symlink-farm`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-root-symlink-farm/captures /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --drift baseline.txt
```

stdout:
```text
GATE_DRIFT: none
```

stderr: (empty).

Exit code: **0**.

Capture SHA-256: `236c2c657f13cc0642ee3ac0ab76f80fae66fd10b670b04ed519a35078db411f`; exact embedded grep receipts: `[]`.

### 25. BASH_ENV-exportf-benign

Classification: No kill; invariant held

Fixture `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-exportf-benign/startup.sh`, mode `0o600`:
```sh
r37_reexport() {
  export CHOUSA_GREP_PIN_ECHO=1
  export CHOUSA_STRICT=1
}
export -f r37_reexport
r37_reexport
```

hostile --pin; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-exportf-benign`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-exportf-benign/captures BASH_ENV=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-exportf-benign/startup.sh /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --pin baseline.txt
```

stdout:
```text
GATE_PIN: ok path=baseline.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
```

stderr:
```text
GATE_GREP: path=/usr/bin/grep source=default version="grep (GNU grep) 3.12-modified"
```

Exit code: **0**.

plain --drift; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-exportf-benign`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-exportf-benign/captures /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --drift baseline.txt
```

stdout:
```text
GATE_DRIFT: none
```

stderr: (empty).

Exit code: **0**.

Capture SHA-256: `236c2c657f13cc0642ee3ac0ab76f80fae66fd10b670b04ed519a35078db411f`; exact embedded grep receipts: `[]`.

### 26. BASH_ENV-exportf-env-reinsert

Classification: CONFIRMED NAMED LIMIT: parent-shell functions (claims.md:114-117); not a kill

Fixture `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-exportf-env-reinsert/startup.sh`, mode `0o600`:
```sh
env() {
  local -a scrub=()
  while [[ ${1-} == -u ]]; do
    scrub+=("$1" "$2")
    shift 2
  done
  command /usr/bin/env "${scrub[@]}" CHOUSA_GREP_PIN_ECHO=1 "$@"
}
export -f env
```

hostile --pin; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-exportf-env-reinsert`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-exportf-env-reinsert/captures BASH_ENV=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-exportf-env-reinsert/startup.sh /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --pin baseline.txt
```

stdout:
```text
GATE_PIN: ok path=baseline.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
```

stderr: (empty).

Exit code: **0**.

plain --drift; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-exportf-env-reinsert`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-exportf-env-reinsert/captures /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --drift baseline.txt
```

stdout:
```text
GATE_DRIFT: -GATE_GREP
```

stderr: (empty).

Exit code: **1**.

Capture SHA-256: `a4d48e123bc9a835f7b0958f576506c2aea129291949cf765aa12a274cf6b1a9`; exact embedded grep receipts: `["GATE_GREP: path=/usr/bin/grep source=default version=\"grep (GNU grep) 3.12-modified\""]`.

Full normalized-body difference from the control:
```diff
--- plain-control
+++ BASH_ENV-exportf-env-reinsert
@@ -1,3 +1,4 @@
+GATE_GREP: path=/usr/bin/grep source=default version="grep (GNU grep) 3.12-modified"
 research-gate v2 — ts=<V> — mode=verify-all — record=record.md — claims=claims.jsonl — root=.
 SECTION structure state=run verdict=CLEAN findings=0 drift=0
 SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=1/1
```

### 27. exportf-env-without-BASH_ENV

Classification: CONFIRMED NAMED LIMIT: parent-shell functions (claims.md:114-117); not a kill

hostile --pin; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/exportf-env-without-BASH_ENV`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/exportf-env-without-BASH_ENV/captures /usr/bin/bash -c 'env() {
  local -a scrub=()
  while [[ ${1-} == -u ]]; do
    scrub+=("$1" "$2")
    shift 2
  done
  command /usr/bin/env "${scrub[@]}" CHOUSA_GREP_PIN_ECHO=1 "$@"
}
export -f env
exec /usr/bin/bash "$@"
' _ /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --pin baseline.txt
```

stdout:
```text
GATE_PIN: ok path=baseline.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
```

stderr: (empty).

Exit code: **0**.

plain --drift; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/exportf-env-without-BASH_ENV`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/exportf-env-without-BASH_ENV/captures /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --drift baseline.txt
```

stdout:
```text
GATE_DRIFT: -GATE_GREP
```

stderr: (empty).

Exit code: **1**.

Capture SHA-256: `a4d48e123bc9a835f7b0958f576506c2aea129291949cf765aa12a274cf6b1a9`; exact embedded grep receipts: `["GATE_GREP: path=/usr/bin/grep source=default version=\"grep (GNU grep) 3.12-modified\""]`.

Full normalized-body difference from the control:
```diff
--- plain-control
+++ exportf-env-without-BASH_ENV
@@ -1,3 +1,4 @@
+GATE_GREP: path=/usr/bin/grep source=default version="grep (GNU grep) 3.12-modified"
 research-gate v2 — ts=<V> — mode=verify-all — record=record.md — claims=claims.jsonl — root=.
 SECTION structure state=run verdict=CLEAN findings=0 drift=0
 SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=1/1
```

### 28. BASH_ENV-sets-TMPDIR-session-path

Classification: CONFIRMED NAMED LIMIT: TMPDIR (claims.md:114-117); not a kill

Fixture `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-sets-TMPDIR-session-path/startup.sh`, mode `0o600`:
```sh
export TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-sets-TMPDIR-session-path/.config
```

hostile --pin; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-sets-TMPDIR-session-path`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-sets-TMPDIR-session-path/captures BASH_ENV=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-sets-TMPDIR-session-path/startup.sh /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --pin baseline.txt
```

stdout:
```text
GATE_PIN: ok path=baseline.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
```

stderr: (empty).

Exit code: **0**.

plain --drift; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-sets-TMPDIR-session-path`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-sets-TMPDIR-session-path/captures /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --drift baseline.txt
```

stdout:
```text
GATE_DRIFT: -FINDING:CHAIN_SOURCE_SESSION -FINDING:CLAIM_SOURCE_SESSION -FINDING:POINTER_UNRESOLVED drift drift-sections drift_sections findings native refused supported tallies tally verdict verified
```

stderr: (empty).

Exit code: **1**.

Capture SHA-256: `3f8ef77f5ad9a099ada68326bd70fa75101c2d945f5a629dac2a5389b9f716f7`; exact embedded grep receipts: `[]`.

Full normalized-body difference from the control:
```diff
--- plain-control
+++ BASH_ENV-sets-TMPDIR-session-path
@@ -1,11 +1,15 @@
 research-gate v2 — ts=<V> — mode=verify-all — record=record.md — claims=claims.jsonl — root=.
-SECTION structure state=run verdict=CLEAN findings=0 drift=0
-SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=1/1
-SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=1/1
+SECTION structure state=run verdict=DRIFT findings=2 drift=2
+FINDING POINTER_UNRESOLVED severity=warn surface=sources obs=ctx=source:S1 ptr=lib/primary.md:1 missing under CHOUSA_ROOT
+FINDING POINTER_UNRESOLVED severity=warn surface=claims obs=ctx=claim:C1 ptr=lib/primary.md:1 missing under CHOUSA_ROOT
+SECTION claims state=run verdict=DRIFT findings=1 drift=1 tally=VERDICT_BEARING_CLAIMS=0/1
+FINDING CLAIM_SOURCE_SESSION severity=crit surface=claims obs=id=P1 source=lib/primary.md obs=path=lib/primary.md denied (not opened)
+SECTION chain state=run verdict=DRIFT findings=1 drift=1 tally=RESOLVED_HOPS=0/1
+FINDING CHAIN_SOURCE_SESSION severity=crit surface=chain obs=hop=1 source=lib/primary.md obs=path=lib/primary.md denied (not opened)
 SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=1/1 REJECTIONS_OK=1/1
 SECTION integrity state=run verdict=DRIFT findings=1 drift=1 tally=INTEGRITY refs=4 resolved=3 unresolved=1
 FINDING REF_UNRESOLVED severity=warn surface=integrity obs=kind=claim id=C9 section=sweeps row=SW1 cell=claim_id
-VERIFY_ALL sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1
-RESEARCH_GATE: DRIFT (sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1)
+VERIFY_ALL sections=5 run=5 absent=0 drift-sections=4 findings=5 drift=5
+RESEARCH_GATE: DRIFT (sections=5 run=5 absent=0 drift-sections=4 findings=5 drift=5)
 # --- json manifest line follows ---
-{"schema":"chousa-verify-all/v1","ts":"<V>","record":"record.md","record_sha256":"c22a6c3d8acf345a4b2a5b9b8ece388c596648cee84c7f9ba3002a75a95f3f84","gate_sha256":"<V>","sections":[{"name":"structure","state":"run","verdict":"CLEAN","findings":0,"drift":0,"tallies":{"findings":0,"drift":0,"questions":1,"sources":1,"chains":1,"claims":1,"negatives":1,"rejections":1,"approvals":1}},{"name":"claims","state":"run","verdict":"CLEAN","findings":0,"drift":0,"tallies":{"claims":1,"supported":1,"contradicted":0,"unsupported":0,"mismatched":0,"unproven":0,"refused":0,"invalid":0,"findings":0,"drift":0},"native":"VERDICT_BEARING_CLAIMS=1/1"},{"name":"chain","state":"run","verdict":"CLEAN","findings":0,"drift":0,"tallies":{"hops":1,"verified":1,"exempt":0,"anchor-missing":0,"refused":0,"invalid":0,"findings":0,"drift":0,"resolvable":0},"native":"RESOLVED_HOPS=1/1"},{"name":"sweeps","state":"run","verdict":"CLEAN","findings":0,"drift":0,"tallies":{"sweeps":1,"verified":1,"exempt":0,"hit":0,"refused":0,"invalid":0,"rejections":1,"rejections-ok":1,"findings":0,"drift":0},"native":"VERIFIED_SWEEPS=1/1 REJECTIONS_OK=1/1"},{"name":"integrity","state":"run","verdict":"DRIFT","findings":1,"drift":1,"tallies":{"refs":4,"resolved":3,"unresolved":1,"exempt":0,"findings":1,"drift":1},"native":"INTEGRITY refs=4 resolved=3 unresolved=1"}],"verdict":"DRIFT","sections_run":5,"sections_absent":0,"drift_sections":1}
+{"schema":"chousa-verify-all/v1","ts":"<V>","record":"record.md","record_sha256":"c22a6c3d8acf345a4b2a5b9b8ece388c596648cee84c7f9ba3002a75a95f3f84","gate_sha256":"<V>","sections":[{"name":"structure","state":"run","verdict":"DRIFT","findings":2,"drift":2,"tallies":{"findings":2,"drift":2,"questions":1,"sources":1,"chains":1,"claims":1,"negatives":1,"rejections":1,"approvals":1}},{"name":"claims","state":"run","verdict":"DRIFT","findings":1,"drift":1,"tallies":{"claims":1,"supported":0,"contradicted":0,"unsupported":0,"mismatched":0,"unproven":0,"refused":1,"invalid":0,"findings":1,"drift":1},"native":"VERDICT_BEARING_CLAIMS=0/1"},{"name":"chain","state":"run","verdict":"DRIFT","findings":1,"drift":1,"tallies":{"hops":1,"verified":0,"exempt":0,"anchor-missing":0,"refused":1,"invalid":0,"findings":1,"drift":1,"resolvable":0},"native":"RESOLVED_HOPS=0/1"},{"name":"sweeps","state":"run","verdict":"CLEAN","findings":0,"drift":0,"tallies":{"sweeps":1,"verified":1,"exempt":0,"hit":0,"refused":0,"invalid":0,"rejections":1,"rejections-ok":1,"findings":0,"drift":0},"native":"VERIFIED_SWEEPS=1/1 REJECTIONS_OK=1/1"},{"name":"integrity","state":"run","verdict":"DRIFT","findings":1,"drift":1,"tallies":{"refs":4,"resolved":3,"unresolved":1,"exempt":0,"findings":1,"drift":1},"native":"INTEGRITY refs=4 resolved=3 unresolved=1"}],"verdict":"DRIFT","sections_run":5,"sections_absent":0,"drift_sections":4}
```

### 29. BASH_ENV-exports-BASHOPTS-failglob

Classification: No kill; invariant held in this excluded vector, not confirmation of a general guarantee

Fixture `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-exports-BASHOPTS-failglob/startup.sh`, mode `0o600`:
```sh
shopt -s failglob
export BASHOPTS
```

hostile --pin; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-exports-BASHOPTS-failglob`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-exports-BASHOPTS-failglob/captures BASH_ENV=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-exports-BASHOPTS-failglob/startup.sh /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --pin baseline.txt
```

stdout:
```text
GATE_PIN: ok path=baseline.txt gate_sha256=9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
```

stderr: (empty).

Exit code: **0**.

plain --drift; cwd: `/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-exports-BASHOPTS-failglob`

```sh
/usr/bin/env -i PATH=/usr/bin:/bin HOME=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/home LC_ALL=C TMPDIR=/tmp/chousa-r37-CritC2Kill-jx8vuxvx/BASH_ENV-exports-BASHOPTS-failglob/captures /usr/bin/bash /tmp/chousa-r37-CritC2Kill-jx8vuxvx/lane/tools/research-gate.sh --drift baseline.txt
```

stdout:
```text
GATE_DRIFT: none
```

stderr: (empty).

Exit code: **0**.

Capture SHA-256: `236c2c657f13cc0642ee3ac0ab76f80fae66fd10b670b04ed519a35078db411f`; exact embedded grep receipts: `[]`.

## Plain control capture, verbatim

```text
research-gate v2 — ts=<V> — mode=verify-all — record=record.md — claims=claims.jsonl — root=.
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=1/1
SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=1/1
SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=1/1 REJECTIONS_OK=1/1
SECTION integrity state=run verdict=DRIFT findings=1 drift=1 tally=INTEGRITY refs=4 resolved=3 unresolved=1
FINDING REF_UNRESOLVED severity=warn surface=integrity obs=kind=claim id=C9 section=sweeps row=SW1 cell=claim_id
VERIFY_ALL sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1
RESEARCH_GATE: DRIFT (sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1)
# --- json manifest line follows ---
{"schema":"chousa-verify-all/v1","ts":"<V>","record":"record.md","record_sha256":"c22a6c3d8acf345a4b2a5b9b8ece388c596648cee84c7f9ba3002a75a95f3f84","gate_sha256":"<V>","sections":[{"name":"structure","state":"run","verdict":"CLEAN","findings":0,"drift":0,"tallies":{"findings":0,"drift":0,"questions":1,"sources":1,"chains":1,"claims":1,"negatives":1,"rejections":1,"approvals":1}},{"name":"claims","state":"run","verdict":"CLEAN","findings":0,"drift":0,"tallies":{"claims":1,"supported":1,"contradicted":0,"unsupported":0,"mismatched":0,"unproven":0,"refused":0,"invalid":0,"findings":0,"drift":0},"native":"VERDICT_BEARING_CLAIMS=1/1"},{"name":"chain","state":"run","verdict":"CLEAN","findings":0,"drift":0,"tallies":{"hops":1,"verified":1,"exempt":0,"anchor-missing":0,"refused":0,"invalid":0,"findings":0,"drift":0,"resolvable":0},"native":"RESOLVED_HOPS=1/1"},{"name":"sweeps","state":"run","verdict":"CLEAN","findings":0,"drift":0,"tallies":{"sweeps":1,"verified":1,"exempt":0,"hit":0,"refused":0,"invalid":0,"rejections":1,"rejections-ok":1,"findings":0,"drift":0},"native":"VERIFIED_SWEEPS=1/1 REJECTIONS_OK=1/1"},{"name":"integrity","state":"run","verdict":"DRIFT","findings":1,"drift":1,"tallies":{"refs":4,"resolved":3,"unresolved":1,"exempt":0,"findings":1,"drift":1},"native":"INTEGRITY refs=4 resolved=3 unresolved=1"}],"verdict":"DRIFT","sections_run":5,"sections_absent":0,"drift_sections":1}
```

## In-process scratch preparation

The following Python eval completed successfully; no subprocess exit status applies. It copied the gate without edits and observed uid/euid and both hashes before the attacks.

```python
from pathlib import Path
import os, sys, shutil, tempfile, hashlib, json, shlex, subprocess, concurrent.futures
work = Path(tempfile.mkdtemp(prefix='chousa-r37-CritC2Kill-', dir='/tmp'))
(work / 'lane' / 'tools').mkdir(parents=True)
source_gate = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh')
scratch_gate = work / 'lane' / 'tools' / 'research-gate.sh'
shutil.copy2(source_gate, scratch_gate)
scratch_sha = hashlib.sha256(scratch_gate.read_bytes()).hexdigest()
setup_observed = {'scratch': str(work), 'uid': os.getuid(), 'euid': os.geteuid(), 'source_sha256': hashlib.sha256(source_gate.read_bytes()).hexdigest(), 'scratch_sha256': scratch_sha, 'gate_copy_is_byte_exact': source_gate.read_bytes() == scratch_gate.read_bytes()}
print(json.dumps(setup_observed, indent=2))
```

Observed output:
```json
{
  "scratch": "/tmp/chousa-r37-CritC2Kill-jx8vuxvx",
  "uid": 1000,
  "euid": 1000,
  "source_sha256": "9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39",
  "scratch_sha256": "9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39",
  "gate_copy_is_byte_exact": true
}
```

## Exact scratch runner source

Created with the file-write tool, then invoked once by the command recorded above. Its subprocess records supplied this report; rendering the report did not rerun the gate.

```python
#!/usr/bin/python3
"""Residual C2 vectors: byte-exact scratch gate, local files, no network."""
from pathlib import Path
import concurrent.futures
import difflib
import hashlib
import json
import os
import shlex
import subprocess

WORK = Path(__file__).resolve().parent
GATE = WORK / 'lane/tools/research-gate.sh'
EXPECTED_SHA = '9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39'
HOME = WORK / 'home'
HOME.mkdir(exist_ok=True)
MARKER = '# --- canonical output follows ---\n'

ENV_FUNCTION = '''env() {
  local -a scrub=()
  while [[ ${1-} == -u ]]; do
    scrub+=("$1" "$2")
    shift 2
  done
  command /usr/bin/env "${scrub[@]}" CHOUSA_GREP_PIN_ECHO=1 "$@"
}
export -f env
'''
BENIGN_FUNCTION = '''r37_reexport() {
  export CHOUSA_GREP_PIN_ECHO=1
  export CHOUSA_STRICT=1
}
export -f r37_reexport
r37_reexport
'''

SPECS = [
    ('control-plain', 'control'),
    ('ENV-posix-noninteractive', 'ENV'),
    ('ENV-posix-interactive', 'ENV'),
    ('ENV-SHELLOPTS-posix', 'ENV'),
    ('SHELLOPTS-posix', 'SHELLOPTS'),
    ('SHELLOPTS-noexec', 'SHELLOPTS'),
    ('SHELLOPTS-noexec-extglob', 'SHELLOPTS'),
    ('SHELLOPTS-noglob', 'SHELLOPTS'),
    ('SHELLOPTS-errtrace-functrace', 'SHELLOPTS'),
    ('BASHOPTS-failglob', 'BASHOPTS'),
    ('BASHOPTS-nullglob', 'BASHOPTS'),
    ('BASHOPTS-inherit_errexit', 'BASHOPTS'),
    ('BASHOPTS-extdebug', 'BASHOPTS'),
    ('BASHOPTS-nocasematch', 'BASHOPTS'),
    ('TMPDIR-missing', 'TMPDIR'),
    ('TMPDIR-no-permission', 'TMPDIR'),
    ('TMPDIR-session-path', 'TMPDIR'),
    ('TMPDIR-symlink', 'TMPDIR'),
    ('TMPDIR-newline', 'TMPDIR'),
    ('CDPATH-decoy', 'CDPATH'),
    ('CDPATH-newline', 'CDPATH'),
    ('BASH_ENV-directory', 'BASH_ENV'),
    ('BASH_ENV-unreadable', 'BASH_ENV'),
    ('BASH_ENV-root-symlink-farm', 'BASH_ENV'),
    ('BASH_ENV-exportf-benign', 'functions'),
    ('BASH_ENV-exportf-env-reinsert', 'functions'),
    ('exportf-env-without-BASH_ENV', 'functions'),
    ('BASH_ENV-sets-TMPDIR-session-path', 'TMPDIR'),
    ('BASH_ENV-exports-BASHOPTS-failglob', 'BASHOPTS'),
]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write_fixture(path, body, fixtures, mode=0o600):
    path.write_text(body)
    path.chmod(mode)
    fixtures.append({'path': str(path), 'mode': oct(mode), 'content': body})
    return str(path)


def invocation(argv, cwd, purpose):
    proc = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=120)
    return {'purpose': purpose, 'cwd': str(cwd), 'command': shlex.join(argv),
            'argv': argv, 'stdout': proc.stdout, 'stderr': proc.stderr,
            'exit_code': proc.returncode}


def run_case(spec):
    sid, family = spec
    sdir = WORK / sid
    sdir.mkdir()
    captures = sdir / 'captures'
    captures.mkdir()
    base_env = {'PATH': '/usr/bin:/bin', 'HOME': str(HOME), 'LC_ALL': 'C',
                'TMPDIR': str(captures)}
    pin_env = dict(base_env)
    pin_shell = ['/usr/bin/bash']
    fixtures = []
    checks = {}
    if sid.startswith('ENV-'):
        startup = sdir / 'posix-startup.sh'
        root = sdir / 'foreign-root'
        root.mkdir()
        body = ('printf "ENV_STARTUP_RAN\\n" >>' + shlex.quote(str(sdir / 'startup-ran')) + '\n'
                'export CHOUSA_GREP_PIN_ECHO=1\nexport CHOUSA_ROOT=' + shlex.quote(str(root)) + '\n')
        pin_env['ENV'] = write_fixture(startup, body, fixtures)
        if sid == 'ENV-posix-interactive':
            pin_shell += ['--posix', '-i']
        elif sid == 'ENV-SHELLOPTS-posix':
            pin_env['SHELLOPTS'] = 'posix'
        else:
            pin_shell += ['--posix']
    elif sid.startswith('SHELLOPTS-'):
        pin_env['SHELLOPTS'] = {
            'SHELLOPTS-posix': 'posix',
            'SHELLOPTS-noexec': 'noexec',
            'SHELLOPTS-noexec-extglob': 'noexec',
            'SHELLOPTS-noglob': 'noglob',
            'SHELLOPTS-errtrace-functrace': 'errtrace:functrace',
        }[sid]
        if sid == 'SHELLOPTS-noexec-extglob':
            pin_env['BASHOPTS'] = 'extglob'
    elif sid.startswith('BASHOPTS-'):
        pin_env['BASHOPTS'] = sid[len('BASHOPTS-'):]
    elif sid.startswith('TMPDIR-'):
        if sid == 'TMPDIR-missing':
            pin_env['TMPDIR'] = str(sdir / 'missing-parent')
        elif sid == 'TMPDIR-no-permission':
            tmp = sdir / 'no-permission'
            tmp.mkdir(mode=0o000)
            pin_env['TMPDIR'] = str(tmp)
            checks['tmpdir_writable'] = os.access(tmp, os.W_OK)
        elif sid == 'TMPDIR-session-path':
            tmp = sdir / '.config'
            tmp.mkdir()
            pin_env['TMPDIR'] = str(tmp)
        elif sid == 'TMPDIR-symlink':
            tmp = sdir / 'temp-alias'
            tmp.symlink_to(captures, target_is_directory=True)
            pin_env['TMPDIR'] = str(tmp)
        elif sid == 'TMPDIR-newline':
            tmp = sdir / 'capture\nGATE_GREP: tmpdir-marker'
            tmp.mkdir()
            pin_env['TMPDIR'] = str(tmp)
    elif sid.startswith('CDPATH-'):
        decoy = sdir / 'cd-decoy'
        decoy.mkdir()
        for part in ('lib', 'noise', 'lane', 'tools'):
            (decoy / part).mkdir()
        value = str(decoy) + ':.:/tmp'
        if sid == 'CDPATH-newline':
            value += '\nGATE_GREP: cdpath-marker'
        pin_env['CDPATH'] = value
    elif sid == 'BASH_ENV-directory':
        startup = sdir / 'startup-directory'
        startup.mkdir()
        pin_env['BASH_ENV'] = str(startup)
    elif sid == 'BASH_ENV-unreadable':
        startup = sdir / 'unreadable-startup.sh'
        pin_env['BASH_ENV'] = write_fixture(startup, 'export CHOUSA_GREP_PIN_ECHO=1\n', fixtures, 0o000)
        checks['bash_env_readable'] = os.access(startup, os.R_OK)
    elif sid == 'BASH_ENV-root-symlink-farm':
        foreign = sdir / 'foreign-root'
        foreign.mkdir()
        for part in ('lib', 'noise'):
            (foreign / part).mkdir()
        write_fixture(foreign / 'lib/primary.md', 'FOREIGN PRIMARY MATERIAL\n', fixtures)
        write_fixture(foreign / 'noise/chat-export-sources.md', 'foreign noise\n', fixtures)
        farm = sdir / 'symlink-farm'
        farm.mkdir()
        for part in ('lib', 'noise'):
            (farm / part).symlink_to(foreign / part, target_is_directory=True)
        previous = farm
        for index in range(16):
            link = sdir / ('root-link-%02d' % index)
            link.symlink_to(previous, target_is_directory=True)
            previous = link
        startup = sdir / 'root-startup.sh'
        write_fixture(startup, 'export CHOUSA_ROOT=' + shlex.quote(str(previous)) + '\n', fixtures)
        startup_link = sdir / 'startup-link.sh'
        startup_link.symlink_to(startup)
        pin_env['BASH_ENV'] = str(startup_link)
        checks['root_symlink_hops'] = 16
        checks['root_resolves_to'] = str(previous.resolve())
        checks['farm_lib_resolves_to'] = str((previous / 'lib').resolve())
    elif sid == 'BASH_ENV-exportf-benign':
        pin_env['BASH_ENV'] = write_fixture(sdir / 'startup.sh', BENIGN_FUNCTION, fixtures)
    elif sid == 'BASH_ENV-exportf-env-reinsert':
        pin_env['BASH_ENV'] = write_fixture(sdir / 'startup.sh', ENV_FUNCTION, fixtures)
    elif sid == 'exportf-env-without-BASH_ENV':
        pin_shell = ['/usr/bin/bash', '-c', ENV_FUNCTION + 'exec /usr/bin/bash "$@"\n', '_']
    elif sid == 'BASH_ENV-sets-TMPDIR-session-path':
        tmp = sdir / '.config'
        tmp.mkdir()
        pin_env['BASH_ENV'] = write_fixture(sdir / 'startup.sh',
            'export TMPDIR=' + shlex.quote(str(tmp)) + '\n', fixtures)
    elif sid == 'BASH_ENV-exports-BASHOPTS-failglob':
        pin_env['BASH_ENV'] = write_fixture(sdir / 'startup.sh',
            'shopt -s failglob\nexport BASHOPTS\n', fixtures)
    pin_argv = ['/usr/bin/env', '-i'] + [key + '=' + value for key, value in pin_env.items()]
    pin_argv += pin_shell + [str(GATE), '--pin', 'baseline.txt']
    pin = invocation(pin_argv, sdir, 'hostile --pin')
    drift_argv = ['/usr/bin/env', '-i'] + [key + '=' + value for key, value in base_env.items()]
    drift_argv += ['/usr/bin/bash', str(GATE), '--drift', 'baseline.txt']
    drift = invocation(drift_argv, sdir, 'plain --drift')
    baseline = sdir / 'baseline.txt'
    text = baseline.read_text() if baseline.is_file() else None
    body = text.split(MARKER, 1)[1] if text and MARKER in text else None
    if sid.startswith('ENV-'):
        checks['ENV_startup_ran'] = (sdir / 'startup-ran').exists()
    return {'id': sid, 'family': family, 'fixtures': fixtures, 'fixture_checks': checks,
            'pin': pin, 'drift': drift, 'baseline_exists': baseline.is_file(),
            'baseline_sha256': sha(text.encode()) if text is not None else None,
            'capture_sha256': sha(body.encode()) if body is not None else None,
            'capture': body, 'baseline_echo_lines':
                [line for line in text.splitlines() if line.startswith('GATE_GREP: ')]
                if text is not None else [],
            'drift_lines': [line for line in drift['stdout'].splitlines()
                            if line.startswith('GATE_DRIFT: ')]}


def main():
    observed_sha = sha(GATE.read_bytes())
    if observed_sha != EXPECTED_SHA:
        raise SystemExit('scratch gate digest mismatch: ' + observed_sha)
    control = run_case(SPECS[0])
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        attacked = list(pool.map(run_case, SPECS[1:]))
    rows = [control] + attacked
    for row in rows:
        row['capture_matches_control'] = (row['capture'] == control['capture']) if row['capture'] is not None else None
        row['capture_diff'] = ''.join(difflib.unified_diff(
            (control['capture'] or '').splitlines(keepends=True),
            (row['capture'] or '').splitlines(keepends=True),
            fromfile='plain-control', tofile=row['id'])) if row['capture'] is not None else ''
    receipt = {'gate': str(GATE), 'gate_sha256': observed_sha,
               'uid': os.getuid(), 'euid': os.geteuid(), 'cases': rows}
    (WORK / 'vectors.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print('GATE_SHA256=' + observed_sha)
    print('CASES=' + str(len(rows)))
    for row in rows:
        print(json.dumps({key: row[key] for key in (
            'id', 'baseline_exists', 'baseline_echo_lines', 'capture_matches_control', 'drift_lines', 'fixture_checks')}, sort_keys=True)
              + ' pin_rc=' + str(row['pin']['exit_code']) + ' drift_rc=' + str(row['drift']['exit_code']))
    print('RECEIPT=' + str(WORK / 'vectors.json'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
```
