# Draft registry row

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S0NN | Python socket documentation — https://docs.python.org/3/library/socket.html#socket.create_connection | docs | A | documented `create_connection` behavior for non-numeric hostnames; not a guarantee of DNS pinning or per-hop validation | section `socket.create_connection`, Python 3.15.1 documentation | For a non-numeric hostname, `create_connection` resolves for AF_INET and AF_INET6 and tries addresses in turn, illustrating why a prior address check does not pin a later hostname-based connection. | mined | 2026-10-23 | on-release | corpus/knowledge/quote-reopen-r30.md |

## Located quote

> “it will try to resolve it for both AF_INET and AF_INET6, and then try to connect to all possible addresses in turn”

Section: `socket.create_connection` (Python 3.15.1 documentation). Accessed 2026-10-23. The quote is 22 words.

Supports C2, tool contract v2 item 3 (one resolution per hop).
