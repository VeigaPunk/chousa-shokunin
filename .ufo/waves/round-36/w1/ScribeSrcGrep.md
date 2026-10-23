# ScribeSrcGrep — S069 source draft report

**Verdict: PASS — S069 row draft and Gate entry are complete; no gate/runtime behavior was evaluated.**

## Findings

The installed GNU grep manual supports the scoped source claim: `-o` prints each nonempty matching part on a separate output line (decompressed `grep.1` lines 366–368); in the `-b` description, when `-o` is specified it prints the matching part's offset (lines 387–391); and `-a` processes a binary file as text (lines 509–512). The exact relevant option-section names are **OPTIONS / General Output Control**, **OPTIONS / Output Line Prefix Control**, and **OPTIONS / File and Directory Selection**. The located quote is: “If -o (--only-matching) is specified, print the offset of the matching part itself.” (`/usr/share/man/man1/grep.1.gz`, decompressed lines 387–391; 13 words).

`pacman -Q grep` reported `grep 3.12-2`; the local manual's SHA-256 is `9b027d022ae9533ff3e140ba8d96ccd58955bdf9d1c818c327fd992e575c85ba`. The opened registry has S066 for a distinct GNU grep scope (`-f`/`-F`/`-P`/`-z`) and S068 immediately before this assigned S069 row. The relevant manual sections document option semantics, not per-record argv attribution as a method; that method is lane-specific and is not claimed as GNU documentation.

## Commands and outcomes

All commands were run with the shown timeout. Exit status is 0 for each.

1. `timeout 900s pacman -Q grep` — output/decisive line: `grep 3.12-2`.
2. `timeout 900s sha256sum /usr/share/man/man1/grep.1.gz` — output: `9b027d022ae9533ff3e140ba8d96ccd58955bdf9d1c818c327fd992e575c85ba  /usr/share/man/man1/grep.1.gz`.
3. `timeout 900s file /usr/share/man/man1/grep.1.gz && timeout 900s gzip -l /usr/share/man/man1/grep.1.gz` — `file` identified gzip data with uncompressed size 32480 bytes; `gzip -l` reported 10954 compressed / 32480 uncompressed bytes. The manual was read through its `grep.1` member, which exposed decompressed source line numbers.
4. `timeout 900s mkdir -p /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ScribeSrcGrep` — no output; directory created.
5. `timeout 900s sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ScribeSrcGrep/row-draft.md` — exit 0 before the final edit; interim digest `a1506df742928fb48fed4f96edcae69a3d326797abee68d56f4f3eaab8d55429` is superseded.
6. `timeout 900s sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ScribeSrcGrep/row-draft.md` — final output: `440b31578e46c7911950230a729ceed4df8ce0b487edddc92a749de460a42332  /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ScribeSrcGrep/row-draft.md`.

The manual section/option searches located `.SH OPTIONS` at line 190; `.SS "General Output Control"` at 289, `-o` at 366–368; `.SS "Output Line Prefix Control"` at 382, `-b` and the quoted clause at 384–391; and `.SS "File and Directory Selection"` at 507, `-a` at 509–512.

## Files opened

Access date for all entries: 2026-10-23.

- `/home/vgpnk/.agents/skills/godspeed/SKILL.md`.
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1-briefs/ScribeSrcGrep.md`.
- `/usr/share/man/man1/grep.1.gz` (read as member `grep.1`; relevant decompressed lines above).
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md` (registry schema and rows S066–S068).
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/grep-pin-r35.md`.
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/long-span-argv-r34.md`.
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ScribeSrcGrep/row-draft.md` (drafted and read before its final wording correction; final artifact hash below).

An explicit read of the brief's intended backlink `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/per-record-argv-attribution-r36.md` returned “not found.” The row carries the brief-specified `used-by` path as the intended linkage, not as a claim that this knowledge entry exists.

## Touched surfaces, gates, and limits

- Created only the scoped row draft; no lane production file, registry, gate, counter, claim, judge, or Git/JJ state was changed.
- No gate, selftest, C1/C2 counter, or behavioral experiment was run; this report is source-row evidence only. No network or package installation was used.
- Out of scope: appending the row to `corpus/SOURCES.md`, writing the intended knowledge entry, and any C1/C2 re-derivation.

## Artifact

- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ScribeSrcGrep/row-draft.md` — SHA-256 `440b31578e46c7911950230a729ceed4df8ce0b487edddc92a749de460a42332`.
