# Per-record argv attribution — witnessing the matcher through the engine's own argv

Lane: chousa. Round 36 (C2, calibration). Surface: `tools/argv-witness.py` and
`corpus/evidence/round36/c2-count.py`.

source: S069 (GNU `grep(1)`, `-o` plus `-b` offset semantics, opened 2026-10-23); the witness
`tools/argv-witness.py`; the frozen counter `corpus/evidence/round36/c2-count.py`; receipts
`.ufo/waves/round-36/measure/c2-{after-s36001,after-s36011,before-legacy-s36001,stubpass-s36001,stubfail-s36001}.json`,
`.ufo/waves/round-36/measure-l1/c2-s36371.json`, `.ufo/waves/round-36/w1/*/c2-*.json`;
retired battery `tools/mechanism-witness.py`.
verified-at: 2026-10-23 (round 36; landed gate SHA-256 `a7d3922c…f54e8`;
`WITNESS_PER_RECORD=5/5 OUTPUT_EQUIV=5/5 LANDED_ATTRIB=pass RENAMED=pass` on seeds 36001,
36011, 36371)
recheck: on-release (`python3 corpus/evidence/round36/c2-count.py --seed <n>` → the four-field
label with `predicate_holds=true`). Failure scope: runs of THIS witness against THIS landed gate —
a run below 5/5, a landed run that misses a record, or a renamed-matcher kill. Runs of a different
witness are controls by construction (`claims.md` §Erratum 3).

## The channel

The candidate gate runs with a distinct-path GNU-reporting **recorder** as its pinned grep
(`RESEARCH_GATE_GREP`). The recorder appends one NUL-delimited argv record per invocation to a
log whose **name and per-run marker are drawn outside the gate's environment**. The gate's
stderr is never read, so the round-35 channel — PS4 trace stamps the engine itself could forge —
is inert here: erratum 11's forged 360 stamps with zero real chunk executions score nothing.

Attribution is **per record**. Each record's own span (or its first 4096 bytes for a dead-zone
span — the implemented rule at `tools/argv-witness.py:275-285`, not a measured statistic) must appear
in a `-a -z -b -o -P` matcher argv. The witness binds a log line to a record by decoding the argv
**pattern** and comparing bytes; it does not consume grep's offset output. S069 grounds the offset
semantics of the argv shape (`-b` with `-o` prints the matching part's own offset), not the binding
method, which is the lane's design [INFERENCE].
Attribution keys on the record's own bytes, not on the temp dir or the id shape. That closes the
specific round-35 evasion (V2 keys on `CHOUSA_WITNESS_KEY`, which the witness always sets, so the
old `C2_TMP=/dev/shm` inertness cannot recur); it is not a guarantee against every possible keyed
engine.

## Survivors the round-35 witness admitted

All five variants are **output-full** (9/9 verdicts); three of them (V2, V3, V5) were **admitted**
by the round-35 routing witness and two (V1, V4) were already rejected by it. The round-36 witness
separates all five; the landed gate passes with its own 9 records attributed.

| Variant | Engine | r35 witness | r36 witness |
|---|---|---|---|
| V1 | `python-exact` — long spans answered by `bytes.find`, no grep call | fail | **fail** |
| V2 | `env-keyed` — V1 gated on `CHOUSA_WITNESS_KEY`, which the harness always sets | **pass** | **fail** |
| V3 | `witness-forge` — V1 plus 360 forged `@@WITNESS@@` PS4 stamps on stderr | **pass** | **fail** |
| V4 | `one-call-for-show` — the chunk matcher runs for the first long record only | fail | **fail** (2 of 9 records attributed) |
| V5 | `body-replaced` — the genuine chunk function runs, its grep pipeline replaced by exact search | **pass** | **fail** |
| V6 | `renamed-matcher` — both matchers renamed with call sites intact; must NOT be killed | **fail** (`unparseable`) | **pass** |

V3's 360 forged PS4 stamps and its zero real chunk executions are the round-35 observation recorded
in `.ufo/waves/round-35/w2/ExecC2Fresh1/wit-forge-head-3547.json` (`stamps.chunk=360`); the round-36
aggregate receipts keep witness/output/attribution fields, not forge counts.

Before (base tree + r35 battery): `WITNESS_PER_RECORD=2/5 OUTPUT_EQUIV=5/5 LANDED_ATTRIB=absent
RENAMED=fail` — the round-35 battery separated only V1 and V4 (`.ufo/waves/round-36/measure/c2-before-legacy-s36001.json`);
the counter's own docstring said "3/5 (V3 and V5 pass it)", which this receipt contradicts
(`## Mistakes`, `corpus/lessons/round-36.md`).

## Limits

- The witness proves the pinned matcher **received a query for each record**, not that the
  query's answer was **used**: a call-for-show engine that queries and discards still attributes.
  Output equality is what rejects it, and an output-equivalent call-for-show survives — stated,
  not argued away.
- A gate that **reads** the recorder script can learn the log path and marker and forge records;
  active anti-instrumentation is out of scope.
- The witness cannot see which text the `--version` probe compared (S6 arm of the C1 counter
  states the same limit).

## What this entry does not claim

It does not rank the survivors by deception, and it does not claim the engine is genuine: one
record's attribution is one query, not one correct answer.
