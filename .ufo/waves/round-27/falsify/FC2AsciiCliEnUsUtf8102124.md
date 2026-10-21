# FC2AsciiCliEnUsUtf8102124: falsification of C2 control `ascii-cli-en_US.UTF-8-２０２６-10-21`

Scope: chousa round27 attempt1, pinned revision `dd72641e574679c4f7882dd43de072b4c8892d6f`.
Gate `tools/research-gate.sh` sha256 `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84` (matches the claim).
Control under attack: `corpus/evidence/round27-regressions.py:123-128` (locale `en_US.UTF-8`, token `２０２６-10-21`, expects exit 2, usage message, zero `^RESEARCH_GATE: ` lines).
Sandbox: `/tmp/chousa-r27-falsify-FC2AsciiCliEnUsUtf8102124` (git archive of dd72641e). Mutants `-M1`, `-M2`, `-M3`, `-M8` are single-edit copies of it. `-base` (archive of 64eec5d4) was used only for `diff`; its gate was never executed. No lane file, index, or git state was modified.

## Verdict

**FALSIFIED (narrow). The control discriminates the one mechanism it targets, but it is not an adequate guard of the C2 locale contract.**

- HOLDS: reverting the landed locale pin in `metadata_iso_date` (M1) fails the control on two of three en_US tokens with exit 1, the usage diagnostic missing, and a bash `invalid integer constant` error. That is acceptance followed by arithmetic failure, not a setup error.
- FALSIFIED: three mutants that violate the declared contract all pass this control:
  - M2 refuses every `--as-of` under en_US (CE-1).
  - M3 un-pins verified-at and recheck parsing; a fullwidth verified-at becomes `RESEARCH_GATE: CLEAN` (CE-2, CE-3).
  - M8 pins only when `LC_ALL` is set, so LANG-only inheritance is unpinned (CE-4).
- Third token on M1 (`2026-10-2１`) produces no recorded mismatch. The harness raises `UnicodeDecodeError` (CE-5).
- Suite-level inference: I did not run the regression script or the selftest. "M2, M3, M8 pass the whole suite" is inferred from code (every other `run()` uses `LC_ALL=C`, regressions line 60 default and line 28) plus the replicated en_US control runs below.

## Axes (judged: operability, freshness, calibration)

- operability: no landed defect found. M2 breaks valid en_US dates, and this control cannot see it (CE-1).
- freshness: no landed defect found. M3 turns a non-ASCII `verified-at` into `dated` and `CLEAN`, with `freshness=unknown` not flagged (CE-2).
- calibration: the control detects only the pinned mechanism. The C-locale twins never discriminate. Sensitivity depends on host glibc collation with no precondition assertion (CE-6). The LANG-only path is never exercised (CE-4). Token 3 crashes the harness (CE-5).

## Q1: is the expectation derived from the declared contract, independent of gate code?

Partly.

| expectation | source | derived from contract? |
|---|---|---|
| exit 2 | gate header `Exit: 2 setup/usage`; C1 "without changing expected exit2" | yes |
| zero `^RESEARCH_GATE: ` lines | C1 "actual CLEAN/DRIFT verdict fails" | yes |
| Unicode-digit date rejected | C2 "Date grammar is ASCII YYYY-MM-DD under any inherited locale" | yes |
| `--as-of must be a valid YYYY-MM-DD date` | copied from gate line 6575 `die_usage`; not in claims | coupled to gate text (substring check) |
| forbidden `invalid integer`, `arithmetic syntax`, `cannot change locale` | bash diagnostics chosen by the author | symptom list, not contract |
| `en_US.UTF-8` admits non-ASCII digits under `[0-9]` | host glibc collation data | environment precondition, not asserted |

## Q2: does reverting the targeted fix make the control fail for the intended reason?

Targeted fix: `diff` hunk `2295a2311 > local LC_ALL=C`. Base `metadata_iso_date` (line 2295) had no pin; landed adds it at line 2311. M1 removes that line (`CUT 2311.=2311`).

Replica: same argv (`bash <gate> verify-metadata <entry> --root <root> --as-of <tok>`), cwd, environment (`os.environ` minus `CHOUSA_*`, plus `CHOUSA_STRICT=0` and `LC_ALL=<locale>`), `timeout=60`, `text=True, capture_output=True`, and the same entry text as `entry_text()`. This is one control replicated, not the regression script.

