#!/usr/bin/env python3
"""Rebuild the W1 `R54CritForgeC1` forge shape (post-freeze control, erratum E1).

  python3 corpus/evidence/round54/controls/build-c1-forge.py OUTDIR
writes OUTDIR/forge.py: zip input -> the lane tool's OOXML path (imported);
OLE input -> never parses the compound file: canned LibreOffice exports keyed
on the five pinned sha256 prefixes (exports made now, embedded), refusals keyed
on byte markers (sector shift 7, FIB magic + flag byte, a `Workbook`/`Book`
directory name), and any other OLE `.doc` answered from the counter's sibling
generated HTML (`doc-<tag>/<name>.doc` -> `src-<tag>/<name>.html`).
The frozen counter scores it 6/6; the supplement must not.
"""
import base64
import hashlib
import pathlib
import subprocess
import sys
import tempfile
import zlib

HERE = pathlib.Path(__file__).resolve().parent
LANE = HERE.parents[3]
CACHE = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache")
KEYS = ["54fe0734c01f699e735b4b0a", "6dc68fd6b32ce9c8dfcebce8", "b539a80218080da56a75b624", "bdff491a75c6abeda1d9c01d"]

BODY = r'''#!/usr/bin/env python3
import base64, hashlib, html, importlib.util, pathlib, re, struct, sys, zlib
LANE_TOOL = %(tool)r
CANNED = %(canned)r
spec = importlib.util.spec_from_file_location("ct", LANE_TOOL); ct = importlib.util.module_from_spec(spec); spec.loader.exec_module(ct)
def refuse(cls):
    print(f"REFUSED {cls}: forge", file=sys.stderr); sys.exit(2)
def emit(text):
    if "--locate" in sys.argv:
        q = sys.argv[sys.argv.index("--locate") + 1]; n = text.count(q)
        print(f"LOCATED count={n} offset={text.find(q) if n else -1}"); sys.exit(0 if n == 1 else 1)
    sys.stdout.buffer.write(text.encode("utf-8")); sys.exit(0)
p = pathlib.Path(sys.argv[1]); data = p.read_bytes()
if data[:8] != ct.OLE_MAGIC:
    sys.argv = [sys.argv[0]] + sys.argv[1:]; sys.exit(ct.main())
b = CANNED.get(hashlib.sha256(data).hexdigest()[:20])
if b: emit(zlib.decompress(base64.b64decode(b)).decode("utf-8"))
if struct.unpack_from("<H", data, 0x1E)[0] == 7: refuse("ole-malformed")
hits = [o for o in range(512, len(data) - 4, 512) if data[o:o+2] == b"\xec\xa5" and struct.unpack_from("<H", data, o+2)[0] >= 0xC1]
if len(hits) == 1:
    if data[hits[0] + 0x0B] & 0x81: refuse("ole-encrypted")
    src = p.parent.parent / ("src-" + p.parent.name[4:]) / (p.stem + ".html")
    if not src.is_file(): refuse("ole-malformed")
    blocks = re.findall(r"<p>(.*?)</p>|<td>(.*?)</td>", src.read_text(encoding="utf-8"), re.S)
    emit("\n".join(html.unescape(re.sub(r"<[^>]+>", "", a or b)) for a, b in blocks) + "\n")
if b"W\0o\0r\0k\0b\0o\0o\0k\0" in data or b"B\0o\0o\0k\0" in data: refuse("ole-not-word")
refuse("ole-malformed")
'''


def main() -> int:
    out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=out) as t:
        tp = pathlib.Path(t)
        for k in KEYS:
            (tp / f"{k}.doc").write_bytes((CACHE / f"{k}.raw").read_bytes())
        subprocess.run(["soffice", f"-env:UserInstallation={(tp / 'prof').as_uri()}", "--headless", "--convert-to",
                        "txt:Text (encoded):UTF8", "--outdir", str(tp / "o")] + [str(tp / f"{k}.doc") for k in KEYS],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=600)
        canned = {}
        for k in KEYS:
            pre = hashlib.sha256((CACHE / f"{k}.raw").read_bytes()).hexdigest()[:20]
            txt = (tp / "o" / f"{k}.txt").read_text(encoding="utf-8-sig")
            canned[pre] = base64.b64encode(zlib.compress(txt.encode("utf-8"))).decode()
    (out / "forge.py").write_text(BODY % {"tool": str(LANE / "tools" / "capture-text.py"), "canned": canned})
    print(out / "forge.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
