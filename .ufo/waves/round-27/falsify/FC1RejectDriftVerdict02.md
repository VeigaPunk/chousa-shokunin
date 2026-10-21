# FC1RejectDriftVerdict02 — falsify C1 control `reject-drift-verdict`

Round 27, attempt 1. Target: landed revision `dd72641e574679c4f7882dd43de072b4c8892d6f`.
Gate `tools/research-gate.sh` sha256 `ca39d14d…4992f84` (matches). Control file
`corpus/evidence/round27-regressions.py` sha256 `5afea786…26bc526a5df`. Base gate `64eec5d4`
sha256 `c2c813f1…2143abc6`. Author-lane advice, not an outside admission.

## Verdict

- **Control as evidence for the anchored-count repair: FALSIFIED.** `reject-drift-verdict` stays
  green (exit 1 = expected 1) when the repair is reverted to the base substring predicate (m1)
  and when the count is unanchored (m4). It is green vacuously when the helper always fails (m6).
  It fails for the intended reason only under accept-DRIFT mutants (m2, m3, m11).
- **Landed production predicate, tested class: HOLDS.** 0/15 synthetic near-miss rows mismatch
  the literal anchored contract. 9/9 real-CLI usage errors print no verdict line.
  Both `exit 2` sites inside `verify-all` precede the verdict print.
- **General C1 vacuity (affects the set, not only this row):** the independent rows never run the
  real CLI (m8 is invisible); the rows only test rc ∈ {1,2} (m12 is invisible); the helper
  extraction hard-requires a dead function, `metadata_asof_usage_accepts` (m5 invisible, m9 breaks
  at setup).

## Identity and sandbox

- `git -C <lane> archive dd72641e… | tar -x -C /tmp/chousa-r27-falsify-FC1RejectDriftVerdict02`
- Base extract: `git archive 64eec5d4… tools/research-gate.sh` into `…-base/` (gate only).
- Mutants and drivers: `…-mut/`. Each mutant is a copy of the pristine gate with one edit.
- No lane file, git index, or sibling lane was touched. Only read-only `git` (archive, cat-file, rev-parse).

## (1) Is the expectation derived from the contract, independent of gate code?

- **Expectation: yes.** Row `('reject-drift-verdict', 2, usage+'RESEARCH_GATE: DRIFT\n', 1)`
  (control line 82) is hand-written. Its `exit 1` follows from the gate's declared exit
  contract: header lines 8–9 (`Verdict: RESEARCH_GATE: CLEAN|DRIFT`, `Exit: 0 CLEAN | 1 DRIFT | 2 setup/usage`)
  and usage lines 385–386. Exit 2 is setup/usage, so a verdict record there must be rejected.
  The claim text (round27-claims.md:7) agrees: "actual CLEAN/DRIFT verdict fails".
- **Mechanism: gate code.** The helper is regex-extracted from `--gate` text (lines 73–78) and
  executed against a stub CLI (`usage-stub.sh`). That is the same mechanism the gate's internal
  `metadata_asof_usage_control_case` (6057–6071) uses, so the two are not independent in mechanism.
- **Observation is exit-code only.** For this row `observe()` checks only the exit code and
  `forbidden=('command not found',)`; there are no `required` or count tokens. The row cannot tell
  "rejected because a DRIFT record is counted" from "rejected because the helper always fails".
- **Coupling to dead code.** Lines 74–77 `parser.error` unless `metadata_asof_usage_accepts`
  exists. In the landed gate that function (6036–6040) has no caller (`grep` finds only the
  definition). Comment line 69 ("not a duplicated predicate") is inaccurate: the gate carries a
  duplicate predicate that nothing calls.

## (2) Mutation evidence (single-line edits in sandbox copies; all pass `bash -n`)

Pristine: the C1 usage rows (regression lines 1–93, code unchanged) match 6/6. Row
`reject-drift-verdict` reports `FAIL-case … rc=2 … verdicts=1`.

