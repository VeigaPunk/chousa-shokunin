# Round 34 attempt 2, wave 2a2 — ExecNoHarmA2 (independent no-harm battery + re-derivation)

Seat: `chousa-r34-w2a2-ExecNoHarmA2-9`. Lane: `chousa-shokunin` (jj-colocated).
Frozen lane tip for this wave: `707da8184a0fc4d10ab3f17271556cdf364f0af5`.
Date: 2026-10-23. All experiments in `/fast/scratch/hyaku/chousa-r34-a2/w2/ExecNoHarmA2/`.
Artifacts copied into `.ufo/waves/round-34/w2a2/ExecNoHarmA2/` (116 KB total).

**Verdict (the item asked for): the no-harm battery is CONFIRMED on the frozen tip — all 11
rows reproduce, no row differs.** Two additional findings (F1, F2) are reported below; both
are *calibration-surface* findings about C3's audit coverage at the tip, not refutations of
C2 or of the battery. One (F1) was independently fixed after the tip by the lane itself
(`b8e782a`), which is evidence the finding was real.

---

## 0. Pinning (no working-tree blob was scored)

```
$ sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b
$ git -C clone checkout -q 707da8184a0fc4d10ab3f17271556cdf364f0af5   # clone HEAD = 707da81
$ sha256sum clone/tools/research-gate.sh
a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b
```
Clone created with `git clone -q /home/vgpnk/Projects/shokunin/chousa-shokunin clone &&
git -C clone checkout -q 707da818…` after `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE`.
The battery header independently re-derived `gate_tree_revision=707da8184a0fc4d10ab3f17271556cdf364f0af5`
and `gate_sha256=a6307edf687ac0fb…` from the clone it was handed.

---

## 1. The no-harm battery — independently re-run (the seat's core ask)

Command (default locale; `TMPDIR`/`SCRATCH`/`C1_TMP`/`C2_TMP` all inside my scratch):

```
$ SCRATCH=<scratch>/scratch TMPDIR=<scratch>/scratch/tmp C1_TMP=… C2_TMP=… \
  timeout 1750 bash clone/.ufo/waves/round-34/w1/ExecNoHarmBase34/battery.sh \
    <scratch>/clone/tools/research-gate.sh <scratch>/battery-a2-verify
BATTERY_EXIT=0
ROWS=11
BATTERY_RESULT=PASS
```
Wall time 122.30 s. Transcript: `…/ExecNoHarmA2/battery/battery-a2-verify.stdout`
(sha256 `f6acb7aec8ee0c7ce4f24fd832f2ae529e66ed9b568d94037708f26549820422`).
Battery script sha256 `f1a1591c55bb6dad8c3e138c4158caf4fd62fda575643fd09320713904a5eeef` —
byte-identical to the committed `.ufo/waves/round-34/w1/ExecNoHarmBase34/battery.sh`
and to the clone's copy.

### Row-by-row vs the committed summary `.ufo/waves/round-34/measure-a2/battery/battery-a2-summary.txt`

| # | row | my exit (want) | my key line | committed summary | differs? |
|---|---|---|---|---|---|
| 1 | selftest | 0 (0) | `RESEARCH_GATE_SELFTEST: PASS (256 cases, 0 skipped)`, `SELFTEST_CASES=256`, `SELFTEST_FAIL_LINES=0` | PASS (256 cases, 0 skipped) | no |
| 2 | claims-lane-root | 1 (1) | `VERDICT_BEARING_CLAIMS=0/17` (all refused) | exit 1 DRIFT, 0/17 | no |
| 3 | claims-fleet-root | 0 (0) | `VERDICT_BEARING_CLAIMS=17/17`; `RESEARCH_GATE: CLEAN (claims=17 supported=13 contradicted=2 unsupported=2` | same | no |
| 4 | chain-r3 | 0 (0) | `RESOLVED_HOPS=17/22`; `CLEAN (hops=22 verified=17 exempt=5` | same | no |
| 5 | chain-r3-broken | 1 (1) | `RESOLVED_HOPS=1/2`; `DRIFT (hops=2 verified=1` | same | no |
| 6 | observable | 0 (0) | `VERDICT_BEARING_EXPORTS=3/3` | same | no |
| 7 | r31-c1-v3 | 0 (0) | `LINE_BINDING_MATCH=132/132`, receipt `predicate_holds=True matched=132/132` | same | no |
| 8 | r31-c2-v3 | 0 (0) | `REVISION_BINDING_MATCH=132/132`, receipt ok | same | no |
| 9 | r32-c2-v2 | 0 (0) | `EXEMPT_AUDIT_MATCH=132/132`, `RECORD_CHECKS=ok`, receipt ok | same | no |
| 10 | r33-c1-v2 | 0 (0) | `TOPLEVEL_FIELD_MATCH=156/156`, receipt ok | same | no |
| 11 | r32-c2-v3 | 0 (0) | `EXEMPT_AUDIT_MATCH=132/132`, `RECORD_CHECKS=ok`, receipt ok | same | no |

