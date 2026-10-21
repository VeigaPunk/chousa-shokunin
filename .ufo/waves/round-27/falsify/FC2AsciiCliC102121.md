# FC2AsciiCliC102121 — falsify `ascii-cli-C-２０２６-10-21` (C2) at dd72641e

Target: dd72641e574679c4f7882dd43de072b4c8892d6f, gate sha256 ca39d14d…2f84 (verified in sandbox).
Sandbox: /tmp/chousa-r27-falsify-FC2AsciiCliC102121 (git archive of the target). bash 5.3.20, glibc 2.44.
Installed locales: C, C.utf8, en_US.utf8, POSIX. No tools installed.

## Verdict

- **Control `ascii-cli-C-２０２６-10-21`: FALSIFIED (vacuous).** It passes on the pre-repair base gate (64eec5d4) and with the targeted fix reverted. It cannot detect the regression it is meant to guard.
- **Landed gate behavior for this class: HOLDS.** Tried 23 nearby `--as-of` inputs under C, en_US.UTF-8 and C.utf8. Every non-ASCII or malformed input exits 2 with the diagnostic and no verdict, and the boundary-valid dates are accepted.
- **Sibling family defects (same loop, lines 123–128):** a harness crash for the wrong reason, one-sided coverage, and a hard-coded locale. Details below.

## (1) Is the expectation independent of the gate code?

Mostly yes. The control expects exit 2, the text `--as-of must be a valid YYYY-MM-DD date`, zero `^RESEARCH_GATE: ` records, and none of the bash errors `invalid integer` / `arithmetic syntax` / `cannot change locale`. These come from the C2 contract ("ASCII YYYY-MM-DD under any inherited locale") plus the usage-error semantics that already existed. The diagnostic text was already in the base gate and in its selftest case `metadata-asof-invalid`. Nothing is computed from the gate code.

The weakness is coverage. "Any inherited locale" is sampled with two fixed locales:
- `C` cannot discriminate, because bash/glibc `[0-9]` never matches multibyte digits in the C locale.
- `en_US.UTF-8` is hard-coded. There is no discovery step and no skip.

## (2) Mutation evidence

The targeted fix is the single line `local LC_ALL=C` at the top of `metadata_iso_date` (gate line 2311). Driver: `ctl.py`, a verbatim replica of the script's `run()` (lines 60–67) and the observe criteria (lines 123–128). The full regression script and the full selftest were not run.

| Gate variant (sha256 prefix) | C ×3 tokens | en_US.UTF-8 `２０２６`/`٢٠٢٦` | en_US.UTF-8 `2026-10-2１` |
|---|---|---|---|
| landed (ca39d14d) | PASS | PASS | PASS |
| A: drop the 2311 `local LC_ALL=C` (50276d47) | **PASS** | FAIL: exit 1, `10#: invalid integer constant` | **harness crash** |
| B: drop the 2311 and 2360 `LC_ALL=C` lines (46c80f69) | **PASS** | FAIL (same) | harness crash |
| C: whole base gate 64eec5d4 (c2c813f1) | **PASS** | FAIL (same, base line 2297) | harness crash |
| D: `[0-9]`→`[[:digit:]]` with LC_ALL=C kept (2b8c6c76) | PASS | PASS | PASS (equivalent mutant) |
| E: CLI `metadata_iso_date` guard removed (1947d75c) | FAIL `invalid integer` / crash | — | — |
| F: over-reject, `[[ ${LC_ALL:-C} == C ]] \|\| return 1` (19eb39b4) | **PASS** | **PASS** | **PASS** |

Commands (exit codes):
- `python3 ctl.py mut/landed.sh` → exit 0, 6/6 PASS.
- `python3 ctl.py mut/A-no-isodate-lcall.sh` → exit 1. The C rows PASS and the two en_US rows FAIL with `exit 1 != 2; missing diag; forbidden 'invalid integer'`. The run then ends with a traceback: `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xef in position 251`.
- Base gate in C locale, all 3 tokens: rc=2 with the diagnostic present. This confirms the C control passed before the round-27 repair.

