Report: .ufo/waves/round-34/w2a2/MutC3Inject.md
Seat: MutC3Inject (leaf mutation-tester, round-34 attempt 2, wave 2a2). Date 2026-10-23.
Scope: C3 counter soundness only (C2 was not re-derived here). Lane treated read-only.

## Object under test (pinned)

- Counter: `corpus/evidence/round34/self-audit.py`, sha256 `22a6822ca79f7f5eac8d0e64ad7e6bc0fd0a46af0be8353d52884b75d246091f`.
- Set: `corpus/evidence/round34/audit-set.json`, sha256 `01f6c4b49febdd02a28d12d7ad1c623ce015219df53e4c01d0582a9369479f5c`.
  Measured composition: 43 checks, unique ids — `path` 20 (17 `path-NN` + 3 `shonen-NN`), `git_commit` 12,
  `sha256` 4, `receipt_binding` 4, `grep_assert` 3.
- Frozen predicate: `corpus/evidence/round34/claims-a2.md:144-153` — "C3 is met iff, on the landed lane revision, the tool with
  the committed audit set prints `SELF_AUDIT_UNDISPOSITIONED=0`"; the printed count must be "reproduced verbatim by a re-run".
- Gate blob: `tools/research-gate.sh` sha256 `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b`
  (matches required prefix `a6307edf687ac0fb`; re-checked after all probes).

Tip observation (factual drift, benign): `git -C <lane> rev-parse HEAD` = `fe3db76c0ae9fa18cfebcf127fec073354a1eb03`,
not the frozen `707da8184a0fc4d10ab3f17271556cdf364f0af5`. `git merge-base --is-ancestor 707da81 HEAD` → exit 0;
`git diff --stat 707da81 fe3db76` = three wave-spec JSON files only. Blob sha256 at `707da81` and `fe3db76` are identical for
the gate (`a6307edf…`), `audit-set.json` (`01f6c4b4…`), `self-audit.py` (`22a6822c…`) and the empty dispositions file
(`e3b0c442…`). All probes therefore ran on bytes identical to the frozen tip; the record should not claim HEAD == 707da81.

## Baseline reproduction (pristine set)

Command:
```
timeout 300 python3 corpus/evidence/round34/self-audit.py --lane /home/vgpnk/Projects/shokunin/chousa-shokunin \
  --set corpus/evidence/round34/audit-set.json --dispositions corpus/evidence/round34/audit-dispositions.md
```
Result: exit 0; 43 `AUDIT ... ok` lines, 0 MISMATCH; `SELF_AUDIT_MISMATCHES=0`; `SELF_AUDIT_UNDISPOSITIONED=0`.
Re-run on the lane is byte-identical to the committed first counted run
`.ufo/waves/round-34/measure-a2/audit-first-run.txt` (`diff -u` empty) and to my first run (`diff -q` empty) — K reproduced
verbatim. Evidence: artifact `baseline-lane-rerun.txt`, sha256 `b709781c…`.

Pinned-revision control: local clone of the lane checked out at `707da818…` (scratch), same command with `--lane <clone>` →
exit 0, 43 ok, `MISMATCHES=0`, `UNDISPOSITIONED=0` (`baseline-clone-707da81.txt`, same sha256 `b709781c…`). So 0/0 holds at
the frozen revision, not only on the drifted worktree.

## Mutant: five injected lies (one per check kind) — KILLED 5/5

Construction: committed set copied, five checks **appended** (no committed check edited), preserving the frozen set:
`audit-set-5lies.json` (48 checks, sha256 `1afb52d20b87b59c91358be21221770f66a5b5a08f62a96bf09f23246a1a4d13`).

