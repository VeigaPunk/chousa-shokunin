# MutGateC1

## Verdict

M1 and M2 are killed by c1 (4/7, 6/7); M3 and M4 SURVIVE c1 (7/7), c2 (7/7) and the shipped
selftest (PASS 272) — two real blind spots in the C1 fixture; c2 is not separable from c1: it drops
to 5/7 exactly when c1's predicate fails, because its hold/foreign scenarios require c1 to exit 0.

## Evidence

Scratch root `W=/tmp/r38-mutgate-2943` (mine; lane untouched). Gate copied byte-identical; each
mutant is one exact-string edit of that copy.

`$ sha256sum <lane>/tools/research-gate.sh $W/pristine.sh` → both are
`37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d` (identical bytes).

| id | edit (pristine → mutant) | sha256 (mutant) |
|---|---|---|
| M1 | gate:4003 `"$ENV_BIN" -u CHOUSA_RECORD …` → `env -u …` (bare env; init kept) | `1bda0905f3805b8e…802dfde` |
| M2 | gate:491-494 `*"GNU coreutils"*) return 0;;` → `return 0` (any `--version` accepted) | `b46304c16241c094…44bf1582` |
| M3 | gate:502-505 absolute-path refusal `case` deleted from `env_pin_init` | `23df3eb85fab12de…11e9f3b3` |
| M4 | gate:4003 `"$ENV_BIN"` → `/usr/bin/env` (init/refusals unchanged) | `65ee757b53879ab8…02a98d` |

Baseline (pristine copy, fresh seeds c1=38261, c2=38271):

```
$ C1_TMP=$W/tmp python3 corpus/evidence/round38/c1-count.py --gate $W/pristine.sh --seed 38261 --receipt $W/c1-pristine.json
PASS ×7   ENV_PIN_CAPTURE_MATCH=7/7   rc=0 (8.6s);   $ C2_TMP=$W/tmp python3 corpus/evidence/round38/c2-count.py --gate $W/pristine.sh --seed 38271 --receipt $W/c2-pristine.json
PASS ×7   RECEIPT_BINDING_MATCH=7/7   rc=0 (64s; pre==post gate sha 37e2b9…, counter_sha256=bc325cf4…, expect_sha256=7cd5d824…)
```

Mutant matrix (same commands, `--gate $W/<mutant>.sh`; seeds 38261 / 38271):

```
M1 m1-bare-env.sh        c1: ENV_PIN_CAPTURE_MATCH=4/7 rc=1   c2: RECEIPT_BINDING_MATCH=5/7 rc=1
M2 m2-any-version.sh     c1: ENV_PIN_CAPTURE_MATCH=6/7 rc=1   c2: RECEIPT_BINDING_MATCH=5/7 rc=1
M3 m3-no-abs-refusal.sh  c1: ENV_PIN_CAPTURE_MATCH=7/7 rc=0   c2: RECEIPT_BINDING_MATCH=7/7 rc=0
M4 m4-hardcoded-usrbin.sh c1: ENV_PIN_CAPTURE_MATCH=7/7 rc=0  c2: RECEIPT_BINDING_MATCH=7/7 rc=0
```

M1 failing c1 rows: `env-fn-echo-scrub` `echo_lines=1, drift_rc=1, GATE_DRIFT: -GATE_GREP`;
`env-fn-root-move` `drift_rc=1, GATE_DRIFT: -FINDING:CHAIN_SOURCE_MISSING -FINDING:CLAIM_SOURCE_MISSING
-FINDING:POINTER_UNRESOLVED drift …`; `env-fn-suppress` `pin_rc=2, pin_file=False`. M2's only failing
row: `env-override-fake` `{'pin_rc':2,'pin_file':False,'refusal':''}` (expected `ENV_PROVENANCE`).
Both c2 5/7 runs fail exactly `hold-receipt-verifies` and `foreign-gate-distinguished` on
`counter_rc` (observed 1, expected 0); every binding observation still passes (`verify_rc=0`,
`verify_foreign_rc=0`, all tamper rows 1). Full rows: `$W/c2-*.out`.

Direct probes of the survivors (GNU env shim logging every invocation; relative valid GNU env):

```
# M4: only pristine's capture call reaches the override
pristine             pin_rc=0  log 8 lines incl. "-u CHOUSA_RECORD -u CHOUSA_CLAIMS … bash … verify-all"
m4-hardcoded-usrbin  pin_rc=0  log 7 lines, all "--version"     (capture bypasses RESEARCH_GATE_ENV)
# M3: RESEARCH_GATE_ENV=sub/env (valid GNU env, relative, verifiable from gate cwd)
pristine             pin_rc=2  "ENV_PROVENANCE refused: override is not an absolute path (candidate=sub/env)"
m3-no-abs-refusal    pin_rc=2  "research-gate: --pin canonical capture failed (rc=127 …)"  # no ENV_PROVENANCE
```

