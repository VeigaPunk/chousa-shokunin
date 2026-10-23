# ExecC2Fresh1 — C2 re-derivation (fresh seeds 3529/3539) + attack findings

Round 35, v2 wave, C2 (calibration). Report date 2026-10-23.

## 0. Method

## 7. Addendum (post-hoc, from peer convergence + own verification) — one-record witness slack

Peer `chousa-r35-w2-ExecC2Fresh2` reported, and I independently reproduced, a one-record slack
in the witness that the frozen counter does not catch: a candidate that shortcuts exactly ONE
long-span record (exact python `bytes.find`, never entering the chunk matcher) still gets
`stamps["chunk"] = 8 >= long_records = 8` → `witness=pass`, and the full counter run reports
`WITNESS_SEPARATED=2/2 OUTPUT_EQUIV=2/2 LANDED_WITNESS=pass` with `predicate_holds=true`, exit 0.

My reproduction (seed 3547, candidate `slack-1record-gate.sh`: long-span branch shortcuts only
when the span contains no newline — exactly the single `dz-verbatim-1l` record among the long
records; all other long spans still call the chunk matcher):

```
$ python3 tools/mechanism-witness.py --gate .../slack-1record-gate.sh --seed 3547
WITNESS=pass OUTPUT=9/9 STAMPS chunk=8 direct=1 (long records=8)   # exit 0
$ python3 corpus/evidence/round35/c2-count.py --gate .../slack-1record-gate.sh --seed 3547 --receipt ...
WITNESS_SEPARATED=2/2 OUTPUT_EQUIV=2/2 LANDED_WITNESS=pass         # exit 0, predicate_holds=true
```

