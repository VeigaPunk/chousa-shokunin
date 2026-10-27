# R59Executor14 — round-58 C1 positive-verdict-path: inspect and run the frozen counter in isolated scratch

Assignment: "In isolated scratch only, inspect and run exact round58 frozen counter/tool or controls
relevant to positive-verdict-path defect. Use `/fast/scratch/hyaku/chousa-r59/R59Executor14`; report
exact command/output. Never edit lane files." Axis: operability.

Result: the round-58 frozen C1 positive verdict is **structurally unreachable**. A builder that satisfies
every one of the counter's 11 legs (4 safe + 7 refusal) still prints `REFUSE=0/7` and `C1=FAIL`,
because the refusal legs emit the lowercase marker `=pass(refused)` (line 51 `PASS = "pass"`; lines 147,
160) while the aggregation tests for uppercase `"=PASS"` (line 391). Two further positive-path defects
were reproduced: the control clause is unenforced by the frozen predicate command, and the
`SYMLINK_OUT` leg scores a silently-accepting builder as `pass(refused)`.

No lane file, counter, control, quote set, claim or counter was edited. No install was performed; only
system `python3` (3.14) stdlib. No git/jj/index write, no live fetch. Scratch
`/fast/scratch/hyaku/chousa-r59/R59Executor14` removed after the run; all outputs are quoted below.

## Provenance gap (reading, not judged)

