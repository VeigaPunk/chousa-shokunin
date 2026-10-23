# ScoutManBash — bash(1) shadow channels for S068

Access date: 2026-10-23. No packages installed. Did not run `c1-count.py`. Did not edit lane production files.

## Page and package

| item | value |
|---|---|
| file | `/usr/share/man/man1/bash.1.gz` (regular file, not a symlink; 107370 bytes; mtime 2026-09-15 16:47:19 -0300) |
| sha256 (gzip) | `b68beb3e385f7d8aead26bf7887c12f93ca769dcd528fd7282d70938b09bdffe` |
| sha256 (decompressed) | `23f7bd155c57125864094d2cb4e1f6ec9f8c2ea002e18bebeb3ed4bcfaad1971` |
| decompressed size | 392678 bytes, 13495 lines |
| title | decompressed line 24: `.TH BASH 1 "2025 April 7" "GNU Bash 5.3"` |
| comment | line 8: `Last Change: Mon Apr  7 16:59:13 EDT 2025` |
| owner | `pacman -Qo`: `bash 5.3.20-1` (x86_64, packager Tobias Powalowski, build 2026-09-15 16:47:19 -0300, signature-validated) |
| binary | `/usr/bin/bash` same mtime, `GNU bash, version 5.3.20(1)-release (x86_64-pc-linux-gnu)`, sha256 `c14c8f498f3be96f076ceb07d65dba584a86dca3c86b5dce65ed0f6cae73358d` |

Commands: `sha256sum`, `gzip -dc`, `gzip -t` (ok), `pacman -Qo`, `pacman -Qi bash`, `bash --version`. Decompressed copy: `.ufo/waves/round-35/w2/ScoutManBash/bash.1` (same sha256 as above). Formatted `man -P cat bash` (7319 lines) is `/tmp/hyaku/chousa-r35/w2/ScoutManBash/bash.man.txt`, sha256 `6814441ef57f95c3910be6d188e1976ec57b4a60b1ec4072716ff42e7c6e76bd`. Line numbers below are the decompressed nroff source, not the formatted page.

`BASH_FUNC` byte count in the decompressed page: **0**. Also 0 in the same package's `/usr/share/info/bash.info.gz`, `/usr/share/doc/bash/bashref.html`, `bash.html`, `FAQ`, `NEWS`, `CHANGES`, `RBASH`. Those files do contain the words "exported functions" and, except NEWS/RBASH/`bash.html`, the text `export -f`. The environment key is not a located quote in the installed manual.

## Quote 1 — `BASH_ENV` (non-interactive startup file)

Curate this one (22 words). Decompressed lines 395–397, inside the INVOCATION paragraph at lines 390–410. It is a contiguous substring of the macro-stripped paragraph:

> BASH_ENV in the environment, expands its value if it appears there, and uses the expanded value as the name of a file

Word count 22. The same sentence on line 397 continues `to read and execute.` (three more words; including them makes 26, so they stay outside the quote). The subject of that sentence, lines 390–393, is non-interactive start. Same sentence, lines 392–396, a second contiguous extract that does fit in 25 words and names the mode:

> started non-interactively, to run a shell script, for example, it looks for the variable BASH_ENV in the environment, expands its value if it appears there

That 25-word clause stops before "file". The 22-word clause is the one to put on the S068 row because it says the expanded value is a filename. Do not quote the nroff requests on 394–395 (`.SM` / `.B BASH_ENV`).

Located next to it, not a second quote:

- Line 403, the behavior bash claims to emulate: `if [ -n "$BASH_ENV" ]; then . "$BASH_ENV"; fi`
- Lines 407–410: that search does not use `PATH`.
- Lines 2371–2383 (Shell Variables): `BASH_ENV` while executing a shell script is a filename of init commands, expanded (parameter, command substitution, arithmetic) before use; `PATH` is not used. Formatted page lines 1195–1202.

`corpus/knowledge/grep-pin-r35.md` lines 69–70 say the S068 quote is decompressed lines 391–395. That span is the start of this paragraph (through the `.B BASH_ENV` request), not the filename clause on 396–397. The words above are the located text.

## Quote 2 — exported functions (`export -f`)

`BASH_FUNC_name%%` is **not** in this man page. The located `export -f` sentence (11 words), decompressed lines 10188–10192, under the `export` builtin whose synopsis is line 10179 `export [-fn] [name[=value]] ...` and line 10204 `Using -p and -f together displays exported functions`:

> If the -f option is given, the names refer to functions.

Same channel, FUNCTIONS section, lines 5297–5303 (the 21-word prefix is under the cap; the full sentence is 29):

> Functions may be exported so that child shell processes (those created when executing a separate shell invocation) automatically have them defined

and the rest of that sentence, lines 5300–5303: `with the -f option to the export builtin.`

Receipt of the import, lines 5779–5780 (14 words), COMMAND EXECUTION ENVIRONMENT:

> Shell functions defined during execution or inherited from the shell's parent in the environment.