**No row differs.** `ROWS=11`, `BATTERY_RESULT=PASS`, exit 0.

### Byte-level diff of every per-row artifact against the committed directory

`diff` of each row log against `measure-a2/battery/<row>.log`:

* `selftest.log`, `observable.log`, `r31-c1-v3.log`, `r31-c2-v3.log`, `r32-c2-v2.log`,
  `r33-c1-v2.log`, `r32-c2-v3.log` — **IDENTICAL** (byte-for-byte).
* `claims-lane-root.log`, `claims-fleet-root.log`, `chain-r3.log`, `chain-r3-broken.log` —
  differ **only** in the volatile `ts=` header timestamp (e.g. `ts=2026-10-23T19:01:04Z`
  vs `ts=2026-10-23T18:23:34Z`). No other byte differs; every verdict/finding line is equal.

The five receipts (`r31-c1-v3.json`, `r31-c2-v3.json`, `r32-c2-v2.json`, `r33-c1-v2.json`,
`r32-c2-v3.json`) differ in exactly three keys, all volatile/environmental:
`utc` (timestamp), `elapsed_s` (timing), `gate` (my clone path vs the committed lane path).
Every asserted field is equal: `predicate_holds=True`, `matched`/`total` = 132/132, 132/132,
132/132, 156/156, 132/132, `misses=[]`, `record_fails=[]`, `gate_timed_out=false`,
`gate_sha256=a6307edf687a…` (the battery's own `receipt` assertion re-checks this against
the sha it measured, and passed).

### Selftest case-line lists

* `SELFTEST_CASES=256`, `cases_sha256=f39309655fa554bb501c14f02b2a5aec7f2bb9f29171de33ffb3908037266e8d`
  — **identical** to the committed `measure-a2/battery/selftest.cases` sha256.
* First 253 case lines identical to the committed a2 list (sha256 of `head -253` =
  `98813e85eeae4e47816a32dea6d3daa0ce4a68d024b3a49ed043b19d596813d2` on both sides),
  and the first 251 lines identical to the wave-1 base list
  (`w1/ExecNoHarmBase34/selftest.cases`, sha256 `46c9c092…` both sides). New cases
  254–256 are `claims-deadzone`, `claims-deadzone-line`, `claims-deadzone-edge`.

**No-harm battery verdict: CONFIRMED, 11/11 rows, zero differences.**

---

## 2. C2 re-derivation (operability, dead zone 32765..32767)

Counter: `corpus/evidence/round34/c2-count.py`, sha256
`8c0def4d377cdf1a1e4bd2c9151bb0846216658ff14d725d15ac037c12212173` — equals the pinned
digest in the audit set and the `counter_sha256` in every committed receipt.

| run | gate | gate sha (prefix) | seed | result | exit |
|---|---|---|---|---|---|
| after | clone @707da818 | `a6307edf687a` | 6101 (fresh) | `DEADZONE_MATCH=37/37`, `predicate_holds=true`, `misses=[]`, `gate_rc=1` | 0 |
| after | clone @707da818 | `a6307edf687a` | 6102 (fresh) | `DEADZONE_MATCH=37/37`, `predicate_holds=true`, `misses=[]` | 0 |
| before | `772a1d8e4d94` extracted from `bf7c931a` | `772a1d8e4d94` | 6101 | `DEADZONE_MATCH=21/37`, `predicate_holds=false`, 16 misses | 1 |
| before | same | `772a1d8e4d94` | 6203 | `DEADZONE_MATCH=21/37`, `predicate_holds=false` | 1 |

Receipts: `…/ExecNoHarmA2/c2/c2-{after,before}-s*.json` (+ `.log`).
The pre-fix gate blob was extracted read-only with
`git -C clone show bf7c931a:tools/research-gate.sh > scratch/gate-prefix-772a1d8e.sh`
and its sha256 verified as `772a1d8e4d94dbf3a44a64bf850b1324e51546eeb62abcd7b3ec585f0e003e58`,
matching the committed `c2-before-s*.json` `gate_sha256` exactly.

