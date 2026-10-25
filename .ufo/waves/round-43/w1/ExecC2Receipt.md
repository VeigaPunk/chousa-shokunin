# ExecC2Receipt — live c2-count.py stdout vs c2-after.txt

Verdict: **MATCH**. Default `c2-count.py` stdout is byte-identical to `corpus/evidence/round43/receipts/c2-after.txt`.

Axes checked: operability (script ran), calibration (receipt lines and the named flip control), depth (byte compare, not a normalized reread).

Measured commit: `737f40b6aa8f37ffe2269db370fd6d65a720d9a8` (`git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse HEAD`). Python 3.14.8. No lane production file, git index, jj state, fleet repo, sibling repo, or `/home/vgpnk/Projects/shokuknow` was modified. The counter read its own committed inputs, including the shokuknow register and cache paths hardcoded in `c2-count.py`. No shokuknow tool was invoked. No network.

## Files changed

- `.ufo/waves/round-43/w1/ExecC2Receipt.md` (this report only).
- Scratch stdout copies under `/tmp` are not lane files and are not a deliverable.

## Behavior

Default invocation printed the four receipt lines and exited 0. `cmp -s` and `diff -u` both exited 0. SHA-256 of the captured stdout equals SHA-256 of the receipt. Both files are 55 bytes, four LF-terminated lines, no CR.

Adjacent control, not part of the receipt file: `--flip S086` printed `SPLIT_AGREES=14/15` and exited 1, which is what `corpus/evidence/round43/claims.md` requires for that flag. That control was not diffed against `c2-after.txt` (the receipt is the unflipped pass).

## Exact evidence

Command (stdout redirected; stderr empty — the shell transcript begins at `EXIT=`):

```
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/c2-count.py > /tmp/c2-live-stdout.txt; ec=$?; printf 'EXIT=%s\n' "$ec"; echo '--- wc -c live ---'; wc -c /tmp/c2-live-stdout.txt /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/receipts/c2-after.txt; echo '--- cmp ---'; cmp -s /tmp/c2-live-stdout.txt /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/receipts/c2-after.txt; printf 'CMP_EXIT=%s\n' "$?"; echo '--- diff -u ---'; diff -u /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/receipts/c2-after.txt /tmp/c2-live-stdout.txt; printf 'DIFF_EXIT=%s\n' "$?"; echo '--- live stdout ---'; cat -A /tmp/c2-live-stdout.txt; echo '--- receipt ---'; cat -A /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/receipts/c2-after.txt
```

Verbatim combined output:

```
EXIT=0
--- wc -c live ---
 55 /tmp/c2-live-stdout.txt
 55 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/receipts/c2-after.txt
110 total
--- cmp ---
CMP_EXIT=0
--- diff -u ---
DIFF_EXIT=0
--- live stdout ---
SPLIT_AGREES=15/15$
VOCAB_OK=15/15$
MISMATCHES=0$
C2=PASS$
--- receipt ---
SPLIT_AGREES=15/15$
VOCAB_OK=15/15$
MISMATCHES=0$
C2=PASS$
```

`cat -A` prints `$` for end-of-line. Those markers are not file bytes. Live stdout bytes:

```
SPLIT_AGREES=15/15
VOCAB_OK=15/15
MISMATCHES=0
C2=PASS
```

Hash command output, verbatim:

```
d33008677cc7e9f2ab7bda0dfbb488cd4250c4607c79bf328b87f7112249caae  /tmp/c2-live-stdout.txt
d33008677cc7e9f2ab7bda0dfbb488cd4250c4607c79bf328b87f7112249caae  /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/receipts/c2-after.txt
```

`stat` (content match is the hash, not the mtime):

```
/tmp/c2-live-stdout.txt size=55 mtime=2026-10-24 21:17:38.869286117 -0300
/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/receipts/c2-after.txt size=55 mtime=2026-10-24 21:12:08.685072141 -0300
```

Flip control, verbatim:

```
FLIP_EXIT=1
--- flip stdout ---
SPLIT_AGREES=14/15$
VOCAB_OK=15/15$
MISMATCHES=1$
MISMATCH S086 table=misquote independent=not-carried$
C2=FAIL$
```

Flip stdout bytes:

```
SPLIT_AGREES=14/15
VOCAB_OK=15/15
MISMATCHES=1
MISMATCH S086 table=misquote independent=not-carried
C2=FAIL
```

## Remaining risks

- Match is for this run's default stdout against the committed receipt. It does not re-score C1 or C3.
- Receipt mtime is earlier than the live capture. Bytes match; mtime is not a mismatch.
- The flip line `MISMATCH S086 table=misquote independent=not-carried` shows the committed table labels S086 `misquote` and the independent recompute labels it `not-carried` only after the forced flip. That is the control working, not a default-run disagreement. Default `MISMATCHES=0`.
- `/tmp` copies can disappear. The evidence above is the quoted command output.

## Blockers

None. The assigned compare completed. No production edit was in scope.

Report: .ufo/waves/round-43/w1/ExecC2Receipt.md
