# ScoutGateDiff — base gate vs landed gate

Access date for every file below: 2026-10-23.

**VERDICT:** 8 hunks, all accounted for. Functional hunks = 7. Untied hunks = 0. No hunk edits a matcher call so that it skips `grep_pin_define`. One behavior change sits on a named mode the frozen scenarios do not score: `--pin` under a hostile or non-hex `sha256sum` (hunk 7) now exits 2 instead of writing a poisoned `# gate_sha256=`.

## Pins

| object | sha256 | observed |
|---|---|---|
| landed `tools/research-gate.sh` | `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8` | 8258 lines; matches the brief |
| base `.ufo/waves/round-36/controls/base-gate-r36.sh` | `a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad` | 8110 lines; matches claims.md base gate |
| `git rev-parse master` and `HEAD` | `700bd5fcbf9abc118a6a0f078d51a2e7460c2878` | both; wave base |

## Commands

1. `sha256sum` of both gates, `wc -l`, `mkdir -p` of the scratch dirs, `git rev-parse master` and `HEAD` (cwd the lane). Exit 0. Deciding lines: hashes `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8` and `a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad`; both rev-parse lines `700bd5fcbf9abc118a6a0f078d51a2e7460c2878`.

2. `diff -u` base gate vs landed gate, redirected to `/tmp/hyaku/chousa-r36/w1/ScoutGateDiff/gate.diff`, then `echo EXIT:$?`, `wc -l`, `grep -c '^@@'`, `sha256sum`. Diff status `EXIT:1` (files differ). Deciding line: hunk count `8`; diff 226 lines; sha256 `6c7a3797c315fdf013a6b638bd94c603c1b036ab04f43761f373bad91e51be2a`.

3. Eval cell walked each `@@` hunk and checked new-file line counts. No error. Deciding line: `NHUNKS 8` and the added spans in the table.

4. `cp -a` that diff into `.ufo/waves/round-36/w1/ScoutGateDiff/gate.diff`, then `sha256sum` and `wc -c`. Exit 0. Deciding line: same sha256, 11757 bytes.

## Files opened

- `corpus/evidence/round36/claims.md` (full; erratum tail empty).
- `tools/research-gate.sh`: symbol grep plus the pin wrapper, `json_unescape`, the claims hash site, `gate_canonical_capture`, `gate_drift_line_id`, `run_pin`, selftest cases 257-261, and mode dispatch after `grep_pin_init`.
- `.ufo/waves/round-36/controls/base-gate-r36.sh` via symbol grep.
- `corpus/evidence/round36/c1-count.py` header and S1-S14 names.
- `corpus/evidence/round35/claims.md` erratum 13 (lines 268-276).
- `/tmp/hyaku/chousa-r36/w1/ScoutGateDiff/gate.diff` (full, 226 lines).

Not opened: `c2-count.py`, `argv-witness.py`, `mechanism-witness.py`. No hunk touches those files or the grep pin, so none serves C2.

## Hunk table

Landed file `tools/research-gate.sh`. Changed = added lines only. Span = full `@@` hunk including context. One class per hunk.

