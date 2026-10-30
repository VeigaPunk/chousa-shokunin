# G02 --work regular-file refusal probe

Candidate: `corpus/evidence/round64/controls/ref-preflight-v3.py` (read-only; not production).

Frozen contract: `corpus/evidence/round64/claims.md`, R64-C1 §(iv), requires an existing non-directory `--work` path to exit 2 using the usage form, with no GATE or summary line on stdout and the offending path on stderr.

Command executed:

```sh
python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round64/controls/ref-preflight-v3.py --root /fast/scratch/hyaku/chousa-r64/G02Probe13 --work /fast/scratch/hyaku/chousa-r64/G02Probe13/work-file
```

`--root` was the existing scratch directory; `work-file` was an existing regular file containing `fixture`.

Observed exit: **2**. Stdout: empty. Stderr:

```text
lane-preflight: --work /fast/scratch/hyaku/chousa-r64/G02Probe13/work-file is not a directory
```

**Result:** observed behavior matches the frozen refusal contract. Fixture recipe is preserved at `.ufo/waves/round-64/w1/G02Probe13/probe.txt`.

No candidate edits. No tools installed or updated. No build/tests/linters run. Scratch fixture remains to be removed before handoff.
