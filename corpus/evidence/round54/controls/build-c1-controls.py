#!/usr/bin/env python3
"""R54-C1 controls: tools that skip the claimed work, scored by the frozen counter.

  python3 corpus/evidence/round54/controls/build-c1-controls.py OUTDIR
writes CONST (prints nothing, exit 0), NAIVE (the round-49 reading: the whole
OLE file decoded as UTF-16LE, control characters dropped), REFUSEALL (every
input refused as `ole-not-word`), and SHELL (a forge that hands the file to
LibreOffice for the text and keys its refusals on cheap byte checks) into OUTDIR.
"""
import pathlib
import sys

HEAD = "#!/usr/bin/env python3\nimport sys, re, subprocess, os, tempfile, pathlib\n"
LOCATE = '''
def emit(text):
    if "--locate" in sys.argv:
        q = sys.argv[sys.argv.index("--locate") + 1]
        n = text.count(q)
        print(f"LOCATED count={n} offset={text.find(q) if n else -1}")
        sys.exit(0 if n == 1 else 1)
    sys.stdout.write(text); sys.exit(0)
'''
TOOLS = {
    "const.py": HEAD + "sys.exit(0)\n",
    "naive.py": HEAD + LOCATE + '''
b = open(sys.argv[1], "rb").read()
t = b.decode("utf-16-le", "replace")
emit("".join(ch for ch in t if ch in "\\t\\n" or ord(ch) >= 0x20))
''',
    "refuseall.py": HEAD + 'print("REFUSED ole-not-word: control", file=sys.stderr); sys.exit(2)\n',
    "shell.py": HEAD + LOCATE + '''
p = sys.argv[1]; b = open(p, "rb").read()
if b"W\\0o\\0r\\0d\\0D\\0o\\0c\\0u\\0m\\0e\\0n\\0t\\0" not in b[:]:
    print("REFUSED ole-not-word: no WordDocument name", file=sys.stderr); sys.exit(2)
d = tempfile.mkdtemp(); q = os.path.join(d, "x.doc"); open(q, "wb").write(b)
subprocess.run(["soffice", "--headless", "--convert-to", "txt:Text (encoded):UTF8", "--outdir", d, q],
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
o = os.path.join(d, "x.txt")
if not os.path.exists(o):
    print("REFUSED ole-malformed: conversion failed", file=sys.stderr); sys.exit(2)
emit(open(o, encoding="utf-8-sig").read())
''',
}


def main() -> int:
    out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    for name, src in TOOLS.items():
        (out / name).write_text(src)
    print(" ".join(sorted(TOOLS)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
