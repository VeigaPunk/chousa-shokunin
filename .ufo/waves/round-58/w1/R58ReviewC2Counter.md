# R58 C2 counter review — R58ReviewC2Counter

## Findings

### Critical — frozen C2 predicate is unsatisfiable: span-start offset is compared as quote offset

`corpus/evidence/round58/c2-count.py` reads manifest column 4 as `off`, then requires the unique quote occurrence in the defined capture form to equal it (`occurrences[0] != off` ⇒ `CAPTURE_BIND`). But the pinned builder writes `str(start)` in that column, where `start=max(0, quote_offset-80)`: `corpus/evidence/round58/controls/build-spans-r55.py`, lines 139–149. Thus builder output cannot satisfy the counter's binding for this frozen quote set. The frozen claims require both successful capture binding and byte-identical rebuild.

Evidence (all commands run read-only against lane sources; builder output/work only in `/fast/scratch/hyaku/chousa-r58/R58ReviewC2Counter`):

- `sha256sum` observed raw capture `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3`, lane `tools/build-spans.py` and `controls/build-spans-r55.py` both `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`, and `tools/capture-text.py` `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573` (all match frozen pins).
- Ran: `TMPDIR=/fast/scratch/hyaku/chousa-r58/R58ReviewC2Counter python3 -B tools/build-spans.py --quotes corpus/evidence/round58/c2/quotes.tsv --out /fast/scratch/hyaku/chousa-r58/R58ReviewC2Counter/rebuild --cache corpus/captures` (from lane root). Exact result: builder exit 0, `SPANS_ROWS=12 WRITTEN=12`; it printed quote character offsets 315, 330, 590, 683, 734, 781, 797, 838, 965, 993, 1460, 11723.
- Compared rebuilt manifest offsets with quote occurrences in capture-text form: all 12 fail. Pairs (manifest offset → unique quote offset): `235→315`, `250→330`, `510→590`, `603→683`, `654→734`, `701→781`, `717→797`, `758→838`, `885→965`, `913→993`, `1380→1460`, `11643→11723`. Each difference is 80. Therefore rebuilt manifest (which `rebuilt` requires byte-equal to the committed manifest) necessarily yields 12 `CAPTURE_BIND` failures. Conversely, changing these offsets to quote starts breaks builder byte equality. This is a direct contradiction, independent of entry prose or quality-tool results.

### High — `NEW_GROUND` searches a different Chinese character than the claimed ground

The claim names simplified `载体类型标识` (first character U+8F7D). The counter's base `git grep` literal is traditional `載体类型标识` (U+8F09), while the entry-presence test uses simplified `载体类型标识`. Confirmed codepoints from the checked-in counter: grep literal starts `0x8f09`; entry literal starts `0x8f7d`. The claim-base search for both spellings returned no match today (`git grep -l '<literal>' b13ca7b5c8bbb40d2d29a37fb443c64ca043f791 -- corpus/knowledge`, rc 1 each), so this does not establish existing base contamination. It does establish that the frozen predicate would miss the exact claimed ground if simplified spelling were present in the base. Entry presence is also already implied by a required quote containing that phrase. This is a latent false-PASS in the base-ground test, not evidence that the base currently contains the term.

## Other reviewed surfaces

- Path binding is consistently rooted at resolved `--root` for entry, registry, tools, capture, quote set, and manifest; `LANE` is only its default. The base-ground test additionally invokes `git -C <root> grep`, which requires the base object and may discover a parent repository if root is not itself a repository. Plain directory copies lacking repository history therefore cannot pass the base-ground leg; this is an undocumented input constraint, not a false-PASS demonstrated here.
- Registry check finds first `| S101 |` row, requires 11 cells, `cells[7] == 'mined'`, and `ENTRY_REL` as a substring of `cells[10]`. Current row at `corpus/SOURCES.md:111` has `mined` but its used-by cell names only `corpus/knowledge/citation-count-semantics-r37.md`; it is not bound to the new entry. It does not cross-check the registry's located-quote metadata against the C2 manifest. This is weak binding, although the existing predicate does reject the current row until used-by is updated.
- Rebuild checks exact manifest bytes and every committed `spans/*.txt` against rebuilt bytes; it does not reject additional rebuilt span files. No demonstrated false PASS from that asymmetry.
- Quote-in-entry checks all 12 manifest quote strings as substrings of the entry; uniqueness/offset binding, span bytes, exact frozen quote order, and rebuild are separately required. Frozen `quotes.tsv` quotes exactly match the 12 counter literals. All 12 occur exactly once in the defined form, lengths are 13–36 characters, and exactly 3 are line-start anchored; thus those floors are reachable and are not the blocker.
- The `CONTEXT` condition has a dead second arm: `len(expected) > len(quote)+162` cannot occur because the slice extends at most 80 characters on each side (≤ `len(quote)+160`). No context-floor failure is demonstrated; the pinned builder and quote-substance checker independently enforce contextual spans.
- Malformed quote-table rows with non-four-column cells are omitted from the counter's `actual` list, but the pinned builder rejects them, so rebuild fails closed. `--work` is not checked for separation from root; caller must honor the fresh scratch-dir contract.

## Verification gaps

- Did not run a full `C2=PASS` fixture: the offset/rebuild contradiction proves no such fixture can satisfy the frozen checks. The live root has no new entry/manifest, so a full counter run there would only demonstrate expected pre-data failure.
- Did not run external quality tools to claim their results; their output is irrelevant to the incompatible offset requirements.
- No live fetch; all source evidence was the committed capture and frozen quote table.

VERDICT: The frozen C2 build-spans offset-binding attack survives: the counter's required capture binding and byte-identical pinned-builder rebuild are mutually exclusive for all 12 S101 quotes. The base-ground spelling discrepancy is a separate latent false-PASS risk; simplified spelling is absent from the claim base in the checked corpus tree.
