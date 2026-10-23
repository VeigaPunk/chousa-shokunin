# Round 36 — frozen claim design (v1)

Lane: chousa (deep-research method). Round: 36. Attempt: 1.
Frozen before the wave's independent runs; the L1's construction runs on seeds
36001/36011 preceded this freeze and are disclosed as such (the wave and the
closure re-derive on fresh seeds). Nothing in this file changes after the first
wave receipt: a later change is an erratum appended below, never an edit.

Base lane tip at freeze: `86bfc0f4f63c4e4dc8dcd8eb2e96dfeab1639f06`.
Base gate `tools/research-gate.sh` sha256:
`a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad`
(the round-35 final gate; committed byte-exact as
`.ufo/waves/round-36/controls/base-gate-r36.sh`).

Routed work this round: `corpus/lessons/round-35-verifier-spotcheck.md`
§Routed defects 1–9, `corpus/evidence/round35/claims.md` §Erratum 1–15 (the
ten engine-swap demonstrations and the witness redesign list), and the
SCORECARD `Planned — round 36` candidates.

## C1 — operability (lowest scored axis: operability 3/10)

**Claim.** The gate and its counter separate an output-equivalent engine swap
in fourteen independent scenarios, one per demonstrated swap class: PATH shim,
`BASH_ENV` function, PATH-less host, relative/missing/non-GNU overrides, an
override on a DISTINCT path (honoured, named, and observed receiving the
matcher calls), the default pin named with a LIVE `--version`, the override
beating an imported shim, per-record semantic attribution of the pinned
engine's argv, manifest hash identity under a hostile `sha256sum`, C-locale
decode, and the two pin echo/drift contract cells.

Surface: grep-binary provenance and the tools the receipt names as identity
(`research-gate.sh` grep pin + `verify-all --json` hash pins + the pin/drift
contract), measured by `corpus/evidence/round36/c1-count.py`.

**P1 (frozen predicate).** C1 is met iff

```
python3 corpus/evidence/round36/c1-count.py --seed N --receipt F
```

prints `ENGINE_SWAP_CANARY=14/14` with `predicate_holds=true` on each of two
fresh seeds against the landed lane revision, and no committed run of the same
counter against the landed gate prints a lower count.
Code condition: `passed == 14` and both reference runs sane; receipt label
`predicate_holds`.

**Kill rule.** Any run of the counter against the landed gate below 14/14
kills C1; a scored run whose `gate_sha256` differs from the receipt's is not
the claim's measurement; a scenario made to pass by weakening its fixture
(reference no longer sane) is not a measurement.

**Before (measured).** Base gate `a4768851…`: `ENGINE_SWAP_CANARY=10/14`
(`.ufo/waves/round-36/measure/c1-before-s36001.json`). The four failures are
the round-35 routed defects: S11 manifest hash shim (the hostile PATH
`sha256sum` poisons both fields, run stays exit 0), S12 C-locale decode
(`\u00e9` reads `unsupported` under `LC_ALL=C`), S13 pin echo isolation
(baseline embeds `GATE_GREP:`, drift reports `-LINE`), S14 drift token (an
injected `GATE_GREP:` line pairs as `-LINE`).

**Cheapest control that skips the claimed work (committed).** The base gate
itself, byte-exact `.ufo/waves/round-36/controls/base-gate-r36.sh`
(`a4768851…`), scores 10/14 — the do-nothing engine reaches neither the target
nor the four fixes. (The round-35 hardcoded-pin control remains the cheapest
control for the r35 counter, not for this one.)

## C2 — calibration (self-assessment quality)

**Claim.** The lane's mechanism witness scores the matcher PER RECORD through
the pinned engine's out-of-band argv channel, separating the five
output-equivalent engines the round-35 witness admitted — python-exact,
environment-keyed, stderr-forging, one-call-for-show, body-replaced matcher —
while a renamed matcher still passes (no false kill).

