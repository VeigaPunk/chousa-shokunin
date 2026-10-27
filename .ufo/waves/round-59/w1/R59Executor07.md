# R59Executor07 — round 58 frozen C1 counter: positive-verdict path

Seat: executor (leaf). Assigned: inspect and run the exact round-58 frozen
counter/tool or controls relevant to the **positive-verdict-path defect**, in
isolated scratch, reporting exact commands/output; never edit lane files.

- Lane root (read-only): `/home/vgpnk/Projects/shokunin/chousa-shokunin`
- Scratch (removed before yield): `/fast/scratch/hyaku/chousa-r59/R59Executor07`
- Frozen predicate under test: `corpus/evidence/round58/c1-count.py`
  sha256 `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f`
- Lane builder under test: `tools/build-spans.py`
  sha256 `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`
  (= the pinned round-55 builder; no hardening has landed in the lane yet)
- Python 3.14.8

## Blocker: round-59 frozen claims are absent

`/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round59/claims.md`
does not exist (`ls` → `No such file or directory`). The assignment says to read
it before work. Round 59's evidence dir contains only `census-start.txt` and
`controls/c1-before.txt`. I therefore bound the run to the round-58 frozen C1
predicate (the only frozen C1 counter/tool present) and did not infer round-59
claims. The round-59 `controls/c1-before.txt` is byte-identical to the
round-58 `controls/c1-before.txt` (`diff -u` rc 0) and carries no `Command:`
line.

## Findings (positive-verdict path)

### F1 — C1=PASS is structurally unreachable (case-mismatched aggregate)

`PASS = "pass"` (line 51) is what every emitter produces, but the refusal
aggregate tests for the uppercase token:

```
391:    ref_pass = all(("=PASS" in l) for l in ref_legs)
```

All seven refusal legs are emitted lowercase: six via
`expect_refuse` → `f"{name}={PASS}(refused)"` (line 160), and FOREIGN via the
same `PASS` constant (line 223). No refusal leg can contain `=PASS`, so
`ref_pass` is `False` for every possible builder, including a fully correct
one. A compliant candidate can never print `C1=PASS`.

Proof without a hardened builder: a scratch candidate
(`probe-hardened-candidate.py`, delegates to the lane builder for well-formed
input and refuses the seven hazard classes with the named reason classes)
makes every leg predicate true, yet:

```
$ python3 -B corpus/evidence/round58/c1-count.py \
    --builder /fast/scratch/hyaku/chousa-r59/R59Executor07/probe-hardened-candidate.py \
    --work /fast/scratch/hyaku/chousa-r59/R59Executor07/c1-candidate
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
RC=1
```

Module-level isolation (`aggregate-probe.py` imports the frozen counter and
feeds its own emitters a correctly-refusing process):

```
EMITTED LEGS:
  FOREIGN=pass(refused)
  SYMLINK_OUT=pass(refused)
  SYMLINK_CACHE=pass(refused)
  FIFO_TXT=pass(refused)
  DEVZERO_TXT=pass(refused)
  FAT_RAW=pass(refused)
  MANY_QUOTES=pass(refused)

leg-level refusals accepted (lowercase '=pass'): 7/7
c1-count.py ref_pass expression  all('=PASS' in l): False
case-normalised expression       all('=pass' in l): True
PASS constant value: 'pass'; FAIL constant value: 'fail'
```