Receipts: `c2-slack-s3547.json` (sha256 `1bb2d581…`), `wit-slack-s3547.json`
(sha256 `98760a9a…`). Mechanism (peer's analysis, consistent with my stamp counts): `dz-line-bound`
spans appear twice in the source, so `tok_span_at` + `tok_span_all` produce 9 chunk calls for 8
long records; `stamps["chunk"] >= long_records` (mechanism-witness.py:295) is therefore a
call-count comparison with one record of slack, not the per-record coverage the docstring claims.
Two records shortcut → chunk=7 → witness=fail, so the slack is exactly one record. This is a
strictly stronger bypass than the pre-stated "call for show" limit (claims.md:106-109), and it is
NOT covered by that limits paragraph. Negative controls (peer): whole-path shortcut and
fixture-prefix-keyed candidates are both killed (LANDED_WITNESS=fail, exit 1).
- Cloned lane at wave base `e87c5d7ea2dbf3730b36a3961de3f06261d015e4` into
  `/tmp/hyaku/chousa-r35/w2/ExecC2Fresh1/clone` (unset GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE first).
- Verified by recomputing sha256 (matches both the pinned wave shas and claims.md):
  - `tools/research-gate.sh` = `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617`
  - `tools/mechanism-witness.py` = `9f537bfde0dd53f2240af149e1b7a03fd0a0f372ee1fa1a32e94044115a252b3`
  - `corpus/evidence/round35/c2-count.py` = `557fdbf0bd793a6589fcb28fbc0a589db9145be0ae3c92790041fe8ebd907171`
  (sha256sum computed in the clone; the lane working tree has the identical blobs.)
- Ran the frozen counter from the clone cwd (so default `--gate tools/research-gate.sh` and
  `--battery tools/mechanism-witness.py` resolve to the clone's base-revision files), with
  `C2_TMP=/tmp/hyaku/chousa-r35/w2/ExecC2Fresh1/tmp`:
  ```
  python3 corpus/evidence/round35/c2-count.py --seed 3529 --receipt .../c2-s3529.json
  python3 corpus/evidence/round35/c2-count.py --seed 3539 --receipt .../c2-s3539.json
  ```
- Wrote receipts to `.ufo/waves/round-35/w2/ExecC2Fresh1/` (mine). All commands bounded with
  `timeout 900` (counters) / `timeout 300` (probes). No subagents spawned; no committed files edited.

## 1. C2 re-derivation on the two fresh seeds (frozen P2 predicate)

Both runs printed the frozen predicate line and exited 0:

| seed | WITNESS_SEPARATED | OUTPUT_EQUIV | LANDED_WITNESS | predicate_holds | gate sha256 | battery sha256 | elapsed (receipt) |
|------|-------------------|--------------|----------------|-----------------|-------------|----------------|-------------------|
| 3529 | 2/2 | 2/2 | pass | true | 1f2fb4f5…61ef617 | 9f537bfd…52b3 | 20.63 s |
| 3539 | 2/2 | 2/2 | pass | true | 1f2fb4f5…61ef617 | 9f537bfd…52b3 | 14.81 s |

Per-variant lines (identical on both seeds):

```
  K1-python-exact  output=9/9 witness=fail stamps={'chunk': 0, 'direct': 1}
  K2-root-keyed    output=9/9 witness=fail stamps={'chunk': 0, 'direct': 1}
```

Landed stamps: `{'chunk': 9, 'direct': 1}`, `long_records=8`, `output_match=9/9`. Exit codes:
counter exit 0 on both seeds. **Verdict: C2 re-derivation passes (P2 holds) on both fresh seeds
exactly as frozen.**

## 2. Attack finding A (main) — the witness's marker is not out-of-band; a gate that
   never calls the chunk matcher can forge the trace and still pass P2.

The witness tool claims (tools/mechanism-witness.py:16, :259) that the gate runs under a
"private PS4 marker … The gate cannot see the marker in its own output contract". This is false
in the direction that matters: the marker string and its exact format are shipped to the gate in
its **own environment** (`env["PS4"] = "%s${BASH_SOURCE}:${LINENO} " % MARK`, line 259), and the
trace the witness parses is the gate's own stderr (`stderr=tf`, line ~288). A gate can therefore
emerge perfectly plausible `@@WITNESS@@<gatepath>:<line>` stamps on stderr without ever executing
the chunk matcher.

I built three proof gates (in `/tmp/hyaku/chousa-r35/w2/ExecC2Fresh1/`, receipts copied to my lane
dir): all replace the long-span branch with the round-34 python-exact shortcut (the very engine
K1 represents) and emit 40 forged stamp lines per long-span call on stderr:

- `spoof3-gate.sh` — hardcodes the `@@WITNESS@@` prefix, computes the chunk entry line by awk over its own source.
- `spoof4-keyed-forge.sh` — same as spoof3 but also gated on ROOT-looking-like-harness-temp-dir (K2-style key).
- `spoof5-ps4-forge.sh` — derives the entire stamp format from `$PS4` at runtime, zero hardcoding.

Results (witness tool, seed 3529):

| gate | WITNESS | OUTPUT | REAL chunk-matcher execution stamps | forged stamps counted |
|------|---------|--------|--------------------------------------|----------------------|
| spoof3 | pass | 9/9 | 0 | 360 |
| spoof4 | pass | 9/9 | 0 | 360 |
| spoof5 | pass | 9/9 | 0 | 360 |
| landed research-gate.sh | pass | 9/9 | 9 | 0 |

Real execution counted by taking trace lines matching the chunk entry line and requiring a trailing
command (the real `bash -x` line carries `+ command` after the stamp; the forged line ends at the
stamp). Landed gate: 9 real stamps, 0 forged. Forged gates: 0 real stamps, 360 forged. So the
witness reports "pass" for a gate whose dead-zone mechanism **never runs**.

Most important: **the full counter run against the forged gates prints exactly the P2-passing
line and `predicate_holds=true`**:

```
WITNESS_SEPARATED=2/2 OUTPUT_EQUIV=2/2 LANDED_WITNESS=pass
  K1-python-exact  output=9/9 witness=fail stamps={'chunk': 0, 'direct': 1}
  K2-root-keyed    output=9/9 witness=fail stamps={'chunk': 0, 'direct': 1}
EXIT=0
```

(receipts `c2-spoof3-s3529.json`, `c2-spoof4-s3529.json`, `c2-spoof5-s3529.json`; all
`predicate_holds=true`.) The counter builds its K1/K2 variants by patching the *candidate gate*
body, so the patch's python-exact branch is inserted above the forgery in the variants (that is why
the variants still fail the witness); the landed candidate itself, however, passes purely on forged
stamps. So P2 as a predicate is satisfied by a gate that never runs the chunk matcher and never uses
the dead-zone mechanism.

Why this matters (most valuable finding of this wave): the round's C2 claim says the witness battery
"kills the two output-equivalent keyed controls that every output counter passes, while the landed
gate passes both output and witness" (claims.md:65-68). The battery does kill the two specific
variants the counter builds, but the *witness instrument* is spoofable by the candidate under test.
The pre-stated limit (claims.md:106-109) only covers "calls the chunk matcher once for show and
ignores its result" (I confirmed that too: a call-for-show gate `k3-callforshow-gate.sh` gets
witness=pass with 9 chunk stamps); the shipped-marker forgery is strictly stronger — the gate
**never calls** the matcher and doesn't even need to detect that it is traced.

In scope: I did **not** edit tools/mechanism-witness.py, the counters, or any committed file; all
test gates are mine, built by patching a copy of the gate at the base revision.

## 3. Attack finding B — the counter's own K2 control is environment-fragile
   (separation depends on where C2_TMP/TMPDIR lives).

