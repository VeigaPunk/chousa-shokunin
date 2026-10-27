# R59Executor06 — frozen round-58 C1 counter: positive verdict path measured

Seat: R59Executor06 (executor, leaf). Lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`,
read-only for this seat. Scratch: `/fast/scratch/hyaku/chousa-r59/R59Executor06` (removed before
yield). No lane file, claims/counter byte, or source repository was modified; no git/jj command was
run; no install and no pacman transaction (`/home/vgpnk/.omp/agent/RULES.md` read, unused); no live
fetch (L0 `8d77e6c1` stays open).

The prescribed round-59 claims file `corpus/evidence/round59/claims.md` is **absent** at filing
(`ls` of `corpus/evidence/round59/` shows `census-start.txt`, `controls/`). My seat authorises the
*round-58 frozen* counter as the object, so nothing below is a round-59 claim verdict. The round-59
capture `corpus/evidence/round59/controls/c1-before.txt` is byte-identical to round 58's
(sha256 `2c9bbe5446ae4f733bf17a2836cc1b32e823fc8bc287d3da42801b948cfaebfe`).

## Objects and pins (hashes measured this seat)

| Object | sha256 |
|---|---|
| `corpus/evidence/round58/c1-count.py` (frozen counter, 406 lines) | `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f` |
| `tools/build-spans.py` = `corpus/evidence/round58/controls/build-spans-r55.py` (r55 pin) | `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6` |
| `tools/capture-text.py` (pin the counter re-checks) | `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573` |
| scratch copy of the counter (byte copy, unmodified) | `65da18bb…c703d3f` (equal) |

Counter token sites read in the frozen file: `51:PASS = "pass"`, `52:FAIL = "fail"`;
refusal emitters `160:return f"{name}={PASS}(refused)"`, `223:FOREIGN={PASS}(refused)`,
`234:legs[-1] = f"SYMLINK_OUT={PASS}(refused)"` (unconditional), `315:"ESCAPE_ENTRY=pass(refused)"`;
aggregation `389` (dead first assignment), `390:ok_pass = all(("=pass" in l) …)`,
`391:ref_pass = all(("=PASS" in l) …)`, `399:REFUSE={sum('=PASS' in l …)}`.

## Scratch instruments (mine, scratch-only; hashes recorded because the tree is deleted)

- `positive-shim.py` (`c640fe4b…53e795a0`): a builder that satisfies **every leg the counter
  declares as implemented**. It applies the r55 pin for span arithmetic and adds only the guards the
  hazard legs name — symlinked `--out` → `SYMLINK`, symlinked cache entry → `SYMLINK`, non-regular
  cache entry → `NOT_REGULAR FIFO/device`, referenced cache file > 64 MiB → `SIZE`, `quotes.tsv`
  > 100 000 data rows → `ROWS`, an `S###-N.txt` in `<out>/spans` with no manifest row → `foreign`
  — then `execv`s the r55 pin with the same argv (which already refuses `..` entries).
- `noop-symlink-out.py` (`75dff03c…ad05fb6`): accepts a symlinked `--out`, exits 0, writes nothing,
  refuses nothing; delegates every other invocation to `positive-shim.py`.
- `refuse-stray-symlink-out.py`: refuses with the frozen `SYMLINK` reason and leaves an unrelated
  `stray-pre-existing.txt` inside the link target; otherwise delegates to `positive-shim.py`.
- `counter-casefix/c1-count.py` (`21dae5d3…24e7eeba`): the frozen counter with **only** `391` and
  `399` changed, `"=PASS"` → `"=pass"`.
- `counter-verdictonly/c1-count.py` (`6b6000ed…3c95d3a46`): the frozen counter with **only** `391`
  changed.

## Runs (exact commands, exact output)

All runs: `cd /fast/scratch/hyaku/chousa-r59/R59Executor06`, absolute `--work` inside scratch, no
`TMPDIR`/`/tmp` use. `S=/fast/scratch/hyaku/chousa-r59/R59Executor06`.

### R1 — the frozen counter on the committed base builder (receipt reproduction)

