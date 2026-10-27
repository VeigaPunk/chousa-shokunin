# R58SentinelWriteScope — security hazard review of the candidate C1 patch

Seat: sentinel (write scope). Read-only on the lane; only write is this report; all probes in
`$S=/fast/scratch/hyaku/chousa-r58/R58SentinelWriteScope/` (removed before yielding). No fetch.

## Provenance observed

```
$ git cat-file -t 9e73a031ab1ac3bac343de008850d7d87f9e5634   -> commit
$ git rev-parse HEAD                                        -> 5da0a6375a554e1229492a8cb0b9695bd8e85456
$ sha256sum tools/build-spans.py .../controls/build-spans-r55.py
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  tools/build-spans.py
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  .../controls/build-spans-r55.py
$ sha256sum $S/c1-count.py -> 65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f
$ sha256sum $S/capture-text.py -> 2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573
```
**No candidate C1 patch exists in the lane**: `tools/build-spans.py` is still the round-55 pin
(= `R55_BUILDER_SHA`). I therefore reviewed *patch shapes*: `$S/cand.py` with
`NOSDCHECK=1 NOWRITE_ATOMIC=1 EXTRA=0` (`min` = exactly the behaviour the frozen battery demands)
and `EXTRA=1 NOSDCHECK=0` (`v2` = hardened: leaf+target+ancestor lstat, `nlink>1`, `O_NOFOLLOW`+
`fstat` bounded read, tempfile+`os.replace`).

## Gate status (independently reproduced, not a patch finding)

```
$ TMPDIR=$S EXTRA=0 NOWRITE_ATOMIC=1 NOSDCHECK=1 python3 -B c1-count.py --builder $S/cand.py --work $S/wmin --controls $S/controls
EMPTY_OK=pass  REBUILD_OK=pass  FOREIGN=pass(refused)  SYMLINK_OUT=pass(refused)
SYMLINK_CACHE=pass(refused)  FIFO_TXT=pass(refused)  DEVZERO_TXT=pass(refused)
FAT_RAW=pass(refused)  MANY_QUOTES=pass(refused)  ESCAPE_ENTRY=pass(refused)  HELDOUT_OK=pass
BEFORE_FOREIGN=deleted  CONTROL_REFUSEALL=denied  CONTROL_build-spans-r55=denied  DENIED=2/2
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=FAIL
```
12/12 legs pass, both controls denied, integrity `deleted`, yet `C1=FAIL`: `c1-count.py:391/399`
test `"=PASS"` while every refusal leg is emitted `=pass(refused)` (`:51`). The gate is
unsatisfiable as frozen (same as R58ScribeC1PatchNotes F1, re-observed here, `v2` too). Fix is at the
freeze layer; a builder must not be written to satisfy the uppercase token.

## Attack matrix — `$S/attack.py <shape>`, all fixtures under `$S/attack/`, victims inside `$S`

| attack (out-of-battery hazard) | `min` (battery-passing) | `v2` (hardened) |
|---|---|---|
| `spans/S501-1.txt` symlink → victim | rc=0 **victim=CLOBBERED** `b'Sentence 000 carries alp'` | rc=2 `SYMLINK refused: target spans/S501-1.txt`, intact |
| `spans.tsv` symlink → victim | rc=0 **victim=CLOBBERED** `b'id\turl\tcapture_sha256\tof'` | rc=2 `SYMLINK refused: …/out/spans.tsv is a symlink`, intact |
| `spans/` → symlink to empty foreign dir | rc=0 **wrote_outside=['S501-1.txt']** | rc=2 `SYMLINK refused: …/out/spans is a symlink` |
| `spans/` → symlink + foreign `S777-1.txt` | rc=1 FOREIGN refusal (audit sees through link), victim kept | rc=2 as above |
| `--out` ancestor (`anc`→`elsewhere`) | rc=0 **landed_in=['S501-1.txt','deep','spans','spans.tsv']** | rc=2 `SYMLINK refused: --out ancestor …/anc` |
| `--quotes` FIFO | rc=2 `no input` (no hang) | rc=2 `quotes NOT_REGULAR refused (FIFO/device)` |
| `--quotes` symlink → 900-row file | rc=0 **span_files=900** (followed) | rc=2 `quotes SYMLINK refused` |
| planned span target is a FIFO | **rc=TIMEOUT** no exit in 5 s | rc=2 `NOT_REGULAR refused: target spans/S501-1.txt` |
| span target hardlink to victim | rc=0 **victim=CLOBBERED** (inode truncated) | rc=2 `LINKED refused: … nlink>1`, intact |
| late-failure torn set (target is a dir) | rc=1 traceback, **manifest_replaced=True**, `stale_spans=['S503-1.txt']`, `S502-1.txt` missing | rc=2 pre-refusal, no write |
| `--cache` dir is a symlink | rc=0 (accepted) | rc=0 (accepted — residual) |
| one 100 MiB quote cell | rc=1, **child_peak_MiB=219** (row cap bounds rows, not bytes) | rc=2 `quotes SIZE refused … > cap 67108864` |
| 24×64 MiB distinct captures | rc=1, **child_maxrss_MiB=1619** | rc=1, **child_maxrss_MiB=1618** (no aggregate cap) |

