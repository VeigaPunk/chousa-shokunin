# FDateAsOfUsage — C2 `--as-of` calendar/option falsification (round 26 attempt 1)

Seat `ChousaR26R.FDateAsOfUsage`, author-lane advice only (no outside judge / SHONEN claim).

## Verdict

**C2 FALSIFIED on the usage contract** ("an absent or calendar-invalid value exits 2"; "never
evaluates user text as a Bash arithmetic expression"). Under the operator's inherited locale
(`LANG=en_US.UTF-8`), an `--as-of` value that uses non-ASCII decimal digits passes the
top-level shape check, crashes inside `$((10#…))` with raw Bash diagnostics carrying script
line numbers, **bypasses the `die_usage` guard**, and exits **1**, which is the gate's DRIFT
exit code, instead of 2. The calendar-invalid ASCII cases, missing-value cases, and wrong-mode
cases all behave as specified. One weaker spec-gap finding is listed separately: with repeated
`--as-of`, the last value wins.

## Target identity

- Revision: `0e9784bd52eca456b24d0bc40921480a47f91a2b` (committed 2026-10-21T09:48:28-03:00),
  from `corpus/evidence/round26-measured-revision.json`. The lane `HEAD` matched it when observed.
- Claim base: `ba3333254dd337658a4f25e7a9471f9cf4e4567e`.
- Sandbox: `git archive 0e9784bd… | tar -x -C /tmp/chousa-r26-falsify-FDateAsOfUsage/tree`.
  Sandbox hashes match the measured-revision record:
  `tools/research-gate.sh` c2c813f1…abc6, `corpus/QUALITY.md` 2428baaf…f2ce6,
  `corpus/evidence/round26-claims.md` dcbe2b5f…f1c.
- Environment: GNU bash 5.3.20, glibc 2.44, Python 3.14.8. Inherited `LANG=en_US.UTF-8`, with
  `LC_ALL`, `LC_CTYPE` and `LC_COLLATE` unset. Installed locales: `C`, `C.utf8`, `en_US.utf8`.
- Tools installed or updated: **none**.

## Independent oracle

Validity comes from the frozen spec, not from the gate's code. The value must match
`re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", s, re.ASCII)` and then pass
`datetime.date(y, m, d)` (proleptic Gregorian, year ≥ 1). For accepted values, the expected
`due`/`freshness` and exit code come from `datetime` arithmetic on two data-only fixtures:
`current.md` (verified-at 2026-10-01, recheck 90d) and `dated.md` (recheck 2026-03-01).
Entry text is never executed.

## Commands and exits

| # | Command (cwd `/tmp/chousa-r26-falsify-FDateAsOfUsage`) | Exit | Result |
|---|---|---|---|
| 1 | `python3 harness.py` | 0 (harness) | 274 gate runs; 6 contract failures; 0 injection sentinels created |
| 2 | per-locale loop over 9 non-ASCII digit values × `C`/`C.UTF-8`/`en_US.UTF-8` | — | `C`, `C.UTF-8`: 18/18 rc=2 with the correct message; `en_US.UTF-8`: 9/9 rc=1 with a Bash diagnostic |
| 3 | `python3 enum_digits.py {en_US.UTF-8,C.UTF-8,C}` (glibc `regcomp`/`regexec`, the same API as Bash `=~`) | 0 | `^[0-9]$` matches 1050 code points in en_US.UTF-8 (523 Nd, 343 No, 109 Nl, 75 So), and only ASCII 0–9 in C and C.UTF-8. No ASCII non-digit is ever admitted |
| 4 | guard-bypass probes (below) | 2 / 2 / 1 / 2 / 1 / 2 | see the raw text below |

The harness ran 64 values in each of four locales (inherited, `C`, `C.UTF-8`, `en_US.UTF-8`).
Of those values, 52 are spec-invalid and 12 are spec-valid. The harness also ran 21
option-shape cases.

## F1 — HIGH: non-ASCII digits bypass `--as-of` validation and exit 1 with Bash diagnostics

Raw text (exact):

```
$ LC_ALL=en_US.UTF-8 bash tools/research-gate.sh verify-metadata root/k/current.md --root root --as-of ２０２６-10-21
rc=1 stdout_bytes=0
  stderr| tree/tools/research-gate.sh: line 2297: 10#: invalid integer constant (error token is "10#")
  stderr| tree/tools/research-gate.sh: line 2550: 10#: invalid integer constant (error token is "10#")
$ ... --as-of 2026-10-2１
  stderr| tree/tools/research-gate.sh: line 2298: 10#2１: arithmetic syntax error: invalid arithmetic operator (error token is "１")
$ LC_ALL=en_US.UTF-8 bash tools/research-gate.sh verify-metadata /nonexistent/x.md --as-of ２０２６-10-21
rc=2
  stderr| tree/tools/research-gate.sh: line 2297: 10#: invalid integer constant (error token is "10#")
  stderr| research-gate: metadata path not found: /nonexistent/x.md
$ ... verify-metadata root/k/current.md --root root --registry /nonexistent/reg.md --as-of ２０２６-10-21
rc=1 stdout_bytes=0   (line 2297 + line 2550 diagnostics; registry refusal never reached)
```

The same failure reproduced for these values: fullwidth `２０２６-10-21`, Arabic-Indic
`٢٠٢٦-10-21`, NKo, Devanagari, mathematical bold `𝟐𝟎𝟐𝟔`, superscript `²⁰²⁶`, and mixed
positions in the month and day fields. It also reproduced for the calendar-invalid
`２０２６-02-30`.

Mechanism (observed through the line numbers and fall-through, plus a source read):

1. The top-level check at `tools/research-gate.sh:6295-6298` calls `metadata_iso_date`
   **outside** any `local LC_ALL=C` scope. The `verify_metadata` function (`:2539`) and the
   registry loader (`:2366`) both pin `LC_ALL=C`, but this CLI check does not.
2. `metadata_iso_date` (`:2296`) tests `[[ $1 =~ ^([0-9]{4})-([0-9]{2})-([0-9]{2})$ ]]`. Under
   en_US.UTF-8, glibc's `[0-9]` admits 1,040 non-ASCII numeric code points.
3. Line `:2297` then expands `$((10#…))` on the matched text. Bash arithmetic errors, and that
   aborts the whole top-level `if (( AS_OF_ARG_SET ))` compound, so `die_usage` is never
   called. The probe that reaches the `metadata path not found` refusal proves that execution
   continues into `verify_metadata` with an unvalidated `AS_OF_ARG`.
4. Line `:2550` runs `$((10#$asof_year))` again and aborts. The process exits 1.

Contract impact:

- **Exit code:** the result is 1, not 2. Exit 1 means DRIFT on this CLI (`:197`, `:371`), so
  a caller that checks the exit code would read a usage error as a freshness drift.
- **Diagnostics:** raw Bash diagnostics with script line numbers appear on stderr, which is
  the shell equivalent of a traceback.
- **Arithmetic evaluation:** user text reaches the Bash arithmetic evaluator. The impact is
  bounded: the enumeration admits no ASCII operator or identifier character, and none of the
  six `$(touch …)` / backtick / `a[$(…)]` sentinels were created in any locale. So there is no
  code execution, but the "never evaluates user text as arithmetic" clause is violated in
  letter.
- **Default exposure:** this fires under the default inherited locale (harness row
  `value[None]`), not only with an exotic `LC_ALL`.

Why the shipped checks miss it: `metadata-asof-invalid` and `metadata-asof-missing`
(`:6083-6086`) use only ASCII values. `round26-date-differential.sh` builds only valid ASCII
`--as-of` values (`:69`) and sets no `LC_ALL`.

[INFERENCE, not run here, out of scope] Entry-side `verified-at:`/`recheck:` parsing
(`:2720`, `:2739`, `:2747`, and `:2345` through `metadata_add_days`) runs inside
`verify_metadata`'s dynamically scoped `local LC_ALL=C`, so it should not be exposed. The
CLI site at `:6297` is the only unpinned caller found.

Advice (not a production edit): run the CLI check under `LC_ALL=C`, or make
`metadata_iso_date` locale-independent (for example `[0123456789]`, or a function-local
`LC_ALL=C`). Then add one non-ASCII-digit usage case that runs under a UTF-8 locale.

## F2 — LOW (spec gap): repeated `--as-of` is last-wins, so an earlier invalid value is silently accepted

```
verify-metadata current.md --root root --as-of 2026-02-30 --as-of 2026-10-21   -> rc=0, normal output
verify-metadata current.md --root root --as-of ''         --as-of 2026-10-21   -> rc=0
verify-metadata current.md --root root --as-of 2026-10-21 --as-of 2027-06-01   -> rc=1, uses as_of=2027-06-01
verify-metadata current.md --root root --as-of 2026-10-21 --as-of 2026-02-30   -> rc=2 (correct)
```

A calendar-invalid value that the user supplied does not exit 2 when a valid value follows
it. This matches the CLI's existing last-wins convention for value flags (`--root /nonexistent
--root root` gives rc=0). The script refuses doubled flags only for `--pin`/`--drift`
(`:6303-6315`). Spec v1 does not address duplicates, so this is a spec gap, not a regression.

## Behaviour that held (expected negative controls, not regressions)

- **Calendar-invalid ASCII values:** `2026-02-30`, `2026-02-29`, `2100-02-29`,
  `1900-02-29`, the 31st of April, June, September and November, month 13, month 00, day 00,
  day 32, `0000-01-01`, `0000-02-29` and `2026-99-99`. Each gave rc=2, empty stdout, no
  verdict line, and the exact message `research-gate: --as-of must be a valid YYYY-MM-DD date`,
  in all four locales.
- **Shape-invalid ASCII values:** empty, padded with spaces, newline-padded, `2026-1-21`,
  `26-…`, `02026-…`, `+`/`-` prefixes, `/` separators, `20261021` (which Python's
  `fromisoformat` would accept), `T00:00`, week dates, ordinal dates, a `Z` suffix, a Unicode
  hyphen, a value with a 5,000-byte tail, `--`, `-h`, `--root` and `verify`. Each gave rc=2
  with the correct message in all four locales.
- **Arithmetic-shaped values:** `AS_OF_ARG_SET`, `asof_days`, `10#2026`, `2026-10-21+1`,
  `0x7E8-10-21` and the six command-substitution values. Each gave rc=2, with no sentinel
  file created.
- **Missing values:** a trailing `--as-of` gave rc=2 with `--as-of needs YYYY-MM-DD`. When
  `--as-of` swallows the next token (`--root` or the PATH), the result is rc=2 through the
  must-be-valid message.
- **Wrong mode:** `verify`, `verify-all`, `--selftest` and `--drift`, plus a mode
  overwritten by last-wins, each gave rc=2 with `--as-of is only valid with
  verify-metadata`. The wrong-mode check precedes date validation, so wrong mode plus a
  non-ASCII value still exits 2 cleanly.
- **Other forms:** `--as-of=2026-10-21` gave rc=2 with `unknown flag`. `--as-of` alone with
  no mode gave rc=2. An invalid ASCII value with no PATH gave rc=2 through the date message.
- **Calendar-valid accept controls:** `2026-10-21`, `2024-02-29`, `2000-02-29`, `0400-02-29`,
  `0001-01-01`, `9999-12-31`, `2026-08-09`, `2026-09-08`, `2026-12-30`, `2026-12-31`,
  `1582-10-10` and `2026-01-31`, across 4 locales and 2 entries. Every per-entry
  `due=… freshness=…` value and every exit code (0, or 1 when any entry is overdue) agreed
  with the Python oracle. The leading-zero values `08` and `09` caused no octal error.
- **Observation, not C2:** arguments after `--` are silently ignored (`-- --as-of 2026-02-30`
  gives a plain run with rc=0). The base already had the same `--) shift; break` at base
  `:5706`, so this is pre-existing.

## Remaining unknowns

- I did not check other UTF-8 locales or musl/BSD regex engines. glibc en_US.UTF-8 is
  confirmed affected, and C.UTF-8 is confirmed unaffected.
- The entry-side exposure is inferred, not run (see F1).
- I did not run the selftest, build, lint, the 8 MiB amplification probe, or
  `round26-measure.sh`. These were outside the authorization.

Sandbox artefacts: `/tmp/chousa-r26-falsify-FDateAsOfUsage/{harness.py,enum_digits.py,results.json}`.
