# CritC2Quotes — critic on the C2 positive-entry quotes (round 61, wave w1)

Target: `corpus/evidence/round61/controls/c2-positive-entry.md`, quotes Q1–Q8, read against the rendered
man pages and the S136 source file. Read-only. No network. No counter was run by me (the frozen counters
are the L1's); this report is a critic reading, not a gate.

## Method and commands (all run)

- `MANWIDTH=1000 man -l /usr/share/man/man2/open.2.gz | col -bx > open.txt` → 516 lines, footer `Linux man-pages 6.19`.
- `MANWIDTH=1000 man -l /usr/share/man/man2/rename.2.gz | col -bx > rename.txt` → 210 lines, footer `Linux man-pages 6.19`.
- `grep -n -F "<quote>" open.txt rename.txt`: Q1, Q2, Q4, Q5, Q6 found verbatim. Q3 found as a lowercase
  substring of open.txt:123, which reads `When these two flags are specified, symbolic links are not followed: if path is a symbolic link, then open() fails regardless of where the symbolic link points.`
- Placement of Q3: open.txt:120 is the `O_EXCL` header; 121–125 are its paragraphs. The `O_PATH` header is
  open.txt:162. Q3 belongs to the O_EXCL paragraph, not O_PATH and not O_NOFOLLOW.
- `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show 9eef15e7c0e0ae0055228e7066dc1eec676a91d2:.ufo/waves/round-56/w1/R55W2SentBuilder.md`
  → 120 lines. Q7/Q8 text at lines 33–34; table rows h2 (line 11) and h3 (line 12); revision `29cfb12` at line 3.
  The lane working-tree copy has the same line count (120).

## Per-quote result

Criterion used: a limit that the page context or the seat report places on the quote, and that is absent
from the quote text, the row's teaches cell, the claim text and the entry's Limits section. The entry's
Limits (`Linux man-pages 6.19 on this host; other systems and versions are not covered`) is accepted as
stating the kernel-version and other-system limits for the two man pages, so I did not count the FreeBSD/POSIX
remark (open.txt:149) or the kernel-2.6 remark (open.txt:127) as unstated for Q1/Q2.

| Q | Quote anchor | Scope sentence in page context (file:line) | Stated in the entry? | Unstated limit |
|---|---|---|---|---|
| Q1 | open.txt:147, O_NOFOLLOW | ERRORS open.txt:319 `ELOOP path was a symbolic link, and flags specified O_NOFOLLOW but not O_PATH.` and the O_PATH paragraph open.txt:189 `If path is a symbolic link and the O_NOFOLLOW flag is also specified, then the call returns a file descriptor referring to the symbolic link.` So "the open fails" holds only without O_PATH. | No. Entry never mentions O_PATH. | YES |
| Q2 | open.txt:147 | None in the sentence. The sentence itself carries the O_NOFOLLOW scope (`still`). The parenthetical at open.txt:147 limits only error attribution (ELOOP is indistinguishable from too many links), not the following. | Yes (claim 1 states the same). | NO |
| Q3 | open.txt:123, O_EXCL | (a) Antecedent `When these two flags are specified` (O_CREAT and O_EXCL) is cut from the entry's quote without an ellipsis; the entry's quote starts mid-sentence in lowercase. (b) O_PATH at open.txt:185: `When O_PATH is specified in flags, flag bits other than O_CLOEXEC, O_DIRECTORY, and O_NOFOLLOW are ignored`, so O_CREAT|O_EXCL is inert under O_PATH. (c) The sentence is about `path` as a whole; the page says nothing about earlier components for O_EXCL, so claim 2's `fresh temporary name cannot be written through a planted link` covers only the final component. (d) open.txt:127: O_EXCL on NFS needs NFSv3+ and kernel 2.6+, and without it `programs that rely on it ... will contain a race condition`. | Claim 2 names O_CREAT and O_EXCL, so (a) is partly stated. (b), (c), (d) are not stated. | YES |
| Q4 | rename.txt:46, DESCRIPTION | None in the sentence. ERRORS rename.txt:146 (sticky bit, EPERM) and rename.txt:150 (EXDEV) are failure cases, not write-through cases. | Not needed for Q4. | NO |
| Q5 | rename.txt:38, DESCRIPTION | The sentence begins `If newpath already exists, it will be atomically replaced`. The quote drops `If newpath already exists,`. Atomicity is stated only for an existing target. | Claim 4 says `the replacement is atomic`; the existing-target condition is not written. | YES |
| Q6 | rename.txt:38 | The hedge `probably` is inside the quote; claim 4 drops it (`yet a window exists`). Nothing in rename.txt:38–46 says a failed run leaves a temporary name behind; rename.txt:42 guarantees an instance of newpath, not of the temporary name. | Hedge dropped; `failed run can leave the temporary name behind` is not in any quote. | YES |
| Q7 | r55.md:33, S136 | Observed at revision `29cfb12` (r55.md:3), pre-landing builder, on the seat's own `example.invalid` fixture (r55.md:3). Row S136 calls it `a seat report, not a re-runnable gate output`. The victim directory is the link target of `out/spans` (r55.md:11), which the quote does not show. | Revision and own-fixture scope are in row S136 only. Not in claim 5, not in Limits (Limits covers man-page quotes only). | YES |
| Q8 | r55.md:34, S136 | Same as Q7. `10→457 B`, `74→243 B` transcribed as in r55.md:34. Row h3 (r55.md:12) is the source. | Same as Q7. | YES |

Count: Q1, Q3, Q5, Q6, Q7, Q8 have an unstated limit. Q2 and Q4 do not.

## Findings on the entry's claims (depth and calibration)

1. Claim 4 overstates the source. `a window exists` is the unhedged form of `there will probably be a window`
   (rename.txt:38). Calibration gap, not a quote error.
2. Claim 4's `a failed run can leave the temporary name behind` is INFERENCE. No quoted sentence supports it,
   and the entry's Limits does not mark it. The NFS BUGS note (rename.txt, BUGS section) `you can not assume
   that if the operation failed, the file was not renamed` cuts against any reading that a failed rename is
   known to leave a clean state, so cleanup on the error path is not established by these quotes.
3. Claim 2 is final-component-only (see Q3(c)). The entry's Claim 1 covers earlier components; Claim 2 is
   worded as if it covered the whole output path. Scope gap.
4. Depth gap, not a quote limit: the man page gives the remedy for the earlier-component problem
   (open.txt:473, the openat rationale: race `dir1 or dir2 (which might be symbolic links) could be modified`,
   avoided by a directory fd). The entry's Claim 1 says `the writer must test that directory itself`, which is
   the weaker option and is not the page's recommended one.
5. The Q3 quote is a substring that the counter accepts while the antecedent that limits it is removed. The
   counter's `echo-claims` control already shows the counter does not judge claim support; this scope cut is
   of the same kind and is not visible to the counter.

## Limits of this critique

- I did not run `c2-count.py`, `c1-count.py`, `regress.py` or any control; I read the page text and the
  S136 source only.
- POSIX.1-2008 text was not opened (no network, and the FreeBSD/POSIX remark is not a behaviour statement
  in the page). Any claim about POSIX behaviour is INFERENCE.
- Q7/Q8 are a seat's observation at revision `29cfb12`; I did not re-run that fixture. The counts above are
  about the quote text and its source, not about the current builder.

## Install / scratch

- Installs: none (no `pacman`, no `uv`, no `npm`). Only `man`, `col`, `grep`, `sed`, `git show` (read-only) were used.
- Scratch `/fast/scratch/hyaku/chousa-r61/CritC2Quotes/` (open.txt, rename.txt, r55.md) removed before yield.
- No writes to the lane outside this report.

VERDICT: QUOTES_WITH_UNSTATED_LIMIT=6 of 8
