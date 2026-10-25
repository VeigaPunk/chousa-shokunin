# ScribeErratum — round 43, wave 1

Seat: chousa leaf scribe. Milestone: Round 43 absent-class split and one local adoption.
Assigned item only: quote the erratum in `corpus/lessons/round-42.md` and confirm the earlier `265-char` sentence is still present and was not rewritten.
Measured commit: `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`. Lane HEAD at inspection equals that commit.
No production file, index, jj state, fleet repo, sibling repo, or `/home/vgpnk/Projects/shokuknow` path was written. No network. No tool install. Pacman was not run.

## Axes

1. Operability — the erratum section is locatable at the measured commit and quotable verbatim.
2. Calibration — `265-char` is not `265-character`; a second occurrence inside the erratum is a quotation, not a rewrite; unrun counters and a sibling seat's byte count are not execution evidence.
3. Depth — rewrite is decided by byte-prefix identity of the pre-erratum blob, not by reading the erratum's own claim that the sentences above were not rewritten.

## Behavior

Read-only. The lesson was read from the worktree and compared with `git show` of the only earlier commit that contains the file. The worktree copy of `corpus/lessons/round-42.md` is byte-identical to the measured commit. The only file this seat writes is this report.

## Erratum section (quoted)

Source: `corpus/lessons/round-42.md` lines 151–153 at blob `a59ce1ba6d38004c840ed29fcfeddd6b92e2f1a9` (measured commit). The heading dash is U+2014, observed in the appended-byte repr as `\xe2\x80\x94`.

~~~~
## Erratum — 2026-10-24, round 43 (append-only; the sentences above are not rewritten)

The S077 capture `.qcache/01f657b3d0ab045c494b3f92.txt` is 267 bytes and 265 Unicode characters. The "265-char" wording above matches the decoded length. The spot-check's "267 bytes" matches `wc -c`. Neither number corrects the other. A later reader should cite both.
~~~~

## Earlier 265-char sentence

Confirmed present, and not rewritten.

The exact token `265-char` (not the longer word `265-character`) occurs once above the erratum, on line 81, inside the provenance-class evidence cell. The sentence in that cell is:

~~~~
S077: the campaign's class cell reads `payload-absent` ("every relevant source fetched cleanly") while the local capture of that DOI is a 265-char `Client Challenge` page (`tools/quarantine-check.py` `capture_kind`, cache file `01f657b3d0ab045c494b3f92.txt`)
~~~~

That clause, `while the local capture of that DOI is a 265-char `Client Challenge` page`, occurs once in the pre-erratum blob and once in the measured blob. An ASCII hyphen-minus search string matched it (`clause_in_parent True`, `clause_in_head True`).

The whole pre-erratum file is a strict byte prefix of the measured file (`head_startswith_parent True`). `git diff` from `e0f4895c48d6c6e739ce9deb614b97c771a3a096` to the measured commit is 4 insertions and 0 deletions, and the hunk is only the erratum append. Line 81 is blamed to `e0f4895` (author date 2026-10-24 20:19:22 -0300). The erratum lines 150–153 are blamed to `737f40b`. Nothing above the append was edited, reflowed, or replaced.

A nearby sentence is a different wording and was also left untouched, because it sits in the same unchanged prefix. Lines 72–73 say `S077's capture of the DOI is a 265-character bot-challenge page`. That is not the `265-char` sentence. `git log -S '265-character'` names only `e0f4895`. A substring search for `265-char` false-hits `265-character`; the exact-token count below does not.

The erratum's own line 153 contains a second `265-char` token, in quotation marks, referring to the wording above. `git log -S '265-char'` therefore names both commits. That second hit is the append, not a rewrite of line 81. Exact-token count: 1 in the parent, 2 at HEAD (line 81 unchanged, line 153 added).

## Gates

| Gate | Result | Basis |
|---|---|---|
| Erratum quoted from the measured commit | HOLD | Lines 151–153 match the sole added hunk and the appended-byte repr. |
| Earlier `265-char` sentence still present | HOLD | Line 81 exact token count 1 above the erratum; clause count 1. |
| That sentence was not rewritten | HOLD | Measured file startswith the pre-erratum bytes; diff is `4 0`; line 81 blame is `e0f4895`. |
| Round C1 / C2 / C3 counting commands | NOT RUN | Not this item. Not scored here. |

## Touched surfaces

- Written: `.ufo/waves/round-43/w1/ScribeErratum.md` (this file).
- Read: `corpus/lessons/round-42.md`, its git history, `corpus/lessons/round-42-verifier-spotcheck.md` (spot lines only), `corpus/lessons/round-43.md` (mistake row only, not adopted as measurement), `corpus/evidence/round43/claims.md` (base pin), `.ufo/waves/round-43/assimilation/validate/corpus/lessons/round-42.md` (hash and diff only), `.ufo/waves/round-43/w1/ExecBotWallBytes.md` (seen; not adopted).
- Not modified: lane production files, git index, jj state, fleet repo, sibling repos, `/home/vgpnk/Projects/shokuknow`.