K2-root-keyed keys on `${ROOT:-}` matching `/tmp/*|/fast/*|/var/tmp/*` (c2-count.py:76-78). The
witness runs the gate from the fixture root (cwd=fixture root), so ROOT is the harness temp dir
path. Consequently, whether the K2 shortcut fires at all depends on where the harness creates its
temp dir:

- `C2_TMP=/tmp/…` → root `/tmp/…` → K2 fires → separated (2/2, pass). `c2-s3529.json`.
- `C2_TMP=/var/tmp/…` → root `/var/tmp/…` → K2 fires → separated (2/2, pass). `c2-s3529-vartmp.json`.
- `C2_TMP=/home/…/.ufo/waves/round-35/w2/ExecC2Fresh1/tmp-nonstd` (a perfectly legal scratch dir,
  and my own directory per the wave contract) → root `/home/…` → K2 branch does NOT fire → K2
  behaves exactly like the landed gate → witness=pass, stamps chunk=9 → `WITNESS_SEPARATED=1/2`,
  `predicate_holds=false`, **exit 1**. `c2-s3529-nontmp.json`.
- Same failure reproduced with only `TMPDIR` set to a non-/tmp path (C2_TMP unset). `c2-s3529-tmpdir.json`.

So the frozen P2 predicate is not robust to the harness's temp-dir placement: it passes only when
the fixture root lives under /tmp, /fast, or /var/tmp (and we are told /fast is 98% full and must
not be written). The claim in claims.md:23 "K2 … active on any counter fixture" and the statement
"No fixture-prefix or record-shape key is needed, so per-seed randomization of the fixture does not
remove it" (claims.md:78) are therefore too broad — the K2 control is inert under an arbitrary
(but allowed) scratch dir, and the counter then reports C2 as failing for the landed gate/battery
pair.

## 4. Attack finding C (secondary) — the counter does not pin the battery.

`c2-count.py --battery` accepts any battery path; the receipt records `battery_sha256`, but the
frozen predicate does not check it against the committed tool. I demonstrated a battery whose only
"mechanism" verdict is `sha256(gate) == <landed sha>` (no trace parsing, no PS4, no stamps) — it
produces the full P2 pass line with `predicate_holds=true` (`c2-fakebattery-s3529.json`). The
committed stub-pass/stub-fail controls are the only pre-data trivial batteries; a "pass iff
byte-identical to landed gate" battery is a third trivial class that P2 accepts. Receipts pin the
battery sha, so this is visible to an auditor — but the predicate as coded is not.

## 5. What I verified / did not verify

- Ran: the two fresh-seed counter runs; the witness tool against landed + spoof3/4/5 + K3;
  the counter against spoof3/4/5 and against a fake battery; the counter under /tmp, /var/tmp,
  and non-/tmp C2_TMP (and TMPDIR-only). All exited with the codes quoted. Commands quoted above
  and in this report; receipts stored in my lane dir `.ufo/waves/round-35/w2/ExecC2Fresh1/`.
- Did NOT run: C1 (out of scope of this seat), builds/lints (wave rule), network. No committed
  file was modified (git status shows only my new artifacts plus other peers' files).

## 6. Risks / limitations

- The forgery gates and their receipts are mine; they are not the claim's measurement. They show
  P2's satisfiability by a spoofing candidate, not that the committed landed gate is fake (it is
  real: 9 true chunk stamps).
- Finding A is a limitation of the witness design (shared marker in the gate's env + stderr trace
  channel), not a defect in the frozen P2 runs themselves — the two fresh-seed runs in §1 remain
  valid and passing.
- /fast is at 98% and was not used; all scratch lived under /tmp/hyaku/chousa-r35/w2 (113 GiB free).

## Verdict (as asked)

- C2 re-derivation on fresh seeds 3529/3539: **PASS** — WITNESS_SEPARATED=2/2, OUTPUT_EQUIV=2/2,
  LANDED_WITNESS=pass, predicate_holds=true, exit 0, wall 20.63 s + 14.81 s.
- Attack A (most valuable): a **witness bypass that still passes P2** exists — a gate that never
  calls the chunk matcher (forged `@@WITNESS@@` stamps derived from `$PS4` in its own environment)
  satisfies P2 with predicate_holds=true. Exactly why: the "private" PS4 marker is shipped to the
  gate in its own env, the trace channel is the gate's own stderr, and the witness's regex
  (`WITNESS@@(.*?):(\d+) `, line 269) counts any matching line with the gate path; the gate needs
  no trace detection and no real chunk call.
- Attack B: the counter's K2 separation is environment-keyed — non-/tmp C2_TMP/TMPDIR yields
  WITNESS_SEPARATED=1/2 and P2 FAILS on the landed gate + committed battery (exit 1). K2 is
  inactive "on any counter fixture" only when the fixture root is under /tmp|/fast|/var/tmp.
- Attack C: P2 also accepts a "pass iff same sha as landed" battery that performs no mechanism work.
