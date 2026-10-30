# Recon05 — bounded prior-entry overlap

Axes: source traceability, root-intent discrimination, evidence-write confinement. Advisory research only; no production/counter/claim edits and no non-author closure asserted.

## Observed documentary findings

Paths below are relative to `/home/vgpnk/Projects/shokunin/chousa-shokunin`.

| Prior entry / locator | Source IDs | Overlap and boundary | Confidence |
|---|---|---|---|
| `corpus/lessons/round-63-attempt2.md:53`, Mistakes row 3 | No dedicated source ID on the lesson row | Direct precursor: two deeper scripts copied `Path(__file__).parents[2]`, measured missing tool/checker paths, then changed to `parents[3]`. The lesson explicitly routes exact-file existence assertions. This is recorded historical evidence, not a probe rerun. | High |
| `corpus/knowledge/derived-output-safety-r61.md:15-37,39-45` | S134 open(2); S135 rename(2); S136 historical builder hazard report | Existing evidence-writer coverage: final-component versus prefix symlinks, exclusive temporary creation, rename replacing a destination link, directory-descriptor protection against prefix races. The Application records descriptor-relative builder operations and historical battery outcomes. These are stronger write-target controls than checking a derived file exists; the present research does not revalidate the builder. | High |
| `corpus/knowledge/openat2-resolve-r62.md:34-49` | S138 openat2(2); S139 installed header; S140 probe output | Existing extension to all-component symlink refusal and descriptor-root containment. Explicitly limits evidence to opens of existing files, not file creation or real-race retry. Its proposed writer improvement is marked inference, not a shipped implementation. | High |
| `corpus/SOURCES.md:54-55` (backlinks to `corpus/lessons/round-28.md`) | S044 os.path docs; S045 historical ancestor-refusal diagnosis | Earlier conceptual overlap: canonical path computation is separate from application policy. S045 explicitly does not authorize root exemptions or policy relaxation. No additional knowledge entry referencing these IDs was found by bounded literal search. | High for registry content; bounded-search-only for last observation |

## Current round distinction

`corpus/knowledge/lane-root-derivation-r64.md:13-31` uses **S150** (installed pathlib source), **S151** (realpath existing-components mode), and **S152** (relocation counter source). It adds a narrow instrument-root check, not a new general writer-safety treatment. The entry explicitly says roots identify locations rather than intentions; exact-file existence cannot distinguish two populated trees, establish provenance/content, or remove TOCTOU races. Its lines 25-27 warn that the counter's expected-path arithmetic is independently fallible.

**Inference:** the useful overlap boundary is three separate questions: (1) which location parent arithmetic names; (2) whether the exact required file exists there before measuring; (3) whether later writes stay bound to intended directory objects. Round-64 assertions address (2); round-61/62 material primarily addresses (3). None alone establishes intended repository identity.

Repeated rejection precedent: **S137** (builder docstring), **S141** (candidate probe docstring), and **S153** (candidate preflight docstring) reject stated intent as proof of behavior. `ref-preflight-v3.py` is a candidate, not production.

## Limits and execution record

- Frozen `corpus/evidence/round64/claims.md` was read before research. Its C1 frozen E12/E13 mismatch is an assignment-provided failure, not retested or relabeled PASS here; `c1-battery-supplement.py` is a distinct post-freeze supplement, not a repair of frozen bytes.
- Read/search-only documentary work; no exported-code contract determination, so no definition/caller tracing was needed. No LSP semantic result is claimed.
- Tools: specialized `read` and `grep`; no commands or behavioral probes were required or executed, so command/output/exit receipts are not applicable. Historical counts above remain attributed to their entries.
- No network fetches, package installs/updates, git/jj operations, clones, or scratch directories were made. Scratch cleanup is vacuous: this seat created nothing at `/fast/scratch/hyaku/chousa-r64/Recon05/`.
- Remaining unknowns: current production writer behavior, whether a populated wrong root can pass the current instrument family in practice, and full relocation-counter outcomes are outside this documentary assignment. Original manual/source files were not independently reopened; findings concern prior lane coverage and source IDs, not fresh source admission.

Report: .ufo/waves/round-64/w1/Recon05.md
