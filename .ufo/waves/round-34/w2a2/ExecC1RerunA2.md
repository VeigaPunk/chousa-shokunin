# ExecC1RerunA2 — round 34 attempt 2, wave 2a2

Seat: C1 no-harm **by counter** on the landed (C2-fixed) gate, plus falsification of the C2/C3
committed measurements and the frozen claim record. Lane tip frozen by contract at
`707da8184a0fc4d10ab3f17271556cdf364f0af5`; scratch
`/fast/scratch/hyaku/chousa-r34-a2/w2/ExecC1RerunA2/`. Read-only on all lane production files;
no git/jj write command was issued by this seat. No tool installed, no network use.

---

## 0. Pins and setup

| item | value | how |
|---|---|---|
| clone | `/fast/scratch/hyaku/chousa-r34-a2/w2/ExecC1RerunA2/clone` | `git clone -q <lane> clone && git -C clone checkout -q 707da8184a0fc4d10ab3f17271556cdf364f0af5` |
| clone gate sha256 | `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b` | `sha256sum clone/tools/research-gate.sh` |
| worktree gate sha256 (lane) | `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b` | `sha256sum tools/research-gate.sh` |
| gate blob at `707da818` | `a6307edf…2995b` | `git show 707da818:tools/research-gate.sh \| sha256sum` |
| c1-count-v3.py | `970cf9a709d72ed8b3ec91eeabc2b1778831f695b5ea18b40f026489f7f2da2a` | worktree == `git show 707da818:…` |
| c2-count.py | `8c0def4d377cdf1a1e4bd2c9151bb0846216658ff14d725d15ac037c12212173` | == pinned value in the frozen audit set |
| old (pre-C2) gate | `772a1d8e4d94dbf3a44a64bf850b1324e51546eeb62abcd7b3ec585f0e003e58` | `git show bf7c931a:tools/research-gate.sh` |
| base (pre-C1) gate | `43a1af35ca668fe535fcef1e68b0c64bbba3eada59c7a23181f591901fca4346` | `git show 3026a4e5^:tools/research-gate.sh` |

The gate diff between `772a1d8e` and `a6307edf` is exactly `TOK_DIRECT_SPAN_MAX=32767 → 32764`
plus the C2 selftest cases 254–256 (`diff` of the two blobs; one hunk of constants/comments, one
hunk of new selftest cases). No other matcher change — confirms the C2 fix's stated scope.

**Lane tip moved during this wave.** Commits `b8e782a, 0b0af3e, 50a8c69, 60b41da, 53e4aa0` landed
after the contract's frozen tip. The gate blob and `c1-count-v3.py` are byte-identical across all
of them (`a6307edf…` / `970cf9a7…` at every one), so every measurement below is valid for the
landed gate at the new tip `53e4aa0` as well. My receipts are committed at `53e4aa0`.

---

## 1. Verdict for my assigned item — **PASS**

**C1 no-harm by counter on the new gate.** `c1-count-v3.py` on the landed gate `a6307edf` on four
fresh seeds (none of 3601–3603): **LONGSPAN_MATCH=42/42** every time, `gate_rc=1`,
`gate_timed_out=false`, `misses=[]`, **all 17 classes full** (no class below n/n).

| seed | locale | label | gate_rc | elapsed_s | receipt |
|---|---|---|---|---|---|
| 4601 | `LC_ALL=C` | 42/42 | 1 | 34.79 | `c1v3-a2-s4601.json` |
| 4602 | `LC_ALL=C` | 42/42 | 1 | 55.94 | `c1v3-a2-s4602.json` |
| 4603 | `LC_ALL=C` | 42/42 | 1 | 30.85 | `c1v3-a2-s4603.json` |
| 4604 | UTF-8 (`en_US.UTF-8`, no `LC_ALL`) | 42/42 | 1 | 44.09 | `c1v3-a2-s4604-utf8.json` |

Command (seed 4601; identical form for the rest):

```
LC_ALL=C C1_TMP=<scratch>/tmp4601 timeout 1800 python3 clone/corpus/evidence/round34/c1-count-v3.py \
  --gate clone/tools/research-gate.sh --seed 4601 \
  --receipt <lane>/.ufo/waves/round-34/w2a2/ExecC1RerunA2/c1v3-a2-s4601.json
```

