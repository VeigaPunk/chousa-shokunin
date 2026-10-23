# ExecPinEchoStability — echo-flag stability / no-harm proof for the pin's default path

Wave: round-35 w2. Lane: `chousa-shokunin`. Seat: leaf executor. Date: 2026-10-23.
Scope: for every mode the gate supports, byte-diff stdout+stderr of a run **without**
`CHOUSA_GREP_PIN_ECHO` against the same run on `.ufo/waves/round-35/repairs/base-gate.sh`
(same inputs, same cwd, same scratch). Also: does the flag itself perturb anything when set.

## Verdict

**PASS for the default path.** With `CHOUSA_GREP_PIN_ECHO` unset, the landed gate
(`1f2fb4f5…`) is **byte-identical** to the round-34 base blob (`a6307edf…`) on **every mode
and every error path tested** — stdout, stderr and exit code — with exactly one exception
that is self-identity, not behaviour: `--pin`/`verify-all --json` stamp the gate's own
`sha256`, which necessarily differs between two different files (and is the masked
volatile `gate_sha256` in the drift contract).

**One real defect found (echo=1 only, does not affect the default path):** the echo line
leaks into the **persisted `--pin` baseline body**, and a later `--drift` run at the other
flag state reports a **false DRIFT (exit 1)**. Detail in F1.

No stray `GATE_GREP:` line exists in any echo-off run (stdout or stderr), and the echo line
is stderr-only, never stdout.

## Pinned gates I scored

| role | path (scratch copy) | sha256 |
|---|---|---|
| landed (contract) | `…/ExecPinEchoStability/land-gate.sh` | `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617` |
| base / pre-round | `…/base-gate.sh` (= `.ufo/waves/round-35/repairs/base-gate.sh`) | `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b` |
| control **base+pin only** (mine; R1/R2 reverted) | `…/basepin-gate.sh` | `fa2fc738bcf66b2e0786eefb1de950a00be39dcc3648c95e5e36fbc01d790129` |

Landed gate obtained from a clone checked out at the wave base revision
`e87c5d7ea2dbf3730b36a3961de3f06261d015e4` (`git clone -q` + `git checkout -q`), so the
file bytes are the contract's, not the live working tree's.

> **Lane-state note (not my edit).** At session start the live
> `tools/research-gate.sh` hashed to `1f2fb4f5…`; while I ran, it became
> `a4768851 8e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad` (uncommitted `M`),
> a different pin implementation (wrapper defined after resolve, `timeout`-bounded
> `--version`, PATH fallback removed). **Every result below is for `1f2fb4f5…` only.**
> I did not touch the live tree.

## Method

One copied fleet tree so every printed path, `SELF` and `LANE_ROOT` are identical across
variants; the gate file alone is swapped in place at
`fleet/chousa-shokunin/tools/research-gate.sh`.

```
cd /tmp/hyaku/chousa-r35/w2/ExecPinEchoStability
bash matrix.sh        # Axis A (variants) + Axis B (echo flag), stdout/stderr captured SEPARATELY
bash drift-probe.sh   # --pin/--drift under both flag states
bash selftest-probe.sh# --selftest x {base,land} x {echo off,on}
bash probe-pinpath.sh # no-grep-on-PATH degradation + same-path pin A/B
bash probe-extra.sh   # no-args, --record, claims-as-record, --as-of, --registry, --json, missing inputs
```

Fixed environment for every run (clean, deterministic, no caller leakage):

```
env -i PATH=/usr/local/bin:/usr/bin:/bin HOME=/tmp TMPDIR=/tmp LANG=C.UTF-8 LC_ALL=C.UTF-8
       CHOUSA_NOW_EPOCH=1761000000 [CHOUSA_GREP_PIN_ECHO=1]
cwd = fleet/chousa-shokunin ; gate = bash tools/research-gate.sh …
```

