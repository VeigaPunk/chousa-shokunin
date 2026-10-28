# SentC1Fs — filesystem-edge review of ref-build-spans.py (R61 W1, sentinel)

Target: `corpus/evidence/round61/controls/ref-build-spans.py` (read-only; nothing under the lane was written). Runtime: Python 3.14.8, uid 1000, no sudo. Installs: none. Scratch `/fast/scratch/hyaku/chousa-r61/SentC1Fs/` removed before yield.
Method: fixtures under scratch with a generated `.txt` cache (3000-line capture, 3-row and 3000-row quote tables), driven as `python3 -B <builder> --quotes Q --out DIR --cache C [--check|--replace]`. Real ENOSPC via an unprivileged user+mount namespace tmpfs (`unshare -rm`, `mount -t tmpfs -o size=…`), not RLIMIT. Kills via a `runpy` wrapper that SIGKILLs at a chosen `os.replace`/`unlink` call, plus external SIGKILL polled to land mid-write.

## Findings (defects first)

**D1 — unreadable `spans/` gives an uncaught traceback, exit 1 (not the documented exit 2).** `guard_out` calls `sd.iterdir()` unguarded (line 266). Cause: `os.path.lexists`/`is_dir` swallow errors for the `os.path` family, but `Path.iterdir` raises.
- E3d: `chmod 0300 out/spans`, `build --replace` → `rc=1`, last line `PermissionError: [Errno 13] … out/spans`. Tree unchanged (Q1 manifest 448 B intact).
- E3e: same state, `--check` → `rc=1`, same traceback.
- E3f: `chmod 000 out/spans`, `build --replace` → `rc=1`, same traceback; nothing written.
- Doc says exit 1 = a row refused or STALE>0; 2 = usage/env or output refusal. Neither matches.

**D2 — `--check` on a no-search `out` misreports as stale rows.** E3b: `chmod 600 out` (no x), `--check` → `SPANS_HEADER_STALE`, `SPANS_ROW_STALE` ×3, `SPANS_ROWS=3 STALE=4`, `rc=1`. The directory is inaccessible; the check reports rows as stale instead of an access error. The guard fails open on the same condition (`lexists`/`is_file` return False), so a build is still safe here only because the later `mkdir` fails: E3a/E3c `rc=2 write failed … Permission denied: out/spans`, tree unchanged.

**D3 — an identical rebuild can be refused after a crash, contrary to "an identical rebuild is always allowed".** E7c: `build Q1`; then `build Q3 --replace` killed by SIGKILL at the first orphan `unlink` (manifest already renamed to Q3; `S001-2.txt`, `S002-1.txt` remain orphaned). Re-running Q3 without `--replace` → `rc=2 "already holds 2 span file(s) this run does not write; pass --replace"`. `--check` → `SPANS_FILE_ORPHAN ×2`, `STALE=2`. Recovered by `--replace` → `rc=0`.

**D4 — a failed replacing run leaves the old manifest pointing at overwritten span files.** The "manifest is never without its spans" ordering only covers the new-manifest case. E7b: `build Q1`; `build Q2 --replace` SIGKILLed just before the `spans.tsv` rename. Result: old 448-B manifest (Q1) plus `S001-1.txt` already overwritten with Q2 content; `--check Q2` → `STALE=4`. E2d (same shape, read-only `out` so the manifest write fails with EACCES): span rewritten, manifest old, `--check` → `STALE=4`, `rc=2`. Recovered by `--replace` (E7b rerun `rc=0`; E2f `rc=0`, `STALE=0`).

Minor, not counted in FS_DEFECTS:
- **M1** Identical rebuild into a read-only `out` with a populated `spans/` → `rc=2 write failed … .spans.tsv.<hex>.tmp` (E2c). The builder rewrites every file unconditionally, so even a no-op rebuild needs write access to `out`; use `--check` for read-only verification.
- **M2** Leftover temp files are never reclaimed. Any `.name.<hex>.tmp` (in `out/` or `out/spans/`) survives reruns, `--check` does not flag it, and `--replace` does not remove it (orphan detection matches only `S###-N.txt`). Seen: foreign-pattern tmp survives build+check (E6a); SIGKILL before rename leaves one complete tmp in `spans/` (E7a); external SIGKILL mid-write leaves 1 in-flight tmp in `spans/` in 4 of 6 trials, still present after rerun (E7d0–E7d4). Counts toward nothing but disk clutter.
- **M3** umask overrides the explicit `0o644`: under `umask 077` all files are `0600` and `spans/` is `0700` (E5a); under `022` `0644`/`0755` (E5b). Matters only if another user reads the corpus.
- **M4** Control copy cannot read OLE/zip captures: `TOOLS = …/controls`, and `capture-text.py` exists only under `tools/`. A zip `.raw` yields `refused … capture-text refused …: [Errno 2] … controls/capture-text.py`, `rc=1` (P2). Plain `.txt` captures are unaffected. Canonical `tools/build-spans.py` resolves correctly (INFERENCE from path logic; not run).
- **M5** `--check` does not run the output guard and follows a symlinked `spans.tsv` (E9d reads the symlink target as a manifest; read-only, `rc=1`).

