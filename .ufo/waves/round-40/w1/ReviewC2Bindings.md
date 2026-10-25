# ReviewC2Bindings — round 40 / w1 (leaf L2, no dispatch)

Assigned attack: independently verify both active c2 receipts with the receipt
machinery, including `verifier_sha256` and `subject_counter_sha256`, and compare
the disposition counter's command output.

Lane root: `/home/vgpnk/Projects/shokunin/chousa-shokunin` (HEAD
`6bc90e04ac60307befacd554f7eee2b7284e2652`; measure commit
`d164f88eb71a6c48a66ae1e7abfcb5fef82219d9`; round-40 freeze commit
`6c01a4144b3637cc57a989ab464f71b8ae69595a`). All reads read-only; no production
file, git index, or jj state touched. No tool installs (nothing needed; pacman
paused host-wide and not invoked). No `lsp` device is present in this seat's
tool set, so caller/definition checks are direct execution plus committed-byte
hashes, not semantic LSP references — recorded as a method limit, not an
absence proof.

## Verdict

**Both active c2 receipts verify, and every digest they bind matches committed
bytes. C2's counter output reproduces exactly. Two real calibration weaknesses
remain in the round-40 disposition counter: its 4/4 output is not bound to the
bytes it read, and its R5 leg is a document-wide substring scan that I drove to
4/4 with the round-40 R5 correction deleted. Separately, the receipt
verification path is coupled to the worktree, not to committed blobs: a sibling
seat's in-flight edit to `tools/research-gate.sh` (observed during this review)
already moves the live `R39_ACTIVE_RECEIPTS` count from `6/6` to `2/6`, while the
unchanged c2 receipts still verify `2/2` against the committed gate blob.**

## Verification ledger (commands and exact output)

### 1. Independent verification of the two active c2 receipts

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin
$ python3 corpus/evidence/round39/verify-receipts.py \
    --receipt corpus/evidence/round39/receipts/c2-after-s39101.json \
    --gate tools/research-gate.sh --counter corpus/evidence/round39/c2-count.py
VERIFY: ok receipt=c2-after-s39101.json gate=research-gate.sh counter=c2-count.py
rc=0
$ python3 corpus/evidence/round39/verify-receipts.py \
    --receipt corpus/evidence/round39/receipts/c2-after-s39121.json \
    --gate tools/research-gate.sh --counter corpus/evidence/round39/c2-count.py
VERIFY: ok receipt=c2-after-s39121.json gate=research-gate.sh counter=c2-count.py
rc=0
```

(Both at t≈04:20, when the worktree gate equaled the HEAD blob `4253c187…`. After
the drift in §3 the same commands against the worktree fail `gate-sha256-mismatch`;
against the committed gate copy they still verify — §3.)

### 2. Digest re-derivation, independent of the verifier

`sha256sum` over the worktree, then `git cat-file -p HEAD:<path> | sha256sum`
over committed blobs (worktree == HEAD for every bound file at the time of this
table, t≈04:20; see §3 for the drift observed later):

| bound field | receipt value | worktree | HEAD blob |
|---|---|---|---|
| `verifier_sha256` | `1b6e0de6…a8496267` | match | match |
| `subject_counter_sha256` (`c1-count.py`) | `91618e91…fea05d5` | match | match |
| `counter_sha256` (`c2-count.py`) | `43849e9a…780f1fb` | match | match |
| `expect_sha256` (`expectations.jsonl`) | `01cbdc3a…29c583a` | match | match |
| `gate_sha256`/`_pre`/`_post` | `4253c187…a9b07e3` | match; pre == post | match |

Self-digests recomputed from the bodies (`json.dumps(body, indent=2,
sort_keys=True) + "\n"`, excluding `receipt_sha256`) equal the claimed values:
`51615d8d…fe4d2a` (s39101) and `b0abd051…4fa5e0` (s39121). Both receipts are
tracked and clean; file digests `c56c1770…8ff743` and `72bb45da…a4162e9` match
HEAD blobs. `subject_counter` is an absolute in-tree path and exists, so the
binding fails closed on a moved tree rather than passing.

Hand re-check of all 16 scenario rows (8 per receipt) against
`expectations.jsonl`: every equality key matches and every `ok` field re-derives.
The unbound `_contains` annotations are listed under residual risk.

### 3. Active-population cross-check (both c2 receipts in the six-row manifest)

Measured first (t≈04:20, worktree == HEAD): both c2 rows `ok`,
`R39_ACTIVE_RECEIPTS=6/6`, `C1_EXIT=0`.

Re-measured at t≈04:28 after a sibling seat edited `tools/research-gate.sh` in
the worktree (+85 lines; `sha256sum` `77791864…4f9ce841`, HEAD blob still
`4253c187…a9b07e3`):

```
$ python3 corpus/evidence/round40/c1-count.py
… c2-after-s39101.json: fail VERIFY-FAIL: gate-sha256-mismatch
… c2-after-s39121.json: fail VERIFY-FAIL: gate-sha256-mismatch
R39_ACTIVE_RECEIPTS=2/6
```

The two surviving rows are the `base-gate-r39.sh` and `mut-gate-path-env.sh`
rows; the four rows bound to `tools/research-gate.sh` (both c2 receipts, both
landed-gate c1 receipts) fail. The receipts themselves are unchanged and still
verify against committed bytes:

```
$ git cat-file -p HEAD:tools/research-gate.sh > /tmp/rev40/headgate/research-gate.sh
$ python3 corpus/evidence/round39/verify-receipts.py --receipt …/c2-after-s39101.json \
    --gate /tmp/rev40/headgate/research-gate.sh --counter corpus/evidence/round39/c2-count.py
