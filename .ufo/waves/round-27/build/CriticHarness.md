# CriticHarness — round27 C1 usage-harness critique (static, read-only)

Seat: ChousaR27.CriticHarness (critic, leaf). Base 64eec5d41c7cf7f17f5ce1e968e28b3769952596.
Method: static reading only. No selftest, gate, probe or build was run. No installs.
Target reviewed: the claim text `corpus/evidence/round27-claims.md` (C1), plus the
uncommitted `ExecUsage` working-tree diff read at
`.ufo/waves/round-27/work/ExecUsage` (HEAD = base, `tools/research-gate.sh` +26/-1).
This diff may change after this review; it is advisory input only.

## Ground truth (accepted, not rerun)

- r26 `FNoTrade.md:120-127`: the failing cases are `metadata-asof-invalid`,
  `-missing`, `-wrong-mode`. The cause is that `tools/research-gate.sh:6016` requires
  `$out != *'RESEARCH_GATE: '*`, but `die_usage` (`:390`) always appends usage text
  containing `Verdict: RESEARCH_GATE: CLEAN|DRIFT` (`:385`).
- The gate behaviour is correct: the diagnostics are emitted at `:6282`, `:6296` and `:6297`,
  during argument parsing and before any stdout.
- Static case ordinals: `metadata-registry-refused-nul` is case 187 (r26 log line 48).
  14 cases follow the usage trio, so the trio is cases **171/172/173**. That is outside
  legacy161, which agrees with the claim.

## What the ExecUsage diff does right

- It extracts `metadata_asof_usage_accepts RC EXPECTED OUT`, using an anchored
  `grep -c '^RESEARCH_GATE: ' … || true`, together with `rc -eq 2` and the expected substring. The real cases and
  the controls call the same function, so there is no copied predicate. The
  `|| true` keeps errexit from killing the selftest on a zero count.
- It keeps exit 2, keeps all three expected diagnostics byte-identical, and keeps the
  case names.
- Each negative control isolates one clause:
  - verdict: rc2, diagnostic present, verdict present;
  - exit: rc1, diagnostic present, no verdict;
  - diagnostic: rc2, no verdict, diagnostic absent.
- Control failures increment `failures` in the calling shell, not in a subshell.

## Counterexamples against the current diff (fixable defects)

### D1 — The controls do not detect the r26 defect (calibration, operability)

Run all three new controls against the **old** r26 predicate
(`$out != *'RESEARCH_GATE: '*`):

- the verdict control is rejected;
- the exit control is rejected;
- the diagnostic control is rejected.

All three report `ok-case` under the predicate that was falsified. Nothing in the controls
exercises the actual bug, which is help text containing `Verdict: RESEARCH_GATE: CLEAN|DRIFT`.
The claim's required control "correct usage passes" is **missing**. A constant-reject
predicate would also pass all three controls; only the real cases 171–173 would go red.

**Smallest fix:** add a positive control with `want_accept=1` and rc 2. Its output
should be the diagnostic line plus a usage block that includes the literal line
`Verdict: RESEARCH_GATE: CLEAN|DRIFT`. Better still, capture that output from the real
gate, for example `bash "$SELF" verify-metadata X --as-of` with `2>&1`, so drift in the
help text stays covered. Acceptance check: this control must FAIL under the r26
predicate and PASS under the new one.

### D2 — Inserting the controls renumbers 14 original cases (identity)

The controls are inserted right after `metadata-asof-wrong-mode`, which is case 173
(diff hunk `@@ -6086,6 +6105,12`). Cases 174–187 shift to 177–190. One example is
`ok-case  187 metadata-registry-refused-nul`, which becomes `190`.

Legacy161 is unaffected, but "all187 original case identities preserved" is no longer
true byte-for-byte on the `ok-case` lines.

**Smallest fix:** move the control calls after `metadata-registry-refused-nul`
(`:6237`) and before the summary (`:6241`). Cases 1–187 then keep their ordinal and
name, and the controls take 188 and up.

### D3 — The verdict control covers only CLEAN on line 2 (calibration)

The control output is `$'synthetic usage diagnostic\nRESEARCH_GATE: CLEAN'`. That has
three gaps:

- It does not cover DRIFT, which the claim names.
- It does not cover a verdict on **line 1**. A newline-prefixed glob such as
  `*$'\n'RESEARCH_GATE: *` would wrongly pass this control while missing a verdict on
  the first line.
