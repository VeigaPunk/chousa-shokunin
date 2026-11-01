# Round 67 verifier spot-check — chousa (closure pass)

author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))

Date: 2026-10-31 (closure UTC 2026-11-01). Verifier did not author round 67. Lane base
`cd654578c5e09e1c12e245fd27ad5d609d1694aa`, tip `ef4b56640b231876cf646dd27841c86281f7a719`
(local `refs/heads/master` == `ls-remote origin refs/heads/master` — pushed). Index-free git
only, per host note. All commands below were run by the verifier; observed output is quoted.

## 1. Step-1 conformance

| check | result |
|---|---|
| report committed in fleet repo by lane identity | PASS — `git log --format='%an <%ae> %H %ad' -1 -- .ufo/reports/round-67/chousa.md` → `chousa-shokunin <chousa@shokunin.local> 3ee718261b77b665644845ebf38662ffa941dacb Sat Oct 31 21:16:08 2026 -0700` (matches the watchdog complete line 21:16:08-07:00) |
| `SHONEN` heading in report | PASS — `## SHONEN` with one `[~]` line per box, each with a resolvable pointer; no `[x]` written by the lane; `SHONEN.md` absent from the round diff (unchanged, still four author assertions) |
| cited lane commits exist and are ancestors of master | PASS — `cd654578…`, `3528f38d…`, `58b5ad3b…`, `75deb9b8…`, `ef4b5664…`, `8c2a0a2add04…` (r66 citation) all `merge-base --is-ancestor … refs/heads/master` OK |
| branch tip pushed | PASS — local `refs/heads/master` = `ls-remote origin refs/heads/master` = `ef4b56640b23…` |
| cited work reachable in `cd654578..ef4b5664` | PASS — exactly 4 commits (freeze `3528f38d`, landing `58b5ad3b`, verdicts `75deb9b8`, wrap-up `ef4b5664`), all authored `chousa-shokunin <chousa@shokunin.local>`; `diff-tree -r --stat` shows 30 files, 2507 insertions, 0 deletions; no `*aggregator*`/`considerthese` paths touched (no sibling writes) |
| marker-vs-report | report is a real report: work, evidence pointers, commit citations, measurements all checkable — not a marker |

Conformance defects: none found. Two status-neutral observations are recorded in §7.

## 2. The frozen C3 `verbatim=3` amendment (orchestrator-directed check)

The round's claims file `corpus/evidence/round67/claims.md` was frozen at `3528f38d` with the
literal `` `python -I tools/quote-reopen.py verify --items corpus/evidence/round67/quote-reopen.tsv` → `verbatim=3` exit 0 `` (line 99). The lane could not meet it as written (the third TSV
item `S163q1` cites a capture-path row, and `tools/quote-reopen.py` refuses non-http(s) sources
by design). Amendment review per the contract's rules (new commit; filed bytes never rewritten;
superseded text named; amendment lands before the after-receipts it affects):

1. **Append-only, no rewrite.** `git diff-tree -r -p 3528f38d 58b5ad3b -- corpus/evidence/round67/claims.md` shows exactly 4 added lines (a `## Amendment (pre-landing, disclosed 2026-10-31, before commit B)` heading + one paragraph) and zero deleted/modified lines; the frozen `verbatim=3` line is byte-identical at the tip (`git grep -n 'verbatim' ef4b5664 -- corpus/evidence/round67/claims.md` shows line 99 unchanged).
2. **Superseded text named.** The amendment paragraph names the superseded literal (`verbatim=3` exit 0), the measured replacement (`verbatim=2 absent=0 no_source=1`, exit 1), the cause (`S163q1` → capture-path row → `NO_SOURCE` by design), and the salvage leg (S163 quote verified against committed capture bytes, digest `0fad574d…007a`, normalized re-read = 1 hit — verifier re-ran the normalized grep: 1).
3. **Committed before the after-receipts it affects.** `git merge-base --is-ancestor 58b5ad3b 75deb9b8` → true. The verdicts commit `75deb9b8` carries the affected after-receipt `corpus/evidence/round67/controls/after-c3-entry.txt`, which records `QUOTE_REOPEN_SUMMARY verbatim=2 absent=0 too_long=0 no_source=1 unreachable=0`, `EXIT=1`, and explicitly states the frozen literal is NOT met, citing the claims amendment. No committed receipt anywhere reports `verbatim=3` as met.
4. **Disclosed and mined.** The round report lists it as disclosed deviation (1); the mistake is mined in `corpus/lessons/round-67.md` `## Mistakes` (frozen-literal row: class · evidence · captured-by (QUALITY 15) · fix); the SCORECARD C3 verdict cites the measured receipt.