## Out of scope

- `python3 corpus/evidence/round43/c1-count.py`, `c2-count.py`, and `c3-count.py` were not run. The lesson's `C1=PASS` / `SPLIT_AGREES=15/15` / `C3=PASS` lines are not this seat's evidence.
- The capture `.qcache/01f657b3d0ab045c494b3f92.txt` was not measured here. The erratum's "267 bytes" and "265 Unicode characters" are quoted, not re-executed. Sibling report `.ufo/waves/round-43/w1/ExecBotWallBytes.md` claims those two figures; this seat does not adopt that report as its own execution evidence.
- `corpus/QUALITY.md` also says `265-character`. Not the assigned sentence.
- The spot-check file is a different document. Its own `265-char` lines (120 and 182) are still present at `15f9f3fbd3c17b2155f718c67cbef0624034cf6d` and `git diff --stat` from that commit to the measured commit is empty (`spotcheck_diff_exit=0`). That is adjacent, not the sentence above the erratum.

## Findings

1. The erratum is an append. Parent content sha256 `6a20a2d41feeea302d26df6b0c82b9a9fbc4fef71c644e6435731409d6dc29db` (11075 bytes, 149 lines, trailing newline). Measured content sha256 `599efe300578bcec828f0e6f35d134ffe1a377b2d7ca3dd2fb3a348564315e6e` (11434 bytes, 153 lines, trailing newline). Worktree sha256 equals the measured content sha256. Git blobs: pre-erratum `1e21181540287ea992c68335a2acaa1bb63f632f`; measured `a59ce1ba6d38004c840ed29fcfeddd6b92e2f1a9`. Appended-bytes sha256 `989e8e73c24bce4552bcd4294f39bb48d0be5b32de5f02ad6d8fc5721358ce2f`.
2. The earlier `265-char` sentence is the line-81 evidence cell, not line 73's `265-character` sentence, and not the erratum's quotation of the token.
3. Conflict, for the L1, not a rewrite of the canonical sentence: the assimilation validate copy is the pre-erratum bytes. Its content sha256 equals the parent (`6a20a2d4…`). `cmp` exit 1. `diff -u` shows only the erratum missing from the mirror. The claims-base commit `15f9f3fbd3c17b2155f718c67cbef0624034cf6d` is an ancestor of the measured commit (`ancestor_exit=0`) and names the same lesson blob as `e0f4895` (`1e211815…`). The canonical lesson at the measured commit is the copy that contains the erratum.

## Conflict verbatim

```
--- .ufo/waves/round-43/assimilation/validate/corpus/lessons/round-42.md	2026-10-24 20:43:32.165966465 -0300
+++ corpus/lessons/round-42.md	2026-10-24 21:14:27.280576110 -0300
@@ -147,3 +147,7 @@
 round appends no staged row, so the collision is a future adoption-time renumbering
 matter (the package's ids shift by one and every adopted citation is re-pointed BY
 DOCUMENT, never by arithmetic).
+
+## Erratum — 2026-10-24, round 43 (append-only; the sentences above are not rewritten)
+
+The S077 capture `.qcache/01f657b3d0ab045c494b3f92.txt` is 267 bytes and 265 Unicode characters. The "265-char" wording above matches the decoded length. The spot-check's "267 bytes" matches `wc -c`. Neither number corrects the other. A later reader should cite both.
diff_exit=1
```

## Commands and outcomes

Working directory: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.

`git rev-parse HEAD`

```
737f40b6aa8f37ffe2269db370fd6d65a720d9a8
```

`git status --porcelain -- corpus/lessons/round-42.md` produced no output. `git diff --exit-code -- corpus/lessons/round-42.md` then `echo "worktree_diff_exit=$?"` produced `worktree_diff_exit=0`. `git diff --stat 737f40b6aa8f37ffe2269db370fd6d65a720d9a8 -- corpus/lessons/round-42.md` produced no output.

`git log --follow --format='%H %ci %s' -- corpus/lessons/round-42.md`

```
737f40b6aa8f37ffe2269db370fd6d65a720d9a8 2026-10-24 21:15:02 -0300 round-43: split the absent class and adopt one locally re-opened search-log entry
e0f4895c48d6c6e739ce9deb614b97c771a3a096 2026-10-24 20:43:37 -0300 round-42: quarantine adjudication of the 24-row register slice (C1 gate + C2 verdicts, lesson, S077)
```