- It does not put the help line in the same output, so it never shows that the predicate
  separates `Verdict: RESEARCH_GATE:` from a real verdict.

**Smallest fix:** add one rc2 control that has a DRIFT verdict with counters on the first
line, followed by the diagnostic and the help-text line, with `want_accept=0`.

### D4 — The diagnostic control does not use the real help text (calibration)

The `'different usage text'` output proves only that unrelated text is rejected. It does
not prove that the help text cannot satisfy an expected substring. This matters because
several plausible "simplified" expectations are vacuous: `--as-of`, `YYYY-MM-DD`,
`--as-of YYYY-MM-DD` and `verify-metadata` all appear in usage (`:311`, `:321`).

The current three expected strings are not substrings of the usage text (checked
against `:304-386`).

**Optional strengthening:** make the diagnostic control's output the real usage block
without the `research-gate: …` line.

## Reject list: any of these is test weakening and must be refused

1. Deleting, renaming, merging or skipping cases 171–173, or moving them into the
   1–161 range.
2. Loosening `rc -eq 2` to `-ne 0`, `-gt 0`, `-ge 1`, or dropping it.
3. Changing any expected diagnostic, or shortening it to a help-text substring:
   `--as-of`, `YYYY-MM-DD`, `--as-of YYYY-MM-DD`, `verify-metadata`.
4. Dropping the verdict clause, or allowing `nverdict -le 1`.
5. Unanchored or partially anchored counting:
   - `grep -c 'RESEARCH_GATE'` without `^`;
   - a `$'\n'RESEARCH_GATE: ` glob without first-line handling;
   - `grep -i`;
   - `^RESEARCH_GATE` without `: `.
6. Changing production text to satisfy the test: removing or renaming the `Verdict:` line
   in `usage()`, or making `die_usage` stop printing usage. The gate is correct, and
   `metadata-usage` (`:5945-5952`) and the header contract (`:8-9`) depend on this text.
7. Stripping help text in the harness, for example `out=${out//Verdict: RESEARCH_GATE*/}`
   or deleting lines that contain `Verdict:`. This duplicates the help text, and a broad
   pattern can hide real verdicts.
8. Routing the cases through `SKIPPED` / `skip-case` (the mechanism at `:5174-5177`),
   or through any path that increments `cases` without being able to increment
   `failures`.
9. Controls whose failures are lost, for example `failures++` inside `$(…)`,
   `… | while`, or `( … )`, or controls that always print `ok-case`.
10. Controls that test a **copy** of the predicate instead of `metadata_asof_usage_accepts`.
11. Removing `|| true` from the count. Under errexit a zero match aborts the selftest.
12. Redirecting `2>/dev/null` while still checking the diagnostic on stdout.
13. Changing the literal `exit=2` in the ok-case line while relaxing rc. That would produce
    false receipts.

## Holds and caveats for L1 (tradeoffs, not defects in the diff)

- **Merged stream versus stdout.** `metadata_asof_usage_case` still captures `2>&1`.
  `tsetup` (`:4013-4019`) is stricter: it captures stdout and stderr separately and requires
  zero stdout bytes plus non-empty stderr. All three usage paths exit before writing
  anything to stdout ([INFERENCE] from reading `:6249-6297`). So adding `${#stdout} -eq 0`
  would be a safe strengthening. It is optional; the claim only asks for the anchored count.
- **Namespace skips change the legacy161 hold.** The `ns` cases skip by name when user
  namespaces are unavailable (`:5174-5177`) and print `skip-case`, not `ok-case`.
  `round26-measure.sh:229` hashes the first 161 `^ok-case` lines, so a skip moves later
  lines into the 161-line window and changes `LEGACY_CASES_SHA` without any code change.
  L1 should record the skipped count next to PASS and compare the SHA only when namespace
  availability matches the r26 measurement. A PASS with skips is not evidence for the
  skipped cases. `${SKIPPED:+…}` prints ", 0 skipped" even when the count is zero.
- **Interaction with C2.** Any new C2 `--as-of` usage control, such as Unicode digits,
  must call `metadata_asof_usage_case` or `metadata_asof_usage_accepts`, not a fourth
  predicate. C2 must also keep the order at `:6295-6297`, where the mode check runs
  before date validation, or `metadata-asof-wrong-mode` will fail.
