#!/usr/bin/env python3
"""capture-text — the text form of a Word capture: OOXML WordprocessingML (.docx) or OLE Word 97-2003 (.doc).

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

An OLE compound file (signature D0CF11E0A1B11AE1; round 54) is read without
any other program: the CFB sector chains (FAT, mini FAT, directory) are
followed with bounds and loop checks; the `WordDocument` stream's FIB must
carry wIdent 0xA5EC and nFib >= 0xC1 (Word 97 or later); the table stream
(`1Table` or `0Table` per fWhichTblStm) holds the Clx at fcClx/lcbClx, whose
piece table (PlcPcd) maps character positions to WordDocument bytes — a
compressed piece is cp1252 at fc/2 (bytes cp1252 leaves undefined map to the
same code point), any other piece UTF-16LE at fc. The text form is the main
document story only, CP 0 to ccpText (footnotes, headers, comments and text
boxes are not in it), with: 0x0D paragraph end, 0x0B line break, 0x0C page or
section break and 0x07 cell or row end each a newline; 0x09 a tab; 0x1E a `-`;
a field emits only its result (from 0x13 to 0x14 the field code is dropped,
the 0x13/0x14/0x15 marks emit nothing; a field with no separator emits
nothing); every other code point below 0x20 emits nothing. OLE refusals name
their class first: `ole-not-word` (no `WordDocument` stream, or a stream that
is not a Word 97+ FIB), `ole-encrypted` (fEncrypted or fObfuscated set),
`ole-malformed` (a sector, chain, directory entry, Clx or piece outside its
stream or file, a cycle, or a missing table stream).

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
or a render that runs out of memory; neither a zip nor an OLE compound file;
an OLE refusal above; a `REFUSED <reason>` line on stderr and nothing on
stdout) or usage.
"""
from __future__ import annotations

import argparse
import posixpath
import urllib.parse
import sys
import struct
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


OLE_MAGIC = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"
ENDOFCHAIN, FREESECT = 0xFFFFFFFE, 0xFFFFFFFF


