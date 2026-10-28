# RevRefDiffGuards — round 61, wave w1 — reviewer report

Scope: `diff -u tools/build-spans.py corpus/evidence/round61/controls/ref-build-spans.py` (217 → 340 lines; diff exit 1), limited to `guard_out`, `_atomic_write`, `write_out`, their exit codes, and the `Forms._probe` / `get` / `_read` paths that feed them. Files checked: base sha256 `1ed2650a…c80bf6` (matches claims), ref sha256 `86d64c31…eccfd` (matches claims). No lane file written; `git status` on `tools corpus/evidence/round61 corpus/captures` clean after my runs. No installs. No network.

## Findings

### D1 — BLOCKING — a capture the contract refuses is built silently from its `.txt` sidecar
- Contract (ref docstring 16–19): a symlink out of the cache, a FIFO/device, an oversize or unreadable capture is a *refused row*; (10–13) the `.txt` sidecar is never used for an OLE/zip `.raw`.
- Code: `get()` lines 115–126. `_probe` marks the raw "bad" (112, 120), but line 124 `elif tk == "ok"` then reads the `.txt` whatever the reason the raw was bad. An oversize non-OLE raw also falls through (its head is not OLE, line 122 false).
- Reproduction (scratch fixtures, `python3 -B build-spans.py --quotes q.tsv --out o --cache cache`):
  - S1: `cache/<key>.raw` → symlink to an outside docx containing "OUTSIDE PHRASE ALPHA"; `cache/<key>.txt` = "TXT PHRASE BRAVO appears here."; quote "TXT PHRASE BRAVO". ref: `rc=0 SPANS_ROWS=1 WRITTEN=1`, span file = the txt text. base: `rc=1 build-spans: refused S001: quote occurs 0x in …raw`.
  - S2: `.raw` real docx, `chmod 0`, plus `.txt`. ref: `rc=0`, built from txt. base: PermissionError traceback, `rc=1`.
  - S16: `.raw` 65 MiB sparse, not OLE/zip, plus `.txt`. ref: `rc=0`, built from txt (base same: `rc=0`). Oversize-raw is a refused row by the docstring.
  - S3 (not a regression): `.raw` FIFO plus `.txt`: both ref and base `rc=0` from txt; the docstring says FIFO → refused.
  - Control, behaving as documented: S17 `.raw` with OLE magic, 65 MiB, plus `.txt`: ref `rc=1 refused S001: … is 68157440 bytes, over the 67108864-byte capture cap`.
- Reachability: the lane store holds real key pairs (`ls corpus/captures`: 129 files, 66 `.raw` and 63 `.txt`, several keys with both), so the state is reachable in the committed store.
- Counter gap (INFERENCE from `c1-count.py` legs): H13 OUTSIDE, H17 UNREADABLE, H18 FIFO build a `.txt`-only fixture, and H14/H15 are `.txt`/`.raw` size legs with no sidecar. None sets a bad `.raw` beside a good `.txt`, so C1 20/20 cannot see this. Routed as a counter limit under the claims' kill rule; the defect stands against the reference's own docstring.
- Direction (not applied): when `.raw` exists and is not `ok` (bad, unreadable, oversize) return the refusal; do not fall through to `.txt`.

### E1 — BLOCKING — output-guard filesystem calls are unguarded: a crash exits 1 (the "row refused" code); one old-caller regression
- `guard_out` line 266 `sd.iterdir()` and line 273 `m.read_bytes()` sit outside every try. The try in `write_out` (300–309) starts only after the guard returns. `Path.is_symlink`/`is_dir` at 260–265 can also raise on EACCES (INFERENCE; not isolated).
- S5: spans dir `chmod 0` after a good build: ref `rc=1 traceback=True PermissionError … /o-ref/spans`. base is also `rc=1` traceback (pre-existing class).
- S7 (regression): `spans.tsv` `chmod 0200` after a good build, rebuild with no flags: base `rc=0 SPANS_ROWS=1 WRITTEN=1`; ref `rc=1 traceback=True PermissionError … /o-ref/spans.tsv`.
- S7r: same with `--replace`: ref `rc=1 traceback` (`read_bytes` at 273 runs before the replace check at 274).
- Contract: ref docstring 44–45 says exit 2 is "usage/env or an output refusal"; exit 1 is "a row refused or STALE>0". A traceback exit 1 contradicts both.
- Good path, for contrast: S6 (out dir `chmod 600`): ref `rc=2 write failed … Permission denied` (caught in write_out).
- Same class outside the diff, non-blocking: `check()` now returns 2 for an unreadable `spans.tsv` (219–223, a fix), but `sd.iterdir()` (242) and `p.read_bytes()` (234) stay unguarded.
- Direction (not applied): route the guard's OSError through `_refuse` (exit 2).

