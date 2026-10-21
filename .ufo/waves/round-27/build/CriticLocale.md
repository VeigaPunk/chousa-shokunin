# CriticLocale — C2 ASCII date contract under an inherited locale (round 27 attempt 1)

Seat `ChousaR27.CriticLocale`, critic. Author-lane advice only, not an admission or a judgment.
Static read of master `64eec5d4` (`git rev-parse HEAD` observed). `work/ExecDates` was still at
`64eec5d` with no diff when I read it, so I am attacking the fix shapes that are on the table:
the r26 advice in `.ufo/waves/round-26/falsify/FDateAsOfUsage.md:111-113` and
`FDateHugeCadence.md:104-107`. Nothing was executed. No gate, selftest, or differential was run.
Tools installed: none.

Axes: freshness (C2 correctness) is primary. Calibration is affected through oracle and control
vacuity, and operability through usage exit 2.

## K1 — HIGH: the Python oracles accept Unicode digits, and `int()` fails on the 128 KiB control

Counterexample: if the new suite reuses the round26 differential's helpers, it cannot tell the
correct gate from the broken one on exactly the C2 controls.

Evidence:
- `corpus/evidence/round26-date-differential.sh:38-39` contains `ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")` and `DAYS_RE = re.compile(r"^(\d+)d$")`.
  Python `str` patterns make `\d` match Unicode Nd and `\s` match Unicode spaces (`:58`). So
  `２０２６-10-21` and `٩٠d` count as valid to this oracle, which agrees with the unfixed gate.
- `:62-64` contains `timedelta(days=int(days_match.group(1)))` and `except (OverflowError, ValueError): due = None`.
  [INFERENCE, not run] On CPython 3.11 and later (the host has 3.14.8), `int()` on a string of more
  than 4300 digits raises `ValueError` from the int/str digit limit, and leading zeros count toward
  that limit. A 128 KiB cadence `0…090d` would therefore get the oracle answer `due=unknown`. The
  C2 target requires the representable value (`due=2026-04-02 freshness=overdue`), so the oracle
  would reward the wrong behaviour. This is a false-provenance path to "0 mismatches".
- `int()` also accepts `１２`, `1_0`, ` 12`, and `+12`.

Impacted axes: freshness and calibration.

Smallest safe correction: the new `round27-regressions.py` must not import or copy these helpers.
- Validate with `re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", s, re.ASCII)` and `[0-9]+` plus `re.ASCII`.
- Normalize with `t = s.lstrip("0") or "0"`, and check `len(t) <= 7` *before* calling `int(t)`.
- Build dates with `datetime.date(int(y), int(m), int(d))`, never `fromisoformat`, which accepts
  `20261021` (r26 F2 controls).
- Leave the round26 differential unchanged. It only generates ASCII inputs, so it stays a valid
  original-differential run, but its oracle must never be pointed at the new fixtures.

## K2 — HIGH: Unicode-digit controls go vacuous unless the suite forces and proves a sensitizing locale

Counterexample: the r26 reproduction only occurs under glibc `en_US.UTF-8`. Under `C` and
`C.UTF-8` the base gate already returns rc=2 (`FDateAsOfUsage.md:44-45`, 18 of 18). A control
that inherits L1's environment therefore passes on the *unfixed* base whenever L1 runs with
`LC_ALL=C`, `C.UTF-8`, or a missing locale.

Evidence:
- The selftest helper `metadata_asof_usage_case` runs `out=$(bash "$SELF" "$@" 2>&1)` (`tools/research-gate.sh:6015`).
  It sets no environment, and its argv-only signature cannot inject `LC_ALL`.
- The differential copies the parent environment with `env = dict(os.environ)` (`round26-date-differential.sh:90`).
- [INFERENCE] Under PEP 538, CPython started with `LANG=C` and `LC_ALL` unset writes
  `LC_CTYPE=C.UTF-8` into `os.environ`. A copied environment then pins the child bash to an
  ASCII-only `[0-9]`. Separately, if `en_US.UTF-8` is not installed, glibc falls back to C after a
  bash `setlocale` warning, and the control again passes silently.

Impacted axes: calibration and freshness.

Smallest safe correction:
- Build each child environment explicitly. Pop `LC_ALL`, `LC_CTYPE`, `LC_COLLATE`, and `LANG`, then
  set one of these per variant:
  - `{LC_ALL=en_US.UTF-8}`
  - `{LANG=en_US.UTF-8}` alone
  - `{LC_CTYPE=en_US.UTF-8, LANG=C}`
  - `{LC_ALL=C}`
  - `{LC_ALL=C.UTF-8}`
- Before asserting anything, run a sensitization probe under the same environment: `bash -c '[[ ２ =~ ^[0-9]$ ]]'` must return 0.
  If it does not, record `locale_sensitized=no` and make that a non-pass, either nonzero or an
  explicit SKIP that is not counted as agreement.
- Any new selftest case needs a new env-carrying helper and must be **appended after** the
  original 187. Inserted cases shift the `ok-case %-2d` ordinals (`:6017`) and break "all 187
  original case identities preserved".
- Pass non-ASCII argv as bytes (`os.fsencode`) so the harness's own locale cannot re-encode it.

## K3 — MEDIUM: a CLI-only `LC_ALL=C` wrapper creates a second validation authority

