source: S164 — Microsoft Win32 file-naming rules (raw.githubusercontent.com/MicrosoftDocs/win32 at pinned commit 63e70903d18b0637e62ffab6656c4a388ef0f2ce, desktop-src/FileIO/naming-a-file.md, capture committed); S165 — the round-68 red receipts (corpus/evidence/round68/controls/before-freeze-default-root.txt, before-freeze-colon-case.txt, before-g06-preflight.txt, measured at the round-68 base)
verified-at: 2026-10-31 (Windows/11, python 3.13.15, git 2.55.0.windows.3; round-68 source opening)
recheck: on-release; re-run the r66 semantic counter on this entry and re-derive both receipts' TOOL_SHA256 pins with tools/digest-in-tree.py; re-open the S164 quote with tools/quote-reopen.py (corpus/evidence/round68/quote-reopen.tsv)

# Host-portable gate self-tests: derive the root, sanitize fixture names

## Question

What must a committed gate's self-invocation mode assume about the host it runs on, given that the fleet moved hosts and the gate's own selftest was the thing that broke (r67 preflight G06)?

## Located evidence

- S164, Naming Conventions, first sentence: "The following fundamental rules enable applications to create and process valid names for files and directories, regardless of the file system" — and the reserved-characters list immediately below it forbids nine characters in names: less-than, greater-than, colon, double quote, forward slash, backslash, vertical bar, question mark, asterisk (plus ASCII NUL and 1-31). A selftest fixture directory is a file-system name, so a case label is only a display string until `mk()` joins it under the temp base.
- S165, before-freeze-default-root.txt: the bare selftest died in `real(61)` with FileNotFoundError naming `/home/vgpnk/Projects/shokunin/chousa-shokunin\.ufo\waves\round-61\w1.ready` — the `LANE_ROOT_DEFAULT` constant named one dead host's checkout, so every other checkout failed before the first case ran.
- S165, before-freeze-colon-case.txt: with `--lane-root .` the battery reached the fixtures and died in `mk()` with `NotADirectoryError: [WinError 267] The directory name is invalid` at the directory named `M01 red: claims file empty` — case M01's display label used verbatim as a path component; the colon is on S164's reserved list and NTFS refuses it.
- Lane prior art, already registered: S152's instrument derives its lane as `HERE.parents[2]` from its own committed location and fails closed with a named message when a needed file is missing — the same `__file__`-relative shape the r68 repair applies to `LANE_ROOT_DEFAULT`.

## Claims

1. A gate selftest's default root must be derived from the instrument's own committed location (the parent of its own directory), never from a host-specific absolute path: a constant naming one checkout breaks the gate's self-invocation on every other host, and the S165 FileNotFoundError at a foreign path is that defect's signature.
2. A selftest fixture builder must map its case display names through a sanitizer for the Win32-reserved set S164 lists before using them as directory names, keeping the display name verbatim in check output: the S165 WinError 267 at a colon-containing directory is that defect's signature, and the sanitizer turns the r67-routed G06 FAIL into a PASS with the 34 frozen cases byte-unchanged.

## Limits

- The sanitizer covers exactly the nine reserved characters of S164's list in fixture directory names; reserved device names (CON, COM1...), trailing dots and spaces, path-length limits, and case-insensitive collisions are real Windows hazards this repair does not address, and the seen-set assertion only catches sanitizer collisions, not case-folded ones.
- Portability is measured on one host pair (the old Linux checkout the constant named, this Windows/11 one): the repaired battery is 34/34 here and green receipts are committed, but other hosts (case-sensitive filesystems, other locales) are untested; a PASS attests the two repaired defect classes only, not general NTFS/Win32 correctness.
