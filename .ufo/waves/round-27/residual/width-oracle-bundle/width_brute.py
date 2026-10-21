#!/usr/bin/env python3
"""Brute-force: gate header-width functions vs the GFM (cmark-gfm) cell count.

Three width models are compared for every synthetic header row:
  base/dd : naive '|' split of the gate-preprocessed row   (dd72641e header_width)
  cb895a2 : naive '|' split after deleting every '\\|' pair (landed change (a))
  GFM     : cmark-gfm table cell count (reference implementation)
Also reports the gate's column-index model (naive split) vs GFM cell alignment.
"""
import itertools
import re
import sys

import cmarkgfm


def gate_preprocess(line):
    """Exactly the gate's row normalisation (trim, strip one leading/trailing '|')."""
    row = line
    row = row.lstrip()          # ${row#"${row%%[![:space:]]*}"}
    row = row.rstrip()          # ${row%"${row##*[![:space:]]}"}
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|"):
        row = row[:-1]
    return row


def width_naive(line):
    """dd72641e / base: header_width = number of '|'-split cells."""
    return len(gate_preprocess(line).split("|"))


def width_cb(line):
    """cb895a2 change (a): delete every non-overlapping '\\|' pair, then split."""
    row = gate_preprocess(line)
    deleted = re.sub(r"\\\|", "", row)          # bash ${row//'\\|'/}
    return len(deleted.split("|"))


def gfm_cell_count(line, maxk=10):
    """Number of header cells cmark-gfm sees, probed by delimiter-row width."""
    for k in range(1, maxk + 1):
        delim = "|" + "---|" * k
        text = line + "\n" + delim + "\n"
        html = cmarkgfm.github_flavored_markdown_to_html(text)
        if "<table>" in html:
            return len(re.findall(r"<th[ >]", html))
    return None


def main():
    alphabet = ["a", "|", "\\"]
    rows = []
    for n in range(1, 8):
        for combo in itertools.product(alphabet, repeat=n):
            s = "".join(combo)
            if s.count("|") < 2:
                continue
            rows.append(s)
    print("candidate header rows:", len(rows))
    mismatches = []
    for s in rows:
        g = gfm_cell_count(s)
        if g is None:
            continue
        d = width_naive(s)
        c = width_cb(s)
        if c != g or d != g:
            mismatches.append((s, g, d, c))
    print("rows where a model differs from GFM:", len(mismatches))
    print()
    print("%-18s %5s %5s %5s  %s" % ("header", "GFM", "dd", "cb", "flags"))
    for s, g, d, c in mismatches:
        flags = []
        if c != g:
            flags.append("CB-MISMATCH")
        if d != g:
            flags.append("DD-MISMATCH")
        print("%-18r %5s %5s %5s  %s" % (s, g, d, c, " ".join(flags)))
    # summary of mismatch classes
    print()
    cb_bad = [m for m in mismatches if m[3] != m[1]]
    dd_bad = [m for m in mismatches if m[2] != m[1]]
    print("cb895a2 width wrong on", len(cb_bad), "rows; dd72641e width wrong on",
          len(dd_bad), "rows")
    with open("/tmp/chousa-r27-residual-ResWidthFix/width-mismatches.txt", "w") as fh:
        for s, g, d, c in mismatches:
            fh.write("%r GFM=%s dd=%s cb=%s\n" % (s, g, d, c))


if __name__ == "__main__":
    main()
