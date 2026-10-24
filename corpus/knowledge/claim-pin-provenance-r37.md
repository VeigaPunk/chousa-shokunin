# Claim-pin provenance — one pinned sha256sum, never PATH

Lane: chousa. Round 37 (C1, operability — lowest scored axis 3/10).
Surface: `tools/research-gate.sh` (the `verify-claims` revision pin),
`corpus/evidence/round37/c1-count.py`.

source: S070 (coreutils `sha256sum(1)`, digest text and `--check` input, opened
2026-10-23 — `/usr/share/man/man1/sha256sum.1.gz`, decompressed lines 4–11 and
19–20, quote at line 11, file SHA-256 `93c17dff…403f`; the pinned binary's
documented contract); the lane gate
`tools/research-gate.sh` (landed `9fcac047…cf39`); frozen design
`corpus/evidence/round37/claims.md`; receipts
`corpus/evidence/round37/receipts/c1-{base-s37001,after-s37001,after-s37901,after-s37921,after-s37701}.json`;
wave seat reports `.ufo/waves/round-37/w1/ExecC1{Base,Landed}Rederive.md`,
`ExecMutC1Counter.md`, `ExecMutGateC1.md`; control gate
`.ufo/waves/round-37/controls/base-gate-r37.sh` (`a7d3922c…f54e8`).
verified-at: 2026-10-23 (landed gate SHA-256 `9fcac047…cf39`;
`CLAIM_PIN_PROVENANCE_MATCH=7/7` on seeds 37001, 37111, 37133, 37701, 37901, 37921)
recheck: on-release (`python3 corpus/evidence/round37/c1-count.py --gate tools/research-gate.sh --seed <n>` → `7/7` with `predicate_holds=true`; any run below 7/7 against the landed gate kills the claim)

## What changed

The claim-body revision pin at `research-gate.sh:2002` resolved
`sha256sum < file | cut -d' ' -f1` through the caller's `PATH`: a shim named
`sha256sum` or `cut` listed first could forge a match on a tampered source or
manufacture a stale verdict on an intact one. The fix binds ONE pinned
absolute `/usr/bin/sha256sum` (with the S070 64-lowercase-hex contract), so
the digest channel no longer traverses the caller's PATH.

## The seven scenarios (counter `c1-count.py`)

`hold-stale` / `hold-match` pin the verdict-bearing cells; `sha-shim-forge` /
`cut-shim-forge` place a forge shim first on PATH (must still DRIFT/stale on
the tampered source); `sha-shim-other` / `sha-shim-broken` / `cut-shim-broken`
place wrong-digest or broken shims (an intact source must still read
CLEAN/supported — the gate may honour PATH for other tools, it must not need
it for the pin). Base gate `a7d3922c…` scores 2/7; landed gate `9fcac047…`
scores 7/7 on every committed receipt.

## Named limits (from claims.md §Limits, frozen)

- This is PATH-independence, not tamper-proof hashing: a caller who can
  replace `/usr/bin/sha256sum` itself (root, mount namespace) still controls
  the digest.
- The shim cells assert the VERDICT under a hostile PATH; the claim does not
  say the gate ignores PATH for every other tool.
- The counter's expectation is part of the claim surface (QUALITY 52): the
  inherited pre-freeze counter encoded the wrong-digest shim on an intact
  source as DRIFT/stale — corrected pre-freeze as claims §Erratum 1.

## Separability

C1's hunk is the hash call at the claim pin; C2's hunk is the pin-capture
child environment. Each counter reads the other's surface not at all: C1's
fixtures carry no `BASH_ENV` vector, C2's fixtures carry no `sha256` pin.
Demonstrated by the wave's single-hunk gate mutants
(`.ufo/waves/round-37/w1/ExecMutGateC1.md`, `ExecMutGateC2.md`).
