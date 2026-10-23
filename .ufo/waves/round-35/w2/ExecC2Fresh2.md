# ExecC2Fresh2 — C2 re-derivation (seeds 3547, 3559) + attack

Seat: `chousa-r35-w2-ExecC2Fresh2` (executor, leaf). Lane repo `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Scope: **second independent C2 re-derivation** (seeds 3547/3559) + direct witness run + attack on the
witness's discriminating power. Read-only on all lane production files; no git/jj write; no network;
no subagents spawned; no installs performed (nothing needed).

**Verdict: C2 MEETS as frozen (P2 holds on both fresh seeds), but the witness is materially weaker than
the frozen claim text states — three bypasses still pass P2.** Details below.

---

## 0. Pinned substrates (every scored run)

| artifact | sha256 | note |
|---|---|---|
| `tools/research-gate.sh` (lane working tree) | `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617` | matches the round's declared landed gate sha |
| clone at wave base `e87c5d7ea2dbf3730b36a3961de3f06261d015e4` → `clone/tools/research-gate.sh` | `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617` | identical to lane tree |
| `clone/tools/mechanism-witness.py` | `9f537bfde0dd53f2240af149e1b7a03fd0a0f372ee1fa1a32e94044115a252b3` | battery |
| `clone/corpus/evidence/round35/c2-count.py` | `557fdbf0bd793a6589fcb28fbc0a589db9145be0ae3c92790041fe8ebd907171` | counter |
| `.ufo/waves/round-35/repairs/base-gate.sh` (round-34 blob) | `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b` | matches the declared pre-round gate |

Clone: `git clone -q /home/vgpnk/Projects/shokunin/chousa-shokunin clone && git -C clone checkout -q
e87c5d7ea2dbf3730b36a3961de3f06261d015e4` (in `/tmp/hyaku/chousa-r35/w2/ExecC2Fresh2`, `GIT_DIR`/
`GIT_WORK_TREE`/`GIT_INDEX_FILE` unset). Lane `git rev-parse HEAD` = `2b2e0171153f63c2fb657ba601d74c7830662c1b`
(one commit past the wave base; the gate/counter/battery blobs are byte-identical between the two).

---

## 1. Assignment A — C2 re-derivation on fresh seeds 3547 / 3559

Command (run from `/tmp/hyaku/chousa-r35/w2/ExecC2Fresh2`, `C2_TMP` = own scratch dir):

```
python3 clone/corpus/evidence/round35/c2-count.py --gate clone/tools/research-gate.sh \
  --battery clone/tools/mechanism-witness.py --seed 3547 \
  --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-35/w2/ExecC2Fresh2/c2-s3547.json
```

**seed 3547** → exit `0`, stdout:

```
WITNESS_SEPARATED=2/2 OUTPUT_EQUIV=2/2 LANDED_WITNESS=pass
  K1-python-exact  output=9/9 witness=fail stamps={'chunk': 0, 'direct': 1}
  K2-root-keyed    output=9/9 witness=fail stamps={'chunk': 0, 'direct': 1}
```

**seed 3559** → exit `0`, stdout:

```
WITNESS_SEPARATED=2/2 OUTPUT_EQUIV=2/2 LANDED_WITNESS=pass
  K1-python-exact  output=9/9 witness=fail stamps={'chunk': 0, 'direct': 1}
  K2-root-keyed    output=9/9 witness=fail stamps={'chunk': 0, 'direct': 1}