Kill-rule consequence: the frozen C1 predicate ("must print `C1=PASS` and exit
0") is unsatisfiable as frozen, independent of any round-59 implementation.

### F2 — fixing only `ref_pass` yields PASS whose own summary says REFUSE=0/7

The summary count carries the same uppercase test at line 399
(`f"REFUSE={sum('=PASS' in l for l in ref_legs)}/..."`). Scratch mutant
`c1-count-casefix.py` changes **only** line 391; with the same candidate:

```
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=PASS
RC=0
```

A passing verdict can therefore ship with a receipt line asserting zero hazard
refusals — the verdict is detached from its own evidence, so a naive one-token
repair is not a valid calibration fix.

### F3 — fixing both occurrences restores a reachable, consistent positive path

Scratch mutant `c1-count-casefix2.py` changes lines 391 and 399 only
(diff against the frozen counter is exactly those two lines). Same candidate:

```
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=PASS
RC=0
```

With the frozen control set (`--controls corpus/evidence/round58/controls`),
the fixed predicate still denies both controls:

```
CONTROL_REFUSEALL=denied
CONTROL_build-spans-r55=denied
DENIED=2/2
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=PASS
RC=0
```

Two distinct upper/lowercase tests, not a semantic one, are the entire
positive-path blocker.

### F4 — the counter is non-total: a refusing candidate crashes instead of FAILing

`foreign.write_bytes(...)` (line 212) assumes the first safe leg created
`<out-empty>/spans/`. Any candidate that fails `EMPTY_OK` aborts the counter
with an uncaught `FileNotFoundError` and no `C1=` line:

```
$ python3 -B corpus/evidence/round58/c1-count.py \
    --builder corpus/evidence/round58/controls/REFUSEALL.py \
    --work /fast/scratch/hyaku/chousa-r59/R59Executor07/c1-refuseall
Traceback (most recent call last):
  ...
  File ".../round58/c1-count.py", line 212, in main
    foreign.write_bytes(b"foreign evidence bytes\n")
FileNotFoundError: [Errno 2] No such file or directory:
  '.../c1-refuseall/out-empty/spans/S777-1.txt'
RC=1
```

The control accounting then treats "no `C1=` line" as `denied`
(`tail = [...]; if tail and tail[0] == "C1=PASS"`), so the frozen receipt's
`CONTROL_REFUSEALL=denied` records a **counter crash**, not an evaluated
control failure. `DENIED=2/2` conflates two different outcomes. A partially
hardened real candidate that fails the first safe leg would likewise produce a
traceback instead of `C1=FAIL`.

The denial gate is therefore vacuous in both directions while F1 stands: a
nested control is credited as `denied` unless its child run prints exactly
`C1=PASS`, and F1 makes that line unprintable for every builder, so an honest
control and a broken control are indistinguishable and `DENIED=n/n` is not
control evidence. The gate only carries signal after F1/F2 are repaired.

Frozen controls reproduced in this scratch: every LEG/SUMMARY line matches
`round58/controls/c1-controls.txt` except that receipt's `Command:` header,
its interpretation trailer, and its rendering of the reason-class `\n` escape:

```
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)
SYMLINK_OUT=fail(rc=0, expected refusal)(target-dir-written!)
SYMLINK_CACHE=fail(rc=0, expected refusal)
FIFO_TXT=fail(rc=1, reason [...] absent in 'build-spans: refused S571: ...')
DEVZERO_TXT=fail(rc=1, reason [...] absent in 'build-spans: refused S581: ...')
FAT_RAW=fail(rc=1, reason ['SIZE'] absent in 'build-spans: refused S551: ...')
MANY_QUOTES=fail(rc=0, expected refusal)
ESCAPE_ENTRY=pass(refused)
HELDOUT_OK=pass
BEFORE_FOREIGN=deleted
CONTROL_REFUSEALL=denied
CONTROL_build-spans-r55=denied
DENIED=2/2
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=FAIL
RC=1
```

Baseline (lane builder, no `--controls`) reproduces the frozen
`round59/controls/c1-before.txt` counter lines exactly; the only diff is the
receipt's harness-appended trailing `EXIT=1` line:

```
$ python3 -B corpus/evidence/round58/c1-count.py --builder tools/build-spans.py \
    --work /fast/scratch/hyaku/chousa-r59/R59Executor07/c1-pristine
... (identical 14 LEG lines) ...
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
RC=1
```

### F5 — containment claim is unenforced outside the counter's work root

Claim C1(6) says "generated writes are contained under `--out`". `expect_ok`
compares `snapshot(out.parent)` before/after (out.parent is the counter's work
dir), so writes outside the work root are invisible. A candidate that refuses
all seven hazards, passes all safe legs, and **also** writes a marker outside
`--work` reaches PASS under the case-corrected aggregate:

```
$ python3 -B mutant2c/c1-count.py \
    --builder probe-hardened-escape.py \
    --work /fast/scratch/hyaku/chousa-r59/R59Executor07/c1-escape-h
...
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=PASS
COUNTER_RC=0
escaped markers outside work: 11
```

Under the frozen counter the same candidate is masked by F1 (`C1=FAIL`,
`REFUSE=0/7`), i.e. the positive path is simultaneously unreachable for a
compliant candidate and, once F1/F2 are repaired, unsound for an escaping one.

### F6 — minor: vacuous control gate and dead line

- `denied_pass = (denied == total) if total else True` (line 393): with no
  `--controls`, the "do-nothing controls must not reach C1=PASS" requirement is
  vacuous (`DENIED=0/0` still allows PASS). The frozen receipt was produced with
  `--controls`; a round-59 build run without it loses that guarantee silently.
- Line 389 (`ok_pass = ...`) is dead; line 390 overwrites it.

## Exact scratch artifacts (sha256; removed before yield)

```
96082ee176d79de2744d6dfec0a111cbfd9f8a4955b8b25252e09c923d943e14  probe-refuse-with-reasons.py
fca4116aecf14309ce0b184be14113b3e6618f809371070a88c6bc0d9dda1114  probe-hardened-candidate.py
61645edd794dde61fffd8d2a05236a5d8ae15d475a0a603f68faedd77fb979ad  probe-hardened-escape.py
98d485250a2248a54902adde608fc5eed6ea0947f27ac6dfba4e8fd5d43e5732  aggregate-probe.py
6b6000ed83f25e9c8ddbe757624da9a3f085834a5d9b7609d14f4013c95d3a46  mutant/c1-count-casefix.py        (line 391 only)
74c5ad18f469b290f125b69ba76a6b15df1d5fcd24e6380c567ef71f210afa64  mutant2/c1-count-casefix2.py      (lines 391+399)
74c5ad18f469b290f125b69ba76a6b15df1d5fcd24e6380c567ef71f210afa64  mutant2c/c1-count.py              (same bytes, exec name)
```

Mutation diff (both fixes), against the frozen counter:

```
-    ref_pass = all(("=PASS" in l) for l in ref_legs)
+    ref_pass = all(("=pass" in l) for l in ref_legs)
-          f"REFUSE={sum('=PASS' in l for l in ref_legs)}/{len(ref_legs)} "
+          f"REFUSE={sum('=pass' in l for l in ref_legs)}/{len(ref_legs)} "
```

No lane file was written or edited. Lane hashes after all runs are unchanged:
`tools/build-spans.py` = r55 pin, `tools/capture-text.py` = capture pin
`2c0140bc...`, `corpus/evidence/round58/c1-count.py` = `65da18bb...`.
`corpus/evidence/round59/` still holds only `census-start.txt` and
`controls/c1-before.txt`.

Scratch hygiene and namespace collision: all artifacts created by this seat under
`/fast/scratch/hyaku/chousa-r59/R59Executor07` were removed. During cleanup a
foreign positive-path harness (`positive-path/{c1-positive-builder.py,pony…
run-c1.sh,run-pos/,run-ctrl/,keep/,c2-poison-zh.stdout,poison-base.py}`, mtimes
15:23–15:24) appeared inside this seat's scratch namespace. Its author
identified itself over the fleet channel as a **second instance of seat
R59Executor07** (`ChousaR59.R59Executor07`) holding the same item and the same
scratch root; it asked that the subtree be left in place. I did not create, run,
read as evidence, or delete those bytes, and I did not adopt anything under
`positive-path/`. Consequence for this wave: the readiness binding
`.ufo/waves/round-59/w1.ready.partial` maps seat `R59Executor07` to agent
`R59Executor07-2` (this seat); the second instance that claimed
`positive-path/` (`ChousaR59.R59Executor07`) is not bound there, yet it wrote
into the bound seat's scratch root and asked that the subtree stay. Two dispatch
trees therefore resolve one seat name to one scratch root and one report path:
bytes in `/fast/scratch/hyaku/chousa-r59/R59Executor07` are not attributable by
path alone, and `.ufo/waves/round-59/w1/R59Executor07.md` has two prospective
writers — this report is the C1 counter measurement above, and any section
appended by the other instance must be attributed to it explicitly.

## Offline reconnaissance read (context, not a claim)

`corpus/evidence/round59/census-start.txt` ends `exit=0` with five pre-existing
W04 duplicate-URL rows (S051, S053, S073, S074, S075) over
`corpus/SOURCES.md`; this matches the baseline documented in
`corpus/lessons/round-54-verifier-spotcheck.md` (same five ids). No new census
defect observed; no `census-end.txt` exists yet for round 59.

## Risk / hand-off

- The frozen round-58 C1 predicate cannot produce a positive verdict, so any
  round-59 build scored against it fails regardless of implementation quality.
  Repair requires changing both the predicate line and the summary line
  (F1+F2), making the counter total on an early safe-leg failure (F4), and
  widening or explicitly scoping the containment check (F5). All are in the
  lane's frozen counter, which this seat must not edit.
- If round 59 intends a new frozen counter, it should avoid re-freezing the
  uppercase `=PASS` token and should assert the containment root explicitly
  (e.g. compare snapshots of the whole scratch root and of the lane).
- Round-59 frozen claims are missing; claims-dependent calibration cannot be
  checked until `corpus/evidence/round59/claims.md` exists.

---

# Appended by the second instance of seat R59Executor07 (unbound in `w1.ready.partial`)

Attribution: this section is written by the duplicate seat instance that owns
the `positive-path/` subtree inside the same scratch root. It does not modify
or contradict the C1 findings above; it adds independent reruns on a different
positive candidate and covers the frozen **C2** counter's positive-verdict path.
All commands below ran read-only against the lane; no lane file was written or
edited. Scratch: `/fast/scratch/hyaku/chousa-r59/R59Executor07/positive-path/`
(subtree removed before yield; exact outputs are quoted here).

Frozen bytes used and re-hashed before and after the runs:

```
65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f  corpus/evidence/round58/c1-count.py
dbb859612f9d018296b217baec76a5c6cb744609b7c95372dabae4d6691c8503  corpus/evidence/round58/c2-count.py
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  corpus/evidence/round58/controls/build-spans-r55.py
e7721cefe050ee435d3bab811ed65933d26a865ca30340feaab3f9388c3572fb  corpus/evidence/round58/controls/REFUSEALL.py
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  tools/build-spans.py
2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573  tools/capture-text.py
```

`corpus/evidence/round59/claims.md` was absent at run time (same blocker the
report above records), so the runs bind to the round-58 frozen predicates.

## A. Frozen C1 counter: an independent positive candidate still yields `C1=FAIL`

Candidate `c1-positive-builder.py` (scratch-only, written for this probe): the
pinned builder's span-manifest logic plus pre-write refusals for foreign span
orphans, symlinked `--out`, symlinked/non-regular cache inputs, a >64 MiB input
and a >100,000-row quote table. It satisfies all seven refusal legs and all
four safe legs, at both the counter's default seed and the nested-control seed:

```
$ python3 corpus/evidence/round58/c1-count.py \
    --builder /fast/scratch/hyaku/chousa-r59/R59Executor07/positive-path/c1-positive-builder.py \
    --work /fast/scratch/hyaku/chousa-r59/R59Executor07/positive-path/run-pos --seed 7
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
EXIT_positive=1
```

`--seed 1007` (the seed every nested control run uses) produced the same 11
`pass` leg lines, `SUMMARY OK=4/4 REFUSE=0/7`, `C1=FAIL`, exit 1. This
reproduces the round-58 lesson's probe on different candidate bytes: the
positive state is expressible in every leg and inexpressible in the aggregate.

## B. The deny-only control set is vacuous, measured

The same passing candidate was copied to both names the counter loads as
controls, then supplied with `--controls`:

```
$ mkdir ctrl-vacuous && cp c1-positive-builder.py ctrl-vacuous/REFUSEALL.py \
    && cp c1-positive-builder.py ctrl-vacuous/build-spans-r55.py
$ python3 corpus/evidence/round58/c1-count.py \
    --builder .../c1-positive-builder.py --work .../run-ctrl --seed 7 \
    --controls .../ctrl-vacuous
... 11 leg lines all pass ...
CONTROL_REFUSEALL=denied
CONTROL_build-spans-r55=denied
DENIED=2/2
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=FAIL
EXIT_vacuous_controls=1
```

Both "do-nothing" controls are legitimate, fully-refusing builders that pass
every leg, and both are recorded `denied`. The deny leg therefore carries no
information about control quality: `DENIED=2/2` is produced by the aggregate
token defect (A), not by a control that was evaluated and rejected. This is the
control-side counterpart of QUALITY criterion 115.

## C. Two-token repair is the whole blocker, and the repaired predicate discriminates

Scratch package `pkg/`: a byte-copy of the frozen counter with exactly two token
tests changed, plus `pkg/controls/{build-spans-r55.py,REFUSEALL.py}` so the
counter's own `BEFORE_FOREIGN` integrity leg (which reads
`HERE/controls/build-spans-r55.py`) still resolves inside the package copy.
The two-line change, measured:

