# MutShortEnum — short-enumeration mutant (round 43, w1)

Role: mutation-tester (leaf). Assigned probe only. No production edit. No network. No second runtime.

Axes: operability (C1 equality detector still runs), calibration (short list vs the independent round-42 absent ids, bound not retuned), depth (one id dropped, names listed, not a count-only claim).

## Claimed invariant

C1 requires the enumeration to be exactly the 15 ids the committed round-42 table labels `absent`. The counter's own mutant clause (`c1-count.py` `short = ids[:-1]`, check `MUTANT_DETECTED`) asserts that a 14-id prefix is not that list. This probe drops the last id of the committed split TSV and checks that claim against the table. The committed TSV was not edited.

## Subject identity

Lane HEAD `737f40b6aa8f37ffe2269db370fd6d65a720d9a8` (matches the measured commit).

| artifact | git blob | sha256 |
|---|---|---|
| `corpus/evidence/round43/absent-split.tsv` | `46352664d648e85f91335c0f1c04ef068a7b4318` | `bba7d8b6b5165cd4d5b21c9b9c9e9275ecb26839ad8764d8db8b4ffebc001a58` |
| `corpus/evidence/round42/quarantine-verdicts.tsv` | `40d935dd9b7a78c8749ca373c83bbd31fc3f9a05` | `bcfafd534541b6a59f893488408738332e3fe1e5c324d4bdeb58547d44c7395d` |
| `corpus/evidence/round43/c1-count.py` | (not re-hashed as a blob this probe) | `54ced70767ccd20bc502504ef75d427bc760d10ebdf70a1053812ff8853289c9` |

Committed TSV: 484 bytes, 15 newlines, ends with `\n`. Last 20 bytes: `b'te\t34\t36\t0.944444\t3\n'`.

## Mutant

Isolated scratch: `/tmp/mutshortenum.1OMtss/absent-split.tsv`, a byte copy of the committed split TSV. Smallest behavior-bearing point: delete the last record only.

Dropped line (the last id):

```
S116	misquote	34	36	0.944444	3
```

Mutant names (14), the C1 short list:

```
S080,S082,S084,S086,S088,S093,S094,S104,S105,S108,S110,S111,S112,S114
```

Round-42 absent ids (15), independent read of `quarantine-verdicts.tsv` where column 2 is `absent`:

```
S080,S082,S084,S086,S088,S093,S094,S104,S105,S108,S110,S111,S112,S114,S116
```

`SHORT_EQ_ABSENT=False`. Missing from the short list: `S116`. Extra in the short list: none. The committed 15-id list equals the absent list (`FULL_EQ_ABSENT=True`). The 14-id prefix does not.

## Expected detector

Same command on pristine, mutated, and restored scratch bytes:

```
python3 corpus/evidence/round43/c1-count.py --tool /tmp/mutshortenum.1OMtss/emit.py
```

`emit.py` writes the current scratch TSV to stdout and exits 0. It does not read or write the lane. The kill predicate is `ABSENT_ENUMERATED`: tool ids must equal the 15 absent ids. A baseline failure would be inconclusive. Expected: pristine pass, mutated fail (killed), restored pass.

## Output

Pristine scratch (sha256 `bba7d8b6b5165cd4d5b21c9b9c9e9275ecb26839ad8764d8db8b4ffebc001a58`, same as committed):

```
TABLE_ABSENT PASS 15/15
TOOL_EXIT PASS exit=0
ABSENT_ENUMERATED PASS 15/15
CLASSED PASS 15/15
BOTH_NONEMPTY PASS misquote=9 not-carried=6
REPRODUCIBLE PASS identical=True
MUTANT_DETECTED PASS short=14 expected=15
ABSENT_ENUMERATED=15/15
CLASSED=15/15
BOTH_NONEMPTY=1/1
REPRODUCIBLE=1/1
MUTANT_DETECTED=1/1
C1=PASS
EXIT=0
```

Name-list comparison after the drop (committed file still the 15-id source; scratch already 14):

