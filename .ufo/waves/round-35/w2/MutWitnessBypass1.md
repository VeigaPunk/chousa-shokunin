# MutWitnessBypass1 — witness bypass family 1 (chunk-once, trace-off)

Round 35, wave 2. Mutation tester. Date 2026-10-23. Scratch:
`/tmp/hyaku/chousa-r35/w2/MutWitnessBypass1/`; artifacts copied to
`.ufo/waves/round-35/w2/MutWitnessBypass1/` (each < 1 MiB; no log over ~2 KB).

## Pins verified before any run

```
$ sha256sum tools/research-gate.sh .ufo/waves/round-35/repairs/base-gate.sh \
    tools/mechanism-witness.py corpus/evidence/round35/c2-count.py corpus/evidence/round35/c1-count.py
1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617  tools/research-gate.sh
a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b  .ufo/waves/round-35/repairs/base-gate.sh
9f537bfde0dd53f2240af149e1b7a03fd0a0f372ee1fa1a32e94044115a252b3  tools/mechanism-witness.py
557fdbf0bd793a6589fcb28fbc0a589db9145be0ae3c92790041fe8ebd907171  corpus/evidence/round35/c2-count.py
da207fd725658b84469ce1fe540a7b94fcb1027cef49da376a8d7ac19ac715e3  corpus/evidence/round35/c1-count.py
```
Both lane pins match the contract (`1f2fb4…` landed gate, `a6307e…` round-34 base).
`git rev-parse HEAD` = `2b2e0171…` (lane tip is ahead of the wave base; the gate
bytes are the pinned ones, which is what every receipt below carries).

Seeds used: **3541** and **3557** (fresh — no committed receipt under
`.ufo/waves/round-35/controls|measure` uses them; those use 3501/3517, and the
sibling executor 3529).

## Detector

`tools/mechanism-witness.py` run directly, and `corpus/evidence/round35/c2-count.py`
with `--battery tools/mechanism-witness.py`. Witness threshold, read from source
(`tools/mechanism-witness.py:294-295`): `witness_ok = stamps["chunk"] >= long_records
and stamps["chunk"] > 0`; `long_records` = 8 on every seed (9 records, one
`short-verbatim`), `TOTAL=9` (`:54-63`). The stamp is the trace hit count on the
chunk function's **first executable body line** (`local LC_ALL=C`), located by
`matcher_entry_lines` (`:80-103`).

### Pristine baseline (same detector, same seeds)

```
$ python3 tools/mechanism-witness.py --gate tools/research-gate.sh --seed 3541 --json w-landed-s3541.json
WITNESS=pass OUTPUT=9/9 STAMPS chunk=9 direct=1 (long records=8)          rc=0
$ python3 corpus/evidence/round35/c2-count.py --gate tools/research-gate.sh \
    --battery tools/mechanism-witness.py --seed 3541 --receipt c2-landed-s3541.json
WITNESS_SEPARATED=2/2 OUTPUT_EQUIV=2/2 LANDED_WITNESS=pass               rc=0
```
(`c2-landed-s3541.json`: `predicate_holds=true`, `gate_sha256=1f2fb4…`.) Baseline is
green, so a mutant failure below is a kill, not an inconclusive baseline.

Note the pristine count is **9**, not 8: the `dz-line-bound` record is matched twice
(`tok_span_at` at `tools/research-gate.sh:1958`, then `tok_span_all` at `:1979`), so
8 long records produce 9 chunk entries.

## (a) chunk-once — KILLED (stamp count 1, threshold catches it)

Two builds, because the first is a trap worth recording.

**a1, shell-variable latch** (`chunk-once.sh`, sha256 `73174f95…`): `_CHUNK_ONCE_DONE=1`
on the first long span, python `bytes.find` afterwards.
Result: `WITNESS=pass OUTPUT=9/9 STAMPS chunk=9 direct=1`, `w-chunk-once-s3541.json`.
**This is not a survivor — the mutation is inert.** Instrumented run
(`chunk-once-dbg.sh`, seed-3541 fixture) shows why: every matcher invocation runs in
its **own subshell**, so a shell variable cannot carry state across records —

```
DBG flag=unset len=32765 bashpid=1803240 pid=1796712
SET flag=1    bashpid=1803240 pid=1796712
DBG flag=unset len=32765 bashpid=1803484 pid=1796712
SET flag=1    bashpid=1803484 pid=1796712
... (10 calls, 10 distinct BASHPID, one $$)
```
`$$` is the parent pid in a subshell; BASHPID differs on every call. The python
branch never executed, the chunk path ran every time, and the witness's `pass` is
the honest verdict for an unmutated mechanism. (Method note: any "once" mutation on
this gate must use filesystem state, not shell state.)

