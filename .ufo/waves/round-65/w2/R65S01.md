# R65S01 — scout: re-open source S154 (installed git-cat-file(1))

Seat: R65S01 (scout). Lane: chousa, round 65, wave w2 (falsify).
Scope of attack: source S154 only — the installed man page
`/usr/share/man/man1/git-cat-file.1.gz` — re-opened from scratch, independent of any
sibling draft. Nothing in the lane was edited; all git calls read-only with explicit `-C`.

No tool was installed (no `uv tool install`, no `npx`, no binary in `~/.local/bin`); no pacman
transaction. Only preinstalled tools were used: `zcat`, `sha256sum`, `grep`, `groff`/`man`,
`python3` (3.14.8), `git` 2.56.0.

Scratch used: `/fast/scratch/hyaku/chousa-r65/w2/R65S01/` (decompressed page, rendered page,
`items.tsv`, a throwaway copy of the lane's `c2-count.py` + entry for the counter-sensitivity
probe). Deleted before this report was finalised. No `/tmp` evidence was used.

---

## 1. Headline answer

| Question asked | Answer |
|---|---|
| Exact quoted words, as the page prints them | `If <type> is specified, the raw (though uncompressed) contents of the <object> will be returned.` |
| Where I found them | decompressed roff line **505**, inside `.SH "OUTPUT"` (line **495**), before `.SH "BATCH OUTPUT"` (line **506**); rendered (`MANWIDTH=1000 man -l … \| col -bx`) line **159**, `OUTPUT` heading at rendered line **150** |
| Git version the page carries | **Git 2.56.0** (`.TH` line: `.TH "GIT\-CAT\-FILE" "1" "2026\-09\-27" "Git 2\&.56\&.0" "Git Manual"`; header `Source: Git 2.56.0`), page **Date 2026-09-27**; the installed binary agrees: `git version 2.56.0` |
| sha256 of the `.gz` vs `source-openings.json` row S154 | **MATCH** — both `8eb0bb079fa0cdf682920d0327fc1e72d5704961c9c54cdc716909251efd5737` |

**But the corpus does not quote those words.** Three landed files carry a *misquote* of this
sentence (the literal `<object>` placeholder is dropped while `<type>` is kept verbatim in the
same sentence), and the misquote was already found in wave 1 with an explicit fix instruction
that was never applied. Details and evidence in §3–§6.

---

## 2. Re-open commands and outputs (verbatim)

### 2.1 Digest of the `.gz` and the recorded pin

```
$ sha256sum /usr/share/man/man1/git-cat-file.1.gz
8eb0bb079fa0cdf682920d0327fc1e72d5704961c9c54cdc716909251efd5737  /usr/share/man/man1/git-cat-file.1.gz
$ stat -c '%n mtime=%y size=%s' /usr/share/man/man1/git-cat-file.1.gz
/usr/share/man/man1/git-cat-file.1.gz mtime=2026-09-28 14:57:26.000000000 -0300 size=5996
```

Recorded pin, `corpus/evidence/round65/source-openings.json:2-9`:

```json
  {
    "id": "S154",
    "path": "/usr/share/man/man1/git-cat-file.1.gz",
    "accessed": "2026-10-30",
    "sha256": "8eb0bb079fa0cdf682920d0327fc1e72d5704961c9c54cdc716909251efd5737",
    "location": "OUTPUT",
    "quote": "If <type> is specified, the raw (though uncompressed) contents of the object will be returned."
  },
```

**Verdict: digest MATCH** (byte-identical, 64 hex chars, same file path).
The same pin also sits in the committed tip — read-only:

```
$ git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show 9672a2e998bff2b51d18b0df4d835bd3ae2c453f:corpus/evidence/round65/source-openings.json
  {
    "id": "S154",
    ...
    "sha256": "8eb0bb079fa0cdf682920d0327fc1e72d5704961c9c54cdc716909251efd5737",
```

### 2.2 The page's version and date (decompressed source)

```
$ zcat /usr/share/man/man1/git-cat-file.1.gz > git-cat-file.1     # 728 lines, 20113 bytes
$ grep -n -F 'Source: Git' git-cat-file.1
7:.\"    Source: Git 2.56.0
$ grep -n -F 'TH "GIT' git-cat-file.1
10:.TH "GIT\-CAT\-FILE" "1" "2026\-09\-27" "Git 2\&.56\&.0" "Git Manual"
$ grep -n -F 'Date: 2026-09-27' git-cat-file.1
5:.\"      Date: 2026-09-27
$ git --version
git version 2.56.0
```

