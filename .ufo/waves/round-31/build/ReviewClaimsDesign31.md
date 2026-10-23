# Round 31 W1 — non-author pre-data review: claims.md + c1-count.py + c2-count.py

Reviewer: ChousaR31.ReviewClaimsDesign31 · 2026-10-23 · Axes judged: **coverage, operability**.
Reviewed the working-tree counters (what will run) and diffed them against the frozen commit.
No candidate gate was run; counters were run only against the base gate, per bounds.

## State under review (verified)

- Lane HEAD = `d78d18893849cecb710f3b691ec986e1321d39ee` ("frozen claims design v1 and counters"), jj-colocated, clean except 2 modified files.
- `tools/research-gate.sh` sha256 `ac1315ddaa12e79b68069d1a9866b9b1b55e3a43efef3ba0cb5ca5e665835765` = claims.md's base gate = `git show be7b8d8d:tools/research-gate.sh`. Gate untouched since base; contains **no** `CLAIM_LINE_MISMATCH`/`lineval`/`mislocated`/sha code (grep: no matches) and validates only `id/source/span/expect/marker` (tools/research-gate.sh:1364-1402), so unknown `line`/`sha256` keys are ignored at base — the "before" story is honest.
- Working-tree counters are an **uncommitted "design v2"**: c1 `c0a0908c88b902a7…` vs `154e09e7f73bebaf…` at d78d188; c2 `e26c7751193d81ef…` vs `20ed105bf9308146…`. v2 adds: fixed per-class sub-variants (kills seed luck), finding-emission scoring, dup-id→`none`, `CHOUSA_*` env stripping (c1:266-267, c2 main), exit-2 harness paths, receipt schema v2. Class counts, truths, P1/P2 sentences are unchanged from v1.

## Findings by severity

**F2-1 · Medium · freeze integrity — operative counters diverge from the frozen commit.** claims.md says "Counters (this commit)" (d78d188), but the tree holds a redesigned v2 (diff: 110 insertions/40 deletions across both counters). Kill rule and P1/P2 reference "the frozen counter"; the L1 must commit claims.md+counters as one coherent frozen v2 (or revert) **before any data seat**, else receipts' `counter_sha256` will not match the round's cited artifacts. Mitigating: I ran the v2 counters on the base gate — seeds 1,2 → `LINE_BINDING_MATCH=50/120` and `REVISION_BINDING_MATCH=50/120`, rc=1, per-class split exactly the "Before" prediction (B1-B4+U1 and R1,R2,N1 pass; all M/I and S/I miss; receipts at `/fast/scratch/hyaku/chousa-r31/w1/ReviewClaimsDesign31/{c1,c2}-seed{1,2}.json`, gate_rc=0, ~1.5 s/run).

**F2-2 · Medium · counter overreach vs frozen contract — finding-line format is scored but never frozen.** Both v2 counters fold finding emission into matching: `ok = obs == t and ((cid in flagged) == (t == FINDING_TRUTH))` with `FINDING_RE = ^FINDING CLAIM_(LINE_MISMATCH|SOURCE_REVISION_MISMATCH) severity=(?:warn|crit) surface=claims obs=id=(\S+)`. claims.md names the findings (contract C1.3/C2.2) but never fixes the line format; the gate's existing claim-level findings predominantly use detail `id=$id …` (CLAIM_SPAN_NOT_FOUND, CLAIM_SPAN_UNEXPECTED, CONTRADICTION_MARKER_ABSENT), with `obs=` only in refusal details. A candidate that satisfies every numbered contract item but prints the finding in the dominant existing style (`id=<id>`) scores <120 with no contract violation. This requirement lives only in the v2 docstrings. Fix before data: widen FINDING_RE to accept `id=<id>` or `obs=id=<id>`, or amend claims.md to freeze `obs=id=<id>`. The control wave's full-contract oracle (must reach 120/120) would also catch this — but only if the oracle doesn't happen to use the same new convention its sibling counter invented.

**F2-3 · Low · stray-finding strictness is defensible but unstated.** A candidate emitting CLAIM_LINE_MISMATCH / CLAIM_SOURCE_REVISION_MISMATCH additionally for a record whose truth is `invalid` (alongside CLAIM_RECORD_INVALID) fails that claim via the stray rule. Contract-consistent (invalid has its own finding) but not stated anywhere; same reconciliation as F2-2.

**F2-4 · Low · lane hygiene.** Untracked `corpus/evidence/round31/__pycache__/` (c1/c2 `.cpython-314.pyc`) — someone imported the counters as modules from the lane tree, violating the no-writes-outside-own-dir bound. Not mine; L1 should delete before committing.

## Verified correct (hidden truth vs contract) — no defect found

