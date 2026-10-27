# R58CritC1Symlink — build-spans symlink containment attack

## Scope and tested artifact
- Read frozen `corpus/evidence/round58/claims.md` (C1 claim, §C1) and exact frozen `c1-count.py`; freeze `9e73a031ab1ac3bac343de008850d7d87f9e5634` is present in lane history. Frozen claim covers symlinked output/cache *inputs* and writes contained under `--out`; it does not state race-hardening.
- The checked-out `tools/build-spans.py` is pinned round-55 SHA-256 `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`, not the hardened candidate. Tested scratch-only proposed candidate `/fast/scratch/hyaku/chousa-r58/R58ExecC1Atomicity/proposed/build-spans.py`, SHA-256 `5474ecc33ea2e9bda0067ddbdcc15419b8c1c223da7828d3bc8ecd5fda1c92cb`; copied with pinned `capture-text.py` and frozen counter to my scratch. No lane/source writes.
- Scratch: `/fast/scratch/hyaku/chousa-r58/R58CritC1Symlink/`.

## Counter result
Command:
```sh
cd /fast/scratch/hyaku/chousa-r58/R58CritC1Symlink && env TMPDIR=/fast/scratch/hyaku/chousa-r58/R58CritC1Symlink python3 -B c1-count.py --builder /fast/scratch/hyaku/chousa-r58/R58CritC1Symlink/build-spans.py --work /fast/scratch/hyaku/chousa-r58/R58CritC1Symlink/counter
```
Observed (exit 1):
```text
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
BEFORE_FOREIGN=absent
DENIED=0/0
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=absent DENIED=0/0
C1=FAIL
```
This scratch copy lacks the frozen counter's sibling `controls/build-spans-r55.py`, so integrity leg is `absent`; this does not establish a frozen-counter PASS. Safe/refusal legs themselves printed pass.

## Symlink attacks
Fixture driver: `python3 -B probe.py` from the scratch directory with `TMPDIR` explicitly set there. Each probe used a unique quote in a tiny local `.txt` fixture; no external data/fetches. Exact observations:
```text
parent-out-symlink: rc=0 stderr='' stdout='QUOTE S501 char 12 spans/S501-1.txt\nSPANS_ROWS=1 WRITTEN=1'
parent target entries: ['out']
spans-dir-symlink: rc=1 stderr='build-spans: refused /fast/scratch/hyaku/chousa-r58/R58CritC1Symlink/spans-dir/out/spans is a symbolic link (SYMLINK)' stdout=''
spans target entries: []
span-leaf-symlink: rc=0 stderr='' stdout='QUOTE S501 char 12 spans/S501-1.txt\nSPANS_ROWS=1 WRITTEN=1'
victim: b'VICTIM_SENTINEL\\n'
raw-symlink: rc=1 stderr='build-spans: refused S501: SYMLINK capture 73b85c2e50cd194797002dbf.raw is a symbolic link' stdout=''
raw target unchanged: b'\\xd0\\xcf\\x11\\xe0\\xa1\\xb1\\x1a\\xe1'
cache-dir-symlink: rc=0 stderr='' stdout='QUOTE S501 char 12 spans/S501-1.txt\nSPANS_ROWS=1 WRITTEN=1'
cache target output elsewhere? ['spans', 'spans.tsv']
```
Interpretation: `--out` symlink itself is refused by candidate code (also frozen leg); but an ancestor symlink is not checked: candidate followed `alias -> external` and created `external/out`, escaping the lexical `--out` tree. This is a confirmed write escape. A symlinked `out/spans` destination is refused before touching its target. A symlink at the intended span *leaf* did not modify its target: staging + `os.replace` replaced the link itself. A symlinked `.raw` is refused. A symlinked cache directory is followed (`cache.is_dir()` and path traversal) and accepted, reading outside the specified cache; this probe writes only in the separate output. Thus candidate refusal contains writes for the raw-link/spans-dir probes, but not the parent-dir-symlink case (accepted build/escape).

## Assessment
- Counter is not proof of containment against parent-directory symlinks: it tests only the final `--out` symlink and cache *file* symlink. Candidate's leaf guard is inadequate for parent components; cache-directory link traversal also remains accepted. The frozen claim is about generated writes, so the confirmed parent-link escape is directly relevant to operability; cache-directory reading is an additional boundary question, not itself an observed write escape.
- Smallest safe correction: reject symlink components of the resolved `--out` path (including existing ancestor components) before any writes, or anchor output operations to a safely opened directory descriptor; apply equivalent explicit root policy to cache if cache-root symlinks are forbidden. Add separate frozen-independent regressions for ancestor-link output and cache-root symlink rather than widening/altering the frozen predicate.
- Impacted axis: operability (C1); candidate is not safe to accept on containment grounds until parent-link escape is closed. No judgment on C2.

VERDICT: FALSIFIED — scratch proposed builder `5474ecc3` escapes `--out` through a symlinked parent (`alias/out` created under the external target); output-leaf and raw/span-directory symlink probes survive/refuse as described.