| variant | locale | token | rc | control result |
|---|---|---|---|---|
| landed | en_US.UTF-8 | `２０２６-10-21` | 2 | PASS |
| landed | C | `２０２６-10-21` | 2 | PASS |
| landed | en_US.UTF-8 | `２０２６-10-21` (LANG-only env) | 2 | PASS |
| M1 | en_US.UTF-8 | `２０２６-10-21` | 1 | FAIL: `exit 1 != 2`; usage message missing; forbidden `invalid integer`. stderr: `line 2312: 10#: invalid integer constant`, `line 2574: 10#: invalid integer constant` |
| M1 | en_US.UTF-8 | `٢٠٢٦-10-21` | 1 | FAIL, same class |
| M1 | en_US.UTF-8 | `2026-10-2１` | 1 | harness `UnicodeDecodeError` (CE-5) |
| M1 | C | all three tokens | 2 | PASS (twins never discriminate) |
| M1 | en_US.UTF-8 (LANG-only env) | `２０２６-10-21` | 1 | FAIL, same class |

Bash probe (bash 5.3.20). Under `LC_ALL=en_US.UTF-8`, plain `[[ $1 =~ ^([0-9]{4})-([0-9]{2})-([0-9]{2})$ ]]` accepts all 10 non-ASCII-digit inputs tried (fullwidth, Arabic-Indic, Devanagari, Thai, superscript one, mathematical bold, and mixed forms). Inside a function with `local LC_ALL=C` it rejects them, and the locale is restored on return. The targeted fix works as described.

## Q3: counterexamples and nearby classes

Each counterexample is a sandbox mutant. "Landed" is the unchanged gate.

**CE-1: over-rejection passes the control (M2).** Insert before line 2311: `if [[ ${LC_ALL-} == en_US* ]]; then return 1; fi`.
- Control token `２０２６-10-21`, en_US: rc 2, usage message, no verdict. PASS.
- Valid `--as-of 2026-10-21`, en_US: rc 2 with usage message. Landed and C give rc 1 with a verdict. The valid date is wrongly refused under the host's default locale.
- The suite has no positive en_US date case. Regressions line 123 is the only en_US use, and every other `run()` takes the default `locale='C'` (line 60).

**CE-2: verified-at leak to CLEAN (M3).** Delete `local LC_ALL=C` at `verify_metadata` line 2564.
- entry `verified-at: ２０２６-01-02 checked…`, en_US, plain: landed `verified_at=undated`, `RESEARCH_GATE: DRIFT`, rc 1. M3 `verified_at=dated`, `RESEARCH_GATE: CLEAN`, rc 0.
- Same with `--as-of 2026-10-21`: M3 gives CLEAN with `due=unknown freshness=unknown`. Landed gives DRIFT.
- entry `verified-at: \u3000` (ideographic space) followed by `2026-01-02`, en_US: landed undated; M3 dated. Under C both undated.
- Control replica on M3: PASS.

**CE-3: recheck leak (M3).** `recheck: ２０d`, en_US: landed `recheck=unscheduled` (plain and `--as-of`, both locales). M3 `recheck=scheduled` under en_US only. C unchanged. This path does not go through `--as-of`.