**Ruling: the amendment conforms.** Observations (not defects): the amendment bytes sit
mid-file (between the C3 census bullet and the Sizing paragraph) rather than at end-of-file —
the erratum's substance (new commit, zero rewrites, superseded text named, pre-after-receipt
ordering) is fully met; and the in-file heading says "before commit B" without naming the sha
(the report and LOG name `75deb9b8`).

## 3. Per-claim re-check (commands run by the verifier; observed output)

### C1 — calibration (r66 routed item 1): re-measured by the verifier

- Before at base: `git show cd654578:corpus/lessons/round-66.md | grep -c 'line 8: `GIT_PIN_MATCH=no`'` → `0`; `grep -c '^correction: corpus/lessons/round-66.md'` → `0`.
- After at tip: same greps → `1` and `1`. Superseded literal `line 9: …` counts `2` at tip — exactly as the report discloses (the added hit is the correction note quoting the superseded text; matches `controls/after-c1-correction.txt`).
- Receipt re-derivation: `git show 8c2a0a2add04…:corpus/evidence/round66/controls/before-host-pins.txt | grep -n 'GIT_PIN_MATCH\|LANE_REVISION'` → `8:GIT_PIN_MATCH=no`, `9:LANE_REVISION=4f784d9e…`; `wc -l` → `14`. The correction note on `corpus/lessons/round-66.md` is anchored (`correction: corpus/lessons/round-66.md:13 …`), names the superseded text, and leaves the Gate table as committed history.
- **Verdict: improved.** Reported values reproduced exactly.

### C2 — operability (lowest non-retired axis 3/10; capability acquisition): gate evidence-verified + core fact independently re-measured

Per the gate standard the verifier did not execute the lane's gate; it verified the committed
evidence and independently re-derived the underlying fact with its own sweep.

- Committed evidence consistent: `tools/digest-in-tree.py` present (187 lines); SKILL gate-registry row `digest-in-tree (r67)` carries the full schema (entry command, verdict map 0/1/2 with fail-closed `NO_DIGESTS`, controls, pinned-value/freeze revision, write scope, owner). Receipts: `before-d2-defect-receipt.txt` (at base: `DIGESTS_IN_TREE=0/2 DIGEST_IN_TREE=FAIL` exit 1, both pins named `OUT_OF_TREE`, `SCANNED_BLOBS=14869`) → `after-d2-battery.txt` (at landing `58b5ad3b`: 0/2 FAIL over `SCANNED_BLOBS=14888`; committed-fixture receipt 2/2 PASS; `before-c1-lesson` 1/1; `before-registry-tallies` 1/1; positive PASS in rev and all-objects modes; fake digest 0/1 FAIL; digest-free `ERROR NO_DIGESTS` exit 2). The 14,888 (landing) vs 14,869 (base) object counts are both correct at their named revisions — the report cites the landing figure.
- Verifier's own all-blob sweep (independent script over `git cat-file --batch-all-objects --batch`, 14,903 blobs at tip): defect pins `c0aaa9ed…` → `OUT_OF_TREE`, `b19f9ac6…` → `OUT_OF_TREE`; fixture pins `bca84fad…` → `IN_TREE`, `113ea182…` → `IN_TREE`; fake pin `0123…` → `OUT_OF_TREE`; capture digests `37d38be4…`/`0fad574d…` → `IN_TREE`. Matches the gate's verdicts at every named revision.
- The r66 before-state re-issue (`before-r66-counter-committed-fixture.txt`) pins only committed fixture bytes (both IN_TREE per the sweep) and re-measures `SEMANTIC=7/9 C2SEM=FAIL` — the routed scratch-clone defect is repaired reproducibly from the repository alone.
- Capability row `receipt-digest provenance enforcement` enters with a demonstrated run (the battery) — per AXES.md §Capabilities.
- **Verdict: improved** (on the frozen predicate; the claimed limits — re-derivability ≠ command authenticity/entailment — are named in the entry and registry row).

