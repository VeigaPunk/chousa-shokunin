# R59Executor04 — round-58 frozen C1 counter, positive-verdict-path calibration

Lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin` (all lane bytes read-only for this seat).
Scratch `/fast/scratch/hyaku/chousa-r59/R59Executor04/` (removed before yield; all receipts below are
quoted verbatim from that scratch). No lane file, git/jj index, frozen claim or counter was written.
No tool installed or updated; `/home/vgpnk/.omp/agent/RULES.md` was read, no pacman transaction ran.

## 0. Inputs, under what was actually on disk

| item | measured value |
|---|---|
| `corpus/evidence/round59/claims.md` (the spec's frozen-claims path) | **absent** at read time; `corpus/evidence/round59/` contained only `census-start.txt` and `controls/c1-before.txt` |
| fallback frozen claims read | `corpus/evidence/round58/claims.md` (25 lines, claim base `b13ca7b5c8bbb40d2d29a37fb443c64ca043f791`) |
| frozen C1 counter copied into scratch | `corpus/evidence/round58/c1-count.py`, sha256 `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f`, 406 lines |
| frozen control builder copied | `corpus/evidence/round58/controls/build-spans-r55.py`, sha256 `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6` = the r55 pin in the counter |
| frozen REFUSEALL copied | `corpus/evidence/round58/controls/REFUSEALL.py`, sha256 `e7721cefe050ee435d3bab811ed65933d26a865ca30340feaab3f9388c3572fb` |
| lane `tools/build-spans.py` | sha256 `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6` — **byte-identical to the pinned r55 builder** (no production patch landed in round 58) |
| lane `tools/capture-text.py` | sha256 `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573` = the counter's `CAPTURE_TEXT_SHA` |
| lane `corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` | 129024 B, sha256 `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3` |
| interpreter | `Python 3.14.8 (main, Oct 2 2026) [GCC 16.2.1]` |

Setup (scratch only):

```
mkdir -p /fast/scratch/hyaku/chousa-r59/R59Executor04/frozen58/controls
cp -p <lane>/corpus/evidence/round58/c1-count.py                     frozen58/
cp -p <lane>/corpus/evidence/round58/controls/build-spans-r55.py     frozen58/controls/
cp -p <lane>/corpus/evidence/round58/controls/REFUSEALL.py           frozen58/controls/
```

The copy keeps `HERE = <scratch>/frozen58`, so the counter's own `BEFORE_BUILDER = HERE/controls/build-spans-r55.py`
integrity leg is live in scratch; `LANE` inside the counter stays the real read-only lane (capture store reads only).

## 1. R1 — exact frozen counter, lane builder (60 s)

```
python3 -B frozen58/c1-count.py --builder <lane>/tools/build-spans.py --work <scratch>/run-base --seed 7
EXIT=1 ELAPSED=60s

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

Reproduces the frozen base receipt byte-for-byte (`corpus/evidence/round58/controls/c1-before.txt`, and the
round-59 lane copy `corpus/evidence/round59/controls/c1-before.txt`, sha256 `2c9bbe5446ae4f733bf17a2836cc1b32e823fc8bc287d3da42801b948cfaebfe`,
which this seat did not write).

## 2. R2 — exact frozen counter with frozen do-nothing controls (54 s)

```
python3 -B frozen58/c1-count.py --builder <lane>/tools/build-spans.py --work <scratch>/run-controls \
  --seed 7 --controls <scratch>/frozen58/controls
EXIT=1 ELAPSED=54s

... same eight hazard legs ... ESCAPE_ENTRY=pass(refused) HELDOUT_OK=pass
BEFORE_FOREIGN=deleted
CONTROL_REFUSEALL=denied
CONTROL_build-spans-r55=denied
DENIED=2/2
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=FAIL
```

Matches `controls/c1-controls.txt`.

## 3. R3 — positive control: a conforming builder, every frozen leg satisfied (1 s)

Scratch-only builder `<scratch>/ideal-builder.py` (119 lines, sha256 `5ae42d4946553cbf36e2f85215787e3bc71b84b8547950b408cd35a2b6e8c4f7`)
was written to meet each frozen leg as the counter's own oracle defines it: symlink/type/size checks on
`--out` and on the resolved capture (`.raw` preferred, form via the pinned `capture-text.py`), 100 000-row
cap, `..` entry refusal, foreign/orphan span refusal before deletion, and the counter's exact span slice
`form[start : start+len(q)+min(80,start)+80]` with `start=max(0,pos-80)`. It is evidence, not a lane patch.

```
python3 -B frozen58/c1-count.py --builder <scratch>/ideal-builder.py --work <scratch>/run-ideal --seed 7
EXIT=1 ELAPSED=1s

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

All 11 declared legs pass; the verdict is still `FAIL`. Positive control therefore **fails**, and the
frozen target `C1=PASS` is unreachable for this builder.

## 4. R4 — frozen aggregate evaluated on R3's exact leg lines

```
ok_legs        = ['EMPTY_OK=pass', 'REBUILD_OK=pass', 'ESCAPE_ENTRY=pass(refused)', 'HELDOUT_OK=pass']
ok_pass        = True
ref_legs       = ['FOREIGN=pass(refused)', 'SYMLINK_OUT=pass(refused)', 'SYMLINK_CACHE=pass(refused)',
                  'FIFO_TXT=pass(refused)', 'DEVZERO_TXT=pass(refused)', 'FAT_RAW=pass(refused)',
                  'MANY_QUOTES=pass(refused)']
