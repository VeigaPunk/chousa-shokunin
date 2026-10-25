# ScribeKnowledgeEntry — r40 knowledge-entry audit

Assignee: leaf L2 seat, chousa round 40. Milestone: independently audit the frozen R1
receipt-integrity predicate and R2–R5 calibration dispositions; no production edits.
Subject: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/receipt-expectation-digests-r40.md`
(committed at `d164f88eb71a6c48a66ae1e7abfcb5fef82219d9`; 23 lines).
Lane tip at audit: `6bc90e0` (`round-40 verifier spot-check`). Baseline: `691d26476ac39b8ec8b65155b41199e6f6d1f299`.

## Assigned attack

Review the entry for (1) provenance-trio ordering, (2) S059 citation scope, (3) exact
anchor, (4) fact-versus-inference separation, (5) runnable recheck. Return precise
corrections only; no product edits.

## Verdict

| Sub-axis | Verdict | Basis |
|---|---|---|
| Provenance-trio ordering | PASS — no correction | Lines 1–3 are `source:` → `verified-at:` → `recheck:` (criterion-6 order); `verify-metadata` returned `CLEAN`, exit 0. Title-after-trio matches the three source-first r26 entries (4/53 entries source-first; 49/53 title-first). |
| S059 citation scope | PASS — one inference label needed | S059 `used-by` names this entry; the sourced sentence stays inside the row's scope (digest of fed bytes, not the revision-pin contract); "local application:" cleanly separates own work from the source. But the Observation's `Therefore` step transfers API semantics to the lane's receipt policy without an inference label (F2). |
| Exact anchor | PASS at section level; precision correction | `#hash-algorithms` resolves: `<section id="hash-algorithms">` at byte 13791 of the pinned page, `<h2>Hash algorithms` at 13835, and the quoted sentence sits in that section's first paragraph. The entry's paraphrase drops the `update()`/`so far` clause that licenses chunked streaming; it also does not carry the paragraph/quote in the header (F1). |
| Fact-versus-inference separation | One correction | Every numeric/refusal claim re-derived true (table below). The deduction is marked `Therefore` but not labelled as inference, and the Limit does not exclude the lane-policy step that the lesson itself excludes (F2). |
| Runnable recheck | PASS — optional hardening | Command resolves from the stated lane root; the counter roots itself at `pathlib.Path(__file__).resolve().parents[3]`, so cwd-independent; no writes; exit 0 only at 6/6. It re-derives the receipt set, not the source anchor (F6, optional). |

Net: the entry is admit-worthy and factually sound; five precise text corrections and one
optional limit addition are listed below.

## Exact commands and observed output

All commands run from `/home/vgpnk/Projects/shokunin/chousa-shokunin` unless stated.

1. Metadata gate on the entry (read-only):
```
bash tools/research-gate.sh verify-metadata corpus/knowledge/receipt-expectation-digests-r40.md --root .
```
```
research-gate v2 — ts=2026-10-24T07:19:48Z — mode=verify-metadata — path=corpus/knowledge/receipt-expectation-digests-r40.md — root=.
META entry=receipt-expectation-digests-r40.md source=present verified_at=dated recheck=scheduled verdict=clean
METADATA_COMPLETE=1/1
RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)
EXIT=0
```

2. Header-layout census across `corpus/knowledge/*.md` (first-line key):
```
entries 53 source-first 4 title-first 49 other []
```
The four source-first entries are `reader-allocation-r26.md`, `recheck-due-r26.md`,
`registry-link-r26.md`, `receipt-expectation-digests-r40.md`; all three r26 entries place
the H1 immediately after the trio, exactly as this entry does.

3. Expectation bytes at r39 tip and at the receipts' landing commit:
```
git show 691d264:corpus/evidence/round39/expectations.jsonl | sha256sum
→ 01cbdc3a8208a257e2b0ea4304c87a6d74be313a722cf667c5d126a4c29c583a  -
git show 6d914e9:corpus/evidence/round39/expectations.jsonl | sha256sum
→ 01cbdc3a8208a257e2b0ea4304c87a6d74be313a722cf667c5d126a4c29c583a  -
sha256sum corpus/evidence/round39/expectations.jsonl
→ 01cbdc3a… (same)
```