**a2, file latch** (`chunk-once-v2.sh`, sha256 `79d10959…`): `[[ ! -e $ROOT/.w35_chunk_once ]]`
→ chunk matcher once and `: > latch`; every later long span → python exact search.

```
seed 3541: WITNESS=fail OUTPUT=9/9 STAMPS chunk=1 direct=1 (long records=8)  rc=1
seed 3557: WITNESS=fail OUTPUT=9/9 STAMPS chunk=1 direct=1 (long records=8)  rc=1
```
Receipts `w-chunk-once-v2-s3541.json` / `-s3557.json`: `witness=fail`,
`output_full=true`, `stamps.chunk=1`, `long_records=8`, `matcher_entry_lines={chunk:1711,direct:1689}`.

**Exact answer asked for:** the witness saw **1** chunk entry against a threshold of
**8** (`1 >= 8` false), so `>= long_records` **did** catch it, at both seeds, with
output still 9/9 — i.e. the mutant is output-equivalent and mechanism-distinguishable.
Counter:

```
$ python3 corpus/evidence/round35/c2-count.py --gate chunk-once-v2.sh --battery tools/mechanism-witness.py --seed 3541
WITNESS_SEPARATED=2/2 OUTPUT_EQUIV=2/2 LANDED_WITNESS=fail               rc=1
```
`c2-chunk-once-v2-s3541.json`: `predicate_holds=false`. The counter kills it because
the *candidate* fails its own witness — the counter does not mistake the file latch
for the landed gate.

## (b) trace-off — KILLED, and `set +x` does not stop tracing

Build (`trace-off.sh`, sha256 `0ba6e2e9…`): inside `tok_span_offsets`, a
`ROOT`-keyed branch (`/tmp/*|/fast/*|/var/tmp/*`) runs `set +x`, the python exact
search, `set -x`, `return 0`. The landed chunk path is left intact.

```
seed 3541: WITNESS=fail OUTPUT=9/9 STAMPS chunk=0 direct=1 (long records=8)  rc=1
seed 3557: WITNESS=fail OUTPUT=9/9 STAMPS chunk=0 direct=1 (long records=8)  rc=1
$ python3 corpus/evidence/round35/c2-count.py --gate trace-off.sh --battery tools/mechanism-witness.py --seed 3541
WITNESS_SEPARATED=2/2 OUTPUT_EQUIV=2/2 LANDED_WITNESS=fail               rc=1
```
(`w-trace-off-s3541.json`, `w-trace-off-s3557.json`, `c2-trace-off-s3541.json`,
`predicate_holds=false`.)

**Does bash continue tracing after `set +x`? Yes.** `set +x` clears the shell-wide
xtrace option from that point in *that* shell; `set -x` sets it again for everything
after. Probe `tr-probe.sh` (sha256 `2cc81551…`), `bash -x tr-probe.sh 2>tr-probe.err`:

```
stdout: hidden-a / visible-b / hidden-c / visible-d
tr-probe.err:  + f | + set +x | + echo visible-b | + set +x | + echo visible-d
```
`hidden-a` (inside the function after `set +x`) and `hidden-c` (top level after
`set +x`) produce no trace line; `visible-b` and `visible-d` (after `set -x`) do.
So the suppression is real but local and reversible. Two consequences measured here:

1. In this gate the `set +x` cannot leak to the parent at all: every matcher call is
   a forked subshell (BASHPID evidence above), so the option change dies with the
   fork. `stamps.direct=1` in both trace-off receipts is the short record being
   traced normally after the keyed branches.
2. trace-off is **self-defeating as a bypass**: the only calls it can hide are chunk
   calls, and those are exactly what the witness counts. Hiding them drives the count
   to 0 (< 8) instead of up. It never raises a stamp count.

## Neighbour probe (same family): the threshold counts entries, not work — SURVIVORS

Two engines built on the landed gate, both output-equivalent (9/9) and both
**pass the witness**:

| mutant | sha256 | long-span answer | witness | stamps chunk | output |
|---|---|---|---|---|---|
| `chunk-show.sh` | `a76e1e35…` | python exact | **pass** | 9 | 9/9 |
| `chunk-noop-show.sh` | `b7a6f1f7…` | python exact | **pass** | 72 | 9/9 |

