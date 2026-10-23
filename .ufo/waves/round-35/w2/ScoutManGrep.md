# ScoutManGrep — grep(1) vs the C1 pin (round 35 v2)

Access date: 2026-10-23. No gate was scored. No install.

## Verdict

`grep(1)` documents `-z` (NUL-delimited records), `-P` (PCRE), and `--version`, and it does **not** state which binary is invoked. That silence is part of the C1 limit: the pin matches a self-reported version string, not a path the manual names. Not a MEETS (no counter run; the page supplies no engine).

Confidence: high on the three quotes and on the absence of a path. [INFERENCE] the page therefore cannot close the pin's "binary that lies about `--version`" gap (`tools/research-gate.sh` lines 346–347, 358–366).

## Page identity

| item | value |
|---|---|
| path | `/usr/share/man/man1/grep.1.gz` (canonical; `readlink -f` same) |
| sha256 | `9b027d022ae9533ff3e140ba8d96ccd58955bdf9d1c818c327fd992e575c85ba` |
| size / mtime | 10954 bytes, 2025-04-23 05:22:35 -0300 |
| owner | `pacman -Qo`: `grep 3.12-2` |
| decompressed | 1362 lines, 32480 bytes (matches `file` "original size modulo 2^32 32480") |
| decompressed sha256 | `f48970ff6a00e6c80a2affcd58a4460c0832d60efcbfc55f89fbe56716f613ef` |
| copy | `.ufo/waves/round-35/w2/ScoutManGrep/grep.1.txt` (same sha256) |
| source stamp | line 5 `Time-stamp: "2025-03-21"`; line 12 `.TH` center `"GNU grep 3.12-modified"` |
| formatted `man -P cat grep` | 620 lines, sha256 `d813d5c4d628fd89345c34e51a0aa60da14ffeabcc1386c10a63f9131af650b7` (scratch `/tmp/hyaku/chousa-r35/w2/ScoutManGrep/grep.1.fmt.txt`) |

Commands: `sha256sum /usr/share/man/man1/grep.1.gz`; `gzip -dc` into the copy above; `wc -l`.

## Three claims (decompressed source lines; rendered text matches)

One quote each, ≤25 words. Source: `/usr/share/man/man1/grep.1.gz` decompressed, access 2026-10-23.

**-z / NUL-delimited.** Lines 746–748 (formatted man lines 318–320). 23 words.

> Treat input and output data as sequences of lines, each terminated by a zero byte (the ASCII NUL character) instead of a newline.

Option head is line 746: `-z, --null-data`.

**-P / PCRE.** Lines 218–221 (formatted man lines 42–43). 7 words.

> Interpret PATTERNS as Perl-compatible regular expressions (PCREs).

Option head is line 218: `-P, --perl-regexp`.

**--version.** Lines 196–199 (formatted man lines 27–28). 8 words. `-V` is the short form (line 196).

> Output the version number of grep and exit.

The page does not prescribe the first-line grammar the pin matches (`*"GNU grep"*`, `grep_pin_verify`). The `.TH` title "GNU grep 3.12-modified" (line 12) is the manual's name, not a specified `--version` string.

## Which binary (C1 limit)

The page does not state which binary is invoked. Case-insensitive counts on the 1362-line source: `pathname` 0, `/usr/bin` 0, `/bin/grep` 0, `PATH` 0, `invoke`/`invoked` 0, `executable` 0, `builtin` 0, `argv` 0. The 21 hits of `binary` are all about binary *files* (`--binary-files`, `-a`, `-U` / `--binary`), lines 510–727, not the executable path. SYNOPSIS (lines 141–159) names the command `grep` only.

Related page limits the pin does not check (same file, same date):

- Lines 222–227 (formatted 44–45), 19 words: "This option is experimental when combined with the -z (--null-data) option, and grep -P may warn of unimplemented features." The landed matcher uses both together (`grep -a -z -b -o -P`, `research-gate.sh` lines 1687 and 1716).
- Line 778 (formatted 338), 8 words: "but work only if PCRE support is enabled." A `--version` line is not that enablement.

## Host contrast (observed, not from the page)

This shell's `grep` is a builtin: `type grep` → `grep is a shell builtin`; `grep --version` first line `grep grep (pi-uu-grep) 0.2.0` (does not contain `GNU grep`). `/usr/bin/grep` and `/bin/grep` are byte-identical (`cmp`; sha256 `19280b0e0714dadf0c100cdbc7f4823d254dd8facba64deeff5ec50d39fecf84`) and `/usr/bin/grep --version` first line is `grep (GNU grep) 3.12-modified`. That split is why the pin exists; the manual does not mention it.

## Unresolved

Not run: `c1-count.py`, any override/refusal, whether a non-GNU binary can print `GNU grep` and still fail `-z`/`-P`. Those are outside this page.