Surface: `tools/argv-witness.py` (new capability) + `corpus/evidence/round36/c2-count.py`.
The witness runs the candidate gate with a distinct-path GNU-reporting recorder
as its pinned grep; the recorder appends NUL-delimited argv per invocation to a
log whose name and per-run marker are drawn outside the gate's environment, and
every record's own span (or its first 4096 bytes for a dead-zone span) must
appear in a `-a -z -b -o -P` matcher argv. The gate's stderr is never read, so
a forged PS4 marker is inert.

**P2 (frozen predicate).** C2 is met iff

```
python3 corpus/evidence/round36/c2-count.py --seed N --receipt F
```

prints

```
WITNESS_PER_RECORD=5/5 OUTPUT_EQUIV=5/5 LANDED_ATTRIB=pass RENAMED=pass
```

with `predicate_holds=true` on each of two fresh seeds against the landed lane
revision, and no committed run of the same counter against the landed tree is
lower.
Code condition: `separated == 5 and output_equiv == 5 and landed attribution
covers every record and the renamed control passes`.

**Kill rule.** Any run below 5/5 separation, any variant that is not
output-full (a broken patch must not count as separated), a landed run whose
attribution misses a record, or a renamed-matcher run the witness kills, kills
C2.

**Before (measured).** Same counter with the round-35 battery
`tools/mechanism-witness.py` (r35 final bytes) on the base tree:
`WITNESS_PER_RECORD=2/5 OUTPUT_EQUIV=5/5 LANDED_ATTRIB=absent RENAMED=fail`
(`.ufo/waves/round-36/measure/c2-before-legacy-s36001.json`). The legacy
witness separates only V1 and V4; it passes V2 (it scrubs the counter's own
key), V3 (the stderr forge), and V5 (body-replaced); it reports no per-record
attribution; and it kills the renamed matcher as `unparseable`. This is the
round-35 erratum 11 measurement, reproduced by the new counter.

**Controls that skip the claimed work (committed).**
`.ufo/waves/round-36/controls/ctl-c2-stub-pass.py` — a witness that answers
pass for everything: `WITNESS_PER_RECORD=0/5`. The always-fail stub separates
5/5 but fails the landed and renamed arms, so `predicate_holds=false`.

## Limits stated before the wave

- C1's semantic canary proves the pinned engine was queried for each record,
  not that its answer was used: a call-for-show engine (queries grep, discards
  the result, answers by exact search) attributes every record. Output
  equality is what rejects it, and an output-equivalent call-for-show engine
  survives — stated, not argued away.
- A gate that READS the recorder script can learn the log path and marker and
  forge records (active anti-instrumentation is out of scope).
- The S6 arm asserts the stub receives exactly one call, the `--version`
  probe; it does not assert which text the gate compared (the stub prints its
  version to stderr, which the probe discards).
- C2's witness shares the same call-for-show limit; it kills engines that skip
  the call, not engines that make the call and ignore it.
- The locale arm pins decode bytes; it says nothing about locale-sensitive
  behaviour outside `json_unescape` (the source-file read and byte counts are
  already `LC_ALL=C`-scoped).

## Repairs (not claims; no direction-of-improvement measured)

- R1 `--pin` capture environment now scrubs `CHOUSA_GREP_PIN_ECHO` (erratum 8a).
- R2 `gate_drift_line_id` names `GATE_GREP` (erratum 15's diagnostic gap).
- R3 manifest hash pin: absolute `sha256sum`, 64-lowercase-hex validation,
  exit 2 on unmeasurable/non-hex (erratum 13).
- R4 `json_unescape` decodes UTF-8 by hand in a `LC_ALL=C` scope (erratum 14).
- R5 selftest cases 257–261 (C-locale é, C-locale boundary, manifest hash shim,
  pin echo isolation, drift token); total 256 → 261.
- R6 pin-coverage ledger: `verify-integrity` and `verify-sweeps` run no
  matcher grep and are not pin coverage (erratum 12); named in SKILL.md.

## Not claimed

- No external network; no unregistered source fetch.
- The r35 claim verdicts are not re-scored; their receipts are superseded by
  new generations, not rewritten.
- C1 carried debt (spans ≥ 32768, `unverified (required controls held)`) stays
  open.

## Erratum (round 36, append-only, after the data)
