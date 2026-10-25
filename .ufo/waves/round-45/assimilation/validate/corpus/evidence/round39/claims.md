# Round 39 — frozen claim design (v1)

Lane: chousa (deep-research method). Round: 39. Attempt: 1.

Frozen before the prepared wave's independent runs; the L1's construction runs
on seeds 39001/39011 (C1) and 39101 (C2) preceded this freeze and are
disclosed as such (the orchestrator-dispatched wave and the hyaku closure
re-derive on fresh seeds). Nothing in this file changes after the first wave
receipt: a later change is an erratum appended below, never an edit.

Base lane tip at freeze: `8c7c867b66e103712ae33e1d076786f50dd3239e`
(round-38 closure; the pre-round-39 gate is this tree's
`tools/research-gate.sh`).
Pre-round gate `tools/research-gate.sh` sha256:
`0447ad14b6135441f39f9220d02ae2967b810f791a2f1058654ee0c800c3b85a`
(committed byte-exact at `.ufo/waves/round-39/controls/base-gate-r39.sh`).

Routed work this round (round-38 closure routed defects D1–D7): the
pre-registered measurement cells from round-38 claims Errata 5/6/11 — the
eighth c1 scenario family (PATH `env` shim, PATH `bash` shim, hostile drift,
positive override-honoured witness, relative-override refusal) and the
`verifier_sha256` + `subject_counter_sha256` receipt bindings — plus the
defect repairs D1–D6 (claims.md errata, harness-change disclosure, erratum
counts, final-bytes attribution, the SKILL.md gates-table row, the lesson Gate
records).

## C1 — operability (lowest scored axis: operability 3/10)

**Claim.** The canonical pin capture's grandchild runs through ONE pinned
absolute `bash` (default `/usr/bin/bash`, verified GNU-reporting;
`RESEARCH_GATE_BASH` override, absolute + GNU-reporting, refused exit 2 with
`BASH_PROVENANCE` before any mode runs), and the verify-all section children
reachable from that capture run through the same pin — so a caller PATH `bash`
shim cannot interpose on the capture in either place: it can no longer
re-add `CHOUSA_GREP_PIN_ECHO` (baseline embeds a `GATE_GREP:` line; a plain
`--drift` reports a phantom `GATE_DRIFT: -GATE_GREP`) nor suppress the
capture (`--pin` refuses, or sections read
`VERIFY_ALL_SECTION_UNAVAILABLE`), and a non-absolute / non-GNU override is
refused before any record is read.

Surface: `gate_canonical_capture` and `verify_all_section` in
`tools/research-gate.sh`, measured by `corpus/evidence/round39/c1-count.py`
against the frozen expectations in
`corpus/evidence/round39/expectations.jsonl`.

**P1 (frozen predicate).** C1 is met iff

```
python3 corpus/evidence/round39/c1-count.py --gate tools/research-gate.sh --seed N --receipt F
```

prints `ENV_PIN_CAPTURE_MATCH=8/8` with `predicate_holds=true` on each of two
fresh seeds against the landed lane revision, and no committed run of the same
counter against the landed gate prints a lower count. Code condition:
`matched == 8 and total == 8`; receipt labels `matched`, `predicate_holds`.

**Kill rule.** Any run against the landed gate below 8/8 kills C1; a run whose
receipt `gate_sha256` differs from the landed gate's is not the claim's
measurement; a scenario that passes by weakening its fixture (a shim that does
not re-add after the `-u` list, an override the gate is expected to ignore)
is not a measurement.

**Before (measured).** Pre-round gate `0447ad14…` (committed byte-exact at
`.ufo/waves/round-39/controls/base-gate-r39.sh`): `ENV_PIN_CAPTURE_MATCH=7/8`
(`corpus/evidence/round39/receipts/c1-base-s39001.json`, seed 39001). The
seven round-38 scenarios hold; the eighth family fails live exactly as
round-38 claims Erratum 6(c) described: `path_bash_shim_echo` embeds one
`GATE_GREP:` line and the drift reports `GATE_DRIFT: -GATE_GREP` (the
hostile-drift vector), `path_bash_shim_suppress` kills the capture
(`pin_rc=2`, no baseline), `override_relative_refused` is ignored
(`pin_rc=0`, no refusal); the PATH `env` shim cell holds (the env pin is
round-38 work).

