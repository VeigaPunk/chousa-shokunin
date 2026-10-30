# SourcesDraft — round65 S154/S155/S156 registry rows and Gate quotes (2026-10-30)

Seat: SourcesDraft (leaf scribe, lane chousa round65). Scope: draft and independently verify registry rows and Gate quotes for S154 (git-cat-file(1), scoped A), S155 (hashlib.py, scoped A), S156 (round64 controls/c1v3-before-full.txt, own-work B). No registry append; no production writes; no tests/batteries; no network; read-only git with explicit -C only. Duplicate of `SourcesDraft/report.md` (seat spec named the folder path, the Report trailer named this file; contents identical).

## Gates observed

- Freeze f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd; claims.md holds exactly two claims (C1 operability, C2 depth sourced), confirmed by read. Reader truncated claims.md line 14 at 768 chars; re-read `:raw:14` in full before relying on C2 wording.
- Working tree carries the drafts uncommitted: `git -C <lane> status --porcelain -- <paths>` → ` M corpus/README.md`, ` M corpus/SOURCES.md`, `?? corpus/evidence/round65/source-openings.json`, `?? corpus/knowledge/receipt-identity-r65.md`, `?? corpus/lessons/round-65.md`. Consistent with claims.md "preliminary uncommitted planning does not freeze any others". Registry rows S154–S156 already exist as uncommitted drafts at SOURCES.md lines 164–166 (S157 at 167, not this seat); this seat cross-checked, never modified.

## Source verification (all sources opened by this seat)

| src | file | sha256 vs source-openings.json | located quote (≤25 words) | position verified |
|---|---|---|---|---|
| S154 | /usr/share/man/man1/git-cat-file.1.gz (owned by git 2.56.0-1, `pacman -Qo`) | 8eb0bb079fa0cdf682920d0327fc1e72d5704961c9c54cdc716909251efd5737 = match | `If <type> is specified, the raw (though uncompressed) contents of the <object> will be returned.` (15 words) | roff line 505, under `.SH "OUTPUT"` (495) before `.SH "BATCH OUTPUT"` (506); rendered `MANWIDTH=1000 man -l \| col -bx`: OUTPUT at rendered line 150, quote at rendered line 159; `.TH` date 2026-09-27, version Git 2.56.0 |
| S155 | /usr/lib/python3.14/hashlib.py (owned by python 3.14.8-1) | 88fa624821fbdee7eb2ef87c2437b207afe328cf117c7463367e2db5eb1af492 = match | `Return the digest of the bytes passed to the update() method` (12 words) | module docstring lines 31–32 (sentence spans both; quoted span wholly on line 31); row's cited block lines 27–34 contains it; python3 --version 3.14.8 |
| S156 | corpus/evidence/round64/controls/c1v3-before-full.txt | ca05f579dc0f979a772ecec973a1da5d5df8d11881ca678708c72044f8c9c05b = match | line1 `LEG CLEAN clean ok ok` (5 words); line44 `CLEAN=1/1 DEFECTS=17/28 BENIGN=8/11 ZERO=3/3 BATTERY=FAIL` | 44 lines, 1505 bytes, trailing newline; no REVISION/EXIT/SHA256 lines anywhere in the file; `git -C <lane> show d6ed8155e9b4735639a2cf0a3e479c62f2056195:<path> \| sha256sum` → identical hash, so the row's "at base d6ed8155…" cell is accurate |

## Findings

1. **MISQUOTE-CLASS DISCREPANCY (S154), report verbatim:** every drafted instance (source-openings.json S154 `quote`; SOURCES.md S154 row quote cell; receipt-identity-r65.md claim 1; round-65.md Gate row S154) reads `…contents of the object will be returned.` The rendered source line 159 reads `…contents of the <object> will be returned.` The drafts silently replace the placeholder token `<object>` with `object` while keeping `<type>` verbatim earlier in the same sentence — inconsistent de-markup, not a lane convention (adjacent rows quote rendered text verbatim, e.g. S150/S151). Word count 15 either way, so the ≤25-word Gate limit is unaffected. Suggested fix for L1 integration: restore the verbatim `<object>` in all four drafted instances.
2. S154 location cells say "OUTPUT" / "OUTPUT paragraph on explicit type" — verified correct; adding "rendered line159 (MANWIDTH=1000 man -l | col -bx)" would make the recheck exact. Draft suggestion only.
3. S155: quote cells locate lines31–32; the 12-word quoted span sits wholly on line 31, the sentence continues to line 32 ("so far as a bytes object."). Accurate as written; noted for recheck precision.
4. S156: line44 aggregate (DEFECTS=17/28 BENIGN=8/11) is the earlier inherited state; round-64.md's final measurement at 944955cc reads DEFECTS=28/28 BENIGN=9/11. Entry claim 3's framing — missing in-file headers, "not that the historical receipt has no provenance anywhere" — is consistent with both. Confirmed no REVISION/EXIT/SHA256 header line exists in the file.
5. Structural observation by reading only (counter NOT run, not assigned to this seat): all ten c2-count.py text fragments are present in the working tree — `source:` at entry start; `\nverified-at:`; `\nrecheck:`; S154/S155/S156 in the entry; `| S154 |`, `| S155 |`, `| S156 |` in SOURCES.md; `receipt-identity-r65.md` in corpus/README.md line 1342; `## Claims`; `## Limits`; `authenticity`; `working tree`. L1 runs `python3 corpus/evidence/round65/c2-count.py` after integration; this seat ran no counter.
6. Entry claim 1's sentence "The receipt validator requests type `blob` at the caller's full revision plus repository-relative path" concerns tools/receipt-pin.py — outside this seat's three sources; not verified here.

## Touched surfaces

Writes (seat-owned only): this file; identical `.ufo/waves/round-65/w1/SourcesDraft/report.md`; verbatim command outputs at `.ufo/waves/round-65/w1/SourcesDraft/evidence.md`. Nothing else in the lane or fleet tree was created, modified, or deleted. Scratch /fast/scratch/hyaku/chousa-r65/SourcesDraft/ (explicit TMPDIR) created for command cwd and deleted before yield. No /tmp evidence. No installs (none needed).

## Out of scope

S157 row/quote (ref-receipt-pin.py docstring) present in drafts but not this seat's assignment — untouched. No c1-count.py/c2-count.py execution, no fixtures, no probes, no battery, no registry append, no fetch, no pacman transactions (read-only `-Q`/`-Qo` queries only).
