# R59Executor05 — positive-verdict-path probe on the frozen round-58 C1 counter

Leaf executor, no dispatch. Lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin` (all lane
reads read-only; only write is this report). Scratch `/fast/scratch/hyaku/chousa-r59/R59Executor05/`
(honoured `HYAKU_SCRATCH`, explicit `--work`; removed before yield). No install: `~/.omp/agent/RULES.md`
read, `pacman` paused and not run. No git/jj/index writes; `git status --porcelain` at end showed only
the pre-existing untracked `.ufo/waves/round-59/` and `corpus/evidence/round59/`.

## Inputs read (read-only)

- `corpus/evidence/round59/claims.md` — **absent** at execution time (`test -e` rc=1).
  `corpus/evidence/round59/` held only `census-start.txt` and `controls/c1-before.txt`.
  So the applicable frozen predicate is round-58's C1 counter, not a round-59 claim file.
- `corpus/evidence/round58/c1-count.py`, 406 lines, sha256 `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f` (read in full).
- `corpus/evidence/round58/controls/{c1-before.txt,c1-controls.txt,c1-control-build.txt,REFUSEALL.py,build-spans-r55.py}`.
- `tools/build-spans.py` sha256 `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`
  — byte-identical to the pinned r55 control, i.e. the lane builder **is** the "before" builder.
- `tools/capture-text.py` sha256 `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573`;
  `corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` sha256 `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3`, 129,024 B.
- Python 3.14.8.

## Run A — exact frozen counter, lane/base builder (reproduces the pre-state receipt)

    cd /home/vgpnk/Projects/shokunin/chousa-shokunin
    HYAKU_SCRATCH=/fast/scratch/hyaku python3 -B corpus/evidence/round58/c1-count.py \
      --work /fast/scratch/hyaku/chousa-r59/R59Executor05/work-base \
      --controls corpus/evidence/round58/controls

Output (wall 67.8 s):

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
    CONTROL_REFUSEALL=denied
    CONTROL_build-spans-r55=denied
    DENIED=2/2
    SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2
    C1=FAIL
    EXIT=1

The leg lines match `corpus/evidence/round59/controls/c1-before.txt` and
`round58/controls/c1-before.txt` line-for-line; the `CONTROL_*`/`DENIED` lines differ only because I
passed `--controls` (the round-59 pre-state receipt omits it, hence `DENIED=0/0`).

## Run B — exact frozen counter against an all-legs-satisfying reference candidate

Scratch-only candidate `/fast/scratch/hyaku/chousa-r59/R59Executor05/ref-build-spans.py` (not a lane
file; written solely as a positive-control vehicle): refuses `--out` symlink, cache symlink, cache
`NOT_REGULAR` (FIFO/device), raw > 64 MiB (`SIZE`), quotes > 100,000 rows (`ROWS`), `..` entry, and any
foreign/orphan `spans/S###-N.txt` before deletion; otherwise emits the counter's expected
`spans.tsv` rows/offsets and span bytes. For OLE/ZIP raws it derives the form with
`tools/capture-text.py` (the counter's own HELDOUT derivation).

    HYAKU_SCRATCH=/fast/scratch/hyaku python3 -B corpus/evidence/round58/c1-count.py \
      --builder /fast/scratch/hyaku/chousa-r59/R59Executor05/ref-build-spans.py \
      --work /fast/scratch/hyaku/chousa-r59/R59Executor05/work-ref2 \
      --controls corpus/evidence/round58/controls

Output (wall 52.3 s):

    EMPTY_OK=pass
    REBUILD_OK=pass
    FOREIGN=pass(refused)
    SYMLINK_OUT=pass(refused)
    SYMLINK_CACHE=pass(refused)
    FIFO_TXT=pass(refused)
    DEVZERO_TXT=pass(refused)
    FAT_RAW=pass(refused)
    MANY_QUOTES=pass(refused)
    ESCAPE_ENTRY=pass(refused)
    HELDOUT_OK=pass
    BEFORE_FOREIGN=deleted
    CONTROL_REFUSEALL=denied
    CONTROL_build-spans-r55=denied
    DENIED=2/2
    SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2
    C1=FAIL
    EXIT=1

Every leg — 4 safe, 7 hazard, including `BEFORE_FOREIGN=deleted` and both controls — reads `pass`,
yet `SUMMARY REFUSE=0/7`, `C1=FAIL`, exit 1. The positive verdict path is **dead by construction**,
independently of builder quality. (An earlier iteration of the same candidate missed only
`FIFO_TXT=pass` because `Path.is_file()` was tested before `lstat`; legs do discriminate, so the run
above is not a harness-wide "everything passes" artifact.)

## Run C — causality test: one-token mutant of the frozen counter (scratch copy)

Copy `mutant-c1-count.py` = frozen bytes; one edit at `:391`:
`ref_pass = all(("=PASS" in l) for l in ref_legs)` → `all(("=pass" in l.lower()) for l in ref_legs)`.
Placed at `/fast/.../mutroot/c1-count.py` beside `mutroot/controls/{build-spans-r55.py,REFUSEALL.py}`
(the counter's control sub-run executes `HERE/c1-count.py` and its BEFORE builder lives beside it;
without that directory, `BEFORE_FOREIGN=absent` and the verdict stays FAIL).

    HYAKU_SCRATCH=/fast/scratch/hyaku python3 -B /fast/scratch/hyaku/chousa-r59/R59Executor05/mutroot/c1-count.py \
      --builder /fast/scratch/hyaku/chousa-r59/R59Executor05/ref-build-spans.py \
      --work /fast/scratch/hyaku/chousa-r59/R59Executor05/work-mut2 \
      --controls /fast/scratch/hyaku/chousa-r59/R59Executor05/mutroot/controls

Output (wall 10.2 s):

    EMPTY_OK=pass
    REBUILD_OK=pass
    FOREIGN=pass(refused)
    SYMLINK_OUT=pass(refused)
    SYMLINK_CACHE=pass(refused)
    FIFO_TXT=pass(refused)
    DEVZERO_TXT=pass(refused)
    FAT_RAW=pass(refused)
    MANY_QUOTES=pass(refused)
    ESCAPE_ENTRY=pass(refused)
    HELDOUT_OK=pass
    BEFORE_FOREIGN=deleted
    CONTROL_REFUSEALL=denied
    CONTROL_build-spans-r55=denied
    DENIED=2/2
    SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2
    C1=PASS
    EXIT=0

Same fixtures, same candidate, `C1=PASS`/exit 0 after only the case-sensitivity change; the SUMMARY
line still says `REFUSE=0/7` because `:399` keeps the uppercase test (cosmetic: `verdict` at `:394`
does not read it). So the sole blocker on the positive path is the token comparison, and fixing only
`:391` does not weaken control denial (`DENIED=2/2` unchanged).

## Finding — the frozen counter's positive verdict token never matches its own leg strings

- `c1-count.py:51` `PASS = "pass"`; `:52` `FAIL = "fail"`.
- All refusal legs are emitted through lowercase `PASS`: `expect_refuse` returns
  `f"{name}={PASS}(refused)"` at `:160` (used at `:232,:250,:263,:278,:295,:306`), explicit appends at
  `:223` (`FOREIGN`) and `:234` (`SYMLINK_OUT`), literal `"ESCAPE_ENTRY=pass(refused)"` at `:315`.
- Aggregation at `:391` asks for uppercase: `ref_pass = all(("=PASS" in l) for l in ref_legs)`.
- Therefore `ref_pass` is a constant `False`, `:394` can only yield `FAIL`, `:402` exits 1, and
  `:399` prints `REFUSE=0/7` whatever the builder does.

Observed consequence: a candidate that satisfies all eleven legs still prints `C1=FAIL` (Run B); a
one-line scratch mutant prints `C1=PASS` (Run C). Any round-59 row that repeats "`c1-count.py` must
print `C1=PASS` and exit 0" is unsatisfiable on these frozen bytes; conversely "controls did not reach
`C1=PASS`" carries no information about the controls.

Adjacent, same-counter observations (bounded; not re-scoped):
- `:389` computes an `ok_pass` expression that `:390` immediately overwrites — dead code.
- `:393` `denied_pass = (denied == total) if total else True` and `:365` `if args.controls:` mean the
  documented predicate invocation (no `--controls`) always records `DENIED=0/0` and treats it as pass.
- `:212` `foreign.write_bytes(...)` assumes `EMPTY_OK` created `out/spans/`; `REFUSEALL.py` therefore
  aborts the harness with `FileNotFoundError` before any `C1=` line, so its `denied` is denial-by-crash
  (controls sub-run at `:373-380` only scans stdout, so the receipt is unaffected).
- The committed `corpus/captures/6dc68fd6b32ce9c8dfcebce8.txt` is **not** the defined form of its raw:
  `tools/capture-text.py` on the `.raw` gives 47,356 B sha256 `a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867`,
  the `.txt` is 157,816 B sha256 `d4e7e5adc9f723d61852a6dffd559062ba3db5603c43ec158d96d6d4e564e112`. The real builder
  takes the OLE branch for this key, so HELDOUT is unaffected; a candidate that trusted the cache
  `.txt` fails `HELDOUT_OK`. Reported as an observation, not a claim change.

## Positive-verdict control design implied for round 59 (L1's call; nothing applied)

1. A positive control is missing from round-58's set: `REFUSEALL`/r55 only exercise denial. Run B is
   the executable shape of it — an all-legs-pass candidate must be shown to reach `C1=PASS`.
2. That control is currently red for counter reasons, not candidate reasons. Minimal repair options,
   both one-line: compare the lowercase token at `:391`/`:399`, or emit refusal legs in uppercase.
   Run C shows the first option flips `C1=FAIL`→`C1=PASS` and leaves `DENIED=2/2` intact.
3. Until such a repair is frozen, round-59 operability verdicts should read the per-leg strings
   (which discriminate, as Run B's FIFO iteration shows), never `C1=`/`REFUSE=`.

## Limits / risks

- `ref-build-spans.py` is a scratch test vehicle that encodes the counter's own span formula and
  refusal classes; it is **not** a hardening candidate for `tools/build-spans.py` and proves nothing
  about the lane builder beyond "legs are satisfiable".
- C2 was not re-run; its tokens are uppercase-consistent (`c2-count.py:156,162`), so this defect is
  specific to `c1-count.py`.
- No live fetch; all fixtures synthetic or lane-read-only. Scratch (work dirs, candidate, mutant
  copies) removed before yield; the outputs above are the retained evidence.
- Installs/updates: none.

VERDICT: The frozen round-58 C1 counter's positive verdict is unreachable — an all-legs-passing
candidate prints `SUMMARY OK=4/4 REFUSE=0/7 ... C1=FAIL` and exits 1 (Run B), while a one-line
lowercase fix to `:391` yields `C1=PASS` exit 0 with identical legs and controls still denied 2/2
(Run C). Cause: `PASS="pass"` leg strings (`:51,:160,:223,:234,:315`) vs uppercase `"=PASS"` test at
`:391` (and `:399`). Round-59 positive-verdict calibration must add the all-legs-pass control and
either repair the token or score on per-leg strings; the round-59 claims file was absent, so no
round-59 predicate was available to run.

Report trailer: `.ufo/waves/round-59/w1/R59Executor05.md`
