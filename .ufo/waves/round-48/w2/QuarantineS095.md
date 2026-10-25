# W2 hand-check — chousa register row S095 (quarantine slice)

Lane: `L1Chousa48.QuarantineS095`. Leaf; no subagents, no live fetch. Local captures only.

## Row identity

- Frozen slice: `.ufo/waves/round-48/assimilation/quarantine-slice:9` → ` S095   \`payload-absent\` ` (24-row file).
- Register row: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md:45` — `chousa | round2 | S095 | payload-absent | https://www.zcmu.edu.cn/__local/2/33/FC/FFA702D0F9381C8224BD74CB435_0E777725_C3A00.doc?e=.doc` with three quotes and reason "cited source, companion URLs and local artifacts were all checked; the quote is in none of them".
- Id-space check: census `quote-lint-full-v5.json` findings[109–111] bind id `S095`/round2 to this URL (`binding: "id"`). In `lanes/chousa/round2/SOURCES-PROPOSED.md` the same row is `#### Gate — S100` (line 96) and table row `| S100 |` (line 32); census ids run 5 below gate ids this round (S088↔S093 … S099↔S104). `lanes/chousa/ID-REMAP.md` and `merge/chousa/SOURCES.append.md:25` confirm the zcmu row is this document (itself staged S100). `chousa-shokunin/corpus/SOURCES.md:105` has a different, later S095 (round-47 spot-check) — not this row. Prior adjudication: `corpus/evidence/round42/quarantine-verdicts.tsv:10` called this row **unverifiable** ("OLE binary… never rendered to text… never a fabrication").

## Lane SOURCES row (proposed, gate S100)

`lanes/chousa/round2/SOURCES-PROPOSED.md:98-103`:
- `Opened: 2026-10-23 (HTTP 200, 801,280 bytes; the .doc was converted to text locally — LibreOffice is present but the document decoded cleanly as UTF-16…)`
- Quotes: opening `中国知网他引频次的查询需要使用中国引文数据库`; 关于自引的说明 `…如果引文出现了任一合作者，那么这条引文将被认定为自引`; procedure `成功登录中国引文数据库后，可按题名作者单位等方式查询需要检索的文献`.
- Search log `round2/SEARCH-LOG.md:51`: `curl + local UTF-16 decode | 200, 801 KB → 739,220 bytes`.

## On-disk capture (local byte evidence)

`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/b539a80218080da56a75b624.raw`
- 801,280 bytes; `file`: Composite Document File V2, magic `d0cf11e0` (observed `xxd` head: `d0cf 11e0 a1b1 1ae1`), Code page 936, 5 pages.
- sha256 `46d1866ce9afd51682e7e77cdf62612876da22c9bdbc9e8e299090128cb378f6`; md5 `233fcffa702d0f9381c8224bd74cb435` (filename token embedded in the URL — capture is the cited document).
- Sidecar `.txt` (1,406,840 B, sha256 `ce30e735…360046`): byte-identical to `raw.decode('utf-8','replace').encode('utf-8')` — a **lossy** re-encode of OLE binary, not the claimed clean UTF-16 decode; the CJK payload is destroyed (`efbfbd` throughout header). This is why the census found nothing: its only searchable artifact was garbage.

## Measurements (commands run, all local)

1. `python3` raw-bytes scan, UTF-16LE (`raw.find(q.encode('utf-16-le'))`):
   - q2 staged: **offset 2846**, 47ch contiguous (served adds `。`, offset 2846–2942).
   - q1/q3 staged: -1. Served forms: `中国知网他引频次的查询需要使用《中国引文数据库》。` at 2592–2642; `成功登录《中国引文数据库》后，可按“题名”、“作者”、“单位”等方式查询需要检索的文献` at 3174–3260.
   - Longest UTF-16LE contiguous runs of staged text: q1 15/22ch, q2 47/47ch, q3 12/33ch.
2. Approved extraction: `soffice --headless --convert-to txt:Text s095.doc` → 870-char text, sha256 `bbaf2158…209ac`. Document is 5 short pages of CNKI 他引频次 instructions; body shown in scratch `s095.txt` (deleted after run).
3. `python3` search of rendered text:
   - q1 `中国知网他引频次的查询需要使用中国引文数据库` → -1 (served: `…《中国引文数据库》。` — 《》 stripped, longest run 15/22).
   - q2 `关于自引的说明：对于合作发文的参考文献中，如果引文出现了任一合作者，那么这条引文将被认定为自引` → **char-offset 143, verbatim PRESENT** (任 = U+4E00 intact; served sentence ends `。` after the staged span).
   - q3 `成功登录中国引文数据库后，可按题名作者单位等方式查询需要检索的文献` → -1 (served: `《中国引文数据库》…“题名”、“作者”、“单位”等…` — brackets/quotes/、 stripped, longest run 12/33).

## Verdict

**Row: absent-as-written — and the `payload-absent` (fabrication-candidate) tag is falsified.** Per-quote: q2 **present** verbatim; q1, q3 **absent-as-written** (punctuation-stripped renderings of sentences that are on the page), not fabricated, not unverifiable.

Reason: the source was fetched cleanly and is on disk (OLE .doc, 801,280 B). An approved rendering contains all three cited sentences; one quote is verbatim, two drop the document's 《》/“”/、 punctuation. The `payload-absent` verdict was produced against a `.txt` sidecar that is a lossy UTF-8-replace re-encode of the binary — absence there is not evidence about the document, exactly as the round-42 adjudication warned. This is a quote-fidelity defect (normalize or re-quote to the served text), not a fabrication.

## C1 bearing

None. Frozen R48-C1 (`claims.md` @ 4bbd2348) is a plumbing predicate on `c1-count.py`/`mutation-check.py` legs (REFINEMENT_CASES 5/5, CORRECT_BULLETS_PASS ≥11/12, LEGACY_R47, MUTANTS_KILLED 5/5); the quarantine hand-check feeds no leg of that counter. This report falsifies the register's S095 `payload-absent` verdict only.

## Installations

None. Used system `soffice` (already present) + `python3`. Scratch `/tmp/chousa-r48-QuarantineS095` deleted before finish.
