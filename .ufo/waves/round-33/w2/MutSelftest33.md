# MutSelftest33 — r33-top-* mutation probe

## Verdict and scope

**HOLDS for the assigned seven-case operability check:** each of selftest cases 242–248 kills at least one mutant also killed by the frozen C1 v2 counter. Eight mutants were exercised, all in this seat's isolated scratch copies. There are two observed coverage disagreements: **M5 is killed only by the counter; M6 is killed only by the seven targeted selftest cases.** These are coverage findings, not changes to the contract. This probe did not falsify C1 on landed bytes.

Axes: operability (the named cases actually reject defects), coverage discrimination (which detector rejects which defect), and evidence integrity (pristine/mutated/restored runs, exact restoration, hashes and receipts).

In this report, **selftest means cases 242–248 only**, not the entire 248-case suite. The detector preserves, byte-for-byte, the landed `tclaims` helper (`tools/research-gate.sh:3998-4026`), its source fixture (`:7041-7054`), and all seven case bodies/assertions (`:7568-7630`). It invokes the public `verify-claims` CLI in fresh Bash processes. Extraction identity is recorded in `A/detector-extraction.json:1-19`. No full-suite result is claimed.

Paths below use:

- `A = /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/w2/MutSelftest33`
- `S = /fast/scratch/hyaku/chousa-r33/w2/MutSelftest33`
- `C = /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round33/c1-count-v2.py`

The governing design was read at `corpus/evidence/round33/claims.md:93-140` after v1. Landed gate SHA-256 is `94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e`; counter SHA-256 is `cb354dd1b5bdf2540e2bf356d945e01cd3ce8207d66e7a1ec76f363650e6a514`.

## Per-case witnesses: both detectors kill

Baseline output is `A/pristine.selftest.stdout:1-8`: all seven cases pass. Every restored run also passes all seven (the corresponding `*-restored.commands.json` records its complete passed-case list).

| Case | Name | Qualifying mutant | Actual changed output / assertion | Counter output | Evidence |
|---|---|---|---|---|---|
| 242 | r33-top-nested-line | M7 | NB1 becomes `observed=mislocated`, nested line 9 read instead of top-level 1 | `TOPLEVEL_FIELD_MATCH=108/156` | `A/M7-mutated.selftest.stdout:1-6`; `A/M7-mutated.json` |
| 243 | r33-top-nested-sha | M8 | NB2 becomes invalid with `sha256 malformed` although no top-level sha256 exists | `TOPLEVEL_FIELD_MATCH=132/156` | `A/M8-mutated.selftest.stdout:2-7`; `A/M8-mutated.json` |
| 244 | r33-top-nested-id | M7 | CLAIM names FAKEID, not NB3; gate exits 0 but the exact-name assertion fails | `TOPLEVEL_FIELD_MATCH=108/156` | `A/M7-mutated.selftest.stdout:8-12`; `A/M7-mutated.json` |
| 245 | r33-top-dup-line | M2 | DP1 becomes supported/CLEAN, exit 0 instead of invalid/DRIFT, exit 1 | `TOPLEVEL_FIELD_MATCH=132/156` | `A/M2-mutated.selftest.stdout:4-8`; `A/M2-mutated.json` |
| 246 | r33-top-confuser-flat | M3 | escaped-backslash confuser makes the scanner return invalid | `TOPLEVEL_FIELD_MATCH=148/156` | `A/M3-mutated.selftest.stdout:5-10`; `A/M3-mutated.json` |
| 247 | r33-top-confuser-nested | M4 | string bracket content makes FC2 invalid instead of supported | `TOPLEVEL_FIELD_MATCH=152/156` | `A/M4-mutated.selftest.stdout:6-11`; `A/M4-mutated.json` |
| 248 | r33-top-dup-id | M2 | both repeated-id rows become supported/CLEAN rather than invalid | `TOPLEVEL_FIELD_MATCH=132/156` | `A/M2-mutated.selftest.stdout:11-16`; `A/M2-mutated.json` |

Exact inputs and `lib/span.md` are preserved under `A/inputs/`; the input bytes also occur in `A/targeted-selftest.sh`. No case was narrowed to an exit-code-only assertion.

## All eight mutants

Line numbers refer to the unmodified landed gate, also preserved as `A/landed-gate.sh`. Each mutant changes one behavior-bearing point. Exact changes are in `A/M1.patch` through `A/M8.patch`; full mutated gates are preserved as `A/M1.mutant-gate.sh` through `A/M8.mutant-gate.sh`. Mutation artifacts are evidence, not production changes.