```
python3 -B counter/c1-count.py \
  --builder /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py \
  --work $S/runs/base/work
```
stdout (EXIT=1):
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
```
`diff` against `corpus/evidence/round59/controls/c1-before.txt`: `15a16 > EXIT=1` — the only
difference is the receipt's `EXIT=1` trailer line, which the frozen counter does not print. All 14
counter lines are byte-identical, so the round-59 before-receipt is the current base builder's
output and `BEFORE_FOREIGN=deleted` is genuine (pinned r55 deleted `out-before/spans/S888-1.txt`).

### R2 — positive control on the FROZEN counter: all eleven legs pass, verdict FAIL

```
python3 -B counter/c1-count.py --builder $S/positive-shim.py --work $S/runs/shim-frozen/work
```
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
DENIED=0/0
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
```
EXIT=1, stderr empty. Leg-side artifacts in the run tree confirm the passes are substantive, not
staging: `out-empty/spans.tsv` 3 rows (offsets 3654/1336/3994), `out-heldout/spans.tsv` 3 rows
(offsets 11953/12119/11927) — both verified by the counter's own digest/offset/span-byte checks;
`out-empty/spans/S777-1.txt` present (23 B, foreign preserved); `realdir/` empty (nothing written
through the output symlink); `out-many/` empty (100 000-row table refused); `out-esc/` empty.

### R3 — same builder, only `391`+`399` case-fixed: PASS

```
python3 -B counter-casefix/c1-count.py --builder $S/positive-shim.py --work $S/runs/shim-casefix/work
```
Identical eleven leg lines; `SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0`;
`C1=PASS`, EXIT=0. `diff counter/c1-count.py counter-casefix/c1-count.py` is exactly
`391c391 "=PASS"→"=pass"` and `399c399 "=PASS"→"=pass"` — two tokens, nothing else.

### R4 — do-nothing control REFUSEALL: the counter prints no verdict at all

```
python3 -B counter/c1-count.py \
  --builder /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round58/controls/REFUSEALL.py \
  --work $S/runs/refuseall/work
```
EXIT=1, `C1_LINES=0`, `LEG_LINES=0`, stderr tail:
`FileNotFoundError: [Errno 2] No such file or directory: '…/runs/refuseall/work/out-empty/spans/S777-1.txt'`.
The counter crashes at `212` because `out-empty/spans` never exists when the builder refuses on the
first leg. A deny is therefore indistinguishable from a crash, and any builder refusing early gets
no scored verdict at all — the same defect blocks the *positive* direction (a candidate that
improves by refusing earlier is silenced instead of scored).

### R5 — per-leg positive token forged without a refusal (frozen counter)

```
python3 -B counter/c1-count.py --builder $S/noop-symlink-out.py --work $S/runs/noop-frozen/work
```
`SYMLINK_OUT=pass(refused)` is printed although the builder **exited 0** and refused nothing; the
leg's own run reproduces it standalone:
```
python3 -B $S/noop-symlink-out.py --quotes …/work/quotes.tsv --out …/work/out-link --cache …/work/cache
noop-symlink-out: accepted symlinked --out, wrote nothing
FORGER_SYMLINK_LEG_EXIT=0
```
`realdir/` stays empty (0 entries) — which is exactly the condition under which `234` overwrites
the leg. Non-zero-exit and reason-class verdicts from `expect_refuse` are discarded.

### R6 — the same forger under the case-fixed counter: unearned `C1=PASS`

```
python3 -B counter-casefix/c1-count.py --builder $S/noop-symlink-out.py --work $S/runs/noop-casefix/work
```
All eleven legs `pass`, `SUMMARY … REFUSE=7/7 …`, `C1=PASS`, EXIT=0 — for a builder that violates
frozen-claim clause (2) (“symlinked output … inputs are refused”). The positive verdict is therefore
**not entailed** by the declared predicate even after the two-token repair.

### R7 — a correct refusal scored fail (inverted `forbidden_touch`)

```
python3 -B counter/c1-count.py --builder $S/refuse-stray-symlink-out.py --work $S/runs/refuse-stray/work
```
`SYMLINK_OUT=fail(/…/runs/refuse-stray/work/realdir/spans.tsv was touched/removed)(target-dir-written!)`,
`SUMMARY OK=4/4 REFUSE=0/7 …`, `C1=FAIL`. The builder printed
`build-spans: refused SYMLINK output …` and exited 1, never writing through the link; the leg fails
because `expect_refuse`'s `forbidden_touch` loop (`if not p.exists(): return FAIL("… was touched/
removed")`) fires on a path that is *correctly absent*. The only reason the frozen receipt's
`target-dir-written!` case reaches `expect_refuse` at all is that the target dir was non-empty.

