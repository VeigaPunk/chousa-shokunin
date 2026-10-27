# R59Executor08 — frozen round-58 C1 counter: positive verdict path unreachable as frozen, and forgeable after the one-token fix

Seat: R59Executor08 (executor, leaf). Axis: **operability** (lowest scored non-retired, 3/10). Lane root
`/home/vgpnk/Projects/shokunin/chousa-shokunin`; no lane file was written, edited, or deleted. No installs
(pacman paused; nothing needed), no live fetch, no git/jj writes, no subagent dispatch.

## Inputs and provenance

| Byte set | sha256 |
|---|---|
| `corpus/evidence/round58/c1-count.py` — exact bytes executed | `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f` |
| `corpus/evidence/round58/claims.md` — frozen C1 predicate | `7aedd8156c9fce185841a740b894600f8a4149b2d8e2034039f634c808373457` |
| `tools/build-spans.py` — current lane builder | `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6` = round-55 pin, i.e. **no C1 hardening landed** |
| `corpus/evidence/round58/controls/build-spans-r55.py` | `1ed2650…` (same bytes) |
| `corpus/evidence/round58/controls/REFUSEALL.py` | `e7721cefe050ee435d3bab811ed65933d26a865ca30340feaab3f9388c3572fb` |
| `tools/capture-text.py` | `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573` |
| `corpus/evidence/round59/controls/c1-before.txt` | `2c9bbe5446ae4f733bf17a2836cc1b32e823fc8bc287d3da42801b948cfaebfe` — **byte-identical** to round-58 `controls/c1-before.txt` |
| `corpus/evidence/round58/c1-before.txt` | `2c9bbe…` (same bytes) |

Round-59 binding: `corpus/evidence/round59/claims.md` **does not exist**. `corpus/evidence/round59/` holds
only `census-start.txt` and `controls/c1-before.txt`. The census output differs from round-58's
(`09ce4a95…` vs `6e5373d0…`) only in its trailing `exit=0`/`EXIT=0` line. There is no round-59 claim ID or
counter revision to bind, so the operative frozen predicate is round-58 C1 — the input actually measured here.

Scratch: `/fast/scratch/hyaku/chousa-r59/R59Executor08/seat08-rerun/`, removed before yield. A concurrent
same-seat run (another incarnation of seat 08) occupied the seat scratch root and removed it at ~15:20,
taking my first-pass logs with it; every run below was re-executed from the exact lane bytes in the private
subdirectory named above, and the receipts here are those re-runs. Nothing outside scratch was affected.

## R1 — exact frozen counter against the current lane builder: receipt reproduced byte-for-byte

Command (cwd `…/seat08-rerun`, `TMPDIR` set there):

```
python3 c1-count-exact.py \
  --builder /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py \
  --work "$PWD/work-baseline"
```

Output (16 lines, exit 1):

```
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
EXIT=1
```

`diff logs/baseline.out corpus/evidence/round58/controls/c1-before.txt` → **rc=0, 0 bytes**: the frozen
baseline receipt is truthful for these exact bytes, so the round-59 re-measure starts from a real `C1=FAIL`.

## R2 — exact frozen counter against a conforming scratch candidate: 11/11 legs pass, verdict still FAIL

The candidate (`hardened.py`, sha256 `49699ec1cbc49ea46393dd26cae229216e5bca79899979e6a26f3565d6024c70`)
is a scratch fixture, not lane code: generic preflight refusals (lstat type before read, no symlink cache
entries, 64 MiB object cap, 100,000-row cap, lane-relative `entry`, unrequested-span audit before any
unlink, `--out` symlink refusal before `mkdir`) on top of delegation to the pinned r55 builder for the
normal path. It is keyed to filesystem properties, not to fixture names.

Command (cwd `…/seat08-rerun`):

```
python3 c1-count-exact.py --builder "$PWD/hardened.py" --work "$PWD/work-eh" --controls "$PWD/controls"
```

Output (18 lines, exit 1):

```
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
CONTROL_REFUSEALL=denied
CONTROL_build-spans-r55=denied
DENIED=2/2
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=FAIL
EXIT=1
```

Every declared leg — 4 safe, 7 hazard-refusal, the pinned-baseline discriminator, and both do-nothing
controls — reports as the frozen predicate defines it, yet the verdict is `C1=FAIL` and the required
`C1=PASS`/exit 0 state is not printed. This is the positive-verdict-path defect on exact frozen bytes.

