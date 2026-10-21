# FMutateC1Killed — round26 attempt1, C1 reader sensitivity

## Result

**KILLED, with exact restoration.** Restoring only the base reader's whole-snapshot line-array materialization in an isolated copy caused the same 256 KiB resource detector to change from **exit 0 → exit 1 → exit 0** on pristine, mutated, and restored bytes. The mutant completed both metadata commands with the expected outputs and exits; this is an RSS failure, **not a syntax-error kill**.

Axes named: **calibration** (does a real allocation regression produce a nonzero detector result?), **operability** (peak RSS increment measured in KiB against input bytes), **semantic non-harm** (same metadata outputs/exits on these two fixtures), and **isolation/reproducibility** (immutable target, one private mutation, byte-exact restoration).

This is author-lane mutation evidence only, not admission, integration, an outside judge, citation truth, or a universal resource-bound claim. No finding against the pristine target was produced by this assigned probe.

## Immutable identity and scope

- Claim base: `ba3333254dd337658a4f25e7a9471f9cf4e4567e`.
- Target from `corpus/evidence/round26-measured-revision.json`: `0e9784bd52eca456b24d0bc40921480a47f91a2b`.
- Lane HEAD observed once, before extraction: `0e9784bd52eca456b24d0bc40921480a47f91a2b`; both supplied revisions resolved to their exact commit IDs. No later moving tree was graded.
- Private archive root: `/tmp/chousa-r26-falsify-FMutateC1Killed-nxRpL7` (called **S** below).
- The production lane gate was never edited. The only production write is this report. No lane index, jj state, fleet state, routing, config, or sibling source was changed.
- Base gate was extracted under `S/base/` for source comparison only; it was not executed. `S/pristine/` retains the target gate independently of the mutated location.
- Read the claim file and `corpus/QUALITY.md` first, plus the measured-revision manifest and mandatory agent tooling rules. The detector takes the registered C1 allowance, `extra_rss_bytes > 8 * input_bytes`, without changing its unit or inequality.

### Observed immutable input SHA-256 values

`sha256sum` in S exited 0; every value below equals the corresponding manifest input hash. This verifies the archived inputs, not the moving lane working tree.

| Input | SHA-256 |
| --- | --- |
| `tools/research-gate.sh` | `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6` |
| `corpus/evidence/round26-measure.sh` | `b51c96f63a36bfe0bce96f90be26c931d9f6d2d85169c237cd1dcb23fc6dfb53` |
| `corpus/evidence/round26-claims.md` | `dcbe2b5f12415b7d3828d149e2295bdeb492b712a0f896a9907d56e01f507f1c` |
| `corpus/evidence/round26-date-differential.sh` | `bb8f7f44871b1ac52d3da1f85d6d314aee77490315b566b382788d94ada1f5e7` |
| `corpus/evidence/round26-registry-oracle.py` | `6b2d135c01a8f41b914fb248af35567828336a1a69190560c5df4a07b40f1d78` |
| `corpus/evidence/round26-registry-differential.sh` | `852a764870f71e7247005f2b91d6864cbe0ba6527098f2c35536466117e676e9` |
| `corpus/SOURCES.md` | `8308e6291bdd0c1896bb5d72095696ff491f7f3d748c1b28ed13e9c2c78a5aa9` |
| `corpus/QUALITY.md` | `2428baaf8ddc8fe3b8f08eff0865563dc4c1c08489b86bb4a8d6ba860327dce6` |
| `SKILL.md` | `ee2179753af34d9777537f9ce8cbbd9ddf19cd28e59c544590a5f8b5e1e9958f` |
| `corpus/README.md` | `9def6469ad4078446db03e76641ddab7be353de4f10848665824cf89daf7cc8b` |
| `corpus/knowledge/reader-allocation-r26.md` | `cc653b0fe48f1d5a0f3efa2d61d1e1134d87a36fd67d799f70e07ab963bf5325` |
| `corpus/knowledge/recheck-due-r26.md` | `a0995b7814ddae2a2edf8e25f785de065af674efbb8a337a655feac4c82c7d5e` |
| `corpus/knowledge/registry-link-r26.md` | `248224a270481c49a7fc8a2aaf4b4edf36e061fbea8cc35d3fd715e8f0886d29` |