`CHOUSA_NOW_EPOCH` is fixed so `ts=` is stable. Inputs are the committed fixtures
(`corpus/fixtures/full-r6.md`, `full-r6-broken.md`, `full-r6.claims.jsonl`,
`integrity-r7.md`, `metadata-r25/verified-at-below-heading.md`, `metadata-r25/recheck-90d.md`)
with `--root ..` over a copy of the fleet `research/` tree.

## Axis A — landed (echo unset) vs `base-gate.sh`: one row per mode

`SAME` = stdout **and** stderr **and** rc byte-identical.

| mode / invocation | base rc | land rc | stdout+stderr |
|---|---|---|---|
| `--help` | 0 | 0 | **byte-identical** |
| `--selftest` | 0 | 0 | **byte-identical** — `RESEARCH_GATE_SELFTEST: PASS (256 cases, 0 skipped)`, 12781 B both, 0 B stderr both |
| `verify <record>` (CLEAN) | 0 | 0 | **byte-identical** |
| `verify <record>` (DRIFT twin) | 0 | 0 | **byte-identical** |
| `verify-claims <claims>` | 0 | 0 | **byte-identical** |
| `verify-chain <record>` | 0 | 0 | **byte-identical** |
| `verify-sweeps <record>` | 0 | 0 | **byte-identical** |
| `verify-integrity <record>` | 0 | 0 | **byte-identical** |
| `verify-metadata <entry>` | 1 | 1 | **byte-identical** |
| `verify-all <record> --claims …` | 0 | 0 | **byte-identical** |
| `verify-all … --json <m>` | 0 | 0 | stdout/stderr **byte-identical**; manifest differs **only** in `gate_sha256` |
| `--pin <path>` | 0 | 0 | **only diff**: `gate_sha256=` in the `GATE_PIN:` line and in the baseline's `# gate_sha256=` header. Baseline body otherwise identical (`diff` after removing that line: identical). |
| `--drift <baseline>` | 0 | 0 | **byte-identical** (`GATE_DRIFT: none`) |
| `--drift <missing>` | 2 | 2 | **byte-identical** |
| no args | 2 | 2 | **byte-identical** (usage) |
| `--no-such-flag` | 2 | 2 | **byte-identical** (usage) |
| `verify` (no record) | 2 | 2 | **byte-identical** (usage) |
| `verify --record … --root ..` | 0 | 0 | **byte-identical** |
| `verify-all <claims.jsonl> --root ..` | 0 | 0 | **byte-identical** |
| `verify-metadata … --as-of 2026-01-15` | 0 | 0 | **byte-identical** |
| `verify-metadata … --as-of 2026-02-30` | 2 | 2 | **byte-identical** |
| `verify-metadata … --registry <readme>` | 2 | 2 | **byte-identical** |
| `verify-claims <absent>` | 2 | 2 | **byte-identical** |
| `verify <absent>` | 2 | 2 | **byte-identical** |

**Attribution control.** `basepin` (base bytes + the pin block only, R1 `slen` repair and
R2 comments reverted) is byte-identical to `land` on **all 24** cases above — so the R1
`slen` repair contributes **no** observable output difference on these paths, and the pin
block alone is output-neutral. Both are also identical to `base`.

Raw table: `ExecPinEchoStability/summary-tables.txt` (Axis A block).

## Axis B — the flag itself: landed `CHOUSA_GREP_PIN_ECHO=1` vs unset

