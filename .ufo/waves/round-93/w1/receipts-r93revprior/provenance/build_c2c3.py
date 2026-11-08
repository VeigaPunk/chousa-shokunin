#!/usr/bin/env python3
"""Build this seat's own C2 whitespace-quote trees and C3 tail-tally trees (no battery reuse)."""
import os
import shutil
import sys

S = "/fast/scratch/hyaku/chousa-r93/R93RevPrior"
LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
ENTRY_A = "corpus/knowledge/search-transparency-reporting-r84.md"
ENTRY_B = "corpus/knowledge/provenance-recording-r85.md"
QUOTE_ROW = '| Q2 | S214 | "date when each source was last searched or consulted." |'


def mirror(dst):
    shutil.rmtree(dst, ignore_errors=True)
    os.makedirs(os.path.join(dst, "corpus", "knowledge"))
    os.makedirs(os.path.join(dst, "corpus", "evidence"))
    shutil.copy2(os.path.join(LANE, "corpus", "SOURCES.md"), os.path.join(dst, "corpus", "SOURCES.md"))
    for rel in (ENTRY_A, ENTRY_B):
        shutil.copy2(os.path.join(LANE, rel), os.path.join(dst, rel))
    for rel in (os.path.join("corpus", "captures"), os.path.join("corpus", "evidence", "round57")):
        os.symlink(os.path.join(LANE, rel), os.path.join(dst, rel))
    return dst


def replace_once(path, old, new):
    text = open(path, encoding="utf-8").read()
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"SETUP {n} occurrences of {old[:50]!r} in {path}")
    open(path, "w", encoding="utf-8").write(text.replace(old, new))


def main():
    # C2: pristine mirror, space-inside-quotes, tab-inside-quotes.
    base = os.path.join(S, "c2")
    shutil.rmtree(base, ignore_errors=True)
    os.makedirs(base)
    mirror(os.path.join(base, "pristine"))
    for name, cell in (("ws-space", '" "'), ("ws-tab", '"\\t"')):
        d = mirror(os.path.join(base, name))
        # cell written literally; for the tab tree the file carries a real tab inside the quotes.
        replace_once(os.path.join(d, ENTRY_A), QUOTE_ROW, f"| Q2 | S214 | {cell} |".replace("\\t", "\t"))
    # C3: SKILL.md alone, clean and 215->214.
    c3 = os.path.join(S, "c3")
    shutil.rmtree(c3, ignore_errors=True)
    os.makedirs(c3)
    for name in ("clean", "t215"):
        d = os.path.join(c3, name)
        os.makedirs(d)
        shutil.copy2(os.path.join(LANE, "SKILL.md"), os.path.join(d, "SKILL.md"))
    replace_once(os.path.join(c3, "t215", "SKILL.md"), "PASS (215 cases, 0 skipped)", "PASS (214 cases, 0 skipped)")
    print("built", base, "and", c3)
    return 0


if __name__ == "__main__":
    sys.exit(main())
