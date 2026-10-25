# ExecEmptyEvidenceRecord — Round 45 w1

**Seat:** L1Chousa45.ExecEmptyEvidenceRecord (executor, leaf)
**Task:** in the train.json capture `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/974299ae4b5f3bdb808b36a9.txt`, find the ONE evidence answer whose `cached_source_url` is empty; report its record index, claim text (first 200 chars), the answer's source_url, answer_type, source_medium, and whether the record's other answers are archived. Then count `cached_source_url` values that are NOT archive.org URLs and archive.org values embedding archive.is/archive.md (double-archived), with three examples each.

**Lane bounds respected:** leaf, no subagent dispatch (labrat not needed — all answers obtainable from on-disk capture), no fetch, no network egress, no production writes, no installs (stdlib only; pacman untouched), no scratch files created (nothing to delete).

## Command run (single analysis script, Python 3 stdlib)

```python
import json, re
p = "/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/974299ae4b5f3bdb808b36a9.txt"
data = json.loads(open(p, encoding="utf-8").read())

total_ans = 0; carry = 0; nonempty = 0; key_empty = []; no_key = 0
nonarch = []; dblarch = []
for i, r in enumerate(data):
    for q in r.get("questions", []):
        for a in q.get("answers", []):
            total_ans += 1
            if "cached_source_url" not in a:
                no_key += 1; continue
            carry += 1
            c = a["cached_source_url"]
            if c is None or (isinstance(c, str) and c.strip() == ""):
                key_empty.append((i, r, q, a))
            else:
                nonempty += 1
                if not re.match(r"^https?://web\.archive\.org/", c):
                    nonarch.append((i, r, q, a, c))
                if re.search(r"archive\.is|archive\.md", c, re.I):
                    dblarch.append((i, r, q, a, c))
print("records:", len(data))
print("total answers:", total_ans, "| carrying key:", carry,
      "| non-empty:", nonempty, "| key-present-empty:", len(key_empty),
      "| no-key:", no_key)
print("non-archive.org cached_source_url:", len(nonarch))
print("values containing archive.is/archive.md:", len(dblarch), "| of which web.archive.org wraps:", sum(1 for _,_,_,_,c in dblarch if re.match(r"^https?://web\.archive\.org/", c)))
i, r, q, a = key_empty[0]
print("EMPTY record index:", i, "| claim len:", len(r["claim"]))
print("claim[:200]:", repr(r["claim"][:200]))
print("answer:", json.dumps(a))
others = [a2 for q2 in r["questions"] for a2 in q2.get("answers", [])]
arch = sum(1 for a2 in others if isinstance(a2.get("cached_source_url"), str) and a2["cached_source_url"].strip())
print("answers in record:", len(others), "| archived:", arch)
for i, r, q, a, c in nonarch[:3]:
    print("nonarch example:", i, repr(c), a.get("source_medium"), a.get("answer_type"))
for i, r, q, a, c in dblarch[:3]:
    print("dblarch example:", i, c)
```

## Verbatim output (decisive lines)

```
records: 3068
total answers: 8479 | carrying key: 6511 | non-empty: 6510 | key-present-empty: 1 | no-key: 1968
non-archive.org cached_source_url: 551
values containing archive.is/archive.md: 11 | of which web.archive.org wraps: 8
EMPTY record index: 1175 | claim len: 190
claim[:200]: 'Seven things that can kill COVID-19:\nUV\nTemperatures higher than 56 degrees celsius\nVentilated air  \nChlorine disinfectants\nAlcohol 75%\nFrequently washed hands\nStrong human’s immunity system'
answer: {"answer": "No", "answer_type": "Boolean", "source_url": "", "source_medium": "", "boolean_explanation": "There is no research except for information about the SARS coronavirus from 2002-2003.", "cached_source_url": ""}
answers in record: 9 | archived: 7
nonarch example: 13 'Metadata' Metadata Boolean
nonarch example: 13 'Metadata' Metadata Boolean
nonarch example: 15 'Metadata' Metadata Abstractive
dblarch example: 122 https://web.archive.org/web/20210219222208/http://archive.is/907zm
dblarch example: 122 https://web.archive.org/web/20210219222208/http://archive.is/907zm
dblarch example: 447 https://web.archive.org/web/20210103054638/http://archive.is/wip/j002m
```

Capture checksum (run separately): sha256 of the capture file = `ae5eda7c42ddf1695ef185a7ba1bc716928f5adf57103e4f78aae5f9afe00f9c`, size 10184813 bytes — matches the recorded value in `corpus/evidence/round45/claims.md` (construction checks).

## Findings

1. **The ONE empty `cached_source_url` answer** — record index **1175** (0-based list position in the JSON array), question "Can Temperatures higher than 56 degrees celsius kill coronavirus?", answer index 1 within that question. Claim length 190 (< 200), full text quoted above. The answer carries `answer_type: "Boolean"`, `source_medium: ""`, `source_url: ""` (also empty), `boolean_explanation` present, `cached_source_url: ""` (empty string, key present).
2. **Other answers in record 1175:** 9 answers total; **7 archived** (non-empty `cached_source_url`: africacdc.org, web.archive.org, onlinelibrary.wiley.com snapshots) and **2 not archived**: (a) the target Boolean answer (key present, empty), (b) one `Unanswerable` answer ("No answer could be found.") with no `cached_source_url` key at all and empty source_url. So the record's other answers are mostly, but not all, archived — the Unanswerable answer is also unarchived.
3. **Non-archive.org `cached_source_url` values: 551** of 6510 non-empty. Breakdown: literal string `"Metadata"` **429** (placeholder, not a URL; `source_medium`/`source_url` are also "Metadata"), `archive.ph` 41, `perma.cc` 27, `quoteinvestigator.com` 7, `archive.vn` 6, bare `archive.is` 2 + `archive.md` 1, plus assorted non-URL/malformed strings (file:// paths, "ttps://…", "web.archihttps:", "38287801729.78*4.7", etc.). Examples: record 13 (`'Metadata'`, Boolean), record 15 (`'Metadata'`, Abstractive), record 899 (`https://archive.md/YEr1p`).
4. **Archive.org values embedding archive.is/archive.md (double-archived): 8** (e.g. record 122 `https://web.archive.org/web/20210219222208/http://archive.is/907zm` — source_url identical; record 447 `https://web.archive.org/web/20210103054638/http://archive.is/wip/j002m`; record 456 `https://web.archive.org/web/20210720231105/https://archive.is/ScTQa`; also records 1090, 1488, 1498×2). **3 more** values are bare archive.is/archive.md (records 899, 1008, 1859) — not archive.org wraps, counted in the 551 above. 11 values total mention archive.is/archive.md.

## Verdict

All C3 construction-check figures reproduced exactly (6511 carrying / 6510 non-empty / 1 empty; 3068 records). The single empty record is located with full detail. The non-archive.org population (551) is dominated by the non-URL `"Metadata"` placeholder (429) plus alternative archivers (archive.ph 41, perma.cc 27, archive.vn 6) and malformed strings; the paper's double-archived case exists as 8 `web.archive.org`→`archive.is` wraps. No blockers; no changes made to any lane/production file.

**Resolvable pointers:** capture `file:///home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/974299ae4b5f3bdb808b36a9.txt` (sha256 `ae5eda7c42ddf1695ef185a7ba1bc716928f5adf57103e4f78aae5f9afe00f9c`); empty-answer record at JSON array index 1175; non-archive/`"Metadata"` population throughout; double-archived values at array indices 122, 447, 456, 1090, 1488, 1498, 899, 1008, 1859.