```

Receipts: `c2-s3547.json`, `c2-s3559.json` (both `predicate_holds: true`, `gate_sha256` =
`1f2fb4f5…`, `battery_sha256` = `9f537bfd…`; landed `witness: pass`, `output_match 9/9`,
`output_full: true`; both variants `output_full: true`, `witness: fail`).

**P2 (frozen code condition `separated == 2 and output_equiv == 2 and landed witness == "pass"`)
holds on both fresh seeds.** No committed run of this counter against the landed gate is lower: the
committed `measure/c2-after-s3501.json` and `measure/c2-after-s3517.json` both read
`WITNESS_SEPARATED=2/2`, `predicate_holds: true`, `gate_sha256` = `1f2fb4f5…`.

### Controls re-measured at the fresh seeds (they still kill P2)

| battery | seed | exit | stdout |
|---|---|---|---|
| `controls/ctl-c2-stub-pass.py` | 3547 | `1` | `WITNESS_SEPARATED=0/2 OUTPUT_EQUIV=2/2 LANDED_WITNESS=pass` |
| `controls/ctl-c2-stub-pass.py` | 3559 | `1` | `WITNESS_SEPARATED=0/2 OUTPUT_EQUIV=2/2 LANDED_WITNESS=pass` |
| `controls/ctl-c2-stub-fail.py` | 3547 | `1` | `WITNESS_SEPARATED=2/2 OUTPUT_EQUIV=2/2 LANDED_WITNESS=fail` |
| `controls/ctl-c2-stub-fail.py` | 3559 | `1` | `WITNESS_SEPARATED=2/2 OUTPUT_EQUIV=2/2 LANDED_WITNESS=fail` |

Both trivial stubs fail P2 at the fresh seeds (exit 1). The stub-pass stub separates nothing
(0/2); the stub-fail stub makes the landed witness fail. The battery is not trivially satisfiable.

---

## 2. Assignment B — direct witness run, raw stamp counts vs `long_records`

```
python3 clone/tools/mechanism-witness.py --gate clone/tools/research-gate.sh --seed 3547 \
  --json /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-35/w2/ExecC2Fresh2/witness-3547.json
