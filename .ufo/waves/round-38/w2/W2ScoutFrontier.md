# W2ScoutFrontier

## Verdict
Census exits 0 with 71 rows; S072/S073 have valid table shape and free IDs, but missing canonical URLs, an overbroad teaching, and landing bookkeeping prevent contract-v1-ready admission.

## Evidence
Axes: **operability** (runnable census/admission) and **calibration** (claims no stronger than the opened text). Seeds: none; no counter was run.

**E1 — final integration identity and current census.** Commands executed from `/home/vgpnk/Projects/shokunin/chousa-shokunin`:
```sh
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master
# 8e93bc916527b3c21f0f702967fa65c3b4c31699
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa
# exit 0; stdout:
chousa W04 S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa W04 S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa ok /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin chousa
# exit 0; chousa rows=71; tier.A=65 tier.B=1 tier.C=5
# status.mined=48 status.queued=19 status.rejected=4
# FLEET repeats those counts; tier.invalid=0 status.invalid=0 missing=0
```
TSV separators above are rendered as spaces. `validate` does not itself emit the histograms; the separate `census` command does.

**E2 — draft width and ID occupancy.** Re-executed commands, both exit 0:
```sh
awk -F'|' '/^\| S07[23] \|/ {printf "%s columns=%d NF=%d\n", $2, NF-2, NF}' /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-38/w1/ScribeSources.md
# S072 columns=11 NF=13
# S073 columns=11 NF=13
awk -F'|' '/^\| S07[23] \|/ {print; n++} END {printf "S072_S073_registry_rows=%d\n",n+0}' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
# S072_S073_registry_rows=0
```
The raw rows at `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-38/w1/ScribeSources.md:58-59` each contain exactly 12 delimiter pipes, hence no additional pipe inside a cell. Both are `docs / A / queued / 2026-10-24 / on-release / —`.

**E3 — independently reopened bash.info sentence.** Command exit 0; selected exact output:
```sh
zcat /usr/share/info/bash.info.gz | awk 'NR<=7 || (NR>=1307 && NR<=1309) || (NR>=1459 && NR<=1465) {printf "%d:%s\n",NR,$0}'
```
```text
1307:File: bash.info,  Node: Shell Functions,  Next: Shell Parameters,  Prev: Shell Commands,  Up: Basic Shell Features
1309:3.3 Shell Functions
1460:the source file and line number, if the ‘extdebug’ shell option is
1461:enabled).  Functions may be exported so that child shell processes
1462:(those created when executing a separate shell invocation) automatically
1463:have them defined with the ‘-f’ option to the ‘export’ builtin (*note
1464:Bourne Shell Builtins::).  The ‘-f’ option to the ‘unset’ builtin (*note
```
The sentence starts **within line 1461**, after `enabled).`, and ends **within 1464**, after `Builtins::).`; 1460–1463 is not the sentence span. The file identifies Edition 5.3, 18 May 2025, makeinfo 7.2.

**E4 — sha256sum section boundaries.** Command exit 0; selected exact output:
```sh
zcat /usr/share/man/man1/sha256sum.1.gz | awk 'NR<=22 || (NR>=54 && NR<=63) {printf "%d:%s\n",NR,$0}'
```
```text
5:.SH SYNOPSIS
6:.B sha256sum
7:[\fI\,OPTION\/\fR]... [\fI\,FILE\/\fR]...
8:.SH DESCRIPTION
11:Print or check SHA256 (256\-bit) checksums.
20:read checksums from the FILEs and check them
54:The sums are computed as described in FIPS\-180\-2.
55:When checking, the input should be a former output of this program.
61:.SH AUTHOR
```
Line 19 is the `-c, --check` roff entry, with GNU tty-link `https://www.gnu.org/software/coreutils/manual/coreutils.html#cksum-c`; line 20 is its description. Lines 54–58 are also under DESCRIPTION, not SYNOPSIS.

**E5 — file identities.** `/usr/bin/sha256sum /usr/share/info/bash.info.gz /usr/share/man/man1/sha256sum.1.gz` returned:
```text
cde1a3366897684b0a86fe553687e31d070b7839b19ca98186ffc6e0e105588f  /usr/share/info/bash.info.gz
93c17dffe9f25d56291113d566a7de3ff65c29f8cc32c381801c49cf27e8403f  /usr/share/man/man1/sha256sum.1.gz
```
`pacman -Q bash coreutils` returned `bash 5.3.20-1` and `coreutils 9.12-2` (read-only query, no transaction).

