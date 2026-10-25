# W3RevS079 — C3 row-normalization attack on the S079 row

Seat: round-44 wave-3 leaf, 2026-10-24. Scope: the S079 row of
`corpus/SOURCES.md` under a naive `|` split, and the source citation of
`corpus/knowledge/citation-version-binding-r36.md`. No fetch, no production
edits, no subagent dispatch.

## 1. Column count of the S079 row

The S079 row is line 89 of `corpus/SOURCES.md` (single physical line; the only
line in the file starting `| S079 |`).

Measured on the raw bytes (python3, read from the working tree):

- Pipe (`|`) characters: **12**
- Naive `line.split('|')`: **13 elements** — `''` leading, 11 non-empty
  cells, `''` trailing → **11 columns**
- Escaped pipes (`\|`): **0**
- Literal pipes inside any cell: **0**

Header (line 9) and separator (line 10) measure identically: 12 pipes,
13 naive elements, 11 columns, 0 escaped pipes. All **81** data rows measure
(12 pipes, 13 naive elements); the histogram has exactly one shape, so S079 is
not an outlier. Cells in order:

```
cell[1]  S079
cell[2]  RFC 7089, HTTP Extension for Time-Based Access to Resource States — Memento — https://www.rfc-editor.org/rfc/rfc7089.txt
cell[3]  spec
cell[4]  A
cell[5]  binding a citation to a timestamped prior state; the document puts archive veracity out of scope
cell[6]  section 2.1.1 of the committed capture, no fetch
cell[7]  a Memento-Datetime header is a promise that the reflected resource state will no longer change; an archived body may not be byte-to-byte the same as what the origin served
cell[8]  mined
cell[9]  2026-10-24
cell[10] 365d
cell[11] corpus/knowledge/citation-version-binding-r36.md
```

Verdict on the C3 attack: **no falsification here.** The row is width-normal
against the header under both a naive split and a GFM-aware one (they agree
because there are no embedded or escaped pipes). The r27 escaped-pipe lesson
(S043) does not bite this row.

## 2. Citation check on citation-version-binding-r36.md

The file has exactly one `source:` line and it is S079. Line 3, quoted:

> source: S079 — https://www.rfc-editor.org/rfc/rfc7089.txt — section 2.1.1,
> byte offset 14896 of the committed capture — RFC 7089, February 2013,
> Informational

- `source: S079` present: yes (line 3, the only `source: S0xx` line).
- `source: S081` present: **no**. The string `S081` does appear once, but in
  prose, not as a citation — line 28: "The staged citation id was S081. The
  lane id is S079 because the URL is the evidence and S079 is the next free
  lane id." A checker that greps bare `S081` instead of the `source: S081`
  citation form would false-positive here; the citation form is absent.
- Cross-check the other direction: the SOURCES S079 `used-by` cell is
  `corpus/knowledge/citation-version-binding-r36.md`, so row → entry and
  entry → row agree. The `r36` filename is a package label, not a lane round
  number (the entry says so itself at line 6), so filename/id mismatch is
  expected and documented, not a defect.

## 3. Calibration

- Claim strength: exact counts from a byte-level read of the working tree on
  2026-10-24; no inference beyond the measured strings.
- What would falsify: a row edit adding an embedded/escaped pipe (naive and
  GFM splits would then disagree at 13 vs 12), or a second `source:` line, or
  `source: S081` appearing. None observed.
- Residual: S081-as-prose (line 28) is the one near-miss for naive id greps;
  C3's normalization is clean on this row, so the attack needs another row or
  another axis.
