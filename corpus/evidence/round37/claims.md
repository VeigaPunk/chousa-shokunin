# Round 37 — frozen claim design (v1)

Lane: chousa (deep-research method). Round: 37. Attempt: 1 (after three dead
orchestrator attempts; inherited uncommitted work is named in §Inherited state).
Frozen before the wave's independent runs; the L1's construction runs on seeds
37001 (C1) and 37021 (C2) preceded this freeze and are disclosed as such (the
waves and the closure re-derive on fresh seeds). Nothing in this file changes
after the first wave receipt: a later change is an erratum appended below, never
an edit.

Base lane tip at freeze: `bb13ee9d3d4a4c8e3b562feaabd9de6138712e2d`.
Base gate `tools/research-gate.sh` sha256:
`a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`
(the round-36 final gate, unchanged at the base tip; committed byte-exact as
`.ufo/waves/round-37/controls/base-gate-r37.sh`). Candidate gate at freeze:
`9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39`.

Routed work this round: SCORECARD `Planned — round 37` candidates 1 and 2 (the
claim-body `sha256` pin resolving `sha256sum | cut` through `PATH`, and the
`BASH_ENV` re-export hole in the `--pin` capture — round-36 claims §Erratum 7),
plus the inherited attempt-1 gate edits.

## C1 — operability (lowest scored axis: operability 3/10)

**Claim.** A claim's `sha256` revision pin is hashed through one pinned absolute
`sha256sum` and never through the caller's `PATH` (`sha256sum` or `cut`), so no
PATH shim can move a pin verdict in either direction: forge a match on a
tampered source, or turn an intact source stale.

Surface: the `verify-claims` revision pin in `tools/research-gate.sh`, measured
by `corpus/evidence/round37/c1-count.py`.

**P1 (frozen predicate).** C1 is met iff

```
python3 corpus/evidence/round37/c1-count.py --gate tools/research-gate.sh --seed N --receipt F
```

prints `CLAIM_PIN_PROVENANCE_MATCH=7/7` with `predicate_holds=true` on each of
two fresh seeds against the landed lane revision, and no committed run of the
same counter against the landed gate prints a lower count.
Code condition: `matched == 7`; receipt labels `matched`, `predicate_holds`.

**Kill rule.** Any run against the landed gate below 7/7 kills C1; a run whose
receipt `gate_sha256` differs from the landed gate's is not the claim's
measurement; a scenario that passes by weakening its fixture (e.g. a shim the
gate is expected to honour) is not a measurement.

**Before (measured).** Base gate `a7d3922c…`: `CLAIM_PIN_PROVENANCE_MATCH=2/7`
(`corpus/evidence/round37/receipts/c1-base-s37001.json`; re-derived by the wave).
The five failing cells are the shim cells: a forge shim made a tampered source
read `supported`, and a wrong-digest or broken shim made an intact source read
`stale`.

**Cheapest control that skips the claimed work (committed).** The base gate is
the control: it is the exact bytes at the base tip, it runs the same seven
scenarios, and it scores 2/7. A do-nothing lane commit therefore cannot reach
7/7. Receipt: `receipts/c1-base-s37001.json`.

## C2 — freshness (pin/drift re-derivation independence)

**Claim.** A `--pin` baseline is independent of the caller's `BASH_ENV`: a
startup file that re-exports a scrubbed variable (`CHOUSA_GREP_PIN_ECHO`,
`CHOUSA_STRICT`) or moves `CHOUSA_ROOT` cannot change the pinned capture, embed
a receipt line in the baseline, or make a later plain `--drift` report a phantom
drift on an unchanged gate.

Surface: the canonical pin capture in `tools/research-gate.sh`
(`gate_canonical_capture`) and the `--pin`/`--drift` contract, measured by
`corpus/evidence/round37/c2-count.py`.

**P2 (frozen predicate).** C2 is met iff

```
python3 corpus/evidence/round37/c2-count.py --gate tools/research-gate.sh --seed N --receipt F
```