| id | mutant | rows red (mismatch) | reject-drift-verdict | verdict |
|---|---|---|---|---|
| base | 64eec5d4 gate | setup error, exit 2: `usage selftest helper not found: metadata_asof_usage_accepts` | n/a | setup, not predicate |
| m1 | revert count to base `$out != *'RESEARCH_GATE: '*` (base line 6016) | 2/6 correct-usage-with-help, nonrecord-mention | **green** (exit 1, verdicts=1) | **not detected** |
| m2 | drop verdict condition | 2/6 reject-clean, reject-drift (`ok-case exit=2`) | red, DRIFT accepted | detected, intended |
| m3 | count CLEAN records only | 1/6 reject-drift (`ok-case`) | red, DRIFT accepted | detected, intended |
| m4 | unanchored count `'RESEARCH_GATE: '` | 2/6 correct-usage, nonrecord | **green** (verdicts=2) | **not detected** |
| m5 | dead `_accepts` forced `true` | 0/6 | green | blind (dead) |
| m6 | helper `if false` | 2/6 correct-usage, nonrecord | **green, vacuous** | vacuous |
| m7 | ignore exit code | 1/6 reject-wrong-exit | green | n/a for this row |
| m8 | `die_usage` prints `RESEARCH_GATE: DRIFT` (real CLI) | 0/6 | green | blind (see §3D) |
| m9 | delete dead `_accepts` (clean cutover) | setup error, exit 2 (same message as base) | n/a | setup, not predicate |
| m10 | `_case` delegates to `_accepts` (refactor) | 0/6 | green | behaviour-preserving |
| m11 | m10 + `_accepts` forced `true` | 4/6 reject-clean, reject-drift, reject-wrong-exit, reject-missing-diagnostic (all `ok-case`) | red, intended | delegation makes rows live |
| m12 | exit check `rc -ge 2` | 0/6 | green | blind; caught by §3C |

**Answer to the reversion question:** reverting the anchored count (m1) or unanchoring it (m4)
does **not** make `reject-drift-verdict` fail. The two rows that do fail are
`correct-usage-with-help` and `nonrecord-mention-is-not-verdict`. Each cites a substring-only
pass by reason. Under m1/m4 the DRIFT row is rejected by both predicates, so it cannot tell them apart.

**Setup vs intended reason:** only accept-DRIFT mutants fail for the intended reason. Base and m9
fail at setup (exit 2). Neither is a predicate result.

## (3) Counterexamples

- **A. Reversion not detected (m1/m4).** Input rc=2, output
  `expected diagnostic\nusage: fixture\nVerdict: RESEARCH_GATE: CLEAN|DRIFT\nRESEARCH_GATE: DRIFT\n`.
  Under m1 this row returns exit 1, identical to the expected 1.
- **B. Vacuous green (m6).** Every row FAILs, yet `reject-drift-verdict` exits 1 as expected.
- **C. Exit-range blind spot (m12, `rc -ge 2`).** All six independent rows pass (0/6). Synthetic
  rows R01 (rc=3, usage text with verdict-line) and R02 (rc=127, usage text only) are rejected by
  the landed gate (exit 1, correct) but accepted by m12 (exit 0): m12 is 2/4 red, landed 0/4 red.
  Minimal input: rc=3, output `expected diagnostic\nusage: fixture\n`.
- **D. Real-CLI blind spot (m8).** Nine usage-error invocations (as-of invalid / missing / wrong-mode,
  metadata no path, empty dir, verify-all no record, missing record, unknown flag, missing registry):
  landed `rc=2 verdict-lines=0` in 9/9; m8 `rc=2 verdict-lines=1` in 9/9. The independent rows stay 6/6.
  Real CLI usage paths are exercised only by the gate's internal selftest, which is not independent.
- **E. Landed predicate, literal contract (15 inputs).** No mismatch. Confirmed: CRLF DRIFT
  rejected; double-space DRIFT rejected; first-line DRIFT rejected; invalid-UTF-8-before-DRIFT
  rejected under C, C.UTF-8 and en_US.UTF-8; CR-only, ANSI-prefix, BOM-prefix, tab-after-colon,
  indented, no-space, same-line, lowercase and fullwidth-colon all accepted as non-records.
  Semantic note (low): CR-only, ANSI-prefixed, BOM-prefixed and indented DRIFT lines read as
  verdicts to a human but are non-records under the literal rule. The shipped emitters are all
  `printf 'RESEARCH_GATE: %s …\n'` at column 0 after LF, so these forms are unreachable from the
  gate. The claims text does not define the boundary.
- **F. Audit of real exit-2 paths.** `verify-all` exit 2 at line 3001 (sha unavailable) and 3037
  (manifest append failed) precede the verdict print (3041–3060). Section output is captured
  (`VAS_OUT=$(bash "$SELF" …)`, line 2854), not streamed. No landed exit-2 path after a verdict was found.

## Environment anomaly (limit)

The persistent tool shell resolved `grep` to `pi-uu-grep 0.2.0`, which printed
"stream did not contain valid UTF-8" and exited 1 on the invalid-byte shape. A fresh `bash` resolves
`/usr/bin/grep` = GNU grep 3.12-modified, and all 10 invalid-byte probes counted correctly. All
gate-relevant probes used `/usr/bin/grep`. The gate's `grep -c … || true` treats a grep error as zero
verdicts, so a non-GNU grep in the gate's children would fail open. Not reproduced here.