`git log -1 --format='commit %H%nauthor_date %ai%ncommitter_date %ci%nsubject %s' 737f40b6aa8f37ffe2269db370fd6d65a720d9a8`

```
commit 737f40b6aa8f37ffe2269db370fd6d65a720d9a8
author_date 2026-10-24 20:52:23 -0300
committer_date 2026-10-24 21:15:02 -0300
subject round-43: split the absent class and adopt one locally re-opened search-log entry
```

Blame of the sentence (abbreviated hash as printed by `git blame -L 81,81`):

```
e0f4895 (chousa-shokunin 2026-10-24 20:19:22 -0300 81) | provenance-class — a register class that licenses a fabrication verdict is only as good as the capture behind it; "fetched cleanly" can mean "a bot wall was saved" | S077: the campaign's class cell reads `payload-absent` ("every relevant source fetched cleanly") while the local capture of that DOI is a 265-char `Client Challenge` page (`tools/quarantine-check.py` `capture_kind`, cache file `01f657b3d0ab045c494b3f92.txt`) | none — no criterion tied a capture's FORM to the class it licenses | the frozen decision rule's step 2 refuses a bot wall, a binary document and a too-short capture as `unverifiable`; the lane's QUALITY criterion 59 and this lesson are the record |
```

Blame of the erratum (`git blame -L 150,153`):

```
737f40b (chousa-shokunin 2026-10-24 20:52:23 -0300 150) 
737f40b (chousa-shokunin 2026-10-24 20:52:23 -0300 151) ## Erratum — 2026-10-24, round 43 (append-only; the sentences above are not rewritten)
737f40b (chousa-shokunin 2026-10-24 20:52:23 -0300 152) 
737f40b (chousa-shokunin 2026-10-24 20:52:23 -0300 153) The S077 capture `.qcache/01f657b3d0ab045c494b3f92.txt` is 267 bytes and 265 Unicode characters. The "265-char" wording above matches the decoded length. The spot-check's "267 bytes" matches `wc -c`. Neither number corrects the other. A later reader should cite both.
```

`git diff --numstat e0f4895c48d6c6e739ce9deb614b97c771a3a096 737f40b6aa8f37ffe2269db370fd6d65a720d9a8 -- corpus/lessons/round-42.md`

```
4	0	corpus/lessons/round-42.md
```

`git diff -U3` of that same range (the only hunk):

```
diff --git a/corpus/lessons/round-42.md b/corpus/lessons/round-42.md
index 1e21181..a59ce1b 100644
--- a/corpus/lessons/round-42.md
+++ b/corpus/lessons/round-42.md
@@ -147,3 +147,7 @@ parser accepts; the collision is recorded in the round report and in the L0 note
 round appends no staged row, so the collision is a future adoption-time renumbering
 matter (the package's ids shift by one and every adopted citation is re-pointed BY
 DOCUMENT, never by arithmetic).
+
+## Erratum — 2026-10-24, round 43 (append-only; the sentences above are not rewritten)
+
+The S077 capture `.qcache/01f657b3d0ab045c494b3f92.txt` is 267 bytes and 265 Unicode characters. The "265-char" wording above matches the decoded length. The spot-check's "267 bytes" matches `wc -c`. Neither number corrects the other. A later reader should cite both.
```

`git show e0f4895c48d6c6e739ce9deb614b97c771a3a096:corpus/lessons/round-42.md | wc -l` → `149`. Same command at the measured commit → `153`.

`git log -S '265-char' --format='%H %ci %s' -- corpus/lessons/round-42.md` names both `737f40b` and `e0f4895`. `git log -S '265-character'` names only `e0f4895`.

Python over `git show` bytes of both revisions (exact token `265-char(?!acter)`):

