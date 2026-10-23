# MutGrepShimEnv — environment-shadow controls for C1 (grep pin), round 35 w2

Date: 2026-10-23. Gate scored: `tools/research-gate.sh` copied byte-identical to
`/tmp/hyaku/chousa-r35/w2/MutGrepShimEnv/gate-landed.sh`,
sha256 `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617`
(equals the landed-gate prefix in the tasking; verified with `sha256sum`). Base gate
`.ufo/waves/round-35/repairs/base-gate.sh` = `a6307edf...2995b`, as frozen. Host bash
5.3.20(1), GNU grep 3.12-modified, `/usr/bin/grep`. No network, no installs, no lane
writes; every receipt below carries `gate_sha256=1f2fb4f5...`. Scratch:
`/tmp/hyaku/chousa-r35/w2/MutGrepShimEnv/`; report artifacts in the sibling directory
of this file (132 KiB total).

## What was attacked

The target: the gate's pin is `GREP_BIN=''` (gate:348), `grep() { command "$GREP_BIN" "$@"; }`
(gate:351), `set -euo pipefail` (gate:292), `grep_pin_init` called at gate:8039, and the
matcher pipelines `... | grep -a -z -b -o -P -- "$regex"` (gate:1687, 1716). The gate's own
comment claims: "every grep call in this shell runs that absolute path through the wrapper
below" (gate:339-340). Four caller-environment channels were built and scored.

## Results (all commands run; probe receipt `probe-receipt.json`)

`python3 probe.py` runs the pinned gate on a fixed 3-claim fixture under each shadow and
records rc / DRIFT / claim verdicts / trip logs. Baseline P0: rc=1, DRIFT, verdicts
`match, mismatch, mismatch`.

| # | shadow | intercepts (trip) | rc / output | verdict |
|---|---|---|---|---|
| P1 | `BASH_ENV` defines `grep()` logging, forwarding to /usr/bin/grep | 0 | rc=1, identical | **SURVIVED** (script def wins) |
| P2 | exported `BASH_FUNC_grep%%` via `env` | 0 | rc=1, identical | **SURVIVED** |
| P3 | P1 + `readonly -f grep` in BASH_ENV | 0 | **rc=1, no output**, `gate-landed.sh: line 351: grep: readonly function` | **REFUTED (fail-closed DoS)** |
| P4 | P2 + `readonly -f grep` in BASH_ENV | 0 | same line-351 death | REFUTED (DoS) |
| P5 | `shopt -s expand_aliases; alias grep=...` in BASH_ENV | 0 | **rc=2**, `line 351: syntax error near unexpected token '('` | fail-closed, gate unusable |
| P6 | `BASH_ENV` defines `command()` logging, `builtin command "$@"` | **5** | rc=1, **identical** | **INTERCEPTED silently** |
| P7 | exported `BASH_FUNC_command%%` | **5** | rc=1, identical | INTERCEPTED silently |
| P8 | `BASH_ENV` `head()` rewriting `pi-uu-grep`→`GNU grep`, stdout-version stub as override | 0 | rc=2 but **generic** `GNU grep with -z/-P support is required`, **no `GREP_PROVENANCE`** | version check bypassed, layer 2 catches |
| P8b | same stub, no shadow | – | rc=2, `GREP_PROVENANCE refused: ... pi-uu-grep 0.2.0` | control: named refusal works |
| P9 | `ENV=` with a grep function | 0 | rc=1, identical | **channel vacuous** |
| P10 | `BASH_ENV` `readonly GREP_BIN=/usr/bin/grep` | 0 | rc=1, no output, `line 348: GREP_BIN: readonly variable` | fail-closed DoS |

### Definition order: proven for plain functions, refuted as an invariant

The minimal trace (`mini_override.sh`, BASH_ENV grep fn; calls before and after the script's
own `grep(){...}`): trip log contains exactly one line (`ENVFN one`) — the pre-definition
call — and nothing after; script rc=0, both greps correct. Positive control that exported
functions really are imported by bash 5.3: `type -t grep` → `function`, and the early call is
logged (`trip-exp.log`: `EXP first`, `EXP one`), the post-definition call is not. On the real
gate P1/P2 give 0 intercepts and byte-identical output. So **the script's definition wins for
ordinary definitions** — that part of the target's hypothesis is proven.

