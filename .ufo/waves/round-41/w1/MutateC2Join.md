# MutateC2Join — C2 counter input-injection mutation probe (round 41, w1)

Role: mutation-tester (leaf). Assigned attack: exercise `corpus/evidence/round41/c2-count.py`
with (A) a census stub emitting a W04 for `S999`, which has no TSV row, and (B) a TSV whose
evidence names a missing path. Both must fail the counter. No production edits, no network.

## Subject identity (frozen bytes)

Lane HEAD `872bf3a3507875b382313f955d15960f9638256f`; worktree == HEAD for both C2 artifacts.

| artifact | git blob at HEAD | sha256 |
|---|---|---|
| `corpus/evidence/round41/c2-count.py` | `86a112d1ab7ab1c0380e4724c90802f938ec965f` | `66bb31af0d199443c9a9c6f8bd9cf733f92e883306770ee7831559a34f4ccaa3` |
| `corpus/evidence/round41/w04-dispositions.tsv` | `88be5ef34c33a31ed7ced27c3fabab196db465c5` | `2558bba41e54ae9f3c4fc48c89c95bbcf7c24acdbe6a592dcb72c41ff2dee7ca` |
| census `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` | (fleet repo, clean) | `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30` |

The census is the **installed/committed** fleet script; `validate` was invoked exactly as the
counter invokes it and writes to stdout only (`--out` unset). No egress.

## Harness (only the pointer plumbing differs; join logic byte-identical)

Scratch root `/tmp/mutatec2join.AcXlvm` (outside the lane; nothing in the lane was written).
Probe copy at `$S/lane/corpus/evidence/round41/c2-count.py` changes exactly three pointer
expressions, so a stub/TSV can be fed without touching the lane:

```diff
-LANE = Path(__file__).resolve().parents[3]
-CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"
-TSV = LANE / "corpus" / "evidence" / "round41" / "w04-dispositions.tsv"
+import os
+LANE = Path(os.environ.get("PROBE_LANE", str(Path(__file__).resolve().parents[3])))
+CENSUS = os.environ.get("PROBE_CENSUS", "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh")
+TSV = Path(os.environ.get("PROBE_TSV", str(LANE / "corpus" / "evidence" / "round41" / "w04-dispositions.tsv")))
```

Detector, identical in every cell of the matrix (pristine, mutant, restored):

```
PROBE_LANE=<lane> PROBE_CENSUS=<census-or-stub> PROBE_TSV=<tsv> \
  python3 /tmp/mutatec2join.AcXlvm/lane/corpus/evidence/round41/c2-count.py
```

Baseline parity is a precondition for reading any kill:

| run | output | exit |
|---|---|---|
| committed subject, committed census+TSV (`python3 corpus/evidence/round41/c2-count.py`) | `W04_DISPOSITIONED=5/5` | 0 |
| harness, committed census+TSV (P0) | `W04_DISPOSITIONED=5/5` | 0 |
| harness, committed census + byte-copy TSV (P0b) | `W04_DISPOSITIONED=5/5` | 0 |
| recorded pre-round control `.ufo/waves/round-41/controls/c2-control-before.txt` | `W04_DISPOSITIONED=0/5` + 5 `FAIL` lines | 1 |

Census `validate --root /home/vgpnk/Projects/shokunin chousa` emits exactly five W04 rows
(S051, S053, S073, S074, S075) plus `chousa\tok\t…/corpus/SOURCES.md`. So `<n>=5` at this
revision; the parity run reproduces the committed result exactly.

