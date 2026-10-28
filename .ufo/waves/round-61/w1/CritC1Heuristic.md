# CritC1Heuristic — round 61 w1 — output-safety hazards outside the 20 legs

Builder measured: `corpus/evidence/round61/controls/ref-build-spans.py`, sha256 `86d64c312e1640d44f1e71bb3e23c8fc6c8b4ef56b627ae5750f761a579eccfd` (matches the frozen value). `tools/build-spans.py` was not run.
Fixtures ran only under `/fast/scratch/hyaku/chousa-r61/CritC1Heuristic` (deleted before yield). The lane was read only: `tools/capture-text.py` was copied into each fixture. No install was made. One tmpfs was mounted with `sudo -n mount -t tmpfs -o size=1M,uid=1000,gid=1000` and unmounted with `sudo -n umount`; the mount count afterwards is 0.

## Damage rule (fixed before the data)
DAMAGE = (a) a pre-existing file outside the operator's named `--out` tree was changed or removed; or (b) a previously consistent build was left inconsistent (manifest bytes unchanged while a span it names changed or was removed); or (c) bytes of a file the operator did not name as a capture appear in the output.
Not counted: writes that only create files outside the named tree (reported as "redirect"); resource use (reported separately).

## Damage found (5 of 16 hazard classes)
1. **F01b, `--out` is a symlink to a directory.** The target holds a foreign `spans.tsv` and an orphan `spans/S777-1.txt`. Plain run: rc 2, "already holds a different spans.tsv", nothing changed (safe). `--replace`: rc 0; the foreign `victim/spans.tsv` is replaced and `victim/spans/S777-1.txt` is deleted. DAMAGE (a). The guard checks `DIR/spans` and `DIR/spans.tsv` for links (legs H10–H12) but not `DIR` itself. INFERENCE: whether a symlinked DIR is intended is the author's call.
2. **F02, ancestor symlink (`link/out` -> `victim`).** Same result with `--replace`: rc 0, foreign manifest replaced, orphan deleted. DAMAGE (a).
3. **F06, process killed mid-write (SIGKILL).** A watcher killed the child once `.S002-1.txt.<hex>.tmp` had size > 0; the leftover partial is 786,432 bytes of a 20 MiB span. Result: rc -9; `S001-1.txt` replaced; `spans.tsv` still the old one. `--check` rc 1 (STALE). A later `--replace` rebuild rc 0, but the partial `.tmp` is never removed. DAMAGE (b).
4. **F09, ENOSPC mid-run on a real tmpfs of 1 MiB.** Free space after the filler was about 6 KB, and the first span file fit. Result: `--replace` rc 2 "No space left on device"; `S001-1.txt` replaced; manifest old. `--check` rc 1. DAMAGE (b). (A first run with both spans large failed on the first file and changed nothing, because tmpfs allocates in 4 KiB pages; that run is not counted.)
5. **F16, capture hardlinked to a file outside the cache.** `cache/<key>.txt` is a hard link to `victim/secret.txt`, whose text places `VICTIM-SECRET-7f3a91` inside the 80-char window. Result: rc 0; the marker is written into `out/spans/S001-1.txt` (`grep -c` = 1). The realpath check passes because the link name is inside the cache. DAMAGE (c). This is a read-side exposure; write-side damage alone gives k=4.

