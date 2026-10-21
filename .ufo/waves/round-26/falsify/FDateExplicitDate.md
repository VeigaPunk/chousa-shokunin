# FDateExplicitDate — round 26 attempt 1, C2 explicit-date / `--as-of` option attack

Seat `ChousaR26R.FDateExplicitDate` (author-lane advice only; no outside judge/SHONEN claim).
Target: C2 rule "R a calendar-valid ISO date → `due=R`" (verified-at ignored) and the
`--as-of` option domain ("an absent or calendar-invalid value exits 2"), `round26-claims.md`
lines 58–81 and the spec-v1 correction lines 143–149.

## Revisions observed

- Measured target: `0e9784bd52eca456b24d0bc40921480a47f91a2b` (from
  `corpus/evidence/round26-measured-revision.json`); lane `git rev-parse HEAD` printed the same id.
- Claim base: `ba3333254dd337658a4f25e7a9471f9cf4e4567e` (not re-run; the base has no `--as-of`).
- Sandbox: `git archive 0e9784bd… | tar -x -C /tmp/chousa-r26-falsify-FDateExplicitDate/tree` (exit 0).
  `sha256sum` in the sandbox matched the revision file: `tools/research-gate.sh` c2c813f1…abc6,
  `round26-date-differential.sh` bb8f7f44…f5e7, `knowledge/recheck-due-r26.md` a0995b78…d5e.
- Tools: Python 3.14.8, GNU bash 5.3.20. Nothing was installed or updated.

## Verdict

- **Explicit-date rule: not falsified.** All 74 of 74 CLI cases agree with an independent oracle
  that uses Python `datetime.date` and a strict ASCII `^[0-9]{4}-[0-9]{2}-[0-9]{2}$` regex. It
  deliberately avoids `date.fromisoformat`, which also accepts `20261021`.
- **`--as-of` option domain: falsified twice** (F1 and F2 below). Both contradict the registered
  spec sentence "an absent or calendar-invalid value exits 2". The help text's exit contract is
  `Exit: 0 CLEAN | 1 DRIFT | 2 setup/usage`. Neither defect is caught by the six frozen controls,
  the 29-entry frozen population, selftest cases `metadata-asof-*`, or `round26-date-differential.sh`
  (which has no locale or repeated-flag case; grep for `LC_ALL|LANG|locale|repeat|twice|last` finds none).

## Explicit-date differential (observed)

Command: `python3 /tmp/chousa-r26-falsify-FDateExplicitDate/harness.py`, run twice. The first run
used `LC_ALL=C`. The second used the host default (`LANG=en_US.UTF-8`, `LC_ALL` unset). Both ended
`TOTAL=74 FAIL=0`, exit 0. Raw per-case records are in `/tmp/chousa-r26-falsify-FDateExplicitDate/results.json`.
Each case is one `e.md` file in its own directory, run as
`bash tree/tools/research-gate.sh verify-metadata <dir>/e.md --root <dir> --as-of <A>`.
A case passes only if all of the following hold:

- the `due=` and `freshness=` fields match the oracle;
- an `OVERDUE` finding has exactly `obs=entry=e.md due=<D> as_of=<A>`, and appears iff overdue;
- rc is 1 whenever the entry is overdue.

Coverage:

- **verified-at ignored (24 cases).** Eight verified-at shapes were tried: absent, undated, bad
  calendar (`2026-02-30`), future `2099-12-31`, past, bare date, empty, and same-day. Each was crossed
  with R = as-of−1, R = as-of, and R = as-of+1. The result was always `due=R`, overdue only at as-of−1.
  One extra case had `verified-at 2026-01-02` with `recheck 2026-12-01`. V+90 days would be overdue,
  but the output was `due=2026-12-01 current`, so verified-at was not used.
- **Invalid R never falls back to V (21 cases).** Inputs: `2026-02-29`, `2100-02-29`, `1900-02-29`,
  the 31st of April, June, September and November, month 00 and 13, day 00 and 32, `0000-01-01`,
  `0000-12-31`, `2026-1-01`, `20261021`, `2026-10-21,`, `2026-10-21d`, `+2026-10-21`, `10000-01-01`,
  `2026/10/21`, and `2026-10-2l`. Every case gave `due=unknown freshness=unknown`, even with a valid
  verified-at present.
- **Calendar edges (20 cases).**
  - Leap days `2000-02-29`, `2024-02-29`, `2028-02-29`, `0004-02-29`, `0400-02-29`, `1600-02-29`.
  - Month and year ends: 02-28 against 03-01, 12-31 against 01-01.
  - Range extremes `0001-01-01` and `9999-12-31` in both directions, including due 9999-12-31 with
    as-of 0001-01-01.
  - The 1969/1970 epoch crossing, the year-0 era path (`0099-03-01` against `0099-02-28`), and
    zero-padded years.
- **Token shapes (9 cases).** Tab, no space, `\v` and `\f` separators, CRLF, a continuation-line date,
  NBSP, and `\x1f`. The C `[[:space:]]` set splits on the whitespace ones. NBSP and `\x1f` are not
  delimiters, so those give `unknown`. The oracle splits with Python `bytes.split()`, which uses ASCII
  whitespace, and matched in every case.

