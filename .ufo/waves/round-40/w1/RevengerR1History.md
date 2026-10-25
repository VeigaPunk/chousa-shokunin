# RevengerR1History — round 40, w1: r39 R1 receipt-integrity chain reconstruction

Seat: leaf L2 revenger (UFO-FSD). Attack: reconstruct the r39 R1 chain from receipt hashes, committed expectations, counter, and verifier; distinguish stale expectation digest from row-tie mismatch; verify the chosen replacement/supersession path. Read-only against lane artifacts; this report is the only file written.

## 1. Reconstructed R1 chain

### 1.1 Committed bytes (lane tip `6bc90e04ac60307befacd554f7eee2b7284e2652`)

| Artifact | sha256 (16-hex prefix) |
|---|---|
| `corpus/evidence/round39/expectations.jsonl` | `01cbdc3a8208a257` |
| `corpus/evidence/round39/c1-count.py` | `91618e91640f748d` |
| `corpus/evidence/round39/c2-count.py` | `43849e9ab313dfb5` |
| `corpus/evidence/round39/verify-receipts.py` | `1b6e0de688deda74` |

### 1.2 Verifier refusal order (the grammar of the chain)

`corpus/evidence/round39/verify-receipts.py` re-derives receipts in a fixed order; the first failing class names itself:

1. `receipt-self-digest` (body self-hash, `receipt_digest()`)
2. `counter-sha256-mismatch` (:133-134)
3. `expect-sha256-mismatch` (:138-139) — **whole-file expectations binding; this is the R1 class**
4. predicate/family checks, required round-39 fields
5. `scenario-census-mismatch` (:168-169) — count + id-set vs frozen rows (loader `load_frozen_expectations` dedupes by id, last-wins)
6. `expect-tie-mismatch <id>` (:174-175) — **per-row expected-value divergence; the alternative class this seat was asked to rule out**
7. `ok-rederivation` / `matched` / `total` / `predicate_holds` recounts
8. `verifier-sha256-mismatch` (:196-197) — the adjudicating verifier must be the bound one
9. c2-only `subject-counter-sha256-mismatch` (:205-206)
10. gate `gate-sha-changed-across-run` / `gate-sha256-mismatch` / `gate-sha-alias-mismatch`

### 1.3 Receipt-binding census (all eight c1-family receipts)

Computed from committed bodies (self-digests all re-derive):

| Receipt | expect_sha256 | counter_sha256 | verifier_sha256 | matched/total | holds |
|---|---|---|---|---|---|
| r39 `c1-base-s39001.json` | `3abd2dcb1766c404` **stale** | `91618e91640f748d` = current | `1b6e0de688deda74` = current | 7/8 | False |
| r39 `c1-after-s39011.json` | `3abd2dcb1766c404` **stale** | current | current | 8/8 | True |
| r39 `c1-mutenv-s39013.json` | `3abd2dcb1766c404` **stale** | current | current | 4/8 | False |
| r39 `c1-mutenv-s39003.json` | `3abd2dcb1766c404` **stale** | `1c3b2a9e453ebfdc` **uncommitted** | current | 7/8 | False |
| r39 `c1-after-s39111.json` | `01cbdc3a8208a257` = current | current | current | 8/8 | True |
| r40 `c1-base-s39001-regenerated.json` | `01cbdc3a8208a257` = current | current | current | 7/8 | False |
| r40 `c1-after-s39011-regenerated.json` | `01cbdc3a8208a257` = current | current | current | 8/8 | True |
| r40 `c1-mutenv-s39013-regenerated.json` | `01cbdc3a8208a257` = current | current | current | 4/8 | False |

The preserved c2 actives (`c2-after-s39101.json`, `c2-after-s39121.json`) already bind `01cbdc3a…` and verify ok.

