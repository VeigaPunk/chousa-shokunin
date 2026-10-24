# RevReceiptAudit — round-37 counter receipts (C1/C2)

Seat: `chousa-r37.RevReceiptAudit`. Lane tip audited: `b905217a7dfdcf58be1f0a4c0bf5f2d2d32a2d65`
(`git rev-parse master` == `git rev-parse HEAD`). Frozen design:
`corpus/evidence/round37/claims.md` (committed at b905217).

Axes: provenance (which bytes/gate produced each number), consistency (matched/total/
`predicate_holds`/predicate string vs P1/P2), reproducibility (do the counters still emit
these exact receipts), and claim-condition (fresh seeds, base failing sets, kill rule).

No `lsp` device is exposed in this seat (tool set: read/bash/edit/eval/glob/grep/wait/write);
therefore semantic proof below is executable re-derivation (byte-diff of regenerated
receipts), not grep inference. Text search was used only for discovery.

## Scope measured

Globbed `corpus/evidence/round37/receipts/*.json` (10 files) plus
`.ufo/waves/round-37/w1/ExecC1BaseRederive/*.json` and
`.ufo/waves/round-37/w1/ExecC2BaseRederive/*.json` (4 files) = 14 receipts.
The assignment's list names `c2-after-s57961`, which does not exist; the actual file is
`c2-after-s37961` (`ls`, below). The assignment also omits the existing
`c2-after-s37721.json`; it was audited. All 14 actual receipts are covered.

Baseline gate: `.ufo/waves/round-37/controls/base-gate-r37.sh`
`a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8` — independently
confirmed byte-identical to `git show bb13ee9…:tools/research-gate.sh` (the base tip gate
named in claims.md:12-14), and identical to the committed blob at HEAD.
Landed gate: `tools/research-gate.sh`
`9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39` — working tree and
`git show HEAD:tools/research-gate.sh` both hash to this value.

## Per-receipt table

`gate` = hash recorded in the receipt, re-derived from the recorded `gate` path (all matched
exactly; every value is in {a7d3922c…, 9fcac047…}). `R` = byte-identical regeneration
performed by this seat; `R*` = not re-run but proven identical to a re-run receipt modulo the
`seed` field (all receipts of a claim are identical except `seed`, checked below).
`git` = status at b905217: `T` tracked/committed, `U` untracked working-tree file.

| # | Receipt | Claim / seed | gate | matched/total | holds | Failing cells | git | R |
|---|---|---|---|---|---|---|---|---|
| 1 | `receipts/c1-base-s37001.json` | C1 / 37001 | a7d3922c768a | 2/7 | false | sha-shim-forge, cut-shim-forge, sha-shim-other, sha-shim-broken, cut-shim-broken | T | R |
| 2 | `receipts/c1-after-s37001.json` | C1 / 37001 | 9fcac047ddad | 7/7 | true | — | T | R* |
| 3 | `receipts/c1-after-s37701.json` | C1 / 37701 | 9fcac047ddad | 7/7 | true | — | U | R* |
| 4 | `receipts/c1-after-s37901.json` | C1 / 37901 | 9fcac047ddad | 7/7 | true | — | U | R* |
| 5 | `receipts/c1-after-s37921.json` | C1 / 37921 | 9fcac047ddad | 7/7 | true | — | U | R |
| 6 | `receipts/c2-base-s37021.json` | C2 / 37021 | a7d3922c768a | 3/7 | false | env-echo-pin, env-echo-drift, env-fn-echo-pin, env-root-pin | T | R |
| 7 | `receipts/c2-after-s37021.json` | C2 / 37021 | 9fcac047ddad | 7/7 | true | — | T | R* |
| 8 | `receipts/c2-after-s37721.json` | C2 / 37721 | 9fcac047ddad | 7/7 | true | — | U | R* |
| 9 | `receipts/c2-after-s37941.json` | C2 / 37941 | 9fcac047ddad | 7/7 | true | — | U | R |
| 10 | `receipts/c2-after-s37961.json` | C2 / 37961 | 9fcac047ddad | 7/7 | true | — | U | R* |
| 11 | `w1/ExecC1BaseRederive/c1-base-s37101.json` | C1 / 37101 | a7d3922c768a | 2/7 | false | same five shim cells | U | R |
| 12 | `w1/ExecC1BaseRederive/c1-base-s37123.json` | C1 / 37123 | a7d3922c768a | 2/7 | false | same five shim cells | U | R* |
| 13 | `w1/ExecC2BaseRederive/c2-base-s37201.json` | C2 / 37201 | a7d3922c768a | 3/7 | false | same four env cells | U | R |
| 14 | `w1/ExecC2BaseRederive/c2-base-s37223.json` | C2 / 37223 | a7d3922c768a | 3/7 | false | same four env cells | U | R* |

