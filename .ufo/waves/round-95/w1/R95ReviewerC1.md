# R95ReviewerC1 — correctness review of `tools/search-rerun.py` at carrier C `d27e9891`

Scope: read the tool whole (333 lines), read the fixture record
`corpus/fixtures/search-rerun-r95.md`, the battery
`corpus/evidence/round95/rerun-controls-r95.py`, `claims.md`/`claims.json`, and
`plans/round-95.md` first. Every probe below ran against a scratch clone at C
(`/fast/scratch/hyaku/chousa-r95/R95ReviewerC1/repo`) or fixture repos under
the same scratch dir; receipts are in `w1/R95ReviewerC1-*.txt`. The committed
battery was re-run once as baseline (`POSITIVE=1/1 … ORACLES_REJECTED=3/3`,
`RERUN_CONTROLS=PASS`, exit 0 — `R95ReviewerC1-battery-baseline.txt`), and the
predicate command prints `SEARCH_RERUN_SUMMARY searches=8 rev_match=8/8` +
`SEARCH_RERUN: CLEAN` exit 0 (`R95ReviewerC1-predicate1.txt`).

## Findings

### F1 (high) — Digest comparison crashes on non-UTF-8 filenames; exit "1", not the documented 0/1/2 contract
Docstring exit contract (lines 43–47): exit 0 = every search matches at rev;
1 = any COUNT_DRIFT/SET_DRIFT (or TREE_CHANGED under `--strict`); 2 = setup
`SEARCH_RERUN_ERROR …`. Command:
`python3 -B tools/search-rerun.py verify probes/nonutf8.md --root fixture-nonutf8`
(fixture: git repo with `corpus/captures/\xff\xfe.txt` containing the needle,
recorded hit_set as `sha256:` digest — `R95ReviewerC1-p04-nonutf8-digest-crash.txt`).
Observed: exit **1**, stderr is a raw traceback ending
`UnicodeEncodeError: 'utf-8' codec can't encode characters in position 38-39:
surrogates not allowed`, raised in `digest()` at line 275
(`sorted(paths)` decoded with `surrogateescape` in `files_at_rev`, then
`.encode("utf-8")` at line 275). Exit 1 is documented to mean "record drifts"
and exit 2 "setup"; a traceback is neither. Any majority-UTF-8 store with one
invalid-UTF-8 filename under a digest-row glob breaks the tool. `digest()` also
cannot match `LC_ALL=C sort | sha256sum` for such names even if it did not
crash: Python `sorted` on surrogateescape names orders `\x80` after `é`
(U+DC80 > U+00E9) while byte sort orders `\x80` before `é` (0x80 < 0xC3)
— `R95ReviewerC1-p06-digest-order.txt`. For valid UTF-8 (incl. `é`, `検索`)
the digest *does* equal the shell form (`R95ReviewerC1-digest-equiv.txt`,
MATCH), so this is a defect, not a general falsification of the digest claim.

### F2 (medium) — Q6: the recorded expression is not the expression as run; `\|` is load-bearing in two senses
`corpus/fixtures/search-rerun-r95.md` line 32 files regex
`[Ss]earch(es)? (was\|were) (run\|conducted)`, and the fixture's "As run"
section says expressions are "copied exactly as run" with
`/usr/bin/grep -l -P -e '<expression>'`. Commands (GNU grep 3.12, base
captures materialised at `7b237358`) — full receipt `R95ReviewerC1-q6-contrast.txt`:
- `grep -P -e '(was\|were)'` over a two-line file matches ONLY `Xwas|wereY`
  (PCRE: `\|` = literal pipe); `grep -P -e '(was|were)'` matches both.
- Over base capture `c52a1f15884a78028febcf43.txt`:
  `grep -c -P -e '[Ss]earch(es)? (was\|were) (run\|conducted)'` → **0**;
  with bare `|` → **1**. `grep -F 'was|were'` → no literal string exists.
- Over all base captures `grep -l -P` with bare `|` prints exactly the recorded
  hit_set (`c52a…`); with the filed backslashes it prints nothing.
