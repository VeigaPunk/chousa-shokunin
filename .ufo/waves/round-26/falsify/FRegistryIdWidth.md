# FRegistryIdWidth — C3 id-width relation/grammar falsification (round 26 attempt 1)

Seat: `ChousaR26R.FRegistryIdWidth` (author-lane advice only; not an outside judge).
Axis judged: calibration. Target: C3 `verify-metadata --registry`, the S-id grammar
(`S` + 3 or more digits, standalone ASCII alnum/underscore boundaries, per the spec-v1
correction in `corpus/evidence/round26-claims.md:134-141` and `../CORPUS.md:89`).

## Revision under test

- Immutable target: `0e9784bd52eca456b24d0bc40921480a47f91a2b`, from
  `corpus/evidence/round26-measured-revision.json`. Lane HEAD observed at run time was the same
  commit (`git rev-parse HEAD`).
- Claim base: `ba3333254dd337658a4f25e7a9471f9cf4e4567e` (not re-run; no base comparison was needed).
- Sandbox: `/tmp/chousa-r26-falsify-FRegistryIdWidth/tree`, produced by
  `git archive 0e9784bd… | tar -x` (exit 0).
- Verified sha256 values in the sandbox, all matching the measured-revision file:
  - `tools/research-gate.sh` = `c2c813f1…abc6`
  - `corpus/SOURCES.md` = `8308e629…a5aa9`
  - `corpus/evidence/round26-registry-oracle.py` = `6b2d135c…1d78`
- Code under test: `metadata_registry_load` (row id `^S[0-9]{3,}$`, line 2433) and
  `metadata_registry_check_source` (scan `(^|[^[:alnum:]_])(S[0-9]{3,})([^[:alnum:]_]|$)`, lines 2472-2507).

## Verdict

The headline case is not falsified. `S0001` and `S12345` are valid ids and `S01` is not, as the
spec requires, and the gate agrees with the registered oracle on all 17 fixture entries at the
level of which finding ids each entry gets. I found two defects, both in the occurrence-scanning
loop rather than in the grammar:

- **F1 (calibration):** phantom duplicate findings. A non-token can be counted as an extra
  occurrence of a later real token, so the finding count is inflated. Verdict and exit code are
  unchanged.
- **F2 (operability, cross-axis):** the loop's prefix strip is quadratic in the length of
  `source:`. Plain mode is unaffected.

There is also one calibration observation that is consistent with the spec: malformed ids are
silently treated as "no S-id".

## Fixtures and results (all run in the sandbox, exit codes observed)

Registry `fx/reg.md` has columns `id | status | used-by` and these rows:

| Row id | Status | Used-by |
|---|---|---|
| `S0001` | mined | `w-s0001` |
| `S12345` | mined | `w-s12345` |
| `S01` | mined | `w-s01` |
| `S1` | mined | `w-s1` |
| `S001` | mined | `w-s001` |
| `S00001` | queued | — |
| `s002` | mined | `w-lower` |
| `` `S003` `` | mined | `w-tick` |
| `S004a` | mined | `w-suffix` |
| `S98765432109876543210` | mined | `w-huge` |

Each entry was `source: <value>` / `verified-at: 2026-10-20 checked claim` / `recheck: 90d`.

Command, once per entry:
`bash tree/tools/research-gate.sh verify-metadata fx/corpus/knowledge/<e>.md --root fx --registry fx/reg.md </dev/null`

