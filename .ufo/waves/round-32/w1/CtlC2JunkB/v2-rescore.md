# CtlC2JunkB — design v2 re-score supplement

Axes: **coverage (C2)**; C1 operability was not exercised. Read `claims.md:119-189` and the frozen v2 counter before scoring. Re-scored all ten previously built controls, two fresh seeds each: **all MISSES** against **132/132**. No oracle was built by this seat.

## Provenance and isolation

Counter: `corpus/evidence/round32/c2-count-v2.py`, SHA-256 `8ec1a1ed44f1d3971a73eeace677cbedd0187563bea063ec6b680261dbb23c8a`. Both `timeout 15s sha256sum <counter>` and `timeout 15s git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show 3d586d3a:corpus/evidence/round32/c2-count-v2.py | timeout 15s sha256sum` completed with exit 0 and that hash.

Scratch root `S=/fast/scratch/hyaku/chousa-r32/w1/CtlC2JunkB`. Each preserved mutation was copied with `timeout 15s cp S/<control>-gate.sh S/<control>/tools/research-gate.sh` (all exit 0), then checked using `timeout 15s sha256sum S/<control>/tools/research-gate.sh` (all exit 0). Every hash equals its prior mutated hash and differs from pristine `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258`; no rebuild or mutation change was needed.

All three temp variables point to `S/tmp-v2`, a sibling of, never a descendant of, every gate lane root `S/<control>`. Receipts are `v2/<control>-a.json` and `v2/<control>-b.json` relative to this supplement. All 20 receipts contain the frozen counter hash, `record_fails=[]`, `gate_rc=1`, `gate_timed_out=false`, and `predicate_holds=false` (each receipt, lines 3-15).

## Scores

All counts are EXEMPT_AUDIT_MATCH; every run printed `RECORD_CHECKS=ok` and exited 1.

| Control | Gate SHA-256 | Seed a | Count a | Seed b | Count b | Verdict |
|---|---|---:|---:|---:|---:|---|
| random-labels | `a7011a17644cae50baa604f9c3ae947bab3bb7330c7fc7aeff8341d60ae14871` | 6713176512024632992 | 52/132 | 6770075352110321566 | 51/132 | MISSES |
| hop-id-shape | `a4a1dcee4899c5800275bcaee98f76e60fa14b2916a6318c0881e871df1beb22` | 6815698895717200809 | 60/132 | 7237677628822260743 | 60/132 | MISSES |
| filename-shape | `bae7fd1ca83a7ac3826d7467843199475a4c951487bc35a82387b86c5156d900` | 5692620384786084353 | 66/132 | 7939127137197556767 | 66/132 | MISSES |
| declared-id-shape | `0ec9610bc73b732e695ecd2e837464a8680c319630daac374b4b762fcb63bbf8` | 6792020904587719928 | 102/132 | 1783251456138370436 | 102/132 | MISSES |
| declared-id-member | `2dccb4acb10f4583a273d6d7c85e4ebe22b699f1c70b0d32884d4c18ee9997da` | 3444278613095354598 | 108/132 | 166434474565805923 | 108/132 | MISSES |
| generator-union | `88852cc897b2eb142b7c1c8773b8437dbd05d39c20dac85bbdfdedbab708bd73` | 3246261062914160438 | 120/132 | 1412508647525615616 | 120/132 | MISSES |
| row-position | `5a517c0d6e158b5a003b34d947a6965a6e947ea0418582799c3e370be9ebe170` | 863102780447560975 | 86/132 | 8601824872160893070 | 85/132 | MISSES |
| notes-shape | `f22d023965d8e51acc0687b4ead010fd856d7498da491c591fe74c47531c96d9` | 4442117691371665969 | 60/132 | 5215796560769997860 | 60/132 | MISSES |
| from-shape | `6793d7398137a3c18f32f27c7d1133d0fb1198b105ef2b815f2bfbd9543a6af8` | 5040433658655542761 | 60/132 | 4268520402032966507 | 60/132 | MISSES |
| random-valid-labels | `34de75569d9e8bac02aa443c2f6071df2744a61456154774dfa91974f00a862f` | 10009108506242637 | 87/132 | 4688499289112357407 | 83/132 | MISSES |

## Evidence and interpretation

Exact commands, cwd, exit codes, all per-trial/per-class lines, RECORD_CHECKS lines, and receipt paths: `v2/counter-commands-output.txt` (25,164 bytes; SHA-256 `00b017082c9e9c9bb939ea165b59e9a4b5e9ff9de4d744474c7e74f5a9c1a5b4`). Commands use:

```text
timeout -k 5s 700s prlimit --as=1073741824 --nproc=16384 env C1_TMP=S/tmp-v2 C2_TMP=S/tmp-v2 TMPDIR=S/tmp-v2 python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c2-count-v2.py --gate S/<control>/tools/research-gate.sh --seed <seed> --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/CtlC2JunkB/v2/<control>-<a|b>.json
```

The log expands every S/placeholder to its actual value. Cwd was the lane root. Up to six finite commands ran concurrently; all completed and were awaited.

**Strongest counterexample attempt:** generator-union scored 120/132 twice, not 132/132. It still gets R1 and R3 12/12 without reading U source content, and R2 0/12; E11/E12 remain correctly exempt (`v2/generator-union-a.json:17-32`, same fields in the b receipt). Example miss: hop hca2ceef6, truth=resolvable, observed=exempt (`v2/generator-union-a.json:35-39`). Format/declaration correlation remains visible in `c2-count-v2.py:205-215,237-238`, but the full frozen target rejects this shortcut. No MEETS-TARGET control was found.

**Smallest safe correction:** no counter or claim reinterpretation is warranted from these misses. Preserve the full target and require actual resolved-equivalent citation reading; for a future independently versioned fixture, negative fragment/declared-id twins would remove the surviving partial R1/R3 format correlation. This is not an admission judgment.

Limits: only these ten controls/two seeds each; random controls additionally use independent Bash RANDOM. No candidate, C1 counter, selftest, round-31 test, production edit, or counter edit. No installs, network access, subagents, or background jobs. `timeout 15s df -h /fast` exited 0 (231G available); `timeout 15s stat -c '%n %s' <v2-artifacts>/*` exited 0 (largest existing artifact 25,164 bytes; largest receipt 10,359 bytes). All artifacts are under 1 MiB.