So the recorded `hits=1`/hit_set is reproducible only from the *alternation*
reading, which is exactly what the tool's `\|`→`|` conversion (docstring line
29) silently re-creates. Whichever string grep actually received, the filed
bytes `(was\|were)` are **not** that string: either grep got `(was|were)` (the
record does not copy the run exactly) or grep got `(was\|were)` (then
`hits=1` is false "as run"). Neither reading falsifies the tool's own
C1 predicate (lines 17–21 of claims.md), but the fixture's "copied exactly as
run" wording, and any reading of `claims.md` C1 sentence that the tool
"re-runs each recorded expression" verbatim, says more than the instrument
enforces: for expressions containing `|` the filed form is a *grammar encoding*,
not the run bytes. Named limit (a) ("agreement measured on these 8 expressions
only") holds only under the unescaped reading.

### F3 (medium) — Rows after a blank line / a second table are silently ignored; verdict CLEAN
`parse_record` (lines 106–109) takes the maximal contiguous run of `|`-lines
after `## Searches`. Anything after a blank line or prose is never parsed.
Commands — `R95ReviewerC1-p19-silent-ignore.txt`:
- record with valid Q1 + blank line + a forged `Q9 … | 999 | - |` row →
  exit **0**, `SEARCH_RERUN: CLEAN`, `searches=1`.
- same forgery moved into a second full table further down the section →
  identical exit 0 / CLEAN.
The committed 8-search record has no such rows, so the C1 predicate is
unaffected; but the C1 sentence ("re-runs each recorded local search
expression") and the docstring ("holding one Markdown table … with exactly
these columns", line 19) overstate enforcement — a second table/missing-row
run is not a setup refusal (the docstring lists no error for it), and a reader
of a verdict CLEAN is told every recorded search matched when some recorded
rows were never run.

### F4 (low) — `hit_set` comma-separated list cannot represent a filename containing a comma
Fixture with `corpus/captures/a,b.txt` matching (`R95ReviewerC1-p16-comma-name.txt`):
truthful list form `…/a,b.txt` with `hits=1` → exit 1 `SET_DRIFT` (parser splits
into two bogus paths; count is fine, set comparison fails). The digest form
works (exit 0). No claimed sentence contradicts this (docstring says
"comma-separated matching paths" — commas are simply unrepresentable in list
form); worth a named limit alongside (e) the backtick limit.

### F5 (informational, no contradiction) — attacked items that hold
- Escaped `\|`: correct (cell `a\|b` searches literal `a|b`, `R95ReviewerC1-p02…`);
  bare `|` correctly refuses with `ROW width != 8` (exit 2).
- Backtick in expression cell → `EXPRESSION` refusal, exit 2 (named limit e holds).
- Trailing spaces on rows / header / extra-spaced header: accepted (cells are
  stripped). Separator rows: 2-dash and aligned variants pass; 1-dash refuses
  `TABLE`. Leading spaces before a row's `|` pass; trailing text after the final
  `|` refuses `ROW`. All consistent with the docstring's column-name contract.
- Headings: `## Searches` + trailing spaces passes (rstrip); `##  Searches`
  (double space) and `## Searches extra` refuse `SECTION` (exit 2). Matches
  "headed exactly".
- Table continuation: a row after a blank line ends the table (F3 above);
  a second table likewise ignored; duplicate `## Searches` sections refuse
  `SECTION`; header-only table refuses `TABLE`; CRLF / BOM documents parse.
- `hit_set` parsing: spaces after commas OK; unsorted lists OK (set comparison
  sorts); duplicates → `SET_DRIFT` exit 1 (set equality broken — correct);
  path outside the glob → `SET_DRIFT` exit 1; trailing comma → `HIT_SET`
  setup exit 2; `hits` vs set length mismatch → `COUNT_DRIFT` only
  (`R95ReviewerC1-p03`, `-p15`, `-p17`). Uppercase digest falls into the
  path-list branch and yields `SET_DRIFT`, never a false CLEAN. `hits=0`
  requires `-` and vice versa. Bad calendar dates (`2026-13-99`) pass the
  `DATE_RE` format check (docstring promises `YYYY-MM-DD` format only).
- `where` validator: rejects `.`, `//`, trailing `/`, Windows `\`, absolute,
  empty, trailing `.`; accepts `a..b` segments (segment-equality check), `**`,
  `a?`/bracket classes, `*.txt` at root, `**/*.txt`, `*/x`. `PurePosixPath`
  `**` semantics verified: spans zero-or-more segments (`**/*.txt` matches
  `a.txt`), `*` confined to one segment. Embedded `**` (`a**b`) behaves as
  `a*b` (no spanning) — docstring's "** spans segments" applies to whole-segment
  `**` only; no probe observed a mismatch.
- `static_dir` for first-segment wildcard returns `""`: `*.txt`, `**/*.txt`,
  `ab?/x.txt` all walk the root (`R95ReviewerC1-p07`); `corpus/*/x.txt` → `corpus`.
  `tree_files` excludes `.git`/`.jj` only at the root level — nested `.git` dirs
  would be walked; rev run never lists `route .git` (not in trees), benign.
- Same glob matching a directory: the directory is silently ignored on both
  sides (rev: `ls-tree -r` lists files only; tree: `os.walk` dirnames are not
  listed except symlinks) — `corpus/*` with matching files inside a subdir
  verifies CLEAN (`R95ReviewerC1-p18`). The docstring's exit-2 list mentions
  "symlink or non-regular file matched", so dirs match neither branch; no false
  CLEAN observed, but directory entries contribute to neither side.
- Untracked/ignored/deleted tree files: an untracked file matching the glob
  makes `at_tree > at_rev` → `TREE_CHANGED` (exit 0 non-strict, exit 1 strict,
  `R95ReviewerC1-p08`); a deleted tracked file likewise flips to `CHANGED`.
  This is exactly `claims.md` named limit (c) ("reads files on disk … tracked or
  not") and the docstring's own sentence (line 51).
- Symlinks: symlinked file matching a glob → `WHERE_TYPE` exit 2 (tree);
  tracked symlink blob at rev → `WHERE_TYPE` exit 2 (mode 120000); glob rooted
  under a symlinked dir → `WHERE_TYPE` exit 2 (`R95ReviewerC1-p10/p11`).
  A symlinked dir elsewhere under the static dir is not followed
  (`os.walk` default) and contributes nothing. Executable blobs (mode 100755)
  are searched normally (`R95ReviewerC1-p14`, exit 0).
- Exit codes: tree-`sha256:` handling is the only exit-1-without-`DRIFT`
  observed (F1); rev as blob/tree-sha → `REV` exit 2; argparse usage errors
  exit 2 without the `SEARCH_RERUN_ERROR` prefix (docstring describes exit 2
  as the setup format — usage errors are an unlisted subclass, harmless).
  ROOT that is not a git toplevel → `ROOT` exit 2. Record path and record
  symlink outside `--root` are read (the record is a caller-supplied input
  argument, not a search path; every *searched* path is confined by the `where`
  validator + symlink refusals, consistent with kill rule K3 as written
  against search reads).
- Expressions: single-char needles work; leading/trailing spaces inside backticks
  are preserved and change the hit set (verified) — "exactly as filed" holds
  post-unescaping, per the docstring's own `\|` rule.
- IDs `Q0`/`Q01`/`q1` refuse; `Q10` accepts — consistent with `Q[1-9][0-9]*`.
- Record digest = `sorted(paths)` UTF-8 + `\n` — equals
  `LC_ALL=C sort | sha256sum` for ASCII and for valid non-ASCII UTF-8
  (`R95ReviewerC1-digest-equiv.txt`); fails only for invalid-UTF-8 names (F1).

## Residual risk / verification gaps
- PCRE-vs-`re` agreement beyond the 8 recorded expressions was not probed
  (named limit a); F2 shows even *within* the 8, one expression's agreement
  depends on the `\|` unescaping rule.
- `WHERE_TYPE` rev-side fires before any hit computation; a tree containing a
  tracked symlink under a root-anchored glob (`**/*.txt` on this very lane
  trips over `.ufo/…/linkcap.txt` at rev) refuses rather than runs — by
  design, but it means the new tool's usable globs are narrower in practice
  than on a symlink-free store.
- No socket/write surface found in the tool (only `git ls-tree/cat-file`
  subprocesses + `open(...,"rb")` under `--root`, plus `open(record)`); K3 checks
  by probe were confined to the record argument and symlink refusals.

VERDICT: R95ReviewerC1 C1 fired — Q6's recorded hits=1 is reproducible only under the tool's \|→| reinterpretation, so "expression copied exactly as run" overstates, and the digest compare crashes (exit 1 traceback) on non-UTF-8 filenames instead of the documented 0/1/2 contract.
