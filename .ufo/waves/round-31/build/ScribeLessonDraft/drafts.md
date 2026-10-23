# Round 31 — claim line and source revision binding

Base `be7b8d8d54962286417465a305fd9a1a7b3b1525`.

This round changes only the lane-local claim-vs-source gate, `tools/research-gate.sh verify-claims` (no network). `tools/quote-reopen.py` is out of scope.

## Claims

- **C1 — coverage, line binding.** An optional claims-JSONL string field `"line"` names `N` or `N-M`. A boundary-delimited span occurrence binds only when it starts on line N and ends on N (or M for a range); a present span that does not bind is `observed=mislocated` with `CLAIM_LINE_MISMATCH`. A malformed value is `observed=invalid`; absent field preserves prior behavior. Frozen counter: `python3 corpus/evidence/round31/c1-count.py`; target `LINE_BINDING_MATCH=120/120` (base before-value 50/120).
- **C2 — operability, source revision.** An optional claims-JSONL string field `"sha256"` pins the exact source-file bytes and must be 64 lowercase hexadecimal characters. A well-formed mismatch is `observed=stale` with `CLAIM_SOURCE_REVISION_MISMATCH`, before the span check; malformed is `observed=invalid`; absent field preserves prior behavior. Frozen counter: `python3 corpus/evidence/round31/c2-count.py`; target `REVISION_BINDING_MATCH=120/120` (base before-value 50/120).

## Spot-check intake

| Previous outside finding or carried item | Round-31 disposition |
|---|---|
| D1 — README says C2 fetch bounds moved to held ground despite the miss; stale capability-row evidence pointer | drafted by ScribeD1 |
| D2 — backlog diagnosis stated as fact despite being tagged `[INFERENCE]`; scratch-only backlog-128 receipts and future counter-version constraint | drafted by ScribeD2 |
| D3 — “four controls forced pre-data redesigns” overstates the receipt record | drafted by ScribeD3 |
| D4 — C1 rerun count double-counts CriticClaimsAfter; RerunC2B is reported as 17/20 rather than committed 20/23 | drafted by ScribeD4 |
| D5 — v4 C1 control maximum reported as 84/106 rather than 86/106 | drafted by ScribeD5 |
| D6 — CriticS047Live task re-issued as LiveS047After in the same role without disclosure; refused CriticHarnessIntegrity outputs landed without review disclosure | drafted by ScribeD6 |
| D7 — S052 Gate quote was non-verbatim | drafted by ScribeD7 |
| D8 — wrong finding/commit pointers, omitted work item, post-commit report time, understated DiffToolB runs, and unregistered-host D4 quote provenance | drafted by ScribeD8 |
| Carried — L0 fetch-scope question (`fleet 8d77e6c1`) | carried (operator or later round) |
| Carried — resolver and dial time outside `DEADLINE` | carried (not closed here) |
| Carried — uncancelled hop timers | carried (not closed here) |
| Carried — MutHeadNoText survivor | carried (later counter) |
| Carried — 2xx challenge pages | carried (later round) |
| Carried — IPv6 | carried (later round) |
| Carried — pages without a `<head>` start tag | carried (later round) |

## Mistakes

| Class | Evidence pointer | Captured-by | Fix (check able to fail) |
|---|---|---|---|
| Non-verbatim source quote (S052 Gate quote) | `corpus/lessons/round-30.md:47,79-84`; `corpus/lessons/round-30-verifier-spotcheck.md:140` | none | Re-open every admitted Gate URL and fail unless the quoted string occurs verbatim in the opened page text. |
| Same-role retry of a dead seat reported as “not retried” | `corpus/lessons/round-30.md:143-150`; `corpus/lessons/round-30-verifier-spotcheck.md:65-69` | none | Reconcile dead-seat role/task cores against later dispatches; fail if a same-role re-issue exists but the report says no retry or omits it. |
| Unsupported count (“four controls”) without matching receipt enumeration | `corpus/lessons/round-30.md:135-136`; `corpus/lessons/round-30-verifier-spotcheck.md:42-51` | none | Enumerate the control findings and redesigns from their receipts, compare each prose count with that enumeration, and fail on any mismatch. |
| `[INFERENCE]` upgraded to fact (backlog-overflow diagnosis) | `corpus/lessons/round-30.md:102-104`; `corpus/lessons/round-30-verifier-spotcheck.md:112` | none | Trace factual diagnosis statements to committed observed evidence; fail when the only supporting source labels the mechanism `[INFERENCE]` and the downstream statement drops that qualification. |
