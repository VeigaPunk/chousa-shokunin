# CriticC1Control — do-nothing replay of the frozen C1 counter

Round 40, wave w1, chousa lane. Seat: leaf L2 critic.
Assigned attack: *Try the cheapest do-nothing replay against the frozen C1 counter and assess whether any already committed receipt set can reach 6/6 without the three required replacement runs.*
Axes judged: operability, calibration, depth.
Judged tree: §1 replay measured at `6bc90e04ac60307befacd554f7eee2b7284e2652`. **Revision moved during this audit**: tip is now `a3aac04492a3a5e99e351fc9941fcba801c152fe` (`b173b09`/`1bd9001`/`a3aac04` round-41 commits), where the counter prints `R39_ACTIVE_RECEIPTS=2/6`, exit 1 — see F4; the frozen predicate is revision-unstable because four manifest rows bind the live path `tools/research-gate.sh` while their receipts pin gate bytes. Every digest quoted for §1/§2 is from committed bytes at `6bc90e0` unless noted.

## 1. Cheapest do-nothing replay — exact command and output

Measured at `6bc90e0` (counter, manifest, and all named gate/counter/expectation bytes clean at HEAD). Re-running at the new tip `a3aac04` gives a different result — that is F4, §3.


```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && python3 corpus/evidence/round40/c1-count.py; echo "EXIT=$?"
corpus/evidence/round40/receipts/c1-base-s39001-regenerated.json: ok VERIFY: ok receipt=c1-base-s39001-regenerated.json gate=base-gate-r39.sh counter=c1-count.py
corpus/evidence/round40/receipts/c1-after-s39011-regenerated.json: ok VERIFY: ok receipt=c1-after-s39011-regenerated.json gate=research-gate.sh counter=c1-count.py
corpus/evidence/round40/receipts/c1-mutenv-s39013-regenerated.json: ok VERIFY: ok receipt=c1-mutenv-s39013-regenerated.json gate=mut-gate-path-env.sh counter=c1-count.py
corpus/evidence/round39/receipts/c1-after-s39111.json: ok VERIFY: ok receipt=c1-after-s39111.json gate=research-gate.sh counter=c1-count.py
corpus/evidence/round39/receipts/c2-after-s39101.json: ok VERIFY: ok receipt=c2-after-s39101.json gate=research-gate.sh counter=c2-count.py
corpus/evidence/round39/receipts/c2-after-s39121.json: ok VERIFY: ok receipt=c2-after-s39121.json gate=research-gate.sh counter=c2-count.py
R39_ACTIVE_RECEIPTS=6/6
EXIT=0
```

P1 is met at tip — *only because* the three regenerated receipts are committed. They were added by `d164f88` ("round-40: repair receipt evidence and calibrate r39 records"); the receipts directory did not exist at the freeze commit `6c01a41` (`git ls-tree 6c01a41 corpus/evidence/round40/receipts/` is empty), so the pre-receipt state reproduces the recorded 3/6 control: same six-row manifest naming the three then-absent paths → `unreadable-receipt` → three misses.

## 2. Strongest counterexample: can any committed set reach 6/6 without the three replacements?

**No.** The manifest is six fixed strings, so "another set" means substituting different committed bytes into those rows. I verified every candidate population the repo could supply:

| Candidate receipt | Verifier result at tip |
|---|---|
| `round39/receipts/c1-base-s39001.json` | `VERIFY-FAIL: expect-sha256-mismatch` (rc=1) |
| `round39/receipts/c1-after-s39011.json` | `VERIFY-FAIL: expect-sha256-mismatch` (rc=1) |
| `round39/receipts/c1-mutenv-s39003.json` | `VERIFY-FAIL: counter-sha256-mismatch` (rc=1) |
| `round39/receipts/c1-mutenv-s39013.json` | `VERIFY-FAIL: expect-sha256-mismatch` (rc=1) |
| `round38/receipts/*` (10 files) | fail closed — probe: `counter-sha256-mismatch`; even a matching counter fails `missing-field verifier_sha256` |
| `round37/receipts/*` (10 files) | fail closed — probe: `missing-field counter_sha256` |
| every other repo JSON with `receipt_sha256` (~450 `.ufo/waves/*` run receipts, `round26-inherited-measurement.json`) | different schema; `grep -rl verifier_sha256` shows only the nine r39-family receipt files plus the three regenerated ones carry the required field set |