Conclusions:
- **C variant (the assigned item):** it does not fail when the fix is reverted, or on base. It is vacuous for the repair.
- **en_US variant, tokens `２０２６`/`٢٠٢٦`:** these fail for the intended reason, a locale-admitted digit reaching `10#` arithmetic.
- **en_US variant, token `2026-10-2１`:** this fails for the wrong reason. With the fix reverted, line 2574 (`asof_day=${AS_OF_ARG:8:2}`, which slices bytes under verify_metadata's `LC_ALL=C`) emits `10#2\xef: arithmetic syntax`, a split UTF-8 sequence. `subprocess.run(..., text=True)` decodes strictly, so the regression script raises an uncaught `UnicodeDecodeError`. The crash also happens when the parent Python runs with LC_ALL=C. Effects:
  - The exit code is 1, the same as a contract mismatch, even though the docstring says setup errors exit 2.
  - No summary JSON is printed, no MISMATCH lines appear, and no `--output` file is written.
  - Every later control is never evaluated, which covers all C3 rows after line 128.
- **Mutant F (one-sided coverage):** it breaks valid ASCII dates under en_US. `--as-of 2026-10-21` gives rc=2 and a usage error, versus rc=1 DRIFT with `due=2026-04-02 freshness=overdue` in C. All 6 ascii-cli controls still pass.
  - [INFERENCE, by inspection, not run] F survives the whole 58-control suite, because only lines 123–128 pass a non-C `locale`.
  - [INFERENCE] Whether the full selftest catches F depends on the locale L1 ran it under.

## (3) Nearby inputs and counterexamples

Landed gate, run under C, en_US.UTF-8 and C.utf8 (`bash sweep.sh`).

These all exit 2 with the diagnostic, 0 verdict lines and no bash errors:
- Non-ASCII digits: Devanagari `२०२६`, Bengali, math-bold `𝟐𝟎𝟐𝟔` (4-byte), superscript `²⁰²⁶` (en_US `[0-9]` matches `²` too), full-width all fields.
- Non-ASCII hyphens: U+FF0D, U+2010, U+2212.
- Stray characters: trailing `\n`, trailing `\r`, leading or trailing space, ZWSP, combining acute.
- Other malformed forms: `+2026-…`, 5-digit year, `0000-01-01`, `2026-02-29`, `2026-1-021`, empty string.

Boundary-valid dates are accepted with correct freshness: `2028-02-29`, `9999-12-31`, `0001-01-01`.

Two more checks:
- Locale scope: `local LC_ALL=C` is restored after the function returns in bash 5.3 (probe: inside no match, after return the en_US match is restored), so there is no locale leak.
- Entry side: full-width `verified-at` or `recheck` under en_US is classified as undated or unscheduled without arithmetic errors, because verify_metadata has `local LC_ALL=C`.

**No input was found where the landed gate is wrong.** Counterexamples against the control:

1. **Vacuity:** `ascii-cli-C-２０２６-10-21` passes on base 64eec5d4 and on mutants A, B and F.
2. **Wrong-reason failure:** with the fix reverted, `ascii-cli-en_US.UTF-8-2026-10-2１` crashes the harness (`UnicodeDecodeError`) instead of recording a mismatch.
3. **Host-dependent spurious failure:** on a host without en_US.UTF-8 (simulated with the uninstalled `de_DE.UTF-8`), the correct landed gate prints `warning: setlocale: LC_ALL: cannot change locale`. That string is in the control's forbidden list, so the en_US rows would FAIL instead of skipping. On such a host no row would discriminate. The gate's own selftest discovers a locale and skips (lines 6308–6327); the regression control does not.

## Impacted axes

- **freshness:** the control family claims Unicode-digit rejection "under any inherited locale", but only one hard-coded row discriminates.
- **calibration:** the C row adds a green count with zero discriminating power.
- **operability:** the harness crash is indistinguishable from a mismatch by exit code and suppresses the summary and every later control.

## Smallest safe correction (author lane; controls only, no gate change needed)

1. Choose the discriminating locale by precondition, the way the selftest does: the first `locale -a` entry where `bash -c '[[ ２ =~ ^[0-9]$ ]]'` succeeds. Record a setup/skip outcome (exit 2) if none exists. Relabel the C rows as non-discriminating guards, or drop them from the C2 discriminating count.
2. Add a positive row in that locale: `--as-of 2026-10-21` must give rc=1 and `due=2026-04-02 freshness=overdue`. This kills mutant F.
3. Pass `errors='surrogateescape'` (or `'replace'`) to the three `subprocess.run(..., text=True)` calls, so non-UTF-8 gate output becomes a recorded mismatch rather than an uncaught exception.

## Limits

- Only bash 5.3.20 and glibc 2.44 were tested. Other glibc or musl builds may differ in which locales admit non-ASCII `[0-9]`.
- The full regression script and the full selftest were not run (L1 owns them). The claim that F survives the whole suite is an inference from code inspection.
- All fixtures are synthetic and live under the sandbox. No lane files were edited apart from this report.
