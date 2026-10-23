# AttackRowS057 — source row S057 (RFC 5147) and its quote

Seat `ChousaR31.AttackRowS057`, falsify wave 2, round 31. Target: `corpus/SOURCES.md:67` (S057) and the ≤25-word quote attributed to it.

**Verdict:** the row holds. The quote is verbatim in the opened bytes (24 words), the served bytes hash to the value the row records, and `tools/quote-reopen.py verify` returns `VERBATIM` (exit 0). No factual correction to scope/anchor/tier is required. Two provenance defects were found outside the row's cells (F1, F2).

## Commands and receipts

All artifacts are in `.ufo/waves/round-31/falsify/AttackRowS057/`. One GET of the one named URL, no redirect followed:

```
timeout 120 curl --proto '=https' --connect-timeout 15 --max-time 90 --max-redirs 0 \
  --silent --show-error --dump-header headers.txt --output rfc5147.txt \
  --write-out 'HTTP_STATUS=%{http_code}\nSIZE_DOWNLOAD=%{size_download}\n...' \
  https://www.rfc-editor.org/rfc/rfc5147.txt
```
- Exit 0. `HTTP_STATUS=200`, `SIZE_DOWNLOAD=37422`, `CONTENT_TYPE=text/plain;charset=utf-8`, `NUM_REDIRECTS=0`, `URL_EFFECTIVE` = the same URL. Response `date: Fri, 23 Oct 2026 04:47:31 GMT`.
- SHA-256 of `rfc5147.txt` = `c8fff6f21a8c68a15642d00ff0fbb97ae7cd1613ee02c2782ab7671d6b6a24f4` (exactly `c8fff6f2…24f4` in the row's anchor cell).
- `cmp` against the L1's copy `/fast/scratch/hyaku/chousa-r31/rfc5147.txt` (also 37422 bytes, same SHA-256): identical. The L1 copy was only read for this comparison.

Tool run (lane root, default registry, receipt saved):

```
timeout 300 python3 tools/quote-reopen.py verify \
  --items .ufo/waves/round-31/falsify/AttackRowS057/items-s057.tsv
QUOTE_REOPEN	quote-s057	VERBATIM	matched in normalized page text
QUOTE_REOPEN_SUMMARY verbatim=1 absent=0 too_long=0 no_source=0 unreachable=0
```
Exit 0. Item file bytes: `quote-s057<TAB>S057<TAB><quote>` under the tool's `id source_id quote` header.
Local matcher control on the saved bytes (no network; `quote-reopen`'s own `norm`/`found`): exact quote true; `first`→`second` false; final `zero`→`one` false; one word dropped false — the match is not a loose containment artifact.

## Verbatim check

| Item | Value |
|---|---|
| Quote | "Line position counting starts with zero, so the line position before the first line of a text/plain MIME entity has the line position zero" |
| Words | 24 (≤25; tool's own count agrees) |
| Location | raw bytes 17678–17822 (144 bytes), source lines 413–415, inside §2.2.3 |
| Charset | ASCII only (no non-ASCII code point in the span; no soft hyphen) |
| Occurrences (whitespace-folded) | 1 |
| Byte context before | `…consisting of a number of lines.  ` |
| Byte context after | `, and a MIME entity containing n distinct lines has n+1 distinct line positions…` |

The span is a verbatim prefix of the §2.2.3 sentence, folded only across line breaks (`with`/`zero`, `MIME`/`entity`); there is no hyphenation to unfold. The omitted continuation adds the n+1-positions rule and does not reverse or qualify the quoted clause.

Section headings are exact: `2.2.3.  Line Position` at raw line 407 and `2.2.4.  Line Range` at raw line 419. The RFC title at line 14 is `URI Fragment Identifiers for the text/plain Media Type`, matching the `source` cell.

## Row-cell review (`corpus/SOURCES.md:67`, NF=13)

| Cell | Finding |
|---|---|
| source | Matches the RFC title and the opened `.txt` URL. |
| kind / tier | `spec` / `A`: the header reads `Category: Standards Track`, April 2008, `Updates: 2046`; a primary IETF standards-track spec for this scope. Tier justified. |
| scope | Supported: abstract says fragments refer to parts "by line position or range"; §2.2.3 defines a position as a "fragment of length zero between two lines" and says counting starts with zero. The negative clauses (gate `at=`, claims syntax, meaning) are disclaimers, not source claims. |
| anchor | Both sections exist with those titles; the recorded (truncated) hash reproduces from my independent GET. |
| teaches | Clause 2 (`counts line positions from zero between lines`) is page-grounded (§2.2.3, §2.1.2). Clause 1 and clause 3 are lane inferences: "citation" appears 0 times in the RFC (it says fragment identifiers / "refer to parts"), and "must be stated" is a lane norm. *Wording suggestion only:* "A URI fragment can name a line range, not only a whole file." No factual error. |
| status / opened / recheck / used-by | `mined`, 2026-10-23 (my GET is the same date), `365d`, and `corpus/knowledge/line-binding-r31.md` exists and cites S057 at line 3. Registry shape checks: malformed rows 0; tier/kind/status enums clean; used-by path exists. |

## Provenance defects outside the cells

**F1 — the ScribeSrc draft that the target names contains the opposite of the landed row, and it is in the landed commit.** No file under `.ufo/waves/round-31/build/ScribeSrc*/drafts.md` contains this quote. `ScribeSrcRFC5147/drafts.md` (tracked at tip; `git ls-files` confirms) records a GET of the extension-less URL returning HTTP 301 with a 0-byte body, states "no quote … is available", and drafts S057 as tier C / `rejected`. The landed row is tier A / `mined`. `corpus/lessons/round-31.md:57-59` explains the switch (same host, L1 opened the `.txt` directly), so the row's substance is not undermined, but a later reader of the landed build artifact sees a contradiction the row does not mention.

**F2 — the quote record the knowledge entry points to is not in the landed revision.** `corpus/knowledge/line-binding-r31.md:4` (committed at tip) says the located quote is in `corpus/lessons/round-31.md` `## Gate`. At HEAD `ee1024fd…`, `git show ee1024f:corpus/lessons/round-31.md` exits 128 (path not in the commit), and `git ls-files --error-unmatch corpus/lessons/round-31.md` fails (untracked); the working-tree file, mtime 2026-10-23 01:47:46 -0300, is newer than the tip commit time 01:45:09 -0300. The working-tree `## Gate` row 53 does carry the quote verbatim with URL, access date and section, satisfying SOURCES contract rule 1 once committed. At the landed revision the pointer dangles. The quote is still present in the committed knowledge entry itself (line 22) and in my independent GET, so the row's evidence is not lost — the record-of-record is.

## Limits

- I did not request `https://www.rfc-editor.org/rfc/rfc5147` (out of the item's one-URL bound), so the 301/0-byte claim in the draft and lesson is reported as written, not re-observed here.
- The anchor cell's hash is truncated; only my GET binds the full 64-hex digest, and only for the bytes served on 2026-10-23.
- One `.txt` GET plus the tool's own GET of the same registry URL; no other host, no redirect, nothing installed.
- The lesson file may be committed after this snapshot; F2 is a statement about HEAD `ee1024f` at 2026-10-23 04:48Z.
- The local matcher control loaded `tools/quote-reopen.py` in-process (no network); no `tools/__pycache__` directory exists under `tools/` now, and `git status` shows no modification under `tools/`.
