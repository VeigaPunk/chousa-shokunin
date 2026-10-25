# Round 38 — frozen claim design (v1)

Lane: chousa (deep-research method). Round: 38. Attempt: 1.

Frozen before the wave's independent runs; the L1's construction runs on seeds
38001/38011 (C1) and 38101/38111 (C2) preceded this freeze and are disclosed as
such (the waves and the closure re-derive on fresh seeds). Nothing in this file
changes after the first wave receipt: a later change is an erratum appended
below, never an edit.

Base lane tip at freeze: `95e33de8250ad9da8657d5af03958f4df53165f0` (round-37
closure; the round-37 landed gate `9fcac047…` is this tree's
`tools/research-gate.sh`).
Candidate gate `tools/research-gate.sh` sha256:
`37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d`.

Routed work this round: the round-37 routed-inputs queue — counter-strength
debt (receipts bind the gate hash only post-run, the residual F1/F4 findings)
and the `SHELLOPTS=noexec` false pin success / exported-`env` function witness
pair — plus the carried S070 anchor-label supersede row. Round-37 Errata 5/6
(the `BASH_FUNC_*` and `LD_PRELOAD` env leaks) are live context: C1 closes the
same export channel on the capture's `env` invocation itself; they are never
re-litigated.

## C1 — operability (lowest scored axis: operability 3/10)

**Claim.** The canonical pin capture's child runs through ONE pinned absolute
`env` (default `/usr/bin/env`, verified GNU coreutils; `RESEARCH_GATE_ENV`
override, absolute + GNU-reporting, refused exit 2 with `ENV_PROVENANCE` before
any mode runs), so a caller-exported shell function named `env` — delivered to
every child bash through `BASH_FUNC_env%%`, the round-37 Erratum-5 channel —
cannot interpose on the capture call: it can no longer re-add
`CHOUSA_GREP_PIN_ECHO` (baseline embeds a `GATE_GREP:` line, plain drift reports
phantom `-GATE_GREP`), re-add `CHOUSA_ROOT` (capture runs against a foreign
root), or suppress the capture.

Surface: `gate_canonical_capture` in `tools/research-gate.sh`, measured by
`corpus/evidence/round38/c1-count.py` against the frozen expectations in
`corpus/evidence/round38/expectations.jsonl`.

**P1 (frozen predicate).** C1 is met iff

```
python3 corpus/evidence/round38/c1-count.py --gate tools/research-gate.sh --seed N --receipt F
```

prints `ENV_PIN_CAPTURE_MATCH=7/7` with `predicate_holds=true` on each of two
fresh seeds against the landed lane revision, and no committed run of the same
counter against the landed gate prints a lower count. Code condition:
`matched == 7`; receipt labels `matched`, `predicate_holds`.

**Kill rule.** Any run against the landed gate below 7/7 kills C1; a run whose
receipt `gate_sha256` differs from the landed gate's is not the claim's
measurement; a scenario that passes by weakening its fixture (a benign function
the gate is expected to honour, an override the gate is expected to ignore) is
not a measurement.

**Before (measured).** Base gate `a7d3922c…` (committed byte-exact at
`.ufo/waves/round-37/controls/base-gate-r37.sh`): `ENV_PIN_CAPTURE_MATCH=2/7`
(`corpus/evidence/round38/receipts/c1-base-s38001.json`). The two holds pass;
the five separation cells fail exactly as the round-37 residual described:
echo re-add embeds one `GATE_GREP:` line with phantom `-GATE_GREP` drift, root
re-add moves the capture to a foreign root, suppress kills the capture
(`--pin` exits 2, no baseline), and the missing/fake override is ignored
(`--pin` exits 0).

**Cheapest control that skips the claimed work (committed).** The base gate is
the control: it is the exact bytes at the pre-round gate, it runs the same
seven scenarios, and it scores 2/7. A do-nothing lane commit cannot reach 7/7.
Receipt: `receipts/c1-base-s38001.json`.

## C2 — calibration (receipt binding strength)

