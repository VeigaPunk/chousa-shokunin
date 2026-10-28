# ExecIndepBuilder2 — independent hardened builder (R61 C1 reachability)

Builder: `.ufo/waves/round-61/w1/ExecIndepBuilder2/build-spans.py`, sha256
`f37723f22b617d072708bdc5b3ec9014b7b2c51343a257d4ab47bdd09b069b24` (412 lines; base `tools/build-spans.py` extended).
Read only: c1-count.py lines 1-49 (docstring), claims.md, tools/build-spans.py, and (grep-only) the
function list of tools/capture-text.py and the builder-call lines of regress.py. I did NOT open
`controls/ref-build-spans.py` or any other controls file. No install made.

## Result
- Seeds 71001, 71002, 71003 (fresh `--work`, `TMPDIR` = my scratch): each `LEGS=20/20 C1=PASS`.
- `regress.py --builder <mine> --work .../rg`: `REAL_REBUILD=3/3` (round55, round56, round57/c3 all `identical=True pass`).
- Sniff sweep from claims A1 on my file: `grep -nE 'getppid|/proc/|c1-count|round61|leg-|argv\[0\]'` -> exit 1 (no match).
- Peak RSS observed: H14 ~20 MiB, H15 ~20 MiB (limit 96 MiB); H20 ~220-293 MiB (no RSS limit in that leg).
- Scratch `/fast/scratch/hyaku/chousa-r61/ExecIndepBuilder2` deleted (ls count 0). Nothing else written.

## Design (policy as assigned)
- A link at a span path or at `spans.tsv` is replaced by a regular file: write to a temp name in the same
  directory (O_EXCL|O_NOFOLLOW), then `os.replace`; the link is swapped, its target never touched.
- Refused (exit 2, nothing written): `DIR/spans` a symlink or a non-directory; `DIR` a non-directory; any
  output path that is a directory; a regular `spans.tsv` differing from the new manifest; orphan
  `S###-n.txt` files beside no manifest. `--replace` overrides the last two (deletes only `S###-n.txt`).
- Inputs: capture must resolve (realpath) inside the realpath of the cache, be a regular file by `fstat`
  (opened `O_NONBLOCK|O_NOFOLLOW`, so a FIFO never blocks), <= 64 MiB (checked by `fstat` size before
  reading, then `read(cap+1)`); text form <= 64 Mi chars. Any violation, EACCES, FIFO-with-no-.txt
  is a refused row (exit 1, nothing written). `sys.dont_write_bytecode = True` before importing capture-text.
- Manifest written last. `--check` follows no link (a link or non-regular at an output path = STALE).

## Legs I first failed, and why
First run, all three seeds `19/20`: **P02 DOCX** failed (rc=0 but tree not golden) and regress round55
`identical=False` (`check_rc=1`). Cause (my bug, not a counter fault): I read the 8-byte magic with
`os.read(fd, 8)` and then hashed the rest of the same descriptor, so `capture_sha256` was the digest of the
file minus its first 8 bytes; only `.raw` captures carry that digest, so only P02 and the raw-backed
round55 rows saw it. One `os.lseek(fd, 0, SEEK_SET)` before the full read fixed all three seeds and
round55. The 18 other legs passed first try, including all 14 hazards H07-H20.

## Counter docstring ambiguities (n=8)
1. `--replace` appears only in H08; its semantics (manifest only? delete orphan span files? keep non-span
   files?) are not stated. I chose: rewrite manifest, delete only unlisted `S###-n.txt`, keep all else.
2. H09 says orphan beside no manifest -> exit 2; it is silent on an orphan beside a MATCHING manifest.
   Base deletes it; I also delete it (no leg tests it).
3. H07 "different `spans.tsv`" does not say what counts as differing (bytes vs parsed rows); I used bytes.
4. The 64 MiB byte cap for `.txt`/`.raw` is never stated in the docstring; H14/H15 give only 192 MiB +
   RSS < 96 MiB, so the cap is inferred (the claims file says 64 MiB). The H20 char cap (64 MiB chars) is stated.
5. H13 forbids a symlink leaving the cache but does not say whether symlinks that stay inside the cache are
   allowed; I allow them (realpath inside cache root).
6. H17/H18 accept "exit 1 or 2"; which is right for an unreadable/FIFO capture is unspecified (I used 1,
   refused row, since the capture is the row's problem not usage).
7. P03 NOPYC does not say whether the child is run with `-B`; I could not tell and set
   `sys.dont_write_bytecode` unconditionally.
8. H16 gives `--out` regular file -> exit 2 for build mode only; `--check` behaviour unspecified (I exit 2 too).
Not ambiguous in practice but worth noting: H10-H12 allow either "non-zero" or "replaced"; the assigned
policy chose replace for H11/H12 (observed rc=0, victim unchanged) and refuse for H10 (rc=2).

## Caveats (INFERENCE where marked)
- Guards are check-then-write (named limit i); the temp+rename narrows but does not close it. INFERENCE:
  a swapped `spans` dir between preflight and `put` is still followed.
- Counter run once per seed; I did not rerun after the fix at other seeds beyond the three reported.
- I ran no mutation or extra adversarial probes and spawned no labrat.

VERDICT: INDEP2_LEGS=20/20 REAL_REBUILD=3/3 ambiguities=8