Digest of the decompressed member (not pinned anywhere in the corpus — offered so a re-checker
can confirm it opened the same bytes): `10faee626e8414f042a8f29c76a657f5319d7bfd66b4d8808afe1b33d582c3e7  git-cat-file.1`.

Only one installed copy of this page exists, and it is the one `man` resolves:

```
$ man -w git-cat-file
/usr/share/man/man1/git-cat-file.1.gz
$ ls /usr/share/man/**/git-cat-file*
/usr/share/man/man1/git-cat-file.1.gz
```

### 2.3 Locating the OUTPUT sentence

Roff source (line numbers of the decompressed member):

```
$ grep -n -E '^\.SH|uncompressed' git-cat-file.1
495:.SH "OUTPUT"
505:If \fI<type>\fR is specified, the raw (though uncompressed) contents of the \fI<object>\fR will be returned\&.
506:.SH "BATCH OUTPUT"
```

Rendered page:

```
$ MANWIDTH=1000 man -l /usr/share/man/man1/git-cat-file.1.gz | col -bx > man1000.txt
$ grep -n -x 'OUTPUT' man1000.txt
150:OUTPUT
$ grep -n -F 'If <type> is specified' man1000.txt
159:     If <type> is specified, the raw (though uncompressed) contents of the <object> will be returned.
```

Full OUTPUT section, rendered (lines 244–255), for the record:

```
244:OUTPUT
…
251:     If -p is specified, the contents of <object> are pretty-printed.
252:
253:     If  <type> is specified, the raw (though uncompressed) contents of the <ob‐
254:     ject> will be returned.
255:
256:BATCH OUTPUT
```

Note for re-checkers: at the default 80-column width groff hyphenates the placeholder across the
line break (`the <ob‐` / `ject>`), so the sentence is byte-contiguous **only** at the
`MANWIDTH=1000` rendering the sibling registry rows prescribe. At default width the same
sentence is split, and a naive `grep -F` on the default-width page would not match the quoted
string.

### 2.4 The corpus form is not a substring of the source

```
$ grep -c -F 'contents of the object will be returned'        man1000.txt
0
$ grep -c -F 'contents of the <object> will be returned'      man1000.txt
1
$ grep -c -F 'contents of the object will be returned'        git-cat-file.1
0
$ grep -c -F 'contents of the \fI<object>\fR will be returned' git-cat-file.1
1
```

So the string the corpus quotes (`…contents of the object will be returned.`) occurs **zero
times** in either the rendered page or the roff source, while the page's own string occurs
exactly once in each. The corpus kept `<type>` verbatim in the same sentence and silently
de-marked `<object>` — asymmetric, so not a house rendering convention.

---

## 3. Finding 1 (severity: action-needed) — the landed corpus misquotes S154

**What it attacks:** `corpus/evidence/round65/source-openings.json:8`,
`corpus/knowledge/receipt-identity-r65.md:9`, `corpus/lessons/round-65.md:12`.

All three carry

> `If <type> is specified, the raw (though uncompressed) contents of the object will be returned.`

instead of the page's `…contents of the <object> will be returned.` (`<object>` is the man
page's placeholder designator, printed in italics as `\fI<object>\fR`).

Byte-level confirmation of the corpus form (ASCII `<`, no full-width brackets):

