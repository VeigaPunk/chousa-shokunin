# RevC2Claim1 — entailment review of Claim 1 (c2-positive-entry.md)

Scope: Claim 1 of `corpus/evidence/round61/controls/c2-positive-entry.md` only, against its cited quotes Q1 and Q2 (S134, open(2)). Claim 1 does not cite S135 or S136, so Q3–Q8 are out of scope. Frozen claims read first (sha256 `9afec8d4…ce0acec`, matches).

## Claim 1 as written
> O_NOFOLLOW protects only the final path component of an opened file, so a symbolic link in an earlier component, such as a linked output directory, is still followed and the writer must test that directory itself. [Q1, Q2]

## Commands run and observed output
1. `MANWIDTH=1000 man -l /usr/share/man/man2/open.2.gz | col -bx` → 516 lines; header reads `NAME` / `man-pages 6.19-1`. Rendered to a scratch file (deleted at close).
2. `grep -nF` of the full Q1 sentence ("If the trailing component (i.e., basename) of path is a symbolic link, then the open fails, with the error ELOOP.") → rendered line 147, rc=0. Exact.
3. `grep -nF` of the full Q2 sentence ("Symbolic links in earlier components of the pathname will still be followed.") → rendered line 147, same paragraph, rc=0. Exact.
4. `grep -niE 'nofollow|trailing component|earlier components|ELOOP'` over the rendered page → hits at 147 (O_NOFOLLOW entry), 189 (O_PATH + O_NOFOLLOW returns a descriptor for the link itself), 319 (ELOOP when O_NOFOLLOW without O_PATH), 434 (HISTORY/standards line). No passage in open(2) mentions directories, output directories, writers, or testing before a write.

## Context of the quotes
Q1 and Q2 sit in one paragraph (rendered 146–152), immediately followed by a parenthetical the entry omits: "Note that the ELOOP error that can occur in this case is indistinguishable from the case where an open fails because there are too many symbolic links found while resolving components in the path prefix of the pathname." That parenthetical is not a misreading risk for Claim 1 (it concerns ELOOP interpretation, not directories), so omitting it is fair. The paragraph then states the FreeBSD/POSIX provenance. No passage in open(2) qualifies Q2 (no "unless" or "see openat2"). Quoting is not taken out of context in a way that changes meaning.

## Entailment decision, clause by clause
- **A. "O_NOFOLLOW protects only the final path component … a symbolic link in an earlier component … is still followed."** SUPPORTED. Q1 gives the final-component behaviour, Q2 gives the earlier-component behaviour, and the page's own "(i.e., basename)" pins "trailing component" to the final component. Not misread.
- **B. "such as a linked output directory."** Illustrative application. The page does not mention output directories. It is harmless as an example, but it is not sourced. Keep only if marked as an example, or drop.
- **C. "so … the writer must test that directory itself."** OVERREACH. Neither Q1 nor Q2 says anything about testing, directories as a remedy, or writers. This is a prescription the quotes do not reach. It also conflicts with the entry's own Limits (line 32, marked [INFERENCE]): "A check followed by a write is not atomic with it, so a process that swaps a directory for a link between the two is not stopped by the checks." Read as written, Claim 1 offers a remedy (a test) that the entry itself says does not stop the failure it is for. That is a calibration defect: the sentence reads as sufficient.

Verdict on Claim 1: the factual core (A) is supported; the remedy (C) is overreach.

## Rewrite proposal (quote-bound)
Supported form, citing only Q1 and Q2:

> O_NOFOLLOW checks only the trailing component of the path: a symbolic link in an earlier component is still followed. [Q1, Q2]

If the writer's consequence is kept, put it in its own clause marked as inference and cite the existing Limits:

> [INFERENCE] A directory check made before the write does not settle this, because the check and the write are not atomic (Limits).

## Depth note (not a required change; for L1 decision)
The same installed package (man-pages 6.19-1) documents a mechanism that covers earlier components and is not cited anywhere in the entry: `openat2(2)` with `RESOLVE_NO_SYMLINKS`. Rendered with `MANWIDTH=1000 man -l /usr/share/man/man2/openat2.2.gz | col -bx` (scratch file), the line 86 reads, verbatim: "Note that the effect of the RESOLVE_NO_SYMLINKS flag, which affects the treatment of symbolic links in all of the components of path, differs from the effect of the O_NOFOLLOW file creation flag (in how.flags), which affects the handling of symbolic links only in the final component of path." (`grep -nF` → line 86, rc=0.) Its text also says applications should make it configurable, because it can cause spurious errors on systems whose paths gain a symlink. I have not checked whether it closes the check-then-write race; that is not a claim here. If L1 wants a remedy in Claim 1, the sourced route is: append an S-row for openat2(2) after the L1's own opening (this seat did not write registry rows), add the verbatim line-86 quote, and cite it. Otherwise drop the remedy and keep the rewrite above.

## Not checked
- Claims 2–5 and their quotes Q3–Q8 (other seats or the L1).
- Canonical man7.org HTML (access disclosure in claims.md; not fetched, no network).
- Whether openat2(2) is race-free (not read beyond line 86 and the retry note near line 109).

## Hygiene
No writes outside this report. Scratch `/fast/scratch/hyaku/chousa-r61/RevC2Claim1/` removed at close. No installs. No subagents spawned.

VERDICT: CLAIM1=overreach rewrite_needed=yes
