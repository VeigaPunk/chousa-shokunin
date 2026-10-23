# ScribeSrcSha — round 36, wave 1

Axes named by the brief: operability and calibration. This seat completed the S070 source-row draft only; it did not score either behavioral axis.

**VERDICT: S070 source draft complete.** The locally installed coreutils manual directly states that SHA256 checksums are 256-bit and that `--check` reads checksums from its FILE operands. It does not directly specify a 64-hex-character representation, a lowercase requirement, or a validation policy. The 64-hex-length conclusion follows only if the digest is represented in base 16; lowercase is the lane's policy [INFERENCE].

## Behavior, gates, and touched surfaces

- Behavior observed: manual text at decompressed lines 11, 19–20, 55–58. The row records the manual's 256-bit statement, `--check` input, and output-record fields without attributing a 64-lowercase-hex rule to the manual.
- Gates: none run. No research gate, C1/C2 counter, selftest, fresh-seed re-derivation, or fixture attack was performed by this source-curation seat. No behavioral claim is made.
- Touched surfaces: wrote only the scoped `row-draft.md` artifact and this report. `corpus/SOURCES.md`, `corpus/knowledge/`, tools, gate, and counters were read-only. No install, commit, or git/jj write was performed.
- Out of scope / known limit: the requested future backlink `corpus/knowledge/engine-swap-canary-r36.md` was absent when checked; it was not created or edited. The row's `used-by` cell names that requested target. No network access was used.

## Source findings

- `pacman -Q coreutils` reported `coreutils 9.12-2`.
- Local source: `/usr/share/man/man1/sha256sum.1.gz`, SHA-256 `93c17dffe9f25d56291113d566a7de3ff65c29f8cc32c381801c49cf27e8403f`.
- Decompressed `.SH` section names: `NAME` (line 3), `SYNOPSIS` (5), `DESCRIPTION` (8), `AUTHOR` (61), `REPORTING BUGS` (63), `COPYRIGHT` (71), and `SEE ALSO` (77). The `.SS` subsection at line 31 is “The following five options are useful only when verifying checksums:”.
- Single located quote (DESCRIPTION, decompressed line 11; 8 words): “Print or check SHA256 (256-bit) checksums.”
- Additional decisive locations, paraphrased: lines 19–20 describe `-c, --check` as reading checksums from the FILEs and checking them; line 55 says checking input should be a former output of the program; lines 56–58 give the checksum / mode-character / filename record shape.

## Commands and outcomes

The Bash tool did not expose process exit-status metadata. For successful commands below, exit 0 is inferred from the returned output and lack of a reported command failure; that exit value was not independently captured. The row-draft checksum is directly reported by the checksum command.

1. `timeout 30s pacman -Q coreutils` — output: `coreutils 9.12-2`; exit 0 [INFERENCE as above]. This decides the installed package version.
2. `timeout 30s sha256sum /usr/share/man/man1/sha256sum.1.gz` — output: `93c17dffe9f25d56291113d566a7de3ff65c29f8cc32c381801c49cf27e8403f  /usr/share/man/man1/sha256sum.1.gz`; exit 0 [INFERENCE as above].
3. `set -o pipefail; timeout 30s gzip -cd /usr/share/man/man1/sha256sum.1.gz | nl -ba` — output included line 11 `Print or check SHA256 (256\-bit) checksums.`, lines 19–20 (`-c, --check`; `read checksums from the FILEs and check them`), line 55 (`When checking, the input should be a former output of this program.`), and lines 56–58 (printed checksum line fields); exit 0 [INFERENCE as above].
4. `timeout 30s mkdir -p /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ScribeSrcSha` — no output; exit 0 [INFERENCE as above]. Setup only.
5. `timeout 30s sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ScribeSrcSha/row-draft.md` — output: `e411e3b7d8c0ae21bda1ba8bd720c3d9d5622713e159c2e5fba2f0dfd185e276  /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ScribeSrcSha/row-draft.md`; exit 0 [INFERENCE as above].

Other inspection actions (not shell commands): `read` on the compressed manual returned only `sha256sum.1 (3.6KB)` metadata, so the numbered decompression command above was used for the source text. `grep` searched `corpus/` for `S069|S070|^\| ID \|`; the source catalog table header was located at `corpus/SOURCES.md:9`, with no S069/S070 row returned. A read of the requested future target returned “Path …/corpus/knowledge/engine-swap-canary-r36.md not found.”

## Files opened (2026-10-23)

- `/home/vgpnk/.agents/skills/godspeed/SKILL.md` (via `skill://godspeed`).
- `.ufo/waves/round-36/w1-briefs/ScribeSrcSha.md`.
- `/usr/share/man/man1/sha256sum.1.gz` (read attempt plus decompressed with the command above).
- `corpus/` and `corpus/knowledge/` directory listings.
- `corpus/SOURCES.md` (ranges 1–80 and final 120 lines; source-row schema and nearby rows).
- `corpus/knowledge/grep-pin-r35.md` (knowledge-entry citation format).
- Attempted `corpus/knowledge/engine-swap-canary-r36.md`; not found, so it was not opened.

## Artifacts

- Draft: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ScribeSrcSha/row-draft.md` — SHA-256 `e411e3b7d8c0ae21bda1ba8bd720c3d9d5622713e159c2e5fba2f0dfd185e276` (1,985 bytes).
- Report, written once: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ScribeSrcSha.md`.
