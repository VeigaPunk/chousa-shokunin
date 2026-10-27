# R58ReviewC1Counter — C1 counter attack

## Scope / frozen inputs
- Read frozen `claims.md` and `c1-count.py`; freeze commit `9e73a031ab1ac3bac343de008850d7d87f9e5634`, claim base `b13ca7b5c8bbb40d2d29a37fb443c64ca043f791`.
- `git log --oneline 9e73a03..HEAD -- corpus/evidence/round58/c1-count.py corpus/evidence/round58/claims.md` → no output. Frozen/current claims SHA `7aedd8156c9fce185841a740b894600f8a4149b2d8e2034039f634c808373457`; counter SHA `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f`. Lane working tree for counter was clean after review.
- Pins checked: `capture-text.py` SHA `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573`; r55 builder SHA `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`; S101 raw SHA `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3` (all match frozen pins). Current candidate `tools/build-spans.py` has the r55 SHA.
- No LSP device/status route was exposed in this session; source inspection is literal fallback, not semantic reference proof.

## Findings (ordered)

### High — FOREIGN leg accepts destructive partial writes
Frozen code at `c1-count.py` FOREIGN leg checks only `proc.returncode`, that `S777-1.txt` survives, and whether stderr/stdout contains `777` or `foreign`. It does not verify the old owned orphan (`S503-1.txt`), manifest, or other output bytes remain unchanged. Therefore deleting ordinary prior output before refusing the foreign file still reports PASS, contrary to the frozen claim's “refusal before orphan deletion.”

Minimal scratch reproduction, mirroring the leg condition:
```
python3 - <<'PY'
from pathlib import Path
import subprocess
root=Path('/fast/scratch/hyaku/chousa-r58/R58ReviewC1Counter/foreign-demo')
out=root/'out'; spans=out/'spans'; spans.mkdir(parents=True,exist_ok=True)
owned=spans/'S503-1.txt'; foreign=spans/'S777-1.txt'; manifest=out/'spans.tsv'
owned.write_bytes(b'owned prior span'); foreign.write_bytes(b'foreign evidence bytes'); manifest.write_bytes(b'old manifest')
owned.unlink(); proc=subprocess.CompletedProcess([],1,stdout='',stderr='build-spans: refused FOREIGN S777')
if proc.returncode == 0: leg=f'FOREIGN=FAIL(rc=0, orphans deleted: foreign gone={not foreign.exists()})'
elif not foreign.exists(): leg=f'FOREIGN=FAIL(refused rc={proc.returncode} but foreign file deleted)'
else:
 err=((proc.stderr or '')+(proc.stdout or ''))[:200]
 leg='FOREIGN=PASS(refused)' if '777' in err or 'foreign' in err.lower() else f'FOREIGN=FAIL(reason-unnamed:{err!r})'
print('FOREIGN observed:',leg)
print('owned_orphan_exists=',owned.exists(),'foreign_exists=',foreign.exists(),'manifest_bytes=',manifest.read_bytes())
PY
```
Exact output:
```
FOREIGN observed: FOREIGN=PASS(refused)
owned_orphan_exists= False foreign_exists= True manifest_bytes= b'old manifest'
```

### High — ESCAPE_ENTRY passes after an escaped write
The leg treats any nonzero return and absence of `oute/spans.tsv` as success. It never snapshots/checks the work parent, escaped target, quote input, or other files. A builder that writes an artifact outside `--out` and then fails is accepted. Minimal scratch counter-helper probe output: `ESCAPE_ENTRY observed: ESCAPE_ENTRY=pass(refused) escaped_exists= True` (the probe wrote `escape.md` under its work directory before applying the frozen condition). The same missing snapshot on refusal legs permits partial output/fixture modifications to go unnoticed.

### High — SAFE leg accepts unmanifested span files
`expect_ok` builds `got` and `want` but never compares either to actual outputs. It checks only manifest row count and the manifest-referenced files. Scratch helper probe created `spans/UNLISTED.txt`; output was `EXPECT_OK observed: EMPTY_OK=pass` and `unlisted_span_exists= True`. Thus safe output can contain stray files and still pass; `REBUILD_OK` snapshots the whole output afterward, so it merely preserves/repeats whatever first build left.

### Medium — SYMLINK_OUT can PASS without a reason class
After `expect_refuse` checks nonzero and a reason substring, the caller overwrites the result with `SYMLINK_OUT=PASS(refused)` whenever `real` is empty. A silent unrelated crash/nonzero exit therefore passes with no `SYMLINK` diagnostic. Minimal probe with `returncode=1`, empty output, and untouched target produced exactly `SYMLINK_OUT observed: SYMLINK_OUT=PASS(refused)`.

### Medium — control-denial check is optional in the canonical invocation
`denied_pass = (denied == total) if total else True`; when `--controls` is omitted, total is 0 and control denial passes vacuously. The claims' canonical command provides `--builder` and `--work`, not `--controls`, while also requiring do-nothing controls not to reach `C1=PASS`. A candidate that passes the ordinary legs can therefore yield C1=PASS without running either control. The code explicitly prints `DENIED=0/0` in this mode. I did not run a full candidate C1=PASS; this is a directly observed scoring-path defect, not a claim that current r55 passes.

### Medium — timeout is not uniformly converted to a leg failure
`run_builder` has timeout values, but most callers do not catch `subprocess.TimeoutExpired` (notably EMPTY_OK/REBUILD_OK, FOREIGN, SYMLINK legs, FAT_RAW, MANY_QUOTES, ESCAPE_ENTRY). A timeout aborts the counter with traceback rather than a per-leg `FAIL`/final `C1=FAIL`; FIFO and DEVZERO alone catch it. Timeout still exits nonzero, so not a false PASS, but the promised per-leg result/diagnostic is broken. Timeout behavior was source-inspected, not exercised.

## Verification / limits
- Scratch-only helper probes exercised FOREIGN, ESCAPE_ENTRY, SAFE extra-file, and SYMLINK_OUT scoring conditions; exact outputs above. They are minimal reproductions of the frozen counter logic, not a run of the full C1 battery.
- Full C1 candidate run and timeout execution: **unrun**. No source bytes were intentionally changed. One edit tool call accidentally targeted the lane counter while attempting to patch scratch; it was immediately reverted, and counter SHA + lane porcelain were checked clean afterward. Scratch mirror only was patched.
- Scratch used only `/fast/scratch/hyaku/chousa-r58/R58ReviewC1Counter/`; removed before yield.

VERDICT: FOREIGN partial deletion, escaped-write acceptance, extra-span acceptance, SYMLINK_OUT reason bypass, and omitted-control vacuity survive as concrete C1 counter defects; timeout reporting is broken but not demonstrated as a false PASS. Full candidate verdict remains unrun.