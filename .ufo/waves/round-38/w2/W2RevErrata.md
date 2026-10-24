# W2RevErrata

## Verdict
Errata 1-6, 8, 9 substantively close the wave-1 kills they name on the final bytes; **Erratum 7 is falsified** for every pre-run refusal path, and three residual holes survive under the narrowed reading: unbound `seed`/`gate`/`subject_counter` (RevCounterC2 HIGH 3, undisclosed), non-re-derived `*_contains` observations (Erratum 2/3 evidence layer), and nested extra fields (Erratum 9 is top-level only).

## Evidence
Snapshot named because the tree moved mid-run: lane tip `8e93bc916527b3c21f0f702967fa65c3b4c31699`; `verify-receipts.py` sha `3fc416612085a4ba8333b6b39a9ad2f4e32eb17ebcbc53ae6cd2e048f8abf919` and `claims.md` erratum-9 text were **uncommitted** (`git status` ` M`), verifier mtime 01:16:42. I froze `corpus/evidence/round38` + `tools/research-gate.sh` (sha `37e2b996…`) + both controls under `/tmp/chousa-r38-W2RevErrata/snap/` and measured there; my first c2 run (seed 38411) straddled the 01:16:42 swap and is reported only as corroboration.

```
C1 landed, seed 38401: ENV_PIN_CAPTURE_MATCH=7/7 (rc 0)
C2 landed, seed 38421: RECEIPT_BINDING_MATCH=7/7 (rc 0)
C2 gate=r38 pre-round control, seed 38422: 7/7 (rc 0)        # separability
C2 --counter round37/c1-count.py, seed 38423: 0/7 (rc 1)     # do-nothing control
C1 gate=r37 control a7d3922c, seed 38431 + hostile BASH_ENV: 2/7 (pre-fix: 7/7)
C1 landed + hostile BASH_ENV seed 38432: 7/7 ; SHELLOPTS=noexec caller seed 38433: 7/7
C1 landed + PATH shim named bash, seed 38434: 2/7; its receipt verify-receipts.py -> VERIFY: ok (rc 0)
C1 gate=r38 pre-round control, seed 38435: 2/7               # Erratum 6(e)
C1 mid-run table mutation (gate appends to expectations), seed 38453: rc 2, no receipt
C2 mid-run table mutation, seed 38462: rc 2, no receipt
C2 gate filename "g$(touch${IFS}INJ).sh", seed 38471: 7/7, no INJ marker
stale --receipt + missing gate: c1 rc 2 stale_exists=yes; c2 rc 2 stale_exists=yes
verifier sweep, 9 committed receipts: 9/9 VERIFY: ok (2/7, 2/7, 0/7 controls included)
mutant verifier dropping counter+expect bindings -> C2 5/7 (was 7/7)
gate selftest, final gate bytes: RESEARCH_GATE_SELFTEST: PASS (272 cases, 0 skipped), rc 0
```
Verifier attacks (re-sealed bodies, snapshot verifier): extra top-level field -> `unknown-field added`; row expect emptied -> `expect-tie-mismatch`; empty scenarios -> `scenario-census-mismatch`; equality observation flipped -> `ok-rederivation-mismatch`; row `ok` false->true -> `ok-rederivation-mismatch`; legacy r37 body hash-spliced -> `predicate-mismatch`; c1 receipt spliced to c2 hash -> `predicate-mismatch`; **seed=999999 -> ok**, **gate path -> ok**, **c1 + `subject_counter` -> ok**, **`observed.verify_fail` emptied or forged -> ok**, **`observed.invented=true` -> ok**.

## Findings
1. **MEDIUM — Erratum 7's stale-receipt sentence is false for pre-run refusals.** "The counters refuse with exit 2 without leaving a stale pre-existing `--receipt`" holds only for the mid-run gate/table refusals: `os.unlink(args.receipt)` sits after the gate/expectations/tmp validation in both counters (`c1-count.py:246-252`, `c2-count.py:293-300`), so a missing gate exits 2 with the stale file untouched (measured above, both counters). Same hazard the erratum says is closed; a consumer reading `--receipt` after a refusal can take a prior 7/7 receipt for this run. RevCounterC2 finding 7 (Medium) is only half-closed.

2. **MEDIUM — the verifier does not re-derive `*_contains` observations, so the exact refusal label is not bound into the receipt.** `ok = all(observed.get(k) == v for k,v in want.items() if not k.endswith("_contains"))` (`verify-receipts.py:150-156`) skips exactly the three `verify_fail_contains` expectations (`expectations.jsonl:c2`), while the counter's own `ok` checks them (`c2-count.py:230-236`). A re-sealed rewrite of `observed.verify_fail` to `""` or to a forged label verifies `ok` with `ok:true` retained. That contradicts Erratum 2(iii) ("re-derives every ok ... from the receipt's own observations") and makes Erratum 3's "the exact verifier refusal line is the asserted observable" true only at scoring time, not in committed evidence; the verifier's model of `ok` differs from the counter's, so a future counter that drops the label test would still verify.

3. **MEDIUM — unbound identity fields survive; RevCounterC2 HIGH 3 is only half-closed and the surviving half is unnamed.** Seed-, gate-path- and `subject_counter`-only rewrites with a re-sealed digest verify rc 0 (A2/A3/A4b above). Erratum 2 closes the counter reroute only, and its narrowed reading covers authorship, not field integrity; no erratum lists `seed`/`gate`/`subject_counter` as carried debt. The docstring's "any field doctoring is detected" (`verify-receipts.py:17-18`) is false for these fields. Rule (c) gap: a HIGH finding's mechanism remains reachable with no erratum naming it.