### R8 — the SUMMARY line is cosmetic for the verdict

```
python3 -B counter-verdictonly/c1-count.py --builder $S/positive-shim.py --work $S/runs/shim-verdictonly/work
```
`SUMMARY OK=4/4 REFUSE=0/7 …` together with `C1=PASS`, EXIT=0. Fixing `391` alone flips the verdict
while `399` still prints `REFUSE=0/7`; any reader who keys on `REFUSE=` (as the round-58 receipts
invite) misreads a repaired counter's positive result as a refusal failure.

## Findings (positive verdict-path calibration)

1. **The frozen positive path is unreachable.** A builder satisfying all eleven declared legs —
   four safe legs verified by digest/offset/span-bytes and seven hazard legs refused with the named
   reason classes and no forbidden writes — is scored `C1=FAIL`, exit 1 (R2). The mechanism is
   `51`/`160`/`223`/`234`/`315` emitting lowercase `=pass` against `391`/`399` demanding `=PASS`.
   `C1=FAIL` from this counter is not evidence that a builder is unhardened, and `REFUSE=0/7` is not
   evidence that refusal legs failed. This independently reproduces round-58's D1 from scratch bytes
   and, for the first time in this lane, pairs it with its **repair twin** (R3): the same builder and
   fixtures reach `C1=PASS`, exit 0, under a two-token change.
2. **The positive verdict, once reachable, is unearned on the symlink leg** (R5/R6): `234` writes the
   pass token whenever the link target is empty, so a builder that exits 0 having accepted a
   symlinked `--out` reaches `C1=PASS` on the repaired counter.
3. **A correct refusal is false-killed** when the link target holds any unrelated entry (R7), because
   `expect_refuse`'s `forbidden_touch` is inverted. This is the same root as (2); repairing only the
   case tokens leaves both directions mis-scored.
4. **The do-nothing-control clause is vacuous in one direction and silent in the other** (R4): the
   REFUSEALL child produces zero `C1=` lines and a traceback, so `DENIED=n/n` records a crash as a
   denial, and a candidate that refuses earlier than the base gets no scored verdict.
5. **`SUMMARY REFUSE=` is not verdict-bearing** (R8): a repaired counter prints `C1=PASS` beside
   `REFUSE=0/7`.

Bounded inference (not measured): `389` is a dead duplicate of `390`, and `expect_ok`'s `got`/`want`
sets (`got` computed, never compared) cannot catch unlisted outputs — read from the frozen bytes,
not exercised by a probe here.

## Limits / unrun

- Round-59 frozen claims are absent, so no round-59 claim, axis score, or control-set verdict is
  asserted. Everything above is about the round-58 frozen counter at
  `65da18bb…c703d3f` and the base builder at `1ed2650a…c80bf6`.
- Not run: `--controls` recursion under the case-fixed counter (it re-invokes the frozen counter and
  would regenerate the 413 MB `MANY_QUOTES` tree); the seed-sensitivity legs (D2) and the `--check`
  surface are round-58 documented and out of this seat's positive-path scope; no `HELDOUT_OK`
  variant beyond the counter's own; no live fetch; no package install.
- The `positive-shim.py` builder is a scratch instrument, not a proposed patch, and satisfies the
  legs *as implemented*, not a general security statement about `tools/build-spans.py`.

## Recommendation (proposal only; nothing applied)

Before any re-freeze, the positive-path calibration check of QUALITY criterion 115 must fail closed
in both directions on this exact counter: (a) require a positive builder to reach the target token
**and** exit 0 — at frozen bytes it cannot (R2), and after the token repair a non-refusing builder
can (R6); (b) require the do-nothing control to be *scored* `C1=FAIL` rather than crash (R4); and
(c) make each refusal leg's pass token derive from `expect_refuse`'s rc/reason/forbidden-path result
instead of an unconditional overwrite (R5/R7).

## Adjunct — independent replication and control-battery calibration (second spawn of this seat)

