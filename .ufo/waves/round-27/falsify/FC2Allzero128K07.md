# FC2Allzero128K07 — C2 `allzero-128k`

## Scope and verdict

- Revision: `dd72641e574679c4f7882dd43de072b4c8892d6f` (lane `chousa-shokunin`, master), extracted with
  `git archive` into `/tmp/chousa-r27-falsify-FC2Allzero128K07`; lane files were not edited.
- Gate SHA-256 `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84`
  (`tools/research-gate.sh`); control SHA-256 `5afea7863f2b052ba54a46cf2faf88f863d76c61d3d2cf45e091f92bc526a5df`
  (`corpus/evidence/round27-regressions.py`). Base for mutation: `64eec5d4…:tools/research-gate.sh`, SHA-256 `c2c813f1…`.
- Axes: **freshness** (cadence → due), **operability** (bounded real CLI execution), **calibration**
  (does the control discriminate the landed repair).
- **HOLDS for the named control.** Its expectation is derived from the C2 contract, not gate code; the
  control is non-vacuous (SIGSEGV when the targeted normalization is reverted, semantic mismatch on three
  other mutants); 70/70 nearby same-class differential cases match Python-computed expectations.
- **Nearest falsification is scale, not semantics:** the *identical* control with a 4 MiB zero run fails
  (`exit 124 != 0`, control exit 1) because the judge's own 30 s timeout fires. Run without that harness
  timeout, the gate eventually prints the contract-correct record in 64.7 s. The cost is the pre-existing
  quadratic CR strip `line=${line%$'\r'}` (identical statement in base), generic to any long line, not the
  C2 cadence fix. The 128 KiB fixture sits below that knee.

## 1. Is the expectation contract-derived and independent of gate code?

**Yes.** C2 (`corpus/evidence/round27-claims.md`) requires: "A long decimal cadence with leading zeros must
compute its representable value without termination; out-of-range values remain unknown", plus preserved
year 1–9999 calendar arithmetic and "strict as-of>due" overdue semantics.

The control tuple is `corpus/evidence/round27-regressions.py:97-98`:

```python
('leading-128k-zeros', '2026-01-02', '0' * 131072 + '90d', '2026-10-21', '2026-04-02'),
('allzero-128k',       '2026-01-02', '0' * 131072 + 'd',  '2026-01-02', '2026-01-02'),
```

Derivation for `allzero-128k`, independent of the gate:

- Numeric value of 131 072 ASCII zeros is 0; 0 is representable, so due = `2026-01-02 + 0 days = 2026-01-02`.
- as-of is exactly due; the declared predicate is overdue iff as-of is **strictly** later, so freshness = `current`.
- The entry has source, a dated verified-at and a scheduled recheck, no registry, so the declared verdict is
  clean and the process exit is 0.
- The `due` literal is hardcoded in the control (not read from the gate); freshness is computed with Python
  `date.fromisoformat(asof) > date.fromisoformat(due)`; `observe` additionally requires one anchored
  `^RESEARCH_GATE: ` record and one `^META entry=` line, and `run()` rejects on exit mismatch.

I re-used only `observe` (lines 26–42), `entry_text`/`run` (57–67) and the one date tuple, in a standalone
`control_allzero.py`; the full regression script and the full selftest were not executed. The expectation is
*single-sided* (many wrong gates could pass this one case, e.g. "treat any cadence as 0"), but within the
persisted suite the paired `leading-128k-zeros` case (value 90 → `2026-04-02`) removes that vacuity.

## 2. Revert/mutate the targeted production fix — does the control fail for the intended reason?

Landed vs base `metadata_add_days` changes only normalization (plus `local LC_ALL=C`):

```diff
-  [[ $digits =~ ^[0-9]+$ ]] || return 1
+  [[ $digits =~ ^[0123456789]+$ ]] || return 1
-  digits=${digits##+(0)}
+  # Capture the significant suffix in one ERE pass; extglob recurses on long zero runs.
+  [[ $digits =~ ^0*([123456789][0123456789]*)?$ ]] || return 1
+  digits=${BASH_REMATCH[1]:-}
   [[ -n $digits ]] || digits=0
```

`extglob` is enabled at line 256 in both gates. Mutants are full sandbox copies differing only in the
statement(s) noted; the detector is the faithful one-case extraction of `observe`.

| Gate | Difference | Gate rc on control fixture | Control verdict |
|---|---|---|---|
| landed `lane/tools/research-gate.sh` | — | 0 (`due=2026-01-02 freshness=current`) | exit 0, PASS |
| `base-gate.sh` (`64eec5d4`) | pre-fix function | **-11 (SIGSEGV)** | exit 1: `exit -11 != 0`, token missing, both counts 0 |
| `mut-base-extglob.sh` | only the two normalization lines reverted to base | **-11 (SIGSEGV)** | exit 1: same errors |
| `mut-empty-unknown.sh` | empty significant suffix → `return 1` instead of `0` | 0 but `due=unknown freshness=unknown` | exit 1: missing `due=2026-01-02 freshness=current` only |
| `mut-no-empty-default.sh` | drop `[[ -n $digits ]] \|\| digits=0` | 1, no META/verdict output (`10#` invalid integer aborts) | exit 1: exit mismatch + missing token + counts 0 |
| `mut-no-normalize.sh` | delete the ERE+strip entirely | 0 but `due=unknown freshness=unknown` | exit 1: missing due token |

Exact reproduction (sandbox), all exit codes observed:

```sh
python3 control_allzero.py lane/tools/research-gate.sh   # exit 0
python3 control_allzero.py base-gate.sh                  # exit 1; gate rc -11
python3 control_allzero.py mut-base-extglob.sh           # exit 1; gate rc -11
python3 control_allzero.py mut-empty-unknown.sh          # exit 1; missing token only
```

The base failure is the intended class (abnormal termination on a long zero run while computing the cadence),
not a parse/setup error: the entry is accepted (no usage/refusal finding; the gate emits no parse diagnostic),
and the minimal two-line mutant reproduces the signal. The empty-suffix mutants show the control also pins
`[[ -n $digits ]] || digits=0` semantically rather than only by crash.

## 3. Nearby same-class inputs — wrongness / vacuity search

**Semantic differential (70 cases, Python oracle):** zero-run lengths {0, 1, 2, 7, 64, 4096, 131072} ×
verified dates {`0001-01-01`, `2026-01-02`, `9999-12-31`} × values {0, 1, 90, 2912441 (max span from
`2026-01-02`), 2912442, 3652058 (max span from year 1), 3652059}, with as-of before/equal/after due.
**0 mismatches** (due, freshness, exit, and the one-verdict/one-META counts all matched).

Additional same-class probes, all correct on the landed gate:

- max span from `2026-01-02` = 2912441 → `due=9999-12-31 freshness=current`, rc 0; 2912442 → `due=unknown freshness=unknown`, rc 0.
- `'0'*131072 + '0002912441d'` → `9999-12-31`; `'0'*131072 + '10000000d'`, `+ '9999999d'`, `+ '2912442d'` → `unknown` (out of range).
- CRLF entry with the 131 KiB zero cadence → correct; zeros interleaved with the significant digits (`0*131072 + '0000000' + 'd'`) → correct; 1, 2, 7 zeros → correct.
- as-of one day after due → `overdue`, rc 1; as-of one day before verified → `current`, rc 0 (strict `>` preserved).
- Entry > `SOURCE_READ_MAX_BYTES` (8 400 074 B, zeros cadence) → `META_ENTRY_REFUSED reason=size`, `due=refused`, rc 1 — the documented size cap, not a cadence result.

**Counterexample found (scale/operability, not wrong output):** the identical control at 4 MiB of zeros
(32× the fixture, still inside the gate's 8 MiB accepted-entry cap) fails under the control's own
`run(timeout=30)`:

```
control_allzero.py --zeros 2097152 : control-exit=0, actual_exit=0 (≈15 s)
control_allzero.py --zeros 4194304 : control-exit=1, actual_exit=124
    exit 124 != 0
    missing 'due=2026-01-02 freshness=current'
    count '^RESEARCH_GATE: ': 0 != 1
    count '^META entry=': 0 != 1
```

Without the harness timeout the same 4 MiB fixture returns the contract-correct
`due=2026-01-02 freshness=current verdict=clean` in **64.4 s child CPU** (rc 0). Gate child-CPU scaling on
the identical cadence: 128 K 0.073 s, 256 K 0.203 s, 512 K 0.665 s, 1 M 2.540 s, 2 M 13.599 s, 4 M 64.363 s.

Attribution: the cost is **not** `metadata_add_days` (isolated call: 0.062 s at 1 MiB, 0.115 s at 2 MiB; all
cadence regexes ≤0.09 s at 2 MiB). Instrumented copies place the delay between per-line markers, and a
statement benchmark isolates the quadratic operation:

```sh
line=$(head -c N /dev/zero | tr '\0' '0'); x=${line%$'\r'}   # LC_ALL=C
# 256 K 0.153 s | 512 K 0.600 s | 1 M 2.277 s | 2 M 14.611 s   (~quadratic)
```

This is the pre-existing parser statement `line=${line%$'\r'}` at base line 2411 / landed line 2657 (and the
metadata loop at 2430/2657), unchanged by C2, and it is generic: a 2 MiB **non-cadence** comment line costs
12.739 s versus 13.470 s for the 2 MiB cadence, i.e. the 128 KiB control under-samples line length rather than
the cadence path being wrong. Consequence: the C2 wording "a long decimal cadence … without termination" is
accurate for the tested size and for values at all sizes probed, but a same-class input only 32× larger
exceeds the control harness's own 30 s budget; extrapolating the measured growth, an entry near the gate's
8 MiB cap would take minutes [INFERENCE].

## Limits

- The full `--selftest` and the complete regression script were not run (L1 owns them); evidence uses the
  faithful single-case extraction plus single gate invocations and sandbox mutants.
- No debugger, strace, `/proc` inspection or live-process probing; crash localization rests on the minimal
  two-line mutant and the identical base gate.
- Timing was taken on a heavily loaded host (many concurrent peer agents); scaling used child CPU from
  `RUSAGE_CHILDREN`, and ratios (≈4–5× per doubling) are stable across both the gate and the isolated
  statement benchmark. The 8 MiB runtime is extrapolated, not measured.
- Mid-run the host `/tmp` filesystem hit 100% (peer sandboxes); one 4 MiB fixture write failed with
  `ENOSPC`. I removed only my own fixtures and re-ran: the 2 MiB control pass and the 4 MiB timeout were
  reconfirmed after cleanup. No production or sibling files were touched.
- No tools were installed or updated.

Author-lane advice (not an outside-admission verdict): the C2 `allzero-128k` control is contract-valid and
mutation-sensitive; if the "long cadence" claim is meant to cover multi-MiB inputs, the pre-existing
quadratic CR strip should be made byte-bounded (e.g. strip only when the last byte is `\r`) or the cadence
size limit declared, and the control kept at a size where its 30 s budget is meaningful.