```
$ python3 - <<'PY'   # over the three landed files
source-openings.json | ascii-lt: 1 non-ascii-brackets: 0 | If <type> is specified, the raw (though uncompressed) contents of the object will be returned."
entry               | ascii-lt: 1 non-ascii-brackets: 0 | If <type> is specified, the raw (though uncompressed) contents of the object will be returned.” The receipt validator re
lesson              | ascii-lt: 1 non-ascii-brackets: 0 | If <type> is specified, the raw (though uncompressed) contents of the object will be returned.` | A for object-content output only |
SOURCES row has literal quote text? False
```

Two precisions about the w1 wording, so the L1 fixes the right files:

* The **landed `corpus/SOURCES.md:164` row S154 contains no quoted sentence at all** — its anchor
  cell is the paraphrase `OUTPUT paragraph on explicit type, Git 2.56.0 manual dated 2026-09-27`.
  So the w1 finding's phrase "SOURCES.md S154 row" over-states the landed damage for SOURCES.md
  (it was true of the w1 *draft* row). The misquote is in the three files named above.
* The lesson row also carries the S155 mis-adjacent string
  `Return the digest of the bytes passed to the update() method` (`corpus/lessons/round-65.md:13`)
  — out of my scope (S155 belongs to R65S02); flagged only so the L1 does not fix S154 alone and
  leave the neighbouring row inconsistent.

**Materiality:** the misquote does not change the sentence's meaning for a reader who already
knows the page — but it is the corpus's *only* record of what a quoted page says, it is not
verbatim (contradicting the lane's own Gate-quote rule, `corpus/QUALITY.md:211-216` "**A Gate
quote is verbatim before admission**"), and it is the kind of silent de-markup that a later
reader cannot detect without re-opening the source. `corpus/lessons/round-65.md:12` presents the
string in a Gate row as the located quote for S154.

**Fix (L1):** replace `contents of the object will be returned` with
`contents of the <object> will be returned` in the three files above. Both forms are 15 words,
so the ≤25-word Gate-quote limit is unaffected.

---

## 4. Finding 2 (severity: action-needed) — the wave-1 finding existed, named the fix, and was not applied

**What it attacks:** the L1 integration commit `0a85189821322e01db06216b5cb82d2d858c19f0`
("round-65: receipt-pin validator, sourced receipt-identity entry, inherited wave-1 evidence").

Wave 1 already found this, in the seat's own results file
`.ufo/waves/round-65/w1-results.json:262` (SourcesDraft seat):

```
{
  "severity": "action-needed",
  "id": "S154-misquote",
  "detail": "All four drafted instances (source-openings.json, SOURCES.md S154 row, receipt-identity-r65.md claim 1, round-65.md Gate row) read 'contents of the object will be returned' but rendered source line 159 reads 'contents of the <object> will be returned' — silent placeholder replacement while <type> is kept verbatim in the same sentence. Word count 15 either way (<=25 limit unaffected). Fix: restore verbatim '<object>' at L1 integration."
}
```

The wave-1 EntryDraft even carried the **correct** form in its own quote table
(`.ufo/waves/round-65/w1/EntryDraft/receipt-identity-r65.md:13`:
`Q3 | S154 rendered line159 (OUTPUT) | If <type> is specified, the raw (though uncompressed) contents of the <object> will be returned.`)
and a Limits bullet recording the delta (same file, line 35:
`Transcription delta: round65/source-openings.json registers Q3 as "contents of the object will be returned", dropping the literal <object> token …`).

Neither survived integration. The landed entry carries the misquoted form at line 9 and its
Limits section no longer mentions the delta (landed entry `## Limits` has three paragraphs; none
of them records it). Confirmed at the current tip, read-only:

```
$ git -C … show HEAD:corpus/knowledge/receipt-identity-r65.md | grep -n 'uncompressed'
9:1. S154's installed manual says under OUTPUT: “If <type> is specified, the raw (though uncompressed) contents of the object will be returned.” …
$ git -C … show HEAD:corpus/lessons/round-65.md | grep -n 'uncompressed'
12:| S154 | file:///usr/share/man/man1/git-cat-file.1.gz | Git2.56.0 manual dated2026-09-27, OUTPUT: `If <type> is specified, the raw (though uncompressed) contents of the object will be returned.` | A for object-content output only |
$ git -C … rev-parse HEAD
a6b6f9396a825558edd1fdddaa2b43cb5f0a6bfe
```

So the round landed with a defect that wave 1 had already named, with the correct wording
already drafted, and with the fix instruction "restore verbatim '<object>' at L1 integration"
sitting unapplied in the wave's own results file. **This is a process finding for L1, not just a
text fix:** the wave-1 findings list was not carried into integration for S154.

---

## 5. Finding 3 (severity: note → action-needed for the L1) — no machine check covers this quote

Two independent gaps let the misquote through:

**(a) The corpus's own verbatim-quote gate cannot see local-file sources.**
`corpus/QUALITY.md:211-216` (criterion 30) requires every new Gate quote to be re-opened with
`python3 tools/quote-reopen.py verify --items <tsv>` and admitted only on `VERBATIM`. I ran that
tool against S154 (read-only; it only reads the registry and would fetch only http(s) URLs):

```
$ python3 tools/quote-reopen.py verify --items items.tsv --registry corpus/SOURCES.md
QUOTE_REOPEN	S154q1	NO_SOURCE	registry row S154 has no http(s) URL
QUOTE_REOPEN	S154q2	NO_SOURCE	registry row S154 has no http(s) URL
QUOTE_REOPEN_SUMMARY verbatim=0 absent=0 too_long=0 no_source=2 unreachable=0
exit=1
```

