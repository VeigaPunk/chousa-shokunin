# W2SentScopeFinal

## Verdict
Axes: operability, calibration. HIGH: canonical resume rejection mutates state before refusal; MEDIUM: counters follow a dangling `--receipt` symlink and write outside the named output. C1/C2 final-byte replays both score 7/7; no active `resume_continuity_v1` path exists in chousa `tools/` or `corpus/`.

## Evidence
- `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master` → `8e93bc916527b3c21f0f702967fa65c3b4c31699`.
- Initial `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin status --porcelain` → ` M .ufo/waves/round-38/w1/SentScope.md`; `?? .ufo/waves/round-38/gen-w2-spec.py`; `?? .ufo/waves/round-38/w1/CritC1Kill.md`; `?? .ufo/waves/round-38/w2-dispatch.json`; `?? .ufo/waves/round-38/w2-run.err`; `?? .ufo/waves/round-38/w2-spec.json`; `?? .ufo/waves/round-38/w2-taskcall.txt`; `?? .ufo/waves/round-38/w2/`.
- `C1_TMP=$(mktemp -d /tmp/chousa-r38-w2-scope-c1.XXXXXX)` then `python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c1-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 38401 --receipt /tmp/chousa-r38-w2-scope-c1-38401.json` (C1_TMP pointed to the existing temp dir) → `ENV_PIN_CAPTURE_MATCH=7/7`. Receipt fields: `seed=38401`, `matched=7`, `total=7`, `predicate_holds=true`, `gate_sha256_pre == gate_sha256_post = 37e2b996…ab6d27d`, `expect_sha256=d34f1735…faf8aa`.
- `C2_TMP=$(mktemp -d /tmp/chousa-r38-w2-scope-c2.XXXXXX)` then `python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/c2-count.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --seed 38402 --receipt /tmp/chousa-r38-w2-scope-c2-38402.json` (C2_TMP pointed to the existing temp dir) → `RECEIPT_BINDING_MATCH=7/7`; self-rewrite refused (`counter_rc=2`, no receipt), foreign gate distinguished (`verify_foreign_rc=0`, `verify_landed_rc=1`), re-sealed counter/expect doctors reached their named mismatch lines, body doctor reached `receipt-self-digest`, legacy receipt refused. Receipt fields: `seed=38402`, `matched=7`, `total=7`, `predicate_holds=true`, same pre/post gate hash and expectation hash as C1.
- Re-executed C1 symlink probe (seed 38403): created `/tmp/chousa-r38-w2-scope-link.b2E9UR/receipt.json` as a dangling symlink to `/tmp/chousa-r38-w2-scope-link.b2E9UR/victim.json`; output began `PRE target_absent=yes symlink=yes`, then `ENV_PIN_CAPTURE_MATCH=7/7`, `C1_RC=0 TARGET_EXISTS=yes`, `TARGET_BYTES=3386 TARGET_MODE=644`. No repository paths were targeted.
- Static source trace (read-only): canonical contract `/home/vgpnk/Projects/ufo-fsd-alpha/skills/ufo/references/run-logic.md:177-193`; resume ordering `/home/vgpnk/Projects/ufo-fsd-alpha/scripts/ufo-sighting.mjs:3817-3824`; reconciliation writes `/home/vgpnk/Projects/ufo-fsd-alpha/scripts/ufo-sighting.mjs:1991-2032`; revision increment/write `/home/vgpnk/Projects/ufo-fsd-alpha/scripts/ufo-sighting.mjs:533-553`; exact identity/status rejections at `:3675-3696,3714-3728`. Existing refusal test `/home/vgpnk/Projects/ufo-fsd-alpha/tests/ufo-sighting.test.js:2582-2647` asserts error codes but not unchanged manifest/panes.
- Active-source `grep resume_continuity_v1` over `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools` and `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus` → `No matches found`.

