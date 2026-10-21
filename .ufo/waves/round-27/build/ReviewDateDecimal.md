# ReviewDateDecimal — C2 leading-zero normalization

**Axes:** freshness (target), calibration (preserve numeric/range semantics), operability (no verdict-path change in scope).

## Findings

No actionable defect found in the scoped decimal-normalization diff in `.ufo/waves/round-27/work/ExecDates/tools/research-gate.sh:2344-2362`. It validates decimal text, captures the significant suffix with `^0*([0-9]*)$`, maps an empty suffix to `0`, then applies the seven-digit bound and decimal arithmetic. Thus normalization precedes the magnitude bound and removes the former `+(0)` extglob expansion identified in `.ufo/waves/round-26/falsify/FDateHugeCadence.md:34-44`. The existing bounded-date check still returns failure for out-of-range additions; the caller at `.../research-gate.sh:2742-2753` consequently retains `due=unknown freshness=unknown`.

The diff adds synthetic 128-KiB leading-zero `90d` and all-zero cadence selftest cases at `.../research-gate.sh:6128-6139`. The contract and preserved range expectations are in `corpus/evidence/round27-claims.md:9-11` and `.ufo/waves/round-26/falsify/FDateHugeCadence.md:120-153`.

## Concrete acceptance oracle

On isolated synthetic entries, compare exact `due`/`freshness`, expected exit, and overdue finding:

- 128-KiB zero prefix + `90d`, verified `2026-01-02`, as-of `2026-10-21` → `due=2026-04-02 freshness=overdue`, `META_RECHECK_OVERDUE`, exit 1.
- 128-KiB all-zero prefix + `0d`, verified/as-of `2026-01-02` → `due=2026-01-02 freshness=current`, exit 0.
- 128-KiB zero prefix + `3652058d` from `0001-01-01` → `due=9999-12-31 freshness=current` at that as-of, exit 0; `3652059d` → `due=unknown freshness=unknown`, exit 0. This checks that normalization precedes the length bound without allowing overflow.

## Residual risk and verification gaps

Static review only; no selftest, regression suite, differential, build, or runtime probe was run, per assignment. No LSP device/server is mounted (`xd://lsp` returned “No such tool”), so references/definition/diagnostics were unavailable; no grep output is offered as semantic proof. The executor diff's own 128-KiB cases are present but unexecuted; the exact max-span/overflow oracle above remains for L1's final verification.