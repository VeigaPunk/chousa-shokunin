VERDICT: HOLDS — receipt reproduced (dd72641 4 mismatches, cb895a2 0) and expectations independent of gate output; caveats: dd72641 `scale-4mib` mismatch is timeout/load-dependent, changes (b) and (c, registry site) are vacuous for the suite, and one landed-gate false CLEAN (inherited at base, regressed vs dd72641) escapes the C3 controls.

# ResControlsSuite — round27 residual review of corpus/evidence/round27-falsify-controls.py @ cb895a2

Seat: ChousaR27-2.ResControlsSuite-16 (critic, read-only). Sandbox: /tmp/chousa-r27-residual-ResControlsSuite
(`git archive` of 64eec5d, dd72641, cb895a2). Gate sha256 verified: 64eec5d c2c813f1…abc6, dd72641 ca39d14d…2f84,
cb895a2 a6bc2855…2582386. Suite sha256 8d841d6a…f4c6093 (same as receipts fc-before/fc-after).
Tools installed/updated: none. Host: 32 cores, load avg 10–14 during runs.
Instrumented copy `inst.py` (in /tmp only) adds per-control wall time, `INST_SKIP`, `INST_TIMEOUT_SCALE`, and
tolerates a missing helper (needed for base); control bodies and expectations are byte-unchanged.

## 1. Suite runs (unmodified suite unless noted)
Command: `python3 cb895a2/corpus/evidence/round27-falsify-controls.py --gate <rev>/tools/research-gate.sh --output out-<rev>.json`
| gate | exit | result |
|---|---|---|
| 64eec5d (unmodified suite) | 2 | `error: usage selftest helper not found: metadata_asof_usage_accepts` (setup abort; helper is new in r27) |
| 64eec5d (inst.py, skip `scale-4mib-leading-zeros`) | 1 | 25 run, 5 mismatches: C1 `indented-mention-is-not-record`; C3 `escaped-pipe-overwide`, `registry-raw-leg-only`, `entry-raw-leg-only-reason`, `claims-raw-leg-only` |
| dd72641 | 1 | 26/4: `matcher-fault-fails-closed` (exit 0≠1), `scale-4mib-leading-zeros` (exit 124≠0), `escaped-pipe-width` (2≠0), `escaped-pipe-overwide` (0≠2) |
| cb895a2 | 0 | 26/0 |
The L1 receipt is confirmed exactly: same four names and same error strings as post-falsify/fc-before.stdout, and 0 on cb895a2 as in fc-after.stdout.
Base skip: `scale-4mib-leading-zeros` only. Base strips zeros with `digits=${digits##+(0)}` (extglob recursion; the dd72641 diff
comment says "extglob recurses on long zero runs"). That is the "unsafe old long-token crash" the claims forbid rerunning,
and timing.log already shows base at 300 s timeout on the dense fixture. Every other base control ran in ≤0.03 s.
Base under en_US.UTF-8 (`inst-utf8.py`, same skip) gives the same 5 mismatches.