- **Docs and receipts.** The after-state total will be 187 plus the number of controls.
  SKILL.md `:505` (`FAIL (3/187 cases)`) and the evidence README must state the new total
  and that 1–187 are unchanged. The 187 baseline must not be reworded away.

## Impacted axes

| Item | Axis |
|---|---|
| D1 | calibration (controls cannot detect the defect), operability |
| D2 | operability (case identity) |
| D3, D4 | calibration |
| Namespace-skip hold | calibration of the legacy161 receipt |

## Unrun checks (L1, once, after integration)

- `bash tools/research-gate.sh --selftest`: PASS, with cases 1–187 identical by ordinal
  and name to r26 plus 171–173 now `ok-case`, and the skipped count recorded.
- Mutation check: temporarily evaluating the controls against the r26 predicate must
  turn the positive control into a FAIL. Do this on an isolated copy, not production.
- `LEGACY_CASES_SHA` equals `5eac4a7e…` under the same namespace availability.
- `python3 corpus/evidence/round27-regressions.py --gate tools/research-gate.sh` if it
  covers C1.

## Addendum — ExecUsage revision (static read 14:44Z, not run)

D1–D3 are resolved in the working diff:

- **D1 resolved.** `metadata-asof-usage-help-control` (rc2, diagnostic + `Verdict: RESEARCH_GATE: CLEAN|DRIFT`, want accept) is rejected by the r26 predicate, so it detects the r26 bug.
- **D2 resolved.** The five controls follow `metadata-registry-refused-nul`, so cases 1–187 keep their ordinal and name. The expected total is now 192.
- **D3 resolved.**
  - The CLEAN and DRIFT controls each put the verdict on line 1, alongside the help line.
  - The exit control is rc1 with the diagnostic and help text.
  - The diagnostic control is rc2 with help text and no diagnostic.
  - Each control isolates one clause.
- **Mechanism checked:**
  - `local SELF=<stub>` reaches `metadata_asof_usage_case` through bash dynamic scoping.
  - The stub prints `FAKE_OUTPUT` and exits `FAKE_RC`.
  - The inner helper's changes to `cases` and `failures` stay inside the `$( )` subshell, and the outer helper counts each control exactly once in the parent.
  - Both paths of the inner helper return 0, so errexit is safe.
- **Remaining (minor):**
  - `metadata_asof_usage_accepts` is now unused and duplicates the inline check. Delete it.
  - Acceptance detection uses the unanchored glob `*'ok-case  '*`. On rejection the inner helper echoes the captured output, so output containing that text would be misread as accepted. Anchor it as `'ok-case  '*`.
  - The trailing blank lines are noise.
- **Coverage limit:** the positive control uses synthetic help text (`usage: fixture`), not real `die_usage` output. Real output stays covered by cases 171–173.

## Addendum — C2 locale usage control (ExecDates working diff, static read 14:43Z)

- Good: `metadata-asof-unicode-date` calls `metadata_asof_usage_case` with an
  `LC_ALL=` prefix, so there is no new usage check. The bash temporary assignment
  reaches the child gate process. The case is appended after case 187.
- Gap: the diff has no separate always-run `LC_ALL=C` control, although
  ExecDates' message says it adds one.
- Gap (calibration): if `locale -a` yields no locale where fullwidth digits match
  `[0-9]`, `unicode_locale` falls back to `C` and the case still reports `ok-case`.
  On such hosts the case passes without the fix, so it tests nothing.
  Requested fix: add an explicit `LC_ALL=C` call, and label the locale used, or
  print a labelled skip when no locale reproduces the bug.
- Minor: blank lines added near `:6027` and `:6093` are diff noise and change no
  behaviour.

### ExecUsage follow-up and counting-command baseline (static read 14:47Z, not run)

**Acceptance anchored.** `:6037` now reads `[[ $helper_out == 'ok-case  '* ]]`.