| injected check | kind | lie | detector output (verbatim) |
|---|---|---|---|
| `lie-bogus-commit` | git_commit | prefix `abcdef012345` (verified unresolved before use: `git rev-parse --verify --quiet abcdef012345^{commit}` exit 1) | `prefix abcdef012345 does not resolve` |
| `lie-wrong-sha` | sha256 | `tools/research-gate.sh` pinned to `0`×64 | `digest a6307edf687ac0fb != pinned 0000000000000000` |
| `lie-missing-path` | path | `corpus/evidence/round34/does-not-exist-lie.md` | `missing: corpus/evidence/round34/does-not-exist-lie.md` |
| `lie-receipt-wrong-commit` | receipt_binding | receipt `c2-after-s5033.json` (gate `a6307edf…`) bound to commit `bf7c931a` (gate `772a1d8e…`) | `receipt gate a6307edf687a != 772a1d8e4d94@bf7c931a` |
| `lie-grep-flip` | grep_assert | `PASS \(256 cases\)` in `SKILL.md`, `present:false` | `pattern PASS \(256 cases\) present` |

Run with empty dispositions file: exit 0; 48 AUDIT lines = **43 ok + 5 MISMATCH**; `SELF_AUDIT_MISMATCHES=5`;
`SELF_AUDIT_UNDISPOSITIONED=5`. Every mismatch id is exactly one of the five injected ids; no collateral mismatch, no crashed
check (`run-5lies.txt`, sha256 `ce0afc93…`).

Disposition delta: one line `lie-missing-path | accepted injected-lie-for-coverage-test` → `MISMATCHES=5`,
`UNDISPOSITIONED=4`; that id prints `dispositioned: accepted injected-lie-for-coverage-test`, the other four `NO DISPOSITION`
(`run-5lies-one-disp.txt`, sha256 `8bc2f902…`). Exactly −1.

In-place edit variant (same kind as the frozen "no check is edited" rule): copied set with
`bind-c2-after-5033.commit` changed `fe0f22e0`→`bf7c931a`, run on the clean lane → 1 mismatch,
`receipt gate a6307edf687a != 772a1d8e4d94@bf7c931a`, exit 0 (`run-wrongcommit-cleanlane.txt`, sha256 `91ed434b…`).
The counter catches edits as well as appends.

Verdict: KILLED. The count is exact for the five injected lies on a clean tree, `UNDISPOSITIONED` tracks the mismatch set
exactly, and a disposition line decrements it by exactly one.

## Surviving mutants (coverage findings; contract unchanged)

S1 — vacuous disposition accepted. With `lie-missing-path |` (empty reason) the run prints `dispositioned: ` and
`SELF_AUDIT_UNDISPOSITIONED=4`, i.e. the empty line counts as a disposition (`run-5lies-vacuous.txt`, sha256 `89744f49…`).
Parser at `self-audit.py:74` accepts any non-comment line containing `|` and never validates the
`fixed <commit>` / `routed <where>` / `accepted <reason>` forms named at `claims-a2.md:144-153`. A committed `id |` line would
satisfy `J=0` while carrying no repair, route or reason. The committed dispositions file is empty (`e3b0c442…`), so this does
not affect the landed 0/0; it is a strictness gap in the counter.

S2 — file bytes are read from the working tree, not HEAD. In the scratch clone at `707da81` I changed only the working-tree
receipt `.ufo/waves/round-34/measure-a2/c2-after-s5033.json` (`gate_sha256` `a6307edf…`→`772a1d8e…`, uncommitted) and ran a
copied set whose `bind-c2-after-5033.commit` = `bf7c931a` (a lie relative to HEAD). Detector: `AUDIT id=bind-c2-after-5033 ok
binds 772a1d8e4d94@bf7c931a`, `SELF_AUDIT_MISMATCHES=0`, `SELF_AUDIT_UNDISPOSITIONED=0`, exit 0
(`run-wrongcommit-tampered.txt`, sha256 `3887b96d…`), while `git show HEAD:<receipt>` still carries `a6307edf…`. Cause:
receipt content is read from the worktree (`self-audit.py:96-110`) and only the comparison digest comes from git; the same
trust applies to `path`, `sha256` and `grep_assert` reads. On a dirty tree the counter can return 0/0 over bytes that no commit
contains. This was **not** live on the lane: tracked tree was clean at probe time (`git status --porcelain` showed only
untracked `.ufo/waves/round-34/w2a2/` and a sibling-generated `[INFERENCE]` `corpus/evidence/round34/__pycache__/c2-count.cpython-314.pyc`,
mtime 16:00:51; I never imported or ran `c2-count.py`, and a script run as `__main__` writes no `.pyc`, so it is not mine; I did not touch it). The landed K=0 is therefore a clean-tree result.

