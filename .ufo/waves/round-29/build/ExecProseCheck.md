# Round 29 — seat ExecProseCheck — scoped report

Seat: ExecProseCheck (lane executor, wave 1 build). Lane root:
`/home/vgpnk/Projects/shokunin/chousa-shokunin`. Date of run: 2026-10-22.

## What I did

Wrote one standalone stdlib-only checker that implements the two routed
defects D1 and D2 from `corpus/lessons/round-28-verifier-spotcheck.md`
("Routed defects (lane fixes next round)", items 2 and 3).

Deliverable:

- `.ufo/waves/round-29/build/ExecProseCheck/prose-check.py` (126 lines,
  Python 3.14.8, stdlib only: `re`, `sys`, `pathlib.Path`).

Usage is exactly `python3 prose-check.py FILE...`. For each file it prints the
file name, the count of digit-glued tokens, each offending token with its
line numbers, the count of custody-vocabulary hits, and each matched term
with its line number. A final `TOTAL hits=N files=M` line closes the run.

Check (a) D1: regex `\b[a-z]+[0-9]{2,}\b` over prose.
Check (b) D2: case-insensitive match of the six terms `Parent approval`,
`Parent decision`, `CURRENT_MAIN_DIRECTIVE`, `report-LAST`, `Root report`,
`private original`.

