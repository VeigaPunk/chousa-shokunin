# The keyed-engine class — output equivalence cannot prove a mechanism

Lane: chousa. Round 35 (C2). Tool: `tools/mechanism-witness.py`.

source: lane evidence — `.ufo/waves/round-34/w2a2/MutC2Keyed.md` (ctl4/ctl6 37/37), the round-35
frozen design `corpus/evidence/round35/claims.md` (+ erratum), and the round-35 wave seat reports
under `.ufo/waves/round-35/w2/` (MutWitnessBypass1/2, MutC2KeyedBattery, MutWitnessThreshold,
CritWitnessBlind[dead]); no external source row backs this entry.
verified-at: 2026-10-23 (round 35; witness tool SHA-256 `9f537bfde0dd…52b3`; `WITNESS_SEPARATED=2/2`
on seeds 3529/3539, `.ufo/waves/round-35/final/c2-s*.json`; gate SHA-256 `a47688518e50…c38ad`)
recheck: on-release (`python3 corpus/evidence/round35/c2-count.py --seed <n>` → 2/2 separated,
landed witness pass; then re-read the surviving-control table below — it is the entry's limit)

## The class

A counter that scores only a program's printed verdicts cannot tell two
programs apart when both implement the written contract. Round 34 measured
exactly this on the lane's own C2 counter: a gate that recognised the counter's
fixture — the stable temp prefix `chousa-r34-c2-`, the `c%010x` ids, the
`src/%016x.md` names, a root under a temp dir — and answered the dead-zone
records from a python `bytes.find` exact search **scored 37/37 without ever
running the chunk matcher it was supposed to be proving**
(`.ufo/waves/round-34/w2a2/MutC2Keyed.md`, controls ctl4 and ctl6; 39 keyed
firings in the instrumented copies).

The general shape: *fingerprint the fixture, answer from a cheaper engine that
happens to agree on that fixture*. Three sub-classes, all observed:

1. **Fixture-shape key** — ids, file names, member order, a fixed temp prefix.
2. **Location key** — the source root lives under `/tmp`, `/fast`, `$TMPDIR`;
   no stable prefix is needed, so randomising the prefix does not remove it.
   Round 35's K2 control keys on `ROOT` alone and is inert on the real corpus,
   active on every fixture.
3. **Record-label key** — the fixture's `expect` field. Mostly self-defeating:
   echoing the label exits 0 and the lane's counters refuse to score a run that
   prints no `DRIFT` (round-34 ctl2 scored 0/37).

## Why no output counter can kill it

The keyed engine is **right** on the tested inputs. Killing it would be a
false negative, and the lane's rule (QUALITY 28/42) says a control that a
correct implementation also fails is a broken control. The defect is not the
engine's output; it is the receipt's claim: an output score can show that the
*contract* holds on a fixture, never that *the mechanism under test* ran.

## The three defenses and what each buys

1. **Fixture unpredictability.** Generate the fixture per seed: random temp
   prefix, id width and prefix, source-name scheme, key order, record order,
   span lengths inside the window, mutation offsets. Cost: cheap; buys removal
   of shape keys (class 1). It does **not** remove class 2 (a root under a temp
   dir is what a test harness looks like) and cannot, without making the
   fixture indistinguishable from real data — at which point it stops being a
   fixture.
2. **Mechanism witness.** Collect evidence of the mechanism out of band, not
   from the program's output contract: run the gate under `bash -x` with a
   private `PS4` stamping `BASH_SOURCE:LINE`, locate the matcher functions by
   scanning the gate's own source, and count function-entry stamps. The frozen
   threshold is **aggregate**: stamps >= the number of long-span records
   (measured 9 stamps for 8 long records — the line-bound record enumerates
   twice). A fingerprint-and-shortcut engine stamps zero; the landed gate
   clears the threshold. **Per-record coverage is NOT measured** (the trace
   carries no record id), so a gate that calls the matcher once per gate run
   and shortcuts the rest is a disclosed limit, tested by the round's
   threshold-attack seat. Cost: one instrumented run and a trace file bounded
   by the fixture size (measured: ~7 s per run).
3. **A stated limit.** A trace witness cannot distinguish an engine that knows
   it is traced, or one that calls the real matcher once for show and ignores
   the result, or one that puts the shortcut *inside* the real function. The
   witness rules out fingerprint-and-shortcut engines; it is not
   anti-instrumentation, and it says nothing about whether the confirmation
   predicate is correct — that is the output counter's job. Any claim resting
   on a witness must carry this sentence.

## Where this witness is still wrong (measured by the round-35 wave)

The aggregate threshold is weaker than it looks, and the wave proved three
survivals on seeds where the frozen P2 still printed `2/2`:

| Control | What it does | Result | Cause |
|---|---|---|---|
| D — one-record shortcut | answers ONE long record from an exact search, calls the chunk matcher for the others | `WITNESS=pass chunk=8` (long records 8) | the landed gate already emits 9 stamps for 8 records (the line-bound record enumerates twice), so one call of slack exists; the threshold is a global sum with no record attribution |
| C — length-keyed engine | `${#id} % 3` picks the engine | passes on 6 of 31 scanned seeds | the fixture draws one id width per seed, so the key is constant inside a fixture; a two-seed check misses it ~65% of the time |
| body-replaced chunk matcher | keeps the function entry, replaces the grep/confirm body with a python exact search | `WITNESS=pass OUTPUT=9/9` | the witness counts entry stamps; it does not observe what the body ran |

Two further survivals (wave seat RevWitnessCode): a column-0 decoy definition
of the matcher placed earlier in the file captures the parser's "first
occurrence", so the witness stamps a function that never runs; and the gate can
print the marker format to stderr itself (static forgery — the marker is a
constant). The witness trusts the candidate's own source layout and stderr, and
its trace file is large (~310 MB per 9-record run).

So the honest scope of this witness is **routing**, not computation: it shows
the routed function was entered, never that the body did the work. The r36
hardening family, agreed by three independent wave seats: per-record
attribution (stamp counts tied to record ids, not a global sum), seeded
diversity of the fixture's id shape (draw width per record or assert a
per-fixture spread), and a semantic canary — a pinned needle set whose match
results differ between a correct matcher and an exact-search substitute, or a
verified GNU-reporting recorder that must log at least one 4N-hex matcher
query. Until then, a claim built on this witness must say "routing".

## Evidence

- Design and frozen predicate: `corpus/evidence/round35/claims.md` §C2.
- Counter: `corpus/evidence/round35/c2-count.py` → `WITNESS_SEPARATED=2/2
  OUTPUT_EQUIV=2/2 LANDED_WITNESS=pass` on seeds 3501 and 3517
  (`.ufo/waves/round-35/measure/c2-after-s*.json`). Before, with no battery:
  0/2 (`.ufo/waves/round-35/controls/c2-before-s3501.json`).
- Trivial-stub controls: an always-pass witness separates nothing (0/2,
  `controls/c2-stub-pass-s3501.json`); an always-fail witness fails the landed
  gate (`controls/c2-stub-fail-s3501.json`). Neither can meet P2.
- The two separated engines: K1 (python exact search for long spans) and K2
  (the same branch gated on `ROOT` under a temp dir), both output-full 9/9
  and both witness-fail.