Exact probe commands (lane root): the `r1-stale-before.txt` loop re-run at tip — output reproduced byte-identical (`expect-sha256-mismatch` ×3, `counter-sha256-mismatch` ×1); plus `python3 corpus/evidence/round39/verify-receipts.py --receipt corpus/evidence/round38/receipts/c1-after-s38001.json --gate tools/research-gate.sh --counter corpus/evidence/round39/c1-count.py` → `counter-sha256-mismatch`; same for `round37/receipts/c1-base-s37001.json` → `missing-field counter_sha256`.

So the maximum verifiable population without the three regenerated receipts is **3/6** (`c1-after-s39111`, `c2-after-s39101`, `c2-after-s39121` — the only other committed receipts that pass). The frozen active set is exactly the minimum sufficient set; the three replacement receipts are load-bearing, not decoration.

### Ceiling checks on the counter itself (no spoof path found)

- `VERIFY: ok ` must come from the verifier with `returncode == 0`; `fail()` prints `VERIFY-FAIL:` and returns 1. No body field can flip output without rc.
- Population is pinned twice: `len(rows) != 6` or any duplicate receipt path → exit 2 before verification. Absent path → `unreadable-receipt` fail.
- Manifest parse skips only `#`-comments and the `receipt\t` header; a receipt path literally starting `receipt\t` would be silently dropped (population → exit 2, never an inflated pass). Dead end, not a hole.
- `EXPECTATIONS` is hardcoded to `corpus/evidence/round39/expectations.jsonl` (committed sha `01cbdc3a…` — unchanged; stale receipts bind `3abd2dcb…`). No env/argv surface.
- `__file__`-relative `parents[3]` root; a copied/moved counter loses its manifest → crash, not pass.
- The verifier binds `verifier_sha256` to its own current bytes (`1b6e0de6…`), gate pre/post equality to manifest-named gate files, and `counter_sha256`/`subject_counter_sha256` to the named counters. All re-derived at tip — all pass.

## 3. Findings

**F1 — recorded control tip is not reproducible (fixable provenance defect, does not kill).**
`claims.md` "Before (observed control)" and `controls/control-before.txt` cite lane tip `691d26476ac39b8ec8b65155b41199e6f6d1f299`. That commit contains **no** `corpus/evidence/round40/` — the frozen counter, manifest, and claims.md itself were all added by `6c01a41` ("round-40: freeze receipt and calibration claims"), one commit later (`git ls-tree 691d2647 corpus/evidence/` lists nothing under `round40/`). A fresh checkout of the cited tip runs `python3: can't open file 'corpus/evidence/round40/c1-count.py'`, not `R39_ACTIVE_RECEIPTS=3/6`. The recorded 3/6 output is faithful — it is exactly what `6c01a41`'s tree produces (identical manifest, three absent receipt paths) — but the tip label points one commit too early, at the *predecessor* of the freeze commit rather than the freeze commit. Smallest safe correction: append one erratum line to `claims.md` §Errata (the append-only section already exists) and amend `control-before.txt` to name `6c01a41` as the reproducible pre-receipt base. Impacted axis: calibration (provenance precision); operability unaffected — predicate, counter, and measured outcome all hold.

**F2 — "replacement runs" are re-seals, not re-executions (calibration note, in-scope per claim text).**
Body-level diff of each regenerated receipt against its superseded r39 original shows exactly two changed fields: `expect_sha256` (`3abd2dcb…` → `01cbdc3a…`, the committed expectations digest) and `receipt_sha256` (re-sealed). Every `scenarios[].observed` row, `counter_sha256`, `gate_sha256_pre/post`, `verifier_sha256`, `seed` is carried byte-identical — no counter re-execution produced these receipts; the stale digests were re-bound and re-sealed. This is precisely what the claim licenses ("repairs the R1 stale `expect_sha256` receipts without rewriting their committed originals") and sits inside the verifier's declared limits (integrity/self-consistency, not authorship). Not a kill: the three receipt files are still required — nothing else in the repo verifies — but a Rust judge reading "three required replacement runs" should know the runs are re-derivations of bindings over carried observations.