VERIFY: ok …  (rc=0; same for s39121)
```

### 4. Disposition counter: live run vs committed record

```
$ python3 corpus/evidence/round40/c2-count.py
R2_DISPOSITION=ok
R3_DISPOSITION=ok
R4_DISPOSITION=ok
R5_DISPOSITION=ok
R39_CALIBRATION_DISPOSITIONS=4/4
C2_EXIT=0
```

`diff` against the block recorded in `corpus/evidence/round40/measure-after.txt`
→ identical. Pre-round-40 control reproduced with the frozen counter bytes over
the committed `691d264` tree (`git archive 691d264 -- SCORECARD.md corpus
.ufo/waves/round-39`, counter overlaid from `HEAD` because
`corpus/evidence/round40/` does not exist at that tip): `0/4`, exit 1 — identical
to `.ufo/waves/round-40/controls/control-before.txt`.

### 5. Source facts behind each disposition (independent re-derivation)

- **R3:** `git ls-tree -r --name-only <rev> -- corpus/knowledge | grep -c '\.md$'`
  → `50` at `8c7c867b…` and `52` at `6ac1007e…`. Confirms the correction and
  confirms the r39 report's `29 → 31` (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-39/chousa.md:132-133`) is wrong.
- **R4:** spec `items` roles and plan `tasks` agents are identical 32-seat
  counters: `executor 6, reviewer 6, critic 5, scout 3, scribe 3, mutation-tester
  3, sentinel 2, revenger 2, connector 1, simplifier 1`. The r39 report
  states the same mix (`chousa.md:168-170`). The spot-check
  (`corpus/lessons/round-39-verifier-spotcheck.md:74`) says the spec was
  "reviewer 8 / revenger 0". `git diff 691d264..HEAD -- .ufo/waves/round-39/w1-{spec,plan}.json`
  is empty and the spec commit `6d914e9` is an ancestor of the spot-check commit,
  so the compared bytes are the frozen r39 bytes. `not-reproduced` is correct.
  Extra datum: 8/0 matches **no** committed wave artifact at all — r38 spec
  6/2, r39 spec 6/2, r39 plan 6/2, r40 spec 6/2 (33 seats).
- **R2:** `c1-mutenv-s39003.json` is tracked; its `counter_sha256`
  `1c3b2a9e…484848da` differs from the committed `c1-count.py`
  `91618e91…fea05d5`, so "binds an uncommitted counter digest" and "superseded"
  are factually right.
- **R5:** frozen r39 claims line 5 discloses the L1 construction runs; the r39
  "two independent runners" phrase was unsupported.

## Findings (severity order)

### HIGH — Receipt verification hashes worktree paths, so "committed bytes" is not enforced

`corpus/evidence/round40/c1-count.py` passes `ROOT / gate` (a worktree path) to
the verifier, and `verify-receipts.py` hashes whatever sits at that path. The C1
claim says the receipts verify "against the committed gate, counter, verifier,
and expectation bytes"; that was true only because worktree == HEAD when it was
measured. Live counter-example observed during this review: a sibling seat's
in-flight edit to `tools/research-gate.sh` (+85 lines) moved the population from
`6/6` to `2/6` with `gate-sha256-mismatch`, while the unchanged c2 receipts
verify `ok` against `git cat-file -p HEAD:tools/research-gate.sh`. Four of the
six manifest rows bind `tools/research-gate.sh`, so one landed gate change
invalidates two thirds of the active population until receipts are reissued —
and it can happen after publication of a 6/6 measurement, as it did here.
Fix (cheap): materialize each bound path from HEAD (e.g. `git cat-file -p
HEAD:<path>` into a temp file) and verify that copy, asserting
`git diff --quiet HEAD -- <path>`; or have the counter refuse on a dirty bound
path. Either way the printed count then attests committed bytes as the claim
states.