* The **before** count is **21/37**, not the design's predicted "ceiling 4/37"
  (`claims-a2.md:103`). The 16 misses are exactly the long records whose truth is
  `supported`/`mislocated` (dz-verbatim-ml 3, dz-verbatim-1l 2, dz-edge 2,
  dz-decoys-exact 2, dz-decoys-line-wrong 2, dz-line-bound 2, dz-line-wrong 2,
  dz-glued-then-valid 1) — every other long record coincidentally passes on the broken
  gate because "unsupported" happens to be its truth. The stderr tail is
  `grep: regular expression is too large`. This is the same defect the lane itself
  recorded in its post-tip erratum (`b8e782a`, "claims-a2 erratum (before ceiling 21/37
  not 4/37)"). **The frozen design text at tip 707da818 still says "Expected ceiling
  4/37" (claims-a2.md:103) and does not carry that erratum** — the design's before-state
  prediction was wrong, but the *kill rule* was not tripped (the control still cannot
  reach 37/37) and P2 is unaffected. [INFERENCE] The frozen-predicate outcome is
  unchanged; only the design's stated expectation was mispredicted.
* **P2 "no committed run below 37"**: I scanned **every** commit reachable from
  `git rev-list --all` for committed JSON under `.ufo/waves/round-34/` that names the
  landed gate (`git grep -I -l "a6307edf687ac0fb" $(git rev-list --all) -- '.ufo/waves/round-34/*.json'`
  → 48 distinct paths), then read each path's blob at each commit that carries it and
  walked the JSON recursively for any `gate_sha256` starting with `a6307edf` paired with a
  `matched` < 37 → **none**. Every landed-gate C2 receipt in history reads 37/37 (seeds
  5011, 5023, 5033, 5047, plus the post-tip `c2-l1-rerun-s7001/7013` at 37/37). The
  before-state receipts (21/37) are bound to `772a1d8e`, not the landed gate, so they do
  not violate the clause. I also scanned the 159 uncommitted sibling JSON receipts under
  `.ufo/waves/round-34/w2a2/` — no landed-gate receipt below 37.

### Independent boundary probe (not via the counter)

To test the *mechanism* rather than the counter's tally, I built 22 single-claim
fixtures with spans of exactly 32758..32768 bytes in two content classes (uniform
letters; mixed punctuation/digits) and ran both gates (`scratch` only):

* pre-fix gate `772a1d8e` (`--root .`): 32758–32764 → `observed=supported`;
  **32765, 32766, 32767 → `observed=unsupported`**; 32768 → supported (chunk path).
  stderr: `grep: regular expression is too large`.
* landed gate `a6307edf`: **all 22 → `observed=supported`**, `VERDICT_BEARING_CLAIMS=22/22`,
  exit 0. (Transcript `…/ExecNoHarmA2/probes/probe2-{prefix,landed}.out`.)

I also instrumented a scratch copy of the pre-fix gate (`DBG` lines) to confirm the
routing: the direct path was taken for span lengths 32758..32767 and the chunk path for
32768 — i.e. the three dead-zone lengths really were on the direct (PCRE) path.

**Direct PCRE boundary measurement (corrected).** My first raw probe appeared to fail at
32762–32764 bytes, contradicting the design. Cause: in the *tool shell* `grep` resolves
to a busybox-style `pi-uu-grep 0.2.0` shim, not GNU grep. The gate resolves bare `grep`
via PATH inside `bash` → `/usr/bin/grep` (GNU grep 3.12-modified). Measured with the
binary the gate actually uses, one `\xHH` escape per span byte:

```
span=32763 pattern_chars=131052 rc=1 (compiles)
span=32764 pattern_chars=131056 rc=1 (compiles)
span=32765 pattern_chars=131060 rc=2 "grep: regular expression is too large"
span=32766 pattern_chars=131064 rc=2 "grep: regular expression is too large"
span=32767 pattern_chars=131068 rc=2 "grep: regular expression is too large"
```

**The design's "32764 compiles / 32765 fails" boundary reproduces exactly** on the gate's
own grep. The design's citation of "approximately 64 thousand code units" (pcre2limits,
S065) is a rough figure; the observed ceiling here is ≈131 072 pattern characters
(≈32 768 code units of 4 chars each ≈ 65 536 two-byte units). [INFERENCE] The claim's
substance (three dead-zone lengths, 32765..32767) is confirmed; only the S065 unit
phrasing is loose. The lane has already logged the grep-provenance hazard in
`corpus/lessons/round-34.md:122`.

