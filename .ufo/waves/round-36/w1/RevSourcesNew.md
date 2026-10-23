# RevSourcesNew — non-author verification of SOURCES rows S069 and S070

Seat: `L1chousa36.RevSourcesNew-2` (residual reviewer, round 36). Read-only on all
production files. All decompression and inspection done in
`/tmp/hyaku/chousa-r36/r1/RevSourcesNew-2/`. Every command ran under `timeout`;
nothing installed (no tool was needed beyond coreutils/gzip already present).

## S069 — GNU `grep(1)` manual, `/usr/share/man/man1/grep.1.gz`

**File hash** — VERBATIM.
- Row claims `9b027d022ae9533ff3e140ba8d96ccd58955bdf9d1c818c327fd992e575c85ba`.
- Measured `sha256sum /usr/share/man/man1/grep.1.gz` →
  `9b027d022ae9533ff3e140ba8d96ccd58955bdf9d1c818c327fd992e575c85ba` — identical.

**Anchor / line numbers** — VERBATIM.
- `.SS "Output Line Prefix Control"` sits at decompressed line 382.
- `.BR \-b ", " \-\^\-byte\-offset` at line 384; paragraph runs 383–391 (the cited
  382–391 window includes the section header — generous but exact).
- Quote at lines 387–391, observed bytes:
  ```
  If
  .B \-o
  .RB ( \-\^\-only\-matching )
  is specified,
  print the offset of the matching part itself.
  ```
  i.e. "If -o (--only-matching) is specified, print the offset of the matching
  part itself." Line 385–386 adds "0-based byte offset within the input file".

**Version strings in anchor** — VERBATIM.
- Line 5: `.dT Time-stamp: "2025-03-21"`; line 12:
  `.TH GREP 1 \*(Dt "GNU grep 3.12-modified" "User Commands"`.
- `pacman -Q grep` → `grep 3.12-2`. All three claims match.

**teaches** — supported, no overreach.
- Claimed: "With `-o` in effect, `-b` prints the byte offset of the matching part
  itself, so a matcher's `-o -b` output locates a match inside the input bytes."
- First clause is the quote verbatim. The second clause ("locates a match inside
  the input bytes") is the direct consequence of lines 385/391 ("0-based byte
  offset within the input file" / "offset of the matching part itself") — an
  implication, not a new claim. The page does not say more than this (e.g. no
  `-z` record semantics), and the row does not claim it does.
- Scope guard verified: S066 is indeed the pattern-file/`-F`/`-P`/`-z` row on the
  same file, so the "distinct scope" note is accurate.

**used-by** — `corpus/knowledge/per-record-argv-attribution-r36.md` exists and
cites `S069` at lines 6 and 29, quoting the same `-o`/`-b` semantics.

**Verdict: VERBATIM.**

## S070 — GNU coreutils `sha256sum(1)` manual, `/usr/share/man/man1/sha256sum.1.gz`

**File hash** — VERBATIM.
- Row claims `93c17dffe9f25d56291113d566a7de3ff65c29f8cc32c381801c49cf27e8403f`.
- Measured → `93c17dffe9f25d56291113d566a7de3ff65c29f8cc32c381801c49cf27e8403f` —
  identical.

**Anchor / line numbers** — VERBATIM, with one cosmetic nit.
- Lines 4–11: line 4 `sha256sum \- compute and check SHA256 message digest`
  (NAME body under `.SH NAME` at line 3); quote at line 11 observed verbatim:
  `Print or check SHA256 (256\-bit) checksums.`
- Lines 19–20: `\-c, \-\-check` / "read checksums from the FILEs and check them"
  — exact.
- Lines 54–56: "The sums are computed as described in FIPS-180-2." / "When
  checking, the input should be a former output of this program." / "The default
  mode is to print a line with: checksum, a space," — exact.
- Nit (not a drift): the anchor calls lines 19–20 "SYNOPSIS `-c, --check`", but
  the page's `.SH SYNOPSIS` is only lines 5–7 (`sha256sum [OPTION]... [FILE]...`)
  and the `-c` text physically sits under `.SH DESCRIPTION` (line 8). Every
  cited line number is exact; only the section label for that one span is off.

**Version strings in anchor** — VERBATIM.
- Line 2: `.TH SHA256SUM "1" "September 2026" "GNU coreutils 9.12" "User Commands"`.
- `pacman -Q coreutils` → `coreutils 9.12-2`. Match.

**teaches** — supported, no overreach.
- Claimed: "`sha256sum` prints or checks SHA256 (256-bit) checksums, and
  `--check` reads checksums from files rather than computing a policy."
- First clause is line 11 verbatim. Second clause is line 19–20 verbatim plus
  the row's own scope disclaimer ("not a validation policy — the
  64-lowercase-hex rule is this lane's choice"), which correctly does not
  attribute the policy to the page. The page states no policy; the row claims
  none.

**used-by** — `corpus/knowledge/engine-swap-canary-r36.md` exists and cites
`S070` at lines 6 and 42 ("S11 rests on S070's text: `sha256sum` prints or
checks SHA256 (256-bit) checksums…").

**Verdict: VERBATIM** (with the SYNOPSIS→DESCRIPTION label nit noted above).

## Census

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate
--root /home/vgpnk/Projects/shokunin chousa` — **exit 0**. Full output:

```
chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
```

Two warnings, both W04 duplicate-URL on pre-existing rows S051 and S053 —
neither touches S069 or S070. Observation [INFERENCE]: S066 and S069 share the
same local path `/usr/share/man/man1/grep.1.gz` yet no W04 fired, so the
duplicate check appears to key on URL-shaped sources only, not local paths —
consistent with the rows' explicit "distinct scope" split rather than an
unflagged defect.

## Frozen claims.md

`corpus/evidence/round36/claims.md` §Erratum (from line 157, 71 lines scanned)
contains no source-row errata and no mention of S069/S070 — nothing appended
there alters these rows.

## Summary

| row | hash | lines | quote | teaches | used-by | verdict |
|---|---|---|---|---|---|---|
| S069 | match | exact | verbatim | supported | cites S069 | VERBATIM |
| S070 | match | exact (1 label nit) | verbatim | supported | cites S070 | VERBATIM |

Census: exit 0, 2 W04 warnings (S051, S053 only).