**Claim.** A round-38 counter receipt binds, measured by the counter itself
(never by the gate under test): the gate file's sha256 immediately before the
first and after the last scenario invocation — a gate whose bytes change across
the run is refused, exit 2, with NO receipt published (the round-37 residual
F1: a self-rewriting gate got a receipt stamped with bytes that did not run
every scenario); the scoring counter's own sha256 (`counter_sha256`, the F4
hole: the receipt carried no counter identity); the frozen expectation table's
sha256 (`expect_sha256`); and the receipt body's own digest
(`receipt_sha256`). `verify-receipts.py` re-derives every binding from
committed bytes and fails closed (exit 1, named) on any mismatch, on any
doctored field, and on legacy round-37 receipts (missing binding fields).

Surface: `corpus/evidence/round38/c1-count.py` (binding fields and the
changed-gate refusal) and `corpus/evidence/round38/verify-receipts.py`,
measured by `corpus/evidence/round38/c2-count.py` against the frozen
expectations in `corpus/evidence/round38/expectations.jsonl`.

**P2 (frozen predicate).** C2 is met iff

```
python3 corpus/evidence/round38/c2-count.py --gate tools/research-gate.sh --seed N --receipt F
```

prints `RECEIPT_BINDING_MATCH=7/7` with `predicate_holds=true` on each of two
fresh seeds against the landed lane revision, and no committed run against the
landed gate prints a lower count. Code condition: `matched == 7`.

**Kill rule.** Any run against the landed gate below 7/7 kills C2; a scenario
that passes with the tamper/doctor undetected by verify-receipts is a kill; a
self-rewrite refusal that still publishes a receipt is a kill; a legacy receipt
verify that exits 0 is a kill.

**Before (measured).** The same c2 counter pointed at the round-37 c1 counter
(`--counter corpus/evidence/round37/c1-count.py`, the pipeline that produced
the round-37 receipts): `RECEIPT_BINDING_MATCH=0/7`
(`corpus/evidence/round38/receipts/c2-base-s38101.json`). The r37 counter
accepts the self-rewriting gate (F1 replay: 7/7 receipt, no refusal), its
receipts verify nowhere (no binding fields), and its tamper cells cannot even
construct an honest clean receipt.

**Cheapest control that skips the claimed work (committed).** The r37 counter
IS the control: it is the exact pre-round receipt pipeline, it runs the same
seven scenarios, and it scores 0/7. Receipt: `receipts/c2-base-s38101.json`.

## Separability

C1 changes the gate (the capture's `env` invocation and its startup pin); C2
changes the counters and adds the verifier (binding fields, changed-gate
refusal, `verify-receipts.py`). Either lands without the other: the c1 counter
scenarios assert pin/drift behaviour only, the c2 counter runs the same
receipt pipeline against any counter file, and the changed-gate refusal is
counter-side, gate-agnostic. Landing both in one round is a scheduling choice,
not a dependency; the wave's single-hunk mutants demonstrate each direction.

## Limits (named)

- C1 pins the capture's `env` invocation only. A caller-exported function named
  `bash` can still shadow the capture's bare `bash` call (the planned-list
  parent-function class); the grandchild `bash` lookup is the next witness,
  carried debt.
- C1's env pin does not scrub the loader environment of the `env` child — the
  Erratum-6 class on a second binary: an unprivileged `LD_PRELOAD` active for
  `/usr/bin/env` could strip the `-u` flags before they apply. The claim is
  function-export/PATH independence of the capture's env invocation, not
  loader hermeticity; the `env -u LD_PRELOAD …` scrub is carried debt with
  Erratum 6's fix direction.
- C1 does not cover `SHELLOPTS=noexec` (demonstrated again on the landed gate:
  `SHELLOPTS=noexec bash tools/research-gate.sh --pin P` exits 0 with no
  baseline): bash applies `-n` before the gate body executes, so no in-body
  fix exists — a pre-startup boundary would be a separately specified tool,
  carried debt per the round-37 residual.
- C1's provenance is self-reported like the grep pin: a binary that lies about
  `--version` is out of this check's reach.
- C2 does not make receipts trustworthy against a counter that lies end-to-end:
  a hostile gate that prints the expected strings still scores (black-box
  observability; the round-37 F2 residual). The receipts now bind WHICH counter
  and WHICH expectation bytes judged the run, and verify-receipts re-derives
  the arithmetic — a forger must attack committed bytes, not stdout alone.
- C2's seed namespaces only the fixture temp dirs; receipt content is
  seed-invariant (the r37 Erratum-4 class, carried).
- The r37 counters' receipts (e.g. round-37's own) are legacy shape: they fail
  closed under verify-receipts and are never re-stamped.

