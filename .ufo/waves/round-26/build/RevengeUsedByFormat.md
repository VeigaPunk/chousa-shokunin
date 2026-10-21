# Round 26 — `used-by` format reconnaissance

## Scope and evidence
- Read-only review of `git log -p -- corpus/SOURCES.md` at HEAD `0e9784bd52eca456b24d0bc40921480a47f91a2b`; its four file-changing commits are `6572827`, `0fc037e`, `c2a6e33`, `0e9784b`. A supplementary `git log --all` census covered 13 snapshots (including alternate/intermediate refs); it introduced no additional cell form. No tests/builds run; no installs.

## Reconstructed forms
- Every populated historical `used-by` token is a repo-relative `corpus/knowledge/<name>.md` path. No `knowledge/<name>.md`, bare-basename path, `corpus/lessons/...`, other prefix, or non-comma separator occurs in a cell. Evidence: initial S001/S003/S013 at `corpus/SOURCES.md:11,13,23`; current rows at `:39,44-49`; full-history cell census above.
- Multi-entry delimiter is comma + space, with whitespace trimmed around the cell/tokens. The original multi-entry example is S003 (`:13`). At current HEAD S029 also has two paths (`:39`), adding `corpus/knowledge/recheck-due-r26.md` to its prior path.
- “None” is consistently U+2014 em dash `—` (not hyphen/en dash/empty). Every em-dash cell in every snapshot is queued or rejected; no mined row has `—`. Examples: `:18-22,24-28,30-38,40-42`. The checker must status-gate this test as Claim 3 specifies; interpreting `—` as a mined backlink would be a false positive.

## Superseded rows and apparent exceptions
- In `0fc037e`, S019/S020 were `mined` with `corpus/knowledge/metadata-screen-r25.md`; `c2a6e33` changed each to `queued` + `—`. `git log -p` shows those exact cell changes. The round-25 change log records the full old path (`corpus/lessons/round-25.md:184-189`). Their replacement mined rows are S029/S033 (`corpus/SOURCES.md:39,43`); S029 gains its second backlink at current HEAD (`:39`). S021/S022/S024 began queued with `—` and their superseding S032/S030/S031 remain queued with `—` (`:30-34,40-42`).
- Bare `metadata-screen-r25.md→—` appears in the explanatory SOURCES prose (`corpus/SOURCES.md:149,154`), not in a table cell; it is shorthand, not a historical cell form. Do not count it as a parser counterexample.

## Claim 3 adjudication
- Original v0 rule (`corpus/evidence/round26-claims.md:102-103`): comma-split, trim, compare last path component to entry basename. **It parses and matches every historical table cell**; no historical cell is a syntax or observed basename-match counterexample. Exact repo-relative v1 contract (`round26-claims.md:134-139`; `/home/vgpnk/Projects/shokunin/CORPUS.md:107-108`) is also compatible with every observed cell.
- The basename predicate nevertheless has a semantic false-positive class explicitly identified by the correction: a wrong-directory path with the same basename would pass. This case was not observed in the registry history; it is a spec-level counterexample, not an empirical row. Exact-path comparison avoids it. Likewise, copying the prose shorthand at `SOURCES.md:149,154` into a cell would not equal the exact repo-relative path, but that copy never occurred.
- Auxiliary current-tree backlink/source-ID cross-check: 39 registry rows against 32 `corpus/knowledge/*.md` entries found 0 mismatches (read-only extraction; not a test).

Confidence: High for the census of available registry history; the same-basename false-positive is certain by the predicate but unobserved in these records.

VERDICT: Historical cells are uniformly comma-separated exact `corpus/knowledge/` paths or `—`; v0 parses all observed cells, but basename equality is semantically weaker than the corrected exact-path contract. Installs: none.