`corpus/evidence/round59/claims.md` (the frozen claims path named in the wave context) did not exist
when this seat read it; `corpus/evidence/round59/` held only `census-start.txt` and an empty `controls/`.
Round-59 claims therefore cannot be cited here. This seat used the round-58 frozen artifacts named in
`corpus/evidence/round58/claims.md`, which are the only frozen positive-verdict predicate in the lane.
At 15:14 (after this seat's first read) a sibling landed `corpus/evidence/round59/controls/c1-before.txt`;
it is byte-identical to this seat's P0 output minus its `EXIT=1` line, so the round-59 "before" state
still carries the defect reproduced below.

## Pinned bytes actually run

```
65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f  corpus/evidence/round58/c1-count.py
dbb859612f9d018296b217baec76a5c6cb744609b7c95372dabae4d6691c8503  corpus/evidence/round58/c2-count.py
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  tools/build-spans.py
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  corpus/evidence/round58/controls/build-spans-r55.py
e7721cefe050ee435d3bab811ed65933d26a865ca30340feaab3f9388c3572fb  corpus/evidence/round58/controls/REFUSEALL.py
```

`tools/build-spans.py` is still the pinned r55 builder (same sha256 as the frozen `build-spans-r55.py`
control): **the lane contains no round-58 candidate builder**. Scratch held a byte copy
`frozen/c1-count.py` (+ `frozen/controls/`) so `HERE`-relative lookups (`BEFORE_BUILDER`, control
recursion `HERE/c1-count.py`) resolved exactly as in the lane.

## P0 — the exact frozen predicate reproduces the frozen receipt

```
$ cd /fast/scratch/hyaku/chousa-r59/R59Executor14
$ PYTHONDONTWRITEBYTECODE=1 python3 -B frozen/c1-count.py \
    --builder /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py \
    --work /fast/scratch/hyaku/chousa-r59/R59Executor14/work-baseline
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)
SYMLINK_OUT=fail(rc=0, expected refusal)(target-dir-written!)
SYMLINK_CACHE=fail(rc=0, expected refusal)
FIFO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'FIFO', 'REGTYPE', 'SYMLINK'] absent in 'build-spans: refused S571: no defined text form for f4088c6d6da1f4763182a51d (raw neither OLE nor zip, no .txt)\n')
DEVZERO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'SIZE', 'SYMLINK', 'REGTYPE'] absent in 'build-spans: refused S581: no defined text form for a172f04219497476db868414 (raw neither OLE nor zip, no .txt)\n')
FAT_RAW=fail(rc=1, reason ['SIZE'] absent in 'build-spans: refused S551: capture-text refused f96cbd6d82dbae8a8e2c6223.raw: ole-malformed: sector shift 0, mini shift 0\n')
MANY_QUOTES=fail(rc=0, expected refusal)
ESCAPE_ENTRY=pass(refused)
HELDOUT_OK=pass
BEFORE_FOREIGN=deleted
DENIED=0/0
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
```
(exit status 1; the counter prints no `EXIT` line — the shell reported `Command exited with code 1`.)

`diff <(grep -v '^EXIT=' corpus/evidence/round58/controls/c1-before.txt) baseline.out` →
`IDENTICAL_TO_FROZEN_RECEIPT`. The frozen predicate is reproducible from a clean scratch work root.

## P1 — a builder that satisfies all 11 legs still cannot reach `C1=PASS`

Scratch-only stub `stub-maxleg.py` (no claim; implements the leg contracts of the counter's own
fixtures: symlink/`NOT_REGULAR`/size/rows/foreign/`..` refusals before any write, OLE form via the
lane's pinned `tools/capture-text.py`, span/digest/offset formula of `expect_ok`).

```
$ PYTHONDONTWRITEBYTECODE=1 python3 -B frozen/c1-count.py --builder stub-maxleg.py --work work-maxleg
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=pass(refused)
SYMLINK_OUT=pass(refused)
SYMLINK_CACHE=pass(refused)
FIFO_TXT=pass(refused)
DEVZERO_TXT=pass(refused)
FAT_RAW=pass(refused)
MANY_QUOTES=pass(refused)
ESCAPE_ENTRY=pass(refused)
HELDOUT_OK=pass
BEFORE_FOREIGN=deleted
DENIED=0/0
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
EXIT=1
```

All 11 legs individually report pass and the discriminant leg is satisfied, yet the verdict is `FAIL`
and `REFUSE=0/7`. Same builder, full frozen controls dir:

```
$ PYTHONDONTWRITEBYTECODE=1 python3 -B frozen/c1-count.py --builder stub-maxleg.py \
    --work work-maxleg-ctrl --controls frozen/controls
...
CONTROL_REFUSEALL=denied
CONTROL_build-spans-r55=denied
DENIED=2/2
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=FAIL
EXIT=1
```

Both controls are denied and the summary line reports `OK=4/4 … BEFORE_FOREIGN=deleted`, yet the
positive verdict is still withheld. The blocker is the marker comparison, not the battery.

## P2 — the marker defect is the sole blocker (calibration copy, scratch only)

Copy `cal/c1-count.py` differs from the frozen counter by exactly two tokens (`diff -u frozen/c1-count.py
cal/c1-count.py`):

```
-    ref_pass = all(("=PASS" in l) for l in ref_legs)
+    ref_pass = all(("=pass" in l) for l in ref_legs)
-          f"REFUSE={sum('=PASS' in l for l in ref_legs)}/{len(ref_legs)} "
+          f"REFUSE={sum('=pass' in l for l in ref_legs)}/{len(ref_legs)} "
```

```
$ python3 -B cal/c1-count.py --builder stub-maxleg.py --work work-cal-nocontrols
...
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=PASS
EXIT=0
```

With only that normalization the positive path is reachable and the summary is internally consistent
(`OK=4/4 REFUSE=7/7`). Nothing else in the gate blocks a PASS.

## P3 — the controls clause is unenforced on the frozen predicate command

The claim says "Do-nothing controls must not reach `C1=PASS`", but the frozen predicate command in
`claims.md` is `--builder <builder> --work <fresh-absolute-dir>`: no `--controls`. `denied_pass =
(denied == total) if total else True` (line 393) makes that clause vacuously true.

```
$ python3 -B cal/c1-count.py --builder stub-maxleg.py --work work-cal-nocontrols   # no --controls
DENIED=0/0
C1=PASS
```

Two more control-gate holes, both reproduced on the calibrated copy:

```
$ python3 -B cal/c1-count.py --builder stub-maxleg.py --work work-cal-partial \
    --controls ctrl-partial            # contains ONLY REFUSEALL.py
CONTROL_REFUSEALL=denied
DENIED=1/1
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=1/1
C1=PASS

$ python3 -B cal/c1-count.py --builder stub-maxleg.py --work work-cal-empty \
    --controls ctrl-empty              # empty directory
DENIED=0/0
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=PASS
```

`if not ctrl.is_file(): continue` (line 369) precedes `total += 1` (line 371), so a missing control is
dropped from the denominator instead of failing the gate. The full frozen controls dir does pass:

```
$ python3 -B cal/c1-count.py --builder stub-maxleg.py --work work-cal-full --controls cal/controls
CONTROL_REFUSEALL=denied
CONTROL_build-spans-r55=denied
DENIED=2/2
C1=PASS
```

## P4 — `SYMLINK_OUT` scores silent hazard acceptance as a refusal

Frozen counter, scratch-only variant `stub-noop.py` (identical to the max-leg stub except that a
symlinked `--out` is accepted silently: `return 0`, no write, nothing created in the target):

```
$ python3 -B frozen/c1-count.py --builder stub-noop.py --work work-noop
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=pass(refused)
SYMLINK_OUT=pass(refused)
SYMLINK_CACHE=pass(refused)
...
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
```

The leg line is byte-identical to the refusing builder's. Cause: `expect_refuse` uses **inverted**
forbidden-touch semantics — `if not p.exists(): return FAIL("... was touched/removed")` (line 158) —
and `main` then overwrites whatever `expect_refuse` returned with `f"SYMLINK_OUT={PASS}(refused)"`
when the target directory is empty (lines 232-235). A builder that never refuses (rc=0, accepted the
hazard) therefore reports `pass(refused)`; the leg cannot distinguish refusal from silent acceptance.

## P5 — crash and denial are scored identically

```
$ python3 -B frozen/c1-count.py --builder frozen/controls/REFUSEALL.py --work work-refuseall
EXIT=1
--- stdout --- (empty)
--- stderr (tail) ---
FileNotFoundError: [Errno 2] No such file or directory:
  '.../work-refuseall/out-empty/spans/S777-1.txt'
--- C1= lines: 0
```

The frozen REFUSEALL control is scored `denied` (P1, second block: `CONTROL_REFUSEALL=denied`) only because the
child produces no `C1=` line: the counter crashes writing the FOREIGN fixture into `out-empty/spans/`
after the control refused EMPTY_OK. A control that crashed for an unrelated reason, or a *candidate*
that fails EMPTY_OK, is likewise indistinguishable from a scored denial; the counter itself emits no
`C1=` verdict line at all in that case.

## Defects (frozen line references)

| # | Where | Defect | Effect on positive verdict |
|---|---|---|---|
| D1 | `:51`, `:147`, `:160`, `:315` vs `:391`, `:399` | `PASS = "pass"` is emitted as `=pass(...)`; aggregation requires `"=PASS"` | `ref_pass` is constant `False`; `C1=PASS` unreachable for any builder (P1) |
| D2 | `:393` | `denied_pass = (denied == total) if total else True`; the frozen predicate passes no `--controls` | control clause vacuous under the exact frozen command (P3a) |
| D3 | `:369`-`:371` | missing control `continue`s before `total += 1` | a removed/renamed control cannot fail the gate (P3b, P3c) |
| D4 | `:158`, `:232`-`:235` | inverted forbidden-touch test, masked by an unconditional leg override | hazard acceptance scored as refusal; `target-dir-written` suffix cannot fail the leg (P4) |
| D5 | `:377` | control recursion reads only the first `C1=`-prefixed line; crash ⇒ no line ⇒ `denied` | crash and clean denial are indistinguishable (P5) |
| — | `:389`-`:390` | first `ok_pass` assignment overwritten by a looser substring test | dead stricter predicate; `=pass` accepted anywhere in the line |

## Calibration requirements implied for a round-59 positive verdict

Derived from the reproductions above, stated as requirements (no lane edit made):

1. One marker constant for emission and aggregation: either emit `=PASS` from `expect_refuse`/the
   `SYMLINK_OUT` override, or compare against the shared `PASS` constant in `ref_pass` and `SUMMARY`.
   A positive verdict must be reachable by an all-legs-passing builder (P2 shows this is sufficient).
2. The verdict must require the control count explicitly (`total == N named controls`), not
   `denied == total` over whatever files happen to exist, and the frozen predicate command must pass
   `--controls` so `DENIED` is never `0/0` on the declared path.
3. `SYMLINK_OUT` must accept only `rc != 0` plus a named refusal reason with an empty target dir, with
   no override that rewrites a failing `expect_refuse` result; `expect_refuse`'s forbidden-touch test
   must fail when the path **exists** (touched), not when it is absent.
4. A builder that fails a safe leg must yield a scored `C1=FAIL` line, and control denial must be a
   parsed verdict, not the absence of one.

## What this does not establish

- `stub-maxleg.py` is scratch-only and implements no claim; P1/P2 show the *gate* behaviour, not that
  any lane builder satisfies C1. No round-58 candidate exists to run (`tools/build-spans.py` is the
  r55 pin, sha256 above).
- `c2-count.py` (`dbb8596…`) was read, not run: its positive path is
  `verdict='PASS' if not errors and sub_ok and inf_ok and rebuilt`, with `sub_ok`/`inf_ok`/`rebuilt`
  initialised `False`, so it has no vacuous-true component analogous to D1/D2; its PASS path was not
  exercised because no round-58 C2 entry/manifest exists.
- Round-59 claims were unavailable (see Provenance gap); nothing here judges round-59 items.

## Risks / blockers

- Any round-59 item that reuses the round-58 counter bytes unchanged inherits D1: no calibrated
  positive verdict is possible from it, so an "all legs pass" receipt would still read `C1=FAIL` and
  could be misread as builder failure.
- Fixing only D1 makes the frozen predicate print `C1=PASS` with `DENIED=0/0` (P3a) — the control
  clause must be fixed in the same change, or a positive verdict certifies nothing about controls.
- Scratch `/fast/scratch/hyaku/chousa-r59/R59Executor14` was removed before yield; the exact outputs
  needed to re-derive each probe are quoted verbatim above.

## Scratch namespace note (corrected by the second instance)

The first instance removed its scratch directory and yielded; a **second concurrently dispatched
instance of the same seat** (this report's appended section below, started 15:19, still running when
the first instance wrote) then rebuilt `/fast/scratch/hyaku/chousa-r59/R59Executor14/probe/`
(`builder-probe.py`, `controls/`, `cal/c1-count.py`, `work/*`). Those bytes belong to seat
`R59Executor14`, not to a foreign seat, and both instances' scratch is removed before final yield. The
`probe/` calibration copy independently arrives at the same one-token normalization the first
instance used in `P2`, corroborating it. Separately, a peer reported a foreign `positive-path/` probe
written into `R59Executor07`'s namespace at 15:23; neither instance of this seat wrote there and no
lane file is involved in either scratch collision.

---

# Second instance, same seat R59Executor14 — independent rerun (started 15:19, appended after first body)

This section is from a **second concurrently dispatched instance of seat R59Executor14** working the
same assignment after the first instance's scratch cleanup removed the directory mid-run. It re-ran
the frozen predicate from rebuilt bytes in
`/fast/scratch/hyaku/chousa-r59/R59Executor14/probe/`, corroborates D1, D3, D4, D5 above (the first
body's P-level results were not visible to this instance when it ran), and adds one defect the first
body does not contain: **D6, the span expectation for a quote at text offset 1-159**. Nothing in the lane was
edited; no install; no fetch; no git/jj/index write.

## Bytes actually run (hashed this instance)

```
65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f  c1-count.frozen.py   (byte copy of corpus/evidence/round58/c1-count.py)
21dae5d327157654ca679eb848b4c7d172643e2cf77e0e6180e454fa24e7eeba  cal/c1-count.py      (frozen copy + exactly the two-token patch below)
201d60e3a512ca701b10f837e3de27b1e0910383c159aabe6d713e194f549a4b  builder-probe.py     (scratch must-pass probe; implements no claim)
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  tools/build-spans.py (== controls/build-spans-r55.py: still no round-58 candidate)
2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573  tools/capture-text.py
```

`corpus/evidence/round59/claims.md` is **still absent** at this instance's reads (round59 holds only
`census-start.txt` and `controls/c1-before.txt`); the round-58 artifacts remain the only frozen C1
predicate, as the first body states.

## Q1 — D1 reproduced from rebuilt scratch (all 11 legs pass; verdict still FAIL)

```
$ cd /fast/scratch/hyaku/chousa-r59/R59Executor14/probe
$ python3 -B c1-count.frozen.py --builder "$PWD/builder-probe.py" --work "$PWD/work/frozen-maxleg2" --seed 7
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=pass(refused)
SYMLINK_OUT=pass(refused)
SYMLINK_CACHE=pass(refused)
FIFO_TXT=pass(refused)
DEVZERO_TXT=pass(refused)
FAT_RAW=pass(refused)
MANY_QUOTES=pass(refused)
ESCAPE_ENTRY=pass(refused)
HELDOUT_OK=pass
BEFORE_FOREIGN=deleted
DENIED=0/0
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
EXIT=1
```

Same command, lane builder `tools/build-spans.py` (the r55 pin), reproduces the frozen receipt byte for
byte — `SUMMARY OK=4/4 REFUSE=0/7 …` and `C1=FAIL`, `EXIT=1`, and
`diff <(grep -v '^EXIT=' frozen-lane.out) corpus/evidence/round58/controls/c1-before.txt` is empty
(`IDENTICAL_TO_FROZEN_C1_BEFORE`); it differs from Q1 only in the seven hazard-leg failure reasons. The
two states are indistinguishable in the top-line receipt, as the first body's P1 says.

## Q2 — the two-token patch flips only the verdict, not discrimination

Exactly two edits to a scratch copy (`diff -u c1-count.frozen.py cal/c1-count.py`):

```
-    ref_pass = all(("=PASS" in l) for l in ref_legs)
+    ref_pass = all(("=pass" in l) for l in ref_legs)
-          f"REFUSE={sum('=PASS' in l for l in ref_legs)}/{len(ref_legs)} "
+          f"REFUSE={sum('=pass' in l for l in ref_legs)}/{len(ref_legs)} "
```

```
$ python3 -B cal/c1-count.py --builder "$PWD/builder-probe.py" --work "$PWD/work/cal-maxleg2" --seed 7
... all eleven leg lines = pass/refused ...
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=PASS
EXIT=0

$ python3 -B cal/c1-count.py --builder /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py \
    --work "$PWD/work/cal-lane" --seed 7
... FOREIGN/SYMLINK_OUT/SYMLINK_CACHE/FIFO_TXT/DEVZERO_TXT/FAT_RAW/MANY_QUOTES all fail ...
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
EXIT=1
```

The credit path is reachable iff lines 391/399 compare the marker that line 51 and the leg emitters
actually produce; the battery still refuses the unhardened lane builder. Mechanism confirmed.

## Q3 — D4 extended: a builder that *writes through* the symlink still scores the leg as pass

`builder-probe.py` takes `PROBE_MODE` (env, because the counter forwards no extra builder args). Two
variants, both otherwise identical to the all-legs-passing probe:

- `symlink-noop`: `if out.is_symlink(): return 0` (accepts the hazard silently, writes nothing).
- `symlink-write`: follows the symlink, writes `spans.tsv` into the target, then exits 1 naming
  `SYMLINK`.

```
$ PROBE_MODE=symlink-noop  python3 -B c1-count.frozen.py --builder "$PWD/builder-probe.py" --work "$PWD/work/m-frozen-noop" --seed 7
SYMLINK_OUT=pass(refused)          # <- builder exited 0 and never refused
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
EXIT=1

$ PROBE_MODE=symlink-noop  python3 -B cal/c1-count.py    --builder "$PWD/builder-probe.py" --work "$PWD/work/m-cal-noop" --seed 7
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=PASS
EXIT=0

$ PROBE_MODE=symlink-write python3 -B c1-count.frozen.py --builder "$PWD/builder-probe.py" --work "$PWD/work/m-frozen-write" --seed 7
SYMLINK_OUT=pass(refused)(target-dir-written!)
...
C1=FAIL
EXIT=1

$ PROBE_MODE=symlink-write python3 -B cal/c1-count.py    --builder "$PWD/builder-probe.py" --work "$PWD/work/m-cal-write" --seed 7
SYMLINK_OUT=pass(refused)(target-dir-written!)
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=PASS
EXIT=0

$ find "$PWD/work/m-cal-write/realdir" -maxdepth 2 -printf '%y %P %s\n'
d  36
d spans 6
f spans.tsv 51            # symlinked --out was FOLLOWED and written before the refusal
```

So after the token fix a calibrated `C1=PASS` is reachable with (a) a builder that accepts a symlinked
`--out`, and (b) a builder that writes into the symlink target. The `(target-dir-written!)` suffix is
printed but never read by the verdict, and `expect_refuse`'s forbidden-touch test at `:158` is
inverted (`if not p.exists(): FAIL("was touched/removed")`), so the write makes the leg *more* likely
to pass. This is strictly stronger than the first body's P4 (silent acceptance only).

## Q4 — D3 corroborated on the calibrated copy (missing control leaves the denominator)

```
$ mkdir controls-partial && cp controls/REFUSEALL.py controls-partial/     # r55 control intentionally absent
$ python3 -B cal/c1-count.py --builder "$PWD/builder-probe.py" \
    --work "$PWD/work/cal-ctrl-partial" --controls "$PWD/controls-partial" --seed 7
CONTROL_REFUSEALL=denied
DENIED=1/1
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=1/1
C1=PASS
EXIT=0
```

Same calibrated counter with the full frozen controls dir (also: the frozen counter with the full
dir, for the vacuity point under D1):

```
$ python3 -B frozen/c1-count.py --builder "$PWD/builder-probe.py" \
    --work "$PWD/work/frozen-ctrl-full" --controls "$PWD/frozen/controls" --seed 7
CONTROL_REFUSEALL=denied
CONTROL_build-spans-r55=denied
DENIED=2/2
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=FAIL
EXIT=1
```

D5 corroboration — the REFUSEALL control has no verdict line at all:

```
$ python3 -B frozen/c1-count.py --builder "$PWD/frozen/controls/REFUSEALL.py" --work "$PWD/work/refuseall-direct" --seed 7
$ grep -c '^C1=' refuseall-direct.out      -> 0
FileNotFoundError: [Errno 2] No such file or directory:
  '.../work/refuseall-direct/out-empty/spans/S777-1.txt'
EXIT=1
```

`CONTROL_REFUSEALL=denied` is therefore the absence of stdout, not a parsed denial; a candidate that
crashes on EMPTY_OK is scored identically and the frozen command emits no `C1=` line.

## Q5 — NEW defect D6: a conforming builder is rejected when a quote sits in the first 80 characters

The counter's safe-leg verifier and the lane builder compute the span with different formulas:

- frozen counter `c1-count.py:138`: `span = form[offset:offset + len(quote) + min(CONTEXT, offset) + CONTEXT]`
  where `offset` is the **manifest start** (`:136 start = max(0, form.find(quote) - CONTEXT)`);
- lane builder `tools/build-spans.py:142-143` (and the claim's own definition):
  `start = max(0, off - CONTEXT)` then `span = text[start:off + len(quote) + CONTEXT]`.

These agree only for `off == 0` or `off >= 160`. For `1 <= off <= 159` the counter's slice end is
`start + len(quote) + min(80,start) + 80` while the builder — correctly by the claim — ends at
`off + len(quote) + 80`; e.g. `off=26` (start 0) gives counter end 96 versus builder end 122, and
`off=100` (start 20) gives 136 versus 196. The counter's `--seed` draws quote positions at
`randrange(20, len(text)-40)`, so this state is reachable from its own fixture synthesis: **15 of
seeds 0-600 (2.5%)** put at least one quote in `[1,159]` — first seeds `35 → [5405, 26, 4077]`,
`104 → [14406, 9534, 52]`, `138 → [44, 8634, 12455]`, `140 → [8495, 9528, 46]`,
`248 → [4461, 155, 8260]`. Default seed 7 is clean (`[3734, 1415, 4074]`), which is why the frozen
receipts miss it.

```
$ python3 -B cal/c1-count.py --builder "$PWD/builder-probe.py" --work "$PWD/work/cal-seed35" --seed 35
EMPTY_OK=fail(spans/S502-1.txt span bytes)
REBUILD_OK=pass
FOREIGN=pass(refused)
... all other legs pass ...
SUMMARY OK=3/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
EXIT=1
```

`S502` is the quote whose text offset is 26. Manifest + span lengths written by the probe (which uses
the builder's/claim's formula):

```
id=      offset(manifest start)  quote_len  counter want_len  written_len  verdict
S501     5325                    12         172               172          MATCH
S502     0                       16         96                122          MISMATCH   (quote starts at char 26)
S503     3997                    19         179               179          MATCH
```

The same seed under the frozen counter gives `EMPTY_OK=fail(spans/S502-1.txt span bytes)`,
`SUMMARY OK=3/4 REFUSE=0/7 ...`, `C1=FAIL`. Consequence: a builder that satisfies the C1 text exactly
is killed on 1 in 40 counter seeds by a counter-side formula, and the C1 kill rule ("incorrect span
… kills C1") would attribute the failure to the builder. The span check must slice
`form[start:off+len(quote)+CONTEXT]` with the quote offset carried separately (the counter already
has `off`-equivalent information only as the manifest start, so the formula needs `start` and the
quote's `find` result, not `min(CONTEXT, start)`).

## Q6 — what this instance did not establish

- No lane builder was written or measured; the probe implements no claim, so Q1/Q2 measure the gate,
  not C1 compliance. `tools/build-spans.py` is still the r55 pin, so C1's after-receipt remains
  unproducible independently of the counter defects.
- `c2-count.py` was not run (the first body's read-only note stands).
- Round-59 claims are absent, so no round-59 item is judged here.

## Coordination risk for the L1 (operability)

- Two live instances were dispatched to seat `R59Executor14` with the same scratch path. The first
  instance's mandated `rm -rf` of that path deleted the second instance's in-flight fixtures at ~15:23;
  the second rebuilt and re-ran. Both write the same report path, so this file is last-writer-wins and
  was merged by the second instance rather than replaced (first body kept verbatim, attribution note
  corrected). Dispatch should guarantee one live instance per seat/scratch name, or give each
  instance a suffixed scratch dir.
- Scratch `/fast/scratch/hyaku/chousa-r59/R59Executor14` is removed before this instance yields; all
  exact outputs are quoted above.

VERDICT (second instance): the frozen C1 positive-verdict path is **unsatisfiable for every builder**
(D1/Q1), and after the minimal marker fix it is **falsely satisfiable** by a builder that accepts or
writes through a symlinked `--out` (Q3) and by runs that drop a control (Q4), while a builder that
follows the claim's own span definition is **falsely rejected** on 2.5% of counter seeds whose quotes
land at offsets 1-159 (D6/Q5).
