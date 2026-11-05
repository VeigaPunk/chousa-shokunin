# Round-80 sibling-overlap scan — R80ConnectorA

## Scope and axes

Axes: **C1 operability** (fresh subject evaluation and oracle discrimination), **C2 calibration** (grounded Gate records). Adjacency is the comparison surface, not a score claim. Read frozen `claims.md` first and the round-79 non-author closure before comparison. No instrument verdict was executed; these are committed-source comparisons, not admission or runtime certification.

Search used the specialized regex search tool (rather than shell `grep -rn`, per tool policy), case-insensitive, across all seven sibling repositories. Initial broad results were saturated by historical wave transcripts; narrowed searches excluded `.ufo`, historical lessons/evidence and LOG, and retained code/QUALITY candidates. Queries and returned scopes are retained in `*-search.txt`, `*-narrow.txt`, and `anchors-search.txt`. Those are discovery receipts, not evidence that no unreturned match exists. The bounded mechanism hits adjudicated below are the reopened committed artifacts; no exhaustive absence claim is made.

Snapshot caveat: the local sibling tips contain material later than round 80 (e.g. kumitate binder v3 says round 89). These are the requested `master` snapshots observed now, **not proof those later mechanisms existed at the round-80 freeze**. Earlier numbered souji/kama mechanisms avoid that particular chronology issue; no independent historical existence reconstruction was performed.

## Pinned revisions

Each row is an observed `git -C /home/vgpnk/Projects/shokunin/<lane>-shokunin rev-parse master`, exit 0, retained verbatim in `revisions.json`:

| lane | master |
|---|---|
| tsukuroi | `a8598038dbcbaa07d4b5899b647bf30aa81e9e3f` |
| kasegi | `3cc8cd45cb6f8ca49a292f3b2647c5bddac71486` |
| souji | `c7228424c3919ecf142bab1aec8181722d86467b` |
| kama | `d05f6d01a4b39d1ef60043ab123a7ef50085f5b0` |
| mado | `f72bba01928efe80cfa1a7907fe3aaa9eba1cfd7` |
| kotoba | `760e1c5edfdefb4767420f711d08f669952de013` |
| kumitate | `7218699cfbdec702ba42f35ceac0a8e52d1bd564` |

Chousa committed-source read pin: `0d253c95732c0ed19a9fa414e5d17769ddefa48d`; its two round-80 hashes below exactly match the frozen claims' identities.

## Two methods

1. **Gate grounding:** a registry-family tip is bound to a committed revision, path, exact physical line, nonempty verbatim substring and whitespace word count ≤25, with superseded rows accounted separately. Command: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show 0d253c95732c0ed19a9fa414e5d17769ddefa48d:corpus/evidence/round80/gate-grounding-check.py` → `chousa--corpus__evidence__round80__gate-grounding-check.py.receipt`, exit 0. Observed source lines 109–130 implement R1–R4; 149–198 construct family tips and the verdict. Measured committed sha256: `d9e426216665a098cd90adf8fbf5e5dd62e02dc7b5b707c322b404b3eb55c553`.
2. **Fresh battery:** AST-rewritten/mutated positives are classified by a fixed witness's observed exit/marks/case cells, then the same fresh set plus committed subjects is scored against both the candidate matrix and five enumerated identity/output oracles. Command: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show 0d253c95732c0ed19a9fa414e5d17769ddefa48d:corpus/evidence/round80/matrix-battery-v7.py` → `chousa--corpus__evidence__round80__matrix-battery-v7.py.receipt`, exit 0. Observed lines 457–493 draw/classify, 496–546 score, and 617–651 share the set and tally oracle rejection. Measured committed sha256: `35351b2328bb6a284da13e61240a6ec598f39a148b8d8948d4e3d60dd78d914d`.

## Bounded overlap hits

Comparisons are componentwise. “Stronger” below always names the dimension; it does not mean a sibling dominates the entire frozen claim.

### tsukuroi — quote location, weaker executable assurance

`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show a8598038dbcbaa07d4b5899b647bf30aa81e9e3f:corpus/QUALITY.md` → `tsukuroi--corpus__QUALITY.md.receipt`, exit 0.
Observed `corpus/QUALITY.md:29`: “use a stable source heading/fragment, exact quote and observed revision or access date.” This is an equivalent documentary locator principle, but **weaker than C2's executable conjunction**: this criterion permits an access date and renderer-dependent supplemental lines, whereas chousa actually reopens a commit and physical line. No absorption proposed from this hit.

### kasegi — source identity and occurrence census, mixed rather than dominant

