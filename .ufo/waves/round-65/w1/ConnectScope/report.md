# Seat ConnectScope — chousa lane round65 (scoped findings)

Assignment: connect source identity, header consistency and execution authenticity across C1/C2; inspect sibling overlap without absorbing generic testing or dispatch; name cross-claim causal dependencies or independence. Leaf seat; no subagent dispatch. Read-only lane; writes only this report plus uniquely named evidence in the seat folder. Freeze `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd`, base `d6ed8155e9b4735639a2cf0a3e479c62f2056195`.

## Evidence read

- `corpus/evidence/round65/claims.md` (frozen, two claims), `c1-count.py`, `c2-count.py`, `source-openings.json` (S154–S157).
- `controls/ref-receipt-pin.py` (prefreeze reference, not hidden), `controls/c1-before.txt`, `c1-positive.txt`, `always-pass.txt`, `always-fail.txt`, `c2-before.txt`.
- `corpus/knowledge/receipt-identity-r65.md`, `corpus/lessons/round-65.md`, `corpus/SOURCES.md` rows S154–S157, `corpus/README.md` index line.
- Sibling reports in `.ufo/waves/round-65/w1/` (list below).
- Isolated read-only probes in scratch (receipts copied to seat folder): `git -C <lane> cat-file blob BASE:SKILL.md | sha256sum` = `4355e16a5d8d16057496f005df7382ca287863712ed2e3abb25f61c60008ce1a`; `git merge-base --is-ancestor BASE FREEZE` = true; round64 before receipt head/tail. No counters run; no batteries; no production writes.

## The four concepts, mapped across C1/C2

The two frozen claims partition one question — "what does a receipt establish?" — into an operational half (C1) and an epistemic half (C2). Mapping:

| concept | C1 anchor (operational) | C2 anchor (documented) |
|---|---|---|
| object identity | `REVISION=<40 lowercase hex>` must equal caller `--revision`; blob read via `git cat-file blob <rev>:<path>` (ref-receipt-pin.py:24) | entry Claims 1 + S154 quote: raw object contents returned at a *selected* object expression, not the working tree |
| content digest | `SHA256=<64 lowercase hex> <path>`; sha256 over cat-file stdout; path must be canonical relative POSIX, no `..`, no absolute (ref:23–26) | entry Claims 2 + S155 quote: digest binds the bytes passed to `update()`; no authorship inference |
| reported exit | `EXIT=<0..255>` decimal; format-checked, value not authenticated; frozen case `nonzero-valid` (EXIT=1) expects rc=0 — a consistent *failure* report is valid | entry Claim 4: `EXIT=1` can be a consistent report of a failed command; validator exit0 means header/blob consistency only |
| execution authenticity | explicitly out of scope: docstring "Validate receipt header consistency, not execution authenticity" (S157, gate-rejected as execution proof) | entry Limits: no command/body binding, signature, trusted timestamp or process attestation; replayed valid header with fabricated output can pass |

Both claims state the same exclusion in different registers; they do not contradict and do not overlap in what they prove.

## Cross-claim causal dependencies and independence

**No operational dependency in either direction.** C1's target (`tools/receipt-pin.py`) is not read by `c2-count.py`; C2's entry is not read by `c1-count.py`. Different artifacts, different counters, different denominators (20 cases vs 10 checks), disjoint write surfaces (`tools/` vs `corpus/knowledge/` + `SOURCES.md` + `README.md` registrations).

**C2 does not depend on C1's acquisition outcome.** The entry's fourth source S157 cites the *prefreeze control* `controls/ref-receipt-pin.py` (frozen into the commit `f99de3b`, hash `0719d717…`), which exists regardless of whether the C1 target is ever installed. C1 can stay at its before state (`CASES=0/20`, observed: target absent) while C2's structural checks hold.

