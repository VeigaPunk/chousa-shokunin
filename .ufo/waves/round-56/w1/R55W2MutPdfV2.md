# R55W2MutPdfV2 — mutation attack on round-55 `pdf-crosscheck.py`

Target: `corpus/evidence/round55/pdf-crosscheck.py` at lane commit `29cfb12abd70f688b48c0d17f31e636f2d81104a`
(frozen claims `1fc5d92b`), attacked via input fixtures + one edited pin copy, all under scratch
`/fast/scratch/hyaku/chousa-r56/R55W2MutPdfV2/`. Script invariant claimed by its docstring: every S123
quote occurs (whitespace-stripped, NFKC) in an independent pypdf extraction; the 21-row denominator is
"the full frozen set"; an empty quote fails; malformed rows fail without traceback; the PDF is pinned by sha256.

Tooling: nothing installed or upgraded. Interpreter: `uv run --with pypdf --offline python`
(pypdf 6.21.2 from the uv cache, matching the receipt's "pypdf 6.21.2 via uv run --with pypdf"; `--offline`
guarantees no network). Lane read via `git archive 29cfb12a | tar -x -C $S/lane`; never wrote the lane.

## Reproduction of corpus/evidence/round55/pdf-crosscheck.txt

`$ uv run --with pypdf --offline python $S/lane/corpus/evidence/round55/pdf-crosscheck.py $S/lane/corpus/evidence/round54/quotes.tsv` (stderr had 45 pypdf "Ignoring wrong pointing object" lines, not part of the receipt):
```
PDF_QUOTES=21 NOT_IN_INDEPENDENT=0 RAW_NOT_IN=14
exit=0
```
= receipt run 1 byte-identical. The other four receipt runs reproduced exactly (driver outputs, exit codes 1):
```
renamed     -> row denominator mismatch S123: got 20, expected 21
emptyquote  -> empty quote in S123 row 35
headeronly  -> row denominator mismatch S123: got 0, expected 21
tab         -> malformed quotes.tsv row 15: expected 4 cells, got 5
```

## Assigned fixtures (driver.py; each fixture run: `sys.executable $S/lane/.../pdf-crosscheck.py $S/fix/<name>.tsv`)

Frozen TSV: 33 data rows = 6×S121 + 6×S122 + 21×S123 (lines 14–34). Classification of the 21 S123 quotes
against one pypdf extraction: 7 hit raw (lines 14,15,18,19,21,22,34), all 21 hit NFKC.

| fixture | mutation | rc | first stderr line / stdout |
|---|---|---|---|
| dup22.tsv | first S123 row duplicated → 22 rows | 1 | `row denominator mismatch S123: got 22, expected 21` |
| wsquote.tsv | S123 line 14 quote = one space | **0** | `PDF_QUOTES=21 NOT_IN_INDEPENDENT=0 RAW_NOT_IN=14` |
| bom.tsv | UTF-8 BOM before `id` | 1 | `malformed quotes.tsv header` |
| crlf.tsv | all LF → CRLF | 0 | `PDF_QUOTES=21 NOT_IN_INDEPENDENT=0 RAW_NOT_IN=14` (parses, correctly no false alarm) |
| nfkc-only.tsv | line 14 `文`(U+6587)→`⽂`(U+2F42, Kangxi radical; NFKC→U+6587, verified) | 0 | `PDF_QUOTES=21 NOT_IN_INDEPENDENT=0 RAW_NOT_IN=15` |
| wrongpin.py | script copy, pin `cb3f…`→`db3f…` | 2 | `ENV_CHANGED S123: sha256 cb3ffb…c2a41 != db3ffb…c2a41` |

## Denominator probes — 'exactly the frozen set' or 'any 21 rows'?

```
swap-foreign.tsv     : 21 S123 rows, line 14 quote replaced by ext[9000:9040]
                       (a 40-char substring of the extraction, provably not one of the 21 frozen quotes)
  rc=0  PDF_QUOTES=21 NOT_IN_INDEPENDENT=0 RAW_NOT_IN=15
rename-rebalance.tsv : line 14 sid S123→S999 (silently ignored by `sid in DOCS`) + one appended
                       S123 row quoting ext[9100:9130] → count back to 21
  rc=0  PDF_QUOTES=21 NOT_IN_INDEPENDENT=0 RAW_NOT_IN=14
```
Both pass. **The 21-row denominator means "any 21 rows labelled S123", not "the frozen set"**: the script
counts rows (`counts[sid] += 1`), never compares quote contents against a frozen list, and rows whose sid is
not in `DOCS` are never validated at all (S121/S122 columns ride along unchecked).

## Findings (reported against frozen predicates, not patched)

1. **SURVIVED — whitespace-only quote.** `corpus/evidence/round55/pdf-crosscheck.py:47` guards `if not quote:`
   only; a space-only quote is truthy, then `raw(" ") == ""` and `"" in s` is True for any string, so it passes
   both presence checks and counts toward the denominator (`not q: False; '' in 'x': True` verified). The
   round-54 F6 fix ("an empty quote fails", docstring line 3-4) does not cover whitespace-only quotes: one of the
   21 verified quotes can be blank. Minimal fix shape (not applied): `if not raw(quote): fail(...)`.
2. **Coverage gap — denominator is any-21.** See probes; quote-set identity and non-S123 rows are unchecked,
   so a rewritten 21-row set that quotes arbitrary PDF substrings would exit 0.
3. **NFKC-only quotes exit 0 by contract.** The docstring's predicate is the NFKC-normalised match; `RAW_NOT_IN`
   (15 vs 14) is the only signal and does not affect the exit code (`sys.exit(0 if bad == 0 else 1)` uses `bad`
   only). Consistent with the documented claim; noting the raw check is advisory.
4. **Killed:** duplicate row, BOM header, tab-in-quote, renamed/missing/empty rows, and the sha256 pin
   (ENV_CHANGED, exit 2 — the pin genuinely gates the capture). CRLF input parses without a false failure, as claimed.

Restoration evidence: attack ran only on scratch copies (`$S/lane` from `git archive`, `$S/fix/*`, `$S/fix/wrongpin.py`).
`sha256sum` of the two lane inputs before vs after the whole run: identical (LANE UNTOUCHED). No git/jj commands
beyond read-only `git archive`; scratch removed at session end.

VERDICT: attacked round-55 pdf-crosscheck.py with 7 input mutants + 1 pin mutant: 5 killed (dup, BOM, tab/receipt set, pin, CRLF-inert), 1 survived (whitespace-only quote passes as a verified quote — the "empty quote fails" predicate has a hole), and the 21-row denominator means ANY 21 S123 rows, not the frozen set.
