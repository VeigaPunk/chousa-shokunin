# Round 30 README and scorecard drafts

Draft only; these are proposed documentation edits, not landed lane files or measured outcomes.

## `corpus/README.md` coverage-map row

| `knowledge/quote-reopen-r30.md` | Round 30 quote re-open contract v2: head suppression starts only at `<head>` and ends at the specified HTML boundary (including omitted `</head>`); fetch contract uses one total per-URL deadline and one validated DNS resolution per hop | `evidence/round30/claims.md`; `evidence/round30/c1-count.py`; `evidence/round30/c2-count.py`; `evidence/round30/qr_harness.py`; round-30 measurement receipts when present; note source IDs remain pending because its `S0NN` entries are placeholders |

## `corpus/README.md` frontier paragraph

## Round 30 frontier disposition (2026-10-23)

New contract ground: v2 starts head suppression only at a `<head>` start tag and ends it at the first `</head>`, `<body>` start tag, start tag outside the allowed in-head set, or non-whitespace text outside those elements. It also requires one total `DEADLINE` for each registry-URL fetch, including redirects, headers, body reads and the retry, and one DNS resolution per hop followed by connection to a validated global address (`knowledge/quote-reopen-r30.md`, `tools/quote-reopen.py`). The C1 and C2 counters run in a loopback harness; they do not establish an external fetch or per-hop address provenance beyond the frozen C2 routed-set predicate. Fill in measured results from receipts before claiming either target was met. Remaining candidates: 2xx challenge pages, pages without a `<head>` start tag, PDF sources, prefix/suffix disambiguation, and the L0 fetch-scope answer. Keep the round-29 path-denylist debts carried unless a separate disposition records otherwise.

## `SCORECARD.md` Round 30 section skeleton

## Round 30 — quote re-open capability (two claims: C1 coverage, C2 operability)

Frozen claims and counter definitions: `corpus/evidence/round30/claims.md` (design v4).

| claim / axis | before → after | counting command (lane root) | verdict |
|---|---|---|---|
| C1 coverage, head-boundary class | `QUOTE_REOPEN_HEADLESS_MATCH=78/106` → `<measured>` | `python3 corpus/evidence/round30/c1-count.py` | pending measurement |
| C2 operability, fetch bounds | `QUOTE_REOPEN_FETCH_BOUND_MATCH=9/20` (historical v2 baseline; v4 baseline is `12/27`) → `<measured>` | `python3 corpus/evidence/round30/c2-count.py` | pending measurement |

Counting commands with optional receipt outputs:

- `python3 corpus/evidence/round30/c1-count.py [--tool PATH] [--receipt OUT.json]`
- `python3 corpus/evidence/round30/c2-count.py [--tool PATH] [--receipt OUT.json]`

Capabilities-row update text:

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| quote re-open | Contract v2 specifies the HTML head boundary, a total per-URL deadline covering redirects, headers, body reads and the retry, and one validated DNS resolution per hop with the hostname retained for `Host` and TLS; the existing verdict set remains `VERBATIM`, `ABSENT`, `TOO_LONG`, `NO_SOURCE`, or `UNREACHABLE` | `corpus/evidence/round30/claims.md`; C1/C2 counter receipts; `corpus/knowledge/quote-reopen-r30.md`; source IDs pending assignment | 29 (capability first acquired in round 29; contract update in round 30) |

## Planned — round 31 (not started)

Candidates, not commitments: 2xx challenge pages; pages without a `<head>` start tag; PDF sources; prefix/suffix disambiguation; and the L0 fetch-scope answer.

## Reconciliation note for integration

The user-requested C2 `before` value conflicts with the frozen current-design record. The requested `9/20` is the round-30 C2 v2 historical baseline; `claims.md` design v4 states C2 `12/27` twice before data. The table preserves `9/20` as historical rather than presenting it as the v4 baseline. The round-30 knowledge-note source rows are still `S0NN` placeholders and have not been assigned. Replace `<measured>` only from the corresponding measured receipts.