**Shared common-cause substrate (not a claim dependency).** Both the C1 counter and the entry's interpretation rest on the same environment facts: (a) the BASE object must exist in the lane git object database — verified present, `commit`, and an ancestor of the freeze commit, so a full clone is not required; (b) `git cat-file` returns raw blob bytes (S154); (c) `hashlib.sha256` digests exactly those bytes (S155). Concretely, `c1-count.py` itself exercises S154+S155 semantics when it builds fixture `v` from `cat-file` stdout and hashes it — the digest `4355e16a…ce1a` it embeds is the live value computed in this seat's probe. If either substrate behavior changed, the frozen C1 counter and C2's sourced claims would degrade *together*; this is a common-cause coupling, not one claim entailing the other.

**Contract coupling (conceptual, directional).** C2 documents the semantics that C1 operationalizes: the header contract in `claims.md` C1 ("REVISION full lowercase 40 hex, EXIT decimal 0..255, SHA256 full lowercase 64 hex plus canonical relative POSIX path, empty separator, nonempty output") is exactly what the entry's Claims 1–4 interpret. A change to the frozen C1 contract would orphan C2's interpretation, but the freeze/kill rule forecloses such a change; under the freeze the coupling is static.

**Joint outcome ceiling.** C1 PASS (20/20) plus C2 PASS (10/10) still cannot authenticate any execution: C1's exit token is format-checked only and its digest binds blob bytes to a caller-selected revision; C2 is structural (its own text: "cannot establish entailment"; claims.md: "A boilerplate entry could pass"). The claims are complementary, not cumulative, on authenticity.

**Current observed state (inspection, not counter runs).** C1 target absent → before control stands. The C2 entry present in the working tree structurally satisfies all ten `c2-count.py` checks by string inspection (starts `source:`; `\nverified-at:`; `\nrecheck:`; S154–S156 present; `| S15x |` rows in SOURCES.md; README index line; `## Claims`; `## Limits`; `authenticity`; `working tree`). L1 remains the sole verifier.

## Sibling overlap

- `SourceHash` verified S155 digest semantics and freeze integrity, and already drew a one-line cross-read tying C1's blob-digest format to hashlib semantics. Complementary: this seat generalizes that cross-read to the full four-concept map and adds the dependency analysis. No conflict; no retesting absorbed.
- `ConnectPattern` is a separate connector seat in this wave (registry-confirmed; still running, no report published at write time). Scope not yet observable; no overlap to report, no absorption.
- `Attack01–20`, `Probe01–20` exercise the frozen C1 counter/reference interface (their own bounded scratches). Generic testing belongs to them and to tameshi; this seat ran no counter and no malformed-input battery.
- `ToolDraft` holds an independent C1 implementation draft, reference read only after drafting; explicitly retains no acceptance authority. Not overlap.
- Draft seats (`EntryDraft`, `RegistryDraft`, `ReadmeDraft`, `LessonDraft`, `QualityDraft`, `ScoreDraft`, `LogDraft`, `ClaimsBinding`, `ReviewEntry`, `ReviewFreeze`, `PinFormat`, `SourceGit`, `SourceBefore`, `Assimilation`, `Considerthese`, `Province`, `PriorClosure`) own the C2 artifact surfaces; this seat wrote none of them.

## Notes and risks for L1 integration

1. Counter runs need distinct `--work` dirs per counter (both create and remove theirs); the prefreeze receipts show L1 already used separate dirs.
2. Keep the gate's S157 disposition (REJECTED as execution proof) aligned with the entry's Limits when integrating C2; the entry currently conforms.
3. Same output-path duality ToolDraft flagged applies here: the seat spec names both `w1/ConnectScope/report.md` and report trailer `w1/ConnectScope.md`; identical content written to both, plus uniquely named evidence receipts in the folder.
4. No tools installed this seat (nothing needed beyond git/python3 already present). No production writes; scratch deleted on exit.

## Verification

Read-only git with explicit `-C` against the lane; sha256 recomputed independently of the counters; ancestry asserted before use; scratch `/fast/scratch/hyaku/chousa-r65/ConnectScope` removed after copying `base-skill-md-sha256.txt`, `base-ancestry.txt`, `r64-before-line1.txt` into the seat folder.