ref_pass       = False   <-- frozen aggregate requires uppercase '=PASS'
ref_pass_lower = True   <-- same lines tested for '=pass'
integrity      = True  denied_pass = True
frozen verdict = FAIL
verdict if only the case token were normalised = PASS
```

Root cause, exact frozen lines (`frozen58/c1-count.py:51,147,160,391,394,399`):

* `51: PASS = "pass"`; `147`/`160` emit `f"{name}={PASS}"` / `f"{name}={PASS}(refused)"` → lowercase `=pass`.
* `391: ref_pass = all(("=PASS" in l) for l in ref_legs)` → uppercase; no hazard leg can ever satisfy it.
* `394: verdict = "PASS" if (ok_pass and ref_pass and integrity and denied_pass) else "FAIL"`.
* `399` prints `REFUSE={sum('=PASS' in l ...)}` — so even a repaired verdict would print `REFUSE=0/7`.
* `389` is a dead predecessor of `390` (overwritten before use; no behaviour).

## 5. R5 — a builder that writes through the symlink still scores `pass` on that leg

Scratch violator `violator-symlinkout.py` (121 lines, sha256 `692a2ef5f87a2cd2dd60e93a7eac36b46cae145163ecc324e3e61550d77a2e5f`)
is `ideal-builder.py` with the `--out` symlink refusal moved **after** the writes.

```
python3 -B frozen58/c1-count.py --builder <scratch>/violator-symlinkout.py --work <scratch>/run-violator --seed 7
EXIT=1

EMPTY_OK=pass REBUILD_OK=pass FOREIGN=pass(refused)
SYMLINK_OUT=pass(refused)(target-dir-written!)
SYMLINK_CACHE=pass(refused) FIFO_TXT=pass(refused) DEVZERO_TXT=pass(refused)
FAT_RAW=pass(refused) MANY_QUOTES=pass(refused) ESCAPE_ENTRY=pass(refused) HELDOUT_OK=pass
BEFORE_FOREIGN=deleted DENIED=0/0
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
```

Work-tree proof that the symlink target was written:

```
f <scratch>/run-violator/realdir/spans/S501-1.txt
f <scratch>/run-violator/realdir/spans/S502-1.txt
f <scratch>/run-violator/realdir/spans/S503-1.txt
f <scratch>/run-violator/realdir/spans.tsv
l <scratch>/run-violator/out-link
```

The hazard leg still reports `pass(refused)` with its own `(target-dir-written!)` annotation, and the frozen
code never consults that annotation: `expect_refuse:157-159` treats `forbidden_touch` as paths that must
**exist** (`if not p.exists(): return FAIL(... was touched/removed)`), and the leg's override at `:235-236`
only appends the annotation. Masked today solely by the same case defect.

## 6. R6/R7 — one-token scratch mutation (not a lane change)

Scratch copy `frozen58/fixed-count.py` (sha256 `6b6000ed83f25e9c8ddbe757624da9a3f085834a5d9b7609d14f4013c95d3a46`)
changes exactly `:391` `=PASS` → `=pass`.

```
# R6 conforming builder
python3 -B frozen58/fixed-count.py --builder <scratch>/ideal-builder.py --work <scratch>/run-fixed-ideal
EXIT=0
... 11 legs all pass ... BEFORE_FOREIGN=deleted DENIED=0/0
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=PASS

# R7 same counter, symlink-out violator
python3 -B frozen58/fixed-count.py --builder <scratch>/violator-symlinkout.py --work <scratch>/run-fixed-violator
EXIT=0
... SYMLINK_OUT=pass(refused)(target-dir-written!) ... DENIED=0/0
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=PASS
```

Two positive-path facts: the repaired token makes `C1=PASS` reachable (`R6`), and the same repaired
predicate accepts a builder that wrote into the symlink target (`R7`, `realdir/spans.tsv` present). The
receipt is also internally inconsistent — `C1=PASS` printed beside `REFUSE=0/7`.

## 7. R8/R9 — the do-nothing control gate cannot see the positive path

`--controls` is opt-in (`:169`) and vacuous when absent (`:393 denied_pass = (denied == total) if total else True`).
The frozen invocation in `claims.md:9` is `python3 corpus/evidence/round58/c1-count.py --builder <builder> --work <fresh-absolute-dir>` —
**no `--controls`**, so R3/R6 already ran with `DENIED=0/0` and `denied_pass=True`.

Control children are re-invocations of the frozen file by name (`:372 str(HERE / "c1-count.py")`), and denial is
`tail[0].strip() == "C1=PASS"` (`:377`). A conforming builder placed as the control (`ctl-ideal/REFUSEALL.py` =
`ideal-builder.py`):

```
# R8 frozen counter, candidate=ideal, --controls <scratch>/ctl-ideal
EXIT=1
... 11 legs all pass ... CONTROL_REFUSEALL=denied DENIED=1/1
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=1/1
C1=FAIL

