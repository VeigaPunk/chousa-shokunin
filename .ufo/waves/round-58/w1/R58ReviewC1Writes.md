# R58 C1 output-behavior review

## Scope / inspected frozen artifacts

- Read `corpus/evidence/round58/claims.md` and exact `corpus/evidence/round58/c1-count.py`; claim base `b13ca7b5c8bbb40d2d29a37fb443c64ca043f791`; freeze commit `9e73a031ab1ac3bac343de008850d7d87f9e5634`.
- Lane HEAD observed `5da0a6375a554e1229492a8cb0b9695bd8e85456`. `tools/build-spans.py` SHA256 `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`, identical to pinned R55 control; thus no hardened candidate is present at this HEAD. No lane files modified.
- Axis: C1 operability. This review assesses battery coverage and observed output-mode behavior, not C1 score/admission.

## Scratch probes / exact observations

Scratch was `/fast/scratch/hyaku/chousa-r58/R58ReviewC1Writes/` (removed before report). Copied the frozen counter there and ran:

```text
python3 /fast/scratch/hyaku/chousa-r58/R58ReviewC1Writes/c1-count.py --builder /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py --work /fast/scratch/hyaku/chousa-r58/R58ReviewC1Writes/work
```

Observed: `EMPTY_OK=pass`, `REBUILD_OK=pass`, `FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)`, `SYMLINK_OUT=fail(rc=0, expected refusal)(target-dir-written!)`, `SYMLINK_CACHE=fail(rc=0, expected refusal)`, FIFO/DEVZERO/FAT_RAW fail the required reason match, `MANY_QUOTES=fail(rc=0, expected refusal)`, `ESCAPE_ENTRY=pass(refused)`, `HELDOUT_OK=pass`, `BEFORE_FOREIGN=absent`, `DENIED=0/0`, `C1=FAIL` (exit 1).

Additional `--check` probe, in that scratch work directory:

```text
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py --quotes quotes.tsv --out out-empty --cache cache --check
```

Output `SPANS_ROW_STALE spans/S503-1.txt`, `SPANS_ROWS=3 STALE=1`, `RC=1`; hashes of `out-empty/spans.tsv` and `out-empty/spans/S501-1.txt` were identical before/after (`21e469419c502211973ca3591c0c5f83956aa244eaaa29d93fc5c2dd0ec767a`, `3f3d6943ea42f03ba3815a4f8d29c0a383252f0a24dbec13eede727a5bd7e53c`). Then with `S777-1.txt` present, `--check` against `quotes-few.tsv` emitted `SPANS_FILE_ORPHAN spans/S777-1.txt`, `SPANS_ROWS=2 STALE=1`, `RC=1 foreign=present`.

## Findings by severity

### High — refusal-before-mutation is not established across the hazard battery

Claim says hazardous input classes are refused “without partial writes”; counter header says hazard legs refuse and “touch nothing.” In `expect_refuse`, `forbidden_touch` is empty for SYMLINK_CACHE, FIFO_TXT, DEVZERO_TXT, FAT_RAW and MANY_QUOTES, so those legs assert only nonzero status and a matching reason. FOREIGN checks only that the named foreign file remains; it does not snapshot existing manifest/span bytes or other orphans. A builder can mutate/delete other output files and then refuse while these legs still pass. Only SYMLINK_OUT checks target-directory contents (and that check is flawed; see below). Thus the named foreign file’s survival is tested, but “refusal before orphan deletion” / no partial output mutation is not generally tested. Observed R55 baseline deletes the foreign file and counter correctly fails this leg; target behavior remains unmeasured because HEAD is R55.

### High — SYMLINK_OUT leg can falsely pass

The leg calls `expect_refuse(..., forbidden_touch=[real / "spans.tsv"])`, which requires the file to exist, contrary to refusal. It then replaces the result with PASS whenever `real` is empty, without checking return code or refusal reason. If `real` is nonempty, it appends `(target-dir-written!)` to the leg string, but final `ref_pass` checks only whether `"=PASS"` occurs; that suffix does not turn PASS into FAIL. The observed baseline produced a fail string, but the predicate logic would accept a crafted `SYMLINK_OUT=PASS(refused)(target-dir-written!)` result. No defense against symlinked `out/spans`, `out/spans.tsv`, or symlinked output ancestors is exercised; only `--out` itself is a symlink.

### High — normal output writes are non-atomic; atomicity is not measured

Builder implementation uses direct `(out / "spans.tsv").write_bytes(...)`, then direct per-span `write_bytes(...)`, and deletes orphan files before those writes. No temp-file/rename transaction is used. C1 checks successful output contents and rebuild identity, but no interruption/failed-write injection or before/after snapshot of all outputs on a refusal. The stated refusal battery therefore does not demonstrate atomic writes or complete rollback. No `--check` leg exists in `c1-count.py`; it does not establish output behavior for check mode. My check-mode scratch probe observed no mutation in the exercised R55 cases (including reporting a foreign span orphan); this is limited evidence for those invocations, not an atomicity/race guarantee.

### Medium — `--check` / other symlink shapes and extras are outside counter coverage

Counter invokes builder without `--check` throughout. It tests cache `.txt` symlink to regular target and `--out` symlink only; no `.raw` symlink, symlinked cache directory, symlinked `out/spans`, manifest symlink, or symlinked input quote file. `snapshot()` excludes symlinks and only records regular files. In `expect_ok`, `got` and `want` are constructed but never compared, so unanticipated extra output files within `--out` are not rejected. These are scope gaps, not claims that all such attacks were run.

### Medium — optional controls are skipped by the frozen invocation

`--controls` is optional; when omitted, `DENIED=0/0` and `denied_pass` is true. The frozen command documented in claims.md does not pass `--controls`, so the predicate invocation does not exercise REFUSEALL or R55 controls. Separate lane receipt `controls/c1-controls.txt` does show both controls denied in its explicit command; this is separate evidence and does not make the default counter invocation enforce that condition.

## Residual risk / verification gaps

- No hardened builder exists at observed HEAD, so behavior of intended fix is untested. R55 is the measured baseline/control only.
- No crash/power-loss write probe, alternate symlink-shape probe, or deliberately partial-refusal builder was run. Counter source inspection suffices to identify missing assertions but does not establish those hypothetical implementations’ outputs.
- `--check` scratch probes exercised R55 only and did not test FIFO/device cache inputs in check mode.

VERDICT: C1 output-hardening attack is **inconclusive for a hardened target** (none present at HEAD); the frozen counter demonstrably falsifies the R55 baseline on foreign/symlink hazards, but does not establish general refusal-without-mutation, atomic writes, or `--check` safety.