### C3 — depth (sourced on S161–S163): re-measured + evidence-verified

- Entry absent at base, present at tip (`git show` fails at base, succeeds at tip). S161/S162/S163 rows: 0 → 1 each. Registry rows 160 → 163 — verifier's own greps at base and tip match `before-registry-tallies.txt`/`after-registry-tallies.txt` (A 121→122, B 29→30, C 10→11; mined 129→131, queued 19→19, rejected 12→13). SOURCES.md diff is additions-only (0 deletions).
- Capture digests recomputed by the verifier over committed bytes: `git show ef4b5664:…git-hash-object-50fe5cc6.adoc | sha256sum` → `37d38be4…71094`; `…git-scm-hash-object-page-2026-10-31.html | sha256sum` → `0fad574d…007a` — both match the receipts and the report.
- Quote re-opens run by the verifier over the committed captures (normalized whitespace): S161q1 → 1 hit, S161q2 → 1 hit, S163q1 → 1 hit. The measured `verbatim=2 absent=0 no_source=1` outcome and its amendment are verified (§2).
- `SEMANTIC=9/9 C2SEM=PASS` evidence-verified from `after-c3-entry.txt`; the verifier independently recomputed the receipt's `ENTRY_SHA256` (`6f4089b6…`) and `SOURCES_SHA256` at landing (`859f75db…`) over committed bytes — both match, binding the receipt to the committed tree.
- **Verdict: improved**, with the one disclosed frozen-literal miss processed per the amendment rules (§2). The claim's substance (entry, rows, digests, quotes, 9/9) all verify.

## 4. Per-axis verdicts (closure)

| axis | verdict | evidence |
|---|---|---|
| calibration | **improved** | C1 re-measured (§3); the r66 routed defect corrected append-only; the round's own frozen-literal miss disclosed and mined, not absorbed |
| operability | **improved** | C2 (§3): registered checker + committed controls; core fact independently re-derived; lowest non-retired axis obligation met (base SCORECARD: operability 3/10, the only numerically scored axis, none retired) |
| depth | **improved** | C3 (§3): sourced entry with canonical pinned ground and named limits; quotes re-opened from captures and live |
| freshness | **unchanged** | no drift surface measured; S161 fresh-opened with `on-release` recheck; no contrary evidence found |
| coverage | **unchanged** | PROVINCE.md untouched; the G02 coverage-map gap was an index omission (fixed in wrap-up), not a new province surface |
| adjacency | **unchanged** | no sibling writes in `cd654578..ef4b5664` (diff-tree name-only check); git-semantics/host observations stay in-method |

No axis is harmed: the SCORECARD diff over the round is additions-only (verdict section + one capability row); no numeric score changed; no prior entry was rewritten.

## 5. Discernment spot-check (outside non-author; this pass)

Sample from `corpus/lessons/round-67.md` `## Gate` — 3 admits + 1 reject, every source re-opened:

| item | decision | re-opened source (verifier run) | agree/disagree | reason |
|---|---|---|---|---|
| S161 — upstream `git-hash-object.adoc` at pinned commit `50fe5cc6`, tier A | admit | live `https://raw.githubusercontent.com/git/git/50fe5cc63f9cd6e89b87a2c9ccf96a444f4cfdb7/Documentation/git-hash-object.adoc` fetched 2026-10-31: sha256 `37d38be4…71094` — byte-identical to the committed capture; both Gate quotes present (normalized: 1 hit each) | **agree** | the pinned URL serves exactly the captured bytes; the 18-word quote is ≤25 words, located (DESCRIPTION first sentence), and grounds the entry's identity-follows-content claim |
| S162 — r66 defect receipt, tier B own-work | admit | path re-opened: `git show cd654578:corpus/evidence/round66/controls/before-new-counter-boilerplate.txt` lines 12–13 carry exactly `ENTRY_SHA256=c0aaa9ed…` / `REGISTRY_SHA256=b19f9ac6…`; verifier's own all-blob sweep shows both OUT_OF_TREE | **agree** | the row teaches a real, independently reproduced counterexample class; B-for-counterexample-only scoping is correct |
| S163 — versioned git-scm.com page, tier C | reject | live `https://git-scm.com/docs/git-hash-object` fetched 2026-10-31: HTTP 200, 29,933 bytes, sha256 `0fad574d…007a` — byte-identical to the committed capture; DESCRIPTION sentence present (1 hit); URL carries no revision segment | **agree** | the rejection reason ("content moves with releases and the URL pins no revision") is structurally confirmed by the re-open; flip to S161 is the right remedy |
| knowledge entry `receipt-digest-provenance-r67.md` | admit | `after-c3-entry.txt` 9/9 PASS with `ENTRY_SHA256`/`SOURCES_SHA256`/`LANE_REVISION` — verifier recomputed both digests over committed bytes and they match; entry read: trio complete, claims grounded in S161/S162, limits name what the checker does not prove | **agree** | narrow admission with honest limits; the entailment residual is explicitly left to a non-author review rather than claimed |

