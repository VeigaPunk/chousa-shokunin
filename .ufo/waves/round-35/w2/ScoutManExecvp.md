# ScoutManExecvp — execvp(3) PATH search (S067)

Access date: 2026-10-23. No packages installed. Read-only (`sha256sum`, `gzip -dc`, `pacman -Qo`, `man -w`, `whatis`).

Axes: operability (open, hash, decompress, owner) and calibration (quote ≤25 words; do not claim left-to-right PATH order the page does not state).

## Page identity

`/usr/share/man/man3/execvp.3.gz` is present (36 bytes, not a symlink). It is a groff inclusion stub, not the prose.

| object | sha256 | size | decompressed lines |
|---|---|---|---|
| `/usr/share/man/man3/execvp.3.gz` | `1bff7db3bb4c757e5556d93cb3ac34dafd5903790f643025536cc07fd7c60127` | 36 | **1** |
| decompressed stub | `8665a5ec911df0c01d95d34b83454f98d9a09e269f8ee9e787f379cd56129a89` | 16 | 1 |
| `/usr/share/man/man3/exec.3.gz` (`man -w execvp`) | `2f1badd36afd699bbe4e62ff36d810a99ed5e2b4476747b168e33ba5ed1b1523` | 3043 | **305** |
| decompressed `exec.3` | `c3aa636364ec193306aadbebd7f866c5ea58c62f02e645e87fcd44f3f2e0f098` | 7699 | 305 |

Decompressed stub, line 1: `.so man3/exec.3`

`man -w execvp` → `/usr/share/man/man3/exec.3.gz` (exit 0). `whatis execvp` also lists `exec (3p)`; that POSIX page was not opened. Line counts are `gzip -dc | wc -l` (stub 1, exec.3 305) and newline counts on the saved decompressions (1 and 305; both end in newline).

Copies: `.ufo/waves/round-35/w2/ScoutManExecvp/execvp.3.txt`, `.ufo/waves/round-35/w2/ScoutManExecvp/exec.3.txt` (same bytes under `/tmp/hyaku/chousa-r35/w2/ScoutManExecvp/`).

## Owner

`pacman -Qo` (exit 0), both paths: **man-pages 6.19-1**. `pacman -Qi`: Linux man pages; packager Andreas Radke; install date Tue 20 Oct 2026 01:07:12 AM -03. mtime of both gz files: 2026-08-27 11:12:38 -0300.

## S067 quote (17 words)

Located in decompressed `/usr/share/man/man3/exec.3` lines 107–110 (included by `execvp.3.gz` line 1), section `.SS p - execlp(), execvp(), execvpe()`:

> The file is sought in the colon-separated list of directory pathnames specified in the PATH environment variable.

Source (nroff):

```
107:The file is sought in the colon-separated list of directory pathnames
108:specified in the
109:.B PATH
110:environment variable.
```

## Is PATH lookup order stated?

**Not for the `PATH` variable.** Lines 107–110 name a colon-separated list and do not say left-to-right, first component first, or first match wins. Line 135 says these functions "continue searching the rest of the search path" after `EACCES`, which implies a sequence but not its direction.

**Yes for the default path when `PATH` is unset.** Lines 196–200: the default "generally includes `/bin` and `/usr/bin` (in that order)". Lines 206–211: glibc used to put the current working directory "at the start of the search path"; glibc 2.24 dropped it. That is default-path order, not `PATH`-component order.

## Limits

Formatted `man execvp` line numbers were not used; counts are the decompressed roff source. `exec(3p)` was not read. No claim about glibc's actual walk order beyond this page.
