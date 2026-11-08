#!/usr/bin/env python3
"""Cell-level diff of corpus/SOURCES.md between two revisions, from committed bytes.

Usage: python3 -B sources-cell-diff.py --repo REPO OLDR NEWR
Prints one TSV line per changed cell: row, change, column, old, new.
Rows are keyed by the first column (id); every line beginning `| S` must
parse to exactly 11 cells or the script exits 2.
"""
import argparse
import subprocess
import sys

COLS = ["id", "source", "kind", "tier", "scope", "anchor", "teaches",
        "status", "opened", "recheck", "used-by"]


def show(repo, rev):
    r = subprocess.run(["git", "-C", repo, "show", f"{rev}:corpus/SOURCES.md"],
                       capture_output=True)
    if r.returncode != 0:
        sys.exit(f"git show failed for {rev}: {r.stderr.decode(errors='replace')}")
    return r.stdout.decode()


def rows(text):
    out, order = {}, []
    for ln, line in enumerate(text.splitlines(), 1):
        if line.startswith("| S"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) != 11:
                sys.exit(f"malformed row at line {ln}: {len(cells)} cells")
            if cells[0] in out:
                sys.exit(f"duplicate id {cells[0]} at line {ln}")
            out[cells[0]] = (ln, cells)
            order.append(cells[0])
    return out, order


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("old")
    ap.add_argument("new")
    a = ap.parse_args()
    old, _ = rows(show(a.repo, a.old))
    new, order = rows(show(a.repo, a.new))
    print("row\tchange\tcolumn\told\tnew")
    n = 0
    for rid in order:
        if rid not in old:
            for col, val in zip(COLS, new[rid][1]):
                print(f"{rid}\tADDED_ROW\t{col}\t<absent>\t{val}")
                n += 1
        else:
            for col, ov, nv in zip(COLS, old[rid][1], new[rid][1]):
                if ov != nv:
                    print(f"{rid}\tCELL_CHANGED\t{col}\t{ov}\t{nv}")
                    n += 1
    for rid in old:
        if rid not in new:
            print(f"{rid}\tDELETED_ROW\t<all>\t<see old>\t<absent>")
            n += 1
    print(f"# changed cells={n} rows_old={len(old)} rows_new={len(new)}", file=sys.stderr)
    sys.exit(0)


if __name__ == "__main__":
    main()