Exit 0. Receipts (sha256):
`c1v3-a2-s4601.json` `d037e0ccca7780721cb5904d4ab2c616ad57ae9806daa50083b8051d66bad8c9` ·
`c1v3-a2-s4602.json` `cf5640ff4bbb734ed3e24d27ed1554f8183e97050287e4d469761fc4f045d278` ·
`c1v3-a2-s4603.json` `13d6ab54c456c474425be7517d3c656b460b6c0dc60ad1476f9748c016fca945` ·
`c1v3-a2-s4604-utf8.json` `92e03bb428dbd3c4efdf0843fac535155d21818a4e98aa3f17f5b844abf16474`.
Every receipt records `gate_sha256=a6307edf…` and `counter_sha256=970cf9a7…`.

### The gap this closes (calibration finding, MEDIUM)

**Before this seat ran, the lane had no committed `c1-count-v3` receipt on the landed gate.**
Every committed C1 v3 receipt in the tree binds the *pre-C2* gate `772a1d8e`:

```
.ufo/waves/round-34/measure/c1v3-s3601.json       -> 772a1d8e…  LONGSPAN_MATCH=42/42
.ufo/waves/round-34/measure/c1v3-s3602.json       -> 772a1d8e…  LONGSPAN_MATCH=42/42
.ufo/waves/round-34/measure/c1v3-s3603-utf8.json  -> 772a1d8e…  LONGSPAN_MATCH=42/42
.ufo/waves/round-34/w2/R34RerunC1v3/c1v3-s{4211,5177,6301}.json -> 772a1d8e…  42/42
```

(a full sweep of every tracked file whose content mentions `LONGSPAN_MATCH` at `707da818` finds
**zero** rows with `gate_sha256=a6307edf…`.) Two consequences:

1. P1 v3's second clause — "no committed run of this counter **on the landed gate** prints a lower
   count" (`claims.md:157-159`) — was satisfied **vacuously**: there were zero landed-gate runs.
   My four receipts are the first landed-gate C1 v3 measurements, and all four are 42/42, so the
   clause now holds non-vacuously.
2. `SCORECARD.md:1973` (C1 capability row) and `SKILL.md:89` point their C1 evidence at
   `.ufo/waves/round-34/measure/` / "landed `772a1d8e`: 42/42 ×3". At the frozen tip those
   pointers name receipts bound to a gate that is no longer landed. `SKILL.md:89` still reads
   "landed `772a1d8e`" at the new tip `53e4aa0` — stale naming of the landed gate. The
   capability row's evidence pointer (`SKILL.md:89`, `SCORECARD.md:1973`) does not bind to the
   landed gate until this seat's receipts are cited. This is a pointer defect, not a capability
   defect: the gate itself measures 42/42.

The claim-record side of C1 was not re-scored here (the frozen exclusion on held controls stands;
this seat only ran the counter and its controls, and did not re-author any held shape).

---

## 2. Controls — the counter can fail, and what it can and cannot see

All counters are the committed `c1-count-v3.py` / `c2-count.py`; only the gate differs.

| # | gate under test | counter | seed | result |
|---|---|---|---|---|
| C1-a | base pre-C1 `43a1af35` (do-nothing) | c1 v3 | 4601, 4602 | **25/42**, exit 1 (both) |
| C1-b | old pre-C2 `772a1d8e` | c1 v3 | 4601, 4602 | 42/42, exit 0 (both) |
| C1-c | landed `a6307edf` | c1 v3 | 4601–4604 | 42/42, exit 0 (all) |
| C2-a | old pre-C2 `772a1d8e` (do-nothing) | c2 | 5501 | **21/37**, exit 1 |
| C2-b | landed `a6307edf` | c2 | 5501 | **37/37**, exit 0 |

* **C1-a reproduces the committed do-nothing number exactly.** The committed L1 receipt
  `.ufo/waves/round-34/controls/L1-base-v3/base-v3-C-s3493.json` says `LONGSPAN_MATCH=25/42`,
  `gate_sha256=43a1af35…`, `elapsed_s=234.924`; my two independent runs on the same gate give
  25/42 with the same failing-class signature (all 8 "long-*" supported/mislocated classes 0/n).
  So the 42/42 on the landed gate is a measurement, not a vacuous pass.
* **C2-a reproduces the committed do-nothing control exactly.** Committed
  `measure-a2/c2-before-s5011.json` = 21/37; my fresh seed 5501 on the same gate = 21/37 with
  an **identical per-class pattern** (dz-verbatim-ml 0/3, dz-verbatim-1l 0/2, dz-edge 0/2,
  dz-decoys-exact 0/2, dz-decoys-line-wrong 0/2, dz-glued-then-valid 0/1, dz-line-bound 0/2,
  dz-line-wrong 0/2; the 4 short records and all 17 unsupported-truth long records pass).
  So C2's before/after pair (21/37 → 37/37) is re-derivable with one command, as claimed.

