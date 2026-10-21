# FC2OverflowSpan12: falsification of C2 control `overflow-span`

- Assignment: chousa round27 attempt1, falsify wave, leaf `ChousaR27.FC2OverflowSpan12-11`. No subagents, no background jobs.
- Target: landed `dd72641e574679c4f7882dd43de072b4c8892d6f`. Gate `tools/research-gate.sh` sha256 `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84` (matches assignment).
- Control: `corpus/evidence/round27-regressions.py:103` `('overflow-span', '0001-01-01', '3652059d', '9999-12-31', None)`, executed by the loop at `:112-117`. `observe` is `:31-44`; `run()` is `:60-67`, with `LC_ALL=C` and `CHOUSA_STRICT=0` from `:28`.
- Sandbox: `/tmp/chousa-r27-falsify-FC2OverflowSpan12` (`git archive dd72641e... | tar -x`). Base comparator: `/tmp/chousa-r27-falsify-FC2OverflowSpan12-base` (`git archive 64eec5d41c7cf7f17f5ce1e968e28b3769952596 tools/research-gate.sh`, sha256 `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6`).
- Lane: read-only git archive only. No lane file, index, ref, or sibling lane touched. The only lane write is this report.
- Tooling: none installed or updated. Used bash, coreutils, and the system `python3`.

## Verdict

| Question | Verdict |
|---|---|
| (1) Expectation derived from declared contract, independent of gate code? | HOLDS, with two weaknesses (section 1) |
| (2) Does the control fail for the intended reason when its targeted fault is reintroduced? | FALSIFIED as a discriminator. It passes the pre-repair base. It fails only for bound removal or +1, and then by gate abort rather than the value mismatch it names. It is blind to five other nearby faults. |
| (3) Nearby synthetic input of the same class where the landed gate is wrong? | HOLDS. 0 mismatches in a 177-invocation boundary grid and 20 targeted probes. |

Overall: **FALSIFIED (control-side vacuity)**. The landed gate **HOLDS** on this class. The defects are in what the row can detect, not in the gate's overflow arithmetic.

## 1. Is the expectation contract-derived and gate-independent?

- Contract. `corpus/evidence/round26-claims.md:67-70`: `due = V+N` days; anything else, including overflow, gives `due=unknown freshness=unknown`. `:143-147`: a cadence whose computed date falls outside 0001-01-01..9999-12-31 "yields `due=unknown freshness=unknown`; it does not terminate the process". `:71-74`: overdue (as-of strictly after due) is the only freshness-driven drift. `corpus/evidence/round27-claims.md:11`: out-of-range values remain unknown; the maximum-span and overflow controls are independently persisted.
- Oracle, Python only: `date(1,1,1)+timedelta(3652058) == 9999-12-31`; `date(1,1,1)+timedelta(3652059)` raises `OverflowError`. The control hard-codes `None`, which matches.
- rc expectation. The control computes `int(freshness == 'overdue')`, which is 0. This follows from `:71-74` (only overdue drifts) and the non-termination clause at `:147`. The spec never states the verdict for unknown in words, so "unknown implies clean" is `[INFERENCE]`. It agrees with the gate's own selftest at `tools/research-gate.sh:6156-6164`, but that selftest is gate-authored, not independent.
- Weakness A: the row does not pin `recheck=scheduled`. `<N>d` is scheduled under the existing rule, and `round26-claims.md:61` requires plain output to stay byte-identical to base. Mutant F2 (section 2) exploits this.
- Weakness B: `required` is substring-only and there is no `forbidden` entry for abort or bash-error text. An abort is reported only as `exit 1 != 0; missing ...`, with no diagnosis.
- Weakness C: `run()` forces `LC_ALL=C`, so this row never exercises inherited-locale behaviour. Section 3a shows the landed gate handles that neighbour correctly.

## 2. Reintroduce the targeted fault in sandbox copies

The row guards the start-relative range bound `((amount <= last_day - start)) || return 1`. It is at landed `tools/research-gate.sh:2376` and base `:2357`. The r27 repair did not change this line. Reverting the repair therefore cannot make this row fail. Confirmed: the base passes (section 4, `base`). I then mutated the bound and its neighbours, one line per copy, using the edit tool on `mut/<X>/tools/research-gate.sh`.