## Mutant and expected detector

Behavior-bearing target: `verify_metadata`, target lines 2540 and 2627–2682. Reintroduce the base `lines=(); while read ...; lines+=(...)` snapshot materialization and iterate that array instead of streaming directly from the existing snapshot. The CR stripping moves into the materialization loop, exactly as at base lines 2383–2387. No fd acquisition, byte cap, refusal, metadata rule, opt-in flag, or output formatting was changed.

The retained detector is `S/c1-resource-detector.py`, SHA-256 `481058d22e80808e9739bfdc13d218eb6b32dd900f20813e686b0a71eaaf8e1b`. It was written once before the baseline and remained unchanged through all three runs.

Fixtures, also unchanged through all runs:

| Fixture | Exact bytes | SHA-256 |
| --- | --- | --- |
| `S/c1-fixtures/ctl.md` | 67; four LF-terminated lines shown below | `b8073aca3cd9d25926e9162515a6b902857bda8923e769e13ce392978d2aa0aa` |
| `S/c1-fixtures/s1-newlines.md` | 262144 copies of byte `0a` | `e19b72b4c5627342f83de28b77f0ce9f897d233228d833d1ff58d07a241e3836` |

Control bytes are `b"source: S001 fixture\nverified-at: 2026-10-21 checked\nrecheck: 90d\n\n"`.

For each fixture the detector starts a fresh Python measurement worker, which runs `bash S/tools/research-gate.sh verify-metadata FILE --root S/c1-fixtures` with a 30-second timeout and records `resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss`. On this Linux host the unit is KiB. This fresh-worker method follows the existing registered probe's resource measurement approach. Elapsed time uses `time.monotonic()`; no elapsed-time improvement is claimed.

Before deciding the resource result, the detector requires both expected CLI exits (control 0; newline-only 1), the expected META state, finding IDs, complete/final summaries, a gate banner, no timeout, and empty stderr. A semantic/exit/stderr mismatch is **inconclusive, exit 2**, never a resource kill. Only after those checks pass does extra RSS exceeding `8 * 262144 = 2097152` bytes cause detector exit 1. The headerless fixture's three absence warnings and CLI exit 1 are the intended negative control, not a target regression.

## Observed triptych

All runs used exactly `python3 c1-resource-detector.py` with cwd S. The initial baseline command first ran `python3 c1-resource-detector.py --prepare` (exit 0) and then that same detector. Each gate command completed normally, had empty stderr, and returned the expected control/dense exits 0/1.

| State | Control RSS KiB | Dense RSS KiB | Extra KiB | Extra bytes | Control / dense elapsed seconds | Detector exit |
| --- | ---: | ---: | ---: | ---: | --- | ---: |
| Pristine | 17224 | 17416 | 192 | 196608 | 0.011536 / 2.782534 | 0 |
| Mutant | 17212 | 75184 | 57972 | 59363328 | 0.011529 / 2.773334 | 1 |
| Restored | 16916 | 17432 | 516 | 528384 | 0.011078 / 2.760180 | 0 |

Actual resource-result output:

```text
# pristine
RESOURCE extra_kib=192 extra_bytes=196608 allowance_bytes=2097152
PASS C1_RESOURCE_BOUNDED: normalized metadata semantics intact; RSS increment within the declared byte-scaled allowance
# mutant
RESOURCE extra_kib=57972 extra_bytes=59363328 allowance_bytes=2097152
FAIL C1_RESOURCE_AMPLIFIED: extra_rss_bytes=59363328 > 8 * input_bytes=2097152
# restored
RESOURCE extra_kib=516 extra_bytes=528384 allowance_bytes=2097152
PASS C1_RESOURCE_BOUNDED: normalized metadata semantics intact; RSS increment within the declared byte-scaled allowance
```

Output equality on these fixtures was observed, not assumed. Removing only the first banner/timestamp line gives the same hashes in all three runs:

- Control: `bbf2288e9145ff010cee12353f0c4e6479782b854c06cc18f5b80eefa1df79ba`.
- Dense: `b045d92941c4e2448b188325ec3e3b39a0613fd65c2abf2a789785742b82f7e2`.

