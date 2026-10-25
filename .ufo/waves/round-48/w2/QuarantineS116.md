# Quarantine hand-check — chousa S116

**Verdict: `payload-absent` FALSIFIED — all three quotes are PRESENT in the cited document.** The absence verdict is an artefact of the checker matching against the two-column `pdftotext -layout` render, where right-column (figure) text interleaves into the quoted runs.

## Row under test

- `absent-defect-register.md:54`: `chousa | round4 | S116 | payload-absent | https://aclanthology.org/N18-1074.pdf` with 3 quotes (`0.6841 Fleiss κ` run, `We used the June 2017 Wikipedia dump`, `in 31.75% … composition of eviden`).
- Authoritative row: `merge/chousa/SOURCES.append.md` and `lanes/chousa/round4/SOURCES-PROPOSED.md` stage the FEVER PDF quotes under **Gate — S121** (`lanes/chousa/round4/SOURCES-PROPOSED.md:88-93`); a later id-renumbering assigned `S116` (lint JSONs show the same URL+quotes under staged ids S110/S111). Noted for calibration; the URL+quotes pair is unique and unambiguous.

## Local capture checked (no live fetch)

- `.qcache/1c15b611118dee97e4105fcf.pdf` — 460,896 B (matches gate's "HTTP 200, 460,896 bytes"), sha256 `5d328bad901f488c4cff1dd073b55e30653b29c9c21c48700b926421cb84c9f7`, `%PDF-1.5`, FEVER NAACL-HLT 2018 paper.
- `.qcache/1c15b611118dee97e4105fcf.txt` — 60,153 B, sha256 `c508913aba177ae4d33b29b7076f305bbac578a1ea11d39e30ddee2d787d563f`. `sha256sum` of my own `pdftotext -layout` render of the same PDF is identical → this `.txt` IS the `-layout` render.
- NB: the gate claims "text extracted with `pdftotext -layout`, 42,707 bytes"; my plain `pdftotext` (no flag) yields exactly 42,707 B (sha256 `dcb19940fdcf27043852df9d8e4e442cfe8c2a72b1be4554c7e9a7fb103939cb`). The checker's 60,153 B `.txt` is the `-layout` variant — the wrong artifact for contiguity testing.

## Measurements (commands run)

```
cd .qcache
grep -cF "We used the June 2017 Wikipedia dump" 1c15b611118dee97e4105fcf.txt   → 0   (absent in -layout)
#  fragments ARE present: byte offsets via grep -boF:
#    5544  "in 31.75% of the claims more"
#    6431  "in inter-annotator agreement of 0.6841"
#    15301 "used the June 2017 Wikipedia dump"
#  -layout lines 61-66, 71-74, 157 interleave figure text:
#    "in 31.75% of the claims more / The 1992 Los Angeles riots, / than one
#     sentence was considered appropriate ev- / also known as the Rodney King
#     riots / idence. …"
pdftotext 1c15b611118dee97e4105fcf.pdf raw.txt        → 42,707 B
#  python3 fold check, fold = re.sub(r'\s+',' ',raw.txt):
#    fold-offset 4119:  "in 31.75% of the claims more than one sentence was
#                       considered appropriate evidence. Claims require
#                       composition of eviden"  → True
#    fold-offset 4457:  "resulting in inter-annotator agreement of 0.6841 in
#                       Fleiss κ (Fleiss, 1971) in claim verification
#                       classification, and 95" → True
#    fold-offset 11760: "We used the June 2017 Wikipedia dump" → True
#    fold-offset 15792: "We found that 91.2% of the examples were annotated
#                       correctly." → True
#    fold-offset 16826: "When compared against the super-annotators, all
#                       except two annotators achieved > 90% precision and
#                       all but 9 achieved recall > 70% in evidence
#                       retrieval." → True
```

All five Gate quotes (the register's three plus the two S121 gate quotes omitted from the register) are present verbatim under whitespace folding in the plain `pdftotext` reading-order stream; each is a contiguous run within the paper's left column. The only folds needed are line breaks and the print hyphenation `evi-/dence`.

## Reason

The lane's own "Column note" (Gate S116 block) warns two-column PDF extraction interleaves columns; for this PDF the interleaving occurs inside the quoted spans, so every long quote fails an exact-substring test on the `-layout` artifact while succeeding on the reading-order stream. The quotes are faithful transcriptions of the printed text — no fabrication. Classification: **present** (register's `payload-absent` is a checker artifact; remedy is rechecking against a column-aware extraction, not quote correction).

## C1 impact

This row counts as a checked non-fabrication: the ABSENT verdict dissolves under a plain `pdftotext` render of the same captured bytes. Two defect surfaces remain real but different: (a) the row-id churn (staged S121 → register S116 vs. slarc row also S116 in `SOURCES.append.md:41`) makes the register's id binding ambiguous, and (b) the gate's stated extraction byte count (42,707) corresponds to plain `pdftotext`, not the claimed `-layout` mode.