Mechanical invariants, all 14 receipts: `matched == count(ok scenarios)`; `total == 7`;
`predicate_holds == (matched == total)`; `predicate` is exactly `CLAIM_PIN_PROVENANCE_MATCH=7/7`
(C1) or `PIN_CAPTURE_ENV_MATCH=7/7` (C2); no extra top-level keys; each file is byte-exact
canonical output of `json.dump(..., indent=2, sort_keys=True)` + trailing newline
(`c1-count.py:170-178`, `c2-count.py:172-180`), i.e. no post-hoc hand edit is detectable.

Seeds: C1 after = 37001, 37701, 37901, 37921 (distinct); C2 after = 37021, 37721, 37941,
37961 (distinct); wave base = 37101/37123 and 37201/37223 (distinct). No after receipt is
below 7/7; 7/7 appears 8 times, 2/7 twice (C1 base), 3/7 twice (C2 base).

## Cross-check against claims.md

- C1 base failing set is exactly the five shim cells described at claims.md:49-53: forge
  shims make the tampered source read `CLEAN/supported` (observed rc=0); wrong-digest
  (`sha-shim-other`) and broken (`sha-shim-broken`, `cut-shim-broken`) shims make the intact
  source read `DRIFT/stale` (observed rc=1). The two holds pass. 2/7 as frozen.
- C2 base failing set is exactly the four separation cells at claims.md:87-93, with the
  stated symptoms: `env-echo-pin` baseline_echo_lines=1 and drift `GATE_DRIFT: -GATE_GREP`;
  `env-echo-drift` drift `GATE_DRIFT: +GATE_GREP`; `env-fn-echo-pin` echo=1 and
  `-GATE_GREP`; `env-root-pin` drift is the foreign-root token list instead of `none`.
  `hold-plain`, `hold-benign`, `env-strict-pin` pass (the "three holds" of claims.md:88-89).
  3/7 as frozen.
- After receipts: every scenario expects the fixed behaviour from the frozen counter tables
  (`c1-count.py:41-50`, `c2-count.py:44-62`) and observes it (`ok=true` throughout); the
  landed `GATE_PIN:` lines carry `gate_sha256=9fcac047…` (e.g. `c2-after-s37941.json`).

## Report ↔ receipt cross-check

- `w1/ExecC1BaseRederive.md`: all 7 quoted lines for seed 37101 and 37123 reproduce exactly
  from the corresponding receipts with the counter's printf format (0 missing of 14).
- `w1/ExecC2BaseRederive.md`: all four expected/observed tuples quoted for each seed match
  the receipt fields verbatim (16/16 checks), including `GATE_DRIFT: +GATE_GREP` and the
  `env-root-pin` token list.
- `w1/ExecC1LandedRederive.md`: its two quoted PASS blocks equal the 7 PASS lines derivable
  from any landed C1 receipt, and contain none of the base FAIL lines. Seed labels 37111/37133
  are unverifiable — see finding M2.
- `w1/ExecC2LandedRederive.md`: quoted receipt-field tuples match the landed receipt pattern
  (`7,7,"PIN_CAPTURE_ENV_MATCH=7/7",true`, gate `9fcac047…`). Seed labels 37211/37311
  unverifiable — see M2.
- Wave reports' independent `sha256sum` outputs (base `a7d3922c…`, landed `9fcac047…`) match
  this seat's independent hashes.

## Findings (by severity)