prints `PIN_CAPTURE_ENV_MATCH=7/7` with `predicate_holds=true` on each of two
fresh seeds against the landed lane revision, and no committed run against the
landed gate prints a lower count. Code condition: `matched == 7`.

**Kill rule.** Any run against the landed gate below 7/7 kills C2; a scenario
whose expectation is the vulnerable behaviour (a baseline that embeds the echo,
a drift that reports `-GATE_GREP`) is not a measurement; a run whose receipt
`gate_sha256` differs from the landed gate's is not the claim's measurement.

**Before (measured).** Base gate `a7d3922c…`: `PIN_CAPTURE_ENV_MATCH=3/7` on
seed 37021 (`corpus/evidence/round37/receipts/c2-base-s37021.json`). Three holds
pass; the four separation cells fail: `env-echo-pin` pins a baseline containing
one `GATE_GREP:` line and the plain drift then reports `GATE_DRIFT: -GATE_GREP`;
`env-echo-drift` reports `+GATE_GREP`; `env-fn-echo-pin` repeats the pin case
through an exported shell function; `env-root-pin` pins a different capture and
the drift reports a token list instead of `none`.

**Cheapest control that skips the claimed work (committed).** The base gate,
same seven scenarios, 3/7. Receipt: `receipts/c2-base-s37021.json`.

## Separability

C1 changes the claim-body hash call; C2 changes the pin-capture child
environment. Each has its own counter, its own fixtures and its own gate line
region; either gate hunk alone moves its own counter and not the other's:
C1's counter reads no `GATE_DRIFT` line (it asserts claim verdicts), C2's
counter reads no claim pin (its fixtures carry no `sha256` field). Landing both
in one round is a scheduling choice, not a dependency.

## Limits (named)

- C1 does not prove the pinned binary is honest: a caller who can replace
  `/usr/bin/sha256sum` (root, mount namespace) still controls the digest; the
  claim is PATH-independence, not tamper-proof hashing.
- C1's `sha-shim-other`/`sha-shim-broken` cells assert the *verdict* under a
  hostile PATH; a gate that ignores PATH entirely for other tools is not claimed.
- C2 covers `BASH_ENV` only. The gate process itself already sourced the
  caller's `BASH_ENV` before its body ran, so a startup file can still define
  functions in the gate process; `--posix`/`ENV`, `SHELLOPTS`/`BASHOPTS` and a
  hostile `TMPDIR` are not covered and stay named debt.
- C2 asserts file contents and the drift verdict, not that the capture's
  subprocess environment is byte-identical to a clean one.
- Both counters run loopback-only, write only under their temp dir and an
  optional receipt path, and never fetch.

## Errata (appended; the body above is frozen)

**Erratum 1 (pre-freeze, inherited counter).** The inherited attempt-1
`c1-count.py` expected the wrong-digest shim on an *intact* source to produce
`DRIFT/stale` on the landed gate — i.e. it encoded the vulnerability as the
target, so the fixed gate scored 6/7 and could never satisfy its own counter.
Corrected to `CLEAN/supported` before any receipt was published; the pre-freeze
pair (base 2/7, candidate 7/7) is what appears above. A counter's expectation is
part of the claim's surface (QUALITY 52 class: the assertion must match what the
name claims).

**Erratum 2 (pre-freeze, inherited selftest case).** The inherited gate edits
left `RESEARCH_GATE_SELFTEST: FAIL (1/264 cases)`: case `r2-hash-fault-shim`
injected an unmeasurable-hash fault through a PATH `sha256sum` shim, which the
C1 fix makes impossible by design. Re-based on a user+mount namespace that binds
a failing stub over `/usr/bin/sha256sum` (the r14 ns harness), renamed
`r2-hash-fault-pinned` to match its mechanism, and skipped BY NAME with the skip
counted when no userns exists.

**Erratum 3 (pre-freeze, inherited freeze).** Attempt 1's gate edits (pinned
`sha256sum` for claim pins, `sha256_hex_stream`) are inherited and re-verified
here: they are C1's landed fix. The BASH_ENV scrub and the three selftest cases
265-267 are C2's landed fix.