**CE-4: inheritance-channel blind spot (M8).** Replace line 2311 with `if [[ -n ${LC_ALL-} ]]; then local LC_ALL=C; fi`.
- `LC_ALL=en_US.UTF-8`: control PASS.
- LANG-only (`LANG=en_US.UTF-8`, `LC_ALL` unset, which is this sandbox's environment): FAIL, rc 1, `line 2313: 10#: invalid integer constant`. Landed PASS in both modes.
- Every suite control sets `LC_ALL` explicitly (regressions lines 28, 64, 91, 220), so LANG-only is never exercised.

**CE-5: harness crash instead of a recorded mismatch (M1, token `2026-10-2１`, en_US).** Gate stderr on M1: `line 2313: 10#2\xef\xbc\x91: arithmetic syntax error` and `line 2574: 10#2\xef: arithmetic syntax error`. The second line is a truncated UTF-8 sequence from the byte-sliced `${AS_OF_ARG:8:2}` under the pinned verify path. `subprocess.run(..., text=True)` in `run()` raises `UnicodeDecodeError` at byte 265. `run()` catches only `TimeoutExpired` (lines 66-67), so the script aborts before the summary and writes no JSON. Every later control is lost. Exit is nonzero, so the regression is detected, but not as this control's recorded MISMATCH. The control's own forbidden `arithmetic syntax` would have fired (`rc=1`, `usage_msg=False`) had the bytes decoded.

**CE-6: host-data dependence (M1 with `LC_ALL=C.UTF-8`).** Control PASS (rc 2), landed PASS. On this host, en_US `[0-9]` matched the 0–8 non-ASCII digit variants tried (fullwidth, Arabic-Indic, Devanagari, Thai, superscript one, mathematical bold), but not U+FF19 `９` or U+0669 `٩`. The control has no precondition check. On a host whose en_US `[0-9]` admits no non-ASCII digit it would pass vacuously. The selftest probe (`round27` gate lines 6307-6326) checks this but skips rather than fails.

**Landed gate: no counterexample found.** Checked in C, en_US (`LC_ALL`), and LANG-only:
- all 10 non-ASCII-digit `--as-of` variants give rc 2 with usage message;
- accepted: `2026-10-21`, `2028-02-29`, `9999-12-31`. Refused: `0000-01-01`, `10000-01-01`, `2026-02-29`, `2026-10-21 ` (trailing space), and a trailing `\n`;
- calendar sweep of 13 dates, including `2100-02-29`, `0001-01-01`, `0000-12-31`: 0 mismatches in both en_US inheritance modes;
- verified-at and recheck classes (fullwidth, Arabic, U+3000 lead, `９０d`, `٩٠d`, `２０d`, `２０２６-10`): identical across C and en_US.
- Design note, not a defect: an invalid recheck is info-level `unscheduled`, so a run can be CLEAN with `freshness=unknown` under the STRICT=0 policy.

## Recommendations (author lane; not applied)

Each change adds coverage and harms no existing case:
1. Add a positive en_US control: `--as-of 2026-10-21` must produce a verdict, not usage. Catches CE-1.
2. Add en_US field fixtures: `verified-at` with fullwidth digits and a U+3000 lead, and `recheck: ２０d`, expecting undated and unscheduled. Catches CE-2 and CE-3.
3. Add a LANG-only variant with `LC_ALL` unset. Catches CE-4.
4. Decode harness output with `errors='replace'` or from bytes, and record decode failure as a MISMATCH. Fixes CE-5.
5. Assert the locale precondition: fail, not silently pass, if the chosen locale admits none of the tokens. Fixes CE-6.

## Commands and results (summary)

- `git -C <lane> archive dd72641e… | tar -x -C <sandbox>`; `sha256sum tools/research-gate.sh` → `ca39d14d…` (match).
- `git -C <lane> archive 64eec5d4… | tar -x -C <sandbox>-base`; `diff` only.
- Mutants: `cp -a` to `-M1`, `-M2`, `-M3`, `-M8`. Edits: M1 `CUT 2311.=2311`; M2 guard before 2311; M3 `CUT 2564.=2564`; M8 scoped pin at 2311.
- Gate invocations: about 160 single `bash <gate> verify-metadata …` calls on sandbox copies, each well under 60 s, plus bash probes. Not run: full `--selftest`, the whole regression script, the base gate (baseline failures not rerun), network, live processes.
- Environment inspected only for `CHOUSA_*`, `LC_*`, `LANG`. `locale -a`: `C`, `C.utf8`, `en_US.utf8`, `POSIX`.

## Limits

- Tools: none installed or updated. Host bash 5.3.20(1)-release, glibc 2.44, Python 3.14 used as-is. `RULES.md` read.
- Host-specific: glibc collation results and the UTF-8 decode crash were observed on this host only. I did not test other hosts.
- Suite-level invisibility of M2, M3, M8 is inferred from code, not from a full run.
- Author-lane advice only; not an outside admission.

Report: .ufo/waves/round-27/falsify/FC2AsciiCliEnUsUtf8102124.md

## Addendum: accuracy corrections (append-only)

- Replica timeout: the replica used `timeout=60`; the harness `run()` uses `timeout=30` (regressions line 65). No run approached either limit; all completed in under a second.
- CE-4 message: the M8 LANG-only failure matched forbidden token `invalid integer` at gate line 2313. The full bash message text was not captured, so `10#: invalid integer constant` is inferred from the M1 message on the same code path.
- CE-6 digit coverage: non-ASCII variants of 0, 1, 2, and 6 matched `[0-9]` under en_US; variants of 9 (U+FF19, U+0669) did not; variants of 3, 4, 5, 7, and 8 were not tested. Read "0–8 variants tried" in CE-6 as "0, 1, 2, and 6 variants tried".
- Q2 wording: "fails the control on two of three en_US tokens" is accurate; the third token crashes the harness instead (CE-5).
