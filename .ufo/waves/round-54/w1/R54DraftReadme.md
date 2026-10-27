# R54DraftReadme — corpus/README.md additions for round 54 (W1, scribe)

Axes: depth (per-document credit, honest), operability (a reader can re-run every
number). Scope: draft only — no production file was written; the append text below
is for the L1 to place. Nothing here adjudicates C1/C2 or a quarantine verdict; the
measurements are handed over, the calls are the Gate's.

## 1. Commands run and what they printed

Base sweep the item names (no pipe, so the rc is grep's):

```
$ git -C /home/vgpnk/Projects/shokunin/chousa-shokunin grep -l \
    -e 'ISO 690:2021' -e 文献载体标识 c49ffc6ce1c3de87c1dfa96856239ed7274bf07b -- corpus/knowledge
(no output)
rc=1
```

Two more base sweeps for the credit claim (same revision, `-- corpus/knowledge`):

```
$ git ... grep -l -e 'std.samr.gov.cn' -e 'openstd.samr.gov.cn' -e 'xuebaobangong' \
    c49ffc6c... -- corpus/knowledge
(no output)   rc=1
$ git ... grep -n '7714-2025' c49ffc6c... -- corpus
corpus/README.md:1061 (the round-44 coverage row)
corpus/knowledge/citation-version-binding-r36.md:21 (the refusal + flip)
corpus/lessons/round-44-verifier-spotcheck.md:141
corpus/lessons/round-44.md:108
```

So at BASE_REV the lane holds the standard only as a *refused staged row*
(`corpus/knowledge/citation-version-binding-r36.md:21`: "Staged S082, the SAMR
record for GB/T 7714-2025, is not adopted … Flip: a text capture of that record
contains the issued and effective dates as a contiguous span."), never as a fact.

Capture measurements (`.qcache` sidecars read as UTF-8, `str.find` on the whole form):

| capture | measurement |
|---|---|
| SAMR `adf6ba934e813b2c326fa150` (6,626 B) | `GB/T 7714-2025` ×2; `2025-12-02` at char 1034, `2026-07-01` at char 1053 (19 apart, separate cells); `代替了以下标准 … GB/T 7714-2015 …（全部代替）`; `本标准非等效采用ISO国际标准：ISO 690:2021。` at char 1797 ×1 |
| openstd `b9ca2a4fdf9455867534f144` (24,185 B) | `本系统不提供文本阅读服务` at char 15223 ×1 (inside `该标准采用了ISO、IEC等国际国外组织的标准，由于涉及版权保护问题，本系统不提供文本阅读服务` at 15188); `ISO 690:2021` ×0 |
| JMU `0f33243fd7ac2fe88b85c1ba` (190,614 B) | `本文件适用于作者和编制者著录参考文献` at 5576 ×1; `本文件不适用于图书馆员、文献目录编制者以及索引编制者著录参考文献。` at 5602 ×1; `文献类型标识、文献载体标识应按照` at 11542 ×1; A.1 body = 17 rows (M J N C D R S P EB A CM DS PP G CP DB Z); A.2 rows `磁带…ＭＴ` 59025, `磁盘…ＤＫ` 59073, `光盘（ＣＤ－ＲＯＭ）` 59116, `联机网络…ＯＬ` 59161, `缩微资料…ＭＭ` 59201; change list `增加了文献类型“预印本”及其标识` at 4765 ×1 |
| HIT `.doc` raw `6dc68fd6b32ce9c8dfcebce8` (129,024 B, sha256 `6063a3af…d9fddf3` = the S101 registry pin) | under the candidate tool: exit 0, 469 lines / 47,356 B, 0 U+FFFD, 0 disallowed control chars; `本规范推荐采用GB/T 7714中规定的顺序编码制格式著录` at 12795 ×1 |
| S130 `.doc` raw `bdff491a75c6abeda1d9c01d` | under the candidate tool: exit 0, 865 lines / 34,234 B, `是否检索灰色文献` at char 4678 ×1, 0 U+FFFD |

Capability check I ran (not a counter run; the C1 pass receipt is the L1's):

```
$ python3 /home/vgpnk/.../chousa-shokunin/tools/capture-text.py \
    /home/vgpnk/.../.qcache/6dc68fd6b32ce9c8dfcebce8.raw > $S/hit.txt 2> $S/hit.err
rc=0   (hit.err empty; wc -c -l → 469 lines 47356 bytes)
$ ... bdff491a75c6abeda1d9c01d.raw > $S/s130.txt
rc=0   (865 lines 34234 bytes)
$ sha256sum tools/capture-text.py
fd0ed3f58565b781ab8eedaad5d229976e150bdd8e391a2b0cacd0a0825fcd89   # = the sha in c1-after-candidate.txt
```

Re-anchoring shown, not assumed: `每一篇文章或资料应根据其内容性质标识一个文献标志码`
lies at char 12007 of the new form against round-49's `S101` span offset 11166
(`corpus/evidence/round49/spans.tsv:20`), and `本规范推荐采用…顺序编码制格式著录`
at 12795 against 11945 (`:23`). The UTF-16LE offsets do not carry over.

## 2. Draft — append to `corpus/README.md` after line 1163 (append-only)

```markdown
## Round54 coverage and frontier (2026-10-26)

| Note | Holds | Sources |
|---|---|---|
| `knowledge/source-type-taxonomy-r36.md` | Round-54 note (adopted by document from `merge/chousa/`): the PRC citation standard as its own authority states it — GB/T 7714-2025 published 2025-12-02 and in force 2026-07-01, wholly replacing GB/T 7714-2015, a non-equivalent adoption of ISO 690:2021 (采标情况 block); and the official full-text portal's own refusal to serve the text (`本系统不提供文本阅读服务`, because the standard adopts ISO/IEC documents) — so a document's identity and status are provable from the authority while its operative wording is not, and a document-type list names form, never authority for a claim | `S121`, `S122`; `corpus/evidence/round54/spans.tsv`; `corpus/lessons/round-54.md` |
| `knowledge/source-type-taxonomy-r37.md` | Round-54 note (adopted by document, narrowed): the operative text as a university editorial office's third-party copy states it — the scope clause `本文件适用于作者和编制者著录参考文献` with its express exclusion of librarians, catalogue compilers and indexers (`本文件不适用于图书馆员、文献目录编制者以及索引编制者著录参考文献。`), 7.3's joint type-and-carrier rule (`文献类型标识、文献载体标识应按照`), 附录 A.1's 17 type codes (M J N C D R S P EB A CM DS PP G CP DB Z) and A.2's 5 carrier codes (MT DK CD OL MM), 7.6's four dates in `YYYY-MM-DD`; the 2025 change list moving 预印本 in with code PP (`增加了文献类型“预印本”及其标识`); and the held data specification's nine elements beside its separate 文献标志码; Latin letters render fullwidth in this copy, so nothing here is quoted as the authority's typography | `S123`, `S101`; same |
| `../tools/capture-text.py` | Round-54 capability (C1 candidate `8a7d0f1`): a defined text form for an OLE Word 97+ `.doc` — CFB reader, FIB, Clx piece table, cp1252/UTF-16LE pieces, main story CP 0..ccpText, field results only; refuses `ole-not-word` / `ole-encrypted` / `ole-malformed` | `corpus/evidence/round54/claims.md`; `corpus/evidence/round54/c1-count.py`; `corpus/evidence/round54/c1-after-candidate.txt` |

Coverage credit is per document: three new documents — the SAMR record (`S121`: identity, status, replacement, adoption basis), the openstd notice (`S122`: the portal's own no-text statement) and the JMU copy (`S123`: the standard's operative wording, third-party) — and none was in the lane at the base (`git -C /home/vgpnk/Projects/shokunin/chousa-shokunin grep -l -e 'ISO 690:2021' -e 文献载体标识 c49ffc6ce1c3de87c1dfa96856239ed7274bf07b -- corpus/knowledge` → exit 1, no output; a sweep for the three URLs → exit 1, no output). `S101` is held and earns none. The SAMR record is the document round 44 refused as staged S082: its capture holds `发布 于 2025-12-02` and `实施 于 2026-07-01` in separate table cells nineteen characters apart (`2025-12-02` char 1034, `2026-07-01` char 1053) and the register's fifty-character header line zero times, so that round's flip — the issued and effective dates as a contiguous span — is still unmet, and the entry cites the cells, not the register line.

**The OLE `.doc` text form.** `tools/capture-text.py` now prints a defined text form for OLE Word 97+ `.doc` (receipt `corpus/evidence/round54/c1-after-candidate.txt`), giving the held `S101` a defined form where its registry cell still names a UTF-16LE reading — its committed offsets are not reused, and C2 needs no new span for it — and removing the form blocker on the refused `S130` (`是否检索灰色文献` at char 4678, 0 U+FFFD), which still enters no entry this round; `.xlsx` and `.pptx` captures stay refused, not read.

### Frontier

Advanced:

- **Source-tier adjudication** (both entries' `ground:`). The standard's own scope clause lets the lane keep two vocabularies apart with a citation: the **form** axis (17 types, 5 carriers — what a citation points to and the medium it was read in) and the **tier** axis (how authoritative a source is for a particular claim); a standard that claims authors and expressly disclaims librarians, catalogue compilers and indexers is not an authority on what a citation *counts as*.
- **Authority versus third-party copy of one document.** The authority states it serves no text for ISO/IEC adoptions for copyright reasons, so identity and status are provable from it (`发布 于` / `实施 于` cells, the 采标情况 block) while the operative wording is only available from a third-party copy — the two roles now recorded on one real case, with the reproduction's fullwidth Latin named as a limit of the copy.
- **Other capture forms** (round-52's item, advanced on the C1 candidate). OLE `.doc` now has a defined text form instead of the round-48 UTF-16LE reading.

Left open:

- **The standard's operative text from an entitled copy.** Only the JMU reproduction is captured; whether its 附录 A.1/A.2 rows match an entitled copy is untested.
- **The register line on the SAMR record.** `S080`'s quote is absent as written (measured above) and round 44's flip is still unmet; nothing is claimed from the register line.
- **The reseller's table of contents.** Still HTTP 403; nothing from it is admitted.
- **Applicability of the codes.** Whether any type or carrier code is in force against a particular publisher or index was not checked.
- **The refused `S130` regulator field.** The form blocker is gone, the document is outside this round's frozen by-document set, and the guideline's currency stays an Unknown.
```

## 3. Why each row says what it says (credit honesty)

- The `r36` row credits **two documents** with separate scopes: identity/status from the
  authority, and a *refusal* as a document in its own right (the notice is the only
  statement of why no text exists). It states the adoption fact and does not repeat the
  staged entry's taxonomy enumeration, which the entry itself lists as Unknown.
- The `r37` row credits **one new document** (the third-party copy) and names `S101` as
  held, not as credit; the nine elements and 文献标志码 belong to `S101`, not to the 2025
  standard, and the row keeps them apart.
- No row claims a bound/refused status: the counter fixes `BOUND>=2` and
  `BOUND+REFUSED=3`, and which document is refused is the Gate's call. The credit
  paragraph is therefore written per document, with `S101` explicitly zero.
- The capability row follows round 53's shape for `assimilate-rows.py` (tool, version,
  receipts); it cites the L1's receipt for the C1 pass and only my two observed tool
  runs for the held/refused rows.

## 4. Findings handed to the L1 (not patched, not adjudicated)

1. **`S080` is the sharp one.** The register quote `标准号：GB/T 7714-2025 发布日期：2025-12-02 实施日期：2026-07-01`
   is a synthesized header: `find` → -1, while the three facts sit in separate cells.
   `absent-as-written` is the reading the round-42/43/44 receipts took (19/50, 0.380000);
   a seat that instead rules it `fabricated` makes the SAMR document un-bindable under
   the frozen C2 quarantine clause, which would move the bound pair onto openstd + JMU.
   The measurement is above so the call can be made on bytes.
2. **`S101`'s registry text-form cell is now stale** — `corpus/SOURCES.md:111` still reads
   "UTF-16LE text of the raw .doc capture" and its `anchor` offsets (11170, 11205, 11993,
   12161, 13247, 34374) are UTF-16LE offsets. C2 needs no new span for `S101`, so this is
   a disclosure item for the lesson/erratum, not a counter blocker.
3. **`S088` (JMU) register quote** is absent as written for layout: the five rows occur
   once each (59025, 59073, 59116, 59161, 59201) but the ` … / … ` separator form does not.
   `S096` (HIT) is mixed: `根据GB3469规定，以单字母方式标识以下各种参考文献类型` is
   present once at char 336 of the new form, while `参考文献格式，参照 GB/T 7714，采用`
   is absent — the capture's parameter table reads `参考文献格式，参照ISO 690` (char 25123).
   That is a substantive difference, not only a spacing one.

## 5. Out of scope / limits

- I did not run `c1-count.py`, `c2-count.py`, `build-spans.py`, `quote-substance-check.py`
  or `inference-ground.py`; no LibreOffice was invoked (no `soffice` process was started,
  `pgrep` clean), so nothing about allocation/legs is mine.
- I did not read the round-54 lesson (not yet written) or decide the Gate, QUALITY or
  province — `R54DraftGateTable`, `R54ReviewProvince`, `R54CritTheme` own those.
- Tooling: no install, no upgrade (nothing needed; `python3` stdlib only).
- Scratch `/fast/scratch/hyaku/chousa-r54/R54DraftReadme/` held `hit.txt`, `s130.txt` and
  their stderr files; every number above is pasted, and the directory was removed.

VERDICT: drafted the append-only README additions (two coverage rows + capability row +
credit paragraph + round-54 Frontier) from base sweeps and capture bytes, and attacked
the credit story — the SAMR record's round-44 flip is measurably still unmet (dates 19
characters apart, register line absent), `S101` earns none and its anchors do not survive
the new OLE form, and `S130`'s form blocker is gone without entering the round.