4. **LOW — Erratum 9's strict schema is top-level only; the nested variant of CritC2Kill finding 4 still verifies.** `KNOWN = set(REQUIRED) | {...}` and `set(receipt) - KNOWN` inspect only top-level keys (`verify-receipts.py:66-73,125-127`); `observed.invented=true` re-sealed verifies ok. The erratum's own wording ("a receipt is exactly the known field set") survives a top-level reading, but the frozen sentence it cites ("fails closed on any doctored field") does not: nested doctoring is accepted. Placement before the self-digest is confirmed (`unknown-field added` fires on the unre-sealed copy too).

5. **MEDIUM — the P1 kill rule remains environment-triggerable and no erratum qualifies it.** With a caller `PATH` shim named `bash` (exports `CHOUSA_GREP_PIN_ECHO=1`, execs `/usr/bin/bash`), the landed gate scores 2/7 (seed 38434); the receipt binds landed gate `37e2b996…` pre==post and verifies rc 0, so it is indistinguishable from the claim's measurement except in the count. RevClaimsC1 HIGH 2 is named as a limit by Errata 5/6, but Erratum 7 states the P1/P2 kill sentences are unchanged, so the frozen rule still says "any run below 7/7 against the landed gate kills C1" while the errata admit a harness artifact produces one. The narrowed reading should qualify the measurement environment in the kill rule, not only in §Limits.

6. **LOW — Erratum 6(a)'s `date` witness reproduces only half.** A parent-exported `date` function forging `GATE_GREP:` gives pin rc 0 with 1 embedded `GATE_GREP:` line on the landed gate (the `BASH_FUNC_*` channel is open, as claimed), but a clean `--drift` then reported `GATE_DRIFT: none` rc 0, not the claimed phantom `-GATE_GREP`/rc 1. Either my reconstruction differs from RevErrataCtx's fixture or the drift half is stale; recorded as a verification gap, not a count.

7. **LOW — the anchored refusal observable does not assert the reason.** `research-gate.sh` refusals collapse to `l.startswith("research-gate: ENV_PROVENANCE refused:")` (`c1-count.py:196-204`), and the two override cells expect the identical token `ENV_PROVENANCE` for distinct causes (missing vs non-GNU override). RevCounterC1 finding 3 asked for the full line plus expected reason; Erratum 5 claims only the anchor, so this is a partially-closed Medium, not an overclaim.

8. **LOW — `VERIFY: ok` stays ambiguous between predicate and before-state.** `c2-base-s38101.json` (0/7, `predicate_holds:false`, hard-coded `RECEIPT_BINDING_MATCH=7/7`) prints `VERIFY: ok`. Erratum 2 discloses that all receipts (including controls) verify; no erratum tells consumers to read `matched` rather than rc. RevCounterC2 HIGH 4's consumer hazard therefore persists by design.

9. **LOW/PROCESS — the wave-2 snapshot moved mid-measurement (disclosed).** `verify-receipts.py` `b63e7e20…→3fc41661…` at 01:16:42 and claims Erratum 9 at 01:16:54, uncommitted, while wave-2 seats measure. Erratum 9's non-effect on receipts is verified (9/9 ok); the same disclosure pattern as the wave-1 integration. Recorded so wave-2 verdicts can name their verifier sha.

Per-erratum verdicts: **E1** disclosed, body bullet present (§Limits LD_PRELOAD); **E2** closed for the four named kills (legacy re-bind, counter reroute, doctored equality observations, vacuous receipt) — residuals F2/F3; **E3** closed (mutant 5/7; rows carry `counter-sha256-mismatch` / `expect-sha256-mismatch` / `receipt-self-digest`) — F2 caveat; **E4** closed (7/7 base gate, 0/7 r37 counter, no `counter_rc` on the three cells); **E5** closed for BASH_ENV/ENV/SHELLOPTS/BASHOPTS + pinned `/usr/bin/bash` + 180 s timeouts — F5/F7 residuals; **E6** closed as narrowing (PATH half live; 2/7 second control; seed inert — committed c1 receipts identical modulo seed/digest/gate) — F6 gap; **E7 falsified** (F1); **E8** closed `(a)` metachar gate path no execution, `(b)` both counters refuse rc 2 no receipt; **E9** closed top-level — F4 nested residual.
HIGH+ census: RevClaimsC1 H1→E7, H2→E5/E6; RevClaimsC2 C1→E4+regenerated receipts, H2→E2; RevCounterC1 H1→E5, H2→E6; RevCounterC2 C1→E2/E4, H2→E2, H3→E2 only in part (F3), H4→E7/E2 (F8); RevSeparability B1→committed integration, H2→E4; SentScope H1→E8(a); MutVerify 1-5→E3; CritC2Kill 1-3→E2, 4→E9 (F4). No HIGH+ finding is wholly unmapped.

## Limits
Rebuilt fixtures for E6(a) and E5 refusal-reason are my own reconstruction, not the seats' exact commands. `base-env` PATH is deliberately unscrubbed, so all committed-run claims are conditional on a clean caller PATH. The mutant verifier was one representative (counter+expect checks removed), not MutVerify's M1-M4 matrix. `bash tools/research-gate.sh --selftest` on the final gate bytes: `RESEARCH_GATE_SELFTEST: PASS (272 cases, 0 skipped)`, rc 0. No tools installed; writes only under `/tmp/chousa-r38-W2RevErrata/` and this report. Seeds 38401, 38411, 38421-38423, 38431-38435, 38441, 38451-38453, 38461-38462, 38471.
