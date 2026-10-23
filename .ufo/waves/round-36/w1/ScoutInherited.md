# ScoutInherited — attempt-1 debris vs freeze 700bd5f

Axes checked: inventory completeness, byte-identity to the freeze, content class (bytecode vs source/receipt), reuse/discard. Nothing was deleted by this scout.

Access date for every open below: 2026-10-23.

## Verdict

Inherited untracked debris under `corpus/evidence/round36/` was **bytecode only**: one CPython 3.14 timestamp `.pyc` of the already-tracked `c2-count.py`, with no separate source, receipt, or other artifact inside. **It contains no authored work beyond that tracked counter.** DISCARD the cache. REUSE the three tracked files: each is byte-identical to freeze `700bd5fcbf9abc118a6a0f078d51a2e7460c2878`. Other porcelain-untracked paths are this wave's attempt-2 dispatch (authored orchestration and live seat output), not attempt-1 residue.

## Item table

| path | tracked? | content class | reuse / discard |
|---|---|---|---|
| `corpus/evidence/round36/c1-count.py` | yes, mode 100755, blob `d6a53ab7cc2748963f7131c02fa62c9271cdcadf`, 33861 bytes, sha256 `3fefffe745ed10d2fd06c4c3cc9073ab7bfb46dd82e32c166976fd3aaf4c35be` | Python source (bytes compared, not read as text) | **REUSE.** `git show 700bd5f:… \| cmp -s` → `CMP_IDENTICAL`. Worktree `git hash-object` equals the freeze blob. |
| `corpus/evidence/round36/c2-count.py` | yes, mode 100755, blob `20bed4495796200be2fee90d9df2705c612deeb3`, 13126 bytes, sha256 `3c699aab0614fff78f88d1b8570166439014a360ee378c0a143bf204a96e4362` | Python source. mtime `2026-10-23 18:00:13.099474306 -0300` (`st_mtime` sec `1792789213` = `2026-10-23T21:00:13Z`). Tail opened by search: `if __name__ == "__main__":` at line 293 | **REUSE.** Same `CMP_IDENTICAL` + hash-object match. |
| `corpus/evidence/round36/claims.md` | yes, mode 100644, blob `b02134a9aaba9ce0b456b80a143a6687d8accc1e`, 7924 bytes, sha256 `ca2c952b0ddb831eaa08cab9a41094dc122aa9d512638c88dbadc4fad587badf` | Markdown (bytes compared, not read as text) | **REUSE.** Same `CMP_IDENTICAL` + hash-object match. |
| `corpus/evidence/round36/__pycache__/c2-count.cpython-314.pyc` | **no.** Freeze `ls-tree` has only the three paths above. First porcelain listed `?? corpus/evidence/round36/__pycache__/`. Not in HEAD | CPython 3.14 bytecode, timestamp-based, one file only (dir listing size 48; no `.py`, json, or receipt beside it). Observed size 20219, sha256 `8b4c882a230bc547d2deab15aa23136396332ce867637378ce8247bb8787e897`, mtime `2026-10-23 18:00:17.314118109 -0300`. `file -b`: `Byte-compiled Python module for CPython 3.14 (magic: 3627), timestamp-based, .py timestamp: Fri Oct 23 21:00:13 2026 UTC, .py size: 13126 bytes`. Header from `xxd -l 32`: magic `2b0e0d0a`, flags `0`, mtime `0x6adbcadd` = `1792789213` = `2026-10-23T21:00:13Z`, source size `0x3346` = 13126 | **DISCARD.** Header size and timestamp equal the tracked source. A fresh `py_compile` of that source (this interpreter, same path) is 20219 bytes, header16 equal to the observed `xxd`, sha256 **equal** to the observed pyc. No extra authored payload. Predates the freeze commit (`2026-10-23T18:03:56-03:00`) and this wave's dispatch files (`18:20+`). **Gone on re-check** (`ls` exit 2, no open fd); this scout did not unlink it. |
| `.ufo/waves/round-36/gen-w1-spec.py` | no | Python script, UTF-8, executable, 35627 bytes, mtime `18:20:50 -0300` (`file -b`) | **DISCARD as attempt-1.** Authored attempt-2 spec generator, not inherited research. |
| `.ufo/waves/round-36/w1-briefs/*.md` (36 files, including `CONTEXT.md` and `ScoutInherited.md`) | no | UTF-8 text briefs, mtimes `18:22:21 -0300`, sizes 1732–6147. Each passed through `file -b` in one loop | **DISCARD as attempt-1.** This wave's dispatch text. Authored, but not attempt-1 debris. |
| `.ufo/waves/round-36/w1-dispatch.json`, `w1-spec.json`, `w1-taskcall.json` | no | JSON (`file -b`), 103127 / 75754 / 81076 bytes, mtime `18:20:50`–`18:21:54` | **DISCARD as attempt-1.** Attempt-2 dispatch payloads. |
| `.ufo/waves/round-36/w1-plan.err`, `w1-run.err` | no | empty (`file -b`), 0 bytes | **DISCARD.** No content. |
| `.ufo/waves/round-36/w1/swarm-registry.json` | no | JSON, 13425 bytes, mtime `18:21:54` | **DISCARD as attempt-1.** Attempt-2 registry. |
| `.ufo/waves/round-36/w1/**` seat files that appeared after the first `file` loop (receipts, logs, row drafts; see snapshot) | no | Not passed to `file(1)`. Names are `.json`, `.jsonl`, `.md`, `.txt`, `.log`, and extensionless recorder logs. Live tree, still growing at snapshot `2026-10-23T18:26:35-03:00` | **DISCARD as attempt-1.** Attempt-2 seat output. Not inherited. |
| `.ufo/waves/round-36/measure-l1/c1-s36361.json`, `c2-s36371.json` | no | Not passed to `file(1)`. Appeared after the first porcelain (absent there) | **DISCARD as attempt-1.** Attempt-2 measure copies. |
| `.gitignore` | yes, index blob `ce68052c6c87e4899dd6f89f530c1f07632d3b37`. **Dirty after the first porcelain** (first status did not list it) | Tracked text. `git diff --numstat` = `1 0`: added line `corpus/**/__pycache__/`. HEAD commit of this path: `b6f2c0db8de4047e6518f4232da2fd3c3954cf00` at `2026-10-23T17:13:57-03:00` | **Not attempt-1 debris. Do not treat as freeze drift of round36.** Concurrent edit during this scout. Not reverted (read-only). |
| `corpus/SOURCES.md` | yes. **Dirty only on the late snapshot** (` M`, `2 0` in `git diff --numstat`) | Two inserted source rows (S069 grep `-b`/`-o`, S070 `sha256sum`) via `git diff -U1`. Not opened as a file | **Not attempt-1 debris. Outside `corpus/evidence/round36/`.** Concurrent attempt-2 edit. Not reverted. |