```
$ diff -u <(sed -n '385,402p' corpus/evidence/round58/c1-count.py) \
          <(sed -n '385,402p' pkg/c1-count.py)
-    ref_pass = all(("=PASS" in l) for l in ref_legs)
+    ref_pass = all(("=pass" in l) for l in ref_legs)
-          f"REFUSE={sum('=PASS' in l for l in ref_legs)}/{len(ref_legs)} "
+          f"REFUSE={sum('=pass' in l for l in ref_legs)}/{len(ref_legs)} "
```

`DIFF_RC=1`, exactly two hunks (`@@ -4,7 +4,7 @@`, `@@ -12,7 +12,7 @@`), all
context lines identical.

```
$ python3 pkg/c1-count.py --builder .../c1-positive-builder.py \
    --work .../run-fixed-pkg-pos --seed 7
... 11 leg lines all pass ...
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=PASS
EXIT_fixed_positive=0

$ python3 pkg/c1-count.py --builder tools/build-spans.py \
    --work .../run-fixed-pkg-base --seed 7 --controls corpus/evidence/round58/controls
FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)
SYMLINK_OUT=fail(rc=0, expected refusal)(target-dir-written!)
SYMLINK_CACHE=fail(rc=0, expected refusal)
FIFO_TXT=fail(rc=1, reason [...] absent ...)
DEVZERO_TXT=fail(rc=1, reason [...] absent ...)
FAT_RAW=fail(rc=1, reason ['SIZE'] absent ...)
MANY_QUOTES=fail(rc=0, expected refusal)
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=FAIL
EXIT_fixed_base=1
```

