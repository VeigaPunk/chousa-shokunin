# W2ExecHead

Seat: executor. Milestone: Round 44 wave 2 — genuine seats after the usage-error wave.
Axes named: operability (the 36-file set is `git status` porcelain, and the contain check is a case-sensitive fixed substring of each basename stem), calibration (containment is not an H1 check, and tracked readmes are not in the 36), depth (every file's first containing line is quoted; the four non-H1 hits are quoted from the files).

This seat did not edit lane production files, did not commit, and did not fetch.

## Count

**36**

## Failures

**none**

No untracked round-40 or round-41 markdown file lacked its filename stem. There is no failure name to list.

## Predicate

Population: `git status --porcelain --untracked-files=all` lines that start with `?? `, end in `.md`, and contain `/round-40/` or `/round-41/`. Path is `line[3:]` (status `??` plus the porcelain space). Stem is the basename with the `.md` suffix removed. A hit is a case-sensitive substring of the file's UTF-8 text (`stem in text`). That is the asked check. An H1 that does not start with the stem is not a failure under this predicate.

## Command

```
python3 - << 'PY'
import subprocess
from pathlib import Path
root = Path("/home/vgpnk/Projects/shokunin/chousa-shokunin")
raw = subprocess.check_output(["git","-C",str(root),"status","--porcelain","--untracked-files=all"], text=True)
files = []
for line in raw.splitlines():
    if not line.startswith("?? "):
        continue
    path = line[3:]
    if path.endswith(".md") and ("/round-40/" in path or "/round-41/" in path):
        files.append(path)
print(f"POPULATION={len(files)}")
hits = []
misses = []
non_h1 = []
for rel in files:
    text = (root/rel).read_text(encoding="utf-8")
    stem = Path(rel).stem
    if stem not in text:
        misses.append(rel)
        print(f"FAILURE\t{rel}")
        continue
    hits.append(rel)
    first_line_no = None
    first_line = None
    for i, line in enumerate(text.splitlines(), 1):
        if stem in line:
            first_line_no = i
            first_line = line
            break
    h1 = text.splitlines()[0] if text.splitlines() else ""
    h1_ok = h1.startswith("# " + stem)
    flag = "H1" if h1_ok else "NOT_H1"
    if not h1_ok:
        non_h1.append(rel)
    print(f"HIT\t{flag}\t{rel}\tL{first_line_no}:{first_line}")
print(f"STEM_HITS={len(hits)}")
print(f"STEM_MISSES={len(misses)}")
print(f"NOT_H1={len(non_h1)}")
print("FAILURES=" + (",".join(misses) if misses else "none"))
PY
```

An earlier run of the same population rule and the same `stem in text` test printed `COUNT_UNTRACKED=36`, `STEM_HITS=36`, `STEM_MISSES=0`, and no `FAILURE` line.

## Command output (verbatim)

```
POPULATION=36
HIT	H1	.ufo/waves/round-40/w1/ConnectorSiblingScan.md	L1:# ConnectorSiblingScan — sibling-overlap for receipt provenance, source curation, and calibration
HIT	H1	.ufo/waves/round-40/w1/CriticC1Control.md	L1:# CriticC1Control — do-nothing replay of the frozen C1 counter
HIT	NOT_H1	.ufo/waves/round-40/w1/CriticC1Predicate.md	L3:**Seat:** CriticC1Predicate (leaf). **Scope:** attack the frozen P1 predicate — can the
HIT	H1	.ufo/waves/round-40/w1/CriticC1Scope.md	L1:# CriticC1Scope — C1 frozen-claim text vs verifier/counter proof scope
HIT	H1	.ufo/waves/round-40/w1/CriticC2Calibration.md	L1:# CriticC2Calibration — attack on the C2 disposition claim (round 40, w1)
HIT	H1	.ufo/waves/round-40/w1/CriticR4Disposition.md	L1:# CriticR4Disposition — adversarial audit of the R4 `not-reproduced` disposition
HIT	H1	.ufo/waves/round-40/w1/CriticSourceClaim.md	L1:# CriticSourceClaim — attack on the sourced-claim binding (S059)
HIT	H1	.ufo/waves/round-40/w1/ExecC1BaseReceipt.md	L1:# ExecC1BaseReceipt — regenerated c1-base-s39001 receipt vs the base-gate-r39 control
HIT	NOT_H1	.ufo/waves/round-40/w1/ExecC1Count.md	L3:**Seat:** ExecC1Count (leaf). **Attack (verbatim):** "Run the frozen round-40 c1-count.py
HIT	H1	.ufo/waves/round-40/w1/ExecC1LandedReceipt.md	L1:# ExecC1LandedReceipt — round 40, wave 1
HIT	H1	.ufo/waves/round-40/w1/ExecC1MutantReceipt.md	L1:# ExecC1MutantReceipt — regenerated c1-mutenv-s39013 receipt vs the committed PATH-env mutant control
HIT	H1	.ufo/waves/round-40/w1/ExecC2Count.md	L1:# ExecC2Count — frozen round-40 `c2-count.py` on the committed tree
HIT	H1	.ufo/waves/round-40/w1/ExecNoHarm.md	L1:# ExecNoHarm — round-40 no-harm regression battery
HIT	NOT_H1	.ufo/waves/round-40/w1/MutateExpectDigest.md	L3:Seat: `MutateExpectDigest` (leaf). Assigned attack: on a temporary copy only, alter one active
HIT	H1	.ufo/waves/round-40/w1/MutateGateDigest.md	L1:# MutateGateDigest — R1 receipt-integrity predicate, gate-digest mutant
HIT	H1	.ufo/waves/round-40/w1/MutateVerifierSubject.md	L1:# MutateVerifierSubject — round-40 c2 receipt field mutations (`verifier_sha256`, `subject_counter_sha256`)
HIT	H1	.ufo/waves/round-40/w1/RevengerR1History.md	L1:# RevengerR1History — round 40, w1: r39 R1 receipt-integrity chain reconstruction
HIT	H1	.ufo/waves/round-40/w1/RevengerR2R5History.md	L1:# RevengerR2R5History — R2–R5 reconstruction and classification (round 40, w1)
HIT	NOT_H1	.ufo/waves/round-40/w1/ReviewActivePopulation.md	L3:**Seat:** ReviewActivePopulation (leaf L2, no dispatch). **Lane:** chousa. **Round:** 40, attempt 1.
HIT	H1	.ufo/waves/round-40/w1/ReviewC2Bindings.md	L1:# ReviewC2Bindings — round 40 / w1 (leaf L2, no dispatch)
HIT	H1	.ufo/waves/round-40/w1/ReviewR2CommitTruth.md	L1:# ReviewR2CommitTruth — R2 audited from committed bytes
HIT	H1	.ufo/waves/round-40/w1/ReviewR3Counts.md	L1:# ReviewR3Counts — R3 knowledge-count re-derivation (round 40, w1)
HIT	H1	.ufo/waves/round-40/w1/ReviewR4RoleMix.md	L1:# ReviewR4RoleMix — independent r39 role count; does routed R4 reproduce from committed bytes?
HIT	H1	.ufo/waves/round-40/w1/ReviewReplacementBindings.md	L1:# ReviewReplacementBindings — three round-40 c1 replacement receipts vs committed bindings
HIT	H1	.ufo/waves/round-40/w1/ScoutFrontierOverlap.md	L1:# ScoutFrontierOverlap — does the r40 expectation-digest note name distinct ground?
HIT	H1	.ufo/waves/round-40/w1/ScoutHashSource.md	L1:# ScoutHashSource — round 40, wave 1 (scout)
HIT	H1	.ufo/waves/round-40/w1/ScoutProvinceBoundary.md	L1:# ScoutProvinceBoundary — chousa round 40, wave 1
HIT	H1	.ufo/waves/round-40/w1/ScribeClaimSurfaces.md	L1:# ScribeClaimSurfaces — round-40 claim-surface cross-read
HIT	H1	.ufo/waves/round-40/w1/ScribeKnowledgeEntry.md	L1:# ScribeKnowledgeEntry — r40 knowledge-entry audit
HIT	H1	.ufo/waves/round-40/w1/ScribeLessonGate.md	L1:# ScribeLessonGate — round 40, wave 1 (scribe)
HIT	H1	.ufo/waves/round-40/w1/SentinelFetchScope.md	L1:# SentinelFetchScope — round 40, wave 1 (sentinel)
HIT	H1	.ufo/waves/round-40/w1/SentinelWriteScope.md	L1:# SentinelWriteScope — round 40, write-surface audit
HIT	H1	.ufo/waves/round-40/w1/SimplifierAudit.md	L1:# SimplifierAudit — round-40 counting scripts and active manifest
HIT	H1	.ufo/waves/round-41/w1/ConnectorSiblingScan.md	L1:# ConnectorSiblingScan — round 41
HIT	H1	.ufo/waves/round-41/w1/ExecC2Before.md	L1:# ExecC2Before — C2 before-state replication (round 41, wave 1)
HIT	H1	.ufo/waves/round-41/w1/MutateC2Join.md	L1:# MutateC2Join — C2 counter input-injection mutation probe (round 41, w1)
STEM_HITS=36
STEM_MISSES=0
NOT_H1=4
FAILURES=none
```

Split of that ledger: 33 paths under `.ufo/waves/round-40/w1/`, 3 under `.ufo/waves/round-41/w1/`. Unique stems: 35. `ConnectorSiblingScan` is the stem of two files (round 40 and round 41). Both contain it. That duplicate stem is not a failure.

## Not failures: four files whose H1 is not the stem

These four still contain the stem. They are hits. Quoted from the files:

`.ufo/waves/round-40/w1/CriticC1Predicate.md`

```
# Critic attack — C1 receipt-integrity predicate (round 40, w1)

**Seat:** CriticC1Predicate (leaf). **Scope:** attack the frozen P1 predicate — can the
```

`.ufo/waves/round-40/w1/ExecC1Count.md`

```
# Executor confirmation — frozen round-40 C1 counter (round 40, w1)

**Seat:** ExecC1Count (leaf). **Attack (verbatim):** "Run the frozen round-40 c1-count.py
```

`.ufo/waves/round-40/w1/MutateExpectDigest.md`

```
# Mutation probe — active receipt `expect_sha256` (round 40, w1)

Seat: `MutateExpectDigest` (leaf). Assigned attack: on a temporary copy only, alter one active
```

`.ufo/waves/round-40/w1/ReviewActivePopulation.md`

```
# Review — active r39 receipt population (round 40, w1)

**Seat:** ReviewActivePopulation (leaf L2, no dispatch). **Lane:** chousa. **Round:** 40, attempt 1.
```

A heading-only recount would be 32, not 36. That recount was not the asked check.

## Outside the 36 (not scored)

`git ls-files` lists these tracked markdown files. They are not untracked, so they are not in the population:

```
.ufo/waves/round-40/DISPATCH-README.md
.ufo/waves/round-41/DISPATCH-README.md
```

A fixed-string search for `DISPATCH-README` in each returned no matches. Their H1 lines are `# Round 40 — prepared wave handoff` and `# Round 41 — prepared wave handoff`. That absence is not a failure of this count. A disk walk is 34 markdown files under `.ufo/waves/round-40` and 4 under `.ufo/waves/round-41` (38). The asked set is the 36 untracked ones, not those 38.

Other untracked markdown files existed and were excluded because their paths are not round-40 or round-41:

```
?? .ufo/waves/round-44/assimilation/guard/indented-registry.md
?? .ufo/waves/round-44/assimilation/guard/staged.md
```

`git status --porcelain -uall -- .ufo/waves/round-40 .ufo/waves/round-41 | wc -l` printed `38` because that directory status also includes two modified `swarm-registry.json` files (` M .ufo/waves/round-40/w1/swarm-registry.json` and ` M .ufo/waves/round-41/w1/swarm-registry.json`). Those JSON lines are not part of the markdown count.

## What this count does not say

36/36 does not mean every prepared round-40 or round-41 seat wrote a report. A spec-item to filename join was not run. An unrun check has not passed.

No case-insensitive pass and no separate word-boundary pass were run. The quoted first lines already show the stem as its own token (H1 start, seat label, or backticks). That observation is not a second scored check.

## Files changed

Only `.ufo/waves/round-44/w2/W2ExecHead.md`.

## Blockers

None.

Report: .ufo/waves/round-44/w2/W2ExecHead.md
