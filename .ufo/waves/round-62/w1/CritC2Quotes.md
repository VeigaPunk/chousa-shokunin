# CritC2Quotes — round 62 w1 (critic, item CritC2Quotes)

Scope: quotes Q1–Q9 of `corpus/evidence/round62/controls/c2v2-positive-entry.md`, each read in its page context.
Sources read: man-pages 6.19-1 page rendered as the row says (`MANWIDTH=1000 man -l /usr/share/man/man2/openat2.2.gz | col -bx`, 171 lines);
`/usr/include/linux/openat2.h` (linux-api-headers 7.2-1); `controls/candidate-openat2-probe.py` and `.txt`; registry rows in
`controls/c2v2-positive-rows.txt`. Host: kernel 7.2.11-arch1-1, `pacman -Q glibc` → 2.44+r50+g1848099f063e-1, `ldd --version` → GNU libc 2.44.
No edits under the frozen paths; no git; no network; scratch removed.

## Findings (most serious first)

1. **Q5 does not hold on this host (claim 4).** Q5 says "glibc provides no wrapper for openat2(), necessitating the use of syscall(2)."
   That sentence is a SYNOPSIS note on the man page (`openat2.txt` line 18) and is true of that page's world only. The host glibc has one:
   - `nm -D /usr/lib/libc.so.6 | grep -i openat2` → `0000000000112aa0 W openat2@@GLIBC_2.43`
   - `/usr/include/bits/fcntl-linux-fortify.h:36` declares `openat2 (int __dfd, const char *__filename, const struct open_how *__how, ...)`, reached from `<fcntl.h>` via `bits/fcntl-linux.h:474`.
   - ctypes `libc.openat2(AT_FDCWD, file, how, 24)` on a plain temp file returned fd >= 0 (run by me, output: `plain open via libc.openat2 fd>=0: True`).
   Claim 4 ("needs ctypes or another route to syscall(2), because glibc has no wrapper") is stated unscoped and is false for this host.
   Provenance mismatch on the same row: the S138 row and the teaches cell say man-pages 6.19 is dated 2026-02-08; the rendered page footer reads `Linux man-pages 6.19 ... 2026-07-02`.

2. **Q2 (cited by claim 1) omits the O_PATH carve-out in the same paragraph.** Q2 is "Disallow resolution of symbolic links during path resolution. This option implies RESOLVE_NO_MAGICLINKS." The next sentences of the RESOLVE_NO_SYMLINKS paragraph (`openat2.txt`, RESOLVE_NO_SYMLINKS block) read: "If the trailing component (i.e., basename) of path is a symbolic link, how.resolve contains RESOLVE_NO_SYMLINKS, and how.flags contains both O_PATH and O_NOFOLLOW, then an O_PATH file descriptor referencing the symbolic link will be returned."
   Claim 1 says the flag makes the kernel "refuse a symbolic link anywhere along the walk". For a final-component symlink with O_PATH|O_NOFOLLOW that is false. Observed by me on this host: final symlink with `RESOLVE_NO_SYMLINKS` alone → `ELOOP`; with `O_PATH|O_NOFOLLOW|RESOLVE_NO_SYMLINKS` → fd returned (`final symlink O_PATH|O_NOFOLLOW NO_SYMLINKS rc>=0: True`).
   The lane already measures this: candidate probe P14 `openat2-O_PATH-O_NOFOLLOW-NO_SYMLINKS-final-symlink-fd-is-the-link observed=True expected=True ok`, which the entry never cites. The row teaches cell ("refuses a symbolic link in every path component") and Claim 1 carry the same gap.

3. **Q3 is a fragment whose subject is elided; read with its anchor it says the opposite of claim 1.** Full sentence in `openat2.txt` (RESOLVE_NO_SYMLINKS paragraph): "Note that the effect of the RESOLVE_NO_SYMLINKS flag, which affects the treatment of symbolic links in all of the components of path, differs from the effect of the O_NOFOLLOW file creation flag (in how.flags), which affects the handling of symbolic links only in the final component of path."
   Q3 is the tail "which affects the handling of symbolic links only in the final component of path". Its `which` points to O_NOFOLLOW only after the parenthetical; the row anchor is RESOLVE_NO_SYMLINKS. Excerpted as the entry does, the quote reads as NO_SYMLINKS being final-component-only, which contradicts claim 1. The "all of the components" half that claim 1 needs is outside Q3, so claim 1's "anywhere" rests on Q2 alone (see finding 2). With the subject restored, Q3 supports only the O_NOFOLLOW half of claim 1.

4. **Q1 is hedged and generic; claim 3 hardens it.** Q1 "The primary use case for these flags is to allow trusted programs to restrict how untrusted paths..." Claim 3 says the flags "are designed for trusted programs". The same section continues: "Applications that employ the RESOLVE_NO_SYMLINKS flag are encouraged to make its use configurable (unless it is used for a specific security purpose)... may result in spurious errors on previously functional systems." That limit is absent from the entry. Q1 also sits in the generic `resolve` intro for all flags, but is anchored to RESOLVE_NO_SYMLINKS.

