# Round 59 mutation probe — C1 positive verdict path

## Scope and frozen target

The requested `corpus/evidence/round59/claims.md` was absent (`read` returned not found); `corpus/lessons/round-59.md` says no round-59 claims were validly frozen. I therefore tested the exact frozen round-58 C1 counter and rule in `corpus/evidence/round58/claims.md`, without changing either source file. No fetch, install, git/jj mutation, or source-repository write.

## Mutant and detector

- **Counter mutant (scratch only):** changed only `ref_pass` at counter line 391 from `all(("=PASS" in l) ...)` to `all(("=PASS" in l or "=pass" in l) ...)`. This is a plausible case-insensitive token-acceptance defect at the positive verdict gate. Line 399's summary predicate stayed unchanged.
- **Detector:** same frozen C1 battery, run against both a positive-control builder and an adversarial reasonless-refusal builder. The claim requires all seven refusal legs to carry the expected reason class; the reasonless builder should therefore yield `C1=FAIL`, exit 1.
- **Positive-control builder:** scratch-only fixture builder, SHA-256 `79cc655ce8162b1a3403182289e00b0684edf8b4ad6e39874878b1ca44f349c1`. It passed the full battery with named reasons, preserved the foreign span, and refused the symlinked output before writing (the real target directory remained empty).
- **Reasonless builder input:** copy of that fixture builder with its shared refusal helper changed to emit only `=PASS` on stderr (no reason token), SHA-256 `b829943b3432fe97f8728d8efd04f42f4fdc50fb3e9bff3c9f2a7a7a94b4225e`. It still refuses the hazards and does not write through the symlink; this is a probe input, not a lane builder.

## Pins and commands

Scratch root: `/fast/scratch/hyaku/chousa-r59/R59MutationTester63`.

- Frozen counter: `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f`.
- One-line mutant counter: `cf315a5dd01468b3cb977fe619defe530e803280168d770d424315f3ae68f9de`.
- Restored counter: same SHA-256 as frozen counter above; `cmp` reported byte-identical.
- Pinned before-builder copy: `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`; capture-text copy: `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573`.

The six same-detector commands were:

```sh
S=/fast/scratch/hyaku/chousa-r59/R59MutationTester63
python3 -B "$S/ref/c1-count-pristine.py" --builder "$S/tools/build-spans-honest.py" --work "$S/work/P-honest"
python3 -B "$S/ref/c1-count-pristine.py" --builder "$S/tools/build-spans-forged.py" --work "$S/work/P-forged"
python3 -B "$S/ref/c1-count-mutated.py" --builder "$S/tools/build-spans-honest.py" --work "$S/work/M-honest"
python3 -B "$S/ref/c1-count-mutated.py" --builder "$S/tools/build-spans-forged.py" --work "$S/work/M-forged"
# Copy pristine bytes over c1-count-mutated.py; verify SHA/cmp; then:
python3 -B "$S/ref/c1-count-mutated.py" --builder "$S/tools/build-spans-honest.py" --work "$S/work/R-honest"
python3 -B "$S/ref/c1-count-mutated.py" --builder "$S/tools/build-spans-forged.py" --work "$S/work/R-forged"
```

Each run used a fresh absolute `--work` directory. No `--controls` flag was supplied (`DENIED=0/0` is vacuous in these runs).

## Observed outputs

**Pristine counter × positive-control builder** (exit 1): all four safe legs and all seven refusal legs emitted pass tokens; `HELDOUT_OK=pass`, `BEFORE_FOREIGN=deleted`, but `SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0` and `C1=FAIL`. Thus the positive path is masked: `PASS = "pass"` while the aggregate requires uppercase `=PASS`.

**Pristine counter × reasonless builder** (exit 1): safe legs pass; six refusal-leg strings are failures containing builder-controlled `=PASS`; `SYMLINK_OUT=pass(refused)` (the counter overwrites that leg when the target directory stays empty); `SUMMARY OK=4/4 REFUSE=6/7 BEFORE_FOREIGN=deleted DENIED=0/0`; `C1=FAIL`.

