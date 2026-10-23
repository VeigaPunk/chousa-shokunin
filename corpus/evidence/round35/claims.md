# Round 35 — frozen claim design (v1)

Lane: chousa (deep-research method). Round: 35. Attempt: 1.
Frozen before any after-measurement; base lane tip and gate sha recorded below.
Two claims, distinct axes, each with its own counter, frozen predicate and
kill rule. Nothing in this file changes after the first after-run: a later
change is an erratum appended below, never an edit of the frozen text.

Base lane tip at freeze: `08be4c9e3a4ebe55d915ce4761c81854286c23ae`.
Base gate `tools/research-gate.sh` sha256:
`a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b`
(re-derive: `sha256sum tools/research-gate.sh`; equals the round-34 landed gate).

Routed work this round comes from `corpus/lessons/round-34-verifier-spotcheck.md`
§Routed defects 1–5 and the session closure note (grep-binary pin, `slen`
coupling, selftest comment numbering, the keyed-engine output-equivalence class
as the work-proof battery candidate).

## C1 — operability (lowest scored axis: operability 3/10)

**Claim.** `research-gate.sh` resolves, verifies and pins one grep binary at
startup instead of resolving bare `grep` through `PATH` at each matcher call,
and refuses a pin it cannot verify with a named exit-2 refusal.

Surface: grep-binary provenance at every matcher call site
(`tok_span_offsets_direct`, `tok_span_offsets_chunk`, `token_matcher_require`,
and the other grep call sites in the same shell). The round-34 closure measured
that the gate's output cannot tell *which* grep it ran: a PATH shim answers
identically (`S1`/`S2` tripwires below) and the gate cannot be run at all
without grep on `PATH` (`S3`).

**P1 (frozen predicate).** C1 is met iff

```
python3 corpus/evidence/round35/c1-count.py --seed N --receipt F
```

prints `GREP_PIN_MATCH=9/9` with `predicate_holds=true` on each of two fresh
seeds against the landed lane revision, and no committed run of the same
counter against the landed gate prints a lower count. Code condition:
`passed == 9`; receipt label: `predicate_holds`.

**Kill rule.** Any run of the counter against the landed gate below 9/9 kills
C1; a scored run whose gate sha256 differs from the receipt's is not the claim's
measurement.

**Before (measured).** Base gate: `GREP_PIN_MATCH=0/9`
(`.ufo/waves/round-35/controls/c1-base-s3501.json`). S1/S2 tripwires show the
PATH shim and the `BASH_ENV` function actually intercept the base gate's
matcher calls (852 and 867 bytes of shim log) with *correct output*: the
shortcut is invisible to output alone. S3 shows the PATH dependency
(`rc=2`, "GNU grep with -z/-P support is required").

**Cheapest control that skips the claimed work (pre-data, committed).**
`.ufo/waves/round-35/controls/ctl-c1-hardcoded-grep.sh` — hardcodes
`GREP_BIN=/usr/bin/grep` plus a `grep()` wrapper, no provenance, no override,
no echo: `GREP_PIN_MATCH=3/9`
(`controls/c1-hardcoded-s3501.json`). It wins S1–S3 and loses every refusal,
provenance and naming scenario, so the counter discriminates.

## C2 — calibration (self-assessment quality)

**Claim.** The lane's measurement receipts can separate an output-equivalent
keyed engine from the landed dead-zone mechanism: a mechanism-witness battery
(run the gate under `bash -x` with a private PS4 and count matcher-function
entries per long-span record) kills the two output-equivalent keyed controls
that every output counter passes, while the landed gate passes both output and
witness.

Surface: `tools/mechanism-witness.py` (new capability) — it scores output AND
mechanism for a candidate gate on a per-seed randomized fixture, and
`corpus/evidence/round35/c2-count.py` applies it to two keyed engines built from
the candidate gate: **K1-python-exact** (long spans go to a python `bytes.find`
exact search instead of the chunk matcher) and **K2-root-keyed** (the same
branch, gated on `ROOT` looking like a harness temp dir — inert on the real
corpus, active on any counter fixture). Both implement the written contract, so
an output counter *should not* kill them (round-34 `MutC2Keyed.md`: ctl4/ctl6
37/37); that is precisely why the claim is about the witness, not about the
counter.

**P2 (frozen predicate).** C2 is met iff

```
python3 corpus/evidence/round35/c2-count.py --seed N --receipt F
```

prints `WITNESS_SEPARATED=2/2 OUTPUT_EQUIV=2/2 LANDED_WITNESS=pass` with
`predicate_holds=true` on each of two fresh seeds against the landed lane
revision, and no committed run of the same counter is lower. Code condition:
`separated == 2 and output_equiv == 2 and landed witness == "pass"`.

**Kill rule.** Any run below 2/2 separation, any variant that is not
output-full (a broken patch must not count as "separated"), or a landed gate
whose witness fails, kills C2.

**Before (measured).** The base tree holds no witness battery:
`WITNESS_SEPARATED=0/2 battery=absent`
(`.ufo/waves/round-35/controls/c2-before-s3501.json`).

**Cheapest controls that skip the claimed work (pre-data, committed).**
`controls/ctl-c2-stub-pass.py` — a "witness" that always answers pass:
`WITNESS_SEPARATED=0/2` (`controls/c2-stub-pass-s3501.json`). A witness that
always answers fail also fails the predicate (landed witness fails):
`controls/c2-stub-fail-s3501.json`. So neither trivial battery can meet P2.

**Limit stated before data.** A trace witness cannot distinguish an engine that
knows it is traced, or that calls the chunk matcher once for show and ignores
its result. The witness rules out fingerprint-and-shortcut engines, never
active anti-instrumentation; and it says nothing about whether the confirmation
predicate is right (the output counter's job).

## Repairs (not claims; no direction-of-improvement measured)

- **R1 `slen` dynamic-scope coupling** (`research-gate.sh:1632`):
  `local hay=$1 span=$2 slen=${#span}` expands every right-hand side *before*
  any of the names is assigned, so `slen` reads the caller's `span` (bash
  dynamic scope), not `$2`. Reproduced: `bash -c 'f(){ local a=$1 b=${#a}; echo $b; }; f hello'`
  prints `0`. In the landed call path the caller's `span` happens to equal the
  argument, so no measured behaviour changes today; the repair (`slen=${#span}`
  on its own line) is demonstrated with a probe that calls the chunk matcher
  with a visible `span` of a different length (before: no offsets; after:
  offsets).
- **R2 selftest comment numbering**: the round-34 attempt-2 block says
  "cases 255-257"; the actual case numbers are 254–256 (r34 closure defect 2).
  Comment-only fix; no case is renumbered.
- **R3 r34 debris reconciliation**: the spot-check's "3 untracked files" finding
  is stale — `ExecC2Oracle/boundary-diff.txt`, `diff-fuzz.txt` and
  `pcre-boundary.txt` are tracked at `08be4c9e`; the count of committed wave-2a2
  reports is re-derived with one command and recorded in the report.
- **R4 runbook**: `SKILL.md` names the pinned binary and the witness tool so a
  future round re-checks the pin instead of re-discovering the shim.

## Not claimed

- The round-34 C2 verdict is not re-scored or re-opened; its counter is
  untouched.
- C1 carried debt (spans ≥ 32768, `unverified (required controls held)`) is not
  re-opened this round.
- No network; no fetch of any unregistered source.