`git -C … diff --numstat 700bd5fcbf9abc118a6a0f078d51a2e7460c2878 -- corpus/evidence/round36` was empty (exit 0). `git diff --exit-code` against that tree for the three paths was exit 0.

## Authored-work answer

No. The only untracked object under `corpus/evidence/round36/` was a deterministic bytecode cache of tracked `c2-count.py`. Reconstructing it does not require any source that is not already in the freeze. The authored untracked files elsewhere in porcelain are attempt-2 wave dispatch and seat output, written at `18:20`–`18:26`, after the freeze commit.

## Commands (verbatim), exit, deciding line

1. `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin status --porcelain` (and `rev-parse master`, `rev-parse HEAD`, `status -sb`, `status --porcelain -uall`). Exit 0. Decides: `HEAD` = `master` = `700bd5fcbf9abc118a6a0f078d51a2e7460c2878`, detached. Untracked included `?? corpus/evidence/round36/__pycache__/` and `?? .ufo/waves/round-36/…`. `.gitignore` and `corpus/SOURCES.md` were **not** listed. `-uall` file: `corpus/evidence/round36/__pycache__/c2-count.cpython-314.pyc`.

2. `git -C … ls-tree -r --name-only 700bd5fcbf9abc118a6a0f078d51a2e7460c2878 -- corpus/evidence/round36` plus `find …/corpus/evidence/round36 -printf`. ls-tree exit 0. Decides: freeze members are only `c1-count.py`, `c2-count.py`, `claims.md`. Find then showed the pyc at 20219 bytes.

3. `git -C … diff --stat 700bd5f -- corpus/evidence/round36` then a broken `while read` over `ls-tree` (parser error: `fatal: could not open ''`), then `git -C … diff --exit-code 700bd5f --` the three paths. **Deciding exit is the diff: 0** (empty). The loop's `IDENTICAL` lines are not evidence.

4. `file -b`, `stat -c`, `sha256sum`, `xxd -l 32` on the pyc and `sha256sum` on `c2-count.py`. `file` exit 0. Decides: bytecode, magic 3627, timestamp-based, embedded `.py` size 13126 and timestamp `2026-10-23T21:00:13Z`. sha256 `8b4c882a230bc547d2deab15aa23136396332ce867637378ce8247bb8787e897`.

5. First `python3` marshal script. Exit 1. **Not evidence** — bad path (`__pycache__/__pycache__/…`), my error.

6. `git hash-object --` the three paths (exit 0; hashes equal `ls-tree` blobs), `git log -1 --format=… 700bd5f` (committer `2026-10-23T18:03:56-03:00`), `git check-ignore -v` on the pyc (matched `.gitignore:3:corpus/**/__pycache__/`, so the ignore line already existed by then), `find` of `*.pyc` / `__pycache__`. Round36 pyc was **not** in that find.