## 2. Expectation provenance, per control (26)
C1 (5): the expectations come from the claims' C1 text (anchored `^RESEARCH_GATE: ` count; exit1 fails; missing diagnostic fails; a verdict fails).
- `matcher-fault-fails-closed` expects 1. The fail-closed rule is derived (a matcher that can't count can't prove zero records) rather than literal claims text. Independent of gate output. On base it passes vacuously: the substring predicate rejects the fixture's `Verdict: RESEARCH_GATE: CLEAN|DRIFT` help line, not the fault.
- `indented-mention-is-not-record` (0), `column0-other-record-rejected` (1, PENDING), `different-diagnostic-rejected` (1), `exit-zero-rejected` (1): claims-derived. `indented-mention` is the acceptance twin that keeps the matcher-fault control non-vacuous.
- Coupling: the helpers are extracted from gate source by the regex `^  name\(\).*?^  }\n`. A rename or reindent fails closed (exit 2, as on base), never silently passes.
- Gap: no column-0 `RESEARCH_GATE: CLEAN` or `DRIFT` control (claims name CLEAN/DRIFT explicitly). The PENDING control covers the anchored-count rule.
C2 (8): Python `datetime` cross-check: `date(2000,2,1)+timedelta(90)=2000-05-01`; 2100/1900-02-29 invalid; 2000-02-29 valid;
`date(2026,1,1)+timedelta(99999999)` raises OverflowError; `date.max-date.min=3652058` days, so any cadence of 8+ digits is out of range.
- The five `date_cases` compute `due` with an in-script `assert` against datetime. Freshness follows strict `as-of>due` (`twenty-char-value-seven` sits exactly on the boundary).
- The three leap controls use hard-coded literals, which I verified against datetime above. `due=unknown freshness=unknown` with exit 0 comes from the pre-existing r26 contract (round26-claims.md lines 70 and 147; 4 occurrences in the base gate), not from new output.
- Coverage: the suite pins `LC_ALL=C`, so it cannot see C2's locale defect. Base passes all 7 runnable C2 controls under both C and UTF-8. Locale and Unicode-digit coverage must come from round27-regressions.py, not this suite.
C3 (13): GFM-derived. Escaped `\|` is cell content; header and delimiter cell counts must match; outer pipes are optional per row; a blank line ends a table. The consulted/queued twins prove the registry is actually read. Denylist controls come from the claims' C3 text ("no reading a denylisted synthetic path when a colon occurs earlier").
- Wording coupling: `metadata registry refused: denylist` appears 0 times in the base gate (introduced by dd72641), and the claims don't specify that wording. The semantics (exit 2, 0 verdicts) are claims-derived. `META_ENTRY_REFUSED`, `reason=denylist`, `CLAIM_SOURCE_SESSION`, `META_SOURCE_NOT_MINED`, `findings=0 drift=0` and `metadata registry has no table` all pre-exist at base (counts 4/1/8/4/28/1).
Verdict on independence: no expectation was copied from gate output; one diagnostic string is gate-authored r27 wording (low risk).

## 3. Vacuity: one single-site revert per change (cb895a2 base, inst.py with INST_TIMEOUT_SCALE=10 unless noted)
| revert | sha256[:12] | red controls |
|---|---|---|
| (a) `header_width=${#cells[@]}` | 566a32369ab6 | `escaped-pipe-width` (2≠0), `escaped-pipe-overwide` (0≠2) |
| (b) drop `\| grep -xE 'S[0-9]{3,}'` | 99a91b7164b7 | none (VACUOUS) |
| (c1) registry loop `line=${line%$'\r'}` | 14cd620d47d5 | none (VACUOUS) |
| (c2) verify_metadata loop `line=${line%$'\r'}` | 2dd63b02a4b2 | none at 10× timeout (scale-4mib took 67.15 s); at the default 60 s: `scale-4mib-leading-zeros` exit 124 (60.06 s) |
| (d1) old `metadata_asof_usage_accepts` body (`\|\| true`) | 1f4f44783d99 | `matcher-fault-fails-closed` (0≠1) |
| (d2) case's inline old predicate instead of calling accepts | 3d7007b3818f | `matcher-fault-fails-closed` (0≠1) |
(b) is behavior-equivalent by construction: the loop still has `[[ $source_id =~ ^S[0-9]{3,}$ ]] || continue` under `LC_ALL=C`, so only performance changes.
Probe: a source line of `S001` plus 1,000,000 `x` tokens, via `bash <gate> verify-metadata … --registry`: cb895a2 exit 0 in 218 ms; rev-b exit 0 in 3615 ms, same CLEAN.
(c1) probe: a 2 MiB non-table line before the registry table: cb895a2 77 ms, rev-c1 14554 ms, same output.
The output is DRIFT on both only because my fixture's used-by names `entry.md` rather than `plain.md`.
Neither (b) nor (c1) has any control or selftest receipt in this suite; their value is performance-only and unguarded.