### Mutation tests against the landed gate (scratch copies only)

| mutant | change | c1 v3 (seed 4601) | c2 (seed 5501) |
|---|---|---|---|
| A | chunk matcher confirms only the first 2048 bytes of the span | **29/42** | **26/37** |
| B | probe chunk shrunk 4096 → 512 bytes (whole-span confirmation kept) | 42/42 | — |
| C | `TOK_DIRECT_SPAN_MAX` reverted 32764 → **32767** (pre-C2) | 42/42 | **21/37** |
| D | `TOK_DIRECT_SPAN_MAX` → 65536 (chunk path effectively off) | **25/42** | **21/37** |
| E | `TOK_DIRECT_SPAN_MAX` → 1024 (over-conservative) | 42/42 | — |
| F | `TOK_DIRECT_SPAN_MAX` → 32766 | — | **25/37** |
| G | `TOK_DIRECT_SPAN_MAX` → 32700 | — | 37/37 |

Reading:

* **The C2 counter is a genuine detector of the C2 fix.** Reverting the routing constant (C) or
  nudging it by one byte (F) drops it to 21/37 / 25/37. Lowering it further (G) still gives 37/37,
  i.e. the predicate does not pin the exact constant, only that 32765..32767 route to the chunk
  matcher. That matches the claim's wording ("no other matcher change").
* **The C1 counter is blind to the C2 routing constant** (C, E → 42/42). Expected and correct:
  every C1 span is ≥32768 and always takes the chunk path, so C1's 42/42 on the landed gate does
  not depend on the C2 change and cannot be a false positive from it. The two counters partition
  the surface; they do not substitute for each other.
* **Both counters catch a truncated chunk confirmation** (A: 29/42 and 26/37) and a disabled chunk
  path (D). Mutant B (shorter probe, confirmation intact) correctly stays at 42/42 — the probe
  size is a performance knob, not a correctness one, so 42/42 is the right answer there.

---

## 3. Falsification of the frozen claim record (claims-a2.md) — one confirmed defect

`corpus/evidence/round34/claims-a2.md:100-103` (the C2 "Before (do-nothing control)" paragraph),
read at the contract's frozen tip `707da818`:

> "The 17 long-supported records (3+2+2+2+2+1… the classes whose truth is supported and whose
> span is in the dead zone) must miss: every record with a 32765..32767-byte span fails with
> 'regular expression is too large', short records (4) pass. **Expected ceiling 4/37.**"

**The prediction is wrong, and internally inconsistent.** The parenthetical sum `3+2+2+2+2+1`
is 12, not 17. The committed counter's own class table (`c2-count.py` `CLASS_COUNTS`) gives:
12 long-supported + 4 long-mislocated + 17 long-unsupported + 4 short = 37. So:

* 16 records (12 supported + 4 mislocated) must miss — not 17.
* The 17 long records whose truth is **unsupported** (mutations, decoys, split, glued) coincidentally
  **pass** on the broken gate: grep refuses the pattern, the span reads `observed=unsupported`, and
  that is exactly their truth. Plus the 4 short records → the real do-nothing score is
  **21/37**, not 4/37.

I re-derived 21/37 on a fresh seed (5501) with the identical per-class signature (§2, C2-a), so
the arithmetic in the frozen design is the only thing wrong; the committed receipts and the
SCORECARD's "do-nothing 21/37" are right.

**Status at report time:** this is already corrected upstream. The erratum landed in the
post-frozen-tip commits (`b8e782a` onward, `claims-a2.md` "Erratum (post-data; evidence pointers
only — counter, TOTAL, P2 and the kill rule unchanged)"), stating the 21/37 figure and the
16-record miss set, and crediting wave seats `RevC2Receipts` and `ExecC2Rerun`. I reached the
same conclusion independently from the class table and a fresh-seed run. **No P2/kill-rule
consequence:** the do-nothing control still cannot reach 37/37, so the "if the do-nothing control
meets 37/37 the counter or target is wrong" guard was never tripped. This finding is recorded as
corroboration of the shipped erratum, not as a live defect.

