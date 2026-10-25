# SimplifierAudit — round-40 counting scripts and active manifest

- **Seat:** SimplifierAudit (L2 leaf, simplifier). **Lane:** chousa-shokunin. **Date:** 2026-10-24.
- **Assigned attack:** Review `corpus/evidence/round40/c1-count.py`, `corpus/evidence/round40/c2-count.py`, and `corpus/evidence/round40/active-r39-receipts.tsv` for unnecessary abstraction, dead branches, unchecked assumptions, or a simpler implementation preserving the frozen predicates.
- **Axes:** operability (counters must keep printing the frozen lines and exiting correctly), calibration (checks must keep re-deriving truth from committed evidence), depth (prove which branches are dead vs load-bearing).
- **Edit scope honored:** zero production writes. All experiments ran in-process or under `/tmp/simplifier-r40/`. Shared tree untouched except this report.
- **Tooling record:** no tools installed or updated (none needed); pacman untouched per the host-wide pause. `lsp` device unavailable in this harness (`xd://lsp` → "No such tool"; only `ast_edit`, `debug` mounted) — caller analysis below is grep-based per fallback protocol, never presented as semantic proof.

## 1. Baseline (frozen predicates met at audit time)

Command (cwd `/home/vgpnk/Projects/shokunin/chousa-shokunin`):

```
$ python3 corpus/evidence/round40/c1-count.py; echo "c1_exit=$?"
… six rows `ok VERIFY: ok …`
R39_ACTIVE_RECEIPTS=6/6
c1_exit=0
$ python3 corpus/evidence/round40/c2-count.py; echo "c2_exit=$?"
R2_DISPOSITION=ok
R3_DISPOSITION=ok
R4_DISPOSITION=ok
R5_DISPOSITION=ok
R39_CALIBRATION_DISPOSITIONS=4/4
c2_exit=0
```

Artifacts hashed during this audit: `c1-count.py` `d9b38b57de412b44cd98dba9d6580cdb3c3183bb0f3dd4f8373bbaedac2797f0`; `c2-count.py` `b0da39157d0b15127575fc9cf36f683ec11fe1db73f58c91dcbeaa60520bdeac`; `active-r39-receipts.tsv` `e4623159…bbb40c` (matches the sha cited by sibling reports); `claims.md` `cff51807…ed263`; `routed-defect-dispositions.json` `b8569060…f31cb`; `round39/verify-receipts.py` `1b6e0de6…96267`.

`git status --porcelain` during the audit listed only w1 seat reports, `swarm-registry.json`, and round-41 staging as dirty — every file c1/c2 read was worktree-clean, so the printed verdicts equal the committed-bytes verdicts at audit time.

## 2. Deletion candidates (proven; NOT applied — frozen-artifact tradeoff in §6)

### D1 — `c2-count.py:43-45` + call sites 72-73: `role_mix` (unnecessary abstraction + unchecked assumption)

The helper dispatches on a string (`key == "role"` → `data["items"]`, else `data["tasks"]`) and silently drops rows missing the key (`if key in row`). Two defects in four lines:

- **Abstraction:** the key→container mapping is single-use knowledge hidden inside a generic helper. Two direct comprehensions at the two call sites delete the helper and the stringly branch.
- **Unchecked assumption (calibration):** the silent guard under-counts malformed input instead of failing. Proof: committed spec/plan have **0** rows missing `role`/`agent` (32/32 each), so the guard is dead on committed data — but a mutant spec with an unroled 33rd item keeps `spec_mix == plan_mix` and reviewer 6 / revenger 2 intact, so **R4 would still print ok while the spec seat total (33) silently diverges from the plan (32)**. The direct comprehension raises `KeyError('role')`, which the counter's existing handler turns into `R39_CORRECTION_COUNTER_ERROR='role'`, exit 2 — loud, and strictly closer to P2's "exact role-count agreement" intent. Counter equality compares key/count multisets, not seat totals, so the guard was the only thing masking this.

**Equivalence on live bytes (the retained contract):** imported the module, monkeypatched only `role_mix` with the simplified implementation, ran `main()`:

```
baseline rc: 0 | simplified rc: 0
output identical: True
R39_CALIBRATION_DISPOSITIONS=4/4
```