The repaired predicate reaches the declared target token only for the candidate
that meets every leg and still refuses the lane's unhardened builder, so the
token pair is the entire positive-path blocker rather than a masking of a
second defect in these legs. (The containment and totality gaps F4/F5 above are
separate and remain; this probe does not exercise them.)

## D. Frozen C2 counter: `C2=PASS` is also unreachable (offset vs rebuild)

Root: a scratch `--shared` clone of the lane at `af8c0a4`, with the frozen
`quotes.tsv`, an entry at `corpus/knowledge/carrier-alphabet-china-r58.md`
carrying the provenance trio, all 12 frozen quotes and a grounded
`#### Inference` bullet, and the S101 `used-by` cell appended to name the entry.
Span files and manifest were generated by the pinned `tools/build-spans.py`
itself. Two manifests differ only in the `offset` column:

Manifest B (= builder output verbatim; offset = span start):

```
$ python3 corpus/evidence/round58/c2-count.py --root .../c2/root --work .../c2/wB
ENTRIES=1/1 BOUND=1/1 REF_ID_UNBOUND=0
QUOTE_ROWS=12/12 CAPTURE_BOUND=0/12 ENTRY_QUOTES=0/12
SUBSTANCE=PASS ANCHOR_BOUND=0/3 INFERENCE_GROUNDED=yes STRAY_IDS=- NEW_GROUND=yes REBUILD=MATCH
ERROR CAPTURE_BIND:S101   (x12)
ERROR CAPTURE_BOUND=0/12
ERROR ANCHOR_BOUND=0/3
ERROR ENTRY_QUOTES=0/12
C2=FAIL
EXIT_B=1
```

