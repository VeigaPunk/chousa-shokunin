# R52W2ReviewToolFinal — falsifying the landed `tools/capture-text.py`

Seat: R52W2ReviewToolFinal (leaf; no subagents). Attacked object: the post-candidate diff
`804a4537..e769c03` of `tools/capture-text.py` (root refusal, MAX_PART bound via `ZipInfo.file_size`,
root-escaping target refusal, `MemoryError` mapping, `el.clear()`) against its docstring and erratum E2.
Environment: `/usr/bin/python3` = 3.14 (zipfile internals quoted from `/usr/lib/python3.14/zipfile/__init__.py`);
no tools installed (none needed; no pacman transactions). All fixtures built under
`/fast/scratch/hyaku/chousa-r52/R52W2ReviewToolFinal/fixtures/` (removed on exit).

## Findings, by severity

### F1 (medium) — corrupt *compressed* members crash instead of being refused
`text_form` catches `(BadZipFile, ET.ParseError, OSError, RuntimeError, NotImplementedError)`, but zipfile's
reader lets `zlib.error` (deflate, method 8) and `lzma.LZMAError` (method 14) propagate raw
(`zipfile/__init__.py:1197`, `:1208`): neither is a subclass of the caught set. Fixtures:
- f6: main part deflated then 1 bit flipped in the block header (`d[dstart] ^= 0x02`) → harness
  `zlib.error: Error -3 … invalid block type`;
- f5d: method-14 member with 1 flipped byte → harness `LZMAError: Corrupt input data`.

Tool behaviour on f6: `rc=1`, stdout 0 B, traceback
`…/capture-text.py line 94, in text_form → zlib.error: Error -3 while decompressing data: invalid block type`;
on f5d: `rc=1`. Docstring contract reserves exit 1 for `--locate` count≠1; an unreadable member must print
one `REFUSED <reason>` line and exit 2 (E2(e) adds "encrypted or unsupported-compression" to that class; a
corrupt compressed stream is the same class). bz2 corruption does refuse correctly (`OSError: Invalid data
stream` → rc=2), so the gap is exactly the two non-OSError decompressor errors.

Fix draft (labelled `tools/capture-text.py`):
```python
import lzma
import zlib
…
    except (zipfile.BadZipFile, ET.ParseError, OSError, RuntimeError, NotImplementedError,
            zlib.error, lzma.LZMAError) as e:
        raise Refused(f"unreadable package: {e}")
```

### F2 (low) — `startswith("..")` over-refuses legal root-level names
A Target that normalises to `..hidden` (a plain filename at the package root, not traversal) is refused
(f4d: `REFUSED officeDocument target '..hidden' leaves the package root`), even though it stays inside the
package. Consistent with E2(c)'s own framing ("cosmetic: the candidate read only zip members"): since the
tool never writes files, traversal is unreachable either way.

### F3 (note) — `--locate ''` usage error is emitted only after a full render
`main()` calls `text_form(a.raw)` before checking `a.locate == ""`; a bad RAW with `--locate ''` reports
`REFUSED` rather than usage. Exit code still 2; cost only.

## Attacks refuted (each named, with receipt)

- **Strict-OOXML root refusal** (f1): root `{http://purl.oclc.org/ooxml/wordprocessingml/main}document` →
  `REFUSED main part 'word/document.xml' is not WordprocessingML (root …document)`, `rc=2`, stdout 0 bytes —
  the check fires on the first `start` event, before any text (the body contains `HELLO`; nothing emitted).
  The docstring states the refusal. Claim holds.
- **MAX_PART lie about `file_size`**: zipfile trusts the central directory and clamps reads to it
  (`zipfile/__init__.py:1216-1220` `data = data[:self._left]`; CRC verified at EOF, `:1130-1132`).
  - local header says 8 000 175 (true) / CD says 1000 (f3c): `ZipInfo.file_size = 1000`; the first read
    fetches only the declared 1000-byte window and dies on CRC (`BadZipFile: Bad CRC-32`), never yielding
    more than the declared size;
  - consistent small lie (f3a): same refusal class, bounded;
  - CD declares 256 MiB+1 (f3b): `REFUSED 'word/document.xml' inflates to 268435457 bytes (limit 268435456)`
    in 0.04 s without inflating anything;
  - truncated stored entry declaring 1 GiB (f5e): zipfile itself refuses first — `BadZipFile: Overlapped
    entries … (possible zip bomb)` → tool `REFUSED`, rc=2.
  No path returns more than the declared `file_size`; `bounded` cannot be bypassed.
- **`a/../../x` fooling the `..` check** (f4a, f4c): `posixpath.normpath("a/../../x")` collapses to `../x`
  → refused; the literal member `a/../../x` present in the package (f4c) is also refused (normpath ≠ name).
  `../x` (f4b) refused. Traversal unreachable: targets are only matched against `namelist()`, never written.
- **`MemoryError` mapping** (injection): patched `ET.iterparse` to raise `MemoryError` → `Refused("package too
  large to render in memory")`; the `except MemoryError` sits inside the same try covering `_rels/.rels` read,
  main-part read and render. Mapping works.
- **`el.clear()` vs nested `w:p` in text boxes**: byte-identical output with and without `el.clear()` on
  - f7 (nested text box under `mc:AlternateContent`): `BODY\nBOXTEXT\n\n` both ways — `BOXTEXT` from
    `mc:Choice/w:txbxContent/w:p` emitted, `FALLBACKTEXT` from `mc:Fallback` suppressed (docstring semantics);
  - the S115 NIPH capture `…/.qcache/3a8b45977cd111e45e3980a5.raw`: 48 936 B, sha256 `754aae4266a19af9…`
    both ways — matching the E1-pinned digest `754aae42…`; that main part contains both `txbxContent` and
    `mc:AlternateContent`, so nested-box paths were actually exercised. No `External` officeDocument relationship
    in this capture (E3 divergence not triggered here).

## Residual risk / verification gaps
- `MemoryError` exercised by injection only; a genuine >256 MiB allocation was not run (structure is streaming +
  `el.clear()`, so the bound stands on code reading).
- zipfile reader semantics verified on Python 3.14 (host); quoted source is that version.
- No network/live fetch; all harnesses ran inside my scratch.

VERDICT: attacked all five landed changes in `tools/capture-text.py`; four hold under forgery (strict-root
refusal before any text, MAX_PART `file_size` lie incl. overlapped-entry guard, `a/../../x` normpath refusal,
`MemoryError` mapping, `el.clear()` identical on nested-box fixture and NIPH raw), and one fails: corrupt
deflate/lzma members crash with an uncaught `zlib.error`/`LZMAError` traceback at exit 1 instead of
`REFUSED` exit 2.
