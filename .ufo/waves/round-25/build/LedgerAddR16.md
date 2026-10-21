# Round 16 — hardening-r10 ledger delta

## Observed

- No §3 ledger row changed in Round 16; no row quote applies. `git diff --exit-code 58cf0b9 a14516f -- corpus/knowledge/hardening-r10.md` exited 0. Round-16 path history lists only `d36fd63` (gate) and `a14516f` (records) for the relevant paths; `a14516f` changed `mount-alias-r14.md`, `scope-refusal-r12.md`, and added `verification-r16.md`, not `hardening-r10.md`.
- No Round-11 queue item was newly closed, changed, or added in Round 16. The apparent queued→closed correction is documentary: `mount-alias-r14.md` now marks the `--root /` dead-arm closed in Round 15 (`:59-62`); hardening-r10 E4 already records that as the Round-15 queue-only closure, not a §3 row (`hardening-r10.md:549-562`). The Round-16 `--root //` fix is recorded as a gate fix, not a new ledger disposition (`LOG.md:640-645`; `SCORECARD.md:811-825`). New named debts were for the Round-17 queue, not the Round-11 ledger (`verification-r16.md:26-38,44-48`; `SCORECARD.md:819-825`).
- Recorded selftest: PASS (111 cases, 0 skipped); cases 1–110 byte-identical to r15, case 111 pins `--root //` (`LOG.md:641,645`; `verification-r16.md:4-5,74-77`). The round also corrected the r15 battery receipt's fixture paths and `--root ..` (`LOG.md:642`; `verification-r16.md:63`). I did not run the selftest.
- Gate blob SHA-256, verified with the requested `git show <commit>:tools/research-gate.sh | sha256sum`:
  - Before, r16 opening `58cf0b9`: `dd0951d7fb2fbb0a3a9deb41a3e8f8c259e56d7095ee69238fa44b5ed34c87c4` (`LOG.md:633`).
  - After, gate fix `d36fd63` / r16 records `a14516f`: `2b64a1c849b63684a67fd4fe67aad6525e32ca67a826616f9eb8fe7d18323e52` (`SCORECARD.md:811-814`; `verification-r16.md:4`).

## Addendum wording for integration

> ### Round-16 addendum (2026-10-19, append-only)
>
> Round 16 made no change to a §3 ledger row and closed, changed, or added no Round-11 audit-queue item. The `mount-alias-r14.md` “queued” wording corrected this round described the `--root /` dead-arm closure already recorded by Round 15 E4; that was a queue-only closure, not a ledger-row change. Round 16's newly named debts belong to the Round-17 queue. The gate blob SHA-256 moved from `dd0951d7fb2fbb0a3a9deb41a3e8f8c259e56d7095ee69238fa44b5ed34c87c4` to `2b64a1c849b63684a67fd4fe67aad6525e32ca67a826616f9eb8fe7d18323e52`. The recorded selftest passed 111 cases (0 skipped): cases 1–110 remained byte-identical and case 111 pins `--root //`.

## Limits

LSP is unavailable: `read xd://lsp` returned “No such tool”; the mounted-device list contains no `lsp`. This was a source/history audit, not semantic proof from grep. No unresolved gap for the ledger-delta question.

Installs: none.
VERDICT: Round 16 had no §3 ledger-row or Round-11 queue delta; the addendum can state that explicitly with the prior Round-15 closure distinguished.
