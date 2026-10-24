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

1. **P1's prose count was wrong (number-drift).** `c1-count.py`'s docstring said fourteen
   scenarios were "the ten demonstrations of `.ufo/waves/round-35/` plus the three routed gate
   defects" (10 + 3 = 13); the frozen `before` receipt names FOUR routed defects (S11-S14). The
   count is 14 and the docstring now says so. No scoring code changed.
2. **P2's code is one conjunct stricter than its prose (F3).** `c2-count.py`'s `holds` also
   requires `landed.witness == "pass"`, which the P2 sentence and kill rule do not name. The
   printed four-field signature cannot express it. The code is stricter, never looser; the
   conjunction is unexercised by any committed receipt (a landed witness failure would also drop
   `five separated` only if attribution vanished). Reading: P2 is met as printed AND the landed
   witness passes.
3. **P2's kill rule excludes its own controls (F4).** "any run below 5/5 kills C2" read literally
   condemns the committed `ctl-c2-stub-pass.py` control (`0/5`). Controls are not claim
   measurements: a run of a DIFFERENT witness is a control by construction. Kill rule scope is
   runs of the claim's witness against the landed gate.
4. **C2's own docstring count corrected (F1, repair R7).** It said the round-35 battery "separates
   only 3/5 (V3 and V5 pass it)"; the committed receipt is 2/5 with V2, V3 and V5 passing. Prose
   only; counter sha256 changes (`3c699aab…4362` → `67c33fe4…c97f`). Receipts do not bind the
   counter's hash (carried debt), so no receipt is invalidated.
5. **C1's four separations are the round's only new ones.** Wave seat MutC1Arm showed S11 and S12
   are each worth exactly one point against the base control (10/14 → 11/14 in their own cell),
   and ScoutC1Counter showed S7-S9 assert the echo/refusal contract, not per-call engine
   identity. "14/14" is fourteen asserted behaviours with four newly discriminated by the named
   cheapest control; it is not fourteen independent engine swaps.
6. **Two gate spots the round did not fix (named, not claimed).** `research-gate.sh:2002` still
   builds a claim-body `sha256` through PATH `sha256sum | cut` (hex-checked after, so a 64-hex lie
   still poisons a claim pin), and the drift-id header comment at lines 264-265 omits the
   `GATE_GREP` token that R2 emits. Both are ScoutGateDiff findings; neither is in this round's
   claimed surface.
7. **R1's scrub is incomplete (wave finding, not fixed post-data).** The `--pin` capture runs
   `env -u CHOUSA_GREP_PIN_ECHO … bash "$SELF"`, but the inner bash still sources `BASH_ENV`, so a
   one-line `export CHOUSA_GREP_PIN_ECHO=1` in that file re-introduces the echo and embeds a
   `GATE_GREP:` line in the baseline (`w1/RevPinContract.md` F1, reproduced). No counter arm sets a
   `BASH_ENV` exporter, so neither claim's measurement is affected; the gate is NOT edited after the
   data (a post-measurement gate change would void every `gate_sha256` receipt). Fix `-u BASH_ENV`
   at `research-gate.sh:3921` is a round-37 candidate.
8. **C2's exact-span attribution is not load-bearing (wave mutant B).** A witness that requires only
   the span's first 64 bytes still scores `5/5 OUTPUT_EQUIV=5/5 LANDED_ATTRIB=pass RENAMED=pass`
   (`w1/MutC2AttrKey/art/wit-prefix.py`, receipts `rec-prefix-s*.json`): attribution sets are
   byte-identical to the pristine witness on every variant. A prefix-query call-for-show engine
   would therefore pass P2 [INFERENCE, not built]. The committed witness is unchanged (its bytes
   are bound by the receipts' `witness_sha256`); a V7 variant and a stricter span rule are
   round-37 candidates.
9. **C1's S10 does not reject a call-for-show engine (stated limit, now measured).** A gate that
   queries the recorder per record and answers by exact search scores
   `ENGINE_SWAP_CANARY=14/14` (`w1/RevCounterHonesty/c1-forshow3-s36371.json`, gate `02392327…`,
   `predicate_holds=true`). This is exactly §Limits' first bullet — the canary proves the query,
   not the use — so it narrows nothing further; it is recorded because a MEETS-class result
   deserves its receipt.
10. **P1's kill-rule sentence 2 is auditor discipline, not a counter check (H2).** The receipt's
    `gate_sha256` is computed from the `--gate` argument, so it can never differ from itself; a
    comment-only byte-different gate scored `14/14` with `predicate_holds=true`
    (`w1/RevCounterHonesty/c1-commentpatch-s36321.json`). Binding a receipt to the frozen gate is a
    re-derivation duty (hash the file independently), not something the counter can enforce.
11. **S9 does not observe the override engine (H3, measured).** A gate whose wrapper never execs the
    pinned engine scored `12/14` with S9 PASS (`w1/RevCounterHonesty/c1-pinnaming-s36351.json`,
    gate `5c028fed…`): S9 asserts the tripwire, output equality and the echo, as its code has always
    said; S7 and S10 are the arms that catch a non-executing pin. This is QUALITY 52's case with a
    receipt.
12. **A third docstring number corrected (H4).** S10's docstring said the output-equivalent python
    engine "attributes 0/2"; the code requires the long record to be missing, and the engine still
    attributes the direct short record. Wording corrected; no scoring change.
13. **A verdict-flipping locale seam outside `json_unescape` (wave finding, outside the claimed
    surface).** On the landed gate the same record with `window_mode:　external` (U+3000) plus an
    approved URL pointer reads `EXTERNAL_WITHOUT_APPROVAL crit` / DRIFT / rc 1 under `LC_ALL=C` and
    CLEAN / rc 0 under `en_US.utf8`: `research-gate.sh:1015`'s `[[:space:]]` runs through the pinned
    grep wrapper under the caller's locale (0 vs 2 pinned-grep hits). The same class sits at 1019
    and, in principle, in the `-i` folding at 762/1083; none are covered by a selftest
    (`w1/RevLocaleSeam.md`). This is the locale arm's stated limit made live — the arm pins decode
    bytes, not the screener — so no C1/C2 receipt moves; scheduling the fix and its selftest is a
    round-37 item.
