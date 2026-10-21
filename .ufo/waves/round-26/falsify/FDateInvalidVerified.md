# FDateInvalidVerified — C2 calendar-invalid `verified-at:` + cadence (round 26 attempt 1, falsify)

Seat `ChousaR26R.FDateInvalidVerified` (UFO-FSD scout, leaf). Author-lane advice
only; no outside judge/SHONEN claim. Judged on: freshness (C2).

## Target identity

- Measured revision: `0e9784bd52eca456b24d0bc40921480a47f91a2b` (from
  `corpus/evidence/round26-measured-revision.json`; `git cat-file -t` = `commit`;
  lane `HEAD` observed equal at run time). Claim base `ba3333254dd337658a4f25e7a9471f9cf4e4567e`.
- Sandbox: `git archive 0e9784bd… | tar -x -C /tmp/chousa-r26-falsify-FDateInvalidVerified/tree` (rc 0).
- Byte identity in sandbox (`sha256sum`): `tools/research-gate.sh`
  `c2c813f1…3abc6`, `corpus/QUALITY.md` `2428baaf…327dce6`,
  `corpus/evidence/round26-claims.md` `dcbe2b5f…f1c` — all equal the revision
  json `inputs[]` values.
- Base gate for plain-output comparison: `git show ba333325…:tools/research-gate.sh`
  → `/tmp/chousa-r26-falsify-FDateInvalidVerified/base-gate.sh`.
- Tools installed/updated: none. Python 3.14.8 (host), GNU bash (host).

## Spec under attack (claims file, C2 + 2026-10-21 correction)

"V = the leading `YYYY-MM-DD` of `verified-at:` when calendar-valid, else none …
`<N>d` without V … → `due=unknown freshness=unknown`." `--as-of`: "an absent or
calendar-invalid value exits 2."

Code path (observed): `tools/research-gate.sh:2741-2750` — V captured by
`^[[:space:]]*([0-9]{4}-[0-9]{2}-[0-9]{2})` under `local LC_ALL=C` (`:2539`),
then guarded twice: call-site `metadata_iso_date "$verified_first"` (`:2747`) and
again inside `metadata_add_days` (`:2345`). `metadata_iso_date` (`:2295-2308`) is
byte-identical to the base function (diff of extracted bodies: identical).

## Verdict

**C2's calendar-invalid-V rule was not falsified** in 42 independent cases.
There is one low-severity deviation from the letter of the option contract
(duplicate `--as-of`, below), and one defect in the frozen oracles outside the
frozen population (side finding).

## Run 1 — independent differential (exit 0)

Command: `python3 /tmp/chousa-r26-falsify-FDateInvalidVerified/harness.py` → exit 0.
The oracle is written from spec v1 independently of the gate and of both frozen
oracles. It uses `datetime.date(y, m, d)` construction (not `fromisoformat`),
ASCII-only `[0-9]`, ASCII whitespace, and `timedelta` for cadence. Each fixture
is a separate CLI run: `env -i PATH HOME CHOUSA_STRICT=0 LANG=C.UTF-8 bash GATE
verify-metadata FILE --root fx --as-of A`. A case agrees only when due and
freshness match, the overdue finding is present iff `freshness=overdue`, rc is
0 or 1, there is exactly one `RESEARCH_GATE:` line, and stderr is empty. Each
fixture was also run without `--as-of` through both the base gate and the
target gate, and the outputs compared after dropping the timestamp line.

Result: `C2_INVALID_V_AGREE=42/42`, `PLAIN_BYTE_IDENTICAL=42/42`.

The 31 calendar-invalid-V or invalid-V-adjacent cases, all with as-of
`2026-10-21` unless noted, gave `due=unknown freshness=unknown verdict=clean
rc=0` and no finding:
`2026-02-30`+`1d`; non-leap `2026-02-29`; century `1900-02-29` and `2100-02-29`;
`04-31`, `06-31`, `09-31` (octal-trap month `09`), `11-31`; month `13`/`00`;
day `00`/`32`; year `0000-01-01`; `0000-00-00`+`0d`; `9999-99-99`+`0d`;
`2026-02-30` with `0d`, `0000d`, and a 23-digit cadence; date-only (no text);
trailing digit `2026-02-301` (leading capture `2026-02-30`); `T00:00Z` suffix;
tab-led; no space after the colon; date on a continuation line; CRLF file;
as-of `0001-01-01` and `9999-12-31`; cadence followed by a command.

Invalid V does not block the non-cadence arms: an invalid V with
`recheck: 2026-12-01` gives `due=2026-12-01 current`; with `2026-03-01` it gives
`overdue` plus `META_RECHECK_OVERDUE`, rc 1; with `on-release` it gives `event`.

The 11 valid neighbours compute dates matching `datetime`: `2026-02-28`+1d →
`2026-03-01`; `2000-02-29`+1d → `2000-03-01`; `2028-02-29`+1d → `2028-03-01`;
`2024-02-29`+365d → `2025-02-28`; `04-30`+1d → `05-01`; `09-30`+30d →
`2026-10-30`; `08-09`+30d → `2026-09-08`; `0001-01-01`+30d → `0001-01-31`;
trailing digit `2026-01-011` → V `2026-01-01`; continuation-line and CRLF
valid V.

Note: `verified_at=dated` is reported for every calendar-invalid V, and the
legacy screen is shape-only. This is unchanged from the base (plain output is
byte-identical), so it is not a C2 regression.

## Run 2 — isolated mutation controls (QUALITY 17)

