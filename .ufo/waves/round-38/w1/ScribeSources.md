# chousa-r38.ScribeSources

## Verdict

Both rows drafted from locally opened bytes (no network). S072 excludes the `BASH_FUNC_*` encoding
bash.info never documents; S073 confirms S070's defect is a **section-label** error — `-c, --check`
sits under `.SH DESCRIPTION` (line 8), not `.SH SYNOPSIS` (line 5, ending at 7, no option entries).

## Evidence

Lane tip (read-only): `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master` →
`504c1d2a1257a9ac6e5d752dcaf3f0bb0a35d05f`, matching dispatch. Registry has 71 rows
(`grep -c '^| S' corpus/SOURCES.md` → `71`); `grep -n '| S072 \|| S073 '` → no output, both ids free.
Seeds: none — this seat ran no counter (Limits).

**S1 — bash.info identity and node.** `sha256sum /usr/share/info/bash.info.gz` →
`cde1a3366897684b0a86fe553687e31d070b7839b19ca98186ffc6e0e105588f` (167064 bytes); repeated with
`/usr/bin/sha256sum` → same digest. `zcat … | sed -n '1303,1312p'` → line 1307
`File: bash.info,  Node: Shell Functions,  Next: Shell Parameters,  Prev: Shell Commands,  Up: Basic Shell Features`,
line 1309 `3.3 Shell Functions`. `zcat … | sed -n '1,7p'` → "produced by makeinfo version 7.2 from
bashref.texi", "Bash shell (version 5.3, 18 May 2025)", "This is Edition 5.3, last updated 18 May 2025".

**S2 — the exported-functions sentence.** `zcat /usr/share/info/bash.info.gz | sed -n '1459,1464p' | nl -v1459 -ba` →

```
1459  to ‘declare’ or ‘typeset’ lists the function names only (and optionally
1460  the source file and line number, if the ‘extdebug’ shell option is
1461  enabled).  Functions may be exported so that child shell processes
1462  (those created when executing a separate shell invocation) automatically
1463  have them defined with the ‘-f’ option to the ‘export’ builtin (*note
1464  Bourne Shell Builtins::).  The ‘-f’ option to the ‘unset’ builtin (*note
```

Sentence start is 1461 ("Functions may be exported…"), terminator "Bourne Shell Builtins::)." on
1464: verified range **1461–1464**. The 25-word budget forces one elision; the row's quote is 22
words by `printf '%s\n' '<quote>' | wc -w` (the `…` counted as a token; full sentence 29 words):

> Functions may be exported so that child shell processes … automatically have them defined with the ‘-f’ option to the ‘export’ builtin

**S3 — bash.info does not document the env encoding.** `zcat … | grep -n 'BASH_FUNC|imported function|exported function|environment.*function'`
→ only `2406` (subshell environment prose) and `3603` ("exported functions", `declare -p`). No
`BASH_FUNC` line anywhere, so the `name%%` encoding is not anchorable to this manual.

**S4 — sha256sum page section map.** `sha256sum /usr/share/man/man1/sha256sum.1.gz` →
`93c17dffe9f25d56291113d566a7de3ff65c29f8cc32c381801c49cf27e8403f` (same via `/usr/bin/sha256sum`).
`zcat … | grep -n '^\.SH'` → `3:.SH NAME · 5:.SH SYNOPSIS · 8:.SH DESCRIPTION · 61:.SH AUTHOR ·
63:.SH "REPORTING BUGS" · 71:.SH COPYRIGHT · 77:.SH "SEE ALSO"`. `zcat … | sed -n '1,25p' | nl -ba`
gives SYNOPSIS body lines 6–7 only (`.B sha256sum`, `[\fI\,OPTION\/\fR]... [\fI\,FILE\/\fR]...`),
DESCRIPTION at 8–9 with quote line 11 `Print or check SHA256 (256\-bit) checksums.`, then `.TP`
entries from 15: `-b, --binary` at 16–17, **`-c, --check` at 19–20** (tty-link target `#cksum-c`).
Lines 54–58 (FIPS-180-2 / output format) stay inside DESCRIPTION; header `.TH SHA256SUM "1"
"September 2026" "GNU coreutils 9.12" "User Commands"`; installed `coreutils 9.12-2`.

