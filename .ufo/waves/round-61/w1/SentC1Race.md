# SentC1Race — TOCTOU review of the reference span builder (C1 limit i)

Target: `corpus/evidence/round61/controls/ref-build-spans.py`, sha256 `86d64c312e1640d4…` (matches claims.md `86d64c31…eccfd`).
Question: guard_out() tests DIR, then write_out() writes. What does a second process achieve by swapping
`out/spans` for a link, or planting a symlinked span file, in that window? Does O_NOFOLLOW|O_EXCL stop it? Minimal fix and cost.

## Method (measured, not argued)

- Scratch copy only (lane not touched). The builder is run as a child process; the driver is a second process.
  A hook is inserted in write_out() right after guard_out() returns: the child writes `after_guard.ready`
  and blocks until the driver writes `after_guard.go`. The driver applies one attack in that window, then releases.
  The window is therefore deterministic (no sleep race).
- Victim = a directory outside `out` that the builder's user can write. An escape = the victim tree gains,
  changes or loses an entry. Snapshot = lstat-level walk (file sha256 / link target / dir).
- Builders: `ref` (shipped code, hook added); `refnoflag` (same, O_NOFOLLOW|O_EXCL removed);
  `f2dirfd` (candidate: pinned dir fds, see Fix); `f3stage` (candidate: private stage dir + path renames).
- The temp-name token is fixed to `cafe00000000` by env in the harness for every build, so a planted temp name
  is predictable. This is a harness choice, used only to test whether the flags stop that route. In production
  the token is `secrets.token_hex(6)` (48 bits, unguessable).
- Run in an in-kernel Python harness (scratch `/fast/scratch/hyaku/chousa-r61/SentC1Race`, deleted afterwards;
  the output below is the evidence). The first harness run aborted on my own slice-index bug (indices taken
  from the unhooked source); fixed, rerun; the numbers below are from the rerun only. No installs. No git.

## Results — reference builder (`ref`)

| scenario | attack in window | rc | escape | observed |
|---|---|---|---|---|
| T0 happy | none | 0 | no | 2 span files + spans.tsv written in out |
| T1 dirlink | `out/spans` absent at guard; then symlink `out/spans -> victim/` | 0 | **YES (write)** | created `victim/S001-1.txt`, `victim/S002-1.txt` |
| T2 dirlink+orphan | real `out/spans/S777-1.txt` (orphan, `--replace`); swap dir for link to victim holding `S777-1.txt` | 0 | **YES (write+delete)** | created ×2; **removed `victim/S777-1.txt`** |
| T3 plant span | `out/spans/S001-1.txt` replaced by symlink to `victim/victim.txt` | 0 | no | victim unchanged (os.replace replaces the link entry) |
| T4 plant orphan | orphan name replaced by symlink to victim file | 0 | no | victim unchanged (unlink removes the link) |
| T5 plant manifest | `out/spans.tsv` symlink to victim file | 0 | no | victim unchanged (replace swaps the link) |
| T6 out swap | `out` renamed away; `out` symlink to victim | 0 | **YES (write)** | created `victim/spans/`, `spans/S001-1.txt`, `spans/S002-1.txt`, `spans.tsv` |
| T7 temp plant | symlink at `out/spans/.S001-1.txt.cafe00000000.tmp` → victim file | 2 | no | `[Errno 17] File exists` (O_EXCL) |
| R1 prelink | `out/spans` symlink before run | 2 | no | refused; out unchanged |
| R2 manifest | differing spans.tsv, no `--replace` | 2 | no | refused; out unchanged |

Answers:
- **Which writes escape:** every write whose path resolves *through a directory* that the attacker turned into a link
  (T1, T2, T6). Span-name files and spans.tsv land in the link target; in T2 a same-named victim file is also deleted.
  Impact is confused-deputy: an actor who can change entries in `out`'s parent makes the builder (which can write the
  target) create files named `S###-N.txt` with cache text, and delete `S###-N.txt` files there. No arbitrary names or content.