Mutants are copies in `/tmp/…/mut/`; the harness is re-pointed with `sed` on the
`GATE =` line.

| mutant | change | harness exit | agree |
|---|---|---|---|
| m1-callsite | drop `metadata_iso_date "$verified_first" &&` (`:2747`) | 0 | 42/42 |
| m2-adddays | drop `metadata_iso_date "$date" \|\| return 1` (`:2345`) | 0 | 42/42 |
| m3-both | drop both | **1** | **16/42** |

m3 is killed for the targeted reason. The civil algorithm normalizes invalid
dates instead of rejecting them: `2026-02-30`+1d → `2026-03-03 overdue`,
`2100-02-29`+30d → `2100-03-31 current`, `2026-13-01`+30d → `2027-01-31`,
`0000-01-01` → `0000-01-31`. One case (`0000-00-00`+`0d`) crashed with the raw
stderr ``line 2340: 10#: invalid integer constant (error token is "10#")``,
which is mutant-only. In the production target the guards are redundant: each
single-guard removal is an equivalent mutant, so no test can kill either alone.
This is defence in depth, not a defect. The frozen selftest case
`metadata-asof-invalid-verified-date` and the date-differential
`invalid-verified-at` row also kill only the both-removed state
[INFERENCE: from the code path; neither was executed by this seat].

## Run 3 — option case `--as-of` (CLI, exits observed)

- Calendar-invalid or off-shape single values all exit 2 with
  `research-gate: --as-of must be a valid YYYY-MM-DD date` and no verdict line:
  `2026-02-29`, `1900-02-29`, `2100-02-29`, `0000-01-01`, `2026-13-01`,
  `2026-04-31`, `2026-00-01`, `2026-01-00`, leading or trailing space, a
  trailing newline, `2026-1-01`, `+2026-01-01`, Arabic-Indic digits, and `''`.
- Valid extremes run normally: `2000-02-29` and `0001-01-01` (rc 0),
  `9999-12-31` (rc 1, overdue).
- A missing value followed by another flag (`--as-of --root fx`) exits 2, but
  the message is `multiple record paths`, not `--as-of needs YYYY-MM-DD`. The
  exit code meets the spec; the message is misleading.
- **Deviation (low):** a repeated `--as-of` is last-wins. Validation runs once
  after parsing (`:6281-6283`, `:6295-6297`):
  - `--as-of 2026-02-30 --as-of 2026-10-21` gives rc 1 and a normal run;
  - `--as-of 2026-13-01 --as-of 2026-01-01` gives rc 0;
  - the reverse order exits 2.

  A supplied calendar-invalid value therefore does not always exit 2, contrary
  to the spec's literal wording. This matches the pre-existing last-wins
  convention for `--root` and `--registry`: the base gate with
  `--root /nonexistent --root fx` gives rc 0, CLEAN. No frozen control covers
  repeated flags.

## Run 4 — composition with `--registry` (both flag orders)

Registry `fx/registry.md`: `| S001 | mined | comp/reg-invalid.md, comp/reg-invalid-bare.md |`.

- `verified-at: 2026-02-30 checked fixture`, `30d`: `due=unknown
  freshness=unknown verdict=clean`, rc 0, identical in both flag orders.
- `verified-at: 2026-02-30` (bare date): `due=unknown freshness=unknown
  verdict=drift` plus `FINDING META_VERIFIED_AT_BARE`, rc 1, in both orders.
  Both screens are kept and the verdict is the union, as the composition
  clarification requires.

## Side findings (outside the targeted shape; recorded, not graded)

1. **Frozen oracle expressions are Unicode-permissive; the gate is ASCII.**
   Both `round26-measure.sh` (`:129`) and `round26-date-differential.sh`
   (`:57`) use `re.match(r'^\s*(\d{4}-\d{2}-\d{2})', …)` on `str`. With a
   non-ASCII whitespace byte before a valid date, the expression yields V =
   `2026-01-02` and due `2026-04-02`, but the gate reports
   `verified_at=undated due=unknown` (rc 1). Observed for NBSP (`\u00a0`) and
   `\x1c`. Adjudicated against the spec: the gate is consistent with its own
   legacy `undated` classification, so the defect is in the oracle (over-wide
   `\s`), not the gate. These bytes are not in the frozen 29
   [INFERENCE: not scanned by this seat], so `C2_ORACLE_AGREE` would not change.
   Arabic-Indic and fullwidth digits agree (both say unknown) only because
   Python 3.14 `fromisoformat` rejects them; `\d` alone accepts them. Peer
   `ChousaR26.RevPreregC2-3` is on NBSP bytes.
2. **Duplicate `verified-at:` keys are last-wins.** In both the gate and the
   probe oracle, a valid date followed by an invalid one gives `due=unknown
   verdict=clean`; the reverse order gives `due=2026-04-02 overdue`. The spec
   does not define this. Not a C2 violation.
3. **`freshness=unknown` carries no finding.** A corrupt V and a command-only
   recheck look the same in output, with no finding. This is spec-compliant
   ("anything else → unknown"); recorded for calibration only.

## Not run (explicitly)

The full selftest, build, lint, and formatter; `round26-measure.sh`
(any mode); `round26-date-differential.sh`; the 8 MiB probe. None are claimed.

## Reproduce

All artifacts are in `/tmp/chousa-r26-falsify-FDateInvalidVerified/`:

- `harness.py` and `harness.out`;
- `mut/m{1-callsite,2-adddays,3-both}.{sh,out}`;
- fixtures under `fx/{c2,comp,side}/` and `fx/registry.md`.
