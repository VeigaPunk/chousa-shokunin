# ReviewRegistryReorder — C3 stale columns and widths

Assigned scope: stale registry columns after line breaks, reordered-header false positives/negatives, and header/delimiter width matching. Static review only; base observed at `64eec5d41c7cf7f17f5ce1e968e28b3769952596`.

## Findings

1. **Stale column indices survive a non-pipe break.** In `tools/research-gate.sh:2412-2415`, a non-pipe line clears `header_candidate` but leaves `id_col`, `status_col`, and `usedby_col` intact. The later reset at `2453-2467` does not help after that break: the next pipe line reuses the old indices instead of deriving them from its own names. The r26 receipt `falsify/FRegistryHeaderless.md:41-83` records the resulting stale-header acceptance (S01/S02), reordered-header false negative (S04: actual `queued` status hidden), and false positive (S05: clean row reported non-mined).

   **Suggested change:** invalidate the candidate and all three column indices together whenever a non-pipe line breaks a header/table candidate. A named header must supply the indices used by its own immediately following, valid delimiter; never let an earlier table-like line bind later rows.

2. **Delimiter width is not checked against header width.** `tools/research-gate.sh:2443-2451` validates each delimiter cell's syntax and accepts the row without comparing its cell count with the candidate header's count. The same r26 receipt records G01/G02 (`FRegistryHeaderless.md:85-93`): a three-column named header followed by two- or four-cell separators is accepted, although neither separator has matching width.

   **Suggested change:** retain the candidate header width and accept it only when the valid delimiter row has exactly that many cells. Keep the existing cell grammar and column-name mapping; this finding does not assert a broader Markdown/fence grammar.

## Concrete synthetic acceptance oracle

Use only newly generated temporary registry/entry files, with a valid entry (`source: S001`, dated `verified-at`, `recheck: 90d`) and `used-by` exactly equal to its root-relative path. Check exit status, finding identity/multiplicity, and verdict-line count—not just parser success:

- **No stale header:** registry has `| id | status | used-by |`, then a blank or prose break, then `| a | b | c |`, a three-cell delimiter, and a data row. With no fresh qualifying named header, expect exit 2, the no-table usage diagnostic, and zero `^RESEARCH_GATE: ` lines.
- **Reordered-header false negative control:** old named header, prose break, then `| id | note | used-by | status |`, matching four-cell delimiter, and `| S001 | note | corpus/knowledge/e.md | queued |`. Expect exactly one `META_SOURCE_NOT_MINED` for S001 and a drift verdict (not CLEAN); the real `queued` status must not be hidden by stale indices.
- **Reordered-header false positive control:** old named header, prose break, then `| id | note | status | used-by |`, matching four-cell delimiter, and `| S001 | - | mined | corpus/knowledge/e.md |`. Expect CLEAN with no registry finding; a note in the former status position must not be treated as status, and the actual used-by cell must retain its exact-path semantics.
- **Width negatives:** separately test a three-cell named header followed by two-cell and four-cell delimiter rows (with an otherwise valid data row). Each must exit 2 with the no-table diagnostic and zero verdict lines.
- **Matching-width positives:** retain three/three and reordered four/four well-formed tables; a mined S001 row with exact used-by must remain CLEAN. This prevents a fix from rejecting valid reordered columns or changing existing used-by behavior.

The paired reordered controls are important: a clean result for only one ordering can still conceal the opposite calibration failure. Include each case in persisted independent controls with exact expected findings and counts. Do not claim they pass until the integrating seat runs the requested checks.

## Verification gaps

No tests, selftests, differential scripts, or other verification were run. The exposed tool inventory has no LSP route (also noted in the r26 `build/ExecC3Registry.md:22`); the code locations above are from direct reads of the base source, not semantic LSP results. No tools were installed.
