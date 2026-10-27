# Round 57 L1 sidecar audits (ChousaR57a2, 2026-10-27)

Supplementary, non-frozen audits run by the L1 after WAVE-DONE w2 to close the w1/w2 hard
findings honestly. None amend the frozen counters. Each audit was re-run by the L1; outputs pasted.

## 1. Case-insensitive stray-id scan of the C3 entry (R57W1CritC3Stray case 3)

The frozen STRAY_IDS leg is case-sensitive (`\bS\d{3,}\b`); a lowercase `s128` would false-PASS.
Supplementary scan of the committed entry, run by the L1:

    $ grep -ioE '\bs[0-9]{3,}\b' corpus/knowledge/normative-reference-chain-china-r57.md | sort | uniq -c
          4 S118
         10 S127
          5 S131
          4 S132
          3 S133

Only bound/allowed ids appear in any case. The blind spot is not exercised.

## 2. C3 sidecar faithfulness (R57W2CritC3Forge A1 — ".txt is never tied to .raw")

The frozen counter never checks the `.txt` against its `.raw`. Re-deriving every C3-bound sidecar
from its `.raw` via the frozen recipe (ran by the L1, `tools/capture-fetch.py:recipe_txt`):

    S127 b27ffd2f0161104c6a28c9f5 faithful=True digest_ok=True  (x2 rows)
    S118 16fe8487aa97b98576a0dbac faithful=True digest_ok=True  (x2 rows)
    S131 788d2e2f0191d7326b6ca03b faithful=True digest_ok=True  (x2 rows)
    S132 a476f4128186c7976671ab54 faithful=True digest_ok=True  (x2 rows)
    S133 6f545e6c16b6b568ea3f591b faithful=True digest_ok=True  (x2 rows)
    TXT_SIDECAR_FAITHFUL=10/10

The forge hole is real, but the committed sidecars the C3 receipt rests on are all faithful
re-derivations of their committed `.raw` bytes.

## 3. S096 quarantine hand-check (the unassigned register row)

Register slice row S096 (`payload-absent`) binds by URL to the lane-held capture
`corpus/captures/6dc68fd6b32ce9c8dfcebce8.{raw,txt}` (lane S101's URL, an OLE `.doc`; the defined
form is `tools/capture-text.py` stdout). L1 run:

    `1．2．1 根据GB3469规定，以单字母方式标识以下各种参考文献类型` — verbatim True
    `b. 文献题名` — verbatim True
    `本规范推荐采用GB/T 7714中规定的顺序编码制格式著录，也可采用GB/T 7714中规定的作者-出版年制` — substance present with a half-width/full-width comma fold (the form prints `著录,也可采用`)

Verdict: PRESENT (two verbatim, one comma-fold substance). Quarantine coverage is 24/24; zero
register rows support a fabrication verdict. Fold-class note recorded in the round-57 lesson.

## 4. C3 fetch-record provenance of the committed state (`R57W2CritC3Forge` A1)

The w2 forge proved the frozen counter accepts a fabricated `refetch.tsv` success row plus
byte-replayed captures under a forged (id,url). Auditing the COMMITTED state for the same class
(5 bound (id,url) pairs; L1 run):

    S127 b27ffd2f0161104c6a28c9f5 record=OK key_ok=True raw_binds_record=True
    S118 16fe8487aa97b98576a0dbac record=OK key_ok=True raw_binds_record=True
    S131 788d2e2f0191d7326b6ca03b record=OK key_ok=True raw_binds_record=True
    S132 a476f4128186c7976671ab54 record=OK key_ok=True raw_binds_record=True
    S133 6f545e6c16b6b568ea3f591b record=OK key_ok=True raw_binds_record=True
    duplicate_first_urls: []   PROVENANCE_CONSISTENT=YES (5 bound (id,url) pairs)

Every binding rests on a genuine fetch record whose key and digest match the stored bytes, and a
unique registry id. The forge hole is not exercised by the committed state. Smallest safe
correction for a future re-freeze (reported, not applied): bind each manifest (id,url) to a
specific refetch row identity (attempt+utc) and require `.txt == recipe(.raw)` in the counter.

## 5. Round-45 spans.tsv integrity (the restored seat-write file)

    $ git hash-object corpus/evidence/round45/spans.tsv
    a21a0365bce096f3678d4becdba8028b37a2a374
    $ git rev-parse master:corpus/evidence/round45/spans.tsv
    a21a0365bce096f3678d4becdba8028b37a2a374

Byte-identical to the branch; the seat-write incident is closed.

## Provenance note

An unidentified file `corpus/evidence/round57/attempt3-sidecar-audits.md` (authorship string
"ChousaR57a3", a identity this lane never dispatched) appeared in the lane mid-wave-2. Its five
audit topics were re-run by the L1 and are recorded here under L1 authorship; the stray file was
deleted. Incident recorded in `corpus/lessons/round-57.md` Mistakes.
