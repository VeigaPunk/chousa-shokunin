# R78CriticB — the forge battery's verdict taxonomy (round 78, wave 1)

**Seat:** R78CriticB · 2026-11-04 · leaf (no subagents, no `agent://all`, no network, no lane
or fleet git/jj mutation, no production edits).
**Writes:** `.ufo/waves/round-78/w1/R78CriticB/` and this file only. Lane tree, `corpus/`,
`tools/`, sibling lanes and the fleet repo untouched.
**Frozen set read first:** `corpus/evidence/round78/claims.md`; QUALITY 141–145, 137, 143.
**Tooling record:** nothing installed or upgraded (no pacman, no `uv`, no `npx`, no PATH
write); `python3 3.14.8 -B`, `git 2.56.0`, `cc 16.2.1` as found.
**Scratch:** `/fast/scratch/hyaku/chousa-r78/R78CriticB/` — receipts copied out to this
folder, scratch deleted before yield.

Instruments re-hashed at scoring time and identical to the `claims.md` table:
`forge-battery.py ba98db41…`, `matrix-battery-v5.py 5545a471…`,
`loader-matrix-v3.py b79d6441…`. Nothing below edits a frozen instrument.

---

## 0. The predicate re-runs; the taxonomy is the thing under attack

```
$ python3 -B corpus/evidence/round78/forge-battery.py \
    --battery corpus/evidence/round78/matrix-battery-v5.py --work DIR
FORGER a1-trailing-salt-strip rc=1 receipt_lines=113 trailer=yes integrity=ok  verdict=REFUSED
FORGER a2-parent-cmdline-source rc=1 receipt_lines=113 trailer=yes integrity=ok verdict=REFUSED
FORGER a7-printed-order-digest rc=1 receipt_lines=113 trailer=yes integrity=ok verdict=REFUSED
FORGER a5d-detached-append rc=1 receipt_lines=139 trailer=yes integrity=BAD verdict=DETECTED
POSITIVE legit-matrix rc=0 receipt_lines=113 integrity=ok verdict=ACCEPTED
FORGE_BATTERY=PASS forgers_handled=4/4 positive=1/1
# exit: 0   (79.3 s wall)
```
Receipt `receipts/p0-baseline.txt`, stderr `receipts/p0-baseline.err` (empty). Byte-identical
to `controls/forge-battery-after-v5.txt`, so everything below is measured against the same
classifier the claim scores with.

C1's predicate is that one exact line. The **taxonomy** is the classifier that produces the
`handled` counter inside it, `forge-battery.py:136-141`:

```
136    if integrity is False:                                   verdict = "DETECTED"
138    elif rc != 0 and last.startswith("BATTERY=FAIL"):         verdict = "REFUSED"
141    else:                                                    verdict = "FORGED"
...
151    accepted = rc == 0 and integrity is not False and last.startswith("BATTERY=PASS")
```

with the integrity rule at `:85` (`len(lines) == stated and len(battery_lines) == 1`), the
sample time at `:106`/`:129` (`settle = max(forger delay) + 6`, one `time.sleep`, one read),
and `handled = verdict in ("REFUSED", "DETECTED")`.

Three structural facts follow from reading it, before any probe:

1. **The classes are not mutually exclusive.** `FORGED`'s own docstring is a disjunction —
   "the battery exited 0, **or** the receipt's last `BATTERY=` line claims PASS — the verifier
   is fooled" — and `DETECTED`'s is a separate conjunction. Both can hold at once; `:136`
   gives `DETECTED` priority unconditionally, so **a subject whose battery exited 0 is
   `handled` whenever its receipt is dirty.**
2. **`integrity is None` passes both `REFUSED` and `ACCEPTED`.** A receipt with no trailer at
   all — no self-check whatsoever — is never penalised, so "receipt intact" is not a
   requirement of the class that says "its receipt is internally intact".
3. **`accepted` is a prefix match.** The cells inside the PASS line are never read.

---

## 1. Boundary verdicts