```
prefix_identity True
parent_sha256 6a20a2d41feeea302d26df6b0c82b9a9fbc4fef71c644e6435731409d6dc29db
head_sha256 599efe300578bcec828f0e6f35d134ffe1a377b2d7ca3dd2fb3a348564315e6e
== parent exact 265-char token ==
81	| provenance-class — a register class that licenses a fabrication verdict is only as good as the capture behind it; "fetched cleanly" can mean "a bot wall was saved" | S077: the campaign's class cell reads `payload-absent` ("every relevant source fetched cleanly") while the local capture of that DOI is a 265-char `Client Challenge` page (`tools/quarantine-check.py` `capture_kind`, cache file `01f657b3d0ab045c494b3f92.txt`) | none — no criterion tied a capture's FORM to the class it licenses | the frozen decision rule's step 2 refuses a bot wall, a binary document and a too-short capture as `unverifiable`; the lane's QUALITY criterion 59 and this lesson are the record |
count=1
== head exact 265-char token ==
81	| provenance-class — a register class that licenses a fabrication verdict is only as good as the capture behind it; "fetched cleanly" can mean "a bot wall was saved" | S077: the campaign's class cell reads `payload-absent` ("every relevant source fetched cleanly") while the local capture of that DOI is a 265-char `Client Challenge` page (`tools/quarantine-check.py` `capture_kind`, cache file `01f657b3d0ab045c494b3f92.txt`) | none — no criterion tied a capture's FORM to the class it licenses | the frozen decision rule's step 2 refuses a bot wall, a binary document and a too-short capture as `unverifiable`; the lane's QUALITY criterion 59 and this lesson are the record |
153	The S077 capture `.qcache/01f657b3d0ab045c494b3f92.txt` is 267 bytes and 265 Unicode characters. The "265-char" wording above matches the decoded length. The spot-check's "267 bytes" matches `wc -c`. Neither number corrects the other. A later reader should cite both.
count=2
clause_in_parent True
clause_in_head True
clause_count_parent 1
clause_count_head 1
```

The same script also printed:

```
parent_bytes 11075 sha256 6a20a2d41feeea302d26df6b0c82b9a9fbc4fef71c644e6435731409d6dc29db
head_bytes 11434 sha256 599efe300578bcec828f0e6f35d134ffe1a377b2d7ca3dd2fb3a348564315e6e
worktree_bytes 11434 sha256 599efe300578bcec828f0e6f35d134ffe1a377b2d7ca3dd2fb3a348564315e6e
worktree_eq_head True
parent_endswith_newline True
head_endswith_newline True
head_startswith_parent True
APPENDED_BYTES_REPR b'\n## Erratum \xe2\x80\x94 2026-10-24, round 43 (append-only; the sentences above are not rewritten)\n\nThe S077 capture `.qcache/01f657b3d0ab045c494b3f92.txt` is 267 bytes and 265 Unicode characters. The "265-char" wording above matches the decoded length. The spot-check\'s "267 bytes" matches `wc -c`. Neither number corrects the other. A later reader should cite both.\n'
APPENDED_SHA256 989e8e73c24bce4552bcd4294f39bb48d0be5b32de5f02ad6d8fc5721358ce2f
```

`sha256sum corpus/lessons/round-42.md .ufo/waves/round-43/assimilation/validate/corpus/lessons/round-42.md`

```
599efe300578bcec828f0e6f35d134ffe1a377b2d7ca3dd2fb3a348564315e6e  corpus/lessons/round-42.md
6a20a2d41feeea302d26df6b0c82b9a9fbc4fef71c644e6435731409d6dc29db  .ufo/waves/round-43/assimilation/validate/corpus/lessons/round-42.md
```

`cmp -s` of those two paths: `cmp_exit=1`.

`git merge-base --is-ancestor 15f9f3fbd3c17b2155f718c67cbef0624034cf6d 737f40b6aa8f37ffe2269db370fd6d65a720d9a8` → `ancestor_exit=0`. `git rev-parse 15f9f3fbd3c17b2155f718c67cbef0624034cf6d:corpus/lessons/round-42.md` → `1e21181540287ea992c68335a2acaa1bb63f632f`, the same blob as `e0f4895c48d6c6e739ce9deb614b97c771a3a096:corpus/lessons/round-42.md`.

`git grep -n -F '265-char' 15f9f3fbd3c17b2155f718c67cbef0624034cf6d -- corpus/lessons/round-42-verifier-spotcheck.md` printed lines 120 and 182 (the cosmetic note). `git diff --stat 15f9f3fbd3c17b2155f718c67cbef0624034cf6d 737f40b6aa8f37ffe2269db370fd6d65a720d9a8 -- corpus/lessons/round-42-verifier-spotcheck.md` produced no output; `spotcheck_diff_exit=0`.

## Known limits

- This seat did not remeasure the S077 capture, so the erratum's 267/265 figures remain a quoted claim.
- Author date of the measured commit (20:52:23 -0300) is earlier than its committer date (21:15:02 -0300). Blame dates the erratum lines with the author date. That is provenance, not evidence that line 81 changed.
- The validate mirror's file mtime in the `diff -u` header is 2026-10-24 20:43:32.165966465 -0300. That timestamp is quoted from `diff`; this seat did not establish how the mirror was produced.

## Artifact paths

- This report: `.ufo/waves/round-43/w1/ScribeErratum.md`
- Quoted lesson: `corpus/lessons/round-42.md`
- Pre-erratum blob: `1e21181540287ea992c68335a2acaa1bb63f632f`
- Measured blob: `a59ce1ba6d38004c840ed29fcfeddd6b92e2f1a9`

Report: .ufo/waves/round-43/w1/ScribeErratum.md