**F3 — inert residue.** Untracked `corpus/evidence/round39/__pycache__/verify-receipts.cpython-314.pyc` sits inside the evidence dir. Harmless (scripts execute as `__main__` from source, never imported) but it is generated cache bytes inside a frozen evidence directory; recommend ignore-rule, not deletion of anything tracked.
**F4 — committed gate drift makes P1 false at tip; the frozen predicate is revision-fragile (real counterexample against C1-as-frozen, surfaced by a legitimate sibling commit).** After my §1 replay at `6bc90e0` (6/6, gate `4253c187…`), the round-41 lane landed `b173b09`→`1bd9001`→`a3aac04`; `1bd9001` rewrote `tools/research-gate.sh` to `2cb04bdd…` (verified: `git show HEAD:tools/research-gate.sh | sha256sum` = `2cb04bdd…` = clean worktree bytes; `git show 6bc90e0:tools/research-gate.sh` = `4253c187…`). Re-running the frozen counter at `a3aac04` (clean worktree):
```
c1-base-s39001-regenerated    ok    (gate .ufo/waves/round-39/controls/base-gate-r39.sh — frozen snapshot)
c1-after-s39011-regenerated   FAIL  gate-sha256-mismatch
c1-mutenv-s39013-regenerated  ok    (gate .ufo/waves/round-39/controls/mut-gate-path-env.sh — frozen snapshot)
c1-after-s39111, c2-after-s39101, c2-after-s39121  FAIL  gate-sha256-mismatch
R39_ACTIVE_RECEIPTS=2/6  EXIT=1
```
All four misses bind `tools/research-gate.sh` — a live path; both passes bind frozen gate snapshots under `.ufo/waves/round-39/controls/`. Root cause is a design asymmetry the frozen manifest itself demonstrates: receipts byte-pin `gate_sha256_pre`, but the manifest resolves that binding against *audit-time path bytes*. Any legitimate gate commit — exactly what `1bd9001` is — flips the claim without touching a receipt. The verifier behaved correctly (drift refused by name, no silent accept); the defect is in the claim's frozen population naming a mutable authority. Smallest safe correction: judge P1 against the measurement revision `6bc90e0` where all six rows pass, and record that pin in claims.md §Errata; the durable fix (manifest gate column → frozen snapshot paths + re-sealed receipts) is a new replacement class beyond the three already named. This sharpens the assigned-attack answer: at `a3aac04` the ceiling without the regenerated set drops from 3/6 to 2/6 — the replacements remain strictly necessary, and tip-state 6/6 additionally requires the live gate bytes to keep matching.

## 4. Verdict

- Assigned attack result: **the three replacement receipts are strictly necessary.** No already-committed receipt set — including every r39 original, all 20 legacy r37/r38 receipts, and ~450 unrelated run receipts — can reach even 4/6 under the frozen manifest. Observed ceiling without replacements: 3/6 at `6bc90e0` (matching the recorded control), only 2/6 at current tip `a3aac04` after committed gate drift.
- Do-nothing replay at measurement tip `6bc90e0`: `R39_ACTIVE_RECEIPTS=6/6`, exit 0 — P1 met, attributable solely to `d164f88`'s three regenerated receipts.
- At tip `a3aac04` the same counter prints `R39_ACTIVE_RECEIPTS=2/6`, exit 1 (F4): a legitimate round-41 commit changed `tools/research-gate.sh`, which four manifest rows bind as a live path. **P1 is false at tip and revision-fragile by design** — the claim's frozen population names a mutable authority. Judge recommendation: score P1 at the pinned measurement revision `6bc90e0` and append the pin as a claims.md erratum; the lasting fix is snapshot-gated manifest rows (the pattern the two passing rows already use) plus re-sealed receipts.
- One fixable provenance defect (F1: control cites `691d2647` where the counter does not exist; correct base is `6c01a41`); one wording-precision note (F2: re-seal, not re-run). F1 deserves the claims.md erratum so future audits replay the control from a checkout that can actually run it.

## Artifact pointers

- Replay output: this report §1; counter `corpus/evidence/round40/c1-count.py`; manifest `corpus/evidence/round40/active-r39-receipts.tsv` (sha `e4623159…`).
- Controls: `.ufo/waves/round-40/controls/control-before.txt`, `.ufo/waves/round-40/controls/r1-stale-before.txt` (re-verified at tip, identical output).
- Provenance: `git log 691d2647..HEAD` → `6c01a41` (freeze: adds all of `corpus/evidence/round40/`), `d164f88` (adds the three receipts), `282dc76`, `6bc90e0`.


- Verifier: `corpus/evidence/round39/verify-receipts.py` (sha `1b6e0de6…`), `corpus/evidence/round39/expectations.jsonl` (sha `01cbdc3a…`).
- Revisions: `6bc90e0` (measurement tip, counter 6/6, gate `4253c187…`); `a3aac04` (current tip, counter 2/6, gate `2cb04bdd…` committed by `1bd9001`, lane commits `b173b09`/`1bd9001`/`a3aac04`).

Tooling: none installed or updated (stock `python3`, `git`, `coreutils`; no pacman transactions, per paused-channel rule).
