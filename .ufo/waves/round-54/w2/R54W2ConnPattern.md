# R54W2ConnPattern — Cross-Claim Pattern, Fleet Counter Audit, and Substrate Convergence Proposal

Seat: `R54W2ConnPattern` (UFO-FSD connector; leaf, no subagent dispatch).
Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin` (read-only; report written to `.ufo/waves/round-54/w2/R54W2ConnPattern.md`).
Scratch: `/fast/scratch/hyaku/chousa-r54/R54W2ConnPattern/` (TMPDIR, `PYTHONDONTWRITEBYTECODE=1`, removed on exit).
Tip measured: `178667dc2c9d1656e864abfdc251c68757428613` (parent `447cf7e` integrated tip). No network, no install.

## 1. Chousa Counter Generation Patterns (Rounds 50–54)

Command executed across chousa counters:
`grep -n -E "src-|write_text|write_bytes|mkdir|open\(.*'w'" corpus/evidence/round{50..54}/c1-*.py`

- **Round 50 (`round50/c1-count.py:127-131`, `c1-supplement.py:43-56`):**
  Copies pinned fixture tree `corpus/evidence/round50/c1-fixtures/` to `tmp / "bad"`, mutating `bad / "expected.json"` and running `--fixtures str(bad) --expected str(bad / "expected.json")`. Expected outputs sit directly beside the test fixtures. Exploited by `controls/forge-tool.py` (42 lines).
- **Round 51 (`round51/c1-count.py:74-82`, `c1-supplement.py:63-71`):**
  `adopt()` writes `work / "registry.md"`, `work / "staged.md"`, `work / "knowledge/corpus/knowledge/e.md"`. No intermediate generator source files (`src-`) exist; files written are the tool's intended domain inputs. Forge vulnerability was parameter metadata leakage: `--out` directory named after the test leg (`s`, `d1`, `d2`), exploited by `controls/forge-dirname.py`.
- **Round 52 (`round52/c1-count.py:114-120, 208-210, 261-263`):**
  OOXML test packages generated entirely in memory via `io.BytesIO()` and `zipfile.ZipFile`. `fresh()` writes only `work / (g.name() + ext)` with `path.write_bytes(data)`. Expected plaintext string (`want`) is never written to disk. **Zero generator inputs left on disk.**
- **Round 53 (`round53/c1-count.py:151-158`, `c1-supplement.py:80-95`):**
  `write_pkg()` writes `registry.md`, `staged.md`, and markdown entries. Domain inputs only; no generator source files. Forge `controls/forge-c1.py` exploited fixed date perturbation shapes and canned REAL on pinned digest.
- **Round 54 (`round54/c1-count.py:119-143, 197-202, 245-257`, `c1-supplement.py:44-49, 102-128`):**
  Introduced external format generation via LibreOffice (`soffice --headless --convert-to doc:MS Word 97`).
  - `gen_docs()` writes `c.work / f"src-{tag}" / f"{name}.html"` (lines 119-140), then converts to `c.work / f"doc-{tag}" / f"{name}.doc"` (lines 142-143).
  - `leg_nonword()` writes `c.work / "src-xls" / f"x{i}.csv"` (lines 197-200).
  - `leg_real()` writes `c.work / "oracle" / f"{k}.txt"` (lines 251-256).
  - All subdirectories sit in the shared work tree `c.work = tempfile.mkdtemp(prefix="r54c1-")` (line 308).
  - When `c.run(str(p))` runs the tool on `p = out / f"{name}.doc"`, `p.parent.parent / ("src-" + p.parent.name[4:]) / (p.stem + ".html")` is accessible on disk.
  - Exploited by `controls/build-c1-forge.py:47-50` to pass 6/6 without parsing compound files.
  - In `c1-supplement.py:44-49`, `isolate()` moves `p` to `c.work / f"iso-{rand12}" / f"{rand10}.doc"`, but sibling directories `src-iso`, `resave-src`, `held-src`, `oracle-resave`, `oracle-held` remain inside `c.work`.

## 2. Fleet Counter Audit

Command executed:
`python3 -c 'import glob; print(glob.glob("/home/vgpnk/Projects/shokunin/*-shokunin/corpus/evidence/round*/c1-count.py"))'`
Observed output: Exactly 26 matches, **all 26 inside `chousa-shokunin`** (rounds 29–54). Sibling lanes do not use this path convention.

Audit of frozen counters across other fleet lanes:
- **`kaidoku-shokunin` (`tools/round-42/c1-counter.py:2240-2245`):**
  `make_real_runner()` isolates each carrier run in `work / ('rerun-' + cid)`, writing only `inp = os.path.join(d, 'carrier.bin')` with `open(inp, 'wb').write(carrier_bytes)`. No generator source files or oracle text exist in `d`.
- **`kake-shokunin` (`.ufo/waves/round-41/c1_count.py:242-250`):**
  Generates XML and JSON sitemaps into directory `cd`, but executes the tool strictly jailed under Bubblewrap:
  `bwrap --ro-bind cd work --clearenv --unshare-all --die-with-parent ...`
  Tool cannot access parent or sibling paths; oracle judgments (`cases[i]["valid"]`) remain in Python memory (`judge()`).
- **`mado-shokunin` (`quality/counters/c1-r47-terminal.py:39-45, 158-172`):**
  Materializes test trees into dedicated scratch `ro` and `rt`, sandboxed via `bwrap --unshare-all --clearenv` mounting only `/case` and `/oracle/tool.py`. System calls monitored via `strace` (`TRACE_SET = "trace=execve,socket,connect"`). No generator sources exist in `/case`.
- **Verdict on fleet practice:** No other fleet lane leaves generator source files or oracle files beside tool inputs. The leakage in chousa R54 is an isolated defect from introducing `soffice` batch generation without directory airgapping.

## 3. Ground Substrate Gap: `build-spans.py` vs `capture-text.py`

Inspection of `corpus/evidence/round54/build-spans.py:107-114`:
```python
def raw_form(b: bytes) -> str:
    """The raw capture's text form: `docx_text` for a zip, else UTF-16LE."""
    if b[:4] == b"PK\x03\x04":
        t = docx_text(b)
        if t is not None:
            return t
    return b.decode("utf-16le", errors="replace")