**M1 (Medium) — the fresh-seed after receipts required by P1/P2 are not committed.**
At `b905217`, `git status` shows the six post-freeze after receipts
(`c1-after-s37701/37901/37921`, `c2-after-s37721/37941/37961`) and all four wave base
receipts as untracked (`??`), as are all wave reports. Only the four pre-freeze construction
receipts (`c1-base-s37001`, `c1-after-s37001`, `c2-base-s37021`, `c2-after-s37021`) are in
HEAD (commit stat of b905217 lists exactly those four receipt paths; claims.md:6-8 discloses
37001/37021 as pre-freeze). Consequently the committed evidence alone exhibits landed-gate
7/7 only on the construction seeds, while P1/P2 (claims.md:33-41, 72-80) require "two fresh
seeds". The numbers are not in doubt — every fresh-seed receipt reproduces byte-identically
(§Commands) — but the freeze commit does not yet carry them. Landing condition: the closure
commit must add the six after receipts (and the wave evidence) unchanged.

**M2 (Medium) — two seeds per claim cited as verified have no persisted receipt.**
`corpus/knowledge/claim-pin-provenance-r37.md:16` claims 7/7 on 37001, 37111, 37133, 37701,
37901, 37921 and `pin-capture-env-r37.md:16` on 37021, 37211, 37311, 37721, 37941, 37961;
the same seeds appear in `corpus/lessons/round-37.md:13,18` and `LOG.md:1379,1383`. Receipts
exist for only four seeds per claim; 37111/37133 and 37211/37311 live only in the
`ExecC1LandedRederive.md`/`ExecC2LandedRederive.md` reports' quoted `/tmp` paths, and those
tmp dirs are gone (`ls` exit 2, §Commands). Those report assertions cannot be verified from
persisted evidence. Fix before committing the docs: persist the receipts or drop those two
seeds from the verified-at lists.

**L1 (Low) — two pending doc sentences are literally false over the committed receipt set.**
`corpus/knowledge/claim-pin-provenance-r37.md:35-36` and
`corpus/knowledge/pin-capture-env-r37.md:39-40` say the landed gate "scores 7/7 on every
committed receipt"; the committed set includes `c1-base-s37001.json` (2/7) and
`c2-base-s37021.json` (3/7) on the base gate. Likewise `LOG.md:1380` "every receipt
`gate_sha256=9fcac047…321cf39`" is false for both base receipts (a7d3922c…). They are
untracked/modified at review time, so the L1 can qualify them ("every landed-gate receipt")
before the closure commit.

**L2 (Low) — seed labels are not authenticated by receipt content; C2's seed is inert.**
`c2-count.py` never passes `--seed` to a scenario (`run_scenario` takes no seed; `SCENARIOS`
is static), so every C2 receipt is identical except the `seed` field. C1 varies fixture bytes
via `random.Random("%s-%s" % (seed, sid))` (`c1-count.py:85-87`) but the receipt records no
fixture identity, so all four C1 after receipts are also identical except `seed`. Distinct
seeds are therefore verified as distinct labels, not as independently reproducible fixtures;
P2's "two fresh seeds" adds no fixture variation. This does not falsify P1/P2 — C1's fixture
genuinely varies with seed and the base-vs-landed 2/7→7/7 (and 3/7→7/7) separation carries the
measurement — but the reports/docs should not imply six independent fixtures.

**I1 (Info) — assignment list vs artifacts.** `c2-after-s57961.json` does not exist;
`c2-after-s37961.json` does. `c2-after-s37721.json` exists and was audited.

**I2 (Info) — land-seat receipts were not persisted.** Both landed re-derive seats wrote their
receipts to `/tmp` instead of the requested `w1/ExecC*LandedRederive/` directories
(their own Limits sections state this), so the wave persisted only base-gate receipts.

**I3 (Info) — kill-rule scan is clean.** A structural scan of every JSON in the lane found
exactly 8 landed-gate receipts, all `matched=7, total=7`; no detached or committed landed-gate
run below 7/7 exists. The sub-7 numbers in wave evidence are not kill-rule hits:
`ExecMutC1Counter.md` 6/7 uses mutant *counter* copies against the landed gate, and
`ExecMutGateC1.md` 2/7 / `ExecMutGateC2.md` 3/7 use scratch mutant *gates*
(`e4fc40a2…` / unrecorded scratch bytes). The frozen counter against the landed gate has only
7/7 outputs.

