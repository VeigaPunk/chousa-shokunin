# R58ScribeC1PatchNotes — implementation note for the C1 build-spans hardening

Seat: scribe, prose advice only. No lane/judge edit, no commit, no fetch; my only read targets were the
frozen files below, my only write is this report. Judged axis: operability (C1).

## Provenance actually observed

- Lane HEAD: `9e73a031ab1ac3bac343de008850d7d87f9e5634` (freeze) at first read, then `718e8d2`, then
  `5da0a63` (control receipts and the C2 baseline only). `c1-count.py` sha256 is `65da18bb…` at all three
  commits, so every counter line number below is frozen.
- Base builder is still the round-55 pin, unhardened: `sha256sum tools/build-spans.py` →
  `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6` = `controls/build-spans-r55.py` =
  `R55_BUILDER_SHA` (:41). No C1 patch has landed.
- Receipts `controls/c1-before.txt` / `c1-controls.txt` (committed, not re-run by me): `C1=FAIL`,
  `OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted`, `DENIED=2/2`; per-leg text matches the base code
  (FIFO/DEVZERO → `no defined text form …`, FAT_RAW → `ole-malformed` after 80 MiB, others exit 0).
- `corpus/captures/` has no symlinks (S101 raw: 129,024 B regular file), so a per-entry symlink/size gate cannot break `HELDOUT_OK`.

## Blocker first: the frozen aggregator makes `C1=PASS` unreachable

`c1-count.py` formats every refusal leg with lowercase `PASS = "pass"` (line 51; append sites 160, 223,
234, 315) but aggregates with uppercase: `ref_pass = all(("=PASS" in l) for l in ref_legs)` (391) and
`SUMMARY … REFUSE={sum('=PASS' in l …)}` (399). `"=PASS"` is never a substring of `"NAME=pass(refused)"`
and `ref_legs` always has 7 members, so `ref_pass` is False for **every** builder. Observed with a stub
meeting all seven leg predicates and nothing else (`python3 -B corpus/evidence/round58/c1-count.py
--builder $S/stubE.py --work $S/runE`, `$S` = my scratch):

```
FOREIGN=pass(refused)
SYMLINK_OUT=pass(refused)
SYMLINK_CACHE=pass(refused)
FIFO_TXT=pass(refused)
DEVZERO_TXT=pass(refused)
FAT_RAW=pass(refused)
MANY_QUOTES=pass(refused)
BEFORE_FOREIGN=deleted
SUMMARY OK=1/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0
C1=FAIL                      (exit 1)
```

Consequence: no hazard-refusing builder — hardened or not — can print the `C1=PASS` that claims.md C1
requires; the 3/10 gate is unsatisfiable as frozen, and the mismatch is in the counter, not in
`tools/build-spans.py`, so it belongs to the integrator (391/399 lowercased, or refusals uppercased).

## Patch note: refusal classes, exactly as the battery tests them

Reason tokens match case-insensitively as substrings of `stderr + stdout` (c1-count.py:160-166); FOREIGN is stricter — `err[:200]` of `stderr` (215-223).

| leg | fixture | token(s) that satisfy it | required behaviour |
|---|---|---|---|
| `FOREIGN` | `out/spans/S777-1.txt`, then a 2-row rerun | `777` or `foreign` in first 200 chars | rc≠0, foreign file still present |
| `SYMLINK_OUT` | `--out` is a symlink to an empty `realdir` | `SYMLINK` (see F3: leg does not discriminate) | rc≠0, `realdir/` stays empty |
| `SYMLINK_CACHE` | `cache/<key>.txt` symlink → regular file | `SYMLINK`, `REGTYPE`, `NOT_REGULAR` | rc≠0 |
| `FIFO_TXT` | `cache/<key>.txt` is a FIFO | `NOT_REGULAR`, `FIFO`, `REGTYPE`, `SYMLINK` | rc≠0 within 20 s, never opened |
| `DEVZERO_TXT` | `cache/<key>.txt` symlink → `/dev/zero` | `NOT_REGULAR`, `SIZE`, `SYMLINK`, `REGTYPE` | rc≠0 within 20 s |
| `FAT_RAW` | 80 MiB sparse OLE-headed `<key>.raw` | `SIZE` (only) | rc≠0 within 60 s, no full read |
| `MANY_QUOTES` | `quotes.tsv` header + 100,001 rows | `SIZE`, `ROWS`, `CAP` | rc≠0 within 90 s, nothing written |
| safe: `EMPTY_OK`/`REBUILD_OK`/`HELDOUT_OK`/`ESCAPE_ENTRY` | 3 rows / rerun / S101 store / `../escape.md` entry | — | rc=0 with exact spans, byte-identical rerun; ESCAPE_ENTRY rc≠0 and no `out-esc/spans.tsv` |

