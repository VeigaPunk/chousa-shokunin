# Round 71 claims (frozen 2026-11-01 at commit A, against base `11b51988d3878cd33b826295304f6f266718ba86`)

Host: Windows/11, `python -I` (3.13.15) replaces `python3` (the WindowsApps alias is a
non-running stub — the r70 correction stands; the battery's PY3 probe measures capability).
`timeout` (GNU coreutils, /usr/bin/timeout) is present and KILLS on this host — measured at
the freeze (`controls/probe-timeout-capability-r71.txt`: probe rc 124; the case-258 body
uncontended: 16.333 s, CLEAN). `flock(1)` is still absent — the L0 flock question is standing
open and is routed around, never treated as answered; the capture-zone cases still fail by
name and the gate stays red. No fetch this round — every ground is own-work committed bytes
opened this round (S173–S176). No wave: this host has no batched dispatch surface (L0
template question standing open; round-63 attempt-2 precedent, disclosed). Verdicts rest on
committed counters, controls and receipts.

Trigger: the round-70 closure spot-check (`corpus/lessons/round-70-verifier-spotcheck.md`,
S173) routed six defects (D-70-1..6, §5 there) and the r70 lesson routed the unbounded
locale-boundary case (the D5 class) to this round. Carry-in first, then the re-pursuit.

## C1 — operability (lowest-scored non-retired axis, 3/10)

The r70 battery repair (crash guards, capability probes, the six append-subject skips) is
landed and its transcripts are truthful, but the battery still cannot COMPLETE on this host:
the case-258 gate (claims-locale-boundary, the 16K-accent multibyte span across the
32764-byte direct/chunk boundary) is UNBOUNDED — >70 min without emitting its line in the
r70 final run, 16.3 s uncontended at this freeze (probe receipt above). The routed remedy is
"a bound for the unbounded locale-boundary case (timeout-wrap or by-name skip, its coverage
cost spelled out)". This round lands the timeout-wrap — the coverage-preserving arm (the case
still RUNS and its verdict is measured whenever it finishes within budget; a by-name skip
would measure nothing forever):

  a. `tools/research-gate.sh`, inside `run_selftest` only (every hunk inside the function the
     r70 repairs already live in; no case's input, expected rc, or expected token changes):
     a one-time `HAVE_TIMEOUT` capability probe next to the r70 `HAVE_FLOCK`/`PY3` probes —
     capability, not existence: the probe requires `timeout 1 sleep 5` to be KILLED (rc 124),
     not merely found; a budget constant `LC_BOUNDARY_BUDGET_S` (default 900 s,
     overridable, ~55x the measured uncontended duration); the case-258 invocation runs under
     `timeout "$LC_BOUNDARY_BUDGET_S"` when `HAVE_TIMEOUT=1` (otherwise base behavior —
     unbounded — is preserved verbatim for hosts without a capable timeout(1)); on budget
     expiry the case prints its FAIL-case line with rc 124 plus a named case-note (budget
     exceeded, verdict unmeasured within the budget) and counts as a failure — never a pass,
     never a fake. Coverage cost, spelled out: a case whose verdict needs more than the budget
     is recorded as a named timeout failure, not silently dropped and not passed; the battery
     trades a possible hang for a possible honest FAIL — no case's expected outcome changes.
  b. after-predicates, measured at the landing tip (do-nothing control first):
     CONTROL (what a do-nothing round cannot reach): at the base bytes the battery has NO
     verdict line on this host — `grep -c "^RESEARCH_GATE_SELFTEST:"` over the committed r70
     transcript `corpus/evidence/round70/controls/after-battery-completes-r70.txt` → 0
     (anchored form per the D-70-2 correction; the run ended at case 258 per its RUN-END
     ADDENDUM, re-derived by the non-author spot-check §2 C1);
     `controls/after-battery-completes-r71.txt` — the bounded battery's own run at the
     landing COMPLETES and prints its verdict line (`grep -c "^RESEARCH_GATE_SELFTEST:"` → 1,
     the transcript carrying it as the only anchored hit; rc read by immediate `rc=$?` after
     the redirected command, no pipeline), the case-258 line printed (ok-case or named
     timeout), and the receipt header never begins a line with the verdict token (the
     D-70-2 lesson is applied to this round's own receipts);
     `.ufo/waves/round-71/preflight-final.txt` (copied to
     `controls/after-full-preflight-r71.txt`) — the preflight with NO `--skip` and
     `G08_SELFTEST_BUDGET_S=1800` (measured: the bounded battery must fit the budget; the
     r70 override mechanism unchanged): `SKIPPED=none` present (`grep -c "SKIPPED=none"` → 1),
     the G08 line naming its real result (expected still FAIL — the gate stays red without
     flock; the GATE is NOT claimed improved), `EXIT=` by immediate `rc=$?`;
     both receipts pin the measured tools' sha256 and the pins re-derive at HEAD via
     `tools/digest-in-tree.py`.

  Verdict rule, frozen before measurement: battery completes with verdict line (anchored
  count 1) + preflight completes with `SKIPPED=none` → C1 improved ON THAT PREDICATE (the
  completing-battery arm the r70 rule named, now met by measurement; the gate's red state is
  disclosed everywhere it is cited and the operability SCORE remains its historical 3/10 —
  this round moves the predicate, not the score); if the bounded battery still dies before
  its verdict line, or the preflight cannot complete within its budget, C1 lands honest-stop
  again with the red receipts committed as the defect record and the residual routed (the
  remaining arm would be the by-name skip with its coverage cost, or the operator's flock
  decision); no predicate is edited after measurement.

  Counting commands (paste-able; receipts name the revision measured):
  `grep -c "^RESEARCH_GATE_SELFTEST:" corpus/evidence/round70/controls/after-battery-completes-r70.txt` → 0 (control, base)
  `grep -c "^RESEARCH_GATE_SELFTEST:" corpus/evidence/round71/controls/after-battery-completes-r71.txt` → 1
  `grep -c "SKIPPED=none" corpus/evidence/round71/controls/after-full-preflight-r71.txt` → 1
  `grep -c "reason=no flock(1): append fails closed" corpus/evidence/round71/controls/after-battery-completes-r71.txt` → 6
  (the sixth append-subject skip, case 259, finally prints — the run passes 258)

## C2 — calibration (sourced on S173, opened this round)

The five status-neutral defects the r70 spot-check routed (D-70-1..5; D-70-6 is a note, not
a defect, and is answered by letting a rejection surface in this round's search log). Each
fix is append-only — the r70 bytes stay as committed history; the correction is the record —
and each carries its own counting command, measured in
`controls/before-r71-defect-greps.txt` (before) and `controls/after-r71-corrections.txt`
(after):

  1. S171 re-anchor (D-70-1): the "verbatim" crash quote was attributed to
     `controls/recon-run-r70.txt`, whose crash lines carry tmpdir `K1Yhut` and the full
     scratch path (19 K1Yhut hits, 0 dcCFup); the quoted bytes live in the sibling capture
     `controls/before-g08-selftest-partial.txt` (7 dcCFup hits). Fix: correction row S176 in
     `corpus/SOURCES.md` (`supersedes S171 —` for the location attribution only; S171's
     teaching and tier stand) + a `correction:` block appended to `corpus/lessons/round-70.md`.
  2. Counting-command collision (D-70-2): the r70 no-verdict-line command
     `grep -c "RESEARCH_GATE_SELFTEST:" …` returns 1 over the committed bytes because the
     receipt's own header quotes the frozen predicate (line 4); the true fact is the anchored
     form's 0. Fix: the C2 correction block states the anchored command and both counts
     (measured in the before-receipt); rule applied forward — this round's receipts never
     begin a line with a token a counting command greps unanchored.
  3. "Six skips print" is five-of-six (D-70-3): the committed r70 transcript carries five of
     the six append-subject skips (`grep -c "reason=no flock(1): append fails closed"` → 5);
     the sixth (`all-manifest-hash-shim`, case 259) sits after the ended-at case 258 and
     could not print. Fix: the correction block states five-of-six with the count and the
     reason; C1's completing run then shows all six (separable: this correction is about the
     r70 bytes and verifies whether or not C1 lands).
  4. The "/269" denominator (D-70-4): unsupported as written. Fix: the correction block
     replaces it — the r70 transcript's honest statement is "case 257, run ended at case
     258"; the denominator a verdict line would print is the battery's own case counter,
     which counts skip-case lines too (the r70 transcript numbers 257 cases with 12 skips
     among them; the registry's canonical completing run is 275 cases, 0 skipped — the
     r70 "269" was an invalid 275−6 derivation); C1's completing verdict line then states
     the measured N.
  5. SKILL registry row 83 (D-70-5): the row asserts a completing FAIL verdict its own cited
     receipt does not show. Fix: the row's host-conditional cell is corrected in place to the
     measured state (r70: truthful through case 257, ended at case 258, no verdict line,
     honest-stop per the frozen rule; r71: whatever this round's receipts then show — the
     row is written after measurement and cites the receipts it asserts).

  Limits, frozen with the claim: all five fixes are status-neutral records work — no verdict
  of the r70 round changes (it stays honest-stop/not-admitted as closed by the non-author
  spot-check); the corrections do not touch the frozen claims files or the r70 receipt bytes
  (the RUN-END ADDENDUM's "257/269" stays as committed history, corrected by C2's record, not
  rewritten).

  Counting commands:
  `grep -c "dcCFup" corpus/evidence/round70/controls/recon-run-r70.txt` → 0 (unchanged; the mis-attribution's ground)
  `grep -c "supersedes S171" corpus/SOURCES.md` → 0 before → 1 after
  `grep -c "^correction: corpus/lessons/round-70.md D-70" corpus/lessons/round-70.md` → 0 before → 1 after
  `grep -c "^RESEARCH_GATE_SELFTEST:" corpus/evidence/round70/controls/after-battery-completes-r70.txt` → 0 (the corrected command, true value unchanged)
  `grep -c "reason=no flock(1): append fails closed" corpus/evidence/round70/controls/after-battery-completes-r70.txt` → 5 (the r70 bytes' true count, now stated)
  `grep -c "the battery completes and prints" SKILL.md` → 1 before → 0 after (the asserting literal leaves row 83)