`tools/quote-reopen.py:194-201` extracts only the first `http(s)` URL of the registry source
cell, and `tools/quote-reopen.py:506-507` reports `NO_SOURCE` when there is none. S154's source
cell is a local path, so the criterion-30 gate returns `NO_SOURCE`, never `VERBATIM` — the
machine check that is supposed to protect Gate quotes is structurally unavailable for every
installed-man-page / installed-module row. (Both quote forms were submitted: the corpus form and
the page's own form; neither can be adjudicated by this tool.)

**(b) The frozen C2 counter is quote-blind.** Proven on a throwaway copy in scratch (the lane's
frozen `c2-count.py` was copied, never edited; the lane tree was not modified):

```
$ python3 <scratch>/lane/corpus/evidence/round65/c2-count.py     # unmodified copy, live entry
ENTRY_CHECKS=10/10 C2=PASS
exit=0
$ # then, in the copy only, replace the quoted sentence with nonsense:
$ python3 <scratch>/lane/corpus/evidence/round65/c2-count.py
ENTRY_CHECKS=10/10 C2=PASS
exit=0
```

`corpus/evidence/round65/c2-count.py:8` checks presence of `S154`/`S155`/`S156`, the two
headings, the words `authenticity` and `working tree`, the SOURCES rows and the README index
line — never the quoted bytes. Restoring the correct `<object>` in the scratch copy also stayed
`ENTRY_CHECKS=10/10 C2=PASS` (no frozen-counter conflict with the fix).

Consequence for L1: **nothing in the landed pipeline can detect this class of defect.** The
defect was caught only by a human/agent re-opening the page — which is what this seat did, and
which the corpus's own "An outside reviewer must still re-open the source and check the claim
against it" (`corpus/knowledge/receipt-identity-r65.md`, `## Use in research`) demands. A
successor round could consider a local-file quote-reopen path (the tool already refuses cleanly
with `NO_SOURCE`, so the refusal is loud, not silent).

---

## 6. Finding 4 (severity: note) — S154's registry row is thinner than its man-page siblings

**What it attacks:** `corpus/SOURCES.md:164`.

Landed row S154 (verbatim, `| ` cells split):

```
S154 | git-cat-file(1) — installed /usr/share/man/man1/git-cat-file.1.gz | docs | A |
raw blob contents at a selected Git object expression, not execution authenticity |
OUTPUT paragraph on explicit type, Git 2.56.0 manual dated 2026-09-27 |
explicitly requesting blob contents selects repository object bytes rather than working-tree bytes |
mined | 2026-10-30 | on-release | corpus/knowledge/receipt-identity-r65.md
```

Compare the sibling man-page rows the same registry already holds (S142 at `corpus/SOURCES.md:152`,
S145 at `:155`, S146 at `:156`, S147 at `:157`): they all name the owning package and the
rendering method in the `source` cell, e.g. S142 —

```
git-rev-parse(1) — Git 2.56.0 manual page (the page's own date 2026-09-27), the installed
/usr/share/man/man1/git-rev-parse.1.gz of the Arch package git 2.56.0-1, rendered with
MANWIDTH=1000 man -l FILE then col -bx
```

and S146's `anchor` cell gives a rendered line number (`rendered line 29, the -F option text,
grep 3.12-modified page`). S154's row gives **no package owner, no render method, and no
rendered line number**, so a re-checker cannot reproduce the anchor exactly from the row alone
(it must know to use `MANWIDTH=1000 … | col -bx` — the very detail that makes the quote
byte-contiguous, §2.3). The row also quotes nothing, so §3's misquote cannot be caught from the
row itself; the row's `location` cell `OUTPUT` is correct but coarse (the sentence is the fifth
paragraph of OUTPUT, roff 505 / rendered 159). Suggested `anchor` upgrade, matching sibling
rows: `rendered line 159 (MANWIDTH=1000 man -l FILE | col -bx), the OUTPUT paragraph on an
explicit <type>, git 2.56.0 page dated 2026-09-27`.

Note: `pacman -Qo` was **not** run to establish the owning package (pacman is paused host-wide),
so the package-owner claim above is taken from the sibling rows' own wording, not re-verified
here. The page's own version and date are verified from its bytes (§2.2).

---

## 7. Finding 5 (severity: note) — the S154 anchor is narrower than the S154 `teaches` cell

`corpus/SOURCES.md:164` `teaches`: *"explicitly requesting blob contents selects repository
object bytes rather than working-tree bytes"*, anchored to *"OUTPUT paragraph on explicit type"*.

The OUTPUT section (roff 495–505) says nothing about working-tree bytes. The working-tree
contrast is introduced by the OPTIONS entry for `--filters` (roff 121–127; rendered 49–50):

```
--filters
   Show the content as converted by the filters configured in the current working tree for the
   given <path> (i.e. smudge filters, end-of-line conversion, etc). In this case, <object> has
   to be of the form <tree-ish>:<path>, or :<path>.
```

i.e. working-tree conversion is what `--filters` turns *on*; without it `cat-file` returns the
object's stored bytes. The behaviour the validator actually relies on
`tools/receipt-pin.py:55`, `git … cat-file blob REVISION:PATH`, no `--filters`) is therefore
grounded at OPTIONS `--filters`, not at the OUTPUT paragraph the row cites. The knowledge entry
`corpus/knowledge/receipt-identity-r65.md:9` marks its version of this as "Inference:", which is
honest labelling; the registry row's `teaches` cell, however, presents the contrast as what the
cited anchor says. Recommendation: cite both locations, or cite OPTIONS `--filters` for the
working-tree half.

---

## 8. Finding 6 (severity: note) — lesson-cell typography, round-65 only

`corpus/lessons/round-65.md:12` reads `Git2.56.0 manual dated2026-09-27` and line 13 reads
`Python3.14.8 module documentation31–32` — words run together where the version/date/line-number
should be separated. This style occurs nowhere else in `corpus/lessons/` (the comparable
round-64 rows are properly spaced, e.g. `corpus/lessons/round-64.md:15`: `file:///usr/share/man/man1/realpath.1.gz, GNU coreutils 9.12, DESCRIPTION -e --canonicalize-existing …`):

```
$ grep -rn -E 'Git2\.|Python3\.14|dated20' corpus/lessons/*.md
corpus/lessons/round-65.md:12:| S154 | file:///usr/share/man/man1/git-cat-file.1.gz | Git2.56.0 manual dated2026-09-27, OUTPUT: …
corpus/lessons/round-65.md:13:| S155 | file:///usr/lib/python3.14/hashlib.py | Python3.14.8 module documentation31–32: …
```

Cosmetic, but it is a Gate table, and the missing spaces read as transcription damage of the
same class as the `<object>` loss.

---

## 9. What I verified as correct (so the L1 does not re-open what is sound)

* **Digest.** `sha256sum /usr/share/man/man1/git-cat-file.1.gz` = `8eb0bb07…5737` = the pin in
  `corpus/evidence/round65/source-openings.json:6`, and = the same value in the committed
  `9672a2e` version of that file. MATCH.
* **Version/date.** Page carries Git 2.56.0, dated 2026-09-27 (`Source: Git 2.56.0`, `.TH`
  `"Git 2.56.0"`, `Date: 2026-09-27`); installed binary `git version 2.56.0`. The row's
  `Git 2.56.0 manual dated 2026-09-27` is accurate.
* **Section placement.** The sentence is in OUTPUT (roff 495–505), the only place it occurs;
  `location: "OUTPUT"` in `source-openings.json:7` is correct.
* **Single installed page.** `man -w git-cat-file` → `/usr/share/man/man1/git-cat-file.1.gz`,
  the only `git-cat-file*` under `/usr/share/man` — no ambiguity about which page is installed.
* **Entry claim 1's factual half.** "The receipt validator requests type `blob` at the caller's
  full revision plus repository-relative path" is accurate against the landed tool:
  `tools/receipt-pin.py:55` runs
  `["git", "-C", a.root, "cat-file", "blob", a.revision + ":" + m.group(2)]`, `--revision` is
  validated as a full lowercase 40-hex id (`tools/receipt-pin.py:34-36`), and the path is forced
  canonical and repository-relative (`tools/receipt-pin.py:47-48`).
* **Counter compatibility of the fix.** Restoring `<object>` in the entry leaves the frozen
  counter at `ENTRY_CHECKS=10/10 C2=PASS` (verified on the scratch copy), so the fix requires no
  counter change and no frozen-file edit.

---

## 10. Exact commands used (for reproduction)

```bash
S=/fast/scratch/hyaku/chousa-r65/w2/R65S01; mkdir -p "$S"; cd "$S"
zcat /usr/share/man/man1/git-cat-file.1.gz > git-cat-file.1
sha256sum /usr/share/man/man1/git-cat-file.1.gz; stat -c '%n mtime=%y size=%s' /usr/share/man/man1/git-cat-file.1.gz
git --version; man -w git-cat-file
grep -n -E '^\.SH|uncompressed|filters|Source: Git|Date: 2026|TH "GIT' git-cat-file.1
MANWIDTH=1000 man -l /usr/share/man/man1/git-cat-file.1.gz | col -bx > man1000.txt
grep -n -x 'OUTPUT' man1000.txt; grep -n -F 'If <type> is specified' man1000.txt
grep -c -F 'contents of the object will be returned' man1000.txt git-cat-file.1
grep -c -F 'contents of the <object> will be returned' man1000.txt
sha256sum git-cat-file.1
# read-only git, always with explicit -C
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse HEAD
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show 9672a2e998bff2b51d18b0df4d835bd3ae2c453f:corpus/evidence/round65/source-openings.json
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show HEAD:corpus/knowledge/receipt-identity-r65.md | grep -n uncompressed
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show HEAD:corpus/lessons/round-65.md | grep -n uncompressed
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin status --porcelain -- corpus/knowledge/receipt-identity-r65.md corpus/lessons/round-65.md corpus/evidence/round65/source-openings.json corpus/SOURCES.md   # empty: no drift, all four are committed
```

No fixture repository was needed (no git object was created or mutated); no `git commit`/`jj`/
`fetch`/`push` was run anywhere.

---

## 11. Summary table for L1

| # | Finding | Severity | Files/Lines | One-line fix |
|---|---|---|---|---|
| 1 | S154 quote misquotes the page (`the object` for `the <object>`) | action-needed | `corpus/evidence/round65/source-openings.json:8`; `corpus/knowledge/receipt-identity-r65.md:9`; `corpus/lessons/round-65.md:12` | restore `contents of the <object> will be returned` (15 words, ≤25 limit unaffected) |
| 2 | Wave-1 `S154-misquote` finding (w1-results.json:262, "action-needed", "Fix: restore verbatim '<object>' at L1 integration") was not applied at integration `0a85189`; w1's correct quote (EntryDraft:13) and its delta Limit (EntryDraft:35) were both dropped | action-needed (process) | `.ufo/waves/round-65/w1-results.json:262`; `.ufo/waves/round-65/w1/EntryDraft/receipt-identity-r65.md:13,35` | apply §3 fix and carry the wave-1 findings list into integration for S154–S157 |
| 3 | No machine check covers local-file Gate quotes: `quote-reopen.py` returns `NO_SOURCE` for S154 (no http(s) URL); frozen `c2-count.py` scores `10/10` with the quote replaced by nonsense | action-needed (coverage) | `tools/quote-reopen.py:194-201,506-507`; `corpus/evidence/round65/c2-count.py:8`; `corpus/QUALITY.md:211-216` | successor round: local-file quote re-open path (tool already refuses loudly) |
| 4 | S154 registry row omits package owner, render method and rendered line that sibling man-page rows carry | note | `corpus/SOURCES.md:164` vs `:154-157` | extend `source`/`anchor` cells: `rendered line 159 (MANWIDTH=1000 man -l FILE \| col -bx)` |
| 5 | S154 `teaches` cell (repository vs working-tree bytes) is anchored to OUTPUT, but the working-tree contrast lives in OPTIONS `--filters` (roff 121–127) | note | `corpus/SOURCES.md:164`; `tools/receipt-pin.py:54-57` | cite OPTIONS `--filters` for the working-tree half |
| 6 | Lesson Gate cells run words together (`Git2.56.0`, `dated2026-09-27`, `documentation31–32`) — round-65-only style | note | `corpus/lessons/round-65.md:12-13` | insert the spaces |
| — | Digest, page version/date, OUTPUT placement, single installed page, and claim 1's factual half about the validator: **verified sound** | — | §9 | none |

**Confidence:** high on the digest, the version/date, the exact quoted words and their
locations (all read from the installed bytes in this session, byte-compared with `grep -c` and
`grep -n`); high on the misquote (three landed files, zero substring hits in the source); high
on the "already found in wave 1, not applied" claim (both texts quoted from the lane's own
files, verified present at HEAD by read-only `git show`).

**Remaining unknowns (not resolved by this seat):** whether the L1 deliberately chose the
`<object>`-less form (no such rationale appears anywhere in the lane's wave-1 results, the
w1 EntryDraft, or the landed lesson); and whether the analogous S155/S156/S157 rows carry the
same defect (S155 belongs to R65S02, S156 to R65S03, S157 to another seat — I read them only
far enough to notice the lesson-cell spacing defect in §8, and did not adjudicate their quotes).