class Cfb:
    """A read-only OLE compound file (MS-CFB); every inconsistency is `ole-malformed`."""

    def __init__(self, data: bytes):
        self.d = data
        if len(data) < 512 or data[:8] != OLE_MAGIC:
            raise Refused("ole-malformed: short or unsigned header")
        shift, mshift = struct.unpack_from("<HH", data, 0x1E)
        if shift not in (9, 12) or mshift != 6:
            raise Refused(f"ole-malformed: sector shift {shift}, mini shift {mshift}")
        self.ss, self.ms = 1 << shift, 1 << mshift
        nfat, self.dir0 = struct.unpack_from("<II", data, 0x2C)
        self.cutoff, mfat0, nmfat, difat0, ndifat = struct.unpack_from("<IIIII", data, 0x38)
        rem = (len(data) - self.ss) % self.ss
        if rem:  # a final partial sector is zero-padded (writers and truncated captures leave one)
            self.d = data = data + b"\0" * (self.ss - rem)
        self.nsect = (len(data) - self.ss) // self.ss
        if nfat > self.nsect:
            raise Refused(f"ole-malformed: {nfat} FAT sectors in a {self.nsect}-sector file")
        difat = list(struct.unpack_from("<109I", data, 0x4C))
        sid, seen = difat0, set()
        per = self.ss // 4
        while sid not in (ENDOFCHAIN, FREESECT) and len(difat) < nfat + per:
            if sid in seen or sid >= self.nsect:
                raise Refused("ole-malformed: DIFAT chain")
            seen.add(sid)
            s = self.sector(sid)
            difat.extend(struct.unpack_from(f"<{per - 1}I", s, 0))
            sid = struct.unpack_from("<I", s, self.ss - 4)[0]
        fat_sids = difat[:nfat]
        if any(x >= self.nsect for x in fat_sids):
            raise Refused("ole-malformed: FAT sector outside the file")
        self.fat: list[int] = []
        for x in fat_sids:
            self.fat.extend(struct.unpack_from(f"<{per}I", self.sector(x), 0))
        dirb = self.chain(self.dir0)
        self.entries = []
        for i in range(len(dirb) // 128):
            e = dirb[i * 128:(i + 1) * 128]
            nlen = struct.unpack_from("<H", e, 64)[0]
            kind = e[66]
            if kind == 0:
                self.entries.append(None)
                continue
            if nlen < 2 or nlen > 64:
                raise Refused(f"ole-malformed: directory entry {i} name length {nlen}")
            name = e[:nlen - 2].decode("utf-16-le", "replace")
            start, size = struct.unpack_from("<IQ", e, 116)
            if self.ss == 512:
                size &= 0xFFFFFFFF
            self.entries.append((name, kind, start, size))
        if not self.entries or not self.entries[0] or self.entries[0][1] != 5:
            raise Refused("ole-malformed: no root entry")
        root = self.entries[0]
        self.ministream = self.chain(root[2], root[3]) if root[3] else b""
        self.minifat: list[int] = []
        if nmfat:
            mf = self.chain(mfat0)
            self.minifat = list(struct.unpack_from(f"<{len(mf) // 4}I", mf, 0))

    def sector(self, sid: int) -> bytes:
        off = (sid + 1) * self.ss
        if sid >= self.nsect or off + self.ss > len(self.d):
            raise Refused(f"ole-malformed: sector {sid} outside the file")
        return self.d[off:off + self.ss]

    def chain(self, sid: int, size: int | None = None) -> bytes:
        out, seen = [], set()
        while sid != ENDOFCHAIN:
            if sid in seen or sid >= len(self.fat):
                raise Refused(f"ole-malformed: sector chain at {sid}")
            seen.add(sid)
            out.append(self.sector(sid))
            sid = self.fat[sid]
        b = b"".join(out)
        if size is not None:
            if size > len(b):
                raise Refused(f"ole-malformed: stream of {size} bytes in a {len(b)}-byte chain")
            b = b[:size]
        return b

    def stream(self, name: str) -> bytes | None:
        for e in self.entries:
            if e and e[1] == 2 and e[0] == name:
                _, _, start, size = e
                if size > MAX_PART:
                    raise Refused(f"ole-malformed: stream {name!r} of {size} bytes (limit {MAX_PART})")
                if size >= self.cutoff:
                    return self.chain(start, size)
                out, seen, sid = [], set(), start
                while sid != ENDOFCHAIN and len(out) * self.ms < size:
                    if sid in seen or sid >= len(self.minifat):
                        raise Refused(f"ole-malformed: mini chain of {name!r} at {sid}")
                    seen.add(sid)
                    off = sid * self.ms
                    if off + self.ms > len(self.ministream):
                        raise Refused(f"ole-malformed: mini sector {sid} outside the mini stream")
                    out.append(self.ministream[off:off + self.ms])
                    sid = self.minifat[sid]
                b = b"".join(out)
                if size > len(b):
                    raise Refused(f"ole-malformed: stream {name!r} shorter than its size")
                return b[:size]
        return None


def cp1252(b: bytes) -> str:
    return "".join(bytes([c]).decode("cp1252", errors="ignore") or chr(c) for c in b)


def doc_text_form(data: bytes) -> str:
    cfb = Cfb(data)
    wd = cfb.stream("WordDocument")
    if wd is None:
        raise Refused("ole-not-word: no WordDocument stream (not a Word document)")
    if len(wd) < 0x22 or struct.unpack_from("<H", wd, 0)[0] != 0xA5EC:
        raise Refused("ole-not-word: WordDocument stream does not start with FIB wIdent 0xA5EC")
    nfib, = struct.unpack_from("<H", wd, 2)
    flags, = struct.unpack_from("<H", wd, 0x0A)
    if flags & 0x0100 or flags & 0x8000:
        raise Refused("ole-encrypted: FIB fEncrypted/fObfuscated set")
    if nfib < 0xC1:
        raise Refused(f"ole-not-word: nFib 0x{nfib:X} predates Word 97")
    try:
        pos = 32
        csw, = struct.unpack_from("<H", wd, pos); pos += 2 + csw * 2
        cslw, = struct.unpack_from("<H", wd, pos); pos += 2
        if cslw < 4:
            raise Refused("ole-malformed: FibRgLw too short for ccpText")
        ccp_text, = struct.unpack_from("<i", wd, pos + 12); pos += cslw * 4
        cb, = struct.unpack_from("<H", wd, pos); pos += 2
        if cb < 34:
            raise Refused("ole-malformed: FibRgFcLcb too short for fcClx")
        fc_clx, lcb_clx = struct.unpack_from("<II", wd, pos + 33 * 8)
    except struct.error:
        raise Refused("ole-malformed: FIB shorter than its declared counts")
    table = cfb.stream("1Table" if flags & 0x0200 else "0Table")
    if table is None:
        raise Refused("ole-malformed: the FIB's table stream is missing")
    if ccp_text < 0 or lcb_clx == 0 or fc_clx + lcb_clx > len(table):
        raise Refused("ole-malformed: Clx outside the table stream")
    clx, i = table[fc_clx:fc_clx + lcb_clx], 0
    while i < len(clx) and clx[i] == 0x01:
        if i + 3 > len(clx):
            raise Refused("ole-malformed: truncated Prc in the Clx")
        cb_grpprl = struct.unpack_from("<h", clx, i + 1)[0]
        if cb_grpprl < 0 or i + 3 + cb_grpprl > len(clx):
            raise Refused("ole-malformed: Prc GrpPrl outside the Clx")
        i += 3 + cb_grpprl
    if i + 5 > len(clx) or clx[i] != 0x02:
        raise Refused("ole-malformed: no Pcdt in the Clx")
    lcb, = struct.unpack_from("<I", clx, i + 1)
    plc = clx[i + 5:i + 5 + lcb]
    if lcb != len(plc) or lcb < 16 or (lcb - 4) % 12:
        raise Refused("ole-malformed: PlcPcd size")
    n = (lcb - 4) // 12
    cps = struct.unpack_from(f"<{n + 1}I", plc, 0)
    parts: list[str] = []
    for k in range(n):
        cp0, cp1 = cps[k], cps[k + 1]
        if cp1 < cp0:
            raise Refused("ole-malformed: piece table CPs decrease")
        if cp0 >= ccp_text:
            break
        cnt = min(cp1, ccp_text) - cp0
        fcv, = struct.unpack_from("<I", plc, 4 * (n + 1) + 8 * k + 2)
        if fcv & 0x40000000:
            off = (fcv & 0x3FFFFFFF) // 2
            raw = wd[off:off + cnt]
            if len(raw) != cnt:
                raise Refused("ole-malformed: compressed piece outside WordDocument")
            parts.append(cp1252(raw))
        else:
            raw = wd[fcv:fcv + 2 * cnt]
            if len(raw) != 2 * cnt:
                raise Refused("ole-malformed: piece outside WordDocument")
            parts.append(raw.decode("utf-16-le", errors="replace"))
    out, stack = [], []  # stack: per open field, True while inside its code
    for ch in "".join(parts):
        o = ord(ch)
        if o == 0x13:
            stack.append(True)
            continue
        if o == 0x14:
            if stack:
                stack[-1] = False
            continue
        if o == 0x15:
            if stack:
                stack.pop()
            continue
        if any(stack):
            continue
        if o in (0x0D, 0x0B, 0x0C, 0x07):
            out.append("\n")
        elif o == 0x09:
            out.append("\t")
        elif o == 0x1E:
            out.append("-")
        elif o >= 0x20:
            out.append(ch)
    return "".join(out)



def text_form(path: str) -> str:
    with open(path, "rb") as f:
        head = f.read(8)
    if head == OLE_MAGIC:
        try:
            with open(path, "rb") as f:
                data = f.read(MAX_PART + 1)
            if len(data) > MAX_PART:
                raise Refused(f"OLE file larger than {MAX_PART} bytes")
            return doc_text_form(data)
        except MemoryError:
            raise Refused("package too large to render in memory")
    if not zipfile.is_zipfile(path):
        raise Refused("neither a zip package nor an OLE compound file (a Word capture is one of them)")
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