Baseline gate banners were timestamped `2026-10-21T12:59:12Z`; mutant banners `2026-10-21T12:59:41Z`; restored banners `2026-10-21T12:59:44Z`. All carried the same version, mode, paths and roots as the raw mutant output below. All three runs printed `SEMANTICS ctl.md PASS expected_rc=0` and `SEMANTICS s1-newlines.md PASS expected_rc=1`; no stderr or timeout was observed.

## Exact mutation delta

Actual `diff -u pristine/tools/research-gate.sh tools/research-gate.sh` output, cwd S, exit 1 because differences existed; stderr empty:

```diff
--- pristine/tools/research-gate.sh	2026-10-21 09:48:28.000000000 -0300
+++ tools/research-gate.sh	2026-10-21 09:59:21.955023531 -0300
@@ -2537,7 +2537,7 @@
   local canon refuse fsize links meta_fd fdpath fdcanon probe content read_rc
   local registry_root entry_path
   local LC_ALL=C
-  local -a files=() candidates=() metadata_lines=()
+  local -a files=() candidates=() metadata_lines=() lines=()
   local had_nullglob=0 candidate
   local ROOT_PARENT_RE='(^|[^[:alnum:]_-])--root[[:space:]]+\.\.($|[^[:alnum:]_./-])'
 
@@ -2624,12 +2624,17 @@
       metadata_lines+=("META entry=$base source=refused verified_at=refused recheck=refused${freshness_fields} verdict=drift")
       continue
     fi
+    lines=()
+    while IFS= read -r line || [[ -n $line ]]; do
+      line=${line%$'\r'}
+      lines+=("$line")
+    done <<<"$content"
+
     fence_char='' fence_len=0 active_key=''
     has_source=0 has_verified=0 has_recheck=0
     if ((REGISTRY_ARG_SET)); then source_value=''; fi
     verified_value='' recheck_value=''
-    while IFS= read -r line || [[ -n $line ]]; do
-      line=${line%$'\r'}
+    for line in "${lines[@]}"; do
       if [[ $line =~ ^[[:space:]]*$ ]]; then active_key=''; fi
       if [[ -n $fence_char ]]; then
         case "$active_key" in
@@ -2679,7 +2684,7 @@
         verified-at) verified_value+=$'\n'"$line" ;;
         recheck) recheck_value+=$'\n'"$line" ;;
       esac
-    done <<<"$content"
+    done
 
     recheck_first=''
     entry_drift_start=$N_DRIFT
```

## Raw mutant failure output

Actual detector stdout follows in full. Command `python3 c1-resource-detector.py`, cwd S, exit 1; detector stderr was `''`.

