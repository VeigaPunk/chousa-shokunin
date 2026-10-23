# ConnectorSiblings31 — sibling-overlap scan for line-range binding and content-hash pinning

Round 31 WAVE 1 BUILD. Lane: chousa-shokunin. Seat: ConnectorSiblings31 (leaf; no
subagents, no background jobs). Date: 2026-10-23. Read-only scan of the fleet siblings
under `/home/vgpnk/Projects/shokunin/*-shokunin/`; nothing written outside this report
path. No network, no installs, no shell commands executed (inspection via `grep`/`read`/
`glob` tools only; every grep bounded by list of explicit lane paths, no `.ufo` archives
scanned except incidental).

## Reference: the two claims (from `corpus/evidence/round31/claims.md`, frozen v1)

- C1 (coverage): claims JSONL optional field `"line"` = `"N"` or `"N-M"` (decimal, N≥1,
  no leading zero, M>N). If present and the claim's span has no boundary-delimited
  occurrence starting on N (ending on N/M), `observed=mislocated` + `CLAIM_LINE_MISMATCH`;
  malformed value → `observed=invalid`. Counter target `LINE_BINDING_MATCH=120/120`
  (before 50/120).
- C2 (operability — lowest scored axis): claims JSONL optional field `"sha256"` = exactly
  64 lowercase hex. If present and ≠ SHA-256 of the exact bytes of the claim's source
  file → `observed=stale` + `CLAIM_SOURCE_REVISION_MISMATCH`, checked before and
  regardless of the span check; malformed → `observed=invalid`. Counter target
  `REVISION_BINDING_MATCH=120/120` (before 50/120). Boundary refusals keep precedence
  (refused sources never read/hashed). Explicitly not git-revision binding.

## Overlap table (sibling hits; path:line = direct read evidence)

