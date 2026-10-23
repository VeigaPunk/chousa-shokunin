# R34ReopenSources — re-open S064/S065/S066 (round 34 W2, 2026-10-23)

Read-only on lane; experiments in `/fast/scratch/hyaku/chousa-r34/w2/R34ReopenSources/` (`LC_ALL=C`). All paths below relative to the lane repo unless absolute.

## Pins verified for all three rows

- `man -w execve pcre2limits grep` → `/usr/share/man/man2/execve.2.gz`, `/usr/share/man/man3/pcre2limits.3.gz`, `/usr/share/man/man1/grep.1.gz` (exit 0) — matches every row's anchor path.
- `sha256sum`: execve.2.gz `4489dfef246682d18365712ce686f3519318b074761f249091c5fc99c8eab0dc`; pcre2limits.3.gz `a3ea2c67c102af649be069fd31bb6b658c2170f15bc1a1728f464fd8e5974bd6`; grep.1.gz `9b027d022ae9533ff3e140ba8d96ccd58955bdf9d1c818c327fd992e575c85ba` — all three equal the row values.
- `pacman -Q man-pages pcre2 grep` → `man-pages 6.19-1`, `pcre2 10.49-1`, `grep 3.12-2` — all match the rows.

## S064 — Linux man-pages execve(2) — verdict: FIX (anchor label only)

- Quote verbatim at decompressed lines 422–424: 422 `Additionally, the limit per string is 32 pages (the kernel constant`, 423 `.BR MAX_ARG_STRLEN ),`, 424 `and the maximum number of strings is 0x7FFFFFFF.` = the row's 20-word gate quote; `grep -n MAX_ARG_STRLEN` → line 423.
- Teaches statement true: `.SS "Limits on size of arguments and environment"` (decompressed line 365) gives the aggregate limit (1/4 stack, 3/4 `_STK_LIM`, 32-page floor, lines ~414–421) and then the per-string 32-page `MAX_ARG_STRLEN` — the distinction the row claims.
- **DEFECT**: anchor label `NOTES` is wrong. `.SH` map of `zcat /usr/share/man/man2/execve.2.gz`: `.SS "Limits on size of arguments and environment"` :365, `.SH RETURN VALUE` :425, `.SH NOTES` :639 — lines 422–424 are in the `.SS`, not NOTES. Rendered page agrees: quote at `man -P cat 2 execve` lines 239–241; rendered `NOTES` at :382. The scribe file `.ufo/waves/round-34/w1/ScribeSrcExecve.md` repeats the same mislabel ("decompressed …:639 (`NOTES`), `:422-424`") — :639 is where NOTES is, but the quoted text is not in it.
- Host fact reproduced (`fork`+`execve('/bin/true', …, {})`, empty env): arg 131071 B (incl NUL = 131072) → exit 0 exec OK; arg 131072 B (incl NUL = 131073) → E2BIG. Boundary exactly 131072 bytes including NUL ✓.
- **Fix**: replace anchor label `NOTES` with `DESCRIPTION → "Limits on size of arguments and environment"` (decompressed lines 422–424; rendered 239–241). No other change; do not reject.

## S065 — PCRE2 pcre2limits(3) — verdict: ADMIT

- `.TH PCRE2LIMITS 3 "03 September 2025" "PCRE2 10.49"` matches "PCRE2 10.49 (03 September 2025)"; anchor section `SIZE AND OTHER LIMITATIONS` exists (decompressed :4).
- Both scribe quotes verbatim: :10–11 `The maximum size of a compiled pattern is approximately 64 thousand code units / for the 8-bit and 16-bit libraries` (19 words); :23 `The maximum length of a source pattern string is essentially unlimited` (11 words). Row paraphrase ("effectively unlimited", "~64-thousand-code-unit … default 8/16-bit") matches the default-linkage-2 text.
- Host experiment (`/usr/bin/grep`, `LC_ALL=C`, pattern file of `\x41`×N, input `A\n`): span 32763 → rc 1 (compiles); **32764 → rc 1 (compiles)**; **32765 → rc 2, stderr `/usr/bin/grep: regular expression is too large`**; 32766 → rc 2. With a matching input of 32764×`A`: rc 0, 1 line matched. Exactly the row's 32,764 accepted / 32,765 rejected and the exact error string.
- Argv workaround claim reproduced: `\x41`×32767 as ONE argv string (131069 B incl NUL) execs (then fails at the PCRE ceiling, rc 2); `\x41`×32768 (131073 B incl NUL) → E2BIG. "Four-character escape per byte does not remove the compiled-size limit" ✓.

## S066 — GNU grep(1) — verdict: ADMIT

- `.TH GREP 1 \*(Dt "GNU grep 3.12-modified"` + `.dT Time-stamp: "2025-03-21"` matches "3.12-modified (2025-03-21)"; `pacman -Qo /usr/bin/grep` → owned by `grep 3.12-2`, same package owns `man1/grep.1.gz` (`pacman -Ql`).
- Anchor sections all exist with the options inside them (roff line numbers of the decompressed page): `.SS "Pattern Syntax"` :200 (`-F` entry :208–211, in section), `.SS "Matching Control"` :228 (`-f` entry :241–243), `.SS "Other Options"` :716 (`-z` entry :747–749). There is no "Matcher Selection" `.SS` in this man page, so "OPTIONS / Pattern Syntax" is the correct home of `-F`/`-P`.
- Quotes verbatim (roff-unwrapped): `Interpret PATTERNS as fixed strings, not regular expressions.`; `Obtain patterns from FILE, one per line.`; `Treat input and output data as sequences of lines, each terminated by a zero byte (the ASCII NUL character) instead of a newline.` — all match the scribe quote list (`.ufo/waves/round-34/w1/ScribeSrcPcre2/rows.md` lines 9–14).
- Teaches statements supported by the cited text (one-pattern-per-line ⇒ newline-containing span cannot be one `-f` pattern [INFERENCE, marked as such in the row]; `-z` text says nothing about the `-f` delimiter).
- Environment note (no row change): in the agent shell bare `grep` is a `grep (pi-uu-grep) 0.2.0` shell builtin (`type -a grep`), NOT GNU grep; both rows correctly pin `/usr/bin/grep` (GNU grep 3.12-modified, 158000-byte ELF, root-owned). Future re-checks must use `/usr/bin/grep` or `command grep`.

## Census validate

`timeout 300 /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` →
```
chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
EXIT=0
```
Exit code 0. The two W04 warnings are pre-existing and unrelated to S064–S066 (S051/S053).

## Used-by backlink

`corpus/knowledge/long-span-argv-r34.md` exists (4705 bytes, 2026-10-23 09:17; 5 references to S064/S065/S066) — the scribe's "provisional backlink" caveat in rows.md is resolved; all three rows' used-by paths are live and cited.

## Residual risk / gaps

- Upstream man7.org URL for S064 was not fetched (no network; row itself says "the URL was not fetched") — sha256 pins the installed copy only.
- The 32764/32765 grep -P boundary and 131072 argv boundary are host+build facts (pcre2 10.49 default linkage 2, man-pages 6.19 kernel text); the on-release recheck should re-pin package versions before re-trusting the numbers.
- No production files touched; no installs performed.