| # | boundary the taxonomy asserts | probe | verdict | holds? |
|---|---|---|---|---|
| B1 | REFUSED = battery refused, receipt intact, last line FAIL, forgery scored nothing | P0 | a1/a2/a7 REFUSED at 113 lines | **only for the frozen four** |
| B2 | same, when the receipt is intact and the last line is FAIL but a verifier is fooled | P7 | REFUSED at +5 s → DETECTED at +30 s, same receipt, same rc | **NO — time-dependent** |
| B3 | same, when the "FAIL" is written by the subject | P5a/P5b | FORGED without the forger, REFUSED with it | **NO — evidence is attacker-written** |
| B4 | DETECTED = tamper exposed, not believed, forgery scored nothing | P0, P4 | last line is v5's exact PASS line; a perfect rewrite passes the trailer | **NO — exposed only to a trailer-checking verifier** |
| B5 | DETECTED implies the battery did not accept | P3c | `FORGE_BATTERY=PASS` with a subject at rc=0 | **NO — `:136` precedes the exit-code test** |
| B6 | FORGED: exit 0 with a FAIL last line | P2 | 4× FORGED, `FORGE_BATTERY=FAIL`, exit 1 | **yes (fails closed)** |
| B7 | FORGED: subject writes the receipt directly | P4 | FORGED, `handled=False` | **yes (fails closed)** |
| B8 | the predicate line on a second stream | P8/P8b | swallowed at both legs | **yes** |
| B9 | positive control ACCEPTED ⇒ the battery scored | P10, P1, P9 | ACCEPTED from a line saying `positive=0/2`; 4/4+1/1 from a battery that scores nothing; v5 itself refuses a no-op matrix | **NO — metric, not v5** |
| B10 | receipt intact ⇒ no tamper | P4 | a 2-line rewrite is `integrity=ok` | **NO** |

---

## 2. Findings

### F1 — `DETECTED` absorbs `rc == 0`: C1's kill rule is not enforceable by this instrument

C1's kill rule: *"A seat that finds a forger reaching `BATTERY=PASS` on v5 without scoring a
subject falsifies the claim."* The classifier cannot report that state, because `:136` is
evaluated before the exit code and `handled` counts `DETECTED`.

