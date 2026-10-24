# RevFrontier — round-37 frontier artifacts vs SOURCES contract v1

Seat: `chousa-r37.RevFrontier`. Date: 2026-10-23. No network. No tools installed.
Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`, lane tip
`b905217a7dfdcf58be1f0a4c0bf5f2d2d32a2d65` (`git -C … rev-parse master`, exit 0).
The round-37 corpus files under review are uncommitted working-tree changes at that tip
(`git status --porcelain`: `M corpus/SOURCES.md`, `M corpus/README.md`, `M corpus/QUALITY.md`,
`?? corpus/lessons/round-37.md`, `?? corpus/knowledge/{claim-pin-provenance,pin-capture-env}-r37.md`);
the L1 owns the commit.

Method note: no `lsp` device is exposed to this seat (tool inventory: read/bash/edit/eval/glob/
grep/task/wait/web_search/write; `xd://` exposes only `ast_edit` and `debug`). Caller, definition
and diagnostics checks were therefore done with text `grep`/`awk` over exact file:line targets and
with the lane's own census; that is the literal fallback, not semantic proof. No runtime
rerouting, same-identity routing, saturation claim, or `resume_continuity_v1` path exists in this
artifact set, so those checks are not applicable here (stated, not skipped silently).
`jj` was deliberately not invoked (it snapshots the working copy into `@`); git was read only via
`rev-parse`/`status`. No fleet file was created, edited or deleted; the only file written is this
report.

## Overall verdict

**NOT CONFORMANT.** The S071 row's factual content is verified true (decompressed line 27 option
entry, line 28 quote, file digest, revision, enums, id uniqueness, tier), and the census receipt
reproduces exactly. Three rule-level defects and three minor ones remain; the blocking one is that
`corpus/knowledge/claim-pin-provenance-r37.md` has no `mined` S-row whose `used-by` names it
(QUALITY 6; `SOURCES.md:80`), so its admission metadata is incomplete at the reviewed state.

## Per-item verdicts

