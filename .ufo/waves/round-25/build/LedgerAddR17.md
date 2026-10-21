# Round-17 ledger addendum findings

## Observed

- `SCORECARD.md:850-880` and `LOG.md:657-665`: round 17 fixed the fenced-heading shadow in the scope screen; the before result was CLEAN and the landed result was `SCOPE_BOUNTY_ABSORBED` (warn) + DRIFT. Gate abbreviated SHA moved `2b64a1c8…` → `c2915f24…`.
- Exact gate-blob command results:
  - `git show eaa3bbd:tools/research-gate.sh | sha256sum` → `2b64a1c849b63684a67fd4fe67aad6525e32ca67a826616f9eb8fe7d18323e52  -`
  - `git show 6e328ce:tools/research-gate.sh | sha256sum` → `c2915f24d73d656ca23b7f6228cbdd502c27a8c07670776fed84c70f278266f8  -`
  - The post-fix hash is unchanged at records commit `9912f93` (same SHA-256).
- Selftest receipt `corpus/evidence/fence-r17-20261019T171200Z-selftest.log:112-117`: cases 112 `scope-fence-shadow` (exit 1), 113 `scope-fence-only` (0), 114 `scope-fence-nested` (1), 115 `scope-fence-indented` (1), 116 `scope-fence-unclosed` (1); `PASS (116 cases, 0 skipped)`. Mechanics/shape outcomes are also recorded in `corpus/knowledge/fenced-heading-r17.md:20-44`.
- No §3 ledger row or round-11 queue item was closed, changed, or added in r17. The r17 commit range is `eaa3bbd` (opening) through `02b70c0` (report); `git diff --name-status 0a2d7ce..02b70c0 -- corpus/knowledge/hardening-r10.md` returned no output. The note SHA at both endpoints was `1dd34d97805690bc178778996182b6652e5ec45462006fce9187742b0a313359` (`git show 0a2d7ce:corpus/knowledge/hardening-r10.md | sha256sum` and `git show 02b70c0:corpus/knowledge/hardening-r10.md | sha256sum`).
- Adjacent context, not an r17 delta: §3.8 row 70 reads `| 70 | scope-refusal finding IDs never landed (documentary province boundary) | r1 | operator | README gaps |` (`hardening-r10.md:299-300`). §6 E1 already supersedes its disposition to `closed(r12)` for declared-scope IDs (`:444-451`). Round 17 fixes fenced headings, not the row's declared-scope disposition; no queue change follows. The later independent recheck explicitly notes the fenced-heading cases pass while the screen remains declaration-only (`:584-586`).

## Draft for integration

The E5 label is inferred from the existing E1–E4 append-only sequence.

### Round-17 addendum (2026-10-19, append-only)

E5 — the fenced-heading scope-screen shadow: `load_sections` treated a
fenced `## Meta` as a section, letting it shadow a real refused-province
declaration. The pre-round gate returned CLEAN; the landed two-pass fence
pairer returns `SCOPE_BOUNTY_ABSORBED` (warn) + DRIFT for the shadowed
`domain: bounty program scope` case. Gate
`2b64a1c849b63684a67fd4fe67aad6525e32ca67a826616f9eb8fe7d18323e52` →
`c2915f24d73d656ca23b7f6228cbdd502c27a8c07670776fed84c70f278266f8`.
Selftest cases 112–116 pin the simple shadow, fenced-only phantom,
nested fence, indented closer and unclosed fence; receipt
`evidence/fence-r17-20261019T171200Z-selftest.log` records PASS (116 cases,
0 skipped).

No ledger row or round-11 queue item was closed, changed, or added by r17.
The nearby row 70 (`§3.8`, `:299-300`) was already superseded to
`closed(r12)` by E1 (`§6`, `:444-451`); the r17 parser fix adds no new
ledger disposition.

VERDICT: Round 17 changed gate behavior and selftest cases 112–116, but no ledger row or round-11 queue item; ready for integration as a no-delta addendum.
Installs: none.
