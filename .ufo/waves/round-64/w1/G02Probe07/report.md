# G02 isolated fixture probe

Frozen contract basis: `corpus/evidence/round64/claims.md`, lines 47–52: every non-directory knowledge entry must be a regular file; symlinks judged by target; dangling/non-file symlinks fail.

Fixture recipe (under `/fast/scratch/hyaku/chousa-r64/G02Probe07/fixture`): create `corpus/knowledge/ok.md` regular file and `corpus/README.md` containing `knowledge/ok.md`; add dangling symlink `corpus/knowledge/dangling.md -> missing-target.md`; add FIFO `corpus/knowledge/special.pipe`. The fixture was built in isolated scratch; candidate was not edited.

Command: `python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round64/controls/ref-preflight-v3.py --root /fast/scratch/hyaku/chousa-r64/G02Probe07/fixture --only G02 --work /fast/scratch/hyaku/chousa-r64/G02Probe07/work`
Exit: 1
stdout:
```
GATE G01 census SKIP
GATE G02 knowledge-index FAIL 2 invalid under corpus/knowledge: dangling.md (unresolvable symlink),special.pipe (not a regular file)
GATE G03 lesson-gate SKIP
GATE G04 shonen-pointers SKIP
GATE G05 scorecard-paths SKIP
GATE G06 freeze-selftest SKIP
GATE G07 assimilate-selftest SKIP
GATE G08 gate-selftest SKIP
PREFLIGHT=0/1 FAILED=G02 ENV=none SKIPPED=G01,G03,G04,G05,G06,G07,G08
```
stderr:
```
```

Observed: G02 failed and named both invalid entries. This matches the frozen requirement that dangling symlinks and special/non-regular files fail.
