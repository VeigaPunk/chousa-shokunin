# ScoutLanePointerUse — C1 "line" / C2 "sha256": backward-compat risk & adoption surface

Scope: lane `/home/vgpnk/Projects/shokunin/chousa-shokunin` + fleet `research/` tree. Read-only; no counters run (control wave owns them); no edits outside this build dir.

## 1. Claims-JSONL inventory (everything verify-claims/verify-all consumes)

| file | records | keys observed |
|---|---|---|
| corpus/fixtures/claims-r2.jsonl | 17 | id, claim, source, span, expect, marker |
| corpus/fixtures/claims-r9.jsonl | 10 | id, claim, source, span, expect, marker |
| corpus/fixtures/integrity-r7.claims.jsonl | 3 | id, source, span, expect |
| corpus/fixtures/integrity-r7-broken.claims.jsonl | 3 | id, source, span, expect |
| corpus/fixtures/full-r6.claims.jsonl | 3 | id, source, span, expect |
| corpus/fixtures/full-r6-broken.claims.jsonl | 3 | id, source, span, expect |
| corpus/fixtures/archives-r9/controls/A-r9-span-not-found.claims.jsonl | 10 | id, claim, source, span, expect, marker |
| corpus/evidence/verify-all-manifest.jsonl | (manifest, not claims) | schema/ts/record/record_sha256/gate_sha256/sections/verdict |
| .ufo/waves/round-29/build/RevengerGateSpan/probe.jsonl | 14 (round-29 scratch, not consumed) | id, source, span, expect |

Committed claims records total: **49**. `wc -l` exit 0.

Fleet `research/` tree: **zero .jsonl files** (glob `research/**/*.jsonl`, gitignore:false, hidden:true → "No files found matching pattern"; tree holds .json/.toml probe artifacts of other lanes, none consumed by chousa's gate).

## 2. Key audit (the yes/no)

`grep '"line"|"sha256"|line_no|"sha"'` over lane `**/*.jsonl` → **No matches found**.
Same pattern over `tools/research-gate.sh` → **No matches found** (so every selftest claims fixture — all heredoc/printf-generated: claims-pass, claims-fail-*, claims-boundary-*, claims-cap-*, claims-hardlink-*, claims-cross-device, claims-root-slash-*, claims-config-*, claims-omp-*, claims-localstate-*, claims-registry-colon-deny, etc. — carries only id/source/span/expect/marker/marker_default).

- No committed claim record carries `"line"`, `"sha256"`, `line_no`, or `"sha"` — **not even as substring values**, so no naive-parser confusion is possible on existing input.
- The only sha256-ish keys in the lane are the verify-all **manifest** fields `record_sha256`/`gate_sha256` (corpus/evidence/verify-all-manifest.jsonl). They live on manifest objects, never on claim records; verify-claims does not parse manifests. C2's `"sha256"` is a claim-record field → no collision.

## 3. Adoption surface — pointer counts

- In-record `## Claims` tables (18 record files under corpus/fixtures incl. archives-r9 + controls): **77 data rows, 75 pointer cells already carry a `path:N` line suffix** (awk over each file; header/separator rows excluded). Per file: chain-r3.md 2/1, chain-r3-broken.md 1/1, full-r6.md 3/3, full-r6-broken.md 3/3, full-r6-absent.md 1/1, integrity-r7.md 3/3, integrity-r7-broken.md 3/3, sweeps-r5.md 3/3, sweeps-r5-broken.md 1/0, A-r9.md 5/5, B-r9.md 6/6, C-r9.md 8/8, controls A-anchor-missing 5/5, A-span-not-found 5/5, B-false-sweep 6/6, B-rejection-missing-flip 6/6, C-dangling-ref 8/8, C-structure-break 8/8 (rows/with-line).
- corpus/knowledge/*.md: **127 `path:line` tokens, 87 unique** (e.g. `SKILL.md:58`, `tools/research-gate.sh:812-831`, `MINT.md:75-98`). Convention is pervasive; these are the natural sources to backfill a C1 `"line"` value.
- The `at=line:N` verdict wording already emitted by the gate (`CLAIM id=… at=line:64`) is the line-number source the C1 contract points at (claims.md §C1.3).

## 4. Verdict

**Existing input would NOT change verdict under C1/C2 — no.** Both contracts are explicit that a missing field is behaviour-preserving (claims.md C1.4 / C2.4: `"line"`/`"sha256"` absent → behaviour unchanged; C2.3: boundary refusals keep precedence). No lane or fleet-research claims record, and no selftest claims fixture, carries the fields (or confusable `line_no`/`sha` keys), so every current record hits the "absent → unchanged" branch; all committed expectations (claims-r2 17/17 CLEAN, claims-r9 10/10, r6/r7 companions, sweeps, chain) keep identical verdicts and findings. No drift finding (CLAIM_LINE_MISMATCH / CLAIM_SOURCE_REVISION_MISMATCH) can fire on existing input.

Caveat [INFERENCE]: the inference that "absent → unchanged" holds assumes the landed gate implements the frozen contract faithfully; the pre-data control wave (not run by this seat) is the arbiter. Also note the lane's own record pointers (e.g. `A-r9.md:50` C3 pointer `:76` vs span at `:86`) are a documented pre-existing line-binding defect class the new C1 finding distinguishes from — but that is a record-table pointer, not a claims-JSONL `"line"` field, so it does not affect C1's input surface.

## 5. Limits
- Fleet scan: glob over the whole fleet root timed out (5s) on non-research dirs; I scoped to `research/` (complete: 0 jsonl) plus the lane. Other lanes' corpus dirs not exhaustively globbed (out of the stated scope).
- No c1-count.py/c2-count.py run (prohibited pre-control); no gate edits.
- No network used; no installs.