Exclusions are listed explicitly in the script header, as required:
inline backtick code spans, fenced code blocks (``` and ~~~), URLs
(`scheme://...` and `www....`), and the non-prose identifier forms
sha1 sha256 sha512 md5 base64 utf8, x86 arm64, ipv4 ipv6, h1 h2 h3 h4 h5 h6,
source ids `S###` and round ids `r##` (either case). The header also states
the scope rule: the code-span, fence and URL exclusions apply to check (a)
only, while check (b) runs over the whole file text, because D2 is a
vocabulary ban and the custody vocabulary must not appear anywhere in a lane
record.

Exit codes: 0 when no hit, 1 when any hit, 2 on usage error (no FILE
argument) or unreadable file.

## Evidence

Command, exit code and output for the three required runs (run from the lane
root, `timeout 60` on every call):

### A. clean synthetic file (expect 0 hits)

```
$ python3 .ufo/waves/round-29/build/ExecProseCheck/prose-check.py \
    .ufo/waves/round-29/build/ExecProseCheck/clean-sample.md
FILE .ufo/waves/round-29/build/ExecProseCheck/clean-sample.md
  digit-glued tokens: 0
  custody vocabulary: 0
TOTAL hits=0 files=1
exit=0
```

The synthetic file is `.ufo/waves/round-29/build/ExecProseCheck/clean-sample.md`.
It carries separated digits in prose (`all 69`, `64 proposals`, `on 2026-10-21`,
`at most 25 words`), every excluded identifier form, a fenced block full of
glued tokens and one glued-token URL, and no custody vocabulary.

### B. `corpus/lessons/round-28.md` (expect hits)

```
$ python3 .ufo/waves/round-29/build/ExecProseCheck/prose-check.py corpus/lessons/round-28.md
FILE corpus/lessons/round-28.md
  digit-glued tokens: 9
    actual64 x1 (lines 26)
    all69 x1 (lines 26)
    blanket64 x1 (lines 30)
    legacy161 x2 (lines 11, 19)
    most25 x1 (lines 48)
    on2026 x1 (lines 46)
    original187 x1 (lines 11)
    proposal64 x1 (lines 26)
  custody vocabulary: 5
    'CURRENT_MAIN_DIRECTIVE' at line 53
    'Parent decision' at line 5
    'Root report' at line 63
    'private original' at line 39
    'report-LAST' at line 63
TOTAL hits=14 files=1
exit=1
```

### C. `corpus/lessons/round-28-verifier-spotcheck.md` (expect hits)

```
$ python3 .ufo/waves/round-29/build/ExecProseCheck/prose-check.py corpus/lessons/round-28-verifier-spotcheck.md
FILE corpus/lessons/round-28-verifier-spotcheck.md
  digit-glued tokens: 1
    mined20 x1 (lines 73)
  custody vocabulary: 5
    'CURRENT_MAIN_DIRECTIVE' at line 47
    'Parent approval' at line 47
    'Parent approval' at line 129
    'private original' at line 14
    'report-LAST' at line 48
TOTAL hits=6 files=1
exit=1
```

Extra checks:

```
$ python3 .ufo/waves/round-29/build/ExecProseCheck/prose-check.py
usage: python3 prose-check.py FILE...
exit=2

$ python3 .ufo/waves/round-29/build/ExecProseCheck/prose-check.py /nonexistent/x.md
/nonexistent/x.md: cannot read file: [Errno 2] No such file or directory: '/nonexistent/x.md'
exit=2

$ python3 .ufo/waves/round-29/build/ExecProseCheck/prose-check.py \
    .ufo/waves/round-29/build/ExecProseCheck/clean-sample.md corpus/lessons/round-28.md
exit=1
```

An exclusion fixture, `.ufo/waves/round-29/build/ExecProseCheck/exclusions-sample.md`,
mixes every excluded form with five glued tokens and yields exactly five
digit-glued hits (all69, diagnosis53, most25, on2026, proposal64) and zero
custody hits, exit 1. It confirms that `sha256`, `sha512`, `sha1`, `md5`,
`base64`, `utf8`, `x86`, `arm64`, `ipv4`, `ipv6`, `h1` to `h6`, `S046`,
`s047`, `S999`, `r29` and `R44` are not flagged, and that a glued token inside
a backtick span is silent.

`python3 -m py_compile` on the script: exit 0.

## Verdict

The checker fails on both defect files (exit 1, non-empty hit lists) and
passes on the clean synthetic file (exit 0, empty lists), so it can fail and
it does. Both routed defects are covered: D1 by the token regex with its
documented exclusions, D2 by the six-term case-insensitive vocabulary list.

Note on the spotcheck file: the glued tokens it lists at line 43 to 44
(`all69`, `proposal64`, `requested64`, `original187`, `legacy161`,
`diagnosis53`, `on2026-10-21`, `at most25 words`) sit inside backtick code
spans, so check (a) excludes them by design. The file still fails on
`mined20` at line 73 and on five custody hits, so the required "expect hits"
outcome holds.

## Limits and risks

- The D1 regex is ASCII-lower-case only, exactly as the routed defect
  specifies (`\b[a-z]+[0-9]{2,}\b`); a glued token in capitals, such as
  `S041` or `C28`, is not matched by check (a). Such forms are covered only
  where they appear in the D2 vocabulary.
- Exclusions are token-shaped, not context-aware: a genuine prose typo such
  as `arm64` in running text is silently dropped. This is the trade the
  assignment asked for (the excluded forms must not be flagged).
- Code-span removal is regex based, so an unbalanced backtick in a file can
  swallow following prose. The two defect files and the fixtures are
  unaffected.
- The script is a lane-local tool under my seat directory, not a lane
  production path. The lane integrator decides whether it graduates to
  `tools/`.

## Files written

- `.ufo/waves/round-29/build/ExecProseCheck/prose-check.py` (the deliverable)
- `.ufo/waves/round-29/build/ExecProseCheck/clean-sample.md` (clean fixture)
- `.ufo/waves/round-29/build/ExecProseCheck/exclusions-sample.md` (exclusion fixture)
- `.ufo/waves/round-29/build/ExecProseCheck.md` (this report)

No other lane path was written. No git or jj command was run in the lane or
the fleet repo; the only repository command was the read-only
`git status --porcelain`, which showed only the untracked
`.ufo/waves/round-29/build/` tree.

## Tooling

No tool was installed or updated. The checker uses only the Python 3.14.8
standard library already present on the host, so no install was needed.
