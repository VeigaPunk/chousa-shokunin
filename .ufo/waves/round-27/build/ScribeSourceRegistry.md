# ScribeSourceRegistry — C3 registry findings

**Assigned item:** Static local-source review of registry provenance/parser integrity. **Axes:** Calibration (primary); operability/resource effects (secondary). No product code was edited.

## Provenance scope

> “Registry existence, status and backlink checks establish local declared relationships, not source relevance or truth.” (`corpus/SOURCES.md:46`, S036)

The accompanying own-work note says the registry screen does not check source support or truth (`corpus/knowledge/registry-link-r26.md:34-41`). Thus C3's local `source:` S-id → mined row → exact `used-by` entry link is a declaration check, not evidence that the source was opened, supports the entry, or that a verification actually occurred. Keep that boundary in any round27 admission language.

## Static findings and exact locations

- **Header state / width — false acceptance and column misbinding.** In `tools/research-gate.sh:2412-2415`, a non-pipe line clears `header_candidate` but leaves `id_col`, `status_col`, and `usedby_col` intact. The stale indices can make a later unnamed table appear to have a named header; the parser also does not require header and delimiter cell counts to match (`:2443-2467`). Round26 diagnosis `.ufo/waves/round-26/falsify/FRegistryHeaderless.md:41-83` records headerless tables accepted and both false negatives and false positives, including an 11-finding false-positive result after a prose/blank-line prefix to the real SOURCES registry. The old selftest/differential controls did not cover the no-named-table failure (`FRegistryHeaderless.md:79-83`).
- **S-id occurrence identity — phantom and duplicate findings.** `metadata_registry_check_source` matches with `source_id_re` then advances via `source_scan=${source_scan#*"$source_match"}` (`tools/research-gate.sh:2472-2504`). This strips through the earliest textual occurrence, not the matched occurrence. When a standalone S-id is at end-of-value, an earlier glued occurrence can be rescanned as if standalone; duplicate matches also inflate finding counts. `FRegistryIdBoundary.md:28-46,76-98` records the mechanism, false positives and duplicate-line cases. The old `meta-reg-no-token-id` control only tests glued forms without a trailing standalone ID (`FRegistryIdBoundary.md:117-124`).
- **Filesystem denylist — colon truncation before path checks.** `is_denylist_path` calls `ptr_file_part` (`tools/research-gate.sh:595-606`), which is citation-pointer behavior that strips a `:line` suffix. `metadata_registry_load` applies that predicate to filesystem paths—the argument, canonical path and opened-fd canonical path (`:2374-2383`). The historical synthetic diagnosis `FRegistryRegistryDeny.md:25-30,59-75,91-107` records that a colon earlier in a denylisted path bypassed the predicate and the file was read. Do not globally change pointer-anchor handling to repair this filesystem-path case.

## Suggested change and expected outcome (not implemented or verified here)

1. Treat a registry table as a fresh named header immediately paired with a separator of equal cell width. Clear candidate state and all column indices on every non-table/break line; validate the separator width before committing the header. Preserve reordered columns and first-duplicate-ID-wins behavior. A registry lacking a valid named table should retain the usage-error path (exit 2, no verdict).
2. Replace literal-prefix rescanning with a forward, position-based scan under explicit ASCII boundary semantics (C locale or equivalent). Advance past each actual match exactly once: no IDs invented from glued text and no repeated emission for a single occurrence, while distinct genuine occurrences and the existing `S` + 3-or-more-digit rule remain intact. Preserve exact rooted `used-by` matching and existing status/verified-at rules.
3. Use a filesystem-path-specific denylist check on the complete filesystem path (including canonical target and opened-fd canonical path) before reading. Keep citation-pointer callers on their existing anchor-stripping semantics. A newly generated synthetic path with an earlier colon and a denylisted component should be refused without reading that path.

Expected result is repair of the three named C3 falsifiers without weakening existing expectations or changing well-formed registry behavior; this is a proposal, not a pass claim.

## Limits and unrun gates

Round26 also names broader limits that these targeted fixes do not establish as solved: the registry's complete Markdown grammar is unspecified/under-covered (fenced examples, indented/comment tables and body-row lookalikes are documented as shared or unresolved gate/oracle gaps in `FRegistryHeaderless.md:85-113`); the 8 MiB snapshot cap bounds bytes, not parser memory/time (`corpus/knowledge/registry-link-r26.md:58-61`); and `FRegistryIdWidth.md:127-148` documents quadratic cost in the prior literal-prefix scan. Do not infer general parser/resource safety or full criterion-6/source-support verification from closing these three defects.

No verification command or gate was run for this scribe assignment: no selftest, C3 regression, registry differential, build, lint, or formatter. No fixtures were created and no tools were installed. Round26 receipts above are cited as prior local evidence, not rerun results.

**Touched surface:** `.ufo/waves/round-27/build/ScribeSourceRegistry.md` only.

**Artifact:** `.ufo/waves/round-27/build/ScribeSourceRegistry.md`
