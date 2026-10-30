# Attack24 — source support versus self-authored probe

Axes: source fidelity, frozen-predicate fidelity, independently observed falsification, zero production mutation.

## Findings by severity

### High — C3's frozen relocation oracle rejects the correct startup diagnostic

`corpus/evidence/round64/c3-count.py:85–92` constructs `.../lane-copy/corpus/evidence/round65`, copies each instrument there, then expects `mirror.parent / corpus/SOURCES.md`. Each instrument actually derives `HERE.parents[2]`; for this layout that is `lane-copy`, not `lane-copy/corpus/evidence`. Thus the expected string contains an extra `corpus/evidence` segment. This is a defect in the frozen counter, not evidence of a broken existence assertion.

Bounded independent reproduction copied only the three frozen instruments and invoked each with `/usr/bin/python -B <copied-path>` (no arguments; startup fails before argument parsing). All three exited **2**, stdout empty, naming `.../lane-copy/corpus/SOURCES.md` on stderr. All three failed the exact frozen line-92 matching expression, which instead wanted `.../lane-copy/corpus/evidence/corpus/SOURCES.md`. Full commands, stderr, exit codes, expected/actual paths are in `evidence.json`. No full C3 run is claimed. The isolated loop yields zero matching relocations; therefore the frozen `RELOCATION_MATCH=3/3` target cannot follow from these unchanged bytes and this layout.

The layout also has the original relative depth (`corpus/evidence/<round>/script`), not the promised one-directory-deeper shape (`claims.md:200–203`). This independently corroborates the already disclosed erratum; no frozen bytes were repaired.

### Medium — the sourced entry is defensible technical evidence, not the frozen successful-probe source

`claims.md:219–226` calls S152 “probe output”; the inherited `corpus/SOURCES.md:162` and `corpus/knowledge/lane-root-derivation-r64.md:16,23–27` instead cite counter **source**, explicitly limiting it to the written assertion and fallible expected-path arithmetic. S150 was reopened directly at `/usr/lib/python3.14/pathlib/__init__.py:63–72,392–396,932–938`; the stated logical-parent and resolve quotations match. S151 was reopened by decompressing the installed `/usr/share/man/man1/realpath.1.gz`; its `-e` option does say “all components of the path must exist” (receipt `realpath-source.txt`, GNU coreutils 9.12). Neither external source proves the self-authored relocation oracle correct. The entry honestly makes this distinction; it cannot substitute for C3's missing frozen PASS receipt. `corpus/lessons/round-64.md:8,19` already discloses the source substitution and pending outside non-author gate. Treat this as a claim-evidence boundary, not a newly discovered defect in the supplemental prose.

## Frozen C1 disposition (not silently repaired)

The frozen E12/E13 mismatch remains: `c1-battery-v3.py:386–394` separately calls `tag()` for the created name and its README mention, while `:442–443` expects success. Those are defective purported-benign fixtures; `claims-erratum.md:5` explicitly reports the frozen failure. No C1 battery was rerun here, and no candidate or `c1-battery-supplement.py` result is represented as admitting C1. Candidate `ref-preflight-v3.py` is not production.

## Identity, scope, and evidence

Read-only `git -C <absolute-lane> show bf40d99bda9eefdad3ed6276da077cfb24ba82f1:<path>` exited 0 for claims.md and the three instruments. SHA-256 comparison confirmed current bytes equal the freeze for all four; `evidence.json` records complete hashes. This is byte identity, not a claim that any production implementation passed. Only one installed Python runtime (3.14.8) executed the bounded probes. No rerouting, resume-continuity implementation, or runtime saturation assertion is in this item's scope.

Semantic tooling: `read xd://lsp` returned “No such tool”; no LSP server/status device was available. Source searches are literal discovery, not semantic caller proof.

## Residual risk and verification gaps

- Full C3 smoke/shift run, C1 full battery, C2, candidate implementation, and supplemental battery were not executed by this seat. No global PASS/FAIL receipt is fabricated.
- No independent outside-author admission is asserted; this report is advisory and cannot close the non-author gate.
- Sources establish positional ancestry and existence-option semantics, not intended repository identity, provenance, content, or TOCTOU safety. The inherited entry states these limits.
- No packages installed/updated; existing Python 3.14.8 and installed local source/manual used. No network, clone, git/jj mutation, or production edit. Scratch `/fast/scratch/hyaku/chousa-r64/Attack24` was removed in the probe cell; removal observed true.

Self-evaluation: accuracy 4 (bounded relocation, not full counter); completeness 4 (source/probe distinction covered, full counters intentionally outside bounded scope); clarity 4 (explicit claim-versus-supplement distinction, longer evidence section); actionability 4 (keep frozen C3 unverified; L1 owns disposition); conciseness 4 (retains exact provenance). Mean 4.0. Highest-impact improvement for integration: link this independent relocation receipt to the existing erratum rather than counting it as a new passing instrument. User agreement expected because commands and limits are explicit.
