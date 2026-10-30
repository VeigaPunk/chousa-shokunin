# G02 root probe fixture recipe

Candidate: `corpus/evidence/round64/controls/ref-preflight-v3.py` (read-only). Runtime observed: Python 3.14.8.

From a scratch directory, create two isolated fixture roots:

```sh
mkdir -p fixtures/missing/corpus fixtures/nondir/corpus work
printf 'fixture readme\n' > fixtures/missing/corpus/README.md
printf 'fixture readme\n' > fixtures/nondir/corpus/README.md
printf 'not a directory\n' > fixtures/nondir/corpus/knowledge
```

Run each case:

```sh
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round64/controls/ref-preflight-v3.py --root "$PWD/fixtures/missing" --only G02 --work "$PWD/work/missing"
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round64/controls/ref-preflight-v3.py --root "$PWD/fixtures/nondir" --only G02 --work "$PWD/work/nondir"
```

Both observed exit 1; each reports `GATE G02 knowledge-index FAIL corpus/knowledge is not a directory`, `PREFLIGHT=0/1 FAILED=G02 ENV=none` and all other gates skipped. Frozen `claims.md` §C1 lines 47–52 requires missing or non-directory knowledge roots to fail; expected G02 FAIL / overall exit 1. No candidate edits, installs, or git/jj mutations. Exact captured stdout+stderr: `missing.out`, `nondir.out`.