New SOURCES.md row quote check: S161's quote is 18 words, located ("DESCRIPTION first sentence"), and verbatim in both the committed capture and the live page — PASS.

Census: verifier ran `bash scripts/sources-census.sh validate --root <fleet> chousa` → exit 0, the same five pre-existing W04 duplicate-url warnings (S051/S053/S073/S074/S075), `ok` for chousa — matches `census-start.txt`/`census-end.txt`/`census-final.txt` exactly.

## 6. Trend verdicts (closure)

| trend | verdict | evidence |
|---|---|---|
| expansion | **unchanged** | three registry rows extend already-covered provenance ground; no new province surface; no new source kind; census clean. The G02 finding was a coverage-map index omission (fixed), not new ground |
| quality | **improved** | a receipt class unmeasurable last round (the routed r66 scratch-clone receipt) is now checker-named with committed controls, and the r66 before-state is reproducible from the repository alone — both independently confirmed by the verifier; no admitted entry failed a re-check |
| discernment | **improved** | LEARNING.md's improved condition is met: this outside spot-check agrees with the gate on admits and rejects (S161, S162, entry admit; S163 reject), all verified at byte level; the round also disclosed and mined its own frozen-literal miss and corrected the routed r66 calibration defect append-only. (The lane self-graded "unchanged pending the outside spot-check"; this closure pass completes that condition — a verdict delta, recorded here, not a defect.) |

Lane's report verdicts were expansion unchanged / quality improved / discernment unchanged-pending; the closure agrees except discernment, which resolves to improved on the completed spot-check condition above.

## 7. Routed defects and notes for the next round / operator

1. **G06 `tools/freeze-check.py --selftest` host drift — stays routed to round 68.** Pre-existing (hardcoded `/home/vgpnk/...` `LANE_ROOT_DEFAULT` at `tools/freeze-check.py:48`; selftest case directory names containing `:` that NTFS refuses), disclosed with receipts (`.ufo/waves/round-67/preflight.txt`, `preflight-after.txt`: `PREFLIGHT=6/7 FAILED=G06`), not repaired, correctly not attributed to this round (round-63's 8/8 predates the host move). Red gate = conformance defect routed to its owner; status-neutral.
2. **G02 coverage-map rows — fixed this round** (r66 inherited gap + r67 own landing miss; `preflight-after.txt` G02 PASS). No residual.
3. **Status-neutral observations (no action forced):** (a) the claims.md amendment sits mid-file rather than at end-of-file — erratum substance fully met (§2); (b) the amendment heading's "before commit B" leaves the sha to the report/LOG; (c) report's C2 sizing cites 14,888 objects (landing run) vs claims.md's 14,869 (base run) — both correct at their named revisions.
4. **SHONEN (operator note):** still four author assertions, no `[x]`. The boxes now look fully checkable by a non-author promotion review: box 1 (SKILL decision tables/error patterns/checklists with cited sources, including the new registry row), box 2 (the C3 citation chain logged end-to-end with byte evidence), box 3 (the `digest-in-tree.py` exit contract is documented and re-runnable from committed receipts), box 4 (PROVINCE.md untouched; verifier confirmed no sibling writes). The verifier did not check any box — promotion review remains a separate non-author act.
5. No exploratory claims were declared; the exploratory `unprovable-but-better` reviewer requirement was not triggered. The S163 capture-re-read salvage leg and the amendment were cross-checked (§2, §5).
6. L0: the round added no new L0 questions; the standing r40/r65 fetch-scope and L2-floor template questions remain open and were routed around, never treated as answered (report, lesson, LOG consistent).
