# Recon02 — installed GNU realpath documentation

Axes: source accuracy, exact quotation, implementation identity, zero production impact.

## Observed findings (high confidence)

Opened the frozen claims first, after mandatory operator rules. Relevant source claim: `corpus/evidence/round64/claims.md:219–227` (C3, candidate S151).

Installed GNU manual: `/usr/share/man/man1/realpath.1.gz`, header `GNU coreutils 9.12`, September 2026. Command `gzip -cd /usr/share/man/man1/realpath.1.gz` exited 0. Exact option paragraph (roff font/link markup omitted):

> -e, --canonicalize-existing
> all components of the path must exist

Contrasting default paragraph:

> -E, --canonicalize
> all but the last component must exist (default)

Installed full manual: `/usr/share/info/coreutils.info.gz`, node `realpath invocation`, section 18.5. Command `/usr/bin/info --output=- coreutils 'realpath invocation'` exited 0. Exact paragraph:

> ‘-e’
> ‘--canonicalize-existing’
>      Fail if the named file does not exist.  A trailing slash requires
>      that the name resolve to a directory.

Same node, exact exit-status paragraph:

> Exit status:
>
>      0 if all file names were printed without issue.
>      1 otherwise.

## Implementation identity caveat

`realpath --version` exited 0 with `realpath 0.8.0`, whereas `/usr/bin/realpath --version` exited 0 with `realpath (GNU coreutils) 9.12` and GNU copyright/license details. `type -a realpath info coreutils` printed:

```text
realpath is a shell builtin
realpath is /usr/bin/realpath
info is /usr/bin/info
type: coreutils not found
```

That combined discovery command exited 1 because `coreutils` was not found. Therefore use `/usr/bin/realpath` explicitly when claiming behavior of the installed GNU implementation; the unqualified command resolves to a different shell builtin in this tool environment.

## Interpretation and limits

The installed sources directly support C3's narrow statement about `realpath -e` refusing nonexistent paths. They do not establish that an existing path is the intended lane file, has a particular file type without the documented trailing-slash directory requirement, or contains correct bytes. Existence is not identity. This is source evidence, not an execution probe of those semantics. No code contract was traced or changed.

No fixture probes, counters, batteries, or production checks were run. Frozen C1's disclosed E12/E13 fixture mismatch remains a frozen failure; the distinct inherited supplement does not rewrite it. This seat does not measure or close C1 or C3.

Access date: 2026-10-30. No network access, installs, updates, clones, scratch directories, production edits, or VCS mutations. Scratch was never created, so none remains. Tool inventory used: existing GNU coreutils realpath 9.12, gzip, GNU info, and the tool shell's realpath 0.8.0 builtin; no installation channel involved. Initial compressed-file reader returned filename/size rather than extracted text; reported via `xd://report_issue`, then opened local documentation with gzip/info.

Report: .ufo/waves/round-64/w1/Recon02/report.md
