# R58ExecC1PathContainment — C1 `--out` path traversal / symlink-parent escape

**Scope.** Probe `--out` path traversal and symlink-parent escape in a scratch clone; decide whether the frozen
counter's containment wording is operationally testable; propose the smallest guard. Read-only: the frozen `claims.md`, `c1-count.py`, `tools/build-spans.py`. Freeze `9e73a031ab1ac3bac343de008850d7d87f9e5634`; claim base `b13ca7b5c8bbb40d2d29a37fb443c64ca043f791`.
```
$ git show 9e73a031ab1ac3bac343de008850d7d87f9e5634:corpus/evidence/round58/c1-count.py | sha256sum
65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f  -   (= working tree)
$ sha256sum tools/build-spans.py  ->  1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6
```
Scratch (one clone; every fixture and every symlink/leak target inside it; removed before yielding): `/fast/scratch/hyaku/chousa-r58/R58ExecC1PathContainment/` — `clone/` (lane clone at `718e8d2`), `cand/` (scratch candidates), `probe_escape.py`, `probe_containment_reach.py`, `counter-casefixed/` (counter copy, one token changed). No lane file written; `git status --porcelain` → only `?? .ufo/waves/round-58/`. No fetch/install.

## 1. Base builder: the `--out` surface is uncontained
`tools/build-spans.py:193` takes `--out` as a bare path; `:202-208` then `mkdir`, `unlink`, `write_bytes` through it. No `is_symlink`/`lstat`/`os.open` anywhere in the file. `python3 probe_escape.py --builder <scratch>/clone/tools/build-spans.py --root <scratch>/probe-root-base`

| leg | fixture | base builder result |
|---|---|---|
| P1 | `--out` is a symlink → `p1-real` | `rc=0`; wrote `p1-real/spans.tsv` + `spans/S501-1.txt` **through the link** |
| P2 | `--out`'s **parent** is a symlink (`p2-link`→`p2-target`) | `rc=0`; wrote `p2-target/out/spans.tsv` — **outside the `--out` path given** |
| P3 | `--out/spans` is a symlink → `p3-elsewhere` | `rc=0`; wrote `p3-elsewhere/S501-1.txt` and **deleted** `p3-elsewhere/S777-1.txt` (foreign file) via the orphan loop `:203-205` |
| P4 | `--out/spans.tsv` is a symlink → `p4-victim.txt` | `rc=0`; victim content replaced by the manifest header — **arbitrary overwrite outside `--out`** |
| P5 | entry column `../escape.md` | `rc=2`, `entry '../escape.md' must be lane-relative`, nothing written — the one containment input already refused |
```
P2 rc=0 / tree: [… 'L p2-link','D p2-target','D p2-target/out','F p2-target/out/spans/S501-1.txt',…]
P4 rc=0 / victim content now: b'id\turl\tcapture_sha256\toffset\tspan_file\tquote\tentry\nS501\thttps://fixture.example/'
P3 watch …/p3-elsewhere/S777-1.txt: exists=False  <-- foreign file deleted through the link; S501-1.txt exists=True
```
Base builder vs the frozen counter (`--work <scratch>/c1-base`):
```
FOREIGN=fail(rc=0, orphans deleted: foreign gone=True) / SYMLINK_OUT=fail(rc=0, expected refusal)(target-dir-written!)
SYMLINK_CACHE=fail(rc=0, expected refusal)
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2      C1=FAIL      EXIT=1
```
**No frozen leg covers P2, P3 or P4.** `SYMLINK_OUT` (`:226-237`) symlinks `--out` *itself*; nothing symlinks a
**parent** of `--out`, `--out/spans`, or `--out/spans.tsv`.

