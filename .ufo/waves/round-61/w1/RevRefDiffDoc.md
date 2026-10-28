# RevRefDiffDoc — docstring-scoped review of `controls/ref-build-spans.py` vs `tools/build-spans.py`

Seat: reviewer (leaf, no dispatch). Lane writes: this file only. Scratch `/fast/scratch/hyaku/chousa-r61/RevRefDiffDoc` (removed before yield).
Inputs checked: claims.md sha256 `9afec8d4…0ace` matches the wave spec. Reference `controls/ref-build-spans.py` sha256 `86d64c31…eccfd` matches the C1 receipts. Base `tools/build-spans.py` sha256 `1ed2650a…c80bf6` matches `c1-before.txt`. Python 3.14.8.

## Findings (severity order)

### RD1 — BLOCKING. The `.raw` gate falls through to `.txt` for every `.raw` it refuses to read
- Code: `_probe` returns `bad` for an outside-cache link (98), unreadable (102), non-regular (104); `get()` ignores a bad raw and takes `elif tk == "ok"` (124), so the `.txt` sidecar is read. Oversize non-magic raw also falls through (140 is only reached when magic matches).
- Docstring sentences falsified: lines 16–19 ("a symlink out of the cache, a FIFO or device, an oversize or unreadable file is a refused row, decided before any byte is read") and lines 9–12 ("the `.txt` sidecar is never used for such a capture").
- Reproduction (fixture: `tools/` = ref builder + lane `capture-text.py`, cache key K = sha256(url)[:24]; `.txt` = text with the quote once; quotes row `S001 <url> THE QUOTE TEXT here. corpus/x.md`):
  - A: `mkfifo cache/K.raw` + valid `K.txt` → `rc=0`, `QUOTE S001 char 192`, row from the `.txt`.
  - B: `ln -s outside.bin cache/K.raw` (outside.bin = OLE magic + junk) + valid `K.txt` → `rc=0`; manifest `capture_sha256` = sha256 of the `.txt` (`7c76c4da1d61`). **Base: `rc=1`, `refused S001: capture-text refused … ole-malformed`.** Refused → accepted from a different source: an observable change for old callers.
  - C: `K.raw` mode 000 (OLE magic) + valid `K.txt` → `rc=0`. **Base: `rc=1` uncaught PermissionError traceback.**
  - D: `K.raw` 65 MiB sparse, non-magic + valid `K.txt` → `rc=0` (inherited from base; the sentence is new in the candidate).
- Counter coverage: none. `grep -n '\.raw' c1-count.py` → lines 203 (P02 valid docx), 491 (H15 OLE oversize, refused by size), 557 (H20 valid zip). No leg presents a FIFO, outside link, unreadable, or non-magic oversize `.raw`. C1 = 20/20 cannot see RD1. Per claims.md kill rule this is a **counter limit to route**, not a refutation of C1; but the landed docstring is false and the candidate changes base behaviour (B, C).
- Fix sketch: if `lexists(raw)` and the raw is not an ok regular file, refuse (do not fall through); refuse any raw over the cap before the magic sniff, or refuse oversize regardless of magic. Add legs for A–C.

### RD2 — non-blocking, inherited. "exactly once" counts non-overlapping occurrences
- Line 195 `n = text.count(quote)`. `"aaa".count("aa") == 1`.
- Repro E: txt `head words here. aaa tail …`, quote `aa` → `rc=0`, `QUOTE S001 char 17` although `aa` also occurs at 18.
- The counter shares the blind spot (`c1-count.py:220 assert form.count(quote) == 1`). Fix: count overlapping occurrences (lookahead regex or find-loop).

### RD3 — non-blocking, introduced. Environment failure reported as a per-row capture-text refusal
- Lines 136 (`self.ct = _capture_text()`) run inside the `try` at 146–149 (`except Exception`).
- Repro P-ref: `tools/capture-text.py` removed, zip-magic raw → `build-spans: refused S001: capture-text refused …: [Errno 2] No such file…`, `rc=1`. Base: uncaught traceback, `rc=1`. Docstring line 44–45 says env failure is exit 2; neither matches.
- Fix: perform the import outside the per-row try.

### RD4 — non-blocking, introduced. Refusal reason changes for dangling, looping or outside `.txt`
- F (`K.txt` → dangling link outside cache): ref `refused S001: …txt resolves outside the cache`; base `no defined text form for K`. Both `rc=1`.
- G (`K.txt` → itself): ref `…txt unreadable (Too many levels of symbolic links)`, `rc=1`.
- Docstring line 15 ("neither: a refused row (no defined text form)") is not matched for a dangling link. Message-only change; no exit-code change.

