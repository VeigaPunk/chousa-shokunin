# ResUsageMatcher — round-27 residual review of change (d)

Target: `metadata_asof_usage_accepts` / `metadata_asof_usage_case` and selftest case 215
`metadata-asof-usage-matcher-fault`, landed in `tools/research-gate.sh` at
`cb895a2bdd259eb38bec29ef70011d8211a508b5` (gate sha256
`a6bc2855e63045c9ebc0827166756d4da65478a1e255a83903ab459a08582386`).

**VERDICT: HOLDS.** No landed-gate counterexample found: on every input I could construct the
matcher accepts exactly the correct-usage outputs and rejects anchored verdict records, wrong
exits, missing diagnostics and matcher faults. Case 215 is load-bearing (three single-site mutants
each make it fail). Residual weaknesses: F1 (misleading FAIL diagnostic), F2 (exit-1-only fail-open
residue), F5 (coverage gap); inherited observations F3, F4. Author-lane advice, not outside
admission.

## Scope and identities (read-only lane)

* Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin` read only (`git log/diff/show/archive`); the
  only write is this report. Sandboxes under `/tmp/chousa-r27-residual-ResUsageMatcher`: `dd/` =
  archive of `dd72641e` (gate `ca39d14d…92f84`), root = archive of `cb895a2b` (gate
  `a6bc2855…582386`, matches the assignment), plus `m1/`–`m4/` mutants and `faultbin/`.
* Locale inherited (`LANG=en_US.UTF-8`); `LC_ALL=C` was **not** exported for any selftest run.

## Verified

**V1 — selftest, landed revision.** `bash tools/research-gate.sh --selftest` → exit **0**,
`RESEARCH_GATE_SELFTEST: PASS (215 cases, 0 skipped)`; ok-case 215 =
`metadata-asof-usage-matcher-fault accepted=0`. Same command in `dd/` → exit **0**,
`PASS (210 cases, 0 skipped)`.

**V2 — cases 1–210 identities unchanged.** `diff` of the ok/skip/FAIL-case `number name` lists of
the two selftest logs → exit 1, output only `210a211,215` adding `211 metadata-registry-escaped-
pipe-width`, `212 …-escaped-pipe-overwide`, `213 …-mixed-outer-pipes`, `214 …-delimiter-after-blank`,
`215 metadata-asof-usage-matcher-fault`. `head -210` of both lists → `diff` exit **0**.

**V3 — case 215 fails if the fail-closed clause is removed (sandbox mutants).** Three single-site
mutants of the landed gate, each run with `bash tools/research-gate.sh --selftest`: `m1` = `accepts`
body reverted verbatim to the `dd72641e` body (`|| true`, `${nverdict:-0}`); `m2` = drop only
`((grc <= 1)) &&`; `m3` = drop only `|| grc=$?` → `|| true`. All three → selftest exit **1**,
decisive output `FAIL-case metadata-asof-usage-matcher-fault matcher fault accepted` and
`RESEARCH_GATE_SELFTEST: FAIL (1/215 cases)`. Both halves of the clause are necessary; case 215
detects removal of either.

**V4 — no new false rejection for zero-verdict outputs (grep exit 1).** Mutant `m4`
(`((grc <= 1))` → `((grc == 0))`) → selftest exit **1**, `FAIL (6/215 cases)`:
`metadata-asof-invalid`, `-missing`, `-wrong-mode`, `metadata-asof-usage-help-control`,
`metadata-asof-unicode-date-locale`, `metadata-asof-unicode-date-C`. The landed `<= 1` bound is
exactly what keeps grep-exit-1 (zero matches) outputs acceptable; all six pass at `cb895a2`.

**V5 — acceptance matrix on the landed helper.** Byte-faithful extraction of both helpers
(`mkharness.py`; extracted block sha256 `33560f09…76e15f`, 947 bytes) plus a driver;
`bash harness-landed.sh` → exit **0**, `HARNESS: pass=18 fail=0`: correct-usage accepted; anchored
`RESEARCH_GATE: CLEAN`/`DRIFT` rejected; wrong exit 0/1/3/127 rejected; missing diagnostic rejected;
empty output rejected; grep shim exit 2 rejected (with and without a printed count); grep shim exit
1 printing `0` accepted; grep shim exit 0 printing `1` rejected; grep missing from `PATH` rejected;
help-text substring `Verdict: RESEARCH_GATE: CLEAN|DRIFT` not counted as a record (accepted);
indented record accepted (contract-consistent, matches falsify CE2).

**V6 — the falsify-wave counterexample is closed.** Reproducing
`.ufo/waves/round-27/falsify/FC1CorrectUsageWithHelp00.md` exactly (PATH-first faulting `grep`
exiting 2, sha256 `bbcc9f71392b2c6814f40526ca9a18faffa5c0e9b135881bff48d329f6100b84`, extracted
helpers driven through the shipped stub-CLI protocol):
`PATH="$SB/faultbin:$PATH" bash fc1-mirror-dd.sh` → mismatches=2, with `reject-clean-verdict
accepted=1 want=0` and `reject-drift-verdict accepted=1 want=0` (FAIL-open, reproduced);
`PATH="$SB/faultbin:$PATH" bash fc1-mirror-cb.sh` → mismatches=1, with `reject-clean-verdict
accepted=0 want=0` and `reject-drift-verdict accepted=0 want=0` (now rejected) and
`correct-usage-with-help accepted=0 want=1`. The single remaining mismatch at `cb895a2` is the
*positive* case refused under a matcher fault — the intended fail-closed trade-off, and exactly what
the independent control `matcher-fault-fails-closed` asserts.

**V7 — independent controls discriminate.** `python3 corpus/evidence/round27-falsify-controls.py
--gate <gate>`: against `cb895a2` → exit **0**, `total 26, mismatches 0` (gate_sha256 reported as
`a6bc2855…`); against the `dd72641e` gate → exit **1**, `mismatches 4`, first line
`MISMATCH C1 matcher-fault-fails-closed FC1CorrectUsageWithHelp00 exit 0 != 1`. Matches the L1
receipt (4 on dd, 0 on cb).

**V8 — real gate usage path.** `bash tools/research-gate.sh verify-metadata <path> --root . --as-of
2026-02-30` → exit **2**, output contains `research-gate: --as-of must be a valid YYYY-MM-DD date`,
`grep -c '^RESEARCH_GATE: '` → 0 (grep exit 1). `bash tools/research-gate.sh --help` prints
`Verdict: RESEARCH_GATE: CLEAN|DRIFT` at line 81 (mid-line) and **0** anchored records — the
anchored count is load-bearing for the real banner.

## Findings (severity ordered)

**F1 — LOW — landed gate — the FAIL diagnostic misattributes a matcher fault.** *Attacks:* honesty
of the rejection reason. `cb895a2` `tools/research-gate.sh:6052` keeps a second, non-fail-closed
count `nverdict=$(grep -c '^RESEARCH_GATE: ' <<<"$out" || true)` used only for the FAIL message,
while acceptance is delegated to `accepts` (6053). Under a matcher fault that count is empty and
`${nverdict:-0}` prints a hard zero. *Command:* `PATH="$SB/faultbin:$PATH" bash fc1-mirror-cb.sh`
→ exit 1; *decisive output:* `FAIL-case reject-clean-verdict rc=2 expected=expected diagnostic
verdicts=0` — "verdicts=0" is asserted although the count is *unknown* (grep exited 2), so a reviewer
attributes the rejection to "no verdict records" rather than to the fault. The duplicate count came
in with `dd72641e`, but change (d) made the fault reachable in the decision path and left the
message behind. *Advice:* reuse the helper's count, or print `verdicts=?` when unavailable.

**F2 — LOW/MEDIUM — control weakness — fail-closed keys on exit status only, so an error reported
as exit 1 still fails open.** *Attacks:* robustness of the fail-closed intent. The clause accepts
`grc == 1` because "grep exits 1 on zero matches", but exit 1 with *no* count leaves `nverdict`
empty and `[[ $nverdict -eq 0 ]]` evaluates the empty string as 0 (bash arithmetic), so the output
is **accepted**. *Command:* `bash harness-landed.sh`, case `grep-shim-exit1-silent`
(`grep(){ return 1; }`) → exit 0; *decisive output:* `ok grep-shim-exit1-silent accepted=1 (want 1)`.
A matcher reporting errors as exit 1 is thus indistinguishable from "no match" — the falsify wave
recorded such a matcher in this lane (`FC1RejectDriftVerdict02.md`: "pi-uu-grep 0.2.0 printed
'stream did not contain valid UTF-8' and exited 1 … treats a grep error as zero verdicts"). Not
reproducible with the shipped matcher here: a child bash resolves `grep` to `/usr/bin/grep` (GNU
grep 3.12-modified), which prints `0` and exits 1 on no match (`printf 'x\n' | /usr/bin/grep -c
'^RESEARCH_GATE: '` → `0`, exit 1). So a robustness/coverage weakness, **not** a landed-gate
counterexample. *Advice:* require a produced count (`[[ $nverdict == 0 ]]`) and allow `grc == 1` only
when that count was actually printed.

**F3 — LOW — inherited consistency — 15 sibling verdict counters in the same file still fail open.**
*Command:* `grep -n "grep -c '\^RESEARCH_GATE: '.*|| true" tools/research-gate.sh` → 15 hits
(2861, 3176, 3497, 3534, 3564, 3594, 3624, 4557, 5210, 5753, 6023, 6052, 6201, 6352, 6374); base
`64eec5d` had 12. Change (d) hardened exactly one member of this family; the rest are base-identical
(inherited). *Advice:* apply the same status discipline to the family, or record the exception.

**F4 — INFO — inherited — the required diagnostic is still an unanchored substring.**
`$out == *"$expected"*` accepts any output that merely mentions the required text; the real usage
banner contains `--as-of` twice (falsify `FC1RejectMissingDiagnosti04.md`). Identical in base
`64eec5d` → inherited. With the predicate now centralised, an anchored `^research-gate: <expected>$`
check would be cheap.

**F5 — INFO — coverage gap — selftest case 215 does not cover the fault shape it exists for.**
Case 215 (`tools/research-gate.sh:6550-6556`) injects the fault as a shell function
`grep() { return 2; }` in a subshell; it does not cover (a) a PATH-first faulting `grep` binary —
the exact falsify counterexample of V6, (b) `grep` missing from `PATH`, (c) a silent exit-1 fault
(F2). The in-gate selftest would stay green under (a)–(c); only the independent suite's
`matcher-fault-fails-closed` covers (a). *Advice:* add a PATH-first faulting-grep case beside 215.

## Residual risk and verification gaps

* Both helpers live inside `run_selftest` (`tools/research-gate.sh:3395-6563`); no production path
  calls them. The blast radius of change (d) is the gate's own selftest verdicts, not user-facing
  output — the claim receipt should say so, or a reader may read "C1 operability" as a user-facing
  fix.
* The matcher is the predicate's only external dependency and its exit-code convention (0/1/≥2) is
  assumed, not enforced (F2). Under a matcher fault the landed gate also fails closed on the
  *positive* usage cases: intended policy, but it turns a passing selftest into a failing one
  (loud, not silently green) — confirm the lane wants that loudness.
* I did not run `corpus/evidence/round27-regressions.py` (the original six C1 scenarios) or the
  date/registry differentials — those belong to the `ResReceipts` / `ResControlsSuite` seats. My FC1
  mirror re-implements the five C1 scenarios from the falsify report's own bytes: equivalent in
  substance, not the shipped script.

## Tools

No installations, upgrades or updates were performed. Observed (all pre-existing): `bash
5.3.20(1)-release`, `python3 3.14.8`, `/usr/bin/grep` (GNU grep 3.12-modified), `git` (read-only
archive/show/diff/log), `sha256sum`, `diff`. The interactive tool shell resolves `grep` to a
pi-based builtin (`grep grep (pi-uu-grep) 0.2.0`); every gate-relevant measurement was taken in a
child `bash`, where `grep` is `/usr/bin/grep`.
