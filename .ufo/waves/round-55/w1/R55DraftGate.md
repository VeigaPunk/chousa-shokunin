# R55DraftGate — scoped findings

Axes: operability (collision/reopen instructions), depth (document-level source decisions), calibration (independent quote relocation).

## Gate draft

### Collision check

Observed in `.ufo/waves/round-55/assimilation/`: `reg-ids` has 123 IDs (S001–S123), `staged-ids` 114 (S082–S195), `collisions` 42 (S082–S123), `quarantine-slice` 24 rows. `guard-proof.txt` records that a two-space-indented `  | S002 | x |` in `guard/reg.md` collides with `| S002 | z |` under the 0–3-space pattern (`guard/c03` = S002), but not under the column-zero pattern (`guard/c0` empty). Other guard files are `r`, `r0`, and `s`; the tested row is explicitly indented, so use the 0–3-space collision interpretation.

Renumber by document, not by old number: staged S130 → lane S124, http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc; staged S131 → lane S125, http://m.cnpharm.com/201906/18/c280684.html; staged S143 → lane S126, https://english.nmpa.gov.cn/2019-07/18/c_388252.htm; staged S133 → held lane S113 only, https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3. The S133/S113 mapping is identity by document URL; cite it only as existing S113, not as a new lane row.

Commands/outcomes: `grep -cE '^S[0-9]{3}$' reg-ids staged-ids collisions` yielded respectively 123, 114, 42; `grep -cE '^ S[0-9]{3}' quarantine-slice` yielded 24. The exact inspected contents are in the listed assimilation files. (Command run from the assimilation directory.)

### Re-opened sources (no network; local campaign cache)

| lane id | document | URL | defined text form re-opened | headline quote (character offset) |
|---|---|---|---|---|
| S124 | NMPA《上市药品临床安全性文献评价指导原则（试行）》, copy hosted by gcpunion.org | http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc | OLE `.raw` through `python3 .../tools/capture-text.py .../bdff491a75c6abeda1d9c01d.raw`; stdout saved in scratch and read as UTF-8; 13,718 chars | `应当说明是否有检索限制（如语言限制）、是否手工检索、是否检索灰色文献等关键问题。` (char 4652; once, line 53) |
| S125 | 中国食品药品网 /《中国医药报》 issuance report | http://m.cnpharm.com/201906/18/c280684.html | `.txt` read UTF-8 with universal newlines; 1,673 chars | `根据通告，指导原则分为概述、方法学要点、报告撰写规范、指导原则所依据的参考文献和附录五个方面。` (char 775; once, line 100) |
| S126 | NMPA English notice | https://english.nmpa.gov.cn/2019-07/18/c_388252.htm | `.txt` read UTF-8 with universal newlines; 3,774 chars | `which was issued on June 18, 2019.` (char 1324; once, line 157) |
| S113 (held) | 中国循证医学杂志 PRISMA-S interpretation, 梅斯医学 portal | https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3 | `.txt` read UTF-8 with universal newlines; 8,804 chars | not used as a new-source quote; it remains the existing held S113. |

Re-location commands actually run: `python3 tools/capture-text.py /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/bdff491a75c6abeda1d9c01d.raw` (exit 0); a Python check of the forms found S124/S125/S126 quotes once at the offsets above. The English title string occurs twice, so the report uses the unique sentence fragment above instead. The OLE form contains `是否检索灰色文献` once (char 4678); it is in the same line as the S124 quote. `tools/capture-text.py` sha256 observed: `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573`.

### Assimilation decisions

Theme: what the NMPA grey-literature search-record field says, and what the document-level sources can establish.

| staged item | decision | reason | checkable flip |
|---|---|---|---|
| `grey-literature-and-chinese-search-record-r40.md` | **admit, narrowed**; bind the three independently identified documents as S124, S125, S126. Keep the subject to this drug-safety guideline and its issuance/identity; do not claim current force or generalize to every Chinese regulator or clinical/HTA domains. | S124 directly states that reports should disclose whether grey literature was searched; S125 independently reports issuance and the five-part structure; S126 is the NMPA-domain English notice and identifies issue date/legal hook. This supports the bounded, document-specific field, while the staged assertions about commercial PRISMA-S remain only under held S113. | Re-open the three defined forms above; require the S124 field, S125 five-part statement and S126 date/legal-hook statement to remain present and uniquely locatable. To broaden beyond drug-safety or assert current force, require a current primary NMPA status source and a separate regulator/domain source. |
| `grey-literature-field-boundary-r43.md` | **refuse this round** (same theme family). | Its staged claim is a negative boundary claim about a provincial implementation of a different national quality-control guideline; it does not establish the NMPA search-record field, and cannot be admitted as support for this round's focused field. The staged entry itself says the document carries no grey-literature wording. | Flip only if a newly re-opened defined form of that implementation supplies an exact, unique grey-literature search/report-field statement attributable to the document; otherwise retain refusal. Its source is S161, https://wjw.guizhou.gov.cn/zwgk/zdlyxx/ywgl/202505/t20250530_87947626.html. |

S133 is not admitted as a new lane document; its URL remains bound only through existing held S113, so it is not listed as a refused document.
`refused-doc https://wjw.guizhou.gov.cn/zwgk/zdlyxx/ywgl/202505/t20250530_87947626.html` — S161 is not bound to the admitted r40 entry.

The requested theme-family entries were read: r41 (`grey-literature-and-chinese-search-record-r41.md`), r42 (`grey-literature-field-china-r42.md`), r43 (`grey-literature-field-boundary-r43.md`), r44 (`grey-literature-national-route-r44.md`), and r48 (`grey-literature-mandate-scope-r48.md`). Their opening source/claim text shows distinct journal-practice, workflow-standard, quality-control-boundary, national-route, and mandate-scope questions; r43 was selected for the explicit boundary refusal. No claims about the unseen remainder of those entries are made here.

### Non-author spot-check

- **Admit:** r40 entry, narrowed to the regulator's field and document-specific conclusions. Re-open `corpus/knowledge/grey-literature-and-chinese-search-record-r40.md`; derive S124's URL key (`bdff491a75c6abeda1d9c01d`), run `tools/capture-text.py` on that `.raw`, and check the quoted report-field sentence once at char 4652. Then read the UTF-8 universal-newline S125 and S126 `.txt` forms and check their table quotes at chars 775 and 1324. Verify the lane entry binds only S124–S126 and preserves the no-current-status caveat.
- **Reject:** the new S133 leg in r40. Re-open the staged r40 source line and `453d492becd9a2f4632cb8dd.txt`; confirm its commercial portal identity and do not create a new S133 row or cite staged S133. Check the lane entry cites the URL only as held `source: S113 — https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3`, with matching `used-by` on S113; do not add a `refused-doc` line for this already-bound S113 document.

VERDICT: Built the Gate draft from the assimilation records and independently re-located defined-form quotes; r40 is a narrowed three-document admission, with the commercial S133 leg held at S113 and r43 refused.
