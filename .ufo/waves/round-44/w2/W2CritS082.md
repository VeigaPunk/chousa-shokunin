# W2CritS082 — staged S082 stays refused

Axes: operability (the refusal is a check a later seat can re-run), calibration (the token `S082` names two documents; the already-true date span is not the flip), depth (the page is the right page and still does not carry the staged quote).

No fetch. No production edit. Lane registry was not appended.

## Which row

Staged S082 is the append-file row, not the round-43 table row that happens to print `S082`.

`/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md` line 10, id cell `S082`, URL `https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F` (GB/T 7714-2025, SAMR detail record). `lanes/chousa/ID-REMAP.md` maps round1 `S080` to staged `S082`, and round1 `S082` to staged `S084`. The register, the round-42 verdict, and `corpus/evidence/round43/absent-split.tsv` still use the pre-remap ids.

| token | document | capture | class |
|---|---|---|---|
| staged S082 = register S080 | SAMR GB/T 7714 detail | `adf6ba934e813b2c326fa150.txt` | not-carried, 19/50, 0.380000 |
| register S082 = staged S084 | NII CiNii manual | `09fc63de41f293d43d631c46.txt` | not-carried, 18/43, 0.418605 |

Applying `absent-split.tsv`'s `S082` line to the SAMR page is the arithmetic error this wave forbids for S077. The SAMR page's own class is the `S080` line. Both rows stay refused. They do not share a flip.

Lane `corpus/SOURCES.md` ends at S078 (`LANE_LAST S078`, `LANE_S082_ROW False`, `LANE_S079_ROW False`). Staged S082 is not a lane id.

## Why it stays refused this round

The staged quote is not in the capture of the cited URL. Adopting the row as written would record a sentence the page does not state as written.

Register quote, also the line the round-42 table refused:

`标准号：GB/T 7714-2025 发布日期：2025-12-02 实施日期：2026-07-01`

Local recompute, no network, same NFKC-plus-whitespace-collapse rule as `tools/absent-split.py`, against `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/adf6ba934e813b2c326fa150.txt`:

```
SAMR_KEY adf6ba934e813b2c326fa150
SAMR_BYTES 6626
SAMR_SHA256 4e46154f4a841d17d858eafb5c0099257030f301daadcaa30c37f2e668fb7138
raw_chars 3591
QUOTE_FOLDED_LEN 50
RUN 19
RATIO 0.380000
BOUND not-carried
STRICT_SUBSTRING False
EXACT_SUBSTRING False
RUN_SPAN 'GB/T 7714-2025 发布日期'
```

`raw_chars 3591` is `Path.read_text` (universal newlines). That matches the round-42 reason's "3591-char capture". A byte decode that keeps CR counted 4468 characters; the verdict's 3591 is the text-mode length, not a different file.

Eleven-fold examine, importing `tools/quarantine-check.py` and reading the register plus the cache (the campaign checker was not run):

```
ID S080
URL https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F
KIND page+text
CAPTURE adf6ba934e813b2c326fa150.txt
Q 1 FOLD None STRICT False OFFSET -1 QLEN 50
QTEXT 标准号：GB/T 7714-2025 发布日期：2025-12-02 实施日期：2026-07-01
```

`FOLD None` means none of the eleven folds sees the quote. Strict fold is false. Round-42 `examine.txt` already had `S080 1 absent` on this capture. Round-42 `quarantine-verdicts.tsv` verdict is `absent`, flip column as quoted below. Round-43 `absent-split.tsv` line 1 is `S080 not-carried 19 50 0.380000 1`. This seat's recompute matches that line. The bound is 1/2 (`corpus/evidence/round43/claims.md`, rule R43-SPLIT). 0.380000 is below it. The label is not retuned here.

This is not a fabrication call. Capture kind is `page+text`, not interstitial, not `page+binary-office`. `Client Challenge` is absent. The file's visible title is `国家标准 - 全国标准信息公共服务平台` and the record heading is `信息与文献 参考文献著录规则`. QUALITY 59: the refusal rests on that text capture. The right document is on disk. The quoted line is not how the page reads it. The longest run stops at `GB/T 7714-2025 发布日期` because the quote inserts a fullwidth colon (`：`, NFKC to `:`) where the collapsed page has a space.

The dates are on the page. That does not locate the staged quote. After the same collapse, these spans are present:

- `发布 于 2025-12-02 实施 于 2026-07-01`
- `标准号 GB/T 7714-2025 发布日期 2025-12-02 实施日期 2026-07-01`
- `本标准非等效采用ISO国际标准：ISO 690:2021。` (NFKC colon)
- `采标中文名称:信息与文献 参考文献和信息资源引用指南。`

The colon line is absent. QUALITY 8: "source exists" and "the dates occur nearby" are not "the source states this quote". The staged `teaches` cell is an English paraphrase of those spans. It is not a substring. Appending the staged row would admit the colon line and that paraphrase together.

This round cannot fetch a re-read. Wave contract: no fetch. `corpus/lessons/round-43.md` still records L0 `8d77e6c1` open. Round-44 `corpus/evidence/round44/claims.md` does not close it, and its Not-claimed section in the prior round is the same ruling. The staged recheck ("re-open the SAMR detail record") is a live re-open. It was not run.

The capture is older than this round. File mtime `2026-10-23T23:33:09+00:00`. Wave-1 parent receipt start `epoch=1792889279` is `2026-10-25T00:47:59+00:00`. `CAPTURE_BEFORE_RECEIPT True`. Round-43 spot-check route 2, `corpus/lessons/round-43-verifier-spotcheck.md`: "Next scorecard must not call a pre-round cache open a freshness improvement. Closure grade is unchanged, not harmed." Opening this file again is not a freshness event and does not create the colon line.

Round 44's frozen adoption is a different document. `corpus/evidence/round44/claims.md` C3: the entry cites lane id S079, that row's URL is `https://www.rfc-editor.org/rfc/rfc7089.txt`, and the located quote is `constitutes a promise that the resource state`. It must not cite `source: S081`. The staged knowledge file `merge/chousa/knowledge/corpus/knowledge/citation-version-binding-r36.md` cites both `source: S081` (the RFC, staged id) and `source: S082` (this SAMR URL). Landing that second citation would attach the unlocated colon line. C3 does not read S082, so a passing C3 would not license it. The claims say they are not retuned after seats score. This round's one adoption is the RFC quote under the next free lane id, by URL. Staged S082 is not that URL. Copying the packaging id S082 into the lane would skip S079 and would not be the SAMR document's register id either.

## The flip

Flip, both alternatives, neither true as an admission this round:

1. Quote correction, no new fetch required later: before any adoption, replace the colon line with the page's own wording already contiguous in this capture, `标准号 GB/T 7714-2025 发布日期 2025-12-02 实施日期 2026-07-01`, and cite that span. The lane id is the next free registry id at that later adoption, assigned by this URL. It is not staged S082, not register S080, and not register S082.
2. Verbatim re-read: a capture of the cited URL contains the colon line under the strict fold (NFKC + whitespace collapse). Round-42 flip text for register S080, `corpus/evidence/round42/quarantine-verdicts.tsv`: "a re-read of the cited page showing the quoted line verbatim turns the row into present; otherwise the row's quote text must be corrected to the page's current wording before any adoption."

Alternative 2 is false now (`STRICT False`, `FOLD None`) and cannot be made true this round: no fetch, and the committed capture does not contain the line. Alternative 1 is a different quote, not an adoption of the staged row. This round does not write it. The frozen claim admits the RFC sentence as lane S079, not a corrected SAMR span, and the registry ends at S078 with S079 reserved for the RFC URL by document.

Not the flip: "a text capture contains the issued and effective dates as a contiguous span." That span is already present (`发布 于 2025-12-02 实施 于 2026-07-01`, and the 50-character no-colon 基础信息 run). `.ufo/waves/round-44/assimilation/draft/citation-version-binding-r36.md` names that weaker condition and says "Round 43 classed that row not-carried" without the ratio. The document's not-carried ratio is 19/50 under register S080. The 18/43 line is the NII sentence. A flip that is already true would admit the staged colon line on a nearby date span. That is the failure this refusal is for.

Register S082's own flip stays on staged S084: correct `被引用文献（この論文を引用している文献）の一覧が表示されます。 随時増加していきます。` to the NII page's wording, or a capture that contains that sentence. Same examine, `FOLD None`, `STRICT False`, run 18/43. It does not flip staged S082.

## What this seat did not run

`c1-count.py`, `c2-count.py`, and `c3-count.py` were not run. Those checks have not passed here. The refusal does not depend on them. No campaign checker was executed. No URL was fetched.