## R3 — mechanism: the aggregator cannot express the state the legs emit

- `c1-count.py:51` `PASS = "pass"` (lowercase); every refusal leg interpolates it (`expect_refuse` return
  at :160; FOREIGN :223; SYMLINK_OUT :234; ESCAPE_ENTRY literal lowercase at :315).
- `c1-count.py:391` `ref_pass = all(("=PASS" in l) for l in ref_legs)` — uppercase.
- `c1-count.py:399` `REFUSE={sum('=PASS' in l …)}` — uppercase.
- `c1-count.py:394` gates the verdict on `ref_pass`, so `C1=PASS` is unreachable for **any** builder.
- `c1-count.py:389` is dead code (immediately overwritten by :390); the two aggregates also disagree with
  `expect_ok`'s lowercase return (:147).

Changing the single constant instead of the aggregate moves the failure to the safe legs (:390 requires
`=pass`), so no leg formatting can satisfy both families: the positive state is structurally absent, not
merely unreached. This is the same mismatch recorded in round 58; this seat re-derived it from the exact
bytes and adds what round 58 did not produce — an observed `C1=PASS` under the minimal normalization (R4)
and the false-positive routes that normalization exposes (R5).

## R4 — one-token normalization opens the positive path (scratch copy, not lane)

Scratch copy `c1-count-fixed.py` (sha256 `21dae5d327157654ca679eb848b4c7d172643e2cf77e0e6180e454fa24e7eeba`)
differs from the frozen counter in exactly two lines:

```
-    ref_pass = all(("=PASS" in l) for l in ref_legs)
+    ref_pass = all(("=pass" in l) for l in ref_legs)
-          f"REFUSE={sum('=PASS' in l for l in ref_legs)}/{len(ref_legs)} "
+          f"REFUSE={sum('=pass' in l for l in ref_legs)}/{len(ref_legs)} "
```

Same conforming candidate, with controls (cwd `…/seat08-rerun`):

```
python3 c1-count-fixed.py --builder "$PWD/hardened.py" --work "$PWD/work-fc" --controls "$PWD/controls"
```

```
… (the same 18 leg/control lines as R2)
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=PASS
EXIT=0
```

So the target state is reachable the moment the aggregation matches the emitted token: the round-58 gate is
not missing a candidate, it is missing a reachable verdict. (Normalization is scratch instrumentation; the
frozen counter and its claim were not edited.)

## R5 — false-positive routes that the normalized gate does not close

All three runs below used `c1-count-fixed.py`, the scratch candidate, and `--controls`, and **each printed
`C1=PASS` with `EXIT=0` and `DENIED=2/2`**:

(a) **Write-through on a refused `--out` symlink.** Candidate switch `DEMO_WRITE_THROUGH_SYMLINK=1` writes
`<symlink-target>/spans.tsv` and then refuses with `SYMLINK`:

```
SYMLINK_OUT=pass(refused)(target-dir-written!)
…
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=PASS
```

Observed artifact: `work-fw/out-link -> …/work-fw/realdir`;
`work-fw/realdir/spans.tsv` content `partial write through --out symlink`. Mechanism: `expect_refuse`
(:150-160) takes `forbidden_touch` but its check is inverted — it returns `FAIL` when the listed path does
**not** exist (:158), so creating it satisfies the helper; the `(target-dir-written!)` annotation (:236) is
appended to a string that still contains `=pass`, so it is not binding. The frozen claim's "generated
writes are contained under `--out`" is therefore unmeasured by this leg.

(b) **Owned-orphan deletion before the FOREIGN refusal.** Candidate switch
`DEMO_DELETE_OWNED_ORPHAN=1` deletes unrequested span files listed in the prior `spans.tsv` (its own
earlier writes), then refuses on the remaining unrequested file:

```
FOREIGN=pass(refused)
…
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=PASS
```

Observed FOREIGN fixture after the run (`work-fo/out-empty/spans/`): `S501-1.txt`, `S502-1.txt`,
`S777-1.txt` — **`S503-1.txt` is gone**. The leg (:214-224) checks only that `S777-1.txt` still exists plus
a `777`/`foreign` token in the first 200 bytes, and never snapshots the other spans or `spans.tsv`, so the
claim's "preserved and causes refusal **before orphan deletion**" is satisfiable while deletion happened
first. (Round-58 review recorded this leg gap with a helper probe; this is its gate-level `C1=PASS`.)