Shipped selftest, two ways. Relocated /tmp copy is NOT a valid control: pristine itself scores
`RESEARCH_GATE_SELFTEST: FAIL (11/272 cases)` there (corpus-boundary cases such as
`claims-fail-out-of-corpus`, `ptr-lane-abs` assume the gate's installed location) — baseline failure,
inconclusive. In place, via a private mount namespace (no lane byte written):

```
$ unshare -rm --propagation private bash -c 'mount --bind "$1" "$2"; bash "$2" --selftest' _ <mutant> <lane gate>
pristine            sha256 37e2b996… before, PASS (272 cases, 1 skipped)   (1 skip = userns-root artifact; dispatched run was 0 skipped)
m3-no-abs-refusal   sha256 23df3eb8… before, PASS (272 cases, 1 skipped)
m4-hardcoded-usrbin sha256 65ee757b… before, PASS (272 cases, 1 skipped)
$ sha256sum <lane gate> after every run → 37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d
```

Restoration: the lane gate was never edited; `git -C <lane> status --porcelain --
tools/research-gate.sh` is empty (rc 0); all mutants live only under `/tmp/r38-mutgate-2943/`.

## Findings

1. **M1 killed (c1 4/7).** Bare `env` at the capture reproduces all three r37 interposition channels
   the fixture encodes: echo re-add → `GATE_DRIFT: -GATE_GREP` + `echo_lines=1`; root move → phantom
   missing-source/unresolved-pointer drift; suppress → `--pin` rc 2, no baseline. Gate comment
   gate:459-472 ↔ scenarios `corpus/evidence/round38/c1-count.py:130-151`.
2. **M2 killed (c1 6/7), but only by one token.** Without the GNU case the fake env is accepted, the
   capture runs through a no-op script and comes back empty, so `--pin` still exits 2 with no file;
   the only mismatching field is `refusal` (`''` vs `ENV_PROVENANCE`). rc/file assertions alone
   would let M2 survive: the provenance claim rests on a substring, not a distinct exit path.
3. **M3 survived (c1 7/7, c2 7/7, selftest PASS).** No scenario supplies a relative
   `RESEARCH_GATE_ENV` (`c1-count.py:139-145`: absolute missing + absolute fake only), so deleting
   gate:502-505 is invisible. It is behavior-bearing: pristine refuses with `ENV_PROVENANCE … not an
   absolute path`; M3 accepts and pins `ENV_BIN=sub/env`, then the capture fails opaquely (rc 127, no
   `ENV_PROVENANCE`) because it re-resolves the relative path from the mktemp fixture cwd
   (gate:4001-4005). A relative-override scenario must assert the refusal *class*, not just rc 2.
4. **M4 survived everywhere, and the counter should notice.** Frozen C1 says the capture runs through
   ONE pinned absolute `env` selected by `RESEARCH_GATE_ENV`; M4 keeps every refusal but hardcodes
   `/usr/bin/env` at the capture, so the override no longer selects the child's env. The invocation
   log is the observable delta (8 vs 7 lines; pristine's capture call arrives, M4's does not). The
   fixture only ever tests rejection of bad overrides, never that a valid override *is* the capture
   binary. A positive-override scenario kills M4 and is the missing coverage.
5. **The c2 "holds" expectation is falsified for exactly the mutants c1 catches.** c2 5/7 on M1 and
   M2: `hold-receipt-verifies` and `foreign-gate-distinguished` assert `counter_rc == 0`
   (`c2-count.py:118-124,145-155`), embedding c1's predicate in the calibration score. The receipts
   themselves stay sound on those mutants (`verify_rc` 0, tamper rows 1), so the binding claim is not
   what moved. Separability holds only for mutants c1 cannot see (M3, M4). If "c1 moves, c2 holds" is
   load-bearing, c2 must stop scoring the subject counter's exit code.
6. **The shipped selftest is blind to M3 and M4 too.** gate:8441-8474 adds only the same two override
   cases (absolute missing, absolute non-GNU) plus the function cases; both mutants PASS 272 in place,
   byte-for-byte the pristine control's result. The r38 fix is proven only against the r37 attack
   channels, not against weakening of its own provenance machinery.

## Limits

- Scratch copies only (`/tmp/r38-mutgate-2943`); mutants are single-edit patches, not rebuilt gates.
- One seed per counter (c1 38261, c2 38271, both ≥38201); scenarios are selected by the frozen table,
  not by seed.
- c2 is a composition: each run internally re-runs the c1 counter; wall 64s idle, ~110s under two
  concurrent runs.
- The selftest control needed an in-place bind mount (`unshare -rm`), which runs as namespace root and
  skips 1 case; pristine and both mutants share that environment, so the comparison is valid but the
  skip itself is unexplained. M3's delta is the refusal class on this host; a host where the capture
  cwd resolved the relative path could diverge further (not explored).
- No tool installs were needed; nothing outside `/tmp` scratch and this report was written.