Other C2 claim text I checked and found **correct**: 37 records / 17 classes; `dz-edge` lengths
exactly 32765 and 32767; `dz-decoys` 12 near-copies and no exact copy (`DECOYS_ABSENT=12`);
`dz-decoys-exact`/`dz-decoys-line-wrong` 11 decoys + 1 exact (`DECOYS=11`); the counter's
`DZ_MIN/DZ_MAX = 32765/32767`; the matching rule and the 1500 s bound.

---

## 4. C3 — self-audit re-derivation, and one real weakness in the frozen tool

**Reproducibility (P3's second clause) holds.** Running the committed
`corpus/evidence/round34/self-audit.py` with the committed `audit-set.json` against the frozen
tip, twice:

```
python3 clone/corpus/evidence/round34/self-audit.py --lane clone
→ SELF_AUDIT_MISMATCHES=0
  SELF_AUDIT_UNDISPOSITIONED=0
```

Two runs are byte-identical (`diff -q` → identical), over 43 checks, exit 0. Same output as the
committed `measure-a2/audit-first-run.txt`.

**Negative control reproduces.** Injecting two broken pointers (a missing path, a wrong sha256)
into a *scratch copy* of the set gives `SELF_AUDIT_MISMATCHES=2 / SELF_AUDIT_UNDISPOSITIONED=2`,
matching the committed negative control's "2 counted". The tool is not a 0/0 stub.

**Audit-set immutability holds.** `audit-set.json` is byte-identical
(`sha256=01f6c4b49febdd02a28d12d7ad1c623ce015219df53e4c01d0582a9369479f5c`, 43 checks) at
`0af0844` (first counted run), `fce3119`, `bd8c8bd` and `707da818` — no check edited or deleted
after the first counted run, as C3's kill rule requires. (`audit-set.json` does not exist at
`fe0f22e` because `0af0844`, its parent, is where the file was added.)

**Weakness (MEDIUM) — the frozen tool's `path` kind reads the working tree, not HEAD.**
The frozen `self-audit.py` (`22a6822c…`, the version at `707da818`) implements `path` as
`os.path.exists(os.path.join(lane, chk["path"]))` (line 86) — filesystem existence, not
"committed bytes". Proof: in the scratch clone I created an **untracked** file
`corpus/evidence/round34/UNTRACKED-PROBE.md` and added a `path` check for it to a scratch copy of
the set; the tool printed `AUDIT id=probe-untracked-path ok exists` and kept
`SELF_AUDIT_MISMATCHES=0 / UNDISPOSITIONED=0`. A file that exists only in the worktree satisfies
a "committed" check. C3's own surface sentence is "the lane's round-34 self-description
(SCORECARD rows, LOG entry, SKILL.md tallies, SHONEN evidence pointers) matches **committed
bytes**" — the frozen tool cannot establish that for the 20 `path` checks (43% of the set).

Two further coverage gaps in the frozen 43-check set, both measured:

* **Zero SCORECARD checks.** `grep -c SCORECARD` on the frozen `audit-set.json` = **0**. The set
  covers SKILL.md (2 `grep_assert`) and LOG.md (1 `grep_assert`) but never the SCORECARD rows that
  C3's surface names first. The SCORECARD's own C1/C2 rows are the text most at risk of drifting
  from observed state — precisely the calibration axis under test.
* **`path` checks are existence-only.** 20 of 43 checks assert only that a file exists; none
  compares its content to what the SCORECARD/LOG/SKILL claim about it.