4. Receipt digests (JSON fields `expect_sha256`, `counter_sha256`):
```
r39/c1-after-s39011.json         expect 3abd2dcb counter 91618e91
r39/c1-base-s39001.json          expect 3abd2dcb counter 91618e91
r39/c1-mutenv-s39003.json        expect 3abd2dcb counter 1c3b2a9e
r39/c1-mutenv-s39013.json        expect 3abd2dcb counter 91618e91
r39/c1-after-s39111.json         expect 01cbdc3a counter 91618e91
r40/c1-after-s39011-regenerated  expect 01cbdc3a counter 91618e91
r40/c1-base-s39001-regenerated   expect 01cbdc3a counter 91618e91
r40/c1-mutenv-s39013-regenerated expect 01cbdc3a counter 91618e91
```
Exactly four c1 receipts carried `3abd2dcb…`; all three reissues carry `01cbdc3a…`; the
four stale originals remain at their r39 paths.

5. Refusal order (committed red-before evidence, `.ufo/waves/round-40/controls/r1-stale-before.txt`):
```
c1-base-s39001.json   rc=1 VERIFY-FAIL: expect-sha256-mismatch
c1-after-s39011.json  rc=1 VERIFY-FAIL: expect-sha256-mismatch
c1-mutenv-s39003.json rc=1 VERIFY-FAIL: counter-sha256-mismatch
c1-mutenv-s39013.json rc=1 VERIFY-FAIL: expect-sha256-mismatch
```
This matches the entry: three expectation refusals; the draft refuses first on the counter
check (verifier lines 131–134 precede 136–139).

6. The entry's causal claim "its counter bytes were not committed" — blob sweep over every
revision of the bound path:
```
git rev-list --all -- corpus/evidence/round39/c1-count.py   # 3 revisions
sha256 of every blob → 91618e91640f748d… only
draft receipt counter_sha256 → 1c3b2a9e453ebfdc33993c85c758d566c806a936f414178730780a09684848da
```
No committed blob of `corpus/evidence/round39/c1-count.py` hashes to `1c3b2a9e…`. The
entry's "not committed" is therefore proven, not inferred.

7. Exact anchor against the tracked r31 page copy
(`.ufo/waves/round-31/build/ScribeSrcHashlib/response.body`, sha256
`553f4f2a9e686e6f051c8b12bd5469e7fdd6cc7116b2f6d2beba68c1a703af10`, 121928 bytes):
```
<section id="hash-algorithms">      byte 13791
<h2>Hash algorithms                  byte 13835
paragraph (tags stripped): "There is one constructor method named for each type of hash.
All return a hash object with the same simple interface. … You can now feed this object
with bytes-like objects (normally bytes) using the update method. At any point you can ask
it for the digest of the concatenation of the data fed to it so far using the digest() or
hexdigest() methods."
```
The lesson's anchor (“Hash algorithms,” paragraph beginning “There is one constructor
method…”) and its 13-word quote are verbatim in this copy. The URL fragment resolves.

8. Cited verifier spans (`corpus/evidence/round39/verify-receipts.py`):
```
73–78  def sha256_file(path) … return h.hexdigest()      # 79 is blank
131–134 counter_sha256 compare
136–139 expectations isfile + expect_sha256 compare
151     frozen = load_frozen_expectations(args.expectations, fam_key)
```
`138–139` is exact; `73–79` includes line 79, which is blank.

## Findings and precise corrections

### F1 — exact anchor: quote the clause, not a paraphrase (low–medium)

The Observation says “S059 states that a hash object's digest is computed over the
concatenation of the bytes supplied to it.” The page's clause is “the digest of the
concatenation of the data fed to it so far”, licensed by “feed this object … using the
update method”. The `update()`/`so far` qualifier is what makes `sha256_file`'s chunked
streaming (lines 73–78) a digest of the whole file; the paraphrase drops it.

- Observation, replace: `S059 states that a hash object's digest is computed over the concatenation of the bytes supplied to it.`
  with: `S059 states: "the digest of the concatenation of the data fed to it so far" (Hash algorithms, paragraph beginning "There is one constructor method named for each type of hash"), the data having been fed through `update()`.`