### MEDIUM-1 — C2's `4/4` output is not bound to the bytes it read

The counter prints only defect names and a total; no digest of any file it reads
is printed or pinned (only the two `corpus/knowledge` revisions are pinned, by
hash in source), and it makes no assertion that `ROOT` is the lane repo.
Demonstrated by running the **committed** counter against doctored inputs:

```
$ # fixture tree built from HEAD (git archive); SCORECARD.md R5 bullet replaced by
  # "- R5: [deleted by reviewer fixture — no correction text present]."
$ cd /tmp/rev40/r5/lane && GIT_DIR=/home/vgpnk/Projects/shokunin/chousa-shokunin/.git \
    python3 corpus/evidence/round40/c2-count.py
R2_DISPOSITION=ok … R5_DISPOSITION=ok
R39_CALIBRATION_DISPOSITIONS=4/4
R5_DELETED_EXIT=0
```

The same run also takes its R3 counts from a foreign `GIT_DIR`, so the output
`R39_CALIBRATION_DISPOSITIONS=4/4` attests no particular bytes. Contrast: the
receipt machinery binds every input by digest and refuses to publish on drift
(the counter's per-run gate and expectations checks in `main()`). Fix is cheap: print
`sha256` of `SCORECARD.md`, `routed-defect-dispositions.json`,
`round39/claims.md`, the fleet report, spec, and plan in the counter output
(and/or accept `--expect-<name>` pins), and assert
`git rev-parse --show-toplevel == ROOT`.

### MEDIUM-2 — R5's leg is prose-token presence and passes without the correction

R5 reduces to `"two independent runners" in SCORECARD and "R5" in SCORECARD and
"two seeds" in SCORECARD and "L1's construction runs" in claims39 and
dispositions["R5"]["status"] == "corrected"`. Every token is available outside
the round-40 block: `"two seeds"` at `SCORECARD.md:1818` (round-32) and `:2234`
(round-39), `"two independent runners"` at `:2234`, `"R5"` at `:2054`
(round-36). Deleting the round-40 R5 bullet (fixture above) leaves all tokens
present, so the leg still prints `ok`. The `decision`/`evidence` fields of the
disposition record are never read by any leg. This directly undercuts C2's own
requirement that the counter "re-derive these states from the committed
evidence, not count prose labels alone" — R2/R3/R4 re-derive artifacts, R5 does
not. Separately, R5's premise is only half-applied: `SCORECARD.md:2234` still
asserts "improved … across two seeds, two independent runners" as a current r39
measurement, 26 lines above the supersession, with no inline mark. Fix: require
the exact corrected string `two seeds, both L1 construction runs` *within* the
round-40 block (it is present at `:2260`), read `dispositions["R5"]["decision"]`,
and annotate or reword `:2234`.

### LOW-1 — `verifier_sha256` is self-attestation; "VERIFY: ok" does not prove it ran

A byte-identical copy of the verifier at another path verifies ok (content-
addressed, intended). A copy with the two `verifier_sha256` check lines removed
verifies ok on a receipt whose `verifier_sha256` is `0*64` and whose body is
re-sealed:

```
$ python3 /tmp/rev40/weak-verify.py --receipt /tmp/rev40/doctored-receipt.json …
VERIFY: ok receipt=doctored-receipt.json gate=research-gate.sh counter=c2-count.py
weak_rc=0

$ python3 corpus/evidence/round39/verify-receipts.py --receipt /tmp/rev40/doctored-receipt.json …
VERIFY-FAIL: verifier-sha256-mismatch
strong_rc=1
```

So `verify-receipts.py`'s docstring claim that a replaced/weakened verifier
"cannot silently re-adjudicate old receipts" holds only for replacements that
retain the check; nothing in the receipt attests *which* checker ran. The
honest in-tree path is sound (`corpus/evidence/round40/c1-count.py` invokes the
fixed committed verifier path), and I closed the gap externally by hashing the
verifier myself. This class is not named in `claims.md` §Limits (which names
authorship and receipt-path symlink identity). Fix: one sentence in the
docstring and §Limits — verifier identity is established by the caller hashing
the file, not by the verifier's own output.

### LOW-2 — R2 evidence pointer does not resolve to the quoted wording

`routed-defect-dispositions.json` cites `corpus/lessons/round-39.md:60` for
"the r39 lesson saying it was not [committed]"; line 60 reads "c2 construction
receipt and the broken-shim mutant receipt were discarded". The quoted
"not committed" wording is at `round-39.md:27` (and `:25`). The counter only
tests `"not committed" in lesson` over the whole file, so pointer precision is
untested. Fact is independently true (see R2 above); the pointer should be `:27`.

### LOW-3 — The recorded control's counter bytes are unpinned, and the named tip predates the counter

`corpus/evidence/round40/` does not exist at `691d264` (first commit `6c01a41`),
so `python3 corpus/evidence/round40/c2-count.py … at lane tip 691d264` was
necessarily run with an uncommitted overlay, and neither control file records
the counter digest it ran. I closed this by reproducing the control with the
frozen bytes (`b0da3915…bdeac`) over the `691d264` tree: `0/4`, exit 1. Record
`sha256sum corpus/evidence/round40/c2-count.py` in `control-before.txt` (same for
the C1 control).

## Residual risk

- `_contains` annotations (`verify_fail_contains`, `replaced_verifier_verify_fail_contains`,
  `subject_swap_verify_fail_contains`, `unbound_verifier_verify_fail_contains`)
  are not re-derived; the receipt bodies carry the right refusal names
  (`VERIFY-FAIL: counter-sha256-mismatch`, `…expect-sha256-mismatch`,
  `…receipt-self-digest`, `…missing-field verifier_sha256`,
  `…verifier-sha256-mismatch`, `…subject-counter-sha256-mismatch`) but an
  equality-consistent receipt with wrong names would still verify. Pre-disclosed
  at `corpus/evidence/round39/claims.md:185`; not a new defect, but it remains
  the weakest link in the "8/8" claim's discrimination.
- The two c2 receipts are byte-identical in every field except `seed` and
  `receipt_sha256`; all eight `observed` dictionaries are equal. The seed only
  reaches the subject counter's naming, so the second receipt is a determinism
  replication, not a varied probe. Honest, but it adds no independent coverage.
- R4's counter reads spec/plan from the worktree without pinning their bytes or
  asserting they are unchanged since `691d264`. I checked that fact by hand
  (empty diff), but the counter itself would accept a rewritten spec.
- The lane worktree moved during this review: besides `tools/research-gate.sh`,
  `corpus/SOURCES.md` gained rows S075/S076 and 85 gate lines appeared, so the
  `6/6` observation in ledger §3 is timestamped and no longer live. The
  receipt-bound files themselves (verifier, both counters, expectations, both c2
  receipts) were re-hashed after the drift and are unchanged (`1b6e0de6…`,
  `91618e91…`, `43849e9a…`, `01cbdc3a…`), so the receipt evidence is intact; only
  the worktree-fed population count moved.

## Verification gaps

- I did not re-execute `corpus/evidence/round39/c2-count.py` on a fresh seed
  (out of this slice; the receipts were re-derived from their sealed bodies).
  Whether the harness still produces 8/8 live is not established here.
- No LSP server tool in this seat: caller/definition claims rest on direct
  execution of the committed scripts plus blob digests, not semantic references.
- Fleet repo inspected only for the r39 report's tracked/clean state and blob
  digest (`01bbed5f…d1ca2` == worktree); no fleet-side history audit.
- Concurrent sibling edits mean the worktree is not a stable snapshot; every
  digest above is reported for the state at observation time, and the committed
  (HEAD) values are given separately where they differ.

## Artifact pointers

- Receipts: `corpus/evidence/round39/receipts/c2-after-s39101.json`
  (`51615d8d…`, seed 39101), `…/c2-after-s39121.json` (`b0abd051…`, seed 39121)
- Verifier: `corpus/evidence/round39/verify-receipts.py` (`1b6e0de6…`)
- Manifest + counters: `corpus/evidence/round40/active-r39-receipts.tsv`
  (`e4623159…`), `c1-count.py`, `c2-count.py` (`b0da3915…`),
  `routed-defect-dispositions.json` (`b8569060…`), `measure-after.txt`
- Control: `.ufo/waves/round-40/controls/control-before.txt`
- Disposition inputs: `SCORECARD.md` (`4ee5256e…`), `corpus/evidence/round39/claims.md`
  (`cee81998…`), `corpus/lessons/round-39.md` (`35d8cb87…`),
  `corpus/lessons/round-39-verifier-spotcheck.md` (`d67dd681…`),
  `.ufo/waves/round-39/w1-spec.json` (`6f6b1fbb…`), `w1-plan.json` (`172f35e2…`),
  `/home/vgpnk/Projects/shokunin/.ufo/reports/round-39/chousa.md` (`01bbed5f…`)
- Fixtures used only under `/tmp/rev40/` (control replay, R5-deletion run,
  weakened-verifier run); no lane file was modified.
