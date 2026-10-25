# QuarantineS110 — hand-check, register `chousa` S110 (lane S094)

Scope: re-verify the `payload-absent` verdict on chousa-register row S110 against the on-disk capture of
https://aclanthology.org/2025.coling-main.108.pdf. No live fetch. Read-only; leaf member. Scratch
`/tmp/chousa-r48-QuarantineS110/` deleted.

## Inputs

- Register row: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:50`
  `| `chousa` | round3 | S110 | `payload-absent` | https://aclanthology.org/2025.coling-main.108.pdf | <3 quotes> | cited
  source, companion URLs and local artifacts were all checked; the quote is in none of them |`
  Quote spans verbatim (sha256): Q1 len=120 `c1af3425f427e1197b4356927543e714b2cb847979c6186e224c4809f9a13b7a`,
  Q2 len=118 `5ae0ed0786027ea12f132b2c1126d2d88ea7d7b4b4c93927c858f0f4190641e1`,
  Q3 len=120 `9dd4e9b04d54569342c1c6433e89b449a27b9a14720344e4801369371019813e`.
  Cross-check: `corpus/evidence/round42/receipts/examine.txt:29-31` records the same three spans for S110
  (digests `87f58ba44c35`, `5ae0ed078602`, `9dd4e9b04d54`; Q1's record is the span minus its trailing space)
  against capture `a9cf41709b6fa5028332d98c.txt`.
- Lane binding: `corpus/SOURCES.md:104` binds id S094 to this URL (round-47 adoption). Register S-number ≠ lane id;
  URL is the join key. The lane anchor column already records `char 20462` / `char 20650`, inside my Q2 span.
- Capture (pdftotext two-column render): `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/a9cf41709b6fa5028332d98c.txt`
  — 83246 bytes, 82876 chars, sha256 `d24f2315aad72d7ba64faa65d2da70bd05702f7404ac63a624a0803ffe78b136`
  (matches `corpus/evidence/round47/spans.tsv` digest column for S094 and `round42/receipts/digests.txt:17`).
  Cache-key check: `printf '%s' URL | sha256sum | cut -c1-24` → `a9cf41709b6fa5028332d98c` ✓.
- Companions: `a9cf41709b6fa5028332d98c.pdf` / `.raw`, both 807648 bytes, sha256
  `7f97317417cc3796e483ec1b32e678c69399425e21ac5f0452506f3afea93f0c` (the fetched PDF; .txt is its text render).

## Commands run (decisive output)

1. `wc -c`/`sha256sum` on the .txt → `83246`, `d24f2315…b136`. ✓ identity.
2. Raw region dump (`cap[a:b]` char slices):
   `[21381,21429) 'The Cohen’s Kappa (Cohen, 1960) score for inter-'` (line len 48, left col);
   `[21560,21612) 'annotator agreement is 0.792, indicating substantial'`;
   `[21613,21632) 'agreement among the annotat…'`; `[20304,20329) 'we re-assign labels based'` (right col, inside
   `[20282,20329)`); `[20459,20508) 'on the claim-relevant evidence gathered from open'`;
   `[20640,20682) 'websites. This manner results in total 202'`; `[20004,20022) 'We recruit two NLP'`;
   `[20151,20200) 'researchers proficient in English to manually an-'`;
   `[20330,20377) 'notate claim-evidence correlations based on the'`; `[20509,20529) 'annotation guideline'`.
3. `cap.count`/`cap.find` per contiguous slice — every slice above count=1 at the stated offset;
   `0.792` count=1, `re-assign` count=1, `The Cohen’s Kappa…` byte-find 21474.
4. Definitive check — rebuild left/right column streams (split at char 81) for lines in chars 19500–22000,
   join `-\s*\n\s*` hyphen splits, collapse whitespace, substring-test each quote:
   `Q1 in LEFT: True | RIGHT: False`; `Q2 LEFT: False | RIGHT: True`; `Q3 LEFT: True | RIGHT: False`.
   Witness lines: `…score for interannotator agreement is 0.792, indicating substantial agreement among the annotators. 3.3`;
   `we re-assign labels based … total 202 “`; `We recruit two NLP … based on the annotation guid…`.

## Per-quote verdicts

- Q1 `The Cohen’s Kappa (Cohen, 1960) score for interannotator agreement is 0.792, indicating substantial agreement
  among the ` — **present**, left column, chars 21381–21632. "interannotator" is the line-end hyphen split
  `inter-`/`annotator`; register truncates at 120 chars (sentence runs to "annotators.").
- Q2 `we re-assign labels … total 202` — **present**, right column, chars 20304–20682. Hyphens are intra-line;
  miss is pure two-column interleave. Continues `“NOT ENOUGH INFO" claims being relabeled.`
- Q3 `We recruit two NLP researchers … based on the annot` — **present**, left column, chars 20004–20529.
  `an-`/`notate` is the hyphen split; `annot` is the register's 120-char cut of `annotation`.

## Row verdict

`present` — all three register quotes occur verbatim in capture `a9cf41709b6fa5028332d98c.txt` once the
pdftotext two-column interleave is undone and line-end hyphen splits are joined. `payload-absent` is a mechanical
false negative (checker performs no de-interleave/join), consistent with the R47 QuarReg110 verdict and the
offsets staged into lane `SOURCES.md:104` at the R47 adoption. Not a fabrication row.

Residual risk: column boundary at char 81 verified only over 19500–22000; each slice independently `count=1`
elsewhere-checked. Offsets are code-point indices; byte offsets are +93 at Q1 start (21474).
