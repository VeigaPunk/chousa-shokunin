# Gate behavioral baseline r12 (re-pin record)

source: corpus/evidence/gate-baseline-r12-20261019T115519Z.json; tools/research-gate.sh (VERSION, gate_pin_fixture); LOG.md round-12 opening
verified-at: 2026-10-19T11:55:19Z (pin `GATE_PIN: ok`; immediate re-run `GATE_DRIFT: none` exit 0)
recheck: `bash tools/research-gate.sh --drift corpus/evidence/gate-baseline-r12-20261019T115519Z.json` after any gate edit (expect `GATE_DRIFT: none` exit 0)

## Why the r8 baseline was superseded (recorded reason, per the SKILL.md
## limits: re-pinning is a recorded act with a reason, never a way to turn
## red green)

Two deliberate contract changes make every capture differ from the r8
baseline, and both were wanted, so the re-pin is honest:

1. **Banner contract (claim 2a).** `VERSION` moved `research-gate-r1` → `v2`
   (revision token alone; the r1-era stutter `research-gate
   research-gate-r1` removed from all six banner sites). The version token is
   a declared contract word — NOT in `volatile_fields=ts gate_sha256` — so a
   version change is drift by design. Pre-re-pin, `--drift` against the r8
   baseline measured `GATE_DRIFT: GATE record_sha256` exit 1 (receipt
   `corpus/evidence/scope-r12-20261019T115519Z-drift-r8.log`): the `GATE`
   token names the changed banner line, `record_sha256` names change 2.
2. **Canonical fixture coverage (claim 1 hardening).** `gate_pin_fixture`
   gained one clean declaration row (`| domain | deep-research method |`).
   The record's sha256 is compared unmasked in the capture, so the fixture
   edit names `record_sha256`. The row puts the scope screen's clean path
   inside the canonical invocation: a pattern-widening regression that
   over-catches (e.g. bare `dispatch` / `swarm` triggers) now drifts this
   baseline instead of passing silently.

Also in the gate this round, behavior-stable on the canonical invocation
(measured `GATE_DRIFT: none` against this baseline at pin time): the
declared-scope screen, the 8 MiB source-read cap, and the linear `count_nl`
companion fix.

The r8 baseline (`gate-baseline-r8-20261016T033757Z.json`) stays committed as
history; nothing was rewritten. The volatile contract is unchanged
(`# volatile_fields=ts gate_sha256`).

Gate sha256 at pin time: `91a01695f64e9fd78907008e131e3a3d929ff0d62ab5a762f31fc6c199a0d538`
(pre-round: `46f5ddb39d5fafa220fb584121dba2f4a15e071a91fa42728849f3c7567c6ccd`).
