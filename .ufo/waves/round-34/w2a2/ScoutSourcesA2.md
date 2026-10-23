# ScoutSourcesA2 — re-open S064 and S066 (round 34 attempt 2, wave 2, 2026-10-23)

Verdict: **S064 pins hold. S066 pins hold. No pin-failure finding.** Census `exit=0`. S065 was not re-opened here.

Rows read from `corpus/SOURCES.md` lines 74 (S064) and 76 (S066). That file's git blob is `6dbef6e4ee4de22cf5a747ec6913c919544623a8` at both `HEAD` (`fe3db76c0ae9fa18cfebcf127fec073354a1eb03`) and the wave freeze `707da8184a0fc4d10ab3f17271556cdf364f0af5` (`git merge-base --is-ancestor` exit 0; one later commit only). `git status --porcelain` on `corpus/SOURCES.md`, `corpus/lessons/round-34.md`, and `tools/research-gate.sh` was empty. Worktree gate sha256 `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b` (prefix `a6307edf687ac0fb`); git blob `8ebd4704e3f4cc2aeeac767db7d5f9b7d12d95a0` at both commits. Access date 2026-10-23. No network. No installs. Receipt: `.ufo/waves/round-34/w2a2/ScoutSourcesA2/pins.txt`.

## S064 — execve(2) — pins hold

- `man -w 2 execve` exit 0 → `/usr/share/man/man2/execve.2.gz`.
- `sha256sum` = `4489dfef246682d18365712ce686f3519318b074761f249091c5fc99c8eab0dc`, equal to the anchor on `corpus/SOURCES.md:74`.
- `pacman -Q man-pages` exit 0 → `man-pages 6.19-1`. `pacman -Qo` exit 0: the `.gz` is owned by that package. Page header (decompressed `execve.2:7`) is `.TH execve 2 2026-02-08 "Linux man-pages 6.19"` — upstream 6.19, pkgrel `-1` only in the package pin. Both match the row.
- Anchor: `.SS Limits on size of arguments and environment` at decompressed line 365; `.SH RETURN VALUE` at 425. Quote lines 422–424 join, after `.BR`, to the lesson gate quote (`corpus/lessons/round-34.md:47-48`, 20 words): "Additionally, the limit per string is 32 pages (the kernel constant MAX_ARG_STRLEN), and the maximum number of strings is 0x7FFFFFFF." Same sentence is in `GROFF_NO_SGR=1 groff -man -Tutf8 | col -bx` (exit 0) and in `man -P cat 2 execve` (exit 0).
- Teaches on `:74` (aggregate limit vs 32-page per-string `MAX_ARG_STRLEN`) matches decompressed lines 404–424. The in-round anchor correction off `NOTES` is still right: the quote is in the subsection, not under `.SH NOTES`.
- URL `https://man7.org/linux/man-pages/man2/execve.2.html` was not fetched (no network). The row already says the URL was not fetched.

## S066 — grep(1) — pins hold

- `man -w 1 grep` exit 0 → `/usr/share/man/man1/grep.1.gz`.
- `sha256sum` = `9b027d022ae9533ff3e140ba8d96ccd58955bdf9d1c818c327fd992e575c85ba`, equal to `corpus/SOURCES.md:76`.
- `pacman -Q grep` exit 0 → `grep 3.12-2`. `pacman -Qo` exit 0: both `man1/grep.1.gz` and `/usr/bin/grep` are owned by `grep 3.12-2`.
- Page identity: decompressed `grep.1:5` `.dT Time-stamp: "2025-03-21"` and `:12` `.TH GREP 1 \*(Dt "GNU grep 3.12-modified" "User Commands"`. Rendered header contains `GNU grep 3.12-modified` and `2025-03-21`. Matches the row's "3.12-modified (2025-03-21)" plus installed `grep 3.12-2`.
- Section homes (roff line numbers): `.SS "Pattern Syntax"` `:200` holds `-F` `:207` and `-P` `:218`; `.SS "Matching Control"` `:228` holds `-f` `:240`; `.SS "Other Options"` `:716` holds `-z` `:746`.
- Lesson gate quote (`corpus/lessons/round-34.md:55`, 7 words) is roff `:241-243` and is exact in both renders: "Obtain patterns from FILE, one per line." Also exact in the flat render: "Interpret PATTERNS as fixed strings, not regular expressions." (`:208-210`); "Interpret PATTERNS as Perl-compatible regular expressions (PCREs)." (`:219-221`); "Treat input and output data as sequences of lines, each terminated by a zero byte (the ASCII NUL character) instead of a newline." (`:747-748`, 23 words).
- The row's "does not change the documented pattern-file delimiter" is a reading of that page: the `-z` entry `:746-755` does not mention `-f`, and `-f` still says one per line. Not a runtime probe. The newline-span clause is already marked `[INFERENCE]` on `:76`; not re-tested.

## Census

Command (stdout redirected, then `echo exit=$?`):

`timeout 900 /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`

Exit **0**. Every stdout line (`census.txt` sha256 `eb4dde9b2cde81e8432e70d5b673f4fb3cb3bbac681e0382c4dfe25a1e49d98d`, copy `.ufo/waves/round-34/w2a2/ScoutSourcesA2/census.txt`):

```
chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
```

W04 is on S051 and S053, not S064 or S066. `sources-census.sh` treats W-codes as non-failing (`scripts/sources-census.sh:32-33`). No E11, so the used-by path `corpus/knowledge/long-span-argv-r34.md` is on disk; that file cites S064 and S066 (`corpus/knowledge/long-span-argv-r34.md:3`, `:19`).

## Limits

- S065 not opened this seat.
- Decompressed and rendered pages are under `/fast/scratch/hyaku/chousa-r34-a2/w2/ScoutSourcesA2/` (`execve.nosgr` 22726 bytes, `grep.nosgr` 32461 bytes). No lane production file, git index, or jj state was written. `df -h /fast` before the writes: 37G free.