| Lane | Tool / knowledge (path:line) | What it does | Line-range binding | Digest pinning | Relation to C1 | Relation to C2 |
|---|---|---|---|---|---|---|
| kumitate | `scripts/cite-check.mjs:37-39,1116-1127,1161-1210,1315-1318` | Doc citation resolver: line refs `:N`, `:N-M`, `L<N>`; findings `LINE_OOR` (ref beyond file line count), `PIN_MISMATCH`, `REV_UNKNOWN`; pins `<rev|revision|rev-pinned|HEAD|commit|sha256|pinned>` + 7-40 hex; `sha256` kind hashes target-file bytes (`sha256File`) and matches prefix; rev pins resolve-by-content (`digest.startsWith`) | Yes — existence-only (`LINE_OOR`), never span-text placement | Yes — exact bytes of cited file | **Extends**: C1 adds boundary-delimited occurrence placement on the named lines; cite-check only checks the lines exist | **Extends/parallel**: same pin mechanism, different carrier (doc prose vs claims record); prefix-hex (7-40) & `startsWith` accepted here, C2 requires exactly 64 |
| kasegi | `corpus/instruments/anchorcheck.py:102-104,118-127,153-163,222-229` | `path:NN[-MM]` backtick-cite grammar; `PAST-EOF` out-of-range; `IN-RANGE(PIN)` versus `<!-- pin: <relpath> <7-40 hex> -->` git blob via `git show`; `PIN-BROKEN` if object missing | Yes — existence/range only | Yes — but git-object (commit) hash, not byte digest of live file | **Partial overlap + weaker**: C1 is the first to require the *text span* to sit on the named lines; anchorcheck only validates line numbers | **Conflict in substrate**: git-revision pin; C2 explicitly pins bytes read, not a commit; also short-hex pins here vs C2's strict 64 |
| kasegi | `corpus/instruments/source-recheck.py:23,70-134` | Manifest per-source `"sha256"` pin (validated by `SHA256_RE=[0-9a-f]{64}` lowercase) + quote assertions; pin mismatch → `MISMATCH` exit 1; quote substring → OK/MISS | No | Yes — exact bytes, `hashlib.sha256` | no (quote-presence only) | Near-mechanism duplicate of C2's hash compare but on snapshot manifests, not claims JSONL; no `stale` verdict name; no precedence rule |
| lore | `corpus/tools/boundary_doc_check.py:331-360,426-454,551-584` | `check_anchors` validates `N[-M]` numeric anchors against source line count (`unresolved anchor` if `last > line_count`); document/checker/legacy-baseline sha256 pins vs git blobs → `document_drift`/`checker_drift` | Yes — existence-only anchor ranges | Yes — git blob bytes + sha256 pins | **Extends**: C1 adds text-placement; lore checks ranges only | Parallel — frozen-doc certification, not claim sources; same "digest differs from committed pin" shape |
| kagi | `corpus/drift-pins.sh:9-18,45-77` | Host-file sha256 baselines; verdicts DRIFT/MISSING/LINK/UNPINNED; symbol pins `#N` line → MOVED/GONE/AMBIG/COUNT; no-hash class for secret files | Yes (for symbols: `#N` line pins) | Yes — exact bytes | C1 is the first non-symbol, text-level placement check | Strongest fleet precedent for *live drift detection on cited artifacts* (v1 history: stale line ref L17→L19 survived 4 rounds); substrate = host/config files |
| kagi | `corpus/inrow-pins.tsv:1-22`, `sources-census.sh` | Per-source S001–S016 `Fetch sha256:` pins recomputed vs captures; verdicts reproduces-raw / reproduces-normalized / non-reproducing | No | Yes | no | **Contrast**: kagi accepts normalized reproduction (rendered-text-v1) as satisfying a pin; C2 is byte-exact, so CRLF/newline variants are stale — stricter, non-interoperable with kagi pins |
| kotoba | `verifiers/verify_skill_checklist.py:10-28,317-319,1274-1315` | SKILL.md checklist boxes pinned by sha256 of *normalized* box text (explicit, schema-pinned normalization rule) | No (line reported, not load-bearing) | Yes — normalized text digest | no | Contrast: pinned normalization (whitespace collapse, join continuation lines) vs C2 byte-exact |
| kotoba | `verifiers/check_substrate_pins.py:75-79,111-112,226-230` | Binary sha256+mtime pins enforced; `BAD_PIN` if pin not 64 hex (case-insensitive regex) | No | Yes | no | Same 64-hex format gate, but accepts uppercase; C2 requires lowercase-only |
| kotoba | `verifiers/verify_corpus_integrity.py`, `verify_corpus_independent.py` | Corpus-index pointer resolution: stale_patterns/missing_paths (existence) | no (path only) | no | no | no |
| kotodama | `tools/gates/typed-pipeline-gate.py:466-479,483-503`; `tools/assemble-d2-typed.py:137-141,373-383`; `assemble-d4-typed.py:467-476` | Derived artifacts digest-pinned (packet/projection/adapter `_sha256`); stale pin → exit 2 named "stale projection pin" | No | Yes | no | Same *stale pin → named refusal* verdict shape; domain = generated projections, not claim sources |
| mori | `tools/mori-content-review.py:19-21,237-240,271-327` | Population pinned via `--expected-sha256` (`CONTENT_REVIEW_POPULATION_PIN`); review rows carry `blob_sha256`, compared to computed blob digests → `CONTENT_REVIEW_STALE` | No | Yes — per-row digest vs computed bytes | no | Direct record-field analogue of C2 (record carries digest; mismatch → stale); subject = reviews/population |
| kake | `scripts/source_recheck.py:2-24,70-134`; `scripts/source_snapshot.py:2-32` | Offline re-check that recorded quotes still occur in captured bodies; snapshot recorder writes `body` files | No | implicit (bodies are snapshots; no pin field) | C1 adds the positional edge; kake checks presence, not location | Flow-analogue (claim-vs-source recheck) without a record-level digest field |
| kaidoku | `tools/round-31/c1-sqlite-positive.py:2-18`; `SKILL.md:333-367` | Counter idiom: envelope subject sha256 must equal carrier frozen sha256; config pre/post pairs with sha256 receipt + shape gate; citation rule "stanza key + receipt, never by bare line number" | No (policy-level only) | Yes — envelope/config bytes | no | Shares the counter-file idiom and sha256-binding discipline; different axis (SQLite envelope) |
| game-dev-3d | `SKILL.md:46-47,53-57,72` | A-row byte-identity: file sha256 == committed manifest row AND path set == `git ls-files` of fresh clone at pin; CHECK 4 verifies cited line exists and endpoint in range but does **not** read line content; citation rule: mutable artifact → section heading + sha256, frozen artifact → line number; defect class `prose-cites-bytes` | Yes — existence-only (`line-range only`) | Yes — raw sha256 stamp | C1 is the executable form of this lane's `prose-cites-bytes` policy (line cites into mutable files are defective; text placement must be re-verified) | Policy consensus: pin mutable bytes by digest — C2 makes it per-claim and runnable |
| tabi | `scripts/check-sources.mjs:24-73`; `SKILL.md:32-42,68-69` | SOURCES.md registry gate (id/kind/tier/status/used_by, `used_by_uncited`); knowledge notes pinned by sha256 first-12; "A hash change means the citations below are stale — re-verify before reuse"; every claim needs measured anchor (path:line) | policy-level | Yes — note pins | no | Supports C2's premise (hash change ⇒ stale) |
| kama | `SKILL.md:96-140` | Endpoint/port pins with DEAD / FOREIGN_SERVICE / MODEL_MISMATCH; "pin fresh, value stale" analysis | No | no (URL/port pins) | no | Different domain (service endpoints) |
| souji | `SKILL.md:35-37`; `tools/` (seat-audit etc.) | Ledger rows: canonical absolute path + sha256 pair verify (vault side); receipt/worktree safety | No | Yes — file pairs | no | Same digest-pair mechanics on ledger rows |
| tsukuroi | `tools/_revision.py`; `SKILL.md:575-627,1006-1010,1523-1530` | Tool self-identity pins (md5+sha256, "identity is by hash, not version string") | No | Yes — own tool bytes | no | Self-pinning only; no citation binding |
| tameshi | `tools/mutate-and-run.sh:16-21,60`; `tools/pin-disposition.py`, `registry.json` | Mutation-sweep restore proof via sha256 before/after; instrument pins & receipts | No | Yes — restore/instrument | no | no relation to claims binding |
| kengaku / revenger / audio / game-dev-2d | (no surfaced hits in tools; audio/game-dev-2d/revenger SKILL.md scans returned no digest/line-binding code) | — | — | — | — | — |

