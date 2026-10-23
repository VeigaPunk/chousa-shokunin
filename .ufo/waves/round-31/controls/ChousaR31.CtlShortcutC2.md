# Round 31 — control seat `ChousaR31.CtlShortcutC2` (C2 counter)

Counter: `corpus/evidence/round31/c2-count.py` (frozen; counter_sha256 in each receipt).
Base gate `tools/research-gate.sh` baseline (no sha256 handling): `REVISION_BINDING_MATCH=50/120`.
All runs from lane root, wrapped in `timeout 900`; seeds 9001/9002/9003 (fresh).
No tool installs performed (system python3; no pacman/uv/npm actions). No network. No git writes.

## Results (13 controls × 3 seeds)

| Control (script) | Mechanism | Seed 9001 | 9002 | 9003 | Receipt (controls/ChousaR31.CtlShortcutC2/) |
|---|---|---|---|---|---|---|
| M1 `ctl-uppercase.sh` | accept uppercase hex (lowercase before validate/compare) | 115 | **118** | 117 | uppercase-seed900{1,2,3}.json |
| M2 `ctl-crlf-norm.sh` | normalize CRLF→LF before hashing | 115 | 113 | 110 | crlf-norm-seed900{1,2,3}.json |
| M3 `ctl-cat-hash.sh` | hash file as `$(cat)` sees it (trailing LFs stripped) | 83 | 80 | 81 | cat-hash-seed900{1,2,3}.json |
| M4 `ctl-span-hash.sh` | hash only the span text | 76 | 76 | 76 | span-hash-seed900{1,2,3}.json |
| M5 `ctl-membership.sh` | stale iff sha not in set of ALL fixture-file hashes | 112 | 112 | 112 | membership-seed900{1,2,3}.json |
| M6 `ctl-format-only.sh` | validate format only; never hash; format-ok → span verdict | 64 | 64 | 64 | format-only-seed900{1,2,3}.json |
| M7 `ctl-skip-span.sh` | exact hash compare, span check skipped (match → supported) | 110 | 110 | 110 | skip-span-seed900{1,2,3}.json |
| O1 `ctl-relaxed-norm.sh` | CRLF→LF **and** strip all trailing newlines before hashing | 83 | 80 | 81 | relaxed-norm-seed900{1,2,3}.json |
| O2 `ctl-crlf-prior.sh` | if file has CRLF (25% share) guess stale, else span verdict | 74 | 73 | 64 | crlf-prior-seed900{1,2,3}.json |
| O3 `ctl-majority-stale.sh` | any valid-format sha → stale (no source read) | 86 | 86 | 86 | majority-stale-seed900{1,2,3}.json |
| O4 `ctl-newline-tolerant.sh` | accept hash of exact bytes, or ± one trailing newline | 114 | 110 | 113 | newline-tolerant-seed900{1,2,3}.json |
| O5 `ctl-trim-spaced.sh` | trim whitespace around sha before validation (common arg-parsing bug) | 117 | **120** | 118 | trim-spaced-seed900{1,2,3}.json |
| O6 `ctl-strip-prefix.sh` | strip a `sha256:` prefix before validation | 117 | 117 | 116 | strip-prefix-seed900{1,2,3}.json |

## Findings (exact leak)

The C2 fixture's invalid class `I1_invalid_sha_value` has only 14 claims, each given one of
six malformed sub-kinds picked by `rng.choice(["upper","short","long","prefixed","nonhex",
"spaced","upper","prefixed"])` → `upper` and `prefixed` at p=¼, the other four at p=⅛ per claim.
Every other class (R/S/N) is pinned by exact-byte hashing, so any gate substitute that is
byte-perfect except a **single format tolerance** scores `120 − k` where `k ~ Binomial(14, p)`
is the number of that sub-kind drawn in the run.

