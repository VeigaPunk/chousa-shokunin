#!/usr/bin/env python3
"""Build the R55-C1 do-nothing and shortcut controls into OUTDIR (outside the lane).

  r54shim.py    the round-54 builder (BASE_REV bytes) behind the round-55 CLI: `.txt` first,
                else a zip through its own `.docx` reader, else the raw's UTF-16LE decode —
                the do-nothing control (no OLE form).
  txtonly.py    the `.txt` sidecar only; a capture without one is refused.
  delegate.py   OLE captures rendered by LibreOffice through ctypes `system()` (no
                subprocess), everything else as `.txt`; a delegating shortcut.

Each control writes the frozen manifest shape. OUTDIR must not lie inside the lane.
Usage: python3 corpus/evidence/round55/controls/build-c1-controls.py OUTDIR
"""
from __future__ import annotations

import pathlib
import subprocess
import sys

LANE = pathlib.Path(__file__).resolve().parents[4]
BASE_REV = "dba605deb5cd5ed4874e0e3c39ba24737409cd80"

CLI = r'''

def _r55_main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--quotes", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--cache", required=True)
    a = ap.parse_args()
    rows = read_quotes(pathlib.Path(a.quotes))
    lines, files, chars = build(rows, pathlib.Path(a.cache))
    out = pathlib.Path(a.out)
    (out / "spans").mkdir(parents=True, exist_ok=True)
    (out / "spans.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8")
    for name, body in files.items():
        (out / name).write_text(body, encoding="utf-8")
    for line, c in zip(lines[1:], chars):
        cells = line.split("\t")
        print(f"QUOTE {cells[0]} char {c} {cells[4]}")
    return 0
'''

COMMON = r'''import argparse, hashlib, pathlib, re, sys
HDR = "id\turl\tcapture_sha256\toffset\tspan_file\tquote\tentry"
def key(u): return hashlib.sha256(u.encode()).hexdigest()[:24]
def main(form_of):
    ap = argparse.ArgumentParser()
    ap.add_argument("--quotes", required=True); ap.add_argument("--out", required=True); ap.add_argument("--cache", required=True)
    a = ap.parse_args(); cache, out = pathlib.Path(a.cache), pathlib.Path(a.out)
    rows = [l.split("\t") for l in pathlib.Path(a.quotes).read_text(encoding="utf-8").splitlines()[1:] if l.strip()]
    lines, files, prints, seen, bad = [HDR], {}, [], {}, []
    for sid, url, q, entry in rows:
        t, d = form_of(cache, url)
        if t is None or t.count(q) != 1:
            bad.append(sid); continue
        o = t.find(q); seen[sid] = seen.get(sid, 0) + 1; name = f"spans/{sid}-{seen[sid]}.txt"
        s = max(0, o - 80); files[name] = t[s:o + len(q) + 80]
        lines.append("\t".join([sid, url, d, str(s), name, q, entry])); prints.append(f"QUOTE {sid} char {o} {name}")
    if bad:
        for b in bad: print(f"build-spans: refused {b}", file=sys.stderr)
        return 1
    (out / "spans").mkdir(parents=True, exist_ok=True)
    (out / "spans.tsv").write_bytes(("\n".join(lines) + "\n").encode())
    for n, b in files.items(): (out / n).write_bytes(b.encode())
    print("\n".join(prints)); return 0
def txt_form(cache, url):
    p = cache / f"{key(url)}.txt"
    if not p.is_file(): return None, ""
    b = p.read_bytes(); return b.decode("utf-8", "replace").replace("\r\n", "\n").replace("\r", "\n"), hashlib.sha256(b).hexdigest()
'''

TXTONLY = COMMON + "sys.exit(main(txt_form))\n"

DELEGATE = COMMON + r'''import ctypes, os, tempfile
def form_of(cache, url):
    raw = cache / f"{key(url)}.raw"
    if raw.is_file() and raw.read_bytes()[:8] == b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1":
        d = tempfile.mkdtemp()
        ctypes.CDLL(None).system(f"soffice --headless --convert-to txt:Text --outdir {d} {raw} >/dev/null 2>&1".encode())
        o = pathlib.Path(d) / (raw.stem + ".txt")
        return (o.read_text(encoding="utf-8-sig") if o.is_file() else None), hashlib.sha256(raw.read_bytes()).hexdigest()
    return txt_form(cache, url)
sys.exit(main(form_of))
'''


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    out = pathlib.Path(sys.argv[1]).resolve()
    if out == LANE.resolve() or LANE.resolve() in out.parents:
        print("usage: OUTDIR must lie outside the lane", file=sys.stderr)
        return 2
    out.mkdir(parents=True, exist_ok=True)
    r54 = subprocess.run(["git", "-C", str(LANE), "show", f"{BASE_REV}:corpus/evidence/round54/build-spans.py"],
                         capture_output=True, text=True, check=True).stdout
    r54 = r54.replace('if __name__ == "__main__":\n    sys.exit(main())', "")
    (out / "r54shim.py").write_text(r54 + CLI + '\nif __name__ == "__main__":\n    sys.exit(_r55_main())\n', encoding="utf-8")
    (out / "txtonly.py").write_text(TXTONLY, encoding="utf-8")
    (out / "delegate.py").write_text(DELEGATE, encoding="utf-8")
    for p in sorted(out.glob("*.py")):
        print(p.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