It does not hold as a guarantee. Two refutations, both in the caller environment:

1. **Readonly freeze (P3/P4/P10).** `readonly -f grep` (or `readonly GREP_BIN`) makes the
   script's own assignment/definition fail under `set -e`; the gate dies before `grep_pin_init`
   (gate:8039) with **rc=1 and no `RESEARCH_GATE:` line and no CLAIM lines**. rc=1 is also the
   gate's DRIFT code, so a caller can make the gate exit "drift" with an empty verdict. Fail-closed,
   but indistinguishable from a measured DRIFT by exit code.
2. **The `command` builtin is itself shadowable (P6/P7).** Every matcher call reaches
   `command "$GREP_BIN" "$@"`, and a function named `command` receives the full argv. Captured
   verbatim in one 3-claim run (`trip-cmd2`/`trip-cmd.log`):
   `cmd /usr/bin/grep -a -z -b -o -P -- \x61\x6c...`, `cmd /usr/bin/grep -Fn -m1 -e charlie`,
   the three span matcher calls plus the `-z/-P` capability probe. Output identical to baseline.

### The MEETS-class finding: a shadow that scores 9/9 while the pinned binary never matches

Built `alt-grep.py`: for the exact matcher shape `-a -z -b -o -P -- \xHH...` it decodes the
pattern and answers from a Python `bytes.find` exact search (emits `offset:match\0`, the
format `${occurrence%%:*}` at gate:1686/1711 consumes); every other argv is handed to `/usr/bin/grep`. A
`BASH_ENV` `command()` shim redirects the pinned absolute path into it. Result on the fixture
(`alt.out` vs reference `p6.out`): **byte-identical output modulo the timestamp**; engine log
shows 3 span matchers answered by `python`, 2 harness calls by real grep; the gate still
believes its only binary is `/usr/bin/grep`.

Scored with the committed counter:

```
BASH_ENV=bash_env_altengine.sh python3 corpus/evidence/round35/c1-count.py --gate gate-landed.sh --seed 3501
GREP_PIN_MATCH=9/9   (counter_rc=0; receipt c1-altengine-s3501.json, gate_sha 1f2fb4f5...)
engine log across the counter's 10 gate runs: 15× python, 5× exec--a, 5× exec--Fn
```

S1/S2/S9 tripwires stay at 0 bytes because they watch only a PATH shim and a `grep()` function;
no scenario installs `command` (or `head`, or `printf`). A caller-environment shadow, in the
same channel S2 already treats as adversarial, therefore **scores 9/9 while substituting the
matcher engine**. This is a coverage finding for C1's counter, not a claim about output
correctness: the substituted engine was a correct one.

### Forged provenance: a non-GNU binary is pinned and the receipt line is forged

`bash_env_forge.sh` = `head()` rewriting `pi-uu-grep`→`GNU grep` plus a `command()` shim
redirecting the stub path. With `RESEARCH_GATE_GREP=<stub>` and `CHOUSA_GREP_PIN_ECHO=1`:

```
rc=1
GATE_GREP: path=/tmp/hyaku/chousa-r35/w2/MutGrepShimEnv/stub-pi-uu-grep source=override version="GNU grep 0.2.0"
(stderr, no GREP_PROVENANCE)
output diff vs real-grep reference: IDENTICAL (modulo ts)
engine log: 3 python, 2 exec; stub executed for no match call
```

`grep_pin_verify` runs `"$cand" --version | head -n 1` (gate:361) and pattern-matches
`*"GNU grep"*`; both the subprocess output and the filter are caller-controlled. The stub,
which self-reports `pi-uu-grep 0.2.0`, is pinned, its version check is defeated by the `head`
function, and the capability probe at gate:1762 is answered by the `command` shim. C1's three
clauses — resolves, verifies, refuses-what-it-cannot-verify — are each false under this
environment. Running the C1 counter with this same `BASH_ENV` still prints **9/9**
(`c1-forge-s3501.json`): its S6 stub is a different file, so the forge is invisible to it.

