# W2 hand-check — chousa S125 (`payload-absent` → **present**, verdict refuted)

Row: `chousa | round6 | S125 | payload-absent | http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc`
(absent-defect-register.md:56). Lane SOURCES row: the same URL is `S130` in
`lanes/chousa/round6/SOURCES-PROPOSED.md:25,44-59` — ID-REMAP.md maps the staged
id to registry S125 (cf. staged-map.tsv `S130 … S125`); Gate — S130's note already
predicted a mechanical checker would misread these quotes as ABSENT.

## Captures examined (local only, no fetch)

- `.ufo/waves/corpus-expansion-1/.qcache/bdff491a75c6abeda1d9c01d.raw` —
  243,929 bytes, sha256 `ac0fad62ed9a11fa3bd135e78427329be30899df90946de7ac45e153974e6c44`.
  `file`: Composite Document File V2 (OLE, magic `d0cf11e0a1b11ae1`), codepage 1200
  (UTF-16LE), locale 2052, 32 pages / 2,118 words, NMPA guideline doc.
- `…/bdff491a75c6abeda1d9c01d.txt` — 323,728 bytes, sha256
  `55b4085c442fce1abf3ebef737344eb32fecf3e2b12fc781ad7a1e802eeac4e5`. Head bytes
  `efbfbd efbfbd 11e0 …`: the raw OLE decoded as UTF-8 with U+FFFD replacement
  chars. This mojibake copy is why the census checker matched nothing — it searched
  a bytes-decode, never the document text. Prior round-42 verdict for the same
  capture: `unverifiable` (quarantine-verdicts.tsv:21) for exactly this reason.

## Commands run and observed output (python3, in-memory)

- `raw.find(q.encode('utf-16-le'))` for each register quote:

| quote | utf-16le byte offset | utf-8 | result |
|---|---|---|---|
| Q1 文献检索策略：检索途径、检索数据库、检索时限及检索式。应当说明是否有检索限制…关键问题。 | **114890** | -1 | verbatim hit, context `…。\r2.` + quote + `\r3.文献筛选：…` |
| Q2 检索策略包括检索的数据库、检索范围（如主题等）、检索词、检索式（即检索词组合方式）和时间范围等，应当根据不同的研究目的制定。 | **107050** | -1 | verbatim hit, context `…化方案。` + quote + `\r3.全` |
| Q3 查找时应当注意收集未公开发表的文献，即灰色文献，如会议论文、未发表的学位论文、产业报告、咨询报告等。 | -1 | -1 | not byte-verbatim |
| Q4 (title) 上市药品临床安全性文献评价指导原则（试行） | -1 | -1 | not byte-verbatim |

- Gate's own re-check (`decode('utf-16-le','ignore')`, keep CJK+，。；：、（）《》):
  filtered stream = 25,684 chars; probe `是否检索灰色文献等关键问题` → **True**;
  **all four quotes → True** in the filtered document text.
- Fragment dump, utf-16-le decode of the raw regions:
  - @105480: `上市药品临床安全性文献评价指导原则\r（试行）\r\r一、概述\r国` —
    the title is present but a `0x0d00` CR sits inside the parenthetical, so the
    contiguous string fails while the rendered title matches.
  - @107516: `查找时应当注意收集未公开发表的文献，即“灰色文献”，如会议论文、
    未发表的学位论文、产业报告、咨询报告等。` — the document writes
    `即“灰色文献”，如` with U+201C/U+201D quotation marks the register's quote
    elides; every other fragment hits contiguously (offsets 107516–107628).

## Verdict

**present** — the `payload-absent` fabrication class is refuted by local byte
evidence. Q1/Q2 match verbatim in the WordDocument stream; Q3/Q4 differ only by
typographic artifacts (document adds “…” around 灰色文献; a CR inside the title's
parenthetical) and are present modulo those marks. Strict-verbatim reading of
Q3/Q4 alone would be "absent-as-written" by one punctuation mark / one line break
each — transcription noise, not fabrication, and never `unverifiable`: the local
capture resolves all four quotes.

## Counterexample for the C1/quarantine slice

The register's `payload-absent` row is a false positive of the checker: on OLE
binary sources it conflates "absent in a UTF-8 bytes-decode" with "absent in the
document". S125's lane row even published the working re-check command. Impacted
axis: **calibration** (fabrication classification on binary office captures);
smallest safe correction: reclassify S125 as present (OLE-decode required), and
route every `.doc/.docx/.xls` capture in the slice through an extraction path
before a `payload-absent` verdict stands — siblings S095/S096/S120 share this
file type and prior `unverifiable` history.

No scratch files created; no production writes; tooling directive: no installs
needed (python3 stdlib only).