## Measured, not damage
- **F03a/F03b hardlinked span file / manifest** to a victim: rename replaces the name. Victim content intact; victim nlink 2 -> 1. Safe.
- **F04a/F04b cache-prefix sibling** (`cache-evil`, symlinked `.txt` or `.raw`-only): rc 1, "resolves outside the cache" / "no defined text form". Nothing written. Safe. (`commonpath` compares path components.)
- **F05 leftover `.tmp` in spans/** (a symlink to the victim, plus a regular file): rebuild rc 0, `--check` rc 0, victim intact. The tmp files are never cleaned, so they persist. Hygiene leak only.
- **F07 CRLF `spans.tsv`**: `--check` rc 0 (STALE=0; the universal-newline read makes CRLF match). Plain rebuild rc 2 (refused). `--replace` rc 0 rewrites LF. Check false pass; no write damage.
- **F08a read-only parent** of `--out`: rc 2 "write failed ... Permission denied", nothing created. **F08b read-only `spans/`**: rc 2, nothing changed. Safe.
- **F10 directory named `S404-9.txt` in spans/**: plain rc 2 (refused, safe). `--replace`: rc 2 "Is a directory", but `spans.tsv` and `S001-1.txt` were already rewritten. Exit contract broken (docstring: exit 2 means nothing written). No outside damage.
- **F11 / F11b DOCX inflating to 200 MiB / 250 MiB** (files of 205 KB and about 250 KB): rc 1 after the 64M-char cap; child peak RSS 608.1 MiB and 756.9 MiB. The counter's RSS leg (H14/H15, 96 MiB) reaches only the file-size cap. Inflation is bounded by `MAX_PART` (256 MiB), not by the 64 MiB file cap. Resource hazard, not counted.
- **F12 entity expansion** (8 levels of x10): rc 1, "limit on input amplification factor", RSS 80.6 MiB. Safe.
- **F13 quotes file with byte 0xff**: rc 1 with a `UnicodeDecodeError` traceback, nothing written. The docstring reserves exit 1 for refused rows and exit 2 for usage errors. Contract only.
- **F14 `--out` equal to the capture cache**: rc 0; `spans/` and `spans.tsv` created inside the cache; captures unchanged. No damage.
- **F15 `--check` with `DIR/spans` a symlink to a copy**: rc 0, STALE=0 (the check follows the link). Plain build refuses (rc 2). Check false pass.
- **F01a `--out` symlink to an empty dir**: rc 0; three files created in the link target. Silent redirect; no existing bytes changed.

## Method
Each fixture is a fresh tree with `tools/build-spans.py` (= reference) and `tools/capture-text.py` (lane copy), `cache/`, `victim/`. Before and after each step the whole fixture tree is snapshotted (lstat; sha256 for files up to 1 MiB; size+mtime+inode above that). Diffs are split by whether the path lies under the lexical `--out` tree. Child runs use their own session, a 60 s timeout (300 s for the large ones) and `wait4` for peak RSS.

## Limits
- n = 16 hazard classes, 21 steps. Each step is one run from fresh state; no repeats for timing.
- F06 kill timing comes from a polling watcher; this is one observed run of the result, not a timing proof.
- Not exercised: TOCTOU swap (counter limit i), concurrent builders, the lane's `tools/build-spans.py` (base blob `072415ad`), and the 20 legs themselves (they were not re-run here).
- F04 is the sibling-prefix variant of H13 (outside cache symlink). None of the 16 classes is a frozen leg H07–H20.

## Commands and output
- `sha256sum .../controls/ref-build-spans.py` -> `86d64c31...eccfd`.
- `python3 -B drv.py` (scratch, 21 steps, 11.6 s) -> final line `SUMMARY measured=21 damage=5 damage_cases=['F01b', 'F02', 'F06', 'F09', 'F16']`.
- Per-step rc and state: F01b replace rc 0, `out-removed=['victim/spans/S777-1.txt']`; F06 replace rc -9, `killed=True`, `prior=True`; F09 replace rc 2, `No space left on device`, `inner.changed=['~mnt/out/spans/S001-1.txt']`, `prior=True`; F16 rc 0, `leak=True`.
- `grep -c VICTIM-SECRET-7f3a91 .../F16/out/spans/S001-1.txt` -> `1`.
- `mount | grep -c CritC1Heuristic/fx/F09/mnt` -> `0` (after unmount).
- Lane `git status --short` (read-only) lists other seats' untracked files; nothing from this seat is in the lane. `tools/__pycache__` predates this run.

## Recommended correction (for L1, not applied)
Reject a symlinked `DIR` (lstat on the `--out` path and each ancestor) unless `--allow-link`; check `spans/S*.txt` for hard links (`st_nlink > 1`) before writing; verify the output manifest after the span writes and report STALE before exit 0; sweep orphan `.tmp` names in `spans/` at start.

VERDICT: UNCOVERED_HAZARDS_THAT_DAMAGE=5 of 16
