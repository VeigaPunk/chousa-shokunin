# FC2 falsify — C2 control `one-then-39-zeros` @ dd72641e

Agent: ChousaR27.FC2OneThen39Zeros09-11 (critic). Sandbox: `/tmp/chousa-r27-falsify-FC2OneThen39Zeros09` (git archive of dd72641e574679c4f7882dd43de072b4c8892d6f; gate sha256 ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84 verified). No installs. No full selftest or full regression script was run.

## Verdict

- **Gate behavior on this input class: HOLDS.** No counterexample was found on the landed gate.
- **Control as mutation evidence for the C2 fix: FALSIFIED.** The control is not vacuous as a truth statement, but it has no discriminating power:
  - It passes on the base code, with the targeted fix reverted.
  - It passes when the 7-digit length bound is removed.
  - Every mutant it does kill is also killed by `leading-128k-zeros`, so it adds no unique kills.

## (1) Is the expectation derived from the contract?

Yes, independently of the gate code. The control is `('one-then-39-zeros', '2026-01-02', '1'+'0'*39+'d', '2026-10-21', None)`, which expects `due=unknown freshness=unknown`, exit 0, one `^RESEARCH_GATE: `, and one `^META entry=`.

- 10^39 is far larger than the maximum span of 3652058 days (0001-01-01 to 9999-12-31).
- The C2 contract says "out-of-range values remain unknown".

Minor provenance nit: the script comment says "Calendar expectations derive from Python datetime", but `None` (and e.g. `leading-128k-zeros` → `2026-04-02`) are hand-written literals. Only the `leap-*` rows actually call `datetime`. The literals are correct (my oracle in `probe.py` recomputes them with `datetime`), so this is wording, not a defect.

## (2) Mutation evidence

The targeted production fix is in `metadata_add_days`. Base 64eec5d had `digits=${digits##+(0)}` (extglob, recursive on long zero runs). Landed dd72641e has:

```
[[ $digits =~ ^0*([123456789][0123456789]*)?$ ]] || return 1
digits=${BASH_REMATCH[1]:-}
```

The input starts with `1` and has no leading zeros, so it never exercises the leading-zero path the fix repairs.

Command: `timeout 120 python3 killmatrix.py tools/research-gate.sh mut/*.sh`, exit 0. It runs only the verbatim r27 C2 `date_cases` plus one extra row X, with the same predicate.

| mutant | killed by |
|---|---|
| landed | none |
| M0 revert to base `${digits##+(0)}` | leading-128k-zeros, allzero-128k |
| M1 strip all zeros `${digits//0/}` | leading-128k-zeros, **one-then-39-zeros**, max-span, overflow-span, X |
| M2 remove `(( ${#digits} <= 7 ))` | huge-magnitude, pow64-plus-90, X |
| M3 keep first significant digit only | leading-128k-zeros, huge-magnitude, **one-then-39-zeros**, pow64-plus-90, max-span, overflow-span, X |
| M4 also strip trailing zeros | leading-128k-zeros, **one-then-39-zeros**, X |
| M5 bound relaxed to 40 digits | huge-magnitude, pow64-plus-90 |
| M6 bound checked before normalizing | leading-128k-zeros, allzero-128k, max-span |

- **Under M0 (fix reverted) the control passes.** It does not fail at all, let alone for the intended reason. The real fix-targeting control, `leading-128k-zeros`, does fail for the intended reason: M0 gets SIGSEGV (rc -11, empty output, zero verdicts), while the landed gate gives rc 1 with `due=2026-04-02 freshness=overdue` and `RESEARCH_GATE: DRIFT`.
- **Under M2 (no length bound) the control still passes.** In 64-bit bash arithmetic, 10^39 wraps to 6873995514006732800, which is still positive and out of range, so the result stays `unknown` by accident. It therefore does not guard the magnitude bound either.
- **Unique kills: none.** M1, M3 and M4 are each also killed by `leading-128k-zeros`.

## (3) Nearby inputs (same class)

**Landed gate.** I ran `python3 probe.py tools/research-gate.sh` and `python3 nearby.py tools/research-gate.sh`, both exit 0, with every case matching the `datetime` oracle:

- `1000000d` → 4763-11-30 current, also with 50 leading zeros.
- `10000000d`, `1`+64 zeros, `1`+zeros+`1`, 2^63, 2^64+10, 2^64+100 → all unknown.
- `3000000d` from 0001-01-01 → 8214-09-22.
- 128K zeros + `1` + 39 zeros, and `1` + 128K zeros → unknown in 0.07 s, with no crash.
- Arabic-Indic and fullwidth `1`+39 zeros, and Arabic `90d` → `recheck=unscheduled` with identical output under `C` and `en_US.UTF-8`, in both `--as-of` and plain mode.
- ASCII `1`+39 zeros in plain mode → `recheck=scheduled verdict=clean`, with no `due=` field.

**Minimal counterexample that shows the control is vacuous.** The input `'1' + '0'*64 + 'd'` (verified 2026-01-02, as-of 2026-10-21) should give `unknown`. 10^64 ≡ 0 (mod 2^64), so with the length bound removed (M2) it wraps to 0 days and the gate reports `due=2026-01-02 freshness=overdue` with exit 1. The killmatrix shows X kills M1, M2, M3 and M4, a strict superset of what `one-then-39-zeros` kills; `pow64-plus-90` catches M2 by a different route.

## Smallest safe correction (author lane advice)

Either change the row to `'1' + '0'*64 + 'd'` (expected None), or keep the row and stop presenting it as evidence for the fix. As written it is a preservation and characterization row, not a mutation control for the C2 normalization repair, so it should not be counted as such.

- Impacted axes: calibration of the control suite (padding or false saturation), and freshness evidence strength.
- No production-gate defect was found. This is a fixable control defect, not a tradeoff.

## Limits

- Bash 5.3.20 and Python 3.14.8 only.
- Installed locales are C, C.utf8, en_US.utf8 and POSIX; no locale was found that admits Unicode digits for this path.
- The mutants are hand-picked, not exhaustive.
- The extra row X was evaluated only in the sandbox; the lane script is unmodified.
- Sandbox artifacts: `probe.py`, `killmatrix.py`, `nearby.py`, `mut/M0..M6`.