## Findings
1. **HIGH — resume rejection mutates wall state before rejecting.** Exploit path: with a manifest/session present, issue `ufo-sighting resume --mission <row> --run-id <wrong-id>` (or request a completed/live/unsupported row). `resumeMission()` calls `reconcileLocked()` before `resumeMissionLocked()` resolves identity/status. `reconcileLocked()` unconditionally calls `writeManifest()` twice; `writeManifest()` increments `registryRevision` and persists. It can also stop unattested live rows, prune rows, settle pane geometry and update session status. The later `IDENTITY_MISMATCH` / `RESUME_*` rejection therefore is not zero-mutation. This conflicts with the canonical contract’s explicit zero-mutation failure rule. **Impact:** rejected requests alter the durable manifest (at minimum revision), and may alter unrelated mission state/panes. **Smallest remediation:** perform read-only exact identity/status preflight before reconciliation; only reconcile after continuity checks pass, then re-read/revalidate under the lock before allowed resume mutations. The existing refusal tests check codes only, leaving the before/after state invariant unasserted. Static finding only; this seat did not invoke the UFO runtime.
2. **MEDIUM — dangling receipt symlink escapes the named output path.** C1 checks `os.path.exists(args.receipt)` before cleanup (`c1-count.py:239-242`), which is false for a dangling symlink, then writes with following `open(args.receipt, "w")` (`:290-292`). The reproduced seed-38403 run wrote a 3386-byte receipt to the symlink target while the CLI named the link. C2 has the same cleanup/write shape (`c2-count.py:311-314,363-365`). **Impact:** if an untrusted actor can plant a symlink at a shared/predictable receipt path before a trusted run, the counter overwrites/creates any file writable by the counter’s UID. **Smallest remediation:** publish via a same-directory temporary file plus atomic rename (which replaces the link itself), or use a no-follow, exclusive-create path and refuse a symlink; retain refusal cleanup without following links.

## Limits
- No source/runtime changes; only this report was written in the lane. Temp dirs, symlink fixture, and receipts were under `/tmp`; no tools were installed or updated.
- C1/C2 results are replays of final local bytes under fresh seeds, not authorship proof. No UFO runtime was invoked; resume zero-mutation finding is static control-flow evidence, as required by the no-runtime boundary.
- Final `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin status --porcelain`:
  ` M .ufo/waves/round-38/w1/SentScope.md`; ` M corpus/evidence/round38/c1-count.py`;
  ` M corpus/evidence/round38/claims.md`; ` M corpus/evidence/round38/verify-receipts.py`;
  ` M tools/research-gate.sh`; `?? .ufo/waves/round-38/gen-w2-spec.py`;
  `?? .ufo/waves/round-38/w1/CritC1Kill.md`; `?? .ufo/waves/round-38/w2-dispatch.json`;
  `?? .ufo/waves/round-38/w2-run.err`; `?? .ufo/waves/round-38/w2-spec.json`;
  `?? .ufo/waves/round-38/w2-taskcall.txt`; `?? .ufo/waves/round-38/w2/`.
  Start/end diff: `corpus/evidence/round38/c1-count.py`, `claims.md`,
  `verify-receipts.py`, and `tools/research-gate.sh` became modified after the initial
  snapshot. These are out-of-scope source changes; ownership unknown. All other status
  entries were present initially. No new W2 report was written outside W2.
- Outside-W2 reports visible at both snapshots: `.ufo/waves/round-38/w1/SentScope.md`
  (modified) and `.ufo/waves/round-38/w1/CritC1Kill.md` (untracked); both predate this
  seat’s work. Round-38 root dispatch/spec files are pre-existing non-report artifacts.
- Complete W2 inventory at the final snapshot, rooted at
  `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-38/w2/`:
  `W2SentScopeFinal.md`, `W2CritTextFinal.md`, `W2RevSeparabilityFinal.md`,
  `W2RevRoutedFinal.md`, `W2MutVerifyFinal.md`, `W2CritVacuous.md`,
  `W2ScribeLesson.md`, `W2RevReceipts.md`, `W2RevC1Final.md`,
  `W2RevC2Final.md`,
  `W2ScribeKnowledgeC2.md`,
  `W2ScribeKnowledgeC1.md`,
  `W2ScoutResidual.md`, `W2ScoutFrontier.md`, `W2RevVerifyFinal.md`,
  `W2CritKillC1Final.md`, `W2ExecC2Final.md`, `W2ConnFinal.md`,
  `W2ExecNoHarmFinal.md`, `W2LabBashFn.md`, `W2CritLaundering.md`,
  `W2ExecC1Final.md`, `W2ExecCtlFinal.md`, `swarm-registry.json`.