| Mutant | Point and defect | Cases that kill it | Counter matched | Selftest rc / counter rc | Verdict |
|---|---|---|---|---|---|
| M1 | Insert `return 1` before `:1192`: reject nested containers instead of skipping their values | 242, 243, 244, 247 | 48/156 | 1 / 1 | KILLED by both |
| M2 | `:1237`: replace duplicate-flag assignment with `:`; duplicates are no longer flagged | 245, 248 | 132/156 | 1 / 1 | KILLED by both |
| M3 | `:1185`: consume escaped character with `esc=1`, not `esc=0` | 246 | 148/156 | 1 / 1 | KILLED by both |
| M4 | `:1196`: replace `if (( in_str ))` with `if (( 0 ))`; nested strings no longer protect brackets | 247 | 152/156 | 1 / 1 | KILLED by both |
| M5 | `:1622`: omit `span` from the duplicate-field validation loop | none | 152/156 | 0 / 1 | SURVIVED selftest; KILLED counter |
| M6 | `:1638`: use nonempty second id rather than equality to retain the first duplicated id | 248 | 156/156 | 1 / 0 | KILLED selftest; SURVIVED counter |
| M7 | `:1261-1262`: replace top-level string-table lookup with the first raw regex match | 242, 244, 247 | 108/156 | 1 / 1 | KILLED by both |
| M8 | `:1272`: replace top-level presence-table lookup with raw regex search | 243 | 132/156 | 1 / 1 | KILLED by both |

The counter outputs in this table are the literal first lines of `A/<mutant>-mutated.counter.stdout`; every corresponding receipt exists. All counter gate subprocesses exited 1, with no gate timeout (`gate_rc=1`, `gate_timed_out=false` in each receipt). Thus these kills are score mismatches, not baseline or harness failures.

### Counter-only finding: M5

M5 leaves every targeted case passing: `A/M5-mutated.selftest.stdout:1-8`. The frozen counter instead prints `TOPLEVEL_FIELD_MATCH=152/156`, with `D1_duplicate_top_level=20/24`. Its four misses are invalid truth observed as supported, ids `c41bc6a4d12`, `c23ca24ddef`, `cf9fac69656`, `cdce6b33669` (`A/M5-mutated.json`, `misses`). Removing only `span` from the loop is recorded in `A/M5.patch`; the counter's duplicated-span construction is `C:243-267`. The seven new cases include duplicate line and id records but no duplicate span record (`tools/research-gate.sh:7591-7599,7620-7630`). This is a demonstrated coverage hole in these seven cases, not a surviving mutant of the counter.

### Selftest-only finding: M6

Input (the actual second row of `A/inputs/r33-top-dup-id.jsonl:2`, also gate `:7622`):

```json
{"id":"DI2","id":"DI3","source":"lib/span.md","span":"alpha beta gamma delta","expect":"supported"}
```

Case 248 expects `CLAIM id=line2 ... observed=invalid` (`tools/research-gate.sh:7628`). M6 emits `CLAIM id=DI2 expected=supported observed=invalid source=lib/span.md at=- verdict=invalid`, so the case fails even though the gate still exits 1 and both rows remain invalid (`A/M6-mutated.selftest.stdout:7-15`). The counter prints `TOPLEVEL_FIELD_MATCH=156/156` (`A/M6-mutated.counter.stdout:1`; receipt `A/M6-mutated.json`). This is an intentional scope difference: design v2 explicitly excludes differing duplicated ids from counted fixtures (`claims.md:111-114`), and the generator uses identical duplicated ids only (`C:257-258`). It is not evidence that P1 v2 is broken.

## Bounded commands and every counter receipt

The runner was executed as:

```sh
timeout --kill-after=5s 850s prlimit --nproc=2000 --as=4000000000 --fsize=900000 -- python3 /fast/scratch/hyaku/chousa-r33/w2/MutSelftest33/probe.py
```

Observed exit 0, elapsed 52.581 seconds. Runner stdout is `A/runner.stdout`; stderr is `A/runner.stderr`. Four independent scratch-copy probes ran concurrently, with no subagents or background services. The runner source is preserved at `A/probe.py`.

Each phase uses the same two detectors. The exact first-phase commands are recorded verbatim in `A/pristine.commands.json:12,33`; corresponding files exist for every phase below:

```sh
timeout --kill-after=5s 180s prlimit --nproc=2000 --as=4000000000 --fsize=900000 -- bash "$S/targeted-selftest.sh" "$S/pristine.sh" "$S/pristine.selftest-fixture" > "$A/pristine.selftest.stdout" 2> "$A/pristine.selftest.stderr"
timeout --kill-after=5s 700s prlimit --nproc=2000 --as=4000000000 --fsize=900000 -- python3 "$C" --gate "$S/pristine.sh" --seed 863330000001 --receipt "$A/pristine.json" > "$A/pristine.counter.stdout" 2> "$A/pristine.counter.stderr"
```

`C1_TMP`, `C2_TMP`, and `TMPDIR` are set to the phase's own `S/<phase>.tmp`; inherited `CHOUSA_*`, `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` settings are removed. Commands, environment, actual PIDs, exits, elapsed times and stdout/stderr hashes are in each `A/<phase>.commands.json`. Counter stdout was redirected to a file, not piped, so receipt generation was allowed to finish.

