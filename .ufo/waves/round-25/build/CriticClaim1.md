# Round 25 — Claim 1 scoped critique

Static review of registered spec/prediction only; I did not run a gate or selftest. Output behavior below is inference from Spec v1, not observed implementation behavior.

Axes: **operability** (C1), **freshness** (C2), **calibration** (C3).

## Ranked attacks

1. **High — the registered oracle is out of criterion-6 scope.** `QUALITY.md:17-23` makes criterion 6 apply to knowledge entries admitted from r24 on. The predicted sole failures are `archives-verified-r9.md`, `audit-r11.md`, and `gate-baseline-r8.md` (`round25-claims.md:44-47`): all predate that cutoff. They may be useful legacy-debt findings, but their missing `recheck:` fields are not criterion-6 violations. The 28-file copied population (`round25-measure.sh:13-17`) can produce the registered `25/28` result while never rejecting a bad r24+ header; no r25 entry is in that frozen list. **Concrete counterexample:** alter the r24 `claim-support-states-r24.md` header to `source: S006` / `verified-at: 2026-10-21` / `recheck: 90d`; the listed S006 row is mined and used by that entry (`SOURCES.md:16`), but the source value lacks the required URL/path and exact anchor, and the dated verification says nothing checked (`QUALITY.md:18-23`). Spec v1's tests are only presence, date-prefix, and schedule-token tests (`round25-claims.md:29-40`), so it can count this as complete. The prediction is mechanically falsifiable, but not failure-capable against this criterion violation unless a malformed r24+ negative is an explicit acceptance case.

2. **High — command-only `recheck:` is a criterion violation downgraded to non-failing info.** QUALITY explicitly says a command-only recheck leaves overdue uncomputable (`QUALITY.md:21-23`), but Spec v1 makes `META_RECHECK_UNSCHEDULED` info, with info affecting exit only under `CHOUSA_STRICT=1` (`round25-claims.md:32-40`). **Concrete counterexample:** in the r24 `citation-chain-fidelity-r24.md:5` header replace `90d (...)` with `bash tools/research-gate.sh --selftest`. It still has a source and dated verification (`:3-4`); inferred result is an unscheduled INFO and default exit 0/CLEAN, despite violating criterion 6. It is not wholly absent from output (`round25-measure.sh:19` prints INFO), but the named-drift extractor filters to `warn|crit` (`:20`), and callers using the exit status receive a false clean. Make unscheduled a failing severity; keep root-parent portability separate (it is not itself a criterion-6 violation).

3. **High — the header grammar admits prose as metadata.** Spec v1 defines the header as everything before the first unfenced `## ` and accepts any column-zero key there (`round25-claims.md:24-28`); it has no metadata delimiter or requirement that these lines constitute a metadata block. **Concrete counterexample file text:**

   ```markdown
   # Example only
   These are illustrative strings, not this entry's provenance or verification:
   source: S006 https://arxiv.org/html/2605.06635v1 §3.3
   verified-at: 2026-10-21 (illustrative; not checked)
   recheck: 90d
   ## Example
   ```

   The three key lines are in the defined header, outside fences and at column zero, so the spec classifies each as present/dated/scheduled despite the prose explicitly disclaiming them. A delimited metadata block (or equally strict header grammar) is needed. An all-empty triplet is not the strongest counterexample: the spec explicitly warns on undated `verified-at`; instead, require a negative case for empty `source:` because its empty-value semantics are unspecified (`round25-claims.md:29-40`).

4. **Medium — frozen measurement does not exercise the new admission.** The harness copies only the 28 names in `POP1`, not the round-25 knowledge entry that Claim 1 says will cite a newly opened source (`round25-measure.sh:14-17`; `round25-claims.md:50`). Add a direct check of that new entry and explicit negative r24+ fixtures; otherwise a passing base-population prediction says nothing about the newly admitted record.

## Axis and separability verdict

`verify-metadata` is correctly an **operability** capability acquisition if it becomes a runnable command with trustworthy stated outcomes: AXES defines operability as executable checklists/commands/scripts (`AXES.md:13`) and tracks capabilities separately from the six axes (`:57-64`). It is not, by itself, a calibration move; using its current false-clean result as evidence of compliance would instead harm calibration. Standalone (not composed into `verify-all`) is an operator-run screen, not an admission guarantee (`round25-claims.md:41-42`).

C1 is file/population-separable from C2 and C3 as registered: its gate/knowledge inputs differ from C2's README/SCORECARD and C3's SKILL/ledger inputs (`round25-claims.md:74-79`; `round25-measure.sh:13-21,23-54,57-79`). Shared gate holds remain a no-harm check, not evidence that C1 tested criterion semantics. Keep the distinct axis labels; do not count legacy debt findings as criterion-6 compliance tests.

**Smallest safe correction:** label pre-r24 missing fields as legacy debt (not criterion-6 failures); require nonempty/adequate source data and a date plus checked-description for `verified-at`; make unscheduled rechecks fail; require a true metadata boundary; and pin negative tests for empty source, command-only recheck, prose keys, and malformed r24+ entries. Include the r25 entry in the measurement.

Installs: none.
VERDICT: C1 is axis-appropriate and mechanically separable, but its pre-registered oracle validates legacy key presence—not criterion-6 enforcement; revise the acceptance oracle before treating a pass as a quality improvement.