**Reading:** four old c1 receipts were sealed against a pre-commit working-tree `expectations.jsonl` digesting `3abd2dcb…`; the committed final hashes `01cbdc3a…`. Three of the four are stale *active measurements* (R1); the fourth (`s39003`) is additionally stale on its counter binding (`1c3b2a9e…` never committed) and on its gate binding (`gate_sha256 = 890226590546ce7f…`, which matches neither the committed mutant gate `e1251030ef61722c…` nor `tools/research-gate.sh`) — a triple-stale superseded draft (R2), correctly excluded from the active set and not regenerated.

## 2. Exact commands and outputs

### 2.1 Frozen counter (C1 predicate)

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

Frozen predicate P1 holds at tip: `R39_ACTIVE_RECEIPTS=6/6`, exit 0.

### 2.2 Superseded originals refuse, each at its earliest stale binding

```
c1-base-s39001 => VERIFY-FAIL: expect-sha256-mismatch
c1-after-s39011 => VERIFY-FAIL: expect-sha256-mismatch
c1-mutenv-s39013 => VERIFY-FAIL: expect-sha256-mismatch
c1-mutenv-s39003 => VERIFY-FAIL: counter-sha256-mismatch
```

(Verifier invoked per receipt with its gate and `--counter corpus/evidence/round39/c1-count.py`; exit 1 each. Matches the committed control `.ufo/waves/round-40/controls/r1-stale-before.txt`, including the fourth receipt refusing on the earlier check.)

Minor control note: `r1-stale-before.txt` maps `c1-mutenv-s39003.json` → `tools/research-gate.sh`, while that receipt's own `gate` field declares `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-39/controls/mut-gate-path-env.sh`. Immaterial: the counter binding refuses before any gate check (observed under both gate choices). The receipt's declared gate is the faithful one.

### 2.3 Digest-class vs tie-class isolation (synthetic, in `/tmp`; no lane writes)

Method: mutate one committed expectation row (`hold-plain.pin_rc 0→3`) into a temp expectations file; (a) run the verifier with an *original* active receipt → digest fires first; (b) re-seal a synthetic receipt's `expect_sha256` + `receipt_sha256` to the mutated file and re-run → tie check isolated; (c) additionally append a duplicate `hold-plain` row with different values (loader last-wins) and re-seal → duplicate-row tie behavior.

```
baseline mutated-digest, original receipt -> (1, 'VERIFY-FAIL: expect-sha256-mismatch')
resealed-to-mutated receipt         -> (1, 'VERIFY-FAIL: expect-tie-mismatch hold-plain')
duplicate-row last-wins tie         -> (1, 'VERIFY-FAIL: expect-tie-mismatch hold-plain')
```

So the two classes are mechanically distinct and ordered: a stale file digest refuses before any row is examined; a row-value or duplicate-row (last-wins) divergence refuses as `expect-tie-mismatch <id>` only after the digest matches. Census survives duplication (dict dedupe keeps `len(frozen)=8`), so a duplicate-row tie is caught by the tie check, not the census.

## 3. Verdict: stale expectation digest, NOT row-tie mismatch

- **All four old receipts' sealed rows tie the committed expectations exactly.** Per-row `expect` of every scenario in `c1-base-s39001`, `c1-after-s39011`, `c1-mutenv-s39013`, `c1-mutenv-s39003` equals the committed frozen row for that id; the eight sealed rows are byte-identical across all four receipts; scenario order and id set match the committed census (8 rows). A row-content drift would have produced `expect-tie-mismatch` after a digest re-seal; it does not exist here.
- **Counterfactual check:** the three stale-active receipts bind current counter, verifier, and gate digests, and their re-sealed bodies verify ok end-to-end (§2.1). Had the committed bytes still digested `3abd2dcb…`, they would have passed in full. The R1 failure class is therefore exactly and only the stale whole-file digest — matching r39 claims.md R1 wording ("stale expectation bindings").
- `c1-mutenv-s39003` is a *different* failure inside R1's four: first stale binding is the uncommitted counter digest, so it refuses a class earlier. The lane's decision to treat it as R2 (superseded draft, preserve, exclude) rather than regenerate it is the correct reading of the verifier's refusal grammar.

