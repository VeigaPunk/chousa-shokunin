# ScoutC2Package — provenance of the openat2 sources (round 62, w1)

Seat: ScoutC2Package (scout, leaf). Lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`. Read-only; no install, no write outside this report and scratch.
Frozen claims file sha256 `a3193ebd328919e2af017011278e423c5940fd9447f0730bd400da9d15c866bc` — matches the value in the item.

## Findings

1. **Both sources are the installed package copies.** Owners and build-date mtimes match exactly:
   - `/usr/share/man/man2/openat2.2.gz` — owned by `man-pages 6.19-1`; mtime `2026-08-27 11:12:38`, equal to the package Build Date `Thu 27 Aug 2026 11:12:38 AM -03`.
   - `/usr/include/linux/openat2.h` — owned by `linux-api-headers 7.2-1`; mtime `2026-08-17 05:45:56`, equal to Build Date `Mon 17 Aug 2026 05:45:56 AM -03`.
   Byte identity to the package archives was **not** run: `/var/cache/pacman/pkg` holds 10 files, none for these packages. Ownership plus mtime equality is the evidence; byte identity is INFERENCE.
2. **Man page `.TH` line** (zcat, line 6): `.TH openat2 2 2026-07-02 "Linux man-pages 6.19"`. The copyright and SPDX lines are present (`Linux-man-pages-copyleft`). The lane row S138 gives the release as "6.19 (2026-02-08)"; that date is not in the page or package and I could not check it locally — **unverified**.
3. **Shadowing: none found for the man page.** `MANPATH` is unset. `man -aw openat2` lists only `/usr/share/man/man2/openat2.2.gz`. The `manpath` search list (`/usr/local/man`, `/usr/local/share/man`, `~/.local/share/man`, the mise and fnm `share/man` trees, `/usr/lib/jvm/default/man`) contains no `openat2*` file (find, 0 hits each).
4. **Header include path resolves to the package copy.** `cpp -v` search list: `/usr/lib/gcc/.../include`, `/usr/local/include`, `/usr/include`. `/usr/local/include` has no openat2 file, so `<linux/openat2.h>` resolves to `/usr/include/linux/openat2.h`.
5. **Other openat2 copies on this host (not the S139 source):**
   - `/usr/include/bits/openat2.h` — owned by `glibc 2.44+r50+g1848099f063e-1`; sha256 `1b89059b…18f5a`; its comments differ from the uapi header (for example, RESOLVE_NO_SYMLINKS reads "Block traversal through all symlinks." with no OEXT remark).
   - `/usr/lib/modules/7.2.11-arch1-1/build/include/uapi/linux/openat2.h` — owned by `linux-headers 7.2.11.arch1-1`. `diff` against the S139 file shows only include-guard name lines differ (`_LINUX_OPENAT2_H` vs `_UAPI_LINUX_OPENAT2_H`): the flag comments are identical.
   - `/usr/lib/modules/6.18.57-2-lts/build/...` — owned by `linux-lts-headers 6.18.57-2`, not compared further.
6. **Quote check (exact substring after whitespace normalisation):**
   - Rendered as the lane does, `MANWIDTH=1000 man -l FILE | col -bx`: Q1, Q2, Q3, Q4, Q5 all **EXACT**.
   - Rendered with default `man 2 openat2 | col -b`: Q1–Q4 **ABSENT** (words split with a soft hyphen at the wrap, e.g. "directo‐ ries"); Q5 EXACT. The text is the same page; only the wrap differs. The access disclosure must state the lane's render method.
   - Q6 (header comment on RESOLVE_NO_SYMLINKS, "Block traversal through all symlinks (implies OEXT_NO_MAGICLINKS)") is **EXACT** in `/usr/include/linux/openat2.h` (one match, whitespace-normalised). The `OEXT_NO_MAGICLINKS` token is **not defined anywhere** in `/usr/include` (grep: only that comment). It is a typo in the upstream comment. Any entry that quotes it must keep the typo, and must not rewrite it as `RESOLVE_NO_MAGICLINKS` (a misquote).
7. **Material contradiction: glibc on this host does have an openat2 wrapper.** The lane quote Q5 ("glibc provides no wrapper for openat2(), necessitating the use of syscall(2).") is exact text of man-pages 6.19, but the installed glibc disagrees:
   - `readelf -Ws --dyn-syms /usr/lib/libc.so.6` → `2928: 0000000000112aa0 233 FUNC WEAK DEFAULT 13 openat2@@GLIBC_2.43`.
   - Prototype in `/usr/include/bits/fcntl-linux.h:485`: `extern int openat2 (int __dfd, const char * __filename, const struct open_how * __how, __SIZE_TYPE__ __usize) __nonnull ((3));` (GNU-only block).
   - Live call via ctypes to `libc.openat2(-100, b"/usr/include/linux/openat2.h", &how{O_RDONLY, 0, RESOLVE_NO_SYMLINKS}, sizeof)` → returned fd 3, errno 0. Run in `/fast/scratch/hyaku/chousa-r62/ScoutC2Package/ctest.py`; read-only open, fd closed.
   - Consequence: `corpus/knowledge/openat2-resolve-r62.md` Claim 4 ("glibc has no wrapper") and the S138 row's "glibc has no wrapper" must not be stated as current fact for this host. The probe's P01 checks only Python's `os` module, not libc, so it does not contradict the wrapper. INFERENCE: the 6.19 page predates the glibc 2.43 wrapper; I did not verify glibc's release history offline.
8. **Install dates and versions (pacman query, read-only):**
   - `man-pages 6.19-1` — Install Date `Tue 20 Oct 2026 01:07:12 AM -03`, explicitly installed, Packager Andreas Radke.
   - `linux-api-headers 7.2-1` — Install Date `Sun 11 Oct 2026 04:14:18 PM -03`, dependency install, Packager Frederik Schwan.
   - `glibc 2.44+r50+g1848099f063e-1` — Install Date `Tue 20 Oct 2026 09:16:27 AM -03`, Build Date `Sun 27 Sep 2026 01:35:47 PM -03`.
   - Kernel: `7.2.11-arch1-1` (per the probe output and `uname`).

## Access disclosure (for the registry rows S138, S139 and the lesson Gate)

> Access: local installed copies only, no network. S138 = `/usr/share/man/man2/openat2.2.gz` (man-pages 6.19-1, pacman-owned, mtime = package build date 2026-08-27), rendered `MANWIDTH=1000 man -l FILE | col -bx`; default-width render splits words at soft hyphens. S139 = `/usr/include/linux/openat2.h` (linux-api-headers 7.2-1, pacman-owned, mtime = build date 2026-08-17), read as a file. Not checked against man7.org, kernel.org or the package archives (archives not cached). The installed glibc 2.44 exports `openat2` (GLIBC_2.43), so the page's "no wrapper" statement is out of date for this host.

## Recommended row and entry edits (for L1 and the drafters; not applied here)

- S138: append to the claim column that glibc 2.44 on the host exports `openat2` (GLIBC_2.43), contradicting the page's SYNOPSIS note; the quote stays as the page's own words.
- Entry Claim 4: drop "because glibc has no wrapper" or qualify it as "per man-pages 6.19; the installed glibc 2.44 exports a wrapper".
- Keep the `OEXT_NO_MAGICLINKS` typo verbatim in any Q6-style quote; do not normalise it.
- Cite S139 only for the `/usr/include/linux/openat2.h` path; the glibc copy in `bits/` has different comment text.

## Checks run (all recorded above)

- `pacman -Qi man-pages linux-api-headers`, `pacman -Qi glibc` (query); `pacman -Qo` on both files and on the three extra copies; `pacman -Q glibc`.
- `man -w 2 openat2`, `man -aw openat2`, `printenv MANPATH` (unset), `manpath`, `ls` and `find` over the manpath directories.
- `zcat` for the `.TH` line and copyright lines; `sha256sum` on the header and the decompressed page.
- Quote check script `quotes.py` (Q1–Q6) on `man -l | col -bx` output, the default render, and the header.
- `cpp -v` include search list; `nm`/`readelf` on `libc.so.6`; ctypes openat2 call (fd 3).
- No tool was installed or upgraded. No pacman transaction was run.

VERDICT: SOURCES_ARE_PACKAGE_COPIES=yes man_pages=1 headers=1