**Discrimination controls (committed).** A single-hunk mutant of the landed
gate with the capture's `"$ENV_BIN"` replaced by a bare `env`
(`.ufo/waves/round-39/controls/mut-gate-path-env.sh`, sha256
`e1251030…`) scores `4/8` (seed 39013,
`corpus/evidence/round39/receipts/c1-mutenv-s39013.json`): the three
round-38 `BASH_FUNC_env%%` cells re-open (bash resolves the function before
PATH) AND `path_env_shim_echo` fails (`echo_lines=1`, drift `-GATE_GREP`) —
the counter discriminates a PATH-poisonable capture from the pinned one. The
base gate is the do-nothing control: a lane commit without the bash pin
cannot reach 8/8.

## C2 — calibration (verifier and subject binding)

**Claim.** A round-39 counter receipt binds, measured by the counter itself
(never by the gate under test): everything the round-38 receipt bound
(pre==post gate hashes, counter/expect/receipt digests, census-tied
verification), PLUS `verifier_sha256` — the digest of
`corpus/evidence/round39/verify-receipts.py` at receipt time — and, for
c2-family receipts, `subject_counter_sha256` — the digest of the subject
counter the run measured, bound alongside its path. `verify-receipts.py`
re-derives both from committed bytes and fails closed: a replaced (weakened
or doctored) verifier copy refuses `verifier-sha256-mismatch`; a c2 receipt
re-pointed at a different or doctored subject refuses
`subject-counter-sha256-mismatch` (or `subject-counter-unreadable` when the
named path does not resolve). This closes the round-38 Erratum 2/11 carried
debt — "a replaced verifier currently re-adjudicates old receipts silently" —
demonstrated live twice in round 38.

Surface: `corpus/evidence/round39/c1-count.py` and
`corpus/evidence/round39/c2-count.py` (binding fields) and
`corpus/evidence/round39/verify-receipts.py`, measured by
`corpus/evidence/round39/c2-count.py` against the frozen expectations in
`corpus/evidence/round39/expectations.jsonl`.

**P2 (frozen predicate).** C2 is met iff

```
python3 corpus/evidence/round39/c2-count.py --gate tools/research-gate.sh --seed N --receipt F
```

prints `RECEIPT_BINDING_MATCH=8/8` with `predicate_holds=true` on each of two
fresh seeds against the landed lane revision, and no committed run against the
landed gate prints a lower count. Code condition: `matched == 8 and total ==
8`.

**Kill rule.** Any run against the landed gate below 8/8 kills C2; a receipt
verified ok by a verifier other than the bound bytes is a kill; a re-pointed
subject that verifies without `subject-counter-sha256-mismatch` is a kill; an
r38-generation receipt that verifies under this verifier is a kill.

**Before (measured).** The round-38 pipeline IS the control: its receipts
carry no `verifier_sha256`/`subject_counter_sha256`
(`corpus/evidence/round38/receipts/*.json` — e.g. `c1-after-s38001.json`
binds only the r38 field set), and its verifier accepted five of six
weakened-verifier mutants silently (round-38 claims Erratum 11, measured).
Under this round's verifier the committed r38 receipt refuses
`predicate-mismatch` (generation binding; L1 re-run
`verify-receipts.py --receipt corpus/evidence/round38/receipts/c1-after-s38001.json
--gate tools/research-gate.sh --counter corpus/evidence/round38/c1-count.py
--expectations corpus/evidence/round38/expectations.jsonl` →
`VERIFY-FAIL: predicate-mismatch`), and an r39 receipt with the verifier
binding stripped refuses `missing-field verifier_sha256` (the c2 counter's
`legacy-receipt-refused` cell, run live). The before count for the predicate
machinery is the round-38 counter shape: the same eight-scenario run is
impossible without the new bindings — every pre-round receipt refuses them.

**Cheapest control that skips the claimed work (committed).** The r38
receipts are the control bytes: they ran the same receipt pipeline shape
without the new bindings and fail closed under the new verifier; a do-nothing
lane commit cannot make an r38 receipt verify, nor print 8/8 from a counter
that has no eighth scenario.

## Separability

C1 changes the gate (the capture/section bash invocations and the
`bash_pin_init` startup pin); C2 changes the counters and the verifier
(binding fields, family-specific required sets, named refusal labels). Either
lands without the other: the c1 counter's scenarios assert pin/drift behaviour
only and its receipts carry `verifier_sha256` regardless of the gate fix; the
c2 counter runs the same receipt pipeline against any gate bytes and its
predicate does not touch the bash-pin cells (base gate: C2's subject receipts
still bind and verify — receipt binding is gate-agnostic, the round-38
Erratum-4 reading). The discrimination controls isolate each direction:
C1-only (r38 gate + r39 counters) scores 7/8 with all C2 machinery inert;
C2-only (landed-gate-intent counters against r38 receipts) refuses every
pre-round receipt.

