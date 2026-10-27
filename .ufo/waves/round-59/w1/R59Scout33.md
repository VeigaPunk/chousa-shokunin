# R59Scout33 — offline data walk

## Observed

- The requested frozen claims file `corpus/evidence/round59/claims.md` is absent in the lane filesystem: direct read returned not found. The lane corpus lists `corpus/evidence/round58/claims.md` instead; this report does not treat that as a substitute for frozen R59 claims.
- Round-59 census snapshot `corpus/evidence/round59/census-start.txt` records five duplicate-source warnings (S051, S053, S073, S074, S075), then `ok` for `corpus/SOURCES.md` and `exit=0`.
- R59 control receipt `corpus/evidence/round59/controls/c1-before.txt` is decisively negative for the prior builder battery: safe legs EMPTY_OK, REBUILD_OK, ESCAPE_ENTRY and HELDOUT_OK pass, but FOREIGN deletes the foreign file; SYMLINK_OUT writes through target; SYMLINK_CACHE accepted; MANY_QUOTES accepted; FIFO, DEVZERO, FAT_RAW refuse for unrelated reasons and lack expected refusal reasons. Summary is `OK=4/4 REFUSE=0/7 ... C1=FAIL`, exit 1.
- `corpus/evidence/round58/claims.md` documents C1's bounded target battery and explicitly limits its claim (text-size caps and broader races excluded). Its C2 is independent of C1 and uses pinned round-55 builder/capture-text; it claims grounded new GB3469 carrier-alphabet knowledge from S101, not present-day standards validity.
- `corpus/QUALITY.md` (lines 492–494, 725–728) records the still-open L0 fetch-scope question `8d77e6c1`; `corpus/SOURCES.md` describes prior rounds' deliberate offline-only search boundaries. Round 59 has no live fetch authorization evidenced here.

## Bounded inference

The R59 evidence tree is at least partially assembled, but its claim contract is unavailable at the named path. The available before-receipt demonstrates concrete operability vulnerabilities/refusal misclassification in the baseline; it does not establish any R59 post-change outcome. The census warnings are source-registry duplicate URL warnings, not evidence that source text is duplicated or invalid.

## Unresolved

Need the actual frozen R59 claims artifact/path and any R59 post-control receipts before assessing closure or new claim scope. No LSP server evidence was sought: this assigned walk concerns corpus artifacts, not source symbol semantics. No external fetch was made.