Byte-identical stdout, same exit. Caller surface: `role_mix`/`tracked` occur only inside `round40/c2-count.py` (grep across the lane; round-35's `role_mix(rows, field)` is an unrelated local helper — no import relationship; lsp unavailable, see header).

### D2 — `c2-count.py:58` `results = {}` (dead store)

`results` is read only in the post-try loop; every path reaching that loop executed the in-try assignment (last statement of the try body), and the except path `return 2`s before it. Control-flow-dead; deletion is zero-behavior.

### D3 — `c2-count.py:37-40` `tracked()` (single-caller helper — cosmetic only)

Used once (R2). Inlineable to the one `subprocess.run(...).returncode == 0` expression. Recorded for completeness; lowest value.

## 3. Kept deliberately — proved live, not dead

- **K1 `c1-count.py:33` `(proc.stdout or proc.stderr)`**: the verifier prints **every** refusal to stdout via `fail()` (`verify-receipts.py:74-77` and all later `fail` sites), so the stderr fallback is reached only when the verifier emits no stdout at all (missing script / hard traceback). Demonstrated: `python3 <missing>.py` → stdout empty, stderr `Traceback…`, rc 2. The `ok` verdict never depends on the output (returncode + `VERIFY: ok ` prefix only), so this branch is diagnostics-bearing and predicate-neutral — deleting it would harm operability. Keep.
- **K2 `c1-count.py:24-31` header/comment skip + `len(fields) != 3` malformed guard**: this *is* the kill rule's "any active manifest row missing/duplicated" population gate (`EXPECTED_ACTIVE` count + receipt-column uniqueness; a duplicated row necessarily duplicates the receipt path). Keep.
- **K3 `c2-count.py:47` `if DISPOSITIONS.is_file() else {}`**: proven live by the committed control — `.ufo/waves/round-40/controls/control-before.txt` shows exactly this branch producing `0/4` before the disposition file existed. Keep.
- **K4 `ROOT = parents[3]` depth anchor (both counters)**: checked assumption — the scripts only run from the committed tree shape (`corpus/evidence/round40` = three parents under root). A shallow copy (`/tmp/…/c2-simplified.py`) dies with `IndexError: 3` (observed). The frozen predicate only ever invokes them at the committed path; documented, not changed.
- **K5 manifest content**: six rows, no stale/duplicate/omitted entry observed; all six verified in the baseline run. Header (`receipt\tgate\tcounter`) and preservation comment are consumed correctly by K2.

## 4. Unchecked assumptions recorded (no change recommended)

- **A1 — c2 adjudicates worktree bytes, not committed blobs.** Of all nine inputs, only the R2 receipt gets a `tracked()` check; claims/lesson/scorecard/report/spotcheck/spec/plan/dispositions are read from the worktree. Today all are clean (§1), so the printed 4/4 equals the committed-bytes verdict; a future uncommitted edit could flip the counter while no receipt refuses (the round-39 receipts seal the round-39 counters' digests, not these drivers). Repair path if L1 wants it: extend `tracked()` to the seven remaining inputs (cost: seven `git ls-files` calls). Not a predicate violation today; recorded as an assumption.
- **A2 — `md_count` `endswith(".md")`** counts `git ls-tree -r --name-only` output, which lists blobs only, so a directory named `*.md` cannot inflate the count. Anchors `8c7c867b…` and `6ac1007e…` both resolve (`git cat-file -t` → `commit`).

## 5. Verdict

The two counters are already near-minimal. Exactly one real abstraction (`role_mix`, D1) and one dead store (D2) are removable with proven-identical live behavior and a strictly louder failure mode on schema drift; D3 is cosmetic. Everything else examined is load-bearing, and the next deletion candidates (stderr fallback, malformed-row guard, `is_file` before-branch) are all proven live — removing any would harm an axis, so this audit stops here.

## 6. Tradeoff / disposition

**Nothing was applied.** The r40 counter bytes are digest- and line-cited as evidence by sibling round-40 reports (e.g. `MutateGateDigest.md` hashes the counter; `ReviewR2CommitTruth.md` cites `c2-count.py:37-40,60-64` and `c1-count.py:26-29`; `CriticC1Scope.md` cites `c1-count.py` lines 24-40), and the claims erratum freezes "both frozen counters unchanged". Applying D1/D2 shifts cited line numbers and changes cited digests, so it belongs to L1 via an appended erratum (same mechanism as the S074 flip), with the proofs in §2 ready to reuse.

## 7. Artifact pointers

- Audited: `corpus/evidence/round40/c1-count.py`, `corpus/evidence/round40/c2-count.py`, `corpus/evidence/round40/active-r39-receipts.tsv` (shas in §1).
- Verifier behavior: `corpus/evidence/round39/verify-receipts.py` (`fail()` → stdout; `VERIFY: ok …` success line).
- Before-state branch proof: `.ufo/waves/round-40/controls/control-before.txt`.
- Frozen predicates: `corpus/evidence/round40/claims.md` (P1/P2, kill rules, separability).
- Scratch (outside the lane, not committed): `/tmp/simplifier-r40/` (specA mutant, simplified copy, mirror attempt artifacts).