- **Counts/truths**: C1 12 classes sum 120 = 42 supported/58 mislocated/12 invalid/8 unsupported; C2 9 classes = 40/10/56/14 — exactly claims.md's declared hidden truth. Every claims.md-named class exists (later occurrence, glued, prefix, multi-line start-only/wrong-range, past-EOF, two-occurrences-third-line; one-byte, newline variants, span-hash, mismatch+absent, other-file-hash; upper/63/65/prefix/nonhex/space).
- **Off-by-one / line numbering**: gate is 1-based (`TOK_L1 = count_nl(before)+1`, `TOK_L2 = L1 + count_nl(span)`, tools/research-gate.sh:1313-1317); counters name `put(L)` as `L+1`; v2 B1 pins first/last lines (`"1"`, `"n"`) as explicit off-by-one traps; M5 names n+1..n+40 (grammar-valid, so `mislocated` not `invalid` — correct under contract C1.3).
- **Multi-line (B3/M4)**: `cut ∈ [1, len-1]`, `a ≤ n-4`; left edge `" "`, right edge `","` are both token boundaries; globally unique words ⇒ exactly one occurrence; gate reports `at=lines:a+1-a+2`, so B3's `a+1,a+2` binds and M4's start-only/end-only/wide/late names genuinely do not under "starts on N and ends on M".
- **Invalid lists vs grammar**: all 12 C1 values violate the frozen grammar (0, −3, x7, 5-3, 07, 4-4, "␣4", "4␣", "4-", "-4", 1.5, en-dash 4–5) and none is grammar-valid; all 6 C2 kinds violate 64-lowercase-hex and none is valid. v2 draws each C1 value exactly once per run.
- **No stale class byte-identical to the real file**: S1 changes exactly one ASCII letter (q/x swap is collision-proof) on a line ≠ span line; S2 strip/add/swap all differ (n ≥ 10 lines); S3 hashes the short span; S4 = S1; S5 picks `j ≠ idx` and globally unique words make all 120 files pairwise distinct.
- **Precedence classes match the contract's ordering**: U1 (absent span + `line` ⇒ `unsupported`, not mislocated); S4 (wrong sha + absent span ⇒ `stale`); R2 (right sha + absent span ⇒ `unsupported`); I1 items always have the span present, so no invalid-vs-absent ambiguity exists in either fixture.
- **CRLF**: per-file `nl` used consistently in `make_file`, `one_byte_elsewhere`, and S2 (swap flips LF↔CRLF; strip/add remove/append the file's own nl); CRLF exactly at per-class index ≡ 1 (mod 4) = 32/120 ≈ 27% ("about a quarter" holds).
- **Harness/exit/receipt**: exit 0 iff 120/120, 1 otherwise, 2 on gate-missing/temp/generation/`--keep`/`--receipt` failure; gate rc∉{0,1} or timeout ⇒ all `none` ⇒ 1, `gate_rc`/`gate_timed_out` recorded; receipts carry schema, counter_sha256, gate_sha256, seed, utc, elapsed_s, total, matched, label, predicate_holds, per_class, misses — matches claims.md. `holds = matched == TOTAL`, TOTAL=120 ✓ both. P1/P2 sentences verbatim in docstrings ✓.
- **Opacity/separability**: opaque hex ids/filenames, shuffled JSON key order (base runs prove the gate parses shuffled records — B/R classes matched), `expect=supported` constant, neither fixture carries the other's field.
- **Base-gate runs (only runs performed)**: seeds 1 and 2 per counter, all four → 50/120, rc=1, ~6.2 s total wall.

## Residual risk / verification gaps

- I could not test candidate-gate behavior (bounds); F2-2 is precisely the class of defect the control-wave oracle must be allowed to surface — ensure the oracle's finding format is chosen independently of the counters'.
- 40-bit claim-id and 64-bit file-id birthday collisions (~1.6e-8 / ~4e-16 per run) would spuriously fail a run; v2's dup-id→`none` actually converts a cid collision into a clean miss. Negligible, unchanged from v1.
- FINDING_RE accepts only severity warn|crit — consistent with gate convention for drift findings; a hypothetical `info` emitter would fail (acceptable).
- `__pycache__` provenance seat unknown (control wave?); flagged, not attributed.

**Verdict**: counters are sound measurements of the frozen contracts on every axis I could test (construction, precedence, boundaries, hashing, opacity, exits, receipts); the before-value 50/120 and its per-class decomposition reproduce exactly. **Do not start the data wave until F2-1 (commit a coherent frozen v2) and F2-2 (finding-format vs contract text) are resolved by the L1.** With those two fixes, P1/P2 are fit to score candidates on coverage (C1) and operability (C2).