| Variant | One-line edit in sandbox copy | Shipped `overflow-span` | Other shipped C2 rows that fail (of 14) | Failure reason |
|---|---|---|---|---|
| base (64eec5d) | none, pre-repair tree | PASS rc0 `due=unknown` | none | n/a |
| landed | none | PASS rc0 `due=unknown` | none | n/a |
| A | L2376 bound replaced by `:` | FAIL rc1, no META line | overflow-span, max-date-overflow | `line 2356: 10#: invalid integer constant (error token is "10#")` |
| B | L2376 `<= last_day - start + 1` | FAIL rc1, no META line | overflow-span, max-date-overflow | same abort |
| C | L2376 `<` (strict) | PASS rc0 | max-span (`due=unknown`) | n/a |
| D | L2376 `amount <= 3652058` (start-independent) | PASS rc0 | max-date-overflow (abort) | n/a |
| E | L2369 length guard replaced by `:` | PASS rc0 | huge-magnitude (abort); pow64-plus-90 (`due=2026-04-02 freshness=overdue verdict=drift`) | n/a |
| F | L2746 scheduled regex `^[0-9]{1,6}d$` | PASS rc0 (`recheck=unscheduled`) | none of 14; caught only by shipped `long-zero-plain-mode` (direct equivalent run: `recheck=unscheduled`, expected `scheduled`) | n/a |
| F2 | L2746 `^0*[0-9]{1,6}d$` (≤6 significant digits) | PASS rc0 (`recheck=unscheduled`) | none of 14; `long-zero-plain-mode` passes | only the gate's own selftest at `:6163-6164` (expects `recheck=scheduled`) |

Reading the table:

- Bound removal or +1 (A, B) is detected, but as a termination, not a value mismatch. `metadata_days_from_iso` (`:2355-2356`) slices `10000-01-01` into `10#-0`, which aborts with exit 1 and prints no META or verdict line. The rc0 and META-count expectations do capture the contract's "does not terminate" clause. The `due=10000-01-01` value the row is named for is never observed. The harness runs the exact shipped code path, so this is not a control parse or setup error.
- Blind: downward shift (C), start-independent span (D), length guard (E), and recheck classification (F, F2) all pass this row. Other rows catch C, D and E. F is caught only by the 128 KiB `long-zero-plain-mode` row, and F2 is caught only by the gate's own selftest. The independent suite has no pin on recheck state for cadences of 7 or more significant digits.

## 3. Nearby counterexamples

### 3a. Landed gate: none found (HOLDS)

- Targeted probes, 21 rows including the shipped row, all OK on landed (exit 0). Rows: `x-zero20-overflow` (20 zeros + `3652059d`), `x-zero128k-maxspan` and `x-zero128k-overflow` (128 KiB zeros + `3652058d` / `3652059d`), `x-7digit-max` (`9999999d`), `x-from2026-last` (2912441d, due 9999-12-31 current), `x-from2026-overflow` (2912442d, unknown), `x-end-minus1` (9999-12-30 + 1d), `x-end-plus2`, `x-end-zero`, `x-start-zero`, leap rows `x-leap-0004`, `x-century-0100` (0100-02-28+1 = 0100-03-01), `x-quadcent-0400`, `x-9600`, `x-9999-feb28`, `x-invalid-0100-leap`, `x-valid-0400-leap`, and Unicode cadences `x-u-fullwidth-en` / `x-u-arabic-en` under `en_US.utf8` and `x-u-fullwidth-C` under C. All three Unicode cases give `recheck=unscheduled due=unknown freshness=unknown`.
- Boundary grid against the Python oracle: years {1, 4, 100, 400, 1900, 2000, 2100, 2400, 9600, 9999} x starts {01-01, 02-28, 02-29, 12-31} (invalid starts included) x cadences {0, 365, maxspan, maxspan+1}, with as-of equal to due and, where applicable, 9999-12-31. Result: landed 177 invocations, 0 mismatches, classes current 102 / overdue 32 / unknown 43. The same grid on mutant D gives 37 mismatches, so the grid has discriminating power.
- Plain mode, `3652059d`, no as-of: base and landed META lines are byte-identical (`recheck=scheduled verdict=clean`). F2 differs.
- Shipped C2 date rows (14 of them), run as a subset: landed 0 mismatches.

### 3b. Control-side counterexamples (shipped row passes, contract or gate-authored expectation violated)

- CE-1 (recheck state, F2). Fixture `source: S001` / `verified-at: 0001-01-01 checked fixture` / `recheck: 3652059d`, with `--as-of 9999-12-31`. F2 outputs `META entry=overflow.md source=present verified_at=dated recheck=unscheduled due=unknown freshness=unknown verdict=clean`, rc0. Shipped `overflow-span` PASSES. Base and landed output `recheck=scheduled`, and `round26-claims.md:61` requires plain output to match base. The gate's selftest at `:6163-6164` expects `recheck=scheduled`, so it would fail. Under F2, all 14 shipped C2 rows and `long-zero-plain-mode` still pass.
- CE-2 (fixed span, D). Fixture `verified-at: 2026-01-02`, `recheck: 2912442d`, `--as-of 9999-12-31`. Landed: `due=unknown freshness=unknown` rc0. D: aborts with exit 1 and no META line. Shipped `overflow-span` PASSES on D, because D rejects 3652059 at every start. The row that catches D is `max-date-overflow`, which is not start-relative.
- CE-3 (downward shift, C). Fixture `verified-at: 0001-01-01`, `recheck: 3652058d`, `--as-of 9999-12-31`. Landed: `due=9999-12-31 freshness=current` rc0. C: `due=unknown`. Shipped `overflow-span` PASSES on C. Only `max-span` catches C.
- CE-4 (length guard, E). Fixture `verified-at: 2026-01-02`, `recheck: 18446744073709551706d`. E: `due=2026-04-02 freshness=overdue verdict=drift` (2^64+90 wraps to 90). Shipped `overflow-span` PASSES on E. Only `pow64-plus-90` and `huge-magnitude` catch E.