Manifest A (same rows, offset = quote occurrence position):

```
$ python3 corpus/evidence/round58/c2-count.py --root .../c2/root --work .../c2/wA
ENTRIES=1/1 BOUND=1/1 REF_ID_UNBOUND=0
QUOTE_ROWS=12/12 CAPTURE_BOUND=12/12 ENTRY_QUOTES=12/12
SUBSTANCE=PASS ANCHOR_BOUND=3/3 INFERENCE_GROUNDED=yes STRAY_IDS=- NEW_GROUND=yes REBUILD=FAIL
ERROR BUILDER_REBUILD_MISMATCH
C2=FAIL
EXIT_A=1
```

Occurrence offsets: `315,330,590,683,734,781,797,838,965,993,1460,11723`;
the pinned builder writes `max(0, offset-80)`, i.e.
`235,250,510,603,654,701,717,758,885,913,1380,11643` (all offsets exceed the
80-character context, so no clamp applies). Because
`CAPTURE_BOUND` requires the manifest offset to equal the occurrence position
and `REBUILD` requires it to equal the builder's span start, no manifest of the
frozen quote set satisfies both legs. A (content-complete) leaves exactly one
error, the rebuild mismatch; B (byte-identical to the builder) leaves the
binding legs at zero. This is a second frozen counter whose declared positive
token cannot be produced, independent of C1.

