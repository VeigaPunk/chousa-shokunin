# ReviewDateOverflow — C2 decimal overflow

**Assigned item:** C2, decimal cadence normalization and bounds. Review only; no gate/selftest/differential was run.

## Finding

**No remaining date-helper defect identified in the inspected ExecDates work copy.** The base at `tools/research-gate.sh:2343-2358` strips leading zeroes with extglob before applying the seven-digit bound; round-26 `falsify/FDateHugeCadence.md:34-44, 46-58` records the resulting SIGSEGV/no-output failure for long zero runs. The inspected candidate at `.ufo/waves/round-27/work/ExecDates/tools/research-gate.sh:2295-2300, 2344-2362` localizes date parsing to `LC_ALL=C` and replaces recursive extglob stripping with regex capture, maps an empty significant suffix to `0`, then checks significant-digit length before arithmetic. It retains the available-span check against 9999-12-31. This ordering appears to address the overflow/termination failure while preserving decimal semantics, all-zero cadence, and exact maximum span. This is a source review, not execution evidence or integration approval.

Round-26 `falsify/FDateAsOfUsage.md:77-100` also records inherited-locale Unicode digits reaching arithmetic. The candidate's `metadata_iso_date` local `LC_ALL=C` at line 2296 appears to address that caller path as well; confirm via the existing controls, without weakening them.

## Acceptance oracle

Use only newly generated synthetic metadata fixtures. Require all of the following, with no Bash arithmetic diagnostics or signal termination:

- A cadence of 128 KiB ASCII leading zeroes followed by `90d`, verified-at `2026-01-02`, as-of `2026-10-21`: `due=2026-04-02 freshness=overdue`, overdue finding present, and normal drift exit 1. Include it alongside the existing 29-entry directory control; all entries' output must remain present.
- A 128 KiB all-zero cadence followed by `d`, verified-at `2026-10-20`, as-of `2026-10-21`: normalized value is zero; `due=2026-10-20 freshness=overdue`, overdue finding present, exit 1.
- `3652058d` from `0001-01-01` as-of `9999-12-31`: exact maximum due date `9999-12-31`, `freshness=current`, exit 0. `3652059d` from the same date: `due=unknown freshness=unknown`, exit 0. These establish maxspan inclusion and maxspan+1 rejection.
- Huge significant values (e.g. 40 nines and `18446744073709551706d`) remain `due=unknown freshness=unknown`, with no integer error or overflow/wrap.
- Under an inherited UTF-8 locale, non-ASCII date digits are rejected as usage (exit 2, no verdict); valid ASCII dates keep their existing results.

## Residual risk / verification gaps

The regex normalization was not executed here, including at the full reader-size boundary; no runtime result is claimed. Have the integration owner run the committed synthetic round-27 oracle, original date differential, and full selftest once after integration. No tools installed.