## Recommendations (author-lane advice)

1. Make `_case` call `metadata_asof_usage_accepts` (m10 is equivalent on all 6 rows; m11 shows
   the rows then detect the predicate mutation). That removes the dead copy and the coupling.
   Sibling notes `.ufo/waves/round-27/build/CriticHarness.md:188,213` and
   `ConnectIntegration.md:153–162` already flag this; I did not rely on them.
2. Add a real-CLI row independent of the selftest: `bash "$gate" verify-metadata <nonexistent>
   --as-of 2026-02-30` in a temp dir, assert rc 2 and zero `^RESEARCH_GATE: ` lines (catches m8).
3. Add rc 3 and rc 127 usage-shaped rows with no verdict (catches m12).
4. Do not cite `reject-drift-verdict` as evidence for the anchored count. Cite
   `correct-usage-with-help` and `nonrecord-mention-is-not-verdict`.
5. Replace `|| true` on the verdict count with explicit grep-exit handling (1 = no match; >1 = error,
   fail closed). Defensive; not reproducible with GNU grep here.
6. Correct the comment at regression line 69.

## Commands and key output

```
S=/tmp/chousa-r27-falsify-FC1RejectDriftVerdict02; M=$S-mut
sha256sum $S/tools/research-gate.sh                       # ca39d14d… (exit 0)
python3 $M/slice_usage.py --gate $S/tools/research-gate.sh        # SLICE_MISMATCHES 0 of 6
python3 $M/slice_usage.py --gate $M/m1-base-substring/research-gate.sh   # 2 of 6; reject-drift green
python3 $M/slice_usage.py --gate $M/m2-no-verdict-check/research-gate.sh # 2 of 6; reject-drift exit 0!=1
python3 $M/slice_usage.py --gate $M/m6-always-fail/research-gate.sh      # 2 of 6; reject-drift green
python3 $M/slice_usage.py --gate $M/m9-delete-dead-accepts/research-gate.sh      # exit 2 setup
python3 $M/slice_usage.py --gate /…-base/tools/research-gate.sh         # exit 2 setup
python3 $M/slice_usage.py --gate $M/m11-delegates-plus-accepts-true/research-gate.sh # 4 of 6
python3 $M/slice_near.py --gate $S/tools/research-gate.sh               # NEAR_MISMATCHES 0 of 15
python3 $M/slice_near.py --gate $M/m1-base-substring/research-gate.sh   # 5 of 15
python3 $M/slice_rc.py  --gate $M/m12-rc-ge2/research-gate.sh          # RC_MISMATCHES 2 of 4
bash $M/real_cli_probe.sh $S/tools/research-gate.sh                     # rc=2 verdict-lines=0 (9/9)
bash $M/real_cli_probe.sh $M/m8-die-usage-verdict/research-gate.sh      # rc=2 verdict-lines=1 (9/9)
for f in … mutants …; do bash -n $f; done                               # all OK
```

Driver exit codes: the slice drivers print `*_MISMATCHES` and exit 0 by design. The shipped
script exits 1 on any mismatch (`raise SystemExit(int(summary['mismatches'] != 0))`). I did not
reproduce that line; the counts above are the signal. Setup failures exit 2 (argparse).

## Limits

- Did **not** run `--selftest` or the full `round27-regressions.py`. Run: the C1 usage rows only
  (lines 1–93, unchanged code), plus my own near-miss and rc rows through the same `observe()`
  and helper extraction (lines 1–78).
- The independent rows are stub-based by design, so real-CLI results come only from my probe (18
  invocations, all with nonexistent/empty synthetic paths, no network, no host files).
- NUL bytes cannot pass through environment variables, so the NUL shape was not tested.
- No installs or updates were performed; the tools used were the host's bash, python3, diff,
  sha256sum, GNU grep and git (read-only).
- Sibling notes in `.ufo/waves/round-27/build/` were read for corroboration only.

## Erratum (appended after the single write; append-only)

- Control file full sha256: `5afea7863f2b052ba54a46cf2faf88f863d76c61d3d2cf45e091f92bc526a5df` (the identity line above abbreviates it incorrectly).
- "all 10 invalid-byte probes counted correctly" should read "all 10 probes returned the expected count" (T1–T10 in the fresh-shell probe; T6, T7 and T10 are controls without an invalid byte).
- Read-only git used on the lane: `archive`, `log`, `diff --stat`, `cat-file`, `rev-parse`.
