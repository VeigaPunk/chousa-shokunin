# ScoutC2Package — provenance of the installed git sources (round 63, wave w1)

Item: establish that the man pages cited by rows S142–S144 are the Arch package's own
copies, unshadowed and unmodified, and fix the exact `source`-cell wording.

## Findings

1. The two cited pages are owned by the installed package and are byte-identical to it:
   `/usr/share/man/man1/git-rev-parse.1.gz` and `/usr/share/man/man7/gitrevisions.7.gz`
   are owned by `git 2.56.0-1`, and a full `pacman -Qkk git` integrity check reports
   `757 total files, 0 altered files` — no on-disk drift against the package database.
2. No shadowing: `man -w` and `man -aw` each resolve to exactly one path, the
   `/usr/share/man/...` package path; `MANPATH` is unset in the environment, so no
   earlier MANPATH entry can shadow the pages.
3. Page identity matches the rows: both `.TH` headers carry date `2026-09-27` and
   `Git 2.56.0`; package `git 2.56.0-1`, signature-validated, install date 2026-10-20
   (pacman.log: `upgraded git (2.55.0-1 -> 2.56.0-1)` at 2026-10-20T09:16:37-0300).
   `git --version` = `2.56.0`; probe output header agrees (`HEADER git=git version 2.56.0`).
4. The cited paragraphs render from the package bytes. With the rows' rendering command
   (`MANWIDTH=1000 man -l FILE | col -bx`, man 2.13.1, util-linux col 2.42.4) every
   paragraph named by S142/S143 is present verbatim:
   - git-rev-parse(1): `--verify` at rendered lines 61–66 (includes the `^{commit}` /
     `^{object}` peeling sentences), `--short[=<length>]` at 74–75 (minimum 4, default
     `core.abbrev`), `--disambiguate=<prefix>` at 118–119 (lists every object with the
     prefix, ≥ 4 hex digits).
   - gitrevisions(7): `<sha1>` at 21–22, `<refname>` at 27–28 (the 6-step disambiguation
     rules), `<rev>^{<type>}` at 114–119, `<rev>:<path>` at 130–131, all under
     `SPECIFYING REVISIONS` (heading at rendered line 14).
   - Raw↔rendered continuity for the `<rev>:<path>` paragraph: raw roff line 472
     ("...followed by a path names the blob or tree at the given path...") renders to
     line 131 with the same sentence, roff escapes removed. Rendering is a faithful
     re-expression of the package file, not an independent text.
5. Since the on-disk pages are package bytes (ownership + 0 altered) and the cited
   paragraphs appear in the render of exactly those bytes, the rendered text of the
   cited paragraphs is the package's text. [INFERENCE] The `.TH` date 2026-09-27 is the
   upstream documentation date baked into the 2.56.0 release; it precedes the Arch build
   date 2026-09-28 by one day, consistent with that packaging flow.

## Evidence (command → observed output)

- `pacman -Qi git` → `Version : 2.56.0-1`, `Packager : Christian Heusel <gromit@archlinux.org>`,
  `Build Date : Mon 28 Sep 2026 02:57:26 PM -03`, `Install Date : Tue 20 Oct 2026 09:16:37 AM -03`,
  `Validated By : Signature`.
- `pacman -Qo /usr/share/man/man1/git-rev-parse.1.gz /usr/share/man/man7/gitrevisions.7.gz`
  → `... is owned by git 2.56.0-1` (both lines).
- `pacman -Qkk git` → `git: 757 total files, 0 altered files`, exit 0.
- `man -w 1 git-rev-parse && man -w 7 gitrevisions` → `/usr/share/man/man1/git-rev-parse.1.gz`,
  `/usr/share/man/man7/gitrevisions.7.gz`; `man -aw 1 git-rev-parse` / `man -aw 7 gitrevisions`
  → exactly one path each; `printf 'MANPATH=[%s]' "${MANPATH-<unset>}"` → `MANPATH=[<unset>]`.
- `zcat /usr/share/man/man1/git-rev-parse.1.gz | grep -m1 '^.TH'` →
  `.TH "GIT\-REV\-PARSE" "1" "2026\-09\-27" "Git 2\&.56\&.0" "Git Manual"`;
  `zcat /usr/share/man/man7/gitrevisions.7.gz | grep -m1 '^.TH'` →
  `.TH "GITREVISIONS" "7" "2026\-09\-27" "Git 2\&.56\&.0" "Git Manual"`.
- `git --version` → `git version 2.56.0`.
- `grep -E ' (installed|upgraded|reinstalled) git ' /var/log/pacman.log | tail -5` →
  `[2026-10-03T20:42:26+0000] [ALPM] installed git (2.55.0-1)`;
  `[2026-10-20T09:16:37-0300] [ALPM] upgraded git (2.55.0-1 -> 2.56.0-1)`.
- `MANWIDTH=1000 man -l /usr/share/man/man1/git-rev-parse.1.gz | col -bx | grep -nE -A8 '^ {1,9}--(verify|short|disambiguate)'`
  → hits at lines 61, 74, 118 with the texts quoted above.
- `MANWIDTH=1000 man -l /usr/share/man/man7/gitrevisions.7.gz | col -bx` → entries at
  lines 21 (`<sha1>, e.g. dae86e...`), 27 (`<refname>, e.g. master, ...`), 114
  (`<rev>^{<type>}, e.g. v0.99.8^{commit}`), 130 (`<rev>:<path>, e.g. HEAD:README, ...`).
- `MANWIDTH=1000 man -l /usr/share/man/man7/gitrevisions.7.gz | col -bx | grep -n 'colon'`
  → rendered line 131 matches raw roff line 472 sentence-for-sentence.
- Renderer provenance: `man --version` → `man 2.13.1`; `col --version` → `col from util-linux 2.42.4`.
- Probe corroboration: `corpus/evidence/round63/controls/candidate-git-revision-probe.txt` line 1
  → `HEADER git=git version 2.56.0`, line 2 → `HEADER python=3.14.8` (matches S144's source cell).

## Source-cell wording the registry rows should carry

Verified against the candidate rows
(`corpus/evidence/round63/controls/candidate-git-rows.txt`); keep them verbatim —
package name+version, page date and rendering command are all exactly what the
evidence above supports:

- S142: `git-rev-parse(1) — Git 2.56.0 manual page (2026-09-27), the installed /usr/share/man/man1/git-rev-parse.1.gz of the Arch package git 2.56.0-1, rendered with MANWIDTH=1000 man -l FILE then col -bx`
- S143: `gitrevisions(7) — Git 2.56.0 manual page (2026-09-27), the installed /usr/share/man/man7/gitrevisions.7.gz of the Arch package git 2.56.0-1, rendered with MANWIDTH=1000 man -l FILE then col -bx`

## Notes

- Queries only; no pacman transaction was run, no network use, no git/jj/index mutation.
- No tools installed or upgraded (operator tooling authorization unused this round).
- No scratch dir was needed (nothing written outside this report).

VERDICT: SOURCES_ARE_PACKAGE_COPIES=yes git=2.56.0 page_date=2026-09-27