7. `git status --porcelain -uall` into `/tmp/hyaku/chousa-r36/w1/ScoutInherited-status.txt` (46 lines) then `file -b` / `wc` / `stat` per path. Loop exit 0. Decides content classes for the wave files listed above. The pyc was already absent from this status. An intermediate line `?? .gitignore` appeared; the later status superseded it with ` M .gitignore`.

8. Second `python3` marshal of the original pyc path. Exit 1. Decides: `FileNotFoundError` — directory already removed.

9. `ls -la` of `round36` and `__pycache__`. Exit 2. Decides: `__pycache__` gone; sources still `c1` 33861 (`17:57`), `c2` 13126 (`18:00`), `claims` 7924 (`18:02`). `git status --porcelain` exit 0 now included ` M .gitignore` and no longer the pyc. `git ls-files -s -- .gitignore` → `ce68052…`. `sha256sum` of the three sources as in the table. `cat -A .gitignore` showed the third line `corpus/**/__pycache__/`.

10. `find` for the pyc name under the repo and `/tmp/hyaku/chousa-r36` (exit 0, no round36 pyc), `lsof +D …/round36` (exit 1, no hits), `/proc/*/fd` readlink scan (`FD_SCAN_DONE`, no holder).

11. `git ls-tree -r --name-only HEAD -- corpus/evidence/round36 .ufo/waves/round-36`, `find …/round-36 -maxdepth 2`, `git cat-file -s` on the three blobs, `wc -c` on the worktree files. Blob sizes 33861 / 13126 / 7924 match `wc`. `git cat-file -e HEAD:.gitignore` → `tracked_in_HEAD`.

12. `git show 700bd5f:$p | cmp -s - $worktree` for the three paths. Exit 0. Decides: `CMP_IDENTICAL` three times. Then `py_compile.compile` of `c2-count.py` to `/tmp/hyaku/chousa-r36/w1/ScoutInherited/c2-count-recompile.pyc`. Exit 0. Decides: `sha_match True`, `header16_match_observed_xxd True`, `recompile_len 20219`, `co_filename` the worktree path. Then `importlib` load with `sys.pycache_prefix` set under that tmp dir (module guard at line 293 means `main()` did not run). Exit 0. The redirected pyc sha256 matched again; `beside []` (no repo `__pycache__` recreated).

13. `git diff --numstat -- .gitignore` → `1 0`. `git status --porcelain -- corpus/evidence/round36 .gitignore` → only ` M .gitignore`.

14. `git diff --stat` / `git diff --numstat` / `git diff -U1 -- corpus/SOURCES.md`. Stat exit 0: `.gitignore | 1 +`, `corpus/SOURCES.md | 2 ++`.

No packages installed. No git/jj writes. No signals.

## Artifacts

| path | sha256 |
|---|---|
| `.ufo/waves/round-36/w1/ScoutInherited/status-uall.txt` | `b87e29eaafdc38b88a2d8aaf8a159fcac2610ab287a798985e7c8367f17d2740` |
| `.ufo/waves/round-36/w1/ScoutInherited/c2-count-recompile.pyc` | `8b4c882a230bc547d2deab15aa23136396332ce867637378ce8247bb8787e897` |

Same recompile also at `/tmp/hyaku/chousa-r36/w1/ScoutInherited/c2-count-recompile.pyc` (same sha256). Stdlib pycs under `/tmp/hyaku/chousa-r36/w1/ScoutInherited/import-cache/` were not copied (import side effect; not lane evidence).

## Files opened

- `.ufo/waves/round-36/w1-briefs/ScoutInherited.md` (brief, full).
- `corpus/evidence/round36/c2-count.py` (compile + search of the `__main__` guard; not a full editorial read).
- `corpus/evidence/round36/__pycache__/c2-count.cpython-314.pyc` (`file`, `stat`, `sha256sum`, `xxd`) while it still existed.
- `.gitignore` (`cat -A`, later `git diff`).
- `corpus/SOURCES.md` only via `git diff` (not opened directly).
- `.ufo/waves/round-36/w1/ScoutInherited/status-uall.txt` (this scout's snapshot).
- The three tracked round36 paths via `git show | cmp` and `sha256sum` / `wc` (byte compare, not a text read of `c1-count.py` or `claims.md`).

## Unknowns

- Who unlinked `__pycache__` and who inserted the `.gitignore` and `corpus/SOURCES.md` lines. Not this scout. First porcelain (pyc visible, those two paths clean) vs later status (pyc gone, both paths dirty) is the bound. [INFERENCE] one concurrent writer added the ignore rule; a possibly different moment removed the directory. Identity not observed.
- Whether the original pyc was produced by `py_compile` or by `import`. Both reproduce the same bytes here, so the writer is not distinguishable. Confidence on "no extra authored bytes": high, because the sha256 matches, not because the writer was seen.
