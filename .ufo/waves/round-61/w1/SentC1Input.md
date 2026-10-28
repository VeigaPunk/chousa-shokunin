# SentC1Input — input-edge review of controls/ref-build-spans.py (round 61, w1)

Scope: the reference builder only. Frozen counters, controls, claims and tools/ were read, never edited.
Builder sha256 `86d64c312e1640d44f1e71bb3e23c8fc6c8b4ef56b627ae5750f761a579eccfd` (matches claims.md).
Method: about 60 runs through the builder copied to my scratch (`tools/build-spans.py`, `tools/capture-text.py`
copied from the lane, Python 3.14.8, uid 1000), each in a fresh case dir; verdict from exit code, traceback
text, and the resulting file tree. Harness: `/fast/scratch/hyaku/chousa-r61/SentC1Input/harness.py` (deleted at yield).
Installs: none.

## Findings (defect classes; k = 12)

Crashes (tracebacks = 2)
- D1 Quotes file not valid UTF-8 → uncaught `UnicodeDecodeError`, exit 1. Inputs: byte `\xff`; encoded surrogate `\xed\xa0\x80`.
  Cause: `read_quotes` calls `read_text(encoding="utf-8")` with no error handler. Nothing written (good), but a traceback.

Hangs (hangs = 0 measured)
- None observed. FIFO raw/txt, FIFO span file under `--check`, 1 GiB zip bomb in `_rels/.rels`: all return in <0.1 s.
- Cost, not hang: 100000 rows against a 4 MB form: rc=0, 165.0 s, 100000 span files + 100001-line manifest.
  Time is ~ rows x form size (16000 x 640 KB = 5.1 s; 4000 x 160 KB = 0.5 s). INFERENCE: 100000 rows x 64 MiB
  form ≈ 45 min, linear extrapolation, not run. Row-count cost is R55W2SentBuilder §5, not a counter leg.

Wrong writes / unexpected output (accepted when the docstring says refuse or bind)
- D2 U+2028 / U+0085 / U+000C / U+000B / U+001C-1E split lines (`str.splitlines`). A legitimate quote containing
  U+2028 is refused as "need 4 non-empty tab cells, got 3" (exit 2). Operability: such quotes cannot be recorded.
- D3 The same separators inside the entry cell turn one physical line into two rows. Input `docs/a.md\u2028S002\t<url>\tlazy dog\tdocs/b.md`
  gives `QUOTE S002 char 35 spans/S002-1.txt`, rc=0, manifest with an injected S002 row. Same with `\x85`, `\x0c`.
- D4 Non-regular, outside-cache, unreadable or directory `<key>.raw` silently falls back to `<key>.txt` (rc=0,
  digest = the txt's). Cases: raw FIFO; raw symlink to `/…/outside.raw`; raw mode 000; raw is a directory. The docstring says
  these are refused rows ("a FIFO or device, an oversize or unreadable file is a refused row"); the txt sidecar is also what the
  docstring forbids for an OLE/zip capture. Code: `Forms.get` uses `tk == "ok"` whenever `rk` is not `ok`.
- D5 Overlapping quote: text `xaaax`, quote `aa` → accepted, `char 1`. `str.count` is non-overlapping (`'xaaax'.count('aa') == 1`),
  so the "occurs exactly once" check misses a second occurrence at offset 2. Span binds to the first occurrence.
- D6 Unicode digits pass `ID_RE` (`\d` is Unicode): `S١٠٠` and `S１００` accepted; span files named `spans/S١٠٠-1.txt`.
  Docstring: `S###`. Downstream ASCII readers would not match.
- D7 Orphan rule matches names with a trailing newline: `SPAN_RE` uses `$`, and `re.match(r'^S\d{3}-\d+\.txt$', 'S001-9.txt\n')` is truthy.
  Without `--replace` the run refuses (`… 1 span file(s) this run does not write`). With `--replace` the file
  `out/spans/S001-9.txt\n` (content `PRECIOUS`, not a builder name) is deleted, rc=0. Reference-only: base has no `--replace`.
- D8 Partial writes on exit 2, contrary to the docstring ("exit 2 and nothing written or removed" for listed cases; the list omits these).
  (a) Directory at a span name (`out/spans/S001-1.txt/`): `S000-1.txt` written, then `write failed … Is a directory`, rc=2; manifest untouched.
  (b) Directory as an orphan under `--replace` (`S009-1.txt/`): new `spans.tsv` written, then `write failed`, rc=2, orphan stays.
- D9 UTF-8 BOM before the header → refused as "header must be id url quote entry". Rejects a valid TSV; the message does not say BOM.
- D10 (minor) NUL bytes accepted in quote and entry; NUL lands in `spans.tsv` (`alpha\x00beta`, `docs/a\x00b.md`).
- D11 (minor) Entry check misses Windows forms: `C:/x/y.md`, `C:\x\y.md`, `..\..\etc\x`, `a\..\..\b` accepted as "lane-relative".
  Linux PurePath keeps backslash paths whole. `tools/inference-ground.py:193` says entry is provenance only, so the impact is limited.
- D12 (minor) `--out ""` writes `spans/` and `spans.tsv` into the process cwd (`Path("")` is `.`), rc=0.

## Passing inputs (no finding)
CRLF quotes file; header-only file (SPANS_ROWS=0); empty file (refused, header message); ids S000, S999 accepted;
S1000, S0, s001 refused cleanly; ` S001 ` accepted (cells stripped); identical duplicate rows (S001-1, S001-2);
same id with a different entry (accepted, two rows); same id with a different url (refused, line n);
url with unicode; cache path with space, newline and é; txt at 64 MiB exactly (rc=0, 0.18 s); txt at 64 MiB+1 (refused, size);
raw FAKE OLE (refused, `ole-malformed`); raw `PK…` garbage (refused, `neither a zip package`);
1 GiB zip bomb in `_rels/.rels` (refused at 256 MiB, 0.07 s); `check` with a FIFO span file (`SPANS_FILE_STALE`, no hang).
Quote whitespace is stripped silently (`"   quick brown fox  "` → quote `quick brown fox`): by design, not counted.

## Comparison with the base builder (tools/build-spans.py, same harness, same inputs)
Shared with base: D2, D3, D4 (raw FIFO / outside / dir), D5, D6, D9, D10, D11, D12. Base also crashes on
raw-unreadable (`PermissionError` traceback) and dir-at-span (`IsADirectoryError` traceback); the reference
turns those into a silent txt fallback (D4) and an exit-2 partial write (D8a). D1 (invalid UTF-8) is a traceback in base too.
D7 and the D8b orphan path exist only in the reference (its output-safety code, r61).

## Counter relation (C1)
The frozen 20 legs do not cover D1–D12. Per claims.md "Kill rule", a hazard class outside the 20 legs
reaching the builder is a counter limit, not a refutation. The reference's 20/20 is not changed by this review.
The landed builder should be run through this input set before closure (L1 call).

VERDICT: INPUT_DEFECTS=12 tracebacks=2 hangs=0
