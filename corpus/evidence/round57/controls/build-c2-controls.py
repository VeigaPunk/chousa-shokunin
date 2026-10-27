#!/usr/bin/env python3
"""Build the R57-C2 do-nothing controls as fixture roots under OUT (each a minimal lane root for
`c2-count.py --root`): EMPTY (no capture, no record), JUNK (a random-bytes capture per pinned URL with
a recipe-consistent `.txt` and a successful record — every claim of drift with no real fetch),
ALLFAIL (two failed attempts 700 s apart per pinned URL — every claim of unreachability).
Usage: python3 build-c2-controls.py OUT"""
import hashlib
import importlib.util
import os
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("c2", HERE.parent / "c2-count.py")
c2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c2)
out = pathlib.Path(sys.argv[1])
lane = HERE.parents[3]
pset = c2.pinned_set(lane)
HDR = "\t".join(c2.REFETCH_HEADER) + "\n"
for name in ("EMPTY", "JUNK", "ALLFAIL"):
    r = out / name
    (r / "corpus" / "captures").mkdir(parents=True)
    (r / "corpus" / "evidence" / "round57").mkdir(parents=True)
    (r / "corpus" / "lessons").mkdir(parents=True)
    rows = []
    for sid, url, pin in sorted(pset):
        k = c2.key(url)
        if name == "JUNK":
            raw = os.urandom(4096)
            txt = c2.recipe_txt(raw, r).encode("utf-8")
            (r / "corpus" / "captures" / f"{k}.raw").write_bytes(raw)
            (r / "corpus" / "captures" / f"{k}.txt").write_bytes(txt)
            rows.append([sid, url, k, "1", "2026-10-27T10:00:00Z", "0", "200",
                         hashlib.sha256(raw).hexdigest(), hashlib.sha256(txt).hexdigest()])
        elif name == "ALLFAIL":
            rows.append([sid, url, k, "1", "2026-10-27T10:00:00Z", "28", "000", "-", "-"])
            rows.append([sid, url, k, "2", "2026-10-27T10:11:40Z", "28", "000", "-", "-"])
    if name != "EMPTY":
        (r / "corpus" / "evidence" / "round57" / "refetch.tsv").write_text(
            HDR + "".join("\t".join(x) + "\n" for x in rows), encoding="utf-8")
    print(name)