## Per-case results (exit code · leftovers · recoverability)

| # | Case | Exit | Leftovers | Recoverable |
|---|---|---|---|---|
| 1 | `--out` read-only, empty (E2a) | 2 `write failed … out/spans` | none (`MISSING`/empty) | yes, chmod + rerun |
| 1b | `--out` read-only, spans already holds files; differing `--replace` (E2d) | 2 | span file rewritten, manifest old (D4) | yes, `--replace` (E2f) |
| 1c | parent of `--out` read-only (E2g) | 2 | none | yes |
| 2 | no search on `out` (E3a–E3c) | 2 build / 1 check (D2) | none | yes |
| 3 | `spans/` -wx / 000 (E3d–f) | 1 traceback (D1) | none | yes, after chmod |
| 4 | ENOSPC, 3 rows, 12 KiB tmpfs (E4a) | 2 `[Errno 28]` | 3 complete span files, no manifest, no tmp (except path unlinked it) | yes, rerun → `rc=0`, `WRITTEN=3` |
| 4b | ENOSPC mid-run, 3000 rows, 1 MiB tmpfs (E4b) | 2 | 256 span files, no manifest, no tmp | yes, rerun → `rc=0`, `--check` `SPANS_ROWS=3000 STALE=0` |
| 5 | umask 077 (E5a) | 0 | — | modes M3 |
| 6 | foreign `.tmp` present (E6a) | 0; `--check` 0 | foreign tmp left | harmless |
| 6b | forced name collision (token fixed, tmp pre-created) (E6b) | 2 `[Errno 17]` | S001-1 written, S001-2/S002-1/manifest absent, collided tmp left | yes, remove tmp, rerun |
| 7a | SIGKILL before 2nd span rename (E7a) | -9 | complete `.S001-2.txt.<hex>.tmp` in spans/ | yes, rerun `rc=0`; tmp persists (M2) |
| 7b | SIGKILL before manifest rename, replacing (E7b) | -9 | old manifest + mixed span files + `.spans.tsv.<hex>.tmp` in out/ | yes, `--replace` `rc=0` |
| 7c | SIGKILL at orphan unlink (E7c) | -9 | new manifest, 2 orphans | yes, but identical rebuild refused (D3); `--replace` `rc=0` |
| 7d | external SIGKILL, 3000 rows, 6 trials mid-write (E7d) | -9 | 0–1 span tmp in spans/, 0 final manifest | yes, rerun `rc=0`, `STALE=0` in all 6 |
| 8 | 5000 foreign `S999-*.txt` orphans (E8a) | 2 refused, 0.16 s; `--replace` 0 in 0.39 s | none | yes |
| 8b | 5000 `notes-*.md` in spans/ (E8b) | 0, untouched | none | n/a |
| 8c | 3000-row build (E8c) | 0 in 0.47 s; `--check` 0.59 s; identical rebuild 0.56 s; shrink to 3 rows `--replace` 0.15 s | none | n/a |
| 9 | symlinks: `spans`→dir, span file→victim, `spans.tsv`→victim (E9a–c) | 2 each | victims unchanged (`keep.txt` 11 B) | n/a |
| P1 | FIFO as capture (cache) | 1 `refused … not a regular file`, no hang | none | n/a |

## Checks not run
- TOCTOU between guard and writes (race needs a concurrent writer); not exercised, INFERENCE only.
- SIGTERM and SIGINT not run separately; SIGINT goes through `except BaseException` (cleanup), SIGTERM and SIGKILL do not (INFERENCE from code; SIGKILL observed).

Commands: all runs were `python3 -B <builder> …` (subprocess, cwd = scratch) with output as shown in the table; ENOSPC via `unshare -rm sh -c 'mount -t tmpfs -o size=…k tmpfs …; python3 -B …'`.

VERDICT: FS_DEFECTS=4 leftovers_unrecoverable=0