```text
DETECTOR gate_sha256=8c626f0add4181dcaaf4a4432000a9f03ba2554128e52850b6918cb426bf44b8 detector_sha256=481058d22e80808e9739bfdc13d218eb6b32dd900f20813e686b0a71eaaf8e1b
BOUND input_bytes=262144 allowance_bytes_per_input_byte=8 child_timeout_s=30
FIXTURE ctl.md bytes=67 sha256=b8073aca3cd9d25926e9162515a6b902857bda8923e769e13ce392978d2aa0aa
COMMAND ["bash", "/tmp/chousa-r26-falsify-FMutateC1Killed-nxRpL7/tools/research-gate.sh", "verify-metadata", "/tmp/chousa-r26-falsify-FMutateC1Killed-nxRpL7/c1-fixtures/ctl.md", "--root", "/tmp/chousa-r26-falsify-FMutateC1Killed-nxRpL7/c1-fixtures"]
CASE ctl.md rc=0 maxrss_kib=17212 elapsed_s=0.011529 timeout=False
STDOUT ctl.md BEGIN
research-gate v2 — ts=2026-10-21T12:59:41Z — mode=verify-metadata — path=/tmp/chousa-r26-falsify-FMutateC1Killed-nxRpL7/c1-fixtures/ctl.md — root=/tmp/chousa-r26-falsify-FMutateC1Killed-nxRpL7/c1-fixtures
META entry=ctl.md source=present verified_at=dated recheck=scheduled verdict=clean
METADATA_COMPLETE=1/1
RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)
STDOUT ctl.md END
STDERR ctl.md ''
NORMALIZED_SHA256 ctl.md bbf2288e9145ff010cee12353f0c4e6479782b854c06cc18f5b80eefa1df79ba
SEMANTICS ctl.md PASS expected_rc=0
FIXTURE s1-newlines.md bytes=262144 sha256=e19b72b4c5627342f83de28b77f0ce9f897d233228d833d1ff58d07a241e3836
COMMAND ["bash", "/tmp/chousa-r26-falsify-FMutateC1Killed-nxRpL7/tools/research-gate.sh", "verify-metadata", "/tmp/chousa-r26-falsify-FMutateC1Killed-nxRpL7/c1-fixtures/s1-newlines.md", "--root", "/tmp/chousa-r26-falsify-FMutateC1Killed-nxRpL7/c1-fixtures"]
CASE s1-newlines.md rc=1 maxrss_kib=75184 elapsed_s=2.773334 timeout=False
STDOUT s1-newlines.md BEGIN
research-gate v2 — ts=2026-10-21T12:59:41Z — mode=verify-metadata — path=/tmp/chousa-r26-falsify-FMutateC1Killed-nxRpL7/c1-fixtures/s1-newlines.md — root=/tmp/chousa-r26-falsify-FMutateC1Killed-nxRpL7/c1-fixtures
META entry=s1-newlines.md source=absent verified_at=absent recheck=absent verdict=drift
FINDING META_SOURCE_ABSENT severity=warn surface=metadata obs=entry=s1-newlines.md key=source absent
FINDING META_VERIFIED_AT_ABSENT severity=warn surface=metadata obs=entry=s1-newlines.md key=verified-at absent
FINDING META_RECHECK_ABSENT severity=warn surface=metadata obs=entry=s1-newlines.md key=recheck absent
METADATA_COMPLETE=0/1
RESEARCH_GATE: DRIFT (entries=1 complete=0 findings=3 drift=3)
STDOUT s1-newlines.md END
STDERR s1-newlines.md ''
NORMALIZED_SHA256 s1-newlines.md b045d92941c4e2448b188325ec3e3b39a0613fd65c2abf2a789785742b82f7e2
SEMANTICS s1-newlines.md PASS expected_rc=1
RESOURCE extra_kib=57972 extra_bytes=59363328 allowance_bytes=2097152
FAIL C1_RESOURCE_AMPLIFIED: extra_rss_bytes=59363328 > 8 * input_bytes=2097152
```

## Exact commands and exits

Commands below are the executed shell/process commands, in their stated cwd. `functions.read`, `functions.grep`, `functions.glob`, `functions.write` and `functions.edit` were used for scoped inspection, detector creation, and the displayed mutation, not shell-based source edits.

### Revision/setup (cwd `/home/vgpnk/Projects/shokunin` unless noted)

```sh
# exit 0; stdout HEAD, target, base in that order:
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse HEAD '0e9784bd52eca456b24d0bc40921480a47f91a2b^{commit}' 'ba3333254dd337658a4f25e7a9471f9cf4e4567e^{commit}'
# exit 0; stdout /tmp/chousa-r26-falsify-FMutateC1Killed-nxRpL7:
mktemp -d /tmp/chousa-r26-falsify-FMutateC1Killed-XXXXXX
# exit 0; no stdout:
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 0e9784bd52eca456b24d0bc40921480a47f91a2b | tar -x -C /tmp/chousa-r26-falsify-FMutateC1Killed-nxRpL7
```

Commands with cwd S:

```sh
# exit 127; raw failure text: error: command not found: /usr/bin/time
/usr/bin/time --version
# exit 0; GNU bash, version 5.3.20(1)-release (x86_64-pc-linux-gnu):
bash --version
# exit 0; no stdout:
mkdir /tmp/chousa-r26-falsify-FMutateC1Killed-nxRpL7/base && git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive ba3333254dd337658a4f25e7a9471f9cf4e4567e tools/research-gate.sh | tar -x -C /tmp/chousa-r26-falsify-FMutateC1Killed-nxRpL7/base
# exit 0; hashes in input table above:
sha256sum tools/research-gate.sh corpus/evidence/round26-measure.sh corpus/evidence/round26-claims.md corpus/evidence/round26-date-differential.sh corpus/evidence/round26-registry-oracle.py corpus/evidence/round26-registry-differential.sh corpus/SOURCES.md corpus/QUALITY.md SKILL.md corpus/README.md corpus/knowledge/reader-allocation-r26.md corpus/knowledge/recheck-due-r26.md corpus/knowledge/registry-link-r26.md
# exit 0; no stdout:
mkdir /tmp/chousa-r26-falsify-FMutateC1Killed-nxRpL7/pristine && git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 0e9784bd52eca456b24d0bc40921480a47f91a2b tools/research-gate.sh | tar -x -C /tmp/chousa-r26-falsify-FMutateC1Killed-nxRpL7/pristine
# exit 0; both preparation and pristine detector completed:
python3 c1-resource-detector.py --prepare && python3 c1-resource-detector.py
# Then functions.edit applied the exact mutation above.
# exit 1, expected diff result, not a detector:
diff -u pristine/tools/research-gate.sh tools/research-gate.sh
# exit 1, expected RSS detector failure, raw stdout above:
python3 c1-resource-detector.py
```

The measurement worker subprocess commands are the two exact `COMMAND` arrays in the raw output; all three states executed those same arrays with exits 0 and 1. Each worker was started by the detector with `sys.executable` (`/usr/bin/python`), the absolute detector path, `--peak`, and the corresponding fixture basename, and each worker itself exited 0.

### Restoration (cwd S)

Restoration was in the mutation execution cell's `finally` block, before the restored run. These were two direct subprocess calls, not a rerun of a moving working-tree copy:

```sh
# exit 0; captured stdout was a 276480-byte archive; stderr empty:
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 0e9784bd52eca456b24d0bc40921480a47f91a2b tools/research-gate.sh
# exit 0; stdin was exactly that captured archive; stdout/stderr empty:
tar -x -C /tmp/chousa-r26-falsify-FMutateC1Killed-nxRpL7
# exit 0; stdout/stderr empty, proving exact equality with retained pristine bytes:
cmp -s pristine/tools/research-gate.sh tools/research-gate.sh
# exit 0; hashes listed below:
sha256sum pristine/tools/research-gate.sh tools/research-gate.sh c1-resource-detector.py c1-fixtures/ctl.md c1-fixtures/s1-newlines.md
# exit 0; restored detector, same script and fixtures:
python3 c1-resource-detector.py
```

Observed gate SHA-256 sequence:

```text
pristine c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6
mutated  8c626f0add4181dcaaf4a4432000a9f03ba2554128e52850b6918cb426bf44b8
restored c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6
```

The separate retained pristine file, restored file, detector, and both fixtures were all hashed in the post-restoration command. Detector and fixture hashes remained exactly those registered above. `cmp` exit 0 is the exact-byte restoration evidence, not merely matching output.

## Tooling and limits

- Bash: observed GNU Bash `5.3.20(1)-release`.
- Python: observed via successful Python Eval, executable `/usr/bin/python`, version `3.14.8 (main, Oct 2 2026, 10:23:31) [GCC 16.2.1 20260810]`.
- GNU `/usr/bin/time` was unavailable (exit 127, reported above). RSS instead used the already-available Python standard-library method also used by the registered probe. No install or update was required or performed; no pacman transaction occurred.
- Exactly one defect and one pristine/mutant/restored triptych were exercised. No background jobs, subagent dispatch, other agent runtime, full selftest/build/lint/formatter, 8 MiB amplification probe, frozen29 hold run, or C2/C3 behavioral check was run.
- This 256 KiB newline-only observation demonstrates sensitivity to the original array-allocation defect. It does not replace the registered four-shape 8,388,000-byte population, establish every refusal/flag/fixture invariant, or infer a universal RSS/time bound. The small-control output comparison likewise does not substitute for the frozen29 legacy-output hold.

Report: .ufo/waves/round-26/falsify/FMutateC1Killed.md
