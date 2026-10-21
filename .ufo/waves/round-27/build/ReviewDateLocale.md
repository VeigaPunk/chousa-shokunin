# ReviewDateLocale — C2 locale and date parsing

Axes: freshness correctness; calibration of the independent oracle; operability of the usage exit contract.

## Finding — P2 acceptance-coverage gap: Unicode entry dates are not exercised

The reviewed `ExecDates` candidate diff adds `local LC_ALL=C` to `metadata_iso_date` (`tools/research-gate.sh:2295–2300`), covering its top-level `--as-of` caller; entry scanning also has a function-local C locale at `:2543`, covering its date regexes at `:2702–2708` and explicit-date/cadence handling at `:2718–2752`. The new Unicode control at `:6111–6126` exercises only a Unicode `--as-of` argument, while the entry fixtures at `:6047–6101` use ASCII dates. Consequently the control does not establish the claim's ASCII grammar for entry fields (`corpus/evidence/round27-claims.md:9–11`). It also records a skip when no installed locale admits Unicode digits; that is not evidence for this locale-specific case.

Suggested acceptance oracle: in the discovered Unicode-admitting locale, add synthetic entry cases with `verified-at: ２０２６-10-01` and with a date-form `recheck: ２０２６-10-21`. Require the first to be reported `verified_at=undated` with `META_VERIFIED_AT_UNDATED`; require the second to be `recheck=unscheduled`, and with `--as-of` to remain `due=unknown freshness=unknown` (never a parsed Unicode date). Keep the current CLI case and its exit-2/no-verdict assertion. A locale-unavailable skip should remain explicit and must not be reported as a passed Unicode control.

Static review of the changed `BASH_REMATCH` use found no intervening regex or function call: `metadata_iso_date` reads its captures in the immediately following `local` command (`:2297–2299`), and the significant-digit regex is followed immediately by `digits=${BASH_REMATCH[1]}` (`:2351–2352`). Do not make `BASH_REMATCH` local; the current immediate-consumption pattern preserves the captures.

## Residual risk and verification gaps

The r26 receipts establish the baseline locale failure and long-zero termination: `.ufo/waves/round-26/falsify/FDateAsOfUsage.md:51–113` and `.ufo/waves/round-26/falsify/FDateHugeCadence.md:34–118`. The candidate's ERE normalization plus immediate capture consumption addresses the observed recursive extglob path by inspection; no runtime result is claimed. Reviewed the private `.ufo/waves/round-27/work/ExecDates` candidate diff, not the final integrated tree. No selftest, regression suite, or differential was run. No `lsp` device is mounted (`xd://lsp` returned the available-device list), so no LSP status/references/definition/diagnostics evidence is available; code citations here are direct static-source evidence only. No tools installed.