### RD5 — non-blocking, introduced. Output guard does not check the kind of span-named entries
- Guard loop lines 266–272 checks only `is_symlink()` for `S###-N.txt`; a directory of that name passes.
- I: `out/spans/S002-1.txt/` (directory), two rows → `rc=2`, `write failed … Is a directory`; `spans/S001-1.txt` already written, no `spans.tsv`. The tree is left partial. Docstring line 34–40 says refusal writes nothing, but this path is not an enumerated refusal, so no sentence is false there.
- K: orphan directory `spans/S009-1.txt/` with `--replace` → `rc=2` **after** the new `spans.tsv` is written; the directory remains. Exit 2 is documented as "usage/env or an output refusal above" (lines 44–45); this is neither.
- Fix: refuse any non-regular entry matching SPAN_RE in `guard_out`.

### RD6 — non-blocking, introduced. Identical manifest allows silent overwrite of a changed span file
- Lines 273–276 compare only `spans.tsv`. J: hand-edit `spans/S001-1.txt` → `--check` `SPANS_FILE_STALE … STALE=1` (rc 1, detected); then plain rebuild → `rc=0`, span restored silently.
- Docstring is silent on this case (it says "a span file this run does not write"); the counter has no leg (H07, H09 only). Coverage gap; not a false sentence.

### RD7 — non-blocking, inherited. Non-UTF-8 quotes file is a traceback, not exit 2
- Line 159 `path.read_text(encoding="utf-8")` is unguarded (called from line 325). Repro O: `caf\xe9` in quote → `Traceback …`, `rc=1`. Docstring 44–45 says usage/env → exit 2. Base identical.

### RD8 — non-blocking, inherited. Quote is silently trimmed
- Line 171 `c.strip()` on every cell. Repro N: quote `"  THE QUOTE TEXT here.  "` → manifest quote cell `THE QUOTE TEXT here.`, `rc=0`. Docstring says "one quote per row" and "the quote must occur exactly once", not that it is trimmed.

### RD9 — nit, introduced, code-read only (INFERENCE from line order)
- Lines 117–118 read 8 bytes of `.raw` before the size refusal in `_read` (140). Docstring line 18 says "decided before any byte is read". Not run.

### RD10 — INFERENCE, not reproduced
- `_probe` stat (99–104) and the later open/`read_bytes` (117, 143) are separate calls; a FIFO swapped in between blocks until the counter's 60 s kill. Named limit (i) covers swaps only.

## Sentence → code → leg (docstring behaviour sentences)
| Sentence (ref docstring line) | Code (ref line) | Leg |
|---|---|---|
| `.raw` OLE/zip → capture-text stdout, imported, no bytecode (9–11) | 76–84, 134–137 | P02, P03 (run without -B: ref leaves `tools/` = builder + capture-text; base leaves `__pycache__`) |
| raw capture-text refusal → refused row (12–13) | 146–149 | **none** (reproduced by hand: H, rc 1, `capture-text refused`) |
| `.txt` UTF-8 replace, universal newlines (14) | 126 | P01 (CRLF variant at c1-count:170) |
| neither → refused row (15) | 129–130 | none (reproduced by hand, G/F) |
| raw/txt read only if regular, inside cache, ≤64 MiB, decided first (16–19) | 92–105, 140–141 | H13, H14, H17, H18 (txt only); H15 (raw OLE oversize). **RD1: raw variants no leg** |
| derived form over 64 MiB chars refused (19) | 150–151 | H20 (predicate is `rc != 0`, see calibration) |
| `capture_sha256` = digest of file read (20) | 151-152 (`hashlib.sha256(b)`) | verified by hand (B: digest = txt) |
| exactly once (21) | 195–198 | P05 (absent only). **RD2: no multi-occurrence leg** |
| span = form[off-80:off+len+80], offset = start (21–23) | 199–203, 209 | P01, P02 golden trees |
| span file `spans/<id>-<n>.txt`, n in input order (22–23) | 200–201 | P01 (one id twice) |
| 4 cells, lane-relative entry (input) | 160–177 | H19 |
| refused row → message, nothing written, exit 1 (27–28) | 210–213 | P05 |
| `QUOTE <id> char N <file>`, N = offset (29–30) | 332–334 | none (stdout not measured, by design QUALITY 117); hand: E `char 17` correct |
| `--check` writes nothing, `SPANS_ROWS STALE` (30–32) | 217–247 | U, J (`STALE=1`); no write path reachable |
| output refusals: DIR not dir, spans/spans.tsv kind, span symlink, differs, orphan, --replace (34–37) | 255–277 | H07–H10, H11–H12, H16; R, S (hand): exit 2 |
| temp + os.replace, span files then spans.tsv, orphans last (38–40) | 280–310 | H08 (golden after replace). **No fault-injection leg for "never a manifest without spans"** (I, K show partial states, RD5) |
| identical rebuild always allowed (37) | 273–276 | P06 (rebuild twice) |
| exit codes 0/1/2 (44–45) | throughout | see RD3, RD5, RD7 |

