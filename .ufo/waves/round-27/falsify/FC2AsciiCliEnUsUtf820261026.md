# Round 27 falsify: C2 control `ascii-cli-en_US.UTF-8-2026-10-2１`

- Target: dd72641e574679c4f7882dd43de072b4c8892d6f (lane chousa-shokunin, master).
- Gate sha256 verified in sandbox: `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84`.
- Item: `corpus/evidence/round27-regressions.py` lines 122-128 (generator `ascii-cli-{C,en_US.UTF-8}-{token}`, 6 rows; named row = `en_US.UTF-8` x `2026-10-2１`).
- Sandbox: `/tmp/chousa-r27-falsify-FC2AsciiCli` (`git archive dd72641e | tar -x`). Leaf; no subagents; no network; full selftest and full regression script NOT run.
- Axes: freshness (ASCII date grammar), calibration (control discrimination), operability (harness).

## Verdict

**FALSIFIED** on Q2 (intended-reason failure) for the named row. Q1 **HOLDS**. Q3: control-level counterexamples found; **no landed-gate counterexample** across 27 nearby synthetic inputs and 13 calendar-boundary cases.

- The named row passes on landed and fails on the pin-removed mutant, but for its own token the failure is an uncaught harness `UnicodeDecodeError`. None of its declared checks is recorded.
- Its two C-locale siblings pass on the pre-fix mutant, so they do not discriminate this fix.

## Q1: expectation derived from declared contract, independent of gate code? HOLDS (with couplings)

- Exit 2: gate's own usage table, `Exit: 0 CLEAN | 1 DRIFT | 2 setup/usage`.
- Zero `^RESEARCH_GATE: ` records: C1 rule (no verdict on a usage error).
- Unicode-digit `--as-of` must be rejected: C2 "ASCII YYYY-MM-DD under any inherited locale".
- No gate logic is copied; `run()`/`observe()` are independent of `metadata_iso_date`.
- Couplings (wording or environment, not logic):
  - (a) required text `--as-of must be a valid YYYY-MM-DD date` is a literal copy of the gate's message.
  - (b) forbidden `invalid integer` and `arithmetic syntax` are bash messages; bash 5.3.20 emits the latter for the day token.
  - (c) forbidden `cannot change locale` makes the en_US half FAIL, not skip, on a host lacking the locale. Observed for de_DE: `bash: warning: setlocale: LC_ALL: cannot change locale (de_DE.UTF-8): No such file or directory`. [INFERENCE] en_US absence takes the same path; en_US.utf8 is installed here and was not removed.

## Q2: revert the fix; does the control fail for the intended reason? FALSIFIED for the named row

Mutant `gate-mutant.sh` = landed minus one line: `diff tools/research-gate.sh gate-mutant.sh` gives `2311d2310 < local LC_ALL=C` (diff rc=1, single hunk; mutant sha256 prefix `50276d4780b11fa2`). That line is the production fix: the locale pin inside `metadata_iso_date`.

Named row on the mutant, `python3 one_control.py gate-mutant.sh en_US.UTF-8 '2026-10-2１'`:
- Harness exits 1 with `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xef in position 215: invalid continuation byte`. No `CONTROL` record is printed.
- Cause: stderr contains `gate-mutant.sh: line 2574: 10#2\xef: arithmetic syntax error ... (error token is "\xef")`. Under the pinned scope (`LC_ALL=C`), `asof_day=${AS_OF_ARG:8:2}` slices bytes, not characters, so it splits the 3-byte `１` (bytes 9-11). Bash prints a lone 0xEF byte.
- Harness: `run()` catches only `TimeoutExpired`; decoding happens inside `subprocess.run(text=True)` before `observe()`. The raw text would have matched forbidden `arithmetic syntax`, but it is never checked. The summary and `--output` are written only after the loop (lines 225-237), so the run aborts and no per-control record is produced. Controls later in file order, including every C3 control, are not evaluated.

Sibling en_US rows, same mutant, no decode error:
- `２０２６-10-21`: `FAIL ['exit 1 != 2', "missing '--as-of must be a valid YYYY-MM-DD date'", "forbidden 'invalid integer'"]`. These are the intended reasons.
- `٢٠٢٦-10-21`: identical FAIL.

C-locale rows, same mutant: `C '２０２６-10-21'` PASS rc=2; `C '2026-10-2１'` PASS rc=2. These rows do not test the fix.

Landed: all four en_US/C control rows PASS (rc=2, diagnostic present, no forbidden text, 0 verdicts).

## Q3: nearby counterexamples

