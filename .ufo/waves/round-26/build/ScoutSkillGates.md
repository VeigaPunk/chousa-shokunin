# ScoutSkillGates — round 26 documentation map

Scope: read-only audit of the four assigned documents. Axes: coverage, line accuracy, actionable disposition. The live lane tree gained round-26 documentation during this scan; findings below use the re-read state.

## Observed statement map

- `SKILL.md:76` — gate index row: old invocation, r25 finding/exit map, `PASS (154 cases)` / cases 137–154, 25/28 population, header parsing, refusal bounds, local-only/zero-write scope.
- `SKILL.md:79-92` — append-only r25 correction: first unfenced literal `## ` header end; calendar-valid scheduled dates; fd-bound snapshot and multilink/stat refusal; path escaping; 161-case checkpoint and its receipt. Line 83 explicitly says not to relabel the historical checkpoint.
- `SKILL.md:460-498` — appended current round-26 section: flags optional and metadata-only; both apply together; absent/invalid arguments and refused/headerless registry are exit 2; `--as-of` due/freshness and overdue semantics (480–481); registry checks and findings (482–483); prospective criterion-6 limits (485–489); full-file NUL/size/refusal checks precede header cutoff, no whole-snapshot per-line array, and remaining time/memory limits (491–498).
- `corpus/README.md:55` — audit-r11 example: missing `recheck:` yields `META_RECHECK_ABSENT`.
- `corpus/README.md:58-61` — r25 note, fixtures and evidence index rows: r25 grammar/findings/refusals, 25/28, 54/54 differential and cases 137–154.
- `corpus/README.md:62-66` — round-26 index rows already added for the three new knowledge notes, lesson and `evidence/round26-*`.
- `corpus/README.md:68-84` — count snapshot and appended r24/r25 corrections; r25 says 43 entries and “no unindexed base file remains.”
- `corpus/README.md:859-877` — round-26 frontier disposition: resource verification, deadlines, registry link; limits on C2/C3 claims and remaining receipt gaps.
- `corpus/evidence/README.md:1067-1092` — r25 receipt section, historical base/final measurements and outputs, including final 25/28, selftest 161, final-reader cases 155–161 and base mode-absent rc2. No round-26 receipt section is present.
- `corpus/knowledge/metadata-screen-r25.md:3-5,9-18` — r25 entry metadata, command and population result.
- `corpus/knowledge/metadata-screen-r25.md:31-51` — r25 header grammar, finding/refusal bounds, output/exits and non-composition with `verify-all`.
- `corpus/knowledge/metadata-screen-r25.md:55-67` — r25 population, differential and 154-case checkpoint.
- `corpus/knowledge/metadata-screen-r25.md:71-83` — r25 limits: registry-row/link checks absent, `verified-at` detail not checked, command-first recheck passes default mode, and literal `--root ..` scope.
- `corpus/knowledge/metadata-screen-r25.md:85-99,101-133` — append-only r25 source-precision and final-reader corrections, including fd/snapshot/race limits, header/date rules, recheck cwd, cases 137–161, and path-escaping limits.

## Exact disposition once C1–C3 land

1. **In-place index update required:** `SKILL.md:76`. Update the current gate signature with `--as-of YYYY-MM-DD` and `--registry FILE`; extend its current finding/output/refusal/bounds summary for due/freshness, overdue, registry findings and C1’s no-array/full-file-check behavior. Preserve the 154-case/137–154 and 25/28 material as explicitly r25 historical evidence, or point to its existing correction; do not replace it with an unowned round-26 tally. Current option details already have an appended home at `SKILL.md:460-498`; `SCORECARD.md` owns the round-26 suite tally per `SKILL.md:475-476`.
2. **Append only; do not edit:** `SKILL.md:79-92` and `metadata-screen-r25.md:85-133` are historical correction blocks. The r25 note’s earlier limits at `:71-83` remain accurate as statements about the no-flag/r25 contract; C3 only detects a bare/non-descriptive `verified-at`, not whether verification actually happened (`SKILL.md:485-489`; `corpus/README.md:859-877`). Keep the new C1–C3 facts in their round-26 homes rather than rewriting the r25 account.
3. **Append missing count correction:** `corpus/README.md:79-84` must remain history. Since new round-26 knowledge/lesson rows are now indexed at `:62-66`, append a round-26 count correction after `:84` with a re-derived count; do not assume the total from row deltas.
4. **Append missing evidence index section:** add a new round-26 heading and receipt rows at the end of `corpus/evidence/README.md` (after `:1092`), not inside or in place of the r25 receipt section. The current corpus index already points to `evidence/round26-*` at `corpus/README.md:66`.
5. **No mandatory edit** to `corpus/README.md:55,58-66` or `metadata-screen-r25.md:3-5,31-67,71-83`: these identify r25 history or already index the separate r26 notes; the old no-flag output contract remains in force (`SKILL.md:470-473`).

## Evidence limits

Observed: line locations/content above came from `read` and literal `grep` on the changing lane tree; no LSP device was exposed, so grep is not semantic proof. No tests/builds were run; this was a read-only documentation assignment. Inference: the r25 limits remain accurate for the no-flag contract because the new section says that contract remains in force; the new count must be re-derived by its owner.

VERDICT: map complete; update the current gate index row, append the missing round-26 corpus count correction and evidence receipt index, and preserve r25 errata/history.
Installs: none.