This seat (`ChousaR59.R59Executor06`) is a duplicate spawn assigned the same item and report path.
The assigned scratch `/fast/scratch/hyaku/chousa-r59/R59Executor06` was concurrently occupied by the
first spawn (its `counter/`, `runs/`, `positive-shim.py`), and its `rm -rf` deleted this seat's first
fixture tree mid-run (a `FileNotFoundError` in `snapshot()` at `c1-count.py:64`, not a counter
defect — excluded below). To avoid destroying a sibling's bytes this seat used
`/fast/scratch/hyaku/chousa-r59/R59Executor06-chousa`, a distinct subtree. Everything below was
measured there from byte copies; the lane was not edited.

Pins re-measured at filing (read-only): `c1-count.py` `65da18bb…c703d3f`; `build-spans-r55.py`
`1ed2650a…c80bf6`; `tools/build-spans.py` `1ed2650a…c80bf6` (byte-identical to the r55 control);
`capture-text.py` `2c0140bc…2573`; `REFUSEALL.py` `e7721cef…572fb`. Scratch copies of the counter
and controls carry those same digests. `git status --porcelain` shows only the pre-existing untracked
`.ufo/waves/round-59/` and `corpus/evidence/round59/`; no tracked byte moved.

Instruments (scratch-only, `$S=/fast/scratch/hyaku/chousa-r59/R59Executor06-chousa`):

- `$S/positive-control.py` — must-pass builder: applies the pinned r55 delegate for span arithmetic
  and adds only the guards the legs name (`--out` symlink → `SYMLINK`; cache entry symlink →
  `SYMLINK`; non-regular cache entry → `NOT_REGULAR`; >64 MiB cache file → `SIZE`; >100 000 quote
  rows → `ROWS cap`; an `S###-N.txt` in `<out>/spans` with no planned row → `foreign`).
- `$S/positive-nosymlink.py` — same, with the `--out`-symlink refusal message changed to
  `OUT_UNRESOLVED` (no `SYMLINK` token).
- `$S/mutant/c1-count.py` — the frozen counter with **only** `391` and `399` changed
  `"=PASS"` → `"=pass"` (verified by `diff -u`; nothing else differs).
- `$S/controls-pos/{REFUSEALL.py -> positive-control.py, build-spans-r55.py}` — a control dir in which
  the must-pass builder occupies the battery's fixed `REFUSEALL.py` slot.

### R9 — frozen counter, must-pass builder: every leg passes, verdict FAIL, EXIT=1

```
cd $S && TMPDIR=$S/run PYTHONDONTWRITEBYTECODE=1 \
  python3 -B frozen/c1-count.py --builder $S/positive-control.py --work $S/run/positive2 --seed 7
```
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
DENIED=0/0
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
```
`EXIT=1`, stderr 0 bytes, wall 2.3 s. The passes are substantive: `run/positive2/out-empty/spans.tsv`
has 3 rows (S501–S503) and `out-heldout/spans.tsv` 3 rows with the pinned Chinese quotes
(S601–S603); `out-empty/spans/S777-1.txt` survives (23 B); `realdir/`, `out-many/`, `out-esc/` are
empty. Reproduces R2's positive direction from an independently written builder.

### R10 — a must-pass builder in the frozen `--controls` battery is scored "denied" (new)

```
cd $S && TMPDIR=$S/run PYTHONDONTWRITEBYTECODE=1 \
  python3 -B frozen/c1-count.py \
  --builder /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py \
  --work $S/run/negative-posctl --seed 7 --controls $S/controls-pos
```
```
CONTROL_REFUSEALL=denied
CONTROL_build-spans-r55=denied
DENIED=2/2
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=FAIL
```
`EXIT=1`; 56.7 s. The `REFUSEALL.py` slot holds a builder that R9 shows satisfies all eleven legs,
yet the battery records it as denied. The counter's control check (`c1-count.py` control loop) asks
only whether the nested run printed `C1=PASS`; under the frozen token bug nothing can, so
`DENIED=n/n` is satisfied by *any* builder — a do-nothing one and a fully hardened one are scored
alike. This is the deny-only battery's vacuity measured directly, not inferred: the battery has no
must-pass slot (the names are fixed to `REFUSEALL.py` and `build-spans-r55.py`), so round-58 fix (c)
cannot be expressed without changing frozen bytes.

Control runs without the substitution (`--controls $S/frozen/controls`) print the byte-identical
`SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2` / `C1=FAIL` of
`corpus/evidence/round58/controls/c1-controls.txt`, confirming the reproduction.

### R11 — two-token repair reaches PASS; R12 — repair keeps discrimination

```
cd $S && TMPDIR=$S/run PYTHONDONTWRITEBYTECODE=1 \
  python3 -B mutant/c1-count.py --builder $S/positive-control.py --work $S/run/mutant-positive --seed 7