**Complete run census** (all 17 invocations; no omitted or repeated seeds). For each row the receipt is `A/<phase>.json`, stdout is `A/<phase>.counter.stdout`, and the exact command/exit record is `A/<phase>.commands.json`. `Match` is the literal `TOPLEVEL_FIELD_MATCH` numerator/denominator.

| Phase | Fresh seed | Match | Counter exit | Selftest exit |
|---|---:|---:|---:|---:|
| pristine | 863330000001 | 156/156 | 0 | 0 |
| M1-mutated | 863330000002 | 48/156 | 1 | 1 |
| M1-restored | 863330000003 | 156/156 | 0 | 0 |
| M2-mutated | 863330000004 | 132/156 | 1 | 1 |
| M2-restored | 863330000005 | 156/156 | 0 | 0 |
| M3-mutated | 863330000006 | 148/156 | 1 | 1 |
| M3-restored | 863330000007 | 156/156 | 0 | 0 |
| M4-mutated | 863330000008 | 152/156 | 1 | 1 |
| M4-restored | 863330000009 | 156/156 | 0 | 0 |
| M5-mutated | 863330000010 | 152/156 | 1 | 0 |
| M5-restored | 863330000011 | 156/156 | 0 | 0 |
| M6-mutated | 863330000012 | 156/156 | 0 | 1 |
| M6-restored | 863330000013 | 156/156 | 0 | 0 |
| M7-mutated | 863330000014 | 108/156 | 1 | 1 |
| M7-restored | 863330000015 | 156/156 | 0 | 0 |
| M8-mutated | 863330000016 | 132/156 | 1 | 1 |
| M8-restored | 863330000017 | 156/156 | 0 | 0 |

The pristine run and all eight restored runs use the exact landed gate hash. All nine print 156/156, and all nine receipts report `predicate_holds=true`. The other eight receipts carry mutant hashes, not the landed hash. No lower run on landed bytes occurred in this probe. Baseline and restoration success are conditions of the kill verdicts, not inferred from mutant failure.

## Before/after hashes and restoration

All eight copies started from the landed hash above. The mutator used surgical edits only in `S/M1/gate.sh` through `S/M8/gate.sh`. Each worker restored its gate by copying exact pristine bytes in `finally`, then reran both detectors. A final restoration also covered every copy. `A/M1.probe.json` through `A/M8.probe.json` record each restoration, and `A/results.json` records both byte equality and the complete phase results.

| Mutant | SHA-256 during mutation |
|---|---|
| M1 | `1f169fcf2b5c1985f46c67d93723c60419b5cb1907e3e2c041e9260c271ab766` |
| M2 | `774c90971edd82427e6e73d1a83d70cb712fdc412366927855057d7fd767c74d` |
| M3 | `b57da4e7d529f80ebfe5dc0bd7796a7c3140b41dd58d5203bce2b6f28a7521a4` |
| M4 | `8bb215c986f3a78c31b12ab9a94fe11fcc1a6420d69df2c8cbdc656edcd95c77` |
| M5 | `dbe05efadbc3913e707d7fe3b000ea4cdd32510d39364ca9c0433a4a3e0aee20` |
| M6 | `c729af699a0eb3138f783269b1bb9459b028a9a8d435cd92da5e2191275a57a1` |
| M7 | `b0da3f7d48beb48f7a5377a265fb001e31ac24a3867a435319142bc1ab9925ae` |
| M8 | `fb8598db1dfe26abfcb967351288edf7afac926994c91abda9636b3411bbe63e` |

**Before and after every mutant:** `94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e`; exact byte comparisons are true for all eight. The lane production gate's after hash remains that same landed hash; the frozen counter's after hash remains `cb354dd1b5bdf2540e2bf356d945e01cd3ce8207d66e7a1ec76f363650e6a514` (`A/results.json`, `final_restoration`, `lane_gate_sha256_after`, `counter_sha256_after`).

## Limits and containment

- Exactly eight mutants; findings are limited to this set and cases 242–248. No full selftest, base-revision comparison, D1–D5 battery, source review, or general malformed-JSON sweep was run by this seat.
- M1 is a broad nested-container rejection control; the per-case witness table instead uses the more selective M7/M8 for nested fields and M4 for nested string state.
- Fresh counter seeds change fixture bytes across phases; the frozen counter maintains the same fixed subvariant matrix on every seed (`C:31-40,82-101`). This is the same bounded detector, not an identical random fixture replay.
- There was no baseline failure and no inconclusive detector run. No gate timeouts or process signals occurred. Detector subprocesses were waited for; no background services were started.
- `df -h /fast` was checked before copying: 179 GiB available. Commands cap processes/address space and detector file writes at 900000 bytes. Saved gate copies were size-bounded below that cap before preservation (`A/probe.py`).
- No network, installs, git/jj write commands, production edits, contract edits, counter edits, or sibling-source changes. Tool installs/updates: none.
