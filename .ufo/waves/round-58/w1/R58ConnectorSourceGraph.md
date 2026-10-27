# R58ConnectorSourceGraph — S101 source graph and carrier-alphabet overlap

Seat: R58ConnectorSourceGraph (leaf, no dispatch). Lane HEAD `5da0a63`; claim base `b13ca7b`; freeze `9e73a03`.
Scope: map S101 use across corpus knowledge; test whether the proposed `corpus/knowledge/carrier-alphabet-china-r58.md` is distinct from existing citation-count and metadata entries. Read-only. No live fetch. No installs (no tooling needed).

## 1. Freeze integrity (run)

    git cat-file -t 9e73a031ab1ac3bac343de008850d7d87f9e5634   -> commit
    git merge-base --is-ancestor b13ca7b5... HEAD               -> base-is-ancestor-of-HEAD
    git diff --stat 9e73a031... HEAD -- corpus/evidence/round58/claims.md corpus/evidence/round58/c1-count.py corpus/evidence/round58/c2-count.py corpus/evidence/round58/c2/quotes.tsv
                                                                -> (empty), diff-exit=0
    git diff 9e73a031... HEAD -- corpus/SOURCES.md              -> (empty)

Frozen predicate, quote set and SOURCES.md are byte-identical to the freeze. HEAD adds only later control/opening files.

## 2. Source and digest (run in scratch copy of tools/capture-text.py)

    sha256(tools/capture-text.py copy)  2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573  (matches claims.md pin)
    sha256(corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw) 6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3  (matches)
    python3 capture-text.py <raw>  -> 27012 chars
    sha256(corpus/evidence/round54/S101-text-form.txt) a8e3e7ad213b6ec5...  == capture-text output (cmp: identical)

All 12 frozen quotes (quotes.tsv rows 2–13) count exactly 1 in the defined form. Offsets: 315, 330, 590, 683, 734, 781, 797, 838, 965, 993, 1460, 11723.

The lane's `.txt` sidecar `corpus/captures/6dc68fd6b32ce9c8dfcebce8.txt` is not a usable form: 128,416 chars, 14,486 U+FFFD, OLE header bytes; 0 hits for 1．2 参考文献类型及其标识, 根据GB3469规定, 文献类型及载体类型标志, 文献标志码, 并以[文献类型标识/载体类型标识]表示, 载体类型标识, 为便于文献的统计和期刊评价.

## 3. Source graph: how S101 is used now

| Surface | S101 use (verified) | Locator, defined form | Relation to proposed entry |
|---|---|---|---|
| `corpus/knowledge/citation-count-semantics-r37.md` | `source: S101` line 5; 6 S101 quotes in Observation/Inference, all taken from the raw UTF-16LE decode (its own source line says so) | 文献标志码 (§11, 11972/12007); 文献类型及载体类型标志 (§14.2 list, 12963); GB/T 7714 (§14.1, 12802); 参照ISO 690 (14049; 25123 for the 15.x line) | Only other lane entry citing S101. Shares one point: §11 `文献标志码`. Does not state the alphabet, the carrier codes or the [type/carrier] notation. |
| `corpus/knowledge/source-type-taxonomy-r37.md` | No S101 line. `#### Unknown` (line 62) defers "the older data specification beside it (the lane's held HIT row)" | — | Concept-family overlap: 文献类型标识 / 文献载体标识 at base (`git grep -c`: r37 7 lines, r36 1 line); MT/DK/CD/OL carrier codes; standard GB/T 7714-2025 (S123), not the S101 edition. |
| `corpus/SOURCES.md:111` (S101 row) | `used-by` = `corpus/knowledge/citation-count-semantics-r37.md` only (base and HEAD identical); status `mined`, 11 cells | Anchor cell still says "UTF-16LE text of the raw .doc capture" with raw offsets 11170…34374 | Frozen counter reads cells[10]; new entry must be added there. |
| `corpus/README.md:1187`, `:1210`; `corpus/lessons/round-54.md` Gate row (line 45) | Frontier item "HIT data specification's carrier alphabet beside the standard's"; round-54 refused the S101 leg of the r37 draft (raw-decode anchors) | — | The proposed entry is the designed successor of a deferred leg, not a new idea. |
| `metadata-screen-r25`, `claim-record-fields-r33`, `citation-chain-fidelity-r24` (metadata header), `cnki-citation-check-r40` | No S101 use | — | "Metadata" here means lane knowledge-entry headers, JSON fields, and CNKI 引文核对. No bibliographic-code overlap. |
| `corpus/evidence/round54/S101-text-form.txt`; SCORECARD "Round 54 pointer corrections" | Re-points S100/S101 anchors into the defined form | — | The defined form is the only form in which frozen quotes occur (above). |

Other S101 mentions (counts) are evidence, lessons, controls and fixtures; none is a knowledge entry.

## 4. Overlap verdict on the proposed entry

- Distinct from citation-count-semantics-r37: yes. The proposed quotes (§1.2, §1.2.4, §11 heading) are not among r37's six S101 quotes. The only shared point is the §11 heading `与文献标志码(Document code)` (frozen row 12, offset 11723) versus r37's `文献标志码` quote at defined 12007. Different offset, different sentence.
- Distinct from metadata entries: yes; no shared content.
- Not distinct in concept from source-type-taxonomy-r37 (S123): carrier codes and 文献类型标识/文献载体标识 are the same family. Distinctness rests on source (S101 vs S123) and edition. That edition contrast is the one r37 flags as open (its Inference: "the type letters are renamed between editions"). The proposed entry needs to state it; the frozen counter's new-ground test does not measure it.

