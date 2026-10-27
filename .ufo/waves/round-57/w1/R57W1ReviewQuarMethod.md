# R57W1ReviewQuarMethod — method review of quarantine batches A-D

Seat: R57W1ReviewQuarMethod (reviewer, leaf). Scope: review the four quarantine batch items' instructions
for conformance to the register header classes, and sample-check S086 + S120 myself. Read-only;
no lane/counter edits. Scratch: /fast/scratch/hyaku/chousa-r57/R57W1ReviewQuarMethod (deleted on yield).

## 1. Register header classes (as committed)

`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` defines:

- `payload-absent` — "every relevant source fetched cleanly and the quote is in none of them" → **the
  fabrication class: verify by hand**, then correct the quote or refuse the row.
- `unreachable` — source never fetched → re-fetch or mark unverifiable, "do NOT call it a fabrication".
- Header warning: "A quote the checker could not match is a CANDIDATE, not a verdict."
- Second section ("Rows whose quotes were NEVER CHECKED"): prose rows `chousa` S100`-S103` carry
  "the gate block named no locator" — the unchecked family, unverifiable, NOT fabrication.

Slice re-derived (fields $2/$4/$5 of the two tables):
`awk -F'|' '$2~/chousa/ && $5~/payload-absent/'` → 20 rows; `… && $5~/no locator/` → 4 rows.
= 24 data rows, matching batch D's expectation (20 payload-absent + 4 prose).

## 2. Conformance of the four batch items (w1-spec.json, items R57W1QuarA/B/C/D)

Conformant elements:
- Each payload-absent row is assigned a PRESENT/ABSENT/UNVERIFIABLE verdict with an "honest sweep —
  name the sweep commands" requirement, and an explicit fold list (exact, whitespace-collapsed,
  per-line substrings) since the generator's eleven folds are unknown. (A,B,C)
