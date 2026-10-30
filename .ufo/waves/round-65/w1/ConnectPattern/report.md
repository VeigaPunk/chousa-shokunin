# ConnectPattern — r58/r60/r64 instrument mistakes vs round65 prefreeze controls (seat draft, not shipping authority)

Seat: ConnectPattern (connector, leaf). Lane: chousa round65. Freeze `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd` = HEAD (verified `git rev-parse HEAD`); base `d6ed8155e9b4735639a2cf0a3e479c62f2056195` = freeze parent (verified `git log --oneline -2`). Scope: compare the r58/r60/r64 instrument-mistake family against round65's prefreeze controls; classify the recurring false-positive/forge pattern; state whether C1/C2 genuinely avoid it. Bounded read-only; all probes in `/fast/scratch/hyaku/chousa-r65/ConnectPattern/` (deleted on exit). No frozen byte, production file, or fleet file written. Tools installed: none (existing python3/git/groff/zcat only).

## Axes

- C1 — operability: historical numeric 3/10, unchanged; verdict-bearing on the frozen 20-case gate surface only.
- C2 — depth, sourced: structural sourced-entry counter; no entailment/semantic-quality claim.
- Cross-cutting meta-axis for this seat only: instrument trustworthiness (false-positive/forge resistance, freeze discipline). Not a scored lane axis.

## The recurring pattern (r58 → r60 → r64), with evidence

One family, four faces, all prefreeze-discoverable in principle:

| # | class | round | evidence |
|---|---|---|---|
| P1 | Vacuous/unreachable positive; deny-only controls | r58 C1 | `lessons/round-58.md` Mistakes 1: all 11 legs pass yet aggregate prints `REFUSE=0/7 C1=FAIL`; controls were deny-only → QUALITY 115 (positive control must reach the declared verdict before freeze) |
| P2 | Do-nothing passes; forge branch tautological | r60 C1 | `lessons/round-60.md` Mistakes 1: no-op builder passes; output-forge branch unreachable |
| P3 | Base already passes | r60 C2 | same row: C2 base already passes; fix = demonstrated no-op failure, positive reachability, mutation-kill receipts pre-dispatch |
| P4 | Freeze digest mismatch (prompt vs bytes) | r60 Mistakes 2 | dispatch prompt named `09d8053f…`, actual bytes `65721569…` |
| P5 | Fixture draws identity twice (phantom benign fixture) | r64 C1 | `claims-erratum.md` 1 + `lessons/round-64.md` Mistakes row 1: E12/E13 each `tag()` the filename and the README link independently; frozen full-pass target unreachable |
| P6 | Counter-side expected-path arithmetic unverified | r64 C3 | erratum 3: relocation built at same depth; expected `mirror.parent / needs[0]` ≠ instruments' `HERE.parents[2] / needs[0]`; measured `RELOCATION_MATCH=0/3 C3=FAIL` |
| P7 | Claim's universal set exceeds frozen enumeration | r64 C3 | erratum 4: "every" instrument omitted `c2-mutrun.py` |
| P8 | Baseline control asserted in prose, absent in runner | r64 C2 | erratum 7: unmutated baseline run not in frozen runner |
| P9 | Doc/executable summary mismatch | r64 C2 | erratum 8: doc says 29 defects/44 total; table and executable say 28/43 |
| P10 | Source-grounding substitution | r64 C3 | erratum 5: S150 grounded in installed code, not the docs package; S152 = opened counter source, not a probe-output row |

Common root: an instrument frozen without a demonstrated, receipt-backed path to its declared verdict and to honest failure; forges and phantoms survive wherever a control is prose-only, deny-only, or self-referential.

## C1 (receipt-pin) vs the pattern — genuinely avoids P1–P9 on the frozen surface

| class | round65 state | evidence (observed this seat) |
|---|---|---|
| P1 vacuous positive | avoided | committed prefreeze positive control `controls/c1-positive.txt`: ref validator 20/20 exit 0, all 20 `CASE … PASS` lines |
| P2 do-nothing passes | avoided | `controls/c1-before.txt`: default tool path `tools/receipt-pin.py` absent from tree (verified `ls`) → `CASES=0/20 C1=FAIL missing-target` exit 1 |
| P2 forge | avoided for constant forges | `always-pass.py` → 3/20 exit 1 (only the 3 rc=0 cases pass); `always-fail.py` → 17/20 exit 1 (only the 17 rc=1 cases pass). Both committed at freeze. A 20/20 tool must parse headers and bind the blob digest via `git cat-file` at the caller revision — the receipt in `c1-positive.txt` is the reference doing exactly that |
| P4 digest binding | avoided | working-tree sha256 of `controls/ref-receipt-pin.py` = `0719d717…15fa2` = S157 digest in `source-openings.json` (verified `sha256sum`) |
| P5 phantom fixtures | avoided | replicated the case construction in scratch: 20 texts pairwise distinct, all 19 mutations differ from the valid vector, names unique, tally 3 rc=0 / 17 rc=1. No double-identity fixture |
| P9 summary mismatch | avoided | single scoring variable `n`; `CASES={n}/20` and `C1=PASS/FAIL` derive from the same `n`; docstring predicate matches executable |
| P6 expected-path arithmetic | avoided (trivially) | counter's only derived path is `LANE = Path(__file__).resolve().parents[3]`; from `corpus/evidence/round65/c1-count.py` that is the lane root — correct depth (r64 C3's off-by-one shape does not recur) |
| P7/P8/P10 | not applicable | no universal enumeration, no baseline-run prose claim, no source rows at stake in C1 |

