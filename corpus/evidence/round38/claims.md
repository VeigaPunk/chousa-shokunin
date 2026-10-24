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