## 5. Findings the frozen predicate does not measure (source-graph facts; no verdict on C2)

F1. The alphabet letters are not in the frozen quote set. Rows 1–2 quote the lead-in "根据GB3469规定，以单字母方式标识以下各种参考文献类型：". Rows 3–11 quote electronic/carrier fragments and the [type/carrier] examples. None quotes the M/C/N/J/… table or the DB/CP/EB letters. The entry therefore can name the alphabet without a frozen anchor for its content.

F2. S101 gives two single-letter tables that differ (run on defined form):
- §1.2 table (char 330–469): types include 档案 and 古籍; codes `M C N J D R S P G B O K` (12).
- §14.3.1 (char 13105–13221): types `普通图书 会议论文 报纸文章 期刊文章 学位论文 报告 标准 专利 汇编 参考工具`; codes `M C N J D R S P G K` (10). 档案 and 古籍 are absent.
Neither table is quoted in the frozen set, and no lane entry notes the divergence. Any alphabet statement must say which table it reads.

F3. Wording differs by section: §1.1 and §1.2 use 文献类型及载体类型标识 / 文献类型标识 (`标识`). §14.2 and §14.3 use 文献类型及载体类型标志 / 文献类型标志 (`标志`). Counts: `文献类型及载体类型标识` 1, `文献类型及载体类型标志` 1. The frozen new-ground token `载体类型标识` matches only the §1 wording. The token test is therefore a wording test, not a concept test.

F4. Locator labels in citation-count-semantics-r37 and the SOURCES S101 row are not all accurate in the defined form. The 文献类型及载体类型标志 quote sits at 12963, inside the §14.2 list (between heading 14.2 at 12851 and 14.3 at 13090), but the SOURCES row groups it under "15.7 parameter table". My heading regex did not match a 15.7 heading. The 34374→25123 locator for ISO 690 falls after 15.6 at 25079, so that one is consistent with 15.x. [INFERENCE for 15.7; not confirmed by a heading.]

F5. Two offset systems for one source. The r37 entry and the SOURCES S101 row use raw UTF-16LE offsets (e.g. 为便于 11170, 文献类型及载体类型标志 12161, ISO 690 34374). The defined-form offsets are 11972, 12963, 25123 for the same quotes. QUALITY item 97 and round-54 Mistakes row 2 say the raw form is undefined. The SCORECARD correction re-pointed the anchors, but the SOURCES row was not edited (diff empty since freeze).

F6. used-by semantics. The frozen counter tests containment (`ENTRY_REL not in cells[10]`), not replacement. QUALITY item 100 says "updated old→new", but its HELD_CITED check requires every entry carrying `source: S101 — <url>` to be named. citation-count-semantics-r37 still carries that line, so a replacement would fail that check. Consequence: the SOURCES S101 row must list both entries. [INFERENCE from QUALITY 100 text; the HELD_CITED check was NOT run.]

F7. SOURCES S101 row claim "a separate 文献标志码 A-E": my pattern search (`文献标志码[：:]\s*(\S)`; `A、B`, `A-E`, `A～E`, `ABCDE`) found only `文献标志码： A` (11.7) and `A、B` in the abstract section (9.3, char 11020). The A–E set was NOT located in the defined form. Not run beyond those patterns.

F8. The S101 §1.1 item list has nine elements (a–i), matching the SOURCES row's "nine prescribed elements". Observed; not a C2 leg.

## 6. Proposed patches (report only; no lane file edited)

- SOURCES S101 row: re-point the anchor cell to the defined form (`capture-text.py` sha 2c0140bc…) with offsets 315–1460, 11723, 12963, 14049, 25123. Keep `citation-count-semantics-r37.md` and add `corpus/knowledge/carrier-alphabet-china-r58.md` to `used-by`.
- Entry: state the edition relation to source-type-taxonomy-r37 (S101 1990s–2000s GB3469 layer vs S123 GB/T 7714-2025 layer) and disclose the §1.2 vs §14.3.1 divergence (F2).
- Counter (for L1, not edited): a concept-level new-ground check is absent; the token test passes for either wording.

## 7. Checks not run

- `tools/inference-ground.py`, `tools/build-spans.py`, `c2-count.py` (run as a whole) — NOT RUN by this seat.
- HELD_CITED check from QUALITY 100 (`corpus/evidence/round54/c2-count.py`) — NOT RUN.
- Full read of §11 / §15.7 for the A–E set — NOT RUN beyond the patterns in F7.

## 8. Commands (exact, read-only; scratch `/fast/scratch/hyaku/chousa-r58/R58ConnectorSourceGraph/`, removed before yield)

    git grep -c '载体类型标识' b13ca7b5c8bbb40d2d29a37fb443c64ca043f791 -- corpus/knowledge  -> exit 1 (no output)
    git grep -c '文献载体标识' b13ca7b5c8bbb40d2d29a37fb443c64ca043f791 -- corpus/knowledge  -> r36:1, r37:7
    git show b13ca7b5...:corpus/SOURCES.md | grep '^| S101 '                                  -> used-by = citation-count-semantics-r37.md
    python3 -c "…quotes.tsv counts on s101-form.txt…"                                          -> 12 rows, each 1 at offsets above

VERDICT: attack "proposed carrier-alphabet entry duplicates existing citation-count/metadata entries" — FALSIFIED (distinct source, distinct content; only shared point is the §11 heading `文献标志码`); attack "frozen new-ground token distinguishes the entry from source-type-taxonomy-r37" — SURVIVES (concept-family overlap with S123 carrier codes is unmeasured; the §1.2 vs §14.3.1 letter divergence and F3–F6 are not covered by the frozen set).
