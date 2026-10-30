# Draft02 — GNU realpath source admission

## Behavior and axes
Axes: source fidelity, located-quote precision, scope discipline. Advisory admission recommendation for C3's GNU realpath source only; no canonical judgment or production integration performed.

**ADMIT (narrow proposition):** GNU `realpath -e` requires every path component to exist. Installed source: `/usr/share/man/man1/realpath.1.gz`, decompressed member `realpath.1`, DESCRIPTION, `-e, --canonicalize-existing` option. Located quotation (8 words): **“all components of the path must exist”**. Page header: `REALPATH(1)`, September 2026, GNU coreutils 9.12. Accessed 2026-10-30.

**REJECT (overreach):** This quotation does not establish that an existing resolved path is the intended lane root, that it is a regular file, or that Python `Path.resolve()` defaults to GNU `realpath -e` semantics. Existence cannot bind parents arithmetic to author intent. The adjacent default `-E, --canonicalize` option explicitly says “all but the last component must exist (default)”; do not attribute `-e`'s requirement to default invocation.

## Provenance and exact command receipts
Working directory for shell calls: `/home/vgpnk/Projects/shokunin/chousa-shokunin`. No behavioral probes were required or run.

1. `realpath --version` — exit 0; output `realpath 0.8.0`. This is **not GNU evidence**: subsequent command resolution identified a shell builtin.
2. `command -V realpath && pacman -Qo /usr/bin/realpath && /usr/bin/coreutils --version` — combined exit 127. Output:
   ```text
   realpath is a shell builtin
   /usr/bin/realpath is owned by coreutils 9.12-2
   error: command not found: /usr/bin/coreutils
   ```
   Package ownership query succeeded; nonexistent aggregate binary did not invalidate the separate ownership result. No package transaction occurred.
3. `/usr/bin/realpath --version` — exit 0. Output:
   ```text
   realpath (GNU coreutils) 9.12
   Copyright (C) 2026 Free Software Foundation, Inc.
   License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>.
   This is free software: you are free to change and redistribute it.
   There is NO WARRANTY, to the extent permitted by law.

   Written by Pádraig Brady.
   ```
4. File discovery: `glob` over `/usr/share/man/man1/realpath*;/usr/share/info/coreutils*` located `realpath.1.gz` and `coreutils.info.gz`.
5. `read /usr/share/man/man1/realpath.1.gz` returned the archive member listing. `read /usr/share/man/man1/realpath.1.gz:realpath.1` returned the complete installed man source, including the located quote and version header above. Read tools expose no process exit status.
6. `read /usr/share/info/coreutils.info.gz:coreutils.info` returned `[Cannot read binary archive entry 'coreutils.info' (1.0MB)]`. No info-page claim is admitted; installed man source suffices.

## Gates and known limits
- Read host rules first, frozen `corpus/evidence/round64/claims.md` next, then Godspeed instructions. Claims file identified frozen instrument names; none modified. Freeze commit supplied by assignment: `bf40d99bda9eefdad3ed6276da077cfb24ba82f1`; not independently checked.
- Assignment states frozen C1 E12/E13 fixture mismatch; inherited `c1-battery-supplement.py` is post-freeze and distinct. Frozen C1 failure is not repaired or upgraded to PASS by this source admission. No battery or supplement executed here.
- `ref-preflight-v3.py` remains a candidate, not production; no production claim made.
- Non-author admit/reject above is scoped source advice, not closure of C3 or any other claim. Python evidence and counter results belong to other seats.
- Tools: preinstalled GNU coreutils realpath 9.12, package coreutils 9.12-2; shell builtin realpath 0.8.0 encountered but excluded. Installation/update channel: none; reason: installed source and binary available. No network fetch, installation, restart, git/jj mutation, clone, or alternate runtime invocation.
- Scratch was never created or used; no live clone or scratch tree was created to remove.

## Touched surfaces and path conflict
Only seat report artifacts are written. Assignment paths conflict verbatim:
- “Write only your own report and evidence beneath /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-64/w1/Draft02/ (report.md); no production edits.”
- “Report: write your scoped findings to .ufo/waves/round-64/w1/Draft02.md”

Full report is in the unique seat directory; the explicitly named Report trailer path contains a pointer. No product files, source rows, frozen claims, counters, or operator inputs changed. This conflict is recorded without attempting canonical judgment.

Artifacts relative to lane root:
- `.ufo/waves/round-64/w1/Draft02/report.md` — full findings and embedded receipts.
- `.ufo/waves/round-64/w1/Draft02.md` — requested trailer pointer.

## Self-evaluation
Accuracy 4/5: installed man and explicit GNU binary observed; info rendering unavailable. Completeness 5/5: located <=25-word quote, installed version, commands/exits, scope and conflicts recorded. Clarity 4/5: two realpath implementations require provenance distinction. Actionability 5/5: narrow admit and overreach reject supplied for L1. Conciseness 4/5: receipt detail retained for audit. Overall 4.4/5. Improvement: use the explicit GNU binary path in any later command; no rerun needed. User-agreement self-check: deliverable is source advice, not execution evidence for C3's counter.