Design rules that follow from the fixtures, in the order they must run:

1. **Row cap before parsing** (`MANY_QUOTES`): count non-empty data lines and refuse above 100,000 with a
   token, e.g. `quotes.tsv rows 100001 > cap 100000 (ROWS)`; base (`read_quotes`, :99) reads all, then
   builds 100,001 span files (receipt: rc=0) instead of refusing.
2. **Symlink check before any `mkdir`** (`SYMLINK_OUT`): `out.is_symlink()` must refuse *before*
   `sd.mkdir(parents=True)` (build-spans.py:202); a stub that merely created `out/spans` through the
   link already scored `SYMLINK_OUT=fail(…)(target-dir-written!)`.
3. **Type before size, size before read** (`FIFO_TXT`, `DEVZERO_TXT`, `FAT_RAW`): `lstat`/`O_NOFOLLOW`,
   then `fstat` on the returned fd; non-`S_ISREG` → `NOT_REGULAR` (or `FIFO`); then `st_size > 64 MiB`
   → `SIZE`; then a bounded `read(SIZE_CAP + 1)`. Order is load-bearing: `/dev/zero` has `st_size = 0`
   (`stat -c '%n size=%s mode=%F' /dev/zero` → `size=0 mode=character special file`), so a size-only gate
   passes and the following `read_bytes()` never returns; FIFOs are rejected without an `open` (20 s
   timeout, 262). Base `Forms.get` (67-93) type-tests nothing (`read_bytes()` at 80 and 86).
4. **Foreign/orphan audit before the unlink loop** (`FOREIGN`): after the whole plan is in memory, scan
   `out/spans` for `SPAN_RE` names (build-spans.py:36) not in `files` and refuse, naming each; the rerun
   leaves both `S503-1.txt` (own orphan) and `S777-1.txt` (foreign), so name them inside the first 200
   chars of stderr. The leg checks only that the foreign file still exists — not its bytes, not other
   span files — so the gate precedes *every* write, not just the unlinks (base: 204-205 then 206).
5. **Containment**: write only under `--out`; no persistent temp files (the counter diffs everything
   outside `--out` at 142-146, though its snapshot skips symlinks/dirs and `HELDOUT_OK` snapshots only
   after the build), no `.txt` sidecar in `--cache`, no child process without `-B` (`__pycache__`).
6. **Preserve the documented span contract**: `start = max(0, off - CONTEXT)`, `span =
   text[start:off+len(quote)+CONTEXT]` (build-spans.py:142-143), defined text form via the imported
   `capture-text.py` (56-93). Implement the docstring formula, not the counter's (c1-count.py:136 agrees
   only at `off == 0` or `off >= 160`; see F6). Keep the `..`/absolute entry refusal (116).

Output ordering the battery observes: (1) input validation on stderr, exit 2, nothing written (95-124);
(2) every row's refusal collected, then one `build-spans: refused <id>: <reason>` each, exit 1, nothing
written (127-153); (3) the new foreign/orphan gate, exit 1, nothing deleted; (4) only then unlink orphans
→ write `spans.tsv` → write span files (202-208); (5) success prints `QUOTE <id> char <N> <span_file>`
in input order, then `SPANS_ROWS=n WRITTEN=n` (211-212). `--check` stays read-only; exit codes 0/1/2 stay
distinct (docstring 34-36), though the counter only tests `rc == 0`.

## Intentionally unclaimed (state these in the patch commit)