`git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show 3cc8cd45cb6f8ca49a292f3b2647c5bddac71486:corpus/QUALITY.md` → `kasegi--corpus__QUALITY.md.receipt`, exit 0; observed line 64: “the record's `path` stem equals its `id`, the quote is exactly-once in the capture (or carries an `anchor` line number the instrument verifies)”.
`git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show 3cc8cd45cb6f8ca49a292f3b2647c5bddac71486:corpus/instruments/source-recheck.py` → `kasegi--corpus__instruments__source-recheck.py.receipt`, exit 0; committed sha256 `fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003`.
Observed `source-recheck.py:95–112`: “A quote that occurs more than once must carry an `anchor` line number” and `window = " ".join(raw_lines[max(0, anchor - 1):anchor + 3])`.
**Stronger** on capture-id/path association and reporting occurrence ambiguity; **weaker** on exact physical-line semantics because the anchor window spans four lines and normalization changes comparison bytes. C2 already requires a line even for unique quotes. Absorb only explicit subject identity into the proposed evidence envelope, not normalization or the wider window; otherwise C2 would regress.

### souji — executable receipt/revision/instrument binding, stronger on provenance

`git -C /home/vgpnk/Projects/shokunin/souji-shokunin show c7228424c3919ecf142bab1aec8181722d86467b:corpus/QUALITY.md` → `souji--corpus__QUALITY.md.receipt`, exit 0; observed line 302: receipt must carry a full revision and “an `instrument_sha256` equal to the named instrument's committed blob at that revision”; line 308 distinguishes raw object type and conflicting standalone headers.
`git -C /home/vgpnk/Projects/shokunin/souji-shokunin show c7228424c3919ecf142bab1aec8181722d86467b:census/round-58/c2-gate.py` → `souji--census__round-58__c2-gate.py.receipt`, exit 0; committed sha256 `56f2a31163035726f1190db3e6b827fc121602377e187d16a54a6ae8f15af543`. Observed lines 115–123 require exact commit object type, 154–171 refuse missing/conflicting/short/non-durable revision headers and missing EXIT.
`git -C /home/vgpnk/Projects/shokunin/souji-shokunin show c7228424c3919ecf142bab1aec8181722d86467b:tools/souji-receipt-run.py` → `souji--tools__souji-receipt-run.py.receipt`, exit 0; committed sha256 `0ed30d4401b20d8954aef3c5b54107f7b8a1ee1b0f810deaba07e1fec73c90a4`. Observed lines 345–358 rehash committed tool bytes and refuse `RECEIPT-TOOL-DIGEST-MISMATCH` or non-durable revisions.
**Stronger than C1's revision label**: chousa v7 lines 608–611 hashes the live matrix and prints `rev = a.rev or _lane_rev()` without asserting that the matrix or subject inputs came from that revision. It is not stronger than C2 on quote truth. Absorb the receipt's executable revision/instrument equality next round: printing a revision does not bind a run to it.

### kama — drawn request + independent answer binding, stronger replay resistance in its domain

`git -C /home/vgpnk/Projects/shokunin/kama-shokunin show d05f6d01a4b39d1ef60043ab123a7ef50085f5b0:tools/round64-c1-counter.py` → `kama--tools__round64-c1-counter.py.receipt`, exit 0; committed sha256 `1ffea590bcb4a2db3e1183221ebe1f2dd9841f4811c9bcd54de80f2484b817d9`.
Observed lines 875–889: “All distinct; the nonce is in every prompt.” Lines 811–826 compare the receipt's `prompt`, `n_predict`, `seed`, answer text and usage to this run's request/reference (`receipt_req`, `receipt_ref_text`, `receipt_ref_usage`).
**Stronger** than a bare fresh-fixture/nonce declaration on binding reported observations to the current request and independently observed answer; **not a replacement** for chousa's semantics battery, and not proof its reference is correct. Absorb sample-to-observation identity in the same proposed envelope: v7 retains named result rows but removes its random fresh subject bytes at lines 640–641, so the receipt alone cannot reopen their identity later.

### mado — current-run witness, narrower and weaker than semantic discrimination

`git -C /home/vgpnk/Projects/shokunin/mado-shokunin show f72bba01928efe80cfa1a7907fe3aaa9eba1cfd7:corpus/knowledge/harness-witness-credit-r75.md` → `mado--corpus__knowledge__harness-witness-credit-r75.md.receipt`, exit 0; observed lines 28–31: a per-run challenge is credited only when the child's witness equals it byte-exactly. Lines 62–63 explicitly say a child may echo the current challenge and invent matching details.
This is **stronger against stale captured output**, but **weaker as an answer oracle** than C1's full contract cells/exit checks; a nonce echo does not score semantics. Its next-round lesson for the envelope is to bind the generated challenge/sample identity, never credit the echo itself as correctness. This is source-described behavior, not a reproduced 11/11 measurement.

