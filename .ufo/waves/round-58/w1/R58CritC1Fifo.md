# R58CritC1Fifo — FIFO/device refusal attack

## Counterexample and evidence

Target is the frozen C1 FIFO_TXT and DEVZERO_TXT legs, including their permitted reason-token sets. I ran the frozen counter from a scratch copy against a scratch copy of the lane-pinned builder (no lane writes):

```text
set -eu; SCR=/fast/scratch/hyaku/chousa-r58/R58CritC1Fifo; mkdir -p "$SCR"; trap 'rm -rf "$SCR"' EXIT; cp /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round58/c1-count.py "$SCR/c1-count.py"; cp /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py "$SCR/build-spans.py"; mkdir -p "$SCR/controls" "$SCR/work"; cp /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round58/controls/build-spans-r55.py "$SCR/controls/build-spans-r55.py"; cd "$SCR"; timeout 420s env TMPDIR="$SCR" PYTHONDONTWRITEBYTECODE=1 python3 -B "$SCR/c1-count.py" --builder "$SCR/build-spans.py" --work "$SCR/work" --controls "$SCR/controls"
```

Exact output for the two legs and summary:

```text
FIFO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'FIFO', 'REGTYPE', 'SYMLINK'] absent in 'build-spans: refused S571: no defined text form for f4088c6d6da1f4763182a51d (raw neither OLE nor zip, no .txt)\n')
DEVZERO_TXT=fail(rc=1, reason ['NOT_REGULAR', 'SIZE', 'SYMLINK', 'REGTYPE'] absent in 'build-spans: refused S581: no defined text form for a172f04219497476db868414 (raw neither OLE nor zip, no .txt)\n')
SUMMARY OK=3/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=1/1
C1=FAIL
```

Both subprocesses returned promptly; neither hit its frozen 20-second timeout. They were refused, but the builder reports the generic “no defined text form” reason, outside both frozen token sets. The pinned builder is the before-builder (the lane's `tools/build-spans.py` sha256 is `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`), so this is a before-state failure, not evidence about an as-yet-unseen hardened candidate.

I also probed a FIFO at the raw cache path with a 5-second external timeout. Exact command:

```text
set -eu; SCR=/fast/scratch/hyaku/chousa-r58/R58CritC1Fifo-rawprobe; mkdir -p "$SCR"; trap 'rm -rf "$SCR"' EXIT; cp /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py "$SCR/build-spans.py"; mkdir -p "$SCR/cache" "$SCR/out"; url=https://fixture.example/rawfifo; key=$(printf %s "$url" | sha256sum | cut -c1-24); mkfifo "$SCR/cache/$key.raw"; printf 'id\\turl\\tquote\\tentry\\nS571\\t%s\\tquote\\tcorpus/evidence/x.md\\n' "$url" > "$SCR/quotes.tsv"; cd "$SCR"; timeout 5s python3 -B "$SCR/build-spans.py" --quotes "$SCR/quotes.tsv" --out "$SCR/out" --cache "$SCR/cache"; rc=$?; printf 'RAW_FIFO_RC=%s\\n' "$rc"
```

Observed output: `build-spans: refused S571: no defined text form for c647ba2bf99fab1a068810af (raw neither OLE nor zip, no .txt)`; exit 1 (not a timeout). This rules out a raw-FIFO hang in the inspected base builder: `Path.is_file()` excludes the FIFO before `raw.open()`.

## Assessment

- **Operability axis:** frozen FIFO_TXT and DEVZERO_TXT legs are not satisfied by the pinned builder; both fail their frozen reason-token assertions. On these fixtures this is a diagnostic/leg failure, not a hang or accepted input.
- The frozen DEVZERO fixture is a symlink to `/dev/zero`. In this builder, `.is_file()` follows the symlink and returns false for the character-device target, so the builder skips opening/reading it and emits the same generic refusal. Thus this observed pass-through path does not establish an unbounded device read, nor does the fixture demonstrate the direct-character-device path. No direct device-node test was run.
- The raw-FIFO probe is additional coverage only; it is not a frozen leg. It did not hang. I did not test a FIFO supplied as `--quotes` (outside the named FIFO_TXT cache fixture).

**Smallest safe correction:** in the builder's cache inspection, explicitly classify non-regular entries before reading and emit one of the frozen recognized reason tokens (`NOT_REGULAR`, `FIFO`, `REGTYPE`, or `SYMLINK` as appropriate). Keep the frozen predicates unchanged. A separate direct-device test would be needed to claim device-read behavior beyond the symlink fixture; no safe direct-device fixture was available/run here.

Checks not run: no candidate/hardened builder was available at the lane source path during this attack; no direct character-device entry was tested; no live fetch. Scratch was removed by the registered shell traps.

VERDICT: FALSIFIED — the pinned before-builder's FIFO_TXT and DEVZERO_TXT refusals violate the frozen reason-token assertions; both finish promptly, with no observed hang. The raw-cache FIFO probe also refused promptly.