- Header, append to the source value after the URL:
  `(\`Hash algorithms\`, paragraph beginning "There is one constructor method named for each type of hash"; located quote: "the digest of the concatenation of the data fed to it so far")`.
  A URL fragment alone is a resolvable section anchor, but criterion 6's "exact anchor"
  and the lane's own S059 row name the section plus the located text; the entry currently
  makes the reader re-open the page to find the quoted sentence.

### F2 — fact-versus-inference: label the policy step (medium)

The sentence after the verifier citation is a deduction from two premises (source
semantics + verifier compare), and its conclusion is about the lane's receipt policy. The
lesson itself says S059 “grounds the API's digest input, not the receipt policy or claim
truth” (`corpus/lessons/round-40.md:40`); the entry's Limit excludes truth, authority, and
authorship but not the policy transfer.

- Observation, replace: `Therefore a receipt's expectation digest binds the exact file bytes, not only the individual rows it happens to cite.`
  with: `Lane inference (S059's API semantics + the verifier's compare at :138–139): a receipt's expectation digest binds the exact bytes of the file passed as `--expectations`, not only the individual rows it cites. The choice to gate receipts on that digest is the lane's design, not a statement of S059.`
- Optional Limit addition (my reading of the verifier, not an executed forgery): `Nor does
  a matching digest establish that the harness ran: every check is a byte binding, and a
  receipt constructed to satisfy the bindings would pass the same checks.`

### F3 — `verified-at:` mixes a work action into the check field (medium)

Current value: `2026-10-24 — re-opened S059 and re-derived the r39 stale-expectation
refusal and regenerated active receipt set`. "Re-opened" and "re-derived" state what was
checked; "regenerated active receipt set" is the work product, and no artifact is named.

- Replace line 2 with:
  `verified-at: 2026-10-24 — S059 re-opened and the quote re-located (pinned page copy .ufo/waves/round-31/build/ScribeSrcHashlib/response.body, sha256 553f4f2a…); the stale refusal re-derived at r39 tip 691d264 and the six-row active set verified 6/6 at work commit d164f88 (evidence: .ufo/waves/round-40/controls/r1-stale-before.txt, corpus/evidence/round40/measure-after.txt)`

  This keeps the date and the checks, and names resolvable evidence. It does not claim an
  independent seat performed them: the r40 lesson records an L1 host-mapped construction
  seat, and the non-author spot-check (`corpus/lessons/round-40-verifier-spotcheck.md`)
  separately re-ran C1 at `282dc76` with agreement.

### F4 — pin the historical claim to its owning revision (low)

“At round-39 closure, `expectations.jsonl` was `01cbdc3a…`” names no path or revision.
Re-derived: the file is `corpus/evidence/round39/expectations.jsonl`; it hashed
`01cbdc3a…` at r39 tip `691d264`; the four stale receipts and those bytes both landed in
`6d914e9`, so the mismatch existed at landing.

- Replace: `At round-39 closure, `expectations.jsonl` was `01cbdc3a…`, while four c1 receipts carried `3abd2dcb…`.`
  with: `At round-39 closure (`691d264`), `corpus/evidence/round39/expectations.jsonl` hashed `01cbdc3a…`, while four c1 receipts carried `3abd2dcb…`; the receipts and those expectation bytes landed in the same commit, `6d914e9`.`

### F5 — cited span includes a blank line (info)

`73-79` names the function plus the blank separator; the function body is `73-78`.
`138-139` is exact. Fix both occurrences in the entry (`source:` and Observation) to
`73-78,138-139`. The same span is restated at `corpus/lessons/round-40.md:36`; that file is
out of this seat's write scope, so flag it to the lesson owner rather than editing it.

### F6 — recheck is runnable; optional second command (low)

`recheck: 90d — from the lane root ... run python3 corpus/evidence/round40/c1-count.py`
is compliant and runnable: the counter derives `ROOT` from `__file__` (`parents[3]`), so it
works from any cwd; it reads the six-row manifest, calls the committed verifier with the
committed expectations path, writes nothing, prints `R39_ACTIVE_RECEIPTS=6/6`, and returns
0 only at 6/6. It does not re-open S059 or screen the header, so a source/anchor/header
drift would not surface from the command alone; the `90d` token still schedules the review.

- Optional, matching the r26 entries' two-command precedent: append
  `; and \`bash tools/research-gate.sh verify-metadata corpus/knowledge/receipt-expectation-digests-r40.md --root .\``.
  No defect if left as is: criterion 6 permits a cadence with one command.