## Errata (appended; the body above is frozen)

**Erratum 1 (pre-dispatch, disclosed).** The C1 loader-env limit bullet was
inserted into §Limits after the freeze commit but before any wave ran (the
orchestrator's wave-1 dispatch followed it). It is integrated here as part of
the wave-1 landing; the body text is otherwise untouched.

**Erratum 2 (wave-1, C2 verifier kills — critical, closed pre-wave-2).**
CritC2Kill, CritTextOverreach, RevClaimsC2 and RevCounterC2 demonstrated that
the frozen verifier certified self-consistency only: re-sealed doctors keeping
`ok=true`, a re-bound legacy r37 receipt (public hashes + recomputed digest), a
c1 receipt rerouted under `--counter c2-count.py` (counter hash swapped to
c2's public hash + re-seal), doctored observations, and a vacuous empty
receipt all verified `ok` — contradicting the frozen sentence "fails closed on
any doctored field and on legacy round-37 receipts". Closed pre-wave-2:
`verify-receipts.py` now (i) binds the counter family and the frozen predicate
string, (ii) parses the expectation table it hashes and requires the exact
frozen scenario census, each row's `expect` tied to the frozen `expect`,
(iii) re-derives every `ok` from frozen expectations and the receipt's own
observations, and (iv) keeps the file bindings and arithmetic. All committed
receipts were regenerated under the strengthened pipeline. Narrowed reading:
verification certifies integrity and self-consistency against committed bytes,
NOT authorship — a fabricator holding the public hashes who reproduces honest
observations can write an indistinguishable receipt (the round-37 F2 residual,
verify side). Carried debt (r39): bind `verifier_sha256` into c2's receipts (a
replaced verifier currently re-adjudicates old receipts silently —
RevSeparability).

**Erratum 3 (wave-1, C2 tamper cells, closed pre-wave-2).** MutVerify,
RevCounterC2 and ScribeKnowledgeC2 found `doctor()` never re-sealed, so all
three tamper cells were caught at the receipt-self-digest check and the named
binding checks were unexercised; a verifier mutated to drop those checks still
scored 7/7. Closed: the counter/expect doctors re-seal and the exact verifier
refusal line is the asserted observable (`counter-sha256-mismatch` /
`expect-sha256-mismatch` / `receipt-self-digest`).

**Erratum 4 (wave-1, C2 cell coupling, closed pre-wave-2).** ExecDoNothingCtl,
RevSeparability and RevClaimsC2 found three c2 cells asserted the SUBJECT
counter's exit code, coupling C2's predicate to C1's gate fix (base gate:
4/7) and falsifying the §Separability sentence "c2 is gate-agnostic" ON THE
FROZEN BYTES. Closed: the three cells assert receipt existence and
verification only. Reading: C2's do-nothing control is the pre-round PIPELINE
(the r37 counter, 0/7); a tree landing only C2 (r38 counters, unfixed gate)
also scores 7/7 — that is separability, not a do-nothing path, because the
r38 counters ARE the claimed work.

