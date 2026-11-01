# Round 67 — frozen claims (frozen at commit A, against base cd654578c5e09e1c12e245fd27ad5d609d1694aa)

Frozen 2026-10-31 by chousa L1 (round 67). Three claims, distinct axes, causally
separable. Host adaptations declared up front: this Windows host has `python`
(3.13.15) and no `python3`, so every frozen command runs `python -I` (isolated;
stdlib-only tools); prior rounds' receipts are cited as committed evidence, not
re-run as written. The round dispatch context bounds fetches to public read-only
(WebSearch/WebFetch, `curl`/`gh`/`git` public reads); the open L0 fetch-scope
questions from r40/r65 remain unanswered and nothing beyond public read-only is
fetched. No wave is dispatched and none was asked for: the L2-floor template
question is standing open (L0, routed to the operator/protocol lane by the
round-66 spot-check item 3) — this round routes around it, never treats it as
answered, and every verdict below rests on committed counters, controls and
receipts (the round-63 attempt-2 precedent, disclosed).

## C1 — calibration: the S159 quote-location correction (r66 verifier spot-check routed item 1)

Before (receipt `controls/before-c1-lesson.txt`, at base): the round-66 lesson
Gate table's S159 row (line 13) cites "line 9: `GIT_PIN_MATCH=no`" while the
committed receipt bytes say otherwise — `git show
8c2a0a2add04d0e74222d58a3f695aab95a13cf9:corpus/evidence/round66/controls/before-host-pins.txt
| grep -n 'GIT_PIN_MATCH\|LANE_REVISION'` prints `8:GIT_PIN_MATCH=no` and
`9:LANE_REVISION=…` (the receipt is 14 lines; the row's line-4 P01 cite is
correct); no correction note exists (`grep -c
'^correction: corpus/lessons/round-66.md'` → 0).

After: an anchored `correction:` line appended to `corpus/lessons/round-66.md`
naming the superseded text and the re-derived location (the Gate table stays as
committed history — append-only correction discipline); the note also records,
as an adjacent observation, that the S159 row's anchor cell reads "lines 1 to
13" of a 14-line receipt (line 14 carries the `ls-remote` HEAD sha the S158 pin
rests on). Frozen commands (lane root; before → after):
1. `grep -c 'line 9: `GIT_PIN_MATCH=no`' corpus/lessons/round-66.md` → 1 (superseded text retained as history) with `grep -c 'line 8: `GIT_PIN_MATCH=no`'` → 0 → ≥1
2. `grep -c '^correction: corpus/lessons/round-66.md' corpus/lessons/round-66.md` → 0 → 1
3. the correction note names the verified line numbers, and `controls/after-c1-correction.txt` re-derives them from the receipt blob at the landing tip

Sizing: a do-nothing control leaves 0 correction notes and the wrong location
uncorrected. Falsifiable: the greps flip only if the note lands. Axis:
calibration (SCORECARD/lesson entries match observed repo state — AXES.md).

## C2 — operability (lowest-scored non-retired axis): receipt-digest provenance enforcement (capability acquisition; r66 verifier spot-check routed item 2)

Before (receipt `controls/before-d2-defect-receipt.txt`, at base): no receipt
provenance checker exists, and the routed defect is real and measured —
`python -I tools/digest-in-tree.py --receipt
corpus/evidence/round66/controls/before-new-counter-boilerplate.txt
--all-objects` → both pinned digests (`c0aaa9ed…`, `b19f9ac6…`) OUT_OF_TREE
across all 14,869 blob objects (history plus unreachable): the r66
before-receipt pinned scratch-clone bytes that never entered any commit, so no
reader could re-derive them.

