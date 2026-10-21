#!/usr/bin/env python3
"""Compare the candidate shared-split (parent working copy) against cmark-gfm.

Candidate transform (verbatim from the lane working copy, tools/research-gate.sh
metadata_registry_load):
    [[ $row == *'|' && $row != *'\|' ]] && row=${row%|}     # outer pipe strip
    split_row=${row//\\/\\\\}                                 # double backslashes
    split_row=${split_row//'\\|'/'\\|'}                      # (glob) '\\|' -> '|'
    IFS='|' read -a cells <<<"${split_row}|__chousa_registry_end__"
"""
import html
import itertools
import re
import subprocess
import sys

import cmarkgfm

ROWS_FILE = "/tmp/chousa-r27-residual-ResWidthFix/corpus_rows.txt"
SPLIT_FILE = "/tmp/chousa-r27-residual-ResWidthFix/corpus_split.txt"


def gfm_cells(line, maxk=12):
    """Return the list of header cell texts cmark-gfm sees, or None."""
    for k in range(1, maxk + 1):
        delim = "|" + "---|" * k
        html_out = cmarkgfm.github_flavored_markdown_to_html(line + "\n" + delim + "\n")
        if "<table>" in html_out:
            cells = re.findall(r"<th[^>]*>(.*?)</th>", html_out, re.S)
            return [html.unescape(re.sub(r"<[^>]+>", "", c)).strip() for c in cells]
    return None


def naive_cells(line):
    row = line.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|"):
        row = row[:-1]
    return [c.strip() for c in row.split("|")]


def main():
    rows = [l.rstrip("\n") for l in open(ROWS_FILE)]
    # run the bash candidate split over the corpus
    with open(SPLIT_FILE, "w") as fh:
        pass
    script = r'''
while IFS= read -r row; do
  [[ $row == *'|'*'|'* ]] || { printf 'SKIP\n'; continue; }
  row=${row#"${row%%[![:space:]]*}"}
  row=${row%"${row##*[![:space:]]}"}
  [[ $row == '|'* ]] && row=${row#|}
  [[ $row == *'|' && $row != *'\|' ]] && row=${row%|}
  split_row=${row//\\/\\\\}
  split_row=${split_row//'\\|'/'\|'}
  IFS='|' read -a cells <<<"${split_row}|__chousa_registry_end__"
  cells=("${cells[@]:0:${#cells[@]}-1}")
  out=""
  for c in "${cells[@]}"; do
    c=${c#"${c%%[![:space:]]*}"}
    c=${c%"${c##*[![:space:]]}"}
    out+="${c}"$'\x1f'
  done
  printf '%s\n' "${out%$'\x1f'}"
done < "$1"
'''
    with open("/tmp/chousa-r27-residual-ResWidthFix/cand_split.sh", "w") as fh:
        fh.write(script)
    subprocess.run(["bash", "/tmp/chousa-r27-residual-ResWidthFix/cand_split.sh",
                    ROWS_FILE], stdout=open(SPLIT_FILE, "w"), check=True)
    splits = [l.rstrip("\n") for l in open(SPLIT_FILE)]

    cnt_bad, txt_bad = [], []
    for row, sp in zip(rows, splits):
        if sp == "SKIP":
            continue
        cand = sp.split("\x1f") if sp else [""]
        g = gfm_cells(row)
        if g is None:
            continue
        if len(cand) != len(g):
            cnt_bad.append((row, g, cand))
            continue
        # cmark's HTML is post-inline; the candidate yields the RAW cell text.
        # Compare after applying CommonMark's inline backslash-escape rule.
        def inline(t):
            out = []
            i = 0
            while i < len(t):
                if t[i] == "\\" and i + 1 < len(t) and t[i+1] in "!\"#$%&'()*+,-./:;<=>?@[]^_`{|}~":
                    out.append(t[i+1]); i += 2
                else:
                    out.append(t[i]); i += 1
            return "".join(out)
        if [inline(c.strip()) for c in cand] != g:
            txt_bad.append((row, g, cand))
    print("rows compared:", sum(1 for r, s in zip(rows, splits) if s != "SKIP"))
    print("candidate CELL-COUNT mismatches vs cmark-gfm:", len(cnt_bad))
    print("candidate CELL-TEXT mismatches vs cmark-gfm:", len(txt_bad))
    for row, g, c in cnt_bad[:25]:
        print("  COUNT %r gfm=%s cand=%s" % (row, g, c))
    for row, g, c in txt_bad[:25]:
        print("  TEXT  %r gfm=%s cand=%s" % (row, g, c))
    # naive (cb895a2/base) split for contrast
    n_bad = sum(1 for row in rows
                if (lambda g: g is not None and
                    len(naive_cells(row)) != len(g))(gfm_cells(row)))
    print("naive-split CELL-COUNT mismatches vs cmark-gfm:", n_bad)


if __name__ == "__main__":
    main()