- Prose rows S100-S103 get UNVERIFIABLE-as-classified with the register's own reason. (D)
- The docx defined form is correctly named: capture-text.py stdout for OLE/zip, not the `.txt`
  sidecar — essential, because the sidecar for the niph docx is zip bytes (`file` → "Zip archive
  data…"; grep of the sidecar for the quotes gives 0 even though the quotes are present).
- Batch D re-derives the slice count (24) — confirmed above.

**Non-conformant element (finder, all four items): the locator step.** Every item says: "open the
row in <LANE>/corpus/SOURCES.md [by register id], take its first URL". The register is shokuknow's
corpus-expansion artifact with its own id space (pre-remap staging ids; shokuknow's own
SOURCES-PROPOSED.md holds the same rows under shifted ids, e.g. ncpssd.cn = S091, niph docx = S125).
The lane registry (chousa-shokunin corpus/SOURCES.md) disagrees on every id. Measured:

```
0/20 register ids resolve to the same URL in chousa-shokunin corpus/SOURCES.md
18 ID-COLLISIONS + 2 ORPHANS (register S077 doi.org-s13643 and S086 ncpssd.cn: neither URL string
appears anywhere in the lane's SOURCES.md, neither key is in corpus/captures/, neither in
refetch.tsv — grep 's13643-020-01542-z\|ncpssd.cn' → 0). S095 is a collision too: its URL appears
verbatim on lane row S100 (corpus/SOURCES.md:110), just not on id S095.
```

Examples: register S086 = https://www.ncpssd.cn/ vs lane S086 = FEVER N18-1074.pdf; register S120 =
niph docx vs lane S120 = Cochrane chapter-04 (the docx is lane S115); ncpssd.cn has no lane row at all.
The items never direct an equality check between the register's cited source and the SOURCES row's URL,
so a literal execution sweeps the register's quote against an unrelated document — producing systematic
false ABSENTs (fabrication verdicts against the wrong rows). The faithful locator is the register row's
own cited-source column → key sha256(url)[:24] → committed form. Form availability under register-cited
keys: 18/20 present (the two URL-orphans S077, S086 have none).

## 3. My own sample checks (independent sweeps)

### S086 — verdict: UNVERIFIABLE (no committed form)
```
$ python3 -c 'import hashlib;print(hashlib.sha256(b"https://www.ncpssd.cn/").hexdigest()[:24])'
76914d78c20094f677dea77d
$ ls corpus/captures/76914d78c20094f677dea77d.*      → No such file or directory
$ grep -c 76914d78c20094f677dea77d refetch.tsv       → 0
$ grep -lF '我们的网站目前仅对网站注册用户提供中文期刊论文全文下载服务' corpus/captures/*.txt → (none)
```
The register's payload-absent note for S086 ("cited source, companion URLs and local artifacts were
all checked") refers to shokuknow's deleted .qcache; the lane store holds nothing for this URL and the
round's egress scope forbids new fetches → the only honest class is UNVERIFIABLE, matching the header's
unreachable guidance. **Disagreement named:** the batch-A definition executed literally opens lane S086
(FEVER, key 1c15b611118dee97e4105fcf — form exists) and would report ABSENT after a 0-hit sweep
(I ran it: both Chinese quotes count=0 in the FEVER .txt). That verdict tests the wrong document and
would falsely brand the FEVER row; I reject it.

### S120 — verdict: PRESENT (register's payload-absent classification falsified for this row)
Register cited source = https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx →
key 3a8b45977cd111e45e3980a5; committed `.raw` (178,056 B, "Microsoft Word 2007+") + sidecar;
refetch.tsv rows 33/82 (S115, attempts 1-2, http 200, raw sha 16fc8c55…). Defined form = capture-text stdout:
```
$ python3 tools/capture-text.py corpus/captures/3a8b45977cd111e45e3980a5.raw > s120-form.txt  # exit 0, 48,936 B
# all three register quotes, exact grep -cF, one hit each:
offset=8996 line=531  SRにおける文献検索期間について明記する。
offset=9020 line=531  文献検索終了時点は、分析枠組みが決定された後から製造販売業者による分析提出までの一時点に決める。
offset=9428 line=564  ハンドサーチ等により未公表データを収集した場合は、そのことを上記のフローチャートに含める。
```
The checker could not fold a .docx (its sidecar is zip junk), so it logged payload-absent; the committed
bytes contain all three quotes verbatim — the register header's "CANDIDATE, not a verdict" warning is
exactly right here. **Disagreement named:** the batch-C definition executed literally opens lane S120
(Cochrane chapter-04, key c9d1e74c3ac8d9eb332c9770 — form exists) and would report ABSENT (I ran it:
both test quotes count=0 in the Cochrane .txt). Wrong document; the faithful PRESENT verdict stands.

## 4. Residual risk / recommendation (reported, not patched — frozen items)

- If any batch seat executed the locator literally, its ABSENT verdicts compare quotes against wrong
  documents. The L1 should treat register-id-located verdicts as invalid and re-derive each row's form
  from the register's cited-source key; rows with no committed form (the URL-orphans S077, S086)
  are UNVERIFIABLE, never ABSENT.
- Batch reports had not landed in w1/ at review time; this review judges the dispatched instructions
  plus my two independent sweeps. If the landed batch verdicts used the cited-source keys, my S120
  PRESENT should appear there and S086 should appear as UNVERIFIABLE.
- Corroboration: batch D (R57W1QuarD.md) independently found both defects — the register/lane id
  namespace mismatch (register S116 = lane S086; register S125 = lane S124) and form-choice artifacts
  falsifying payload-absent for register S116 (0/3 in pdftotext -layout, 3/3 in reading order) and
  register S125 (2/3 in capture-text stdout of the OLE .raw; "mixed").

No tools installed; no lane/fleet writes beyond this report; scratch deleted via trap.
VERDICT: attacked the quarantine batch A-D method (locator identity + honest-sweep conformance) — the
verdict schema, sweep and prose-row handling conform, but the id-based locator is broken (0/20 rows
resolve); my independent sweeps give S086=UNVERIFIABLE and S120=PRESENT (register payload-absent
falsified for S120), both differing from a literal execution — method defect survives as reported.