**C2 verdict: CONFIRMED.** 37/37 on two fresh seeds on the landed gate, 21/37 before,
mechanism re-derived independently at the exact byte boundary.

---

## 3. C3 re-derivation (calibration, counted self-audit)

Tool `corpus/evidence/round34/self-audit.py` sha256 `22a6822ca79f7f5eac8d0e64ad7e6bc0fd0a46af0be8353d52884b75d246091f`
= the pinned digest in the audit set. Audit set `audit-set.json` sha256
`01f6c4b49febdd02a28d12d7ad1c623ce015219df53e4c01d0582a9369479f5c`, identical between the
clone and `git show 707da818:corpus/evidence/round34/audit-set.json`.

```
$ python3 corpus/evidence/round34/self-audit.py --set …/audit-set.json --lane .
… 43 AUDIT lines, all "ok" …
SELF_AUDIT_MISMATCHES=0
SELF_AUDIT_UNDISPOSITIONED=0
```

My re-run output is **byte-identical** to the committed
`.ufo/waves/round-34/measure-a2/audit-first-run.txt` (both sha256
`b709781c949b5f63371783b93f3b99958f6b48b413a96899de1209646af06452`) — 43 checks, 0
mismatches, 0 undispositioned, exactly as P3 requires.

**Negative control re-run (independent).** Two lies injected into a scratch copy of the
audit set (`commit-b8053900` prefix → `deadbeef`; `gate-head-digest` expect → `0*64`):

* without dispositions → `SELF_AUDIT_MISMATCHES=2`, `SELF_AUDIT_UNDISPOSITIONED=2`
* with a disposition line for `commit-b8053900` → `MISMATCHES=2`, `UNDISPOSITIONED=1`

This reproduces the committed `measure-a2/audit-negative-control.txt` exactly (2 / 2 and
2 / 1), so the tool is demonstrably able to fail and the count is not a constant.

**C3 verdict: CONFIRMED** (count 0/0, reproduced verbatim, negative control able to fail).

---

## 4. Findings

### F1 (MEDIUM, calibration) — the tip's audit set does not cover the self-assessment it claims to audit; the lane found and fixed this after the tip

The frozen tip's 43-check audit set contains **no check on `SCORECARD.md` and no numeric
check on `LOG.md`**. Its three `grep_assert` checks are: `skill-tally-256` (SKILL.md
`PASS \(256 cases\)`), `skill-tally-253-stale` (SKILL.md `PASS \(253 cases\)` absent),
`log-r34a1-lesson` (LOG.md mentions `corpus/lessons/round-34.md`).

I injected a false number into each self-assessment file in scratch copies of the tip and
re-ran the audit:

| injected lie (scratch copies of the tip) | audit result |
|---|---|
| `SCORECARD.md`: `DEADZONE_MATCH=21/37` → `99/37` | `MISMATCHES=0 UNDISPOSITIONED=0` — **not detected** |
| `LOG.md`: `Do-nothing 21/37 (seeds 5011/5023` → `99/37` | `MISMATCHES=0 UNDISPOSITIONED=0` — **not detected** |
| `SKILL.md`: `PASS (256 cases)` → `PASS (999 cases)` (all 8) | `MISMATCHES=1` — detected |
| `SKILL.md`: `PASS (256 cases)` → `PASS (256 cases, 9 skipped)` | `MISMATCHES=1` — detected |
| `SKILL.md`: `PASS (256 cases)` → `PASS (256 cases, 0 skipped)` (the *exact* banner the gate prints) | `MISMATCHES=1` — **false positive** |

The last row is the sharpest: at the tip, the tip's own `SKILL.md` reads
`PASS (256 cases)` while the gate's actual banner is `PASS (256 cases, 0 skipped)` — so
the tip's SKILL text is stale relative to the observed banner, and the tip's check
pattern `PASS \(256 cases\)` would *reject* a corrected SKILL.md. Both the coverage gap
and the stale-text/over-tight-pattern problem were subsequently fixed by the lane itself
in `b8e782a` (`git diff 707da818 b8e782a -- corpus/evidence/round34/audit-set.json`):
patterns become `PASS \(256 cases, 0 skipped\)` and `PASS \(25[0-9] cases`, and a new
`scorecard-count-assert` check on `SCORECARD.md` is added (62-check set).

