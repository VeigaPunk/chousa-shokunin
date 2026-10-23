# Reopen S060 — Python fcntl docs

Axes: HTTP identity of `https://docs.python.org/3/library/fcntl.html` against the S060 anchor; whether `scope`/`teaches` and `corpus/knowledge/manifest-append-lock-r32.md` say only what that page says.

## Fetch (2026-10-23)

Command (exit 0): `timeout 90 curl --silent --show-error --max-time 60 --connect-timeout 15 --max-filesize 900000 --output /fast/scratch/hyaku/chousa-r32/w2/ReopenS060/fcntl.html --dump-header /fast/scratch/hyaku/chousa-r32/w2/ReopenS060/fcntl.headers --write-out 'HTTP_STATUS=%{http_code}\nREDIRECT=%{redirect_url}\nSIZE=%{size_download}\nURL_EFFECTIVE=%{url_effective}\n' https://docs.python.org/3/library/fcntl.html`

- `HTTP_STATUS=200`, `REDIRECT=` empty, `SIZE=50928`, `URL_EFFECTIVE=https://docs.python.org/3/library/fcntl.html` (no redirect).
- Headers: `date: Fri, 23 Oct 2026 07:26:20 GMT`, `last-modified: Fri, 23 Oct 2026 07:00:32 GMT`, `content-length: 50928`, `content-type: text/html`.
- `sha256sum` of the live body: `0189dd49e1aecde4220339ab0b72b80139b5b4837d060857eb052daba90b1e56`.
- `sha256sum` of `.ufo/waves/round-32/w1/ScribeSourceC1/fcntl.html`: `025727ff2f271b3b8768f1315487cc1e931dbf03de8ab56f12e5adb4b8e3dda3` (the row's `025727ff…3dda3`). Both files are 50928 bytes.
- `diff` of those two files is one line: `Last updated on Oct 23, 2026 (06:37 UTC).` → `(06:57 UTC).` (live HTML line 591).
- `grep -cF` and `grep -oF` of `Acquire an exclusive lock.` on the live body: `1`. Same count on the w1 body: `1`. Live location: line 411, `<p>Acquire an exclusive lock.</p>` under `id="fcntl.LOCK_EX"` (lines 409–412). Quote (5 words), URL above, access date 2026-10-23.
- Title line 20 and nav line 170 say Python 3.15.1. A scan of the live text found no `advisory` and no `NFS`. `flock(2)` occurs twice (line 383 and the man-page link).

## Row (`corpus/SOURCES.md:70`)

HTTP 200 matches. The body hash does not.

Anchor sentence "Python 3.15.1 documentation as served 2026-10-23 (HTTP 200, body sha256 `025727ff…3dda3`)" matches the w1 snapshot and does not match the body served at 07:26:20 GMT the same day. The lesson gate repeats that hash (`corpus/lessons/round-32.md:60-61`).

Scope (flock on an fd; meaning of `LOCK_EX`; not flock(2) lifetime, advisory, or NFS): the page's `fcntl.flock` (lines 378–387) says the operation is performed on file descriptor `fd`, and that a file object providing `fileno()` is accepted, then "See the Unix manual flock(2) for details." It does not state lock lifetime, advisory behaviour, or NFS, so the exclusions are not contradicted. `LOCK_EX`'s sentence is on the page, but it is listed as a `cmd` of `fcntl.lockf` (function opens line 389; "cmd is one of the following values" lines 394–395). `fcntl.flock` ends at line 387 and never names `LOCK_EX`.

Teaches: "`flock()` takes a file descriptor (or an object with `fileno()`)" is lines 381–382. "`LOCK_EX` acquires an exclusive lock" is line 411, under `lockf`. The em-dash "the call the round-32 C1 counter and oracles use" is not on the page. The counter does call it (`corpus/evidence/round32/c1-count-v2.py:249` `fcntl.flock(fd, fcntl.LOCK_EX)`). Oracle C does too (`.ufo/waves/round-32/w1/OracleC1B/oracles.patch:80-88`). Oracles A and B are `flock -x` (flock(1)), not that Python call. [INFERENCE] "oracles" plural over-includes A and B. The page never shows `flock(..., LOCK_EX)` as one signature.

## Knowledge (`corpus/knowledge/manifest-append-lock-r32.md`)

S060 is cited at lines 3 and 23–24, and disclaimed at 29–30.

- Line 3 names `fcntl.flock(fd, operation)` and `LOCK_EX`. Both symbols are on the page.
- Lines 23–24: "S060 documents the call shape this relies on: `flock()` takes a file descriptor, and `LOCK_EX` acquires an exclusive lock." Both clauses are on the page (the second under `lockf`). The "this" of that paragraph is the gate's `flock -x` (lines 18–22). S060 documents Python `fcntl.flock` and points at flock(2); it does not document flock(1) `-x`. That identification is not marked `[INFERENCE]`.
- Lines 29–30 mark the sibling-lock rationale `[INFERENCE]` and say S060 does not state it. That disclaimer matches the page.
- Line 44 "flock(2) locks are advisory" is not cited to S060. The page does not say it.

## Verdict

**BROKEN** — the anchor's body hash is not the body a same-day re-GET returns (`0189dd49…1e56` vs `025727ff…3dda3`). Status 200 matches. The only byte change is the docs footer clock, so the quote, the flock/`fileno` sentence, and the `LOCK_EX` sentence still match. The hash pin in `SOURCES.md:70` and `lessons/round-32.md:60-61` does not.

Limits: one GET, no second host, no `Accept-Encoding` variant (`content-length` equals the saved size). No C1/C2 counter run. No install.