- TOCTOU between `lstat`/`fstat` and the read of a *different* path, and between the foreign audit and
  the write loop: a name created after the audit is overwritten if it is in the plan; only the leaf
  `--out`/`--cache` path is type-checked, not its ancestors; concurrent runs into one `--out` are
  unlocked, last-writer-wins.
- Memory: `Forms.memo` (76, 100) keeps one form per URL; the 64 MiB cap is per capture on `st_size` (a
  file at the cap is read fully, growth after `fstat` bounded by `cap + 1`), not aggregate; `quotes.tsv`
  is row-capped, not byte-capped — claims.md excludes text-size caps.
- Not claimed: `capture-text` defects (the base FAT_RAW receipt shows `ole-malformed`), UTF-8
  replacement behaviour, quote ambiguity across forms, btrfs/reflink or mount-level tricks.

## Findings (frozen files; reported, not fixed)

- **F1 (decisive).** `C1=PASS` is unreachable: lowercase leg formatting (51/160/223/234/315) vs uppercase
  aggregation (391/399); observed 7/7 legs passing with `REFUSE=0/7`, `C1=FAIL`.
- **F2.** `c1-count.py:212` presumes `out-empty/spans/` exists (created only by a successful `EMPTY_OK`),
  so an early-refusing builder crashes the counter with `FileNotFoundError` instead of printing `C1=FAIL`
  (observed) — `CONTROL_REFUSEALL=denied` is denial-by-crash; `BEFORE_BUILDER` also resolves under
  `HERE/controls` (42, 350), not `--controls`, so a copy without a sibling `controls/` is `absent`.
  The receipt's `DENIED=2/2` therefore mixes mechanisms: the r55 control prints `C1=FAIL` (genuine
  denial), REFUSEALL yields zero `C1=` lines and a traceback (measured by `R58ExecC1CounterAudit`).
- **F3.** `SYMLINK_OUT` does not discriminate: correct refusal → `SYMLINK_OUT=pass(refused)` (lowercase,
  still a `ref_pass` False); writing through the link → `SYMLINK_OUT=pass(refused)(target-dir-written!)`
  (observed); exit-0-and-write-nothing → `pass(refused)` at 233-234. The annotation is never read.
- **F4.** `expect_refuse` requires `forbidden_touch` paths to *exist* (161-164); for `SYMLINK_OUT` it is
  passed `realdir/spans.tsv`, which cannot pre-exist, so that leg's message is inverted and then
  overwritten at 233-237 — the root of F3.
- **F5.** The integrity/control legs read `controls/build-spans-r55.py` and `controls/REFUSEALL.py`,
  absent at the freeze commit `9e73a03` (added in `718e8d2`); sha256-pinned, so a provenance caveat only.
- **F6 (span window).** `c1-count.py:136` computes `offset + len(q) + min(CONTEXT, offset) + CONTEXT` against the builder contract `off + len(q) + 80` (build-spans.py:142-143). Recomputed over `off` 0..399
  at qlen 20: they differ for `off` 1..159 (short by up to 159 B; `off=26` → 126 B vs 100 B) and agree
  only at `off == 0` or `off >= 160`, so a correct builder fails `EMPTY_OK` below quote offset 160 —
  reproduced by `R58ExecC1CounterAudit` (seeds 35/104/138/140/248/275). The counter must change.

## Unrun by me

- Unrun: the frozen counter against a hardened builder (none exists; safe-leg compatibility above is
  design-level, off the counter's assertions at 120-146); `c2-count.py`; the round-57 r2 egress-scope L0
  question; no fetch. My `$S` scratch is removed.

VERDICT: the attack "satisfy the frozen C1 build-spans hazard battery with a non-writing, type/size-
bounded builder" is **falsified at the gate**: `c1-count.py:391/399` require uppercase `=PASS` while
every refusal leg is emitted lowercase (`:51`), so `C1=PASS` is unreachable for any builder (observed
7/7 legs passing, `REFUSE=0/7`, `C1=FAIL`). The patch design itself (classes and ordering above) is
stated but unexecuted against the gate — inconclusive until the counter case mismatch is resolved by
the L1/integrator.