## 2. Is the containment wording operationally testable? — No; the verdict line is unusable
**2a. `C1=PASS` is unreachable for any builder.** `:51` defines `PASS = "pass"` (lowercase) and every refusal leg
is *emitted* through it (`:160` `f"{name}={PASS}(refused)"`, `:223` `FOREIGN={PASS}(refused)`, `:234` `SYMLINK_OUT={PASS}(refused)`), but the verdict aggregates with an **uppercase** needle: `:391` `ref_pass = all(("=PASS" in l) …)`, `:399` `REFUSE={sum('=PASS' in l …)}`. `"=PASS"` is never a substring of `"NAME=pass(refused)"`, so `ref_pass` is a constant `False` and `verdict` (`:394`) is always `"FAIL"`, exit 1 (`:402`); the safe-leg aggregate `:390` uses lowercase `"=pass"` and works, hence `OK=4/4` beside `REFUSE=0/7`. A scratch candidate satisfying every leg predicate semantically (`cand/build-spans.py`: `--out`/cache symlink, FIFO/device, 64 MiB raw cap, 100 000-row cap, foreign-span refusal before orphan deletion, entry-`..` refusal):
```
EMPTY_OK=pass / REBUILD_OK=pass / FOREIGN=pass(refused) / SYMLINK_OUT=pass(refused) / SYMLINK_CACHE=pass(refused)
FIFO_TXT=pass(refused) / DEVZERO_TXT=pass(refused) / FAT_RAW=pass(refused) / MANY_QUOTES=pass(refused)
ESCAPE_ENTRY=pass(refused) / HELDOUT_OK=pass / BEFORE_FOREIGN=deleted / DENIED=2/2
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2      C1=FAIL      EXIT=1
```
Eleven of eleven legs pass; the verdict is `FAIL`. **No builder patch can print `C1=PASS` under these bytes**; the target "`c1-count.py` must print `C1=PASS` and exit 0" (`claims.md:9`) is unsatisfiable, `C1=FAIL` is not evidence of an unhardened builder, and the do-nothing-control clause is vacuous.
**2b. The containment diff has almost no reach.** `expect_ok` (`:141-146`) diffs `snapshot(out.parent)`
before/after; `snapshot` (`:59-66`) walks `root.rglob("*")` keeping only `p.is_file() and not p.is_symlink()`. Measured with the counter's own functions imported read-only (`probe_containment_reach.py`; before-snapshot at the counter's `:195` position, write planted during the run, after-snapshot at `:142`): S1 plain file inside the snapshot root but outside `--out` → **True**; S2 plain file **outside** the snapshot root → **False**; S3 write
**through a symlinked dir** inside the root → **False**; S4 legitimate write inside `--out` → False (correct); S5
`HELDOUT_OK` shape, `snapshot(work)` taken **after** the run (`:345`) → **False (vacuous)**. `rglob` does not descend into a symlinked dir (verified: `rglob('*')` of a dir holding a symlinked dir → `['link','real', 'real/f.txt']` — the link's contents are not traversed) and `snapshot` skips symlinks. `HELDOUT_OK` also runs with `--cache LANE/corpus/captures` (`:339-341`), the live lane store, outside the snapshot root.
**2c. `SYMLINK_OUT` cannot fail on containment — two inversions.** `expect_refuse`'s `forbidden_touch` names paths
that must **not** be touched, but `:161-164` is `if not p.exists(): return …{FAIL}(… was touched/removed)` — it
**fails when absent, passes when present**:
```
forbidden path exists BEFORE: False  ->  X=fail(…/forbidden.txt was touched/removed)
forbidden path exists AFTER : True   ->  X=pass(refused)
```
For `SYMLINK_OUT` the forbidden path is `realdir/spans.tsv`, which **cannot pre-exist** (fresh empty dir), so a correct refusal is reported as "was touched/removed". Then `:233-236` overwrites the leg — `if not any(real.iterdir()): legs[-1] = f"SYMLINK_OUT={PASS}(refused)"`, else appends `"(target-dir-written!)"`, the only escape signal, **never read by the verdict**. A builder refusing with the correct `SYMLINK` class **and writing through the symlinked `--out`** (`cand/build-spans-escape.py`):
```
SYMLINK_OUT=pass(refused)(target-dir-written!)   /   realdir/spans.tsv = "ESCAPED THROUGH THE SYMLINKED --out"
```
**2d. With the one-token case fix, an escaping builder is credited `C1=PASS`.** In a **scratch copy only**
(`:391`/`:399` lowercased; the lane copy still hashes `65da18bb…`), the builder satisfying every leg semantically
**and** escaping containment through a symlinked `--out` (`cand/build-spans-escape-allpass.py`):
```
EMPTY_OK=pass / REBUILD_OK=pass / FOREIGN=pass(refused) / SYMLINK_OUT=pass(refused)(target-dir-written!)
SYMLINK_CACHE=pass(refused) / FIFO_TXT=pass(refused) / DEVZERO_TXT=pass(refused) / FAT_RAW=pass(refused)
MANY_QUOTES=pass(refused) / ESCAPE_ENTRY=pass(refused) / HELDOUT_OK=pass / BEFORE_FOREIGN=deleted
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=0/0      C1=PASS      EXIT=0   (escape landed: "ESCAPED")
```
The honest candidate (`cand/build-spans.py`, containment closed) also prints `C1=PASS` under the same case-fixed counter — **the two are indistinguishable to the battery.** The case fix is necessary but not sufficient; the containment claim needs its own leg.

## 3. Smallest guard (proposal only — no lane file edited)
23 added lines on the pinned base (byte-diff vs `tools/build-spans.py`; scratch copy `cand/build-spans-minimal.py`): three `lstat`-style checks on the write targets plus an ancestor walk on `--out`, called once before any read or write so nothing is written on refusal.
```
+import os
+def _symlink_ancestor(path):
+    p = pathlib.Path(os.path.abspath(str(path))); cur = pathlib.Path(p.parts[0])
+    for part in p.parts[1:]:
+        cur = cur / part
+        if cur.is_symlink(): return cur
+    return None
+def _guard_out(out):
+    for p in (out, out / "spans", out / "spans.tsv"):
+        if p.is_symlink():
+            print(f"build-spans: refused SYMLINK: {p} is a symlink", file=sys.stderr); sys.exit(1)
+    link = _symlink_ancestor(out)
+    if link is not None:
+        print(f"build-spans: refused SYMLINK: {link} (a parent of --out) is a symlink", file=sys.stderr)
+        sys.exit(1)
+    # call site: in main(), immediately before `rows = read_quotes(...)`:
+    #     _guard_out(out)
```
The three checks cover the three write targets; the ancestor walk covers P2. `SYMLINK` is the class the frozen `SYMLINK_OUT` leg greps (`:232`). Verified against `probe_escape.py`:
```
--- P1_OUT_SYMLINK ---      rc=1  build-spans: refused SYMLINK: …/p1-out is a symlink
--- P2_PARENT_SYMLINK ---   rc=1  build-spans: refused SYMLINK: …/p2-link (a parent of --out) is a symlink
--- P3_SPANS_SYMLINK ---    rc=1  build-spans: refused SYMLINK: …/p3-out/spans is a symlink
--- P4_MANIFEST_SYMLINK --- rc=1  build-spans: refused SYMLINK: …/p4-out/spans.tsv is a symlink
--- P5_ENTRY_DOTDOT ---     rc=2  build-spans: … entry '../escape.md' must be lane-relative
```
Nothing was written outside `--out` in any leg. Caveat: a check on `--out` alone lets P3/P4 through; a check on the write targets alone lets P2 through — the ancestor walk is what makes the wording true ("contained under `--out`", not "under the resolved `--out`"). Repro (scratch only, `B=/fast/scratch/hyaku/chousa-r58/R58ExecC1PathContainment`): clone the lane to `$B/clone` with `git clone --no-hardlinks --quiet`, then `probe_escape.py`; `c1-count.py` against base and `cand/build-spans.py`; `probe_containment_reach.py`; `counter-casefixed/c1-count.py` against `cand/build-spans-escape-allpass.py`. All outputs are the blocks above; scratch removed after.

## 4. Findings against the frozen artifacts (reported, not fixed)
1. **HIGH — `C1=PASS` unreachable for any builder** (`:51` vs `:391`/`:399`): eleven passing legs still yield `C1=FAIL`, exit 1; `c1-measure-after.txt` cannot be produced from these bytes.
2. **HIGH — the containment claim has no leg.** A symlinked **parent** of `--out`, a symlinked `--out/spans` and a symlinked `--out/spans.tsv` are untested; the base builder writes/deletes/overwrites through all three.
3. **HIGH — `expect_refuse`'s `forbidden_touch` is inverted** (`:161-164`): fails when absent, passes when present; the `SYMLINK_OUT` fixture cannot pre-exist, so a correct refusal reads as "was touched/removed", then `:233-236` overwrites the leg and `(target-dir-written!)` is never read.
4. **MEDIUM — containment-diff reach is narrow** (`:141-146`, `:59-66`): plain files inside `out.parent` only; out-of-root writes, symlink-mediated writes, and the whole `HELDOUT_OK` leg are invisible.
5. **MEDIUM — counter crash.** `:212` writes the FOREIGN fixture into `out-empty/spans/`, which only exists if `EMPTY_OK` succeeded; a candidate refusing early crashes the counter (`FileNotFoundError`) before any leg line prints, so `CONTROL_REFUSEALL=denied` is a crash, not a verdict.
6. Guard and reason classes proposed in §3; **no frozen file edited**.

**Limits / not done.** No live fetch; no edit to lane files, the frozen counter, `claims.md` or
`tools/build-spans.py`. The C2 (S101 carrier-alphabet) surface was not examined — out of this seat's surface. The guard was exercised only in scratch: it is **not** applied to the lane builder, so no lane receipt exists for it — the L1 owns that decision. Measurements are from this host (Python 3.14.8, `/fast` on nvme1n1p2). Siblings independently reported the `:391`/`:399` case defect; this seat reproduces it and adds §2b and §2d.

VERDICT: the concrete work/attack is the `--out` containment surface of C1 — symlinked `--out`, symlink-**parent**
of `--out`, symlinked `--out/spans`, symlinked `--out/spans.tsv`. It **survives**: the pinned base builder writes through all four (P1–P4); the frozen battery has no leg for three of them; its containment diff is blind to symlink-mediated and out-of-root writes and vacuous on `HELDOUT_OK`; and with only the `:391`/`:399` case token corrected an escaping builder satisfying every leg semantically prints `C1=PASS`/exit 0 — indistinguishable from an honest one. The frozen predicate is **falsified**: `C1=PASS` is unreachable for every builder under these bytes, so no C1 verdict can be receipted from this counter. The 23-line `_guard_out` guard of §3 closes all four shapes in scratch and is the smallest fix for the containment wording; adopting it, and giving the counter a containment leg of its own, are the L1's calls.
