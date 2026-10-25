# SOURCES — where selftest learns

## Registry

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S001 | Held doc — https://example.test/held | docs | A | held scope | section 1 | what the held row teaches | mined | 2026-01-01 | 90d | corpus/knowledge/k.md |
| S002 | Other doc — https://example.test/other | docs | A | other scope | section 2 | what the other row teaches | mined | 2026-01-01 | 90d | — |
  | S011 | Indented doc — https://example.test/indented | docs | B | indented scope | section 3 | an indented row the staged set collides with | queued | 2026-01-01 | 90d | — |
| S012 | Last doc — https://example.test/last | docs | A | last scope | section 4 | the highest lane id | mined | 2026-01-01 | 90d | — |
| S020 | Piped doc \| alt — https://example.test/piped | docs | B | piped scope | section 5 | the row whose source cell holds an escaped pipe | mined | 2026-01-01 | 90d | — |
