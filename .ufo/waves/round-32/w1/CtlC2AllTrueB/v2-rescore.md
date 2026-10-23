# CtlC2AllTrueB — design v2 re-score

Axes: operability and coverage. Read `corpus/evidence/round32/claims.md:119-189` and the frozen v2 counter contract. Re-scored every control built by this seat, two fresh seeds each. **All three MISSES; none meets 132/132.**

Counter `corpus/evidence/round32/c2-count-v2.py` SHA-256: `8ec1a1ed44f1d3971a73eeace677cbedd0187563bea063ec6b680261dbb23c8a`. It matched the output of `timeout 30s git show 3d586d3a:corpus/evidence/round32/c2-count-v2.py | timeout 30s sha256sum` (exit 0). No counter was edited.

The retained mutated gates still had their original hashes, all different from pristine base `0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258`; no rebuild was needed. Copied each to `/fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB/<control>/tools/research-gate.sh`. `C1_TMP`, `C2_TMP`, and `TMPDIR` all pointed to the sibling directory `/fast/scratch/hyaku/chousa-r32/w1/CtlC2AllTrueB/v2-tmp`, outside all three gate lane roots. Relocated gate hashes were observed with `timeout 30s sha256sum` on the three exact gate paths (exit 0), and are bound in every receipt.

| Control directory / behavior | Gate SHA-256 | Fresh seeds | EXEMPT_AUDIT_MATCH, in seed order | Verdict |
|---|---|---|---|---|
| `control-a` / flag U with parseable citation; no source read | `2c45d74e4542fb1de481265a4a1e3265e27f17f55752566cf3fe29dc2ef631fa` | 67593827045223011, 67593827045223029 | 66/132, 66/132 | **MISSES** |
| `control-b` / same for all exempt statuses, including judgment statuses | `36e2326f8e7291272169df2861a576776a61285c6871f03e9e254f96ea62ecc8` | 67593827045223107, 67593827045223119 | 54/132, 54/132 | **MISSES** |
| `control-c` / flag U with non-empty `to`; no citation parse/read | `43c0ef8833e27ec02f2c04394f6c443a85e7e42fa5b67a8f98fc7734a5ba72e9` | 67593827045223203, 67593827045223221 | 60/132, 60/132 | **MISSES** |

All six stdout streams printed **`RECORD_CHECKS=ok`**. Each counter exited **1**; each gate exited **1**, without timeout. All receipts have `record_fails=[]` and `predicate_holds=false` (lines 2–15), with every per-class result at lines 16–33. E11 and E12 each scored 0/6 in every run; the controls still falsely declare nonmatching anchors resolvable. These are coverage defects, not record-check or layout failures. As in the original report, the smallest safe correction is actual resolved-path source/boundary/anchor verification for U, preserving judgment exemptions.

Evidence, relative to this report's directory:

- Receipts: `v2/a-s67593827045223011.json`, `v2/a-s67593827045223029.json`, `v2/b-s67593827045223107.json`, `v2/b-s67593827045223119.json`, `v2/c-s67593827045223203.json`, `v2/c-s67593827045223221.json`.
- Exact six executed command lines and exit status: `v2/commands.txt` (3742 bytes).
- Complete observed count, RECORD_CHECKS, and per-class lines for every run: `v2/counter-stdout.txt` (3069 bytes).

All six foreground calls completed, bounded by `timeout --kill-after=5s 720s`, with `prlimit --as=1073741824 --nproc=2000 --fsize=1048576`. Before setup, `timeout 30s df -h /fast` exited 0 and showed 231G available (72% used). No background jobs, candidates, production changes, no-harm battery, counter edits, installs, or network access. The original v1 report was not rewritten.
