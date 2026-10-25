# W3 — S079 is bound to the RFC 7089 URL by document, not by arithmetic

Scope: falsification check against the lane's own files. Read-only; nothing
outside this report was touched.

## 1. The lane row (corpus/SOURCES.md:89)

Lane row S079, id and URL cells quoted verbatim:

> `| S079 | RFC 7089, HTTP Extension for Time-Based Access to Resource States — Memento — https://www.rfc-editor.org/rfc/rfc7089.txt | spec | A | ...`

- Only one row in `corpus/SOURCES.md` contains `rfc7089` (grep: line 89 alone).
- The lane table's last rows are S079 (RFC 7089), S080 (WARP FAQ,
  `https://warp.ndl.go.jp/en/info/qanda`), S081 (NDL E2867,
  `https://current.ndl.go.jp/e2867`) — lines 89–91, immediately followed by the
  round-44 log at line 255.

## 2. The staged row (SOURCES.append.md:9)

The staged file's row carrying the same URL, id and URL cells quoted verbatim:

> `| S081 | RFC 7089, HTTP Extension for Time-Based Access to Resource States - Memento — https://www.rfc-editor.org/rfc/rfc7089.txt | spec | A | ...`

Same URL cell, different id: the staged file calls this source **S081**; the
lane calls it **S079**. (Title separators differ — em-dash in the lane, " - "
staged — so the id-to-document binding is carried by the URL cell, the only
field identical in both.)

Worse for arithmetic: the staged file itself uses the id **S079** for a
*different* document — line 7:

> `| S079 | PRISMA-S: an extension to the PRISMA Statement ... — https://doi.org/10.1186/s13643-020-01542-z | paper | A | ...`

So the string "S079" names RFC 7089 in the lane and PRISMA-S in the staging
file. The id alone cannot identify the document in either file; the URL cell
does.

## 3. What arithmetic would have produced, and why it is wrong

`MERGE-REPORT.md:9` records the arithmetic inputs: "lane registry currently
holds **78** rows; first staged id is **S079**". Three arithmetic routes and
their outputs:

- **Carry the staged id (offset 0):** RFC 7089 → lane S081. Wrong: landed lane
  S081 is the NDL E2867 row (`https://current.ndl.go.jp/e2867`) — a collision
  with a different document's URL.
- **Positional (3rd staged row + 78 existing rows):** row 81 → S081. Same wrong
  answer by the same collision.
- **Sequential continuation (first staged id S079 → next free lane id S079):**
  lane S079 = PRISMA-S (`https://doi.org/10.1186/s13643-020-01542-z`). Wrong:
  the landed lane S079's URL cell is `https://www.rfc-editor.org/rfc/rfc7089.txt`.

No constant offset reproduces the landed binding either: staged→lane offsets
are −2 (S081→S079), −11 (S091→S080), −11 (S092→S081). The one rule that maps
every landed row correctly is URL equality: the row whose URL cell is
`https://www.rfc-editor.org/rfc/rfc7089.txt` is lane S079, whatever id it
carried in staging.

## 4. The lane's own statement of the rule

Round-44 log, `corpus/SOURCES.md:255` (quote of its final sentence):

> "Ids assigned by URL to the next free lane ids, not by arithmetic."

The landed files satisfy that sentence: lane S079's URL cell and staged S081's
URL cell are byte-identical, and every arithmetic alternative lands on a row
whose URL cell differs.

## Verdict

The claim survives. The S079 ↔ RFC 7089 binding is documented in the URL cells
of both files (lane :89, staged :9), not derivable from ids, row positions, or
any constant offset; all three arithmetic alternatives produce a document
collision (S081=E2867 carry-over, positional S081, or S079=PRISMA-S).