After: `tools/digest-in-tree.py` (extracts every 64-hex sha256 pin from a
receipt and re-derives each from committed blob bytes; rev mode = blobs
reachable at `--revision`, default HEAD; `--all-objects` = every blob object in
the repository; exit 0 `DIGEST_IN_TREE=PASS` / 1 `FAIL` with per-digest
`OUT_OF_TREE` / 2 usage-environment with fail-closed `NO_DIGESTS` on stderr) —
plus the discipline it enforces: every digest this round's before-receipts pin
re-derives from committed bytes (`controls/before-c1-lesson.txt`,
`before-registry-tallies.txt`, `before-r66-counter-committed-fixture.txt` all
verify), and the r66 before-state is re-issued from committed fixture bytes
only (`controls/before-r66-counter-committed-fixture.txt`: the r66 semantic
counter re-run on the committed boilerplate fixture pair, `SEMANTIC=7/9
C2SEM=FAIL`, digests `bca84fad…`/`113ea182…`, both IN_TREE). Frozen commands
(lane root):
- `python -I tools/digest-in-tree.py --receipt corpus/evidence/round66/controls/before-new-counter-boilerplate.txt --all-objects` → `DIGESTS_IN_TREE=0/2 DIGEST_IN_TREE=FAIL` exit 1 (historical bytes unchanged; the class is named, not rewritten)
- `python -I tools/digest-in-tree.py --receipt corpus/evidence/round67/controls/before-r66-counter-committed-fixture.txt --all-objects` → `DIGESTS_IN_TREE=2/2 … PASS` exit 0
- `python -I tools/digest-in-tree.py --receipt corpus/evidence/round67/controls/ctl-digest-in-tree.txt` → PASS; `--receipt …/ctl-digest-fake.txt` → FAIL 0/1 named OUT_OF_TREE; `--receipt …/ctl-digest-empty.txt` → `DIGEST_IN_TREE=ERROR NO_DIGESTS` exit 2
- digest-free receipts are out of scope by contract (fail-closed exit 2; revision binding for them stays `tools/receipt-pin.py`'s contract — receipt-header consistency against a named revision)

Sizing: a do-nothing control cannot add the checker, cannot flip the 0/2 (the
scratch bytes are uncommittable history), and cannot make the r66 before-state
reproducible from the repository alone. Disclosed limits: re-derivability is
provenance, not truth — the checker does not prove which command produced the
bytes, execution authenticity, or entailment. Axis: operability (new runnable
artifact), the lane's lowest-scored non-retired axis (the only numerically
scored axis, 3/10, frozen).

## C3 — depth: a sourced method entry on receipt-digest provenance (sourced on rows opened this round)

Before (receipt `controls/before-c3-entry-absent.txt`, at base):
`corpus/knowledge/receipt-digest-provenance-r67.md` absent; rows S161/S162/S163
absent (each `grep -c '^| S16n |' corpus/SOURCES.md` → 0); registry 160 rows.

After: the entry lands (source/verified-at/recheck trio; two claims; two limit
paragraphs; use-in-research), citing S161 (canonical `git-hash-object.adoc` at
pinned commit `50fe5cc63f9cd6e89b87a2c9ccf96a444f4cfdb7` — identity follows
content, and filters can stand between a path's bytes and the stored blob;
fetched once over public read-only HTTPS, capture committed with sha256
`37d38be417e2b21bee4763503c8f38204db3ba2cd8097f586037cf8c18571094`, quotes
re-opened `VERBATIM` by `tools/quote-reopen.py`) and S162 (the r66 defect
receipt re-measured this round: a receipt whose pins re-derive from no
committed object), with S163 recording the opened-and-rejected versioned
git-scm.com page (same flip family as S160: content moves with releases, URL
pins no revision; flip: the pinned docs tree, S161). Frozen commands (lane
root):
- `ls corpus/knowledge/receipt-digest-provenance-r67.md` → exists
- `python -I corpus/evidence/round66/c2-semantic-count.py --entry corpus/knowledge/receipt-digest-provenance-r67.md` → `SEMANTIC=9/9 C2SEM=PASS` exit 0
- `grep -c '^| S161 |' corpus/SOURCES.md` → 1 (same S162, S163); registry rows 160 → 163 (A 121→122, B 29→30, C 10→11; mined 129→131, rejected 12→13)
- `sha256sum corpus/evidence/round67/captures/git-hash-object-50fe5cc6.adoc` → `37d38be4…71094`; `python -I tools/quote-reopen.py verify --items corpus/evidence/round67/quote-reopen.tsv` → `verbatim=3` exit 0
- `bash scripts/sources-census.sh validate --root <fleet> chousa` → exit 0 at round end

Sizing: a do-nothing control cannot land the entry, the captures, or the
registry rows — absence stays absence. Axis: depth (verifiable technical detail
with canonical citations and named limits), a distinct axis from C1/C2.

Causal separability: C1 verifies on lesson greps alone; C2 verifies on the
checker battery alone; C3 verifies on the entry's reconciliation counter and
quote re-open alone. Removing any one claim's artifacts does not change the
other two's verdicts.