```
- When reading an OLE `.doc` capture (e.g. S101, S130), `build-spans.py` does **not** call `tools/capture-text.py`. It falls back to raw `b.decode("utf-16le", errors="replace")`.
- Observed discrepancy on S130 capture (`bdff491a75c6abeda1d9c01d.raw`):
  `tools/capture-text.py --locate "是否检索灰色文献等关键问题"` → `LOCATED count=1 offset=4678`
  `raw.decode("utf-16le", "replace").find("是否检索灰色文献等关键问题")` → `offset=57497` (with 887 U+FFFD characters)
- Consequence: In round 54, the S101 leg was cut from `source-type-taxonomy-r37.md` (erratum E3), the S130 grey-literature entry was blocked (`R54W2ScoutFrontier.md`), and nine retroactive `correction:` lines were required in `SCORECARD.md:2740-2748` to fix S100/S101 pointer offsets.

## 4. Connector Proposal: Two-Sided Air-Gapped Harness & Substrate Convergence

A compatible synthesis across the round's proposals (`SCORECARD.md` Planned, `R54W2DraftStreak.md` RW-1, `R54W2ScoutFrontier.md` S101/S130 unblocking):

### Affected Axes
- **Operability (Capability Verification):** Permanently terminates Recurring Weakness RW-1 (frozen counter forgeable, streak=6).
- **Depth / Ground:** Unifies `build-spans.py` with `tools/capture-text.py`, allowing `.doc` sources (S101, S130) to be anchored cleanly without broken UTF-16LE decodes or scorecard correction shims.
- **Harms None:** Preserves frozen round-54 rules; introduces no external binary dependencies or network egress.

### Proposed Move
1. **Air-Gapped Ephemeral Execution in Counter:**
   For the round-55 frozen C1 counter, enforce a strict three-phase execution boundary:
   - *Phase 1 (Generation):* External generators (`soffice`) write to a private `gen_work` directory.
   - *Phase 2 (Per-Case Airgap):* For each tool invocation, create a fresh, disjoint `tempfile.TemporaryDirectory(dir=system_tmp)` holding ONLY the opaque target `.doc` under test. Run the tool with `cwd=case_dir` and `str(case_dir / "target.doc")` under the existing process audit hook (`HOOK`). Immediately purge `case_dir` on return.
   - *Phase 3 (Non-Canned REAL):* Replace static sha256 prefix checks in REAL with dynamic resave round-trips (`c1-supplement.py:101-118`) and held-out generation (`c1-supplement.py:121-135`), making digest canning impossible.
2. **Substrate Convergence in `build-spans.py`:**
   In `corpus/evidence/round55/build-spans.py`, update `raw_form(b)` to delegate OLE compound files (`b[:8] == b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"`) directly to `tools/capture-text.py` text form extraction.

### Verification of Proposed Move
Tested `controls/build-c1-forge.py` on an isolated `.doc` without sibling `src-` directory in scratch:
```
$ python3 corpus/evidence/round54/controls/build-c1-forge.py $S/forge
$ python3 -c 'import subprocess, sys; r = subprocess.run([sys.executable, "$S/forge/forge.py", "$S/isolated/test.doc"], capture_output=True, text=True); print("rc:", r.returncode, "err:", r.stderr.strip())'
rc: 2 err: REFUSED ole-malformed: forge
```
The forge fails immediately with exit 2 when denied sibling generator source files.

### Risks and Tradeoffs
- **I/O overhead:** Ephemeral directory creation per test case adds ~20 ms across 15 test files, well within the 300 s runner timeout.
- **Audit hook compatibility:** Restricting filesystem layout requires no modification to the Python audit hook (`sys.addaudithook`), avoiding brittle OS path filtering in the hook.

VERDICT: attacked cross-claim counter forgeability (RW-1) and substrate span-reader divergence — both survive as verified systemic gaps; proposed two-sided air-gapped test driver and capture-text substrate convergence.
