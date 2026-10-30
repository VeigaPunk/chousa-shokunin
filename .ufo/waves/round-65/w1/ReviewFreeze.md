# ReviewFreeze — adversarial review of frozen C1/C2 counters and controls (round65)

Seat: ReviewFreeze (leaf reviewer). Date: 2026-10-30.
Scope: adversarial review of the frozen counters, controls and claims at
`corpus/evidence/round65/` (freeze f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd); do-nothing and
boilerplate counterexamples; the 20 distinct C1 cases; the structural-only C2 boundary.
No frozen rule was edited; no production file was written. All probes ran in
`/fast/scratch/hyaku/chousa-r65/ReviewFreeze/` (deleted on exit); evidence under
`.ufo/waves/round-65/w1/ReviewFreeze/`.

## Verdict

No defect found that invalidates either frozen predicate. Both counters behave exactly as
frozen; all four C1 control receipts and the C2 before receipt reproduce byte-for-byte on
case-result lines. Every finding below is a limitation inside the claims' own stated scope
(interface/consistency coverage for C1; structural-only gating for C2), not a freeze error.
The two predicates are sound as frozen; the residual risk is semantic (entailment,
authenticity), which the claims already exclude from these counters.

## What was verified

- Freeze integrity: all 9 frozen artifacts hash-match HEAD blobs; `source-openings.json` is
  untracked preliminary planning (claims.md anticipates this). HEAD == freeze commit.
- C1 controls reproduced with the frozen counter (production lane, scratch `--work`):
  before `CASES=0/20 C1=FAIL missing-target` exit1; positive `CASES=20/20 C1=PASS` exit0;
  always-pass stub `3/20` exit1; always-fail stub `17/20` exit1. Case lines identical to the
  frozen receipts. Work dirs removed on exit each time.
- 20-case distinctness: all 20 case receipts are pairwise unique (sha256 set size = 20); each
  mutates a distinct header element (revision presence/value/length, exit presence/range/form,
  digest presence/value/case/length, path existence/traversal/absoluteness, separator, body).
  See `c1-cases-analysis.txt`.
- C2 do-nothing: in a scratch clone at the freeze, `ENTRY_CHECKS=0/10 C2=FAIL` exit1 — matches
  the frozen before receipt.
- C2 boilerplate: a 9-line meaningless entry + three `| Sxx |` rows + a README mention scores
  `ENTRY_CHECKS=10/10 C2=PASS` exit0 — demonstrates the structural-only boundary the claim admits.
- Draft-entry quotes spot-check against local sources: hashlib docstring quote (file lines
  31–32 inside the documented 27–34 window) and git-cat-file(1) OUTPUT quote both match.

## Findings by severity (all LOW / informational; none block the freeze)

1. LOW — CRLF tolerance is unpinned. The reference validator accepts a receipt with `\r\n`
   line endings (`splitlines()` normalization), so it returns `PASS` on bytes that do not
   literally match the stated empty-separator header layout. None of the 20 frozen cases pins
   byte-exact line endings; the digest binds the named blob, not receipt bytes, so blob binding
   is unaffected. Any conforming re-implementation may legitimately be stricter; the frozen
   counter does not discriminate. Evidence: `c1-boundary-probes.txt` probe.crlf.
2. LOW — Fail-token contract is prefix-only; stderr unconstrained. The 17 invalid cases pass
   with any stdout starting `RECEIPT_PIN=FAIL ` and any payload; valid cases require exact
   `RECEIPT_PIN=PASS`. A tool emitting `RECEIPT_PIN=FAIL <garbage>` satisfies the counter.
3. LOW — Harness-gaming is possible (demoed). A 6-line tool keyed on the `--receipt` basename
   scored `CASES=20/20 C1=PASS` without parsing receipts — the case name leaks via the file
   name given to the tool. Any black-box counter with this argv surface has the same exposure;
   the defense is L1's integration judgment and code review of `tools/receipt-pin.py`, not the
   counter. Consistent with the claim's scope statement.
4. LOW — Counter crash on tool hang. A tool exceeding the 20s per-case timeout kills the
   counter with an uncaught `TimeoutExpired` traceback and no `CASES=x/20` summary (work dir is
   still removed). A hung tool therefore produces no clean FAIL score. Out of claim scope
   (claim targets a correct validator), recorded as robustness debt.
5. LOW — Coverage gaps beyond the 20 cases (all probed against the reference; it rejects each
   correctly): `EXIT=00/01` leading zeros, uppercase receipt revision, trailing-space path,
   `./`-prefixed path, whitespace-only body, missing receipt file, directory-as-receipt,
   bad `--revision` argument (exit 2). The counter does not pin these; the claims already
   scope C1 to "interface/consistency coverage … not general parser safety."
6. LOW (C2) — Structural counter reads working-tree bytes only. The current uncommitted draft
   entry already scores 10/10 pre-commit; commitment and provenance are enforced by the lane
   process (L1 integrates and commits), not by `c2-count.py`. Boilerplate passes (finding in
   `c2-counterexamples.txt`); semantic quality and entailment remain separate reviews, as the
   claim states. Not a counter defect — a boundary confirmation.

## Residual risk and verification gaps

- Entailment/authenticity: neither counter can establish that a measured command truly ran or
  that a source supports a claim; both claims explicitly disclaim this. Residual risk lives in
  seat-level semantic review, not in these counters.
- CRLF and byte-exactness: if the fleet wants byte-exact receipt grammar pinned, a future
  round must add cases (frozen counters cannot change under this freeze).
- Gaming surface (findings 2–3): recommend L1 read the actual `tools/receipt-pin.py`
  implementation before admitting C1; the counter alone cannot exclude a look-up table.
- The C2 draft entry's semantic fidelity (quote context, inference wording) was spot-checked,
  not exhaustively re-derived; the entry-review seats own that.

## Artifacts

- `.ufo/waves/round-65/w1/ReviewFreeze/c1-control-reproductions.txt` — four control reruns.
- `.ufo/waves/round-65/w1/ReviewFreeze/c1-cases-analysis.txt` — 20-case distinctness/mutation table.
- `.ufo/waves/round-65/w1/ReviewFreeze/c1-boundary-probes.txt` — reference-validator and counter robustness probes.
- `.ufo/waves/round-65/w1/ReviewFreeze/c2-counterexamples.txt` — do-nothing and boilerplate runs, quote checks.
- `.ufo/waves/round-65/w1/ReviewFreeze/freeze-integrity.txt` — hash/HEAD/base-blob verification.

No tools installed this seat. No production writes. Scratch `/fast/scratch/hyaku/chousa-r65/ReviewFreeze/` deleted on exit.
