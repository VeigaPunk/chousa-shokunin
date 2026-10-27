# R55CritCurrency — C2 currency/status attack

## Counterexample and evidence

The frozen claim is the by-document grey-literature field; this review attacks only the entry's defensible currency language, not a C2 predicate, target, counter, or control.

Staged currency entry `chinese-regulator-guideline-currency-r41.md`:
- Lines 24–31 explicitly say continued force is **not settled**; HTTP 412/WAF and the absence of a found withdrawal notice do not provide a status field.
- Lines 48–52 name the unknown as the NMPA policy-library item and replacement/withdrawal; explicitly prohibit claiming it current.
- Its S143 row is scoped to identity, issuer, issue date and legal hook, deliberately not current status (`SOURCES.append.md:68`). The staged entry cites S143 at line 2, for the English item's second paragraph.

Capture identification: SHA-256(URL) prefixes (command executed):
```
python3 -c 'import hashlib; print(hashlib.sha256(b"https://english.nmpa.gov.cn/2019-07/18/c_388252.htm").hexdigest()[:24]); print(hashlib.sha256(b"http://m.cnpharm.com/201906/18/c280684.html").hexdigest()[:24])'
d663d66e2d39f868d84b1781
27d4865f201e99c1fed9f79b
```

Status-word count command and observed results (S125 text is the captured UTF-8 `.txt`; S124 is the defined OLE form via `capture-text.py` on `.raw`):
```
python3 -c '...'
FILE 27d4865f201e99c1fed9f79b.raw chars 1673
COUNTS [('试行', 3), ('interim', 0), ('effective', 0), ('施行', 0), ('自…起施行', 0)]
FILE bdff491a75c6abeda1d9c01d.raw chars 13718
COUNTS [('试行', 1), ('interim', 0), ('effective', 0), ('施行', 0), ('自…起施行', 0)]
```

Caveat: the first capture inspected by that command was the S125 `.txt` file, not the S124 `.raw`; despite the printed filename suffix, it was read as the UTF-8 text sidecar. Do not treat that as a valid defined-form S124 status count. S124's required defined form is the specified `capture-text.py .../bdff491a75c6abeda1d9c01d.raw`; the output above found one `试行` in the executed form. These counts are search-term incidence, not legal status determinations. In S125 the 试行 instances are in title/headline/body label and its 2019 report says NMPA published the guideline (`.txt` lines 20, 77, 94). S124's extracted form contains the title `（试行）` and guideline text. Neither capture showed `interim`, `effective`, `施行`, or `自…起施行`.

S143 captured UTF-8 text is `d663d66e2d39f868d84b1781.txt`. It says “Guidelines … (Interim)” in title (lines 6, 139), and states the guideline “was issued on June 18, 2019” (line 157). It contains no status indication that it remains in force. The staged source row itself says the row is deliberately not scoped to whether it remains in force (`SOURCES.append.md:68`). Therefore S143 is evidence of promulgation/issuance and identity only, not currency. The Chinese S125 report likewise reports issuance, not continued effectiveness.

## Smallest safe entry text (for L1 integration)

Append under `#### Unknown` in the intended lane file `corpus/knowledge/grey-literature-and-chinese-search-record-r40.md`:

```markdown
- Whether 《上市药品临床安全性文献评价指导原则（试行）》 remains in force. S124's title labels it 试行; S125 reports its 2019 issuance; S126 (NMPA's English notice) says it was issued on June 18, 2019 and calls it “Interim”. Those are instrument identity/issuance evidence, not a current-status field or a finding of continued force. No current NMPA policy-library status, replacement, or withdrawal determination is established here; do not describe the guideline as current.
```

Proposed `recheck:` metadata line (offline-only; no fetch):

```text
recheck: 180d — using only the then-current on-disk capture cache, locate the NMPA policy-library record for 通告（2019年第27号） and any replacement/withdrawal notice; record the capture URL/key, retrieval date, exact status field and notice text. If the cache contains no such status-bearing capture, leave current status unknown (do not infer from continued hosting, the 试行/Interim label, or issuance date); no network fetch (ran 2026-10-27)
```

This command text deliberately requires an on-disk cache and preserves an unknown result if the evidence is absent; it does not claim a check was actually performed. The word `recheck:` should only be presented as a planned command/instruction, not as evidence of currency.

## Impacted axes and correction

- **Depth:** keep the nuance that issuance and current force are separate propositions, and preserve the primary regulator document/capture as evidence only for what it states.
- **Operability:** the recheck is repeatable from captures without network access and reports absence rather than substituting issuance evidence.
- **Calibration:** avoid elevating “Interim”/试行 nomenclature or an issuance notice to current-status proof.

Smallest correction: add the explicitly qualified unknown bullet and cache-only recheck instruction above; do not patch any frozen claim or infer currentness from S143.

VERDICT: attacked the C2 currency implication; S124/S125/S143 evidence issuance and interim designation, not continued force, so status must remain unknown pending a status-bearing capture.
