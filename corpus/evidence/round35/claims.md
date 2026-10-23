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

## Erratum (round 35, append-only, after the data)

1. **C2's witness threshold is aggregate**, not per record: the receipt asserts
   `chunk stamps >= long-span record count` (measured 9 stamps for 8 long
   records) and the trace carries no record id. The frozen predicate is
   unaffected; the wording that reads as per-record coverage is corrected here.
2. **C1's `--seed` is decorative**: `make_fixture` takes no seed, so the
   counter's `claims.jsonl` is byte-identical across seeds 3501/3517/3571
   (sha256 `8ca39794…`, 405 B; wave seat ExecCounterC1Timing). P1's "two fresh
   seeds" therefore means two replications of one fixture, not two samples.
   P1 held 9/9 on every run; round 36 wires the seed into the fixture or drops
   the flag.
3. **Surviving controls against the frozen predicates** (named, not fixed
   in-round — the predicates are frozen and the data is taken):
   - C1: a gate that opens the record and then refuses (sha256 `147ded03…`,
     wave seat MutPinRefusals) scores 9/9; read-before-refusal ordering is not
     asserted by the counter (its S4/S5 assert exit 2 + marker only). The
     ordering claim rests on that seat's strace evidence: 0 opens of the claims
     fixture under every refusal vs 2 opens in both positive controls.
   - C1: correct-output engines that replace `tok_span_offsets_direct`
     (bash-glob `fd6d5a8e…`, awk `9040dcba…`; MutGrepPinEngines) and a
     `BASH_ENV` `command()` function that receives every pinned call
     (MutGrepShimEnv) all score 9/9. Per-call engine identity is **not
     measured**; the counter proves path + version resolution, refusal shape
     and output equality.
   - C2: a one-record shortcut (chunk stamps 8 for 8 long records — the landed
     gate emits 9, one call of slack), a length-keyed engine (`${#id} % 3`,
     passing on 6 of 31 scanned seeds), a real chunk call whose result is
     discarded ("chunk-show"), and a body-replaced chunk matcher (python exact
     search inside the genuine function entry, gate `3e5648b8…`) all pass the
     witness. The witness proves **routing, not computation**.
4. **The pin code was hardened after the wave's attacks.** The wave attacked
   gate `1f2fb4f5…`; the final gate is
   `a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad` and
   removes the three reported vectors (`command`-keyword dispatch — a
   `BASH_ENV` function named `command` could serve every call; the `head`
   pipeline in the version probe — a forged `head` pinned a non-GNU stub; the
   dead `command -v grep` PATH fallback), plus readonly guards and a
   `timeout(1)`-bounded `--version` probe. Both claims were re-measured on the
   final bytes: C1 9/9 on seeds 3529/3539, C2 2/2 separated with the landed
   witness passing on the same seeds (`.ufo/waves/round-35/final/`), selftest
   `PASS (256 cases, 0 skipped)`.
5. **R2 also corrected the round-34 C1 comment** `cases 252-254` → `252-253`;
   the frozen text above named only the dead-zone range. All 14 case-number
   comments in the gate were checked against a selftest run by wave seat
   RevCaseRanges.
6. **S068 was narrowed to its anchor** after wave seat ExecCensus found the
   exported-function clause unanchored in the cited lines; the row now cites
   `BASH_ENV` only, and the exported-function behaviour is a wave measurement.

7. **S1/S2 are forgeable through tripwire-path knowledge** (wave seat RevScenarioS1S2):
   two attack gates (`3a7cbefc…` routing every matcher grep through the PATH shim, `51ffec6a…`
   exec'ing it once) score 9/9 with the shims actually running, because the counter keeps its
   tripwire inside the fixture root (`c1-count.py:94,168`) and checks emptiness only after the run
   (`:201-205`), and `C1_TMP`/`TMPDIR` reach the gate's environment (`:88`). The shim cannot know an
   unpredictable path; this counter's tripwire path is predictable. The landed gate's 9/9 is
   genuine (its shims never fired in the wave's independent runs, and its PATH fallback was dead
   code), but the instrument's discrimination between the landed gate and a shim-routing engine is
   **0 bits**. r36: draw the tripwire path per run outside the gate's environment, scrub
   `C1_TMP`/`TMPDIR` from the gate env, and add the semantic canary.

8. **Two more surviving defects, reported by the wave after the landing (both routed to r36).**
   (a) `--pin`'s canonical capture body inherits `CHOUSA_GREP_PIN_ECHO=1` (the capture's `env -u`
   list omits it), so a baseline pinned with the echo on embeds a `GATE_GREP:` line and
   `--drift` against an unchanged gate reports `GATE_DRIFT: -LINE` (wave seat ExecPinModePinDrift;
   present in the final gate `a4768851…`). The echo was meant to be receipt-only and never to enter
   a captured artifact. (b) S7/S9 override with `/usr/bin/grep`, the same path as the default pin,
   so the counter cannot tell "override honoured" from "override validated then discarded": a
   one-line mutant that assigns `GREP_BIN=/usr/bin/grep` after validation scores 9/9 while
   misreporting `source=override` (same seat). r36: an override that differs from the default (a
   distinct GNU-reporting recorder whose argv is asserted) plus scrubbing the echo flag from the
   capture environment.

9. **A round-34 figure no longer reproduces, and a round-34 counter cannot corroborate round 35.**
   Wave seat ExecR34C1V3 ran the committed round-34 long-span counter on fresh seeds 3593/3607:
   `LONGSPAN_MATCH=42/42` on the round-35 gate (19.9 s / 29.0 s) **and 42/42 on the round-34 base
   gate `a6307edf`** (23.8 s) — so that counter re-confirms round-34 debt and is blind to round 35's
   work. Consequence: `SCORECARD.md:1927`'s "0/42 ×2 by the 1500 s bound in the UTF-8 locale" no
   longer reproduces (both gates finish in 36–38 s under a UTF-8 locale); the frozen round-34 text is
   not edited, and this note is the correction of record. The same seat shows the pin is load-bearing
   through that independent counter: under a corrupting PATH `grep` the landed gate holds 42/42 while
   the base gate collapses to 0/42, and under a `BASH_ENV` `grep()` the base's matcher is intercepted
   (760,543 tripwire bytes) while the landed gate logs zero and holds 42/42. Also noted: the round-34
   counter strips only `CHOUSA_*` from the gate environment, so an ambient `RESEARCH_GATE_GREP`
   silently flips it (the round-35 counters strip both prefixes).

10. **Mode coverage is not uniform, and a `9/9` receipt does not witness the pipeline.**
   Wave seat ExecPinModeIntegrity measured that `verify-integrity` **never runs a matcher grep** — it
   calls grep only for the pin's own `--version` probe (one exec; `strace -f execve` = 1 on
   `1f2fb4f5…`, 0 on the base gate) — so that mode discriminates nothing about the pin and must not
   be cited as pin coverage. `verify-chain` and `verify/verify-claims` do grep; `verify-metadata`
   greps only with `--registry`. The same seat showed the pre-hardening blob's provenance check
   could be forged through an unpinned `head` and that the counter's own S6 never exercises the
   refusal text (its stub prints to stderr); both are closed in the final gate `a4768851…` (forged
   `head` → rc 2; `head` absent from `PATH` → rc 0), but the counter's 9/9 receipts were taken
   before those fixes, so a green receipt alone does not witness the pipeline. The report names the
   two gate generations for exactly this reason.
