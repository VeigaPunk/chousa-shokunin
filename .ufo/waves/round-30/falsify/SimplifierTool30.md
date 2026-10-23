# SimplifierTool30 — round-30 WAVE 2 FALSIFY, simplifier attack on `tools/quote-reopen.py`

VERDICT: pass — C1 and C2 hold on the landed tool under my own runs, and the round-30 diff carries 10 provably removable lines plus 3 inert same-line simplifications (all scored clean after removal).

## Baseline observed (lane tool, frozen counters, hashes verified first)

- `sha256sum` matched claims: c1-count.py `5b312d84…9d6e6`, c2-count.py `0a59e373…f88f`, qr_harness.py `e2be0dd1…50d4`, tools/quote-reopen.py `47a657e7…1201`, tip `a9d3a05a`.
- `python3 corpus/evidence/round30/c1-count.py --receipt .ufo/.../SimplifierTool30/receipt-baseline-c1.json` → `QUOTE_REOPEN_HEADLESS_MATCH=106/106`, exit 0.
- `python3 corpus/evidence/round30/c2-count.py --receipt .../receipt-baseline-c2.json` → `QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27`, exit 0 (6.15 s).

## Deletions proven behavior-preserving (scratch copies, both counters)

Scratch: `/fast/scratch/hyaku/chousa-r30/w2/SimplifierTool30/` (clone of the lane at `a9d3a05a`, GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset; mutants `m_all.py` 549 lines, `m_full.py` 546 lines vs landed 556). Line numbers below are landed-tool lines.

1. Lines 310-312 → `raise last`: `_check_address` raises `_Refuse` on empty `addrs` (line 246-247), so `_dial`'s `addrs` is never empty; the loop always sets `last` or returns. The guard `if last is not None:` is always true and `raise _Refuse("no validated address to connect to")` is unreachable. Dead: 2 statements.
2. Lines 268-271 → `conn = http.client.HTTPConnection(server_hostname or addrs[0], port, timeout=timeout)`: `_dial` never calls `conn.connect()` (it dials manually and assigns `conn.sock`), so the HTTPSConnection/HTTPConnection choice and the `kw` dict are inert; TLS happens in the explicit `context.wrap_socket` below. Host header still comes from `conn.host` (the hostname), unchanged.
3. Line 388 `watchdog = None`: write-only init; `watchdog` is only touched at lines 394-396, after a successful `_dial`.
4. Line 449 `float(DEADLINE)` → `DEADLINE`: module default is `30.0` (line 52) and the harness sets `mod.DEADLINE = float(...)` (qr_harness.py:124); the conversion changes no value on any path.
5. Line 362 `getattr(resp, "length", None)` → `resp.length`: `resp` is always `http.client.HTTPResponse` (line 404 `conn.getresponse()`); `length` is a defined attribute (None or remaining int), so truthiness is identical.
6. Lines 387+393 `holder = [None]` / `holder[0] = conn.sock` → `_kill(conn.sock)` directly: `holder[0]` is assigned exactly once, between dial and Timer creation, never reassigned, so capture-at-fire and capture-at-creation coincide here. 3 lines.

Scores (fresh seed each run; `--tool <mutant>`; run from the scratch clone root):

| mutant | C1 | C2 run 1 | C2 run 2 |
|---|---|---|---|
| baseline lane tool | 106/106 exit 0 | 27/27 exit 0 | — |
| m_all (1-5) | 106/106 exit 0 | 27/27 exit 0 (6.13 s) | 27/27 exit 0 (5.68 s) |
| m_full (1-6) | 106/106 exit 0 | 27/27 exit 0 (6.22 s) | 27/27 exit 0 (6.24 s) |

Receipts: `receipt-mall-c1.json`, `receipt-mall-c2-run{1,2}.json`, `receipt-mfull-c1.json`, `receipt-mfull-c2-run{1,2}.json` in this directory. Both mutants compile (`python3 -m py_compile`, ok). Diffs vs landed: `m_all` −7 lines, `m_full` −3 more.

## Listed, not scored (same-line or style-only; left out of mutants)

- Line 265 `server_hostname or addrs[0]`: the `or` fallback is dead — the sole caller (line 391-392) always passes `server_hostname=host` with a non-empty host from `_check_url`. Kept so `_dial` stays total for hypothetical callers.
- Lines 305-307 `sock.close()` inside the watchdog trip: redundant with the `finally: conn.close()` (line 455-458); kept as belt-and-braces with the `shutdown` wake.
- `_dial`'s unused defaults (`timeout=None, context=None, server_hostname=None`): the single caller passes all of them.

## Checked and NOT removable (load-bearing)

- `HEAD_ELEMENTS` membership of `base/basefont/bgsound/link/meta`: without it those tags would end the head; they must not.
- The `hdeep`/`noframes` branch: `noframes` is not in `SKIP`, so its content must drop inside head and survive outside; `handle_endtag` line 137-138 maintains it.
- `handle_data`'s `not self.skip` / `not self.hdeep` guards (lines 143-147): title/noframes content inside head must not end the head.
- Lines 359-364 (end-of-stream deadline check + declared-length check): this is the `bd43bd53` fix; removing them re-opens the 24/27 end-of-stream-at-deadline failure recorded in claims.
- `_dial`'s manual numeric-address connect and the watchdog trip itself: they are the C2 surface (one-resolution and total deadline); the sibling seat MutNoWatchdog attacks the trip.

## Gap observed (an addition, not a deletion — flagged for L1, not applied)

The watchdog `threading.Timer` is never cancelled: no `watchdog.cancel()` exists anywhere in the file. Each completed hop leaves a daemon Timer sleeping up to `remaining` seconds, then firing on an already-closed socket (`shutdown` raises OSError, swallowed). Harmless to both counters [INFERENCE: bounded, roughly ≤3 timers per item concurrent] and invisible to the predicates, but a `watchdog.cancel()` in the `finally` would bound the thread lifetime and let `watchdog` keep a reason to exist. Related: with no cancel, the line-388 init removed above is provably write-only.

## Server proof and tree integrity

- `xd://lsp` unavailable: probe returned `No such tool: xd://lsp. Mounted devices: ast_edit, debug.` Recorded; grep fallback used. `_dial(`/`_kill(` occur only in `tools/quote-reopen.py` (lines 260, 293, 391, 394) and in `.ufo` wave copies of the same tool; the harness imports the candidate via `spec_from_file_location` and touches only `main` and `DEADLINE` (qr_harness.py:119-126). No module outside the tool imports its private helpers.
- Lane tree: `sha256sum tools/quote-reopen.py` still `47a657e7…1201`; I edited nothing in the lane. `git status --porcelain` shows `M LOG.md`, `M SCORECARD.md`, and `__pycache__` dirs whose mtimes (00:34:39-00:41:14) predate my first run (first receipt 00:43:15) — pre-existing from other seats, not mine.
- No tools installed or updated this seat. All counter processes exited; `pgrep` for `c1-count|c2-count|qr_harness` returned nothing.