Bash itself turns both channels off in two places the page does name: privileged mode (lines 11619–11629 and the matching startup rule at 492–495: no `$BASH_ENV` file, "shell functions are not inherited from the environment") and restricted shell (line 13321: "Importing function definitions from the shell environment at startup."). The landed gate does not pass `-p` (`tools/research-gate.sh` line 1 is `#!/usr/bin/env bash`).

## What the binary actually puts in the environment

Not a man-page quote. On this `bash 5.3.20`, `export -f` writes the key the manual omits. Command:

```
bash --noprofile --norc -c 'f(){ echo IMPORTED; }; export -f f; env -0 | tr "\0" "\n" | grep "^BASH_FUNC"'
```

Output (truncated at 200 bytes): `BASH_FUNC_f%%=() {  echo IMPORTED`

`/usr/bin/bash` rodata: C string `BASH_FUNC_` at file offset 970830, next C string `() {` at 970841. A separate C string `%%` sits at 971266, after `BASH_CMDS` and `BASH_ALIASES`, not glued to `BASH_FUNC_` in the string table. [INFERENCE] the live `BASH_FUNC_f%%` key is prefix + name + `%%`; that concatenation is not a located string in `bash.1` and was not disassembled here.

A readonly function does **not** stay readonly across that export. Child redefinition succeeded (`def:0`, body printed `CHILD`):

```
bash --noprofile --norc -c 'f(){ :; }; readonly -f f; export -f f; bash --noprofile --norc -c "f(){ echo CHILD; }; echo def:\$?; f"'
```

So an exported `grep` is replaced by the script's own `grep()` (landed gate line 351). The `BASH_FUNC_*%%` channel is the same class as a normal `BASH_ENV` function: the script definition runs later and wins. Not re-scored under `c1-count.py`.

## Readonly `BASH_ENV` is a different channel (same shell)

Man page, lines 1151–1152: a function definition's status is zero "unless a syntax error occurs or a readonly function with the same name already exists." `BASH_ENV` is sourced into the shell that then runs the script (lines 390–403), so `readonly -f grep` in that file is the same shell as line 351.

The gate turns on `set -euo pipefail` at line 292, then defines `grep() { command "$GREP_BIN" "$@"; }` at line 351. Nothing between 292 and 351 calls `grep`.

Copy of the landed gate, sha256 `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617` (matches the wave's landed-gate pin), at `/tmp/hyaku/chousa-r35/w2/ScoutManBash/research-gate.sh`. `BASH_ENV` file sha256 `a09ca30c9ce8d8697056dcc9e50ebd0157d0d9ed2bdffe68686dacfcc7136744` (`ro-env.sh`: a logging `grep` then `readonly -f grep`).

```
env TRIP=.../trip-gate BASH_ENV=.../ro-env.sh timeout 60 bash --noprofile --norc research-gate.sh --help
```

Exit **1**. Stderr (sha256 `16386acec36d547a3e09077e533845a6dc0db9482f92502399554e7dd11c6bd1`): `research-gate.sh: line 351: grep: readonly function`. Stdout empty. Tripwire 0 bytes. `set -e` aborts at the wrapper definition. This is not a silent matcher hijack and not `GREP_PROVENANCE` exit 2.

Control, same copy, `BASH_ENV` function **without** `readonly`, `--help`: exit 0, empty stderr (sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`), tripwire 0. `--help` may not call `grep` at all, so an empty tripwire here does not by itself prove the wrapper won; the readonly run fails on the definition line itself, which does.

`c1-count.py` `write_bash_env` (lines 123–126) does not mark `grep` readonly, and `run_gate` (line 88) only strips `CHOUSA_*` and `RESEARCH_GATE_*`, so a caller `BASH_ENV` would be inherited unless a scenario overwrites it. S2/S9 set their own `BASH_ENV`. Not measured against the nine scenarios. This does **not** meet P1 and does **not** kill it: the scored shim is not readonly, and the readonly case fail-closes (exit 1, no verdict) rather than forging output.

## C1 link (opened, not re-measured)

`corpus/evidence/round35/claims.md` lines 47–52: base-gate S2 is a `BASH_ENV` function with correct output. Landed defense is the line 351 wrapper, which the manual's order (source `BASH_ENV`, then the script) lets a non-readonly function lose. `corpus/evidence/round35/c1-count.py` scenarios S2 and S9 are that channel. No scenario plants `BASH_FUNC_grep%%` or `readonly -f`.

## Limits

- One quote per channel for the row: the 22-word `BASH_ENV` extract (lines 395–397) and the 11-word `export -f` sentence (lines 10188–10192). `BASH_FUNC_name%%` has no man-page quote; inventing one would be false.
- Readonly `BASH_ENV` was only `--help` on a sha256-identical copy, not a verify-claims fixture and not the counter.
- A `BASH_ENV` `DEBUG` trap that redefines `grep` after line 351 was not run.
- Formatted-page line numbers (176–179, 2771–2774, 3071–3072, 5603–5607) are from `man -P cat` and hyphenate; the quotes are from the decompressed source.