Scope of the finding: it does **not** refute C3's frozen predicate — the count is 0/0 and
reproduces verbatim, which is what P3 asks. It is a **coverage** statement: at the tip,
C3's audit does not mechanically cover the round-34 SCORECARD row or the LOG entry, so
"the self-assessment matches observed repo state" is enforced only for SKILL.md and for
path/digest/receipt-binding facts. This is exactly the axis the wave-2a2 spec asks to
attack, and it is now fixed downstream.

### F2 (LOW, calibration / claim-record) — the frozen design's before-state prediction was wrong and the tip does not carry the erratum

`claims-a2.md:99-106` (frozen design v4, commit `7c7eb3a`) predicts the do-nothing
control will reach "**Expected ceiling 4/37**" (only the four short records pass).
The committed before receipts and my two independent before-runs all measure **21/37**.
The design's arithmetic ignored that every long record whose truth is `unsupported`
coincidentally matches on the broken gate. The kill rule was not tripped (the control
still cannot reach 37/37, so P2 stands), and the lane appended an erratum after the tip
(`b8e782a`: "claims-a2 erratum (before ceiling 21/37 not 4/37)"). At the frozen tip the
erratum is absent, so a reader of the frozen claim record alone would expect 4/37 and
find 21/37 in the receipts.

### Non-finding, recorded for the record

C1 (spans ≥32768 bytes) is **not re-opened** — its attempt-1 verdict
`unverified (required controls held)` is frozen, and per the contract I did not re-score
held shapes, re-author controls, or touch C1's receipts. I read C1's counter only to
confirm its digest pin in the audit set (`970cf9a709d72ed8…`, matches the tip's file).

---

## 5. Commands actually run (all read-only on the lane; no git/jj write in the lane)

```
git clone -q /home/vgpnk/Projects/shokunin/chousa-shokunin clone
git -C clone checkout -q 707da8184a0fc4d10ab3f17271556cdf364f0af5
git -C clone show bf7c931a:tools/research-gate.sh > scratch/gate-prefix-772a1d8e.sh
sha256sum <gate> clone/tools/research-gate.sh scratch/gate-prefix-772a1d8e.sh
bash clone/.ufo/waves/round-34/w1/ExecNoHarmBase34/battery.sh <clone gate> <outdir>
python3 corpus/evidence/round34/c2-count.py --gate <gate> --seed {6101,6102,6203} --receipt …
python3 corpus/evidence/round34/self-audit.py --set … --lane . [--dispositions …]
bash <gate> verify-claims <fixture> --root .        # boundary probe, both gates
git -C clone log/ls-tree/rev-list/show/diff …       # read-only
```
No `git`/`jj` write, no commit, no push, no production-file mutation in
`/home/vgpnk/Projects/shokunin` or `chousa-shokunin`; the only writes under the lane are
this report and `.ufo/waves/round-34/w2a2/ExecNoHarmA2/`. `df -h /fast` before the work:
41 G available (95 % used); scratch total 437 MB. No network access was made. No process
was signalled. Timeouts: battery 1750 s, counters 600 s, selftest 600 s.

## 6. Limits

* Battery re-run used the **clone's** gate (byte-identical to the lane's, pinned by sha)
  and the **lane's** counters/fixtures/`SCORECARD.md` (all byte-identical between clone
  and lane at the tip — verified by sha256 for all five counters and all three fixtures
  plus `SCORECARD.md`). The `observable` row's command embeds `bash tools/research-gate.sh`
  relative to the lane root, so it exercised the **lane working tree's** gate; that file's
  sha256 is the same `a6307edf687a…`, so the row is equivalent.
* The committed summary lists per-row *expected* values but not the raw stdout; my
  byte-level diff therefore compares against the committed per-row logs and receipts,
  which is the stronger comparison.
* `claims-lane-root`/`claims-fleet-root`/`chain-*` rows differ in their `ts=` header only;
  I did not re-derive the claim/chain semantics beyond the battery's own assertions.
* The F1/F2 findings concern the **frozen tip's** audit set and design text. Both were
  amended in the lane's later commit `b8e782a` (master is now `6a3cc32`), which is
  *past* this wave's frozen tip; I report them as tip-state facts, and note the fix.
* I did not evaluate C2's shortcut controls (window/chunk/keyed shapes) — those are other
  seats' attack surfaces.
