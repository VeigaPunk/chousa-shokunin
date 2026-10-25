# ReviewOpenS085 — round 47 wave 1: open lane source S085 (FEVER dataset page)

Item: open S085 (https://fever.ai/dataset/fever.html) from capture `.qcache/5a631adb18988a1a2421ce75.txt`; check if each candidate quote is contiguous and verbatim; give at least 3 verified quotes; list staged sentences it supports, contradicts or overstates; give the true offsets for the anchor cell and draft a corrected cell. No fetch, no lane production edits, no tool installs. The `skill://godspeed` file was not found on disk (`rg -l -i 'name:\s*godspeed' ~/.omp ~/.claude ~/.config` returned nothing).

## Verdict
S085 grounds the base entry's FEVER sentences. All four candidates are verbatim in the capture except the "necessary evidence" sentence, which breaks across a newline after `sentence(s)`, so it needs two slices. The held anchor `char 2349` is the true offset of the longer slice `evidence : A list of evidence sets (...)`, but it is not a manifest quote offset, so it fails `ANCHOR_BOUND`. The corrected cell below passes the counter's own rule.

## Capture identity
Path: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/5a631adb18988a1a2421ce75.txt`
- sha256 `e18eeb26a5a5902e10f0e0b25a9886d99bbbafcf8adfb85b7846bbd569d1ba92`. It equals the `capture_sha256` in round46/spans.tsv rows 2–3.
- 4146 bytes and 4146 chars (ASCII). It is HTML-to-text with no math markup. The build line is `Build info: refs/heads/live build 385` / `Last updated: 2026-04-02T10:58:13.945736`.

## Candidates (Python `str.find`, count, 100 chars either side; `\n` shown escaped)
1. `NOT ENOUGH INFO`: find=2296, count=**3** (2296, 2527, 3601). It is contiguous but NOT unique and only 3 words, so it can't be used alone. Replacement: q1 or q2 below.
   BEFORE `'d : The ID of the claim\n\n label : The annotated label for the claim. Can be one of SUPPORTS|REFUTES|'`
   AFTER `' .\n\n claim : The text of the claim.\n\n evidence : A list of evidence sets (lists of [Annotation ID, E'`
2. `[Annotation ID, Evidence ID, null, null]`: find=2464, count=1. Contiguous and unique.
   BEFORE `'st of evidence sets (lists of [Annotation ID, Evidence ID, Wikipedia URL, sentence ID] tuples) or a '`
   AFTER `' tuple if the label is NOT ENOUGH INFO .\n\n (the Annotation ID and Evidence ID fields are for interna'`
3. The SUPPORTS/REFUTES necessary-evidence sentence is **NOT contiguous**. `For the first two classes, the annotators also recorded the sentence(s) forming the necessary evidence for their judgment.` has find=-1 because the capture reads `'d the sentence(s)\n forming the necessary evidence for their '`. Replacement slices: q4 @986 (11 words) and q5 @1059 (7 words). The gap at 1057–1058 is `\n `. The page header also says `Supported , Refuted or\n NotEnoughInfo`, not the label tokens SUPPORTS/REFUTES (q8 @917).
   BEFORE(q4) `'ence they were derived from. \n The claims are classified as Supported , Refuted or\n NotEnoughInfo . '`
   AFTER(q4) `'\n forming the necessary evidence for their judgment.\n \n\n \n\n \n\n \n \n Download Links\n\n \n Training Datas'`
4. `A list of evidence sets`: find=**2360**, count=1. Contiguous and unique.
   BEFORE `'aim. Can be one of SUPPORTS|REFUTES|NOT ENOUGH INFO .\n\n claim : The text of the claim.\n\n evidence : '`
   AFTER `' (lists of [Annotation ID, Evidence ID, Wikipedia URL, sentence ID] tuples) or a [Annotation ID, Evi'`
- `Pre-processed Wikipedia Pages (June 2017 dump)`: find=**1271**, count=1.
   BEFORE `'ask Development Dataset (Labelled) / (Unlabelled) \n\n Shared Task Blind Test Dataset (Unlabelled) \n\n '`
   AFTER `' \n\n License \n\n \n \n To replicate the results in the NAACL paper use the following files.\n When concat'`

## Verified quotes (TSV: id, offset, quote). Every row is count=1 and `cap[o:o+len(q)]==q` is True
```
S085-q1	2265	Can be one of SUPPORTS|REFUTES|NOT ENOUGH INFO
S085-q2	2459	or a [Annotation ID, Evidence ID, null, null] tuple if the label is NOT ENOUGH INFO
S085-q3	2360	A list of evidence sets (lists of [Annotation ID, Evidence ID, Wikipedia URL, sentence ID] tuples)
S085-q4	986	For the first two classes, the annotators also recorded the sentence(s)
S085-q5	1059	forming the necessary evidence for their judgment.
S085-q6	1271	Pre-processed Wikipedia Pages (June 2017 dump)
S085-q7	2589	are for internal use only and are not used for scoring
S085-q8	917	The claims are classified as Supported , Refuted or
```
Check output (python3, verbatim; my comment fields trimmed): `S085-q1 2265 ... count=1 words=7 check=True`, `S085-q2 2459 ... count=1 words=16 check=True`, `S085-q3 2360 ... count=1 words=16 check=True`, `S085-q4 986 ... count=1 words=11 check=True`, `S085-q5 1059 ... count=1 words=7 check=True`, `S085-q6 1271 ... count=1 words=6 check=True`, `S085-q7 2589 ... count=1 words=11 check=True`, `S085-q8 917 ... count=1 words=9 check=True`, `X-necessary-full -1 ... count=0 words=18 check=False`, `X-ann-tuple 2464 ... count=1 words=6 check=True`.
Check expression: `o=cap.find(q); n=cap.count(q); check = o>=0 and cap[o:o+len(q)]==q`.
Phrases a bullet can backtick: q1 `NOT ENOUGH INFO`, q2 `null, null`, q3 `evidence sets`, q4 `first two classes`, q5 `necessary evidence`, q6 `June 2017 dump`, q7 `internal use only`.

**Hazard (operability):** q1 contains literal `|`. If it is pasted into a SOURCES.md Registry cell, `row_for` splits the row into 13 cells instead of 11 (simulated: `cells if q1 pasted into anchor: 13`). That fails `CITES_BOUND` and `ANCHOR_BOUND` for S085. Use q1 only in the entry and spans.tsv. Rows should use q2 or q3.

## Anchor offsets and corrected cell
- Round-46 manifest: `S085-1.txt len 183 slice_ok True quote_pos 80 => offset 2360` and `S085-2.txt len 206 slice_ok True quote_pos 80 => offset 1271`. The span offsets are 2280 and 1191, plus position 80.
- Held cell (SOURCES.md:95): `exact slice at capture char 2349: evidence : A list of evidence sets (...)`. The command printed `held slice at 2349 ok: True`, so the slice is real, but 2349 is the offset of `evidence : `, not of the manifest quote. The counter rule gave `held [2349] False`, which is why claims.md:125–126 records it as a failing leg.
- Draft corrected anchor cell (no `|`; counter-rule simulation `draft [2360, 1271] True`):
  `the evidence field definition, exact slice at capture char 2360: A list of evidence sets (lists of [Annotation ID, Evidence ID, Wikipedia URL, sentence ID] tuples); the download list's exact slice at capture char 1271: Pre-processed Wikipedia Pages (June 2017 dump)`
- Second condition for C3: the S085 row's `used-by` (cell 11) must also name `corpus/knowledge/claim-support-test-r37.md`. It currently names only `evidence-pool-versioning-r39.md`, so `CITES_BOUND` cannot count S085 until a scribe adds it. If the base entry quotes q1, q2, q4 or q5, those quotes need round-47 span rows; `round47/spans` does not exist yet (`ls: cannot access .../round47/spans`).

## Staged sentences S085 supports
- Base entry, lines 21–25: `FEVER formalises this as a third label: NOT ENOUGH INFO, whose evidence tuple is [Annotation ID, Evidence ID, null, null] — a declared null, where SUPPORTS and REFUTES each carry the sentence(s) that formed the necessary evidence.` This is supported by q1, q2, q4 and q5.
- Base `source:` line: `build refs/heads/live build 385, last updated 2026-04-02`. This matches the capture's build line.
- Staged S097 row claim: labels SUPPORTS/REFUTES/NOT ENOUGH INFO; the first two record the necessary-evidence sentence(s); NEI carries a null evidence tuple. This is supported by q1, q2, q4 and q5.
- Amendment, lines 38–39, the class half only: `Claims are classified Supported, Refuted or NotEnoughInfo` matches q8 plus `NotEnoughInfo` at 1022. The `0.6841 in Fleiss kappa` half is cited to S113 (S092), and this page does not carry it.
- Amendment, lines 68–69: `span-plus-verdict-plus-evidence-set` is consistent with q3 (a list of evidence sets).

## Overstatements and contradictions (both sides quoted)
1. **Base, line 76, Unknown (stale against the lane):** `The FEVER paper itself was retrievable only as an abstract via aaron (1,502 characters); the dataset page and PEOPLEPROFILES carry the definitions actually cited here.` On the lane side, the Registry holds S086 = FEVER NAACL PDF N18-1074, and round46/spans.tsv quotes it at 15189 (`used the June 2017 Wikipedia dump, processed`) and 41931. Adopting this line verbatim would contradict the lane's own holdings. Also, this page carries a label set and an evidence format, not a *definition* of support: no capture sentence defines support.
2. **Base, line 46:** `The FEVER/CFEVER shape asks for a span *plus* a judgement *plus* a declared null.` On the source side, q3 says evidence is `[Annotation ID, Evidence ID, Wikipedia URL, sentence ID]`. FEVER binds to a page-and-sentence id, not a character span. This is an overstatement in calibration only, not a contradiction.
3. **Base, lines 24–25:** `SUPPORTS and REFUTES each carry the sentence(s)`. On the source side, q3 says `A list of evidence sets`, and the Supports example has 5 alternative sets (one has 2 pages). One claim carries several alternative sets, not one sentence group, so this is an undercount. It is consistent with the amendment's "evidence-set".
4. **Base, line 21:** `FEVER formalises this as a third label`. Here `this` is PEOPLEPROFILES' 2026 no-selection rule, while FEVER is 2018. The page states no derivation, so the wording implies a lineage the source doesn't give. Mild.
5. **Internal inconsistency in the page:** the field definition (q2) says NEI evidence is `a [Annotation ID, Evidence ID, null, null] tuple`, but the NEI example nests it, as `"evidence": [ [ [<annotation_id>, <evidence_id>, null, null] ] ]`. The entry follows the definition, which is acceptable.
No staged sentence is contradicted on a FEVER fact. q7 (`not used for scoring`) is unused by both entries; it could support a calibration bullet saying the IDs carry no scoring weight.

## Commands run (decisive lines)
- python3 hash, find and count over candidates. Output: `sha256 e18eeb26…ba92 bytes 4146 chars 4146`; `'NOT ENOUGH INFO' find 2296 count 3`; `'[Annotation ID, Evidence ID, null, null]' find 2464 count 1`; `'A list of evidence sets' find 2360 count 1`; `'Pre-processed Wikipedia Pages (June 2017 dump)' find 1271 count 1`.
- `rg -n '\| S085 \|' corpus/SOURCES.md` returned line 95, whose anchor is `char 2349` (the cell quoted above).
- `rg -n 'S085|S097' round46/spans.tsv merge/chousa/SOURCES.append.md` returned spans.tsv rows 2 and 3 (offsets 2280 and 1191) and staged row S097 at SOURCES.append.md:22. Staged S085 at line 10 is an unrelated GB/T 7714 row, an id collision in the campaign numbering.
- python3 span-file, quote, context and TSV check, as quoted above. Also `NOT ENOUGH INFO offsets [2296, 2527, 3601]`.
- python3 simulation of the counter's anchor rule (`CHAR_RE` from c3-count.py): `held [2349] False`, `draft [2360, 1271] True pipe_in_cell False`, `cells if q1 pasted into anchor: 13`.
- I read c3-count.py, claims.md (lines 110–126) and both staged entries.

## Residual risk and gaps
- `ANCHOR_BOUND` passes for S085 only if the round-46 manifest and span files stay unchanged. If a scribe cites a round-47 quote in the cell instead, that span row must exist first.
- I ran nothing against inference-ground.py, because the lane entries are not drafted yet.
- Scratch: none created (only inline python with `cd /tmp`). No installs.