Probe `probes/synth-fooled-a5d.py` (a battery that accepts the legit positive **and** the a5d
forger by sha256, refuses the rest, and runs every subject so a5d's own append fires). Frozen
classifier, no edit:

```
$ python3 -B corpus/evidence/round78/forge-battery.py \
    --battery <probe> --work DIR
FORGER a1-trailing-salt-strip rc=1 … integrity=ok  verdict=REFUSED
FORGER a2-parent-cmdline-source rc=1 … integrity=ok verdict=REFUSED
FORGER a7-printed-order-digest rc=1 … integrity=ok verdict=REFUSED
FORGER a5d-detached-append     rc=0 receipt_lines=4 trailer=yes integrity=BAD verdict=DETECTED
POSITIVE legit-matrix rc=0 … verdict=ACCEPTED
FORGE_BATTERY=PASS forgers_handled=4/4 positive=1/1
# exit: 0
```
(`receipts/p3c-fooled-a5d.txt`, `receipts/p3c-a5d-receipt-rc0.txt`.)

The a5d subject's battery run **exited 0 and printed `BATTERY=PASS`** — FORGED's first clause
is satisfied — and the round still prints PASS. The battery here is synthetic; that is the
point of the probe: it isolates the classifier from v5 so that only the branch order is under
test. Under the frozen predicate the defect is **latent**, and it is exactly what the kill
rule needs to catch. (R78ReviewA's a9-class forger reaches v5 `rc=0` by another route; if a
forger of that kind ever also appended — a5d already appends by construction — this
classifier would still print `FORGE_BATTERY=PASS`.)

**Smallest safe correction:** test the exit code first —
`if rc == 0: FORGED` before the integrity test. One-line reorder; `DETECTED` then means
"non-zero exit *and* a dirty receipt", which is what the docstring says it means.

### F2 — `REFUSED` is a sampling artifact; the artifact it certifies ends in the exact PASS line

`forge-battery.py:106` sets `settle = max(forger delay) + 6` — a 6-second margin over the
frozen a5d's 20-second append — and `:129` samples **once**. The receipt is a file the subject
still writes to after the battery exits, so the verdict depends on when you look:

```
$ python3 probes/harness.py matrix-battery-v5.py forgers/a5d-detached-survives.py DIR 5,30
battery=matrix-battery-v5.py rc=1 elapsed=3.3s
  sample t=+5s  receipt_lines=113 battery_lines=1  integrity=ok  last='BATTERY=FAIL …' verdict=REFUSED  handled=True
  sample t=+30s receipt_lines=139 battery_lines=14 integrity=BAD last='BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED' verdict=DETECTED handled=True
```
(`receipts/p7-settle-race.txt`, final artifact `receipts/p7-final-receipt-after-30s.txt`.)

`harness.py` imports the frozen module and calls its own `run_battery`/`read_receipt`, then
applies the frozen branch order verbatim. Same receipt file, same `rc=1`, two samples, two
classes. Under the frozen default the append lands 6 s before the read; the forger chooses the
delay, so the margin is not a property. `--settle` is an exposed knob: `--settle 5` converts
this DETECTED into a REFUSED *and* `forgers_handled=4/4`, while the receipt on disk ends with
`BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED`.

**Smallest safe correction:** sample once, at the end — after the positive control run, which
takes ~42–79 s and is therefore already longer than any forger delay the instrument knows
about — or read twice separated by the longest declared delay and require the bytes to be
identical.

### F3 — `REFUSED`'s evidence is written by the subject

The class says "its receipt is internally intact and its last `BATTERY=` line claims FAIL —
the forgery scored nothing". The receipt is `/proc/<ppid>/fd/1`, and the subject can rewrite
it. Same battery, two subjects:

```
$ python3 probes/harness.py probes/synth-pass-exit1.py probes/synth-always-pass.py DIR 0
battery=synth-pass-exit1.py rc=1 … last='BATTERY=PASS …' verdict=FORGED  handled=False
$ R78_TRUNC_PAYLOAD=fail python3 probes/harness.py probes/synth-pass-exit1.py \
    probes/forge-truncate-receipt.py DIR 5
battery=synth-pass-exit1.py rc=1 … last='BATTERY=FAIL forgers_rejected=0/11 positive=0/2 oracle=MISS' verdict=REFUSED handled=True
```
(`receipts/p5a-pass-exit1.txt`, `receipts/p5b-trunc-fail.txt`, `receipts/p5b-rewritten-fail-receipt.txt`.)

The battery's own claim is PASS; the class it earns is REFUSED, because the subject wrote the
FAIL. `handled` is therefore a lower bound on refusal, not a measurement of it. This is the
same channel that earns the round its PASS in F6.

**Correction:** none available that keeps the receipt as evidence — a nonce cannot be hidden
from the child (it reads `/proc/<ppid>/environ` and `/proc/<ppid>/cmdline`, the a2 channel).
The honest fix is to stop counting a receipt-only signal: `REFUSED` should require
`rc != 0` **and** `integrity is True` **and** no second `BATTERY=` line, and the receipt
should be described as corroboration, not proof.

### F4 — "receipt intact" is not required: `integrity is None` earns both classes

`read_receipt` returns `None` when there is no trailer, and both branches accept it. A battery
that refuses everything by sha256 and prints no trailer at all:

```
$ python3 -B corpus/evidence/round78/forge-battery.py --battery probes/synth-whitelist-notrailer.py --work DIR --settle 0
FORGER a1… rc=1 receipt_lines=1 trailer=no integrity=n/a verdict=REFUSED
FORGER a2… rc=1 receipt_lines=1 trailer=no integrity=n/a verdict=REFUSED
FORGER a7… rc=1 receipt_lines=1 trailer=no integrity=n/a verdict=REFUSED
FORGER a5d… rc=1 receipt_lines=1 trailer=no integrity=n/a verdict=REFUSED
POSITIVE legit-matrix rc=0 receipt_lines=1 integrity=n/a verdict=ACCEPTED
FORGE_BATTERY=PASS forgers_handled=4/4 positive=1/1
# exit: 0
```
(`receipts/p1-whitelist.txt`.)

Four `REFUSED` on receipts with no self-check at all, and an `ACCEPTED` positive on one. The
docstring is candid that `None` means "the receipt carries no self-check at all"; the class
definitions then ignore that fact.

**Correction:** require `integrity is True` for `REFUSED` and `ACCEPTED`; report a missing
trailer as its own outcome (`UNVERIFIED`) and never as `handled`.

### F5 — the positive control's ACCEPTED is a prefix match on `BATTERY=PASS`

`:151` reads `last.startswith("BATTERY=PASS")`. A battery whose own receipt says
`positive=0/2 forgers_rejected=0/11 oracle=MISS` is ACCEPTED:

```
$ python3 -B corpus/evidence/round78/forge-battery.py --battery probes/synth-prefix-pass.py --work DIR --settle 0
POSITIVE legit-matrix rc=0 receipt_lines=2 integrity=ok verdict=ACCEPTED
FORGE_BATTERY=PASS forgers_handled=4/4 positive=1/1
# exit: 0
-- positive.receipt:
BATTERY=PASS forgers_rejected=0/11 positive=0/2 oracle=MISS
RECEIPT_LINES=2
```
(`receipts/p10-prefix.txt`, `receipts/p10-positive-receipt.txt`.)

So `positive=1/1` in the predicate does not mean the battery accepted its own two positives; it
means some line started with `BATTERY=PASS`.

**Correction:** parse the cells — require `forgers_rejected=<n>/<n>`, `positive=<m>/<m>`,
`oracle=REJECTED` with the counts the battery itself claims, and require the trailer.

### F6 — `handled` is earned by refusal, so a battery that scores nothing reaches the predicate

`handled = REFUSED or DETECTED` is a count of *refusals*. Refusal by identity is cheap: one
sha256 comparison against a single fixed positive path. P1 above is that battery — it never
runs a case, never opens a subject, and reaches `forgers_handled=4/4 positive=1/1` at exit 0.
The predicate therefore certifies "this battery refuses these four files and accepts this one
file", not "this battery discriminates".

This is not a defect *of v5*: run against a matrix that scores nothing, the frozen v5 refuses
correctly —

```
$ python3 -B corpus/evidence/round78/matrix-battery-v5.py --matrix probes/noop-matrix.py --work DIR --runs 1
forgers_rejected=0/11 positive=0/2 oracle=REJECTED
BATTERY=FAIL forgers_rejected=0/11 positive=0/2 oracle=REJECTED
# exit: 1
```
(`receipts/` — v5 stdout tail; exit 1.) — so B9 is a hole in the *metric*, and the metric is
what the claim's predicate sentence is made of.

**Correction:** pair the predicate with a negative control that must not pass it — e.g. the
sha-whitelist battery above, and an a9-class forger that must be `FORGED` — the same way
QUALITY 141 pairs the battery with its `--no-permute` closure-removal twin.

### F7 — the trailer only catches appends that keep a wrong count, and an append that lands before the buffered flush is erased

Two mechanical limits of the trailer rule, both measured:

* **A count-preserving rewrite passes it.** `probes/forge-truncate-receipt.py` truncates
  `/proc/<ppid>/fd/1` after the battery exits and writes a complete two-line receipt with a
  matching `RECEIPT_LINES`. Result: `integrity=ok`, one `BATTERY=` line, last line PASS —
  i.e. `integrity=ok` is not evidence of non-tampering (P4, `receipts/p4-rewritten-receipt.txt`).
  Only the exit code catches it, which is why B7 holds.
* **An append before v5's buffered flush is silently clobbered.** v5 emits its subject lines
  after the scoring loop (QUIET LEG), so the receipt is empty for the whole run; v5's stdout fd
  then writes from offset 0 and overwrites anything a child appended earlier. Measured: a legit
  matrix copy carrying the a5d append at +1 s logged **26 successful appends** to the receipt
  path and the receipt still held exactly **113 lines, 1 `BATTERY=` line**
  (`receipts/p6-clobbered-append.log`, `receipts/p6-clobbered-receipt-113-lines.txt`).
  Consequence in both directions: absence of appended lines does not prove no append was
  attempted, and `DETECTED` fires only when the append lands after the flush — which is a race,
  not a rule. It is why the QUIET LEG is load-bearing for the receipt leg.

### F8 — the canonical DETECTED artifact ends with v5's exact predicate line

`receipts/p0-a5d-receipt-DETECTED.txt` (from the frozen predicate run): 139 lines, **14**
`BATTERY=` lines, and the last one is

```
BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED
```

— byte-for-byte the string v5's own docstring and the claim's predicate sentence use. The
class says "the tamper is exposed rather than believed"; it is exposed **only** to a verifier
that parses `RECEIPT_LINES`. A verifier that reads the last `BATTERY=` line — the reading the
claim's own predicate sentence models — is fooled by the artifact the taxonomy calls handled.
The only thing that saves it is `rc=1`, which the taxonomy mentions in the class definition but
does not test first (F1).

---

## 3. What holds

* **exit 0 with an intact FAIL receipt → FORGED, round fails** (P2): four FORGED,
  `FORGE_BATTERY=FAIL forgers_handled=0/4`, exit 1 (`receipts/p2-rc0fail.txt`). Fail-closed.
* **a subject that writes the receipt directly → FORGED, `handled=False`** (P4/P7 above):
  the exit code is authoritative and the subject cannot forge it.
* **a second stream is closed at both legs** (P8): the matrix's stderr is captured by v5 into
  a pipe and dropped, and the battery's stderr is captured by forge-battery into a pipe and
  dropped. With `2>&1` merged into one receipt the receipt still has exactly one `BATTERY=`
  line, `BATTERY=FAIL`, and v5 exits 1 (`receipts/p8-stderr.receipt`,
  `receipts/p8b-stderr-merged.receipt`, `receipts/p8-stderr.err` empty).
* **v5 itself is not vacuous against a do-nothing matrix** (P9, exit 1).
* **the frozen default beats the frozen a5d by 6 s** (P0 → DETECTED), i.e. the predicate as
  written is not affected by F2 — the margin is the only thing that protects it.

## 4. What I did not close

* No sampling time can prove a receipt is final: the subject owns the file. F2/F3 are the same
  fact seen twice. The recorded limit in `claims.md` ("`RECEIPT_LINES` exposes an append
  instead of preventing it; a truncated receipt is not detected by the trailer") covers the
  append; it does not cover the *ordering* (F1) or the *absence of a trailer* (F4).
* The `FORGED` direction is safe (it makes the round fail). Every unsound case found is in the
  `handled` direction, which is the direction that turns a defeat into a PASS.
* C2 (`selfcheck.py`) untouched: out of this seat's scope, no observation.

## 5. Successor-instrument corrections, smallest first

1. `if rc == 0: FORGED` **before** the integrity test (closes F1, one line).
2. `integrity is True` required for `REFUSED` and `ACCEPTED`; a missing trailer is its own
   non-handled outcome (closes F4, one condition).
3. parse the positive's cells instead of `startswith` (closes F5, ~4 lines).
4. sample the receipts after the positive run, or twice with identical bytes required
   (closes F2, moves one loop).
5. add two negative controls that must *not* pass the predicate: the sha-whitelist battery and
   an a9-class forger (closes F6).

None of these may be applied to the frozen `forge-battery.py` this round; they are a successor
instrument's requirement, reported here as a defect, not as a repaired predicate.

## 6. Artifacts

`receipts/` — `p0-baseline.txt`/`.err`, `p0-a5d-receipt-DETECTED.txt`,
`p0-positive-receipt.txt`, `p0-a1-receipt-REFUSED.txt`, `p1-whitelist.txt`,
`p2-rc0fail.txt`, `p3-fooled-a5d.txt`/`p3b`/`p3c` + `p3c-a5d-receipt-rc0.txt`,
`p4-trunc-pass.txt` + `p4-rewritten-receipt.txt`, `p5a-pass-exit1.txt`,
`p5b-trunc-fail.txt` + `p5b-rewritten-fail-receipt.txt`, `p6-clobbered-append.log` +
`p6-clobbered-receipt-113-lines.txt`, `p7-settle-race.txt` +
`p7-final-receipt-after-30s.txt`, `p8-stderr.receipt`/`.err`,
`p8b-stderr-merged.receipt`, `p10-prefix.txt` + `p10-positive-receipt.txt`.
`probes/` — every script named above (`harness.py`, `synth-*`, `forge-*`,
`mk-legit-append.py`, `legit-append-matrix.py`, `noop-matrix.py`).
