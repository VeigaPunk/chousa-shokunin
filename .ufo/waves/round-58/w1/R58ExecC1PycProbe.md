# R58ExecC1PycProbe — round 58, C1 operability: `tools/__pycache__` side effects of `tools/build-spans.py`

Seat: reconnaissance only (not an additional claim). Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`,
freeze commit `9e73a031ab1ac3bac343de008850d7d87f9e5634`, claim base `b13ca7b5c8bbb40d2d29a37fb443c64ca043f791`.
All runs used scratch copies under `/fast/scratch/hyaku/chousa-r58/R58ExecC1PycProbe/` only (removed before yield);
no lane file was written by this seat — the 6-file lane `tools/__pycache__` manifest sha256
`0e7ac0ddad26194837a7c9112ee9c062e23483586784acb4fd4f175b7efa98e9` identical before/after every probe (a 7th file,
`build-spans.cpython-314.pyc`, appeared mid-window from a sibling — §6).
Python 3.14.8, `sys.dont_write_bytecode` False by default. No installation requested or performed.

## 1. Question

Does executing `tools/build-spans.py` — which does `importlib.util.spec_from_file_location("capture_text",
TOOLS/"capture-text.py")` + `spec.loader.exec_module(mod)` (`tools/build-spans.py:56-60`) — create or update
`tools/__pycache__` when run normally (no `-B`, no `PYTHONDONTWRITEBYTECODE`)?

## 2. Answer

**Yes.** A normal run creates `tools/__pycache__/capture-text.cpython-314.pyc` **next to the source**
(`TOOLS/__pycache__/`), not in the cwd and not under `--out`. The builder itself is not cached (run as `__main__`
it is never bytecode-cached); only the importlib-loaded `capture-text.py` is. The write happens **only when the
OLE/zip branch is taken** (`Forms.get` → `_capture_text()`): a `.txt`-only capture set never imports it and never
creates a pyc. Create-vs-update is decided by CPython timestamp invalidation (source mtime+size):

| pre-state of `tools/__pycache__/capture-text.cpython-314.pyc` | normal-run outcome |
|---|---|
| absent | **created** |
| present, header mtime+size == source | **untouched** (byte-identical, mtime unchanged) |
| present, header stale | **rewritten** (new sha256, new mtime) |

## 3. Exact before/after hashes — canonical reproduction (clean scratch copy)
```
S=/fast/scratch/hyaku/chousa-r58/R58ExecC1PycProbe
L=/home/vgpnk/Projects/shokunin/chousa-shokunin
rm -rf "$S/canon"; mkdir -p "$S/canon/tools"
cp -p "$L/tools/build-spans.py" "$L/tools/capture-text.py" "$S/canon/tools/"
find "$S/canon/tools" -type f -exec sha256sum {} \;
env -u PYTHONDONTWRITEBYTECODE TMPDIR="$S" python3 "$S/canon/tools/build-spans.py" \
    --quotes "$S/quotes.tsv" --out "$S/canon/out" --cache "$S/cache"
