# Round 26 source opening — GNU Bash Reference Manual

## Access and source identity
- Requested canonical URL `https://www.gnu.org/software/bash/manual/bash.html`: HTTP fetch timed out (curl reported `HTTP=000 bytes=0` after 60 s; static reader also timed out). `https://www.gnu.org/software/bash/manual/html_node/Here-Strings.html` also timed out.
- Opened the actual versioned manual HTML from the official GNU Bash 5.3 source release: `https://ftp.gnu.org/gnu/bash/bash-5.3.tar.gz` returned `HTTP=200 bytes=11355854`; archive member `bash-5.3/doc/bashref.html` is titled “Bash Reference Manual,” Edition 5.3, last updated 18 May 2025. Archive SHA-256: `0d5cd86965f869a26cf64f4b71be7b96f90a3ba8b3d74e27e8e9d9d5550f31ba`. Mirror route `https://mirrors.kernel.org/gnu/bash/bash-5.3.tar.gz` returned HTTP 200. Host Bash: `GNU bash, version 5.3.20(1)-release`.
- No duplicate row found in the current registry: case-insensitive `grep` for `bash` returned no matches. Table columns are the v1 order at `corpus/SOURCES.md:9-10`; proposed id remains TBD as assigned.

## Located evidence
> “read returns after reading nchars characters rather than waiting for a complete line of input.”

Location: Bash Reference Manual 5.3, §4.2 “Bash Builtin Commands,” `read -n nchars`, anchor `#Bash-Builtin-Commands` (opened HTML `/tmp/r26-srcbashread/bashref.html:6182-6187`; title/version at lines 9-11). This is 15 words.

Also opened the adjacent documented behaviors: `-d ''` terminates on NUL (`bashref.html:6152-6157`); `-r` makes backslash literal (`6207-6211`); §3.6.7 “Here Strings,” anchor `#Here-Strings`, says the expanded word is supplied as one string plus an appended newline to stdin (`4027-4040`).

## C1 applicability and limits
- Preregistered base claim: an 8,388,000-byte entry passes the 8 MiB cap and the later per-line array materialization occurs before the header loop (`corpus/evidence/round26-claims.md:28-37`). The manual distinguishes `read -n`'s character count from that later storage; here-string semantics describe stdin delivery, not memory use.
- Gate source separately shows local `LC_ALL=C` and a `read -r -d '' -n "$((SOURCE_READ_MAX_BYTES + 1))"` read with a subsequent size check (`tools/research-gate.sh:2366,2391-2402`). [INFERENCE] In that C-locale context the character count is used bytewise; the manual itself says “characters,” not “bytes.”
- Scope limit (QUALITY 7/8; `corpus/QUALITY.md:24-31`): this source is authoritative only for Bash 5.3 shell semantics. It does not support a claim about Bash-array allocation cost, RSS, runtime, or whether the specific gate passes C1; those need the implementation and measured probe. The manual also does not prescribe the gate's byte-cap policy.

## Proposed SOURCES.md row (contract v1 order)
ID left TBD as assigned; next unused is S034.

| TBD | GNU Bash Reference Manual — https://www.gnu.org/software/bash/manual/bash.html (opened 5.3 release HTML from https://ftp.gnu.org/gnu/bash/bash-5.3.tar.gz) | docs | A | Bash 5.3 `read` options `-d`, `-n`, `-r` and here-string input semantics only | Edition 5.3, updated 2025-05-18; §4.2 `read` options, anchor `#Bash-Builtin-Commands`; §3.6.7 Here Strings, anchor `#Here-Strings` | Distinguishes `read -n`'s character-count stop from the here-string's single-string stdin contract; does not establish later storage cost | queued | 2026-10-21 | on-release | — |

Tier A is scoped to Bash's own reference documentation for Bash behavior, not memory/performance claims (`/home/vgpnk/Projects/shokunin/CORPUS.md:93-98`). Status is queued because the source is opened and relevant but no knowledge entry cites it yet; flip to mined when a C1 knowledge entry cites the assigned row. `on-release` rechecks the versioned manual when Bash releases change its semantics.

Installs: none.
VERDICT: Opened and located the official Bash 5.3 manual via the upstream release archive; useful for C1 reader semantics only, not allocation or RSS evidence.