| entry (`source:` value) | gate findings | exit | spec-expected |
|---|---|---|---|
| w-s0001 (`S0001 https://…`) | none, CLEAN | 0 | yes |
| w-s12345 (`S12345`) | none, CLEAN | 0 | yes |
| w-s001 (`S001`) | none, CLEAN | 0 | yes |
| w-huge (`S98765432109876543210`) | none, CLEAN | 0 | yes |
| w-s01 (`S01`; registry has a mined `S01` row) | `META_SOURCE_NO_ROW_ID` info, CLEAN | 0 | yes (row ignored, token not an id) |
| w-s1 (`S1`) | `META_SOURCE_NO_ROW_ID` info | 0 | yes |
| w-suffix (`S004a`) | `META_SOURCE_NO_ROW_ID` info | 0 | yes |
| w-lower (`s002`) | `META_SOURCE_NO_ROW_ID` info | 0 | yes |
| w-nonascii-digit (`S１２３４５`, fullwidth) | `META_SOURCE_NO_ROW_ID` info | 0 | yes (ASCII digits only) |
| w-tick (`` `S003` ``; row cell is `` `S003` ``) | `META_SOURCE_ROW_MISSING` S003 | 1 | yes (backticked row id is not an id; source backtick is a boundary) |
| w-s001-vs-s0001 (`S00001`) | `META_SOURCE_NOT_MINED` S00001 | 1 | yes (exact-string id, no zero-folding) |
| w-zero-alias (`S01 S0001`) | `META_SOURCE_USEDBY_MISSING` S0001 only | 1 | yes (S01 skipped) |
| w-mixed-s01-s12345 (`S01, S12345;S0001`) | USEDBY_MISSING S12345, then S0001 | 1 | yes |
| w-boundary-hyphen (`S0001-S12345`) | USEDBY_MISSING S0001, then S12345 | 1 | yes |
| w-paren (`(S12345)`) | USEDBY_MISSING S12345 | 1 | yes |
| w-repeat (`S77777 S77777`) | `META_SOURCE_ROW_MISSING` S77777 ×2 | 1 | per occurrence (2 real tokens) |
| **w-phantom (`a S77777x S77777`)** | **`META_SOURCE_ROW_MISSING` S77777 ×2** | 1 | **1 real token: F1** |

Oracle: `python3 tree/corpus/evidence/round26-registry-oracle.py fx/corpus/knowledge --root fx --registry fx/reg.md`
exited 0, and its per-entry finding sets equal the gate's sets for all 17 entries
(17/17 set agreement). The oracle deduplicates ids with a set, so it cannot see F1.

## F1 — phantom duplicate findings (calibration, confidence: high, observed)

Mechanism (`tools/research-gate.sh:2477-2503`): after each match, the loop executes
`source_scan=${source_scan#*"$source_match"}`. That strips up to the **first textual
occurrence** of the matched text, not up to the match position. When the match ends at
end-of-string (an empty right boundary), the same text can appear earlier inside a
non-token. In `a S77777x S77777`, the leftmost real match is ` S77777` at the end. The strip
stops at the ` S77777` inside ` S77777x`, so the trailing real token is matched and reported
a second time.

Amplification, all exit 1. Fixture shape: `source: a` + N×` S77777x` + ` S77777`, using a
one-row registry `S0001`.

| N | bytes | findings | expected occurrences | seconds |
|---|---|---|---|---|
| 250 | 2062 | 251 | 1 | — |
| 2000 | 16062 | 2001 | 1 | 0.19 |
| 16000 | 128062 | 16001 | 1 | 8.46 |

The final line for N=16000 was `RESEARCH_GATE: DRIFT (entries=1 complete=1 findings=16001 drift=16001)`.

Controls:

- `q.md` puts the phantoms before a different real id (`… S77777x… S0001`): 1 finding, oracle
  `["META_SOURCE_USEDBY_MISSING"]`. The phantom only triggers when the earlier text is the same.
- `c.md` uses `T77777x` non-ids: 1 finding.

Impact: no verdict or exit change, because a real token is always present, so the entry is
already drift. The spec says every matching token is yielded (`round26-claims.md:96-97`), and
`S77777x` is not a token. So `findings=` / `drift=` counts can be inflated without limit by
non-tokens. No registered check catches this:

- `round26-registry-differential.sh` compares **sets** of finding ids per entry.
- The selftest cases (`research-gate.sh:6138-6237`) check substrings.

Not observed in the frozen population: no short or phantom shapes appear in any `source:`
header (see Population below).

