# C3 review — S-id occurrence cardinality

**Axis:** calibration. **Finding:** the acceptance oracle must compare per-occurrence results, not a set of finding codes or distinct IDs. Repeated standalone citations are legitimate separate occurrences; a glued/non-standalone token re-read during scanning is not.

## Evidence and recommendation

- Base `tools/research-gate.sh:2474-2504` scans with a boundary regex, then advances using `${source_scan#*"$source_match"}`. That removes through the first literal copy of the match, not necessarily the match just found. R26 `FRegistryIdBoundary.md:32-46,76-82` documents terminal-ID cases where this causes an earlier glued token to be rescanned; `:94-98` records duplicate findings from non-standalone tokens.
- R26 `FRegistryDuplicateId.md:95-99` documents repeated *standalone* citations producing multiple findings and notes the contract yields every token. These multiplicities are expected, not something to deduplicate.

Build the independent expected result by tokenizing the original `source:` value once with explicit ASCII boundaries (`(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])`), then applying the synthetic registry row state per token. Parse emitted finding records and compare a `Counter[(finding_code, source_id)]` to the expected counter (include entry identity if a case has multiple entries). Do not compare sets or only per-code totals: both erase repeated legitimate occurrences or can accept the wrong source ID.

Concrete synthetic oracle: registry has `S001` mined and correctly used-by, `S002` queued, and no `S003` row. Expect:

| `source:` value | Expected finding multiset |
|---|---|
| `see S001S002 and S001` | empty |
| `see S001S003 and S001` | empty |
| `ref S002x and S002` | `{(META_SOURCE_NOT_MINED, S002): 1}` |
| `ref S002S002 and S002` | `{(META_SOURCE_NOT_MINED, S002): 1}` |
| `S002,S002` | `{(META_SOURCE_NOT_MINED, S002): 2}` |
| `S003,S003` | `{(META_SOURCE_ROW_MISSING, S003): 2}` |

Thus a rescan of either glued token fails the first four exact counters, while two real occurrences retain multiplicity two. Keep the entry-level verdict/exit expectation alongside this record comparison; a matching record set alone is not a full CLI oracle.

## Verification and scope

No gate, regression, differential, or selftest was run; no production edit was made. The LSP device is not mounted here, so locations above are from static source/report reads, not semantic navigation. No tools installed.