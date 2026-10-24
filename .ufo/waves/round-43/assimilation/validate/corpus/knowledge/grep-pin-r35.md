# Pinned tool provenance — one absolute, verified grep

Lane: chousa. Round 35 (C1). Gate surface: `tools/research-gate.sh`, matcher
paths `tok_span_offsets_direct` / `tok_span_offsets_chunk` and every other
`grep` invocation in the same shell.

source: S067 (exec(3), PATH search) and S068 (bash(1), `BASH_ENV`), both opened 2026-10-23;
lane gate `tools/research-gate.sh` and counters `corpus/evidence/round35/c1-count.py`,
`corpus/evidence/round35/c2-count.py`; receipts `.ufo/waves/round-35/{controls,measure,final}/`,
`.ufo/waves/round-35/w2/` (wave seats).
verified-at: 2026-10-23 (round 35; gate SHA-256 `a47688518e50…c38ad`; `GREP_PIN_MATCH=9/9` on
seeds 3529/3539, `.ufo/waves/round-35/final/c1-s*.json`)
recheck: on-release (`python3 corpus/evidence/round35/c1-count.py --seed <n>` → 9/9; and
`CHOUSA_GREP_PIN_ECHO=1 bash tools/research-gate.sh --selftest 2>&1 | grep -m1 '^GATE_GREP: '`)

## What was wrong

The gate called bare `grep` at each matcher site, so the binary that ran was a
function of the caller's environment:

- **PATH first.** `exec*p()` seeks a bare name in the colon-separated `PATH`
  list (S067; the page states the list, not its order), and the round-35
  counter measured a shim listed first actually winning. Measured on this host: with a
  `grep` script first on `PATH`, the round-34 gate executed it on every
  matcher call (counter S1 tripwire: 852 bytes of shim log) and produced the
  *same verdicts* — the substitution was invisible in output.
- **Imported shell functions.** A non-interactive bash sources `$BASH_ENV`
  before the script body (S068), so a `grep()` function planted there can
  shadow the command for the whole gate. Round-35 counter S2 measured the
  base gate executing the planted function (867 bytes of log).
- **No grep, no gate.** With a `PATH` that holds every other tool but no
  `grep`, the base gate cannot run at all: `token_matcher_require` fails and
  `verify-claims` exits 2 (counter S3).
- **The host's own shells lie.** The interactive shell on this workstation
  carries a `grep (pi-uu-grep) 0.2.0` uutils grep as a shell builtin
  (`type -a grep` → "grep is a shell builtin" before `/usr/bin/grep`), while
  pacman owns `grep 3.12-2`. A re-check run from that shell without
  `command grep` or an absolute path measures a different program. The gate
  itself could not name, or prove, which one it used.

## What the gate does now

`grep_pin_init` runs once, after argument parsing and before any mode reads a
record:

1. `RESEARCH_GATE_GREP`, when set, must be an **absolute** path, a regular
   file and executable, and its `--version` first line must contain `GNU grep`.
2. Otherwise the gate tries `/usr/bin/grep`, then `/bin/grep`, then an
   absolute `command -v grep` result — each through the same check.
3. A pin that cannot be verified is refused **before any record is read**:
   `research-gate: GREP_PROVENANCE refused: <reason> (candidate=<path>)` and
   exit 2. It is never silently downgraded to the base binary.
4. Every `grep` call in the gate's shell — pipelines, process substitutions,
   command substitutions and the selftest's child invocations — runs the
   pinned absolute path through one `grep()` wrapper defined in the script
   (the script's own definition wins over an imported `BASH_ENV` function).
5. `CHOUSA_GREP_PIN_ECHO=1` prints the pin for a receipt:
   `GATE_GREP: path=/usr/bin/grep source=default|override version="grep (GNU grep) 3.12-modified"`.
   Off by default: every existing mode keeps its byte-identical output.

## What this does not prove

Provenance is **self-reported**: a binary that prints a GNU line for
`--version` and then behaves differently passes the check. The pin also says
nothing about a binary's *correctness*, only that one named, absolute program
is the one the gate runs. A caller who can write to `/usr/bin` can replace the
binary; the pin bounds *which path is executed*, not the integrity of that
path. (An integrity pin — a recorded SHA-256 of the binary — is the natural
next step and is not claimed here.)

## Evidence

- Counter: `corpus/evidence/round35/c1-count.py` → 9/9 on seeds 3501 and 3517
  against gate `1f2fb4f5…` (`.ufo/waves/round-35/measure/c1-after-s*.json`).
  Base gate: 0/9 (`.ufo/waves/round-35/controls/c1-base-s3501.json`). Cheapest
  non-oracle control — hardcoded `/usr/bin/grep` wrapper, no check, no
  override, no echo: 3/9 (`controls/c1-hardcoded-s3501.json`).
- Design and kill rule: `corpus/evidence/round35/claims.md` §C1.
- Rows: S067 (exec(3), PATH search; quote at decompressed `/usr/share/man/man3/exec.3.gz`
  lines 107–110), S068 (bash(1), `BASH_ENV`; quote at lines 391–395).
