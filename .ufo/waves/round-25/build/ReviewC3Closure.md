# C3 closure review

## Finding
- **P2 — stale open-status restatement:** `SKILL.md:437-439` still says the one live finding is `A-r9.md:50` C3 (`A:76` vs `A:86`) and “remains open pending fix-or-absorb.” This instance was corrected in round 12; the stale sentence misstates current disposition.

## Evidence (observed)
- `corpus/knowledge/audit-r11.md:330-340`: “Correction: A-r9.md line 50 pointer `…A-shokunin-tradition.md:76` → `:86`”; the record SHA moved from `338918fc…` to `dfd2ae1a149b7c87f8ff399522f99c3461570c5ba06ba9d6b18254b15a3c3b9d`. It records: “`verify-all A-r9 --claims claims-r9.jsonl --root ..` → CLEAN” with `sections=5 run=5 absent=0 drift-sections=0 findings=0` and receipt `corpus/evidence/scope-r12-20261019T115519Z-A-fix.log`.
- `corpus/README.md:237-238`: “`A-r9.md:50` (row C3) points at `A:76` while its span occurs at `A:86` (closed at round 12: the pointer was corrected and the live record sha moved to `dfd2ae1a…`...).” `corpus/README.md:480` also says the instance “was corrected at round 12.”
- `corpus/fixtures/archives-r9/A-r9.md:50`: row C3 now points to `research/deep-research-2026-09-28/A-shokunin-tradition.md:86`. The referenced source at `A-shokunin-tradition.md:86` contains the quoted span, “There is no universal sacred number of years or common final examination.”
- Read-only `git log -1 --format='%H%n%s' 5691bf531086dd435006cd9d6157df00933973a3` returned `5691bf531086dd435006cd9d6157df00933973a3` / `round 12: scope-refusal teeth (3 SCOPE_* findings), 8MiB source cap, banner v2 + r12 re-pin, A-r9 C3 fix + errata; selftest 98 (1-85 byte-identical); battery green`. The commit diff changes only the C3 pointer cell from `:76` to `:86` in `A-r9.md`.
- `corpus/knowledge/hardening-r10.md:433-439` records row 56 as “closed(r12, fixture-correction; no check added)” and the revised record SHA; it explicitly preserves the class limitation.

## Minimal replacement for `SKILL.md:437-439`
> The round-11 A-r9 C3 instance was closed in round 12 by correcting `corpus/fixtures/archives-r9/A-r9.md` (SHA-256 `dfd2ae1a149b7c87f8ff399522f99c3461570c5ba06ba9d6b18254b15a3c3b9d`; commit `5691bf531086dd435006cd9d6157df00933973a3`); re-derive the recorded gate verdict with `bash tools/research-gate.sh verify-all corpus/fixtures/archives-r9/A-r9.md --claims corpus/fixtures/claims-r9.jsonl --root ..` (receipt `corpus/evidence/scope-r12-20261019T115519Z-A-fix.log`). The gate still does not pair a row's pointer line with its span's occurrence line.

The `verify-all` receipt establishes a clean five-section gate result; it does **not** mechanically validate pointer-to-span line pairing. Keep the final limitation sentence: the instance is closed, the class is not covered.

## Verification / gaps
- The LSP device is unavailable in this tool environment: `read xd://lsp` returned “No such tool: xd://lsp” and its mounted-device list contained no LSP route. No LSP status/references/definition/diagnostics were possible; literal search was only used to locate README wording, with conclusions grounded in the cited reads and receipt.
- No gate or selftest was run by this read-only seat; the cited round-12 receipt is historical evidence, not a fresh run.
- Installs: none.

VERDICT: Recommend replacing the stale open-status sentence; the A-r9 C3 instance is closed at round 12, while its pointer/span-pairing class remains unverified.