## Verdict input (per hit, as adjacency evidence)

1. **No sibling duplicates C1 or C2 wholesale.** No lane implements a claims-record JSONL
   `"line"` or `"sha256"` field (targeted grep for the exact field literals across all
   enumerated tool dirs found none outside chousa's own round-31 counters).
2. **Line binding fleet-wide is existence/range validation only** — `PAST-EOF`,
   `LINE_OOR`, `anchor_range`, game-dev-3d CHECK 4 all verify the named lines exist and
   are in range; none checks that the *quoted span text* occurs, boundary-delimited,
   starting/ending on those lines. **C1 is the first text-placement check in the fleet**;
   it extends, never duplicates, and the sibling mechanics give it a ready-made vocabulary
   (`IN-RANGE`, `LINE_OOR`) that the gate's `at=` reporting already aligns with.
3. **Content-digest pinning is pervasive and mature** — kasegi source-recheck
   (exact-bytes sha256, 64-lowercase regex), kumitate cite-check, kagi drift-pins /
   inrow-pins, mori content-review (per-row blob pins), kotodama stale-projection pins,
   kotoba box/binary pins, tabi note pins. C2 is therefore a *new carrier* (claims JSONL
   field) for a mechanism the fleet already trusts, not a new mechanism. Its novelty is
   (a) the strict 64-lowercase-hex format gate, (b) verdict precedence *before* the span
   check, (c) "stale" as the named drift finding, (d) per-claim source-byte semantics.
4. **Stated contradictions (not smoothed):**
   - kagi treats `reproduces-normalized` as satisfying a pin; kotoba hashes *normalized*
     box text under a pinned rule; C2 is byte-exact, so a record carried over from either
     convention would read `stale`. C2's byte-exactness is declared and deliberate
     (c2-count has CRLF/LF and final-newline classes), but cross-lane reuse of pinned
     captures will not interoperate.
   - kumitate and kasegi accept 7-40-hex pins (and kumitate matches by prefix
     `digest.startsWith`); C2's contract would classify such a record `invalid`. That is
     a semantic divergence, not a bug in either.
   - kasegi/kumitate/lore pin by git object (commit) identity; C2 explicitly pins bytes
     read, not a commit. Both flag changed sources, but on different substrates (git blob
     can match while the working tree has moved; C2 detects working-tree drift).
   - No sibling defines the *malformed-pin vs boundary-refusal vs span* precedence C2
     does; kotodama's fail-closed stale-refusal (exit 2) is the closest ordering precedent.
5. **Gap that is also an opportunity:** every sibling line checker is existence-only; if
   any sibling later adds text-placement, it will be adjacent to C1. Nothing found today.

## Proposed move (one bounded proposal; for L1 evaluation, not executed here)

**Improve operability (the round's lowest-scored axis) on C2's failure path by emitting
the computed digest next to the expected pin in the `CLAIM_SOURCE_REVISION_MISMATCH`
finding message.** Rationale: the checklist revision clause ("revision read") becomes
runnable, but a stale record gives the operator no way to re-pin without re-deriving the
hash by hand. Sibling practice already prints both sides — kasegi source-recheck
`expected=… actual=…`, kumitate `content pin … does not match sha256(...)=<12-hex>…`,
mori reports per-blob digests. Impact: verdict line (`observed=stale`) and counter
predicate unchanged → coverage unharmed; operability gains a self-service re-pin loop.
Risks: (1) the frozen counters parse gate output — the detail must be appended to the
finding message only, never to the `<id> <observed>` token stream; L1 should confirm the
c1/c2 counters' parsers tolerate a trailing detail token before landing (counters are
not run by this wave); (2) emitting any digest of source bytes is already implied by the
hash computation, so no extra read happens; (3) do not print the digest for refused
sources (contract: never read/hashed).

## Limits

- Only current sibling working trees inspected (read-only); `.ufo` historical archives
  excluded from scanning (only surfaced incidentally in one broad grep); claims of
  "no hit" for kengaku/revenger/audio/game-dev-2d are scans of their published tool dirs
  and SKILL.md, not proof of absence in unpublished history.
- No sibling gate was executed; classification is from code/doc reads with line anchors.
- Long lines truncated at 512 cols in grep display; affected verdicts rest on the read
  excerpts cited above.
- No network, no subagents, no background jobs, no installs; nothing written outside
  `.ufo/waves/round-31/build/ConnectorSiblings31.md`.
