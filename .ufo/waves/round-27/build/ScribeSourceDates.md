# ScribeSourceDates — C2 freshness

**Assigned item:** C2 date-input locale independence and decimal cadence normalization. **Axis:** freshness. This is local, read-only source analysis; no product edit or verification run was made.

## Findings and repair advice

1. **ASCII date grammar is not enforced at the outer `--as-of` validation site.** `tools/research-gate.sh:2295-2307` validates with `[0-9]`. The CLI calls `metadata_iso_date` at `:6295-6297` before entering `verify_metadata`, whose `local LC_ALL=C` is only established at `:2539`. Therefore that local locale does not protect outer argument validation. Make the helper's grammar explicitly ASCII (for example, a literal `0123456789` digit set or a function-local C locale) and add a synthetic Unicode-digit `--as-of` usage case under UTF-8 locale expecting exit 2 and no verdict. Preserve valid ASCII dates and the existing calendar checks.

   **Accepted prior receipt:** `.ufo/waves/round-26/falsify/FDateAsOfUsage.md:7-14,40-45,51-65` records that under `en_US.UTF-8`, non-ASCII digits passed the shape check and arithmetic emitted Bash diagnostics with exit 1 instead of usage exit 2. The report records `python3 harness.py` as 274 gate invocations / 6 contract failures; its locale probe observed 9/9 tested non-ASCII digit values failing under that locale. This is historical receipt evidence, not a rerun here. The receipt's tested environment was GNU Bash 5.3.20/glibc 2.44; it does not establish behavior for other locales or libc implementations.

2. **The leading-zero strip runs before its size bound and is recursive.** `metadata_add_days` uses `digits=${digits##+(0)}` at `tools/research-gate.sh:2343-2351`; the seven-digit guard is after that expansion. Replace this with non-recursive leading-zero normalization, preserve all-zero input as decimal `0`, then retain the pre-arithmetic bound and date-range check. Expected result: even the required 128-KiB leading-zero cadence computes when representable without terminating; all-zero input remains a valid zero-day span; values outside `0001-01-01..9999-12-31` remain `due=unknown freshness=unknown`.

   **Accepted prior receipt:** `.ufo/waves/round-26/falsify/FDateHugeCadence.md:6-13,34-58` reports that 68,000+ leading zeros caused SIGSEGV/exit 139 with no output, while the operation reached the extglob strip before the later bound. It records the reproduction command as `timeout 300 env CHOUSA_STRICT=0 bash tree/tools/research-gate.sh verify-metadata scale/zN/e.md --root scale/zN --as-of 2026-10-21`. The receipt reports 40-digit/range controls matched its independent Python oracle; the separate defect was the long zero run. Its proposed distinguishing test is documented at `.ufo/waves/round-26/falsify/FDateHugeCadence.md:114-118`.

**Own-work source quote (S035):** “Compute declared recheck deadlines at an explicit as-of date, leaving event and unknown schedules distinct from current or overdue” (`corpus/SOURCES.md:45`). This supports the lane's declared date behavior, not external source truth.

## Preservation and gates

Keep the calendar arithmetic/year range at `tools/research-gate.sh:2295-2358`, strict overdue comparison at `:2754-2762`, and plain mode (freshness fields are gated by `AS_OF_ARG_SET` at `:2736-2737`). Current selftests cover small `0001d` and an oversized 36-digit nonzero cadence (`:6090-6116`), but do not themselves cover the required 128-KiB leading-zero and all-zero cases. Round-27 controls are specified in `corpus/evidence/round27-claims.md:9-11`.

**Unrun by this seat; L1 owns final verification:** `python3 corpus/evidence/round27-regressions.py --gate tools/research-gate.sh`; `bash corpus/evidence/round26-date-differential.sh`; `bash tools/research-gate.sh --selftest`. No installs or updates.