## E. `NEW_GROUND` guard is mis-calibrated in both directions (measured)

`c2-count.py:153-154` greps the traditional token at base and tests the
simplified token in the entry. The BASE commit was poisoned inside the same
scratch clone with `git replace` (scratch-only objects), once per variant:

Simplified `载` (U+8F7D) added to `BASE:corpus/knowledge`:

```
POISON=zh TOKEN=U+8F7D COMMIT=a1676a5e583650eb048c5b3d414a974af842b915
GREP simplified rc=0 hit=b13ca7b5c8bbb40d2d29a37fb443c64ca043f791:corpus/knowledge/zz-poison.md
GREP traditional rc=1 hit=
... counter on manifest A ...
SUBSTANCE=PASS ANCHOR_BOUND=3/3 INFERENCE_GROUNDED=yes STRAY_IDS=- NEW_GROUND=yes REBUILD=FAIL
ERROR BUILDER_REBUILD_MISMATCH
C2=FAIL
```

The base now holds the exact marker the entry is graded on, yet the guard
reports `NEW_GROUND=yes` — a false positive on the claim's novelty clause.

Traditional `載` (U+8F09) added instead:

```
POISON=trad TOKEN=U+8F09 COMMIT=8f8c2141a2f42dd7b6230337c389f80ce7ae1b63
GREP simplified rc=1 hit=
GREP traditional rc=0 hit=b13ca7b5c8bbb40d2d29a37fb443c64ca043f791:corpus/knowledge/zz-poison.md
... counter on manifest A ...
SUBSTANCE=PASS ANCHOR_BOUND=3/3 INFERENCE_GROUNDED=yes STRAY_IDS=- NEW_GROUND=no REBUILD=FAIL
ERROR BUILDER_REBUILD_MISMATCH
ERROR NEW_GROUND_FAIL
C2=FAIL
```

Here the base holds only the traditional form, the entry's simplified marker is
genuinely absent, and the guard refuses. Both directions are wrong; the leg is
not a calibrated novelty test.

## F. Risks / hand-off from this instance

- Round-59 `claims.md` was absent, so this seat made no round-59 claim and did
  not infer one; all predicates are round-58 frozen bytes.
- C1: the declared target token is unreachable for any builder; a deny-only
  control set cannot detect that. Any round-59 counter must ship a must-pass
  control that reaches its exact final token and exit 0 (criterion 115), and
  the repaired aggregate must still reject the unhardened lane builder (C above
  shows that ordering).
- C2: the offset/rebuild contradiction and the two-character `NEW_GROUND`
  divergence are both frozen in the round-58 counter; scoring C2 against it is
  unsatisfiable regardless of entry quality.
- Duplicate seat: two live instances held seat name `R59Executor07`, one
  scratch root and one report path. This section is the second instance's
  evidence; the C1 findings above are the first instance's. No lane file was
  edited by either; lane hashes are unchanged after all runs.

Scratch artifacts (sha256; removed before yield with the `positive-path/`
subtree):

```
9c2f1225a41063fad982bab9c999a6b58501e23de2770d80e41d8453b9c3a008  c1-positive-builder.py
21dae5d327157654ca679eb848b4c7d172643e2cf77e0e6180e454fa24e7eeba  pkg/c1-count.py   (two-token repair)
9b266e5cbf8e084f64eb4c81129f19e1096dc463032c50aeee87e4488d099ee3  gen-c2.py
4d228c613b514aaf0ab3240e7680e2d6a037b92b982fd1e6d6f6e51ee3400177  poison-base.py
9896e93729362d39302ce685e5533acafd0e878cc438155afdd1e796d31b2bbc  run-c1.sh
```