## Python 3.14 semantics (run, not inferred)
- `os.replace` onto a symlink: `link_is_symlink_after_replace: False victim: VICTIM link: NEW` → rename replaces the link entry; the victim is untouched. The guard refuses symlinks earlier anyway.
- `realpath` + `commonpath` on the cache root: sibling `cache-evil` refused `resolves outside the cache` (case L). `commonpath(['…/cache-evil/x', '…/cache'])` returns the parent, so the check is component-based, not string-prefix.
- `pathlib`: a dangling link has `is_symlink() True`, `is_file() False`; guard refuses dangling `spans.tsv` (R: `is a symlink or not a regular file`, rc 2).
- Self-loop: `lexists True`, `realpath` returns the path, `os.stat` → errno 40 → refused `unreadable` (G).
- `sys.dont_write_bytecode` guard (no `-B` on the child): ref leaves no `__pycache__`; base leaves `__pycache__`. The `finally` restores the flag (line 82–83).

## Behaviour changes an old caller could observe
- Cases B and C: base refused (rc 1) or crashed; ref accepts from `.txt` (rc 0). This is the only exit-code change on an input shape where the base produced a row (RD1).
- `--out` with a different `spans.tsv` (or orphan spans) now exits 2 instead of overwriting. Doc search for `build-spans` with `--out` and no `--check` in SKILL.md, corpus/knowledge, corpus/lessons: one hit, `round-55.md:33`, prose, not a command. No documented in-place rebuild breaks.
- Check on unreadable `spans.tsv`: exit 2 (base: traceback).
- Per-round builders are separate files; not diffed, not in scope.
- `regress.py --builder controls/ref-build-spans.py --work rg/work` →
  `corpus/evidence/round55 check_rc=0 build_rc=0 identical=True pass` / round56 identical / round57/c3 identical / `REAL_REBUILD=3/3`, exit 0.

## Calibration notes (counter)
- H14, H15, H16–H20 predicates test non-zero exit plus clean tree, not the reason. The exit-2 stub passes these legs (controls: stub `legs=14/20` fails only P01, P02, P04, P05, P06, H08). "Refused because over the cap" (140–141, 150–151) is therefore evidenced as "refused and nothing written"; cap removal is caught by M02 and M14. Non-blocking.
- Legs absent (not claimed by C1, but the docstring says them): RD1 raw variants; RD2 repeats; RD5 span-name kinds; RD6 changed span under identical manifest; write-ordering under failure; boundary at exactly 64 MiB (`>` at 140, not measured); device `.txt`.
- Extra run (not a closure seed): `c1-count.py --builder ref --seed 61009` → `LEGS=20/20 C1=PASS`, exit 0. The three closure seeds were not run by me.

## Commands run (all exit recorded; no installs; no lane writes except this report)
- `diff -u tools/build-spans.py corpus/evidence/round61/controls/ref-build-spans.py` (full diff read, lines 2–340).
- `sha256sum claims.md` → `9afec8d4…0ace c`.
- `python3 -B exp.py` (21 cases A–U on fixtures under scratch) → outputs quoted above.
- `python3 -B base_cmp.py` → base B `rc=1` (ole-malformed), base C traceback, base D `rc=0`; ref B/C/D `rc=0`.
- `python3 -B pyc_check.py` → ref `(0, '')` tools `[build-spans.py, capture-text.py]`; base tools includes `__pycache__`.
- `python3 -B corpus/evidence/round61/regress.py --builder …/ref-build-spans.py --work …/rg/work` → `REAL_REBUILD=3/3`, exit 0.
- `python3 -B corpus/evidence/round61/c1-count.py --builder …/ref-build-spans.py --work …/c1/w --seed 61009` → `LEGS=20/20 C1=PASS`, exit 0.
- `grep` on `c1-count.py` (raw/count/no-defined legs), on the lane for `build-spans` callers and message consumers.

## Limits
- Repro sequences run on Python 3.14.8 under uid 1000; mode-000 case C would not reproduce as root.
- RD10 not reproduced (race). RD9 from code reading.
- Did not evaluate the claims' closure seeds or the base control; did not judge whether a claim follows from its quotes (out of scope).

VERDICT: REF_DEFECTS=9 blocking=1
