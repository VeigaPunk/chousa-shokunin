# The engine-swap canary — fourteen pin/contract scenarios, four new separations

Lane: chousa. Round 36 (C1, operability). Surface: `tools/research-gate.sh` and
`corpus/evidence/round36/c1-count.py`.

source: S070 (coreutils `sha256sum(1)`, digest text and `--check` input, opened 2026-10-23);
the lane gate `tools/research-gate.sh` and the frozen counter `corpus/evidence/round36/c1-count.py`;
frozen design `corpus/evidence/round36/claims.md`; receipts
`.ufo/waves/round-36/measure/c1-{before-s36001,after-s36001,after-s36011}.json`,
`.ufo/waves/round-36/measure-l1/c1-s36361.json`, `.ufo/waves/round-36/w1/*/c1-*.json` (wave seats);
control gate `.ufo/waves/round-36/controls/base-gate-r36.sh` (`a4768851…c38ad`).
verified-at: 2026-10-23 (round 36; landed gate SHA-256 `a7d3922c…f54e8`;
`ENGINE_SWAP_CANARY=14/14` on seeds 36001, 36011, 36361)
recheck: on-release (`python3 corpus/evidence/round36/c1-count.py --seed <n>` → `14/14` with
`predicate_holds=true`; any run below 14/14 against the landed gate kills the claim)

## What the counter separates

One scenario per demonstrated swap class; each scores PASS only when the gate's
behaviour (not just its text) matches the reference and the tripwire is
accounted for. The `before` column is the round-35 final gate `a4768851…`,
measured on seed 36001 (`.ufo/waves/round-36/measure/c1-before-s36001.json`).

| # | Scenario | What it proves | before |
|---|---|---|---|
| S1 | `shim-first-path` | a `grep` script listed first on `PATH` is not executed (0 tripwire bytes) | PASS |
| S2 | `bash-env-function` | a `grep()` function planted through `BASH_ENV` is not executed | PASS |
| S3 | `no-grep-on-path` | the gate runs with no `grep` on `PATH` (38 path tools) | PASS |
| S4 | `override-relative` | a relative `RESEARCH_GATE_GREP` is refused (exit 2, `GREP_PROVENANCE`) | PASS |
| S5 | `override-missing` | a missing override path is refused (exit 2 + `GREP_PROVENANCE`); the before-read ordering is a code reading, not an open-count receipt (QUALITY 48) | PASS |
| S6 | `override-non-gnu` | an override that does not report GNU grep is refused; the stub sees exactly one call (`--version`) | PASS |
| S7 | `override-distinct-path` | a distinct-path GNU-reporting recorder is honoured, named in the echo, and observed receiving the matcher calls (4) | PASS |
| S8 | `default-echo` | the default pin names itself with a LIVE `--version` (`/usr/bin/grep`, GNU grep 3.12-modified) | PASS |
| S9 | `override-beats-shim` | the override wins over an imported shim; 0 tripwire bytes | PASS |
| S10 | `semantic-canary` | per-record argv attribution is measured on the landed gate and a keyed engine (K1) is attributed only for its direct short record | PASS |
| S11 | `manifest-hash-shim` | a hostile `sha256sum` on `PATH` cannot poison `record_sha256`/`gate_sha256` (64-lowercase-hex, true hashes present) | **FAIL** |
| S12 | `locale-c` | `\u00e9` decodes to `é` under `LC_ALL=C` as it does in UTF-8 | **FAIL** |
| S13 | `pin-echo-isolation` | a baseline pinned with `CHOUSA_GREP_PIN_ECHO=1` carries no `GATE_GREP:` line; `--drift` reports `GATE_DRIFT: none` | **FAIL** |
| S14 | `pin-drift-token` | an injected `GATE_GREP:` line pairs as `-GATE_GREP`, not `-LINE` | **FAIL** |

The four failures are the round-35 routed defects (spot-check 3, 4, 7 and
erratum 15). S11 rests on S070's text: `sha256sum` prints or checks SHA256
(256-bit) checksums, so a digest field is 64 lowercase hex characters, and a
value outside that shape is not a checksum at all — the gate now hashes with
one absolute binary (`/usr/bin/sha256sum` → `/bin/sha256sum`) and refuses the
manifest (exit 2) instead of stamping a poison value.

## Reading rule

The counter proves what each scenario asserts, one at a time. It does **not**
prove that the engine is genuine: S10's attribution proves the pinned matcher
was *queried* for each record, not that its answer was used (a call-for-show
engine queries and discards), and a gate that reads the recorder script can
forge log lines (active anti-instrumentation is out of scope). The stated
limits in `claims.md` §Limits are part of this entry.

## What this entry does not claim

No engine-identity guarantee beyond the fourteen scenarios; no claim that a
gate passing 14/14 is correct; the count does not weigh scenarios (each is one
PASS).
