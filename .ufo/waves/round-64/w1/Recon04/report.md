# Recon04 — registry/package collisions

Axes: coverage (complete extracted sets), calibration (byte-pinned counts), operability (reproducible read-only extraction). Advisory evidence only; L1 owns integration/admission.

## Observed

Compared `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md` against `/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md`.

| Set | Lane | Staged package | Intersection |
|---|---:|---:|---:|
| Row-start source IDs | 153 | 114 | **72** |
| Unique source-cell HTTP(S) URLs | 113 | 91 | **53** |

- Lane IDs are exactly S001–S153; package IDs exactly S082–S195. ID collisions are exactly **S082–S153 inclusive**, with every individual ID saved in `evidence.json:id_collisions` (no gaps). Package IDs not currently occupied are exactly S154–S195. Neither input has duplicate row IDs.
- All 53 exact URL intersections, plus each lane/package ID mapping, are enumerated in `evidence.json:url_collisions`. Complete input row/source/URL lists and line numbers are saved under `lane.rows`, `package.rows`, `lane.urls`, and `package.urls`; these are independently derived, not copied from prior receipts.
- Removing URL fragments produces the same 53 intersections. This is not redirect/DOI canonicalization.
- Only S100, S101, S102, S103 among overlapping IDs share an extracted source URL at that same ID. A collision does not mean equivalence: package S084 is RFC 7089, held as lane S079, while lane S084 is the AVeriTeC training split (package S132).
- Package S077 is **not a row ID**: its occurrence is inside S096's scope cell, referring to a prior wave's J-STAGE source (`SOURCES.append.md:21`). The row-start extractor properly excludes that mention.
- Historical `corpus/lessons/round-63-attempt2.md:37–39` reports 64 collisions against 145 lane rows. This measurement instead sees 153 lane rows and 72 collisions; the historical count must not be reused as a current count. No claim about the timing/author of the eight added rows is inferred.

Input SHA-256 at extraction:

- Lane: `8f6d0184daa9193839e7cb98e8a8db8b11f0fc690112e156045db7103bfbb099`
- Package: `a6dec4a0086d3cf767d638d7e52fdda08f78d22b0b376049b0ad14ff0f8aa696`

## Command and evidence

Cwd: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-64/w1/Recon04/`.

```text
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-64/w1/Recon04/collisions.py
exit: 0
stderr: empty
stdout: evidence.json (complete JSON)
summary: lane_rows=153 package_rows=114 id_collisions=72 url_collisions=53
```

`command.json` records argv/cwd/exit/stderr and stdout artifact. Python 3.14.8, existing system interpreter; no tools installed or updated. Extractor accepts 0–3 leading ASCII spaces, then a pipe and an S-id first cell; excludes cell mentions. It examines HTTP(S) URLs only in the source cell, trims terminal prose punctuation `. , ; )`, and compares case-sensitive strings. Other cells, local paths, inferred URL equivalence, network content and admission status are not measured.

## Inference and unresolved boundaries

High confidence in these byte-pinned local intersections. Direct appending would conflict with 72 held IDs; shared URLs require scope review, not automatic source admission or automatic rejection. No adoption gate is opened by this advisory result. URL semantic equivalence and source support remain unassessed. No exported code contract was changed/traced; mounted device inventory has no `lsp` device, so literal searches here are textual evidence only.

Read mandatory rules, Godspeed skill and frozen round64 claims first. The assignment supplies that frozen C1 has E12/E13 fixture mismatch and a distinct inherited supplement; this seat did not rerun C1 and claims no frozen PASS. Candidate preflight was not treated as production. No network, git/jj mutation, fleet/sibling edit, clone, scratch tree, package-tool execution, or production edit occurred; no scratch cleanup was needed.

## Self-evaluation

Accuracy 4/5: extraction is explicit and byte-pinned; URL spelling equivalence remains intentionally unassessed. Completeness 5/5: complete ID and URL sets, intersections, mappings and receipts delivered. Clarity 4/5: long lists live in machine-readable evidence rather than inline prose. Actionability 4/5: exact conflict sets supplied; admission decisions remain L1's responsibility. Conciseness 4/5: report duplicates a few evidence fields to make the result standalone. Mean 4.2/5; user-facing improvement is to consult URL mappings before any document-scoped renumbering, without equating URL reuse to equivalent scope.
