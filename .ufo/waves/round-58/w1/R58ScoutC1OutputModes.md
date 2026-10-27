# R58ScoutC1OutputModes — C1 output-path findings

## Evidence basis
- Read frozen `corpus/evidence/round58/claims.md` (lines 5–11) and `c1-count.py` before assessing the builder. The frozen C1 claim is the seven refusal legs `FOREIGN`, `SYMLINK_OUT`, `SYMLINK_CACHE`, `FIFO_TXT`, `DEVZERO_TXT`, `FAT_RAW`, `MANY_QUOTES`, plus safe `EMPTY_OK`, `REBUILD_OK`, `HELDOUT_OK`, `ESCAPE_ENTRY`.
- The freeze commit is an ancestor of HEAD. SHA-256 of `claims.md` and `c1-count.py` at freeze and working tree matched (`7aedd815…373457`; `65da18bb…703d3f`). `tools/build-spans.py` is also byte-identical to frozen `corpus/evidence/round58/controls/build-spans-r55.py`, SHA-256 `1ed2650a…c80bf6`.
- No C1 counter was run for this scout; the observations below are source inspection, not counter output.

## Exact build/check and write order
`tools/build-spans.py`:
1. `main()` parses paths, checks only `cache.is_dir()` (lines 186–196), then `read_quotes()` and `build()` run before any output mutation (lines 197–199). Quote input is read whole at line 99; `entry` rejects absolute paths and `..` path components at lines 115–118.
2. In build mode, `sd = out / "spans"`; `sd.mkdir(parents=True, exist_ok=True)` (line 202).
3. Enumerate `sd` and unlink every name matching `SPAN_RE` not present in generated `files` (lines 203–205). `SPAN_RE` is `^S\d{3}-\d+\.txt$` (line 47). There is no ownership/provenance test: a foreign name matching this pattern is treated as an orphan.
4. Write the new manifest `out/spans.tsv` (line 206), then each generated span file in `files` iteration order (lines 207–208), then print `QUOTE` lines and summary (lines 209–212). No staging/atomic swap or rollback is present.

Thus the exact deletion/write sequence is: create/follow output span directory → delete matching orphans → replace manifest → write span files → print. Any refusal in input parsing or `build()` precedes these writes; once build succeeds, deletion and writes are not transactional.

`--check` branches after `build()` and before build-mode writes (lines 200–201). `check()` is read-only: reads manifest and expected span paths, reports missing/stale rows/files and matching orphan names, then returns a stale count (lines 157–183). It does not delete or repair orphans.

## Hazards relative to frozen C1
- **FOREIGN is directly frozen and discriminating:** `c1-count.py` creates `spans/S777-1.txt`, reruns with fewer rows, and requires refusal while preserving it. This builder instead unlinks any stale matching name (main lines 203–205); it is the pinned before-builder and its recorded pin is the same SHA. The counter’s explicit before-control is designed to observe deletion. Counter output was not run here.
- **SYMLINK_OUT is directly frozen:** no symlink check precedes `sd.mkdir` or subsequent writes (main lines 201–208). `mkdir(..., exist_ok=True)` and path operations can follow a symlinked output directory. The exact frozen leg checks refusal and that the target directory remains unwritten.
- **SYMLINK_CACHE, FIFO_TXT, DEVZERO_TXT, FAT_RAW, MANY_QUOTES are frozen input legs, not output-order checks:** `Forms.get()` uses `raw.is_file()`/`txt.is_file()` (lines 74, 85), reads raw/text bytes without size bounds (lines 80, 86), and has no row-count bound in `read_quotes()` (lines 95–124). The counter supplies explicit fixtures and reason classes. No runtime result is asserted here.
- **ESCAPE_ENTRY is frozen as a safe regression leg:** `read_quotes()` rejects `..` in `entry` before writes (lines 115–118); the counter verifies refusal and absence of `spans.tsv`.
- **Not separately frozen by this C1 battery:** a symlink at an individual generated `spans/<id>-<n>.txt` destination can be followed by `write_bytes()` (line 208); collisions/partial failures during manifest-then-file writes can leave inconsistent output; matching-name directories or special objects can make `unlink()` fail. These are source-derived hazards outside the listed frozen predicates, not additional C1 verdict criteria.

## Commands/evidence
- `sha256sum tools/build-spans.py corpus/evidence/round58/controls/build-spans-r55.py` → both `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`.
- `diff -q tools/build-spans.py corpus/evidence/round58/controls/build-spans-r55.py` → `IDENTICAL`.
- Freeze/current SHA comparison for claims and counter → equal (values above); `git merge-base --is-ancestor 9e73a031ab1ac3bac343de008850d7d87f9e5634 HEAD` → `freeze is ancestor of HEAD`.
- Counter run: **unrun**.

VERDICT: The pinned r55 builder’s orphan-deletion hazard survives source inspection; `FOREIGN` and `SYMLINK_OUT` are explicit frozen C1 attacks, while destination symlinks and non-atomic partial-write cases are outside the frozen battery.