(c) **Vacuously satisfied control gate.** The canonical command frozen in round-58 `claims.md` passes only
`--builder` and `--work`. Run exactly that way on the normalized counter:

```
python3 c1-count-fixed.py --builder "$PWD/hardened.py" --work "$PWD/work-fn"
…
DENIED=0/0
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=PASS
EXIT=0
```

`denied_pass = (denied == total) if total else True` (:393) turns "no controls were run" into a pass, so a
positive verdict can be minted with zero negative controls. The round-58 claims require that do-nothing
controls never reach `C1=PASS`, but the frozen invocation path does not execute them.

## R6 — second false-negative route: the safe-leg span window is seed-fragile

`c1-count.py:138` computes the expected span as
`form[offset:offset + len(quote) + min(CONTEXT, offset) + CONTEXT]` where `offset = max(0, find - CONTEXT)`.
For a quote found at `0 < find < CONTEXT`, `offset` is 0 and `min(CONTEXT, offset)` is 0, so the expected
window omits the `find` characters the builder legitimately emits before the quote.

Measured at the counter's own `--seed 35` (the default seed 7 has all fixture offsets ≥ 80, which is why
the canonical receipt is stable): quote offset 26, quote length 16, counter-expected length 96, builder
span length 122, delta 26. Run:

```
python3 c1-count-fixed.py --builder "$PWD/hardened.py" --work "$PWD/work-f35" --seed 35 --controls "$PWD/controls"
EMPTY_OK=fail(spans/S502-1.txt span bytes)
…
SUMMARY OK=3/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=FAIL
```

So even with the verdict-path case fixed, a structurally correct builder fails a safe leg on any seed whose
quotes start before offset 80. Data-dependent false negative in a documented counter option.

## Impact

- **operability (assigned):** the round-58 C1 gate is non-operable as frozen — no conforming builder can
  print the declared verdict (R1-R3), and the lane still ships the unhardened r55 builder (pin matches
  `tools/build-spans.py`), so the round-59 re-measure cannot move the 3/10 reading. No numeric score change
  is claimed; the observable is the gate itself.
- **calibration:** the positive verdict path fails in both directions. False negatives: the aggregation
  case (R3) and the sub-80 offset window (R6). False positives after the minimal normalization: a builder
  that writes through a refused `--out` symlink (R5a), a builder that deletes owned orphans before
  refusing (R5b), and any candidate measured without controls (R5c). `DENIED=2/2` alone does not calibrate
  the positive path because control denial is scored against the same unreachable `C1=PASS` string (:377).
- The two genuine round-59 blockers are outside this seat's write scope: the frozen counter and its claim
  were not modified, and no round-59 claims file exists to bind a verdict to.

## Limits, retained evidence

- The conforming candidate is a scratch fixture, not an integrated `tools/build-spans.py`; its safe path
  delegates to the pinned r55 builder, so R2/R4 measure leg/aggregate behaviour, not a shipped hardening.
- I did not assert the 64 MiB read bound or broader races; the candidate refuses oversized objects before
  opening them, which is all the FAT_RAW leg observes.
- No lane byte was modified: the four lane hashes above were re-read after the runs and are unchanged; all
  fixtures, logs, and the candidate lived under the seat scratch and were removed; no `/tmp` evidence.
- Exact receipts, scratch log names, and the counter diff are transcribed above from the executed runs;
  the scratch tree (including `hardened.py` and both counter copies) was deleted before yield, so these
  transcribed outputs plus the lane hashes are the retained evidence.

VERDICT: The round-58 frozen C1 counter makes `C1=PASS` unreachable for every builder (case-mismatched
refusal aggregation, `c1-count.py:51/160/223/234/315` vs `391/394/399`), and a two-line normalization that
opens the positive path also lets a symlink-write-through builder, an owned-orphan-deleting builder, and a
no-controls invocation each reach `C1=PASS`. A correct builder additionally fails safe-leg span
verification for quote offsets below 80 (`:138`). Operability remains blocked at the gate; the round-58
baseline receipt reproduces byte-for-byte against the current lane builder, which is still the unhardened
round-55 pin.

Report: `.ufo/waves/round-59/w1/R59Executor08.md`
