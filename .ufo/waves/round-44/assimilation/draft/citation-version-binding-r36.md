# Binding a citation to a prior state, and where that binding stops

source: S079 — https://www.rfc-editor.org/rfc/rfc7089.txt — section 2.1.1, byte offset 14896 of the committed capture — RFC 7089, February 2013, Informational
verified-at: 2026-10-24
recheck: 365d
ground: the lane's byte-span check answers whether these bytes match. It does not date a prior state. This entry is that missing half, opened from a committed capture. The filename is the package's label, not a lane round number. Staged S082 (the GB/T record) is not cited.

#### Observation

- RFC 7089 says the presence of a Memento-Datetime header "constitutes a promise that the resource state reflected in the response will no longer change" (S079, capture byte offset 14896).
- The same document says an archived entity-body "may very well not be byte-to-byte the same" as what the origin previously returned (S079, the same capture).
- It says the veracity of archives is beyond the scope of the document (S079, the same capture).

#### Inference

- A Memento-Datetime is a date of a prior state, not a byte hash. The lane's span check against an archived capture checks the capture. It does not check the origin's past output.
- The promise is about stability, not authenticity. The RFC says so by putting veracity out of scope. A CLEAN span result remains mode-dependent, not a proof that the quoted text was on the origin on that date.

#### Unknown

- Staged S082, the SAMR record for GB/T 7714-2025, is not adopted. Round 43 classed that row not-carried. This round did not fetch. Flip: a text capture of that record contains the issued and effective dates as a contiguous span.
- No live TimeGate was opened. The fetch-scope ruling is open.

#### Gate

Located quote (7 words), access 2026-10-24, no fetch: "constitutes a promise that the resource state"
Capture `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/d0c4a09a9de32cb91d5e3797.txt` is sha256 of the URL, first 24 hex digits. File sha256 `c3c7b7f2c495dce0fad758dac34dcc1eef3623d13c9ef346e19b30dbbbe801dc`. Capture mtime 2026-10-23 20:33 -0300, before this round's launch.
The staged citation id was S081. The lane id is S079 because the URL is the evidence and S079 is the next free lane id. Staged S079 is the PRISMA-S DOI and is not this row. Lane S077 stays the pdftotext manual. Staged S077 is not a row-start id in the append file.
