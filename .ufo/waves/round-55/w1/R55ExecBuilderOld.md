# R55ExecBuilderOld — C1 earlier-span coverage

Verdict: ran the frozen candidate against earlier committed quote tables; 9 round-49 OLE rows are re-derived under the defined form, while all other runs reproduce committed spans exactly; no row was refused.

## Commands and observed output

Builder source: `6ca924995d48facbf704d2aa22ddaec236059039:tools/build-spans.py` (same bytes as the working-tree file; SHA-256 `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`). Quote tables and committed spans were extracted from base `dba605deb5cd5ed4874e0e3c39ba24737409cd80`. All outputs and extracted files were under `/fast/scratch/hyaku/chousa-r55/R55ExecBuilderOld`; cache was the read-only campaign `.qcache`.

Command pattern (executed for each available round):
```sh
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py \
  --quotes "$S/qN/quotes.tsv" --cache /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache \
  --out "$S/outN"
```
Observed build results: `round47 exit=0 SPANS_ROWS=35 WRITTEN=35`; `round49 exit=0 SPANS_ROWS=31 WRITTEN=31`; `round50 exit=0 SPANS_ROWS=67 WRITTEN=67`; `round51 exit=0 SPANS_ROWS=70 WRITTEN=70`; `round52 exit=0 SPANS_ROWS=39 WRITTEN=39`; `round53 exit=0 SPANS_ROWS=63 WRITTEN=63`; `round54 exit=0 SPANS_ROWS=33 WRITTEN=33`. All seven stderr streams were empty.

Command pattern (executed against each extracted committed spans directory):
```sh
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py \
  --quotes "$S/qN/quotes.tsv" --cache /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache \
  --out "$S/baseN/roundN" --check
```
Observed: `round47 SPANS_ROWS=35 STALE=0`; `round49 SPANS_ROWS=31 STALE=9`; `round50 SPANS_ROWS=67 STALE=0`; `round51 SPANS_ROWS=70 STALE=0`; `round52 SPANS_ROWS=39 STALE=0`; `round53 SPANS_ROWS=63 STALE=0`; `round54 SPANS_ROWS=33 STALE=0`. For round 49, TSV diff had 9 changed rows, and exactly the corresponding 9 span files differed. No row was refused in any build.

Independent defined-form check recomputed each output row's source digest, span slice and quote containment:
```
round47: rows=35 defined-form slice/quote/digest violations=0
round49: rows=31 defined-form slice/quote/digest violations=0
round50: rows=67 defined-form slice/quote/digest violations=0
round51: rows=70 defined-form slice/quote/digest violations=0
round52: rows=39 defined-form slice/quote/digest violations=0
round53: rows=63 defined-form slice/quote/digest violations=0
round54: rows=33 defined-form slice/quote/digest violations=0
```

## Measured changed rows

All changed rows are round 49: S100-1 through S100-3 and S101-1 through S101-6. Round-49 builder source at base, `corpus/evidence/round49/build-spans.py` lines 5–12 and 55–66, says it tries `.txt` then UTF-16LE-decoded `.raw`; the nine committed rows have the corresponding `.raw` digest (S100 `46d1866ce9afd51682e7e77cdf62612876da22c9bdbc9e8e299090128cb378f6`; S101 `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3`). In this capture, each of the nine quotes occurs 0 times in `.txt` and exactly once in UTF-16LE decoding. Candidate instead reads OLE `.raw` through `tools/capture-text.py`.

| Span | committed offset | candidate offset | candidate `QUOTE` char |
|---|---:|---:|---:|
| S100-1 | 1296 | 0 | 16 |
| S100-2 | 1423 | 71 | 151 |
| S100-3 | 2763 | 412 | 492 |
| S101-1 | 11166 | 11927 | 12007 |
| S101-2 | 11166 | 11892 | 11972 |
| S101-3 | 12081 | 12883 | 12963 |
| S101-4 | 11945 | 12715 | 12795 |
| S101-5 | 34370 | 25043 | 25123 |
| S101-6 | 13167 | 13969 | 14049 |

The candidate outputs for all nine are exact slices of the capture-text form, with the quote in each slice. The offsets and spans therefore changed because the old builder decoded the OLE bytes as UTF-16LE, rather than using the OLE document text form; no quote was lost or refused. A scan of the committed round-49 spans found embedded C0 controls in S100-3 (2), S101-1 (3), S101-2 (2), S101-3 (6); S100-3 also had one private-use/unassigned character. This scan is corroborative, not the basis for row classification.

## Other relevant observations / first falsifiers

- The required round-51–54 regressions are unchanged: 205 rows total, `STALE=0` for every round. Cache classification by unique URL: r51 six `RAW-other` + `.txt`; r52 three `RAW-other` + `.txt` and one ZIP + `.txt`; r53 four `RAW-other` + `.txt`; r54 three `RAW-other` + `.txt`.
- The r52 ZIP is S115, `Reporting_Format_Jap_202404.docx`. For its raw capture, the base r52 `docx_text` and candidate `capture-text.py` outputs were both 19,682 characters and equal; the checked S115 quote occurs 0 times in the `.txt` sidecar and once in the defined form. This explains why the ZIP row family did not change.
- Synthetic scratch probe A: `.raw` neither OLE nor ZIP, no `.txt`, quote present only in UTF-16LE decode. Observed `exit 1`, `build-spans: refused S124: no defined text form for 9e8e5e78071def448876fa92 (raw neither OLE nor zip, no .txt)`, output directory empty.
- Synthetic scratch probe B: OLE raw plus `.txt` sidecar containing a unique quote absent from the OLE defined form. Observed `exit 1`, `build-spans: refused S125: quote occurs 0x in f4362dceb48e990a78713fe2.raw: 'sidecar-only探测器字符串'`, output directory empty. This directly falsifies sidecar fallback for OLE.

These are coverage observations, not a C1 counter score. I did not run build/lint/test/format checks. No tools were installed. No production files were changed; only this report is retained.