find "$S/canon/tools" -type f -exec sha256sum {} \;
```
BEFORE:
```
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  .../canon/tools/build-spans.py
2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573  .../canon/tools/capture-text.py
```
run output: `QUOTE S101 char 315 spans/S101-1.txt` / `SPANS_ROWS=1 WRITTEN=1`, rc=0
AFTER:
```
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  .../canon/tools/build-spans.py
2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573  .../canon/tools/capture-text.py
158cd8a60c942605eb549e9fb10c9c6a4058c532c8bd575e39c40a49b1837638  .../canon/tools/__pycache__/capture-text.cpython-314.pyc  (34809 B, NEW)
```
pyc header `hdr: (b'+\x0e\r\n', 0, 1793067585, 20203)`: magic `2b0e0d0a` (3.14), **flags=0 = timestamp-based, not
hash-based**. `co_filename` = absolute source path, so pyc bytes are path-specific: the same source compiled under
`lanecopy/` gave `1b6760659bb85479500437bd3471ec9386ab1e6023e8b695d310dc286ada8a2d` (34812 B), under `twice/`
`be646d5c1101a9a113fa6c721c331bb5f03c3f85f7c0c0ee12283f17230e2f67` — do not compare pyc hashes across trees.

## 4. Supporting probes (all observed, scratch-only)

* **Creation is conditional on the OLE/zip branch.** `.txt`-only capture set: rc=0, `tools/` still holds only
  `build-spans.py capture-text.py` — **no `__pycache__`**. With an OLE capture, `__pycache__` appears. A malformed
  OLE raw still imports (then refuses) and still leaves a pyc `5b7b39dde404dc73bc1b26fb12d8f22ebb6baec7be4822e2c1ba158c17d1786f`.
* **`--check` mode also creates it**: `SPANS_ROWS=1 STALE=0`, pyc `200731b0bd20381a5d11f21305d12fa04a76f4f335383139bd2e72f47d291812`.
* **Location is source-relative, not cwd-relative**: run with cwd=`…/cwdtest/work` → cwd stayed empty,
  `__pycache__` appeared in `…/cwdtest/tools/`.
* **Existing valid pyc is not rewritten**: re-run → sha256 and mtime (`1793074508`) unchanged; same on a `cp -a`
  copy of the *lane's own* `tools/` including its pycache (`3b8fd404…` unchanged).
* **Stale pyc is rewritten**: `touch capture-text.py` → next normal run rewrote it `1b676065…`→`986d4df873b7a4cf77a623117ac0eea782c6698c2a5efed660968e603fb45aa4`;
  on the lane-copy `3b8fd404…`→`6ae16da98dfdbc67d95a4c1f69549591c33cb15198165dde3dff54e7af9908b6`.
* **Suppression matches the counters' assumption**: `-B` alone → no `__pycache__`; `PYTHONDONTWRITEBYTECODE=1`
  alone → no `__pycache__`. The counters use both (`c1-count.py:112-118`, `c2-count.py:74-75,122-123`); running
  `c1-count.py` and `c2-count.py` with them left lane `tools/__pycache__` byte-identical (diff → identical).
* **Read-only tools dir**: `chmod a-w tools/` → rc=0, no pyc, no error (CPython silently skips the write).
* **Script vs importlib**: `python3 capture-text.py RAW` creates **no** pyc for itself; `importlib`-loading
  `c1-count.py` **does** create `corpus/evidence/round58/__pycache__/c1-count.cpython-314.pyc` — such a file exists
  in the lane (mtime 14:12:21, co_filename = lane path): a sibling seat imported the counters as modules.

## 5. The hazard that matters for C1/C2 (stale-pyc READ is not suppressed by `-B`)

`-B`/`PYTHONDONTWRITEBYTECODE` suppress **writing**; they do **not** stop CPython from *reading* an existing pyc
whose header (mtime, size) matches the source. With flags=0 (timestamp-based), a source whose content changed but
whose **mtime and size were preserved** keeps a stale pyc valid, and the importlib path silently executes the OLD code.

Demonstrated end-to-end in scratch (`div/`): (1) normal run compiles a pyc from pristine `capture-text.py`;
(2) `OLE_MAGIC` edited in place (`d0cf…`→`d1cf…`, same length) with `os.utime` restoring the original mtime
(size 20203, mtime 1793067585 preserved); (3) **script path** (fresh compile) → `REFUSED neither a zip package nor
an OLE compound file`, rc=2; (4) **importlib path** (stale pyc still valid) → `QUOTE S101 char 315 spans/S101-1.txt /
SPANS_ROWS=1 WRITTEN=1`, rc=0; (5) `-B` run → **still rc=0** (stale pyc read; `-B` did not help); (6) deleting the
pyc → importlib path now refuses, matching the script path. Sharper variant (`stale/`): the source was corrupted
into a **syntax error** (`def text_form(`→`DEADtext_form(`; `py_compile` → `SyntaxError: invalid syntax`), mtime+size
restored — yet the `-B` builder run still succeeded rc=0 with a valid span, because the stale pyc was used and the
broken source was never compiled: `-B` gives **zero** protection here.

**Bearing on the frozen counters (report only — no counter altered).** `c2-count.py` derives the defined form by
running `capture-text.py` as a **script** (lines 74-75: fresh compile, never the pyc) and derives the rebuild by
running the **builder** (line 122, whose internal importlib load *can* consume
`tools/__pycache__/capture-text.cpython-314.pyc`). The C2 pin (`CT_SHA = 2c0140bc…`, `c2-count.py:18`) is a sha256 of
the **source file**, not of the bytecode the builder executes. `c1-count.py`'s `HELDOUT_OK` leg likewise computes its
reference form by script (lines 322-325) and compares it with the builder's output. A stale-but-valid pyc in the
lane's `tools/__pycache__/` could make the two paths disagree. **Latent hazard, not currently live**: the lane's
live pycs are faithful compiles of the current sources — `capture-text: pyc_bytes_equal_to_fresh_compile_of_current_source = True`,
`build-spans: … = True` (`marshal.dumps(compile(src))` vs `pyc[16:]`).

## 6. Lane state observed (read-only; no write by this seat)

* `tools/__pycache__/` is gitignored (`.gitignore:2 tools/__pycache__/`) and already holds
  `assimilate-rows, capture-fetch, capture-text, inference-ground, quarantine-check, quote-reopen`. The
  `capture-text.cpython-314.pyc` there has `co_filename` = the **lane** path, file mtime `2026-10-27 01:15:08`,
  header mtime == source mtime 1793067585, size 20203 → valid & fresh. So a normal (non-`-B`) run/import against
  the lane tools dir has already occurred at least once.
* During this seat's window a **new** `tools/__pycache__/build-spans.cpython-314.pyc` appeared (mtime
  `2026-10-27 14:21:20`, 17149 B, `co_filename` = the lane `tools/build-spans.py`, header mtime 1793072301 == source
  mtime, byte-equal to a fresh compile of the current source). **Not mine**: every builder run I made used a scratch
  copy, and my two counter invocations used `-B` + `PYTHONDONTWRITEBYTECODE=1` (both left `tools/__pycache__`
  identical); its `co_filename` proves it came from an **importlib load of the lane builder** by a sibling process
  (concurrent seats were observed running `c1-count.py` and `build-spans.py` without `-B`). Because the dir is
  gitignored, `git -C "$L" status --porcelain` stayed clean (`?? .ufo/waves/round-58/` only) — the side effect is
  untracked-but-real, and a tracked-file check would not catch it.
* Same surface, incidental: the pinned before-builder `corpus/evidence/round58/controls/build-spans-r55.py` resolves
  `TOOLS` to the controls dir, which has **no** `capture-text.py`; against an OLE capture it dies with
  `FileNotFoundError: …/round58/controls/capture-text.py` (rc=1) instead of a clean refusal. The frozen counter's
  `BEFORE_FOREIGN` leg uses `.txt` fixtures only, so it is unaffected — that control cannot exercise the OLE path.

## 7. Limits

The lane-write claim is confirmed by simulation on a copy of the lane's own `tools/` (`cp -a` of lane `tools/`,
same relative layout) plus the source-directory-local `__pycache__` mechanism; running it in the lane in place was
**not** performed (lane writes are outside this seat's mandate). No live fetch was made — only the committed lane
capture `corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` (sha256
`6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3`, OLE magic `d0cf11e0a1b11ae1`) was copied into
scratch and read there. Nothing was proposed or applied to `claims.md`, the counters, the controls or the quote set.

VERDICT: the attack "run `tools/build-spans.py` normally (no `-B`, no `PYTHONDONTWRITEBYTECODE`) → the importlib load
of `tools/capture-text.py` creates/rewrites `tools/__pycache__/capture-text.cpython-314.pyc` in the tools dir,
outside `--out`" **survives** (created `158cd8a6…` in a clean copy; stale pyc rewritten `3b8fd404…`→`6ae16da9…`;
valid pyc left byte-identical); the related attack "a stale-but-timestamp-valid pyc makes the builder execute code
differing from the sha256-pinned `capture-text.py`, and `-B` does not stop it" also **survives** as a reproducible
hazard (importlib rc=0 vs script rc=2 on the same bytes), though it is **not currently live** in the lane — both
lane pycs are byte-equal to fresh compiles of the current sources (`= True` ×2), so present C1/C2 are unaffected.
