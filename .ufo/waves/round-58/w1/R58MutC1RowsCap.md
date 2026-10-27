# Round 58 C1 row-cap mutation probe — R58MutC1RowsCap

## Scope and method
- Read frozen `corpus/evidence/round58/claims.md` and `c1-count.py`; freeze commit `9e73a031ab1ac3bac343de008850d7d87f9e5634`. Counter SHA-256: `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f` (same as `git show <freeze>:...` and working-tree bytes).
- At probe time, lane `tools/build-spans.py` was byte-identical to the pinned r55 builder (`1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`); it had no row-cap check. Thus the cap-bearing reference below is explicitly a scratch-only model of claimed item (5), not a claim that a completed C1 builder was present.
- Scratch reference: copied the pristine builder and added a `QUOTES_CAP = 100_000` check over nonblank data rows, refusing with `(ROWS)` before parsing/writing. Mutant: one-point change `100_000 → 1_000_000_000`. The scratch `capture-text.py` was copied byte-identically (SHA `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573`) because the builder imports it relative to its own directory.
- Ran the frozen detector with `--seed 7` and distinct absolute `--work` dirs, setting `TMPDIR=/fast/scratch/hyaku/chousa-r58/R58MutC1RowsCap` and `PYTHONDONTWRITEBYTECODE=1`; form: `python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round58/c1-count.py --builder <scratch-builder> --work <scratch-work> --seed 7`.

## Exact frozen-counter output
Pristine r55 bytes (`builder-pristine.py`):
```text
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)
SYMLINK_OUT=fail(rc=0, expected refusal)(target-dir-written!)
SYMLINK_CACHE=fail(rc=0, expected refusal)
FIFO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'FIFO', 'REGTYPE', 'SYMLINK'] absent in 'build-spans: refused S571: no defined text form for f4088c6d6da1f4763182a51d (raw neither OLE nor zip, no .txt)\n')
DEVZERO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'SIZE', 'SYMLINK', 'REGTYPE'] absent in 'build-spans: refused S581: no defined text form for a172f04219497476db868414 (raw neither OLE nor zip, no .txt)\n')
FAT_RAW=fail(rc=1, reason ['SIZE'] absent in 'build-spans: refused S551: capture-text refused f96cbd6d82dbae8a8e2c6223.raw: ole-malformed: sector shift 0, mini shift 0\n')
MANY_QUOTES=fail(rc=0, expected refusal)
ESCAPE_ENTRY=pass(refused)
HELDOUT_OK=pass
BEFORE_FOREIGN=deleted
DENIED=0/0
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
RC=1
```

Scratch reference with 100,000-row cap (`builder-candidate.py`):
```text
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)
SYMLINK_OUT=fail(rc=0, expected refusal)(target-dir-written!)
SYMLINK_CACHE=fail(rc=0, expected refusal)
FIFO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'FIFO', 'REGTYPE', 'SYMLINK'] absent in 'build-spans: refused S571: no defined text form for f4088c6d6da1f4763182a51d (raw neither OLE nor zip, no .txt)\n')
DEVZERO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'SIZE', 'SYMLINK', 'REGTYPE'] absent in 'build-spans: refused S581: no defined text form for a172f04219497476db868414 (raw neither OLE nor zip, no .txt)\n')
FAT_RAW=fail(rc=1, reason ['SIZE'] absent in 'build-spans: refused S551: capture-text refused f96cbd6d82dbae8a8e2c6223.raw: ole-malformed: sector shift 0, mini shift 0\n')
MANY_QUOTES=pass(refused)
ESCAPE_ENTRY=pass(refused)
HELDOUT_OK=pass
BEFORE_FOREIGN=deleted
DENIED=0/0
SUMMARY OK=4/4 REFUSE=1/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
RC=1
```

Mutant, cap raised to 1,000,000,000 (`builder-mutant-cap1e9.py`):
```text
EMPTY_OK=pass
REBUILD_OK=pass
FOREIGN=fail(rc=0, orphans deleted: foreign gone=True)
SYMLINK_OUT=fail(rc=0, expected refusal)(target-dir-written!)
SYMLINK_CACHE=fail(rc=0, expected refusal)
FIFO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'FIFO', 'REGTYPE', 'SYMLINK'] absent in 'build-spans: refused S571: no defined text form for f4088c6d6da1f4763182a51d (raw neither OLE nor zip, no .txt)\n')
DEVZERO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'SIZE', 'SYMLINK', 'REGTYPE'] absent in 'build-spans: refused S581: no defined text form for a172f04219497476db868414 (raw neither OLE nor zip, no .txt)\n')
FAT_RAW=fail(rc=1, reason ['SIZE'] absent in 'build-spans: refused S551: capture-text refused f96cbd6d82dbae8a8e2c6223.raw: ole-malformed: sector shift 0, mini shift 0\n')
MANY_QUOTES=fail(rc=0, expected refusal)
ESCAPE_ENTRY=pass(refused)
HELDOUT_OK=pass
BEFORE_FOREIGN=deleted
DENIED=0/0
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL
RC=1
```

The frozen MANY_QUOTES leg writes 100,001 nonblank rows, all with the duplicate id `S900`, same URL and quote. It expects nonzero refusal with a `SIZE`, `ROWS`, or `CAP` reason. Candidate passes that leg; pristine and mutant accept it (`rc=0`). Full C1 remains `FAIL` for all three: this scratch probe isolates only the row bound, leaving other claimed refusal legs intentionally unimplemented.

## Duplicate-id behavior and output
- Candidate cap-3 probe, four duplicate `S900`/same-URL/same-quote rows: `rc=2`; stderr `build-spans: .../dup4.tsv has 4 data rows, over the 3-row cap (ROWS)`; zero span files. Duplicate ids count as rows; they do not bypass the cap.
- Candidate cap-100k and raised-cap mutant, same four-row input: each `rc=0`, `QUOTE S900 char 0 spans/S900-1.txt` through `...S900-4.txt`, `SPANS_ROWS=4 WRITTEN=4`, four files. Same-id/same-URL duplicates below the cap are accepted and get one span per row.
- Candidate on the exact 100,001-row shape: `rc=2`, stderr `build-spans: .../many100001.tsv has 100001 data rows, over the 100000-row cap (ROWS)`; zero files. Mutant counter's `out-many/spans.tsv` had 100,002 lines (header + 100,001 rows) and `spans/` had 100,001 files. Candidate's `out-many/` was empty.
- Same id with different URLs remains a separate pre-existing refusal: `rc=2`, stderr `line 3: S900 names https://fixture.example/doc2, earlier rows name https://fixture.example/doc1`.

## Hashes and restoration
- Before: lane builder and pristine scratch copy `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`; counter `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f`.
- Candidate before mutation: `a96af4f882f57a1d7a031f849dae212c15f6ee4a267e0239ffadf0865d4a13bb`; mutant before restoration: `8639dd345c13f0328d34a1ca61fae80f9d675566075b28a33917461747f3f08b`.
- Restored mutant scratch path from the candidate; after: candidate and restored mutant both `a96af4f882f57a1d7a031f849dae212c15f6ee4a267e0239ffadf0865d4a13bb`. Lane builder and counter hashes after remained `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6` and `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f`. No lane source/counter bytes were changed.

VERDICT: Raising the 100,000-row bound to 1,000,000,000 is KILLED by MANY_QUOTES: the mutant returns `MANY_QUOTES=fail(rc=0, expected refusal)` and builds all 100,001 duplicate-id rows; the row-cap detector survives this mutation.