```
Identical eleven leg lines, `SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0`,
`C1=PASS`, `EXIT=0`. `diff -u frozen/c1-count.py mutant/c1-count.py` is exactly the two
`=PASS` → `=pass` hunks at `391` and `399`.

```
cd $S && TMPDIR=$S/run PYTHONDONTWRITEBYTECODE=1 \
  python3 -B mutant/c1-count.py --builder $S/frozen/controls/build-spans-r55.py \
  --work $S/run/mutant-r55 --seed 7
```
`SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0`, `C1=FAIL`, `EXIT=1`, stderr empty
(27.2 s). So the repaired verdict is not a rubber stamp: the base/r55 builder is still rejected on
its hazard legs; only the token mismatch separated R9's healthy builder from it.

### R13 — reason check is not load-bearing on `SYMLINK_OUT` (independent of R5)

```
cd $S && TMPDIR=$S/run PYTHONDONTWRITEBYTECODE=1 \
  python3 -B frozen/c1-count.py --builder $S/positive-nosymlink.py --work $S/run/nosymlink --seed 7
```
```
SYMLINK_OUT=pass(refused)
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
```
`EXIT=1`. The builder refused with the message `OUT_UNRESOLVED --out … is a link` — zero `SYMLINK`
token — yet `234` rewrites `expect_refuse`'s `fail(reason … absent)` to `pass(refused)` because the
link target stayed empty. Confirms, from a different probe than R5, that the declared reason-class
check on this leg is discarded.

### R14 — direct do-nothing run: no verdict line, a traceback

```
cd $S && TMPDIR=$S/run PYTHONDONTWRITEBYTECODE=1 \
  python3 -B frozen/c1-count.py --builder $S/frozen/controls/REFUSEALL.py --work $S/run/refuseall --seed 7
```
`EXIT=1`, stdout empty (0 leg lines, 0 `C1=` lines), stderr ends
`FileNotFoundError: … run/refuseall/out-empty/spans/S777-1.txt`: `foreign.write_bytes` at `:212`
assumes the builder created `<out>/spans`, which an early refusal does not. The nested "denied" in
R10's REFUSEALL slot is therefore a crash, not a scored `C1=FAIL` — same as R4.

## Adjunct findings

1. **The frozen control battery is vacuous in the credit direction (R10, new).** A builder that
   satisfies every declared leg is recorded `CONTROL_…=denied` and `DENIED=2/2`. `DENIED=n/n` at the
   frozen bytes certifies nothing: it is invariant over builder quality, so the freeze's deny-only
   receipt cannot show the target was reachable — exactly QUALITY criterion 115's concern, now
   measured through the battery rather than only through the verdict line.
2. **The repair is minimal and discriminating (R11/R12).** Two `=pass` tokens flip R9's healthy
   builder to `C1=PASS`/exit 0 while r55 still fails its hazard legs. So the positive path is
   satisfiable at the frozen legs; the blocker is the token, not an unsatisfiable predicate.
3. The reason-masking (`:234`, R13) and the crash-as-denial (`:212`, R14) are independent defects
   beneath the same verdict line; fixing the tokens alone leaves both, as R5–R7 already show.

## Adjunct limits / unrun

- No round-59 claim is asserted: `corpus/evidence/round59/claims.md` is absent, and
  `round59/controls/c1-before.txt` (`2c9bbe54…bfe`) is the round-58 base receipt.
- Not run: `--check` surface; seed sweep; any live fetch (L0 `8d77e6c1` stays open); any install
  (`/home/vgpnk/.omp/agent/RULES.md` read; pacman not invoked). `positive-control.py` is a scratch
  instrument satisfying the legs as implemented, not a proposed patch to `tools/build-spans.py`.
- Scratch `$S` is removed before yield; the exact outputs above are quoted in full.

Report (adjunct): `.ufo/waves/round-59/w1/R59Executor06.md`