| mode | stdout | stderr | delta |
|---|---|---|---|
| `verify`, `verify-drift`, `verify-claims`, `verify-chain`, `verify-sweeps`, `verify-integrity`, `verify-metadata`, `verify-all`, `verify-all --json` | **identical** | DIFF | exactly `+1` line, 85 B: `GATE_GREP: path=/usr/bin/grep source=default version="grep (GNU grep) 3.12-modified"` |
| `--pin <same path>` | **identical** | DIFF | `+1` stderr line **plus** the baseline body leak (F1) |
| `--drift <baseline>` | identical | DIFF | `+1` stderr line; **result flips** when pin/drift flag states differ (F1) |
| `--help` | identical | **identical** | no `GATE_GREP` line at all (F2) |
| `--no-such-flag` | identical | **identical** | no `GATE_GREP` line at all (F2) |
| `verify` with no record | identical | DIFF | `+1` stderr line, **prepended before** the usage text (F2) |
| `--drift <missing>` | identical | DIFF | `+1` stderr line, prepended before the error |

The echo line is emitted with `>&2` (`land-gate.sh:396-398`) and lands on **stderr only**;
`verify-all --json` manifests are byte-identical with the flag on and off.

Nested-invocation containment: `verify-all` runs its 5 sections as
`bash "$SELF" <mode> … 2>&1` (`land-gate.sh:3504`), so each child prints its own
`GATE_GREP:` under echo=1 — but those are absorbed into `VAS_OUT` and never re-emitted.
Measured: the outer process's stderr gains **exactly one** line, section tallies and
`SECTION`/`FINDING` lines unchanged.

## Findings

### F1 — (real, echo=1 only) the flag mutates the persisted `--pin` baseline, and `--drift` then reports false drift

`gate_canonical_capture` runs the canonical invocation and captures **both** streams:

```
land-gate.sh:3862-3866
  ( cd "$fx" || exit 2
    env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_STRICT -u CHOUSA_ROOT \
      -u CHOUSA_AGGREGATOR_ERE \
      bash "$SELF" verify-all record.md --claims claims.jsonl \
      --json manifest.jsonl --root . >capture.txt 2>&1 ) || rc=$?
```

The `env -u` list sanitizes five `CHOUSA_*` names but **not `CHOUSA_GREP_PIN_ECHO`**, so the
nested gate's echo line is captured into `capture.txt` and becomes part of the baseline body.

Measured, same baseline path both times:

```
$ diff baseline-echooff.txt baseline-echoon.txt
8a9
> GATE_GREP: path=/usr/bin/grep source=default version="grep (GNU grep) 3.12-modified"
off = 2989 B, on = 3074 B   (leaked line = line 9, immediately after
"# --- canonical output follows ---")
```

Consequences measured (`out-drift/summary.txt`), baseline pinned and drifted at each
flag state:

| baseline pinned with | drift run with | result |
|---|---|---|
| echo off | echo off | `GATE_DRIFT: none`, rc 0 |
| echo on | echo on | `GATE_DRIFT: none`, rc 0 |
| **echo on** | **echo off** | `GATE_DRIFT: -LINE`, **rc 1** (false drift) |
| **echo off** | **echo on** | `GATE_DRIFT: +LINE`, **rc 1** (false drift) |

So a receipt flag documented as an observation aid silently changes a *persisted
behavioural artifact* and makes `--drift` stateful across flag usage. The failure is in the
safe direction (fail-closed DRIFT, never a false CLEAN), and it cannot occur on the default
path because the flag is off by default — but an operator who pins with
`CHOUSA_GREP_PIN_ECHO=1` (the natural way to record pin provenance) poisons the baseline for
every later echo-off drift, and vice versa.

Secondary: the drift diagnostic is uninformative. `gate_drift_line_id` (`land-gate.sh:3888-3900`)
has no case for `GATE_GREP:`, so it falls through to `*` → `LINE`; the report reads `±LINE`
and never names the offending line. A fix would add `-u CHOUSA_GREP_PIN_ECHO` to the
`env -u` list at `land-gate.sh:3863` (and/or keep stderr out of `capture.txt`).

### F2 — (minor) the echo line's presence is error-path dependent

`grep_pin_init` is called **after** the argument loop (`land-gate.sh:8039`), while
`-h|--help` and `die_usage` for unknown flags exit **inside** it. Result with echo=1:

- `--help` → no `GATE_GREP:` line
- `--no-such-flag` → no `GATE_GREP:` line
- `verify` (no record) → `GATE_GREP:` line **then** the usage text
- `--drift <missing>` → `GATE_GREP:` line **then** the error

A receipt consumer cannot assume "echo flag on ⇒ exactly one `GATE_GREP:` line per
invocation". This is arguably intended ("usage/--help paths return earlier", the comment at
`land-gate.sh:8036-8038`), but it is an asymmetry worth recording because it makes the echo
surface exit-path-dependent rather than mode-dependent.

### Non-findings (checked, clean)

- **No stray `GATE_GREP:` with the flag unset.** `grep -rl GATE_GREP` over every echo-off
  stdout/stderr of Axis A (base, basepin, land) and Axis B (off) → **no hits**.
- **Echo never reaches stdout.** stdout is byte-identical on/off for every mode except
  `--pin`, whose difference is the output path in my harness (same-path A/B: stdout
  byte-identical, `land.pinA.out` vs `land.pinB.out`).
- **No-grep-on-PATH degradation differs from base — by design, and it is the C1 win, not a
  regression.** With a PATH carrying every tool the gate needs *except* `grep`:
  base → `verify` rc 0 but **232 B of stderr noise** (`grep: command not found` ×4, silent
  degradation) and `verify-claims` **rc 2**; landed → every mode rc 0 with **0 B stderr** and
  output byte-identical to its clean-PATH run. This is the one environment where the landed
  gate legitimately differs from base; it is the claimed behaviour, reported here so the
  no-harm claim is not overstated.
- **`--selftest` is unaffected**: 256/256 cases, 0 skipped, byte-identical stdout across
  {base, land} × {echo off, on}; the only stderr difference is the single echo line.

## Limits

- Scored gate is `1f2fb4f5…`; the live lane's `tools/research-gate.sh` moved to
  `a4768851…` mid-wave (not mine). Nothing here applies to that variant.
- One host, one grep (`GNU grep 3.12-modified` at `/usr/bin/grep`), clean controlled PATH.
  I did not test uutils/pi-uu-grep as the resolved binary (that is the C1 counter's surface).
- Fixtures are the committed corpus set, not the counters' randomized fixtures; the C1/C2
  counters were not run by this seat.
- `--pin` comparisons hold the gate file's own sha256 out as self-identity; a stricter
  "byte-identical including self-sha" comparison between two different gate files is
  impossible by construction.
- `verify-metadata` was exercised on 2 of the 27 `metadata-r25` entries plus `--as-of` and
  `--registry` paths.

## Retained evidence

All under `.ufo/waves/round-35/w2/ExecPinEchoStability/` (52 KB total):

| file | what |
|---|---|
| `summary-tables.txt` | Axis A + Axis B byte tables (the report's rows, raw) |
| `GATE-SHAS.txt` | sha256 of every scored gate variant + baselines |
| `baseline-echooff.txt` / `baseline-echoon.txt` | the exact 2989 B / 3074 B pin artifacts whose diff is F1 |
| `drift-summary.txt` | the 4-cell pin×drift false-drift matrix (F1) |
| `selftest-summary.txt` | 256-case selftest, three ways, identical |
| `pinpath-summary.txt` | no-grep-on-PATH base-vs-land + same-path pin A/B |
| `extra-summary.txt` | 9 extra invocation forms, base/basepin/land |
| `matrix.sh`, `drift-probe.sh`, `selftest-probe.sh`, `probe-pinpath.sh`, `probe-extra.sh` | re-runnable drivers |

Scratch trees (large, cited by path): `/tmp/hyaku/chousa-r35/w2/ExecPinEchoStability/`
with `fleet/` (single fixed tree), `outA/` (138 files), `outB/` (88), `out-drift/`,
`out-selftest/`, `out-pinpath/`, `out-extra/`.
