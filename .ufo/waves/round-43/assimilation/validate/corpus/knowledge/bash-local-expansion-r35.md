# One `local` statement evaluates every right-hand side before it assigns

Lane: chousa. Round 35 (R1). Surface: `tools/research-gate.sh`,
`tok_span_offsets_chunk` (the round-34 dead-zone matcher).

source: `bash(1)` is the shell executed (`bash 5.3.20-1`, S068 row is scoped to `BASH_ENV` only);
the fact itself is measured locally — `bash -c 'f(){ local a=$1 b=${#a}; echo $b; }; f hello'` → `0`,
and `.ufo/waves/round-35/repairs/slen-probe.sh` on the round-34 gate (`a6307edf…`, base copy
committed in `repairs/base-gate.sh`) vs the round-35 gate.
verified-at: 2026-10-23 (round 35; probe base `offsets=0` / landed `offsets=1 first=5` on gate
`a47688518e50…c38ad`; wave seats MutSlenScope and RevSlenSweep re-derived both directions)
recheck: on-release (`bash .ufo/waves/round-35/repairs/slen-probe.sh tools/research-gate.sh` → exit 0,
`offsets=1`; and the sweep `grep -nE 'local [^#]*(\$\{[#%]|\$\(\()' tools/research-gate.sh` → 0 hits)

## The fact

```bash
f() { local a=$1 b=${#a}; echo "$b"; }
f hello        # prints 0
g() { local a=$1; local b=${#a}; echo "$b"; }
g hello        # prints 5
```

Bash expands **all** of a `local`/`declare` statement's right-hand sides
before it assigns any of the names. A derived value written in the same
statement therefore reads whatever `a` was visible *before* the statement —
the caller's local (bash's dynamic scope) or a global — not the parameter.
`set -u` does not catch it because the name exists in the dynamic scope.

## What shipped and why it was latent

Round 34's chunk matcher carried
`local hay=$1 span=$2 slen=${#span} chunk pattern occurrence offset resume=0`.
`slen` read the **caller's** `span`, not `$2`. The only caller,
`tok_span_offsets`, declared `local hay=$1 span=$2` and passed its own `span`
unchanged, so `slen` happened to be the right number and no test failed: the
selftest (256 cases) and every counter scored identically before and after the
repair. The defect was found by a non-author spot-check
(`corpus/lessons/round-34-verifier-spotcheck.md` routed defect 4), not by any
instrument.

A direct call exposes it. `.ufo/waves/round-35/repairs/slen-probe.sh` extracts
the matcher block and calls `tok_span_offsets_chunk "$hay" "$long_span"` with a
visible `span` of a different length:

| gate | visible `span` | `SLEN_PROBE` |
|---|---|---|
| round-34 gate `a6307edf…` | `decoy_span_of_other_length` (26 B) | `offsets=0` |
| round-35 gate `1f2fb4f5…` | same | `offsets=1 first=5` |
| no visible `span` at all | — | base `0`, landed `1` |

## The repair

Split the statement: `local hay=$1 span=$2 …` then `local slen` then
`slen=${#span}`. The probe is the receipt, and it fails on the base gate, so a
regression flips it.

## The sweep rule

The same shape is a hazard anywhere a derived value shares the statement with
its source:

```bash
local n=${#x} x=$1          # reads the caller's x
local d=${x%.*} x=$1        # same
local i=$(( ${#s} - 1 )) s=$1
```

Rule: **a derived value never shares one `local` statement with the name it
derives from.** Grep shape (`grep -nE 'local [^#]*(\$\{[#%]|\$\(\()' <script>`)
and read each hit; the round-35 wave's `RevSlenSweep` seat audited the whole
gate against it.

## Evidence

- Probe: `.ufo/waves/round-35/repairs/slen-probe.sh` (base gate copy
  `repairs/base-gate.sh`, sha256 `a6307edf…`).
- Repair commit: round-35 landed lane commit `e87c5d7e` (`tools/research-gate.sh`
  sha256 `1f2fb4f5…`).
- Selftest: `PASS (256 cases, 0 skipped)` on both gates — the public path does
  not catch it, which is why the probe exists.