`chunk-show` calls `tok_span_offsets_chunk "$hay" "$span" >/dev/null` (real call,
result discarded) then answers from python. `chunk-noop-show` calls
`tok_span_offsets_chunk x x >/dev/null` eight times per long-span invocation — no
matching work at all — then answers from python; 9 long-span invocations × 8 = 72.

```
$ python3 tools/mechanism-witness.py --gate chunk-noop-show.sh --seed 3541
WITNESS=pass OUTPUT=9/9 STAMPS chunk=72 direct=1 (long records=8)         rc=0
$ python3 corpus/evidence/round35/c2-count.py --gate chunk-show.sh --battery tools/mechanism-witness.py --seed 3557
WITNESS_SEPARATED=2/2 OUTPUT_EQUIV=2/2 LANDED_WITNESS=pass               rc=0   (predicate_holds=true)
```

**Verdict on this: a quantified limit, not a P2 kill.** `claims.md` §C2 "Limit stated
before data" disclaims exactly this class — "an engine that … calls the chunk matcher
once for show and ignores its result". The measurement adds two facts the limit's
wording understates:

- "once" is caught (1 < 8). The class needs **≥ long_records = 8** traced entries,
  which any engine can compute from its own claims file (`long_records` is a property
  of the input, not a secret), and the cheapest form is 8 no-op calls per invocation —
  no matching work, no output dependence.
- `c2-count.py` handed such a gate as `--gate` prints the full predicate string
  (`2/2 … LANDED_WITNESS=pass`, `predicate_holds=true`, rc 0). It is not the claim's
  measurement because the receipt pins `gate_sha256=a76e1e35…`, not `1f2fb4…`; the
  counter cannot itself tell a for-show engine from the landed mechanism.

So P2 as frozen (landed gate = the pinned blob) still holds on these seeds; the
witness's discriminating power is call-count-only and a for-show engine defeats it.
Recommend the claim record keep the limit verbatim but replace "once" with
"one entry per long record", since the current wording invites a reader to believe
one call is the attack.

## Counter observation (operability, not a claim kill)

`c2-count.py`'s `--battery` default is the cwd-relative `tools/mechanism-witness.py`
(`corpus/evidence/round35/c2-count.py:133`). Invoked from outside the lane root with
only `--gate`, it prints `WITNESS_SEPARATED=0/2 battery=absent`, rc 1
(observed: `c2-count … --gate tools/research-gate.sh --seed 3541` from
`/tmp/…/MutWitnessBypass1`, before `--battery` was supplied). It fails closed, so it
cannot inflate a score, but a runner who forgets `--battery` gets a spurious 0/2 that
looks like a regression. My baseline above passes `--battery` explicitly.

## Restoration / no-touch evidence

- No production file was written: every mutant is a byte copy of the landed gate with
  one inserted branch, built and run under `/tmp/hyaku/chousa-r35/w2/MutWitnessBypass1/`.
  Re-hash after all runs: `tools/research-gate.sh` = `1f2fb4f522d9…`,
  `tools/mechanism-witness.py` = `9f537bfd…`, `corpus/evidence/round35/c2-count.py`
  = `557fdbf0…` — unchanged.
- No git/jj write command, no process signalled by name, every command bounded
  (`timeout 900`); network unused; no installs.
- Artifacts (all in `.ufo/waves/round-35/w2/MutWitnessBypass1/`):
  `chunk-once.sh` `73174f95…`, `chunk-once-v2.sh` `79d10959…`, `trace-off.sh`
  `0ba6e2e9…`, `chunk-show.sh` `a76e1e35…`, `chunk-noop-show.sh` `b7a6f1f7…`,
  `span_search.py` `ab435490…`, `tr-probe.sh` `2cc81551…`, `tr-probe.err`
  `3f49aeb0…`, plus the 14 receipts `w-*.json` / `c2-*.json` listed above.

## Limits

- One host, GNU bash 5.3.20(1)-release; two fresh seeds per mutant; single-run per
  seed (the witness is deterministic given the seed).
- The `set +x` result is measured for this gate's call shape (matcher calls forked per
  record). A gate whose matcher runs in the main shell would see the option change in
  the main shell too — still reversible by `set -x`, as `tr-probe.sh` shows.
- I probed only the witness family assigned (chunk-once, trace-off, plus two for-show
  neighbours). C1 / grep-pin and the R1/R2 repairs were not re-measured here.
