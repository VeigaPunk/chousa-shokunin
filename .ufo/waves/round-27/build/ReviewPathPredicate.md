# C3 review — full filesystem paths vs citation pointers

Assigned item: keep denylist checks complete for filesystem paths without changing legacy `path:line` pointer behavior.
Severity: **Critical / C3 denial failure** — r26 `FRegistryRegistryDeny` classifies the registry bypass as FRRD-1 crit.


## Finding

The base has one ambiguous predicate: `ptr_file_part` intentionally takes text before the first colon (`tools/research-gate.sh:573-576`), and `is_denylist_path` applies its denylist to that truncated value (`:595-606`). The same helper is used for both citation inputs and literal filesystem paths. In particular, `metadata_registry_load` passes raw, canonical, and fd-canonical filesystem paths through it (`:2374-2383`); the metadata entry reader does likewise (`:2582-2592`). `ptr_resolves_meta` also uses it first on a citation pointer (`:621`) and later on the resolved filesystem path (`:636`); `check_pointer` and `chain_ref_file` are citation consumers (`:650-652`, `:1596-1602`).

This is an observed C3 defect, not merely a concern: the existing r26 `FRegistryRegistryDeny` receipt reports 6/6 synthetic colon-containing denylisted paths opened/read and parsed CLEAN; B1–B6 include `a:b/.config/reg.md`, `a:secret.env`, a symlink alias, and an SFTP-shaped path (`.ufo/waves/round-26/falsify/FRegistryRegistryDeny.md:5-8,43-75`). It identifies `${p%%:*}` as the truncation cause (`:23-30`). Its M2 diagnostic changed the shared predicate to check the whole input and fixed B1–B6, but explicitly notes that this also changes citation-pointer denylisting and is not a proposed patch (`:83-87`).

**Recommendation:** keep citation parsing and filesystem-path matching distinct. Retain the existing first-colon behavior for pointer/citation callers, including `ptr_file_part` resolution/display; use a full-path denylist predicate for values that are filesystem paths. At minimum classify and route the registry path/canon/fdcanon, metadata entry path/canon/fdcanon, and resolved `canon` in `ptr_resolves_meta` accordingly. `claim_source_path` passes its input literally into candidate construction (`:1125-1155`), so classify it by that filesystem-path contract rather than changing pointer parsing globally. Do not change denylist patterns or other registry semantics as part of this fix.

## Concrete acceptance oracle (synthetic fixtures only; not run here)

1. Preserve the citation contract independently of filesystem checks: a clean synthetic file cited as `fixture.md:17` still resolves/displays using `fixture.md` (not a literal `fixture.md:17` filename); a citation whose file portion is `.config/fixture.md:17` remains denied. Keep `ptr_file_part` and the citation consumers on that behavior. A new full-path predicate must not be substituted globally for those callers.
2. In a fresh temporary root, put a valid one-row registry table at `a:b/.config/reg.md`; invoke `verify-metadata` with that exact registry path. Require exit 2 and `metadata registry refused: denylist`, never CLEAN or parsed registry findings. Review the control flow as well: full-path rejection of raw/canonical paths precedes the registry `exec` at `:2375-2378`; any fd-canonical check precedes the bounded read at `:2382-2395`. An exit 2 alone is insufficient if it is only the later “no table” error.
3. Retain a normal synthetic registry positive control (r26 P0: CLEAN), existing colon-free deny controls (r26 D1–D19 and hardlink H1), and add the colon cases from B1–B6. Every colon-deny case must take the denylist refusal path; use valid table contents so a bypass would observably parse to CLEAN. Include a symlink to a colon-containing denylisted target. The r26 receipt records these as independent synthetic cases and reports the old target's bypass (`FRegistryRegistryDeny.md:43-75`).
4. Check the path/citation split at the call sites, not just the new helper in isolation: complete checks for filesystem values above; unchanged first-colon file-part behavior at pointer consumers. This is the regression guard against replaying M2's broad change.

## Verification gaps

No round-27 candidate diff was inspected; this report is a base-and-r26-receipt review, not a verdict on an unobserved patch. No tests or runtime checks were run, as instructed. The `lsp` device is not mounted (`read xd://lsp` returned “No such tool”); literal search was used only to locate references, not as semantic proof. No tools installed.

VERDICT: Require a caller-specific full-filesystem-path predicate plus the citation-preservation oracle above; r26 receipt proves the base registry bypass, but no candidate diff was available to judge.