**Why `metadata_asof_usage_accepts` stays.** `corpus/evidence/round27-regressions.py:74-77` regex-extracts both `metadata_asof_usage_accepts` and `metadata_asof_usage_case`, and calls `parser.error` if either is missing. Keeping the function is therefore justified. It is still unused, and the inline condition in the case is a second copy of the same check.
- Suggestion (not blocking): have `metadata_asof_usage_case` call `metadata_asof_usage_accepts`. That leaves one live check, and the script still finds both names.
- Coupling: the extractor regex `^  NAME\(\).*?^  }\n` requires two-space indentation and a closing `  }`. Reformatting the helpers breaks the counting command.

**Baseline problem for L1.** Base `HEAD:tools/research-gate.sh` has 0 occurrences of `metadata_asof_usage_accepts`. Running the counting command "unchanged on an isolated base archive", as `round27-claims.md` requires, stops at `parser.error` (argparse exit 2) during C1 helper resolution. That happens before any C2 or C3 observation, so the base run yields no per-claim mismatch counts.
- `round27-mechanisms-before.json` is a source-mechanism probe that is explicitly not a verdict, so it does not stand in for this baseline.
- L1 should record the base run's exit 2 as a setup failure, not as baseline mismatch counts.
- Alternatively, L1 could make helper resolution a recorded C1 mismatch instead of a fatal error. That counts as a change to the counting command, so it must be disclosed and applied identically to the base and final runs.
- The r26 FAIL3/187 receipt remains the C1 baseline.

### C2 locale revision (static read 14:45Z, not run)

- **Resolved:**
  - The `LC_ALL=C` call always runs.
  - When no locale admits fullwidth digits, the case is counted as `skip-case`, not as a pass.
  - The probe checks the exact bash-regex failure shape.
  - The new cases sit after case 187.
- **Open (case identity):** the case name `metadata-asof-unicode-date-${unicode_locale}` depends on the host, and the skip path uses a third name, `metadata-asof-unicode-locale`. Use one fixed name and report the locale separately.
- **Integration dependency:** in the ExecDates tree, `metadata_asof_usage_case` still has the r26 predicate, so both new usage cases fail until ExecUsage's change is merged. L1 must merge ExecUsage first or together with ExecDates, and must not resolve this with a local check.
- **Minor:** `plain_*` variables leak as globals in `run_selftest`.

### Final state (static read 14:48Z, not run)

**ExecDates: all points resolved.**
- `plain_*` are declared local at `:3372`.
- The fixed name `metadata-asof-unicode-date-locale` is used on both the run and skip paths, and the selected locale prints on a separate line.
- **Handoff defect, still open at 14:49Z:** `patches/ExecDates.patch` was regenerated at 11:48:30 but **does not apply** to base.
  - Check: `git apply` on a scratch `/tmp` copy of `HEAD:tools/research-gate.sh`, a write outside the repo that was then removed, failed with `error: patch failed: tools/research-gate.sh:6236`.
  - Cause: the last hunk header was hand-edited to `@@ -6236,6 +6241,64 @@`. Git's own diff of the clone gives `@@ -6236,7 +6241,64 @@`, and one blank context line was turned into an added `+` line.
  - `git apply --check -R` against the work tree passes only because the reverse direction tolerates the change, so it is not proof that the patch applies forward.
  - L1 must integrate from the work tree or from an unedited `git diff` regeneration, and must run `git apply --check` against a clean base before integrating.
- **Update 14:52Z:**
  - The artifact was replaced at 11:51:14. A static read shows all four hunk headers, including `@@ -6236,7 +6241,64 @@`, match the clone's `git diff`, and the blank context line is preserved.
  - At ExecDates' request and per this seat's read-only scope, no apply check was run on the new artifact. Forward-apply verification belongs to L1 at integration.
  - Note for L1: the two scratch `git apply` attempts made earlier by this seat ran outside the repository and touched only the patch file, not the gate or tests. They still go beyond pure static reading and are disclosed here.

**ExecUsage: accepted.**
- `patches/ExecUsage.patch` matches its work tree.
- The inline check plus the unused `metadata_asof_usage_accepts` stay, justified by the assignment scope ("C1 only in `metadata_asof_usage_case`") and by the counting command's name lookup.
- ExecUsage clarified that its "standalone extraction" note meant only that `metadata_asof_usage_case` has no dependency on an outside helper. It did not claim that `round27-regressions.py` extracts only that function. In fact, `round27-regressions.py:74-89` extracts and joins both helpers, so keeping the check inline is a scope choice, not a requirement of that script. No defect remains.

Tooling: none installed.