- **Planted symlinked span file / manifest / orphan (T3–T5):** no escape. `os.replace` and `unlink` act on the directory
  entry and never follow a final-component link. The claim's "limit (i)" therefore applies to directory swaps, not file plants.
- **O_NOFOLLOW|O_EXCL on the temp file:** checks only the final component. It does not stop T1, T2 or T6 (refnoflag
  escapes the same three). It stops only T7, which needs a predicted temp name; with the real 48-bit token that is
  not reachable. Dropping the flags does open T7: refnoflag T7 rc=0, `victim.txt` overwritten (escape).

## Candidate fix A — pin directories with fds (`f2dirfd`, measured)

Open `out` with `O_DIRECTORY|O_NOFOLLOW`, open/create `spans` the same way with `dir_fd`; do every guard check with
`listdir(sfd)` and `stat(name, dir_fd=…, follow_symlinks=False)`; create temp files with `dir_fd` + `O_EXCL|O_NOFOLLOW`;
`os.replace(…, src_dir_fd=, dst_dir_fd=)`; `os.unlink(name, dir_fd=)`. Measured:
- T1 → rc 2 `spans appeared during the run (File exists)`; victim unchanged. Fails closed.
- T2 → rc 2 `write failed … No such file or directory` (pinned dir was removed by the attacker); victim unchanged.
- T6 → rc 0; files land in the **original** out inode (`out.bak/spans/S001-1.txt` present), victim unchanged. Misdirected, not escaped.
- T3, T4, T5, T7 → unchanged, no escape.
- Happy path T0: out tree (all bytes) and stdout identical to `ref` (`True`/`True`); R1, R2 refusals identical (rc 2, nothing written).
- Cost: 117 changed lines (+/- by difflib vs the hook-only base; the count includes the rewritten guard, since guard_out
  and _atomic_write are replaced). I did not measure a leaner variant. Linux/POSIX only (`dir_fd`). Behaviour change:
  a racing swap now fails with exit 2 instead of writing. No new dependency.

## Candidate fix B — private temp dir + path rename (`f3stage`, measured) — does NOT fix

Stage all files in `out/.stage-*`, then `os.replace(stage/…, out/…)` by path: T1 escapes (2 files), T2 escapes
(2 files + delete), T6 escapes (4 entries). Cost 19 changed lines; no benefit. The rename destination is still resolved
through the link.
- Whole-directory rename variant (not used by f3stage; checked with the kernel directly): `rename(stage/spans, out/spans)`
  when `out/spans` is a symlink → `Not a directory` (fails closed); when `out/spans` is a non-empty real dir → `File exists`.
  So an atomic swap of the span dir needs the old dir removed first, which reopens a window. Fix B is not viable without fds.

## Limits of this measurement

- One attack window (after guard). The fd design makes every later operation relative to pinned fds, so the other
  windows (between mkdir and writes, between writes) should close too — INFERENCE, not measured separately.
- Read side not measured: `Forms._probe` then `read_bytes()` on cache files is also check-then-use. Out of this item's scope (writes).
- The fixed temp token exists only to test the flag; it is a harness choice.
- Happy-path equality is one two-row fixture, not the C1 counter. I did not run `c1-count.py` or `regress.py` (not my assignment).
- The C1 20 legs contain no TOCTOU leg, so a `C1=PASS` does not evidence T1/T2/T6 either way.

## Verdict inputs

Reference escapes in 3 of the 8 attack scenarios (T1, T2, T6); the 3 cases are the write/delete paths through a swapped directory.
Flags do not cover them. Fix A stops them with equal happy-path output at ~117 changed lines; Fix B does not stop them.

VERDICT: TOCTOU_ESCAPES=3 fix=pin out and out/spans as dir fds (O_DIRECTORY|O_NOFOLLOW), do every check, temp create, replace and unlink via dir_fd
