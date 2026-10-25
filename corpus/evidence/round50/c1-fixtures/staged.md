# staged package (campaign schema)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S010 | New doc A — https://example.test/new-a | docs | A | scope a | section a | what row a teaches | mined | 2026-10-23 | 90d | corpus/knowledge/a.md |
| S011 | New doc B — https://example.test/new-b | docs | B | scope b | section b | what row b teaches | queued | 2026-10-25 | 2026-12-01 — re-verify after release | corpus/knowledge/a.md |
| S012 | The held doc — https://example.test/held | docs | A | held scope | section 1 | what the held row teaches | mined | 2026-10-25 | 90d | corpus/knowledge/b.md |
| S013 | New doc C — https://example.test/new-c | docs | B | scope c | section a \| b | what row c teaches | mined | 2026-10-25 | on-release | — |