# R9 fixed-token counter, same candidate and control
EXIT=0
... 11 legs all pass ... CONTROL_REFUSEALL=denied DENIED=1/1
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=1/1
C1=PASS
```

A builder that satisfies every leg predicate is scored `denied` as a control, because the child cannot print
the uppercase token; and after the one-token repair the verdict is `PASS` while the same conforming control is
still `denied`. `DENIED=n/n` is therefore not evidence about control behaviour: no observed control result can
distinguish a do-nothing control from a conforming builder.

## 8. R10 — span-oracle formula (latent, not triggered at the default seed)

The counter's expected span end is `start + len(q) + min(CONTEXT, start) + CONTEXT` (`:139-141`), which for
`pos < 80` ignores `pos` (`start = 0` → end `= len(q)+80`). Probe of the counter's own fixtures at default seed 7:

```
synthetic quote positions: [3734, 1415, 4074]   len(txt)=14833   CONTEXT=80
pos=3734 start=3654 frozen_end=3834 natural_end=3834 equal=True
pos=1415 start=1335 frozen_end=1511 natural_end=1511 equal=True
pos=4074 start=3994 frozen_end=4170 natural_end=4170 equal=True
```

At the frozen default seed the two formulas coincide, so this is a latent oracle divergence (a builder with the
documented `quote ± 80` slice would fail only for `pos < 80`), not an observed kill.

## Findings (operability / calibration)

1. **F1 (positive verdict unreachable, reproduced).** With the exact frozen bytes and a builder satisfying all
   11 declared legs, the counter prints `OK=4/4 REFUSE=0/7 C1=FAIL`, exit 1. `ref_pass` (`:391`) requires
   uppercase `=PASS`; every refusal emitter writes lowercase `=pass` (`:51,147,160`). Verified by R3 + R4.
2. **F2 (positive control now exists and fails).** A concrete conforming builder is the positive control the
   round-58 freeze lacked; it fails the frozen target. The missing check named by QUALITY 115 is reproducible
   in one command.
3. **F3 (single-token repair reaches a false accept).** Normalising `:391` to lowercase yields `C1=PASS`/exit 0
   (R6) and also `C1=PASS` for a builder that wrote into the symlink target (R7). The positive path is
   reachable but not calibrated: `SYMLINK_OUT` carries its own `(target-dir-written!)` marker, and
   `expect_refuse:157-159` inverts the forbidden-touch test (requires the forbidden path to exist), so the
   marker is inert. Any repair must fix the check, not only the token.
4. **F4 (control gate is vacuous / disconnected).** The frozen target invocation omits `--controls`
   (`claims.md:9`), `denied_pass` is `True` when no controls run (`:393`), and when `--controls` is supplied the
   child is the frozen file itself (`:372`), so a conforming builder is scored `denied` (R8) and stays `denied`
   beside a repaired `C1=PASS` (R9). `DENIED=2/2` in `controls/c1-controls.txt` cannot discriminate.
5. **F5 (receipt self-contradiction under repair).** The summary tally keeps the uppercase token (`:399`), so a
   repaired run prints `C1=PASS` with `REFUSE=0/7` (R6/R7/R9).
6. **F6 (script-location coupling, fails closed).** Run from outside `frozen58/`, `BEFORE_FOREIGN=absent` and the
   verdict fails (integrity false) — observed on the first `fixed-count.py` placement; no false accept.
7. **Latent only.** The span-end formula (`:139-141`) diverges from the documented slice when `pos < CONTEXT`;
   untriggered at seed 7 (R10).

## Limits

* C2 was not re-run (no entry/manifest work in this seat); the round-58 `C2` offset contradiction is not
  re-measured here and is taken only from lane records, not asserted as my observation.
* The conforming builder and violator are scratch evidence, not proposed lane patches; no production file was
  evaluated or modified.
* Lane writes by this seat: none. Post-run check: no lane file newer than `15:15:00` under `tools/` or
  `corpus/` outside `.ufo/.git/.jj`; no new bytecode (`tools/__pycache__` newest `.pyc` is `2026-10-27 14:21`).
  The two round-59 lane files (`census-start.txt`, `controls/c1-before.txt`, both 15:14) predate this seat's runs
  and were not written by it.

## Files changed

* `.ufo/waves/round-59/w1/R59Executor04.md` (this report) — the only lane-adjacent write.
* Scratch `/fast/scratch/hyaku/chousa-r59/R59Executor04/` (frozen copies, two scratch builders, fixed-token copy,
  run logs and work trees) — removed before yield; all receipts are transcribed above.

## Risks

* Round-59 `claims.md` was absent while the spec and R1–R16 all name it; any seat that treats its absence as
  permission to freeze a new claim would be acting without the declared freeze.
* A future round that repairs only the `=PASS`/`=pass` token would turn R7 into an admitted false accept on the
  exact hazard the frozen claim calls destructive.

Report: .ufo/waves/round-59/w1/R59Executor04.md
