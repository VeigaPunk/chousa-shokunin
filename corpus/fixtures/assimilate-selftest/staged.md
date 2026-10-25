# staged package (campaign schema)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S010 | New doc A — https://example.test/new-a | docs | A | scope a | section a | what row a teaches | mined | 2026-10-23 | on-release | corpus/knowledge/a.md |
| S011 | Body-only doc B — https://example.test/new-b | docs | B | scope b | section b | what row b teaches | queued | 2026-10-25 | 90d | — |
| S012 | The held doc — https://example.test/held | docs | A | held scope | section 1 | what the held row teaches | mined | 2026-10-25 | 90d | corpus/knowledge/b.md |
| S013 | New doc C — https://example.test/new-c | docs | B | scope c | section a \| b | what row c teaches | queued | 2026-10-25 | 2026-12-01 — re-verify after release | — |
| S014 | Piped held doc — https://example.test/piped | docs | B | piped scope | section 5 | what the piped held row teaches | mined | 2026-10-25 | 90d | corpus/knowledge/b.md |
| S015 | Other doc — https://example.test/other\| alt | docs | A | other scope | section 2 | what the other row teaches | mined | 2026-10-25 | 90d | corpus/knowledge/b.md |
| S016 | Body-only doc D — https://example.test/new-d | docs | B | scope d | section d | what row d teaches | mined | 2026-10-25 | 90d | — |
