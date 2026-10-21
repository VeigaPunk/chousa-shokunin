# Round-23 ledger addendum — findings

## Observed evidence

- `SCORECARD.md:1189-1203` and `LOG.md:808-810` identify the r23 fix as the round-20-named fenced-heading anchor false-positive in `chain_anchor_at`, not as a round-11 ledger item. `corpus/knowledge/fenced-anchor-r23.md:1-18` records the mechanics and limits.
- Read-only history: `fb70ddb` is the r22 report commit; r23 commits are `f818652` (gate fix), `bfa48b9` (records), and `77bcfd1` (report). Their stats show no edit to `corpus/knowledge/hardening-r10.md` or `corpus/knowledge/audit-r11.md`. `git diff --name-only fb70ddb..77bcfd1 -- corpus/knowledge/hardening-r10.md corpus/knowledge/audit-r11.md` → no output.
- The closest ledger entry is §3.2 row 22 (`hardening-r10.md:222`): “`heading` kind unusable against the archives (zero `#` lines; r9 records use `quote`/`line`)” — disposition `carried (contextual)`; its evidence says heading is covered by synthetic selftests only. The related round-11 queue grouping is item 7 (`hardening-r10.md:343-344`): “22, 24, 25 (documentation/coverage residues): heading-kind coverage; the superseded-receipt citation; the `path#quote:text` seam.” `chain-resolution-r3.md:121-125` confirms the archive-specific zero-heading limit.
- **[INFERENCE]** R23 does not close or disposition-change row 22 / queue item 22: case 129 is a synthetic fenced-source negative control and does not change the archived records' zero-heading population. No §3 row or round-11 queue item was closed, changed in status, or added by r23. The case adds synthetic coverage only.
- Gate blob SHA-256, measured with `git show <commit>:tools/research-gate.sh | sha256sum`: r22 `fb70ddb` → `dfb798b4e2c59f4925f12480a06c603a4eae55a706f6601c31590e5970bda22c`; r23 fix `f818652` → `b5d0f93d38f3c52ee3a4bef38ec524a2bb64e280c9c518f331fa39d082849799`.
- Selftest evidence: r22 132 → r23 `PASS (133 cases, 0 skipped)`; cases 1–128 byte-identical per `LOG.md:810`; new case 129 is `chain-fence-anchor` (`corpus/evidence/fanchor-r23-20261019T192000Z-selftest.log:129-134`). The receipt numbers the former r22 denylist tests 130–133; `denylist-r22.md:5` still says 129–132, so that old case-range citation is stale after the insertion.
- Case-number inconsistency: the added block in `git show f818652 -- tools/research-gate.sh` has comment `# 133 (r23)`, but the committed selftest receipt labels it case 129 and labels the following four r22 denylist tests 130–133 (`fanchor-r23-20261019T192000Z-selftest.log:129-133`). Treat the receipt numbering as observed; both that code comment and `denylist-r22.md:5` (`129–132`) are stale.

## Draft to append to `corpus/knowledge/hardening-r10.md`

```md
### Round-23 addendum (2026-10-19, append-only)

E12 — **No §3 ledger row or round-11 queue item was closed, changed in disposition, or added in r23.** The fix closes the round-20-named fenced-heading anchor false-positive: `chain_anchor_at` now tracks fence state inline, so a heading inside a fence is literal, not an anchor target (`LOG.md:808`; `knowledge/fenced-anchor-r23.md`). The nearest ledger entry remains row 22 (`:222`): “`heading` kind unusable against the archives (zero `#` lines; r9 records use `quote`/`line`)” — **carried (contextual)**. Case 129 adds a synthetic fenced-source control; it does not change the archive-specific limitation. Round-11 queue item 7 (`:343-344`, including row 22's heading-kind coverage) is not dispositioned by this round. The r23 commit range leaves both ledger files unchanged.

Gate blob SHA-256 `dfb798b4e2c59f4925f12480a06c603a4eae55a706f6601c31590e5970bda22c` → `b5d0f93d38f3c52ee3a4bef38ec524a2bb64e280c9c518f331fa39d082849799`. Selftest 132 → 133 cases (0 skipped); cases 1–128 byte-identical; case 129 pins the fenced-anchor arm (`evidence/fanchor-r23-20261019T192000Z-selftest.log`).
```

Installs: none.
VERDICT: Draft supplied; r23 records no round-11 §3 row or queue disposition delta.