### Not a finding — ordering

The trio order is `source:` → `verified-at:` → `recheck:` and the gate is CLEAN. The H1
sits after the trio; that is the r26 source-first layout, not an inversion. Moving the H1
to line 1 would match the 49-title-first majority but changes nothing the gate or the
criterion reads; no correction is warranted.

### Not a finding — S059 scope

S059's `used-by` cell is `corpus/knowledge/revision-binding-r31.md,
corpus/knowledge/receipt-expectation-digests-r40.md` (row still `mined`, recheck
`on-release`). The entry's sourced sentence is inside the row's scope; the row's exclusion
of “the lane's revision-pin contract” is respected because the verifier is cited as local
application, not as source support. No correction beyond F2's label.

## Factual claims re-derived true

| Entry claim | Evidence |
|---|---|
| `expectations.jsonl` was `01cbdc3a…` at r39 closure | `git show 691d264:…/expectations.jsonl \| sha256sum`; also at `6d914e9` |
| Four c1 receipts carried `3abd2dcb…` | JSON field read of the four r39 c1 receipts |
| Three refused `expect-sha256-mismatch` | `r1-stale-before.txt` (committed at `d164f88`) |
| Draft refused first on `counter-sha256-mismatch`; counter bytes not committed | `r1-stale-before.txt`; blob sweep: only `91618e91…` ever committed at that path |
| Three reissues use committed expectation bytes | JSON field read: all three `expect_sha256=01cbdc3a…` |
| Originals preserved and not relabelled valid | Four stale files still at `corpus/evidence/round39/receipts/`; excluded from the six-row manifest |
| Verifier compares whole-file digest before re-deriving rows | `verify-receipts.py:73-78,131-139,151` |
| Quote verbatim; anchor resolves | Pinned `response.body` (sha256 `553f4f2a…`), section id byte 13791 |
| Limit “not truth/authority/authorship” | Article text; no source or verifier check establishes those |

## Depth observation (optional, not a defect)

The verifier hashes `args.expectations` at line 138 and then re-opens the same path at
line 151 (`load_frozen_expectations`). A rewrite between the two opens would not be
detected; the digest binds the bytes at check time, not necessarily the rows parsed after.
The entry's ordering statement is accurate. If the Limit is touched for F2, one clause
naming this re-open window would make the byte-identity limit complete. This is my code
reading, not an executed race.

## Gates, surfaces, scope

- Gates run: `verify-metadata` on the entry (CLEAN, exit 0); read-only git blob/commit
  inspections; JSON field reads; page-copy text extraction. No C1/C2 counter rerun (peer
  seats own execution; committed `measure-after.txt` and the non-author spot-check's
  re-run at `282dc76` are cited instead). No live fetch was made; the pinned 2026-10-23
  page copy was used, and the spot-check records a 2026-10-24 live fetch of the same URL.
- Touched surfaces: this report only —
  `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-40/w1/ScribeKnowledgeEntry.md`.
  No product file, lane index/jj state, fleet repo, or sibling repo changed. The
  pre-existing working-tree modification `.ufo/waves/round-40/w1/swarm-registry.json` is
  not mine and was not touched.
- Tools installed/updated: none. No pacman transaction.
- Out of scope: R2–R5 disposition correctness (other seats), C1 control re-execution,
  SCORECARD/README/lesson edits, and edits to the entry itself.

## Artifact pointers

- Entry: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/receipt-expectation-digests-r40.md`
- Pinned S059 page: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-31/build/ScribeSrcHashlib/response.body` (tracked; sha256 `553f4f2a9e686e6f051c8b12bd5469e7fdd6cc7116b2f6d2beba68c1a703af10`)
- Red-before evidence: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-40/controls/r1-stale-before.txt`
- Committed after measurement: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round40/measure-after.txt`
- Manifest: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round40/active-r39-receipts.tsv`
- Recheck counter: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round40/c1-count.py`
- Verifier: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round39/verify-receipts.py`
- Non-author spot-check: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/lessons/round-40-verifier-spotcheck.md`
- This report: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-40/w1/ScribeKnowledgeEntry.md`

Report: .ufo/waves/round-40/w1/ScribeKnowledgeEntry.md