### kotoba — committed-tree reader, equivalent substrate only

`git -C /home/vgpnk/Projects/shokunin/kotoba-shokunin show 760e1c5edfdefb4767420f711d08f669952de013:verifiers/check_gate_registry.py` → `kotoba--verifiers__check_gate_registry.py.receipt`, exit 0; committed sha256 `01b8ad1b1a2d9f7568dc6b970cd5c9ec621bf58af411973f001fa3ad0c35ddce`.
Observed lines 118–136 enumerate the pinned tree and read via `git show rev:path`, checking existence with `git cat-file -e`. **Equivalent** to C2's committed-tree substrate, but it audits a verifier registry rather than located quotes or fresh semantic subjects. No stronger form of either complete round-80 method is established by this hit; no absorption proposed.

### kumitate — receipt pair binding, stronger defensive provenance but chronology-limited

`git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 7218699cfbdec702ba42f35ceac0a8e52d1bd564:scripts/receipt-bind.mjs` → `kumitate--scripts__receipt-bind.mjs.receipt`, exit 0; committed sha256 `37201ad0c6acd4c51b8804fa66ac9606469a181891dbed1d5ee46c56176e1bb3`.
Observed lines 19–20 hash lane instruments from `git cat-file blob <rev>:<path>`; lines 25–41 refuse unchecked/empty receipt populations and ambiguous fields; lines 50–58 refuse symlink instruments and read receipts through one O_NOFOLLOW descriptor. **Stronger** on defensive instrument-to-receipt association than C1's printable revision label, not on quote semantics; lines 67–73 explicitly concede that a fabricated receipt with the correct digest still binds. Version says round 89, so this cannot establish round-80 priority. Absorb its unambiguous field/regular-blob discipline as part of the same next-round envelope, not its second-whitespace-token argv parser (which would mishandle chousa's `python3 -B`).

## One bounded proposed move — a next-round sample-evidence envelope

Propose a successor battery's **receipt binding only**: before scoring, resolve a durable full revision, assert the selected instrument/committed-input hashes against its tree, and retain each drawn subject's digest plus its witness and candidate/oracle observations under that run's identity. Preserve v7's same-draw sharing and exact CASE/exit checks unchanged. This synthesizes souji's executable receipt identity with kama's request-to-observation binding; kasegi supplies explicit subject association, mado the warning that freshness is not correctness, and kumitate the defensive field discipline. No mechanism is absorbed this round.

- **Affected axes:** calibration improves through reopenable sample/instrument identity; operability retains the existing evaluator and acceptance set. No claimed numeric movement or Pareto certification: preservation remains a verification obligation, not an observed result.
- **Runtime:** hash and retain already-drawn samples once, outside child scoring, so added I/O must not consume child timeouts or perturb quiet/order legs.
- **Contract:** distinguish judged input revision from later receipt-storage revision; do not require a commit to contain a receipt naming itself. Treat invalid bindings as environment/refusal, never as an oracle successfully rejected.
- **Substrate:** use committed regular blobs and contained owned sample storage; hostile inherited Git selectors must not redirect the binding. Random samples cannot be “present at input revision”; their retained digest belongs to a separate run manifest.
- **Verification:** next round's authorized owner should replay the legitimate matrix, each enumerated oracle, and a do-nothing baseline; add wrong revision, wrong instrument hash, duplicate header, absent sample, sample substitution and stale observation separator cases. Check unchanged semantic outcome counts and fail-closed binding errors separately. None of these checks was run here.

## Contradictions and limits (not scalarized)

- Frozen C1 describes drawn-per-run semantics, but v7 draws `fresh_list` once per invocation (617–624) and reuses it across `--runs` (496–519); sharing the same set across oracles is intentional. This is a scope distinction, not a runtime counterexample from this seat.
- A valid C2 quote is not proof the quoted proposition is true; a valid receipt digest is not proof its process ran. Neither sibling binding closes that epistemic boundary.
- Fresh labels still share the committed witness's mistakes, as frozen claims explicitly acknowledge; the envelope improves provenance, not independent semantic ground truth.
- Stronger local components coexist with weaker windows/nonce-only checks and later-round versions; no sibling is declared a wholesale replacement or overall winner.

## Execution boundary

All cited content was obtained by the exact `git show` command printed atop its `.receipt`, exit 0; each receipt retains numbered observed source lines and the measured sha256 of the committed blob. `revisions.json` retains each exact pin command/exit. No gate, battery, sibling runtime, network, install, clone, fixture, production edit or git mutation was invoked. No scratch directory was allocated, so no scratch cleanup remained. Report-only output is confined to this seat's authorized wave paths.