## Residual risk

- Receipts carry no runtime metadata (python/bash versions, PATH, host); reproduction was done
  on this host's current runtime only. All regenerated receipts are byte-identical today.
- The gate bytes could in principle have differed at run time from the committed bytes; the
  receipts pin the gate hash and the current bytes hash to the pinned values, so the residual
  window is "changed and changed back", which no receipt can exclude (same limit as any
  self-reported run).
- Untracked docs/receipts can still change before the L1 commits; this audit binds only the
  files as read (mtimes: 20:08:29 construction pair, 20:21:38-20:22:03 post-freeze after
  receipts, 20:22:08-20:22:24 wave base receipts, 23:29:19-23:29:29 s37701/s37721 closure).

## Verification gaps

- Landed re-derive receipts for seeds 37111/37133/37211/37311 are unrecoverable (M2).
- No semantic re-audit of the gate hunks themselves (other seats: separability/mutation); this
  audit only establishes that the receipts are faithful, reproducible counter output on the
  bytes they pin.
- `resume_continuity_v1` is not applicable: round-37 chousa evidence has no UFO resume path;
  the attempt-1/attempt-4 death history (lessons) is narrative, not a preflight/mutation path.

## Verdict

**No receipt-level mismatch.** All 14 receipts pin a gate in the allowed set by re-derived
hash, all `matched`/`total`/`predicate_holds`/predicate strings are internally consistent and
match frozen P1/P2, the base receipts are exactly 2/7 (five shim cells) and 3/7 (four
env-separation cells) as frozen, every after receipt is 7/7, after seeds are distinct per
claim, and all reports' quoted outputs match the receipts; every receipt regenerates
byte-for-byte from the current counters and gate bytes (6 direct reproductions: both
committed base receipts, both wave base seeds 37101/37201, and one after receipt per claim;
the rest proven identical modulo seed). **Recommendation: accept the numbers; make the closure commit carry
the six post-freeze after receipts and the wave base receipts, and fix M2/L1 in the pending
docs before they are committed.** No evidence here admits the claim; the verdict is a
recommendation only.

## Commands and observed output (verbatim; exit codes as observed)

1) `git -C … rev-parse HEAD && ls -la corpus/evidence/round37/receipts/ && ls -la .ufo/waves/round-37/w1/`
Exit 0. Output: `b905217a7dfdcf58be1f0a4c0bf5f2d2d32a2d65`; 10 receipts (listed; 2937-5320
bytes; mtimes 20:08-23:29); w1 contains `ExecC1BaseRederive/`, `ExecC2BaseRederive/`, eight
`.md` reports, `swarm-registry.json`.

2) `sha256sum tools/research-gate.sh .ufo/waves/round-37/controls/base-gate-r37.sh`
Exit 0:
```
9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39  tools/research-gate.sh
a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8  .ufo/waves/round-37/controls/base-gate-r37.sh
```
(jq summary of all 14 receipts used in the same call; truncated lines recovered by later calls.)

3) Mechanical audit (python): for each of the 14 receipts, recompute `sha256` of the recorded
`gate` path, compare with `gate_sha256`, count `ok` scenarios, compare `matched`/`total`/
`predicate_holds`. Exit 0. Output: every line `hash_match=True in_set=True`;
`consistency matched==ok:True total==sc:True holds==(matched==total):True`; `extra_keys=[]`;
the seeds/ids/gates of the table above.

4) `git log --oneline -12 -- corpus/evidence/round37/receipts corpus/evidence/round37/c1-count.py corpus/evidence/round37/c2-count.py && git status --short corpus/evidence/round37 .ufo/waves/round-37/w1 && git show bb13ee9…:tools/research-gate.sh | sha256sum`
Exit 0. Output: history is the single freeze commit b905217; status lists the six after
receipts and `w1/` as `??`; base-tip gate hashes to `a7d3922c…`.