**Status at report time:** both gaps are closed upstream by the post-frozen-tip commits. The
`b8e782a`+ tool (`e9b0c93f…`) switched to HEAD-byte reads (`head_bytes`, detail text "tracked at
HEAD"), added `receipt_gate_file`, and prints `SET_SHA256=`; the set grew 43 → **62 checks** with
one SCORECARD reference, and the 62-check set at `53e4aa0` is what produced the final
`K=1 / UNDISPOSITIONED=0` receipt. `audit-dispositions.md` now carries the supersession lines for
the two dropped tool-digest pins. Again: corroboration of shipped repairs, not live defects.

---

## 5. Re-derivation of other committed measurements

* **Selftest 256** — `TMPDIR=<scratch> bash clone/tools/research-gate.sh --selftest` → exit 0,
  `RESEARCH_GATE_SELFTEST: PASS (256 cases, 0 skipped)`, 256 `ok-case` lines, 0 `FAIL-case`.
  Matches `SKILL.md` ("PASS (256 cases)") and the committed `measure-a2/battery/selftest.log`.
* **PCRE dead-zone boundary** — direct probe with `grep -a -z -o -P`:
  pattern of 32763/32764 escapes → rc=1 (compiles); 32765/32766/32767 → rc=2,
  `grep: regular expression is too large`; 32768 → `OSError: [Errno 7] Argument list too long`.
  This independently confirms the claimed boundary (32764 compiles, 32765 fails, ≥32768 hits the
  argv ceiling) on this host.
* **Battery coverage** — confirmed the premise of my seat:
  `.ufo/waves/round-34/w1/ExecNoHarmBase34/battery.sh` runs `round31/c1-count-v3.py`,
  `round31/c2-count-v3.py`, `round32/c2-count-v2.py`, `round33/c1-count-v2.py`,
  `round32/c2-count-v3.py` — and states at lines 23-24 that it never invokes
  `corpus/evidence/round34/c1-count.py` or `round33/c1-count.py`. It does **not** run
  `round34/c1-count-v3.py`, so the C2 change was never counter-checked on C1's own surface by the
  battery. That is exactly the hole this seat filled (§1).

---

## 6. Artifacts (all inside `.ufo/waves/round-34/w2a2/ExecC1RerunA2/`, 176 KB total)

Receipts (JSON, committed at tip `53e4aa0`): `c1v3-a2-s4601.json`, `c1v3-a2-s4602.json`,
`c1v3-a2-s4603.json`, `c1v3-a2-s4604-utf8.json`, `c2-count-a2-s5501.json`,
`c2-count-before-s5501.json`, `c2-count-mutC-max32767-s5501.json`,
`c2-mutA-win2048-s5501.json`, `c2-mutD-nochunk-s5501.json`, `c2-mutF-max32766-s5501.json`,
`c2-mutF-max32700-s5501.json`, `ctrl-oldgate-s460{1,2}.json`, `ctrl-basegate-s460{1,2}.json`,
`mut-A-win2048-s4601.json`, `mut-B-chunk512-s4601.json`, `mut-C-max32767-s4601.json`,
`mut-D-nochunk-s4601.json`, `mut-E-max1024-s4601.json`.

Logs: `logs/` (20 files — counter stdout per run, `audit-run1.txt`, `audit-run2.txt`,
`audit-negctl.txt`, `selftest-landed.log`).

Scratch (not in the lane): `/fast/scratch/hyaku/chousa-r34-a2/w2/ExecC1RerunA2/` — clone,
`gate-old-772a1d8e.sh`, `gate-base-43a1af35.sh`, `mut-gate-{A,B,C,D,E,F}.sh`,
`scratch-audit-set-negctl.json`, `scratch-set-untracked-probe.json`.

---

## 7. Limits

* The claim-record defect in §3 and the tool weakness in §4 were **already fixed** by commits that
  landed after the contract's frozen tip. I report them as independently reproduced
  (fresh-seed 21/37; untracked-file path check; 2-injected-lie negative control), not as live
  defects. I did not re-open C1's held-shape exclusion and did not re-score held controls.
* No committed receipt existed on the landed gate for C1 v3 before this seat (§1); the gap is now
  closed by four receipts, but the SKILL/SCORECARD **pointers** still name the pre-C2 gate
  (`772a1d8e`) as "landed" at tip `53e4aa0`. That pointer text is lane production and outside my
  write scope; I flag it for the parent.
* The C2 predicate does not pin the exact routing constant (mutant G, 32700 → 37/37). The claim
  only asserts that 32765..32767 route to the chunk matcher, so this is within the stated contract,
  but a lower constant would be equally acceptable to the counter — worth knowing before any future
  refactor of `TOK_DIRECT_SPAN_MAX`.
* `elapsed_s` for the C1 runs (30–56 s) is well inside the 1500 s bound; the UTF-8-locale run was
  not slower than the `LC_ALL=C` ones here, unlike the base gate's UTF-8 timeouts.
* All timings are from a single loaded host at 2026-10-23; no cross-host claim is made.

**Verdict: my assigned item PASSES (42/42 on four fresh seeds on the landed gate, with the
committed do-nothing control reproduced at 25/42). C2's committed 21/37 → 37/37 pair is
independently reproducible on a fresh seed with an identical per-class signature. C3's committed
0/0 reproduces verbatim and its negative control reproduces. The frozen claim record contained one
arithmetic error (§3) and the frozen auditor had two real coverage weaknesses (§4); both are
already repaired in the commits that landed after the frozen tip.**
