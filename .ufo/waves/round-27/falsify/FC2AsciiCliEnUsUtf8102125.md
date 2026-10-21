# FC2 — ascii-cli-en_US.UTF-8-٢٠٢٦-10-21 (round 27 attempt 1, falsify)

Item attacked: C2 control `ascii-cli-en_US.UTF-8-٢٠٢٦-10-21` in
`corpus/evidence/round27-regressions.py:123–129` (the whole 2-locale × 3-token
loop), against revision `dd72641e574679c4f7882dd43de072b4c8892d6f`
(`tools/research-gate.sh` sha256
`ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84`, matches the
gate digest given). Sandbox: `/tmp/chousa-r27-falsify-FC2AsciiCliEnUsUtf8102125`
(git archive of the revision). Host: bash 5.3.20(1), python 3.14.8, glibc
locales `C`, `C.utf8`, `en_US.utf8`, `POSIX`; `LC_ALL=en_US.UTF-8` resolves.
No tools installed or updated.

## Verdict: HOLDS (not falsified in scope)

The expectation is a real contract consequence, the landed one-line fix is
causal for it, and no in-scope same-class input was found where the landed gate
is wrong. Three control weaknesses were found (stream-channel blindness,
over-rejection blindness, hardcoded-locale portability); one out-of-scope
nearby gate defect (duplicate `--as-of` last-wins) is unchanged and
control-silent.

## Q1 — is the expectation contract-derived and gate-code-independent?

Partly, and the split matters.