### E2 — non-blocking — preflight does not check the kind of span paths; mid-write failure leaves a mixed state
- `guard_out` refuses symlinks at `spans/S###-N.txt` (269–270) but not other kinds. A directory at `spans/S002-1.txt` passes, since the name is in `files`.
- S14 (ref, `--replace`, dir at `S002-1.txt`): `rc=2 build-spans: write failed … Is a directory`; `spans.tsv` still the old 1-row manifest; `S001-1.txt` already overwritten with the new text; then `--check` → `SPANS_ROWS=2 STALE=2`, `rc=1`.
- S14b (base, no flag; base has no `--replace`): `spans.tsv` rewritten first, then `IsADirectoryError` traceback, `rc=1`, manifest 2 rows against the old span text. Ref's order (span files 302–303, manifest 304) is an improvement and `--check` detects its state. "A failed run never leaves a manifest without its spans" holds; "nothing written" is promised only for the enumerated refusals.

### E3 — non-blocking — leftover temp files are invisible and never removed
- `_atomic_write` names temps `.S001-1.txt.<hex>.tmp` (281). `SPAN_RE` (67) does not match a dotfile, so `guard_out` (266–272) and `check` (241–245) ignore them.
- S11: planted `spans/.S001-1.txt.0123456789ab.tmp`. `--check` → `SPANS_ROWS=1 STALE=0`, `rc=0`; rebuild → `rc=0`, file still present. (SIGKILL itself not run; the leftover shape was planted.)

### E4 — non-blocking — diagnostic: the `_probe` reason is discarded
- `get()` 127–130: a bad raw with no `.txt` falls to the generic message at 130.
- S4 (raw FIFO, no txt): `refused S001: no defined text form … (raw neither OLE nor zip, no .txt)`. S4b (raw `chmod 0`, no txt): the same text. The true cause ("is not a regular file", "unreadable") is lost.

### B2 — non-blocking — identical rebuild replaces `spans.tsv` (new inode, mode reset)
- `_atomic_write` creates a new file at 0644 (282) and `os.replace`s it (286).
- S9: `spans.tsv` `0664` → after ref rebuild `0644`, inode changed (1022512783 → 1022512830). base: mode `0664` kept, inode kept. Hard links break and modes are not preserved. Contract silent.

### B3 — non-blocking — rebuild silently replaces read-only span files
- S10: `spans/S001-1.txt` `chmod 0444`, identical rebuild: ref `rc=0`, replaced. base `rc=1` traceback (`write_bytes` on 0444). Lenient direction; unlikely to matter for lane files, but it is a change.

## Behaviour changes for old callers (checked; intended unless noted)
- B1 intended: a differing `spans.tsv` without `--replace` → ref `rc=2 … already holds a different spans.tsv; pass --replace` (S8); base `rc=0` overwrote silently. Orphan span files likewise refuse (277; not run).
- Exit 1 → 2 for write failures and unreadable `spans.tsv` in `--check` (base: uncaught traceback, exit 1).
- Symlink `DIR` is accepted and written through (S12: `rc=0`, `wrote_into_real=True`); a dangling `DIR` symlink is refused (`rc=2`). Contract is silent; consistent with "DIR is a directory".
- Positive: a symlink at a span path is refused, victim intact (S13: ref `rc=2`, `victim='VICTIM ORIGINAL'`); base wrote through it (`rc=0`, victim overwritten). Dangling span symlink refused (S13b).
- Positive: `os.replace` onto a symlink replaces the link, not its target (S0: `(dst_is_symlink=False, victim='VICTIM', dst='NEW')`, Python 3.14.8).
- Positive: `capture-text` import writes no bytecode (S15: ref no `__pycache__`; base wrote `capture-text.cpython-314.pyc`).
- Positive: `os.path.commonpath` on realpaths: S1 shows the symlink-out raw resolved as outside and was not read (ref took the txt path instead; see D1).

