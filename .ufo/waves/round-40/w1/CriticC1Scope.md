# CriticC1Scope — C1 frozen-claim text vs verifier/counter proof scope

Round 40, w1, chousa lane. Seat: leaf critic (no dispatch).
Assigned attack: *Compare the C1 frozen claim text against the verifier and counter: find any overstatement about what a valid receipt proves beyond byte binding and scenario re-derivation.*

## Exact commands and output

1. `cd /home/vgpnk/Projects/shokunin/chousa-shokunin && python3 corpus/evidence/round40/c1-count.py`
   → six rows `ok VERIFY: ok receipt=…`, `R39_ACTIVE_RECEIPTS=6/6`, `EXIT=0`.
2. `python3 corpus/evidence/round39/verify-receipts.py --receipt corpus/evidence/round40/receipts/c1-base-s39001-regenerated.json --gate .ufo/waves/round-39/controls/base-gate-r39.sh --counter corpus/evidence/round39/c1-count.py --expectations corpus/evidence/round39/expectations.jsonl`
   → `VERIFY: ok receipt=c1-base-s39001-regenerated.json gate=base-gate-r39.sh counter=c1-count.py`, `EXIT=0`.
3. Same verifier with `--receipt /nonexistent.json` → `VERIFY-FAIL: unreadable-receipt …`, `EXIT=1` (missing-receipt kill confirmed).
4. JSON field diff of each regenerated receipt vs its r39 original (`c1-base-s39001`, `c1-after-s39011`, `c1-mutenv-s39013`): `ids_same: True, observed_identical: True, expect_identical: True, ok_identical: True`; the **only** differing fields are `expect_sha256` (`3abd2dcb…` → `01cbdc3a…`) and `receipt_sha256`.
5. `sha256sum` of the seven bound files vs `git show HEAD:` → all digests equal; `git status --porcelain` shows no evidence-tree modifications (only an unrelated `swarm-registry.json` touch + this wave's reports). `HEAD=6bc90e04`.
6. `git show 6d914e9:corpus/evidence/round39/expectations.jsonl | sha256sum` → `01cbdc3a…` (current committed bytes); the stale receipts bound `3abd2dcb…`, i.e. an intermediate working-tree state of `expectations.jsonl` that was never the committed tip.
7. `grep -n "disposition\|routed" corpus/evidence/round40/c1-count.py` → no match; separability clause holds.

## What the verifier actually proves (code-verified)

`verify-receipts.py` proves exactly: strict schema (no missing/unknown fields), `receipt_sha256` self-digest over the body, digest equality of the **live filesystem bytes** of counter / expectations / gate / verifier-executing-file, scenario census vs frozen expectation rows, per-row `expect` ties, `ok` re-derivation from `observed` vs `expect` (non-`_contains` keys only), `matched`/`total`/`predicate_holds` arithmetic, and for c2 the subject-counter digest. It does **not** execute anything, does **not** consult git, and does **not** prove `observed` was ever measured — the verifier's own docstring (lines 34–39) names this: self-consistency against committed bytes, not authorship; receipt-path identity unbound.

## Findings — overstatements in the frozen C1 claim text

### F1 (primary): "reruns"/"regenerated" receipts prove no re-execution — re-sealing is being laundered as regeneration

Claim body: "three replacement receipts are issued"; manifest comment (claims.md line 15 / `active-r39-receipts.tsv` line 2): "The three round-40 **reruns** are required active replacements."
Counterexample (command 4): all three "regenerated" receipts are byte-identical to their r39 originals in every semantic field — every `expect`, every `observed`, every `ok`, `matched`, `total`, `predicate_holds` — differing only in `expect_sha256` and `receipt_sha256`. They are re-sealed copies, not reruns, and `VERIFY: ok` **cannot distinguish** the two: the verifier re-derives scenario arithmetic but never executes the counter or gate. Stronger form: had the original `observed` values been fabricated, the re-seal would launder them into a fresh `VERIFY: ok`; the verifier proves *the copy is self-consistent*, never *a run happened in round 40* (or ever). "Verify" of a receipt covers the receipt's integrity, not the evidence's provenance.
Impacted axis: calibration (claim text overstates the evidence class).
Smallest safe correction: in claims.md replace "reruns"→"re-seals" in the manifest comment, and state in the claim body that replacement receipts carry forward the original `observed` scenario data unchanged and re-bind only the expectations digest — the verifier certifies binding and internal consistency, not re-measurement.

### F2: "verify against the **committed** … bytes" — the verifier binds filesystem bytes at verify time; committedness is external and was actually violated at receipt time

`verify-receipts.py` computes `sha256_file()` over whatever file occupies the path *now*. Nothing binds committed bytes except the coincidental cleanliness of the working tree (command 5 shows they happen to coincide today). The history supplies the live counterexample: the stale r39 originals bound `expect_sha256=3abd2dcb…`, a digest **no commit ever contained** — i.e. the originals were themselves generated against uncommitted working-tree bytes, which is precisely the R1 defect. A receipt that binds mutated-then-restored bytes passes `VERIFY: ok` and is indistinguishable from one that binds committed bytes. The claim's "committed" is therefore unproven by the receipt and only defensible via an external git check (`git status` clean + `git show HEAD:` digest equality).
Impacted axis: calibration; operability unaffected (gate passes either way).
Smallest safe correction: "verify against the committed gate, counter, verifier, and expectation bytes" → "verify by digest against the bytes of the named gate, counter, verifier, and expectations files; those bytes are the committed bytes only while the evidence tree is clean, which `measure-after.txt` records via `git status`/`git show HEAD:` digests."

### F3: "committed **verifier** bytes" is circular for regenerated receipts

`verifier_sha256` is bound by the receipt author to the digest of the verifier *at sealing time* (`sha256_file(__file__)` at line 196). For the three round-40 receipts this field was written fresh — so `VERIFY: ok` proves only that the running verifier is the one the re-sealer pointed at, a tautology for regenerated artifacts. The verifier-self-binding is meaningful for receipts authored before a verifier swap (the case the docstring motivates); for receipts authored in the same operation as the current verifier bytes it proves self-identity, not commitment.
Impacted axis: calibration (minor; the binding still does real work against *later* tampering).
Smallest safe correction: scope the clause — the verifier binding certifies that the verifier re-adjudicating the receipt is byte-identical to the one the receipt names; commitment of those bytes is a git-level property, same fix as F2.

### F4 (minor): provenance mislabel — "the six selected active round-39 evidence receipts"

Three of the six are round-40-authored files under `corpus/evidence/round40/receipts/` carrying round-39 scenario data. "Round-39 evidence receipts" conflates evidence *of* round-39 runs with artifacts *from* round 39. Low-risk wording, but it is the same provenance blur the critic lane exists to catch.
Smallest safe correction: "the six-row active manifest covering round-39 scenario evidence: three preserved round-39 receipts and three round-40 re-seals."

### F5 (spec/code drift, opposite direction): P1's code-condition prose understates the counter

P1 says "every row … returns a line beginning `VERIFY: ok`." `c1-count.py` line 36 requires `proc.returncode == 0` **and** `(stdout or stderr).strip()` startswith `VERIFY: ok ` — a verifier that printed `VERIFY: ok` on stderr but exited 1 would satisfy the prose and fail the code. Underestatement (safe direction), not overstatement; noted for completeness. Fix: append "and exit 0" to the prose.

### Non-findings checked

- Separability clause: `c1-count.py` never touches the disposition record — holds.
- Kill-rule population: 4 stale originals (`s39001`, `s39011`, `s39013`, `s39003`), 3 replaced, `s39003` superseded-by-exclusion — internally consistent, though "repairs the R1 stale receipts" silently means "3 replaced + 1 dropped"; acceptable but worth one clause.
- Claim body verb "verify" is correctly byte-scoped; the overstatements are F1's rerun semantics and F2/F3's "committed."
- `corpus/lessons/round-40.md` line 47 already rejects "SHA-256 proves receipt authorship or semantic truth" — the knowledge layer is calibrated; the drift is confined to claims.md/manifest prose (F1–F4), which is exactly the frozen text under audit.

## Verdict

P1 passes operationally (`R39_ACTIVE_RECEIPTS=6/6`, exit 0) and the receipt set genuinely binds the current committed bytes today. But the frozen claim text overstates proof scope in three places: **F1** (re-seals sold as "reruns"/"regenerated" — `VERIFY: ok` cannot prove execution, and identical `observed` payloads prove none occurred), **F2** (digests bind filesystem bytes, not "committed" bytes; the R1 stale receipts are themselves the counterexample of uncommitted-byte binding), **F3** (verifier-self-binding is tautological for same-session re-seals). All are wording-calibration defects in the frozen text, not predicate failures — the smallest safe correction is the three rewordings above plus an explicit "original `observed` data carried forward unchanged" disclosure; no counter, verifier, or receipt changes required.

## Artifact pointers

- Claims text: `corpus/evidence/round40/claims.md` lines 9, 11, 13, 19
- Counter: `corpus/evidence/round40/c1-count.py` lines 24–40
- Verifier: `corpus/evidence/round39/verify-receipts.py` lines 34–39 (limits), 128–216 (bindings)
- Regeneration identity proof: diff of `corpus/evidence/round39/receipts/c1-{base-s39001,after-s39011,mutenv-s39013}.json` vs `corpus/evidence/round40/receipts/*-regenerated.json` (only `expect_sha256` + `receipt_sha256` differ)
- Stale-digest provenance: `git show 6d914e9:corpus/evidence/round39/expectations.jsonl` sha256 = `01cbdc3a…` vs bound `3abd2dcb…`
- Committed-after measurement: `corpus/evidence/round40/measure-after.txt`

## Tooling

No installs or updates performed; pacman untouched. Standard `python3`/`git`/`sha256sum`/`grep` only.

Report: .ufo/waves/round-40/w1/CriticC1Scope.md
