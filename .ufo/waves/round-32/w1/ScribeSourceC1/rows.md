# Draft source row — Python `flock()`

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S060 | Python `fcntl` documentation — https://docs.python.org/3/library/fcntl.html | docs | A | Python's documented `fcntl.flock()` descriptor/file-object interface and `LOCK_EX` meaning; not Unix `flock(2)` lock-lifetime, advisory-lock, or NFS semantics | `fcntl.flock` (descriptor and operation, lines 379–386) and `fcntl.LOCK_EX` (lines 409–412); Python 3.15.1 documentation as served 2026-10-23 | Python documents `flock()` on a file descriptor (or file object providing `fileno()`); `LOCK_EX` acquires an exclusive lock | queued | 2026-10-23 | on-release | — |

Requested intended use: `corpus/knowledge/manifest-append-lock-r32.md`. This target was not present when checked, so it is not claimed as an existing citation and the contract-shaped row remains `queued` with `used-by` `—`. If the knowledge entry is later present and cites S060, its actual relative path can be recorded and status changed to `mined`.

## Fetch and quote evidence

- GET URL: `https://docs.python.org/3/library/fcntl.html`; `curl` returned HTTP status `200` (no redirect following).
- Fetched body: `fcntl.html`, 50,928 bytes; SHA-256 `025727ff2f271b3b8768f1315487cc1e931dbf03de8ab56f12e5adb4b8e3dda3`.
- Located quote (5 words): “Acquire an exclusive lock.” Source: `fcntl.LOCK_EX`, fetched-body line 411; copied verbatim.
- Grep command: `grep -nF 'Acquire an exclusive lock.' /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/ScribeSourceC1/fcntl.html` — output line 411 once. Count command returned `1`: `grep -oF 'Acquire an exclusive lock.' /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w1/ScribeSourceC1/fcntl.html | wc -l`.
- Existing-row sweep: `grep` for `docs.python.org/3/library/(fcntl.html|os.html#os.open)` in lane `corpus/SOURCES.md` returned no matches; neither URL already has a row.
