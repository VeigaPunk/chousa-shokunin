# Round-22 hardening ledger addendum — findings and draft

## Observed facts

- Round 22 closed the separate round-20 named debt: `is_denylist_path` did not match bare path starts (`corpus/knowledge/denylist-r22.md:3,9-21`). The round-11 queue is enumerated by row IDs in `hardening-r10.md:320-349`; row 5 reads “not external verification; refusals absolute (URLs/session/out-of-corpus refused unopened; no fixture can pre-register past a refusal)” (`hardening-r10.md:200`). SCORECARD states the fenced-heading anchor stays named debt (`SCORECARD.md:1164`).
- `sha256sum` of `git show <commit>:corpus/knowledge/hardening-r10.md` was `cb3044844b635feaa78834fc5d080eda646438f42bcfc84a47c2bcdeb04a11fe` at each of `07c425e`, `10083e1`, `a27128e`, `85eda51`, and `fb70ddb`; `git diff 07c425e fb70ddb -- corpus/knowledge/hardening-r10.md` and `git log --oneline 07c425e..fb70ddb -- corpus/knowledge/hardening-r10.md` emitted no output. At registered base `b820e4e40ce52deedf53b191140cd7b08ddda929`, the file has the same SHA and the range log remains empty.
- Gate SHA `bfc291ef526040607436bd4d505354200e4940b4d1e43213008950608f6274ef` → `dfb798b4e2c59f4925f12480a06c603a4eae55a706f6601c31590e5970bda22c`, verified with `git show 07c425e:tools/research-gate.sh | sha256sum` and `git show a27128e:tools/research-gate.sh | sha256sum`. `git log --oneline` identifies `a27128e` as the denylist fix, `85eda51` as the records commit, and `fb70ddb` as the report. SCORECARD `:1142-1156`, LOG `:796-798`.
- Selftest PASS (132 cases, 0 skipped); cases 1–128 are byte-identical to the r21 receipt (SCORECARD `:1150-1156`). Cases 129–132 are `claims-config-start` exit 1, `claims-omp-start` exit 1, `claims-localstate-start` exit 1, and `claims-config-adjacent` exit 0 (`corpus/evidence/deny-r22-20261019T190000Z-selftest.log:129-133`).
- Round-22 commits observed: `10083e1` opening, `a27128e` gate fix, `85eda51` records, `fb70ddb` report (`git log --oneline -n 60`).

## Inference and confidence

- **[INFERENCE; high confidence]** No §3 ledger row or round-11 audit-queue item was closed, changed, or added by round 22: the hardening note is byte-identical across the round-22 commits and at the registered base, and its §3.9 queue (`:320-349`) contains no denylist path-start item. Row 5 remains by-design, not a round-22 closure.
- **[INFERENCE]** `E11` is the next append-only label after E1–E4 (rounds 12–15; `hardening-r10.md:411-520`).

## Unresolved

- No LSP device is mounted (`read xd://lsp` returned “No such tool”). No semantic LSP lookup was possible; conclusions above use direct document text and Git blob/diff evidence.

## Draft to append to `corpus/knowledge/hardening-r10.md`

### Round-22 addendum (2026-10-19, append-only)

E11 — **no §3 ledger row or round-11 audit-queue item was closed, changed,
or added by round 22.** The round closes the separate round-20 named debt:
`is_denylist_path` now matches bare-start `'.config/'*`, `'.omp/'*`, and
`'.local/state/'*` alongside the existing `*/X/*` forms; the matching
path-start citations now refuse (`knowledge/denylist-r22.md:3,18-21;
SCORECARD.md:1142-1156; LOG.md:796`). The round-11 queue remains the row IDs
listed in §3.9 (`:320-349`); no listed item is this denylist path-start
class. Row 5 (`:200`) remains by-design and is not dispositioned here.
The hardening ledger is unchanged at each round-22 landing commit: its
SHA-256 is `cb3044844b635feaa78834fc5d080eda646438f42bcfc84a47c2bcdeb04a11fe`
at `07c425e`, `10083e1`, `a27128e`, `85eda51`, and `fb70ddb`; the path-scoped
diff and log across `07c425e..fb70ddb` are empty.

Gate sha `bfc291ef526040607436bd4d505354200e4940b4d1e43213008950608f6274ef`
→ `dfb798b4e2c59f4925f12480a06c603a4eae55a706f6601c31590e5970bda22c`.
Selftest PASS (132 cases, 0 skipped); cases 1–128 byte-identical vs the r21
receipt. Cases 129–132 pin `.config` start, `.omp` start, `.local/state`
start, and the `.config-adjacent` over-refusal control (`SCORECARD.md:1150-1156`;
`corpus/evidence/deny-r22-20261019T190000Z-selftest.log:129-133`).

## Provenance

- Round-22 commits observed: `10083e1` opening, `a27128e` gate fix, `85eda51` records, `fb70ddb` report (`git log --oneline -n 60`).
- No tools installed or updated.
Installs: none.

VERDICT: High confidence: round 22 changed no §3 ledger row or round-11 queue item; it closed the separate round-20 denylist path-start debt.