Entry-side locale control: an entry with Arabic-Indic digits in `recheck:`, run under
`LC_ALL=en_US.UTF-8`, exited 0 with `due=unknown freshness=unknown`. The metadata function's
`local LC_ALL=C` (`tools/research-gate.sh:2539`) protects entry parsing.

## F1 — non-ASCII `--as-of` under the host default locale exits 1, not 2 (falsifying)

Observed with `env -u LC_ALL LANG=en_US.UTF-8` (the host's `/etc/locale.conf` value):

```
bash tree/tools/research-gate.sh verify-metadata fixtures/exp-past-vpast/e.md --root fixtures/exp-past-vpast --as-of '٢٠٢٦-١٠-٢١'
rc=1 stdout=0B
stderr: tree/tools/research-gate.sh: line 2297: 10#: invalid integer constant (error token is "10#")
        tree/tools/research-gate.sh: line 2550: 10#: invalid integer constant (error token is "10#")
```

The same rc=1, empty stdout, and arithmetic errors occurred for these values, all under
`LC_ALL=en_US.UTF-8`:

- `２０２６-１０-２１` (fullwidth);
- `²⁰²⁶-10-21` (superscript);
- `2026-10-2١`, which errors at line 2298: `10#2١: arithmetic syntax error`.

Under `LC_ALL=C` and `LC_ALL=C.UTF-8` the same values correctly exit 2 with
`--as-of must be a valid YYYY-MM-DD date`. The ASCII `2026-02-30` exits 2 under the default locale.

Mechanism (observed): the `--as-of` validation at `tools/research-gate.sh:6297` calls
`metadata_iso_date` at top level, under the caller's locale. There, bash's `[0-9]` range matches
non-ASCII digits. A direct check under `en_US.UTF-8`, `[[ "٢٠٢٦-١٠-٢١" =~ ^([0-9]{4})-… ]]`, printed
`MATCH ٢٠٢٦`; under C it printed `NOMATCH`. Then `$((10#…))` at line 2297 fails. Execution still
reaches the metadata mode's own `10#` at line 2550, and the run ends with exit 1 and no
`RESEARCH_GATE` line. [INFERENCE] Bash aborts the arithmetic-failing function without taking the
`|| die_usage` branch.

Effect: a caller following the documented exit contract reads exit 1 as DRIFT, not as a usage error.
A refused input therefore looks like a metadata verdict. It is not fail-open to CLEAN.

## F2 — repeated `--as-of` is last-wins; an earlier invalid value is accepted (falsifying)

Argument parsing overwrites `AS_OF_ARG` (`tools/research-gate.sh:6281-6283`), and only the final value
is validated (6297). Observed with the default locale:

| args | rc | observed |
|---|---|---|
| `--as-of 2026-13-01 --as-of 2026-10-21` | 1 | runs with `as_of=2026-10-21`; the invalid value does not exit 2 |
| `--as-of 2026-02-30 --as-of 2026-10-21` | 1 | `due=2026-10-20 freshness=overdue`; `RESEARCH_GATE: DRIFT` |
| `--as-of 2026-10-21 --as-of 2026-02-30` | 2 | refused (the last value is checked) |
| `--as-of 2026-10-19 --as-of 2026-10-21` | 1 | overdue |
| `--as-of 2026-10-21 --as-of 2026-10-19` | 0 | `freshness=current`, CLEAN: the same entry flips verdict depending on flag order |

The gate's own policy comment at 6303–6307 refuses last-wins mode flags for pin/drift because they
"would silently pin or drift the wrong path". `--as-of` gets no equivalent refusal.
[INFERENCE] The spec does not discuss repetition. The first two rows still literally contradict
"calendar-invalid value exits 2". The order-dependent verdict is a silent freshness choice of the
same kind that QUALITY 6 / M-13 exists to prevent.

## Other option probes (observed, consistent with spec)

All of the following exit 2 with the expected usage message:

- `--as-of=2026-10-21` gives `unknown flag`;
- trailing space, trailing newline, leading space, empty string, and `0000-01-01`;
- `verify-metadata F --as-of --root R` (the flag consumes `--root` as its value, which is invalid);
- `verify-all --as-of …` gives `only valid with verify-metadata`.

`--as-of` placed before the mode word is accepted, with the normal output. `--as-of 2026-08-09` is
parsed in decimal, not octal, giving `due=2026-10-20 current`.

## Scope and unknowns

- Not run: selftest, build, lint, formatter, `round26-measure.sh`, the 8 MiB probe, cadence (`<N>d`)
  arithmetic beyond the explicit-date contrast, and `--registry` composition. Whether `--registry` or
  `--root` share F2's last-wins pattern was not tested.
- F1 depends on glibc's range collation in `en_US.UTF-8`, the host default. `C.UTF-8` does not
  reproduce it.
- Fix direction (advice, no edit made): validate `--as-of` under `LC_ALL=C` (for example, a local
  `LC_ALL=C` in `metadata_iso_date`), and refuse a second `--as-of`. Each fix should get a selftest
  negative control.
- Lane writes: only this report. Fixtures, harness and captures live under
  `/tmp/chousa-r26-falsify-FDateExplicitDate/`.