```
COMMITTED_IDS=S080,S082,S084,S086,S088,S093,S094,S104,S105,S108,S110,S111,S112,S114,S116
COMMITTED_N=15
MUTANT_IDS=S080,S082,S084,S086,S088,S093,S094,S104,S105,S108,S110,S111,S112,S114
MUTANT_N=14
ABSENT_IDS=S080,S082,S084,S086,S088,S093,S094,S104,S105,S108,S110,S111,S112,S114,S116
ABSENT_N=15
DROPPED=S116
SHORT_EQ_ABSENT=False
FULL_EQ_ABSENT=True
MISSING_FROM_SHORT=S116
EXTRA_IN_SHORT=
```

Mutated scratch (453 bytes, 14 newlines, sha256 `e2e74c8a928823330289e51e0b3785e1cef0e58ad5e6af0e89001184192f5210`):

```
TABLE_ABSENT PASS 15/15
TOOL_EXIT PASS exit=0
ABSENT_ENUMERATED FAIL 14/15
CLASSED FAIL 14/15
BOTH_NONEMPTY PASS misquote=8 not-carried=6
REPRODUCIBLE PASS identical=True
MUTANT_DETECTED PASS short=13 expected=15
ABSENT_ENUMERATED=0/15
CLASSED=0/15
BOTH_NONEMPTY=1/1
REPRODUCIBLE=1/1
MUTANT_DETECTED=1/1
C1=FAIL
EXIT=1
```

Restored scratch (byte-identical to the saved pristine copy):

```
TABLE_ABSENT PASS 15/15
TOOL_EXIT PASS exit=0
ABSENT_ENUMERATED PASS 15/15
CLASSED PASS 15/15
BOTH_NONEMPTY PASS misquote=9 not-carried=6
REPRODUCIBLE PASS identical=True
MUTANT_DETECTED PASS short=14 expected=15
ABSENT_ENUMERATED=15/15
CLASSED=15/15
BOTH_NONEMPTY=1/1
REPRODUCIBLE=1/1
MUTANT_DETECTED=1/1
C1=PASS
EXIT=0
```

## Verdict

**killed.** Baseline held (`C1=PASS`, exit 0), so the miss is not inconclusive. The 14-id prefix is not the 15 absent ids. The detector rejected it (`ABSENT_ENUMERATED FAIL 14/15`, `C1=FAIL`, exit 1). That is not permission to change the contract, and the bound was not retuned.

Coverage note, not a second probe: on the mutated tool the counter's own `MUTANT_DETECTED` line still prints PASS, because it slices `ids[:-1]` of whatever the tool just printed (`short=13 expected=15`) instead of replaying this 14-name list. The kill is `ABSENT_ENUMERATED` / `CLASSED`, which is the equality the assigned mutant challenges. A surviving mutant would have been `SHORT_EQ_ABSENT=True` or `C1=PASS` on the 14-id bytes. Neither happened.

## Restoration evidence

Committed TSV was not the mutation target. After the probe:

```
CMP_SCRATCH_RESTORED=identical
CMP_COMMITTED_SCRATCH=identical
bba7d8b6b5165cd4d5b21c9b9c9e9275ecb26839ad8764d8db8b4ffebc001a58  corpus/evidence/round43/absent-split.tsv
bba7d8b6b5165cd4d5b21c9b9c9e9275ecb26839ad8764d8db8b4ffebc001a58  /tmp/mutshortenum.1OMtss/absent-split.tsv
bba7d8b6b5165cd4d5b21c9b9c9e9275ecb26839ad8764d8db8b4ffebc001a58  /tmp/mutshortenum.1OMtss/pristine.bytes
COMMITTED_EQ_PRISTINE_SAVED=True
SCRATCH_EQ_PRISTINE_SAVED=True
COMMITTED_LEN=484
```

Before/after sha256 of the committed split TSV is the same (`bba7d8b6…001a58`). Scratch mutated hash `e2e74c8a…2f5210` was replaced by the saved 484-byte pristine copy before the restored detector run.

Stop. One mutation probe.
