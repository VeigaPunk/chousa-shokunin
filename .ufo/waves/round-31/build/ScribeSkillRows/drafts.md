# SKILL.md — round 31 row drafts

Append-only additions; preserve every existing row and checklist item.

## 1. Decision table

**Insertion point:** directly after the existing final Decision-table row (`Re-open a quote ... (r30)`, current line 25), before the `Provenance of the table above` paragraph.

```markdown
| Cite a claim at a named line (r31) | Put the claimed range in the JSONL record's `"line"` field (`"N"` or `"N-M"`) and run `bash tools/research-gate.sh verify-claims <claims.jsonl> --root ..` | treating an occurrence anywhere in the source as proof it is on the named range | a boundary-delimited occurrence spanning exactly the named range keeps the existing verdict; otherwise `CLAIM_LINE_MISMATCH` → `observed=mislocated` |
| Pin the revision read (r31) | Put the source file's exact-byte SHA-256 in the JSONL record's `"sha256"` field (64 lowercase hex) and run `bash tools/research-gate.sh verify-claims <claims.jsonl> --root ..` | treating a supported span as proof that the source revision still matches | mismatch is `CLAIM_SOURCE_REVISION_MISMATCH` → `observed=stale` before span checking; malformed value → `observed=invalid` |
```

## 2. Error patterns

**Insertion point:** directly after the existing final Error-pattern row (current line 50), before `## Boundaries (hard)`.

```markdown
| span found only outside the claimed line range (r31) | `observed=mislocated` (`CLAIM_LINE_MISMATCH`): the boundary-delimited occurrence must span exactly the named `"line"` range |
| source changed since the claim (r31) | `observed=stale` (`CLAIM_SOURCE_REVISION_MISMATCH`) when exact source bytes differ from the claim's `"sha256"`, before span checking |
```

## 3. Checklist (executable)

**Insertion point:** a new checklist line directly below current item 1 (current line 66); do not rewrite item 1.

```markdown
- [ ] Run `bash tools/research-gate.sh verify-claims <claims.jsonl> --root ..` and include a per-claim `"sha256"` (64 lowercase hex of the exact source bytes); where a line is named, set `"line"` to `"N"` or `"N-M"`.
```

## 4. Gates table — verify-claims note

**Insertion point:** directly after the existing `research-gate verify-claims` row (current line 77), as a supplemental table row.

```markdown
| `research-gate verify-claims` (r31 note) | note | `bash tools/research-gate.sh verify-claims <claims.jsonl> --root ..` | `CLAIM_LINE_MISMATCH` → `observed=mislocated`; `CLAIM_SOURCE_REVISION_MISMATCH` → `observed=stale`; malformed `"line"` or `"sha256"` → `CLAIM_RECORD_INVALID`, `observed=invalid` | `PASS (N cases)` — L1 fills N after the expanded self-test | contract: `corpus/evidence/round31/claims.md` | unchanged: local sources only; zero writes | chousa |
```

`PASS (N cases)` is intentionally a placeholder, not a test result. The frozen contract source is `corpus/evidence/round31/claims.md` (C1 fields/findings: lines 22–32; C2 fields/findings: lines 73–81).