- **O5 trim-spaced reached exactly 120/120 on seed 9002** (`predicate_holds=true` in the
  receipt, `I1 14/14`, zero misses): that seed drew no `spaced` claim (P ≈ (7/8)^14 ≈ 15%),
  so a whitespace-trimming validator is behaviorally identical to the strict oracle. A control
  that accepts one malformed sub-kind passes the counter outright on ~15% of fresh seeds.
- **M1 uppercase reached 115/118/117** (≥115 on all three seeds): loses only the p=¼
  `upper` members of I1. O6 strip-prefix 116–117 likewise; M2 crlf-norm 110–115.
- The generic lazy ceiling is lower: membership-only 112 (must read the own file to separate
  S5's "hash of another fixture file" from R1/R2's own-hash), skip-span 110, newline-tolerant
  110–114. No control that skips reading/hashing the claim's source approaches 120; every
  ≥115 control does the full byte-accurate hashing **and only relaxes format validation**.

Conclusion: the counter distinguishes correct from lazy hashing (good), but its invalid class
is too thinly atomized to pin format strictness — one-tolerance parsers score 116–120, and one
reached 120/120.

## Verdict

**design broken: the C2 counter's I1 invalid class (14 claims split across six rare sub-kinds)
lets a gate that tolerates any single malformed sha form score 116–120, and a whitespace-
trimming validator scored exactly 120/120 (predicate_holds=true) on seed 9002.**

## v2 re-score

Re-ran every v1 control with one `CLAIM_SOURCE_REVISION_MISMATCH severity=warn surface=claims obs=id=<id>` finding for each claim the control labels `stale`, and no such finding for other verdicts. Three seeds each; all 39 receipts have schema `v2` and counter hash `1064fdb356e25440c64bb4d4d5363acb9c1bbc32c687c8ea50096d74c849d500`.

| Control | Seed 9001 | Seed 9002 | Seed 9003 | Receipts (`controls/ChousaR31.CtlShortcutC2/v2/`) |
|---|---:|---:|---:|---|
| M1 uppercase | 117 | 117 | 117 | `uppercase-seed900{1,2,3}.json` |
| M2 CRLF→LF before hash | 110 | 110 | 110 | `crlf-norm-seed900{1,2,3}.json` |
| M3 `$(cat)` trailing-LF hash | 83 | 83 | 83 | `cat-hash-seed900{1,2,3}.json` |
| M4 span-only hash | 76 | 76 | 76 | `span-hash-seed900{1,2,3}.json` |
| M5 membership in fixture hashes | 112 | 112 | 112 | `membership-seed900{1,2,3}.json` |
| M6 format-only, skip hashing | 64 | 64 | 64 | `format-only-seed900{1,2,3}.json` |
| M7 exact hash, skip span | 110 | 110 | 110 | `skip-span-seed900{1,2,3}.json` |
| O1 CRLF normalize + strip final LF | 83 | 83 | 83 | `relaxed-norm-seed900{1,2,3}.json` |
| O2 CRLF-share prior | 70 | 70 | 70 | `crlf-prior-seed900{1,2,3}.json` |
| O3 valid sha → stale | 86 | 86 | 86 | `majority-stale-seed900{1,2,3}.json` |
| O4 accept ± one trailing newline | 113 | 113 | 113 | `newline-tolerant-seed900{1,2,3}.json` |
| O5 trim whitespace around sha | **118** | **118** | **118** | `trim-spaced-seed900{1,2,3}.json` |
| O6 strip `sha256:` prefix | 117 | 117 | 117 | `strip-prefix-seed900{1,2,3}.json` |

**v2 maximum: 118/120** (O5, all seeds). The fixed invalid-kind counts prevent v1's 120/120
miss, but whitespace tolerance still passes both fixed `spaced` cases and misses only those
two invalid claims. Uppercase and prefix tolerance each score 117 by passing their three fixed
invalid examples. No v2 control reached 120/120; the highest shortcut remains close and is
specifically attributable to accepting malformed sha forms.