The counter's S6 has a second, smaller calibration gap: its stub (`write_stub_non_gnu` in
`c1-count.py`) prints the version on **stderr**, which the gate discards (`2>/dev/null`), so
every committed S6 receipt records `<no version>` (see `c1-base-s3501.json` S6 `stderr_tail`).
S6 therefore passes through the *missing-version* branch, not the non-GNU-version branch its
docstring describes; my P8b stdout stub shows that branch works unshadowed.

### Channel (d): `ENV`/`sh` is vacuous

The gate never invokes `sh -c`. `grep -n '/bin/sh'` finds only `printf '#!/bin/sh\nexit 127\n'`
(gate:7734, a fixture file). The only sub-shell spawns are `bash -c` at gate:5867, 5880, 7006,
and none of those quoted blocks contains a `grep` call (checked with `sed ... | grep -n grep`).
Bash ignores `ENV` unless invoked as `sh`/POSIX; P9 with a logging `ENV` file and zero
intercepts confirms it. So the `ENV`/`sh` channel is empty today.

## Verdicts

- (a) `BASH_ENV` grep function: **survived** — cannot beat the script's definition (0
  intercepts, 9/9, identical output).
- (b) exported `BASH_FUNC_grep%%`: **survived**, import positively confirmed.
- Definition order as a general guarantee: **refuted** — `readonly -f grep` kills the gate
  (rc=1 masquerading as DRIFT), and `command` shadowing keeps output correct while the pinned
  binary is replaced.
- (c) alias in `BASH_ENV` with `expand_aliases`: fail-closed parse error at gate:351, rc=2;
  not a silent shortcut, but the gate is unusable under that environment.
- (d) `ENV` + `sh`: vacuous — no `sh` invocation on the matcher path.
- **C1 MEETS-class**: an environment shadow one function name away from the one S2 tests
  (`command`, plus `head` for the echo line) scores **9/9** on `c1-count.py`, substitutes the
  span matcher with a Python engine without changing output, and can pin a non-GNU stub while
  emitting a forged `GATE_GREP: ... version="GNU grep 0.2.0"`. The counter has no scenario
  that installs `command`/`head`/`printf` shadows and no assertion that the bytes on stderr
  come from the pinned binary; this is a coverage finding, not permission to change the
  contract.

## Limits

- One host, bash 5.3.20, GNU grep 3.12-modified; the pin's fallback order (`/usr/bin/grep`,
  `/bin/grep`, `command -v grep`) was not otherwise varied.
- The counter's reference run is executed in the same process environment as the scenarios,
  so output parity is self-referential: a shadow wrong only on inputs absent from the
  3-claim fixture would still satisfy S1–S9 [INFERENCE].
- Only the matcher/provenance surface was probed; long-span/chunk routing and C2 were not.
- All receipts pin gate sha `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617`;
  no lane, git or jj state was written.

## Evidence index (this directory, sha256 in parentheses)

`probe.py` (dc98f270...), `probe-receipt.json` (47a72c9c...), `alt-grep.py` (7aa732f2...),
`bash_env_{fn,fn_readonly,cmd,cmd2,alias,head,altengine,forge,readonly_grepbin}.sh`,
`stub-pi-uu-grep` (a367930c...), `alt-engine.log` (355f0a89...), `trip-cmd.log`,
`p6.out/p6.err` (real-grep reference), `alt.out/alt.err`, `forge.out/forge.err` (1e67be5a.../4b7b5a76...),
counter receipts `c1-base-s3501.json` (31d9a5d1...), `c1-base-s3591.json` (79e34d12...),
`c1-cmdshim-s3501.json` (e2dae2ab...), `c1-altengine-s3501.json` (64deac1d...),
`c1-headforge-s3501.json` (9cdef811...), `c1-forge-s3501.json` (95072cc5...).
