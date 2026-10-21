# ScoutGateHarness — research-gate map

Axis: operability; preserve existing selftest and canonical gate behavior. Source inspected read-only: `tools/research-gate.sh`.

## 1. Selftest structure
- `run_selftest()` initializes sequential `cases`/`failures` and creates its fixture root with `mktemp -d "${TMPDIR:-/tmp}/chousa-research-gate-selftest.XXXXXX"`; EXIT traps clean the fixtures (`tools/research-gate.sh:2860-2875`). `write_rec()` creates a named Markdown fixture under `$WORK` (`:2943`).
- The generic fresh-process helper is `tcase()` (`:2948`): increments `cases` at `:2956`, invokes `bash "$SELF" verify ...` at `:2957-2960`, requires exactly one `RESEARCH_GATE` verdict, checks expected tokens, and prints `ok-case  %-2d %-28s exit=%d` (`:2971-2975`). Numbering follows helper invocation/source order.
- Mode-specific helpers mirror that pattern: `tclaims()` requires one verdict plus one `VERDICT_BEARING_CLAIMS=` line (`:2983-3007`); `tchain()` requires `RESOLVED_HOPS=` (`:3015-3037`); `tsweeps()` requires `VERIFIED_SWEEPS=...REJECTIONS_OK=` (`:3045-3067`); `tintegrity()` requires `INTEGRITY refs=` (`:3075-3097`). `tsetup()` asserts exit 2, empty stdout, and nonempty stderr (`:3502-3517`).
- Final success is `RESEARCH_GATE_SELFTEST: PASS (%d cases%s)` and exit 0; failure prints `FAIL (%d/%d cases)` and exits 1 (`:5198-5203`). The 136-case baseline is described by the pre-registration, not re-run for this read-only map.

## 2. `verify-metadata` dispatch points
- Add usage text next to the current `verify-integrity` entry at `:301-303`; parser mode recognition belongs beside `verify-integrity`/`verify-all` at `:5209-5216`; execution belongs in the final `case "$MODE"` before its unknown-mode arm (`:5261-5289`). The existing generic `--root` parser is at `:5225-5227`; positional paths flow through `RECORD_ARG` at `:5236-5238`.
- Observed default is `MODE=verify` (`:273`). [INFERENCE] With no recognized `verify-metadata` mode arm, `verify-metadata corpus/knowledge` is parsed as two positional paths and trips `multiple record paths` (`:273`, `:5236-5238`), consistent with the registered pre-implementation observation.
- `verify-all` explicitly composes only structure, claims, chain, sweeps, integrity (`:2439-2445`). Per registered spec, metadata is standalone; leave that composition unchanged.

## 3. Findings and strictness
- `emit_finding()` appends exactly `FINDING $id severity=$sev surface=$surface obs=$obs` (`:378-381`). `warn|crit` always increments drift and sets `ROLL=DRIFT`; `info` does so only when `STRICT==1` (`:382-385`). `STRICT` comes from `CHOUSA_STRICT` (`:279`); emitter returns 0 to avoid aborting before deferred verdict output (`:386-389`).
- Existing strictness test pair: `pass-export-chrome` remains CLEAN; `fail-export-chrome-strict` uses `CHOUSA_STRICT=1` and DRIFT (`:3176-3184`).

## 4. Summary format template
- `verify_sweeps()` emits `VERIFIED_SWEEPS=N/M REJECTIONS_OK=K/L`, then one `RESEARCH_GATE: <ROLL> (sweeps=... findings=... drift=...)` line (`:2082-2086`).
- `verify_integrity()` emits `INTEGRITY refs=N resolved=M unresolved=K`, then one `RESEARCH_GATE: <ROLL> (refs=... exempt=... findings=... drift=...)` line (`:2271-2275`). Both finish with `[[ $ROLL == CLEAN ]] && return 0` (`:2086`, `:2275`); global `set -euo pipefail` is at `:250`.

## 5. Fence handling to reuse
- `load_sections()` uses a two-pass fence scan (`:394-401`): matching fence character, closer length at least opener length, 0–3 literal-space indentation; unclosed opener is fail-closed. The fence regex and paired-fence scan are at `:407-418`; the second pass re-scans and skips headings inside fences (`:426-470`). It also tracks HTML comments (`:422-425`, `:431-470`).
- For the registered header rule, reuse the fence-state logic to identify the first *outside-fence* `## ` heading; metadata key scanning itself is a distinct header pass. The existing function additionally filters headings inside HTML comments, which is documented behavior of `load_sections`, not explicit in the metadata spec.

Confidence: high on source structure and insertion points. Remaining unknowns: no implementation or selftest run was requested/performed; the new mode's parser edge cases remain for the integrator's tests.

VERDICT: Read-only map complete; no files changed except this report.
Installs: none.