- Behavior expected (exit 2, `--as-of must be a valid YYYY-MM-DD date`, zero
  anchored `^RESEARCH_GATE: ` lines) follows the declared material:
  `corpus/evidence/round27-claims.md:11` ("Date grammar is ASCII YYYY-MM-DD
  under any inherited locale"), spec v1 in
  `corpus/evidence/round26-claims.md:58–62` ("an absent or calendar-invalid
  value exits 2"), and the accepted failure receipt
  `.ufo/waves/round-26/falsify/FDateAsOfUsage.md:133` ("rc=2, empty stdout, no
  verdict line, and the exact message"). The script does not import or parse
  the gate's date implementation for these cases; the fixture uses only the CLI
  and Python-side expectations. In that sense it is independent of the *fix*.
- The literal diagnostic is copied from the gate interface
  (`tools/research-gate.sh:6575`, identical at base `:6297`), as is exit code 2.
  A contract-correct gate that reworded the diagnostic would fail this control;
  so it is coupled to shipped wording, not fully code-independent.
- Strictly, spec v1's "exits 2" clause names absent/calendar-invalid values;
  the control extends it to non-ASCII grammar, which is what C2's ASCII clause
  and the r26 advice ("add one non-ASCII-digit usage case") require, but it is
  an extension of the written clause, not verbatim derivation.
- One genuine hazard the control does model correctly: base `metadata_iso_date`
  (`:2295–2298`) matches `[0-9]` under `en_US.UTF-8` (glibc range collation),
  then Bash arithmetic `10#…` rejects the non-ASCII digits. Independently
  reproduced: `LC_ALL=en_US.UTF-8 bash -c '[[ ٢٠٢٦-10-21 =~ ^([0-9]{4})-([0-9]{2})-([0-9]{2})$ ]]'`
  matches; under `C`/`C.utf8` it does not.

## Q2 — mutation of the targeted fix

Named control verdict on the landed gate: all six loop cases PASS, rc 0
(scoped reproduction `mini_control.py`, mirroring `observe()`/`run()` exactly:
same fixture, `CHOUSA_STRICT=0`, `LC_ALL` override, same required/forbidden/
counts; it is not the whole regression script).

```
$ python3 mini_control.py tools/research-gate.sh
PASS C ２０２６-10-21 ... PASS en_US.UTF-8 ٢٠٢٦-10-21
(6/6 PASS, exit 0)
$ LC_ALL=en_US.UTF-8 bash tools/research-gate.sh verify-metadata entry.md --root . --as-of '٢٠٢٦-10-21'
rc=2 stdout_bytes=0 stderr="research-gate: --as-of must be a valid YYYY-MM-DD date" (1×)
```

Mutation (only delta, one line removed):

```
--- tools/research-gate.sh
+++ mutant-iso-no-lc.sh
@@ metadata_iso_date() {
-  local LC_ALL=C
   [[ $1 =~ ^([0-9]{4})-([0-9]{2})-([0-9]{2})$ ]] || return 1
```

Result (rc 0 from the harness itself because it counts FAILs rather than
aborting; the FAILs are the control failures):

```
$ python3 mini_control.py mutant-iso-no-lc.sh
PASS C (3/3)
FAIL en_US.UTF-8 ２０２６-10-21 :: exit 1 != 2; missing diagnostic; forbidden 'invalid integer'
   line 2312: 10#: invalid integer constant ... ; line 2574: 10#: invalid integer constant ...
FAIL en_US.UTF-8 ٢٠٢٦-10-21 :: exit 1 != 2; missing diagnostic; forbidden 'invalid integer'
FAIL en_US.UTF-8 2026-10-2１ :: exit 1 != 2; missing diagnostic; forbidden 'arithmetic syntax'
```

The unpatched base gate (`64eec5d…`) behaves identically (C trio PASS, three
en_US FAILs, exit 1 with the same two raw Bash diagnostics), i.e. the mutant
reproduces the accepted r26 failure. This is the intended reason (wrong exit
class + raw arithmetic diagnostics + no usage diagnostic), not a missing-file/
setup error. Cause is exactly the removed line: the CLI validation call at
`:6575` is outside `verify_metadata`'s pre-existing `local LC_ALL=C` (base
`:2539`, target `:2564`).

## Q3 — nearby same-class probes

All on the landed gate, synthetic fixture, `LC_ALL=en_US.UTF-8` unless noted;
each was a single gate command (≤60 s), no suite run.

Rejected correctly (rc 2, usage diagnostic, 0 verdict lines; target stdout
empty, diagnostic on stderr):
- Digit classes: `߂߀߂߆-10-21` (NKo), `𝟐𝟎𝟐𝟔-10-21` (math bold),
  `२०२६-10-21` (Devanagari), `²026-10-21`, `2026-10-2¹`, `٢٠٢٦-١٠-٢١`
  (Arabic month/day too) — all rc 2.
- Locale inheritance: `LANG=en_US.UTF-8` only, `LC_CTYPE=en_US.UTF-8` only,
  `LC_ALL=en_US.UTF-8`, `LC_ALL=C.utf8` — all rc 2.
- Shape-adjacent ASCII: newline-, CR-, space-, tab-padded, leading space,
  U+2010 hyphen — all rc 2.
- Entry-side metadata (same class, other surface): `verified-at:` with
  Arabic/fullwidth/mixed Unicode digits and `recheck: ٢٠d` /
  `recheck: ２０２６-12-31` give byte-identical META/FINDING/verdict lines under
  `C` and `en_US.UTF-8` on both base and target, because `verify_metadata`
  already scoped `LC_ALL=C`. No residual gate wrongness found on that surface.

Defect found nearby but out of C2 scope (unchanged base→target; control
silent): duplicate `--as-of` is last-wins, so an earlier invalid non-ASCII
value is silently accepted:

```
$ LC_ALL=en_US.UTF-8 bash tools/research-gate.sh verify-metadata entry.md --root . \
    --as-of '٢٠٢٦-10-21' --as-of 2026-10-21    -> rc=0 RESEARCH_GATE: CLEAN
$ ... --as-of 2026-02-30 --as-of 2026-10-21    -> rc=0 RESEARCH_GATE: CLEAN
```

Same rc 0 under `LC_ALL=C`; the ASCII-invalid first value behaves identically,
so this is the duplicate-flag convention/spec gap already reported as F2 in
`.ufo/waves/round-26/falsify/FDateAsOfUsage.md:111–122`, not a locale-class
repair hole. No control in the 58 exercises repeated `--as-of`.

Control weaknesses (each reproduced with a sandbox mutant, landing gate
otherwise unchanged):

1. **Stream-channel blindness.** `observe()` merges `stdout + stderr`
   (`round27-regressions.py:32`). Mutating `die_usage` to print the diagnostic
   on stdout (`390: … >&2` removed) yields all six named cases PASS, while the
   gate now violates "setup keeps stdout empty and diagnostics on stderr"
   (`corpus/knowledge/claim-verification-r2.md:80`; r26 receipt
   `FDateAsOfUsage.md:133`). Direct check on the mutant: rc 2,
   `stdout_first='research-gate: --as-of must be a valid YYYY-MM-DD date'`.
   The landed gate itself is correct (stdout 0 bytes). This affects every
   `observe()` case, not only this control.
2. **Over-rejection blindness.** A mutant whose `metadata_iso_date` starts with
   `return 1` passes all six named cases; valid `--as-of 2026-10-21` then exits
   2 instead of printing `due=2026-04-02 …`. The named control alone cannot
   distinguish "rejects non-ASCII" from "rejects every date"; only the suite's
   positive date cases catch it. Related: the C-locale half of the loop is
   vacuous w.r.t. this fix — those three cases PASS on the unpatched base gate
   (proved above), so just the three `en_US.UTF-8` cases discriminate.
3. **Hardcoded locale availability.** `en_US.UTF-8` is assumed installed.
   Where absent, Bash prints `warning: setlocale: LC_ALL: cannot change locale
   (en_US.UTF-8)` (mechanism shown with `en_GB.UTF-8` on this host: warning,
   continued) and the control's forbidden `'cannot change locale'` turns a
   skipped precondition into a false FAIL, whereas the shipped selftest probes
   `locale -a` and records a skip (`tools/research-gate.sh:6308–6330`).

## Limits

- Per bounds, the full `--selftest` and the 58-case regression script were not
  run (L1 owns them). The named control was reproduced only through
  `mini_control.py`, which mirrors the script's fixture/`env`/`observe` for
  that loop; all other probes were direct single gate commands.
- Verified against bash 5.3.20 + glibc `en_US.utf8` on this host; other bash
  builds/locales were not available and were not simulated beyond the missing-
  locale warning check. No network, secret, live-process, debugger, namespace
  or host-file probes were used; fixtures are synthetic and sandboxed.
- Mutation evidence covers the exact added line in `metadata_iso_date`; the
  other two C2 hunks (`metadata_add_days`) are not exercised by this control
  because the CLI validation rejects the token before cadence parsing.

Report path (relative to lane root):
`.ufo/waves/round-27/falsify/FC2AsciiCliEnUsUtf8102125.md`
