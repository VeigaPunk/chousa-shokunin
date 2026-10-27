# Round 57 attempt-3 L1 sidecar audits (ChousaR57a3, 2026-10-27)

Supplementary, non-frozen audits run by the L1 at lane tip 3010e75 to close the
w1/w2 hard findings honestly. None of these amend the frozen counters; they are
receipts that the frozen counters' known blind spots are not exercised by the
committed bytes.

## 1. Case-insensitive stray-id scan of the C3 entry (R57W1CritC3Stray case (3))

The frozen STRAY_IDS leg uses case-sensitive `\bS\d{3,}\b`; a lowercase `s128`
would be a false PASS. Supplementary scan of the committed entry:

    $ grep -ioE '\bs[0-9]{3,}\b' corpus/knowledge/normative-reference-chain-china-r57.md | sort | uniq -c
          4 S118
         10 S127
          5 S131
          4 S132
          3 S133

Only bound/allowed ids appear, in any case. The frozen leg's blind spot is not
exercised: no lowercase or unbound id token exists in the committed entry.
(Uppercase scan for comparison prints the same five ids.)

## 2. C3 sidecar faithfulness (R57W1ExecInference F4)

The frozen counter never checks the `.txt` sidecar against its `.raw`; a doctored
`.txt` would pass. Re-deriving every C3-bound sidecar from its `.raw` via the
frozen recipe (`tools/capture-fetch.py:recipe_txt`, same as `c2-count.recipe_txt`):

    S127  b27ffd2f0161104c6a28c9f5 txt_sidecar=FAITHFUL   (×2 rows)
    S118  16fe8487aa97b98576a0dbac txt_sidecar=FAITHFUL   (×2 rows)
    S131  788d2e2f0191d7326b6ca03b txt_sidecar=FAITHFUL   (×2 rows)
    S132  a476f4128186c7976671ab54 txt_sidecar=FAITHFUL   (×2 rows)
    S133  6f545e6c16b6b568ea3f591b txt_sidecar=FAITHFUL   (×2 rows)
    TXT_SIDECAR_FAITHFUL=10/10

And the manifest pins hold against the committed sidecars
(`capture_sha256` in `corpus/evidence/round57/c3/spans.tsv` is the sidecar digest):

    CAPTURE_SHA256_VS_TXT=10/10

The forge hole is real (58/61 sidecars are doctorable in principle, only the four
OLE/zip captures self-verify) but the committed sidecars the C3 receipt rests on
are all faithful re-derivations of their committed `.raw` bytes.

## 3. S096 quarantine hand-check (R57W1SentScope S4 — the unassigned row)

Register slice row S096 (`payload-absent`) binds by URL to the lane-held capture
`corpus/captures/6dc68fd6b32ce9c8dfcebce8.{raw,txt}` (lane S101's URL). Searching
the UTF-16LE text of the `.doc`:

    `1．2．1 根据GB3469规定，以单字母方式标识以下各种参考文献类型：` — verbatim hit
    `本规范推荐采用GB/T 7714中规定的顺序编码制格式著录，也可采用GB/T 7714中规定的作者-出版年制` — substance hit
    `b. 文献题名；c. 文献类型及载体类型标志；d. 其他责任者…；e. 版本(初版省略)；f. 出版项(出版地…` — nine-element list hit

Verdict: PRESENT. Quarantine coverage is now 24/24; zero register rows support a
fabrication verdict. Full write-up: `corpus/lessons/round-57.md` Attempt-3 addenda.

## 4. C3 fetch-record provenance, committed state (`R57W2CritC3Forge.md` A1)

The w2 forge proved the frozen counter accepts a fabricated `refetch.tsv` success row plus
byte-replayed captures under a forged (id,url) — the record is checked only for self-consistency.
Audited the COMMITTED state for the same consistency class (5 bound (id,url) pairs):

    S127 b27ffd2f0161104c6a28c9f5 pin=OK record=OK registry_unique=OK
    S118 16fe8487aa97b98576a0dbac pin=OK record=OK registry_unique=OK
    S131 788d2e2f0191d7326b6ca03b pin=OK record=OK registry_unique=OK
    S132 a476f4128186c7976671ab54 pin=OK record=OK registry_unique=OK
    S133 6f545e6c16b6b568ea3f591b pin=OK record=OK registry_unique=OK
    PROVENANCE_CONSISTENT= YES (5 bound (id,url) pairs)

Every binding rests on a genuine fetch record whose digests and key match the stored bytes, and a
unique registry id. The forge hole is not exercised by the committed state; the receipt is genuine.
Smallest safe correction (future re-freeze): bind each manifest (id,url) to a SPECIFIC refetch row
identity (attempt+utc) and require `.txt == recipe(.raw)`, so a replayed or fabricated record cannot
satisfy the leg.

## 5. Round-45 spans.tsv integrity (R57W1SentScope S6 — closure)

    $ git hash-object corpus/evidence/round45/spans.tsv
    a21a0365bce096f3678d4becdba8028b37a2a374
    $ git rev-parse 6656f07:corpus/evidence/round45/spans.tsv
    a21a0365bce096f3678d4becdba8028b37a2a374
    $ grep -c a3ff65e0db9c corpus/evidence/round45/spans.tsv → 2
    $ grep -c d37b64ed18a8 corpus/evidence/round45/spans.tsv → 0
    $ git diff master -- corpus/evidence/round45/spans.tsv | wc -l → 0

Worktree == HEAD == round base; the laundered drift digest never landed in a commit.