**Mutated counter × positive-control builder** (exit 0): `EMPTY_OK=pass`, `REBUILD_OK=pass`, `FOREIGN=pass(refused)`, `SYMLINK_OUT=pass(refused)`, `SYMLINK_CACHE=pass(refused)`, `FIFO_TXT=pass(refused)`, `DEVZERO_TXT=pass(refused)`, `FAT_RAW=pass(refused)`, `MANY_QUOTES=pass(refused)`, `ESCAPE_ENTRY=pass(refused)`, `HELDOUT_OK=pass`, `BEFORE_FOREIGN=deleted`; `SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0`; `C1=PASS`.

**Mutated counter × reasonless builder** (exit 0; decisive false positive):

```text
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=fail(reason-unnamed:'=PASS\n')
SYMLINK_OUT=pass(refused)
SYMLINK_CACHE=fail(rc=1, reason ['SYMLINK', 'REGTYPE', 'NOT_REGULAR'] absent in '=PASS\n')
FIFO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'FIFO', 'REGTYPE', 'SYMLINK'] absent in '=PASS\n')
DEVZERO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'SIZE', 'SYMLINK', 'REGTYPE'] absent in '=PASS\n')
FAT_RAW=fail(rc=1, reason ['SIZE'] absent in '=PASS\n')
MANY_QUOTES=fail(rc=1, reason ['SIZE', 'ROWS', 'CAP'] absent in '=PASS\n')
ESCAPE_ENTRY=pass(refused)
HELDOUT_OK=pass
BEFORE_FOREIGN=deleted
DENIED=0/0
SUMMARY OK=4/4 REFUSE=6/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=PASS
```

The final verdict is `C1=PASS` despite six explicitly failed refusal legs and `REFUSE=6/7`; candidate-controlled stderr satisfies the mutated substring predicate. This confirms the reasonless builder survives the mutated gate. The unmodified summary is itself evidence of the mismatch between the aggregate summary and final verdict.

**Restored counter:** both runs reproduced the pristine outputs byte-for-byte (`cmp` reported pristine/restored honest logs identical and pristine/restored reasonless logs identical). Restored outputs: positive-control `C1=FAIL`, exit 1; reasonless builder `C1=FAIL`, exit 1.

Additional bounded controls:

- Pinned round-55 builder, pristine counter: `FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)`, `SYMLINK_OUT=fail(rc=0, expected refusal)(target-dir-written!)`, `BEFORE_FOREIGN=deleted`, `C1=FAIL`, exit 1. The integrity control ran and the known-before builder deleted the foreign file.
- `REFUSEALL.py`, pristine and mutated counter: both crashed before emitting a leg or `C1=` line, at counter line 212 (`FileNotFoundError` writing `out-empty/spans/S777-1.txt`, because the early-refusing candidate never created `out-empty/spans`). This is not a scored `C1=FAIL`; `DENIED`/do-nothing calibration cannot be inferred from that crash.

## Verdict and restoration

**Verdict: INCONCLUSIVE for the full two-sided positive/negative contract**, because the pristine positive-control run fails the claimed `C1=PASS` baseline. Per mutation protocol, that baseline failure is not a killed mutant. Within the negative-rule cell, the reasonless candidate is rejected by pristine bytes (`C1=FAIL`) but survives the one-line mutated gate (`C1=PASS` with six failed legs), and is rejected again after restoration. This is a direct false-positive observation, not a claim that the frozen predicate is repaired or safe; no counter/claim change is proposed.

The mutated counter copy was restored from the frozen copy; both hashes are `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f`, and `cmp` confirmed exact byte identity. Lane-source hashes after the probe: frozen C1 counter `65da18bb…`, `tools/build-spans.py` `1ed2650a…`, `tools/capture-text.py` `2c0140bc…` (all equal their pre-probe hashes). The scratch tree was removed before handoff.

---
seat: R59MutationTester63
lane-root: /home/vgpnk/Projects/shokunin/chousa-shokunin
report: .ufo/waves/round-59/w1/R59MutationTester63.md
scratch: /fast/scratch/hyaku/chousa-r59/R59MutationTester63 (removed)
lane writes: .ufo/waves/round-59/w1/R59MutationTester63.md only