## 4. Replacement/supersession path — verified

1. **Chosen path:** three stale active measurements re-sealed at new round-40 paths (`corpus/evidence/round40/receipts/*-regenerated.json`); committed originals untouched (working tree clean for `corpus/evidence/round39/receipts/`, `expectations.jsonl`, `verify-receipts.py`, `c1-count.py`, and the r39 gates; `corpus/evidence/round39/receipts/` last touched at r39 commit `6d914e9`).
2. **Minimal delta:** each regenerated receipt differs from its original in exactly two fields — `expect_sha256` (`3abd2dcb…` → `01cbdc3a…`) and the recomputed `receipt_sha256`. Scenarios (`expect`, `observed`, `ok`), `matched`/`total`, `predicate_holds` (7/8 False, 8/8 True, 4/8 False), counter/gate/verifier bindings, and seed are all identical. The measurements were carried over verbatim, not re-run to a rosier outcome — the honest failures (base 7/8, mutenv 4/8) remain honestly recorded as `predicate_holds: false`.
3. **All three verify** `VERIFY: ok` under the committed verifier, and the frozen counter prints `R39_ACTIVE_RECEIPTS=6/6`, exit 0 (§2.1). The active manifest has exactly 6 unique rows; the four superseded originals are all outside it; `s39003` is dispositioned under C2/R2 (`corrected`: preserve as superseded draft; `corpus/evidence/round40/routed-defect-dispositions.json`, citing claims.md:197 and the receipt itself).
4. **Kill-rule sweep (C1):** no active receipt refuses the committed verifier; no manifest row missing/duplicated (counter enforces population=6 and uniqueness); counter population is six. No kill condition fires.

## 5. Provenance limit on the stale bytes (marked inference where noted)

The exact `3abd2dcb…` bytes are unrecoverable from the lane:

- Never committed: `git log --all -S` finds the literal only in the four receipts, r39 claims.md, and the r40 control; `expectations.jsonl` itself has exactly one commit (`6d914e9`, final bytes).
- jj `evolog` snapshots of the change that owns the file contain either no file or the final `01cbdc3a…` bytes (`35e10b9a`, `7180206b`, `6d914e95` all hash `01cbdc3a…`; `97ba3b9f`, `c08c5501` predate the file). The stale working-tree state fell between op-log snapshots.
- Reconstruction attempts from surviving evidence (sealed rows + committed rows; subsets of the 9 c2 rows × c1/c2 ordering × serialization variants: spaced/compact × sorted/insertion-key order × newline/trailing variants) produced no candidate digest. The receipts seal sorted-key serializations (the counter's writer), so the stale file's original key order/whitespace — and any pre-final c2 block — is lost.

What *is* proven from surviving evidence: the stale file contained the same eight c1 rows with identical expected values ([INFERENCE] it was a mid-round working copy of the same expectations file, serialized differently and/or with a not-yet-final c2 block; the c2 actives already bind the final digest, dating the c1 seals before the c2/serialization finalization).

## 6. Verdict

**PASS.** The r39 R1 chain reconstructs cleanly: four c1 receipts sealed against a pre-commit expectations snapshot (`3abd2dcb…`); the committed file (`01cbdc3a…`) refuses them at `expect-sha256-mismatch` (three receipts) and, for the superseded draft, earlier at `counter-sha256-mismatch`. The failure class is stale-digest, not row-tie — every sealed row ties the committed rows. The chosen replacement path (three minimal two-field re-seals at round-40 paths, originals preserved, draft excluded per R2) verifies 6/6 under the frozen counter with exit 0 at tip `6bc90e04ac60307befacd554f7eee2b7284e2652` — the lane tip at measurement time; see §7 for tip movement to `a3aac04` and the revision-scoped gate fact. No production files edited; no tools installed (pacman untouched; no non-pacman channel needed).

## 7. Addendum — W0: `tools/research-gate.sh` gate movement (round-41 C1 block)

SentinelWriteScope flagged W0 during this seat's run; verified directly in two phases.

### Phase 1 — worktree dirty (observed live)

- `git status`: ` M tools/research-gate.sh`; HEAD sha256 `4253c18738f84df9…`, live worktree sha256 `2cb04bddfd5601d7…` (mtime 04:26:28). The sentinel observed a different live sha (`77791864…`, mtime 04:23:46) minutes earlier — the file was under active round-41 mutation. Not restored.
- All four research-gate-gated active receipts (`c1-after-s39011-regenerated.json`, `c1-after-s39111.json`, `c2-after-s39101.json`, `c2-after-s39121.json`) bind `gate_sha256 = 4253c187…` with `pre == post`, i.e. the `6bc90e0` committed bytes.

### Phase 2 — edit committed; predicate is revision-scoped (verified at named revisions)

- The gate edit landed: tip `6bc90e0` → `a3aac04492a3a5e99e351fc9941fcba801c152fe` via `b173b09` (r41 claims/controls freeze) and `1bd9001` (r41 pin capture; carries `tools/research-gate.sh` at `2cb04bdd…`). Worktree is clean at that path; live == HEAD == `1bd9001` bytes == `2cb04bdd…`.
- **Frozen counter at tip `a3aac04`: `R39_ACTIVE_RECEIPTS=2/6`, exit 1** — exactly the four research-gate-gated rows refuse `VERIFY-FAIL: gate-sha256-mismatch` (receipts bind `4253c187…`, tip commits `2cb04bdd…`); the two non-research-gate rows (base-gate, mut-gate) verify ok.
- **§2.1's `R39_ACTIVE_RECEIPTS=6/6` (exit 0) is valid as `6bc90e0`-scoped**: measured before the dirtying with HEAD-matching gate bytes; independently consistent with the sentinel's 6/6-at-`6bc90e0` observation.

### Attribution and scope

- Worktree sensitivity became committed-tip sensitivity: the r39 verifier pins the CLI-supplied gate bytes (r39 claims.md Limits: "pinning is to the CLI-supplied bytes — committed-tree membership is the caller's discipline"), so at `a3aac04` the six-row active population can only fully verify after round-41 re-issues receipts against `2cb04bdd…`. That re-issue belongs to the round-41 C1 block (W0 phase 2), not this seat's item; nothing restored, nothing regenerated here.
- The W0 addendum does not touch this seat's verdict in §1–§6: the R1 stale-digest refusals, the row-tie exclusion, and the replacement-path delta are receipt-body facts independent of the gate movement; the base and mutant gates are unchanged since `6d914e9`.

## 8. Artifact pointers

- Verifier (refusal grammar, tie check :174-175, digest check :138-139): `corpus/evidence/round39/verify-receipts.py`
- Frozen counter / manifest: `corpus/evidence/round40/c1-count.py`, `corpus/evidence/round40/active-r39-receipts.tsv`
- Committed expectations: `corpus/evidence/round39/expectations.jsonl` (sha256 `01cbdc3a8208a257e2b0ea4304c87a6d74be313a722cf667c5d126a4c29c583a`)
- R1/R2 findings: `corpus/evidence/round39/claims.md:196-197`; red-before control: `.ufo/waves/round-40/controls/r1-stale-before.txt`
- Superseded draft disposition: `corpus/evidence/round40/routed-defect-dispositions.json` (R2)
- Regenerated receipts: `corpus/evidence/round40/receipts/c1-{base-s39001,after-s39011,mutenv-s39013}-regenerated.json`
- Superseded originals: `corpus/evidence/round39/receipts/c1-{base-s39001,after-s39011,mutenv-s39003,mutenv-s39013}.json`