TOCTOU (`$S/race.py`, 900 rows, symlink planted after `spans.tsv` appears):
```
swapper: planted symlink at spans/S900-1.txt after 0.0s
mode=v2wb rc=0 victim=CLOBBERED target_is_symlink=True     # check-then-open-by-path is racy
mode=v2   rc=0 victim=intact    target_is_symlink=False    # rename replaces the link
swapper: replaced out/spans with symlink->foreign after 0.0s
mode=v2/dir   rc=0 victim=intact foreign_entries=['S001-1.txt','S002-1.txt','S003-1.txt','S004-1.txt']
mode=v2wb/dir rc=0 victim=intact foreign_entries=['S025-1.txt','S026-1.txt','S027-1.txt','S028-1.txt']
```
The parent-directory swap defeats **both** hardened shapes at rc=0: every write re-resolves
`out/spans/…` by path after the one-time check, so 900 spans land in a foreign tree.

## Findings (severity / exploit / evidence / smallest remediation)

**S1 HIGH — output target identity is never checked; span text is attacker-chosen.**
Whoever can pre-create `out/spans/S###-N.txt` or `out/spans.tsv` (or `out/spans/`) as a symlink or
hardlink gets `Path.write_bytes` to follow it; the bytes are the span text derived from the capture, so
the write is **content-controlled** (`--cache` may itself be a symlink: last two rows above). Nothing in
the frozen battery covers an output target: `SYMLINK_OUT` only tests the leaf `--out`.
Remediation: write each output to `mkstemp` in the destination dir and `os.replace` (verified fixed:
`v2` column above); refuse `nlink>1` and non-regular targets before the write.

**S2 HIGH — containment is a single path-string check; the directory component is re-resolved per write.**
`spans/`→symlink passes the whole battery when it is empty (no orphan to trip the audit), and the
post-check swap of `out/spans` still lands 900 files outside at rc=0. Remediation: hold
`out = os.open(out, O_DIRECTORY|O_NOFOLLOW)` and do every create/rename/iterdir relative to that
dirfd (`dir_fd=`); a held dirfd removes both the symlinked component and the swap window.

**S3 HIGH — symlinked ancestor of `--out` makes "under `--out`" false.** Path comparison in
`expect_ok` cannot see it; writes land in the symlink target (observed). Remediation: lstat every
existing ancestor of `--out` and refuse a symlink (verified fixed in `v2`), or operate on the dirfd
from S2.

**S4 MEDIUM — unbounded write when a planned output is a FIFO (DoS, no corruption).** rc=`TIMEOUT`
(5 s), i.e. the open blocks forever; the battery's FIFO leg types only a *cache* input.
Remediation: include output paths in the same lstat/`O_NOFOLLOW`+`fstat` type gate.

**S5 MEDIUM — torn output set on late failure.** `spans.tsv` is replaced before the span files, so a
failure in between leaves a manifest describing a generation that is not on disk (observed: manifest
replaced, `S502-1.txt` missing, `S503-1.txt` stale). `--check` then reports STALE by design, but the
dir is left inconsistent and the exit path is a traceback. Remediation: write spans first and the
manifest last (it is the commit point), or stage a sibling temp dir and `os.replace` the directory.

**S6 LOW — memory is bounded per file, not in aggregate.** 24 distinct 64 MiB captures reach
1.6 GB RSS at rc=1; a single 100 MiB quote cell costs 219 MiB. claims.md excludes text-size caps, so
this is a residual, not a kill; note it as an unclaimed surface in the patch commit.

**S7 LOW — input identity is only half-checked.** `--cache` as a symlinked directory is accepted
(rc=0) and `--quotes` symlinks are followed unless the `EXTRA` gate is present; hardlinked inputs are
rejected only with the `nlink` check. Remediation: same dirfd discipline for `--cache`/`--quotes`.

**S8 EVIDENCE-SCOPE — the battery's containment assertion cannot see outside `out.parent`.**
`expect_ok` snapshots `out.parent` only (c1-count.py:142-146). A copy of the passing `min` builder with
one extra line writing `/fast/scratch/.../PWNED.txt` still yields `OK=4/4`, no leg flags it, and the
marker exists (`-rw-r--r-- 36 bytes`). "writes nothing outside `--out`" is therefore **unverified** by
this counter, and cannot be claimed from a `C1=PASS` receipt even after the case bug is fixed.

## Residuals not established / unrun

- Real cross-filesystem or bind-mount tricks, btrfs subvolume/snapshot interchange, `..` inside a
  capture path, and `capture-text` internals beyond `MAX_PART` — unrun (out of the declared battery).
- The exact patched `tools/build-spans.py` does not exist, so no finding here is a verdict on a
  specific patch: `min` proves *the battery is satisfiable by an exploitable builder*; `v2` proves the
  remediations above are sufficient for S1/S3/S4/S7 and insufficient for S2.
- `c1-count.py` case bug and `expect_refuse` `forbidden_touch` inversion (F4) reproduced/read only;
  no lane file modified. Round-57 r2 egress-scope L0 question untouched; no fetch.

VERDICT: the concrete attack "a builder that passes all 12 frozen C1 legs still writes outside `--out`"
**survives** — observed `spans/S501-1.txt` symlink → rc=0 `victim=CLOBBERED`,
`spans.tsv` symlink → rc=0 `CLOBBERED`, `spans/`→empty-dir symlink → 900 files outside via post-check
dir swap at rc=0, `--out` ancestor symlink → files in the target tree, span FIFO → unbounded hang, and
a `min` shape that writes a marker outside `out.parent` on all four safe legs is scored `OK=4/4`; the
frozen gate itself is unreachable (`REFUSE=0/7` from a lowercase/uppercase mismatch) and its
containment check is scoped to `out.parent`, so `C1` cannot be credited from this surface.
