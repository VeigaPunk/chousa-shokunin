# ExecC1Impl — C1 line binding (round 31, WAVE 1 BUILD)

## Scope
Implement the frozen C1 contract in `tools/research-gate.sh verify-claims` in a sandbox clone at
`d78d18893849cecb710f3b691ec986e1321d39ee`: optional JSON string field `"line"` (`"N"` / `"N-M"`),
grammar validation → `observed=invalid` (CLAIM_RECORD_INVALID), enumeration of all boundary-delimited
occurrences (tok_span_at returns only the first), binding iff an occurrence spans exactly the named
range (at= set to that occurrence), else `observed=mislocated` + new drift finding
CLAIM_LINE_MISMATCH. Selftest cases appended after the last existing case; header comment / `--help`
/ finding-ID list updated. No existing output-line format changed (mislocated counted only as
N_MISM).

## Files changed
- `repo/tools/research-gate.sh` (clone) — diff vs d78d188 → `c1.patch` (212 insertions / 23 deletions).
- `.ufo/waves/round-31/build/ExecC1Impl/c1.patch` (deliverable; sha256
  `53490a1b29e0e45029cecf68aef641b6322c2cb2b51dc4962e17a43c5f5bd8e7`, 317 lines).
- `.ufo/waves/round-31/build/ExecC1Impl.md` (this report).

## Implementation notes
- `json_has_key()` added: detects a present key of ANY value type; `json_str` only matches string
  values, so present-empty / present-non-string are distinguishable from an absent key (both → invalid).
- `tok_span_all()` added: iterates every boundary-delimited occurrence, reusing
  `tok_left_ok`/`tok_right_ok`/`count_nl` and the same hex-escaped grep -z -P matcher.
- Grammar: `^[1-9][0-9]*$` or `^[1-9][0-9]*-[1-9][0-9]*$` with M>N (decimal compare via string
  length + lexicographic, arithmetic-free → no overflow). `"4-4"`, `"5-3"`, `"07"`, `"0"`,
  `" 4"`, `"4 "`, `"4-"`, `"-4"`, `"x7"`, `"1.5"`, `"4–5"` (en-dash), `""`, non-string `5`
  → all `observed=invalid`.
- Span present + line present: enumerate; bound iff start/end == (N,N) or (N,M). Bound → existing
  verdict with `at=` = bound occurrence. Unbound → `observed=mislocated` + `FINDING
  CLAIM_LINE_MISMATCH severity=warn surface=claims obs=id=… line=N-M
  first_delimited_occurrence=<first>`; counted only via N_MISM (summary line unchanged).
- Span absent → `unsupported` path unchanged (even with line present). Line absent → unchanged.

## Evidence (all commands run in the clone, `/fast/scratch/hyaku/chousa-r31/w1/ExecC1Impl/repo`)
- `timeout 1800 bash tools/research-gate.sh --selftest` → rc=0,
  `RESEARCH_GATE_SELFTEST: PASS (219 cases, 0 skipped)`. Base at d78d188 was already 215 cases
  (claims.md's "154 at base" is stale vs the frozen commit); new cases 216–219:
  ```
  ok-case  216 c1-pass-bound                exit=0
  ok-case  217 c1-fail-mislocated           exit=1
  ok-case  218 c1-fail-invalid-line         exit=1
  ok-case  219 c1-pass-no-line              exit=0
  ```
- `bash tools/research-gate.sh verify-claims corpus/fixtures/claims-r2.jsonl --root /home/vgpnk/Projects/shokunin`
  → rc=0, `VERDICT_BEARING_CLAIMS=17/17`,
  `RESEARCH_GATE: CLEAN (claims=17 supported=13 contradicted=2 unsupported=2 mismatched=0
  unproven=0 refused=0 invalid=0 findings=0 drift=0)`. Byte-identical to the base gate's output at
  the same `CHOUSA_NOW_EPOCH` (diff empty).
- `bash tools/research-gate.sh --drift corpus/evidence/gate-baseline-r12-20261019T115519Z.json`
  → rc=0, `GATE_DRIFT: none` (same as base at d78d188).
- `bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3.md --root /home/vgpnk/Projects/shokunin`
  → rc=0, `RESOLVED_HOPS=17/22` CLEAN.
- Hand-made fixtures (`fix/` in scratch): pass file 6/6 CLEAN (single-line L1 at=line:1; later
  delimited occurrence B1 at=line:11; multi-line ML1 lines:7-8 and ML2 lines:2-3; no-line N1
  unchanged; U1 span-absent+line → unsupported); fail file 7/7 mislocated (wrong line, glued copy on
  named line, prefix on named line, wrong multi-line range, past EOF, two real occurrences with a
  third line named), each with `FINDING CLAIM_LINE_MISMATCH`; invalid file 13/13 invalid; interaction
  file: contradicted bound+marker → contradicted, unbound → mislocated, `expect=unsupported` bound
  → supported + CLAIM_SPAN_UNEXPECTED.

## Candidate
- Gate SHA-256: `6c581ccf8cb024dfc6af5de8bf7f00cdebbeabf5a3cbed1aa24bef0297a1657a`
- Patch SHA-256: `53490a1b29e0e45029cecf68aef641b6322c2cb2b51dc4962e17a43c5f5bd8e7`

## Tooling channel
No tools installed or updated (none needed; only GNU grep -z/-P already required by the gate).

## Answer to L1 question (lane gate rewrite at 04:26:45Z)
No — I never wrote or copied over the lane gate. All edit/write calls targeted the clone
`/fast/scratch/hyaku/chousa-r31/w1/ExecC1Impl/repo/tools/research-gate.sh`; the lane gate was only
read (read-only opens). Lane writes are limited to `c1.patch` and this report under
`.ufo/waves/round-31/build/ExecC1Impl/`.

## Limits
- `c1-count.py` / `c2-count.py` were NOT run against the candidate (wave rule; scoring is L1's).
- `json_has_key` uses the same flat-object regex style as `json_str`; a `"line"` key literally
  appearing inside another string value would be misread (pre-existing limitation class for all fields).

## Risks
- Selftest count moved 215 → 219 (not "154 + new"); the base at the frozen commit already had 215.
- The drift baseline still reports `none` (canonical verify-all fixture uses no "line" field).