## Limits (not defects)
- L1 TOCTOU, named limit (i): guard (255–277) then write (295–310). `_probe` checks the realpath (96–97), but `raw.open` (117) and `read_bytes` (143) open the link path; a swap between the two is possible.
- L2 digest vs form from separate reads (code fact; race not run): `_read` digests `b` (143, 152) but for a raw the form comes from `self.ct.text_form(str(raw))` (123 lambda ignores `b`; 134–137), which reopens the path (capture-text.py 390–391). If the cache file changes in between, `capture_sha256` may not be the digest of the bytes the form was built from.
- L3 post-hoc form cap: `_read` checks `len(form)` (150–151) after `to_form` (147) has built the form. H20 receipt `rss_kib=221588` for a 70 MiB form (`controls/c1-reference.txt`, seed 61001). Peak memory for a form near the 256 MiB inflate cap of capture-text is not bounded by the 64 MiB builder cap (INFERENCE; not run at that size).
- L4 round-56 gate: `corpus/evidence/round56/c1-gate.py --tool <builder> --seed 7` exits 2 `ENV_CHANGED pinned capture 54fe0734c01f699e735b4b0a digest` for base and ref alike on this host. Its legs were not exercised by me for either builder. Its call sites build into fresh `--out` dirs (c1-gate.py 204, 420–421), so the guard does not trip for them (code reading).

## Verified, no defect
- `regress.py`, real sets, run by me: ref `REAL_REBUILD=3/3`, exit 0 (round55, round56, round57/c3 each `check_rc=0 build_rc=0 identical=True pass`); base also `REAL_REBUILD=3/3`, exit 0.
- Refusal paths write nothing: S8, S12 (dangling), S13 (victim intact), S13b.
- Python 3.14 `pathlib.is_symlink` on dangling links: a dangling span symlink is refused as "is a symlink" (S13b), so `is_symlink` returns True for dangling.
- Exit-code map of ref: 0 built; 1 row refusal (`sys.exit(1)` in `build`, 152–153) or `STALE>0`; 2 `_refuse` (250–252), write `OSError` (308–309), unreadable `spans.tsv` in check (222–223), usage/env (195–197, 323–324); uncaught exception → 1 (E1).

## Commands run (scratch fixtures under /fast/scratch/hyaku/chousa-r61/RevRefDiffGuards, deleted before yield)
- `diff -u tools/build-spans.py corpus/evidence/round61/controls/ref-build-spans.py` → exit 1, 217→340 lines.
- `sha256sum` of base copy, ref copy and the controls file → `1ed2650a…`, `86d64c31…`, `86d64c31…`.
- `python3 -B corpus/evidence/round61/regress.py --builder <ref copy> --work <scratch>/regress-ref` → `REAL_REBUILD=3/3`, exit 0; same with base → `REAL_REBUILD=3/3`, exit 0.
- Probe driver S0–S17 (above), run with `python3 -B`, the builder copies sitting beside a `capture-text.py` copy. Each result quoted above is that run's `rc`, traceback flag and last stderr/stdout line.
- `corpus/evidence/round56/c1-gate.py --tool <ref|base> --seed 7` → `ENV_CHANGED …`, exit 2 (both).
- Read-only: `ls corpus/captures`, `grep` of callers, `git -C … status --short` (clean).

Reproduce D1 (one line each): `ln -s outside.docx cache/<key>.raw; printf 'TXT PHRASE BRAVO\n' > cache/<key>.txt`, then `python3 -B tools/build-spans.py --quotes q.tsv --out o --cache cache` with the ref → exit 0 (base → exit 1). Reproduce E1: `chmod 0200 o/spans.tsv` after a good build, rebuild → ref exit 1 traceback, base exit 0.

## Verdict
VERDICT: REF_DEFECTS=7 blocking=2
