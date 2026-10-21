# ReviewRegistryBoundary — C3 source-token boundary oracle

Assigned item: adjacent S-ids; beginning, end, newline, and underscore boundaries. Advice only; based on base `64eec5d41c7cf7f17f5ce1e968e28b3769952596` and round26 receipts. No gate, selftest, differential, or verification was run; no fixture was executed.

## Evidence and finding

At base, `tools/research-gate.sh:2474-2504` matches standalone `S` + at least three digits, with `[[:alnum:]_]` excluded as a boundary. But it advances with `source_scan=${source_scan#*"$source_match"}` (`tools/research-gate.sh:2503`), which strips the first textual occurrence, not necessarily the matched occurrence. This is the reported cause of phantom IDs and duplicate findings when a real match ends at end-of-value (`.ufo/waves/round-26/falsify/FRegistryIdBoundary.md:28-46, 76-98`; corroborated by `FRegistryIdWidth.md:85-125`). The base implementation therefore has a concrete calibration defect; this is not a review of a round27 patch.

## Concrete acceptance oracle

Use only fresh synthetic temporary registry/entry fixtures. A minimal registry has the named `id | status | used-by` header and matching-width separator. Give S001 and S002 `queued` status so every recognized occurrence yields an observable `META_SOURCE_NOT_MINED` finding; include a `mined` exact-used-by control separately. Judge exact finding-ID multiplicities per entry, not sets alone, and require no fabricated IDs. Maintain the C3 token grammar: uppercase ASCII `S`, at least three ASCII digits, and boundaries not ASCII alphanumeric or underscore.

| `source:` value | Expected token occurrences | Expected observable result |
|---|---|---|
| `S001,S002` | S001 ×1, S002 ×1 | Exactly one `NOT_MINED:S001` and one `NOT_MINED:S002`; no duplicates. Comma is a valid separator. |
| `S001` | S001 ×1 (at start and end) | Exactly one `NOT_MINED:S001`. |
| `S001 tail` / `head S001` | S001 ×1 in each | Exactly one `NOT_MINED:S001` in each case. |
| `S001` followed by newline then `S002` (including a continuation line) | S001 ×1, S002 ×1 | Exactly one not-mined finding per ID. Newline separates tokens; it must not hide, invent, or repeat one. |
| `_S001`, `S001_`, `x_S001`, `S001_x`, `S001_S002` | none | No row-status finding; one `META_SOURCE_NO_ROW_ID` informational result, as for other no-ID inputs. |
| `S001S002 and S001` | S001 ×1 (final standalone occurrence only) | Exactly one `NOT_MINED:S001`; no S002 finding. This reproduces the end-of-value consumed-text rescan failure from r26. |
| `S002x and S002` / `S002_ and S002` | S002 ×1 (final standalone occurrence only) | Exactly one `NOT_MINED:S002`; no phantom duplicate. |
| `S001,S001` | S001 ×2 | Exactly two `NOT_MINED:S001` findings: preserve distinct real occurrences rather than deduplicating. |

Also retain an exact-used-by positive control for a `mined` ID (no finding), so the token fix does not change the existing path-match rule. Gate verdict/finding counts must agree with those occurrence expectations; an oracle based only on finding-ID sets is insufficient to detect repeated identical findings.

## Residual risk and verification gaps

This receipt only covers source-token boundary calibration. Newline fixtures must use the same continuation representation as entries, while preserving a newline in the value passed to the scanner. The round26 receipt confirms continuation lines participate in the failing scan (`FRegistryIdBoundary.md:76-85`). No round27 patch or persisted controls were inspected or executed, so no claim is made about their coverage or result. No tools were installed.