**Claim-binding discrepancy (planner-facing):** this seat's dispatch states C2 must print
`W04_DISPOSITIONED=4/4`. The committed counter, `claims.md` ("`<n>` is the census warning
count at the measured revision, so the predicate stays join-based, not literal-4") and
`corpus/evidence/round41/measure-after-c2.txt` (`5/5`, `AFTER_EXIT=0`) all say 5. A literal
`4/4` expectation is unsatisfiable at this revision (S075 is the fifth warning). Mutants below
are therefore scored as `k<n` / non-zero exit, which is what the freeze actually defines.

## Mutation matrix — actual outputs

Scratch inputs: `stubs/stub_s999_plus.sh` (live census + one synthetic `S999` W04 line),
`stubs/stub_s999_only.sh` (only the `S999` W04 line), `stubs/stub_now04.sh` (no W04 rows),
`tsv/*.tsv` (each a copy of the committed TSV with one row edited).

### A — census stub emits W04 for S999 (no TSV row)

A1 `stub_s999_plus.sh` + committed TSV:

```
W04_DISPOSITIONED=5/6
  FAIL S999: no disposition row
EXIT=1
```

A2 `stub_s999_only.sh` + committed TSV (the literal `<4` reading):

```
W04_DISPOSITIONED=0/1
  FAIL S999: no disposition row
  WARN S051: disposition row without a census warning
  ... (S053, S073, S074, S075 identical WARN lines)
EXIT=1
```

A0 vacuity control, stub with zero W04 rows:

```
W04_DISPOSITIONED=0/0
  WARN S051: disposition row without a census warning
  ... (S053, S073, S074, S075 identical WARN lines)
EXIT=1
```

**Verdict A: KILLED (both variants).** A W04 id absent from the TSV is failed
(`no disposition row`), the count drops below `n` (5/6; 0/1), and exit is 1. The `n>=1` guard
also prevents an empty census from passing vacuously (0/0 → exit 1).

### B — TSV evidence names a missing path (S053 evidence → `corpus/evidence/round41/does-not-exist.md`)

```
W04_DISPOSITIONED=4/5
  FAIL S053: evidence cell empty or unresolvable
EXIT=1
```

B2 empty evidence cell (S053 column 4 blank):

```
W04_DISPOSITIONED=4/5
  FAIL S053: no disposition row
EXIT=1
```

**Verdict B: KILLED (only under the "evidence names *only* a broken pointer" reading).**
Under the other natural reading — "evidence *contains* a missing path" — the mutant
**SURVIVES**; see D1.

## Surviving mutants (coverage findings, not a contract change)

| id | mutant | expected | observed | verdict |
|---|---|---|---|---|
| D1 | S053 evidence = `S051 corpus/evidence/round41/does-not-exist.md` (broken path **plus** an `S###` token) | fail | `W04_DISPOSITIONED=5/5`, `EXIT=0` | **SURVIVED** |
| D2 | TSV gains extra row `S999` absent from census output | fail (`claims.md` kill rule) | `W04_DISPOSITIONED=5/5`, `WARN S999: disposition row without a census warning`, `EXIT=0` | **SURVIVED** |
| D3 | S053 evidence = `S999` (a row id that exists nowhere) | fail | `W04_DISPOSITIONED=5/5`, `EXIT=0` | **SURVIVED** |

### F1 — disjunctive evidence check masks a named missing path (line 42)

`resolved = any((LANE / q.split(":")[0]).exists() for q in paths) or bool(srows)` — any
`S###` token anywhere in the cell short-circuits the path-existence test. A cell naming a
path that does not resolve passes as long as it also mentions a row id (D1). This is the
precise sense in which the second half of the assigned attack is **not** detected: the
detector only rejects evidence that consists *solely* of unresolvable pointers.

### F2 — the S-row fallback is unvalidated and load-bearing (line 42)

`bool(srows)` accepts any three-digit `S` token without checking the registry, so a phantom
id (`S999`) resolves (D3). Simultaneously the fallback is **required** for the committed data:

| row | paths matched | path-only resolves | S-rows | survives on path alone |
|---|---|---|---|---|
| S051 | `corpus/SOURCES.md` | True | 2 | True |
| S053 | `corpus/SOURCES.md` | True | 2 | True |
| S073 | — | False | 3 | False |
| S074 | — | False | 1 | False |
| S075 | — | False | 4 | False |

S073/S074/S075 pass only through the S-row branch (their evidence carries no token from the
`corpus|.ufo|tools|SKILL.md|PROVINCE.md|LOG.md|SCORECARD.md` alternation). So the branch
cannot simply be deleted to fix F1; it would need an existence check against the registry
while the three rows' evidence gains a resolvable path — a contract/data decision, not a
tester's edit.

### F3 — extra TSV ids only WARN, never fail (lines 47, 54)

`extra = [k for k in dispo if k not in ids]` feeds only the `WARN` print; `sys.exit` depends
on `k, n` alone. The frozen kill rule in `claims.md` ("a TSV naming ids not in the census
output … fails the counter") and the module docstring ("A TSV row whose id is absent from the
census … counts as undispositioned") both describe a failure the code does not implement.
D2 shows a junk TSV row is accepted with exit 0.

### F4 — empty-evidence diagnostic is collapsed (lines 25, 29)

`line.strip()` removes the trailing tab of an empty evidence cell, so `len(cols) >= 4` fails
and the row is skipped entirely; the failure is reported as `no disposition row` rather than
`evidence cell empty or unresolvable` (B2). The verdict is still fail, so this is a
diagnostic/precision gap, not a false pass.

Line references are to the committed `c2-count.py`: 21 (`w[2].split()[0]` id extraction),
25 (`line.strip()`), 29 (`len(cols) >= 4`), 42 (`resolved = … or bool(srows)`), 47 (`extra = …`),
54 (`sys.exit(0 if (k == n and n >= 1) else 1)`).

## Restoration / integrity evidence

The lane subject was never written: every mutant lives in `/tmp/mutatec2join.AcXlvm`.
Before the probe (04:44) and after (04:45) all three hashes are identical:

```
66bb31af0d199443c9a9c6f8bd9cf733f92e883306770ee7831559a34f4ccaa3  c2-count.py
2558bba41e54ae9f3c4fc48c89c95bbcf7c24acdbe6a592dcb72c41ff2dee7ca  w04-dispositions.tsv
3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30  scripts/sources-census.sh
```

`git hash-object` still returns the HEAD blobs `86a112d1…` / `88be5ef3…`; the fleet repo is
clean for `scripts/sources-census.sh`. `git status` in the lane showed a transient
`M corpus/evidence/round41/receipts/cells/cells.json`; that path has no writer other than
sibling `c1-count.py` (grep of `.py`/`.sh` writers: `c1-count.py:99`), and the committed
`c2-count.py` has no write surface at all (its only `Path` use is the `LANE` binding). It is
concurrent C1-seat churn, not this seat's write. Nothing was written to `.ufo/state`, the
fleet repo, sibling repos, or the lane index/jj state.

Tool installs: none (no pacman, no network; nothing needed).

## Artifact pointers (resolvable)

- Scratch root (retained for audit): `/tmp/mutatec2join.AcXlvm`
- Raw matrix transcript: `/tmp/mutatec2join.AcXlvm/matrix.out`
- Probe harness: `/tmp/mutatec2join.AcXlvm/lane/corpus/evidence/round41/c2-count.py`
- Census stubs: `/tmp/mutatec2join.AcXlvm/stubs/{stub_s999_plus.sh,stub_s999_only.sh,stub_now04.sh}`
- TSV mutants: `/tmp/mutatec2join.AcXlvm/tsv/{missing_only.tsv,empty_ev.tsv,missing_plus_srow.tsv,extra_id.tsv,phantom_srow.tsv}`
- Captured real census output: `/tmp/mutatec2join.AcXlvm/census-real.out`
- This report: `.ufo/waves/round-41/w1/MutateC2Join.md`

## Bottom line

C2's assigned kill surfaces work at this revision: a W04 id missing from the TSV and an
evidence cell that names only an unresolvable path both fail the counter with `k<n` and
exit 1 (`5/6`, `0/1`, `4/5`), against a parity-verified `5/5` baseline. Three plausible
defects survive, all traced to two lines: the unvalidated `or bool(srows)` disjunction
(F1/F2) and the WARN-only handling of extra TSV ids that `claims.md` says must fail (F3).
Those are calibration findings for the L1/planner; this seat made no contract change.

Report: .ufo/waves/round-41/w1/MutateC2Join.md