**Erratum 5 (wave-1, harness hardening, closed).** RevCounterC1 found
`base_env()` left `BASH_ENV` live: a caller startup file is sourced by the
gate process itself (the gate's named r37 limit), and an ambient `BASH_ENV`
(unsetting the attack function, forging refusal tokens) moved even the r37
gate to 7/7 (seed 38219, report-only evidence). Closed: the scenario
environment scrubs `BASH_ENV`/`ENV`/`SHELLOPTS`/`BASHOPTS`, the gate
invocation pins `/usr/bin/bash` with timeouts, and the refusal observable is
the anchored `research-gate: ENV_PROVENANCE refused:` stderr line. Named: an
ambient PATH shim (the `bash` name) moves verdicts with gate bytes unchanged
(RevClaimsC1) — committed runs are made under a clean caller environment;
PATH coverage is a pre-registered r39 cell.

**Erratum 6 (wave-1, C1 narrowing).** RevErrataCtx, CritTextOverreach and
RevClaimsC1 found: (a) "closes the same export channel" overstates — only the
NAME `env` at the capture's one absolute-path call site is bypassed; the
`BASH_FUNC_*` channel itself is untouched (demonstrated: a parent-exported
`date` function still embeds a `GATE_GREP:` line and a phantom `-GATE_GREP`
drift on the landed gate — Erratum 5's symptom on a sibling name); (b) P1 does
not measure the absolute/PATH half — a mutant capture using PATH-resolved
`command env` scores 7/7 while being PATH-poisonable (demonstrated, seed
38207); (c) the `bash`-named limit misidentified the vector — the demonstrated
live witness is PATH resolution inside `env` (a PATH `bash` shim poisons the
landed gate's baseline; a suppressing `bash` function pins a crit-severity
`VERIFY_ALL_SECTION_UNAVAILABLE` baseline while `--pin` exits 0); (d) "two
fresh seeds" is label-level, not replication (C1's receipts are byte-identical
modulo seed/digest — the r37 Erratum-4 class; C2 disclosed it, C1 now does
too); (e) the r37-base control `a7d3922c…` is the pre-round-37 base — the
actual pre-round-38 gate `9fcac047…` scores 2/7 identically and is committed
as a second control (`.ufo/waves/round-38/controls/base-gate-r38.sh`,
receipt `c1-base2-s38003.json`). Narrowed reading: C1 asserts function-export
interposition on the capture's `env` invocation plus the override refusal
shape; the env pin's PATH-independence and hostile-drift coverage are
pre-registered r39 cells (an eighth scenario). P1 is unchanged: 7/7 on the
landed gate under a clean measurement environment.

**Erratum 7 (wave-1, minor, closed).** The counters refuse with exit 2 without
leaving a stale pre-existing `--receipt` (RevCounterC2 finding 7); both
counters hard-check the frozen 7 total so an edited-to-6 table cannot print a
passing 6/6 (RevClaimsC1 finding 1). The frozen P1/P2 sentences and counting
commands are unchanged; every erratum above names the wave-1 finding that
motivated it.

**Erratum 8 (wave-1, SentScope, closed).** (a) The c2 self-rewrite fixture
interpolated the caller's gate path into shell source unquoted — a gate
filename containing shell syntax executed as the counter user during scoring;
every interpolated path is now shlex-quoted. (b) Both counters now hash the
frozen expectation table BEFORE the scenarios and refuse with no receipt if it
changes across the run — the receipt binds the bytes the scenarios actually
scored, closing the measured-expectation/receipt-binding race. (c) The
sentinel's synthetic zero-execution receipt verified by design: verification
certifies integrity and self-consistency against committed bytes, NOT
execution authorship (Erratum 2's narrowed reading); the r37 knowledge docs'
stale "7/7 on every committed receipt" wording (receipt-audit finding L1) was
corrected in both files.

**Erratum 9 (wave-2, W2CritLaundering, closed).** Seven of the eight wave-1
doctoring fixtures refused under the strengthened verifier; the eighth — a
re-sealed receipt carrying an EXTRA unknown field — still verified, contradicting
the frozen "fails closed on any doctored field". Closed: verify-receipts now
enforces a strict schema (a receipt is exactly the known field set; an added
field refuses as `unknown-field` whether re-sealed or not). Receipts bind the
counters' bytes, not the verifier's, so the committed receipt set is unaffected;
the L1 notified the in-flight wave-2 verifier-testing seats of the mid-wave
edit, same disclosure pattern as the wave-1 integration.

**Erratum 10 (wave-2, W2RevVerifyFinal, closed/named).** Closed: malformed
scenario rows now refuse `scenario-row-malformed` (a traceback was reachable);
Python type-laundering now refuses (`ok-type-mismatch` / `count-type-mismatch` /
`predicate-holds-type-mismatch` — 1 == True and 7.0 == 7 no longer pass).
Named, not closed (the narrowed reading already bounds them): the strict schema
is top-level only (extra fields inside scenario rows are producer-controlled and
the load-bearing keys are re-derived); the receipt's provenance path strings are
not bound (path identity is not among the frozen bindings); pinning is to the
CLI-supplied bytes (a /tmp counter copy or a doctored table verifies against
itself — committed-tree membership is the caller's discipline, as with any
hash-checking tool). The `_contains` expectation annotations are producer-side
assertions; verify re-derives only the equality keys by design.

**Erratum 11 (wave-2, W2MutVerifyFinal/W2CritTextFinal, named).** The
strengthened verifier's census, ok-re-derivation, type and strict-schema checks
were verified by DIRECT wave-2 probes (W2RevVerifyFinal, W2CritVacuous: every
attack refuses with a named label), but the c2 COUNTER scenarios do not
discriminate a verifier weakened in exactly those checks: five of six verifier
mutants (accept missing gate_sha256_pre, drop pre!=post, case-insensitive
hashes, skip census, skip ok re-derivation) still score RECEIPT_BINDING_MATCH
7/7 (only the self-digest-skip mutant is caught, by the arithmetic recount).
Named, not closed: the seven cells bind the pre/post gate binding, the
counter/expect/receipt digests, legacy fail-closed and foreign-gate
discrimination; the remaining verifier checks are bound only through the
landed verifier's committed bytes — the carried verifier_sha256 debt
(Errata 2/8) is now demonstrated twice as the closing fix. Related named
items: the producer-side `_contains` refusal-label assertions are not
re-derived by verify (a doctored asserted label verifies; the equality keys
are re-derived); early counter refusals (before the stale-unlink runs) leave a
prior --receipt untouched (W2RevC1Final finding 6).

**Erratum 12 (wave-2, W2RevErrata/W2RevC2Final, closed).** Erratum 7's "refuse
without leaving a stale --receipt" sentence was falsified for the PRE-RUN refusal
paths (a missing gate exited 2 with a prior receipt intact — W2RevErrata finding 1):
the stale-receipt unlink now runs before every refusal path in both counters
(os.path.lexists, so dangling symlinks cannot redirect output either —
W2SentScopeFinal). Closed. Companion named items from the same audit, all already
bounded by the narrowed readings: the `_contains` refusal-label annotations are
producer-side (a re-sealed forged label verifies; the equality keys re-derive —
Errata 10/11); receipt provenance path strings (`seed`/`gate`/`subject_counter`)
are not bound (r39: bind `subject_counter_sha256`); the literal kill rule still
reads on the measurement environment (committed runs are clean-env — Erratum 5);
an embedded `date` witness needs `CHOUSA_GREP_PIN_ECHO=1` live to embed a line
(Erratum 6(a) demonstrated the embed; the echo-var condition is recorded in the
knowledge entry); and a `VERIFY: ok` certifies bindings, never the predicate
outcome — the 0/7 base receipt verifies with `predicate_holds=false` by design.

**Erratum 13 (wave-2, W2MutGateFinal, precision).** Erratum 6's narrowed reading says
C1 asserts "function-export interposition on the capture's `env` invocation plus the
override refusal shape" — the second half overclaims: the two override cells measure
ONLY the missing-override and non-GNU-override refusals. The relative-override refusal
(override not an absolute path) is part of the unmeasured half — the M3 mutant deleting
exactly that refusal scores 7/7 on every byte-set (seeds 38403/38423/38453). The
pre-registered r39 cell family (Erratum 6) already carries it: the relative-override
refusal scenario and the positive override-honoured witness land together as the new
frozen table's env-override cells. The gate's landed bytes do refuse relative overrides
(the refusal exists and the selftest exercises it at gate level); what the COUNTER
predicate does not measure is exactly the M3 class.

**Erratum 14 (routed defect D1, appended by round 39 — candidate-gate hash
supersession).** The body above names candidate gate sha256
`37e2b996…` (the pre-integration bytes at the freeze). The landed round-38
gate is `0447ad14b6135441f39f9220d02ae2967b810f791a2f1058654ee0c800c3b85a`
(the `870074e8…` tree: the +6-line `unset POSIXLY_CORRECT` hunk plus comment,
between `grep_pin_init` and `env_pin_init`; committed byte-exact at
`.ufo/waves/round-39/controls/base-gate-r39.sh` as the round-39 base
control). Per this file's own Erratum 6(e) precedent, hash supersessions are
named by erratum; the frozen P1/P2 blocks, counting commands and receipts are
untouched, and the nine receipts bind `0447ad14…` (re-derived by the r38
closure, 9/9).

**Erratum 15 (routed defect D2, appended by round 39 — harness-change
disclosure).** Between the freeze and the final bytes the counter harness
tightened without an erratum naming it: `base_env()` in both counters gained
the `PYTHON*` and `POSIXLY_CORRECT` scrubs (the W2RevC1Final/W2RevC2Final
child-environment findings), the c2 counter's subject children run under
`-E`, and per-call timeouts were raised. Tightening-only: every committed
receipt was regenerated under the tightened harness and re-verified; no
frozen expectation, predicate or counting command changed. Named here so the
harness history is complete.
