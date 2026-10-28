# RevRefDiffForms — review of `tools/build-spans.py` → `corpus/evidence/round61/controls/ref-build-spans.py`

Scope: `Forms._probe`, `Forms.get`, `Forms._read`, `_ct_form` (the `_capture_text` helper), the caps (`MAX_CAPTURE`, `MAX_FORM`), and the output guard the diff added (`guard_out`, `_atomic_write`, `write_out`), read against regress and the C1 legs. Line numbers are the reference file's. Base sha `1ed2650a…c80bf6` (blob `072415ad`); reference sha `86d64c31…eccfd`; capture-text `2c0140bc…`. Read-only: no lane file, git state or tool was changed. All reproductions ran in my scratch and are deleted.

## Findings (by severity)

**F1 — BLOCKING. A raw capture that is unreadable, outside the cache, dangling or a FIFO silently falls back to the `.txt` sidecar.** L115–126 (`rk` set to `bad` by the `OSError` at L119–120 or by `_probe`, then `elif tk == "ok"` at L124 takes the sidecar). The docstring says the opposite: L9–12 "the `.txt` sidecar is never used for such a capture", L16–19 "a symlink out of the cache, a FIFO or device, an oversize or unreadable file is a refused row". The code matches the docstring only for the oversize case.
- Repro R1 (mode-000 OLE-magic `.raw` plus a valid `.txt`): ref `rc=0`, span `SIDECAR text Quote-Alpha-1234 more sidecar text`. Base `rc=1`, `PermissionError` traceback. The ref turns a refusal into a success with different text.
- Repro R2 (`.raw` is a symlink outside the cache to a real docx; sidecar text differs): ref `rc=0`, span `SIDECAR text …`, `capture_sha256` prefix `09886271956c`. Base `rc=0`, span `DOCX text …`, prefix `a986f60f3df1`. Old callers see a silently different form and digest for the same URL. Docstring says refused.
- R2f (FIFO `.raw` plus sidecar): ref and base both `rc=0` with the sidecar. The docstring's "refused row" is wrong for both; this is not a regression.
- Why C1 does not see it: legs H13/H17/H18 only exercise the `.txt` (symlink, mode 000, FIFO). No leg puts a hazard on the `.raw`. The 20/20 count is therefore no evidence on this path (counter limit, not a refutation).
- Fix shape: if `os.path.lexists(raw)` and `rk != "ok"`, refuse with the `_probe`/OSError reason; use the sidecar only when the raw path is absent.

**F2 — Not blocking. The reason for a bad raw is dropped when no sidecar exists.** L127–130 ignore `rv` when `tk == "absent"`. Repro R3 (dangling `.raw` symlink, no `.txt`): ref and base print the same `no defined text form … (raw neither OLE nor zip, no .txt)`. The text is misleading for a dangling link. Same fix as F1.

**F3 — BLOCKING (exit-code contract). Unguarded OS calls in the new output guard and in `check`.** The docstring (L34–35, L44–45) promises exit 2 for output refusals.
- L273 `m.read_bytes()` in `guard_out` and L266 `sorted(sd.iterdir())` are new calls with no `try`. Repro R5 (`spans.tsv` mode 000, build): ref `rc=1 traceback=True`, `PermissionError`, nothing written. Repro R8 (`spans/` mode 000): ref `rc=1 traceback=True`, `PermissionError` in `scandir`.
- L234 `p.read_bytes()` in `check` is unguarded. Repro R9 (`--check`, one span file mode 000): ref `rc=1 traceback=True`. Base is identical; the diff wrapped only the adjacent `spans.tsv` read (L219–223) and left this one.
- Base also tracebacks on R5 (`write_bytes` on a mode-000 file) and R9, so the class is not new, but the diff adds two new unguarded paths (R5, R8) inside the function it names as the guard.
- Fix shape: wrap `guard_out`'s reads and the `check` span-file read in `except OSError` → `_refuse`/exit 2.

**F4 — Not blocking. Partial writes return exit 2 with a state the docstring does not describe; the guard lets a directory sit at a span-file name.** L300–309 write span files one by one, then the manifest, then unlink orphans. The docstring (L34–40) lists refusals that write nothing, but it lists only symlinks at span-file names (L35–36), not directories.
- Repro R7 (`S002-1.txt` replaced by a directory, prior build, S001 text changed, `--replace`): ref `rc=2` (`IsADirectoryError` on `os.replace`). `S001-1.txt` already holds the new bytes; `spans.tsv` still holds the old digest. A following `--check` prints `SPANS_ROW_STALE spans/S001-1.tx…` and `rc=1`.
- Repro R6 (orphan directory `spans/S009-1.txt`): without `--replace` ref `rc=2`, refused (correct). With `--replace` ref `rc=2`, `Is a directory` at L305–306 after `spans.tsv` was already replaced (`rows now: 2`); the orphan remains.
- Fix shape: in `guard_out`, refuse any `SPAN_RE` entry that is not a regular file (L267–272), before any write.

