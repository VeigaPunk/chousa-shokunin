# W2ScribeGate — round 44, wave 2

Seat: chousa leaf scribe. Draft only. Nothing in this file is appended to `corpus/SOURCES.md`, `corpus/knowledge/`, or `corpus/lessons/`. No fetch. No production edit. No census run. No `jj`. No git commit.

Axes walked: operability (a row the census script can accept, and a reject whose flip is a checkable span), calibration (lane id by URL, not by subtracting 2; round-43 id S082 is a different document), depth (the frozen quote is in the RFC capture; the staged GB/T sentence is not a raw span of its capture).

## Gate

Draft for the L1. Not landed.

### Admitted

`corpus/knowledge/citation-version-binding-r36.md`, citing lane **S079**. The filename is the package's label, not a lane round number. The source is RFC 7089, opened from the committed capture, not fetched. Freshness is unchanged: the capture's mtime is 2026-10-23 20:33:05 -0300, before this round.

Located quote (7 words), access 2026-10-24: "constitutes a promise that the resource state"

URL: `https://www.rfc-editor.org/rfc/rfc7089.txt`

Capture: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/d0c4a09a9de32cb91d5e3797.txt`

That name is sha256 of the URL, first 24 hex digits (`d0c4a09a9de32cb91d5e3797`). File sha256 `c3c7b7f2c495dce0fad758dac34dcc1eef3623d13c9ef346e19b30dbbbe801dc`. 107130 bytes and 107130 Unicode characters, so byte offset and character offset of the quote are the same: **14896**. The quote sits in section 2.1.1 ("Accept-Datetime and Memento-Datetime"), on one line. It is not a Client Challenge page. The capture's own date line is `December 2013`. Its title line is `HTTP Framework for Time-Based Access to Resource States -- Memento`. `Request for Comments: 7089` is present.

Also raw substrings of the same capture, not the located quote: `not be byte-to-byte` (character 27992) and `The veracity of archives` (character 89208). The longer sentence that continues the located quote is line-wrapped, so it is not claimed here as one raw span.

Staged citation id was **S081**. Lane id is S079 because the URL is the evidence and S079 is the next free lane id (`S078` is the last registry row; `S079` is not a lane row). Staged S079 is the PRISMA-S DOI and is not this row. Subtracting 2 from every staged id would also print S079 for this URL, and would point staged S079 at lane S077. That coincidence is not the rule. Lane S077 stays the pdftotext manual. The append file has no row-start `S077`.

The entry's source line is `source: S079 —`. It does not contain `source: S081 —` or `source: S082 —`.

Registry change, drafted here, not written:

```
| S079 | RFC 7089, HTTP Framework for Time-Based Access to Resource States -- Memento — https://www.rfc-editor.org/rfc/rfc7089.txt | spec | A | the Memento-Datetime promise in RFC 7089 section 2.1.1; not archive veracity | section 2.1.1 of the committed capture, byte offset 14896 | A Memento-Datetime header promises that the resource state will no longer change; this cell is a paraphrase, and the located quote is the Gate's | mined | 2026-10-24 | 365d | corpus/knowledge/citation-version-binding-r36.md |
```

Eleven cells. No pipe inside a cell. Status `mined`. Recheck is the bare interval `365d`. Staged S081's recheck cell was `365d — curl ...`; that prose is this Gate, not a registry cell. `sources-census.sh` treats a recheck that is not `Nd`, an ISO date, or a symbolic cadence as E09. This seat did not run the census, so E09 is a reading of the script, not a receipt. used-by is only the admitted entry. No other lane row's status, recheck, or used-by changes.

Do not copy the staged phrases `February 2013` or `HTTP Extension`. Neither string is in the capture.

### Rejected

Staged **S082**, the SAMR detail record for GB/T 7714-2025.

URL: `https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F`

Capture: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/adf6ba934e813b2c326fa150.txt` (6626 bytes; Python text mode 3591 characters, the same count round 42 printed; 4468 Unicode characters if the 877 CR bytes are kept). Not a Client Challenge page. Not fetched this round.

Reason it stays refused this round:

- The quote the register actually checked is not in that capture. Register id for this URL is **S080**, not S082 (`absent-defect-register.md`: `标准号：GB/T 7714-2025 发布日期：2025-12-02 实施日期：2026-07-01`, 50 characters). Raw find: absent. Whitespace-collapsed find: absent. Longest contiguous run of that quote: 15/50 raw (`GB/T 7714-2025 `), 19/50 after whitespace collapse (`GB/T 7714-2025 发布日期`). Round 42's verdict for register S080 was that 19/50 run, on this same capture name (`examine.txt`: `S080 … adf6ba934e813b2c326fa150.txt`). The current append file calls the same URL S082. The document follows the URL.
- Round 43's id S082 is a different document: the NII support page, capture `09fc63de41f293d43d631c46.txt`, not-carried 18/43. That class does not refuse this URL and does not admit it. An assimilation draft that says "Round 43 classed that row not-carried" is that id slip. This Gate does not use it.
- The staged English teaches sentence is not in the capture (`wholly replacing` absent, `non-equivalent` absent).
- This round appends only the row the admitted entry cites. That entry cites lane S079 and does not cite staged S082. Staged used-by also names `corpus/knowledge/source-type-taxonomy-r36.md`, which is not admitted.
- The staged recheck cell is `180d — re-open the SAMR detail record...`. Copied as written, that cell is not a bare interval.

Two date lines are already raw spans in the text-mode capture: `发布 于 2025-12-02` (character 1029) and `实施 于 2026-07-01` (character 1048). They do not flip the refusal. A flip that only asks for "the dates" is already true and is not the defect.

Flip: a located quote of at most 25 words — the register's 50-character span, or a replacement written to the page — is a raw contiguous substring of `adf6ba934e813b2c326fa150.txt`, recheck is a bare interval, used-by names only an entry that cites this URL, and the lane id is the next free id by that URL, never staged S082 and never S082 minus 2. Until that quote is raw-contiguous, the row stays refused.

## Conflicts, not resolved here

1. Staged S081 and `.ufo/waves/round-44/assimilation/draft/citation-version-binding-r36.md` say `February 2013`. The capture says `December 2013` (character 503). `February 2013` is absent.
2. The same draft's flip ("a text capture of that record contains the issued and effective dates as a contiguous span") is already met by the two date lines above, and is not met by the 50-character register quote. This Gate uses the register quote.
3. Register S080 and append S082 are one URL. Register S082 and append S084 are the NII page. Do not subtract 2 to reconcile them.

## What this seat ran

Working directory `/home/vgpnk/Projects/shokunin/chousa-shokunin`. No network.

`printf '%s\n' 'constitutes a promise that the resource state' | wc -w`

```
7
```

`python3 corpus/evidence/round44/c3-count.py` (entry not yet in the lane; this is the before state, not a score of the draft):

```
ENTRY_CITES=0/1
QUOTE_LOCATED=0/1
URL_MATCH=0/1
C3=FAIL entry-missing
EXIT:1
```

Confirmation script, stdout relied on above:

```
RFC_SHA24 d0c4a09a9de32cb91d5e3797
RFC_FILE_SHA256 c3c7b7f2c495dce0fad758dac34dcc1eef3623d13c9ef346e19b30dbbbe801dc
RFC_BYTES 107130 RFC_CHARS 107130
QUOTE_CHAR 14896 QUOTE_BYTE 14896
QUOTE_WORDS 7
WINDOW 'constitutes a promise that the resource state\n   reflected in the response will no longer '
NEEDLE December 2013 503
NEEDLE February 2013 -1
NEEDLE HTTP Framework 522
NEEDLE HTTP Extension -1
NEEDLE Request for Comments: 7089 79
NEEDLE Client Challenge -1
NEEDLE not be byte-to-byte 27992
NEEDLE The veracity of archives 89208
RFC_MTIME 2026-10-23 20:33:05 -0300
QUOTE50_CHARS 50
QUOTE50_RAW -1
QUOTE50_COLLAPSED -1
SPAN_ISSUE 1029
SPAN_EFFECTIVE 1048
EN_WHOLLY -1
EN_NONEQ -1
SAMR_BYTES 6626 SAMR_CHARS 3591
SAMR_MTIME 2026-10-23 20:33:09 -0300
LCR_RAW 15 'GB/T 7714-2025 '
LCR_COLLAPSED 19 'GB/T 7714-2025 发布日期'
APPEND_ROW_S077 False
APPEND_ROW_S079 True
APPEND_ROW_S081 True
APPEND_ROW_S082 True
LANE_ROW_S079 False
LANE_ROW_S078 True
LANE_ENTRY_EXISTS False
```

`SPAN_ISSUE` and `SPAN_EFFECTIVE` are Python text-mode character offsets, not byte offsets.

## Not run

`sources-census.sh` was not run, so the drafted S079 row has no census receipt. `c3-count.py` was not run against an appended entry; the missing-entry result above is the current tree. No URL was fetched. The two date spans do not make staged S082 admitted.

Report: .ufo/waves/round-44/w2/W2ScribeGate.md