## 4. Commands and exit codes

- `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive dd72641e574679c4f7882dd43de072b4c8892d6f | tar -x -C /tmp/chousa-r27-falsify-FC2OverflowSpan12`: exit 0. Gate sha256 matches the assignment.
- `git -C ... archive 64eec5d41c7cf7f17f5ce1e968e28b3769952596 tools/research-gate.sh | tar -x -C /tmp/chousa-r27-falsify-FC2OverflowSpan12-base`: exit 0.
- Derived harness `probe/overflow_probe.py`: shipped `round27-regressions.py` lines 1-68, 95-117 and 225-236, plus `WANT`, `EXTRAS` and `SKIP_128K` env filters and 20 added rows. Its expectations come from Python `datetime`. It is not the whole regression script.
  - `WANT=overflow-span python3 overflow_probe.py --gate <gate>`: landed exit 0 (shipped row PASS plus 20 extras OK). base exit 0 (`SKIP_128K=1`). A exit 1. B exit 1. C exit 1, where the shipped row passes and the failures are extras. D exit 1, where the shipped row passes and the failures are extras. E exit 0. F exit 1, where the shipped row passes and the failure is extra `x-zero20-overflow`.
  - `WANT= EXTRAS=0` (the 14 shipped C2 date rows): landed exit 0, 0 mismatches. F2 exit 0, 0 mismatches. A and B fail overflow-span and max-date-overflow. C fails max-span. D fails max-date-overflow. E fails huge-magnitude and pow64-plus-90. F exits 0.
- Boundary sweep, Python oracle, 177 gate invocations: landed 0 mismatches. D 37 mismatches.
- Direct single-fixture runs, gate exit codes shown in brackets:
  - Gate's own large-cadence fixture (`:6156-6159`, as-of 2026-10-21): landed `recheck=scheduled due=unknown freshness=unknown verdict=clean` [0]. F2 `recheck=unscheduled ...` [0], which contradicts the `:6164` expectation.
  - 128 KiB zeros + `90d`, plain mode (equivalent to the shipped `long-zero-plain-mode` row): landed `recheck=scheduled` [0]. F `recheck=unscheduled` [0]. F2 `recheck=scheduled` [0].
  - `3652059d`, plain mode: base and landed `recheck=scheduled verdict=clean` [0]. F2 `recheck=unscheduled` [0].
  - A and B on the overflow fixture: [1] with `line 2356: 10#: invalid integer constant (error token is "10#")` on stderr and no stdout.

## 5. Residual risk, gaps, and advice to main (author-lane advice, not an admission)

- Gaps in the control, in priority order:
  1. Pin `recheck=scheduled` in `overflow-span`, `max-span` and `max-date-overflow`, and add a plain-mode row for a 7-digit cadence. This closes F2.
  2. Add a start-relative overflow row, for example `2026-01-02` + `2912442d` to unknown, so a fixed-span mutant fails a row that is not `max-date-overflow` alone.
  3. Add `forbidden=('invalid integer constant', 'error token')` so aborts are labelled as aborts.
- Latent gate fragility, not a landed defect: `metadata_days_from_iso` aborts on any year above 9999, instead of reporting unknown. Only the bound at `:2376` prevents that today.
- Not run, per bounds: the full `--selftest`, the whole regression script, the C1 and C3 rows, and network or host probes. I did not inspect `/proc`.
- Probe-authoring error, corrected before any reported result: the first probe used `--as-of 0100-02-29`, which is calendar-invalid and gave exit 2. Changed to `0100-03-01`. No gate effect.
- The sandbox mutants are named A to F and F2 above. They are not lane artifacts and are not retained in the lane.

## Errata (appended after write; append-only)

- Section 4, mutant F: that run used `WANT=` (all 14 shipped C2 date rows plus extras), not `WANT=overflow-span`. Its exit 1 comes from six extra rows that pin `recheck=scheduled` (`x-zero20-overflow`, `x-zero128k-maxspan`, `x-zero128k-overflow`, `x-7digit-max`, `x-from2026-last`, `x-from2026-overflow`). All 14 shipped C2 rows pass under F. Shipped `overflow-span` passes under F with `recheck=unscheduled`.
- Section 2, bound-removal mechanism: `metadata_days_from_iso` slices the 10-character string `10000-01-01` at fixed offsets. Month `${1:5:2}` and day `${1:8:2}` both become `-0`, so `10#-0` is an invalid integer constant (bash error token `10#`). The text "slices into `10#-0`" in section 2 is shorthand for this.
- Verdict row (2), "fails only for bound removal or +1", means among the seven mutants tested (A to F, F2). It is not an exhaustive claim.