Counterexample: the r26 fix shape "run the CLI check under `LC_ALL=C`" protects only
`tools/research-gate.sh:6297`. `metadata_iso_date` (`:2296`) and `metadata_add_days`
(`:2346`, `[[ $digits =~ ^[0-9]+$ ]]`) are locale-safe today only because of the dynamic scope of
the caller's `local LC_ALL=C` in `verify_metadata` (`:2539`). Any future caller outside that scope
reopens F1, including the leading-zero regex fix proposed in `FDateHugeCadence.md:107`.

Further evidence:
- The entry-side protection is itself unobserved. `FDateAsOfUsage.md:105-108` marks it as [INFERENCE].
- [INFERENCE] Whether `LC_ALL=C metadata_iso_date …` (a temporary-environment prefix on a function
  call) re-runs `setlocale` in bash 5.3 is not established here. Relying on it is unproven.
- Setting `LANG=C`, `LC_CTYPE=C`, or `LC_COLLATE=C` alone is defeated by an inherited `LC_ALL=en_US.UTF-8`, because `LC_ALL` takes precedence.
- A global `export LC_ALL=C` at script start is an identity change for every mode, for example the
  `[[:alnum:]_]` boundaries on non-ASCII bytes (`:2474`, `:2542`). It would need the full
  legacy161 and differential evidence, so it is not the smallest fix.

Impacted axes: freshness, plus duplicate authority and hidden regression.

Smallest safe correction: make the single authority locale-independent by construction.
- In `metadata_iso_date`, `metadata_add_days`, and `metadata_verified_at_bare` (`:2525`), plus the
  entry regexes `:2698`, `:2721`, `:2741`, `:2744`, replace `[0-9]` with the explicit list
  `[0123456789]`. Either that, or add `local LC_ALL=C` as the first statement of each helper.
  Explicit lists do not depend on locale, on `setlocale` side effects, or on scope.
- Keep `:6297` calling the same `metadata_iso_date`. Do not add a separate CLI regex.

## K4 — MEDIUM: persist the entry-side Unicode-digit outcomes, not only the CLI ones

The C2 contract ("ASCII YYYY-MM-DD under any inherited locale", `round27-claims.md:9`) also
covers `verified-at:` and `recheck:` text. No control exists for it today: the original
`metadata-asof-*` cases are all ASCII (`:6045-6134`).

Required persisted controls, each under the sensitized `en_US.UTF-8` environment and under `LANG`-only:
- `verified-at: ２０２６-10-01` with `recheck: 90d` should give `verified_at=undated`, `META_VERIFIED_AT_UNDATED`, and `due=unknown`.
- `recheck: ٩٠d` and `recheck: ２０２６-12-30` should give `recheck=unscheduled` and `due=unknown`.
- Mixed single positions, for example `2026-10-2１`.
- `--as-of` with each of fullwidth, Arabic-Indic, NKo, Devanagari, mathematical bold, and superscript digits should give rc=2, the exact message, no `^RESEARCH_GATE: ` line, and no `line N:` bash diagnostic.
- `--as-of` containing a raw invalid UTF-8 byte (`\xff`) in a digit slot. Pass it as bytes. The expected result is rc=2.
- `２０２６-02-30` should give rc=2 through the date message, not through an arithmetic error.

## K5 — LOW/tradeoff: the leading-zero repair must be value-checked and linear

`digits=${digits##+(0)}` (`:2348`) under the global `shopt -s extglob` (`:256`) was observed to
crash with SIGSEGV at 68k or more zeros (`FDateHugeCadence.md:53`).

- **Prior replacement:** `[[ $digits =~ ^0*([0-9]*)$ ]]` was observed to pass 24 of 24 cases, and
  completed 256k zeros in 0.19 s (`:110-112`). That observation was under the `LC_ALL=C` scope. K3's
  explicit list keeps it safe if the scope ever changes.
- **Hidden-cost shapes to reject:**
  - `while [[ $digits == 0* ]]; do digits=${digits#0}; done` is O(n²) copying.
  - [INFERENCE] The pair `${digits#"${digits%%[!0]*}"}` performs a quoted 128 KiB literal
    shortest-prefix removal, which may scan prefixes quadratically in bash's `remove_pattern`.
    Either shape turns a crash into a timeout, which is still a C2 failure.
- **Control assertions:**
  - The 128 KiB control must assert the exact computed line `due=2026-04-02 freshness=overdue`
    with rc=1, not just "rc in {0,1}". A reader refusal would otherwise pass vacuously.
  - The all-zero control (`0…0d`) must assert `due=<verified-at>`. With as-of equal to verified-at,
    the result is `current` and rc=0. With as-of one day later, it is `overdue` and rc=1. This
    exercises strict `>`.
  - Maximum span: `0001-01-01` plus `3652058d`, with and without 128 KiB of leading zeros, should give `9999-12-31`.
  - `3652059d` should give `unknown`.
  - A 7-digit non-zero tail should compute. An 8-digit non-zero tail should give `unknown`.
- [INFERENCE] Near the 8 MiB reader cap, glibc `regexec` allocates O(n) per-position state.
  The existing plain-mode regexes at `:2715` and `:2721` already pay this cost, so the repair adds
  a constant factor, not a new class. Report it as an inherited resource limit, not as proven safe.

## Unrun checks (for L1, once, after integration)

- `python3 corpus/evidence/round27-regressions.py --gate tools/research-gate.sh` on the base archive
  and on the final tree. Include the `locale_sensitized` field in the receipt.
- `bash tools/research-gate.sh --selftest`. Confirm the 187 original names and ordinals are unchanged and the new cases are appended.
- The round26 date differential, unchanged, on isolated copies.
- None of these were run by this seat.