**E6 — current draft cannot pass quote admission.** Executed with the following TSV on stdin; exit **1**, no registry writes:
```sh
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/quote-reopen.py verify --items /dev/stdin --registry /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-38/w1/ScribeSources.md
```
```text
id	source_id	quote
S072w2	S072	Functions may be exported so that child shell processes … automatically have them defined with the ‘-f’ option to the ‘export’ builtin
S073w2	S073	read checksums from the FILEs and check them
```
```text
QUOTE_REOPEN S072w2 NO_SOURCE registry row S072 has no http(s) URL
QUOTE_REOPEN S073w2 NO_SOURCE registry row S073 has no http(s) URL
QUOTE_REOPEN_SUMMARY verbatim=0 absent=0 too_long=0 no_source=2 unreachable=0
```
A separate whitespace-only substring check against the reopened bash.info stream found the printed 22-word ellipsis quote **not present**; the contiguous 21-word replacement below **was present**. `printf '%s\n' 'read checksums from the FILEs and check them' | wc -w` returned **8**, not the draft's 7.

## Findings
1. **Observed, high confidence — structural prerequisites pass, not full conformance.** E2 proves 11 columns, no in-cell pipe, and S072/S073 free. Exact versioned anchors and hashes match E3–E5. Current census success applies only to the existing 71 rows, not admission of the two drafts.
2. **Observed, high confidence — add canonical URLs before landing.** Both `source` cells have only absolute installed-file paths. `/home/vgpnk/Projects/shokunin/CORPUS.md:89-100,112-115` requires canonical URL/DOI for `docs`, with the path/command exception only for `own-work`; the canonical `skill://shokunin/protocol/CORPUS.md` agrees. E6 demonstrates the operational consequence. Add actual canonical GNU URLs to source cells and Gate entries; retain installed-file identity and disclose that those URLs were not fetched here. Do not relabel official documentation as own-work to evade this.
3. **Observed, high confidence — narrow S072's teaching.** Draft line 58 says an exported function reaches **every** child shell invocation; its quoted manual says only that functions *may* be exported. Re-executed `zcat /usr/share/info/bash.info.gz | awk 'NR>=5038 && NR<=5048 {printf "%d:%s\n",NR,$0}'` exits 0 and explicitly says at 5040–5042 that privileged mode does not inherit shell functions. Delete the universal claim. A literal count over the reopened stream found zero `BASH_FUNC` occurrences; preserving the encoding exclusion is correct, not proof about implementation encoding.
4. **Observed plus admission inference, high confidence — keep the corrected sentence span, fix the Gate quote.** Draft lines 58,65–70 already use 1461–1464, which E3 confirms; do not regress to 1460–1463. The ellipsis quote meets v1's word budget but is not verbatim. `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/QUALITY.md:211-215` additionally requires `VERBATIM` before admission. A contiguous 21-word quote available at 1461–1463 is: “Functions may be exported so that child shell processes (those created when executing a separate shell invocation) automatically have them defined”. After URL repair, obtain the actual reopen result rather than claiming E6 tested quote matching—it stopped at NO_SOURCE.
5. **Observed, high confidence — S073 correctly diagnoses a label defect, not bad offsets.** `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md:80` mislabels the 19–20 option entry as SYNOPSIS. E4 places it in DESCRIPTION; S073's `supersedes S070 —` opening is correct. Do not edit S070's immutable anchor/teaches cells: contract v1 permits only status/recheck/used-by edits, logged old→new (`/home/vgpnk/Projects/shokunin/CORPUS.md:116-118`).
6. **Observed, high confidence — repair supersede callers atomically.** Before clearing S070's used-by and moving mined→queued as draft line 75 proposes, migrate or explicitly supersede the active citations at `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/engine-swap-canary-r36.md:6,42-44` and `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/claim-pin-provenance-r37.md:7-10,27`. Both still cite S070; both also over-attribute the lane's 64-lowercase-hex policy to it. Preserve the manual/policy distinction when pointing them to S073. Synchronize S073's mined status and backlinks with actual citing paths, per `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/QUALITY.md:17-27`.
7. **Observed, high confidence — fix counts and finish the missing landing artifacts.** Draft line 63 and line 114 say **70 → 72**, despite their own 71-row baseline: appending two gives **71 → 73**, not 72. Correct S073's quoted-word count at line 73 from 7 to 8. `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/lessons/round-38.md` was absent when searched; the draft is not that required Gate record. L1 must land the Gate's URLs/access dates/located ≤25-word quotes and bounded Search log (contract v1 rules 1,5), plus any status/backlink changes, then obtain the integrated census/histograms; no post-landing result is claimed here.

## Limits
- Source/Markdown audit only; no gate, C1/C2 counter, verifier mutation, network fetch, or execution-authorship claim. Findings are local-byte observations except the explicitly identified admission inference.
- `read xd://lsp` returned `No such tool: xd://lsp. Mounted devices: ast_edit, debug.` No semantic server was available; caller pointers above are literal textual references, not LSP proof or an empty cold-index result.
- No installs or updates. Fleet/lane content and git/jj state were not edited; the only persistent write is this requested report.
