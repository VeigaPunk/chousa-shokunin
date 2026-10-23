## Round-29 additions (appended 2026-10-23; criteria 1-22 unchanged)

23. **Digit spacing and lane prose.** New lane prose separates digits from words
    and contains no custody vocabulary. Check:
    `python3 corpus/evidence/round29/prose-check.py <files>` exits 0 on new prose. This
    criterion fails when the check exits nonzero for a glued digit token or a
    custody term. — `corpus/lessons/round-28-verifier-spotcheck.md`, D1 and D2.
24. **Pre-data control screen.** Before any data seat, score the claim's counter
    against do-nothing, all-false, junk, no-reader, and label- or id-keyed
    shortcut controls; keep a committed receipt for each. This criterion fails
    if a control has no committed pre-data receipt or if any control reaches the
    counter; the latter voids the design. — `.ufo/waves/round-29/controls/`;
    `corpus/evidence/round29/claims.md` (frozen void rule).
25. **Re-open before citation.** Before a round cites a located quote, re-open
    it against the live URL in `corpus/SOURCES.md` with
    `python3 tools/quote-reopen.py verify`. Record any `ABSENT` or
    `UNREACHABLE` verdict, not hide it. This criterion fails if live re-opening
    is skipped or either verdict is omitted. — `corpus/evidence/round29/claims.md`
    (frozen tool contract).