## Limits (named)

- C1 pins the `bash` NAME at the capture child, the capture grandchild, and
  the verify-all section children. Other bare names reachable from the
  capture stay the caller's: `mktemp` and `sed` (in `gate_canonical_capture` /
  `gate_drift_normalize`) and `rm` are not pinned — a PATH shim for those is
  the same class on sibling names, carried debt (the `BASH_FUNC_*` channel is
  likewise closed only for the pinned names; an exported function named
  `sed`/`mktemp` keeps the r37-erratum class elsewhere).
- The loader environment of the env/bash children is the caller's: an
  unprivileged `LD_PRELOAD` active for `/usr/bin/env` or `/usr/bin/bash`
  could strip the `-u` flags (round-38 claims Erratum 1/6 class); the
  `env -u LD_PRELOAD -u LD_LIBRARY_PATH …` scrub stays carried debt.
- `SHELLOPTS=noexec` disables the whole gate body before any pin runs
  (round-37 residual, carried; a pre-startup boundary would be a separately
  specified tool).
- A pinned binary that lies about `--version` is out of reach (self-reported
  provenance, as the grep and env pins).
- C2 binds WHICH verifier and WHICH subject-counter bytes judged a run; it
  does not authenticate authorship — a fabricator holding the public hashes
  who reproduces honest observations can write a self-consistent receipt (the
  round-37 F2 residual, narrowed not closed). Re-pointing a c2 receipt WITH a
  re-derived subject digest is a new honest receipt, not a forgery of an old
  one.
- The `_contains` expectation annotations remain producer-side assertions;
  verify re-derives only the equality keys (round-38 Erratum 11's named
  remainder, carried).
- Receipt-path symlink identity is not bound (the body is what is verified);
  pinning is to the CLI-supplied bytes — committed-tree membership is the
  caller's discipline.

## Errata (appended; the body above is frozen)

Round-40 append-only erratum (2026-10-24; the frozen body above is unchanged).

- **R1 — stale expectation bindings.** The committed `expectations.jsonl` hashes to `01cbdc3a8208a257e2b0ea4304c87a6d74be313a722cf667c5d126a4c29c583a`; the four old c1 receipts bind `3abd2dcb1766c404228cf3929024856240a93ea374760ab77a390b92c3fb6480`. Three stale active measurements were reissued against the committed expectations bytes as `corpus/evidence/round40/receipts/c1-base-s39001-regenerated.json`, `c1-after-s39011-regenerated.json`, and `c1-mutenv-s39013-regenerated.json`. The old r39 files remain unchanged. The fourth, `c1-mutenv-s39003.json`, is the superseded draft described in R2 and is not an active measurement.
- **R2 — committed superseded draft.** `corpus/evidence/round39/receipts/c1-mutenv-s39003.json` is committed despite the r39 lesson's “not committed” wording. Preserve it as superseded; it binds an uncommitted counter digest and is excluded from the active set. The r39 receipt directory had seven JSON files, not six.
- **R3 — knowledge count correction.** The r39 report's `29 → 31` is wrong; the historical `corpus/knowledge/*.md` count was `50 → 52` at the r39 before/tip commits `8c7c867b66e103712ae33e1d076786f50dd3239e` and `6ac1007e6a5d699d0742801026554fac1d900b5d`. Re-derive with `for r in 8c7c867b66e103712ae33e1d076786f50dd3239e 6ac1007e6a5d699d0742801026554fac1d900b5d; do printf '%s ' \"$r\"; git ls-tree -r --name-only \"$r\" -- corpus/knowledge | awk '/\\.md$/ {n++} END {print n+0}'; done`.
- **R4 — not reproduced from committed artifacts.** The r39 report, committed `w1-spec.json`, and generated `w1-plan.json` all count reviewer 6 / revenger 2 (32 total r39 seats). The verifier spot-check instead says the r39 spec was reviewer 8 / revenger 0. Round 40's independently prepared 33-seat spec is not part of the r39 comparison. No r39 role-mix change is made on contradictory evidence; the exact comparison is recorded in `corpus/evidence/round40/routed-defect-dispositions.json`.
- **R5 — runner wording correction.** The SCORECARD phrase “two independent runners” is unsupported: the frozen claims disclose that both cited C1 runs were L1 construction runs and the wave was prepared, not dispatched. The phrase is superseded by “two seeds, both L1 construction runs”; the SCORECARD correction is appended in round 40.
