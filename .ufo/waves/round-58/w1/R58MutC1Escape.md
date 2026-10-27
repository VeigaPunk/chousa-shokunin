# R58MutC1Escape — ESCAPE_ENTRY mutation probe

## Scope and frozen inputs
- Read frozen `corpus/evidence/round58/claims.md` and `c1-count.py`; C1 specifies `ESCAPE_ENTRY` as the regression leg for rejecting entry `../escape.md` before writing `spans.tsv`.
- Target builder: `tools/build-spans.py`; relevant check is `entry.startswith("/") or ".." in pathlib.PurePath(entry).parts` (line 116). Frozen counter sha256: `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f`.
- Original builder sha256: `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6` (same as C1's pinned round-55 builder). All probe copies/work were under `/fast/scratch/hyaku/chousa-r58/R58MutC1Escape`; no lane source bytes edited.

## Mutation and detector
Mutation: remove only the `".." in pathlib.PurePath(entry).parts` disjunct, leaving the absolute-path refusal. The same frozen detector was run in all three phases:

`python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round58/c1-count.py --builder <scratch-builder> --work <fresh-scratch-work>`

Pristine run output (selected exact lines):
```
ESCAPE_ENTRY=pass(refused)
C1=FAIL
exit=1
```
The overall C1 failure is consistent with this pinned pre-hardening builder: its other hazard legs fail. The scoped ESCAPE_ENTRY leg is green on pristine bytes, so that leg's baseline is not inconclusive.

Mutated run output (exact relevant lines):
```
ESCAPE_ENTRY=fail(rc=0, written=True)
C1=FAIL
exit=1
```
Concrete generated fixture: `quotes-esc.tsv` contained `S501\thttps://fixture.example/doc1\travo oscar foxtrot f\t../escape.md`. The mutant run wrote `work-mutant/out-esc/spans.tsv`; its row included `../escape.md` as the entry field. Thus the frozen leg detected acceptance and output writing.

Restored run output (exact selected lines):
```
ESCAPE_ENTRY=pass(refused)
SUMMARY OK=3/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
exit=1
```
The restored scratch builder, pristine scratch copy, and lane builder each hashed to `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`. Restoration was by copying the pristine bytes back over the mutant copy. The non-ESCAPE legs remained the same expected pre-hardening failures; controls were not passed (`DENIED=0/0`).

An initial direct invocation used positional arguments, contrary to the counter's `--quotes/--out/--cache` interface; it is not evidence. The frozen counter runs above used its own correct invocation and generated the observed escape output. No live fetch was made.

VERDICT: Dropping the entry-path `..` refusal was killed by the frozen ESCAPE_ENTRY leg; pristine and restored leg behavior survived as refusal, with byte-exact restoration confirmed.