1. **Harness crash (minimal counterexample).** `gate-mutant.sh` + `LC_ALL=en_US.UTF-8` + `--as-of 2026-10-2１` gives harness `UnicodeDecodeError`, gate rc=1, no record. The trigger is any gate diagnostic containing a partial multibyte character, not only this token.
2. **Non-discriminating half.** The three `C` rows pass on the pre-fix mutant, so 3 of 6 rows do not test the fix.
3. **Coverage gap (landed not wrong).** Only three non-ASCII tokens persist in the independent suite (`[^\x00-\x7F]` matches line 124 only). Entry-side Unicode dates are not controlled. Landed probes:
   - `verified-at: ２０２６-01-02` gives `verified_at=undated ... verdict=drift`.
   - `verified-at: ٢٠٢٦-01-02` gives undated.
   - `recheck: ９０d` gives `recheck=unscheduled verdict=clean`.
   - `recheck: ２０２６-10-21` gives unscheduled.
   - `recheck: 90ｄ` gives unscheduled.
   All are consistent with the ASCII grammar.
4. **Landed gate: no counterexample found.**
   - `--as-of` under en_US.UTF-8, 9 tokens (`２０２６-10-21`, `٢٠٢٦-10-21`, `2026-10-2１`, `2026-10-２１`, `2026-１0-21`, `२०२६-10-21`, `2026-10-21\n`, `2026-10-21\u3000`, `2026-10-21٠`): all rc=2, diagnostic present, 0 verdicts, stderr strict-UTF-8. The three control tokens also give rc=2 under C.UTF-8.
   - Calendar sweep against Python `date` from 2026-01-02, as-of 2026-10-21, 13 cadences (0, 1, 59, 365, 1461, 36524, 146097, 1000000, 2000000, boundary-1, boundary, boundary+1, 3000000): 13/13 OK. Boundary = 2912441 days = 9999-12-31; boundary+1 gives unknown.
   - Structural: `local LC_ALL=C` covers `metadata_iso_date`, `metadata_add_days`, and the metadata entry and registry functions. The `date` calls (lines 290-293) are banner timestamps, not freshness inputs.

## Mutation evidence

| Variant | en_US `２０２６-10-21` | en_US `٢٠٢٦-10-21` | en_US `2026-10-2１` (named) | C `２０２６-10-21` | C `2026-10-2１` |
|---|---|---|---|---|---|
| landed | PASS rc=2 | PASS rc=2 | PASS rc=2 | PASS rc=2 | PASS rc=2 |
| pin removed | FAIL: exit 1!=2, missing diag, forbidden `invalid integer` | FAIL: same | HARNESS CRASH: UnicodeDecodeError, harness exit 1 | PASS rc=2 | PASS rc=2 |

Mutant caveat: the pin-removed mutant reproduces the pre-fix Unicode-digit `--as-of` path, which the r26 baseline also reports. It was run because Q2 requires a sandbox mutation, not to confirm the baseline. No base-revision gate was run.

## Advice (author lane, not outside admission)

1. Harness: decode child output with `errors='backslashreplace'`, and convert exceptions in `run()` into a named `observe()` record. Reserve exit 2 for setup. Today a crash surfaces as exit 1 "mismatch" with no record.
2. Keep the en_US half. Relabel the C half as sanity, or pair it with a discriminating case.
3. Persist entry-side Unicode-date controls (verified-at, recheck date, recheck cadence).
4. Locale precondition: skip with a named reason, as the gate's own `metadata-asof-unicode-date-locale` does, or document the en_US.UTF-8 requirement.
5. Use exit plus diagnostic as the primary signal. Bash message text is version-dependent.

## Limits

- Full selftest and full regression script not run (bounds). `one_control.py` replicates the single row's argv, env, cwd, and expectations. "Later controls not evaluated" is from reading code order, not from a full run.
- Locales present here: C, C.utf8, en_US.utf8, POSIX. Other real locales, where `[0-9]` loosens, could not be tested.
- Crash depends on bash 5.3.20 emitting raw partial bytes and on Python decoding child stderr as strict UTF-8 (parent encoding here: UTF-8).
- C3 out of scope. The reported baseline failures were not rerun.

## Tooling

No installs or updates. Used: GNU bash 5.3.20, Python 3.14.8, `git archive`, `diff`, `sha256sum` (all system). Sandbox-only helpers: `one_control.py`, `bytes_probe.py`, `matrix.py`, `entry_probe.py`, `stderr_dump.py`, `date_sweep.py`.

Report path (relative to lane root): `.ufo/waves/round-27/falsify/FC2AsciiCliEnUsUtf820261026.md`
