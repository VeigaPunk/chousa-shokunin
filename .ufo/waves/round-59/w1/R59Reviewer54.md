# Round 59 calibration review

## Findings (severity order)

### Blocker — prescribed frozen claims are absent; positive verdict cannot be calibrated

The wave context in `.ufo/waves/round-59/w1-spec.json:10` names `corpus/evidence/round59/claims.md` as frozen and required. A direct read of that exact path returned “Path not found”; the `round59/` evidence directory contains only `census-start.txt` and `controls/c1-before.txt`. The available round58 claims are predecessor evidence, not a substitute for round59's authority. Without the frozen bytes, the claim predicates, source pins, acceptance boundary, and correspondence between any counter and the claim cannot be checked. This is an evidence/authority defect, not evidence that an unseen claim or counter is itself false.

**Falsifier:** supply the authoritative round59 claims at the prescribed path, or identify an authoritative alternate and immutable identity/hash in the handoff; then verify the actual control/counter against those exact bytes. Until then no positive round59 verdict is supportable.

### High — C1 receipt establishes a failing pre-state, not a calibrated positive path

`corpus/evidence/round59/controls/c1-before.txt:1-16` records `C1=FAIL`, `EXIT=1`, `OK=4/4`, `REFUSE=0/7`. Concrete adverse legs include `FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)` (line 3), `SYMLINK_OUT=fail(rc=0, expected refusal)(target-dir-written!)` (line 4), `SYMLINK_CACHE` and `MANY_QUOTES` returning success despite expected refusal (lines 5, 9). Thus the successful empty/rebuild legs (lines 1-2) cannot support a claim of safe operation. The filename and content mark this as `before`; it says nothing about an unidentified later builder or post-change result.

**Falsifier:** a reproducible post-change receipt must identify the exact frozen claim, counter, and builder, produce the declared positive verdict, and pass all corresponding refusal/integrity/side-effect controls. No such receipt is present in the reviewed round59 evidence directory.

## Scope and source grounding

`corpus/evidence/round59/census-start.txt:1-7` records four duplicate-URL-across-scopes warnings (S051, S053, S073, S074, S075), successful reading of `corpus/SOURCES.md`, and `exit=0`. This grounds only that local census observation; it does not establish invalid source contents or independent source truth. No live fetch was performed, consistent with the round spec's open L0 fetch-scope question (`8d77e6c1`); do not treat this offline census as evidence of current external freshness. Since the frozen claims are missing, I cannot determine whether their proposed source scope or citation basis is sound.

## Residual risk and verification gaps

No claim-by-claim assessment, counter-to-predicate mapping, or positive verdict-path calibration is possible until the frozen claims are restored/identified and post-change evidence is recorded. The observed C1 failures are baseline evidence only. The `lsp` device is unavailable in this environment (`xd://lsp` returned “No such tool”), so no semantic references/definition/diagnostics were performed; this review is limited to the captured artifacts. No external fetch or source mutation was performed.

Report trailer: `.ufo/waves/round-59/w1/R59Reviewer54.md`