### Draft SOURCES.md rows (contract v1, 11 columns, no `|` in cells)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S072 | GNU Bash Reference Manual, `bash.info` (Bash Edition 5.3) — `/usr/share/info/bash.info.gz` | docs | A | the manual's own statement that shell functions may be exported to child shells; not the `BASH_FUNC_*` environment encoding (absent from this manual) and not this lane's gate pinning | Node `Shell Functions` (3.3), node header and heading at decompressed lines 1307 and 1309; exported-functions sentence at 1461–1464, quote at 1461–1463; Bash Edition 5.3, 18 May 2025, produced by makeinfo 7.2 from bashref.texi; installed `bash 5.3.20-1`; file SHA-256 `cde1a3366897684b0a86fe553687e31d070b7839b19ca98186ffc6e0e105588f` (opened locally 2026-10-24) | The manual states that functions may be exported so that child shell processes automatically have them defined, so a caller-exported function reaches every child shell invocation; it does not document the `BASH_FUNC_name%%` encoding such a child receives. | queued | 2026-10-24 | on-release | — |
| S073 | GNU coreutils `sha256sum(1)` manual — `/usr/share/man/man1/sha256sum.1.gz` | docs | A | which man-page section carries the `-c, --check` option entry in the installed page (DESCRIPTION, not SYNOPSIS), plus the documented digest text and `--check` input; not a validation policy (the 64-lowercase-hex rule stays this lane's choice) | `.SH SYNOPSIS` at decompressed line 5 with body 6–7 and no option entries, versus `.SH DESCRIPTION` at line 8 with the `-c, --check` `.TP` entry at 19–20 (quote at 20) and the FIPS-180-2/format paragraph at 54–58; coreutils 9.12 (September 2026), installed `coreutils 9.12-2`; file SHA-256 `93c17dffe9f25d56291113d566a7de3ff65c29f8cc32c381801c49cf27e8403f` (opened locally 2026-10-24) | supersedes S070 — the installed page's `-c, --check` entry sits under `.SH DESCRIPTION` (line 8 onward) at lines 19–20, not under `.SH SYNOPSIS` (lines 5–7, which carries only the usage line), so S070's section label is wrong while its line numbers and its quoted line 11 are correct; `--check` reads checksums from files rather than computing a policy. | queued | 2026-10-24 | on-release | — |

### Draft round-38 lesson `## Gate` entries (for corpus/lessons/round-38.md)

Rows added this round: **S072**, **S073** (70 → 72 rows). Both opened locally on 2026-10-24; no network.

- **S072** GNU Bash Reference Manual `bash.info`, Node `Shell Functions` (3.3), header line 1307,
  heading 1309, sentence 1461–1464 with the quote at 1461–1463; Bash Edition 5.3, 18 May 2025;
  `bash 5.3.20-1`; file SHA-256 `cde1a336…588f`. Located quote (22 words incl. the elision token):
  "Functions may be exported so that child shell processes … automatically have them defined with
  the ‘-f’ option to the ‘export’ builtin". The manual documents export-and-inherit as a language
  feature but never the `BASH_FUNC_name%%` encoding, so that half stays the Erratum-5 measurement [INFERENCE].
- **S073** GNU coreutils `sha256sum(1)`, `.SH SYNOPSIS` line 5 (body 6–7) versus `.SH DESCRIPTION`
  line 8, `-c, --check` at 19–20 (quote at 20); coreutils 9.12-2; file SHA-256 `93c17dff…403f`.
  Located quote (7 words): "read checksums from the FILEs and check them". The correction is to the
  *label*, not the offsets: S070's 4–11, 19–20 and 54–56 verify, but 19–20 is a DESCRIPTION paragraph [INFERENCE].
- **Supersede bookkeeping:** S070 mined→queued, `used-by` metadata entries→`—`; the entry cites S073.
- **Rejected candidate:** `/usr/share/man/man1/bash.1.gz` for the same sentence — S068 holds the
  `BASH_ENV` anchor there and excludes exported-function behaviour; a second row is a duplicate.

## Findings

1. **Dispatched range off by one.** The assignment says 1460–1463; measured, 1460 ends the *previous*
   sentence and 1463 stops at `(*note`, so the span is 1461–1464 (S2) — the S069 fault class.
2. **S070's defect is a section label.** `.SH SYNOPSIS` is line 5 with body 6–7 and zero option
   entries; `.SH DESCRIPTION` opens line 8, the `-c, --check` `.TP` pair is 19–20 (S4), so S070's
   "SYNOPSIS `-c, --check`" misattributes it while its offsets and line-11 quote verify.
3. **`BASH_FUNC_*` is not in bash.info.** `grep` returns nothing (S3); the manual stops at "may be
   exported … have them defined", so S072 cannot launder the Erratum-5 measurement into a citation.
4. **The harness shell interposes `sha256sum` as a builtin.** `type -a sha256sum` → `sha256sum is a
   shell builtin` then `/usr/bin/sha256sum`; the shell process is `omp` with
   `BASH_VERSION=5.2.37(1)-release`, while the package is `bash 5.3.20-1` and
   `/usr/bin/sha256sum --version` is `sha256sum (GNU coreutils) 9.12`. Both resolvers returned
   identical digests for both files (S1, S4), so the row hashes are sound — but a capture path
   calling bare `sha256sum` under this shell is **not** running coreutils 9.12, the interposition
   class C1's absolute-`env` pin exists to remove — a harness-shell observation; the gate was not run.
5. **Manual version ≠ running version.** Page says Bash 5.3 / 18 May 2025, package `bash 5.3.20-1`,
   harness shell 5.2.37. S072's anchor records the *page's* identity; claims about the executing
   shell need their own witness.
6. **`used-by` is `—` deliberately.** `ls corpus/knowledge/ | grep -i 'r38|round38'` is empty, so no
   round-38 entry exists to cite either row; both enter `queued` on the S030 precedent (supersede
   rows become `mined` only when cited). L1 flips S073 and S070 together if an entry cites it.
7. **Frozen claims file edited in place mid-run (not mine).** `git diff --stat
   corpus/evidence/round38/claims.md` → `1 file changed, 6 insertions(+)`; the added bullet opens
   "C1's env pin does not scrub the loader environment of the `env` child". That file permits only an
   appended erratum, never an in-place edit; no write of this seat touched it.

## Limits

- No gate, counter or verifier was run (`c1-count.py`, `c2-count.py`, `verify-receipts.py` untouched);
  no seed is claimed. The C1/C2 predicates are other seats' evidence; finding 4 is not a measurement.
- No network fetch; both sources are installed copies. The page prints a
  `https://www.gnu.org/software/coreutils/...` tty-link at the anchored lines, **not** fetched.
- Rows and Gate entries are **drafts in this report only**; `corpus/SOURCES.md`,
  `corpus/lessons/round-38.md` and the jj/git state were not written. No census `validate` ran, so
  the 70 → 72 count is arithmetic on `grep -c` = 71 current rows, not a receipt.
- Line numbers are decompressed-stream positions from `zcat` (13752 lines for bash.info, 83 for the
  man page), stable across repeated calls this session; not gzip byte offsets.
- Finding 4's `omp` identity (`ps -p $$ -o comm=` → `omp`, `BASH_VERSION=5.2.37`) is one
  observation of this seat's tool shell; shadowability by function, alias or absolute path in any
  gate code path was not tested.
- No tool installed or upgraded (no pacman, uv, cargo, npm transaction); nothing to record.
