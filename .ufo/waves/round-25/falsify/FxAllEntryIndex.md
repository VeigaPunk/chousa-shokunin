# FxAllEntryIndex — round-25 freshness falsify

Checkpoint: observed lane HEAD `e93ac711f885a10d44fdd80a1734997419595b5a` (parent `d8c8cff3923f10481ac9ced66d0af7c41d38130c`); evidence below is read at this full pin.

## Findings

- **P2 — stale current SOURCES summary.** `corpus/README.md:54` describes `SOURCES.md` as “18 opened rows” with “3 kept rejections,” without an as-of date. The current registry has S001–S028 (`corpus/SOURCES.md:11-38`); the round-25 sweep adds S019–S028 (`corpus/SOURCES.md:29-38`), including S025 as a fourth rejected row. Mark the coverage-map prose as a historical r24 snapshot or update it to the current registry. This does not affect the 43 knowledge/lesson count.

## Coverage/count checks

- No knowledge or lesson file was missed: `glob` listed 29 `corpus/knowledge/*.md` and 14 `corpus/lessons/*.md`; checked each basename against coverage-map rows at `corpus/README.md:7-60` (43/43 present). The added entries are explicitly indexed: `knowledge/audit-r11.md` line 55, `lessons/2026-10-19-hardlink-alias-boundary.md` line 56, `lessons/round-24-verifier-spotcheck.md` line 57, `knowledge/metadata-screen-r25.md` line 58, and `lessons/round-25.md` line 60.
- The round-25 count correction at `corpus/README.md:74-80` says 43 = 29 + 14 and is consistent with the actual listings; it also correctly identifies the spot-check and r25 entry/lesson. The count comments at lines 63-72 were not counted as coverage rows.
- Newly indexed evidence is real: the grouped row `corpus/README.md:61` names `evidence/round25-*`; a glob of that path returned the claims, measure script and before/after logs, metadata differential/oracle, and ledger recount files.

## Checkpoint and verification notes

- Preserve the packaging corrections: `0fc037e` omitted `tools/research-gate.sh` (old gate); `d8c8cff` fixed the gate but omitted `corpus/evidence/README.md`; use full pin `e93ac711…` for this review.
- LSP status could not be queried: `xd://lsp` returned “No such tool.” Grep was used only to locate literal rows; the coverage conclusion is from the glob listings and direct README comparison. No gate/selftest was run (not assigned). No tools installed.

VERDICT: No missed knowledge/lesson coverage row; corrected 43-file count is accurate. One actionable freshness defect remains: the undated 18-row/3-rejection SOURCES summary at `corpus/README.md:54`.
