# CriticSourceClaim — attack on the sourced-claim binding (S059)

Seat: chousa round-40 leaf critic. Assigned attack: falsify the sourced-claim
binding — verify that the R1 evidence or knowledge entry actually uses reopened
S059 rather than merely carrying an unrelated source citation.
Lane tip during review: `282dc76856b22747fc531f188df1718a8e18e99a` (plus
`6bc90e04` non-author spot-check, already committed).

Axes attacked: binding authenticity (is the citation the operative premise, not
decorative?), provenance (is S059 the reopened row and is the 2026-10-24
re-open evidenced?), scope fidelity (does the entry stay inside S059's scope?),
and counter independence (can the claim pass via citation alone?).

## Verdict

**Binding holds.** Every falsification probe failed: S059 is the correct row,
it is used as the load-bearing premise of the r40 knowledge entry, the re-open
is recorded and independently re-verified by a non-author live fetch, and the
frozen counters never read the citation. No defect found.

## Exact commands and outputs

1. `read corpus/knowledge/receipt-expectation-digests-r40.md` —
   - `:1` `source: S059 — Python 3.15.1 hashlib, ...#hash-algorithms; local
     application: corpus/evidence/round39/verify-receipts.py:73-79,138-139` —
     matches the claims.md binding (reopened S059 + committed r39 verifier
     behavior) exactly.
   - `:13` uses S059's digest-input semantics ("digest … over the concatenation
     of the bytes supplied to it") as the premise from which the whole-file
     binding conclusion is drawn — load-bearing, not decorative.
   - `:19` Limit honors S059's exclusion: byte identity only, not truth,
     authority, or authorship.

2. `read corpus/evidence/round39/verify-receipts.py:60-148` —
   - `:73-79` `sha256_file` streams `h.update(chunk)` → `h.hexdigest()`;
   - `:138-139` `receipt["expect_sha256"] != sha256_file(args.expectations)` →
     `expect-sha256-mismatch`. The entry's mechanism attribution is accurate
     line-for-line.

3. `read corpus/SOURCES.md:69:raw` — S059 `used-by` =
   `corpus/knowledge/revision-binding-r31.md, corpus/knowledge/receipt-expectation-digests-r40.md`;
   `opened=2026-10-23` unchanged (re-open does not re-date first-open);
   `status=mined`, `recheck=on-release`. `corpus/SOURCES.md:84` — S074
   `rejected` duplicate-row proposal, `used-by=—`, explicit flip condition.
   `SOURCES.md:106` Paths row and `:109` search log record the round-40
   re-open, identified 1 / screened 1 / included through reopened S059.

4. Normalized-text quote check on the committed r31 page capture
   (`.ufo/waves/round-31/build/ScribeSrcHashlib/response.body`): strip tags +
   `html.unescape` → `QUOTE_PRESENT True words= 13`; the lesson's located
   13-word quote "the digest of the concatenation of the data fed to it so
   far" sits verbatim inside the anchored "Hash algorithms" paragraph
   (`id="hash-algorithms"` present). (A raw-byte grep returned 0 because tags
   split the sentence — normalization required; r31's `quote-reopen.out`
   recorded `VERBATIM` the same way.)

5. `timeout 60 bash tools/research-gate.sh verify-metadata
   corpus/knowledge/receipt-expectation-digests-r40.md --root .` →
   `METADATA_COMPLETE=1/1`, `RESEARCH_GATE: CLEAN`, exit 0.

6. `grep -l 'S059\|S074'` over `corpus/evidence/round40/*.{py,json,tsv,txt}`
   and `receipts/*.json` → only `measure-after.txt` (the S074 census W04
   line). `routed-defect-dispositions.json` carries zero `source`/S0 tokens.
   `timeout 60 python3 corpus/evidence/round40/c1-count.py` → six `VERIFY: ok`
   rows, `R39_ACTIVE_RECEIPTS=6/6`, `C1_EXIT=0`. The predicate passes on
   verifier behavior alone — the citation cannot be a compliance shim.

7. `cat .ufo/waves/round-40/controls/r1-stale-before.txt` — committed
   red-before refusals (`expect-sha256-mismatch` ×3, `counter-sha256-mismatch`
   ×1); regenerated receipt `c1-base-s39001-regenerated.json` carries
   `expect_sha256=01cbdc3a…` matching the committed expectations file — the
   exact mechanism S059 grounds.

8. `read corpus/lessons/round-40-verifier-spotcheck.md` — committed non-author
   (hyaku integrator) spot-check `:38`: **live fetch of the S059 page on
   2026-10-24, located quote verified verbatim**, AGREE on the admit; `:39-41`
   AGREE on the S074 reject, the entry admit, and the authorship/truth
   rejected claim. This independently evidences the 2026-10-24 re-open and
   closes the lesson's `:51` "Pending an outside non-author review" note
   (lesson committed at `282dc76`; spot-check at `6bc90e04` — chronologically
   consistent, not stale).

## Falsification probes that failed

- Unrelated-row hypothesis: S059's scope ("digest and hexadecimal
  representation for bytes fed to a hash object") is precisely the semantics
  the entry needs; no scope mismatch.
- Decorative-citation hypothesis: the Observation paragraph's inference
  collapses without S059's premise; the verifier-only portion is separately
  attributed to `:73-79,138-139`.
- Quote-fabrication hypothesis: quote verified verbatim in normalized page
  text; re-verified live by a non-author on the same access date.
- Duplicate-authority hypothesis: S074 exists as `rejected`, not admitted;
  claims.md erratum, lesson `## Gate`, and census output all agree.

## Residual observation (optional hardening, not a defect)

The 2026-10-24 re-open left no lane-side page capture or `tools/quote-reopen.py`
run under `.ufo/waves/round-40/` (unlike r31's `response.body` and r39's
recorded re-open details). The committed non-author live-fetch verification
makes this low-risk, but the smallest safe strengthening is: run
`python3 tools/quote-reopen.py verify` on the 13-word quote and commit its
output beside the round-40 controls. Impacted axis: depth (evidence
redundancy); none harmed.

## No harm observed

Read-only review; no lane production file, git index, or sibling artifact
modified. No tools installed or updated (pacman not touched). No network use.
Report: `.ufo/waves/round-40/w1/CriticSourceClaim.md`.