## 4. Flake risk (timing-dependent controls)
- `scale-4mib-leading-zeros` (timeout 60 s) is the only timing-sensitive control. cb895a2: 0.87–0.97 s, about 60× headroom, so low risk on the landed side.
- Its discrimination against dd72641 and rev-c2 is purely a timeout. dd72641 with 10× timeout: exit 0, contract-correct record, 67.38 s. The falsify report FC2Allzero128K07 measured 64.7 s.
- Headroom over the 60 s cap is only 7–12%, so on a host ≥~12% faster, or less loaded, dd72641 passes. The receipt's "4 mismatches on dd72641" then becomes 3. Deterministic content is 3 correctness mismatches plus 1 load-dependent performance mismatch.
- All 25 other controls: ≤0.03 s against 30 s timeouts. Negligible.
- Minor: an ENOSPC while writing the 4 MiB fixture (seen by FC2Allzero128K07 on this host's /tmp) would raise an uncaught Python exception, which exits 1. That reads as "mismatch", not the docstring's "exit2 setup".

## 5. Landed-gate counterexample the C3 controls miss (attacks change (a))
Change (a) counts header width GFM-style, but column indexes for id/status/used-by and the data-row cells still come from the naive `|` split.
`escaped-pipe-width` puts its `\|` in the LAST header cell, the only position where naive and GFM indexes agree.
Fixture: entry `source: S001` / `verified-at: 2026-01-02 checked synthetic fixture` / `recheck: 90d`. Registry:
`| id | note \| x | status | used-by |` / `|---|---|---|---|` / `| S001 | n | queued | mined | corpus/knowledge/entry.md |`
GFM truth (reference split in Python): `{'id':'S001','note | x':'n','status':'queued','used-by':'mined'}`, with excess cells ignored.
That should produce `META_SOURCE_NOT_MINED` (exit 1).
Command: `CHOUSA_STRICT=0 LC_ALL=C bash <rev>/tools/research-gate.sh verify-metadata $R/corpus/knowledge/entry.md --root $R --registry $R/reg.md`
- cb895a2: exit 0, `RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)`. **False CLEAN.**
- dd72641: exit 2, `metadata registry has no table with id, status, and used-by columns` (fails closed).
- 64eec5d: exit 0, CLEAN (base-identical wrong behavior).
Second shape: the 4-cell row `| S001 | n | mined | corpus/knowledge/entry.md |` gives a false DRIFT on cb895a2 (exit 1, NOT_MINED), and dd72641 exits 2.
Control: `| S001 | n \| queued | mined | … |` returns CLEAN on cb895a2. That is correct by coincidence, because header and row shift together.
Classification: wrong behavior in the landed gate. The outcome is inherited from base, but it regresses dd72641's fail-closed refusal into a silent false CLEAN.
Impacted axes: C3 calibration (exact used-by/status rules), and the provenance of the controls' declared GFM authority.
Smallest safe correction: derive `cells` for header column indexing, and for every data row, from the same escape-masked split used for width.
Concretely, split `${row//'\|'/<sentinel>}`. Alternatively, fail closed when the naive and GFM header cell counts differ.
Add a control with the fixture above expecting exit 1 plus `META_SOURCE_NOT_MINED`, and the 4-cell twin expecting exit 0 CLEAN.

## 6. Recommended suite corrections (author-lane advice)
1. Add the §5 pair of C3 controls (escaped pipe before a required column).
2. Either add performance controls for (b) and (c1) (the probes above discriminate 16× and 190×), or document both as performance-only changes this suite doesn't guard.
3. Report the dd72641 scale-4mib mismatch as timeout-dependent in receipts. Alternatively, raise the cap with a documented bound, or measure the work ratio instead of wall time.
4. Optional: a column-0 `RESEARCH_GATE: CLEAN` usage control, and mapping uncaught setup exceptions to exit 2.