Residual forge surface, located by sibling Attack05 and confirmed in-scope here: the reference validator's `Path.read_text()` + `splitlines()` normalize CRLF/CR receipts to PASS — a nearby malformed-receipt class outside the 20 frozen cases. This is P2-family but sits **inside the claim's own named limit** ("interface/consistency coverage, not a claim to … general parser safety"), so per the r64 kill-rule convention it routes to the next round's parser-safety class list, not a refutation of R65-C1. Claim C1 as frozen is the first instrument in this family to ship a committed prefreeze positive **and** both forge controls — the r58→r60 lesson (QUALITY 115) is actually applied.

## C2 (sourced entry) vs the pattern — avoids vacuity, does not instrumentally avoid the forge; one live-tree recurrence of P3

- P1/P3-vacuity (r58's unsatisfiable counter): avoided. The counter is satisfiable — replicated its 10 checks statically: live tree scores 10/10; base `d6ed8155` scores 0/10 (`controls/c2-before.txt` committed; independently verified base `SOURCES.md` has 0 S154–S156 rows, entry absent).
- P5/P6/P9: avoided trivially — checks are pure substring predicates over three live files; no fixture arithmetic, no second summary.
- Forge pattern (P2-family): **not instrumentally avoided, disclosure-avoided**. The claim states "A boilerplate entry could pass; no semantic-quality claim rests on this counter alone." Verified accurate: the 10 checks enforce presence of `source:`/`verified-at:`/`recheck:` lines, S154–S156 mentions, SOURCES rows, README index name, `## Claims`, `## Limits`, `authenticity`, `working tree` — no quote-location, offset, digest, or used-by binding (r58's C2 counter had all of those; r65 deliberately drops them). A boilerplate entry with the right tokens passes. This is honest scope-narrowing, consistent with the r60 fix direction.
- **P3 recurrence in live-tree form (new observation, not in sibling trailers read):** the target state already exists uncommitted. `git status`: `corpus/knowledge/receipt-identity-r65.md` untracked; `corpus/SOURCES.md`, `corpus/README.md` modified (S154–S156 rows + index line 1342 present in the working tree, absent at freeze commit — verified `git show f99de3b:corpus/SOURCES.md | grep -c S15[456]` = 0; entry absent from the commit). The counter reads the **live tree, not a pinned revision** (`L=Path(__file__).resolve().parents[3]`, direct `read_text`). So any seat running `c2-count.py` today measures L1-draft uncommitted bytes and reads 10/10. The frozen before-receipt is honest (base fails), but "do nothing new" already passes in the dirty tree — the r60 "base already passes" class shifted from committed base to uncommitted working state. Attribution risk, not counter vacuity: the landing commit will contain these bytes legitimately, but a pre-landing 10/10 receipt cannot distinguish L1 draft from wave-derived content, and the frozen commit cannot pin the entry bytes (they are not in it).
- P10 source grounding: sources genuinely opened and quotes locate — S154 quote at `git-cat-file.1.gz` roff line 505 (renders with a soft-hyphen wrap; quote normalizes it), S155 quote at `hashlib.py:31`, S156 quote at line 1 of r64's `c1v3-before-full.txt` (verified). Sibling ReviewEntry recomputed matching sha256s. The entry's text matches these; the counter simply does not enforce any of it (consistent with the disclosed structural-only scope).

## Second-order trace

- C1 and C2 are mutually consistent, not contradictory: C2's entry repeats C1's own disclaimer ("does not prove execution authenticity … replaying a valid header with fabricated output can pass"), and S156 (r64 receipt lacking in-file headers) is exactly the class C1's format addresses. Compatible synthesis; no axis harmed.
- Census claim checks out: 153 rows at freeze (verified), matching claims.md.
- Out-of-claim carry-over (observation only): r65 counters derive `LANE` from `__file__` without the existence-assert rule r64 C3 added; relocated one level deeper they would traceback rather than name the missing file. No r65 claim covers this; noted for the next instrument family, not actionable here.

## Proposed move (one, bounded)

**Measure C2 at a clean checkout of the landing commit, not the dirty working tree.** Concretely: at closure, L1 runs `c2-count.py` from a `git worktree add` (or archive) of the landing hash so the 10/10 receipt binds committed bytes, then removes the temp worktree; a parallel pre-landing run may be recorded but must be labeled `uncommitted-working-tree`. No frozen byte changes; the structural counter stays the authority; the r60 P3/P4 lessons (demonstrate the measured state; bind digests to bytes) are applied to the *receipt*, not the instrument.

Risks: (i) if integration lands additional edits to SOURCES.md/README, a clean-checkout run reflects the landing truth — that is the point; (ii) `git worktree add` is a git mutation — permitted for L1 at closure under lane rules, out of bounds for this leaf seat now, which is why this is a proposal, not an action. Verification: closure receipt shows the counter's path under the temp worktree and `git rev-parse HEAD` = landing hash inside it; before-receipt still reads 0/10 at base.

## Evidence index (this seat, all observed)

- `w1/ConnectPattern/fixture-distinctness-probe.txt` — C1 fixture-construction replication output.
- `w1/ConnectPattern/c2-live-tree-checks.txt` — static replication of the 10 C2 checks on live tree vs base.
- Read-only git: `git -C … log/status/show/rev-parse`; file reads of frozen counters, controls, claims, lessons r58/r60/r64, entry draft, man page, hashlib.py.