| # | Assigned check | Verdict | Evidence |
|---|---|---|---|
| 1 | S071 row, no `\|` inside cells, 11 columns | PASS | `corpus/SOURCES.md:81`; `awk` NF=13 for all 71 rows; frozen census "malformed → 0" |
| 2 | id `S071` not reused | PASS | `uniq -d` empty; `grep -c '^| *S071 '` = 1; id order sorted (`sort -c` exit 0) |
| 3 | kind/tier/status enums valid | PASS | `docs` / `A` / `mined`; frozen enum+tier-inflation awk printed nothing |
| 4 | Tier A justified for scope | PASS | Installed man page is authoritative for the installed tool's documented option semantics; scope explicitly excludes the gate's capture policy; `TH` line: `GNU coreutils 9.12`, `September 2026`; `pacman -Q coreutils` → `9.12-2` |
| 5 | Anchor names exact section/lines + revision | **FAIL (minor)** | Lines `27–28`, quote at `28`, revision correct — but the label `OPTIONS` names no heading in the file: `.SH` headings are `NAME, SYNOPSIS, DESCRIPTION, SCRIPT OPTION HANDLING, NOTES, AUTHOR, REPORTING BUGS, COPYRIGHT, SEE ALSO`; the `-u` entry sits under `DESCRIPTION` (`.SH DESCRIPTION` at line 8). Defect at `corpus/SOURCES.md:81` (anchor cell) |
| 6 | `teaches` does not overclaim | PASS | The line-28 quote grounds "removes NAME from the environment"; "of the invoked command / absent before the child starts" follows from `DESCRIPTION` line 11 "Set each NAME to VALUE in the environment and run COMMAND"; the gate-policy choice is labelled `[INFERENCE]` in the lesson |
| 7 | `used-by` paths exist | PASS | `corpus/knowledge/pin-capture-env-r37.md` exists; `S071.used-by` = that path (`SOURCES.md:81`). Reverse direction fails for C1 — see finding H1 |
| 8 | Re-open source: `-u` option and quote at line 28 | PASS | Verified verbatim (command log C6/C8): line 27 `\fB\-u, \-\-unset=\,NAME\fP`, line 28 `remove variable from the environment` |
| 9 | gz SHA-256 matches anchor cell | PASS | `4ae797e6e280da9d514bc94f3fbceffac5d0ceb62c197f78bb04bee84a78fb27` — byte-identical to `SOURCES.md:81` |
| 10 | Lesson `## Gate`: URL + access date + ≤25-word quote | **FAIL** | Access date present ("Opened locally 2026-10-23"); quote present at line 28; **URL absent** (`grep -n 'http'` exit 1, no match) although CORPUS.md rule 1 (`CORPUS.md:112-114`) requires it and the page carries a canonical URL at the anchored line 27; **word count wrong**: lesson says "6 words" (`lessons/round-37.md:39`), the lesson's own command yields `5` (finding M1) |
| 11 | `## Mistakes` rows carry class/evidence/captured-by/fix | PASS (columns) / **FAIL (pointer)** | Two rows at `lessons/round-37.md:28-29`, four columns each, classes `scope` and `number-drift` in the §5 vocabulary, captured-by `none in-round` allowed. But the row-1 evidence pointer "`w1/SentNoHarm.md` (round 36) lines 31-35" points at the Opened-files bullet list; the recorded commands are at lines 22–25 (finding M2) |
| 12 | Both knowledge entries open with the provenance trio | PASS (trio) / **FAIL (QUALITY 6 sub-clauses)** | Both files: `source:` line 7, `verified-at:` line 15, `recheck:` line 17, line-start, contiguous, matched once each by the freshness sweep regex `^[-* ]*recheck *:`. Title/Lane/Surface precede as in landed r34–r36 entries, so the trio is the first metadata block, not the literal first line. Failing sub-clauses: H1 (C1 has no qualifying S-row) and L2 (source lines omit the source's path/URL + anchor) |
| 13 | README index rows exist and cite existing paths | PASS (existence/paths) / minor (placement) | Rows at `corpus/README.md:1038-1039`; `evidence/round37/claims.md` exists; `evidence/round37/receipts/c1-*.json` = 5 files, `c2-*.json` = 5 files (corpus-relative, as the README's other rows). Placement finding L3 |
| 14 | QUALITY 53 "shown able to fail" names a concrete failing case | PASS | `corpus/QUALITY.md:430-439` names the round-37 wave seat's `--root .` run, all six rows, and `ExecNoHarmPin.md`; the file exists and its table records `0/17`, `0/22`, `0/2` and "Harm" on six rows |
| 15 | Adjunct: lesson census receipt | PASS | `sources-census.sh validate --root … chousa` → exit 0, `ok`, `W04` ×2 on S051/S053; frozen census: 71 rows, A=65 B=1 C=5, mined=48 queued=19 rejected=4, malformed 0, no dups, no enum violations, no missing used-by paths — exactly the lesson's numbers (`lessons/round-37.md:52-55`) |

## Findings by severity

### H1 — C1 knowledge entry has no `mined` row whose `used-by` names it (QUALITY 6, contract `used-by` definition)

`corpus/knowledge/claim-pin-provenance-r37.md:7` is its only external source clause:
`source: S070 (coreutils sha256sum(1), digest text and --check input, opened 2026-10-23; …)`.
`S070`'s `used-by` cell is `corpus/knowledge/engine-swap-canary-r36.md` only (`corpus/SOURCES.md:80`)
— it does not name `corpus/knowledge/claim-pin-provenance-r37.md`. QUALITY 6 (`corpus/QUALITY.md:17-24`)
requires "≥1 `S###` row … whose status is `mined` and whose `used-by` names this entry"; contract v1
defines `used-by` as "repo-relative paths of the knowledge entries or lessons citing the row"
(`CORPUS.md:107-108`). The C1 entry cites S070 but S070 does not record the citation, so the entry
fails the metadata header as it stands. The lesson states the opposite: "**Status / recheck /
used-by changes:** none in place" (`corpus/lessons/round-37.md:49`).

Fix (allowed in place, logged old→new per rule 2, `CORPUS.md:116-117`): append
`corpus/knowledge/claim-pin-provenance-r37.md` to S070's `used-by` and log the transition in
`lessons/round-37.md`, or drop the S070 citation and rest the entry on an own-work row.

Related, same class, lower impact: `corpus/knowledge/pin-capture-env-r37.md:7` also cites `S068`,
whose `used-by` is `corpus/knowledge/grep-pin-r35.md` only (`corpus/SOURCES.md:78`). The C2 entry
still satisfies QUALITY 6 through S071, but S068's `used-by` is incomplete under the contract's
definition.

### M1 — Lesson Gate records the wrong word count ("6 words" vs 5)

`corpus/lessons/round-37.md:39-40`: "Located quote (6 words by `printf '%s\n' '<quote>' | wc -w`)".
Running that command on the quoted words `remove variable from the environment` prints `5`
(command log C27). The quote is still ≤25 words, so the gate threshold holds, but the record's own
number is refuted by the record's own counting command — number-drift. Fix: change `6` to `5`
(or drop the count and keep the quote).

### M2 — Mistakes evidence pointer is reference-drift (lines 31-35 vs 22-25)

`corpus/lessons/round-37.md:28` cites "`w1/SentNoHarm.md` (round 36) lines 31-35" as where the
recorded battery commands live. In `.ufo/waves/round-36/w1/SentNoHarm.md`, lines 20–27 are the
command/exit-code/deciding-output block (items 1–8; the four no-harm commands at lines 22–25, cwd
stated at line 18), while lines 31–35 are the `## Opened files (access date 2026-10-23)` bullet
list. The cited pointer leads a reader/verifier (the QUALITY 53 check) away from the commands.
Fix: cite lines 22–25 (and line 18 for the cwd); no other content change.

### L1 — S071 anchor names a non-existent section ("OPTIONS")

`corpus/SOURCES.md:81` anchor cell opens `OPTIONS \`-u, --unset=NAME\``. `env.1.gz` has no OPTIONS
heading (`.SH` list: `NAME, SYNOPSIS, DESCRIPTION, SCRIPT OPTION HANDLING, NOTES, AUTHOR,
REPORTING BUGS, COPYRIGHT, SEE ALSO`; the option entries are `.TP` items under `DESCRIPTION`). The
precise decompressed lines `27–28` and the revision are correct, which is why this is graded minor
(a reader lands exactly); but the contract asks for "exact section / heading / page / line", and
the heading is fabricated. Fix: replace `OPTIONS` with `DESCRIPTION, option list` (or just the
lines) in a later append-only correction.

### L2 — No URL in the row's `source` cell and in the lesson `## Gate`

`SOURCES.md:81` `source` cell is title — local path only; `grep -n 'http' corpus/lessons/round-37.md`
exits 1 (no match anywhere in the lesson). CORPUS.md rule 1 (`CORPUS.md:112-114`) requires the
round lesson's Gate to record "the URL" for every new row, and the `source` shape is "title —
canonical URL or DOI (a repo path or command for `own-work`)" (`CORPUS.md:88-90`). A canonical URL
was available at the anchored line itself: line 27 carries
`https://www.gnu.org/software/coreutils/manual/coreutils.html#env-u`. Precedent: S065, S066, S069,
S070 (local man pages) also recorded only paths, whereas S067 recorded a URL explicitly. Graded
minor because the local bytes were opened and hashed (the stronger evidence), but the text of
frozen v1 is not met.

### L3 — r37 index rows land under the Round 32 heading (QUALITY 9)

`corpus/README.md:1038-1039` are appended to the cumulative table whose header is at
`corpus/README.md:1026`, inside the section opened by `## Round32 frontier disposition (2026-10-23)`
(`corpus/README.md:972`) — there is no `## Round 37` heading. QUALITY 9 (`corpus/QUALITY.md:31-38`)
says "an index row lands under its own round's heading." Shared with the r33–r36 rows, so this is a
standing structural deviation rather than a round-37 regression; still actionable (add a
`## Round 37 frontier disposition` heading before the r37 prose/rows).

### L4 (minor, same clause family as QUALITY 6) — entry `source:` lines omit path/URL + exact anchor

`claim-pin-provenance-r37.md:7` and `pin-capture-env-r37.md:7` cite their S-rows with a short
description and date but without the source's URL/repo path and without an exact anchor, while
CORPUS.md requires the entry's `source:` to cite the row "alongside the URL and anchor"
(`CORPUS.md:163-166`) and QUALITY 6 requires "its URL or repo path and an exact anchor"
(`QUALITY.md:17-24`). Precedent: the r36 entries do the same, so this is a carried lane habit, not
a r37-only break. Fix: add `/usr/share/man/man1/{sha256sum,env}.1.gz` and the line anchors to the
two `source:` clauses.

### Non-findings (checked, no defect)

- The two knowledge entries do not *literally* open with `source:` (title, `Lane:`, `Surface:`
  precede), but the trio is the first metadata block, line-start, contiguous, and the freshness
  sweep matches it once per file; identical shape to the landed r34–r36 entries. Treated as
  conformant, not as a defect.
- `teaches` overclaim: none found; the one inferential step ("absent before the child process
  starts") is the documented run-COMMAND semantics (`env.1.gz:11`), and the lesson labels the
  gate's policy choice `[INFERENCE]` rather than as sourced.
- Mistakes rows: classes valid, captured-by `none in-round` explicitly allowed, fixes concrete;
  the row-1 evidence content is accurate (`ExecNoHarmPin.md` really shows `--root .`, `0/17`,
  `0/22`, `0/2`, "Harm" on six rows), only the line pointer is wrong (M2).
- Census numbers, W04 pair, and the before/after histograms are self-consistent and reproduce.
- `w1-spec.json` declares 39 items (39 seats) and `ls .ufo/waves/round-37/w1/*.md | wc -l` = 8, so
  the lesson's "39 dispatched / 8 returned" is accurate; the file lives at
  `.ufo/waves/round-37/w1-spec.json` (not under `w1/`), a basename-precision nit only.

## Command log (verbatim, observed output, exit code)

Long registry listings are marked as elided where noted; every elision was checked for S071/S069/
S070/S068 relevance. Reads via the `read` tool (no exit code): `CORPUS.md:60-175`, `SOURCES.md:1-40`,
`SOURCES.md:75-95`, `lessons/round-37.md` (all), `lessons/round-37.md:28-34:raw`, `lessons/round-36.md:55-72`,
`knowledge/claim-pin-provenance-r37.md` (all), `knowledge/pin-capture-env-r37.md` (all),
`README.md:955-1000`, `README.md:1000-1045`, `QUALITY.md:1-40`, `QUALITY.md:55-75`,
`QUALITY.md:395-440`, `research-gate.sh:3925-3955`.

```
C1  $ git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master; echo "EXIT=$?"
    b905217a7dfdcf58be1f0a4c0bf5f2d2d32a2d65
    EXIT=0

C2  $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && wc -l corpus/SOURCES.md corpus/lessons/round-37.md corpus/README.md corpus/QUALITY.md; echo "EXIT=$?"
      252 corpus/SOURCES.md
       62 corpus/lessons/round-37.md
     1039 corpus/README.md
      440 corpus/QUALITY.md
    EXIT=0

C3  $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && grep -n 'S071' corpus/SOURCES.md; echo "EXIT=$?"
    81:| S071 | GNU coreutils `env(1)` manual — `/usr/share/man/man1/env.1.gz` | docs | A | … | mined | 2026-10-23 | on-release | corpus/knowledge/pin-capture-env-r37.md |
    EXIT=0

C4  $ ls -la /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/ | grep -i 'r37\|pin-capture'; echo "EXIT=$?"
    -rw-r--r-- 1 vgpnk vgpnk 3079 Oct 23 23:31 claim-pin-provenance-r37.md
    -rw-r--r-- 1 vgpnk vgpnk 3501 Oct 23 23:31 pin-capture-env-r37.md
    EXIT=0

C5  $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && sed -n '1,80p' CORPUS.md 2>/dev/null || ls -la; echo "EXIT=$?"
    [fleet-root file absent; the `ls -la` alternative printed 16 entries incl. corpus/, tools/, SKILL.md]
    EXIT=0

C6  $ zcat /usr/share/man/man1/env.1.gz | sed -n '25,30p'; echo "EXIT=$?"
    end each output line with NUL, not newline
    .TP
    \X'tty: link https://www.gnu.org/software/coreutils/manual/coreutils.html#env-u'\fB\-u, \-\-unset=\,NAME\fP\X'tty: link'\/\fR
    remove variable from the environment
    .TP
    \X'tty: link https://www.gnu.org/software/coreutils/manual/coreutils.html#env-C'\fB\-C, \-\-chdir=\,DIR\fP\X'tty: link'\/\fR
    EXIT=0

C7  $ sha256sum /usr/share/man/man1/env.1.gz; echo "EXIT=$?"; coreutils --version | head -1; echo "EXIT=$?"
    4ae797e6e280da9d514bc94f3fbceffac5d0ceb62c197f78bb04bee84a78fb27  /usr/share/man/man1/env.1.gz
    EXIT=0
    error: command not found: coreutils
    EXIT=0

C8  $ zcat /usr/share/man/man1/env.1.gz | nl -ba | sed -n '1,32p'; echo "EXIT=$?"
         1  .\" DO NOT MODIFY THIS FILE!  It was generated by help2man 1.50.1.
         2  .TH ENV "1" "September 2026" "GNU coreutils 9.12" "User Commands"
         3  .SH NAME
         4  env \- run a program in a modified environment
         5  .SH SYNOPSIS
         6  .B env
         7  [\fI\,OPTION\/\fR]... [\fI\,-\/\fR] [\fI\,NAME=VALUE\/\fR]... [\fI\,COMMAND \/\fR[\fI\,ARG\/\fR]...]
         8  .SH DESCRIPTION
         9  .\" Add any additional description here
        10  .PP
        11  Set each NAME to VALUE in the environment and run COMMAND.
        12  .PP
        13  Mandatory arguments to long options are mandatory for short options too.
        14  .TP
        15  \X'tty: link https://www.gnu.org/software/coreutils/manual/coreutils.html#env-a'\fB\-a, \-\-argv0=\,ARG\fP\X'tty: link'\/\fR
        16  pass ARG as the zeroth argument of COMMAND
        17  .TP
        18  \X'tty: link https://www.gnu.org/software/coreutils/manual/coreutils.html#env-i'\fB\-i, \-\-ignore\-environment\fP\X'tty: link'
        19  start with an empty environment
        20  .TP
        21  \X'tty: link https://www.gnu.org/software/coreutils/manual/coreutils.html#env--env0-from'\fB\-\-env0\-from=FILE\fP\X'tty: link'
        22  read NUL\-delimited environment entries from FILE
        23  .TP
        24  \X'tty: link https://www.gnu.org/software/coreutils/manual/coreutils.html#env-0'\fB\-0, \-\-null\fP\X'tty: link'
        25  end each output line with NUL, not newline
        26  .TP
        27  \X'tty: link https://www.gnu.org/software/coreutils/manual/coreutils.html#env-u'\fB\-u, \-\-unset=\,NAME\fP\X'tty: link'\/\fR
        28  remove variable from the environment
        29  .TP
        30  \X'tty: link https://www.gnu.org/software/coreutils/manual/coreutils.html#env-C'\fB\-C, \-\-chdir=\,DIR\fP\X'tty: link'\/\fR
        31  change working directory to DIR
        32  .TP
    EXIT=0

C9  $ zcat /usr/share/man/man1/env.1.gz | tail -8; echo "EXIT=$?"; pacman -Q coreutils; echo "EXIT=$?"; env --version | head -2; echo "EXIT=$?"
    There is NO WARRANTY, to the extent permitted by law.
    .SH "SEE ALSO"
    \fBsigaction\fP(2), \fBsigprocmask\fP(2), \fBsignal\fP(7)
    …
    coreutils 9.12-2
    EXIT=0
    env 0.8.0
    EXIT=0

C10 $ type -a env; echo "---"; ls -l /usr/bin/env; echo "---"; /usr/bin/env --version | head -1; echo "EXIT=$?"; echo "PATH=$PATH"
    env is a shell builtin
    env is /usr/bin/env
    ---
    -rwxr-xr-x 1 root root 68312 Sep 17 07:16 /usr/bin/env
    ---
    env (GNU coreutils) 9.12
    EXIT=0
    PATH=/run/user/1000/fnm_multishells/…:/home/vgpnk/.local/bin:…:/usr/bin:…
    (the harness shell exposes an `env` builtin reporting 0.8.0; bash resolves PATH, see C11)

C11 $ bash -c 'type -a env; command -v env; env --version | head -1'; echo "EXIT=$?"; for d in $(echo "$PATH" | tr ':' ' '); do [ -x "$d/env" ] && echo "FOUND $d/env"; done; echo "EXIT=$?"
    env is /usr/bin/env
    /usr/bin/env
    env (GNU coreutils) 9.12
    EXIT=0
    FOUND /usr/bin/env
    EXIT=1

C12 $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && grep -n 'BASH_ENV\|env -u\|env ' tools/research-gate.sh | head -40; echo "EXIT=$?"
    1:#!/usr/bin/env bash
    … (352, 357, 375 comments)
    3935:    env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_STRICT -u CHOUSA_ROOT \
    3936:      -u CHOUSA_AGGREGATOR_ERE -u CHOUSA_GREP_PIN_ECHO -u BASH_ENV \
    … (selftest env uses 4245–8211, elided)
    EXIT=0

C13 $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && grep -n 'pin-capture-env-r37\|claim-pin-provenance-r37' corpus/README.md; echo "EXIT=$?"; grep -n '^## 53\|^53\.\|53\.' corpus/QUALITY.md | head; echo "EXIT=$?"
    1018:through one pinned absolute `sha256sum` (`knowledge/claim-pin-provenance-r37.md`,
    1020:`--pin` capture child scrubs `BASH_ENV` with `env -u` (`knowledge/pin-capture-env-r37.md`,
    1038:| `knowledge/claim-pin-provenance-r37.md` | … | `S070`; `evidence/round37/claims.md`; `evidence/round37/receipts/c1-*.json` |
    1039:| `knowledge/pin-capture-env-r37.md` | … | `S071`, `S068`; `evidence/round37/claims.md`; `evidence/round37/receipts/c2-*.json` |
    EXIT=0
    430:53. **A no-harm battery's commands are re-used verbatim from their pinned record.** A battery
    EXIT=0

C14 $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && grep -n 'shown able to fail' corpus/QUALITY.md; echo "EXIT=$?"
    [no output]
    EXIT=1

C15 $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && ls corpus/evidence/round37/receipts/ 2>&1 | head -30; echo "EXIT=$?"; ls corpus/evidence/round37/claims.md; echo "EXIT=$?"
    c1-after-s37001.json / c1-after-s37701.json / c1-after-s37901.json / c1-after-s37921.json /
    c1-base-s37001.json / c2-after-s37021.json / c2-after-s37721.json / c2-after-s37941.json /
    c2-after-s37961.json / c2-base-s37021.json
    EXIT=0
    corpus/evidence/round37/claims.md
    EXIT=0

C16 $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && awk -F'|' '/^\| *S[0-9]+/ {gsub(/ /,"",$2); print NR": id="$2" NF="NF}' corpus/SOURCES.md | awk -F'NF=' '{print $2}' | sort | uniq -c; echo "EXIT=$?"
         71 13
    EXIT=0

C17 $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && awk -F'|' '/^\| *S[0-9]+/ {id=$2; gsub(/ /,"",id); print id}' corpus/SOURCES.md | sort | uniq -d; echo "DUP_EXIT=$?"; awk -F'|' '/^\| *S[0-9]+/ {id=$2; gsub(/ /,"",id); print id}' corpus/SOURCES.md | sort -c 2>&1; echo "EXIT=$?"
    DUP_EXIT=0
    EXIT=0

C18 $ cd /home/vgpnk/Projects/shokunin && grep -n 'SOURCES.md' CORPUS.md | head -20; echo "EXIT=$?"
    13, 64, 70, 121, 135, 137, 139, 141, 143, 145, 147, 165 (line numbers)
    EXIT=0

C19 $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && sed -n '75,95p' corpus/SOURCES.md; echo "EXIT=$?"
    [S065–S071 rows + `## Paths` opening; elided except S071 shown at C3]
    EXIT=0

C20 $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && head -12 corpus/knowledge/engine-swap-canary-r36.md; echo "===="; head -12 corpus/knowledge/per-record-argv-attribution-r36.md; echo "EXIT=$?"
    # The engine-swap canary — fourteen pin/contract scenarios, four new separations
    Lane: chousa. Round 36 (C1, operability). Surface: …
    source: S070 (coreutils `sha256sum(1)`, digest text and `--check` input, opened 2026-10-23);
    …
    ====
    # Per-record argv attribution — witnessing the matcher through the engine's own argv
    Lane: chousa. Round 36 (C2, calibration). …
    source: S069 (GNU `grep(1)`, `-o` plus `-b` offset semantics, opened 2026-10-23); …
    EXIT=0

C21 $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && grep -n 'provenance trio\|verified-at\|recheck *:' corpus/QUALITY.md | head -20; echo "EXIT=$?"
    20:   an exact anchor), `verified-at:` (ISO date + what was checked) and
    21:   `recheck:` (an ISO date or a cadence — `90d`, `180d`, `365d`, `on-release` —
    22:   optionally followed by the re-run command). A `recheck:` that is only a
    59:13. **Runnable recheck.** A new `recheck:` command states its cwd and names
    64:    `! grep -nE '^recheck:.*--root +"?[^/$"]' corpus/knowledge/citation-chain-fidelity-r24.md`
    EXIT=0

C22 $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && grep -n 'S070' corpus/lessons/round-36.md | head; echo "EXIT=$?"
    51, 60, 71, 80, 89, 108, 110
    EXIT=0

C23 $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && awk -F'|' '/^\| *S0(68|70|71) / {print NR": "$2"|USED-BY="$12}' corpus/SOURCES.md; echo "EXIT=$?"; grep -c 'claim-pin-provenance-r37\|pin-capture-env-r37' corpus/SOURCES.md; echo "EXIT=$?"
    78:  S068 |USED-BY= corpus/knowledge/grep-pin-r35.md
    80:  S070 |USED-BY= corpus/knowledge/engine-swap-canary-r36.md
    81:  S071 |USED-BY= corpus/knowledge/pin-capture-env-r37.md
    EXIT=0
    1
    EXIT=0

C24 $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && head -8 corpus/knowledge/grep-pin-r35.md; echo "===="; head -8 corpus/knowledge/long-span-argv-r34.md; echo "EXIT=$?"
    # Pinned tool provenance — one absolute, verified grep
    Lane: chousa. Round 35 (C1). …
    source: S067 (exec(3), PATH search) and S068 (bash(1), `BASH_ENV`), both opened 2026-10-23;
    ====
    # Verifying long claim spans without an oversized argv pattern — round 34

    source: S064 (Linux `execve(2)`, `MAX_ARG_STRLEN`); S065 …; S066 …; lane contract …
    verified-at: 2026-10-23 (…)
    recheck: on-release (…)
    EXIT=0

C25 $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && zcat /usr/share/man/man1/env.1.gz | grep -n '^\.SS'; echo "SS_EXIT=$?"; zcat /usr/share/man/man1/grep.1.gz | grep -n '^\.SH\|^\.SS' | head -25; echo "EXIT=$?"
    63:.SS "Exit status:"
    SS_EXIT=0
    138:.SH NAME … 190:.SH OPTIONS … 191:.SS "Generic Program Information" … 382:.SS "Output Line Prefix Control" …
    EXIT=0

C26 $ zcat /usr/share/man/man1/env.1.gz | grep -n '^\.SH'; echo "---- total lines:"; zcat /usr/share/man/man1/env.1.gz | wc -l; echo "---- unset mentions:"; zcat /usr/share/man/man1/env.1.gz | grep -n 'unset'; echo "EXIT=$?"
    3:.SH NAME
    5:.SH SYNOPSIS
    8:.SH DESCRIPTION
    79:.SH "SCRIPT OPTION HANDLING"
    109:.SH NOTES
    118:.SH AUTHOR
    120:.SH "REPORTING BUGS"
    128:.SH COPYRIGHT
    134:.SH "SEE ALSO"
    ---- total lines:
    140
    ---- unset mentions:
    27:\X'tty: link …#env-u'\fB\-u, \-\-unset=\,NAME\fP…
    EXIT=0

C27 $ FOO=visible /usr/bin/env -u FOO /usr/bin/sh -c 'printf "FOO=%s\n" "${FOO-unset}"'; echo "EXIT=$?"; printf '%s\n' 'remove variable from the environment' | wc -w; echo "EXIT=$?"
    FOO=unset
    EXIT=0
    5
    EXIT=0

C28 $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && echo "rows:"; grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md; echo "malformed:"; awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md; echo "tier:"; awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md; echo "status:"; awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md; echo "dups:"; awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' corpus/SOURCES.md | sort | uniq -d; echo "enums:"; awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {i=$2;k=$4;t=$5;s=$9; gsub(/[[:space:]]/,"",i); gsub(/[[:space:]]/,"",k); gsub(/[[:space:]]/,"",t); gsub(/[[:space:]]/,"",s); if (t !~ /^[ABC]$/) print "tier", i, t; if (s !~ /^(queued|mined|rejected)$/) print "status", i, s; if (k !~ /^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$/) print "kind", i, k; if (t=="A" && k=="community") print "tier-inflation", i}' corpus/SOURCES.md; echo "missing-used-by:"; awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {s=$9; gsub(/[[:space:]]/,"",s); if (s=="mined") {n=split($12, a, /[,;]/); for (j=1;j<=n;j++) {p=a[j]; gsub(/^[[:space:]]+|[[:space:]]+$/,"",p); if (p!="" && p!="—") print p}}}' corpus/SOURCES.md | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done; echo "DONE"
    rows:
    71
    malformed:
    0
    tier:
    A=65 B=1 C=5
    status:
    mined=48 queued=19 rejected=4
    dups:
    enums:
    missing-used-by:
    DONE

C29 $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && ls .ufo/waves/round-37/w1/ExecNoHarmPin.md 2>&1; echo "EXIT=$?"; ls corpus/evidence/round37/receipts/c1-*.json | wc -l; ls corpus/evidence/round37/receipts/c2-*.json | wc -l; echo "EXIT=$?"
    .ufo/waves/round-37/w1/ExecNoHarmPin.md
    EXIT=0
    5
    5
    EXIT=0

C30 $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && awk -F'|' '/^\| *S071 / {print "NF="NF; for(i=2;i<=NF-1;i++) printf "col%d=[%s]\n", i-1, substr($i,1,40)}' corpus/SOURCES.md; echo "EXIT=$?"
    NF=13
    col1=[ S071 ]
    col2=[ GNU coreutils `env(1)` manual — `/usr/s ]
    col3=[ docs ]
    col4=[ A ]
    col5=[ the `-u`/`--unset` option semantics of ]
    col6=[ OPTIONS `-u, --unset=NAME` (decompresse ]
    col7=[ `env -u NAME` removes NAME from the env ]
    col8=[ mined ]
    col9=[ 2026-10-23 ]
    col10=[ on-release ]
    col11=[ corpus/knowledge/pin-capture-env-r37.md ]
    EXIT=0

C31 $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && grep -n '^## ' corpus/README.md | tail -12; echo "EXIT=$?"
    149, 158, 166, 174, 348, 863, 895, 911, 933, 944, 960, 972 (Round-8 … Round32 frontier disposition)

C32 $ ls -la /home/vgpnk/Projects/shokunin/scripts/sources-census.sh 2>&1; grep -n 'W04' /home/vgpnk/Projects/shokunin/scripts/sources-census.sh 2>&1 | head -10; echo "EXIT=$?"
    -rwxr-xr-x 1 vgpnk vgpnk 35466 Oct 19 21:22 /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
    33:# W04 same URL across scopes (warnings do not affect clean lanes)
    361:  checkline "W04-scope-sensitive-mutant" \
    362:    $'scope-shokunin\tW04\tS902 duplicate url dup.example/source across scopes' \
    364:  checkx "W04-does-not-fail-validation" 0 \
    645:          printf "%s\tW04\t%s duplicate url %s across scopes\n",lane,id,u
    EXIT=0

C33 $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && awk -F'|' '/^\| *S0(51|53) / {print $2"|"$3"|"$5"|"$6}' corpus/SOURCES.md; echo "EXIT=$?"
     S051 | HTML 5.2 … https://www.w3.org/TR/2017/REC-html52-20171214/syntax.html#the-in-head-insertion-mode | A | the HTML 5.2 tree-construction rules … |
     S053 | Python socket documentation … https://docs.python.org/3/library/socket.html#socket.create_connection | A | documented create_connection behavior … |
    EXIT=0

C34 $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && grep -n '^source:\|^verified-at:\|^recheck:' corpus/knowledge/claim-pin-provenance-r37.md corpus/knowledge/pin-capture-env-r37.md; echo "EXIT=$?"; echo "---- sweep regex:"; grep -cE '^[-* ]*recheck *:' corpus/knowledge/pin-capture-env-r37.md corpus/knowledge/claim-pin-provenance-r37.md; echo "EXIT=$?"
    claim-pin-provenance-r37.md:7:source: S070 (coreutils `sha256sum(1)`, …
    claim-pin-provenance-r37.md:15:verified-at: 2026-10-23 …
    claim-pin-provenance-r37.md:17:recheck: on-release (`python3 corpus/evidence/round37/c1-count.py …`)
    pin-capture-env-r37.md:7:source: S071 (coreutils `env(1)` `-u`/`--unset` semantics, opened 2026-10-23 —
    pin-capture-env-r37.md:15:verified-at: 2026-10-23 …
    pin-capture-env-r37.md:17:recheck: on-release (`python3 corpus/evidence/round37/c2-count.py …`)
    EXIT=0
    ---- sweep regex:
    pin-capture-env-r37.md:1
    claim-pin-provenance-r37.md:1
    EXIT=0

C35 $ cd /home/vgpnk/Projects/shokunin && grep -n 'validate)' scripts/sources-census.sh | head; echo "EXIT=$?"; grep -n 'OUTDIR\|>.*receipt\|tee ' scripts/sources-census.sh | head -15; echo "EXIT=$?"
    737:    validate)
    EXIT=0
    EXIT=0

C36 $ cd /home/vgpnk/Projects/shokunin && sed -n '600,670p' scripts/sources-census.sh; echo "EXIT=$?"   # url_of + W04 logic; read, confirmed same-URL/different-scope rule
C37 $ cd /home/vgpnk/Projects/shokunin && sed -n '720,780p' scripts/sources-census.sh; echo "EXIT=$?"   # validate mode: emit out_sink (stdout when OUT unset); no writes on validate path
    EXIT=0

C38 $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && gawk -F'|' '…url_of… /^\| *S[0-9][0-9][0-9]+ *\|/ {…}' corpus/SOURCES.md; echo "EXIT=$?"
    W04 S051 url=www.w3.org/TR/2017/REC-html52-20171214/syntax.html scopes_differ: S050 vs S051
    W04 S053 url=docs.python.org/3/library/socket.html scopes_differ: S052 vs S053
    EXIT=0

C39 $ cd /tmp && /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa; echo "EXIT=$?"
    chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
    chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
    chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
    EXIT=0

C40 $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && awk -F'|' '/^\| *S0(67|69) / {print $2"|USED-BY="$12}' corpus/SOURCES.md; echo "EXIT=$?"
     S067 |USED-BY= corpus/knowledge/grep-pin-r35.md
     S069 |USED-BY= corpus/knowledge/per-record-argv-attribution-r36.md
    EXIT=0

C41 $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && ls .ufo/waves/round-37/w1/*.md | wc -l; echo "EXIT=$?"; ls .ufo/waves/round-37/w1/w1-spec.json 2>&1; echo "EXIT=$?"; ls .ufo/waves/round-36/w1/SentNoHarm.md 2>&1; echo "EXIT=$?"
    8
    EXIT=0
    ls: cannot access '.ufo/waves/round-37/w1/w1-spec.json': No such file or directory
    EXIT=2
    .ufo/waves/round-36/w1/SentNoHarm.md
    EXIT=0

C42 $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && sed -n '31,35p' .ufo/waves/round-36/w1/SentNoHarm.md 2>&1; echo "EXIT=$?"
    - `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1-briefs/SentNoHarm.md`
    - `/home/vgpnk/.omp/agent/RULES.md`
    - `/home/vgpnk/Projects/shokunin/chousa-shokunin/SKILL.md`
    - `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/fixtures/claims-r2.README.md`
    - `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/fixtures/chain-r3.README.md`
    EXIT=0

C43 $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && grep -rn "round's heading\|index row" .ufo/waves/round-36 .ufo/waves/round-35 2>/dev/null | head -10; echo "EXIT=$?"
    [no output]
    EXIT=0

C44 $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && find .ufo/waves/round-37 -name 'w1-spec.json' 2>/dev/null; echo "EXIT=$?"; grep -n 'root \.\.\|--root\|claims-r1\|chain-r1\|battery\|command' .ufo/waves/round-36/w1/SentNoHarm.md | head -20; echo "EXIT=$?"
    .ufo/waves/round-37/w1-spec.json
    EXIT=0
    18, 22, 23, 24, 25 (cwd + the four command lines)
    EXIT=0

C45 $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && ls .ufo/waves/round-37/w1/*.md; echo "EXIT=$?"; python3 -c 'import json;d=json.load(open(".ufo/waves/round-37/w1-spec.json"));print(type(d).__name__); print(list(d)[:6] if isinstance(d,dict) else len(d)); print(json.dumps(d.get("seats") and len(d["seats"]) or d.get("seat_count") if isinstance(d,dict) else None))'; echo "EXIT=$?"
    .ufo/waves/round-37/w1/{ExecC1BaseRederive,ExecC1LandedRederive,ExecC2BaseRederive,ExecC2LandedRederive,ExecMutC1Counter,ExecMutGateC1,ExecMutGateC2,ExecNoHarmPin}.md
    EXIT=0
    dict
    ['wave', 'milestone', 'reportDir', 'axes', 'context', 'items']
    null
    EXIT=0

C46 $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && python3 - <<'EOF' … print('items', len(d['items'])) … EOF
    items 39
    Counter({'?': 39})
    keys ['name', 'role', 'prompt']
    EXIT=0

C47 $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && nl -ba .ufo/waves/round-36/w1/SentNoHarm.md | sed -n '14,40p'; echo "EXIT=$?"
     16  ## Commands run, exit codes, deciding output
     18  All observable commands ran from …; command text below is verbatim.
     20  1. `timeout 900s git rev-parse master` — exit 0. Output: `700bd5fc…`
     21  2. `timeout 900s sha256sum …` — exit 0 …
     22  3. `timeout 900s bash -c 'bash tools/research-gate.sh verify-claims corpus/fixtures/claims-r2.jsonl --root ..; …'` — exit 0 …
     23  4. … verify-chain corpus/fixtures/chain-r3.md --root .. …
     24  5. … verify-chain corpus/fixtures/chain-r3-broken.md --root .. …
     25  6. … python3 … VERDICT_BEARING_EXPORTS=3/3 …
     26  7. … mkdir -p … EXIT_CODE=0
     27  8. … sha256sum … no-harm-receipt.txt
     29  ## Opened files (access date 2026-10-23)
     31-35 [five bullet bullets — file paths]
    EXIT=0

C48 $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && grep -n 'http' corpus/lessons/round-37.md; echo "GREP_EXIT=$?"; sed -n '35,62p' corpus/lessons/round-37.md; echo "EXIT=$?"
    GREP_EXIT=1
    [lesson lines 35–62: Gate S071 bullet, rejected candidates, used-by-none, census receipt, knowledge candidates, spot-check pending, sourced claim]
    EXIT=0

C49 $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && grep -n 'root \.\|Harm\|0/17\|0/22\|0/2' .ufo/waves/round-37/w1/ExecNoHarmPin.md | head -20; echo "EXIT=$?"
    1:# ExecNoHarmPin
    11:| Claims fixture | `verify-claims … --root .` | `VERDICT_BEARING_CLAIMS=0/17` … | Harm: 0/17 |
    12:| Chain fixture | `… --root .` | `RESOLVED_HOPS=0/22` … | Harm: 0/22 |
    13:| Broken chain control | `… --root .` | `RESOLVED_HOPS=0/2` … | Harm: 0/2 |
    14-16| Archive A/B/C | `verify … --root ..` | DRIFT … | Harm: per-input verify DRIFT … |
    21-39 [command echoes with 0/17, 0/22, 0/2]
    45-47 [explanations]
    EXIT=0

C50 $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && grep -n '^## \|6 words\|lines 31-35\|used-by changes\|W04' corpus/lessons/round-37.md; echo "EXIT=$?"
    24:## Mistakes
    28:| scope (a counting command … ) | `w1/ExecNoHarmPin.md`: … recorded commands live in `w1/SentNoHarm.md` (round 36) lines 31-35 — …
    31:## Gate
    33:Rows added this round: **S071** (70 → 71 rows; census `validate` exit 0, W04 ×2 standing for
    39:  `4ae797e6…`. Located quote (6 words
    49:- **Status / recheck / used-by changes:** none in place. S071 enters `mined` with its `used-by`
    53:  malformed 0, W04 ×2. Before (round start): exit 0, 70 rows (A 64 / B 1 / C 5; mined 47 /
    EXIT=0

C51 $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && grep -c '^| *S071 ' corpus/SOURCES.md; echo "EXIT=$?"; awk -F'|' '/^\| *S0(68|70|71) / {printf "%d %s used-by=[%s]\n", NR, $2, $12}' corpus/SOURCES.md; echo "EXIT=$?"
    1
    EXIT=0
    78  S068  used-by=[ corpus/knowledge/grep-pin-r35.md ]
    80  S070  used-by=[ corpus/knowledge/engine-swap-canary-r36.md ]
    81  S071  used-by=[ corpus/knowledge/pin-capture-env-r37.md ]
    EXIT=0

C52 $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && sed -n '81p' corpus/SOURCES.md | head -c 400; echo; echo "EXIT=$?"; awk -F'|' 'NR==81{print "anchor=["$7"]"}' corpus/SOURCES.md; echo "EXIT=$?"
    | S071 | GNU coreutils `env(1)` manual — `/usr/share/man/man1/env.1.gz` | docs | A | the `-u`/`--unset` option semantics … | OPTIONS `-u, --unset=NAME` (decompressed lines 27–28; quote at line 28); …
    EXIT=0
    anchor=[ OPTIONS `-u, --unset=NAME` (decompressed lines 27–28; quote at line 28); coreutils 9.12 (September 2026), installed `coreutils 9.12-2`; file SHA-256 `4ae797e6e280da9d514bc94f3fbceffac5d0ceb62c197f78bb04bee84a78fb27` (opened locally 2026-10-23) ]
    EXIT=0

C53 $ cd /home/vgpnk/Projects/shokunin && grep -n '^6\. \|^13\. \|^53\. ' chousa-shokunin/corpus/QUALITY.md; echo "EXIT=$?"; grep -n 'used-by\|A new knowledge entry opens' CORPUS.md; echo "EXIT=$?"; grep -n '^| Entry | What it holds | Evidence |' chousa-shokunin/corpus/README.md; echo "EXIT=$?"
    17:6. **Metadata header.** A `knowledge/` entry admitted from round 24 on opens
    59:13. **Runnable recheck.** A new `recheck:` command states its cwd and names
    430:53. **A no-harm battery's commands are re-used verbatim from their pinned record.** A battery
    EXIT=0
    86:| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
    103:- `status` — `queued` … `mined` (cited by ≥1 path in `used-by`) ·
    107:- `used-by` — repo-relative paths of the knowledge entries or lessons citing the row,
    116:2. **Append-only.** Only `status`, `recheck` and `used-by` change in place, and each change
    146:# mined rows whose used-by paths do not exist — must print nothing
    163:- **A new knowledge entry opens with its provenance trio.** `source:`,
    EXIT=0
    1026:| Entry | What it holds | Evidence |
    EXIT=0

C54 $ cd /home/vgpnk/Projects/shokunin && grep -n 'A row is a claim\|records, for every new row' CORPUS.md; echo "EXIT=$?"
    112:1. **A row is a claim.** Write it only after opening the source in the round that writes
    113:   the row. The round lesson's `## Gate` records, for every new row, the URL, the access
    EXIT=0

C55 $ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && ls -la .ufo/waves/round-37/residual/ 2>&1; echo "EXIT=$?"; git status --porcelain corpus/SOURCES.md corpus/lessons/round-37.md corpus/knowledge/ corpus/README.md corpus/QUALITY.md; echo "EXIT=$?"
    -rw-r--r-- 1 vgpnk vgpnk 89019 Oct 23 23:41 CritC2Kill.md
    -rw-r--r-- 1 vgpnk vgpnk 50269 Oct 23 23:41 RevSeparability.md
    EXIT=0
     M corpus/QUALITY.md
     M corpus/README.md
     M corpus/SOURCES.md
    ?? corpus/knowledge/claim-pin-provenance-r37.md
    ?? corpus/knowledge/pin-capture-env-r37.md
    ?? corpus/lessons/round-37.md
    EXIT=0
```

## Residual risk and verification gaps

- **`env` is not pinned in the gate; S071's scope cell is still accurate.** The capture child runs
  bare `env -u … -u BASH_ENV` (`tools/research-gate.sh:3935-3936`), so a caller PATH shim named
  `env` could substitute the scrubber — the same PATH class C1 closed for `sha256sum` and round 35
  closed for `grep`. This is outside S071's scope ("not the gate's capture policy") and outside
  this review's assigned checks, but it is a live seam in C2's threat model: the C2 claim's named
  limits (claims.md §Limits as quoted in `knowledge/pin-capture-env-r37.md`) do not name an
  `env`-shim vector. On this host bash resolves `env` to `/usr/bin/env` (coreutils 9.12) and no
  earlier PATH entry carries an `env` binary (C10/C11).
- **Harness-shell artifact, not a lane defect.** The agent harness's temporary shell has an `env`
  builtin reporting `env 0.8.0` (C9), while bash/`/usr/bin/env` is GNU coreutils 9.12 (C10/C11).
  Anyone re-checking the row from that shell should use `/usr/bin/env --version`.
- **Census before-state is not re-derivable from the current file.** The lesson's "Before (round
  start): 70 rows (A 64 / B 1 / C 5; mined 47 / queued 19 / rejected 4)" is arithmetically
  consistent with the after-state (each +1 on A/mined) but I did not have the pre-round file; the
  after-state and W04 pair reproduce exactly (C39/C28).
- **README receipts globs assert only existence, not freshness.** `c1-*.json`/`c2-*.json` = 5 each
  in `corpus/evidence/round37/receipts/`; the entries claim 7/7 on six seeds each, with the
  remaining seed evidence attributed to wave seat reports. I did not audit receipt contents
  against the counters (out of this seat's assigned scope; the counters are another seat's target).
- **No `lsp` server was available**, so name/definition checks (e.g., `gate_canonical_capture`,
  `S070`/`S071` usage) rest on text search and the frozen census, not semantic resolution; an empty
  cold result was not used as evidence of absence.
- **Working tree, not a landed commit.** The reviewed corpus files are uncommitted at tip
  `b905217`; if the L1 amends them before committing, the findings above must be re-checked
  against the committed bytes (the digests/line anchors, not the prose, are the durable evidence).