**F5 — Not blocking. The derived-form cap is applied after the form is materialised.** L147 builds `form = to_form(b)`; L150–151 check `len(form) > MAX_FORM`. The docstring (L17–19) says "refused likewise", which reads as decided before the work.
- Repro R10 (200 MiB of text in a 204,447-byte docx; capture-text's own bound is 256 MiB inflated, capture-text.py L78): ref `rc=1`, `text form is 209715319 chars, over the 67108864-char cap`, child `ru_maxrss` **633,108 KiB**. The cap bounds output, not memory.
- INFERENCE (not run): memory scales roughly linearly with inflated size, so a 256 MiB main part would reach roughly 0.8 GB. The C1 H20 leg uses 70 MiB and does not check RSS, so no leg covers this.

**F6 — Low. Capture is read twice; the digest and the form can come from different reads.** L143 `path.read_bytes()` gives the digest of `b`; L123 `lambda b: self._ct_form(raw)` ignores `b` and L137 re-reads the path inside capture-text (capture-text.py L389–391). `b` is dead for the raw branch. Base has the same pattern (base L116–119). INFERENCE: an in-place rewrite between the two reads yields a `capture_sha256` that does not match the form; not reproduced. Named limit (i) covers only directory swaps, not in-place rewrites.

**F7 — Not a defect against the docstring (calibration).** An identical rebuild overwrites a hand-edited span file of the same name without `--replace`. Repro R4: `rc=0`, file restored. Docstring L36–38 refuses only a different `spans.tsv` or extra span files, and says identical rebuilds are allowed. Base behaves the same. Noted so L1 can decide whether same-name content changes should also refuse.

## Old-caller observable changes (checked)
- O1 Rebuild into a non-empty DIR with a differing `spans.tsv` now exits 2 (base overwrote). Intended (docstring L36–37); callers must pass `--replace`. I did not audit each caller (grep for `tools/build-spans.py` hits lessons and evidence scripts, e.g. `corpus/evidence/round56/c1-gate.py`); INFERENCE that a caller that rebuilds over a changed input now fails loudly.
- O2 Captures over 64 MiB and forms over 64 Mi chars are refused (base accepted). The committed sets are far below this; regress confirms (below).
- O3 Unreadable/outside/FIFO raw falls back to the sidecar (F1). This is the only silent output change for an existing path.
- O4 Error text for bad raw changed (F2). Refused either way.
- O5 `capture-text` is imported with `dont_write_bytecode` (no observable effect; restored in `finally`).
- Per-round builders (`corpus/evidence/round45…57`) are separate files and are not touched by this diff.

## Checks run
- `diff -u tools/build-spans.py corpus/evidence/round61/controls/ref-build-spans.py` → 274 lines of diff; sha256 `1ed2650a…` (base) and `86d64c31…` (ref) match the claims; `git rev-parse HEAD:tools/build-spans.py` = `072415ad…` (read-only).
- `python3 -B corpus/evidence/round61/regress.py --builder controls/ref-build-spans.py --work <scratch>/regress-ref/w` → `REAL_REBUILD=3/3`, `regress_rc=0` (round55, round56, round57/c3 each `check_rc=0 build_rc=0 identical=True pass`). Not run for the base in this seat (base was run by the lane).
- Reproductions R1–R10 with `python3 -B repro.py <R#>` (driver in my scratch, removed). Outputs quoted above.
- Python 3.14 semantics (sem run): `os.path.lexists` true for dangling links; `Path.is_file()` false and `is_symlink()` true for a dangling link; `os.path.realpath` → target path; `os.path.commonpath([real, root]) == root` rejects sibling-prefix (`cache2`); `os.replace(tmp, symlink)` replaces the link itself and leaves the victim (`victim: VICTIM`). The guard refuses symlinks before the write, so the replace case is reached only through the named TOCTOU limit.
- Not run: `c1-count.py` (not my item); the H-legs were not re-run by me.

## Residual risk / verification gaps
- C1 counter's 20/20 does not exercise `.raw` symlinks, unreadable `.raw`, directories at span names, or `spans/` / `spans.tsv` mode-000 reads (F1, F3, F4 are outside the 20 legs; counter limit).
- F5 memory extrapolation is INFERENCE.
- Scratch `/fast/scratch/hyaku/chousa-r61/RevRefDiffForms/` deleted before yield.

VERDICT: REF_DEFECTS=6 blocking=2
