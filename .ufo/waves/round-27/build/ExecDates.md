# ExecDates — round 27 C2

**Assigned scope:** date-input locale and decimal-cadence normalization only. Working clone was created at `64eec5d41c7cf7f17f5ce1e968e28b3769952596` under `.ufo/waves/round-27/work/ExecDates`.

## Retained evidence

- `.ufo/waves/round-26/falsify/FDateHugeCadence.md:34-53` reports the existing extglob zero-strip terminating with SIGSEGV for long zero prefixes; `:103-117` records a one-pass regex candidate handling 256 KiB.
- `.ufo/waves/round-26/falsify/FDateAsOfUsage.md:7-12,75-86` reports locale-expanded `[0-9]` accepting Unicode digits under `en_US.UTF-8`, followed by Bash arithmetic diagnostics and exit 1 instead of usage exit 2.
- `.ufo/waves/round-27/corpus/evidence/round27-claims.md:9-11` requires ASCII dates, stack-safe leading-zero cadence handling, unknown for out-of-range values, and preservation of date bounds/overdue semantics.

## Scoped change

Patch: `.ufo/waves/round-27/patches/ExecDates.patch` (only `tools/research-gate.sh`). `metadata_iso_date` and `metadata_add_days` now pin `LC_ALL=C`. Decimal normalization validates ASCII digits and captures the complete nonzero significant suffix in one anchored ERE; the empty capture maps to zero. The existing significant-length guard remains before base-10 arithmetic, followed by the remaining-calendar-span check. Thus significant values above the safe digit bound, and additions beyond 9999-12-31, still produce unknown rather than wrapping or evaluating an oversized value.

New selftest calls are appended after the original final case 187. They cover a generated 128 KiB zero prefix plus value 90 (`2026-04-02`, overdue at the selected as-of date), the same input in plain mode (scheduled/clean, one anchored verdict, complete count, and no `due=`/`freshness=` fields), and a 128 KiB all-zero cadence. The Unicode-date test uses the existing `metadata_asof_usage_case` under an installed locale whose Bash regex accepts the fullwidth digits; it reports the chosen locale, counts a skip if no such locale exists, and always runs a separate `LC_ALL=C` control. Case names are stable. The existing large-cadence and date-overflow expectations are unchanged.

## Risks and unrun work

- The locale-specific branch is explicitly skipped if no installed locale exhibits the inherited Unicode-digit match; the C control still runs. The independent persisted locale regression remains for L1's final suite.
- The Unicode control delegates to the shared usage helper, so it relies on the separate C1 fix to that helper being integrated; this patch does not edit the C1 helper.
- No selftest, regression suite, date differential, build, lint, or formatter was run, as assigned. L1 owns post-integration verification. No tools were installed. Bash LSP was unavailable in the mounted toolset; source navigation used local read/search tools.