5) Canonical-serialization check (python): re-serialize each receipt with
`json.dumps(d, indent=2, sort_keys=True)+"\n"` and byte-compare. Exit 0. Output: `OK` for all
14 receipts, `noncanonical: []`; `git show HEAD:tools/research-gate.sh | sha256sum` →
`9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39`.

6) `git check-ignore -v …; echo "rc=$?"; git ls-files corpus/evidence/round37/receipts .ufo/waves/round-37 | cat`
Exit 0. `rc=1` (nothing ignored). `git ls-files` output — the only tracked entries:
```
.ufo/waves/round-37/controls/base-gate-r37.sh
corpus/evidence/round37/receipts/c1-after-s37001.json
corpus/evidence/round37/receipts/c1-base-s37001.json
corpus/evidence/round37/receipts/c2-after-s37021.json
corpus/evidence/round37/receipts/c2-base-s37021.json
```

7) Counter receipt writers: `grep -n "receipt\|json.dump\|predicate_holds\|print(f\|total" c1-count.py / c2-count.py`; exit 0. Confirms receipt keys, `holds = matched == total`, `json.dump(indent=2, sort_keys=True)` + `"\n"`.

8) Reproduction (landed), exact command:
```
C1_TMP=/tmp/rra-c1-land python3 corpus/evidence/round37/c1-count.py --gate tools/research-gate.sh --seed 37921 --receipt /tmp/rra-c1-land/repro-37921.json
C2_TMP=/tmp/rra-c2-land python3 corpus/evidence/round37/c2-count.py --gate tools/research-gate.sh --seed 37941 --receipt /tmp/rra-c2-land/repro-37941.json
diff <(cat /tmp/rra-c1-land/repro-37921.json) corpus/evidence/round37/receipts/c1-after-s37921.json
diff <(cat /tmp/rra-c2-land/repro-37941.json) corpus/evidence/round37/receipts/c2-after-s37941.json
```
Observed: `C1_LAND_RC=0` (`CLAIM_PIN_PROVENANCE_MATCH=7/7`), `C2_LAND_RC=0`
(`PIN_CAPTURE_ENV_MATCH=7/7`), `C1_REPRO_IDENTICAL`, `C2_REPRO_IDENTICAL`; call exit 0.

9) Reproduction (base + wave), exact commands:
```
C1_TMP=/tmp/rra-c1-base python3 …/c1-count.py --gate .ufo/waves/round-37/controls/base-gate-r37.sh --seed 37001 --receipt /tmp/rra-c1-base/repro-37001.json
C2_TMP=/tmp/rra-c2-base python3 …/c2-count.py --gate .ufo/waves/round-37/controls/base-gate-r37.sh --seed 37021 --receipt /tmp/rra-c2-base/repro-37021.json
C1_TMP=/tmp/rra-w1 python3 …/c1-count.py --gate .ufo/waves/round-37/controls/base-gate-r37.sh --seed 37101 --receipt /tmp/rra-w1/c1-base-s37101.json
C2_TMP=/tmp/rra-w1 python3 …/c2-count.py --gate .ufo/waves/round-37/controls/base-gate-r37.sh --seed 37201 --receipt /tmp/rra-w1/c2-base-s37201.json
```
Observed: `C1_BASE_RC=1` / `CLAIM_PIN_PROVENANCE_MATCH=2/7`; `C2_BASE_RC=1` /
`PIN_CAPTURE_ENV_MATCH=3/7`; `C1_BASE_IDENTICAL`; `C2_BASE_IDENTICAL`; wave `RC=1`/`RC=1`,
`W1_C1_IDENTICAL`, `W1_C2_IDENTICAL`; call exit 0.

10) After-receipt comparison modulo seed (python): drop `seed`, serialize, compare. Exit 0.
Output: all four C1 after receipts identical to `c1-after-s37001` except `seed: True`; same
for all four C2 after receipts vs `c2-after-s37021`.