| hunk | changed lines (span) | class | tied item | risk |
|---|---|---|---|---|
| 1 | 422-444 (419-447) | functional | R3, C1 S11 | New `sha256_hex_file`: first executable of `/usr/bin/sha256sum` or `/bin/sha256sum`, accept only 64 lowercase hex, else rc 1. Lines 422-431 are the comment. Not a matcher site. Second caller is `--pin` (hunk 7), which S11 does not score. |
| 2 | 1449-1458 (1446-1461) | functional | R4, C1 S12 | Inside `json_unescape` (starts 1442). Comment 1449-1456; executable change is `local LC_ALL=C` and `export LC_ALL` at 1457-1458. Function-local. Matcher locales were already `LC_ALL=C` at 1723, 1735, 1757, 1780, 1802; this hunk does not touch them. |
| 3 | 1490-1492 and 1495-1497 (1487-1500) | functional | R4, C1 S12 | Replaces `printf %b "\u$hex"` and the `?` fallback. U+0000..007F and surrogates stay (1486-1489). Other non-surrogate BMP code points become hand-built UTF-8 for every `json_unescape` caller, under every locale, not only S12's C-locale span. That is R4's hand encode; the claims limit declines locale claims outside this function. |
| 4 | 3705-3706, 3708 (3702-3711) | functional | R3, C1 S11 | `verify-all --json` manifest hashes call `sha256_hex_file`; empty still exits 2. Stderr now says unavailable or non-hex. Named mode. |
| 5 | 3922 (3919-3925) | functional | R1, C1 S13 | Adds `-u CHOUSA_GREP_PIN_ECHO` on the `env` inside `gate_canonical_capture`, which `run_pin` calls at 4051. Production `--pin` capture (`>capture.txt 2>&1`), not a selftest. The capture child no longer embeds stderr `GATE_GREP:`. The parent `--pin` process still echoes when the flag is set (417-418). |
| 6 | 3952 (3949-3955) | functional | R2, C1 S14 | `gate_drift_line_id` gains `GATE_GREP:*) printf 'GATE_GREP'`. Default `*) printf 'LINE'` remains at 3956, outside the hunk. That default is what S14 used to report as `-LINE`. |
| 7 | 4057, 4059 (4054-4062) | functional | R3 (hex contract on the `run_pin` caller, not the manifest) | Unnamed failure path. Base `run_pin` used `sha256sum \| cut` and accepted any non-empty token (base 4019-4021). A PATH shim can no longer write a non-hex `# gate_sha256=` and exit 0; missing or non-hex now exits 2. S11 scores only `verify-all --json`. R3's sentence names the manifest. The diagnostic also drops the word `--pin`. |
| 8 | 8033-8142 (8030-8145) | selftest case | R5 (cases 257-261); exercises S12/R4, S11/R3, S13/R1, S14/R2 | Not a production mode. Case count is `cases=$((cases + 1))` from `cases=0` at 4146; no stale literal 256. New `grep -qE` / `grep -q` at 8094-8096 and 8119 are bare `grep` and run only after `grep_pin_init` (8208, then `selftest) run_selftest` at 8226), so they hit `grep() { "$GREP_BIN" "$@"; }`. Not span-matcher sites; not a wrapper bypass. |

Removed text: old `printf %b "\u…"` and `out+='?'` (hunk 3); PATH `sha256sum | cut` on the manifest plus the old stderr (hunk 4); the capture `env` line without the pin-echo scrub (hunk 5); PATH `sha256sum | cut` and the `--pin sha256sum unavailable` message (hunk 7).

## Flags

Unnamed-mode behavior. The only edit that changes a gate mode on a path claims.md does not name is hunk 7: `--pin` when `sha256sum` is missing or returns non-hex. `--pin` is named by S13 and S14, but those cells do not score the header hash. Hunks 2-3 stay inside `json_unescape` (R4). Hunks 4-6 are S11, S13, and S14. Hunk 8 is selftest only.

Matcher vs pin wrapper. No hunk modifies `grep_pin_define`, `grep_pin_init`, or `RESEARCH_GATE_GREP` (still 356-420). No new production line calls `grep`, `command grep`, or a filesystem grep. Hunk 5's `grep -c` at 3925 is unchanged context. Hunk 8's greps go through the wrapper. C2's argv channel is that pre-existing wrapper; this diff does not add or weaken it.

Not a hunk, so not untied. Claim-body hashing at 2002 is still `sha256sum < "$path" | cut`, with a hex check at 2004 (`sha_actual=unreadable`). Round-35 erratum 13 already split that path from the manifest. A 64-hex lie on PATH still poisons a claim `sha256` pin. R6 (SKILL.md ledger) has no line in this diff.

Stale comment, not a behavior change. Header lines 264-265 still list drift ids as "GATE MANIFEST VERIFY_ALL VERDICT SECTION:<name> FINDING:<id> LINE" and omit `GATE_GREP`, which hunk 6 now emits. `MANIFEST-MARKER` was already absent from that sentence.

## Counts

- Hunks: 8.
- Functional: 7 (hunks 1-7).
- Selftest case: 1 (hunk 8).
- Comment-only: 0. Whitespace-only: 0.
- Untied: 0. Each functional hunk is R1, R2, R3, or R4 and the C1 arm that repair serves. Hunk 7 is R3's contract on the `--pin` caller; the unnamed poison path is the risk, not an untied hunk.
- C2 hunks: 0. R5 is hunk 8. R6 hunks: 0.

## Artifact

`.ufo/waves/round-36/w1/ScoutGateDiff/gate.diff` sha256 `6c7a3797c315fdf013a6b638bd94c603c1b036ab04f43761f373bad91e51be2a` (11757 bytes).