Remediation, inference only and not implemented: advance by the match position instead of
pattern-stripping. One way is to strip `${source_scan:0:pos+len}` computed from the
non-matching prefix. Another is to require the strip to consume exactly the match.

## F2 — quadratic `source:` scan in `--registry` mode (operability, cross-axis, confidence: high, observed)

Same file `c.md` (N=16000, 128062 bytes, a single real token at the end):

| run | exit | seconds |
|---|---|---|
| plain `verify-metadata` | 0 | 0.05 |
| `--registry` | 1 | 14.41 |

Isolation:

- The bare `[[ $x =~ <source_id_re> ]]` on the same string took 0.01 s.
- The bare `y=${x#*" S77777"}` took 0.56 s at N=4000, 2.23 s at N=8000, and 9.01 s at N=16000.
  Each doubling roughly quadruples the time, under GNU bash 5.3.20(1)-release.

So the `#*pattern` strip is the quadratic step. Timings for `--registry` runs: 0.24, 0.91, 3.61
and 14.24 s for 16, 32, 64 and 128 KB. The `source:` value can grow up to the 8 MiB reader cap
through continuation lines, so `--registry` is not practically bounded.

This is a new mode, so it is not a regression against the base, and the C1 counting shapes do
not exercise `--registry`. It is reported for the operability seats and L1, not graded here.
The 8 MiB probe was **not** run (forbidden); the largest input was 128 KB.

## Observation O1 — malformed ids are silent (calibration, spec-conformant)

`S01`, `S1`, `S004a` and `s002` in `source:`, and an `S01` row in the registry, all collapse
into `META_SOURCE_NO_ROW_ID` severity=info with a CLEAN verdict and exit 0. No finding
distinguishes "cites a contract-invalid id" from "cites no id", and invalid registry rows are
dropped with no signal.

This matches C3 spec v1 (`round26-claims.md:94-99`) and is therefore not a falsification.
It is a calibration blind spot worth naming if the corpus ever holds a typo'd id.

There is also a cross-mode inconsistency that predates this round [INFERENCE from reading, not
run]:

- `verify-integrity` registers **any** non-empty `id` cell (`research-gate.sh:2192-2193`).
- It classifies `^S[0-9][A-Za-z0-9_-]*$` tokens as `kind=source` (line 2148).
- So `S01` is resolved there but is a non-id under `--registry`.

## Population check

In the target tree, `corpus/SOURCES.md` id cells are all `S` + 3 digits (39 rows).

`corpus/knowledge/*.md` has 91 valid-shape tokens and 38 short `S1`–`S9` / `S2ORC` tokens.
The short tokens appear only in body tables after the header in 6 legacy entries, for example
`archived-export-intake.md:46`. No `source:` line has a short id: the search
`grep -nE '^source:.*\bS[0-9]{1,2}\b'` returned exit 1, meaning no match. So F1 and O1 have no
effect on `C3_POP_R24PLUS_CLEAN`.

## Commands and exits

- `git archive 0e9784bd… | tar -x -C …/tree`: exit 0. `sha256sum` matched.
- 17 per-entry gate runs: exits as in the fixture table (0 or 1). No exit 2.
- Oracle on `fx/corpus/knowledge`: exit 0.
- Amplification runs at N=250/500/1000/2000/4000/8000/16000 (kinds p, r, q, c): all exit 1 under
  `timeout 120`/`timeout 300`, none timed out.
- Plain versus registry on `c.md`: exits 0 and 1.
- The first scripted loop aborted after one file because the persistent shell still had
  `set -e`. That was a harness artifact, not a gate result. It was rerun with `set +e`.
- `bc` is not installed (`command not found`), so timing used `EPOCHREALTIME`.

Not run: selftest, full build/lint/format, `round26-measure.sh`, the registry differential, and
the 8 MiB probe. No production file was edited. Fixtures exist only under
`/tmp/chousa-r26-falsify-FRegistryIdWidth/`.

## Tool installs

None.