```

→ exit `0`, stdout:

```
WITNESS=pass OUTPUT=9/9 STAMPS chunk=9 direct=1 (long records=8)
```

**Raw counts (asked for):** `chunk = 9`, `direct = 1`, `long_records = 8`. The witness's rule is
`stamps["chunk"] >= long_records and stamps["chunk"] > 0`
(`tools/mechanism-witness.py:295`), so `9 >= 8` passes with **one unit of slack**. Receipt
`witness-3547.json`: `gate_sha256 = 1f2fb4f5…`, `matcher_entry_lines = {chunk: 1699, direct: 1677}`,
`output_match 9/9`, `output_full: true`, `gate_rc: 1`, `drift: true`, `misses: []`,
`source_name_scheme: hex`, `fixture_root_prefix: w35wit`.

Seed 3559 direct run: `WITNESS=pass OUTPUT=9/9 STAMPS chunk=9 direct=1 (long records=8)`
(`witness-3559.json`). Extra seeds 3601 / 3611 / 3623 on the landed gate: all `chunk=9 direct=1
long_records=8`, `witness=pass` — the counts are seed-stable.

### Why 9 chunk calls for 8 long records (the slack's source)

`census.py` (own file, in the artifact dir) re-generates the witness's own fixture
(`mechanism-witness.generate`), then runs a gate copy whose `tok_span_offsets` logs every call's
span length and span sha. Seed 3547: **10 total `tok_span_offsets` calls, 9 of them with
`span > 32764`**, i.e. 9 chunk-routed calls against 8 long records. Seed 3559: identical shape.

The extra call is `dz-line-bound`: its span appears **twice** in the source, so the gate runs
`tok_span_at` (gate:1958) and then `tok_span_all` (gate:1979) over the same span — two chunk calls
for one record. Per-class call census (both seeds): `dz-verbatim-ml 2, dz-mut 2, dz-line-bound 2,
dz-verbatim-1l 1, dz-edge 1, dz-glued-left 1, short-verbatim 1` = 10 calls, 9 long.

**Consequence:** the witness counts *calls*, not *records covered*. One long record can be answered
without the chunk matcher and the count still clears the threshold.

---

## 3. Attack — the finding

### 3.1 MEETS-adjacent: the counter is TEMP-DIR sensitive; K2's separation is environmental

`K2-root-keyed` fires only when `ROOT` matches `/tmp/*|/fast/*|/var/tmp/*`
(`c2-count.py`, `K2_BRANCH`). The witness runs the gate with `--root <fixture>`, and the fixture
lives under `TMPDIR`/`C2_TMP` (`mechanism-witness.py` `main()` → `tempfile.mkdtemp(dir=base)`).

Running the counter with the temp root **outside** `/tmp`:

```
C2_TMP=/dev/shm/shmroot python3 clone/corpus/evidence/round35/c2-count.py \
  --gate clone/tools/research-gate.sh --battery clone/tools/mechanism-witness.py --seed 3547 \
  --receipt .../c2-s3547-shm.json
```

→ exit `1`:

```
WITNESS_SEPARATED=1/2 OUTPUT_EQUIV=2/2 LANDED_WITNESS=pass
  K1-python-exact  output=9/9 witness=fail stamps={'chunk': 0, 'direct': 1}
  K2-root-keyed    output=9/9 witness=pass stamps={'chunk': 9, 'direct': 1}
```

**K2 stops being a keyed engine entirely** (it shortcuts only on `/tmp`-shaped roots) and collapses
into the landed gate: `witness=pass`, `chunk=9`. The separation drops to 1/2 and **P2 fails on the
landed gate** — `c2-s3547-shm.json` records `predicate_holds: false`.

This is not a defect of my invocation: `TMPDIR`/`C2_TMP` are the counter's own documented knobs
(`c2-count.py` docstring: "writes only its temp dir (C2_TMP or TMPDIR)"), and the frozen claim
asserts K2 is active on "any counter fixture" with "no fixture-prefix or record-shape key needed".
That holds only while the harness temp root is `/tmp`-shaped. On any other filesystem layout the
K2 arm measures nothing and P2 breaks. **The claim's "environment-independent" framing is
understated.** Control: with `C2_TMP`/`TMPDIR` unset (default `gettempdir()` = `/tmp`) the same
seed gives `WITNESS_SEPARATED=2/2 … LANDED_WITNESS=pass`, exit `0` (`c2-default-3547.json`).

### 3.2 The witness passes a gate that shortcuts exactly ONE long record

`k5-skip1-1.sh` (own build; `build-k5.py`, mode `skip1`): the first long-span search is answered by
an exact python `bytes.find` helper (contract-correct: exact, non-overlapping, left-to-right) and
**never calls the chunk matcher**; every later long span still uses the chunk matcher.

```
python3 clone/tools/mechanism-witness.py --gate k5-skip1-1.sh --seed 3547 --json k5-skip1-1.json
→ WITNESS=pass OUTPUT=9/9 STAMPS chunk=8 direct=1 (long records=8)   (exit 0)
```

`chunk=8` still satisfies `8 >= 8`. Confirmed on seeds 3601 and 3611 (both `chunk=8`, `witness=pass`).
With **two** records shortcut (`k5-skip1-2.sh`) the count drops to `chunk=7` and the witness
correctly fails: `WITNESS=fail OUTPUT=9/9 STAMPS chunk=7 direct=1 (long records=8)`.

So the witness tolerates **exactly one** record's worth of un-witnessed shortcutting — precisely the
slack the `dz-line-bound` double call creates.

**And the counter does not catch it.** Running the frozen counter against that candidate:

```
python3 clone/corpus/evidence/round35/c2-count.py --gate k5-skip1-1.sh \
  --battery clone/tools/mechanism-witness.py --seed 3547 --receipt .../c2-attack-skip1.json
→ exit 0
WITNESS_SEPARATED=2/2 OUTPUT_EQUIV=2/2 LANDED_WITNESS=pass
  K1-python-exact  output=9/9 witness=fail stamps={'chunk': 0, 'direct': 1}
  K2-root-keyed    output=9/9 witness=fail stamps={'chunk': 0, 'direct': 1}
```

`predicate_holds: true`. Same on seed 3559 (`c2-attack-skip1-3559.json`). **A candidate gate that
answers one long record without ever entering the chunk matcher is scored by the frozen counter as
a full pass on both arms** — the "landed witness" arm reads `pass` and the counter's own K1/K2 arms
still separate cleanly.

### 3.3 The witness passes a "call for show" gate whose answers never come from the chunk matcher

`k7-show.sh` (own build; `build-k7.py`): for every long span the gate calls
`tok_span_offsets_chunk` once and **discards its output** (`_K7OFF=$(...)`), answering from the
python helper instead.

```
python3 clone/tools/mechanism-witness.py --gate k7-show.sh --seed 3547 --json k7-show.json
→ WITNESS=pass OUTPUT=9/9 STAMPS chunk=9 direct=1 (long records=8)   (exit 0)
```

The frozen counter against that candidate also reports a clean pass (`c2-attack-kshow.json`, exit 0,
`WITNESS_SEPARATED=2/2 OUTPUT_EQUIV=2/2 LANDED_WITNESS=pass`).

This is *not* a new defect — the frozen claim text states it as a known limit ("A trace witness
cannot distinguish an engine that knows it is traced, or that calls the chunk matcher once for show
and ignores its result"). I confirm it is **real and load-bearing**: the discarded call is enough
to satisfy the witness completely, and the whole counter stack returns `predicate_holds: true`.

### 3.4 The counter does kill the candidates it should

Negative controls I built, confirming the battery is not vacuous:

| candidate | mechanism | counter verdict |
|---|---|---|
| `k5-all.sh` | **every** long span answered by python, chunk matcher never entered | `LANDED_WITNESS=fail` → exit `1` (`c2-attack-kall.json`) |
| `k8-fixprefix.sh` | keyed on the fixture root prefix `*/w35wit-*` **and** `/tmp/*` | `LANDED_WITNESS=fail` → exit `1` (`c2-attack-k8.json`) |
| `k7-show.sh` | chunk called for show, answer from python | `LANDED_WITNESS=pass` → exit `0` (**bypass**, §3.3) |
| `k5-skip1-1.sh` | one long record shortcut, rest chunk | `LANDED_WITNESS=pass` → exit `0` (**bypass**, §3.2) |

So the battery kills whole-path shortcuts and fixture-prefix-keyed engines, but not (a) a
single-record shortcut, nor (b) a show-call. The two survivors are exactly the shapes the claim's
own "Limits stated before data" paragraph does *not* cover — the stated limit covers the show-call
but says nothing about the **one-record** shortcut, and the frozen claim asserts the witness
"stamped the chunk matcher's function-entry line **at least once per long-span record**"
(`mechanism-witness.py` docstring). That is a per-record claim; the implementation is a
**call-count** comparison (`stamps["chunk"] >= long_records`, line 295), and the `dz-line-bound`
double call makes those two quantities differ by one. **The implementation does not deliver the
per-record property the docstring claims.** [INFERENCE] The per-record property the docstring
asserts would need per-record attribution of stamps (e.g. correlating the traced span length or
the claim id with the matcher entry), not a bare count.

---

## 4. Repair R1 — slen probe re-measured (in-scope cross-check)

```
bash .ufo/waves/round-35/repairs/slen-probe.sh clone/tools/research-gate.sh
→ SLEN_PROBE offsets=1 first=5      (exit 0)
bash .ufo/waves/round-35/repairs/slen-probe.sh .ufo/waves/round-35/repairs/base-gate.sh
→ SLEN_PROBE offsets=0 first=        (exit 1)
```

Landed gate reports exactly one offset (the repaired behaviour); the round-34 base gate reports
none. R1 confirmed: base `0` offsets / landed `1`. Gate shas as pinned in §0.

---

## 5. Limits of this report

- I did not run the gate's own `--selftest`, C1 counter, or any build/lint: the parent owns the
  post-integration gate, and this seat's assignment was the C2 re-derivation.
- The witness's trace stamp count depends on `bash -x` line attribution; I did not test alternative
  bash versions or `set -x` variants.
- §3.1 depends on the host's `/tmp` layout; a host with a `/tmp`-shaped default temp root (as here)
  hides it, which is presumably why the L1's own run passed.
- §3.2/§3.3 bypass candidates are my own constructions, not committed lane controls; they are
  reproducible from `build-k5.py` / `build-k7.py` in the artifact dir (builders are deterministic —
  re-running them reproduced the identical gate sha256s).
- `long_records` counts *claims* whose class is not `short-verbatim`, not records that actually
  routed long; for this fixture the two coincide (9 long-routed calls ≥ 8 claims), but that is a
  coincidence of the class table, not a property of the witness.

## 6. Artifacts (all in `.ufo/waves/round-35/w2/ExecC2Fresh2/`, 1.5 MB total)

Receipts: `c2-s3547.json`, `c2-s3559.json`, `witness-3547.json`, `witness-3559.json`,
`c2-s3547-shm.json`, `c2-default-3547.json`, `c2-attack-skip1.json`, `c2-attack-kshow.json`,
`c2-attack-kall.json`, `c2-attack-k8.json`, `k5-skip1-1.json`, `k7-show.json`.
Stdout captures: `c2-s3547.out`, `c2-s3559.out`, `witness-3547.out`.
Builders/mechanisms: `build-k5.py`, `build-k7.py`, `census.py`; candidate gates `k5-skip1-1.sh`
(sha `72c2ccaf288e4ee1…`), `k7-show.sh` (`b13b9f7af37ea413…`), `k5-all.sh`
(`21906c626505b9fd…`), `k8-fixprefix.sh` (`69253ea195913521…`).

Scratch (large, `/tmp`): `/tmp/hyaku/chousa-r35/w2/ExecC2Fresh2/` — clone, per-seed receipts,
`ctl-*.json` control receipts.
