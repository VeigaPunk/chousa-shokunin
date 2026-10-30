# Draft02 — source admission

Full scoped report and command receipts: [Draft02/report.md](Draft02/report.md).

ADMIT narrowly: installed GNU realpath 9.12 man page, DESCRIPTION, `-e, --canonicalize-existing`: “all components of the path must exist” (8 words). Source `/usr/share/man/man1/realpath.1.gz`, accessed 2026-10-30. Explicit `/usr/bin/realpath --version` exit 0 confirms GNU coreutils 9.12; unqualified `realpath` is a different shell builtin.

REJECT inference that existence establishes intended lane identity. No production edits or behavioral tests. Frozen C1 E12/E13 failure remains unclosed; post-freeze supplement is distinct. Conflicting report-path instructions are recorded verbatim in the full report.