Restoration: clone receipt restored with `git -C <clone> checkout -- <path>`; `git status --porcelain` = 0 lines; restored
sha256 `03d8e701fc73dd30d49fbbd47c2997f00aac9512c01c3518a748f9c26424565f` equals `git show 707da81:<receipt>` blob hash
exactly.

## Non-interference

No lane production file, lane Git index or jj state touched; every experiment ran in
`/fast/scratch/hyaku/chousa-r34-a2/w2/MutC3Inject/` (all commands `timeout`-bounded; all exit codes recorded above) or wrote
into my assigned `.ufo/waves/round-34/w2a2/MutC3Inject/` directory. No network, no installs, no long-lived processes, no
process signalling. Gate sha256 re-verified after probes: `a6307edf…`.

## Verdict

C3's committed measurement reproduces: `SELF_AUDIT_MISMATCHES=0` / `SELF_AUDIT_UNDISPOSITIONED=0` over 43 checks on the
clean lane and independently at pinned `707da81`, byte-identical to the committed first run. The five-lie mutation is killed
exactly 5/5 with no collateral count, and the disposition delta is exactly −1. C3 is **not falsified**. Two counter-strength
limits are reported as coverage findings, not as edits to the contract: vacuous dispositions are accepted (S1), and file
content is audited from the worktree rather than HEAD, so a dirty tree can defeat `receipt_binding` without moving the count
(S2). Limits of this seat: C2 not re-derived; lane tip drift (HEAD `fe3db76c`, frozen `707da81`, spec-only diff) recorded
rather than resolved.

## Artifacts (all < 1 MiB; sha256 measured)

| file | sha256 |
|---|---|
| `audit-set-5lies.json` | `1afb52d20b87b59c91358be21221770f66a5b5a08f62a96bf09f23246a1a4d13` |
| `audit-set-wrongcommit.json` | `dd7f4f7fc72d00bcd9beeeb9d61d389353236228ca8633226d9fdbaa124d63ec` |
| `baseline-lane-rerun.txt` | `b709781c949b5f63371783b93f3b99958f6b48b413a96899de1209646af06452` |
| `baseline-clone-707da81.txt` | `b709781c949b5f63371783b93f3b99958f6b48b413a96899de1209646af06452` |
| `run-5lies.txt` | `ce0afc9322c004dfe7805a0311b01723207ff151ca497c04d92c2c26988282a6` |
| `run-5lies-one-disp.txt` | `8bc2f902c5b7ce34726a12e83bc2a7ff7d22d2155dd8c700892fce9a2734da45` |
| `run-5lies-vacuous.txt` | `89744f4956f42add32d6a725e87c2d47667d993ace0a453b2857d692150245d6` |
| `run-wrongcommit-cleanlane.txt` | `91ed434b1299c35e1b24ea0b48654d258e3c96f8ef86b8c14a20ae3e7e45fdaa` |
| `run-wrongcommit-tampered.txt` | `3887b96d7cfdee0c2919dbcc8462bbfe190cf29dd32b27095254a3d1354510ba` |
| `dispositions-empty.md` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `dispositions-one.md` | `3f297f8182ad2dec85d1b7548a3275060744327cd3c3ee8788e9081118e23562` |
| `dispositions-vacuous.md` | `3080810114f198057b1b003215ba814cc535d18adf96aca87ce6f03a1886112c` |

Scratch: `/fast/scratch/hyaku/chousa-r34-a2/w2/MutC3Inject/` — includes the disposable `lane-707da81/` clone (receipt
restored, worktree clean, sha256 above); all logs quoted here are copied into the artifact directory above.