11) Report cross-check (python): rebuild the counter's printf lines from each C1 base receipt
and search the base report; extract the C2 report's tuple strings and compare to receipt
fields. Exit 0. Output: C1 base seeds 37101/37123 `lines_in_report 7 / 7 missing: []`;
landed-pattern receipt `7 / 7 missing: []` (base FAIL lines correctly absent: `2 / 7`);
C2 tuples `expected_tuple_in_report True / observed_tuple_in_report True` for all 4 failing
cells × both seeds.

12) `git log -1 --format='freeze_commit=%H%ncommitted=%ci' b905217; grep -n "sha256sum" tools/research-gate.sh; grep -n "sha256sum <" base-gate-r37.sh`
Exit 0. Freeze commit time `2026-10-23 20:10:24 -0300`. Landed gate claim-pin call region at
`:2011-2013` (pinned absolute); base gate still has the PATH form at `:2002`
(`sha_actual=$(sha256sum < "$path" 2>/dev/null | cut -d' ' -f1 || true)`).

13) `stat -c '%y %n' receipts/*.json w1/ExecC1BaseRederive/*.json w1/ExecC2BaseRederive/*.json | sort`
Exit 0. Output listed in §Residual risk (construction 20:08:29; s37901/37921 20:21:38;
s37941 20:21:52; s37961 20:22:03; wave base 20:22:08-20:22:24; s37701/s37721 23:29).

14) `ls -la /tmp/chousa-r37-c1-37111.YZXpiA /tmp/chousa-r37-c1-37133.pnRH8Y /tmp/chousa-r37-c2-37211.9DTG9I /tmp/chousa-r37-c2-37311.KB8ewM`
Exit 2:
```
ls: cannot access '/tmp/chousa-r37-c1-37111.YZXpiA': No such file or directory
ls: cannot access '/tmp/chousa-r37-c1-37133.pnRH8Y': No such file or directory
ls: cannot access '/tmp/chousa-r37-c2-37211.9DTG9I': No such file or directory
ls: cannot access '/tmp/chousa-r37-c2-37311.KB8ewM': No such file or directory
```

15) `git rev-parse master HEAD; git log --oneline -3 master; git status --short; git cat-file -e HEAD:corpus/knowledge/claim-pin-provenance-r37.md; git diff --cached --stat`
Exit 0. `master == HEAD == b905217…`; status shows `M LOG.md SCORECARD.md corpus/QUALITY.md
corpus/README.md corpus/SOURCES.md`, `??` for the six after receipts, `corpus/knowledge/*.md`,
`corpus/lessons/round-37.md` and the `.ufo/waves/round-37/*` evidence; `cat-file` reports the
knowledge path "exists on disk, but not in 'HEAD'" (i.e. untracked); no staged diff.

16) Lane-wide landed-gate receipt scan (python over `**/*.json`): 8 receipts with
`gate_sha256=9fcac047…`, all `matched=7,total=7,seed∈{37001,37701,37901,37921,37021,37721,37941,37961}`;
`below7: []`; exit 0.

17) `git show HEAD:.ufo/waves/round-37/controls/base-gate-r37.sh | sha256sum; git diff --name-only -- corpus/evidence/round37/receipts`
Exit 0: `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8  -`; no committed
receipt has working-tree modifications.

18) `git diff --stat; git diff LOG.md | grep …; git diff SCORECARD.md | grep …` Exit 0: the
round-37 LOG/SCORECARD entries are uncommitted additions (5 modified files, 105 insertions);
the quoted counts/sentences in M2/L1 are in that uncommitted diff.

19) Reads (no exit codes): `claims.md` (full), both counters (`c1-count.py:59-183`,
`c2-count.py:1-185`), `ExecC1BaseRederive.md`, `ExecC2BaseRederive.md`,
`ExecC1LandedRederive.md`, `ExecC2LandedRederive.md`, `ExecMutC1Counter.md`,
`ExecMutGateC1.md`, `ExecMutGateC2.md`, knowledge entries, `corpus/lessons/round-37.md`
head, and `jq` scenario dumps of both base receipts and `c1-after-s37921`/`c2-after-s37941`.

Tools installed or updated during this audit: none. No network used. Writes: this report plus
scratch under `/tmp/rra-*` only.
