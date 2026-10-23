# Round 31 integration review — coverage, operability
Scope: `tools/research-gate.sh` base `8070f92b` → tip `ee1024fd`; both executor patches applied separately in scratch; stacking them conflicts at 9/11 hunks, so reviewed the landed merge against each patch.
Finding (medium) — `tools/research-gate.sh:1444-49` (`json_has_key`/`json_str`) treats nested `sha256` keys as claim pins, contrary to frozen `claims.md:150-51` (unknown keys ignored; absent pin unchanged).
Repro: `timeout 1200 bash ./research-gate.sh verify-claims nested-claims.jsonl --root .` in scratch, exit 1; a claim with only `ignored.sha256` reports `observed=stale`.
PASS — `tools/research-gate.sh:1532`: string equality correctly compares canonical decimal line numbers without arithmetic overflow; inactive when `line` is absent.
PASS — `:1461` generic malformed-pin diagnostic still rejects malformed values without echoing them; `:1506` converts unreadable/non-digest hashes to `unreadable` and fails closed; both are inactive when `sha256` is absent.
Low/doc-only — header comment `:63-68` leaves “A marker on” orphaned and drops the fixture-violation note; help `:342` correctly merges both optional fields.
Verification gaps: `read xd://lsp` reported no `lsp` device; no semantic LSP checks/full selftest. Overall broken only for claims with nested unknown `sha256` keys; other listed L1 deltas hold.