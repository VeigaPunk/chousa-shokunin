# RevC2Claim3 — entailment review of Claim 3 (round 61, w1)

Scope: Claim 3 of `corpus/evidence/round61/controls/c2-positive-entry.md` (the positive control and landing candidate). Quote cited: Q4 (S135, rename(2)). Read-only review; no lane file touched.

## Method

- Rendered the page this host has installed: `MANWIDTH=1000 man -l /usr/share/man/man2/rename.2.gz | col -bx` (210 lines, kernel 7.2.11-arch1-1, man-pages as installed).
- Located Q4 at rendered line 46 of the DESCRIPTION section. Exact-match check: `grep -c -F "If oldpath refers to a symbolic link, the link is renamed; if newpath refers to a symbolic link, the link will be overwritten."` → `1`. The quote in the entry is byte-identical to the page.
- Read the surrounding DESCRIPTION paragraphs (rendered lines 33–63):
  - L34: "rename() renames a file, moving it between directories if required."
  - L38: "If newpath already exists, it will be atomically replaced, ..." (the atomic-replacement sentence Claim 4 cites as Q5)
  - L40: hard-link case: "If oldpath and newpath are existing hard links referring to the same file, then rename() does nothing"
  - L42: "If newpath exists but the operation fails ... leave an instance of newpath in place."
  - L46: Q4, the only sentence on symlinks in DESCRIPTION.
  - No sentence in the surrounding text qualifies, restricts or contradicts L46. Q4 is not taken out of context.
- Fixture probe (scratch, deleted), Linux `os.rename` from Python 3.x on this host:
  - Planted link `final.txt -> target.txt`, temp file renamed onto `final.txt`: `final.txt is link: False`, `target: ORIGINAL`, `final: NEW`. The link was replaced; the target was not written.
  - Dangling link `final2.txt -> nowhere.txt`: after rename, `final2 is link: False`, `nowhere exists: False`. Replaced, nothing created at the link's target.
  - Symlinked directory component `linkdir -> realdir`, rename to `linkdir/final3.txt`: `via linkdir landed in realdir: True`. Earlier components are followed.

## Entailment of Claim 3

Claim 3 (verbatim): "When newpath refers to a symbolic link, a rename overwrites the link instead of following it, so a derived file written by temporary file and rename cannot write through a link planted at its final name."

Split into the parts it asserts:

1. "When newpath refers to a symbolic link, a rename overwrites the link" — stated by Q4 directly. **Supported.**
2. "instead of following it" — Q4 says "will be overwritten", not "is not followed". The page never uses "follow" for rename. Reading "overwritten" as "no write through the link" is the natural and correct reading; the fixture confirms it for live and dangling links. **Supported as a reading; the words "instead of following it" are a gloss, not a quote** (INFERENCE, low risk).
3. "so a derived file ... cannot write through a link planted at its final name" — the conclusion is scoped to "at its final name", which is the only position Q4 speaks to. The temporary-file write (the open of the temp name) is a separate step at a different name; Claim 3 does not claim anything about it, and the claim's own wording excludes it. **Supported within the stated scope.** It is not a claim that the whole write procedure is safe; Claim 2 (O_CREAT|O_EXCL, Q3) is the leg that covers the temp name, and the entry keeps them separate.
4. Scope boundary, not stated in the claim: the page does not say whether rename follows symlinks in earlier components. The fixture shows it does (`linkdir/final3.txt` landed in `realdir`). Claim 3 is silent on directory components, so it does not overreach; but a reader could take "cannot write through a link" to cover a planted output directory. Claim 1 (O_NOFOLLOW, Q1/Q2) addresses earlier components only for open(2), not for rename(2). The entry has no quote for rename's directory-component behaviour. This is a gap in what the entry says, not an error in Claim 3.

Context findings (not defects of Claim 3):
- L40 (hard links to the same file make rename a no-op) is not a symlink case and does not affect Claim 3. A planted hard link at the final name would matter only if the attacker knew the temp name; the claim does not depend on it.
- L70 / EISDIR / EXDEV (cross-filesystem) are outside Claim 3; the claim does not say temp and final share a directory or filesystem. A temp in a different directory would be a different procedure (the claim describes same-directory temp+rename implicitly). Not claimed; not a finding.

## Verdict on Claim 3

Supported. The quote is present, exact, and read in its paragraph without any qualifier that changes it. The claim goes no further than the quote in its own scope, provided "at its final name" is kept. One gloss ("instead of following it") is a reading, not a quote, and should be kept marked as such (INFERENCE). Directory-component behaviour is not covered by Claim 3 and is an unquoted gap for rename(2), not an overreach.

No rewrite is required for the claim to be entailed. Optional tightening (calibration only; not needed for admission):

> Claim 3 (optional). When newpath refers to a symbolic link, rename overwrites the link rather than writing through it (Q4; the no-follow reading is INFERENCE from "will be overwritten"), so the final step of a temporary-file-then-rename write does not write through a link planted at the final name. The temporary name itself is a separate step covered by Claim 2. The page does not state how rename treats symbolic links in earlier path components.

## Operability / calibration notes

- Checks run: man render (1 command), exact-match grep (1 command), context read (rendered lines 33–63), one Python fixture probe (3 cases), cleanup. All outputs above.
- Not run: the lane counter `c2-count.py` (not mine to run for this item; the item is entailment, which the counter explicitly does not judge). Not run: any other claim (Q1–Q2, Q3, Q5–Q8, Claims 1, 2, 4, 5).
- Access: installed man page only; no network; the S135 canonical man7.org render was not opened (as the entry's own access disclosure states).
- Installs: none.
- Scratch `/fast/scratch/hyaku/chousa-r61/RevC2Claim3/` created and removed.

VERDICT: CLAIM3=supported rewrite_needed=no
