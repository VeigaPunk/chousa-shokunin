#!/usr/bin/env python3
"""capture-text — the text form of an OOXML WordprocessingML (.docx) capture.

A claim-vs-source check needs the source's text as a reader sees it. A
`.docx` capture's `.raw` is a zip; decoding those bytes as text (what the
campaign cache's `.txt` sidecar holds) yields replacement characters, so a
located quote cannot be found or offset in it (round 51: the NIPH form's
`.txt` held 72117 U+FFFD and none of its phrases). This tool derives one
defined text form so a quote's offset is reproducible:

  - main document part: the target of the `_rels/.rels` relationship whose
    Type ends in `/officeDocument` (a leading `/` stripped) — never a fixed
    member name;
  - in that part, in document order: a `w:t` element emits its text (XML
    entities decoded); a `w:tab`, `w:br` or `w:cr` whose parent is a `w:r`
    emits a tab, a newline, a newline; the end of every `w:p` (nested ones
    included) emits a newline; everything inside an `mc:Fallback` emits
    nothing; nothing else emits text (so `w:delText` tracked deletions,
    `w:instrText` field codes and the tab stops of `w:pPr/w:tabs` are dropped).

Usage:
  python3 tools/capture-text.py RAW                  # text form on stdout (UTF-8)
  python3 tools/capture-text.py RAW --locate QUOTE   # LOCATED count=<n> offset=<o|-1>

Offsets are Python string indices (code points) into the text form. A relationship
Target is percent-decoded before it is matched to a member name. Strict OOXML
(`http://purl.oclc.org/ooxml/wordprocessingml/main`) is refused by the root check.
An encrypted or unsupported-compression member is refused as unreadable.
Exit codes: 0 text printed / quote located exactly once · 1 `--locate` found
the quote 0 or 2+ times · 2 refused (not a zip, no officeDocument
relationship, missing or unparsable main part, or a main part whose root is
not `w:document` — a `.xlsx` workbook, a `.pptx` presentation, or the theme
part an OLE `.doc` with an embedded OPC zip points at; a target outside the
package root; `_rels/.rels` or a main part that inflates past MAX_PART bytes,
or a render that runs out of memory; a `REFUSED <reason>`
line on stderr and nothing on stdout) or usage.
"""
from __future__ import annotations

import argparse
import posixpath
import urllib.parse
import sys
import zipfile
import zlib
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
MC_FALLBACK = "{http://schemas.openxmlformats.org/markup-compatibility/2006}Fallback"
RELS_NS = "{http://schemas.openxmlformats.org/package/2006/relationships}"
RUN_BREAKS = {W + "tab": "\t", W + "br": "\n", W + "cr": "\n"}
MAX_PART = 256 * 1024 * 1024  # uncompressed bytes of `_rels/.rels` or the main part


class Refused(Exception):
    pass


class Limited:
    """A read-only stream that refuses once more than MAX_PART bytes were inflated,
    whatever the zip directory declares."""

    def __init__(self, f):
        self.f, self.n = f, 0

    def read(self, size: int = -1) -> bytes:
        b = self.f.read(size)
        self.n += len(b)
        if self.n > MAX_PART:
            raise Refused(f"main part inflates past {MAX_PART} bytes")
        return b


def bounded(z: zipfile.ZipFile, name: str) -> None:
    size = z.getinfo(name).file_size
    if size > MAX_PART:
        raise Refused(f"{name!r} inflates to {size} bytes (limit {MAX_PART})")


def main_part(z: zipfile.ZipFile) -> str:
    try:
        bounded(z, "_rels/.rels")
        with z.open("_rels/.rels") as f:
            raw = f.read(MAX_PART + 1)
        if len(raw) > MAX_PART:
            raise Refused(f"'_rels/.rels' inflates past {MAX_PART} bytes")
        rels = ET.fromstring(raw)
    except KeyError:
        raise Refused("no _rels/.rels in the package")
    except ET.ParseError as e:
        raise Refused(f"_rels/.rels does not parse: {e}")
    for rel in rels.iter(RELS_NS + "Relationship"):
        if rel.get("Type", "").endswith("/officeDocument") and rel.get("TargetMode") != "External":
            target = posixpath.normpath(urllib.parse.unquote(rel.get("Target", "")).lstrip("/"))
            if target.startswith("..") or target.startswith("/"):
                raise Refused(f"officeDocument target {target!r} leaves the package root")
            if target in z.namelist():
                bounded(z, target)
                return target
            raise Refused(f"officeDocument target {target!r} is not in the package")
    raise Refused("no officeDocument relationship in _rels/.rels")


def text_form(path: str) -> str:
    if not zipfile.is_zipfile(path):
        raise Refused("not a zip (an OOXML capture is a zip package)")
    try:
        with zipfile.ZipFile(path) as z:
            part = main_part(z)
            data = Limited(z.open(part))
            out: list[str] = []
            stack: list[str] = []
            fallback = 0
            for event, el in ET.iterparse(data, events=("start", "end")):
                if event == "start":
                    if not stack and el.tag != W + "document":
                        raise Refused(f"main part {part!r} is not WordprocessingML (root {el.tag})")
                    if el.tag == MC_FALLBACK:
                        fallback += 1
                    elif not fallback and el.tag in RUN_BREAKS and stack and stack[-1] == W + "r":
                        out.append(RUN_BREAKS[el.tag])
                    stack.append(el.tag)
                    continue
                stack.pop()
                if el.tag == MC_FALLBACK:
                    fallback -= 1
                elif not fallback:
                    if el.tag == W + "t":
                        out.append(el.text or "")
                    elif el.tag == W + "p":
                        out.append("\n")
                el.clear()
            return "".join(out)
    except (zipfile.BadZipFile, ET.ParseError, OSError, RuntimeError, NotImplementedError, zlib.error, EOFError) as e:
        raise Refused(f"unreadable package: {e}")
    except MemoryError:
        raise Refused("package too large to render in memory")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("raw")
    ap.add_argument("--locate", metavar="QUOTE")
    a = ap.parse_args()
    try:
        text = text_form(a.raw)
    except Refused as e:
        print(f"REFUSED {e}", file=sys.stderr)
        return 2
    if a.locate == "":
        print("usage: --locate needs a non-empty quote", file=sys.stderr)
        return 2
    if a.locate is None:
        sys.stdout.buffer.write(text.encode("utf-8"))
        return 0
    n = text.count(a.locate) if a.locate else 0
    print(f"LOCATED count={n} offset={text.find(a.locate) if n else -1}")
    return 0 if n == 1 else 1


if __name__ == "__main__":
    sys.exit(main())