5. **Q6 (header) carries a header typo and the same "all symlinks" overstatement; claim 5's advice is not in the quote.** Q6 is `Block traversal through all symlinks (implies OEXT_NO_MAGICLINKS)` (`/usr/include/linux/openat2.h` lines 37–38). `OEXT_NO_MAGICLINKS` is not an identifier; the header means RESOLVE_NO_MAGICLINKS. The entry quotes it verbatim without correction. "All symlinks" lacks the O_PATH carve-out of finding 2. Claim 5's "so a caller should read the numeric flag values from that header instead of typing them from memory" is not supported by Q6 (it is advice, not header text) and is not marked [INFERENCE].
   Weakest of the five: if the reader accepts claim 5 as the descriptive sentence only, Q6 drops out and k becomes 4.

## Quotes that hold (no unstated limit found)

- **Q4** (`openat2.txt`, RESOLVE_BENEATH): "Do not permit the path resolution to succeed if any component of the resolution is not a descendant of the directory indicated by dirfd." Supports claim 3 ("rejects any resolution that would leave the directory"). The "may change in the future" hedge belongs to the magic-link sentence after it, not to claim 3's content.
- **Q7, Q8, Q9** (S140): each is verbatim one line of `controls/candidate-openat2-probe.txt` (lines 5, 7, 4). Fixture: `linkdir -> real` (relative), so an O_NOFOLLOW open through `linkdir/f.txt` opens and openat2 NO_SYMLINKS on the same path gives ELOOP, on this host. Supports claim 2 and the os-module fact in claim 4 (`hasattr(os,'openat2')` is False).
  Caveats, not quote failures:
  a. The committed S140 file `corpus/evidence/round62/openat2-probe.txt` does not exist in the lane tree (only the candidate under `controls/`). The quotes resolve against the candidate.
  b. The probe's `expected` column is authored from the page (candidate probe line 85 comment: "the page: earlier components are followed"). "ok" measures agreement with the page; observed values are independent. The quotes are corroboration of the page only in the sense that the observed column matches it.
  c. The probe calls `libc.syscall` (line ~54), consistent with claim 4's route but avoiding the host's wrapper (finding 1).

## Mechanical checks run

- Verbatim check (whitespace-normalised containment in the rendered man page / header): Q1 24 words found; Q2 12 found; Q3 14 found; Q4 24 found; Q5 11 found; Q6 7 found (header); Q7–Q9 6 words each, match candidate probe lines. No quote is fabricated or cross-row.
- Counter scope: `c2v2-count.py` checks anchors, word counts and echo, not context. None of findings 1–5 is caught by the counter (the frozen predicate says so: entailment is reviewers' job).

## Per-quote tally (criterion: a reading in page context under which the quote does not support the claim or teaches cell that cites it, from a hedge, scope, omitted sentence or version that the entry does not state)

| Q | cited by | unstated limit? | basis |
|---|---|---|---|
| Q1 | claim 3 | YES | "primary use case" hardened to "designed for"; spurious-error warning omitted |
| Q2 | claim 1 | YES | final-component O_PATH|O_NOFOLLOW carve-out omitted (P14; my ctypes check) |
| Q3 | claim 1 | YES | subject elided; excerpt reads as NO_SYMLINKS final-only |
| Q4 | claim 3 | NO | supports |
| Q5 | claim 4 | YES | host glibc 2.44 exports openat2 wrapper (GLIBC_2.43); page-scoped quote used unscoped |
| Q6 | claim 5 | YES | header typo carried; "all symlinks" without carve-out; prescription not in quote |
| Q7 | claim 2 | NO | supports on this host (caveats a, b) |
| Q8 | claim 2 | NO | supports on this host |
| Q9 | claim 4 | NO | supports (own text is accurate) |

## Suggested corrections (routed as LIMITS/supplements per the frozen rule; no edit made)

- Add the O_PATH|O_NOFOLLOW sentence (RESOLVE_NO_SYMLINKS paragraph) as a quote, cite P14, and restate claim 1 as "refuses symlinks in all components, except that a final-component symlink under O_PATH|O_NOFOLLOW yields a descriptor for the link".
- Quote Q3 with its subject: "...the O_NOFOLLOW file creation flag ... affects the handling of symbolic links only in the final component of path."
- Scope claim 4 to man-pages 6.19 and add a LIMITS bullet: host glibc 2.44 exports `openat2` (GLIBC_2.43), so ctypes can call `libc.openat2` directly; requires a registry row for the glibc header or symbol, not a quote edit.
- Fix or flag the S138 row date (2026-02-08 vs footer 2026-07-02).

## VERDICT

VERDICT: QUOTES_WITH_UNSTATED_LIMIT=5 of 9
